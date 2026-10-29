"""Experiment X3: filter-size scaling, on one store.

    python x3_filter_scaling.py --store pgvector --data x6data --out results [--mode full|smoke]
        [--seeds 5] [--budget-minutes 330] [--group-deadline EPOCH] [--remaining N]

For each seed it builds one index of 100,000 vectors (the FiQA passage embeddings of the data job,
topped up with seeded synthetic vectors; all synthetic when the data job's files are missing) in
which a seeded 10% of the chunks, the pool, is readable at every level. Then, for each number of
groups per subject G (1 to 40,000), it times the store's own translation of the permission filter
`Or(In(allowed_users, [u]), In(allowed_groups, G groups + "*"))`, runs a warm-up pass and the timed
passes of pre-filtered retrievals through wardowl's public API, and records latency, recall@10
against exact search over the pool, and every error with its message. For pgvector it adds EXPLAIN
ANALYZE of each level's first query. Each seed runs in a process of its own, so a store that crashes
the client process (Chroma, at 40,000 groups) loses that seed's remaining levels only; the crash is
recorded (Amendment 1 of PREREG_X3_X6.md).

Writes <out>/x3-<store>.jsonl. The statistics are x3_stats.py's.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import x3x6_common as common
from x3x6_common import DIM, K, SEED_BASE, log

LEVELS = (1, 10, 100, 1_000, 4_000, 10_000, 40_000)
MODES: dict[str, dict[str, Any]] = {
    "full": {"docs": 100_000, "queries": 30, "passes": 3, "slow_queries": 10, "translate_reps": 3},
    "smoke": {"docs": 8_000, "queries": 3, "passes": 1, "slow_queries": 2, "translate_reps": 1},
}
POOL_SHARE = 0.10
CLUSTERS = 200
SIGMA = 0.06
SLOW_S = 2.0  # a level whose first retrieval takes longer runs `slow_queries` queries
TIMEOUT_S = 120.0
OTHER_GROUPS = 100_000  # the namespace of groups no subject holds
QUERY_TEXT = "passage"  # the in-memory control ranks by words; every chunk's text holds this one


def corpus(
    seed: int, n_docs: int, semantic: np.ndarray | None, queries: np.ndarray | None, n_queries: int
) -> dict[str, Any]:
    """Vectors, ACLs, query vectors and the exact answers of one seed."""
    rng = np.random.default_rng([SEED_BASE, seed, 3])
    real = semantic[:n_docs] if semantic is not None else np.zeros((0, DIM), dtype=np.float32)
    n_synthetic = n_docs - len(real)
    centres = rng.standard_normal((CLUSTERS, DIM))
    centres /= np.linalg.norm(centres, axis=1, keepdims=True)
    synthetic = centres[rng.integers(0, CLUSTERS, size=n_synthetic)] + SIGMA * rng.standard_normal((n_synthetic, DIM))
    synthetic /= np.linalg.norm(synthetic, axis=1, keepdims=True)
    vectors = np.concatenate([real.astype(np.float32), synthetic.astype(np.float32)])
    if queries is not None and len(queries) >= n_queries:
        asked = queries[np.sort(rng.choice(len(queries), size=n_queries, replace=False))].astype(np.float32)
    else:
        near = centres[rng.integers(0, CLUSTERS, size=n_queries)] + SIGMA * rng.standard_normal((n_queries, DIM))
        asked = (near / np.linalg.norm(near, axis=1, keepdims=True)).astype(np.float32)

    pool = np.zeros(n_docs, dtype=bool)
    pool[rng.choice(n_docs, size=round(POOL_SHARE * n_docs), replace=False)] = True
    groups: list[list[str]] = [[] for _ in range(n_docs)]
    for index, level in enumerate(LEVELS):
        own = rng.integers(0, level, size=n_docs)
        other = rng.integers(0, OTHER_GROUPS, size=n_docs)
        for d in range(n_docs):
            groups[d].append(f"L{level}-{own[d]}" if pool[d] else f"N{index}-{other[d]}")
    order = rng.permutation(n_docs)  # the insertion order

    exact: list[dict[str, Any]] = []
    members = np.flatnonzero(pool)
    for q in asked:
        scores = vectors[members] @ q
        kk = min(K, len(members))
        top = np.argpartition(-scores, kk - 1)[:kk]
        top = top[np.argsort(-scores[top], kind="stable")]
        sigma = float(scores[top[-1]])
        exact.append({"tstar": {f"d{int(i)}" for i in members[scores >= sigma - 1e-4]}, "R": int(len(members))})
    return {"vectors": vectors, "queries": asked, "pool": pool, "groups": groups, "order": order, "exact": exact}


def documents(world: dict[str, Any]) -> tuple[list[Any], np.ndarray]:
    from wardowl import Document

    docs = [
        Document(f"d{int(d)}", f"{QUERY_TEXT} {int(d)}", {"allowed_users": [f"owner{int(d) % 997}"],
                                                          "allowed_groups": world["groups"][int(d)]})
        for d in world["order"]
    ]  # fmt: skip
    return docs, world["vectors"][world["order"]]


def measure(retriever: Any, query: Any, subject: Any, tstar: set[str], size: int) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        result = retriever.retrieve(query, subject, K)
    except Exception as error:
        cause = error.__cause__
        return {
            "latency_ms": round((time.perf_counter() - started) * 1000, 4),
            "error": common.short(error, 1500),
            "cause": common.short(cause, 1500) if cause is not None else None,
        }
    latency = (time.perf_counter() - started) * 1000
    ids = [h.id for h in result.hits]
    return {
        "latency_ms": round(latency, 4),
        "error": None,
        "count": len(ids),
        "complete": bool(result.complete),
        "violations": result.violations,
        "recall": len(set(ids) & tstar) / min(K, size) if size else None,
    }


def timed_out(observed: dict[str, Any]) -> bool:
    if observed.get("error") is None:
        return False
    text = f"{observed.get('error')} {observed.get('cause')}".lower()
    return observed["latency_ms"] >= 0.9 * TIMEOUT_S * 1000 or "timeout" in text or "timed out" in text


def translate(target: common.Target, f: Any, reps: int) -> dict[str, Any]:
    times: list[float] = []
    try:
        output = None
        for _ in range(reps):
            started = time.perf_counter()
            output = target.translate(f)
            times.append(round((time.perf_counter() - started) * 1000, 4))
    except Exception as error:
        return {"status": "error", "error": common.short(error, 1500), "ms": times}
    if output is None:
        return {"status": "in-process", "ms": times}
    status = "fallback" if isinstance(output, dict) and output.get("fallback") else "ok"
    return {"status": status, "ms": times, "size": common.size_of(output)}


def play_seed(
    seed: int,
    args: argparse.Namespace,
    target: common.Target,
    semantic: np.ndarray | None,
    query_pool: np.ndarray | None,
    records: common.Records,
    hard_deadline: float,
) -> dict[str, Any]:
    from wardowl import MetadataACLAuthorizer, PermissionedRetriever, Query, Subject

    settings = MODES[args.mode]
    clock = time.monotonic()
    world = corpus(seed, settings["docs"], semantic, query_pool, settings["queries"])
    docs, vectors = documents(world)
    records.write(
        {
            "type": "seed-start",
            "seed": seed,
            "docs": len(docs),
            "semantic": 0 if semantic is None else int(min(len(semantic), settings["docs"])),
            "pool": int(world["pool"].sum()),
            "queries": len(world["queries"]),
            "prepare_s": round(time.monotonic() - clock, 1),
        }
    )
    clock = time.monotonic()
    log(f"  seed {seed}: building ({len(docs):,} chunks)")
    built = target.build(common.unique_base(f"x3s{seed}"), docs, vectors)
    del docs
    records.write({"type": "build", "seed": seed, "seconds": round(time.monotonic() - clock, 1), "info": built.info})
    log(f"  seed {seed}: built in {time.monotonic() - clock:.0f} s {built.info}")
    authorizer = MetadataACLAuthorizer()
    retriever = PermissionedRetriever(built.vector, authorizer, strategy="prefilter")
    queries = [Query(text=QUERY_TEXT, vector=q) for q in world["queries"]]
    stop = False
    summary: dict[str, Any] = {"seed": seed, "complete": False, "levels": {}}
    try:
        for level in LEVELS:
            if stop:
                reason = "a smaller level timed out"
                records.write({"type": "level", "seed": seed, "G": level, "run": False, "reason": reason})
                continue
            if hard_deadline and time.time() > hard_deadline:
                raise TimeoutError("the job's hard deadline passed during the seed")
            records.write({"type": "level-start", "seed": seed, "G": level})
            subject = Subject(f"reader-{level}", [f"L{level}-{j}" for j in range(level)])
            f = authorizer.filter_for(subject)
            translated = translate(target, f, settings["translate_reps"])
            records.write({"type": "translate", "seed": seed, "G": level, **translated})
            used = len(queries)
            reduced = refused = level_timeout = False
            errors = 0
            for number in range(settings["passes"] + 1):  # pass 0 is the warm-up
                for qi in range(len(queries)):
                    if qi >= used:  # a slow level runs its first `slow_queries` queries only
                        break
                    reference = world["exact"][qi]
                    observed = measure(retriever, queries[qi], subject, reference["tstar"], reference["R"])
                    records.write({"type": "retrieval", "seed": seed, "G": level, "pass": number, "warmup": number == 0,
                                   "query": qi, **observed})  # fmt: skip
                    if observed["error"] is not None:
                        errors += 1
                    if timed_out(observed):
                        level_timeout = True
                        break
                    if number == 0 and qi == 0 and observed["error"] is None and observed["latency_ms"] > SLOW_S * 1000:
                        used = min(used, settings["slow_queries"])
                        reduced = True
                if level_timeout:
                    break
                if number == 0 and errors >= used:
                    refused = True  # every warm-up retrieval failed: the timed passes are not run
                    break
            records.write({"type": "level", "seed": seed, "G": level, "run": True, "queries": used, "reduced": reduced,
                           "refused": refused, "timed_out": level_timeout, "errors": errors})  # fmt: skip
            summary["levels"][str(level)] = "timeout" if level_timeout else "refused" if refused else "ok"
            state = summary["levels"][str(level)]
            log(f"  seed {seed}: G={level:,}: {state}, {errors} errors, translation {translated['status']}")
            if level_timeout:
                stop = True
                continue
            if args.store == "pgvector" and not refused:
                record: dict[str, Any] = {"type": "explain", "seed": seed, "G": level}
                try:
                    record["plan"] = target.explain(built.vector, queries[0], K, f)  # type: ignore[attr-defined]
                except Exception as error:
                    record["error"] = common.short(error, 500)
                records.write(record)
        summary["complete"] = True
        return summary
    finally:
        try:
            target.drop(built)
        except Exception as error:
            log(f"  seed {seed}: dropping the index failed: {common.short(error, 200)}")


def load(data: Path) -> tuple[np.ndarray | None, np.ndarray | None, str]:
    """The data job's FiQA passage and query embeddings, or None for both (all synthetic)."""
    if not common.data_ready(data):
        return None, None, "synthetic-only: the data job's files are missing"
    semantic = np.load(data / "fiqa_corpus.npy")
    query_pool = np.load(data / "fiqa_queries.npy")
    described = f"{len(semantic):,} FiQA passage embeddings and {len(query_pool):,} FiQA query embeddings"
    return semantic, query_pool, described


def run_seed(args: argparse.Namespace, records: common.Records) -> int:
    """One seed, in a process of its own (Amendment 1): a store that crashes the process loses that seed's
    remaining levels only. Exit status 0, 4 when the job's hard deadline passed, 5 on an error."""
    seed = args.only_seed
    semantic, query_pool, _ = load(Path(args.data))
    target = common.make_target(args.store)
    try:
        attempts = common.connect(target)
    except Exception as error:
        versions = common.target_versions(target, reachable=False)
        records.write({"type": "setup-error", "seed": seed, "error": common.short(error, 1000), "versions": versions})
        common.annotate("error", f"x3 {args.store} setup", common.short(error, 1000))
        return 1
    versions = common.target_versions(target, reachable=True)
    records.write({"type": "versions", "seed": seed, "attempts": attempts, **versions})
    started = time.time()
    status = 0
    try:
        outcome = play_seed(seed, args, target, semantic, query_pool, records, args.hard_deadline)
    except TimeoutError as error:
        records.write({"type": "seed-aborted", "seed": seed, "error": common.short(error)})
        outcome, status = {"seed": seed, "complete": False, "error": common.short(error, 300)}, 4
    except Exception as error:
        # A build or level that fails is recorded, and the next seed is tried on a fresh index.
        records.write({"type": "seed-error", "seed": seed, "error": common.short(error, 1500)})
        common.annotate("error", f"x3 {args.store} seed {seed}", common.short(error, 1500))
        outcome, status = {"seed": seed, "complete": False, "error": common.short(error, 300)}, 5
    finally:
        target.close()
    outcome["seconds"] = round(time.time() - started, 1)
    records.write({"type": "seed-end", **outcome})
    log(f"x3 {args.store}: seed {seed} done in {outcome['seconds'] / 60:.1f} min")
    return status


def run(args: argparse.Namespace) -> int:
    out = Path(args.out)
    base = {"exp": "x3", "store": args.store, "mode": args.mode, "run": common.RUN_ID}
    records = common.Records(out / f"x3-{args.store}.jsonl", base)
    if args.only_seed is not None:
        try:
            return run_seed(args, records)
        finally:
            records.close()
    deadline = common.deadline_for(args.budget_minutes, args.group_deadline, args.remaining)
    hard_deadline = (args.group_deadline + 600) if args.group_deadline else deadline + 1800
    _, _, source = load(Path(args.data))
    if source.startswith("synthetic-only"):
        common.annotate("warning", f"x3 {args.store}", source)
    records.write({"type": "start", "args": vars(args), "settings": MODES[args.mode], "levels": list(LEVELS),
                   "corpus": source, "host": common.host(), "deadline": deadline})  # fmt: skip
    durations: list[float] = []
    statuses: dict[int, int] = {}
    status = 0
    for seed in common.seed_list(args.seeds, args.seed_list):
        if durations and time.time() + 1.2 * max(durations) > deadline:
            records.write({"type": "seed-skipped", "seed": seed, "reason": "not enough time left in the budget"})
            common.annotate("warning", f"x3 {args.store}", f"seed {seed} skipped: not enough time left")
            continue
        started = time.time()
        log(f"x3 {args.store}: seed {seed}")
        command = [sys.executable, str(Path(__file__).resolve()), "--store", args.store, "--data", args.data,
                   "--out", args.out, "--mode", args.mode, "--seeds", str(args.seeds), "--only-seed", str(seed),
                   "--hard-deadline", str(hard_deadline)]  # fmt: skip
        limit = max(60.0, hard_deadline - time.time() + 300)
        try:
            code = subprocess.run(command, check=False, timeout=limit).returncode  # noqa: S603
        except subprocess.TimeoutExpired:
            code = -999
        statuses[seed] = code
        durations.append(time.time() - started)
        if code not in (0, 1, 4, 5):
            # The process died (a signal, such as a segmentation fault, or the time limit): the level it
            # had started is the last `level-start` record of the seed without a `level` record.
            records.write({"type": "seed-crash", "seed": seed, "returncode": code})
            common.annotate("warning", f"x3 {args.store}", f"seed {seed}: the process ended with status {code}")
            status = 6
        elif code != 0:
            status = max(status, code)
        if code == 4:
            break
    records.write({"type": "end", "statuses": statuses, "status": status})
    records.close()
    common.annotate("notice" if status == 0 else "warning", f"x3 {args.store}", json.dumps(statuses))
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
    parser.add_argument("--only-seed", type=int, default=None, help=argparse.SUPPRESS)  # the per-seed child
    parser.add_argument("--hard-deadline", type=float, default=0.0, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.mode == "smoke":
        args.seeds = min(args.seeds, 1)
    try:
        return run(args)
    except BaseException as error:
        if not isinstance(error, SystemExit):
            common.fail_loudly(f"x3 {args.store}", error)
        raise


if __name__ == "__main__":
    sys.exit(main())
