"""Experiment X5: detecting and repairing under-retrieval (PREREG_X2_X5.md, section 5).

One job runs pgvector or Qdrant on one prepared corpus, for the layouts and builds it is given:

    python x5_mitigation.py --data data-e --store qdrant --layouts as-run,tenant --builds 0,1,2 --out out

Every arm is a PermissionedRetriever configuration over the same store, build and base search
settings (pgvector: relaxed_order, ef_search 100, the scan limits at their defaults; Qdrant:
hnsw_ef 128, no ACORN): `short_results` report, count, exact with max_exact_rows 1,000, 10,000
and None, widen, and the recall monitor at 1%; plus the store-native alternatives (pgvector's
raised tuple limit alone; Qdrant's ACORN alone; Qdrant's per-tenant layout). Pass 1 runs k = 5
and k = 10 for every pair; passes 2 and 3 repeat k = 10, timed. The backends are wrapped in a
recorder, so each row also holds what the retriever asked of the store (the first search and how
many hits it returned, the count, the search run again), from which the truly short first
searches and the detection rates are computed.
"""

from __future__ import annotations

import argparse
import random
import time
from dataclasses import dataclass, field
from typing import Any

import x2_frontiers as x2
import x2x5_common as xc
import x2x5_stores as xs
from x2x5_common import log

from wardowl import PermissionedRetriever


class Recorder:
    """A backend that does what `inner` does and records each call: [what, k or limit, result, ms]."""

    supports_filters = True

    def __init__(self, inner: Any, calls: list[list[Any]], tag: str) -> None:
        self.inner, self.calls, self.tag = inner, calls, tag

    @property
    def supports_exact(self) -> bool:
        return getattr(self.inner, "supports_exact", False) is True

    @property
    def exact_search(self) -> bool:
        return getattr(self.inner, "exact_search", False) is True

    def search(self, query: Any, k: int, filter: Any = None, **options: Any) -> list[Any]:
        started = time.perf_counter()
        hits = self.inner.search(query, k, filter, **options)
        what = f"{self.tag}-exact" if options.get("exact") else self.tag
        self.calls.append([what, k, len(hits), round((time.perf_counter() - started) * 1000, 3)])
        return hits

    def count(self, filter: Any, limit: int) -> int | None:
        started = time.perf_counter()
        found = self.inner.count(filter, limit)
        self.calls.append(["count", limit, found, round((time.perf_counter() - started) * 1000, 3)])
        return found


@dataclass(frozen=True)
class Arm:
    id: str
    short_results: str = "report"
    max_exact_rows: int | None = 10_000
    widen: bool = False
    sample_rate: float = 0.0
    base: dict[str, Any] = field(default_factory=dict)  # overrides of the base search settings
    layouts: tuple[str, ...] = ("default", "as-run")

    def describe(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "short_results": self.short_results,
            "max_exact_rows": self.max_exact_rows,
            "widen": self.widen,
            "recall_sample_rate": self.sample_rate,
            "base_overrides": self.base,
        }


LIBRARY_ARMS = (
    Arm("report"),
    Arm("count", "count"),
    Arm("exact-1k", "exact", 1_000),
    Arm("exact-10k", "exact", 10_000),
    Arm("exact-inf", "exact", None),
    Arm("widen", "widen", widen=True),
    Arm("monitor", sample_rate=0.01),
)
PG_BASE = {"iterative_scan": "relaxed_order", "ef_search": 100}
PG_WIDER = {**PG_BASE, "ef_search": 400, "max_scan_tuples": 1_000_000, "scan_mem_multiplier": 16}
QDRANT_BASE = {"hnsw_ef": 128}
QDRANT_WIDER = {"hnsw_ef": 512, "acorn": 1.0}
NATIVE = {
    "pgvector": Arm("native-scan1m", base={"max_scan_tuples": 1_000_000}),
    "qdrant": Arm("native-acorn", base={"acorn": 1.0}),
}


def arms_for(store: str, layout: str) -> list[Arm]:
    if layout == "tenant":
        return [Arm("native-tenant", layouts=("tenant",))]
    return [*LIBRARY_ARMS, NATIVE[store]]


def make_backend(store: xs.Store, params: dict[str, Any]) -> Any:
    if isinstance(store, xs.PgVector):
        return store.make(params)
    from wardowl.backends.qdrant import QdrantBackend

    return QdrantBackend(store.client, xs.NAME, None, search_params=xs.Qdrant.params(params))


def run_unit(job: x2.Job, corpus: xc.Corpus, deadline: xc.Deadline, layout: str, build: int, units_left: int) -> None:
    args = job.args
    unit: dict[str, Any] = {"layout": layout, "build": build, "settings": []}
    job.record["units"].append(unit)
    store = xs.make_store(args.store, corpus, layout, args.out / "work")
    base = PG_BASE if args.store == "pgvector" else QDRANT_BASE
    wider_params = PG_WIDER if args.store == "pgvector" else QDRANT_WIDER
    try:
        log(f"== {args.store} {layout} build {build}: loading {len(corpus):,} chunks")
        started = time.perf_counter()
        unit["load"] = store.load(build)
        unit["load"]["seconds"] = round(time.perf_counter() - started, 1)
        job.save()
        arms = arms_for(args.store, layout)
        pairs = store.pairs(corpus.pairs)
        for index, arm in enumerate(arms):
            budget = deadline.share((len(arms) - index) + units_left * len(LIBRARY_ARMS))
            entry: dict[str, Any] = {**arm.describe(), "budget_seconds": round(budget, 1)}
            unit["settings"].append(entry)
            label = f"{args.store} {layout} b{build} {arm.id}"
            if deadline.left() < 600 or budget < 30:
                entry["status"] = "skipped"
                job.record["skipped"].append({"what": label, "left_seconds": round(deadline.left())})
                job.save()
                continue
            log(f"-- {label}: {arm.describe()} (budget {budget / 60:.1f} min)")
            made: list[Any] = []
            try:
                calls: list[list[Any]] = []
                inner = make_backend(store, {**base, **arm.base})
                made.append(inner)
                wider = None
                if arm.widen:
                    wider_inner = make_backend(store, wider_params)
                    made.append(wider_inner)
                    wider = Recorder(wider_inner, calls, "wider")
                timer = xc.LastEvent()
                retriever = PermissionedRetriever(
                    Recorder(inner, calls, "search"),
                    corpus.authorizer,
                    observers=[timer],
                    short_results=arm.short_results,
                    max_exact_rows=arm.max_exact_rows,
                    wider=wider,
                    recall_sample_rate=arm.sample_rate,
                )

                def take(calls: list[list[Any]] = calls) -> list[list[Any]]:
                    found = list(calls)
                    calls.clear()
                    return found

                def reseed(p: int, arm_id: str = arm.id, layout: str = layout, build: int = build) -> None:
                    random.seed(f"x5-{arm_id}-{layout}-{build}-{p}")  # the monitor's sampler, the same every run

                entry["effective"] = store.effective(inner, xs.Setting(arm.id, "arm", {**base, **arm.base}))
                result = xc.sweep(
                    corpus,
                    retriever,
                    timer,
                    pairs,
                    label=label,
                    budget=budget,
                    deadline=deadline,
                    ks=(5, 10),
                    timed_k=10,
                    before_pass=reseed,
                    calls=take,
                )
                rows = x2.tag_rows(
                    result.rows,
                    exp="x5",
                    corpus=corpus.name,
                    store=args.store,
                    layout=layout,
                    build=build,
                    setting=arm.id,
                    job=args.label,
                )
                xc.write_jsonl_gz(x2.rows_path(args.out, args.store, layout, build, arm.id), rows)
                entry.update(status="done", sweep=result.info, summary=xc.summarize_rows(result.rows))
                log(f"   {label}: {entry['summary']}")
            except xc.LeakError:
                raise
            except Exception as error:
                entry["status"] = "failed"
                entry["error"] = f"{type(error).__name__}: {error}"
                job.fail(label, error)
            finally:
                for backend in made:
                    store.release(backend)
                job.save()
    finally:
        try:
            store.close()
        except Exception as error:
            log(f"   could not drop {args.store} {layout} build {build}: {type(error).__name__}: {error}")


def parse_args(argv: list[str] | None = None) -> Any:
    args = x2.parse_args(argv)
    if args.store not in ("pgvector", "qdrant"):
        raise SystemExit("X5 runs on pgvector and qdrant only")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    deadline = xc.Deadline(args.minutes)
    corpus = xc.load_corpus(args.data)
    job = x2.Job(args, "x5", corpus)
    units = [(layout, build) for layout in args.layouts for build in args.builds]
    status = "done"
    try:
        for index, (layout, build) in enumerate(units):
            if deadline.left() < 900:
                job.record["skipped"].append({"what": f"{layout} build {build}", "left_seconds": round(deadline.left())})
                continue
            try:
                run_unit(job, corpus, deadline, layout, build, len(units) - index - 1)
            except xc.LeakError:
                raise
            except Exception as error:
                job.fail(f"{args.store} {layout} build {build}", error)
    except xc.LeakError as leak:
        xc.write_json(args.out / "LEAK.json", leak.detail)
        job.record["leak"] = leak.detail
        log(f"A PERMISSION LEAK OR VIOLATION STOPPED THE JOB: {leak.detail}")
        status = "leak"
    if status == "done" and job.record["failures"]:
        status = "done with failures"
    job.finish(status)
    (args.out / "summary.md").write_text(x2.summary_markdown(job.record), encoding="utf-8")
    log(f"X5 {args.label}: {status}")
    return 3 if status == "leak" else 1 if job.record["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
