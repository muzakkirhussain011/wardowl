"""X3 and X6 follow-up, exploratory readings (PREREG_X3_X6.md, amendment 4, part B).

    python x3x6_followup.py --run1 run1 --followup parts --out reports [--resamples 10000]

--run1 holds the artifacts of run 40940385704 (x3x6-data, x3x6-results-x6-*, x3x6-results-x3-*);
--followup holds this run's (x6cb-<store>.jsonl, x3bisect-chroma.jsonl). Writes to --out:

* fu_faiss_components.csv (item 1): FAISS `post` at m = 1 and 10, W1 against W0, per component of
  the latency (search_ms, authorize_ms, the rest) and for the widening rounds;
* fu_hubs.csv, fu_hubs_summary.csv (item 3): per m = 1,000 probe, hubs and readable passages among
  its 1,000 nearest in W1 and W0, the counts they predict and the counts each store returned;
* fu_x3_pgvector_plans.csv (item 4) and fu_x6_pgvector_explain.csv (item 5, the main run's plans);
* fu_crossbuild_cells.csv, fu_crossbuild_readings.csv (item 2), fu_pg_state.csv and
  fu_cb_explain.csv (item 5, this run);
* fu_bisect.csv and fu_crash_stacks.md (item 6);
* fu_report.md, everything above in one place.

Nothing here changes a verdict: each reading is exploratory, by the rules amendment 4 fixed.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import traceback
from collections import defaultdict
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import x3x6_common as common
import x6_stats
from x3x6_common import SEED_BASE

Row = dict[str, Any]
NAN = math.nan
CONTRASTS = (
    ("replication", "W1", "W0a"),
    ("age", "W1", "W1r"),
    ("matched-content", "W1r", "W0a"),
    ("cross-build-aa", "W0b", "W0a"),
)
# The side of 0.5 on which run 40940385704 printed each offset (x6_report.md, paired latency AUC):
# FAISS post at m = 1: 0.667 [0.617, 0.717]; FAISS pre pooled: 0.276 [0.246, 0.306]; pgvector
# pre-exact pooled: 0.147 [0.123, 0.172].
TARGETS = (
    ("faiss", "post", 1, "above"),
    ("faiss", "pre", "all", "below"),
    ("pgvector", "pre-exact", "all", "below"),
)
STORES = ("faiss", "pgvector", "qdrant", "elasticsearch")


# ---- reading -------------------------------------------------------------------------------------


def find(folder: Path, name: str) -> list[Path]:
    return sorted(folder.glob(f"**/{name}"))


def iter_records(paths: Sequence[Path], *markers: str) -> Iterator[Row]:
    """Records of these files, skipping lines that hold none of the markers (cheap prefilter)."""
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if markers and not any(m in line for m in markers):
                    continue
                try:
                    yield json.loads(line)
                except ValueError:
                    continue


def median(values: Sequence[float]) -> float:
    kept = [v for v in values if v is not None and not math.isnan(v)]
    return float(np.median(kept)) if kept else NAN


def mean(values: Sequence[float]) -> float:
    kept = [v for v in values if v is not None and not math.isnan(v)]
    return float(np.mean(kept)) if kept else NAN


# ---- item 1: FAISS post at m = 1 and 10 -----------------------------------------------------------

COMPONENTS = ("latency", "search", "authorize", "rest")


def faiss_components(run1: Path, resamples: int, seed: int) -> list[Row]:
    paths = find(run1, "x6-faiss.jsonl")
    groups: dict[tuple[int, int, int, int, str], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in iter_records(paths, '"config": "post",'):
        if r.get("type") != "retrieval" or r.get("config") != "post" or r.get("warmup") or r.get("error"):
            continue
        level = int(r["level"])
        if level not in (1, 10):
            continue
        key = (int(r["seed"]), int(r["probe"]), int(r["pct"]), level, str(r["slot"]))
        latency = float(r["latency_ms"])
        search = r.get("search_ms")
        authorize = r.get("authorize_ms")
        g = groups[key]
        g["latency"].append(latency)
        g["search"].append(NAN if search is None else float(search))
        g["authorize"].append(NAN if authorize is None else float(authorize))
        rest = NAN if search is None or authorize is None else latency - float(search) - float(authorize)
        g["rest"].append(rest)
        g["searches"].append(NAN if r.get("searches") is None else float(r["searches"]))
    obs = {
        key: {**{c: median(g[c]) for c in COMPONENTS}, "searches": mean(g["searches"])} for key, g in groups.items()
    }
    rows: list[Row] = []
    for level in (1, 10):
        for pct in ("all", 1, 10, 50):
            pairs = []
            for (s, probe, p, lv, slot), a in obs.items():
                if slot != "W1" or lv != level or (pct != "all" and p != pct):
                    continue
                b = obs.get((s, probe, p, lv, "W0"))
                if b is not None:
                    pairs.append({"seed": s, "probe": probe, "pct": p, "a": a, "b": b})
            if not pairs:
                continue
            clusters = np.array([f"{p['seed']}:{p['probe']}" for p in pairs])
            for component in (*COMPONENTS, "searches"):
                values = [{"seed": p["seed"], "probe": p["probe"], "a": {"latency": p["a"][component]},
                           "b": {"latency": p["b"][component]}} for p in pairs]  # fmt: skip
                rng = common.rng_for(seed, "fu1", level, pct, component, "auc")
                cell = x6_stats.auc_cell(values, "latency", resamples, rng) or {}
                diff = np.array([p["a"][component] - p["b"][component] for p in pairs], dtype=float)
                keep = np.isfinite(diff)
                rng = common.rng_for(seed, "fu1", level, pct, component, "diff")
                d = x6_stats.mean_cell(diff[keep], clusters[keep], resamples, rng)
                equal = float(np.mean(np.isclose(
                    [p["a"][component] for p in pairs], [p["b"][component] for p in pairs], equal_nan=True)))  # fmt: skip
                rows.append({
                    "level": level, "pct": pct, "component": component, "pairs": len(pairs),
                    "clusters": len(set(clusters.tolist())), "mean_w1": cell.get("mean_w1"),
                    "mean_w0": cell.get("mean_w0"), "diff_mean": d["mean"], "diff_lo": d["lo"], "diff_hi": d["hi"],
                    "diff_median": float(np.median(diff[keep])) if keep.any() else NAN,
                    "paired_auc": cell.get("paired"), "auc_lo": cell.get("paired_lo"), "auc_hi": cell.get("paired_hi"),
                    "share_equal": equal,
                })  # fmt: skip
    return rows


# ---- item 3: hubs ----------------------------------------------------------------------------------


def observed_counts(run1: Path, level: int = 1000) -> dict[tuple[str, int, int, int, str], float]:
    """Median count over the timed repetitions of `post`, per (store, seed, probe, p, slot)."""
    found: dict[tuple[str, int, int, int, str], list[float]] = defaultdict(list)
    for store in STORES:
        for r in iter_records(find(run1, f"x6-{store}.jsonl"), '"config": "post",'):
            if r.get("type") != "retrieval" or r.get("config") != "post" or r.get("warmup") or r.get("error"):
                continue
            if int(r["level"]) != level:
                continue
            found[(store, int(r["seed"]), int(r["probe"]), int(r["pct"]), str(r["slot"]))].append(float(r["count"]))
    return {key: float(np.median(v)) for key, v in found.items()}


def hubs_table(run1: Path) -> tuple[list[Row], list[Row], dict[str, Any]]:
    import x6_data

    data = next((p.parent for p in find(run1, "manifest.json") if (p.parent / "fiqa_corpus.npy").is_file()), None)
    if data is None:
        raise FileNotFoundError("no data folder (manifest.json with fiqa_corpus.npy) under --run1")
    corpus = np.load(data / "fiqa_corpus.npy")
    queries = np.load(data / "fiqa_queries.npy")
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    common.log(f"followup: neighbours of {len(queries):,} queries in {len(corpus):,} passages")
    near_index, near_similarity = x6_data.neighbours(queries, corpus, x6_data.DEPTH)
    hubs, info = x6_data.hub_mask(near_index, len(corpus))
    check = {"recomputed": info, "manifest": manifest.get("hubs"), "same": info == manifest.get("hubs")}
    counts = observed_counts(run1)
    rows: list[Row] = []
    seed = 0
    while common.plan_path(data, seed).is_file():
        plan = json.loads(common.plan_path(data, seed).read_text(encoding="utf-8"))
        secret = np.zeros(len(corpus), dtype=bool)
        secret[np.asarray(plan["secret"], dtype=np.int64)] = True
        buckets = np.asarray(plan["buckets"], dtype=np.int64)
        own = {int(g["group"]): set(int(i) for i in g["secrets"]) for g in plan["groups"]}
        for probe in plan["probes"]:
            if int(probe["level"]) != 1000:
                continue
            q = int(probe["qindex"])
            ranked = near_index[q]
            top = ranked[:1000]
            mine = own[int(probe["group"])]
            w0 = np.array([i for i in ranked if int(i) not in mine][:1000])
            row: Row = {
                "seed": seed, "group": int(probe["group"]), "probe": q, "rank_m": int(probe["rank_m"]),
                "hubs_top1000": int(hubs[top].sum()),
                "nonhub_nonsecret_top1000": int((~hubs[top] & ~secret[top]).sum()),
                "sim_1000": float(near_similarity[q, 999]), "sim_1001": float(near_similarity[q, 1000]),
            }  # fmt: skip
            for pct in plan["pcts"]:
                readable_w1 = int((~secret[top] & (buckets[top] < pct)).sum())
                readable_w0 = int((~secret[w0] & (buckets[w0] < pct)).sum())
                row[f"readable_w1_p{pct}"] = readable_w1
                row[f"predicted_w1_p{pct}"] = min(10, readable_w1)
                row[f"readable_w0_p{pct}"] = readable_w0
                row[f"predicted_w0_p{pct}"] = min(10, readable_w0)
                for store in STORES:
                    row[f"{store}_w1_p{pct}"] = counts.get((store, seed, q, pct, "W1"))
                    row[f"{store}_w0_p{pct}"] = counts.get((store, seed, q, pct, "W0"))
            rows.append(row)
        seed += 1
    summary: list[Row] = []
    for store in STORES:
        for pct in (1, 10, 50):
            for world in ("w1", "w0"):
                pairs = [(r[f"predicted_{world}_p{pct}"], r.get(f"{store}_{world}_p{pct}")) for r in rows]
                pairs = [(a, b) for a, b in pairs if b is not None]
                if not pairs:
                    continue
                predicted = np.array([a for a, _ in pairs], dtype=float)
                observed = np.array([b for _, b in pairs], dtype=float)
                summary.append({
                    "store": store, "pct": pct, "world": world, "probes": len(pairs),
                    "share_equal": float(np.mean(predicted == observed)),
                    "mean_predicted": float(predicted.mean()), "mean_observed": float(observed.mean()),
                    "mean_abs_difference": float(np.abs(predicted - observed).mean()),
                    "correlation": float(np.corrcoef(predicted, observed)[0, 1])
                    if predicted.std() > 0 and observed.std() > 0 else NAN,
                })  # fmt: skip
    return rows, summary, check


# ---- items 4 and 5: pgvector plans -------------------------------------------------------------------


def signature(nodes: Sequence[Row]) -> str:
    """The plan's nodes in order, each as depth:type, with the index it scans."""
    parts = []
    for n in nodes:
        name = f"{n.get('depth', 0)}:{n.get('Node Type', '?')}"
        if n.get("Index Name"):
            name += f"({n['Index Name']})"
        parts.append(name)
    return " / ".join(parts)


def plan_figures(plan: Row | None) -> Row:
    if not plan:
        return {}
    nodes = plan.get("nodes") or []
    total = lambda key: sum(int(n.get(key) or 0) for n in nodes)  # noqa: E731
    return {
        "signature": signature(nodes),
        "rows_top": nodes[0].get("Actual Rows") if nodes else None,
        "rows_removed_by_filter": total("Rows Removed by Filter"),
        "rows_removed_by_recheck": total("Rows Removed by Index Recheck"),
        "shared_hit": total("Shared Hit Blocks") if any("Shared Hit Blocks" in n for n in nodes) else None,
        "shared_read": total("Shared Read Blocks") if any("Shared Read Blocks" in n for n in nodes) else None,
        "exact_heap_blocks": total("Exact Heap Blocks") if any("Exact Heap Blocks" in n for n in nodes) else None,
        "workers_launched": total("Workers Launched") if any("Workers Launched" in n for n in nodes) else None,
        "execution_ms": plan.get("execution_ms"),
        "planning_ms": plan.get("planning_ms"),
    }


def x3_pgvector_plans(run1: Path) -> list[Row]:
    rows = []
    for r in iter_records(find(run1, "x3-pgvector.jsonl"), '"type": "explain"'):
        if r.get("type") != "explain":
            continue
        rows.append({"seed": r.get("seed"), "G": r.get("G"), "error": r.get("error"), **plan_figures(r.get("plan"))})
    rows.sort(key=lambda r: (int(r["G"] or 0), int(r["seed"] or 0)))
    return rows


def x6_pgvector_explain(run1: Path) -> list[Row]:
    rows = []
    for r in iter_records(find(run1, "x6-pgvector.jsonl"), '"type": "explain"'):
        if r.get("type") != "explain":
            continue
        rows.append({key: r.get(key) for key in ("seed", "group", "probe", "level", "pct", "world", "config", "error")}
                    | plan_figures(r.get("plan")))  # fmt: skip
    rows.sort(key=lambda r: (r["config"] or "", r["seed"] or 0, r["level"] or 0, r["pct"] or 0, r["world"] or ""))
    return rows


# ---- item 2: cross-build A/A ---------------------------------------------------------------------------


def inside(c: Row | None) -> bool:
    return c is not None and 0.40 <= c["paired_lo"] and c["paired_hi"] <= 0.60


def outside(c: Row | None, side: str | None = None) -> bool:
    if c is None:
        return False
    above, below = c["paired_lo"] > 0.60, c["paired_hi"] < 0.40
    return above if side == "above" else below if side == "below" else above or below


def crossbuild(followup: Path, resamples: int, seed: int) -> tuple[list[Row], list[Row], list[Row], list[Row]]:
    paths = find(followup, "x6cb-*.jsonl")
    records, _ = common.read_records(paths)
    retrievals = [r for r in records if r.get("type") == "retrieval"]
    cells: list[Row] = []
    found: dict[tuple[str, str, str, Any, Any], Row] = {}
    if retrievals:
        data = x6_stats.Data(retrievals, resamples, seed)
        levels: list[Any] = [*data.levels, "all"]
        for store, config in data.configs:
            for name, a, b in CONTRASTS:
                pairs = data.pairs(store, config, a, b)
                for level in levels:
                    for pct in ("all", *data.pcts):
                        if pct != "all" and not (store == "faiss" and config == "post" and level in (1, 10)):
                            continue
                        chosen = x6_stats.select(data, pairs, level, pct)
                        if not chosen:
                            continue
                        for observable in ("latency", "count"):
                            if observable == "count" and level != 1:
                                continue
                            rng = common.rng_for(seed, "fu2", name, store, config, level, pct, observable)
                            c = x6_stats.auc_cell(chosen, observable, resamples, rng)
                            if c is None:
                                continue
                            same = float(np.mean([(p["a"]["ids"] or ((),))[0] == (p["b"]["ids"] or ((),))[0]
                                                  for p in chosen]))  # fmt: skip
                            row = {"contrast": name, "a": a, "b": b, "store": store, "config": config, "level": level,
                                   "pct": pct, "observable": observable, "ids_identical": same, **c}  # fmt: skip
                            cells.append(row)
                            if observable == "latency":
                                found[(name, store, config, level, pct)] = row
    readings: list[Row] = []
    for store, config, level, side in TARGETS:
        got = {name: found.get((name, store, config, level, "all")) for name, _, _ in CONTRASTS}
        if any(v is None for v in got.values()):
            readings.append({"store": store, "config": config, "level": level, "reading": "not measured"})
            continue
        matched, age, aa = got["matched-content"], got["age"], got["cross-build-aa"]
        if inside(matched) and (outside(age) or outside(aa)):
            reading = "supported: a difference between builds"
        elif outside(matched, side) and inside(age) and inside(aa):
            reading = "refuted: the content difference, with builds matched, reproduces the offset"
        else:
            reading = "inconclusive"
        row = {"store": store, "config": config, "level": level, "main_side": side, "reading": reading}
        for name, c in got.items():
            row[name] = f"{c['paired']:.3f} [{c['paired_lo']:.3f}, {c['paired_hi']:.3f}] ({c['clusters']} clusters)"
        readings.append(row)
    states = []
    for r in records:
        if r.get("type") == "table-state":
            states.append({k: v for k, v in r.items() if k not in ("schema", "exp", "mode", "run")})
    explains = []
    for r in records:
        if r.get("type") == "explain":
            keys = ("seed", "group", "probe", "level", "pct", "slot", "table", "config", "error")
            explains.append({key: r.get(key) for key in keys} | plan_figures(r.get("plan")))
    return cells, readings, states, explains


# ---- item 6: Chroma's bisection --------------------------------------------------------------------------


def bisect(followup: Path) -> tuple[list[Row], str]:
    records, _ = common.read_records(find(followup, "x3bisect-chroma.jsonl"))
    attempts = {int(r["G"]): r for r in records if r.get("type") == "attempt"}
    levels = {int(r["G"]): r for r in records if r.get("type") == "level"}
    rows = []
    stacks = ["# Chroma: what the crashing processes printed", ""]
    for r in records:
        if r.get("type") != "probe":
            continue
        g = int(r["G"])
        a = attempts.get(g, {})
        lv = levels.get(g, {})
        rows.append({
            "G": g, "gdb": r.get("gdb"), "result": r.get("result"), "returncode": r.get("returncode"),
            "seconds": r.get("seconds"), "translation_chars": a.get("translation_chars"),
            "translate_ms": a.get("translate_ms"), "build_s": a.get("build_s"), "docs": a.get("docs"),
            "error": (lv.get("error") or "")[:300] if not r.get("gdb") else None,
            "latency_ms": lv.get("latency_ms") if not r.get("gdb") else None,
        })  # fmt: skip
        if r.get("result") == "crash" or r.get("gdb"):
            title = f"G = {g:,}" + (" under gdb" if r.get("gdb") else " (fault handler on)")
            stacks += [f"## {title}: {r.get('result')}, exit status {r.get('returncode')}", ""]
            for label in ("stderr_tail", "stdout_tail"):
                text = (r.get(label) or "").strip()
                if not text:
                    continue
                lines = text.splitlines()
                if r.get("gdb"):
                    lines = [ln for ln in lines if ln.startswith(("#", "Thread", "*", "  "))
                             or "signal" in ln or "SIGSEGV" in ln or "No stack" in ln][:120]  # fmt: skip
                else:
                    start = next((i for i, ln in enumerate(lines) if "Fatal Python error" in ln), max(0, len(lines) - 80))
                    lines = lines[start : start + 120]
                if lines:
                    stacks += [f"{label}:", "", "```", *lines, "```", ""]
    rows.sort(key=lambda r: (bool(r["gdb"]), r["G"]))
    return rows, "\n".join(stacks) + "\n"


# ---- report -----------------------------------------------------------------------------------------------


def table(rows: Sequence[Row], keys: Sequence[str]) -> list[str]:
    return common.markdown_table(list(keys), [[r.get(k) for k in keys] for r in rows])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run1", default="run1")
    parser.add_argument("--followup", default="parts")
    parser.add_argument("--out", default="reports")
    parser.add_argument("--resamples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=SEED_BASE)
    args = parser.parse_args(argv)
    run1, followup, out = Path(args.run1), Path(args.followup), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# X3 and X6 follow-up: exploratory readings (amendment 4, part B)", ""]
    lines += [f"Run 40940385704's records from `{run1}`; this run's from `{followup}`. "
              f"{args.resamples:,} bootstrap resamples, seed {args.seed}. Nothing here changes a verdict.", ""]  # fmt: skip

    def section(title: str, work: Any) -> None:
        nonlocal lines
        lines += [f"## {title}", ""]
        try:
            lines += work()
        except Exception as error:
            trace = traceback.format_exc()
            common.annotate("error", f"followup {title}", f"{common.short(error, 500)}\n{trace[-1500:]}")
            lines += [f"Failed: {common.short(error, 500)}", "", "```", trace[-3000:], "```", ""]

    def item1() -> list[str]:
        rows = faiss_components(run1, args.resamples, args.seed)
        common.write_csv(out / "fu_faiss_components.csv", rows)
        keys = ["level", "pct", "component", "pairs", "mean_w1", "mean_w0", "diff_mean", "diff_lo", "diff_hi",
                "paired_auc", "auc_lo", "auc_hi", "share_equal"]  # fmt: skip
        return table([r for r in rows if r["pct"] == "all"], keys) + ["Per selectivity: fu_faiss_components.csv.", ""]

    def item3() -> list[str]:
        rows, summary, check = hubs_table(run1)
        common.write_csv(out / "fu_hubs.csv", rows)
        common.write_csv(out / "fu_hubs_summary.csv", summary)
        found = [f"Hub set recomputed: {json.dumps(check, default=str)}", ""]
        keys = ["store", "pct", "world", "probes", "share_equal", "mean_predicted", "mean_observed",
                "mean_abs_difference", "correlation"]  # fmt: skip
        found += table(summary, keys)
        keys = ["seed", "group", "probe", "rank_m", "hubs_top1000", "nonhub_nonsecret_top1000", "readable_w1_p1",
                "readable_w1_p10", "readable_w1_p50", "faiss_w1_p1", "faiss_w1_p10", "faiss_w1_p50"]  # fmt: skip
        return found + table(rows, keys)

    def item4() -> list[str]:
        rows = x3_pgvector_plans(run1)
        common.write_csv(out / "fu_x3_pgvector_plans.csv", rows)
        keys = ["G", "seed", "signature", "rows_top", "rows_removed_by_filter", "execution_ms", "error"]
        return table(rows, keys)

    def item5_main() -> list[str]:
        rows = x6_pgvector_explain(run1)
        common.write_csv(out / "fu_x6_pgvector_explain.csv", rows)
        keys = ["config", "seed", "level", "pct", "world", "signature", "rows_removed_by_filter", "execution_ms"]
        shown = [r for r in rows if r["config"] == "pre-exact"]
        return table(shown, keys) + ["All configurations: fu_x6_pgvector_explain.csv.", ""]

    def item2() -> list[str]:
        cells, readings, states, explains = crossbuild(followup, args.resamples, args.seed)
        common.write_csv(out / "fu_crossbuild_cells.csv", cells)
        common.write_csv(out / "fu_crossbuild_readings.csv", readings)
        common.write_csv(out / "fu_pg_state.csv", states)
        common.write_csv(out / "fu_cb_explain.csv", explains)
        found = ["### Readings fixed by amendment 4", ""]
        found += table(readings, ["store", "config", "level", "main_side", "replication", "age", "matched-content",
                                  "cross-build-aa", "reading"])  # fmt: skip
        found += ["### Paired latency AUC by contrast (pooled over p)", ""]
        keys = ["store", "config", "contrast", "level", "paired", "paired_lo", "paired_hi", "pooled", "mean_w1",
                "mean_w0", "clusters", "ids_identical"]  # fmt: skip
        shown = [c for c in cells if c["pct"] == "all" and c["observable"] == "latency"]
        found += table(shown, keys)
        found += ["### pgvector tables: pages and vacuum state", ""]
        keys = ["seed", "group", "phase", "slot", "relpages", "relallvisible", "vm_all_visible", "n_live_tup",
                "n_dead_tup", "n_ins_since_vacuum", "autovacuum_count", "last_autovacuum", "vm_error"]  # fmt: skip
        found += table(states, keys)
        found += ["### pgvector pre-exact plans in this run (first group of each seed)", ""]
        keys = ["seed", "level", "pct", "slot", "signature", "shared_hit", "shared_read", "exact_heap_blocks",
                "rows_removed_by_filter", "execution_ms", "error"]  # fmt: skip
        return found + table(explains, keys)

    def item6() -> list[str]:
        rows, stacks = bisect(followup)
        common.write_csv(out / "fu_bisect.csv", rows)
        (out / "fu_crash_stacks.md").write_text(stacks, encoding="utf-8")
        keys = ["G", "gdb", "result", "returncode", "seconds", "translation_chars", "translate_ms", "build_s", "error"]
        return table(rows, keys) + ["Stacks: fu_crash_stacks.md.", ""]

    section("Item 1: FAISS post at m = 1 and 10, W1 against W0, by component (pooled over p)", item1)
    section("Item 2 and 5: cross-build A/A (this run)", item2)
    section("Item 3: hubs among the 1,000 nearest passages of each m = 1,000 probe", item3)
    section("Item 4: pgvector's X3 plans (run 40940385704)", item4)
    section("Item 5: pgvector's X6 plans of the main run (pre-exact, first group of each seed)", item5_main)
    section("Item 6: Chroma's crash threshold", item6)
    (out / "fu_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    common.log("followup: done")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException as error:
        if not isinstance(error, SystemExit):
            common.fail_loudly("followup", error)
        raise
