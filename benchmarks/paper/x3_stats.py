"""Experiment X3, statistics: acceptance, latency and recall against the number of groups.

Reads every x3-<store>.jsonl under --in and writes, to --out:

* x3_levels.csv: per (store, G): the translation's status, time and size; whether the store accepts
  the level (share of timed retrievals without error) or refuses it (first retrieval failed in every
  seed); latency p50, p95 and p99 (per pass over the queries, median of the passes, then the median
  over seeds); recall@10 with a 95% cluster-bootstrap interval over (seed, query); the first error;
* x3_ratios.csv: latency ratios between levels, paired by query (p50 over p50, bootstrapped);
* x3_recall.csv: recall differences between levels, paired by query;
* x3_errors.csv: every distinct error message per (store, G);
* x3_verdicts.csv and x3_report.md: the verdict on each pre-registered hypothesis, by the rules of
  PREREG_X3_X6.md and nothing else.

    python x3_stats.py --in parts --out reports [--resamples 10000] [--seed 20261029] [--annotate]

numpy only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import x3x6_common as common
from x3x6_common import SEED_BASE

LEVELS = (1, 10, 100, 1_000, 4_000, 10_000, 40_000)
TOP = 40_000
PREDICTED = {
    "elasticsearch": "accepts",
    "opensearch": "accepts",
    "qdrant": "accepts",
    "pgvector": "accepts",
    "lancedb": "accepts",
    "cassandra": "accepts",
    "faiss": "accepts",
    "memory": "accepts",
    "chroma": "refuses",
}
RECALL_INVARIANT = ("qdrant", "elasticsearch", "opensearch", "redis", "weaviate", "milvus", "mongodb", "chroma", "vespa")
EXACT = ("faiss", "lancedb")
NO_RECALL = ("memory",)  # ranks by words: recall against the dense exact answer is not defined
MIN_CLUSTERS = 20
MIN_SEEDS = 5
MAX_ERROR_RATE = 0.05
CONFIRMED, FALSIFIED, INCONCLUSIVE = "confirmed", "falsified", "inconclusive"


class Data:
    def __init__(self, records: list[dict[str, Any]], resamples: int, seed: int) -> None:
        self.records = [r for r in records if r.get("exp") == "x3"]
        self.resamples = resamples
        self.seed = seed
        self.stores = sorted({r["store"] for r in self.records if r.get("store")})
        self.translations: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
        self.levels: dict[tuple[str, int], dict[int, dict[str, Any]]] = defaultdict(dict)
        # (store, G) -> (seed, query) -> pass -> retrieval
        self.retrievals: dict[tuple[str, int], dict[tuple[int, int], dict[int, dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(dict)
        )
        self.seeds_done: dict[str, set[int]] = defaultdict(set)
        for r in self.records:
            kind = r.get("type")
            store = r.get("store")
            if kind == "translate":
                self.translations[(store, int(r["G"]))].append(r)
            elif kind == "level":
                self.levels[(store, int(r["G"]))][int(r["seed"])] = r
            elif kind == "retrieval":
                self.retrievals[(store, int(r["G"]))][(int(r["seed"]), int(r["query"]))][int(r["pass"])] = r
            elif kind == "seed-end" and r.get("complete"):
                self.seeds_done[store].add(int(r["seed"]))

    def timed(self, store: str, level: int) -> list[dict[str, Any]]:
        return [r for by_pass in self.retrievals[(store, level)].values() for p, r in by_pass.items() if p >= 1]

    def per_query(self, store: str, level: int, field: str) -> dict[tuple[int, int], float]:
        """Per (seed, query): the median latency or mean recall over the timed passes without error."""
        found: dict[tuple[int, int], float] = {}
        for key, by_pass in self.retrievals[(store, level)].items():
            values = [r.get(field) for p, r in by_pass.items() if p >= 1 and r.get("error") is None]
            values = [float(v) for v in values if v is not None]
            if values:
                found[key] = float(np.median(values)) if field == "latency_ms" else float(np.mean(values))
        return found


def outcome(data: Data, store: str, level: int) -> dict[str, Any]:
    """Accepts, refuses, mixed or not run, by the rules of X3-H2, with the evidence."""
    seeds = data.levels.get((store, level), {})
    run = {s: r for s, r in seeds.items() if r.get("run")}
    timed = data.timed(store, level)
    ok = sum(1 for r in timed if r.get("error") is None)
    share = ok / len(timed) if timed else math.nan
    firsts = []
    for seed in run:
        first = data.retrievals[(store, level)].get((seed, 0), {}).get(0)
        if first is not None:
            firsts.append(first.get("error") is None)
    errors = [r for by_pass in data.retrievals[(store, level)].values() for r in by_pass.values() if r.get("error")]
    if not run:
        result = "not run"
    elif timed and share >= 0.95:
        result = "accepts"
    elif firsts and not any(firsts):
        result = "refuses"
    else:
        result = "mixed"
    return {
        "outcome": result,
        "seeds_run": len(run),
        "timed": len(timed),
        "ok_share": share,
        "timed_out_seeds": sum(1 for r in run.values() if r.get("timed_out")),
        "reduced_seeds": sum(1 for r in run.values() if r.get("reduced")),
        "first_error": errors[0].get("error") if errors else None,
        "first_cause": errors[0].get("cause") if errors else None,
    }


def latency_percentiles(data: Data, store: str, level: int) -> dict[str, float]:
    per_seed: dict[str, list[float]] = defaultdict(list)
    by_seed_pass: dict[tuple[int, int], list[float]] = defaultdict(list)
    for (seed, _), by_pass in data.retrievals[(store, level)].items():
        for number, r in by_pass.items():
            if number >= 1 and r.get("error") is None:
                by_seed_pass[(seed, number)].append(float(r["latency_ms"]))
    seeds = sorted({s for s, _ in by_seed_pass})
    for seed in seeds:
        passes = [v for (s, _), v in by_seed_pass.items() if s == seed]
        for name, q in (("p50", 50), ("p95", 95), ("p99", 99)):
            per_seed[name].append(float(np.median([np.percentile(v, q) for v in passes])))
    return {name: float(np.median(values)) for name, values in per_seed.items()}


def weighted_medians(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """The weighted median of `values` for each row of `weights`."""
    order = np.argsort(values, kind="stable")
    ranked = values[order]
    cumulative = np.cumsum(weights[:, order], axis=1)
    half = cumulative[:, -1:] / 2.0
    index = np.argmax(cumulative >= half, axis=1)
    return ranked[index]


def ratio(data: Data, store: str, top: int, bottom: int) -> dict[str, Any] | None:
    a = data.per_query(store, top, "latency_ms")
    b = data.per_query(store, bottom, "latency_ms")
    keys = sorted(set(a) & set(b))
    if not keys:
        return None
    num = np.array([a[k] for k in keys])
    den = np.array([b[k] for k in keys])
    clusters = np.array([f"{s}:{q}" for s, q in keys])
    rng = common.rng_for(data.seed, "ratio", store, top, bottom)
    boot = []
    for weights in common.cluster_weights(clusters, data.resamples, rng):
        boot.append(weighted_medians(num, weights) / weighted_medians(den, weights))
    lo, hi = common.percentile_interval(np.concatenate(boot))
    return {"store": store, "top": top, "bottom": bottom, "ratio": float(np.median(num) / np.median(den)), "lo": lo, "hi": hi,
            "pairs": len(keys), "seeds": len({s for s, _ in keys}), "p50_top_ms": float(np.median(num)),
            "p50_bottom_ms": float(np.median(den))}  # fmt: skip


def recall_difference(data: Data, store: str, top: int, bottom: int) -> dict[str, Any] | None:
    a = data.per_query(store, top, "recall")
    b = data.per_query(store, bottom, "recall")
    keys = sorted(set(a) & set(b))
    if not keys:
        return None
    diff = np.array([a[k] - b[k] for k in keys])
    clusters = np.array([f"{s}:{q}" for s, q in keys])
    rng = common.rng_for(data.seed, "recall", store, top, bottom)
    boot = [(w @ diff) / w.sum(axis=1) for w in common.cluster_weights(clusters, data.resamples, rng)]
    lo, hi = common.percentile_interval(np.concatenate(boot))
    return {"store": store, "top": top, "bottom": bottom, "difference": float(diff.mean()), "lo": lo, "hi": hi,
            "pairs": len(keys), "seeds": len({s for s, _ in keys}), "recall_top": float(np.mean([a[k] for k in keys])),
            "recall_bottom": float(np.mean([b[k] for k in keys]))}  # fmt: skip


def recall_interval(data: Data, store: str, level: int) -> dict[str, Any]:
    values = data.per_query(store, level, "recall")
    if not values:
        return {"recall": math.nan, "recall_lo": math.nan, "recall_hi": math.nan}
    keys = sorted(values)
    x = np.array([values[k] for k in keys])
    clusters = np.array([f"{s}:{q}" for s, q in keys])
    rng = common.rng_for(data.seed, "recall-level", store, level)
    boot = [(w @ x) / w.sum(axis=1) for w in common.cluster_weights(clusters, data.resamples, rng)]
    lo, hi = common.percentile_interval(np.concatenate(boot))
    return {"recall": float(x.mean()), "recall_lo": lo, "recall_hi": hi}


def translation(data: Data, store: str, level: int) -> dict[str, Any]:
    rows = data.translations.get((store, level), [])
    if not rows:
        return {"translation": "missing"}
    statuses = sorted({r["status"] for r in rows})
    times = [float(np.median(r["ms"])) for r in rows if r.get("ms")]
    sizes = [r.get("size") for r in rows if r.get("size") is not None]
    errors = [r.get("error") for r in rows if r.get("error")]
    return {
        "translation": "/".join(statuses),
        "translation_ms": float(np.median(times)) if times else math.nan,
        "translation_size": int(np.median(sizes)) if sizes else None,
        "translation_error": errors[0] if errors else None,
    }


def level_rows(data: Data) -> list[dict[str, Any]]:
    rows = []
    for store in data.stores:
        for level in LEVELS:
            if (store, level) not in data.levels and (store, level) not in data.translations:
                continue
            row: dict[str, Any] = {"store": store, "G": level, **outcome(data, store, level), **translation(data, store, level)}
            row.update(latency_percentiles(data, store, level))
            if store not in NO_RECALL:
                row.update(recall_interval(data, store, level))
            rows.append(row)
    return rows


def error_rows(data: Data) -> list[dict[str, Any]]:
    seen: dict[tuple[str, int, str], dict[str, Any]] = {}
    for (store, level), by_query in data.retrievals.items():
        for by_pass in by_query.values():
            for r in by_pass.values():
                message = r.get("error")
                if message:
                    key = (store, level, message[:200])
                    row = seen.setdefault(key, {"store": store, "G": level, "error": message, "cause": r.get("cause"), "count": 0})
                    row["count"] += 1
    return sorted(seen.values(), key=lambda r: (r["store"], r["G"]))


# ---- verdicts ------------------------------------------------------------------------------------


class Judge:
    def __init__(self, data: Data, levels: list[dict[str, Any]]) -> None:
        self.data = data
        self.levels = {(r["store"], r["G"]): r for r in levels}
        self.rows: list[dict[str, Any]] = []
        self.ratios: list[dict[str, Any]] = []
        self.recalls: list[dict[str, Any]] = []

    def part(self, hypothesis: str, store: str, label: str, result: str, evidence: str) -> str:
        self.rows.append({"hypothesis": hypothesis, "store": store, "part": label, "outcome": result, "evidence": evidence})
        return result

    def verdict(self, hypothesis: str, scope: str, outcomes: list[str]) -> None:
        if not outcomes:
            result = INCONCLUSIVE
        elif FALSIFIED in outcomes:
            result = FALSIFIED
        elif all(o == CONFIRMED for o in outcomes):
            result = CONFIRMED
        else:
            result = INCONCLUSIVE
        self.rows.append({"hypothesis": hypothesis, "store": scope, "part": "VERDICT", "outcome": result,
                          "evidence": f"{outcomes.count(CONFIRMED)} confirmed, {outcomes.count(FALSIFIED)} falsified, "
                                      f"{outcomes.count(INCONCLUSIVE)} inconclusive parts"})  # fmt: skip

    def enough(self, store: str) -> bool:
        return len(self.data.seeds_done.get(store, set())) >= MIN_SEEDS

    def h1(self) -> None:
        outcomes = []
        for store in self.data.stores:
            for level in LEVELS:
                rows = self.data.translations.get((store, level), [])
                if not rows:
                    outcomes.append(self.part("X3-H1", store, f"G={level}", INCONCLUSIVE, "no translation recorded"))
                    continue
                if all(r["status"] == "in-process" for r in rows):
                    continue  # FAISS and in-memory evaluate the filter in Python: nothing to translate
                errors = [r for r in rows if r["status"] == "error"]
                slow = [float(np.median(r["ms"])) for r in rows if r.get("ms")]
                median = float(np.median(slow)) if slow else math.nan
                if errors or (not math.isnan(median) and median >= 5000):
                    result = FALSIFIED
                elif not math.isnan(median) and median < 1000 and len(rows) >= MIN_SEEDS:
                    result = CONFIRMED
                else:
                    result = INCONCLUSIVE
                evidence = f"{len(rows)} seeds, status {sorted({r['status'] for r in rows})}, median {median:.1f} ms"
                if errors:
                    evidence += f"; {errors[0].get('error')}"
                outcomes.append(self.part("X3-H1", store, f"G={level}", result, evidence))
        self.verdict("X3-H1", "every store", outcomes)

    def h2(self) -> None:
        for store in self.data.stores:
            predicted = PREDICTED.get(store)
            row = self.levels.get((store, TOP))
            observed = outcome(self.data, store, TOP) if row is None else row
            evidence = (f"observed {observed['outcome']} in {observed['seeds_run']} seeds, ok share {observed['ok_share']:.3f}, "
                        f"first error {observed.get('first_error')}")  # fmt: skip
            if predicted is None:
                self.part("X3-H2", store, "G=40,000 (no prediction)", "reported", evidence)
                continue
            if observed["seeds_run"] < MIN_SEEDS:
                result = INCONCLUSIVE
            elif observed["outcome"] == predicted:
                result = CONFIRMED
            elif observed["outcome"] in ("accepts", "refuses"):
                result = FALSIFIED
            else:
                result = INCONCLUSIVE
            self.verdict("X3-H2", store, [self.part("X3-H2", store, f"G=40,000 predicted {predicted}", result, evidence)])

    def ratio_part(self, hypothesis: str, store: str, top: int, bottom: int, rule: Any) -> str:
        found = ratio(self.data, store, top, bottom)
        if found is not None:
            self.ratios.append(found)
        top_row = self.levels.get((store, top)) or {}
        bottom_row = self.levels.get((store, bottom)) or {}
        usable = (
            found is not None
            and found["pairs"] >= MIN_CLUSTERS
            and found["seeds"] >= MIN_SEEDS
            and all(1 - (r.get("ok_share") if r.get("ok_share") is not None else math.nan) <= MAX_ERROR_RATE
                    for r in (top_row, bottom_row))
        )  # fmt: skip
        if not usable or found is None:
            return self.part(hypothesis, store, f"p50 G={top:,} / G={bottom:,}", INCONCLUSIVE, f"{found}")
        result: str = rule(found)
        evidence = f"ratio {found['ratio']:.2f} [{found['lo']:.2f}, {found['hi']:.2f}], {found['pairs']} queries, {found['seeds']} seeds"
        return self.part(hypothesis, store, f"p50 G={top:,} / G={bottom:,}", result, evidence)

    def h3(self) -> None:
        def pgvector(r: dict[str, Any]) -> str:
            if r["hi"] < 10:
                return FALSIFIED
            return CONFIRMED if r["ratio"] >= 50 and r["lo"] >= 20 else INCONCLUSIVE

        def control(r: dict[str, Any]) -> str:
            if r["lo"] > 3:
                return FALSIFIED
            return CONFIRMED if r["ratio"] <= 2 else INCONCLUSIVE

        def cassandra(r: dict[str, Any]) -> str:
            if r["hi"] < 1:
                return FALSIFIED
            return CONFIRMED if r["lo"] > 1 else INCONCLUSIVE

        self.verdict("X3-H3a", "pgvector", [self.ratio_part("X3-H3a", "pgvector", TOP, 1, pgvector)])
        self.verdict("X3-H3b", "faiss, memory", [self.ratio_part("X3-H3b", s, TOP, 1, control) for s in ("faiss", "memory")])
        self.verdict("X3-H3c", "cassandra", [self.ratio_part("X3-H3c", "cassandra", 100, 1_000, cassandra)])
        for store in self.data.stores:  # every store's ratio, for the report
            if store not in ("pgvector", "faiss", "memory"):
                found = ratio(self.data, store, TOP, 1)
                if found is not None:
                    self.ratios.append(found)

    def h4(self) -> None:
        for store in RECALL_INVARIANT:
            if store not in self.data.stores:
                self.verdict("X3-H4", store, [self.part("X3-H4", store, "recall", INCONCLUSIVE, "the store did not run")])
                continue
            accepted = [g for g in LEVELS if g >= 1_000 and (self.levels.get((store, g)) or {}).get("outcome") == "accepts"]
            if not accepted or (self.levels.get((store, 1)) or {}).get("outcome") != "accepts":
                self.verdict("X3-H4", store, [self.part("X3-H4", store, "recall", INCONCLUSIVE, "no accepted level pair")])
                continue
            top = TOP if TOP in accepted else max(accepted)
            found = recall_difference(self.data, store, top, 1)
            if found is not None:
                self.recalls.append(found)
            if found is None or found["pairs"] < MIN_CLUSTERS or found["seeds"] < MIN_SEEDS:
                result = INCONCLUSIVE
            elif (found["lo"] > 0 or found["hi"] < 0) and abs(found["difference"]) > 0.05:
                result = FALSIFIED
            elif abs(found["difference"]) <= 0.02 and found["lo"] >= -0.05 and found["hi"] <= 0.05:
                result = CONFIRMED
            else:
                result = INCONCLUSIVE
            evidence = "missing" if found is None else (
                f"recall G={top:,} minus G=1: {found['difference']:.4f} [{found['lo']:.4f}, {found['hi']:.4f}], {found['pairs']} queries")
            self.verdict("X3-H4", store, [self.part("X3-H4", store, f"G={top:,} vs G=1", result, evidence)])
        for store in ("pgvector", "cassandra"):  # exploratory
            if store in self.data.stores:
                found = recall_difference(self.data, store, TOP, 1)
                if found is not None:
                    self.recalls.append(found)
        for store in EXACT:  # sanity: exact search finds the exact answer at every level
            for level in LEVELS:
                row = self.levels.get((store, level))
                if row and not math.isnan(row.get("recall", math.nan)):
                    ok = row["recall"] >= 0.999
                    self.part("X3-sanity", store, f"G={level} recall is 1", "passed" if ok else "FAILED", f"{row['recall']:.4f}")

    def all(self) -> list[dict[str, Any]]:
        self.h1()
        self.h2()
        self.h3()
        self.h4()
        return self.rows


def health(data: Data) -> list[dict[str, Any]]:
    rows = []
    for store in data.stores:
        mine = [r for r in data.records if r.get("store") == store]
        setup = next((r.get("error") for r in mine if r.get("type") == "setup-error"), None)
        seed_errors = [r.get("error") for r in mine if r.get("type") in ("seed-error", "seed-aborted")]
        builds = [r.get("seconds") for r in mine if r.get("type") == "build"]
        retrievals = [r for r in mine if r.get("type") == "retrieval"]
        rows.append({
            "store": store,
            "mode": next((r.get("mode") for r in mine), None),
            "seeds_done": sorted(data.seeds_done.get(store, set())),
            "skipped": [r.get("seed") for r in mine if r.get("type") == "seed-skipped"],
            "retrievals": len(retrievals),
            "errors": sum(1 for r in retrievals if r.get("error")),
            "build_s": round(float(np.mean(builds)), 1) if builds else None,
            "setup_error": setup,
            "seed_errors": seed_errors[:3],
            "corpus": next((r.get("corpus") for r in mine if r.get("type") == "start"), None),
        })  # fmt: skip
    return rows


def report(data: Data, rows: list[dict[str, Any]], judge: Judge, verdicts: list[dict[str, Any]], health_rows: list[dict[str, Any]],
           unreadable: int) -> str:  # fmt: skip
    lines = ["# X3: filter-size scaling", ""]
    lines += [f"{len(data.records):,} records ({unreadable} unreadable lines), {data.resamples:,} bootstrap resamples, "
              f"seed {data.seed}. Verdicts follow PREREG_X3_X6.md.", ""]  # fmt: skip
    lines += ["## Health", ""]
    lines += common.markdown_table(
        ["store", "mode", "seeds done", "skipped", "retrievals", "errors", "build s", "setup error", "seed errors"],
        [[h["store"], h["mode"], h["seeds_done"], h["skipped"], h["retrievals"], h["errors"], h["build_s"], h["setup_error"],
          h["seed_errors"]] for h in health_rows],
    )  # fmt: skip
    lines += ["## Verdicts", ""]
    lines += common.markdown_table(["hypothesis", "scope", "outcome", "evidence"],
                                   [[v["hypothesis"], v["store"], v["outcome"], v["evidence"]] for v in verdicts if v["part"] == "VERDICT"])  # fmt: skip
    lines += ["## Levels", ""]
    lines += common.markdown_table(
        ["store", "G", "outcome", "ok share", "p50 ms", "p95 ms", "p99 ms", "recall", "translation", "translation ms", "size", "first error"],
        [[r["store"], r["G"], r["outcome"], r["ok_share"], r.get("p50"), r.get("p95"), r.get("p99"), r.get("recall"),
          r.get("translation"), r.get("translation_ms"), r.get("translation_size"), (r.get("first_error") or "")[:160]] for r in rows],
    )  # fmt: skip
    lines += ["## Latency ratios (p50, paired by query)", ""]
    lines += common.markdown_table(["store", "G top", "G bottom", "ratio", "interval", "pairs"],
                                   [[r["store"], r["top"], r["bottom"], r["ratio"], f"[{r['lo']:.2f}, {r['hi']:.2f}]", r["pairs"]]
                                    for r in judge.ratios])  # fmt: skip
    lines += ["## Recall differences (paired by query)", ""]
    lines += common.markdown_table(["store", "G top", "G bottom", "difference", "interval", "pairs"],
                                   [[r["store"], r["top"], r["bottom"], r["difference"], f"[{r['lo']:.4f}, {r['hi']:.4f}]",
                                     r["pairs"]] for r in judge.recalls])  # fmt: skip
    lines += ["## Every verdict part", ""]
    lines += common.markdown_table(["hypothesis", "store", "part", "outcome", "evidence"],
                                   [[v["hypothesis"], v["store"], v["part"], v["outcome"], v["evidence"]] for v in verdicts
                                    if v["part"] != "VERDICT"])  # fmt: skip
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--in", dest="folder", default="parts")
    parser.add_argument("--out", default="reports")
    parser.add_argument("--resamples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=SEED_BASE)
    parser.add_argument("--annotate", action="store_true", help="also print the health and verdicts as GitHub annotations")
    args = parser.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    paths = sorted(Path(args.folder).glob("**/x3-*.jsonl"))
    records, unreadable = common.read_records(paths)
    common.log(f"x3 stats: {len(records):,} records from {len(paths)} files")
    data = Data(records, args.resamples, args.seed)
    health_rows = health(data)
    common.write_csv(out / "x3_health.csv", health_rows)
    if args.annotate:
        common.annotate("notice", "x3 health", json.dumps(health_rows, default=str), chunks=3)
    rows = level_rows(data)
    common.write_csv(out / "x3_levels.csv", rows)
    common.write_csv(out / "x3_errors.csv", error_rows(data))
    judge = Judge(data, rows)
    verdicts = judge.all()
    common.write_csv(out / "x3_ratios.csv", judge.ratios)
    common.write_csv(out / "x3_recall.csv", judge.recalls)
    common.write_csv(out / "x3_verdicts.csv", verdicts)
    (out / "x3_report.md").write_text(report(data, rows, judge, verdicts, health_rows, unreadable), encoding="utf-8")
    if args.annotate:
        summary = [f"{v['hypothesis']} {v['store']}: {v['outcome']}" for v in verdicts if v["part"] == "VERDICT"]
        common.annotate("notice", "x3 verdicts", "\n".join(summary), chunks=2)
        table = [f"{r['store']} G={r['G']}: {r['outcome']} ok={r['ok_share']:.2f} p50={r.get('p50', math.nan):.1f}ms "
                 f"recall={r.get('recall', math.nan):.3f} tr={r.get('translation')} err={(r.get('first_error') or '')[:120]}"
                 for r in rows]  # fmt: skip
        common.annotate("notice", "x3 levels", "\n".join(table), chunks=5)
    common.log("x3 stats: done")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException as error:
        if not isinstance(error, SystemExit):
            common.fail_loudly("x3 stats", error)
        raise
