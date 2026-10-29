"""Experiment X2: recall against throughput under permission-shaped filters (PREREG_X2_X5.md).

One job runs one store on one prepared corpus, for the layouts and builds it is given:

    python x2_frontiers.py --data data-m --store qdrant --layouts as-run --builds 1 --out out --minutes 320

For each (layout, build) it loads the corpus into the store and runs every setting of
PREREG section 4 (exact settings on build 0 only) through wardowl's PermissionedRetriever: 20
warm-up retrievals, pass 1 over a balanced prefix of the round-robin pair order within 40% of the
setting's time budget, then passes 2 and 3 over the same prefix. Every hit is checked by wardowl's
re-check and by the corpus's own oracle; a leak stops the job (exit code 3, LEAK.json). Rows, one
per (setting, pair), go to <out>/rows/*.jsonl.gz; the job's record to <out>/job.json, and a
Markdown summary to <out>/summary.md.
"""

from __future__ import annotations

import argparse
import time
import traceback
from pathlib import Path
from typing import Any

import x2x5_common as xc
import x2x5_stores as xs
from x2x5_common import log

from wardowl import PermissionedRetriever

CLIENTS = (
    "psycopg", "psycopg-pool", "pgvector", "qdrant-client", "elasticsearch", "opensearch-py", "weaviate-client",
    "redis", "pymilvus", "pymongo", "lancedb", "pyarrow", "chromadb", "faiss-cpu",
)  # fmt: skip


class Job:
    """The job's record, rewritten after every setting so a crash keeps what finished."""

    def __init__(self, args: argparse.Namespace, experiment: str, corpus: xc.Corpus) -> None:
        self.args, self.out = args, args.out
        self.record: dict[str, Any] = {
            "experiment": experiment,
            "label": args.label,
            "corpus": corpus.describe(),
            "store": args.store,
            "layouts": args.layouts,
            "builds": args.builds,
            "minutes": args.minutes,
            "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "environment": xc.environment(CLIENTS),
            "units": [],
            "failures": [],
            "skipped": [],
            "status": "running",
        }
        self.save()

    def save(self) -> None:
        xc.write_json(self.out / "job.json", self.record)

    def fail(self, what: str, error: BaseException) -> None:
        trace = traceback.format_exc()
        log(trace)
        log(f"FAILED {what}: {type(error).__name__}: {error}")
        self.record["failures"].append({"what": what, "error": f"{type(error).__name__}: {error}", "trace": trace[-4000:]})
        self.save()

    def finish(self, status: str) -> None:
        self.record["status"] = status
        self.record["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.save()


def rows_path(out: Path, store: str, layout: str, build: int, setting: str) -> Path:
    return out / "rows" / f"{store}__{layout}__b{build}__{setting}.jsonl.gz"


def tag_rows(rows: list[dict[str, Any]], **fields: Any) -> list[dict[str, Any]]:
    return [{**fields, **row} for row in rows]


def run_unit(
    job: Job, corpus: xc.Corpus, deadline: xc.Deadline, layout: str, build: int, units_left: int
) -> None:
    """Loads one build of one layout and runs its settings."""
    args = job.args
    unit: dict[str, Any] = {"layout": layout, "build": build, "settings": []}
    job.record["units"].append(unit)
    store = xs.make_store(args.store, corpus, layout, args.out / "work")
    try:
        log(f"== {args.store} {layout} build {build}: loading {len(corpus):,} chunks")
        started = time.perf_counter()
        unit["load"] = store.load(build)
        unit["load"]["seconds"] = round(time.perf_counter() - started, 1)
        log(f"   loaded: {unit['load']}")
        job.save()
        settings = [s for s in store.settings() if build == 0 or not s.build0]
        pairs = store.pairs(corpus.pairs)
        for index, setting in enumerate(settings):
            parts = (len(settings) - index) + units_left * len(settings)
            budget = deadline.share(parts)
            entry: dict[str, Any] = {**setting.describe(), "budget_seconds": round(budget, 1)}
            unit["settings"].append(entry)
            label = f"{args.store} {layout} b{build} {setting.id}"
            if deadline.left() < 600 or budget < 30:
                entry["status"] = "skipped"
                job.record["skipped"].append({"what": label, "left_seconds": round(deadline.left())})
                log(f"-- {label}: skipped, {deadline.left() / 60:.0f} min left")
                job.save()
                continue
            log(f"-- {label}: {setting.params} (budget {budget / 60:.1f} min)")
            try:
                backend = store.backend(setting)
            except Exception as error:
                entry["status"] = "unsupported"
                entry["error"] = f"{type(error).__name__}: {error}"
                job.fail(f"{label}: making the backend", error)
                continue
            try:
                entry["effective"] = store.effective(backend, setting)
                before = store.counters()
                timer = xc.LastEvent()
                retriever = PermissionedRetriever(backend, corpus.authorizer, observers=[timer])
                plan = None
                if args.store == "pgvector":

                    def plan(pair: xc.Pair, k: int, backend: Any = backend) -> str:
                        return store.plan(backend, pair, k)

                result = xc.sweep(corpus, retriever, timer, pairs, label=label, budget=budget, deadline=deadline, plan=plan)
                after = store.counters()
                if before is not None and after is not None:
                    entry["qdrant_counters"] = {k: after.get(k, 0) - before.get(k, 0) for k in after}
                rows = tag_rows(
                    result.rows,
                    exp="x2",
                    corpus=corpus.name,
                    store=args.store,
                    layout=layout,
                    build=build,
                    setting=setting.id,
                    kind=setting.kind,
                    level=setting.level,
                    asrun=int(setting.asrun),
                    job=args.label,
                )
                xc.write_jsonl_gz(rows_path(args.out, args.store, layout, build, setting.id), rows)
                entry.update(status="done", sweep=result.info, summary=xc.summarize_rows(result.rows))
                log(f"   {label}: {entry['summary']}")
            except xc.LeakError:
                raise
            except Exception as error:
                entry["status"] = "failed"
                entry["error"] = f"{type(error).__name__}: {error}"
                job.fail(label, error)
            finally:
                store.release(backend)
                job.save()
    finally:
        try:
            store.close()
        except Exception as error:
            log(f"   could not drop {args.store} {layout} build {build}: {type(error).__name__}: {error}")


def summary_markdown(record: dict[str, Any]) -> str:
    lines = [
        f"### {record['experiment'].upper()} {record['label']} ({record['corpus']['name']}, {record['store']}): "
        f"{record['status']}",
        "",
    ]
    rows = []
    for unit in record["units"]:
        for s in unit["settings"]:
            summary = s.get("summary") or {}
            sweep = s.get("sweep") or {}
            rows.append(
                [
                    unit["layout"],
                    unit["build"],
                    s["id"],
                    s.get("status"),
                    sweep.get("pairs_run"),
                    sweep.get("passes"),
                    summary.get("recall10"),
                    summary.get("err10"),
                    summary.get("p50_ms"),
                    summary.get("qps"),
                ]
            )
    header = ["layout", "build", "setting", "status", "pairs", "passes", "recall@10", "empty", "p50 ms", "QPS"]
    lines += xc.markdown_table(header, rows)
    for unit in record["units"]:
        load = unit.get("load") or {}
        lines.append(f"- {unit['layout']} build {unit['build']}: loaded in {load.get('seconds')} s")
    for failure in record["failures"]:
        lines.append(f"- FAILED {failure['what']}: {failure['error']}")
    for skipped in record["skipped"]:
        lines.append(f"- skipped {skipped['what']}")
    if record.get("leak"):
        lines.append(f"- LEAK: {record['leak']}")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Experiment X2: recall against throughput")
    parser.add_argument("--data", type=Path, required=True, help="a folder x2x5_prepare.py wrote")
    parser.add_argument("--store", choices=sorted(xs.STORES), required=True)
    parser.add_argument("--layouts", default="default", help="comma-separated layouts of the store")
    parser.add_argument("--builds", default="0", help="comma-separated build numbers")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--label", default=None)
    parser.add_argument("--minutes", type=float, default=320.0, help="no setting starts after this many minutes")
    args = parser.parse_args(argv)
    args.layouts = [x.strip() for x in args.layouts.split(",") if x.strip()]
    args.builds = [int(x) for x in args.builds.split(",") if x.strip()]
    args.label = args.label or f"{args.store}-{'-'.join(args.layouts)}-b{'.'.join(map(str, args.builds))}"
    args.out.mkdir(parents=True, exist_ok=True)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    deadline = xc.Deadline(args.minutes)
    corpus = xc.load_corpus(args.data)
    job = Job(args, "x2", corpus)
    units = [(layout, build) for layout in args.layouts for build in args.builds]
    status = "done"
    try:
        for index, (layout, build) in enumerate(units):
            if deadline.left() < 900:
                job.record["skipped"].append({"what": f"{layout} build {build}", "left_seconds": round(deadline.left())})
                log(f"skipped {layout} build {build}: {deadline.left() / 60:.0f} min left")
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
    (args.out / "summary.md").write_text(summary_markdown(job.record), encoding="utf-8")
    log(f"X2 {args.label}: {status}")
    return 3 if status == "leak" else 1 if job.record["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
