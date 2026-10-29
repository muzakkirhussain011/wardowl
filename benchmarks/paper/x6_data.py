"""Experiments X3 and X6, the data job: FiQA and SciDocs, their embeddings, and X6's plans.

Downloads BEIR FiQA-2018 (corpus and queries) and BEIR SciDocs (corpus), embeds them on the CPU with
sentence-transformers/all-MiniLM-L6-v2, and computes, by exact search, the plan of every X6 seed:
the probes of each level m, their near sets and zones, the far chunks that replace the near sets in
W0, the permission buckets, and each probe's exact readable top 10 (see PREREG_X3_X6.md). Every store
job reads these files, so all stores play the identical game. X3 reads the FiQA embeddings as its
semantic subset.

    python x6_data.py --out x6data [--mode full|smoke] [--seeds 5]

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
UKP = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{name}.zip"
PCTS = (1, 10, 50)
SIZES: dict[str, dict[str, Any]] = {
    # None keeps every passage or query.
    "full": {
        "fiqa": None,
        "queries": None,
        "scidocs": 12_000,
        "levels": {1000: 8, 100: 16, 10: 24, 1: 24},
        "zone": 1000,
    },
    "smoke": {"fiqa": 6_000, "queries": 600, "scidocs": 1_500, "levels": {1000: 1, 100: 2, 10: 2, 1: 2}, "zone": 300},
}


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
    described = {"model": MODEL, "revision": revision, "max_seq_length": MAX_SEQ_LENGTH, "threads": torch.get_num_threads()}
    return model, described


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


def make_plan(
    seed: int,
    sizes: dict[str, Any],
    corpus: np.ndarray,
    queries: np.ndarray,
    query_ids: list[str],
    near_index: np.ndarray,
    near_similarity: np.ndarray,
    far_vectors: np.ndarray,
    tokens: np.ndarray,
) -> dict[str, Any]:
    levels: dict[int, int] = sizes["levels"]
    extra: int = sizes["zone"]
    n = len(corpus)
    rng = np.random.default_rng([SEED_BASE, seed])
    order = rng.permutation(len(queries))
    secret = np.zeros(n, dtype=bool)
    zone = np.zeros(n, dtype=bool)
    used: set[int] = set()
    probes: list[dict[str, Any]] = []
    shortfall: dict[str, int] = {}
    for m in sorted(levels, reverse=True):
        depth = m + extra
        if depth > near_index.shape[1]:
            raise RuntimeError(f"level {m} needs {depth} neighbours; {near_index.shape[1]} were computed")
        got = 0
        for position in order:
            if got >= levels[m]:
                break
            q = int(position)
            if q in used:
                continue
            near = near_index[q, :m]
            region = near_index[q, :depth]
            # No probe's near set inside another probe's zone, in either direction.
            if zone[near].any() or secret[region].any():
                continue
            secret[near] = True
            zone[region] = True
            used.add(q)
            got += 1
            probes.append(
                {
                    "qindex": q,
                    "qid": query_ids[q],
                    "level": m,
                    "near": [int(i) for i in near],
                    "tau": float(near_similarity[q, depth - 1]),
                }
            )
        if got < levels[m]:
            shortfall[str(m)] = got
            log(f"  seed {seed}: level {m}: only {got} of {levels[m]} probes could be placed")
    if not probes:
        raise RuntimeError(f"seed {seed}: no probe could be placed")
    secret_ids = np.flatnonzero(secret)

    # W0's far chunks: SciDocs passages less similar to every probe than any probe's zone boundary.
    probe_vectors = queries[[p["qindex"] for p in probes]]
    boundary = min(p["tau"] for p in probes)
    closest = (far_vectors @ probe_vectors.T).max(axis=1)
    eligible = np.flatnonzero(closest < boundary)
    fallback = False
    if not len(eligible):
        fallback = True
        eligible = np.argsort(closest)[: max(1, len(closest) // 2)]
    eligible = eligible[rng.permutation(len(eligible))]
    near_order = secret_ids[rng.permutation(len(secret_ids))]
    far = [
        [int(d), int(eligible[i % len(eligible)]), int(tokens[d])] for i, d in enumerate(near_order)
    ]  # [near passage, first SciDocs passage, word tokens]

    buckets = rng.integers(0, 100, size=n)
    readable = ~secret
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

    counts = {str(m): sum(1 for p in probes if p["level"] == m) for m in levels}
    notes = {
        "probes": counts,
        "shortfall": shortfall,
        "secret": int(len(secret_ids)),
        "far_eligible": int(len(eligible)),
        "far_reused": bool(len(eligible) < len(secret_ids)),
        "far_fallback": fallback,
        "boundary": boundary,
        "far_closest_max": float(closest[eligible].max()) if len(eligible) else None,
    }
    log(f"  seed {seed}: probes {counts}, {len(secret_ids):,} secrets, {len(eligible):,} eligible far passages")
    return {
        "seed": seed,
        "k": K,
        "pcts": list(PCTS),
        "levels": {str(m): c for m, c in levels.items()},
        "zone_extra": extra,
        "buckets": [int(b) for b in buckets],
        "secret": [int(i) for i in secret_ids],
        "probes": probes,
        "far": far,
        "exact": exact,
        "notes": notes,
    }


# ---- main ----------------------------------------------------------------------------------------


def run(args: argparse.Namespace) -> int:
    sizes = SIZES[args.mode]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    timings: dict[str, float] = {}
    clock = time.monotonic()

    log("== datasets")
    fiqa_rows, fiqa_queries, fiqa_source = fetch("fiqa", need_queries=True)
    scidocs_rows, _, scidocs_source = fetch("scidocs", need_queries=False)
    corpus_items = subset(passages(fiqa_rows, "fiqa"), sizes["fiqa"], "fiqa")
    query_items = subset(passages(fiqa_queries, "q"), sizes["queries"], "queries")
    far_items = subset([item for item in passages(scidocs_rows, "scid") if item[1]], sizes["scidocs"], "scidocs")
    del fiqa_rows, fiqa_queries, scidocs_rows
    timings["download_s"] = round(time.monotonic() - clock, 1)
    log(f"  {len(corpus_items):,} FiQA passages, {len(query_items):,} queries, {len(far_items):,} SciDocs passages")

    log("== embeddings")
    clock = time.monotonic()
    model, model_info = load_model()
    corpus = embed(model, [t for _, t in corpus_items], "FiQA passages")
    queries = embed(model, [t for _, t in query_items], "FiQA queries")
    far_vectors = embed(model, [t for _, t in far_items], "SciDocs passages")
    timings["embed_s"] = round(time.monotonic() - clock, 1)
    write_texts(out, "fiqa_corpus", corpus_items, corpus)
    write_texts(out, "fiqa_queries", query_items, queries)
    write_texts(out, "scidocs_subset", far_items, far_vectors)

    log("== plans")
    clock = time.monotonic()
    depth = max(sizes["levels"]) + sizes["zone"]
    near_index, near_similarity = neighbours(queries, corpus, depth)
    tokens = np.array([common.count_tokens(t) for _, t in corpus_items], dtype=np.int64)
    query_ids = [key for key, _ in query_items]
    summaries = {}
    for seed in range(args.seeds):
        plan = make_plan(seed, sizes, corpus, queries, query_ids, near_index, near_similarity, far_vectors, tokens)
        common.plan_path(out, seed).write_text(json.dumps(plan), encoding="utf-8")
        summaries[str(seed)] = plan["notes"]
    timings["plans_s"] = round(time.monotonic() - clock, 1)

    manifest = {
        "experiment": "x3x6-data",
        "mode": args.mode,
        "sizes": {**sizes, "levels": {str(m): c for m, c in sizes["levels"].items()}},
        "seeds": args.seeds,
        "embedding": model_info,
        "sources": {"fiqa": fiqa_source, "scidocs": scidocs_source},
        "counts": {
            "fiqa_corpus": len(corpus_items),
            "fiqa_queries": len(query_items),
            "scidocs_subset": len(far_items),
        },
        "tokens": {"fiqa_mean": float(tokens.mean()), "fiqa_median": float(np.median(tokens))},
        "plans": summaries,
        "timings": timings,
        "versions": common.versions(
            "sentence-transformers", "torch", "transformers", "huggingface-hub", "tokenizers", "numpy", "pyarrow"
        ),
        "host": common.host(),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    common.annotate(
        "notice",
        f"x6 data ({args.mode})",
        json.dumps({k: manifest[k] for k in ("counts", "sources", "timings", "plans", "embedding")}, default=str),
    )
    log("== done")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="x6data")
    parser.add_argument("--mode", choices=sorted(SIZES), default="full")
    parser.add_argument("--seeds", type=int, default=5)
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
