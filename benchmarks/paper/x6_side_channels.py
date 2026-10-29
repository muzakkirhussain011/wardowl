"""Experiment X6: side channels of permission-aware retrieval, on one store.

    python x6_side_channels.py --store pgvector --data x6data --out results [--mode full|smoke]
        [--seeds 5] [--budget-minutes 330] [--group-deadline EPOCH] [--remaining N]

For each seed of the data job's plans (x6_data.py), with the design of PREREG_X3_X6.md and its
Amendment 1, it builds W1 (the background and every group's secrets) and SEP (the background only,
the attacker's tenant under per-tenant separation) once, then, group by group, W0_g (W1 with group g's
secrets replaced by far chunks). For every probe of the group, attacker (selectivity 1%, 10%, 50%)
and configuration, it runs one warm-up and the timed repetitions; each repetition queries the slots
W0 (W0_g), W1, SEPa and SEPb (SEP twice: the A/A null) in a fresh random order, through wardowl's
public retrieval API, and records what a caller observes (latency, hits, scores, count, `complete`)
and what explains it (widening rounds, candidates examined and denied, time in the store and the
authorizer). For pgvector it adds EXPLAIN ANALYZE for the first group's probes. Any hit outside the
attacker's readable set stops the run.

Writes <out>/x6-<store>.jsonl. The statistics are x6_stats.py's.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import x3x6_common as common
from x3x6_common import K, MAX_CANDIDATES, SECRET_META, SEED_BASE, log

SLOTS = ("W0", "W1", "SEPa", "SEPb")
WORLD = {"W0": "w0", "W1": "w1", "SEPa": "sep", "SEPb": "sep"}
CONFIGS: dict[str, tuple[str, ...]] = {
    "pgvector": ("pre", "pre-exact", "post", "post-const", "bm25-pre"),
    "qdrant": ("pre", "pre-exact", "post", "post-const", "bm25-pre"),
    "elasticsearch": ("pre", "pre-exact", "post", "post-const", "bm25-pre", "hybrid-pre", "hybrid-exact"),
    "faiss": ("pre", "post", "post-const"),
    "memory": ("pre", "post"),
}
KEYWORD_STORES = frozenset({"pgvector", "qdrant", "elasticsearch"})
MODES: dict[str, dict[str, Any]] = {
    # smoke: group 0 of each seed only, one timed repetition
    "full": {"reps": 5, "warmup": 1, "groups": None, "memory": {"probes": 3, "pcts": [10], "reps": 3}},
    "smoke": {"reps": 1, "warmup": 1, "groups": 1, "memory": {"probes": 1, "pcts": [10], "reps": 1}},
}
MAX_ERRORS_IN_A_ROW = 25  # a configuration failing this often in a row is stopped for the seed


class LastEvent:
    """An observer that keeps the retriever's last event (rounds and time in the store)."""

    def __init__(self) -> None:
        self.event: Any = None

    def __call__(self, event: Any) -> None:
        self.event = event


def make_retriever(config: str, built: common.Built) -> tuple[Any, LastEvent]:
    from wardowl import MetadataACLAuthorizer, PermissionedRetriever, RankFusion

    observer = LastEvent()
    extra: dict[str, Any] = {}
    backend: Any
    if config == "pre":
        backend, strategy = built.vector, "prefilter"
    elif config == "pre-exact":
        backend, strategy = built.exact, "prefilter"
    elif config == "post":
        backend, strategy = built.vector, "postfilter"
    elif config == "post-const":
        # Constant work: k * overfetch reaches the cap, so every retrieval fetches it in one round.
        backend, strategy = built.vector, "postfilter"
        extra["overfetch"] = max(2, -(-MAX_CANDIDATES // K))
    elif config == "bm25-pre":
        backend, strategy = built.keyword, "prefilter"
    elif config == "hybrid-pre":
        backend = RankFusion(built.vector, built.keyword) if built.keyword is not None else None
        strategy = "prefilter"
    elif config == "hybrid-exact":
        both = built.keyword is not None and built.exact is not None
        backend = RankFusion(built.exact, built.keyword) if both else None
        strategy = "prefilter"
    else:
        raise ValueError(f"unknown configuration {config!r}")
    if backend is None:
        raise ValueError(f"configuration {config!r} needs a backend this store did not build")
    retriever = PermissionedRetriever(
        backend,
        MetadataACLAuthorizer(),
        strategy=strategy,
        max_candidates=MAX_CANDIDATES,
        observers=[observer],
        **extra,
    )
    return retriever, observer


def measure(retriever: Any, observer: LastEvent, query: Any, subject: Any) -> dict[str, Any]:
    """One retrieval, timed around the public API call."""
    observer.event = None
    started = time.perf_counter()
    try:
        result = retriever.retrieve(query, subject, K)
    except Exception as error:
        latency = (time.perf_counter() - started) * 1000
        cause = error.__cause__
        return {
            "latency_ms": round(latency, 4),
            "error": common.short(error, 500),
            "cause": common.short(cause, 300) if cause is not None else None,
            "count": None,
            "complete": None,
            "ids": [],
            "scores": [],
        }
    latency = (time.perf_counter() - started) * 1000
    event = observer.event
    return {
        "latency_ms": round(latency, 4),
        "error": None,
        "count": len(result.hits),
        "complete": bool(result.complete),
        "examined": result.examined,
        "denied": result.denied,
        "violations": result.violations,
        "searches": getattr(event, "searches", None),
        "search_ms": getattr(event, "search_ms", None),
        "authorize_ms": getattr(event, "authorize_ms", None),
        "ids": [h.id for h in result.hits],
        "scores": [float(h.score) for h in result.hits],
    }


class Worlds:
    """The chunks of one seed in their insertion order, and the documents of each index.

    Every secret (a near passage of some probe) has a fixed position among the background, which
    every index keeps: W1 holds the secret there, W0_g its far chunk when the secret belongs to group
    g and the secret itself otherwise, and SEP holds the background alone, in the same order.
    """

    def __init__(self, plan: dict[str, Any], fiqa: common.Texts, scid: common.Texts, seed: int) -> None:
        from wardowl import Document

        self.fiqa = fiqa
        self.scid = scid
        n = len(fiqa.ids)
        buckets = plan["buckets"]
        if len(buckets) != n:
            raise ValueError(f"the plan has {len(buckets)} buckets for {n} passages")
        secret = np.zeros(n, dtype=bool)
        secret[np.asarray(plan["secret"], dtype=np.int64)] = True
        rng = np.random.default_rng([SEED_BASE, seed, 101])
        background = np.flatnonzero(~secret)
        background = background[rng.permutation(len(background))]
        secrets = np.flatnonzero(secret)
        secrets = secrets[rng.permutation(len(secrets))]
        total = len(background) + len(secrets)
        is_secret = np.zeros(total, dtype=bool)
        is_secret[rng.choice(total, size=len(secrets), replace=False)] = True
        rest, hidden = iter(background), iter(secrets)
        self.order = [(bool(s), int(next(hidden)) if s else int(next(rest))) for s in is_secret]

        def secret_metadata() -> dict[str, list[str]]:
            return {key: list(values) for key, values in SECRET_META.items()}

        self.background_doc = {}
        for i in background:
            b = buckets[int(i)]
            metadata = {"allowed_users": [f"owner{b:02d}"], "allowed_groups": [f"g{b:02d}"]}
            self.background_doc[int(i)] = Document(fiqa.ids[int(i)], fiqa.texts[int(i)], metadata)
        self.secret_doc = {int(d): Document(fiqa.ids[int(d)], fiqa.texts[int(d)], secret_metadata()) for d in secrets}
        # A secret may belong to several groups (Amendment 2): it is replaced in each of their W0.
        self.groups_of: dict[int, set[int]] = {}
        for group in plan["groups"]:
            for near in group["secrets"]:
                self.groups_of.setdefault(int(near), set()).add(int(group["group"]))
        self.far_doc: dict[int, Any] = {}
        self.far_source: dict[int, int] = {}
        for number, (near, source, n_tokens) in enumerate(plan["far"], 1):
            text = common.far_text(scid.texts, source, n_tokens)
            self.far_doc[near] = Document(f"far-{number}-{scid.ids[source]}", text, secret_metadata())
            self.far_source[near] = source
        missing = set(self.secret_doc) - (set(self.far_doc) & set(self.groups_of))
        if missing:
            raise ValueError(f"{len(missing)} secrets have no far chunk or no group")
        self.readable = {
            pct: {fiqa.ids[int(i)] for i in background if buckets[int(i)] < pct} for pct in plan["pcts"]
        }

    def index(self, world: str, group: int | None = None) -> tuple[list[Any], np.ndarray]:
        docs: list[Any] = []
        rows: list[np.ndarray] = []
        for hidden, i in self.order:
            if not hidden:
                docs.append(self.background_doc[i])
                rows.append(self.fiqa.vectors[i])
            elif world == "sep":
                continue
            elif world == "w0" and group in self.groups_of[i]:
                docs.append(self.far_doc[i])
                rows.append(self.scid.vectors[self.far_source[i]])
            else:
                docs.append(self.secret_doc[i])
                rows.append(self.fiqa.vectors[i])
        return docs, np.stack(rows).astype(np.float32)


def chosen_probes(plan: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    """The probes this run measures: every group's (full), group 0's (smoke), or, for the in-memory
    control, the first probes of each level in group order (its reduced design)."""
    settings = MODES[args.mode]
    probes = sorted(plan["probes"], key=lambda p: (p["group"], -p["level"], p["qindex"]))
    if args.store == "memory":
        limit = settings["memory"]["probes"]
        kept: list[dict[str, Any]] = []
        for probe in probes:
            if sum(1 for p in kept if p["level"] == probe["level"]) < limit:
                kept.append(probe)
        return kept
    if settings["groups"] is not None:
        groups = sorted({p["group"] for p in probes})[: settings["groups"]]
        return [p for p in probes if p["group"] in groups]
    return probes


def build(
    target: common.Target, args: argparse.Namespace, worlds: Worlds, world: str, seed: int, group: int | None,
    records: common.Records,
) -> common.Built:  # fmt: skip
    docs, vectors = worlds.index(world, group)
    clock = time.monotonic()
    label = world if group is None else f"{world} group {group}"
    log(f"  seed {seed}: building {label} ({len(docs):,} chunks)")
    name = common.unique_base(f"x6s{seed}{world}" + ("" if group is None else f"g{group}"))
    built = target.build(name, docs, vectors, keyword=args.store in KEYWORD_STORES)
    seconds = round(time.monotonic() - clock, 1)
    record = {"type": "build", "seed": seed, "world": world, "group": group, "docs": len(docs), "seconds": seconds}
    records.write({**record, "info": built.info})
    log(f"  seed {seed}: {label} built in {seconds:.0f} s {built.info}")
    return built


def play_seed(
    seed: int,
    args: argparse.Namespace,
    target: common.Target,
    data: Path,
    fiqa: common.Texts,
    queries: common.Texts,
    scid: common.Texts,
    records: common.Records,
    hard_deadline: float,
) -> dict[str, Any]:
    from wardowl import MetadataACLAuthorizer, Query, Subject

    settings = MODES[args.mode]
    plan = json.loads(common.plan_path(data, seed).read_text(encoding="utf-8"))
    worlds = Worlds(plan, fiqa, scid, seed)
    probes = chosen_probes(plan, args)
    pcts: list[int] = list(plan["pcts"])
    reps, warmup = settings["reps"], settings["warmup"]
    if args.store == "memory":
        pcts = [p for p in settings["memory"]["pcts"] if p in pcts]
        reps = settings["memory"]["reps"]
    groups = sorted({p["group"] for p in probes})
    configs = CONFIGS[args.store]
    records.write(
        {
            "type": "seed-start",
            "seed": seed,
            "probes": len(probes),
            "groups": groups,
            "levels": {str(m): sum(1 for p in probes if p["level"] == m) for m in sorted({p["level"] for p in probes})},
            "pcts": pcts,
            "configs": list(configs),
            "reps": reps,
            "warmup": warmup,
            "notes": plan.get("notes"),
        }
    )
    subjects = {pct: Subject(f"attacker-p{pct:02d}", [f"g{i:02d}" for i in range(pct)]) for pct in pcts}
    query_of = {
        p["qindex"]: Query(text=queries.texts[p["qindex"]], vector=queries.vectors[p["qindex"]]) for p in probes
    }
    rng = np.random.default_rng([SEED_BASE, seed, 202])
    live: dict[str, common.Built] = {}
    retrievers: dict[str, dict[str, tuple[Any, LastEvent]]] = {}
    in_a_row = dict.fromkeys(configs, 0)
    first_error: dict[str, str] = {}
    disabled: set[str] = set()
    total = len(probes) * len(pcts) * len(configs) * (warmup + reps) * len(SLOTS)
    done = 0
    clock = shown = time.monotonic()
    outcome: dict[str, Any] = {"seed": seed, "complete": False}
    try:
        for world in ("w1", "sep"):
            live[world] = build(target, args, worlds, world, seed, None, records)
            retrievers[world] = {config: make_retriever(config, live[world]) for config in configs}
        for group in groups:
            live["w0"] = build(target, args, worlds, "w0", seed, group, records)
            retrievers["w0"] = {config: make_retriever(config, live["w0"]) for config in configs}
            members = [p for p in probes if p["group"] == group]
            for index in rng.permutation(len(members)):
                probe = members[int(index)]
                q = probe["qindex"]
                query = query_of[q]
                for pct in pcts:
                    subject = subjects[pct]
                    reference = plan["exact"][str(q)][str(pct)]
                    tstar = {fiqa.ids[i] for i in reference["tstar"]}
                    size = int(reference["R"])
                    allowed = worlds.readable[pct]
                    for config in configs:
                        for rep in range(warmup + reps):
                            if config in disabled:
                                break
                            if time.time() > hard_deadline:
                                raise TimeoutError("the job's hard deadline passed during the seed")
                            for slot in rng.permutation(SLOTS):
                                retriever, observer = retrievers[WORLD[str(slot)]][config]
                                observed = measure(retriever, observer, query, subject)
                                done += 1
                                leaked = [i for i in observed["ids"] if i not in allowed]
                                if leaked:
                                    records.write({"type": "leak", "seed": seed, "probe": q, "pct": pct,
                                                   "config": config, "slot": str(slot), "ids": leaked})  # fmt: skip
                                    common.annotate("error", f"x6 {args.store} leak", f"{config} {slot}: {leaked}")
                                    raise SystemExit(3)
                                recall = None
                                if observed["error"] is None and size > 0:
                                    recall = len(set(observed["ids"]) & tstar) / min(K, size)
                                records.write(
                                    {
                                        "type": "retrieval",
                                        "seed": seed,
                                        "group": group,
                                        "probe": q,
                                        "level": probe["level"],
                                        "pct": pct,
                                        "config": config,
                                        "slot": str(slot),
                                        "rep": rep,
                                        "warmup": rep < warmup,
                                        "R": size,
                                        "recall": recall,
                                        **observed,
                                    }
                                )
                                if observed["error"] is None:
                                    in_a_row[config] = 0
                                    continue
                                in_a_row[config] += 1
                                first_error.setdefault(config, observed["error"])
                                if in_a_row[config] >= MAX_ERRORS_IN_A_ROW and config not in disabled:
                                    disabled.add(config)
                                    records.write({"type": "config-stopped", "seed": seed, "config": config,
                                                   "error": observed["error"]})  # fmt: skip
                                    log(f"  seed {seed}: {config} stopped after {in_a_row[config]} errors in a row")
                    if time.monotonic() - shown > 60:
                        shown = time.monotonic()
                        rate = done / max(1e-9, shown - clock)
                        left = (total - done) / max(rate, 1e-9) / 60
                        log(f"  seed {seed}: {done:,}/{total:,} retrievals ({rate:.1f} per s, {left:.0f} min left)")
            if args.store == "pgvector" and group == groups[0]:
                explain(seed, target, live, members, pcts, subjects, query_of, records, MetadataACLAuthorizer())
            target.drop(live.pop("w0"))
        outcome.update(complete=True, retrievals=done, disabled=sorted(disabled), first_error=first_error)
        return outcome
    finally:
        for world, index in live.items():
            try:
                target.drop(index)
            except Exception as error:
                log(f"  seed {seed}: dropping {world} failed: {common.short(error, 200)}")


def explain(
    seed: int,
    target: Any,
    live: dict[str, common.Built],
    probes: list[dict[str, Any]],
    pcts: list[int],
    subjects: dict[int, Any],
    query_of: dict[int, Any],
    records: common.Records,
    authorizer: Any,
) -> None:
    """pgvector's plans for the first probe of each level of a group, in W0 and W1, for the pre-filters."""
    firsts: dict[int, dict[str, Any]] = {}
    for probe in probes:
        firsts.setdefault(probe["level"], probe)
    for level, probe in sorted(firsts.items()):
        for pct in pcts:
            f = authorizer.filter_for(subjects[pct])
            for world in ("w0", "w1"):
                index = live[world]
                for config, backend in (("pre", index.vector), ("pre-exact", index.exact), ("bm25-pre", index.keyword)):
                    if backend is None:
                        continue
                    record: dict[str, Any] = {"type": "explain", "seed": seed, "group": probe["group"],
                                              "probe": probe["qindex"], "level": level, "pct": pct, "world": world,
                                              "config": config}  # fmt: skip
                    try:
                        record["plan"] = target.explain(backend, query_of[probe["qindex"]], K, f)
                    except Exception as error:
                        record["error"] = common.short(error, 500)
                    records.write(record)


def run(args: argparse.Namespace) -> int:
    data = Path(args.data)
    out = Path(args.out)
    base = {"exp": "x6", "store": args.store, "mode": args.mode, "run": common.RUN_ID}
    records = common.Records(out / f"x6-{args.store}.jsonl", base)
    if args.store not in CONFIGS:
        raise SystemExit(f"X6 runs on {sorted(CONFIGS)}, not {args.store!r}")
    if not common.data_ready(data):
        records.write({"type": "setup-error", "error": f"the data job's files are missing from {data}"})
        common.annotate("error", f"x6 {args.store}", f"the data job's files are missing from {data}")
        return 2
    deadline = common.deadline_for(args.budget_minutes, args.group_deadline, args.remaining)
    hard_deadline = (args.group_deadline + 600) if args.group_deadline else deadline + 1800
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    log(f"x6 {args.store}: loading the data")
    fiqa = common.Texts(data, "fiqa_corpus")
    queries = common.Texts(data, "fiqa_queries")
    scid = common.Texts(data, "scidocs_subset")
    seeds = [s for s in common.seed_list(args.seeds, args.seed_list) if common.plan_path(data, s).is_file()]
    keep = ("mode", "embedding", "sources", "counts", "design", "hubs", "versions", "from_cache")
    records.write(
        {
            "type": "start",
            "args": vars(args),
            "settings": MODES[args.mode],
            "configs": list(CONFIGS[args.store]),
            "seeds": seeds,
            "data": {key: manifest.get(key) for key in keep},
            "host": common.host(),
            "deadline": deadline,
        }
    )
    target = common.make_target(args.store)
    try:
        attempts = common.connect(target)
    except Exception as error:
        versions = common.target_versions(target, reachable=False)
        records.write({"type": "setup-error", "error": common.short(error, 1000), "versions": versions})
        common.annotate("error", f"x6 {args.store} setup", common.short(error, 1000))
        return 1
    records.write({"type": "versions", "attempts": attempts, **common.target_versions(target, reachable=True)})
    durations: list[float] = []
    outcomes: list[dict[str, Any]] = []
    status = 0
    try:
        for seed in seeds:
            if durations and time.time() + 1.2 * max(durations) > deadline:
                records.write({"type": "seed-skipped", "seed": seed, "reason": "not enough time left in the budget"})
                common.annotate("warning", f"x6 {args.store}", f"seed {seed} skipped: not enough time left")
                continue
            started = time.time()
            log(f"x6 {args.store}: seed {seed}")
            try:
                outcome = play_seed(seed, args, target, data, fiqa, queries, scid, records, hard_deadline)
            except TimeoutError as error:
                records.write({"type": "seed-aborted", "seed": seed, "error": common.short(error)})
                status = 4
                break
            outcome["seconds"] = round(time.time() - started, 1)
            durations.append(time.time() - started)
            outcomes.append(outcome)
            records.write({"type": "seed-end", **outcome})
            log(f"x6 {args.store}: seed {seed} done in {outcome['seconds'] / 60:.1f} min")
    finally:
        target.close()
        records.write({"type": "end", "outcomes": outcomes, "status": status})
        records.close()
    problems = {o["seed"]: o.get("first_error") for o in outcomes if o.get("first_error")}
    summary = {
        "seeds": [o["seed"] for o in outcomes if o.get("complete")],
        "minutes": [round(o.get("seconds", 0) / 60, 1) for o in outcomes],
        "retrievals": [o.get("retrievals") for o in outcomes],
        "stopped": {o["seed"]: o.get("disabled") for o in outcomes if o.get("disabled")},
        "first_errors": problems,
    }
    common.annotate("warning" if problems or status else "notice", f"x6 {args.store}", json.dumps(summary, default=str))
    return status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--store", required=True)
    parser.add_argument("--data", default="x6data")
    parser.add_argument("--out", default="results")
    parser.add_argument("--mode", choices=sorted(MODES), default="full")
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--budget-minutes", type=float, default=330)
    parser.add_argument("--group-deadline", type=float, default=0)
    parser.add_argument("--remaining", type=int, default=1)
    parser.add_argument("--seed-list", default="", help='the seeds this job runs, such as "0-2" (default: all)')
    args = parser.parse_args(argv)
    try:
        return run(args)
    except BaseException as error:
        if not isinstance(error, SystemExit):
            common.fail_loudly(f"x6 {args.store}", error)
        raise


if __name__ == "__main__":
    sys.exit(main())
