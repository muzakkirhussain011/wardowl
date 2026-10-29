"""X7 statistics: the pre-registered verdicts (PREREG_X4_X7.md), CSV tables and a markdown report.

    python benchmarks/paper/x7_stats.py results/x7-*.jsonl --out report

Reads the X7 records, applies the rules of the pre-registration and nothing else, prints each
verdict, writes `x7_report.md` and the CSV tables into `--out`, appends the report to the job summary
and annotates the verdicts. Needs numpy (for the bootstrap) and the standard library.
"""

from __future__ import annotations

import argparse
import collections
import math
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from x4x7_common import (
    Verdicts,
    boot_ratio,
    boot_stat,
    fmt,
    fmt_ci,
    md_table,
    publish_summary,
    quantile,
    read_records,
    write_csv,
    zero_bound,
)

CONDITIONS = ("nocache", "ttl5", "ttl30", "ttl30-inv", "ttl30-shared-inv")
TTL = {"nocache": 0.0, "ttl5": 5.0, "ttl30": 30.0, "ttl30-inv": 0.0, "ttl30-shared-inv": 0.0}
STALENESS = {
    "acl-pgvector": 0.0,
    "acl-qdrant": 0.0,
    "openfga": 0.0,
    "openfga-cached-hc": 0.0,
    "openfga-cached-ml": 10.0,
    "spicedb-fc": 0.0,
    "spicedb-ml": 5.5,
    "opa-data": 0.0,
    "opa-policy": 0.0,
}
TIGHT_PATHS = ("openfga", "openfga-cached-hc", "spicedb-fc", "spicedb-ml", "opa-data", "opa-policy")
TRANSPORT = ("down", "refuse", "blackhole", "slow-3000", "http500", "http503")
CONTENT = ("truncate", "empty", "garbage-json", "type-flip", "drop-last")
ENGINES = ("openfga", "spicedb", "opa", "cerbos")
SEEDS_REQUIRED = 5


def _by(records: Iterable[Mapping[str, Any]], *keys: str) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    out: dict[tuple[Any, ...], list[Mapping[str, Any]]] = collections.defaultdict(list)
    for r in records:
        out[tuple(r.get(k) for k in keys)].append(r)
    return out


def _seeds(records: Iterable[Mapping[str, Any]]) -> int:
    return len({r.get("seed") for r in records})


def _median(values: Sequence[float]) -> float:
    return quantile(list(values), 0.5)


# ---- X7a ------------------------------------------------------------------------------------------------


def x7a(records: Sequence[Mapping[str, Any]], verdicts: Verdicts, out: Path) -> str:
    trials = [r for r in records if r.get("type") == "x7a-trial"]
    rows = []
    cells = _by(trials, "path", "condition")
    order = {c: i for i, c in enumerate(CONDITIONS)}
    for (path, condition), recs in sorted(cells.items(), key=lambda kv: (kv[0][0], order.get(kv[0][1], 9))):
        valid = [r for r in recs if r.get("valid")]
        effects = [r["effect_s"] for r in valid if r.get("effect_s") is not None]
        median = boot_stat(effects)
        violations = sum(1 for r in valid if r.get("violates_bound"))
        horizon = sum(1 for r in valid if r.get("horizon_hit"))
        rows.append([
            path, condition, len(recs), len(valid), fmt_ci(median), fmt(max(effects) if effects else math.nan),
            fmt(quantile(effects, 0.95)), fmt(recs[0].get("bound_s")), violations, horizon,
            sum(r.get("flaps", 0) for r in valid), sum(r.get("poll_errors", 0) for r in valid),
            fmt(_median([r["write_s"] for r in valid if "write_s" in r])),
        ])
        enough = len(valid) >= 30 and _seeds(valid) >= SEEDS_REQUIRED
        if path in STALENESS:
            # X7-H1: every valid trial within B + 1 s.
            detail = f"{len(valid)} valid trials, {violations} beyond B + 1 s ({horizon} never took effect), B = {recs[0].get('bound_s')}"
            if violations:
                verdicts.add(f"X7-H1 {path} {condition}", "falsified", detail)
            else:
                verdicts.add(f"X7-H1 {path} {condition}", "confirmed" if enough else "inconclusive", detail)
        stale = STALENESS.get(path)
        if path in TIGHT_PATHS and condition in ("ttl5", "ttl30") and stale is not None:
            ttl = TTL[condition]
            detail = f"median {fmt_ci(median)} against [{ttl - 1}, {ttl + stale + 1}]"
            m = median[0]
            if math.isnan(m) or not enough:
                verdict = "inconclusive"
            elif m < ttl - 2 or m > ttl + stale + 2:
                verdict = "falsified"
            elif ttl - 1 <= m <= ttl + stale + 1:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add(f"X7-H2 {path} {condition}", verdict, detail)
        if stale is not None and condition in ("ttl30-inv", "ttl30-shared-inv"):
            limit = stale + 0.5 + (1.0 if condition == "ttl30-shared-inv" else 0.0)
            m = median[0]
            detail = f"median {fmt_ci(median)}, limit {limit}"
            if math.isnan(m) or not enough:
                verdict = "inconclusive"
            elif m > limit + 0.5:
                verdict = "falsified"
            elif m <= limit:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add(f"X7-H3 {path} {condition}", verdict, detail)
        if path in ("acl-pgvector", "acl-qdrant"):
            m = median[0]
            detail = f"median {fmt_ci(median)}"
            if math.isnan(m) or not enough:
                verdict = "inconclusive"
            elif m > 1.0:
                verdict = "falsified"
            elif m <= 0.5:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add(f"X7-H4 {path} {condition}", verdict, detail)
        if path == "spicedb-ml" and condition == "nocache":
            m, top = median[0], (max(effects) if effects else math.nan)
            detail = f"median {fmt_ci(median)}, maximum {fmt(top)}"
            if math.isnan(m) or not enough:
                verdict = "inconclusive"
            elif m < 0.25 or top > 6.5:
                verdict = "falsified"
            elif m >= 0.5 and top <= 6.5:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add("X7-H5 spicedb-ml staleness", verdict, detail)
        if path in ("openfga-cached-ml", "cerbos-policy"):
            verdicts.add(f"X7 exploratory {path} {condition}", "exploratory",
                         f"median {fmt_ci(median)}, maximum {fmt(max(effects) if effects else math.nan)}")
    headers = ["path", "condition", "trials", "valid", "median s [95% CI]", "max s", "p95 s", "bound B s",
               "beyond B + 1 s", "never took effect", "flaps", "poll errors", "median write s"]
    write_csv(out / "x7a_revocation.csv", headers, rows)
    return md_table(headers, rows)


# ---- X7b ------------------------------------------------------------------------------------------------


def _share(episodes: Sequence[Mapping[str, Any]], numerator: Any) -> tuple[float, float, float]:
    return boot_ratio([numerator(e) for e in episodes], [e["inside_n"] for e in episodes])


def x7b(records: Sequence[Mapping[str, Any]], verdicts: Verdicts, out: Path) -> str:
    episodes = [r for r in records if r.get("type") == "x7b-episode"]
    excluded = [e for e in episodes if e.get("baseline_n", 0) and e["baseline_ok"] / e["baseline_n"] < 0.99]
    usable = [e for e in episodes if e not in excluded]
    rows = []
    for (target, fault, condition), eps in sorted(_by(usable, "target", "fault", "condition").items(), key=str):
        fail = _share(eps, lambda e: e["inside_fail"] + e["inside_hang"])
        ok = _share(eps, lambda e: e["inside_ok"] + e["inside_deviate"])
        recovery = boot_stat([e["recovery_s"] for e in eps if e.get("recovery_s") is not None])
        failed_latency = [_median(e["inside_fail_ms"]) for e in eps if e.get("inside_fail_ms")]
        codes: collections.Counter[str] = collections.Counter()
        for e in eps:
            codes.update(e.get("codes", {}))
        rows.append([
            target, fault, condition, len(eps), sum(e["inside_n"] for e in eps), fmt_ci(fail), fmt_ci(ok),
            sum(e.get("leaks", 0) for e in eps), sum(e.get("failures_not_authz", 0) for e in eps),
            sum(e.get("failures_naming_host", 0) for e in eps), fmt_ci(recovery),
            fmt(_median(failed_latency)) if failed_latency else "n/a", dict(codes),
            "; ".join(sorted({f"{x['class']}: {x['message']}"[:120] for e in eps for x in e.get("errors", [])}))[:400],
        ])
    headers = ["target", "fault", "condition", "episodes", "requests inside", "failing [95% CI]", "succeeding [95% CI]",
               "leaks", "failures not AuthorizationError", "failures naming a host", "recovery s [95% CI]",
               "median failed latency s", "codes", "errors"]
    write_csv(out / "x7b_faults.csv", headers, rows)
    _verdicts_b(usable, verdicts)
    note = f"{len(episodes)} episodes; {len(excluded)} excluded by G4 (baseline below 99% exact)."
    return note + "\n\n" + md_table(headers, rows)


def _verdicts_b(episodes: Sequence[Mapping[str, Any]], verdicts: Verdicts) -> None:
    engines = [e for e in episodes if e.get("kind") == "engine"]
    stores = [e for e in episodes if e.get("kind") == "store"]
    # G3: the allow-all control leaks on every engine.
    controls = {t: sum(e.get("leaks", 0) for e in engines if e["target"] == t and e["fault"] == "allow-all") for t in ENGINES}
    present = {t for t in ENGINES if any(e["target"] == t for e in engines)}
    g3 = bool(present) and all(controls[t] > 0 for t in present)
    verdicts.add("G3 leak detection (allow-all leaks)", "confirmed" if g3 else "falsified", str({t: controls[t] for t in present}))
    # X7-H6: fail closed.
    judged = [e for e in engines if e["fault"] != "allow-all"]
    leaks = sum(e.get("leaks", 0) for e in judged) + sum(e.get("leaks", 0) for e in stores)
    not_authz = sum(e.get("failures_not_authz", 0) for e in judged)
    naming = sum(e.get("failures_naming_host", 0) for e in judged)
    requests = sum(len(e.get("requests", [])) for e in judged) + sum(len(e.get("requests", [])) for e in stores)
    detail = (f"{requests} requests: {leaks} leaks (one-sided bound {fmt(zero_bound(requests), 6)}), "
              f"{not_authz} engine failures not AuthorizationError, {naming} naming a host")
    if leaks or not_authz or naming:
        verdicts.add("X7-H6 fail closed", "falsified", detail)
    else:
        verdicts.add("X7-H6 fail closed", "confirmed" if g3 and _seeds(judged) >= SEEDS_REQUIRED else "inconclusive", detail)
    store_naming = sum(e.get("failures_naming_host", 0) for e in stores)
    verdicts.add("X7 store errors (reported)", "exploratory",
                 f"{sum(e.get('failures', 0) for e in stores)} store-fault failures, {store_naming} naming a host")
    # X7-H7 (a) transport faults on engines; (b) slow faults; (c) stores.
    for (target, fault), eps in sorted(_by([e for e in engines if e["condition"] == "plain"], "target", "fault").items()):
        if fault in TRANSPORT:
            fail = _share(eps, lambda e: e["inside_fail"] + e["inside_hang"])
            _judge_share(verdicts, f"X7-H7a {target} {fault}", fail, 0.99, 0.95, eps, above=True)
        elif fault in ("slow-200", "slow-1000"):
            _judge_slow(verdicts, target, fault, eps)
    for (target, fault), eps in sorted(_by(stores, "target", "fault").items()):
        if fault in ("slow-200", "slow-1000"):
            _judge_slow(verdicts, target, fault, eps)
        else:
            fail = _share(eps, lambda e: e["inside_fail"] + e["inside_hang"])
            _judge_share(verdicts, f"X7-H7c {target} {fault}", fail, 0.99, 0.95, eps, above=True)
    # Content faults: exploratory.
    for (target, fault), eps in sorted(_by([e for e in engines if e["fault"] in CONTENT], "target", "fault").items()):
        codes: collections.Counter[str] = collections.Counter()
        for e in eps:
            codes.update(e.get("codes", {}))
        verdicts.add(f"X7 exploratory {target} {fault}", "exploratory", str(dict(codes)))
    # X7-H8 recovery.
    for (target, fault, condition), eps in sorted(_by(engines, "target", "fault", "condition").items()):
        values = [e["recovery_s"] for e in eps if e.get("recovery_s") is not None]
        median = boot_stat(values)
        enough = bool(values) and _seeds(eps) >= SEEDS_REQUIRED
        if condition == "plain" and fault in ("refuse", "blackhole", "slow-3000", "http500", "http503"):
            verdicts.add(f"X7-H8a {target} {fault}", _limit(median[0], 1.0, enough), f"median recovery {fmt_ci(median)}")
        elif condition == "plain" and fault == "down":
            verdicts.add(f"X7 exploratory recovery {target} down", "exploratory", f"median recovery {fmt_ci(median)}")
        elif condition == "breaker":
            verdicts.add(f"X7-H8b {target} {fault} recovery", _limit(median[0], 6.0, enough), f"median recovery {fmt_ci(median)}")
    for target in ENGINES:
        plain = {(e["seed"], e["episode"]): e for e in engines if e["target"] == target and e["fault"] == "blackhole" and e["condition"] == "plain"}
        guarded = {(e["seed"], e["episode"]): e for e in engines if e["target"] == target and e["fault"] == "blackhole" and e["condition"] == "breaker"}
        both = [k for k in plain if k in guarded and plain[k].get("inside_fail_ms") and guarded[k].get("inside_fail_ms")]
        if not both:
            continue
        fast = _median([_median(guarded[k]["inside_fail_ms"]) for k in both])
        slow = _median([_median(plain[k]["inside_fail_ms"]) for k in both])
        enough = len({k[0] for k in both}) >= SEEDS_REQUIRED
        if fast <= 0.1 and slow >= 1.9:
            verdict = "confirmed" if enough else "inconclusive"
        else:
            verdict = "falsified"
        verdicts.add(f"X7-H8b {target} blackhole fail-fast", verdict, f"failed latency {fmt(fast)} s with breaker, {fmt(slow)} s without")
    # X7-H9 cache masks the outage.
    for (target, fault), eps in sorted(_by([e for e in engines if e["condition"] == "cache30"], "target", "fault").items()):
        ok = _share(eps, lambda e: e["inside_ok"] + e["inside_deviate"])
        enough = _seeds(eps) >= SEEDS_REQUIRED
        if math.isnan(ok[0]) or not enough:
            verdict = "inconclusive"
        elif ok[0] < 0.95:
            verdict = "falsified"
        elif ok[0] >= 0.99:
            verdict = "confirmed"
        else:
            verdict = "inconclusive"
        verdicts.add(f"X7-H9 {target} {fault}", verdict, f"succeeding {fmt_ci(ok)}")


def _limit(value: float, limit: float, enough: bool) -> str:
    if math.isnan(value) or not enough:
        return "inconclusive"
    return "confirmed" if value <= limit else "falsified"


def _judge_share(verdicts: Verdicts, name: str, share: tuple[float, float, float], threshold: float, floor: float,
                 episodes: Sequence[Mapping[str, Any]], *, above: bool) -> None:
    detail = f"{fmt_ci(share)} over {sum(e['inside_n'] for e in episodes)} requests"
    estimate, low, high = share
    enough = _seeds(episodes) >= SEEDS_REQUIRED
    if math.isnan(estimate) or not enough:
        verdict = "inconclusive"
    elif above:
        if high < threshold:
            verdict = "falsified"
        elif estimate >= threshold and low >= floor:
            verdict = "confirmed"
        else:
            verdict = "inconclusive"
    else:
        if low > threshold:
            verdict = "falsified"
        elif estimate <= threshold:
            verdict = "confirmed"
        else:
            verdict = "inconclusive"
    verdicts.add(name, verdict, detail)


def _judge_slow(verdicts: Verdicts, target: str, fault: str, episodes: Sequence[Mapping[str, Any]]) -> None:
    delay = float(fault.split("-", 1)[1]) / 1000.0
    fail = _share(episodes, lambda e: e["inside_fail"] + e["inside_hang"])
    _judge_share(verdicts, f"X7-H7b {target} {fault} failing", fail, 0.01, 0.0, episodes, above=False)
    rises = [_median(e["inside_ok_ms"]) - _median(e["baseline_ok_ms"]) for e in episodes
             if e.get("inside_ok_ms") and e.get("baseline_ok_ms")]
    rise = boot_stat(rises)
    enough = _seeds(episodes) >= SEEDS_REQUIRED
    if math.isnan(rise[0]) or not enough:
        verdict = "inconclusive"
    elif rise[2] < delay:
        verdict = "falsified"
    elif rise[0] >= delay:
        verdict = "confirmed"
    else:
        verdict = "inconclusive"
    verdicts.add(f"X7-H7b {target} {fault} latency rise", verdict, f"median rise {fmt_ci(rise)} s against {delay} s")


# ---- Amendment 2: the targeted rerun with the fixed library ----------------------------------------------

# The full run's numbers for the cells amendment 2 runs again (run 40919304635, evidence x4-x7-run1.md).
RUN1_X7A = {
    ("spicedb-ml", "nocache"): "median 3.251 [2.994, 3.371], max 8.742; 1 of 40 beyond 6.5 s",
    ("spicedb-ml", "ttl5"): "median 5.023 [5.021, 5.026], max 6.828",
    ("spicedb-ml", "ttl30"): "median 30.018 [30.008, 30.031], max 30.044",
    ("spicedb-ml", "ttl30-inv"): "median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s",
    ("spicedb-ml", "ttl30-shared-inv"): "median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s",
    ("cerbos-policy", "nocache"): "median 2.549 [2.369, 3.219], max 4.035",
    ("cerbos-policy", "ttl30-inv"): "median 30.025 [30.019, 30.032], max 30.052",
    ("cerbos-policy", "ttl30-shared-inv"): "median 31.039 [31.026, 31.047], max 31.066",
}
RUN1_X7B = {
    ("spicedb", "empty", "plain"): "4,703 inside, failing 0.000; 4,746 deviating answers, 1 failure",
    ("pgvector", "down", "plain"): "10 inside, failing 1.000; client classes (psycopg, psycopg_pool)",
    ("pgvector", "refuse", "plain"): "10 inside, failing 1.000; client classes (psycopg, psycopg_pool)",
    ("pgvector", "blackhole", "plain"): "0 inside (closed loop): 8 hangs, 5 pool timeouts across its edges",
    ("qdrant", "down", "plain"): "5,570 inside, failing 1.000; qdrant_client classes",
    ("qdrant", "refuse", "plain"): "5,683 inside, failing 1.000; qdrant_client classes",
    ("qdrant", "blackhole", "plain"): "10 inside, failing 1.000; qdrant_client classes",
    ("qdrant", "http500", "plain"): "5,553 inside, failing 1.000; UnexpectedResponse with the raw response",
    ("qdrant", "http503", "plain"): "5,550 inside, failing 1.000; UnexpectedResponse with the raw response",
    ("qdrant", "truncate", "plain"): "5,236 inside, failing 1.000; json.decoder.JSONDecodeError",
}
A2_MEDIAN_LIMITS = {"spicedb-ml": (6.0, 7.0), "cerbos-policy": (4.0, 5.0)}  # A2-H2: ttl30-inv, ttl30-shared-inv
A2_INVALIDATION = ("ttl30-inv", "ttl30-shared-inv")
SEARCH_ERROR = "wardowl.retriever.SearchError"


class _Quiet(Verdicts):
    """Collects verdicts without printing them: the registered rules' tables are shown for an
    amendment-2 run, but their verdicts belong to the full run."""

    def add(self, name: str, verdict: str, detail: str) -> None:
        self.rows.append((name, verdict, detail))


def _is_amendment2(records: Iterable[Mapping[str, Any]]) -> bool:
    return any(r.get("type") == "run-start" and (r.get("settings") or {}).get("amendment") == 2 for r in records)


def _within(median: float, limit: float, enough: bool) -> str:
    """A median against a limit, as X7-H3 judges one: falsified above it by more than 0.5 s."""
    if math.isnan(median) or not enough:
        return "inconclusive"
    if median > limit + 0.5:
        return "falsified"
    return "confirmed" if median <= limit else "inconclusive"


def a2_revocation(records: Sequence[Mapping[str, Any]], verdicts: Verdicts) -> str:
    trials = [r for r in records if r.get("type") == "x7a-trial" and r.get("amendment") == 2]
    order = {c: i for i, c in enumerate(CONDITIONS)}
    rows = []
    for (path, condition), recs in sorted(_by(trials, "path", "condition").items(),
                                          key=lambda kv: (kv[0][0], order.get(kv[0][1], 9))):
        valid = [r for r in recs if r.get("valid")]
        effects = [r["effect_s"] for r in valid if r.get("effect_s") is not None]
        median = boot_stat(effects)
        top = max(effects) if effects else math.nan
        declared, bound2 = recs[0].get("declared_staleness_s"), recs[0].get("bound2_s")
        beyond = sum(1 for r in valid if r.get("violates_bound2"))
        never = sum(1 for r in valid if r.get("horizon_hit"))
        enough = len(valid) >= 30 and _seeds(valid) >= SEEDS_REQUIRED
        rows.append([path, condition, len(valid), fmt(declared), fmt(bound2), fmt_ci(median), fmt(top),
                     fmt(quantile(effects, 0.95)), beyond, never, sum(r.get("flaps", 0) for r in valid),
                     RUN1_X7A.get((path, condition), "")])
        # A2-H1 (after invalidate()) and A2-H3 (no cache, ttl): every valid trial within B2 + 1 s.
        name = "A2-H1" if condition in A2_INVALIDATION else "A2-H3"
        detail = (f"{len(valid)} valid trials, {beyond} beyond B2 + 1 s ({never} never took effect), "
                  f"B2 = {fmt(bound2)} (D = {fmt(declared)})")
        if bound2 is None:
            verdict = "inconclusive"  # no declared staleness: not the fixed library
        elif beyond:
            verdict = "falsified"
        else:
            verdict = "confirmed" if enough else "inconclusive"
        verdicts.add(f"{name} {path} {condition}", verdict, detail)
        # A2-H2: after invalidate(), the median is the engine's own delay.
        if condition in A2_INVALIDATION and path in A2_MEDIAN_LIMITS:
            limit = A2_MEDIAN_LIMITS[path][A2_INVALIDATION.index(condition)]
            verdicts.add(f"A2-H2 {path} {condition}", _within(median[0], limit, enough),
                         f"median {fmt_ci(median)}, limit {limit}; full run {RUN1_X7A.get((path, condition), 'n/a')}")
        # Replications, judged as first written: X7-H2 (ttl) and X7-H5 (staleness).
        stale = STALENESS.get(path)
        if path == "spicedb-ml" and condition in ("ttl5", "ttl30") and stale is not None:
            ttl, m = TTL[condition], median[0]
            if math.isnan(m) or not enough:
                verdict = "inconclusive"
            elif m < ttl - 2 or m > ttl + stale + 2:
                verdict = "falsified"
            elif ttl - 1 <= m <= ttl + stale + 1:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add(f"X7-H2 (replication) {path} {condition}", verdict,
                         f"median {fmt_ci(median)} against [{ttl - 1}, {ttl + stale + 1}]")
        if path == "spicedb-ml" and condition == "nocache":
            m = median[0]
            if math.isnan(m) or not enough:
                verdict = "inconclusive"
            elif m < 0.25 or top > 6.5:
                verdict = "falsified"
            elif m >= 0.5:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add("X7-H5 (replication) spicedb-ml staleness", verdict, f"median {fmt_ci(median)}, maximum {fmt(top)}")
    headers = ["path", "condition", "valid", "D s", "B2 s", "median s [95% CI]", "max s", "p95 s", "beyond B2 + 1 s",
               "never took effect", "flaps", "full run (comparison)"]
    return md_table(headers, rows)


def _pooled_median(episodes: Sequence[Mapping[str, Any]], key: str) -> float:
    values = [v for e in episodes for v in e.get(key, [])]
    return _median(values) if values else math.nan


def a2_faults(records: Sequence[Mapping[str, Any]], verdicts: Verdicts) -> str:
    episodes = [r for r in records if r.get("type") == "x7b-episode" and r.get("amendment") == 2]
    excluded = [e for e in episodes if e.get("baseline_n", 0) and e["baseline_ok"] / e["baseline_n"] < 0.99]
    usable = [e for e in episodes if e not in excluded]
    rows = []
    for (target, fault, condition), eps in sorted(_by(usable, "target", "fault", "condition").items(), key=str):
        inside = sum(e["inside_n"] for e in eps)
        failhang = _share(eps, lambda e: e["inside_fail"] + e["inside_hang"])
        failing = _share(eps, lambda e: e["inside_fail"])
        exact = _share(eps, lambda e: e["inside_ok"])
        deviating = _share(eps, lambda e: e["inside_deviate"])
        hangs = sum(e["inside_hang"] for e in eps)
        failhang_s = _pooled_median(eps, "inside_failhang_ms")
        fail_s = _pooled_median(eps, "inside_fail_ms")
        classes: collections.Counter[str] = collections.Counter()
        for e in eps:
            classes.update(e.get("failure_classes", {}))
        enough = _seeds(eps) >= SEEDS_REQUIRED and len(eps) >= 10
        rows.append([target, fault, condition, len(eps), inside, fmt_ci(failhang), fmt_ci(failing), hangs,
                     fmt_ci(exact), fmt_ci(deviating), fmt(failhang_s), fmt(fail_s),
                     sum(e.get("failures_all", 0) for e in eps), sum(e.get("failures_search_error", 0) for e in eps),
                     dict(classes), sum(e.get("failures_all_naming_host", 0) for e in eps), sum(e.get("leaks", 0) for e in eps),
                     RUN1_X7B.get((target, fault, condition), "")])
        if target == "pgvector" and fault == "blackhole":
            if inside < 30 or not enough:
                verdicts.add(f"A2-H4 pgvector blackhole {condition}", "inconclusive", f"{inside} requests inside")
            else:
                _judge_share(verdicts, f"A2-H4b pgvector blackhole {condition}", failhang, 0.99, 0.95, eps, above=True)
                verdicts.add(f"A2-H4c pgvector blackhole {condition}", "confirmed" if failhang_s >= 4.5 else "falsified",
                             f"median latency of inside failures and hangs {fmt(failhang_s)} s, at least 4.5 predicted")
        if target == "pgvector" and fault == "lock":
            if inside < 30 or not enough:
                verdicts.add(f"A2-H5 pgvector lock {condition}", "inconclusive", f"{inside} requests inside")
            elif condition == "stmt-timeout":
                _judge_share(verdicts, "A2-H5 pgvector lock stmt-timeout failing", failing, 0.99, 0.95, eps, above=True)
                verdict = "falsified" if hangs or math.isnan(fail_s) or fail_s > 1.5 else "confirmed"
                verdicts.add("A2-H5 pgvector lock stmt-timeout latency", verdict,
                             f"{hangs} hangs; median latency of inside failures {fmt(fail_s)} s, at most 1.5 predicted")
            else:
                verdicts.add(f"A2-H5 pgvector lock {condition} latency", "confirmed" if failhang_s >= 4.5 else "falsified",
                             f"median latency of inside failures and hangs {fmt(failhang_s)} s, at least 4.5 predicted")
        if target == "spicedb" and fault == "empty":
            estimate, low, high = failhang
            if math.isnan(estimate) or not enough:
                verdict = "inconclusive"
            elif high < 0.99 or deviating[1] > 0.01:
                verdict = "falsified"
            elif estimate >= 0.99 and low >= 0.95 and deviating[0] <= 0.01:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add("A2-H6 spicedb empty", verdict,
                         f"failing {fmt_ci(failhang)}, deviating {fmt_ci(deviating)} over {inside} requests; "
                         f"full run {RUN1_X7B[('spicedb', 'empty', 'plain')]}")
        if target == "spicedb" and fault == "empty-lookup":
            _judge_share(verdicts, "A2-H6 spicedb empty-lookup exact", exact, 0.99, 0.95, eps, above=True)
    # A2-H7: every store failure is SearchError with its fixed message, none names a host, no leak.
    stores = [e for e in usable if e.get("kind") == "store"]
    failures = sum(e.get("failures_all", 0) for e in stores)
    wrapped = sum(e.get("failures_search_error", 0) for e in stores)
    naming = sum(e.get("failures_all_naming_host", 0) for e in stores)
    leaks = sum(e.get("leaks", 0) for e in stores)
    detail = f"{failures} failures, {wrapped} SearchError with a fixed message, {naming} naming a host, {leaks} leaks"
    if stores and (wrapped < failures or naming or leaks):
        verdicts.add("A2-H7 store errors", "falsified", detail)
    elif stores:
        enough = failures >= 100 and _seeds(stores) >= SEEDS_REQUIRED
        verdicts.add("A2-H7 store errors", "confirmed" if enough else "inconclusive", detail)
    # A2-H8: fail closed on the engine episodes (replication of X7-H6).
    engines = [e for e in usable if e.get("kind") == "engine"]
    if engines:
        leaks = sum(e.get("leaks", 0) for e in engines)
        not_authz = sum(e.get("failures_not_authz", 0) for e in engines)
        naming = sum(e.get("failures_naming_host", 0) for e in engines)
        requests = sum(len(e.get("requests", [])) for e in engines)
        detail = (f"{requests} requests: {leaks} leaks (one-sided bound {fmt(zero_bound(requests), 6)}), "
                  f"{not_authz} failures not AuthorizationError, {naming} naming a host")
        if leaks or not_authz or naming:
            verdicts.add("A2-H8 fail closed", "falsified", detail)
        else:
            verdicts.add("A2-H8 fail closed", "confirmed" if _seeds(engines) >= SEEDS_REQUIRED else "inconclusive", detail)
    headers = ["target", "fault", "condition", "episodes", "requests inside", "failing or hanging [95% CI]",
               "failing [95% CI]", "hangs", "exact [95% CI]", "deviating [95% CI]", "median failing or hanging s",
               "median failing s", "failures", "SearchError, fixed message", "failure classes", "naming a host", "leaks",
               "full run (comparison)"]
    note = f"{len(episodes)} episodes; {len(excluded)} excluded by G4 (baseline below 99% exact)."
    return note + "\n\n" + md_table(headers, rows)


# ---- the report -----------------------------------------------------------------------------------------


def harness_section(records: Sequence[Mapping[str, Any]]) -> str:
    starts = [r for r in records if r.get("type") == "run-start"]
    failures = [r for r in records if r.get("type") in ("path-failed", "target-failed", "episode-failed", "x7b-control-error")]
    errors = sorted((r for r in records if r.get("type") == "harness-error"), key=lambda r: -r.get("count", 0))
    lines = [f"Runs: {len(starts)} job records; profile {sorted({r.get('profile') for r in starts})}; "
             f"commit {sorted({str(r.get('commit'))[:7] for r in starts})}."]
    for r in failures[:30]:
        lines.append(f"- **{r['type']}** {r.get('path') or r.get('target')} {r.get('fault', '')}: "
                     f"{r.get('class')}: {str(r.get('message'))[:300]} at {r.get('where')}")
    if errors:
        lines.append("")
        lines.append(md_table(["job", "where", "count", "error"], [
            [r.get("job"), r.get("where"), r.get("count"), f"{r.get('class')}: {str(r.get('message'))[:200]}"] for r in errors[:25]
        ]))
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("files", nargs="+")
    parser.add_argument("--out", default="report")
    parser.add_argument("--annotate", action="store_true", help="annotate the verdicts (GitHub Actions)")
    args = parser.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    files = [f for f in args.files if Path(f).is_file()]
    records = read_records(files)
    verdicts = Verdicts()
    profiles = sorted({r.get("profile") for r in records if r.get("type") == "run-start"})
    sections = [f"# X7: revocation and faults\n\nProfile: {profiles}. Files: {len(files)}; records: {len(records)}."
                + (" **Smoke data: not analysed for the hypotheses.**" if "smoke" in profiles else "")]
    if _is_amendment2(records):
        # The targeted rerun: amendment 2's hypotheses only. The registered rules' tables are shown,
        # without their verdicts, which belong to the full run.
        refs = sorted({str(r.get("wardowl_ref")) for r in records if r.get("type") == "run-start"})
        sections[0] += f"\n\nAmendment 2: the targeted rerun, wardowl from {refs}."
        sections.append("## Amendment 2: revocation\n\n" + a2_revocation(records, verdicts))
        sections.append("## Amendment 2: faults\n\n" + a2_faults(records, verdicts))
        sections.append("## X7a tables (registered rules, no verdicts)\n\n" + x7a(records, _Quiet(), out))
        sections.append("## X7b tables (registered rules, no verdicts)\n\n" + x7b(records, _Quiet(), out))
    else:
        sections.append("## X7a: revocation latency\n\n" + x7a(records, verdicts, out))
        sections.append("## X7b: faults\n\n" + x7b(records, verdicts, out))
    sections.insert(1, "## Verdicts\n\n" + verdicts.markdown())
    sections.append("## Harness\n\n" + harness_section(records))
    report = "\n\n".join(sections) + "\n"
    (out / "x7_report.md").write_text(report, encoding="utf-8")
    publish_summary(report)
    if args.annotate:
        verdicts.annotate("X7")
    return 0


if __name__ == "__main__":
    sys.exit(main())
