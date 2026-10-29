"""Statistics of experiments X2 and X5: tables, intervals and the pre-registered verdicts.

    python x2x5_stats.py --results results/ --meta-e data-e/ --meta-m data-m/ --out stats/

`--results` holds the jobs' folders (rows/*.jsonl.gz and job.json each); `--meta-*` the prepared
corpus folders (only their small files are read: pairs.csv, subjects.json, people.json,
config.json). PREREG_X2_X5.md, sections 7 and 8, define every number here; this script applies
those rules and nothing else, and prints each verdict with the numbers behind each criterion.
Intervals are 95% percentile intervals from a cluster bootstrap over subjects (E: people; M:
subjects, within their (seed, family, level, shape) stratum). Writes CSV tables, verdicts.json and
report.md (a shorter summary.md for the job summary).
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import defaultdict
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import x2x5_common as xc
from x2x5_common import log

APPROXIMATE = ("pgvector", "qdrant", "elasticsearch", "opensearch", "weaviate", "redis", "milvus", "mongodb", "lancedb",
               "chroma")  # fmt: skip
MAIN_LAYOUT = {"qdrant": "as-run"}  # every other store's main layout is "default"
X0 = {"redis": 0.980, "elasticsearch": 0.948, "opensearch": 0.938, "weaviate": 0.892, "chroma": 0.883,
      "lancedb": 0.860, "pgvector": 0.732, "qdrant": 0.561, "faiss": 1.000}  # fmt: skip
MID_LEVELS = (2, 3, 4)  # 2%, 10%, 30%
REPAIR_ARMS = ("count", "exact-1k", "exact-10k", "exact-inf", "widen")
LIBRARY_ARMS = ("report", *REPAIR_ARMS, "monitor")
SCALARS = (
    "exp", "corpus", "store", "layout", "build", "setting", "kind", "level", "asrun", "job", "pid", "err",
    "n5", "recall5", "rid5", "max5", "empty5", "short5", "gross5", "gap5", "complete5", "shortfall5", "fallback5",
    "sfms5", "sampled5", "n10", "recall10", "rid10", "max10", "empty10", "short10", "gross10", "gap10",
    "complete10", "shortfall10", "fallback10", "sfms10", "sampled10", "plan10",
)  # fmt: skip


# ---- loading ----------------------------------------------------------------------------------------


def load_rows(results: Path) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    samples: list[dict[str, Any]] = []
    for path in sorted(results.glob("**/rows/*.jsonl.gz")):
        for r in xc.read_jsonl_gz(path):
            rec = {key: r.get(key) for key in SCALARS}
            lat = r.get("lat") or []
            rec["passes"] = len(lat)
            for p in range(3):
                rec[f"lat{p}"] = lat[p] if len(lat) > p else math.nan
            rec["lat"] = float(np.median(lat)) if lat else math.nan
            slat = [x for x in (r.get("slat") or []) if x is not None]
            rec["slat"] = float(np.median(slat)) if slat else math.nan
            for k in (5, 10):
                calls = r.get(f"calls{k}") or []
                rec[f"first{k}"] = calls[0][2] if calls and calls[0][0] == "search" else math.nan
                counted = [c[2] for c in calls if c[0] == "count"]
                rec[f"counted{k}"] = counted[0] if counted and counted[0] is not None else math.nan
            triggered = [x[1] for x in r.get("sfms_passes") or []]
            if r.get("shortfall10") is not None and r.get("sfms10") is not None:
                triggered.append(r["sfms10"])
            rec["sfms_med"] = float(np.median(triggered)) if triggered else math.nan
            records.append(rec)
            for s in r.get("samples") or []:
                samples.append(
                    {"corpus": r.get("corpus"), "store": r.get("store"), "layout": r.get("layout"),
                     "build": r.get("build"), "setting": r.get("setting"), "pid": r.get("pid"), "pass": s[0],
                     "k": s[1], "sampled": s[2], "rid": s[3]}  # fmt: skip
                )
    frame = pd.DataFrame(records)
    log(f"{len(frame):,} rows from {results}, {len(samples):,} sampled-recall records")
    return frame, samples


def load_jobs(results: Path) -> list[dict[str, Any]]:
    jobs = []
    for path in sorted(results.glob("**/job.json")):
        with open(path, encoding="utf-8") as handle:
            job = json.load(handle)
        job["leaked"] = (path.parent / "LEAK.json").is_file()
        jobs.append(job)
    return jobs


def load_pairs(folder: Path | None, corpus: str) -> pd.DataFrame:
    if folder is None or not (folder / "pairs.csv").is_file():
        return pd.DataFrame()
    frame = pd.read_csv(folder / "pairs.csv")
    frame["corpus"] = corpus
    return frame.drop(columns=[c for c in ("top_rows", "top_scores", "question") if c in frame])


def subjects_of(folder: Path | None, corpus: str) -> pd.DataFrame:
    """Every subject of a corpus with its bootstrap stratum."""
    if folder is None:
        return pd.DataFrame(columns=["sid", "stratum", "corpus"])
    if corpus == xc.M_NAME and (folder / "subjects.json").is_file():
        subjects = xc.read_json(folder / "subjects.json")
        rows = [{"sid": s["sid"], "stratum": f"m:{s['family']}{s['seed']}:{s['level']}:{s['shape']}"} for s in subjects]
    elif (folder / "people.json").is_file():
        rows = [{"sid": p["id"], "stratum": "e"} for p in xc.read_json(folder / "people.json")]
    else:
        rows = []
    frame = pd.DataFrame(rows, columns=["sid", "stratum"])
    frame["corpus"] = corpus
    return frame


# ---- the bootstrap ----------------------------------------------------------------------------------


class Boot:
    """Cluster bootstrap over subjects, stratified: W[b, s] is how often subject s was drawn in b."""

    def __init__(self, subjects: pd.DataFrame, resamples: int, seed: int = xc.SEED) -> None:
        keys = [f"{c}:{s}" for c, s in zip(subjects["corpus"], subjects["sid"], strict=True)]
        self.index = {key: i for i, key in enumerate(keys)}
        rng = np.random.default_rng(seed)
        self.W = np.zeros((resamples, len(keys)), dtype=np.float64)
        groups: dict[str, list[int]] = defaultdict(list)
        for i, stratum in enumerate(subjects["stratum"]):
            groups[stratum].append(i)
        for stratum in sorted(groups):
            members = np.asarray(groups[stratum])
            n = len(members)
            draws = rng.integers(0, n, size=(resamples, n))
            flat = (draws + np.arange(resamples)[:, None] * n).ravel()
            self.W[:, members] = np.bincount(flat, minlength=resamples * n).reshape(resamples, n)

    def idx(self, frame: pd.DataFrame) -> np.ndarray:
        return np.array([self.index[f"{c}:{s}"] for c, s in zip(frame["corpus"], frame["sid"], strict=True)], dtype=int)

    def ratio(self, idx: np.ndarray, num: np.ndarray, den: np.ndarray) -> tuple[float, np.ndarray]:
        """sum(num) / sum(den) over observations, and its bootstrap replicates."""
        size = self.W.shape[1]
        ok = ~(np.isnan(num) | np.isnan(den))
        s_num = np.bincount(idx[ok], weights=num[ok], minlength=size)
        s_den = np.bincount(idx[ok], weights=den[ok], minlength=size)
        total = s_den.sum()
        estimate = float(s_num.sum() / total) if total else math.nan
        with np.errstate(invalid="ignore", divide="ignore"):
            boot = (self.W @ s_num) / (self.W @ s_den)
        return estimate, boot

    def mean(self, idx: np.ndarray, values: np.ndarray) -> tuple[float, np.ndarray]:
        values = np.asarray(values, dtype=float)
        return self.ratio(idx, values, np.where(np.isnan(values), np.nan, 1.0))


def interval(boot: np.ndarray) -> tuple[float, float]:
    finite = boot[np.isfinite(boot)]
    if not len(finite):
        return math.nan, math.nan
    lo, hi = np.percentile(finite, [2.5, 97.5])
    return float(lo), float(hi)


def excludes_zero(lo: float, hi: float) -> bool:
    return bool(np.isfinite(lo) and np.isfinite(hi) and (lo > 0 or hi < 0))


# ---- weighted Spearman (H2.2) -----------------------------------------------------------------------


class Ranked:
    """A variable sorted once, so that average ranks under bootstrap weights cost O(n)."""

    def __init__(self, values: np.ndarray) -> None:
        self.order = np.argsort(values, kind="mergesort")
        ordered = values[self.order]
        self.group = np.concatenate(([0], np.cumsum(ordered[1:] != ordered[:-1])))

    def ranks(self, weights: np.ndarray) -> np.ndarray:
        w = weights[self.order]
        totals = np.bincount(self.group, weights=w)
        ends = np.cumsum(totals)
        average = ends - totals + (totals + 1.0) / 2.0
        out = np.empty_like(w)
        out[self.order] = average[self.group]
        return out


def weighted_pearson(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    total = w.sum()
    if total <= 0:
        return math.nan
    mx, my = (w * x).sum() / total, (w * y).sum() / total
    dx, dy = x - mx, y - my
    vx, vy = (w * dx * dx).sum(), (w * dy * dy).sum()
    if vx <= 0 or vy <= 0:
        return math.nan
    return float((w * dx * dy).sum() / math.sqrt(vx * vy))


def spearman_boot(boot: Boot, idx: np.ndarray, x: np.ndarray, y: np.ndarray) -> tuple[float, np.ndarray]:
    rx, ry = Ranked(x), Ranked(y)
    ones = np.ones(len(x))
    estimate = weighted_pearson(rx.ranks(ones), ry.ranks(ones), ones)
    reps = np.empty(boot.W.shape[0])
    for b in range(boot.W.shape[0]):
        w = boot.W[b, idx]
        reps[b] = weighted_pearson(rx.ranks(w), ry.ranks(w), w)
    return estimate, reps


# ---- plain tests, reported beside the rules -------------------------------------------------------------


def wilcoxon(diff: np.ndarray) -> float:
    """Two-sided p of the Wilcoxon signed-rank test, normal approximation, zeros dropped, ties averaged."""
    d = diff[np.isfinite(diff) & (diff != 0)]
    n = len(d)
    if n < 10:
        return math.nan
    ranks = Ranked(np.abs(d)).ranks(np.ones(n))
    w_plus = ranks[d > 0].sum()
    mean = n * (n + 1) / 4.0
    _, counts = np.unique(np.abs(d), return_counts=True)
    var = n * (n + 1) * (2 * n + 1) / 24.0 - (counts**3 - counts).sum() / 48.0
    if var <= 0:
        return math.nan
    z = (w_plus - mean) / math.sqrt(var)
    return float(math.erfc(abs(z) / math.sqrt(2)))


def mcnemar(a: np.ndarray, b: np.ndarray) -> float:
    """Exact two-sided McNemar p for two paired binary outcomes."""
    ok = np.isfinite(a) & np.isfinite(b)
    x = int(((a[ok] == 1) & (b[ok] == 0)).sum())
    y = int(((a[ok] == 0) & (b[ok] == 1)).sum())
    n = x + y
    if n == 0:
        return 1.0
    low = min(x, y)
    logs = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) - n * math.log(2) for i in range(low + 1)]
    top = max(logs)
    tail = math.exp(top) * sum(math.exp(v - top) for v in logs)
    return float(min(1.0, 2 * tail))


# ---- the analysis -------------------------------------------------------------------------------------


class Analysis:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.out: Path = args.out
        self.out.mkdir(parents=True, exist_ok=True)
        self.rows, self.samples = load_rows(args.results)
        self.jobs = load_jobs(args.results)
        pairs = [load_pairs(args.meta_e, xc.E_NAME), load_pairs(args.meta_m, xc.M_NAME)]
        self.pairs = pd.concat([p for p in pairs if len(p)], ignore_index=True) if any(len(p) for p in pairs) else pd.DataFrame()
        subjects = pd.concat([subjects_of(args.meta_e, xc.E_NAME), subjects_of(args.meta_m, xc.M_NAME)], ignore_index=True)
        self.boot = Boot(subjects, args.resamples)
        self.verdicts: dict[str, Any] = {}
        self.report: list[str] = []
        self.subjects_m = pd.DataFrame(xc.read_json(args.meta_m / "subjects.json")) if args.meta_m and (
            args.meta_m / "subjects.json"
        ).is_file() else pd.DataFrame()
        if len(self.rows) and len(self.pairs):
            self.rows = self.rows.merge(self.pairs, on=["corpus", "pid"], how="left", suffixes=("", "_pair"))
        self.pair_level = self.collapse(self.rows) if len(self.rows) else pd.DataFrame()

    # -- helpers --

    @staticmethod
    def collapse(rows: pd.DataFrame) -> pd.DataFrame:
        """A pair's metric in a setting is its mean over the builds that setting ran on."""
        metrics = [c for c in ("recall5", "recall10", "rid5", "rid10", "max5", "max10", "empty5", "empty10", "short5",
                               "short10", "gross10", "gap10", "complete5", "complete10", "lat", "slat") if c in rows]  # fmt: skip
        frame = rows[rows["err"].isna()].copy() if "err" in rows else rows.copy()
        for c in metrics:
            frame[c] = pd.to_numeric(frame[c], errors="coerce")
        keys = ["exp", "corpus", "store", "layout", "setting", "pid"]
        grouped = frame.groupby(keys, dropna=False)
        out = grouped[metrics].mean().reset_index()
        out["builds"] = grouped["build"].nunique().values
        first = grouped[["kind", "level", "asrun"]].first().reset_index(drop=True)
        out[["kind", "level", "asrun"]] = first.values
        attributes = [c for c in rows.columns if c not in rows.columns.intersection(metrics) and c not in keys]
        attributes = [c for c in attributes if c in ("sid", "family", "seed", "level_pair", "nominal", "shape", "regime",
                                                       "person_type", "category", "original", "R", "sigma", "acorn",
                                                       "gls", "alpha", "rho100", "rho1000", "r1", "r10")]  # fmt: skip
        if attributes:
            attrs = frame.groupby(keys, dropna=False)[attributes].first().reset_index()
            out = out.merge(attrs, on=keys, how="left")
        return out

    def select(self, frame: pd.DataFrame, **match: Any) -> pd.DataFrame:
        mask = np.ones(len(frame), dtype=bool)
        for key, value in match.items():
            if isinstance(value, (list, tuple, set)):
                mask &= frame[key].isin(list(value)).to_numpy()
            else:
                mask &= (frame[key] == value).to_numpy()
        return frame[mask]

    def mean_ci(self, frame: pd.DataFrame, column: str) -> dict[str, Any]:
        if not len(frame):
            return {"est": math.nan, "lo": math.nan, "hi": math.nan, "n": 0}
        est, boot = self.boot.mean(self.boot.idx(frame), frame[column].to_numpy(dtype=float))
        lo, hi = interval(boot)
        return {"est": est, "lo": lo, "hi": hi, "n": int(frame[column].notna().sum())}

    def main_layout(self, store: str) -> str:
        return MAIN_LAYOUT.get(store, "default")

    def x2m(self, store: str, setting: str) -> pd.DataFrame:
        p = self.pair_level
        if not len(p):
            return p
        return p[(p["exp"] == "x2") & (p["corpus"] == xc.M_NAME) & (p["store"] == store)
                 & (p["layout"] == self.main_layout(store)) & (p["setting"] == setting)]  # fmt: skip

    def gap(self, frame: pd.DataFrame, a: pd.DataFrame, b: pd.DataFrame) -> tuple[float, np.ndarray]:
        ea, ba = self.boot.mean(self.boot.idx(a), a["recall10"].to_numpy(dtype=float))
        eb, bb = self.boot.mean(self.boot.idx(b), b["recall10"].to_numpy(dtype=float))
        return ea - eb, ba - bb

    def seeds_hold(self, frame: pd.DataFrame, statistic: Callable[[pd.DataFrame], float], sign: int = 1) -> int:
        """In how many layout seeds the statistic has the given sign."""
        held = 0
        for seed in sorted(frame["seed"].dropna().unique()):
            value = statistic(frame[frame["seed"] == seed])
            held += bool(np.isfinite(value) and value * sign > 0)
        return held

    def record(self, hid: str, verdict: str, criteria: list[str], data: dict[str, Any] | None = None) -> None:
        self.verdicts[hid] = {"verdict": verdict, "criteria": criteria, "data": data or {}}
        log(f"{hid}: {verdict}")
        for line in criteria:
            log(f"   {line}")

    def write(self, frame: pd.DataFrame, name: str) -> None:
        frame.to_csv(self.out / f"{name}.csv", index=False)

    # -- X2 tables --

    def x2_tables(self) -> None:
        p = self.pair_level
        x2 = p[p["exp"] == "x2"] if len(p) else p
        if not len(x2):
            return
        rows = []
        for (corpus, store, layout, setting), frame in x2.groupby(["corpus", "store", "layout", "setting"]):
            ci = self.mean_ci(frame, "recall10")
            raw = self.select(self.rows, exp="x2", corpus=corpus, store=store, layout=layout, setting=setting)
            lat = raw["lat"].dropna()
            rows.append(
                {"corpus": corpus, "store": store, "layout": layout, "setting": setting,
                 "kind": frame["kind"].iloc[0], "level": frame["level"].iloc[0], "asrun": frame["asrun"].iloc[0],
                 "pairs": ci["n"], "builds": int(frame["builds"].max()), "recall10": ci["est"], "lo": ci["lo"],
                 "hi": ci["hi"], "err10": frame["empty10"].mean(), "short10": frame["short10"].mean(),
                 "gross10": frame["gross10"].mean(),
                 "p50_ms": lat.quantile(0.5) if len(lat) else math.nan,
                 "p95_ms": lat.quantile(0.95) if len(lat) else math.nan,
                 "p99_ms": lat.quantile(0.99) if len(lat) else math.nan}  # fmt: skip
            )
        settings = pd.DataFrame(rows)
        self.write(settings, "x2_settings")
        self.write(self.frontier(), "x2_frontier")
        builds = (
            self.rows[self.rows["exp"] == "x2"]
            .assign(recall10=lambda f: pd.to_numeric(f["recall10"], errors="coerce"))
            .groupby(["corpus", "store", "layout", "setting", "build"])["recall10"].mean().reset_index()
        )
        spread = builds.groupby(["corpus", "store", "layout", "setting"])["recall10"].agg(["count", "min", "max", "std"])
        spread["range"] = spread["max"] - spread["min"]
        self.write(spread.reset_index(), "x2_builds")
        self.write(self.axis_table(), "x2_axes")
        self.write(self.plan_table(), "x2_pgvector_plans")
        self.settings_table = settings

    def cell_keys(self, frame: pd.DataFrame) -> pd.Series:
        if "regime" in frame and frame["regime"].notna().any():
            return frame["family"].astype(str) + "-" + frame["regime"].astype(str) + "-" + frame["level_pair"].astype(
                "Int64"
            ).astype(str) + "-" + frame["shape"].astype(str)
        return frame["person_type"].astype(str) if "person_type" in frame else pd.Series("all", index=frame.index)

    def frontier(self) -> pd.DataFrame:
        """Recall@10 and single-client QPS per (store, layout, build, setting, cell), within one job each."""
        raw = self.rows[self.rows["exp"] == "x2"].copy()
        if not len(raw):
            return pd.DataFrame()
        raw["recall10"] = pd.to_numeric(raw["recall10"], errors="coerce")
        out = []
        for corpus, frame in raw.groupby("corpus"):
            frame = frame.copy()
            frame["cell"] = self.cell_keys(frame)
            pooled = frame.assign(cell="all")
            for (store, layout, build, setting, cell), part in pd.concat([frame, pooled]).groupby(
                ["store", "layout", "build", "setting", "cell"]
            ):
                qps = []
                for p in range(3):
                    lat = part[f"lat{p}"].dropna()
                    if len(lat):
                        qps.append(1000.0 * len(lat) / lat.sum())
                out.append(
                    {"corpus": corpus, "store": store, "layout": layout, "build": build, "setting": setting,
                     "cell": cell, "job": part["job"].iloc[0], "pairs": int(part["recall10"].notna().sum()),
                     "recall10": part["recall10"].mean(), "qps": float(np.median(qps)) if qps else math.nan,
                     "p50_ms": part["lat"].median()}  # fmt: skip
                )
        return pd.DataFrame(out)

    def axis_table(self) -> pd.DataFrame:
        p = self.pair_level
        frame = p[(p["exp"] == "x2") & (p["setting"] == "default")].copy() if len(p) else p
        if not len(frame) or "rho1000" not in frame:
            return pd.DataFrame()
        bins = {
            "sigma": ([0, 1e-3, 1e-2, 1e-1, 1.0001], None),
            "rho1000": ([-0.001, 0.0, 0.01, 0.1, 0.5, 1.0001], None),
            "gls": ([-1.0001, -0.3, 0.3, 1.0001], None),
            "log10_r1": ([-0.001, 1, 2, 3, 4, 5, 7], None),
        }
        frame["log10_r1"] = np.log10(pd.to_numeric(frame["r1"], errors="coerce"))
        out = []
        for axis, (edges, _) in bins.items():
            frame[f"{axis}_bin"] = pd.cut(pd.to_numeric(frame[axis], errors="coerce"), edges)
        for axis in ("acorn", "alpha"):
            values = pd.to_numeric(frame[axis], errors="coerce")
            frame[f"{axis}_bin"] = pd.qcut(values, 5, duplicates="drop") if values.notna().sum() >= 5 else np.nan
        for axis in ("sigma", "rho1000", "gls", "log10_r1", "acorn", "alpha"):
            grouped = frame.groupby(["corpus", "store", "layout", f"{axis}_bin"], observed=True)["recall10"]
            for (corpus, store, layout, b), values in grouped:
                out.append({"corpus": corpus, "store": store, "layout": layout, "axis": axis, "bin": str(b),
                            "pairs": int(values.notna().sum()), "recall10": values.mean()})  # fmt: skip
        return pd.DataFrame(out)

    def plan_table(self) -> pd.DataFrame:
        raw = self.rows[(self.rows["exp"] == "x2") & (self.rows["store"] == "pgvector")].copy()
        if not len(raw) or "plan10" not in raw:
            return pd.DataFrame()
        parts = []
        for _, frame in raw.groupby("corpus"):
            frame = frame.assign(cell=self.cell_keys(frame), hnsw=(frame["plan10"] == "hnsw").astype(float))
            parts.append(frame.groupby(["corpus", "setting", "cell"])["hnsw"].agg(["mean", "count"]).reset_index())
            pooled = frame.groupby(["corpus", "setting"])["hnsw"].agg(["mean", "count"]).reset_index()
            parts.append(pooled.assign(cell="all"))
        return pd.concat(parts, ignore_index=True)

    # -- X2 verdicts --

    def h21(self) -> dict[str, dict[str, Any]]:
        per_store: dict[str, dict[str, Any]] = {}
        for store in APPROXIMATE:
            frame = self.x2m(store, "default")
            if not len(frame):
                continue
            mid = frame[frame["level_pair"].isin(MID_LEVELS)]
            u, n = mid[mid["regime"] == "U"], mid[mid["regime"] == "N"]
            if not len(u) or not len(n):
                continue
            g, boot = self.gap(mid, u, n)
            lo, hi = interval(boot)

            def stat(part: pd.DataFrame) -> float:
                a, b = part[part["regime"] == "U"]["recall10"], part[part["regime"] == "N"]["recall10"]
                return float(a.mean() - b.mean()) if len(a) and len(b) else math.nan

            seeds = self.seeds_hold(mid, stat)
            outcome = "unclear"
            if g >= 0.05 and lo > 0 and seeds >= 4:
                outcome = "gap"
            elif abs(g) < 0.02 and lo > -0.03 and hi < 0.03:
                outcome = "no gap"
            per_store[store] = {"G": g, "lo": lo, "hi": hi, "seeds_positive": seeds, "outcome": outcome,
                                "pairs_u": len(u), "pairs_n": len(n), "boot": boot}  # fmt: skip
        gaps = [s for s, v in per_store.items() if v["outcome"] == "gap"]
        none = [s for s, v in per_store.items() if v["outcome"] == "no gap"]
        verdict = "confirmed" if len(gaps) >= 6 else "falsified" if len(none) >= 5 else "inconclusive"
        criteria = [f"{s}: G {v['G']:.4f} [{v['lo']:.4f}, {v['hi']:.4f}], positive in {v['seeds_positive']} of 5 seeds: "
                    f"{v['outcome']}" for s, v in per_store.items()]  # fmt: skip
        criteria.append(f"stores with a gap: {len(gaps)} (confirm at 6); with no gap: {len(none)} (falsify at 5)")
        self.record("H2.1", verdict, criteria, {s: {k: v for k, v in d.items() if k != "boot"} for s, d in per_store.items()})
        self.write(pd.DataFrame([{"store": s, **{k: v for k, v in d.items() if k != "boot"}} for s, d in per_store.items()]),
                   "x2_h21")  # fmt: skip
        return per_store

    def h22(self) -> None:
        rows, outcome = [], {}
        for store in APPROXIMATE:
            frame = self.x2m(store, "default")
            if not len(frame):
                continue
            frame = frame.assign(log_r1=np.log10(pd.to_numeric(frame["r1"], errors="coerce")))
            base = frame.dropna(subset=["recall10", "sigma", "rho1000"])
            below = int((base["recall10"] < 1).sum())
            idx = self.boot.idx(base)
            y = base["recall10"].to_numpy(dtype=float)
            est_g, boot_g = spearman_boot(self.boot, idx, y, base["sigma"].to_numpy(dtype=float))
            est_l, boot_l = spearman_boot(self.boot, idx, y, base["rho1000"].to_numpy(dtype=float))
            d, boot_d = abs(est_l) - abs(est_g), np.abs(boot_l) - np.abs(boot_g)
            lo, hi = interval(boot_d)
            status = "not assessable" if below < 100 else "local" if d >= 0.05 and lo > 0 else "global" if d < 0 and hi < 0 else "neither"
            outcome[store] = status
            row = {"store": store, "pairs": len(base), "below_1": below, "rho_sigma": est_g, "rho_rho1000": est_l, "D": d,
                   "lo": lo, "hi": hi, "status": status}  # fmt: skip
            for axis in ("acorn", "gls", "alpha", "rho100", "log_r1"):
                part = frame.dropna(subset=["recall10", axis])
                if len(part) > 10:
                    rx = Ranked(part["recall10"].to_numpy(dtype=float)).ranks(np.ones(len(part)))
                    ry = Ranked(part[axis].to_numpy(dtype=float)).ranks(np.ones(len(part)))
                    row[f"rho_{axis}"] = weighted_pearson(rx, ry, np.ones(len(part)))
            rows.append(row)
        self.write(pd.DataFrame(rows), "x2_h22")
        assessable = [s for s, v in outcome.items() if v != "not assessable"]
        local = [s for s in assessable if outcome[s] == "local"]
        glob = [s for s in assessable if outcome[s] == "global"]
        verdict = "inconclusive"
        if len(assessable) >= 4 and len(local) * 3 >= 2 * len(assessable):
            verdict = "confirmed"
        elif assessable and len(glob) * 2 >= len(assessable):
            verdict = "falsified"
        criteria = [f"{r['store']}: D {r['D']:.4f} [{r['lo']:.4f}, {r['hi']:.4f}], {r['below_1']} pairs below 1: {r['status']}"
                    for r in rows]  # fmt: skip
        criteria.append(f"assessable {len(assessable)}, local {len(local)}, global {len(glob)}")
        self.record("H2.2", verdict, criteria)

    def h23(self, h21: dict[str, dict[str, Any]]) -> None:
        rows = []
        for store, info in h21.items():
            if info["outcome"] != "gap":
                continue
            sweeps = self.select(self.pair_level, exp="x2", corpus=xc.M_NAME, store=store, layout=self.main_layout(store))
            sweeps = sweeps[sweeps["kind"] == "sweep"]
            if not len(sweeps):
                continue
            top = sweeps["level"].max()
            setting = sweeps[sweeps["level"] == top]["setting"].iloc[0]
            frame = self.x2m(store, setting)
            mid = frame[frame["level_pair"].isin(MID_LEVELS)]
            u, n = mid[mid["regime"] == "U"], mid[mid["regime"] == "N"]
            if not len(u) or not len(n):
                continue
            g_max, boot_max = self.gap(mid, u, n)
            narrowing = info["boot"] - boot_max
            n_lo, n_hi = interval(narrowing)
            m_lo, m_hi = interval(boot_max)
            narrowed = info["G"] - g_max > 0 and n_lo > 0
            remains = g_max >= 0.02 and m_lo > 0
            rows.append({"store": store, "max_setting": setting, "G_default": info["G"], "G_max": g_max,
                         "narrowing": info["G"] - g_max, "narrowing_lo": n_lo, "narrowing_hi": n_hi, "G_max_lo": m_lo,
                         "G_max_hi": m_hi, "narrowed": narrowed, "remains": remains,
                         "closed": g_max < 0.01, **self.lowest_levels(store)})  # fmt: skip
        self.write(pd.DataFrame(rows), "x2_h23")
        both = [r for r in rows if r["narrowed"] and r["remains"]]
        closed = [r for r in rows if r["closed"]]
        verdict = "inconclusive"
        if len(rows) >= 3 and len(both) * 2 >= len(rows):
            verdict = "confirmed"
        elif rows and len(closed) * 2 >= len(rows):
            verdict = "falsified"
        criteria = [f"{r['store']} ({r['max_setting']}): G {r['G_default']:.4f} -> {r['G_max']:.4f} "
                    f"[{r['G_max_lo']:.4f}, {r['G_max_hi']:.4f}], narrowing [{r['narrowing_lo']:.4f}, "
                    f"{r['narrowing_hi']:.4f}]" for r in rows]  # fmt: skip
        criteria.append(f"stores with a gap and a sweep: {len(rows)}; narrowed and remaining: {len(both)}; closed: {len(closed)}")
        self.record("H2.3", verdict, criteria)

    def lowest_levels(self, store: str) -> dict[str, Any]:
        """For U and N, the lowest sweep level reaching recall@10 >= 0.95 (s 2% to 30%)."""
        out: dict[str, Any] = {}
        frame = self.select(self.pair_level, exp="x2", corpus=xc.M_NAME, store=store, layout=self.main_layout(store))
        frame = frame[(frame["kind"] == "sweep") & frame["level_pair"].isin(MID_LEVELS)]
        for regime in ("U", "N"):
            part = frame[frame["regime"] == regime].groupby("level")["recall10"].mean()
            reached = [int(level) for level, value in part.items() if value >= 0.95]
            out[f"lowest_level_{regime}"] = min(reached) if reached else None
        return out

    def h24(self) -> None:
        rows = []
        for store in APPROXIMATE:
            frame = self.x2m(store, "default")
            if not len(frame):
                continue
            frame = frame[(frame["regime"] == "N") & (frame["shape"] == "groups")]
            levels = {}
            for level in (0, 1, 2, 3):
                part = frame[frame["level_pair"] == level]
                if len(part):
                    levels[level] = self.boot.mean(self.boot.idx(part), part["recall10"].to_numpy(dtype=float))
            if 0 not in levels or not any(lv in levels for lv in (1, 2, 3)):
                continue
            mids = [levels[lv] for lv in (1, 2, 3) if lv in levels]
            v = levels[0][0] - min(m[0] for m in mids)
            boot = levels[0][1] - np.minimum.reduce([m[1] for m in mids])
            lo, hi = interval(boot)

            def stat(part: pd.DataFrame) -> float:
                means = part.groupby("level_pair")["recall10"].mean()
                if 0 not in means or not any(lv in means for lv in (1, 2, 3)):
                    return math.nan
                return float(means[0] - min(means[lv] for lv in (1, 2, 3) if lv in means))

            seeds = self.seeds_hold(frame, stat)
            status = "U-shaped" if v >= 0.05 and lo > 0 and seeds >= 4 else "monotone" if v <= 0 else "neither"
            rows.append({"store": store, "V": v, "lo": lo, "hi": hi, "seeds_positive": seeds, "status": status,
                         **{f"recall_level{lv}": levels[lv][0] for lv in levels}})  # fmt: skip
        self.write(pd.DataFrame(rows), "x2_h24")
        u_shaped = [r for r in rows if r["status"] == "U-shaped"]
        monotone = [r for r in rows if r["status"] == "monotone"]
        verdict = "confirmed" if len(u_shaped) >= 5 else "falsified" if len(monotone) >= 5 else "inconclusive"
        criteria = [f"{r['store']}: V {r['V']:.4f} [{r['lo']:.4f}, {r['hi']:.4f}], {r['seeds_positive']} seeds: {r['status']}"
                    for r in rows]  # fmt: skip
        criteria.append(f"U-shaped {len(u_shaped)} (confirm at 5), monotone {len(monotone)} (falsify at 5)")
        self.record("H2.4", verdict, criteria)

    def validity(self) -> None:
        raw = self.rows[self.rows["exp"] == "x2"] if len(self.rows) else self.rows
        checks = []
        exact = raw[(raw["kind"] == "exact")] if len(raw) else raw
        if len(exact):
            recall = pd.to_numeric(exact["recall10"], errors="coerce")
            worst = exact.assign(recall10=recall).groupby(["corpus", "store", "layout", "setting"])["recall10"].min()
            for key, value in worst.items():
                checks.append({"check": "V1", "what": " ".join(map(str, key)), "value": value, "ok": bool(value >= 0.999)})
        p = self.pair_level
        if len(p):
            asrun = p[(p["exp"] == "x2") & (p["corpus"] == xc.E_NAME) & (p["asrun"] == 1)]
            if "original" in asrun:
                asrun = asrun[asrun["original"] == 1]
            for store, want in X0.items():
                part = asrun[asrun["store"] == store]
                if len(part):
                    got = part["recall10"].mean()
                    checks.append({"check": "V2", "what": f"{store} ({', '.join(sorted(part['setting'].unique()))})",
                                   "value": got, "x0": want, "ok": bool(abs(got - want) <= 0.03)})  # fmt: skip
        leaked = [j["label"] for j in self.jobs if j.get("leaked") or j.get("leak")]
        checks.append({"check": "V3", "what": "jobs stopped by a leak", "value": len(leaked), "ok": not leaked,
                       "detail": leaked})  # fmt: skip
        if len(self.subjects_m):
            s = self.subjects_m[self.subjects_m["level"] >= 1]
            ratio = s["sigma"] / s["nominal"]
            share = float(((ratio >= 0.75) & (ratio <= 1.25)).mean()) if len(s) else math.nan
            checks.append({"check": "V4", "what": "M subjects at s >= 0.5% within 25% of nominal", "value": share,
                           "ok": bool(share >= 0.9)})  # fmt: skip
        frame = pd.DataFrame(checks)
        self.write(frame, "validity")
        v2 = frame[frame["check"] == "V2"] if len(frame) else frame
        self.verdicts["validity"] = {
            "V1": bool(frame[frame["check"] == "V1"]["ok"].all()) if len(frame) else None,
            "V2": f"{int(v2['ok'].sum())} of {len(v2)} stores within 0.03" if len(v2) else None,
            "V2_holds": bool(v2["ok"].sum() >= 7) if len(v2) else None,
            "V3": bool(not leaked),
            "V4": frame[frame["check"] == "V4"]["value"].tolist() if len(frame) else None,
        }

    # -- X5 --

    def x5_frame(self) -> pd.DataFrame:
        raw = self.rows[(self.rows["exp"] == "x5")].copy() if len(self.rows) else self.rows
        if not len(raw):
            return raw
        for c in ("n5", "n10", "first5", "first10", "R", "recall5", "recall10", "max10", "complete10", "short5",
                  "short10", "empty5", "empty10"):  # fmt: skip
            raw[c] = pd.to_numeric(raw[c], errors="coerce")
        return raw[raw["err"].isna()]

    def x5_tables(self, raw: pd.DataFrame) -> None:
        out, confusion = [], []
        for (corpus, store, layout, arm), frame in raw.groupby(["corpus", "store", "layout", "setting"]):
            row: dict[str, Any] = {"corpus": corpus, "store": store, "layout": layout, "arm": arm, "rows": len(frame)}
            for k in (5, 10):
                scorable = frame[frame["R"] >= 1]
                want = np.minimum(k, frame["R"])
                truly = frame[f"first{k}"] < want
                flagged = frame[f"shortfall{k}"] == "missed"
                row[f"recall{k}"] = scorable[f"recall{k}"].mean()
                row[f"err{k}"] = scorable[f"empty{k}"].mean()
                row[f"short{k}"] = scorable[f"short{k}"].mean()
                row[f"trigger{k}"] = frame[f"shortfall{k}"].notna().mean()
                row[f"repair{k}"] = frame[f"fallback{k}"].isin(["exact", "widened"]).mean()
                row[f"truly_short_first{k}"] = int(truly.sum())
                row[f"detection{k}"] = float((truly & flagged).sum() / truly.sum()) if truly.sum() else math.nan
                row[f"false_alarm{k}"] = int((flagged & ~truly).sum())
                complete = frame[f"complete{k}"] == 1
                maximal = frame[f"max{k}"] == 1
                row[f"false_complete{k}"] = float((complete & ~maximal).sum() / complete.sum()) if complete.sum() else math.nan
                for c_value in (True, False):
                    for m_value in (True, False):
                        confusion.append({"corpus": corpus, "store": store, "layout": layout, "arm": arm, "k": k,
                                          "complete": c_value, "maximal": m_value,
                                          "count": int(((complete == c_value) & (maximal == m_value)).sum())})  # fmt: skip
            lat = frame["lat"].dropna()
            trig = frame["sfms_med"].dropna()
            for q, name in ((0.5, "p50"), (0.95, "p95"), (0.99, "p99")):
                row[f"{name}_ms"] = lat.quantile(q) if len(lat) else math.nan
                row[f"triggered_{name}_ms"] = trig.quantile(q) if len(trig) else math.nan
            out.append(row)
        self.write(pd.DataFrame(out), "x5_arms")
        self.write(pd.DataFrame(confusion), "x5_confusion")
        self.x5_arms = pd.DataFrame(out)

    def x5_verdicts(self, raw: pd.DataFrame) -> None:
        arms = getattr(self, "x5_arms", pd.DataFrame())
        # H5.1
        criteria, held, failed, judged = [], True, False, 0
        for (corpus, store), frame in raw[raw["setting"] == "count"].groupby(["corpus", "store"]):
            truly_n = alarms = detected = 0
            exhausted_bad = 0
            for k in (5, 10):
                want = np.minimum(k, frame["R"])
                truly = frame[f"first{k}"] < want
                flagged = frame[f"shortfall{k}"] == "missed"
                truly_n += int(truly.sum())
                alarms += int((flagged & ~truly).sum())
                detected += int((flagged & truly).sum())
                exhausted = frame[f"shortfall{k}"] == "exhausted"
                exhausted_bad += int((exhausted & (frame[f"n{k}"] != want)).sum())
            if truly_n < 10:
                criteria.append(f"{corpus} {store}: {truly_n} truly short first searches (< 10): not judged")
                continue
            judged += 1
            rate = detected / truly_n
            ok = alarms == 0 and rate >= 0.99 and exhausted_bad == 0
            held &= ok
            failed |= alarms > 0 or rate < 0.95
            criteria.append(f"{corpus} {store}: false alarms {alarms}, detection {rate:.4f} of {truly_n}, "
                            f"exhausted without min(k, R) hits {exhausted_bad}")  # fmt: skip
        verdict = "falsified" if failed else "confirmed" if judged and held else "inconclusive"
        self.record("H5.1", verdict, criteria)
        # H5.2
        criteria, ok_all, bad, judged = [], True, False, 0
        for store in ("pgvector", "qdrant"):
            for corpus in (xc.E_NAME, xc.M_NAME):
                report = raw[(raw["store"] == store) & (raw["corpus"] == corpus) & (raw["setting"] == "report")]
                exact = raw[(raw["store"] == store) & (raw["corpus"] == corpus) & (raw["setting"] == "exact-inf")]
                shorts = int(report["short5"].fillna(0).sum() + report["short10"].fillna(0).sum())
                if shorts < 10 or not len(exact):
                    criteria.append(f"{store} {corpus}: report has {shorts} short results (< 10) or no exact-inf: not judged")
                    continue
                judged += 1
                scorable = exact[exact["R"] >= 1]
                residual = int(scorable[["empty5", "empty10", "short5", "short10"]].fillna(0).to_numpy().sum())
                triggered = exact[exact["shortfall10"].notna()]
                recall = triggered["recall10"].mean() if len(triggered) else math.nan
                ok = residual == 0 and (not len(triggered) or recall >= 0.999)
                ok_all &= ok
                bad |= not ok
                criteria.append(f"{store} {corpus}: report short {shorts}; exact-inf empty or short {residual}; recall@10 "
                                f"on {len(triggered)} triggered {recall:.4f}")  # fmt: skip
        verdict = "falsified" if bad else "confirmed" if judged and ok_all else "inconclusive"
        self.record("H5.2", verdict, criteria)
        # H5.3
        criteria, ok_all, over, judged = [], True, False, 0
        for (corpus, store, build), frame in raw.groupby(["corpus", "store", "build"]):
            report = frame[frame["setting"] == "report"].set_index("pid")
            for arm in REPAIR_ARMS:
                other = frame[frame["setting"] == arm].set_index("pid")
                common = report.index.intersection(other.index)
                if not len(common):
                    continue
                untriggered = common[(report.loc[common, "shortfall10"].isna() & other.loc[common, "shortfall10"].isna()).to_numpy()]
                if not len(untriggered):
                    continue
                ratio = (other.loc[untriggered, "lat"] / report.loc[untriggered, "lat"]).median()
                judged += 1
                ok = 0.95 <= ratio <= 1.05
                ok_all &= ok
                over |= ratio > 1.10
                criteria.append(f"{corpus} {store} b{build} {arm}: median latency ratio on {len(untriggered)} untriggered "
                                f"pairs {ratio:.4f}")  # fmt: skip
        verdict = "falsified" if over else "confirmed" if judged and ok_all else "inconclusive"
        self.record("H5.3", verdict, criteria)
        # H5.4
        self.h54(raw)
        # H5.5
        self.h55(raw)
        # H5.6
        self.h56(raw)
        # H5.7
        criteria = []
        tenant = arms[(arms["corpus"] == xc.E_NAME) & (arms["store"] == "qdrant") & (arms["arm"] == "native-tenant")] if len(arms) else arms
        library = arms[(arms["corpus"] == xc.E_NAME) & (arms["store"] == "qdrant") & arms["arm"].isin(LIBRARY_ARMS)] if len(arms) else arms
        if len(tenant) and len(library):
            t = float(tenant["recall10"].iloc[0])
            best = float(library["recall10"].max())
            verdict = "confirmed" if t >= 0.90 and best <= 0.75 else "falsified" if t < 0.85 or best > 0.85 else "inconclusive"
            criteria.append(f"per-tenant layout recall@10 {t:.4f}; best library arm {best:.4f}")
        else:
            verdict = "inconclusive"
            criteria.append("missing the per-tenant arm or the library arms of Qdrant on E")
        self.record("H5.7", verdict, criteria)

    def collapse_x5(self, raw: pd.DataFrame, arm: str, **match: Any) -> pd.DataFrame:
        frame = raw[raw["setting"] == arm]
        for key, value in match.items():
            frame = frame[frame[key] == value]
        return frame

    def h54(self, raw: pd.DataFrame) -> None:
        criteria = []
        base = raw[(raw["store"] == "qdrant") & (raw["corpus"] == xc.E_NAME) & (raw["layout"] == "as-run")]
        report = base[base["setting"] == "report"]
        if not len(report):
            self.record("H5.4", "inconclusive", ["no report arm for Qdrant on E"])
            return

        def fc(frame: pd.DataFrame) -> tuple[float, np.ndarray]:
            complete = frame["complete10"] == 1
            marked = frame.assign(num=(complete & (frame["max10"] == 0)).astype(float), den=complete.astype(float))
            per = marked.groupby(["corpus", "sid", "pid"])[["num", "den"]].sum().reset_index()
            return self.boot.ratio(self.boot.idx(per), per["num"].to_numpy(), per["den"].to_numpy())

        fc_report, boot_report = fc(report)
        criteria.append(f"report: false-completeness {fc_report:.4f} (confirm needs >= 0.20)")
        inside, lowered = True, False
        for arm in REPAIR_ARMS:
            frame = base[base["setting"] == arm]
            if not len(frame):
                inside = False
                criteria.append(f"{arm}: missing")
                continue
            value, boot = fc(frame)
            lo, hi = interval(boot - boot_report)
            diff = value - fc_report
            inside &= abs(diff) < 0.02 and lo > -0.03 and hi < 0.03
            lowered |= diff <= -0.05 and excludes_zero(lo, hi)
            criteria.append(f"{arm}: {value:.4f}, minus report {diff:.4f} [{lo:.4f}, {hi:.4f}]")
        verdict = "inconclusive"
        if fc_report < 0.05 or lowered:
            verdict = "falsified"
        elif fc_report >= 0.20 and inside:
            verdict = "confirmed"
        self.record("H5.4", verdict, criteria)

    def h55(self, raw: pd.DataFrame) -> None:
        criteria = []
        ok_a = True
        for job in self.jobs:
            if job.get("experiment") != "x5":
                continue
            for unit in job.get("units", []):
                for s in unit.get("settings", []):
                    if s.get("id") != "monitor" or not s.get("sweep"):
                        continue
                    n, x = s["sweep"]["retrievals"], s["sweep"]["sampled"]
                    half = 3.29 * math.sqrt(n * 0.01 * 0.99)
                    inside = n * 0.01 - half <= x <= n * 0.01 + half
                    ok_a &= inside
                    criteria.append(f"(a) {job['label']} {unit['layout']} b{unit['build']}: {x} of {n} sampled: "
                                    f"{'inside' if inside else 'outside'} the 99.9% interval")  # fmt: skip
        samples = pd.DataFrame(self.samples)
        if len(samples):
            samples = samples[samples["setting"] == "monitor"].dropna(subset=["sampled", "rid"])
        agree = float((np.abs(samples["sampled"] - samples["rid"]) <= 0.1).mean()) if len(samples) else math.nan
        criteria.append(f"(b) agreement within 0.1 on {len(samples)} sampled retrievals: {agree:.4f}")
        diffs = []
        for corpus in (xc.E_NAME, xc.M_NAME):
            part = samples[(samples["store"] == "qdrant") & (samples["corpus"] == corpus)] if len(samples) else samples
            monitor = raw[(raw["store"] == "qdrant") & (raw["corpus"] == corpus) & (raw["setting"] == "monitor")]
            if not len(part) or not len(monitor):
                criteria.append(f"(c) Qdrant {corpus}: no samples")
                diffs.append(math.nan)
                continue
            population = pd.concat([pd.to_numeric(monitor["rid5"], errors="coerce"), pd.to_numeric(monitor["rid10"], errors="coerce")]).mean()
            diff = abs(part["sampled"].mean() - population)
            diffs.append(diff)
            criteria.append(f"(c) Qdrant {corpus}: mean sampled {part['sampled'].mean():.4f} on {len(part)}, population "
                            f"{population:.4f}, difference {diff:.4f}")  # fmt: skip
        verdict = "inconclusive"
        if (np.isfinite(agree) and agree < 0.8) or any(np.isfinite(d) and d > 0.10 for d in diffs):
            verdict = "falsified"
        elif ok_a and np.isfinite(agree) and agree >= 0.95 and diffs and all(np.isfinite(d) and d <= 0.05 for d in diffs):
            verdict = "confirmed"
        self.record("H5.5", verdict, criteria)

    def h56(self, raw: pd.DataFrame) -> None:
        pg = raw[raw["store"] == "pgvector"]
        exact = pg[(pg["setting"] == "exact-inf") & pg["shortfall10"].notna()]
        widen = pg[(pg["setting"] == "widen") & pg["shortfall10"].notna()]
        keys = ["corpus", "sid", "pid"]
        a = exact.groupby(keys)["recall10"].mean().reset_index()
        b = widen.groupby(keys)["recall10"].mean().reset_index()
        both = a.merge(b, on=keys, suffixes=("_exact", "_widen"))
        if len(both) < 20:
            self.record("H5.6", "inconclusive", [f"{len(both)} retrievals triggered in both arms (< 20)"])
            return
        diff = (both["recall10_exact"] - both["recall10_widen"]).to_numpy(dtype=float)
        est, boot = self.boot.mean(self.boot.idx(both), diff)
        lo, hi = interval(boot)
        verdict = "confirmed" if est >= 0.01 and lo > 0 else "falsified" if est < 0.002 and lo <= 0 <= hi else "inconclusive"
        self.record("H5.6", verdict, [f"exact-inf minus widen on {len(both)} triggered pairs: {est:.4f} [{lo:.4f}, {hi:.4f}], "
                                      f"Wilcoxon p {wilcoxon(diff):.4g}"])  # fmt: skip

    def x5_paired_tests(self, raw: pd.DataFrame) -> None:
        """McNemar on empty results and Wilcoxon on recall@10, each arm against report (reported, not judged)."""
        out = []
        for (corpus, store, layout), frame in raw.groupby(["corpus", "store", "layout"]):
            report = frame[frame["setting"] == "report"].groupby("pid")[["recall10", "empty10", "max10"]].mean()
            for arm in frame["setting"].unique():
                if arm == "report":
                    continue
                other = frame[frame["setting"] == arm].groupby("pid")[["recall10", "empty10", "max10"]].mean()
                common = report.index.intersection(other.index)
                if not len(common):
                    continue
                r, o = report.loc[common], other.loc[common]
                out.append({"corpus": corpus, "store": store, "layout": layout, "arm": arm, "pairs": len(common),
                            "recall10_diff": float((o["recall10"] - r["recall10"]).mean()),
                            "wilcoxon_p": wilcoxon((o["recall10"] - r["recall10"]).to_numpy(dtype=float)),
                            "mcnemar_empty_p": mcnemar(np.round(o["empty10"].to_numpy(dtype=float)),
                                                       np.round(r["empty10"].to_numpy(dtype=float))),
                            "mcnemar_maximal_p": mcnemar(np.round(o["max10"].to_numpy(dtype=float)),
                                                         np.round(r["max10"].to_numpy(dtype=float)))})  # fmt: skip
        self.write(pd.DataFrame(out), "x5_paired_tests")

    # -- the report --

    def run(self) -> None:
        started = time.perf_counter()
        if len(self.rows):
            self.x2_tables()
            h21 = self.h21()
            self.h22()
            self.h23(h21)
            self.h24()
            self.validity()
            raw = self.x5_frame()
            if len(raw):
                self.x5_tables(raw)
                self.x5_verdicts(raw)
                self.x5_paired_tests(raw)
        xc.write_json(self.out / "verdicts.json", self.verdicts)
        self.write_report()
        log(f"statistics done in {time.perf_counter() - started:.0f} s")

    def write_report(self) -> None:
        lines = ["## X2 and X5: pre-registered verdicts", ""]
        lines += xc.markdown_table(
            ["hypothesis", "verdict"],
            [[h, v["verdict"]] for h, v in self.verdicts.items() if isinstance(v, dict) and "verdict" in v],
        )
        validity = self.verdicts.get("validity")
        if validity:
            lines.append(f"Validity: {json.dumps(validity)}")
            lines.append("")
        jobs = [[j.get("experiment"), j.get("label"), j.get("status"), len(j.get("failures", [])), len(j.get("skipped", []))]
                for j in self.jobs]  # fmt: skip
        lines += ["### Jobs", ""] + xc.markdown_table(["exp", "job", "status", "failures", "skipped"], jobs)
        summary = list(lines)
        settings = getattr(self, "settings_table", None)
        if settings is not None and len(settings):
            lines += ["### X2 settings (recall@10 with 95% interval; latency in its own job)", ""]
            lines += xc.markdown_table(
                ["corpus", "store", "layout", "setting", "pairs", "builds", "recall@10", "lo", "hi", "empty", "p50 ms"],
                settings[["corpus", "store", "layout", "setting", "pairs", "builds", "recall10", "lo", "hi", "err10",
                          "p50_ms"]].itertuples(index=False),  # fmt: skip
            )
        arms = getattr(self, "x5_arms", None)
        if arms is not None and len(arms):
            lines += ["### X5 arms", ""]
            columns = ["corpus", "store", "layout", "arm", "recall5", "recall10", "err10", "short10", "trigger10",
                       "detection10", "false_complete10", "p50_ms", "triggered_p95_ms"]  # fmt: skip
            lines += xc.markdown_table(columns, arms[columns].itertuples(index=False))
        for hid, v in self.verdicts.items():
            if isinstance(v, dict) and "criteria" in v:
                lines += [f"### {hid}: {v['verdict']}", "", *[f"- {c}" for c in v["criteria"]], ""]
        (self.out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (self.out / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Statistics and verdicts of X2 and X5")
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--meta-e", type=Path, default=None)
    parser.add_argument("--meta-m", type=Path, default=None)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--resamples", type=int, default=10_000)
    args = parser.parse_args(argv)
    for name in ("meta_e", "meta_m"):
        folder = getattr(args, name)
        if folder is not None and not folder.is_dir():
            log(f"{folder} does not exist: {name} is left out")
            setattr(args, name, None)
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    Analysis(args).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
