"""X6 follow-up, exploratory (PREREG_X3_X6.md, amendment 4, part B, items 2 and 5): a cross-build A/A.

    python x6_crossbuild.py --store faiss --data x6data --out results [--mode full|smoke]
        [--seeds 5] [--budget-minutes 330] [--group-deadline EPOCH] [--remaining N]

The run that this follows (40940385704) found latency offsets between W1 and W0_g that did not depend
on m, in configurations whose answers were identical in both worlds. Its A/A guard measured one index
twice and could not tell whether two builds differ. This script plays the main run's game again on
the same plans, with the same probes, attackers, warm-up and repetitions, for FAISS (`pre`, `post`)
and for pgvector, Qdrant and Elasticsearch (`pre-exact`), with other slots:

* W1 and SEP are built at the start of each seed, as in the main run (SEP is kept, not measured);
* for each group g, W1r (W1 again), W0a and W0b (W0_g twice) are built in a seeded random order, W0a
  being the first W0 built;
* each repetition queries W1, W1r, W0a and W0b in a fresh random order.

For pgvector it also records, for each of the four tables before and after each group is measured,
the pages, all-visible pages, live and dead tuples and vacuum history, and EXPLAIN (ANALYZE, BUFFERS)
of `pre-exact` on the four tables for the first probe of each level of each seed's first group.

Writes <out>/x6cb-<store>.jsonl, in the main run's record format (slot names as above). The readings
are x3x6_followup.py's; none of them changes a verdict of the design.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import x3x6_common as common
import x6_side_channels as x6
from x3x6_common import K, SEED_BASE, log

SLOTS = ("W1", "W1r", "W0a", "W0b")
CONFIGS: dict[str, tuple[str, ...]] = {
    "faiss": ("pre", "post"),
    "pgvector": ("pre-exact",),
    "qdrant": ("pre-exact",),
    "elasticsearch": ("pre-exact",),
}
PLAN_KEYS = (
    "Node Type",
    "Index Name",
    "Relation Name",
    "Actual Rows",
    "Actual Loops",
    "Actual Total Time",
    "Rows Removed by Filter",
    "Rows Removed by Index Recheck",
    "Exact Heap Blocks",
    "Lossy Heap Blocks",
    "Heap Fetches",
    "Shared Hit Blocks",
    "Shared Read Blocks",
    "Shared Dirtied Blocks",
    "Shared Written Blocks",
    "Workers Planned",
    "Workers Launched",
    "Sort Method",
)


def plan_nodes(node: dict[str, Any], depth: int = 0) -> list[dict[str, Any]]:
    found = [{"depth": depth, **{key: node[key] for key in PLAN_KEYS if key in node}}]
    for child in node.get("Plans", []) or []:
        found += plan_nodes(child, depth + 1)
    return found


def explain_buffers(backend: Any, query: Any, f: Any) -> dict[str, Any]:
    """EXPLAIN (ANALYZE, BUFFERS) of the statement the backend's search runs, in its settings."""
    from psycopg import sql

    from wardowl.types import Query

    q = Query.of(query)
    statement, params = backend._statement(q, backend._query_vector(q), K, f)
    with backend.pool.connection() as conn, conn.transaction():
        for setting in backend._settings():
            conn.execute(setting)
        row = conn.execute(sql.SQL("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ") + statement, params).fetchone()
    document = row[0]
    if isinstance(document, str):
        document = json.loads(document)
    top = document[0]
    return {
        "nodes": plan_nodes(top["Plan"]),
        "planning_ms": top.get("Planning Time"),
        "execution_ms": top.get("Execution Time"),
    }


def table_state(target: Any, name: str) -> dict[str, Any]:
    """What PostgreSQL knows about one table's pages and vacuum history, now."""
    state: dict[str, Any] = {"table": name}
    with target.pool.connection() as conn:
        row = conn.execute(
            "SELECT relpages, relallvisible, reltuples FROM pg_class WHERE oid = to_regclass(quote_ident(%s))",
            (name,),
        ).fetchone()
        if row is not None:
            state.update(relpages=row[0], relallvisible=row[1], reltuples=row[2])
        row = conn.execute(
            "SELECT n_live_tup, n_dead_tup, n_ins_since_vacuum, last_vacuum, last_autovacuum, last_analyze,"
            " last_autoanalyze, vacuum_count, autovacuum_count, analyze_count, autoanalyze_count, now()"
            " FROM pg_stat_user_tables WHERE relid = to_regclass(quote_ident(%s))",
            (name,),
        ).fetchone()
        if row is not None:
            keys = ("n_live_tup", "n_dead_tup", "n_ins_since_vacuum", "last_vacuum", "last_autovacuum",
                    "last_analyze", "last_autoanalyze", "vacuum_count", "autovacuum_count", "analyze_count",
                    "autoanalyze_count", "now")  # fmt: skip
            state.update({key: (str(value) if value is not None and key.startswith(("last", "now")) else value)
                          for key, value in zip(keys, row, strict=True)})  # fmt: skip
        try:
            with conn.transaction():
                row = conn.execute(
                    "SELECT all_visible, all_frozen FROM pg_visibility_map_summary(to_regclass(quote_ident(%s)))",
                    (name,),
                ).fetchone()
            if row is not None:
                state.update(vm_all_visible=row[0], vm_all_frozen=row[1])
        except Exception as error:
            state["vm_error"] = common.short(error, 200)
    return state


def prepare(target: Any, records: common.Records) -> None:
    """pgvector only: the visibility-map extension, if the image has it (contrib)."""
    if getattr(target, "name", None) != "pgvector":
        return
    try:
        with target.pool.connection() as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS pg_visibility")
        records.write({"type": "extension", "name": "pg_visibility", "ok": True})
    except Exception as error:
        records.write({"type": "extension", "name": "pg_visibility", "ok": False, "error": common.short(error, 300)})


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

    settings = x6.MODES[args.mode]
    plan = json.loads(common.plan_path(data, seed).read_text(encoding="utf-8"))
    worlds = x6.Worlds(plan, fiqa, scid, seed)
    probes = x6.chosen_probes(plan, args)
    pcts: list[int] = list(plan["pcts"])
    reps, warmup = settings["reps"], settings["warmup"]
    groups = sorted({p["group"] for p in probes})
    configs = CONFIGS[args.store]
    records.write({"type": "seed-start", "seed": seed, "probes": len(probes), "groups": groups, "pcts": pcts,
                   "configs": list(configs), "reps": reps, "warmup": warmup, "slots": list(SLOTS)})  # fmt: skip
    subjects = {pct: Subject(f"attacker-p{pct:02d}", [f"g{i:02d}" for i in range(pct)]) for pct in pcts}
    query_of = {
        p["qindex"]: Query(text=queries.texts[p["qindex"]], vector=queries.vectors[p["qindex"]]) for p in probes
    }
    authorizer = MetadataACLAuthorizer()
    rng = np.random.default_rng([SEED_BASE, seed, 404])  # measurement order (the main run used 202)
    order_rng = np.random.default_rng([SEED_BASE, seed, 405])  # build order within each group
    live: dict[str, common.Built] = {}
    retrievers: dict[str, dict[str, tuple[Any, x6.LastEvent]]] = {}
    done = 0
    try:
        for world in ("w1", "sep"):
            live[world] = x6.build(target, args, worlds, world, seed, None, records)
        retrievers["W1"] = {config: x6.make_retriever(config, live["w1"]) for config in configs}
        for group in groups:
            position = int(order_rng.integers(0, 3))  # where W1r falls among the three builds
            sequence = ["w0", "w0"]
            sequence.insert(position, "w1")
            named: list[tuple[str, str]] = []
            w0_seen = 0
            for world in sequence:
                if world == "w1":
                    named.append(("W1r", world))
                else:
                    named.append(("W0a" if w0_seen == 0 else "W0b", world))
                    w0_seen += 1
            for number, (slot, world) in enumerate(named):
                clock = time.time()
                live[slot] = x6.build(target, args, worlds, world, seed, group, records)
                retrievers[slot] = {config: x6.make_retriever(config, live[slot]) for config in configs}
                records.write({"type": "slot-build", "seed": seed, "group": group, "slot": slot, "world": world,
                               "position": number, "name": live[slot].name, "finished": time.time(),
                               "seconds": round(time.time() - clock, 1)})  # fmt: skip
            tables = {"W1": live["w1"].name, **{slot: live[slot].name for slot, _ in named}}
            if args.store == "pgvector":
                for slot, name in tables.items():
                    records.write({"type": "table-state", "seed": seed, "group": group, "phase": "before",
                                   "slot": slot, **table_state(target, name)})  # fmt: skip
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
                            if time.time() > hard_deadline:
                                raise TimeoutError("the job's hard deadline passed during the seed")
                            for slot in rng.permutation(SLOTS):
                                retriever, observer = retrievers[str(slot)][config]
                                observed = x6.measure(retriever, observer, query, subject)
                                done += 1
                                leaked = [i for i in observed["ids"] if i not in allowed]
                                if leaked:
                                    records.write({"type": "leak", "seed": seed, "probe": q, "pct": pct,
                                                   "config": config, "slot": str(slot), "ids": leaked})  # fmt: skip
                                    common.annotate("error", f"x6cb {args.store} leak", f"{config} {slot}: {leaked}")
                                    raise SystemExit(3)
                                recall = None
                                if observed["error"] is None and size > 0:
                                    recall = len(set(observed["ids"]) & tstar) / min(K, size)
                                records.write({"type": "retrieval", "seed": seed, "group": group, "probe": q,
                                               "level": probe["level"], "pct": pct, "config": config,
                                               "slot": str(slot), "rep": rep, "warmup": rep < warmup, "R": size,
                                               "recall": recall, **observed})  # fmt: skip
            if args.store == "pgvector":
                for slot, name in tables.items():
                    records.write({"type": "table-state", "seed": seed, "group": group, "phase": "after",
                                   "slot": slot, **table_state(target, name)})  # fmt: skip
                if group == groups[0]:
                    explain_group(seed, live, tables, members, pcts, subjects, query_of, authorizer, records)
            for slot, _ in named:
                retrievers.pop(slot, None)
                target.drop(live.pop(slot))
            log(f"  seed {seed}: group {group} done, {done:,} retrievals")
        return {"seed": seed, "complete": True, "retrievals": done}
    finally:
        for name, index in live.items():
            try:
                target.drop(index)
            except Exception as error:
                log(f"  seed {seed}: dropping {name} failed: {common.short(error, 200)}")


def explain_group(
    seed: int,
    live: dict[str, common.Built],
    tables: dict[str, str],
    members: list[dict[str, Any]],
    pcts: list[int],
    subjects: dict[int, Any],
    query_of: dict[int, Any],
    authorizer: Any,
    records: common.Records,
) -> None:
    """EXPLAIN (ANALYZE, BUFFERS) of pre-exact for the first probe of each level, on the four tables."""
    firsts: dict[int, dict[str, Any]] = {}
    for probe in members:
        firsts.setdefault(probe["level"], probe)
    indexes = {"W1": live["w1"], **{slot: live[slot] for slot in tables if slot != "W1"}}
    for level, probe in sorted(firsts.items()):
        for pct in pcts:
            f = authorizer.filter_for(subjects[pct])
            for slot, index in indexes.items():
                record: dict[str, Any] = {"type": "explain", "seed": seed, "group": probe["group"],
                                          "probe": probe["qindex"], "level": level, "pct": pct, "slot": slot,
                                          "table": tables[slot], "config": "pre-exact"}  # fmt: skip
                try:
                    record["plan"] = explain_buffers(index.exact, query_of[probe["qindex"]], f)
                except Exception as error:
                    record["error"] = common.short(error, 500)
                records.write(record)


def run(args: argparse.Namespace) -> int:
    data = Path(args.data)
    out = Path(args.out)
    base = {"exp": "x6cb", "store": args.store, "mode": args.mode, "run": common.RUN_ID}
    records = common.Records(out / f"x6cb-{args.store}.jsonl", base)
    if args.store not in CONFIGS:
        raise SystemExit(f"the cross-build A/A runs on {sorted(CONFIGS)}, not {args.store!r}")
    if not common.data_ready(data):
        records.write({"type": "setup-error", "error": f"the data files are missing from {data}"})
        common.annotate("error", f"x6cb {args.store}", f"the data files are missing from {data}")
        return 2
    deadline = common.deadline_for(args.budget_minutes, args.group_deadline, args.remaining)
    hard_deadline = (args.group_deadline + 600) if args.group_deadline else deadline + 1800
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    log(f"x6cb {args.store}: loading the data")
    fiqa = common.Texts(data, "fiqa_corpus")
    queries = common.Texts(data, "fiqa_queries")
    scid = common.Texts(data, "scidocs_subset")
    seeds = [s for s in common.seed_list(args.seeds, args.seed_list) if common.plan_path(data, s).is_file()]
    if args.mode == "smoke":
        seeds = seeds[:1]
    records.write({"type": "start", "args": vars(args), "settings": x6.MODES[args.mode],
                   "configs": list(CONFIGS[args.store]), "slots": list(SLOTS), "seeds": seeds,
                   "data": {key: manifest.get(key) for key in ("embedding", "counts", "design", "hubs")},
                   "host": common.host(), "deadline": deadline})  # fmt: skip
    target = common.make_target(args.store)
    try:
        attempts = common.connect(target)
    except Exception as error:
        versions = common.target_versions(target, reachable=False)
        records.write({"type": "setup-error", "error": common.short(error, 1000), "versions": versions})
        common.annotate("error", f"x6cb {args.store} setup", common.short(error, 1000))
        return 1
    records.write({"type": "versions", "attempts": attempts, **common.target_versions(target, reachable=True)})
    prepare(target, records)
    durations: list[float] = []
    status = 0
    finished: list[int] = []
    try:
        for seed in seeds:
            if durations and time.time() + 1.2 * max(durations) > deadline:
                records.write({"type": "seed-skipped", "seed": seed, "reason": "not enough time left in the budget"})
                common.annotate("warning", f"x6cb {args.store}", f"seed {seed} skipped: not enough time left")
                continue
            started = time.time()
            log(f"x6cb {args.store}: seed {seed}")
            try:
                outcome = play_seed(seed, args, target, data, fiqa, queries, scid, records, hard_deadline)
            except TimeoutError as error:
                records.write({"type": "seed-aborted", "seed": seed, "error": common.short(error)})
                status = 4
                break
            outcome["seconds"] = round(time.time() - started, 1)
            durations.append(time.time() - started)
            finished.append(seed)
            records.write({"type": "seed-end", **outcome})
            log(f"x6cb {args.store}: seed {seed} done in {outcome['seconds'] / 60:.1f} min")
    finally:
        with contextlib.suppress(Exception):
            target.close()
        records.write({"type": "end", "seeds": finished, "status": status})
        records.close()
    common.annotate("notice" if not status else "warning", f"x6cb {args.store}", f"seeds done {finished}")
    return status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--store", required=True)
    parser.add_argument("--data", default="x6data")
    parser.add_argument("--out", default="results")
    parser.add_argument("--mode", choices=sorted(x6.MODES), default="full")
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--budget-minutes", type=float, default=330)
    parser.add_argument("--group-deadline", type=float, default=0)
    parser.add_argument("--remaining", type=int, default=1)
    parser.add_argument("--seed-list", default="")
    args = parser.parse_args(argv)
    try:
        return run(args)
    except BaseException as error:
        if not isinstance(error, SystemExit):
            common.fail_loudly(f"x6cb {args.store}", error)
        raise


if __name__ == "__main__":
    sys.exit(main())
