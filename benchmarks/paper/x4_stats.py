"""X4 statistics: the pre-registered verdicts (PREREG_X4_X7.md), CSV tables and a markdown report.

    python benchmarks/paper/x4_stats.py results/x4-*.jsonl --out report

Reads the X4 records, applies the rules of the pre-registration and nothing else, prints each
verdict, writes `x4_report.md` and the CSV tables into `--out`, appends the report to the job summary
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
    annotate,
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

WELL_FORMED = ("openfga", "openfga-ctx", "spicedb", "opa-acl-doc", "opa-rel-doc", "opa-rel-pe", "cerbos")
UNPINNED = {
    "openfga": ("writer-hc", "writer-ml"),
    "spicedb": ("writer-fc", "writer-ml"),
    "opa": ("writer",),
}
QUIET = {"openfga": "quiet-hc", "spicedb": "quiet-ml", "opa": "quiet"}
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


def _order(item: tuple[tuple[Any, ...], Any]) -> tuple[str, ...]:
    """Sort grouped records by their keys, numbers by value."""
    return tuple(f"{k:012.3f}" if isinstance(k, (int, float)) else str(k) for k in item[0])


# ---- X4a ------------------------------------------------------------------------------------------------


def x4a(records: Sequence[Mapping[str, Any]], verdicts: Verdicts) -> tuple[str, list[list[Any]]]:
    rows: list[list[Any]] = []
    subjects = [r for r in records if r.get("type") == "x4a-subject"]
    by_profile = _by(subjects, "profile")
    guard_g1 = _guard_controls(by_profile)
    verdicts.add("G1 controls", "confirmed" if guard_g1[0] else "falsified", guard_g1[1])
    for (profile,), recs in sorted(by_profile.items()):
        measured = [r for r in recs if "check_true" in r]
        with_filter = [r for r in measured if r.get("filter_status") == "filter"]
        pairs = sum(r["n_docs"] for r in with_filter)
        fa = sum(r.get("fa", 0) for r in with_filter)
        fd = sum(r.get("fd", 0) for r in with_filter)
        repro = sum(r.get("repro_fa", 0) + r.get("repro_fd", 0) for r in with_filter)
        co = sum(r.get("co_fa", 0) + r.get("co_fd", 0) for r in measured)
        co_pairs = sum(r["n_docs"] for r in measured)
        subject_rate = boot_ratio([1.0 if r.get("fa", 0) + r.get("fd", 0) else 0.0 for r in with_filter])
        pair_rate = boot_ratio([r.get("fa", 0) + r.get("fd", 0) for r in with_filter], [r["n_docs"] for r in with_filter])
        errors = sum(1 for r in recs if r.get("check_error") or r.get("filter_status") == "error")
        rows.append([
            profile, len(recs), len(with_filter), errors, pairs, fa, fd, repro,
            fmt_ci(subject_rate), fmt(zero_bound(len(with_filter)), 4), fmt_ci(pair_rate, 6),
            co, fmt(co / co_pairs if co_pairs else math.nan, 6), _seeds(recs),
            sum(r.get("fa_scalar", 0) for r in with_filter),
        ])
        if profile in WELL_FORMED or profile == "opa-acl-doc-drift":
            g2 = co_pairs > 0 and co / co_pairs <= 0.001
            if profile in WELL_FORMED and co_pairs:
                verdicts.add(f"G2 encoding {profile}", "confirmed" if g2 else "falsified",
                             f"check vs oracle {co} of {co_pairs} pairs")
            name = f"X4-H1 {profile}" if profile in WELL_FORMED else f"X4-H2 {profile}"
            detail = (f"{len(with_filter)} subjects with a filter, {fa} false admits, {fd} false denials, "
                      f"{repro} reproduce; subject bound {fmt(zero_bound(len(with_filter)), 4)}")
            if repro > 0:
                verdicts.add(name, "falsified", detail)
            elif fa + fd == 0 and len(with_filter) >= 500 and guard_g1[0] and (g2 or profile not in WELL_FORMED) \
                    and _seeds(recs) >= SEEDS_REQUIRED:
                verdicts.add(name, "confirmed", detail)
            else:
                verdicts.add(name, "inconclusive", detail)
        elif profile == "cerbos-drift":
            scalar = sum(r.get("fa_scalar", 0) for r in with_filter)
            detail = f"{fa} false admits ({scalar} on documents with a scalar ACL field), {fd} false denials"
            if fd > 0 or (with_filter and fa == 0) or scalar < fa:
                verdicts.add("X4-H2 cerbos-drift", "falsified", detail)
            elif fa > 0 and _seeds(recs) >= SEEDS_REQUIRED:
                verdicts.add("X4-H2 cerbos-drift", "confirmed", detail)
            else:
                verdicts.add("X4-H2 cerbos-drift", "inconclusive", detail)
        elif profile in ("cerbos-excl", "opa-rel-pe-excl"):
            share = len(with_filter) / len(measured) if measured else math.nan
            detail = f"{fa} false admits; filter for {len(with_filter)} of {len(measured)} subjects ({fmt(share)})"
            if fa > 0:
                verdicts.add(f"X4-H3 {profile}", "falsified", detail)
            elif measured and _seeds(recs) >= SEEDS_REQUIRED:
                verdicts.add(f"X4-H3 {profile}", "confirmed", detail)
            else:
                verdicts.add(f"X4-H3 {profile}", "inconclusive", detail)
            if profile == "cerbos-excl":
                predicted_ok = len(with_filter) == 0
                verdicts.add("X4-H3 availability cerbos-excl (predicted 0)",
                             "confirmed" if predicted_ok and measured else "falsified", detail)
            else:
                agree = sum(1 for r in measured if (r.get("filter_status") == "filter") == (r.get("banned_docs", 1) == 0))
                verdicts.add("X4-H3 availability opa-rel-pe-excl (filter iff no ban in scope)",
                             "confirmed" if measured and agree == len(measured) else "falsified",
                             f"{agree} of {len(measured)} subjects as predicted")
    headers = ["profile", "subjects", "with filter", "errors", "pairs", "false admits", "false denials",
               "reproduce", "subjects disagreeing [95% CI]", "zero bound", "pair rate [95% CI]",
               "check vs oracle", "check vs oracle rate", "seeds", "false admits on scalar fields"]
    return md_table(headers, rows), [headers, *rows]


def _guard_controls(by_profile: Mapping[tuple[Any, ...], list[Mapping[str, Any]]]) -> tuple[bool, str]:
    oracle = [r for r in by_profile.get(("control-oracle",), []) if "check_true" in r]
    planted = [r for r in by_profile.get(("control-planted",), []) if "check_true" in r]
    oracle_ok = bool(oracle) and all(r.get("fa", 0) + r.get("fd", 0) + r.get("co_fa", 0) + r.get("co_fd", 0) == 0 for r in oracle)
    planted_ok = bool(planted) and all(
        r.get("fa") == r.get("planted_fa") and r.get("fd") == r.get("planted_fd") for r in planted
    )
    detail = (f"control-oracle {len(oracle)} subjects, {'none' if oracle_ok else 'some'} disagreeing; "
              f"control-planted {len(planted)} subjects, counts {'exact' if planted_ok else 'NOT exact'}")
    return oracle_ok and planted_ok, detail


# ---- X4b ------------------------------------------------------------------------------------------------


def x4b(records: Sequence[Mapping[str, Any]], verdicts: Verdicts) -> str:
    trials = [r for r in records if r.get("type") == "x4b-trial" and "disagree" in r]
    rows = []
    by_condition = _by(trials, "engine", "condition")
    for (engine, condition), recs in sorted(by_condition.items()):
        indicator = boot_ratio([1.0 if r["disagree"] else 0.0 for r in recs])
        pairs = sum(r["disagree"] for r in recs)
        explained = sum(r.get("explained", 0) for r in recs)
        repro = sum(r.get("repro_fa", 0) + r.get("repro_fd", 0) for r in recs)
        mismatch = sum(r.get("oracle_mismatch_filter", 0) + r.get("oracle_mismatch_check", 0) for r in recs)
        writes = [r.get("writes_in_window", 0) for r in recs if "writes_in_window" in r]
        rows.append([engine, condition, len(recs), fmt_ci(indicator), pairs, explained,
                     fmt(explained / pairs if pairs else math.nan), repro, mismatch,
                     fmt(_median(writes)) if writes else "n/a", _seeds(recs)])
        detail = (f"{len(recs)} trials, trials disagreeing {fmt_ci(indicator)}, {pairs} pairs, "
                  f"{explained} skew-explained, {repro} reproduce, {mismatch} oracle mismatches")
        enough = _seeds(recs) >= SEEDS_REQUIRED
        if condition == "writer-pinned":
            if repro > 0:
                verdicts.add("X4-H4a spicedb writer-pinned", "falsified", detail)
            elif pairs == 0 and mismatch == 0 and enough:
                verdicts.add("X4-H4a spicedb writer-pinned", "confirmed", detail)
            else:
                verdicts.add("X4-H4a spicedb writer-pinned", "inconclusive", detail)
        elif condition in UNPINNED.get(engine, ()):
            share = explained / pairs if pairs else math.nan
            if pairs >= 20 and share < 0.90:
                verdict = "falsified"
            elif indicator[1] > 0 and pairs and share >= 0.95 and enough:
                verdict = "confirmed"
            else:
                verdict = "inconclusive"
            verdicts.add(f"X4-H4b {engine} {condition}", verdict, detail)
        elif condition == QUIET.get(engine):
            if repro > 0:
                verdicts.add(f"X4-H4c {engine} {condition}", "falsified", detail)
            elif pairs == 0 and enough:
                verdicts.add(f"X4-H4c {engine} {condition}", "confirmed", detail)
            else:
                verdicts.add(f"X4-H4c {engine} {condition}", "inconclusive", detail)
    # (d) paired: SpiceDB writer-ml minus writer-pinned, per (seed, user).
    spice = {(r["seed"], r["user"], r["condition"]): r for r in trials if r["engine"] == "spicedb"}
    diffs = [
        (1.0 if spice[(s, u, "writer-ml")]["disagree"] else 0.0) - (1.0 if spice[(s, u, "writer-pinned")]["disagree"] else 0.0)
        for (s, u, c) in spice
        if c == "writer-ml" and (s, u, "writer-pinned") in spice
    ]
    paired = boot_ratio(diffs)
    detail = f"{len(diffs)} pairs, difference {fmt_ci(paired)}"
    if not diffs:
        verdicts.add("X4-H4d spicedb ml minus pinned", "inconclusive", detail)
    elif paired[2] <= 0:
        verdicts.add("X4-H4d spicedb ml minus pinned", "falsified", detail)
    elif paired[1] > 0 and _seeds([r for r in trials if r["engine"] == "spicedb"]) >= SEEDS_REQUIRED:
        verdicts.add("X4-H4d spicedb ml minus pinned", "confirmed", detail)
    else:
        verdicts.add("X4-H4d spicedb ml minus pinned", "inconclusive", detail)
    headers = ["engine", "condition", "trials", "trials disagreeing [95% CI]", "pairs", "skew-explained",
               "explained share", "reproduce", "oracle mismatches", "median writes in window", "seeds"]
    return md_table(headers, rows)


# ---- X4c ------------------------------------------------------------------------------------------------


def x4c(records: Sequence[Mapping[str, Any]], verdicts: Verdicts, out: Path) -> str:
    parts: list[str] = []
    calls = [r for r in records if r.get("type") == "x4c-engine-call"]
    rows = []
    for (engine, structure, n, api), recs in sorted(_by(calls, "engine", "structure", "n", "api").items(), key=_order):
        ok = [r for r in recs if r.get("status") == 200]
        counts = sorted({r.get("count") for r in ok})
        keys = sorted({tuple(r.get("keys") or r.get("result_keys") or []) for r in ok})
        rows.append([engine, structure, n, api, len(recs), len(ok), counts, fmt(_median([r["elapsed_s"] for r in recs])),
                     sum(r.get("missing", 0) for r in ok), sum(r.get("extra", 0) for r in ok),
                     sum(1 for r in ok if r.get("has_cursor")), sum(len(r.get("error_lines") or []) for r in ok), keys])
    headers = ["engine", "structure", "N", "api", "calls", "status 200", "counts", "median s", "missing", "extra",
               "with cursor", "error lines", "answer keys"]
    write_csv(out / "x4c_engine_calls.csv", headers, rows)
    parts.append("#### Engine list calls\n\n" + md_table(headers, rows))

    # X4-H5a and b.
    for engine, api, name in (("openfga", "list-objects", "X4-H5a"), ("spicedb", "lookup-limit", "X4-H5b")):
        relevant = [r for r in calls if r.get("engine") == engine and r.get("api") == api and r.get("structure") == "simple-direct"
                    and r.get("status") == 200 and (engine != "openfga" or r.get("elapsed_s", 99) < 2.5)]
        wrong = [r for r in relevant if r.get("count") != min(r["n"], 1000)]
        signal = [r for r in relevant if engine == "openfga" and r.get("keys") not in (["objects"], None)]
        detail = f"{len(relevant)} calls, {len(wrong)} with another count, {len(signal)} with keys besides objects"
        if wrong or signal:
            verdicts.add(f"{name} {engine}", "falsified", detail)
        elif relevant and _seeds(relevant) >= SEEDS_REQUIRED:
            verdicts.add(f"{name} {engine}", "confirmed", detail)
        else:
            verdicts.add(f"{name} {engine}", "inconclusive", detail)

    filters = [r for r in records if r.get("type") == "x4c-filter"]
    rows = []
    for (engine, route, structure, n, timeout), recs in sorted(_by(filters, "engine", "route", "structure", "n", "timeout").items(), key=_order):
        outcomes = collections.Counter(r.get("outcome") for r in recs)
        rows.append([engine, route, structure, n, timeout, len(recs), dict(outcomes), fmt(_median([r["elapsed_s"] for r in recs]))])
    headers = ["engine", "route", "structure", "N", "timeout s", "calls", "outcomes", "median s"]
    write_csv(out / "x4c_filters.csv", headers, rows)
    parts.append("#### wardowl's filter_for\n\n" + md_table(headers, rows))
    rebac = [r for r in filters if r.get("engine") in ("openfga", "spicedb")]
    short = [r for r in rebac if r.get("outcome") == "short"]
    detail = f"{len(rebac)} calls, {len(short)} silent short filters"
    verdicts.add("X4-H5c no silent truncation", "falsified" if short else ("confirmed" if rebac and _seeds(rebac) >= SEEDS_REQUIRED else "inconclusive"), detail)
    bad_small = [r for r in rebac if r["n"] <= 999 and r.get("outcome") not in ("error",) and r.get("elapsed_s", 0) < 3.0
                 and r.get("outcome") != "exact"]
    bad_large = [r for r in rebac if r["n"] >= 1000 and r.get("outcome") in ("exact", "short", "over", "other")]
    detail = f"{len(bad_small)} small-N calls without an exact filter, {len(bad_large)} large-N calls with a filter"
    verdicts.add("X4-H5d filter below the limit, none at it",
                 "falsified" if bad_small or bad_large else ("confirmed" if rebac and _seeds(rebac) >= SEEDS_REQUIRED else "inconclusive"), detail)
    opa = [r for r in filters if r.get("engine") == "opa"]
    if opa:
        not_exact = [r for r in opa if r.get("outcome") != "exact"]
        verdicts.add("X4c OPA routes exact (consistency check)", "exploratory",
                     f"{len(opa)} calls, {len(not_exact)} not exact: {dict(collections.Counter(r.get('outcome') for r in not_exact))}")
    slow = sorted({(r["engine"], r["structure"], r["n"]) for r in calls if r.get("elapsed_s", 0) > 2.0})
    verdicts.add("X4c exploratory: list calls over 2 s", "exploratory", str(slow[:20]))

    queries = [r for r in records if r.get("type") == "x4c-query"]
    rows = []
    for (engine, route, structure), recs in sorted(_by(queries, "engine", "route", "structure").items(), key=_order):
        by_n = _by(recs, "n")
        results: dict[str, Any] = {}
        for (n,), level in sorted(by_n.items()):
            done = [r for r in level if r.get("recall") is not None]
            failed = [r for r in level if r.get("error")]
            recall = boot_ratio([r["recall"] for r in done])
            false_complete = sum(1 for r in done if r["recall"] < 1 and r.get("complete"))
            leaks = sum(r.get("leaks", 0) for r in done)
            strategies = dict(collections.Counter(r.get("strategy") for r in done))
            rows.append([engine, route, structure, n, len(level), len(failed), fmt_ci(recall), false_complete, leaks,
                         strategies, fmt(_median([r["elapsed_s"] for r in level]))])
            results[n] = (done, failed, recall, false_complete, len(level))
        if engine in ("openfga", "spicedb"):
            _h6(verdicts, engine, structure, results)
    headers = ["engine", "route", "structure", "N", "queries", "failed", "recall@10 [95% CI]", "false complete",
               "leaks", "strategies", "median s"]
    write_csv(out / "x4c_recall.csv", headers, rows)
    parts.append("#### Permission-recall@10 through wardowl\n\n" + md_table(headers, rows))
    return "\n\n".join(parts)


def _h6(verdicts: Verdicts, engine: str, structure: str, results: Mapping[int, Any]) -> None:
    def failing(level: Any) -> bool:
        return level[4] > 0 and len(level[1]) / level[4] > 0.05

    small = [results[n] for n in results if n <= 999]
    mid = [results[n] for n in results if n in (1000, 1001)]
    large = [results[n] for n in results if n >= 10_000]
    seeds = len({r.get("seed") for level in results.values() for r in level[0]})
    name = f"X4-H6 {engine} {structure}"
    # A level where more than 5% of retrievals failed makes (a) to (c) inconclusive, whatever else.
    # (a)
    below = sum(1 for level in small for r in level[0] if r["recall"] < 1)
    if not small or any(failing(lv) for lv in small) or seeds < SEEDS_REQUIRED:
        a = "inconclusive"
    else:
        a = "falsified" if below else "confirmed"
    verdicts.add(f"{name} (a) N<=999 recall 1", a, f"{below} queries below 1")
    # (b)
    pooled = [r["recall"] for level in mid for r in level[0]]
    interval = boot_ratio(pooled)
    if not pooled or any(failing(lv) for lv in mid) or seeds < SEEDS_REQUIRED:
        b = "inconclusive"
    else:
        b = "confirmed" if interval[2] < 1 else "falsified"
    verdicts.add(f"{name} (b) N in 1000-1001 recall below 1", b, f"mean {fmt_ci(interval)} over {len(pooled)} queries")
    # (c)
    means = {n: boot_ratio([r["recall"] for r in results[n][0]])[0] for n in results if n >= 10_000}
    if not means or any(failing(lv) for lv in large) or seeds < SEEDS_REQUIRED:
        c = "inconclusive"
    elif any(m < 0.97 for m in means.values()):
        c = "falsified"
    elif all(m >= 0.99 for m in means.values()):
        c = "confirmed"
    else:
        c = "inconclusive"
    verdicts.add(f"{name} (c) N>=10000 recall >= 0.99", c, str({n: fmt(m) for n, m in means.items()}))
    # (d)
    false_complete = sum(level[3] for level in results.values())
    d = "falsified" if false_complete else ("confirmed" if results and seeds >= SEEDS_REQUIRED else "inconclusive")
    verdicts.add(f"{name} (d) no false completeness", d, f"{false_complete} false-complete results")


# ---- X4d ------------------------------------------------------------------------------------------------


def x4d(records: Sequence[Mapping[str, Any]], verdicts: Verdicts, out: Path) -> str:
    latency = [r for r in records if r.get("type") == "x4d-latency" and "check_hit_ms" in r]
    rows = []
    per_engine: dict[str, list[tuple[Any, Any]]] = collections.defaultdict(list)
    for (engine, route, structure, n), recs in sorted(_by(latency, "engine", "route", "structure", "n").items(), key=_order):
        filter_ratios = [_median(r["filter_uncached_ms"]) / max(_median(r["filter_hit_ms"]), 1e-6)
                         for r in recs if r.get("filter_uncached_ms") and r.get("filter_hit_ms")]
        check_ratios = [_median(r["check_uncached_ms"]) / max(_median(r["check_hit_ms"]), 1e-6) for r in recs]
        f_ci, c_ci = boot_stat(filter_ratios), boot_stat(check_ratios)
        uncached_f = _median([_median(r["filter_uncached_ms"]) for r in recs if r.get("filter_uncached_ms")]) if filter_ratios else math.nan
        uncached_c = _median([_median(r["check_uncached_ms"]) / max(r.get("batch", 1), 1) for r in recs])
        rows.append([engine, route, structure, n, len(recs), fmt(uncached_f), fmt(uncached_c), fmt_ci(f_ci, 1), fmt_ci(c_ci, 1)])
        if engine in ("openfga", "spicedb", "opa", "cerbos") and not route.startswith(("opa-acl", "cerbos-", "opa-rel-pe-excl")):
            per_engine[engine].append((f_ci, c_ci))
    for engine, cells in sorted(per_engine.items()):
        intervals = [ci for pair in cells for ci in pair if not math.isnan(ci[0])]
        if any(ci[2] < 5 for ci in intervals):
            verdict = "falsified"
        elif intervals and all(ci[0] >= 10 and ci[1] >= 5 for ci in intervals):
            verdict = "confirmed"
        else:
            verdict = "inconclusive"
        verdicts.add(f"X4-H7 caching {engine}", verdict, f"{len(cells)} cells; lowest median ratio "
                     f"{fmt(min((ci[0] for ci in intervals), default=math.nan), 1)}")
    headers = ["engine", "route", "structure", "N", "records", "filter_for uncached ms (median)", "check per hit ms",
               "filter speedup cached [95% CI]", "check speedup cached [95% CI]"]
    write_csv(out / "x4d_latency.csv", headers, rows)
    return md_table(headers, rows)


# ---- the report -----------------------------------------------------------------------------------------


def harness_section(records: Sequence[Mapping[str, Any]]) -> str:
    starts = [r for r in records if r.get("type") == "run-start"]
    failures = [r for r in records if r.get("type") in ("setup-failed", "part-failed")]
    errors = sorted((r for r in records if r.get("type") == "harness-error"), key=lambda r: -r.get("count", 0))
    lines = [f"Runs: {len(starts)} job records; profile {sorted({r.get('profile') for r in starts})}; "
             f"commit {sorted({str(r.get('commit'))[:7] for r in starts})}."]
    for r in failures:
        lines.append(f"- **{r['type']}** {r.get('engine')} {r.get('part', '')}: {r.get('class')}: {str(r.get('message'))[:300]} at {r.get('where')}")
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
    sections = [f"# X4: engine filters against engine checks\n\nProfile: {profiles}. Files: {len(files)}; records: "
                f"{len(records)}." + (" **Smoke data: not analysed for the hypotheses.**" if "smoke" in profiles else "")]
    table_a, csv_a = x4a(records, verdicts)
    write_csv(out / "x4a_profiles.csv", csv_a[0], csv_a[1:])
    sections.append("## X4a: one revision\n\n" + table_a)
    sections.append("## X4b: unpinned, under a writer\n\n" + x4b(records, verdicts))
    sections.append("## X4c: truncation\n\n" + x4c(records, verdicts, out))
    sections.append("## X4d: latency and caching\n\n" + x4d(records, verdicts, out))
    sections.insert(1, "## Verdicts\n\n" + verdicts.markdown())
    sections.append("## Harness\n\n" + harness_section(records))
    report = "\n\n".join(sections) + "\n"
    (out / "x4_report.md").write_text(report, encoding="utf-8")
    publish_summary(report)
    if args.annotate:
        verdicts.annotate("X4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
