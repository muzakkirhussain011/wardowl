"""Experiment X6, statistics: the attacker's advantage, the mitigations' costs and the verdicts.

Reads every x6-<store>.jsonl under --in and writes, to --out:

* x6_cells.csv: per cell (store, config, m, selectivity p, observable) and comparison (W1 against
  W0; SEPb against SEPa, the A/A null; padded latency; raw latency on the padding seeds): the paired
  AUC (two-alternative forced choice, the differencing attacker) and the pooled AUC (one shot), each
  with a 95% cluster-bootstrap interval over (seed, probe), the largest TPR - FPR, and the cell's
  size, seeds and error rate;
* x6_deltas.csv: paired-AUC differences between a configuration and its mitigation, bootstrapped
  jointly on the same probes;
* x6_costs.csv: each mitigation's latency cost (ratio of means with its interval, median ratio);
* x6_listchange.csv: the share of probes whose ordered hit ids differ between W1 and W0 (and between
  SEPa and SEPb), for the deterministic configurations;
* x6_health.csv, x6_verdicts.csv and x6_report.md: what ran, the guards and the verdict on each
  pre-registered hypothesis, by the rules of PREREG_X3_X6.md and nothing else.

    python x6_stats.py --in parts --out reports [--resamples 10000] [--seed 20261029] [--annotate]

numpy only. Observations: per (store, config, seed, probe, p, slot), the median latency, median count,
share of `complete`, mean recall and mean of the mean score over the timed repetitions.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import x3x6_common as common
from x3x6_common import SEED_BASE

OBSERVABLES = ("latency", "count", "complete", "recall", "score")
# Each observable times its sign is larger in the world predicted to hold the secrets (W1).
SIGN = {"latency": 1.0, "count": -1.0, "complete": -1.0, "recall": -1.0, "score": -1.0}
VECTOR_STORES = ("faiss", "pgvector", "qdrant", "elasticsearch")
DETERMINISTIC = {
    ("pgvector", "pre-exact"),
    ("qdrant", "pre-exact"),
    ("elasticsearch", "pre-exact"),
    ("faiss", "pre"),
    ("memory", "pre"),
    ("pgvector", "bm25-pre"),
    ("qdrant", "bm25-pre"),
    ("elasticsearch", "bm25-pre"),
    ("elasticsearch", "hybrid-exact"),
}
PCT_GROUPS = {"low": (1, 10)}  # pooled selectivities a rule names (H3 c)
MIN_CLUSTERS = 20
MIN_SEEDS = 5
MAX_ERROR_RATE = 0.05
CONFIRMED, FALSIFIED, INCONCLUSIVE = "confirmed", "falsified", "inconclusive"


def has_recall(store: str, config: str) -> bool:
    """Recall against the exact dense top 10 means something for vector search only."""
    return store != "memory" and not config.startswith(("bm25", "hybrid"))


# ---- observations --------------------------------------------------------------------------------


class Data:
    def __init__(self, records: list[dict[str, Any]], resamples: int, seed: int) -> None:
        self.records = records
        self.resamples = resamples
        self.seed = seed
        self.groups: dict[tuple[Any, ...], dict[str, Any]] = {}
        self.single: dict[tuple[str, str], list[tuple[int, float]]] = defaultdict(list)  # (seed, latency) per retrieval
        self.cells: dict[tuple[Any, ...], dict[str, Any]] = {}
        for r in records:
            if r.get("type") != "retrieval":
                continue
            key = (r["store"], r["config"], int(r["seed"]), int(r["probe"]), int(r["pct"]), r["slot"])
            g = self.groups.setdefault(
                key,
                {"level": int(r["level"]), "lat": [], "pad": [], "count": [], "complete": [], "recall": [], "score": [],
                 "searches": [], "examined": [], "errors": 0, "total": 0, "first": None, "ids": None},
            )  # fmt: skip
            if r.get("warmup"):
                continue
            g["total"] += 1
            if r.get("error"):
                g["errors"] += 1
                continue
            g["lat"].append(float(r["latency_ms"]))
            g["count"].append(float(r["count"]))
            g["complete"].append(1.0 if r["complete"] else 0.0)
            g["recall"].append(math.nan if r.get("recall") is None else float(r["recall"]))
            scores = r.get("scores") or []
            g["score"].append(float(np.mean(scores)) if scores else -math.inf)
            g["searches"].append(float(r["searches"]) if r.get("searches") is not None else math.nan)
            g["examined"].append(float(r.get("examined") or 0))
            if g["first"] is None or int(r["rep"]) < g["first"]:
                g["first"] = int(r["rep"])
                g["ids"] = (tuple(r.get("ids") or []), tuple(round(float(s), 9) for s in scores))
            self.single[(r["store"], r["config"])].append((int(r["seed"]), float(r["latency_ms"])))
        self.obs: dict[tuple[Any, ...], dict[str, Any]] = {}
        for key, g in self.groups.items():
            if not g["lat"]:
                continue
            self.obs[key] = {
                "level": g["level"],
                "latency": float(np.median(g["lat"])),
                "count": float(np.median(g["count"])),
                "complete": float(np.mean(g["complete"])),
                "recall": float(np.mean(g["recall"])) if not any(math.isnan(x) for x in g["recall"]) else math.nan,
                "score": float(np.mean(g["score"])),
                "searches": float(np.nanmean(g["searches"])) if any(not math.isnan(x) for x in g["searches"]) else math.nan,
                "examined": float(np.mean(g["examined"])),
                "ids": g["ids"],
                "lat_all": list(g["lat"]),
            }
        self.configs = sorted({(k[0], k[1]) for k in self.groups})
        self.levels = sorted({g["level"] for g in self.groups.values()})
        self.pcts = sorted({k[4] for k in self.groups})

    def pairs(self, store: str, config: str, a: str, b: str, *, seeds: Iterable[int] | None = None) -> list[dict[str, Any]]:
        """Observations of slot `a` and slot `b` of the same (seed, probe, p)."""
        chosen = set(seeds) if seeds is not None else None
        found = []
        for key, first in self.obs.items():
            if key[0] != store or key[1] != config or key[5] != a:
                continue
            seed, probe, pct = key[2], key[3], key[4]
            if chosen is not None and seed not in chosen:
                continue
            second = self.obs.get((store, config, seed, probe, pct, b))
            if second is None:
                continue
            found.append({"seed": seed, "probe": probe, "pct": pct, "level": first["level"], "a": first, "b": second})
        found.sort(key=lambda p: (p["seed"], p["probe"], p["pct"]))
        return found

    def error_rate(self, store: str, config: str, slots: Sequence[str], level: Any, pcts: Sequence[int]) -> float:
        errors = total = 0
        for key, g in self.groups.items():
            if key[0] == store and key[1] == config and key[5] in slots and key[4] in pcts:
                if level == "all" or g["level"] == level:
                    errors += g["errors"]
                    total += g["total"]
        return errors / total if total else math.nan


def select(pairs: list[dict[str, Any]], level: Any, pct: Any) -> list[dict[str, Any]]:
    pcts = PCT_GROUPS.get(pct) if isinstance(pct, str) and pct in PCT_GROUPS else None
    return [
        p
        for p in pairs
        if (level == "all" or p["level"] == level)
        and (pct == "all" or (pcts is not None and p["pct"] in pcts) or (pcts is None and p["pct"] == pct))
    ]


# ---- statistics ----------------------------------------------------------------------------------


def comparison_matrix(x1: np.ndarray, x0: np.ndarray) -> np.ndarray:
    return (x1[:, None] > x0[None, :]).astype(float) + 0.5 * (x1[:, None] == x0[None, :])


def ks_advantage(x1: np.ndarray, x0: np.ndarray) -> float:
    """The largest TPR - FPR of a threshold on the observable, in the predicted direction."""
    values = np.unique(np.concatenate([x1, x0]))
    if not len(values):
        return math.nan
    best = 0.0
    for start in range(0, len(values), 2048):
        thresholds = values[start : start + 2048]
        tpr = (x1[None, :] >= thresholds[:, None]).mean(axis=1)
        fpr = (x0[None, :] >= thresholds[:, None]).mean(axis=1)
        best = max(best, float(np.max(tpr - fpr)))
    return best


def auc_cell(pairs: list[dict[str, Any]], observable: str, resamples: int, rng: np.random.Generator) -> dict[str, Any] | None:
    if not pairs:
        return None
    sign = SIGN[observable]
    x1 = np.array([sign * p["a"][observable] for p in pairs], dtype=float)
    x0 = np.array([sign * p["b"][observable] for p in pairs], dtype=float)
    keep = ~(np.isnan(x1) | np.isnan(x0))
    if not keep.any():
        return None
    x1, x0 = x1[keep], x0[keep]
    kept = [p for p, k in zip(pairs, keep, strict=True) if k]
    clusters = np.array([f"{p['seed']}:{p['probe']}" for p in kept])
    out: dict[str, Any] = {
        "pairs": len(kept),
        "clusters": len(set(clusters.tolist())),
        "seeds": len({p["seed"] for p in kept}),
        "mean_w1": float(np.mean(sign * x1)),
        "mean_w0": float(np.mean(sign * x0)),
    }
    if np.array_equal(x1, x0):
        # Identical observations: every comparison is a tie, so both AUCs are 0.5 on every resample.
        return {**out, "paired": 0.5, "paired_lo": 0.5, "paired_hi": 0.5, "pooled": 0.5, "pooled_lo": 0.5,
                "pooled_hi": 0.5, "ks": 0.0}  # fmt: skip
    gt = comparison_matrix(x1, x0)
    diagonal = np.diag(gt).copy()
    paired_b: list[np.ndarray] = []
    pooled_b: list[np.ndarray] = []
    for weights in common.cluster_weights(clusters, resamples, rng):
        total = weights.sum(axis=1)
        paired_b.append((weights @ diagonal) / total)
        pooled_b.append(((weights @ gt) * weights).sum(axis=1) / total**2)
    paired_lo, paired_hi = common.percentile_interval(np.concatenate(paired_b))
    pooled_lo, pooled_hi = common.percentile_interval(np.concatenate(pooled_b))
    return {
        **out,
        "paired": float(diagonal.mean()),
        "paired_lo": paired_lo,
        "paired_hi": paired_hi,
        "pooled": float(gt.mean()),
        "pooled_lo": pooled_lo,
        "pooled_hi": pooled_hi,
        "ks": ks_advantage(x1, x0),
    }


def mean_cell(values: np.ndarray, clusters: np.ndarray, resamples: int, rng: np.random.Generator) -> dict[str, Any]:
    if not len(values):
        return {"mean": math.nan, "lo": math.nan, "hi": math.nan, "n": 0, "clusters": 0}
    boot = [(w @ values) / w.sum(axis=1) for w in common.cluster_weights(clusters, resamples, rng)]
    lo, hi = common.percentile_interval(np.concatenate(boot))
    return {"mean": float(values.mean()), "lo": lo, "hi": hi, "n": len(values), "clusters": len(set(clusters.tolist()))}


def ratio_cell(num: np.ndarray, den: np.ndarray, clusters: np.ndarray, resamples: int, rng: np.random.Generator) -> dict[str, Any]:
    if not len(num):
        return {"ratio": math.nan, "lo": math.nan, "hi": math.nan, "median_ratio": math.nan, "n": 0}
    boot = [(w @ num) / (w @ den) for w in common.cluster_weights(clusters, resamples, rng)]
    lo, hi = common.percentile_interval(np.concatenate(boot))
    return {
        "ratio": float(num.sum() / den.sum()),
        "lo": lo,
        "hi": hi,
        "median_ratio": float(np.median(num / den)),
        "mean_num_ms": float(num.mean()),
        "mean_den_ms": float(den.mean()),
        "n": len(num),
        "clusters": len(set(clusters.tolist())),
    }


# ---- the cells -----------------------------------------------------------------------------------


def padded_pairs(data: Data, store: str, config: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], float | None]:
    """Raw and padded latency pairs (W1, W0) on seeds 1 and up, with T from seed 0's largest latency."""
    seed0 = [lat for seed, lat in data.single[(store, config)] if seed == 0]
    if not seed0:
        return [], [], None
    budget = float(math.ceil(max(seed0)))
    raw = data.pairs(store, config, "W1", "W0", seeds=[s for s in range(1, 1000)])
    padded = []
    for p in raw:
        a = dict(p["a"])
        b = dict(p["b"])
        a["latency"] = float(np.median([budget * math.ceil(x / budget) for x in p["a"]["lat_all"]]))
        b["latency"] = float(np.median([budget * math.ceil(x / budget) for x in p["b"]["lat_all"]]))
        padded.append({**p, "a": a, "b": b})
    return raw, padded, budget


def compute_cells(data: Data) -> dict[tuple[Any, ...], dict[str, Any]]:
    cells: dict[tuple[Any, ...], dict[str, Any]] = {}
    levels: list[Any] = [*data.levels, "all"]
    pcts: list[Any] = [*data.pcts, "all", *PCT_GROUPS]
    for store, config in data.configs:
        families: dict[str, tuple[list[dict[str, Any]], tuple[str, ...]]] = {
            "W": (data.pairs(store, config, "W1", "W0"), ("W1", "W0")),
            "AA": (data.pairs(store, config, "SEPb", "SEPa"), ("SEPb", "SEPa")),
        }
        raw, padded, budget = padded_pairs(data, store, config)
        families["RAW1"] = (raw, ("W1", "W0"))
        families["PAD"] = (padded, ("W1", "W0"))
        for kind, (pairs, slots) in families.items():
            observables = ("latency",) if kind in ("RAW1", "PAD") else OBSERVABLES
            for level in levels:
                for pct in pcts:
                    chosen = select(pairs, level, pct)
                    if not chosen:
                        continue
                    pct_list = data.pcts if pct == "all" else PCT_GROUPS.get(pct, (pct,)) if isinstance(pct, str) else (pct,)
                    error_rate = data.error_rate(store, config, slots, level, list(pct_list))
                    for observable in observables:
                        if observable == "recall" and not has_recall(store, config):
                            continue
                        rng = common.rng_for(data.seed, kind, store, config, level, pct, observable)
                        result = auc_cell(chosen, observable, data.resamples, rng)
                        if result is None:
                            continue
                        result.update(kind=kind, store=store, config=config, level=level, pct=pct,
                                      observable=observable, error_rate=error_rate, budget_ms=budget)  # fmt: skip
                        cells[(kind, store, config, level, pct, observable)] = result
    return cells


def deltas(data: Data) -> list[dict[str, Any]]:
    """Paired-AUC differences between a configuration and its mitigation, on the same resamples."""
    rows = []
    comparisons = [("post", "post-const", "W"), ("pre", "pre-exact", "W")]
    for store in sorted({s for s, _ in data.configs}):
        for base, mitigated, _ in comparisons:
            if (store, base) not in data.configs or (store, mitigated) not in data.configs:
                continue
            a_pairs = {(p["seed"], p["probe"], p["pct"]): p for p in data.pairs(store, base, "W1", "W0")}
            b_pairs = {(p["seed"], p["probe"], p["pct"]): p for p in data.pairs(store, mitigated, "W1", "W0")}
            rows += _delta_rows(data, store, f"{base} - {mitigated}", a_pairs, b_pairs)
        for config in sorted(c for s, c in data.configs if s == store):
            a_pairs = {(p["seed"], p["probe"], p["pct"]): p for p in data.pairs(store, config, "W1", "W0")}
            b_pairs = {(p["seed"], p["probe"], p["pct"]): p for p in data.pairs(store, config, "SEPb", "SEPa")}
            rows += _delta_rows(data, store, f"{config}: shared - separated", a_pairs, b_pairs)
            raw, padded, _ = padded_pairs(data, store, config)
            rows += _delta_rows(
                data,
                store,
                f"{config}: raw - padded",
                {(p["seed"], p["probe"], p["pct"]): p for p in raw},
                {(p["seed"], p["probe"], p["pct"]): p for p in padded},
                observables=("latency",),
            )
    return rows


def _delta_rows(
    data: Data,
    store: str,
    name: str,
    a_pairs: dict[tuple[int, int, int], dict[str, Any]],
    b_pairs: dict[tuple[int, int, int], dict[str, Any]],
    observables: Sequence[str] = ("latency", "count", "complete"),
) -> list[dict[str, Any]]:
    keys = sorted(set(a_pairs) & set(b_pairs))
    rows = []
    for level in [*data.levels, "all"]:
        chosen = [k for k in keys if level == "all" or a_pairs[k]["level"] == level]
        if not chosen:
            continue
        clusters = np.array([f"{k[0]}:{k[1]}" for k in chosen])
        for observable in observables:
            sign = SIGN[observable]
            da = np.array([_win(sign * a_pairs[k]["a"][observable], sign * a_pairs[k]["b"][observable]) for k in chosen])
            db = np.array([_win(sign * b_pairs[k]["a"][observable], sign * b_pairs[k]["b"][observable]) for k in chosen])
            keep = ~(np.isnan(da) | np.isnan(db))
            if not keep.any():
                continue
            diff = da[keep] - db[keep]
            rng = common.rng_for(data.seed, "delta", store, name, level, observable)
            cell = mean_cell(diff, clusters[keep], data.resamples, rng)
            rows.append({"store": store, "comparison": name, "level": level, "observable": observable,
                         "delta_paired_auc": cell["mean"], "lo": cell["lo"], "hi": cell["hi"], "pairs": cell["n"],
                         "clusters": cell["clusters"]})  # fmt: skip
    return rows


def _win(x1: float, x0: float) -> float:
    if math.isnan(x1) or math.isnan(x0):
        return math.nan
    return 1.0 if x1 > x0 else 0.5 if x1 == x0 else 0.0


def costs(data: Data) -> list[dict[str, Any]]:
    """Each mitigation's latency against the configuration it replaces, paired by (seed, probe, p, slot)."""
    rows = []
    stores = sorted({s for s, _ in data.configs})
    for store in stores:
        specs: list[tuple[str, Callable[[], list[tuple[str, float, float]]]]] = []
        for base, mitigated in (("post", "post-const"), ("pre", "pre-exact")):
            if (store, base) in data.configs and (store, mitigated) in data.configs:
                specs.append((f"M1/M2 {mitigated} / {base}", _config_ratio(data, store, mitigated, base)))
        for config in sorted(c for s, c in data.configs if s == store):
            specs.append((f"M3 separated / shared ({config})", _slot_ratio(data, store, config)))
            specs.append((f"M4 padded / raw ({config})", _padding_ratio(data, store, config)))
        for name, make in specs:
            items = make()
            if not items:
                continue
            clusters = np.array([c for c, _, _ in items])
            num = np.array([n for _, n, _ in items])
            den = np.array([d for _, _, d in items])
            rng = common.rng_for(data.seed, "cost", store, name)
            rows.append({"store": store, "mitigation": name, **ratio_cell(num, den, clusters, data.resamples, rng)})
    return rows


def _config_ratio(data: Data, store: str, num: str, den: str) -> Callable[[], list[tuple[str, float, float]]]:
    def make() -> list[tuple[str, float, float]]:
        items = []
        for key, a in data.obs.items():
            if key[0] == store and key[1] == num and key[5] in ("W0", "W1"):
                b = data.obs.get((store, den, *key[2:]))
                if b is not None:
                    items.append((f"{key[2]}:{key[3]}", a["latency"], b["latency"]))
        return items

    return make


def _slot_ratio(data: Data, store: str, config: str) -> Callable[[], list[tuple[str, float, float]]]:
    def make() -> list[tuple[str, float, float]]:
        return [(f"{p['seed']}:{p['probe']}", p["a"]["latency"], p["b"]["latency"]) for p in data.pairs(store, config, "SEPa", "W0")]

    return make


def _padding_ratio(data: Data, store: str, config: str) -> Callable[[], list[tuple[str, float, float]]]:
    def make() -> list[tuple[str, float, float]]:
        raw, padded, _ = padded_pairs(data, store, config)
        items = []
        for r, p in zip(raw, padded, strict=True):
            cluster = f"{r['seed']}:{r['probe']}"
            items.append((cluster, p["a"]["latency"], r["a"]["latency"]))
            items.append((cluster, p["b"]["latency"], r["b"]["latency"]))
        return items

    return make


def list_changes(data: Data) -> dict[tuple[Any, ...], dict[str, Any]]:
    found: dict[tuple[Any, ...], dict[str, Any]] = {}
    for store, config in data.configs:
        for kind, (a, b) in (("W", ("W1", "W0")), ("AA", ("SEPb", "SEPa"))):
            pairs = data.pairs(store, config, a, b)
            for level in [*data.levels, "all"]:
                for pct in [*data.pcts, "all"]:
                    chosen = select(pairs, level, pct)
                    if not chosen:
                        continue
                    changed = np.array([0.0 if p["a"]["ids"] == p["b"]["ids"] else 1.0 for p in chosen])
                    ids_only = np.array([0.0 if p["a"]["ids"][0] == p["b"]["ids"][0] else 1.0 for p in chosen])
                    clusters = np.array([f"{p['seed']}:{p['probe']}" for p in chosen])
                    rng = common.rng_for(data.seed, "change", kind, store, config, level, pct)
                    cell = mean_cell(changed, clusters, data.resamples, rng)
                    found[(kind, store, config, level, pct)] = {
                        "kind": kind, "store": store, "config": config, "level": level, "pct": pct,
                        "deterministic": (store, config) in DETERMINISTIC, "rate": cell["mean"], "lo": cell["lo"],
                        "hi": cell["hi"], "ids_rate": float(ids_only.mean()), "pairs": cell["n"],
                        "clusters": cell["clusters"], "seeds": len({p["seed"] for p in chosen}),
                    }  # fmt: skip
    return found


# ---- guards and verdicts -------------------------------------------------------------------------


class Judge:
    def __init__(self, data: Data, cells: dict[tuple[Any, ...], dict[str, Any]], changes: dict[tuple[Any, ...], dict[str, Any]]) -> None:
        self.data = data
        self.cells = cells
        self.changes = changes
        self.rows: list[dict[str, Any]] = []
        self.guard_rows: list[dict[str, Any]] = []
        self.g1: dict[tuple[str, str], bool | None] = {}
        self.g2: dict[str, bool | None] = {}
        self._guards()

    # cells

    def cell(self, kind: str, store: str, config: str, level: Any, pct: Any, observable: str) -> dict[str, Any] | None:
        return self.cells.get((kind, store, config, level, pct, observable))

    @staticmethod
    def usable(c: dict[str, Any] | None, seeds: int = MIN_SEEDS) -> bool:
        if c is None:
            return False
        rate = c.get("error_rate")
        bad_rate = rate is not None and not math.isnan(rate) and rate > MAX_ERROR_RATE
        return c["clusters"] >= MIN_CLUSTERS and c["seeds"] >= seeds and not bad_rate

    @staticmethod
    def show(c: dict[str, Any] | None, key: str = "paired") -> str:
        if c is None:
            return "missing"
        return f"{c[key]:.3f} [{c[key + '_lo']:.3f}, {c[key + '_hi']:.3f}] ({c['clusters']} clusters, {c['seeds']} seeds)"

    # guards

    def _guards(self) -> None:
        for store, config in self.data.configs:
            c = self.cell("AA", store, config, "all", "all", "latency")
            ok = None if not self.usable(c) else bool(c and 0.40 <= c["paired_lo"] and c["paired_hi"] <= 0.60)
            self.g1[(store, config)] = ok
            self.guard_rows.append({"guard": "G1", "store": store, "config": config, "passed": ok, "evidence": self.show(c)})
        for store in sorted({s for s, _ in self.data.configs}):
            exact = [c for s, c in self.data.configs if s == store and ((s, c) in DETERMINISTIC and c in ("pre-exact", "pre"))
                     and not (s == "memory")]  # fmt: skip
            results = []
            for config in exact:
                change = self.changes.get(("W", store, config, "all", "all"))
                if change is not None:
                    results.append((config, change["rate"]))
            ok = None if not results else all(rate <= 0.01 for _, rate in results)
            self.g2[store] = ok
            self.guard_rows.append({"guard": "G2", "store": store, "config": ",".join(c for c, _ in results),
                                    "passed": ok, "evidence": "; ".join(f"{c}: change rate {r:.4f}" for c, r in results)})  # fmt: skip

    def latency_guard(self, store: str, config: str) -> bool:
        return self.g1.get((store, config)) is True

    # parts

    def at_least(self, c: dict[str, Any] | None, threshold: float, falsify_below: float | None) -> str:
        if not self.usable(c):
            return INCONCLUSIVE
        assert c is not None
        if falsify_below is not None and c["paired"] < falsify_below:
            return FALSIFIED
        return CONFIRMED if c["paired"] >= threshold else INCONCLUSIVE

    def present(self, c: dict[str, Any] | None, threshold: float, falsify_hi_below: float | None) -> str:
        if not self.usable(c):
            return INCONCLUSIVE
        assert c is not None
        if falsify_hi_below is not None and c["paired_hi"] < falsify_hi_below:
            return FALSIFIED
        return CONFIRMED if c["paired"] >= threshold and c["paired_lo"] > 0.55 else INCONCLUSIVE

    def absent(self, c: dict[str, Any] | None, *, upper: float = 0.60, falsify_lo_above: float = 0.60) -> str:
        if not self.usable(c):
            return INCONCLUSIVE
        assert c is not None
        if c["paired_lo"] > falsify_lo_above:
            return FALSIFIED
        return CONFIRMED if 0.40 <= c["paired_lo"] and c["paired_hi"] <= upper else INCONCLUSIVE

    def part(self, hypothesis: str, store: str, config: str, label: str, outcome: str, evidence: str, *, latency: bool = False) -> str:
        if latency and outcome != INCONCLUSIVE and not self.latency_guard(store, config):
            outcome, evidence = INCONCLUSIVE, f"{evidence}; guard G1 did not pass"
        if self.g2.get(store) is False:
            outcome, evidence = INCONCLUSIVE, f"{evidence}; guard G2 failed for {store}"
        self.rows.append({"hypothesis": hypothesis, "store": store, "config": config, "part": label, "outcome": outcome, "evidence": evidence})
        return outcome

    def verdict(self, hypothesis: str, scope: str, outcomes: list[str]) -> None:
        if not outcomes:
            outcome = INCONCLUSIVE
        elif FALSIFIED in outcomes:
            outcome = FALSIFIED
        elif all(o == CONFIRMED for o in outcomes):
            outcome = CONFIRMED
        else:
            outcome = INCONCLUSIVE
        self.rows.append({"hypothesis": hypothesis, "store": scope, "config": "", "part": "VERDICT", "outcome": outcome,
                          "evidence": f"{outcomes.count(CONFIRMED)} confirmed, {outcomes.count(FALSIFIED)} falsified, "
                                      f"{outcomes.count(INCONCLUSIVE)} inconclusive parts"})  # fmt: skip

    def observables(self, store: str, config: str) -> list[str]:
        return [o for o in OBSERVABLES if o != "recall" or has_recall(store, config)]

    # hypotheses

    def h1(self) -> None:
        outcomes = []
        for store in VECTOR_STORES:
            config = "post"
            for pct in self.data.pcts:
                c = self.cell("W", store, config, 1000, pct, "count")
                outcomes.append(self.part("H1", store, config, f"(a) m=1000 p={pct} count >= 0.95", self.at_least(c, 0.95, 0.80), self.show(c)))
            for pct in (10, 50):
                c = self.cell("W", store, config, 100, pct, "latency")
                outcome = self.present(c, 0.75, 0.60 if pct == 50 else None)
                outcomes.append(self.part("H1", store, config, f"(b) m=100 p={pct} latency >= 0.75", outcome, self.show(c), latency=True))
            for observable in self.observables(store, config):
                c = self.cell("W", store, config, 1, "all", observable)
                outcomes.append(self.part("H1", store, config, f"(c) m=1 no channel in {observable}", self.absent(c), self.show(c),
                                          latency=observable == "latency"))  # fmt: skip
        self.verdict("H1", "vector stores", outcomes)

    def h2(self) -> None:
        outcomes = []
        for store in VECTOR_STORES:
            config = "post-const"
            c = self.cell("W", store, config, "all", "all", "latency")
            outcomes.append(self.part("H2", store, config, "(a) no latency channel pooled", self.absent(c), self.show(c), latency=True))
            c = self.cell("W", store, config, 1000, "all", "latency")
            outcomes.append(self.part("H2", store, config, "(a) m=1000 latency upper <= 0.65",
                                      self.absent(c, upper=0.65), self.show(c), latency=True))  # fmt: skip
            for pct in (10, 50):
                c = self.cell("W", store, config, 1000, pct, "count")
                outcomes.append(self.part("H2", store, config, f"(b) m=1000 p={pct} count >= 0.95", self.at_least(c, 0.95, 0.80), self.show(c)))
        self.verdict("H2", "vector stores", outcomes)

    def h3(self) -> None:
        for name, store, cells in (
            ("H3a", "pgvector", ((1000, 10), (1000, 50), (100, 50))),
            ("H3b", "elasticsearch", ((1000, 10), (1000, 50))),
        ):
            outcomes = []
            for level, pct in cells:
                c = self.cell("W", store, "pre", level, pct, "latency")
                falsify = 0.60 if (level, pct) == (1000, 50) else None
                outcomes.append(self.part(name, store, "pre", f"m={level} p={pct} latency >= 0.75", self.present(c, 0.75, falsify),
                                          self.show(c), latency=True))  # fmt: skip
            self.verdict(name, store, outcomes)
        outcomes = []
        for observable in self.observables("qdrant", "pre"):
            c = self.cell("W", "qdrant", "pre", "all", "low", observable)
            outcomes.append(self.part("H3c", "qdrant", "pre", f"p in (1, 10): no channel in {observable}", self.absent(c), self.show(c),
                                      latency=observable == "latency"))  # fmt: skip
        self.verdict("H3c", "qdrant", outcomes)

    def h4(self) -> None:
        for store, config in (("pgvector", "pre-exact"), ("qdrant", "pre-exact"), ("elasticsearch", "pre-exact"), ("faiss", "pre"), ("memory", "pre")):
            outcomes = []
            for observable in self.observables(store, config):
                c = self.cell("W", store, config, "all", "all", observable)
                outcomes.append(self.part("H4", store, config, f"no channel in {observable} pooled", self.absent(c), self.show(c),
                                          latency=observable == "latency"))  # fmt: skip
                c = self.cell("W", store, config, 1000, "all", observable)
                outcome = self.absent(c, upper=0.65, falsify_lo_above=0.65)
                outcomes.append(self.part("H4", store, config, f"m=1000 {observable} upper <= 0.65", outcome, self.show(c),
                                          latency=observable == "latency"))  # fmt: skip
            self.verdict("H4", f"{store} {config}", outcomes)

    def change(self, store: str, config: str, level: Any) -> dict[str, Any] | None:
        return self.changes.get(("W", store, config, level, "all"))

    def show_change(self, c: dict[str, Any] | None) -> str:
        if c is None:
            return "missing"
        return f"change rate {c['rate']:.3f} [{c['lo']:.3f}, {c['hi']:.3f}] ({c['clusters']} clusters, {c['seeds']} seeds)"

    def change_usable(self, c: dict[str, Any] | None) -> bool:
        return c is not None and c["clusters"] >= MIN_CLUSTERS and c["seeds"] >= MIN_SEEDS

    def h5(self) -> None:
        for store in ("elasticsearch", "qdrant"):
            outcomes = []
            for level in self.data.levels:
                c = self.cell("W", store, "bm25-pre", level, "all", "score")
                outcome = self.at_least(c, 0.90, None)
                if level == 1000 and self.usable(c) and c is not None and c["paired_hi"] < 0.70:
                    outcome = FALSIFIED
                outcomes.append(self.part("H5a", store, "bm25-pre", f"m={level} score >= 0.90", outcome, self.show(c)))
            self.verdict("H5a", store, outcomes)
        outcomes = []
        c = self.cell("W", "pgvector", "bm25-pre", "all", "all", "score")
        outcomes.append(self.part("H5b", "pgvector", "bm25-pre", "no channel in the score", self.absent(c), self.show(c)))
        change = self.change("pgvector", "bm25-pre", "all")
        if not self.change_usable(change):
            outcome = INCONCLUSIVE
        else:
            assert change is not None
            outcome = FALSIFIED if change["rate"] > 0.05 else CONFIRMED if change["rate"] <= 0.01 else INCONCLUSIVE
        outcomes.append(self.part("H5b", "pgvector", "bm25-pre", "id-list change rate <= 0.01", outcome, self.show_change(change)))
        self.verdict("H5b", "pgvector", outcomes)
        change = self.change("elasticsearch", "hybrid-exact", 1000)
        if not self.change_usable(change):
            outcome = INCONCLUSIVE
        else:
            assert change is not None
            outcome = CONFIRMED if change["rate"] >= 0.25 else FALSIFIED if change["rate"] < 0.05 else INCONCLUSIVE
        part = self.part("H5c", "elasticsearch", "hybrid-exact", "m=1000 change rate >= 0.25", outcome, self.show_change(change))
        self.verdict("H5c", "elasticsearch", [part])

    def h6(self) -> None:
        outcomes = []
        for store, config in self.data.configs:
            complete_seeds = {s for s, _ in self.data.single[(store, config)]}
            for level in self.data.levels:
                raw = self.cell("RAW1", store, config, level, "all", "latency")
                if raw is None or raw["paired"] < 0.75:
                    continue
                padded = self.cell("PAD", store, config, level, "all", "latency")
                # T comes from seed 0 and the cells use seeds 1 to 4: the rule needs all five seeds.
                outcome = self.absent(padded) if len(complete_seeds) >= MIN_SEEDS and self.usable(padded, seeds=MIN_SEEDS - 1) else INCONCLUSIVE
                outcomes.append(self.part("H6", store, config, f"m={level} padded latency: no channel",
                                          outcome, f"raw {self.show(raw)}; padded {self.show(padded)}", latency=True))  # fmt: skip
        self.verdict("H6", "every cell with a raw latency channel", outcomes)

    def all(self) -> list[dict[str, Any]]:
        self.h1()
        self.h2()
        self.h3()
        self.h4()
        self.h5()
        self.h6()
        return self.rows


# ---- health and report ---------------------------------------------------------------------------


def health(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stores: dict[str, dict[str, Any]] = {}
    for r in records:
        store = r.get("store")
        if not store or r.get("exp") != "x6":
            continue
        h = stores.setdefault(store, {"store": store, "mode": r.get("mode"), "seeds_done": [], "skipped": [], "aborted": [],
                                      "retrievals": 0, "errors": defaultdict(int), "first_error": {}, "stopped": [],
                                      "builds": defaultdict(list), "setup_error": None, "leaks": 0, "versions": None})  # fmt: skip
        kind = r.get("type")
        if kind == "retrieval":
            h["retrievals"] += 1
            if r.get("error"):
                h["errors"][r["config"]] += 1
                h["first_error"].setdefault(r["config"], r["error"])
        elif kind == "seed-end" and r.get("complete"):
            h["seeds_done"].append(r["seed"])
        elif kind == "seed-skipped":
            h["skipped"].append(r["seed"])
        elif kind == "seed-aborted":
            h["aborted"].append(r["seed"])
        elif kind == "config-stopped":
            h["stopped"].append(f"{r['config']}@{r['seed']}")
        elif kind == "build":
            h["builds"][r["world"]].append(r["seconds"])
        elif kind == "setup-error":
            h["setup_error"] = r.get("error")
        elif kind == "leak":
            h["leaks"] += 1
        elif kind == "versions":
            h["versions"] = {"image": (r.get("image") or {}).get("image"), "reported": r.get("reported")}
    rows = []
    for h in stores.values():
        rows.append({
            **{k: v for k, v in h.items() if k not in ("errors", "builds")},
            "errors": dict(h["errors"]),
            "build_s": {w: round(float(np.mean(v)), 1) for w, v in h["builds"].items()},
        })  # fmt: skip
    return rows


def report(data: Data, cells: dict[tuple[Any, ...], dict[str, Any]], verdicts: list[dict[str, Any]], judge: Judge,
           cost_rows: list[dict[str, Any]], changes: dict[tuple[Any, ...], dict[str, Any]], health_rows: list[dict[str, Any]],
           unreadable: int) -> str:  # fmt: skip
    lines = ["# X6: side channels of permission-aware retrieval", ""]
    lines += [f"{len(data.records):,} records ({unreadable} unreadable lines), {data.resamples:,} bootstrap resamples, seed {data.seed}. "
              "Verdicts follow PREREG_X3_X6.md. AUC: 0.5 means no advantage; the paired AUC is the differencing attacker's.", ""]  # fmt: skip
    lines += ["## Health", ""]
    lines += common.markdown_table(
        ["store", "mode", "seeds done", "skipped", "retrievals", "errors", "stopped", "build s", "setup error", "leaks"],
        [[h["store"], h["mode"], h["seeds_done"], h["skipped"], h["retrievals"], json.dumps(h["errors"]), h["stopped"],
          json.dumps(h["build_s"]), h["setup_error"], h["leaks"]] for h in health_rows],
    )  # fmt: skip
    lines += ["## Verdicts", ""]
    lines += common.markdown_table(
        ["hypothesis", "scope", "outcome", "evidence"],
        [[v["hypothesis"], v["store"], v["outcome"], v["evidence"]] for v in verdicts if v["part"] == "VERDICT"],
    )
    lines += ["## Guards", ""]
    lines += common.markdown_table(["guard", "store", "config", "passed", "evidence"],
                                   [[g["guard"], g["store"], g["config"], g["passed"], g["evidence"]] for g in judge.guard_rows])  # fmt: skip
    lines += ["## Paired AUC (W1 against W0), pooled over selectivity", ""]
    rows = []
    for store, config in data.configs:
        for level in [*data.levels, "all"]:
            row: list[Any] = [store, config, level]
            for observable in OBSERVABLES:
                c = cells.get(("W", store, config, level, "all", observable))
                row.append("" if c is None else f"{c['paired']:.2f} [{c['paired_lo']:.2f}, {c['paired_hi']:.2f}]")
            aa = cells.get(("AA", store, config, level, "all", "latency"))
            row.append("" if aa is None else f"{aa['paired']:.2f} [{aa['paired_lo']:.2f}, {aa['paired_hi']:.2f}]")
            rows.append(row)
    lines += common.markdown_table(["store", "config", "m", *OBSERVABLES, "A/A latency"], rows)
    lines += ["## Mitigation costs (latency, ratio of means)", ""]
    lines += common.markdown_table(
        ["store", "mitigation", "ratio", "interval", "median ratio", "pairs"],
        [[r["store"], r["mitigation"], r["ratio"], f"[{r['lo']:.2f}, {r['hi']:.2f}]", r["median_ratio"], r["n"]] for r in cost_rows],
    )
    lines += ["## Id-list change rate, W1 against W0 (deterministic configurations)", ""]
    lines += common.markdown_table(
        ["store", "config", "m", "rate", "interval", "A/A rate", "pairs"],
        [[c["store"], c["config"], c["level"], c["rate"], f"[{c['lo']:.2f}, {c['hi']:.2f}]",
          (changes.get(("AA", c["store"], c["config"], c["level"], "all")) or {}).get("rate"), c["pairs"]]
         for key, c in sorted(changes.items(), key=lambda kv: str(kv[0]))
         if key[0] == "W" and key[4] == "all" and c["deterministic"]],
    )  # fmt: skip
    lines += ["## Every verdict part", ""]
    lines += common.markdown_table(
        ["hypothesis", "store", "config", "part", "outcome", "evidence"],
        [[v["hypothesis"], v["store"], v["config"], v["part"], v["outcome"], v["evidence"]] for v in verdicts if v["part"] != "VERDICT"],
    )
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
    paths = sorted(Path(args.folder).glob("**/x6-*.jsonl"))
    records, unreadable = common.read_records(paths)
    common.log(f"x6 stats: {len(records):,} records from {len(paths)} files")
    data = Data(records, args.resamples, args.seed)
    health_rows = health(records)
    common.write_csv(out / "x6_health.csv", health_rows)
    if args.annotate:
        common.annotate("notice", "x6 health", json.dumps(health_rows, default=str), chunks=3)
    if not data.obs:
        (out / "x6_report.md").write_text("# X6\n\nNo retrieval was recorded.\n", encoding="utf-8")
        common.annotate("warning", "x6 stats", "no X6 retrieval was recorded")
        return 0
    cells = compute_cells(data)
    common.write_csv(out / "x6_cells.csv", list(cells.values()))
    common.write_csv(out / "x6_deltas.csv", deltas(data))
    cost_rows = costs(data)
    common.write_csv(out / "x6_costs.csv", cost_rows)
    changes = list_changes(data)
    common.write_csv(out / "x6_listchange.csv", list(changes.values()))
    judge = Judge(data, cells, changes)
    verdicts = judge.all()
    common.write_csv(out / "x6_verdicts.csv", [*judge.guard_rows, *verdicts])
    text = report(data, cells, verdicts, judge, cost_rows, changes, health_rows, unreadable)
    (out / "x6_report.md").write_text(text, encoding="utf-8")
    if args.annotate:
        summary = [f"{v['hypothesis']} {v['store']}: {v['outcome']}" for v in verdicts if v["part"] == "VERDICT"]
        summary += [f"{g['guard']} {g['store']} {g['config']}: {g['passed']}" for g in judge.guard_rows]
        common.annotate("notice", "x6 verdicts", "\n".join(summary), chunks=2)
        headline = []
        for store, config in data.configs:
            for observable in ("latency", "count", "score"):
                c = cells.get(("W", store, config, "all", "all", observable))
                if c is not None:
                    headline.append(f"{store} {config} {observable}: paired {c['paired']:.2f} [{c['paired_lo']:.2f},{c['paired_hi']:.2f}] n={c['pairs']}")
        common.annotate("notice", "x6 cells (all m, all p)", "\n".join(headline), chunks=4)
    common.log("x6 stats: done")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException as error:
        if not isinstance(error, SystemExit):
            common.fail_loudly("x6 stats", error)
        raise
