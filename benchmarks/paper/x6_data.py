"""Experiments X3 and X6, the data job: FiQA and SciDocs, their embeddings, and X6's plans.

Downloads BEIR FiQA-2018 (corpus and queries) and BEIR SciDocs (corpus), embeds them on the CPU with
sentence-transformers/all-MiniLM-L6-v2, and computes, by exact search, the plan of every X6 seed
(PREREG_X3_X6.md with its Amendment 1): 8 groups of probes, each probe's near set (its m nearest
passages that are not hubs) and zone, the far chunks that replace a group's near sets in its W0, the
permission buckets, and each probe's exact readable top 10. Every store job reads these files, so all
stores play the identical game. X3 reads the FiQA embeddings as its semantic subset.

    python x6_data.py --out x6data [--mode full|smoke] [--seeds 5] [--cache x6cache]

With --cache, the texts and embeddings are read from that folder when it holds them for the same
model and corpus, and written to it otherwise (the workflow keeps it with actions/cache). Smoke and
full runs use the same corpus and the same plans; a smoke run plans seed 0 only.

Writes to --out: fiqa_corpus.jsonl/.npy, fiqa_queries.jsonl/.npy, scidocs_subset.jsonl/.npy,
plan_seed<N>.json and manifest.json. Needs numpy, sentence-transformers (with torch) and
huggingface-hub; pyarrow when a source serves Parquet. It does not import wardowl.
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import os
import re
import shutil
import sys
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import x3x6_common as common
from x3x6_common import DIM, K, SEED_BASE, log

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MAX_SEQ_LENGTH = 256
SCIDOCS_SUBSET = 12_000
UKP = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{name}.zip"
EMBEDDED = ("fiqa_corpus", "fiqa_queries", "scidocs_subset")
EMBEDDING_KEY = f"{MODEL}|max_seq_length={MAX_SEQ_LENGTH}|fiqa=all|scidocs={SCIDOCS_SUBSET}|v1"
PCTS = (1, 10, 50)
GROUPS = 8
PER_GROUP = {1000: 1, 100: 2, 10: 3, 1: 3}  # probes per level in each group (8, 16, 24, 24 per seed)
ZONE = 1000  # a zone reaches 1,000 passages past the m-th near passage
HUB_SHARE = 0.01  # the share of passages that are hubs
HUB_DEPTH = 2000  # hubs are counted among each query's 2,000 nearest passages
DEPTH = 3000  # neighbours kept per query: room for the m-th near passage, hubs skipped, plus the zone


# ---- the datasets --------------------------------------------------------------------------------


def _read(path: str) -> list[dict[str, Any]]:
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq

        rows: list[dict[str, Any]] = pq.read_table(path).to_pylist()
        return rows
    opener: Any = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _pick(files: list[str], stem: str) -> list[str]:
    """The files of one table (corpus or queries) in a dataset repository, in order of preference."""
    patterns = (
        rf"^{stem}\.jsonl\.gz$",
        rf"^{stem}\.jsonl$",
        rf"(^|/){stem}[^/]*\.jsonl(\.gz)?$",
        rf"(^|/){stem}/[^/]*\.parquet$",
        rf"(^|/){stem}[^/]*\.parquet$",
    )
    for pattern in patterns:
        found = sorted(f for f in files if re.search(pattern, f) and "qrels" not in f)
        if found:
            return found
    return []


def _from_hub(repo: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    from huggingface_hub import HfApi, hf_hub_download

    files = list(HfApi().list_repo_files(repo, repo_type="dataset"))
    corpus, queries = _pick(files, "corpus"), _pick(files, "queries")
    if not corpus:
        raise FileNotFoundError(f"{repo}: no corpus file among {files[:30]}")
    rows = [row for name in corpus for row in _read(hf_hub_download(repo, name, repo_type="dataset"))]
    asked = [row for name in queries for row in _read(hf_hub_download(repo, name, repo_type="dataset"))]
    return rows, asked


def _from_ukp(name: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    request = urllib.request.Request(UKP.format(name=name), headers={"User-Agent": "wardowl-paper"})  # noqa: S310
    with urllib.request.urlopen(request, timeout=900) as response:  # noqa: S310
        data = response.read()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()

        def table(stem: str) -> list[dict[str, Any]]:
            member = next((n for n in names if n == f"{stem}.jsonl" or n.endswith(f"/{stem}.jsonl")), None)
            if member is None:
                return []
            with archive.open(member) as handle:
                return [json.loads(line) for line in io.TextIOWrapper(handle, encoding="utf-8") if line.strip()]

        return table("corpus"), table("queries")


def fetch(name: str, *, need_queries: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    """A BEIR dataset's corpus and queries, from the first source that serves them."""
    sources = [("hub", f"BeIR/{name}"), ("hub", f"mteb/{name}"), ("ukp", name)]
    problems = []
    for kind, where in sources:
        try:
            corpus, queries = _from_hub(where) if kind == "hub" else _from_ukp(where)
        except Exception as error:
            problems.append(f"{kind}:{where}: {common.short(error, 300)}")
            log(f"  {name}: {kind} {where} failed: {common.short(error, 300)}")
            continue
        if len(corpus) < 1000 or (need_queries and len(queries) < 100):
            problems.append(f"{kind}:{where}: {len(corpus)} passages and {len(queries)} queries")
            continue
        log(f"  {name}: {len(corpus):,} passages and {len(queries):,} queries from {kind} {where}")
        return corpus, queries, f"{kind}:{where}"
    raise RuntimeError(f"no source served {name}: {problems}")


def passages(rows: list[dict[str, Any]], prefix: str) -> list[tuple[str, str]]:
    """(id, text) pairs, the title joined to the text, sorted by id, without repeated ids."""
    found: dict[str, str] = {}
    for row in rows:
        raw = row.get("_id", row.get("id"))
        if raw is None:
            continue
        key = f"{prefix}-{raw}"
        if key in found:
            continue
        title = str(row.get("title") or "").strip()
        text = str(row.get("text") or "").strip()
        found[key] = f"{title}\n{text}".strip() if title else text
    return sorted(found.items())


def subset(items: list[tuple[str, str]], size: int | None, label: str) -> list[tuple[str, str]]:
    if size is None or size >= len(items):
        return items
    rng = np.random.default_rng([SEED_BASE, sum(map(ord, label))])
    chosen = np.sort(rng.choice(len(items), size=size, replace=False))
    return [items[i] for i in chosen]


def write_texts(folder: Path, name: str, items: list[tuple[str, str]], vectors: np.ndarray) -> None:
    with (folder / f"{name}.jsonl").open("w", encoding="utf-8") as handle:
        for key, text in items:
            handle.write(json.dumps({"id": key, "text": text}) + "\n")
    np.save(folder / f"{name}.npy", vectors.astype(np.float32))


def read_texts(folder: Path, name: str) -> tuple[list[tuple[str, str]], np.ndarray]:
    items = []
    with (folder / f"{name}.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            items.append((row["id"], row["text"]))
    return items, np.load(folder / f"{name}.npy")


# ---- embeddings ----------------------------------------------------------------------------------


def load_model() -> tuple[Any, dict[str, Any]]:
    import torch
    from sentence_transformers import SentenceTransformer

    torch.set_num_threads(os.cpu_count() or 4)
    model = SentenceTransformer(MODEL, device="cpu")
    model.max_seq_length = MAX_SEQ_LENGTH
    dim = model.get_sentence_embedding_dimension()
    if dim != DIM:
        raise RuntimeError(f"{MODEL} gives {dim} dimensions, not {DIM}")
    revision = None
    try:
        from huggingface_hub import model_info

        revision = model_info(MODEL).sha
    except Exception as error:
        log(f"  could not read the model's revision: {common.short(error, 200)}")
    described = {"model": MODEL, "revision": revision, "max_seq_length": MAX_SEQ_LENGTH}
    return model, {**described, "threads": torch.get_num_threads()}


def embed(model: Any, texts: list[str], label: str) -> np.ndarray:
    out = np.zeros((len(texts), DIM), dtype=np.float32)
    started = time.monotonic()
    step = 2048
    for start in range(0, len(texts), step):
        part = texts[start : start + step]
        out[start : start + len(part)] = model.encode(
            part, batch_size=64, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False
        )
        done = start + len(part)
        rate = done / max(1e-9, time.monotonic() - started)
        left = (len(texts) - done) / max(rate, 1e-9) / 60
        log(f"  {label}: {done:,}/{len(texts):,} embedded ({rate:.0f} per s, {left:.1f} min left)")
    return out


def cached(cache: Path | None) -> dict[str, Any] | None:
    """The cache's description, when it holds the texts and embeddings of this model and corpus."""
    if cache is None or not (cache / "embeddings.json").is_file():
        return None
    try:
        info: dict[str, Any] = json.loads((cache / "embeddings.json").read_text(encoding="utf-8"))
    except ValueError:
        return None
    if info.get("key") != EMBEDDING_KEY:
        return None
    for name in EMBEDDED:
        if not (cache / f"{name}.jsonl").is_file() or not (cache / f"{name}.npy").is_file():
            return None
    return info


def texts_and_embeddings(out: Path, cache: Path | None) -> dict[str, Any]:
    """Writes the three embedded tables to `out`, from the cache or computed, and describes them."""
    found = cached(cache)
    if found is not None and cache is not None:
        log(f"  texts and embeddings from the cache ({cache})")
        for name in EMBEDDED:
            for suffix in (".jsonl", ".npy"):
                shutil.copyfile(cache / f"{name}{suffix}", out / f"{name}{suffix}")
        return {**found, "from_cache": True}
    clock = time.monotonic()
    fiqa_rows, fiqa_queries, fiqa_source = fetch("fiqa", need_queries=True)
    scidocs_rows, _, scidocs_source = fetch("scidocs", need_queries=False)
    corpus_items = passages(fiqa_rows, "fiqa")
    query_items = passages(fiqa_queries, "q")
    far_items = subset([item for item in passages(scidocs_rows, "scid") if item[1]], SCIDOCS_SUBSET, "scidocs")
    del fiqa_rows, fiqa_queries, scidocs_rows
    download_s = round(time.monotonic() - clock, 1)
    log(f"  {len(corpus_items):,} FiQA passages, {len(query_items):,} queries, {len(far_items):,} SciDocs passages")
    clock = time.monotonic()
    model, model_info = load_model()
    tables = {
        "fiqa_corpus": (corpus_items, embed(model, [t for _, t in corpus_items], "FiQA passages")),
        "fiqa_queries": (query_items, embed(model, [t for _, t in query_items], "FiQA queries")),
        "scidocs_subset": (far_items, embed(model, [t for _, t in far_items], "SciDocs passages")),
    }
    info = {
        "key": EMBEDDING_KEY,
        "embedding": model_info,
        "sources": {"fiqa": fiqa_source, "scidocs": scidocs_source},
        "counts": {name: len(items) for name, (items, _) in tables.items()},
        "timings": {"download_s": download_s, "embed_s": round(time.monotonic() - clock, 1)},
        "versions": common.versions("sentence-transformers", "torch", "transformers", "huggingface-hub", "tokenizers"),
    }
    for name, (items, vectors) in tables.items():
        write_texts(out, name, items, vectors)
    if cache is not None:
        cache.mkdir(parents=True, exist_ok=True)
        for name in EMBEDDED:
            for suffix in (".jsonl", ".npy"):
                shutil.copyfile(out / f"{name}{suffix}", cache / f"{name}{suffix}")
        (cache / "embeddings.json").write_text(json.dumps(info, indent=2, default=str), encoding="utf-8")
    return {**info, "from_cache": False}


# ---- plans ---------------------------------------------------------------------------------------


def neighbours(queries: np.ndarray, corpus: np.ndarray, depth: int) -> tuple[np.ndarray, np.ndarray]:
    """For each query, the `depth` most similar corpus rows (indices and similarities), best first."""
    depth = min(depth, len(corpus))
    index = np.empty((len(queries), depth), dtype=np.int32)
    similarity = np.empty((len(queries), depth), dtype=np.float32)
    for start in range(0, len(queries), 256):
        block = queries[start : start + 256] @ corpus.T
        part = np.argpartition(-block, depth - 1, axis=1)[:, :depth]
        values = np.take_along_axis(block, part, axis=1)
        order = np.argsort(-values, axis=1, kind="stable")
        index[start : start + len(block)] = np.take_along_axis(part, order, axis=1)
        similarity[start : start + len(block)] = np.take_along_axis(values, order, axis=1)
    return index, similarity


def hub_mask(near_index: np.ndarray, n: int) -> tuple[np.ndarray, dict[str, Any]]:
    """Hubs: the HUB_SHARE of passages found among the HUB_DEPTH nearest of the most queries."""
    counts = np.bincount(near_index[:, :HUB_DEPTH].ravel(), minlength=n)
    take = max(1, round(HUB_SHARE * n))
    order = np.argsort(-counts, kind="stable")
    mask = np.zeros(n, dtype=bool)
    mask[order[:take]] = True
    expected = near_index.shape[0] * min(HUB_DEPTH, near_index.shape[1]) / n
    described = {
        "hubs": int(take),
        "count_threshold": int(counts[order[take - 1]]),
        "count_max": int(counts.max()),
        "count_median": float(np.median(counts)),
        "count_expected": round(float(expected), 1),
    }
    return mask, described


class Candidate:
    """A query's near set (its m nearest passages that are not hubs) and its zone."""

    def __init__(self, q: int, m: int, near_index: np.ndarray, near_similarity: np.ndarray, hubs: np.ndarray) -> None:
        ranked = near_index[q]
        positions = np.flatnonzero(~hubs[ranked])[:m]
        self.ok = len(positions) == m and int(positions[-1]) + 1 + ZONE <= ranked.shape[0]
        if not self.ok:
            return
        depth = int(positions[-1]) + 1 + ZONE  # the zone: up to the m-th near passage, plus ZONE
        self.near = ranked[positions]
        self.zone = ranked[:depth]
        self.tau = float(near_similarity[q, depth - 1])
        self.rank_m = int(positions[-1]) + 1


def make_plan(
    seed: int,
    corpus: np.ndarray,
    queries: np.ndarray,
    query_ids: list[str],
    near_index: np.ndarray,
    near_similarity: np.ndarray,
    hubs: np.ndarray,
    far_vectors: np.ndarray,
    tokens: np.ndarray,
) -> dict[str, Any]:
    n = len(corpus)
    rng = np.random.default_rng([SEED_BASE, seed])
    order = [int(q) for q in rng.permutation(len(queries))]
    # Every secret of the seed. Near sets of different groups may share passages (Amendment 2): a
    # shared passage is replaced in the W0 of each group it belongs to, so every probe's two worlds
    # still differ in its own group's secrets only.
    claimed = np.zeros(n, dtype=bool)
    used: set[int] = set()
    probes: list[dict[str, Any]] = []
    shortfall: list[dict[str, Any]] = []
    for group in range(GROUPS):
        zone = np.zeros(n, dtype=bool)  # the group's zones
        secret = np.zeros(n, dtype=bool)  # the group's near sets
        for m in sorted(PER_GROUP, reverse=True):
            for _ in range(PER_GROUP[m]):
                chosen: tuple[int, Candidate] | None = None
                for q in order:
                    if q in used:
                        continue
                    c = Candidate(q, m, near_index, near_similarity, hubs)
                    # Within the group, no near set inside a mate's zone, in either direction.
                    if not c.ok or zone[c.near].any() or secret[c.zone].any():
                        continue
                    chosen = (q, c)
                    break
                if chosen is None:
                    shortfall.append({"group": group, "level": m})
                    log(f"  seed {seed}: group {group}: no probe could be placed at level {m}")
                    continue
                q, c = chosen
                used.add(q)
                claimed[c.near] = True
                secret[c.near] = True
                zone[c.zone] = True
                probes.append(
                    {
                        "qindex": q,
                        "qid": query_ids[q],
                        "group": group,
                        "level": m,
                        "near": [int(i) for i in c.near],
                        "rank_m": c.rank_m,
                        "tau": c.tau,
                    }
                )
    if not probes:
        raise RuntimeError(f"seed {seed}: no probe could be placed")

    # Far chunks: SciDocs passages less similar to every probe than any probe's zone boundary, one
    # per secret passage, without replacement while they last. A secret's far chunk replaces it in
    # the W0 of every group whose near sets hold it.
    probe_vectors = queries[[p["qindex"] for p in probes]]
    boundary = min(p["tau"] for p in probes)
    closest = (far_vectors @ probe_vectors.T).max(axis=1)
    eligible = np.flatnonzero(closest < boundary)
    fallback = not len(eligible)
    if fallback:
        eligible = np.argsort(closest)[: max(1, len(closest) // 2)]
    eligible = eligible[rng.permutation(len(eligible))]
    secret_ids = np.flatnonzero(claimed)
    shuffled = secret_ids[rng.permutation(len(secret_ids))]
    far = [[int(d), int(eligible[i % len(eligible)]), int(tokens[d])] for i, d in enumerate(shuffled)]
    groups: list[dict[str, Any]] = []
    for group in range(GROUPS):
        members = [p for p in probes if p["group"] == group]
        own = sorted({int(i) for p in members for i in p["near"]})
        groups.append({"group": group, "probes": [p["qindex"] for p in members], "secrets": own})
    shared = int(sum(len(g["secrets"]) for g in groups) - len(secret_ids))

    buckets = rng.integers(0, 100, size=n)
    readable = ~claimed
    exact: dict[str, dict[str, Any]] = {}
    for probe in probes:
        similarity = corpus @ queries[probe["qindex"]]
        per: dict[str, Any] = {}
        for pct in PCTS:
            candidates = np.flatnonzero(readable & (buckets < pct))
            if not len(candidates):
                per[str(pct)] = {"R": 0, "top": [], "tstar": [], "sigma_k": None}
                continue
            scores = similarity[candidates]
            kk = min(K, len(candidates))
            top = np.argpartition(-scores, kk - 1)[:kk]
            top = top[np.argsort(-scores[top], kind="stable")]
            sigma = float(scores[top[-1]])
            tstar = candidates[scores >= sigma - 1e-4]
            per[str(pct)] = {
                "R": int(len(candidates)),
                "top": [int(i) for i in candidates[top]],
                "tstar": [int(i) for i in tstar],
                "sigma_k": sigma,
            }
        exact[str(probe["qindex"])] = per

    counts = {str(m): sum(1 for p in probes if p["level"] == m) for m in PER_GROUP}
    notes = {
        "probes": counts,
        "groups_full": sum(1 for g in groups if len(g["probes"]) == sum(PER_GROUP.values())),
        "shortfall": shortfall,
        "secret": int(len(secret_ids)),
        "secret_extra_group_memberships": shared,
        "far_eligible": int(len(eligible)),
        "far_reused": bool(len(eligible) < len(secret_ids)),
        "far_fallback": fallback,
        "boundary": boundary,
        "far_closest_max": float(closest[eligible].max()) if len(eligible) else None,
        "rank_m_max": {str(m): max((p["rank_m"] for p in probes if p["level"] == m), default=None) for m in PER_GROUP},
    }
    log(f"  seed {seed}: probes {counts}, {notes['groups_full']} full groups, {len(secret_ids):,} secrets")
    return {
        "seed": seed,
        "k": K,
        "pcts": list(PCTS),
        "per_group": {str(m): c for m, c in PER_GROUP.items()},
        "zone_extra": ZONE,
        "buckets": [int(b) for b in buckets],
        "secret": [int(i) for i in secret_ids],
        "probes": probes,
        "groups": groups,
        "far": far,  # [secret passage, first SciDocs passage, word tokens]
        "exact": exact,
        "notes": notes,
    }


# ---- main ----------------------------------------------------------------------------------------


def run(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cache = Path(args.cache) if args.cache else None
    log("== texts and embeddings")
    described = texts_and_embeddings(out, cache)
    corpus_items, corpus = read_texts(out, "fiqa_corpus")
    query_items, queries = read_texts(out, "fiqa_queries")
    _, far_vectors = read_texts(out, "scidocs_subset")

    log("== plans")
    clock = time.monotonic()
    near_index, near_similarity = neighbours(queries, corpus, DEPTH)
    hubs, hub_info = hub_mask(near_index, len(corpus))
    log(f"  hubs: {hub_info}")
    tokens = np.array([common.count_tokens(t) for _, t in corpus_items], dtype=np.int64)
    query_ids = [key for key, _ in query_items]
    summaries = {}
    for seed in range(args.seeds):
        plan = make_plan(seed, corpus, queries, query_ids, near_index, near_similarity, hubs, far_vectors, tokens)
        plan["hubs"] = hub_info
        common.plan_path(out, seed).write_text(json.dumps(plan), encoding="utf-8")
        summaries[str(seed)] = plan["notes"]
    plans_s = round(time.monotonic() - clock, 1)

    manifest = {
        "experiment": "x3x6-data",
        "mode": args.mode,
        "seeds": args.seeds,
        "design": {"groups": GROUPS, "per_group": {str(m): c for m, c in PER_GROUP.items()}, "zone": ZONE},
        "hubs": hub_info,
        **{key: described.get(key) for key in ("key", "embedding", "sources", "counts", "versions", "from_cache")},
        "tokens": {"fiqa_mean": float(tokens.mean()), "fiqa_median": float(np.median(tokens))},
        "plans": summaries,
        "timings": {**(described.get("timings") or {}), "plans_s": plans_s},
        "numpy": np.__version__,
        "host": common.host(),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    shown = {k: manifest[k] for k in ("counts", "sources", "timings", "hubs", "plans", "from_cache")}
    common.annotate("notice", f"x6 data ({args.mode})", json.dumps(shown, default=str))
    log("== done")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="x6data")
    parser.add_argument("--mode", choices=("full", "smoke"), default="full")
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--cache", default="", help="a folder that keeps the texts and embeddings between runs")
    args = parser.parse_args(argv)
    if args.mode == "smoke":
        args.seeds = min(args.seeds, 1)
    try:
        return run(args)
    except BaseException as error:
        common.fail_loudly("x6 data", error)
        raise


if __name__ == "__main__":
    sys.exit(main())
