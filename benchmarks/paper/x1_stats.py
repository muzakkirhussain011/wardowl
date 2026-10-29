"""Experiment X1, statistics: intervals, paired tests and the pre-registered verdicts.

Reads the tidy outputs of x1_underretrieval.py and writes, to <in>/stats/:

* summary_by_build.csv: every metric of section 6.5 per (store, layout, setting, build);
* summary_by_setting.csv: the same across builds (mean, and the range between builds);
* intervals.csv: 95% cluster-bootstrap intervals over persons, per setting, overall and by person
  type, question category, region and rho_100 bin;
* paired.csv: paired comparisons with the setting of the original run (and the other pairs the
  predictions need): the mean difference with its interval, McNemar's exact test for the
  empty-result rate and Wilcoxon's signed-rank test for per-question recall and latency;
* explain_summary.csv, qdrant_paths.csv, acorn_engagement.csv: pgvector's EXPLAIN and Qdrant's
  search paths, summarised;
* predictions.csv and report.md: each prediction of section 6.6 judged confirmed, falsified or
  inconclusive by the rules of PREREGISTRATION.md, with every number the rule used.

Each question's value is first averaged over the builds a setting ran on; the mean over questions is
then bootstrapped by resampling persons (10,000 resamples by default, seeded, percentile intervals).
A difference between two settings is taken per (question, replicate), averaged per question and
bootstrapped the same way. CPU only.

Run 2 (amendment 2 of PREREGISTRATION.md) is read from several shard folders at once: the first
folder's question table is used and every other folder's must describe the same questions, and a
setting and build reported by two folders stops the statistics. Its outputs add plans.csv (the
plans each pgvector setting executed) and the verdict on P5; P1 and P2 then use `pg-custom` as
their reference and leave out settings that ran mostly exact.

    python x1_stats.py [--in /kaggle/working/x1run2 ...] [--out DIR] [--resamples 10000] [--seed 20261026]
"""

from __future__ import annotations

import argparse
import json
import math
import time
import zlib
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import paper_common as pc
from paper_common import log

Key = tuple[str, str, str]  # (store, layout, setting)

PG_REF: Key = ("pgvector", "hnsw-m16-efc64", "p-asrun")
PG_CUSTOM: Key = ("pgvector", "hnsw-m16-efc64", "pg-custom")  # run 2: the reference of P1 and P2 (amendment 2)
PG_WIDE = "hnsw-m32-efc200"
Q_REF: Key = ("qdrant", "as-run", "q-asrun")
X0_RECALL5 = 0.691  # the original run's pgvector recall@5 (results.json of notebookd8377caca8)
HNSW_SHARE_FLOOR = 0.5  # amendment 2, item 3: below this, a setting meant to search the graph ran mostly exact

METRICS = [
    "recall5",
    "recall10",
    "empty5",
    "empty10",
    "short5",
    "short10",
    "gross_miss5",
    "gross_miss10",
    "sim_gap5",
    "sim_gap10",
    "target_found5",
    "kb_share5",
    "complete5",
    "complete10",
    "false_complete5",
    "false_complete10",
    "false_incomplete5",
    "false_incomplete10",
    "latency_ms",
    "search_ms",
]
SUBGROUP_METRICS = ["recall5", "recall10", "empty5", "sim_gap10"]
PAIRED_METRICS = ["recall5", "recall10", "empty5", "empty10", "short5", "gross_miss10", "sim_gap10", "latency_ms"]
SUBGROUPS = ("persona_type", "category", "region", "rho_bin")
QUESTION_COLUMNS = ["qid", "person", "persona_type", "category", "region", "answerable", "R", "r1", "rho100"]
RHO_BINS = [0.0, 0.01, 0.1, 0.5, 1.0001]
RHO_LABELS = ["rho100 < 0.01", "0.01 to 0.1", "0.1 to 0.5", "0.5 or more"]
RAISED = ("pa-t100k-m1", "pa-t20k-m8", "pa-t100k-m8", "pa-t1000k-m1", "pa-t1000k-m8", "pa-t1000k-m16", "pb-wm64")


def name(key: Key) -> str:
    return "/".join(key)


# ---- statistics ----------------------------------------------------------------------------------


def rng_for(seed: int, *parts: Any) -> np.random.Generator:
    """A generator seeded by the run's seed and what is being estimated, so every interval is
    reproducible on its own, whatever else is computed."""
    return np.random.default_rng([seed, zlib.crc32("/".join(map(str, parts)).encode())])


def cluster_bootstrap(
    values: np.ndarray, clusters: np.ndarray, resamples: int, rng: np.random.Generator
) -> dict[str, Any]:
    """The mean of `values` with a 95% percentile interval from resampling whole clusters (persons)."""
    keep = np.isfinite(values)
    values, clusters = values[keep], clusters[keep]
    if not len(values):
        return {"mean": math.nan, "low": math.nan, "high": math.nan, "n": 0, "clusters": 0}
    _, inverse = np.unique(clusters.astype(str), return_inverse=True)
    sums = np.bincount(inverse, weights=values)
    counts = np.bincount(inverse).astype(float)
    p = len(sums)
    weights = rng.multinomial(p, np.full(p, 1.0 / p), size=resamples).astype(float)
    means = (weights @ sums) / (weights @ counts)
    low, high = np.percentile(means, [2.5, 97.5])
    return {"mean": float(values.mean()), "low": float(low), "high": float(high), "n": len(values), "clusters": p}


def mcnemar(a: np.ndarray, b: np.ndarray) -> dict[str, Any]:
    """McNemar's exact test on paired binary outcomes (here: an empty result under a and under b)."""
    from scipy import stats

    keep = np.isfinite(a) & np.isfinite(b)
    a, b = a[keep].astype(bool), b[keep].astype(bool)
    only_a, only_b = int((a & ~b).sum()), int((~a & b).sum())
    n = only_a + only_b
    p = 1.0 if n == 0 else float(stats.binomtest(min(only_a, only_b), n, 0.5).pvalue)
    return {"mcnemar_only_a": only_a, "mcnemar_only_b": only_b, "mcnemar_p": p}


def wilcoxon(differences: np.ndarray) -> dict[str, Any]:
    """Wilcoxon's signed-rank test on per-question differences; zeros are dropped, as Wilcoxon did."""
    from scipy import stats

    d = differences[np.isfinite(differences)]
    d = d[d != 0]
    if not len(d):
        return {"wilcoxon_p": 1.0, "wilcoxon_note": "every difference is zero"}
    try:
        return {"wilcoxon_p": float(stats.wilcoxon(d).pvalue), "wilcoxon_note": f"{len(d)} non-zero differences"}
    except ValueError as error:
        return {"wilcoxon_p": math.nan, "wilcoxon_note": f"not computed: {error}"}


def excludes_zero(interval: dict[str, Any] | None) -> bool | None:
    if interval is None or math.isnan(interval["low"]):
        return None
    return interval["low"] > 0 or interval["high"] < 0


# ---- loading -------------------------------------------------------------------------------------


class Data:
    """x1's outputs, joined with the question table, and the estimates the rules ask for."""

    def __init__(self, folders: Sequence[Path], resamples: int, seed: int) -> None:
        self.folders, self.resamples, self.seed = list(folders), resamples, seed
        self.folder = self.folders[0]
        questions = pc.read_table(self.folder / "questions")
        if questions is None:
            raise FileNotFoundError(f"{self.folder} has no questions table: run x1_underretrieval.py first")
        self.questions = questions
        for other in self.folders[1:]:
            self._same_questions(other)
        runs = self._tables("runs")
        if runs.empty:
            raise FileNotFoundError(f"{self.folders} hold no results: run x1_underretrieval.py first")
        twice = runs.duplicated(["store", "layout", "build", "setting", "qid"])
        if twice.any():
            clash = runs.loc[twice, ["store", "layout", "build", "setting"]].drop_duplicates()
            first = clash.head(5).to_dict("records")
            raise RuntimeError(f"settings and builds reported by more than one folder: {first}")
        runs["error"] = runs["error"].fillna("").astype(str)
        for column in ("hits5", "hits10", "plan5", "plan10"):
            if column in runs:
                runs[column] = runs[column].fillna("").astype(str)
        self.runs = runs.merge(questions[QUESTION_COLUMNS].drop(columns="person"), on="qid", how="left")
        self.runs["rho_bin"] = pd.cut(self.runs["rho100"], RHO_BINS, labels=RHO_LABELS, right=False).astype(str)
        self.explain = self._tables("explain")
        self.telemetry = self._tables("telemetry")
        estimates = [pc.read_table(f / "pg_filter_estimates") for f in self.folders]
        self.estimates = next((e for e in estimates if e is not None and not e.empty), None)
        self.metas = self._records("meta")
        self.builds = self._records("builds")
        self.keys: set[Key] = set(self.runs[["store", "layout", "setting"]].itertuples(index=False, name=None))
        self.per_question = self._per_question()
        self.grid = self._grid()
        self.pg_ref = PG_CUSTOM if self.grid == "run2" else PG_REF  # the reference of P1 and P2
        self.plans = plan_table(self.runs)
        overall = self.plans.to_dict("records") if not self.plans.empty else []
        self.mostly_exact = {
            (r["store"], r["layout"], r["setting"])
            for r in overall
            if r["build"] == "all" and r["meant_for_graph"] and r["hnsw_share"] < HNSW_SHARE_FLOOR
        }
        log(
            f"{len(self.runs):,} result rows of {len(self.keys)} settings from {len(self.folders)} folders; "
            f"{len(self.metas)} setting records; grid {self.grid}; P1 and P2 reference {name(self.pg_ref)}"
        )

    def _tables(self, kind: str) -> pd.DataFrame:
        frames = [pc.read_tables(f / kind) for f in self.folders]
        frames = [f for f in frames if not f.empty]
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def _records(self, kind: str) -> list[dict[str, Any]]:
        paths = [p for f in self.folders for p in sorted((f / kind).glob("*.json"))]
        return [json.loads(p.read_text(encoding="utf-8")) for p in paths]

    def _same_questions(self, other: Path) -> None:
        """A shard's question table must describe this one's questions, persons and readable counts."""
        theirs = pc.read_table(other / "questions")
        if theirs is None:
            raise FileNotFoundError(f"{other} has no questions table")
        key = ["qid", "person", "question", "R"]
        a, b = self.questions[key].reset_index(drop=True), theirs[key].reset_index(drop=True)
        if len(a) != len(b) or not a.astype(str).equals(b.astype(str)):
            raise RuntimeError(f"{other} describes other questions than {self.folder}")

    def _grid(self) -> str:
        """run1 or run2, from the option every invocation of x1_underretrieval.py recorded (run1 before it)."""
        grids = set()
        for folder in self.folders:
            path = folder / "manifest.json"
            if path.is_file():
                for entry in json.loads(path.read_text(encoding="utf-8")).get("invocations", []):
                    grids.add((entry.get("options") or {}).get("grid") or "run1")
        if len(grids) > 1:
            raise RuntimeError(f"the folders mix grids {sorted(grids)}: analyse run 1 and run 2 separately")
        return grids.pop() if grids else "run1"

    def usable(self, key: Key) -> bool:
        """Amendment 2, item 3: P1 and P2 leave out a setting that was meant to search the graph and mostly did not."""
        return key not in self.mostly_exact

    def _per_question(self) -> pd.DataFrame:
        """Each (setting, question)'s metrics averaged over the builds the setting ran on."""
        means = self.runs.groupby(["store", "layout", "setting", "qid"], sort=False)[METRICS].mean().reset_index()
        means = means.merge(self.questions[QUESTION_COLUMNS], on="qid", how="left")
        means["rho_bin"] = pd.cut(means["rho100"], RHO_BINS, labels=RHO_LABELS, right=False).astype(str)
        return means

    def of(self, key: Key, frame: pd.DataFrame | None = None) -> pd.DataFrame:
        frame = self.per_question if frame is None else frame
        store, layout, setting = key
        return frame[(frame["store"] == store) & (frame["layout"] == layout) & (frame["setting"] == setting)]

    def estimate(
        self, key: Key, metric: str, where: Callable[[pd.DataFrame], pd.Series] | None = None
    ) -> dict[str, Any] | None:
        """The mean of a metric over a setting's questions (optionally a subset), with its interval."""
        if key not in self.keys:
            return None
        frame = self.of(key)
        if where is not None:
            frame = frame[where(frame)]
        result = cluster_bootstrap(
            frame[metric].to_numpy(float),
            frame["person"].to_numpy(),
            self.resamples,
            rng_for(self.seed, *key, metric, "subset" if where else "all"),
        )
        return result if result["n"] else None

    def difference(
        self, a: Key, b: Key, metric: str, where: Callable[[pd.DataFrame], pd.Series] | None = None
    ) -> dict[str, Any] | None:
        """a minus b, per (question, replicate) they share, averaged per question, bootstrapped by person."""
        if a not in self.keys or b not in self.keys:
            return None
        merged = self.paired_rows(a, b, [metric])
        if where is not None:
            merged = merged[where(merged)]
        if merged.empty:
            return None
        per_question = (merged[f"{metric}_a"] - merged[f"{metric}_b"]).groupby(merged["qid"]).mean()
        persons = merged.groupby("qid")["person"].first().loc[per_question.index]
        result = cluster_bootstrap(
            per_question.to_numpy(float),
            persons.to_numpy(),
            self.resamples,
            rng_for(self.seed, *a, "minus", *b, metric, "subset" if where else "all"),
        )
        result["per_question"] = per_question
        return result if result["n"] else None

    def paired_rows(self, a: Key, b: Key, metrics: Sequence[str]) -> pd.DataFrame:
        """The two settings' rows side by side, matched on question and replicate."""
        columns = ["qid", "rep", *metrics]
        left = self.of(a, self.runs)[columns]
        right = self.of(b, self.runs)[columns]
        merged = left.merge(right, on=["qid", "rep"], suffixes=("_a", "_b"))
        return merged.merge(self.questions[QUESTION_COLUMNS], on="qid", how="left")


# ---- tables --------------------------------------------------------------------------------------


def build_summary(runs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (store, layout, setting, build), g in runs.groupby(["store", "layout", "setting", "build"], sort=True):
        latency = g["latency_ms"].dropna()
        row: dict[str, Any] = {
            "store": store,
            "layout": layout,
            "setting": setting,
            "build": build,
            "rep": int(g["rep"].iloc[0]),
            "questions": len(g),
            "scorable": int(g["recall10"].notna().sum()),
            "errors": int((g["error"] != "").sum()),
            "unstable5": int(g["unstable5"].sum()),
        }
        row.update({m: g[m].mean() for m in METRICS if m != "latency_ms"})
        for q in (50, 95, 99):
            row[f"latency_p{q}"] = float(np.percentile(latency, q)) if len(latency) else math.nan
        for k in (5, 10):
            row[f"false_complete{k}_count"] = int(g[f"false_complete{k}"].sum())
            row[f"false_incomplete{k}_count"] = int(g[f"false_incomplete{k}"].sum())
        rows.append(row)
    return pd.DataFrame(rows)


def setting_summary(by_build: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (store, layout, setting), g in by_build.groupby(["store", "layout", "setting"], sort=True):
        row: dict[str, Any] = {"store": store, "layout": layout, "setting": setting, "builds": len(g)}
        for metric in ("recall5", "recall10", "empty5", "short5", "gross_miss10", "sim_gap10", "latency_p50"):
            row[metric] = g[metric].mean()
            row[f"{metric}_range"] = g[metric].max() - g[metric].min() if len(g) > 1 else math.nan
        rows.append(row)
    return pd.DataFrame(rows)


def interval_table(data: Data) -> pd.DataFrame:
    rows = []
    for (store, layout, setting), g in data.per_question.groupby(["store", "layout", "setting"], sort=True):
        groups: list[tuple[str, str, pd.DataFrame, Sequence[str]]] = [("all", "all", g, METRICS)]
        for column in SUBGROUPS:
            groups += [(column, str(v), sub, SUBGROUP_METRICS) for v, sub in g.groupby(column, sort=True)]
        for column, value, sub, metrics in groups:
            for metric in metrics:
                rng = rng_for(data.seed, store, layout, setting, column, value, metric)
                result = cluster_bootstrap(sub[metric].to_numpy(float), sub["person"].to_numpy(), data.resamples, rng)
                if result["n"]:
                    where = {"store": store, "layout": layout, "setting": setting, "subgroup": column, "value": value}
                    rows.append({**where, "metric": metric, **result})
    return pd.DataFrame(rows)


def comparisons(keys: set[Key], pg_ref: Key = PG_REF) -> list[tuple[Key, Key, str]]:
    """Every setting against its store's original-run setting, plus the pairs the predictions need;
    in run 2 every pgvector setting also against `pg-custom`, the reference of P1 and P2."""
    pairs: list[tuple[Key, Key, str]] = []
    for key in sorted(keys):
        reference = PG_REF if key[0] == "pgvector" else Q_REF
        if key != reference:
            pairs.append((key, reference, "against the original run's setting"))
        if key[0] == "pgvector" and pg_ref != PG_REF and key[2] != pg_ref[2]:
            pairs.append((key, (pg_ref[0], key[1], pg_ref[2]), "against pg-custom on the same index (amendment 2)"))
        if key[0] == "qdrant" and key[1] != Q_REF[1] and (key[0], Q_REF[1], key[2]) in keys:
            pairs.append((key, (key[0], Q_REF[1], key[2]), "layout against as-run, same setting"))
        if key[0] == "pgvector" and key[1] == PG_WIDE and (key[0], PG_REF[1], key[2]) in keys:
            pairs.append((key, (key[0], PG_REF[1], key[2]), "index family against m16/efc64, same setting"))
    pairs.append((("qdrant", "as-run", "qa-acorn100"), ("qdrant", "as-run", "qa-acorn040"), "ACORN 1.0 against 0.4"))
    seen, unique = set(), []
    for a, b, why in pairs:
        if a in keys and b in keys and (a, b) not in seen:
            seen.add((a, b))
            unique.append((a, b, why))
    return unique


def paired_table(data: Data) -> pd.DataFrame:
    rows = []
    for a, b, why in comparisons(data.keys, data.pg_ref):
        merged = data.paired_rows(a, b, PAIRED_METRICS)
        for metric in PAIRED_METRICS:
            row: dict[str, Any] = {"a": name(a), "b": name(b), "why": why, "metric": metric}
            result = data.difference(a, b, metric)
            if result is None:
                rows.append({**row, "note": "no shared question and replicate"})
                continue
            row.update({k: v for k, v in result.items() if k != "per_question"})
            row["mean_a"] = float(merged[f"{metric}_a"].mean())
            row["mean_b"] = float(merged[f"{metric}_b"].mean())
            if metric.startswith("recall") or metric == "latency_ms":
                row.update(wilcoxon(result["per_question"].to_numpy(float)))
            if metric.startswith("empty"):
                row.update(mcnemar(merged[f"{metric}_a"].to_numpy(float), merged[f"{metric}_b"].to_numpy(float)))
            rows.append(row)
    return pd.DataFrame(rows)


def explain_summary(explain: pd.DataFrame) -> pd.DataFrame:
    if explain.empty:
        return pd.DataFrame()
    ok = explain[explain["error"].fillna("") == ""].copy()
    if ok.empty:
        return pd.DataFrame()
    ok["empty"] = ok["n_hits"] == 0
    rows = []
    for (store, layout, setting, reason, k, empty), g in ok.groupby(
        ["store", "layout", "setting", "reason", "k", "empty"], sort=True
    ):
        rows.append(
            {
                "store": store,
                "layout": layout,
                "setting": setting,
                "reason": reason,
                "k": k,
                "empty": empty,
                "plans": len(g),
                "rows_emitted_median": g["rows_emitted"].median(),
                "removed_by_filter_median": g["removed_by_filter"].median(),
                "estimated_rows_median": g["estimated_rows"].median(),
                "execution_ms_median": g["execution_ms"].median(),
                "uses_hnsw": float(g["uses_hnsw"].astype(bool).mean()),
                "scan_nodes": json.dumps(g["scan_node"].value_counts().to_dict()),
            }
        )
    return pd.DataFrame(rows)


def plan_table(runs: pd.DataFrame) -> pd.DataFrame:
    """Amendment 2, item 3: per pgvector setting, over its builds ("all") and per build, how many
    first-pass searches had their executed plan captured, and the shares that searched the HNSW
    graph, the GIN index or the whole table, and that ran a generic plan."""
    if "plan5" not in runs:
        return pd.DataFrame()
    rows = []
    pg = runs[runs["store"] == "pgvector"]
    for (store, layout, setting), g in pg.groupby(["store", "layout", "setting"], sort=True):
        for build, part in [("all", g), *g.groupby("build", sort=True)]:
            kinds = pd.concat([part["plan5"], part["plan10"]], ignore_index=True)
            kinds = kinds[kinds != ""]
            generic = pd.concat([part["generic5"], part["generic10"]], ignore_index=True).dropna()
            if not len(kinds):
                continue
            rows.append(
                {
                    "store": store,
                    "layout": layout,
                    "setting": setting,
                    "build": build,
                    "captured": len(kinds),
                    "hnsw_share": float((kinds == "hnsw").mean()),
                    "gin_share": float((kinds == "gin").mean()),
                    "seq_share": float((kinds == "seq").mean()),
                    "generic_share": float(generic.mean()) if len(generic) else math.nan,
                    "meant_for_graph": setting != "ph-exact",
                }
            )
    return pd.DataFrame(rows)


def segment_path(telemetry: pd.DataFrame) -> str | None:
    """The JSON path of Qdrant's per-segment counters, or the busiest path if none names segments."""
    if telemetry.empty:
        return None
    totals = telemetry.groupby("path")["count"].sum().sort_values(ascending=False)
    segments = [p for p in totals.index if "segment" in str(p)]
    return segments[0] if segments else str(totals.index[0])


def path_table(data: Data) -> tuple[pd.DataFrame, str | None]:
    telemetry = data.telemetry
    path = segment_path(telemetry)
    if path is None:
        return pd.DataFrame(), None
    t = telemetry[telemetry["path"] == path]
    types = data.questions.groupby("person")["persona_type"].first()
    t = t.assign(persona_type=t["person"].map(types))
    counts = t.groupby(["store", "layout", "setting", "persona_type", "counter"], sort=True)["count"].sum()
    table = counts.unstack("counter", fill_value=0)
    filtered = [c for c in table.columns if str(c).startswith("filtered_")]
    total = table[filtered].sum(axis=1).replace(0, np.nan)
    for column in filtered:
        table[f"share_{column}"] = table[column] / total
    return table.reset_index(), path


def acorn_engagement(data: Data, path: str | None) -> tuple[pd.DataFrame, str]:
    """Q2: per person, whether qa-acorn040 searches took the ACORN path, from telemetry or inferred."""
    key = ("qdrant", "as-run", "qa-acorn040")
    # The rule infers engagement only when the telemetry does not expose the ACORN counter at all; when
    # it does, a person whose searches never took the ACORN path counts as not engaged.
    acorn = [m for m in data.metas if m.get("layout") == key[1] and m.get("setting") in (key[2], "qa-acorn100")]
    exposed = any(m.get("acorn_counter_seen") or (m.get("acorn_searches_counted") or 0) > 0 for m in acorn)
    t = data.telemetry
    if exposed and path is not None and not t.empty:
        t = t[(t["path"] == path) & (t["store"] == key[0]) & (t["layout"] == key[1]) & (t["setting"] == key[2])]
        per = t.pivot_table(index="person", columns="counter", values="count", aggfunc="sum", fill_value=0)
        acorn = per["filtered_acorn"] if "filtered_acorn" in per else pd.Series(0, index=per.index)
        large = per["filtered_large_cardinality"] if "filtered_large_cardinality" in per else 0 * acorn
        frame = pd.DataFrame({"acorn": acorn, "large_cardinality": large})
        frame = frame[(frame["acorn"] + frame["large_cardinality"]) > 0]
        frame["engaged"] = frame["acorn"] > 0
        return frame.reset_index(), "telemetry (filtered_acorn among people whose searches took a graph path)"
    # Inferred: a person is engaged when any of their top 5 differs from q-asrun's on the same build.
    merged = data.paired_rows(key, Q_REF, [])
    if merged.empty:
        return pd.DataFrame(), "unavailable"
    a = data.of(key, data.runs)[["qid", "rep", "hits5"]]
    b = data.of(Q_REF, data.runs)[["qid", "rep", "hits5"]]
    both = a.merge(b, on=["qid", "rep"], suffixes=("_a", "_b")).merge(data.questions[["qid", "person"]], on="qid")
    both["differs"] = both["hits5_a"] != both["hits5_b"]
    frame = both.groupby("person")["differs"].any().rename("engaged").reset_index()
    return frame, "inferred (top 5 differs from q-asrun on the same build): the telemetry did not count ACORN"


# ---- the pre-registered rules --------------------------------------------------------------------


def judged(name_: str, prediction: str, confirm: dict[str, Any], falsify: dict[str, Any], notes: str = "") -> dict:
    """A verdict: falsified if any falsifying condition holds; confirmed if every confirming one does."""
    if any(v is True for v in falsify.values()):
        verdict = "falsified"
    elif confirm and all(v is True for v in confirm.values()):
        verdict = "confirmed"
    else:
        verdict = "inconclusive"
    return {
        "hypothesis": name_,
        "prediction": prediction,
        "verdict": verdict,
        "confirm": confirm,
        "falsify": falsify,
        "notes": notes,
    }


def value(result: dict[str, Any] | None, field: str = "mean") -> float | None:
    return None if result is None else result[field]


def show(result: dict[str, Any] | None) -> str:
    if result is None:
        return "missing"
    return f"{result['mean']:.4f} [{result['low']:.4f}, {result['high']:.4f}]"


def q1(d: Data) -> dict:
    def judy(f: pd.DataFrame) -> pd.Series:
        return f["persona_type"] == "judy"

    def company(f: pd.DataFrame) -> pd.Series:
        return (f["persona_type"] == "kb-reader") & f["category"].isin(["targeted", "generic"]) & f["answerable"]

    judys, docs = d.estimate(Q_REF, "recall10", judy), d.estimate(Q_REF, "recall10", company)
    rows = d.of(Q_REF, d.runs)
    rows = rows[company(rows)]
    noncounting = rows["noncounting5"].sum()
    kb_share = float(rows["noncounting_kb5"].sum() / noncounting) if noncounting else None
    acorn = d.estimate(("qdrant", "as-run", "qa-acorn100"), "recall10")
    m0 = d.estimate(("qdrant", "tenant-m0", "q-asrun"), "recall10")
    best = max((v for v in (value(acorn), value(m0)) if v is not None), default=None)
    reference = d.of(Q_REF)
    misses = reference.dropna(subset=["recall10"]).groupby("category")["recall10"].agg(["mean", "count"])
    misses = misses[misses["count"] >= 30]
    spread = float((1 - misses["mean"]).max() - (1 - misses["mean"]).min()) if len(misses) >= 2 else None
    gains = [d.difference(("qdrant", "as-run", "qa-acorn100"), Q_REF, "recall10"),
             d.difference(("qdrant", "tenant-m0", "q-asrun"), Q_REF, "recall10")]
    no_gain = None if any(g is None for g in gains) else all(g["mean"] < 0.02 for g in gains)
    confirm = {
        f"(i) judy recall@10 {show(judys)} >= 0.95": None if judys is None else judys["mean"] >= 0.95,
        f"(ii) company-document recall@10 {show(docs)} <= 0.75, upper end below judy's lower end": None
        if judys is None or docs is None
        else docs["mean"] <= 0.75 and docs["high"] < judys["low"],
        f"(iii) kb/ share of non-counting top-5 hits {pc.cell(kb_share)} >= 0.5": None
        if kb_share is None
        else kb_share >= 0.5,
        f"(iv) best of ACORN 1.0 {show(acorn)} and tenant-m0 {show(m0)} >= 0.90": None if best is None else best >= 0.9,
    }
    falsify = {
        f"category miss-rate spread {pc.cell(spread)} < 0.10": None if spread is None else spread < 0.10,
        f"gains of ACORN 1.0 and tenant-m0 ({', '.join(pc.cell(value(g)) for g in gains)}) both < 0.02": no_gain,
    }
    return judged("Q1", "islanded permitted subgraph in Qdrant", confirm, falsify)


def q2(d: Data, engagement: pd.DataFrame, method: str) -> dict:
    share = float(engagement["engaged"].mean()) if len(engagement) else None
    diff = d.difference(("qdrant", "as-run", "qa-acorn100"), ("qdrant", "as-run", "qa-acorn040"), "recall10")
    confirm = {
        f"share of people ACORN 0.4 engaged for {pc.cell(share)} in (0.05, 0.95)": None
        if share is None
        else 0.05 < share < 0.95,
        f"ACORN 1.0 minus 0.4 in recall@10 {show(diff)} above 0": None if diff is None else diff["low"] > 0,
    }
    falsify = {
        "|ACORN 1.0 minus 0.4| < 0.01 with an interval containing 0": None
        if diff is None
        else abs(diff["mean"]) < 0.01 and diff["low"] <= 0 <= diff["high"]
    }
    return judged("Q2", "ACORN's default gate engages unreliably", confirm, falsify, f"engagement: {method}")


def segments_of(d: Data, layout: str) -> set[Any]:
    """The segment counts a layout's builds ended with: in run 2, the segments holding points
    (amendment 2, item 6); in run 1, Qdrant's segments_count."""
    found = set()
    for build in d.builds:
        if build.get("store") == "qdrant" and build.get("layout") == layout:
            counted = build.get("data_segments") if d.grid == "run2" else None
            found.add(json.dumps(counted if counted is not None else build.get("segments"), sort_keys=True))
    return found


def q3(d: Data, by_build: pd.DataFrame) -> dict:
    store, layout, setting = Q_REF
    ref = by_build[(by_build["store"] == store) & (by_build["layout"] == layout) & (by_build["setting"] == setting)]
    spread = float(ref["recall10"].max() - ref["recall10"].min()) if len(ref) >= 2 else None
    diff = d.difference(("qdrant", "one-segment", "q-asrun"), Q_REF, "recall10")
    same_segments = bool(segments_of(d, "as-run")) and segments_of(d, "as-run") == segments_of(d, "one-segment")
    confirm = {
        f"recall@10 range between as-run builds {pc.cell(spread)} >= 0.01": None if spread is None else spread >= 0.01,
        f"one-segment minus as-run {show(diff)} excludes 0": excludes_zero(diff),
    }
    falsify = {
        "range < 0.002 and |one-segment minus as-run| < 0.002": None
        if spread is None or diff is None
        else spread < 0.002 and abs(diff["mean"]) < 0.002
    }
    notes = f"segments: as-run {segments_of(d, 'as-run')}, one-segment {segments_of(d, 'one-segment')}"
    result = judged("Q3", "recall varies by build and segment layout", confirm, falsify, notes)
    if same_segments:
        result.update(verdict="inconclusive", notes=result["notes"] + "; both layouts ended with the same segments")
    return result


def q4(d: Data) -> dict:
    gain = d.difference(("qdrant", "as-run", "qb-ef512"), Q_REF, "recall10")
    g = value(gain)
    return judged(
        "Q4",
        "hnsw_ef 128 was not the cause",
        {f"hnsw_ef 512 minus 128 {show(gain)} < 0.05": None if g is None else g < 0.05},
        {"gain > 0.15": None if g is None else g > 0.15},
    )


def excluded_note(d: Data, keys: Sequence[Key]) -> str:
    left_out = [name(k) for k in keys if not d.usable(k)]
    return f"; left out, ran mostly exact (amendment 2): {left_out}" if left_out else ""


def p1(d: Data) -> dict:
    ref = d.pg_ref
    base = d.estimate(ref, "empty5") if d.usable(ref) else None
    if base is None or base["mean"] == 0:
        reproduced = {f"{ref[2]} reproduces empty results": None if base is None else False}
        why = f"no empty result under {ref[2]}" + excluded_note(d, [ref])
        return judged("P1", "the iterative scan's budget runs out", reproduced, {}, why)
    rows = d.of(ref, d.runs)
    empties = rows[rows["empty5"] == 1]
    explain = d.explain
    reach_rows = None
    if not explain.empty:
        e = explain[(explain["store"] == ref[0]) & (explain["layout"] == ref[1])]
        e = e[(e["setting"] == ref[2]) & (e["reason"] == "short") & (e["k"] == 5) & (e["n_hits"] == 0)]
        e = e[e["error"].fillna("") == ""]
        if len(e):
            reach_rows = float(e["rows_emitted"].median())
    reach = reach_rows if reach_rows is not None else 10_000.0
    share = float((empties["r1"] > reach / 2).mean()) if len(empties) else None
    raised = [(ref[0], ref[1], s) for s in RAISED]
    errs = {k[2]: value(d.estimate(k, "empty5")) if d.usable(k) else None for k in raised}
    lowest = min((v for v in errs.values() if v is not None), default=None)
    top = errs.get("pa-t1000k-m16")
    tuples_only = [errs[s] for s in ("pa-t100k-m1", "pa-t1000k-m1") if errs.get(s) is not None]
    memory_only = [errs[s] for s in ("pa-t20k-m8", "pb-wm64") if errs.get(s) is not None]
    binding = []
    if tuples_only and min(tuples_only) <= 0.1 * base["mean"]:
        binding.append("hnsw.max_scan_tuples")
    if memory_only and min(memory_only) <= 0.1 * base["mean"]:
        binding.append("scan memory (work_mem x hnsw.scan_mem_multiplier)")
    confirm = {
        f"(a) share of empties with r1 > {reach / 2:.0f} (half the reach {reach:.0f}"
        f"{'' if reach_rows is not None else ', no EXPLAIN: 10,000 assumed'}) {pc.cell(share)} >= 0.95": None
        if share is None
        else share >= 0.95,
        f"(b) lowest ERR of a raised limit {pc.cell(lowest)} <= 10% of {ref[2]}'s {base['mean']:.4f}": None
        if lowest is None
        else lowest <= 0.1 * base["mean"],
        f"(c) median rows emitted on empties {pc.cell(reach_rows)} in [10000, 25000]": None
        if reach_rows is None
        else 10_000 <= reach_rows <= 25_000,
    }
    falsify = {
        f"ERR at 1M tuples and 16x memory {pc.cell(top)} >= half of {ref[2]}'s": None
        if top is None
        else top >= 0.5 * base["mean"]
    }
    notes = f"reference {name(ref)}; empty results under it: {len(empties)}; "
    notes += f"ERR by raised limit: {json.dumps({k: v for k, v in errs.items() if v is not None})}; binding: "
    notes += ", ".join(binding) if binding else "no single-limit raise removed 90% of the empties"
    notes += excluded_note(d, raised)
    return judged("P1", "the iterative scan's budget runs out", confirm, falsify, notes)


def p2(d: Data) -> dict:
    base = d.pg_ref
    wide = (base[0], PG_WIDE, base[2])
    ef1000, lim10 = (base[0], base[1], "pc-ef1000"), (base[0], base[1], "pd-lim10")
    usable = d.usable(base)

    def diff(key: Key, against: Key) -> dict[str, Any] | None:
        return d.difference(key, against, "recall10") if usable and d.usable(key) and d.usable(against) else None

    a, b, c = diff(ef1000, base), diff(lim10, base), diff(wide, base)
    ref = d.of(base).dropna(subset=["recall10", "rho100"]) if usable else d.of(base).iloc[0:0]
    low, high = ref[ref["rho100"] < 0.1], ref[ref["rho100"] >= 0.1]
    loss_low = float((1 - low["recall10"]).mean()) if len(low) else None
    loss_high = float((1 - high["recall10"]).mean()) if len(high) else None
    concentrated = None if loss_low is None or loss_high is None else loss_low >= 2 * loss_high  # as written
    missed = ref[ref["recall10"] < 1]["sim_gap10"].dropna()
    gap = float(missed.mean()) if len(missed) else None
    confirm = {
        f"(a) ef_search 1000 minus 100 {show(a)} >= 0.02, above 0": None
        if a is None
        else a["mean"] >= 0.02 and a["low"] > 0,
        f"(b) inner LIMIT 10x minus 1x {show(b)} above 0": None if b is None else b["low"] > 0,
        f"(c) m32/efc200 minus m16/efc64 {show(c)} above 0": None if c is None else c["low"] > 0,
        f"(d) loss at rho_100 < 0.1 {pc.cell(loss_low)} at least twice the rest {pc.cell(loss_high)}": concentrated,
        f"(e) mean similarity gap of missed questions {pc.cell(gap)} <= 0.02": None if gap is None else gap <= 0.02,
    }
    falsify = {
        "|ef_search 1000 minus 100| < 0.01 with an interval containing 0": None
        if a is None
        else abs(a["mean"]) < 0.01 and a["low"] <= 0 <= a["high"]
    }
    notes = f"reference {name(base)}" + excluded_note(d, [base, ef1000, lim10, wide])
    return judged("P2", "mis-retrieval from shallow, relaxed scans", confirm, falsify, notes)


def p5(d: Data) -> dict:
    """Amendment 2, item 5: the plan cache decides whether pgvector searches the graph."""

    def original(f: pd.DataFrame) -> pd.Series:
        return ~f["persona_type"].astype(str).str.startswith("probe")

    def share(key: Key) -> float | None:
        rows = d.plans[(d.plans["setting"] == key[2]) & (d.plans["layout"] == key[1])] if not d.plans.empty else None
        rows = rows[rows["build"] == "all"] if rows is not None else None
        return float(rows["hnsw_share"].iloc[0]) if rows is not None and len(rows) else None

    def latency(key: Key, builds: set[str]) -> float | None:
        rows = d.of(key, d.runs)
        rows = rows[rows["build"].isin(builds)]["latency_ms"].dropna()
        return float(rows.median()) if len(rows) else None

    custom, auto = PG_CUSTOM, PG_REF
    rc, ra = d.estimate(custom, "recall5", original), d.estimate(auto, "recall5", original)
    sc, sa = share(custom), share(auto)
    shared = set(d.of(custom, d.runs)["build"]) & set(d.of(auto, d.runs)["build"])  # one shard per build
    lc, la = latency(custom, shared), latency(auto, shared)
    confirm = {
        f"(a) HNSW share under pg-custom {pc.cell(sc)} >= 0.9 and under p-asrun {pc.cell(sa)} <= 0.1": None
        if sc is None or sa is None
        else sc >= 0.9 and sa <= 0.1,
        f"(b) pg-custom recall@5 on the original questions {show(rc)} within 0.08 of {X0_RECALL5}": None
        if rc is None
        else abs(rc["mean"] - X0_RECALL5) <= 0.08,
        f"(c) p-asrun recall@5 on the original questions {show(ra)} >= 0.99, and its median latency "
        f"{pc.cell(la)} ms at least 10x pg-custom's {pc.cell(lc)} ms on builds {sorted(shared)}": None
        if ra is None or la is None or lc is None
        else ra["mean"] >= 0.99 and la >= 10 * lc,
    }
    falsify = {
        f"pg-custom HNSW share {pc.cell(sc)} >= 0.9 with recall@5 {show(rc)} >= 0.95": None
        if sc is None or rc is None
        else sc >= 0.9 and rc["mean"] >= 0.95,
        f"p-asrun HNSW share {pc.cell(sa)} >= 0.5": None if sa is None else sa >= 0.5,
    }
    replays = []
    for setting in ("p-x0", "p-x0v"):
        key = (PG_REF[0], PG_REF[1], setting)
        recall = d.estimate(key, "recall5", original)
        metas = [m for m in d.metas if m.get("setting") == setting and m.get("status") == "done"]
        generic = sum(int((m.get("prepared_statements") or {}).get("search_generic_plans") or 0) for m in metas)
        pending = []
        for m in metas:
            gin = (m.get("table_state_before") or {}).get("gin_metapage")
            pending.append(gin.get("n_pending_pages") if isinstance(gin, dict) else None)
        replays.append(
            f"{setting}: recall@5 {show(recall)}, HNSW share {pc.cell(share(key))}, generic plans {generic}, "
            f"GIN pending pages before {pending}"
        )
    notes = "; ".join(replays)
    return judged("P5", "the plan cache decides whether pgvector searches the graph", confirm, falsify, notes)


def p3(d: Data) -> dict:
    estimates = d.estimates
    ratios = None
    if estimates is not None and not estimates.empty:
        ratios = estimates.loc[estimates["persona_type"] == "judy", "ratio"].dropna()
    median = float(ratios.median()) if ratios is not None and len(ratios) else None
    exact = value(d.estimate((PG_REF[0], PG_REF[1], "ph-exact"), "empty5"))
    confirm = {
        f"median planner estimate / R for judys {pc.cell(median)} >= 5": None if median is None else median >= 5,
        f"ph-exact ERR {pc.cell(exact)} == 0": None if exact is None else exact == 0,
    }
    falsify = {"median ratio within [0.5, 2]": None if median is None else 0.5 <= median <= 2}
    return judged("P3", "the planner overestimates a judy filter", confirm, falsify)


def generic_plan_evidence(d: Data) -> tuple[int | None, int | None, int]:
    """P4 as amended: how often PostgreSQL ran the search statement with a generic plan under p-asrun
    (pg_prepared_statements, summed over builds), and for how many fixed questions the generic plan
    (EXPLAIN (GENERIC_PLAN)) has another shape than the custom plan (EXPLAIN ANALYZE with the values)."""
    metas = [m for m in d.metas if (m.get("store"), m.get("layout"), m.get("setting")) == PG_REF]
    metas = [m for m in metas if "search_generic_plans" in (m.get("prepared_statements") or {})]
    used =sum(int(m["prepared_statements"]["search_generic_plans"]) for m in metas) if metas else None
    e = d.explain
    if e.empty or "generic_plan_shape" not in e:
        return used, None, 0
    e = e[(e["store"] == PG_REF[0]) & (e["layout"] == PG_REF[1]) & (e["setting"] == PG_REF[2])]
    e = e[(e["reason"] == "fixed") & (e["error"].fillna("") == "")]
    explained = e[e["generic_plan_shape"].fillna("") != ""]
    differ = int((explained["plan_shape"] != explained["generic_plan_shape"]).sum()) if len(explained) else None
    return used, differ, len(explained)


def p4(d: Data) -> dict:
    confirm: dict[str, Any] = {}
    falsify: dict[str, Any] = {}
    for setting in ("pg-custom", "pg-noprepare"):
        key = (PG_REF[0], PG_REF[1], setting)
        recall = d.difference(key, PG_REF, "recall10")
        err = d.difference(key, PG_REF, "empty5")
        rows = d.paired_rows(key, PG_REF, ["empty5"]) if key in d.keys else pd.DataFrame()
        test = mcnemar(rows["empty5_a"].to_numpy(float), rows["empty5_b"].to_numpy(float)) if len(rows) else None
        confirm[f"{setting}: |recall@10 difference| {show(recall)} < 0.005"] = (
            None if recall is None else abs(recall["mean"]) < 0.005
        )
        confirm[f"{setting}: |ERR difference| {show(err)} < 0.002"] = None if err is None else abs(err["mean"]) < 0.002
        falsify[f"{setting}: |recall@10 difference| >= 0.01, interval excluding 0"] = (
            None if recall is None else abs(recall["mean"]) >= 0.01 and bool(excludes_zero(recall))
        )
        falsify[f"{setting}: McNemar p for ERR {pc.cell(None if test is None else test['mcnemar_p'])} < 0.05"] = (
            None if test is None else test["mcnemar_p"] < 0.05
        )
    used, differ, explained = generic_plan_evidence(d)
    plan_ok = None if used is None else used == 0 or (differ is not None and differ == 0)
    plan_bad = None if used is None else used > 0 and differ is not None and differ > 0
    if used == 0:
        plan_bad = False
    plan = f"generic plans run under p-asrun: {used}; fixed questions with another generic plan: {differ} of {explained}"
    confirm[f"{plan}: none run, or none differs"] = plan_ok
    falsify[f"{plan}: some run and some differ"] = plan_bad
    generic: dict[str, int] = {}
    for m in d.metas:
        wanted = m.get("setting") in (PG_REF[2], "pg-custom", "pg-noprepare") and m.get("status") == "done"
        if wanted and m.get("store") == PG_REF[0] and m.get("layout") == PG_REF[1]:
            plans = (m.get("prepared_statements") or {}).get("search_generic_plans") or 0
            generic[m["setting"]] = generic.get(m["setting"], 0) + int(plans)
    notes = f"generic plans of the search statement, summed over builds, per setting: {generic} (amendment 1)"
    return judged("P4", "generic plans make no difference", confirm, falsify, notes)


# ---- report --------------------------------------------------------------------------------------


def report(data: Data, settings: pd.DataFrame, predictions: list[dict], path_note: str | None) -> str:
    missing = [m for m in data.metas if m.get("status") in ("unsupported", "failed")]
    folders = ", ".join(f"`{f}`" for f in data.folders)
    lines = [
        "# X1: under-retrieval under permission filters, statistics",
        "",
        f"Input: {folders} (grid {data.grid}); {len(data.runs):,} result rows of {len(data.keys)} settings; "
        f"{data.resamples:,} bootstrap resamples, seed {data.seed}. Verdicts follow PREREGISTRATION.md"
        + (", with amendment 2: P1 and P2 read `pg-custom` where they say `p-asrun`." if data.grid == "run2" else "."),
        "",
        "## Verdicts",
        "",
    ]
    for p in predictions:
        lines += [f"### {p['hypothesis']}: {p['verdict']} ({p['prediction']})", ""]
        lines += [f"- confirm: {k}: **{v}**" for k, v in p["confirm"].items()]
        lines += [f"- falsify: {k}: **{v}**" for k, v in p["falsify"].items()]
        if p["notes"]:
            lines.append(f"- notes: {p['notes']}")
        lines.append("")
    lines += ["## Settings (means over builds; range between builds)", ""]
    columns = ["store", "layout", "setting", "builds", "recall5", "recall10", "recall10_range", "empty5", "short5"]
    columns += ["gross_miss10", "sim_gap10", "latency_p50"]
    lines += pc.frame_table(settings, columns)
    if not data.plans.empty:
        lines += [
            "## pgvector: the plans the searches executed (auto_explain, first pass; amendment 2)",
            "",
            f"A setting meant to search the HNSW graph with an HNSW share below {HNSW_SHARE_FLOOR} ran mostly exact"
            f" and is left out of P1 and P2: {sorted(name(k) for k in data.mostly_exact) or 'none'}.",
            "",
        ]
        overall = data.plans[data.plans["build"] == "all"]
        lines += pc.frame_table(overall, ["layout", "setting", "captured", "hnsw_share", "gin_share", "generic_share"])
    if missing:
        lines += ["## Settings that did not run", ""]
        for m in missing:
            trace = (m.get("trace") or "").strip().splitlines()
            why = m.get("reason") or (trace[-1] if trace else "no reason recorded")
            lines.append(f"- {m.get('store')} {m.get('build')} {m.get('setting')}: {m.get('status')}, {why}")
        lines.append("")
    if path_note:
        lines += [f"Qdrant search paths were read from the telemetry path `{path_note}`.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Experiment X1: statistics and pre-registered verdicts")
    parser.add_argument("--in", dest="folders", type=Path, nargs="+", default=[Path("/kaggle/working/x1run2")])
    parser.add_argument("--out", type=Path, default=None, help="default <the first --in>/stats")
    parser.add_argument("--resamples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=pc.SEED)
    args = parser.parse_args(argv)
    out = args.out or args.folders[0] / "stats"
    out.mkdir(parents=True, exist_ok=True)
    log.to(out / "x1_stats.log")
    started = time.perf_counter()
    data = Data(args.folders, args.resamples, args.seed)

    by_build = build_summary(data.runs)
    settings = setting_summary(by_build)
    tables: dict[str, pd.DataFrame] = {"summary_by_build": by_build, "summary_by_setting": settings}
    log("intervals")
    tables["intervals"] = interval_table(data)
    log("paired comparisons")
    tables["paired"] = paired_table(data)
    tables["explain_summary"] = explain_summary(data.explain)
    paths, path = path_table(data)
    tables["qdrant_paths"] = paths
    engagement, method = acorn_engagement(data, path)
    tables["acorn_engagement"] = engagement
    tables["plans"] = data.plans

    log("pre-registered verdicts")
    predictions = [q1(data), q2(data, engagement, method), q3(data, by_build), q4(data), p1(data), p2(data)]
    predictions += [p3(data), p4(data)]
    if data.grid == "run2":
        predictions.append(p5(data))
    tables["predictions"] = pd.DataFrame(
        [{**p, "confirm": json.dumps(p["confirm"]), "falsify": json.dumps(p["falsify"])} for p in predictions]
    )
    for key, table in tables.items():
        table.to_csv(out / f"{key}.csv", index=False)
        log(f"wrote {out / key}.csv ({len(table):,} rows)")
    (out / "report.md").write_text(report(data, settings, predictions, path), encoding="utf-8")
    pc.write_json(
        out / "manifest.json",
        {
            "experiment": "X1 statistics",
            "input": [str(f) for f in args.folders],
            "grid": data.grid,
            "resamples": args.resamples,
            "seed": args.seed,
            "settings": sorted(name(k) for k in data.keys),
            "verdicts": {p["hypothesis"]: p["verdict"] for p in predictions},
            "versions": pc.versions(["numpy", "pandas", "scipy", "pyarrow"]),
            "seconds": round(time.perf_counter() - started, 1),
        },
    )
    for p in predictions:
        log(f"{p['hypothesis']}: {p['verdict']}")
    log(f"X1 statistics done in {time.perf_counter() - started:.0f} s: {out / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
