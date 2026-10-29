"""Data for experiments X2 and X5: embeddings, permission layouts, subjects, the exact baseline.

Two steps per corpus, each run as its own GitHub Actions job (PREREG_X2_X5.md, sections 1 to 3):

    python x2x5_prepare.py embed --corpus e --shard 0 --shards 6 --out shards/
    python x2x5_prepare.py prepare --corpus e --shards shards/ --out data-e/

`embed` builds the corpus (E: acceptance/kaggle/enterprise_rag.py's documents; M: the first million
non-empty BEIR MS MARCO passages) and embeds one contiguous range of it on the CPU, recording the
SHA-256 of its vectors and of the ids it embedded. `prepare` builds the corpus again, checks every
shard against it, merges them, embeds the queries, draws M's layouts and subjects, computes the
exact top 10 readable chunks of every (query, subject) pair with the measured axes, and writes a
folder that `x2x5_common.load_corpus` reads, with checksums.json over every file. `--smoke` makes
a corpus of a few thousand chunks with every code path.
"""

from __future__ import annotations

import argparse
import dataclasses
import gzip
import hashlib
import json
import os
import time
from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import x2x5_common as xc
from x2x5_common import log

E_MODEL = "BAAI/bge-base-en-v1.5"
M_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "  # both models' instruction
SIZES = {
    "full": {"e": {"variants": 208, "kb_limit": 0}, "m": {"docs": 1_000_000, "pool": 20_000, "divisions": 100,
             "seeds": 5, "subjects": 10, "queries": 4}},
    "smoke": {"e": {"variants": 4, "kb_limit": 2000}, "m": {"docs": 20_000, "pool": 2_000, "divisions": 10,
              "seeds": 2, "subjects": 2, "queries": 2}},
}  # fmt: skip
PROBE_GROUPS = ("hr", "finance", "board", "engineering", "sre", "legal", "contractors", "employees")
PROBE_TENANTS, PROBE_FIQA, PROBE_SEED = 3, 4, 61  # X1's probe set
SMOKE_PEOPLE = ("northwind-eu-judy", "contoso-judy", "fabrikam-judy", "dave", "carol", "frank", "mallory")
SMOKE_PROBE_GROUPS = ("board", "employees", "contractors", "hr")
NEIGHBOURS = 1000  # unfiltered neighbours kept per pool query, to pick P and N queries
P_RHO100 = 0.5  # P: at least half of the 100 nearest passages readable


def digest(items: Sequence[str]) -> str:
    h = hashlib.sha256()
    for item in items:
        h.update(item.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def shard_range(total: int, shard: int, shards: int) -> tuple[int, int]:
    return total * shard // shards, total * (shard + 1) // shards


def encoder(model_name: str) -> Any:
    import torch
    from sentence_transformers import SentenceTransformer

    torch.set_num_threads(os.cpu_count() or 4)
    return SentenceTransformer(model_name, device="cpu")


def encode(model: Any, texts: Sequence[str], batch: int, prefix: str = "") -> np.ndarray:
    """Unit-length float32 embeddings on the CPU, in blocks of 5,000 with a log line each."""
    parts = []
    started = time.perf_counter()
    for start in range(0, len(texts), 5000):
        block = [prefix + t for t in texts[start : start + 5000]]
        vectors = model.encode(
            block, batch_size=batch, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False
        )
        parts.append(np.asarray(vectors, dtype=np.float32))
        done = min(start + 5000, len(texts))
        log(f"  embedded {done:,} of {len(texts):,} ({time.perf_counter() - started:.0f} s)")
    if not parts:
        return np.zeros((0, model.get_sentence_embedding_dimension()), dtype=np.float32)
    vectors = np.vstack(parts)
    return (vectors / np.linalg.norm(vectors, axis=1, keepdims=True)).astype(np.float32)


def versions() -> dict[str, Any]:
    return xc.environment(["torch", "sentence-transformers", "transformers", "datasets", "faiss-cpu"])


# ---- E: the enterprise scenario ------------------------------------------------------------------------


def enterprise_run(work: Path, smoke: bool) -> tuple[Any, Any, int]:
    """The scenario's corpus, people and questions, plus X1's probe set; the number of original questions."""
    er = xc.scenario()
    cfg = er.Config(work=str(work), repo=str(xc.REPO), stores=(), remote_authorizers=())
    size = SIZES["smoke" if smoke else "full"]["e"]
    cfg.variants, cfg.kb_limit = size["variants"], size["kb_limit"]
    run = er.Run(cfg)
    run.build_corpus()
    failed = [(name, detail) for name, ok, detail in run.report.checks if not ok]
    if failed:
        raise RuntimeError(f"the scenario's own checks failed: {failed}")
    original = add_probes(er, run)
    if smoke:
        keep = set(SMOKE_PEOPLE)
        first: dict[str, str] = {}
        for p in run.people:
            if "-probe-" in p.id and p.groups[0] in SMOKE_PROBE_GROUPS:
                first.setdefault(p.groups[0], p.id)
        keep |= set(first.values())
        flags = [i < original for i in range(len(run.pairs))]
        kept = [(pair, flag) for pair, flag in zip(run.pairs, flags, strict=True) if pair.persona.id in keep]
        run.pairs = [pair for pair, _ in kept]
        original = sum(flag for _, flag in kept)  # the original questions still come first
        run.people = [p for p in run.people if p.id in keep]
    return er, run, original


def fiqa_queries() -> list[str]:
    from datasets import load_dataset

    data = load_dataset("BeIR/fiqa", "queries", split="queries")
    return sorted({t.strip() for t in data["text"] if t and t.strip()})


def add_probes(er: Any, run: Any) -> int:
    """X1's probe set (section 6.1 of the investigation), appended after the original questions."""
    original = len(run.pairs)
    rng = np.random.default_rng(PROBE_SEED)
    generated = [t for t in er.TENANT_IDS if t not in er.enterprise.TENANTS]
    by_kind: dict[tuple[str, str], list[Any]] = defaultdict(list)
    for d in run.docs:
        if d.kind in er.KINDS:
            by_kind[(d.tenants[0], d.kind)].append(d)
    queries = fiqa_queries()
    people, pairs = [], []
    for g, group in enumerate(PROBE_GROUPS):
        for j in range(PROBE_TENANTS):
            tenant = generated[(PROBE_TENANTS * g + j) % len(generated)]
            persona = er.Persona(f"{tenant}-probe-{group}", tenant, (group,), f"probe: only {group}")
            people.append(persona)
            for kind in sorted(er.KINDS):
                docs = by_kind[(tenant, kind)]
                d = docs[int(rng.integers(len(docs)))]
                pairs.append(
                    er.Pair(persona, d.question or "", "probe-template", d.id, d.fact, (kind,), er.readable(persona, d))
                )
            reads_kb = bool(set(persona.groups) & set(er.KB_READERS))
            for index in rng.choice(len(queries), size=PROBE_FIQA, replace=False):
                pairs.append(er.Pair(persona, queries[int(index)], "probe-fiqa", None, None, ("kb",), reads_kb))
    run.people += people
    run.pairs += pairs
    log(f"probe set: {len(people)} people, {len(pairs)} questions")
    return original


def scratch(name: str) -> Path:
    """A working folder outside every uploaded folder (enterprise_rag.Run writes its cache there)."""
    return Path(os.environ.get("RUNNER_TEMP", "/tmp")) / f"x2x5-{name}"


def embed_e(args: argparse.Namespace) -> None:
    _, run, _ = enterprise_run(scratch("work-e"), args.smoke)
    ids = [d.id for d in run.docs]
    start, end = shard_range(len(ids), args.shard, args.shards)
    log(f"E shard {args.shard} of {args.shards}: chunks {start:,} to {end:,} of {len(ids):,}")
    model = encoder(E_MODEL)
    vectors = encode(model, [d.text for d in run.docs[start:end]], batch=16)
    save_shard(args, "e", vectors, ids, start, end, E_MODEL)


def save_shard(
    args: argparse.Namespace, corpus: str, vectors: np.ndarray, ids: Sequence[str], start: int, end: int, model: str
) -> None:
    path = args.out / f"{corpus}-{args.shard:02d}.npy"
    np.save(path, vectors)
    meta = {
        "corpus": corpus,
        "shard": args.shard,
        "shards": args.shards,
        "start": start,
        "end": end,
        "rows": int(vectors.shape[0]),
        "dim": int(vectors.shape[1]),
        "model": model,
        "ids_sha256": digest(ids[start:end]),
        "all_ids_sha256": digest(ids),
        "sha256": xc.sha256_file(path),
        "environment": versions(),
    }
    xc.write_json(args.out / f"{corpus}-{args.shard:02d}.json", meta)
    log(f"wrote {path} ({meta['rows']:,} x {meta['dim']}), SHA-256 {meta['sha256']}")


def merge_shards(folder: Path, corpus: str, ids: Sequence[str]) -> tuple[np.ndarray, list[dict[str, Any]]]:
    """The shards of `corpus`, checked against the ids this step built, in order."""
    metas = sorted((xc.read_json(p) for p in folder.glob(f"{corpus}-*.json")), key=lambda m: m["shard"])
    if not metas:
        raise FileNotFoundError(f"no {corpus} shards in {folder}")
    shards = metas[0]["shards"]
    if [m["shard"] for m in metas] != list(range(shards)):
        raise RuntimeError(f"{corpus}: shards {[m['shard'] for m in metas]} of {shards}")
    parts = []
    for m in metas:
        path = folder / f"{corpus}-{m['shard']:02d}.npy"
        if xc.sha256_file(path) != m["sha256"]:
            raise RuntimeError(f"{path} does not match the SHA-256 its job recorded")
        if m["all_ids_sha256"] != digest(ids) or m["ids_sha256"] != digest(ids[m["start"] : m["end"]]):
            raise RuntimeError(f"{path} embedded other chunks than this corpus holds")
        part = np.load(path)
        if part.shape[0] != m["end"] - m["start"]:
            raise RuntimeError(f"{path} holds {part.shape[0]} rows, not {m['end'] - m['start']}")
        parts.append(part)
    vectors = np.ascontiguousarray(np.vstack(parts), dtype=np.float32)
    if vectors.shape[0] != len(ids):
        raise RuntimeError(f"{corpus}: {vectors.shape[0]} vectors for {len(ids)} chunks")
    norms = np.linalg.norm(vectors, axis=1)
    if not np.allclose(norms, 1.0, atol=1e-3):
        raise RuntimeError(f"{corpus}: vectors are not unit length (norms {norms.min():.4f} to {norms.max():.4f})")
    return vectors, metas


def masks_of(er: Any, docs: Sequence[Any], people: Sequence[Any]) -> dict[str, np.ndarray]:
    """What each person may read, by the scenario's oracle (as enterprise_rag.Run._masks)."""
    groups: dict[tuple[Any, Any], int] = {}
    examples: list[Any] = []
    of_row = np.empty(len(docs), dtype=np.int32)
    for row, d in enumerate(docs):
        key = (d.tenants, d.readers)
        if key not in groups:
            groups[key] = len(examples)
            examples.append(d)
        of_row[row] = groups[key]
    return {p.id: np.array([er.readable(p, d) for d in examples], dtype=bool)[of_row] for p in people}


def prepare_e(args: argparse.Namespace) -> None:
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    er, run, original = enterprise_run(scratch("work-e"), args.smoke)
    ids = [d.id for d in run.docs]
    vectors, metas = merge_shards(args.shards, "e", ids)
    log(f"E: {len(ids):,} chunks, {len(run.people)} people, {len(run.pairs):,} questions ({original} original)")
    model = encoder(E_MODEL)
    unique = sorted({p.question for p in run.pairs})
    index = {q: j for j, q in enumerate(unique)}
    qunique = encode(model, unique, batch=32, prefix=QUERY_PREFIX)
    qvecs = np.ascontiguousarray(qunique[[index[p.question] for p in run.pairs]], dtype=np.float32)
    masks = masks_of(er, run.docs, run.people)
    persons = sorted({p.persona.id for p in run.pairs})
    rank = {person: r for r, person in enumerate(np.random.default_rng(xc.SEED).permutation(persons).tolist())}
    position: dict[str, int] = defaultdict(int)
    rows = []
    by_person: dict[str, list[int]] = defaultdict(list)
    for i, pair in enumerate(run.pairs):
        by_person[pair.persona.id].append(i)
    truth: dict[int, dict[str, Any]] = {}
    started = time.perf_counter()
    for person, idx in by_person.items():
        sims = qvecs[idx] @ vectors.T
        for j, i in enumerate(idx):
            truth[i] = xc.pair_truth(sims[j], masks[person])
    log(f"E: exact baseline and axes of {len(truth):,} pairs in {time.perf_counter() - started:.0f} s")
    keys = []
    for i, pair in enumerate(run.pairs):
        person = pair.persona.id
        keys.append((position[person], rank[person], i))
        position[person] += 1
    order = {i: o for o, (_, _, i) in enumerate(sorted(keys))}
    regions = {"probe-fiqa": "kb", "redteam": "redteam"}
    for i, pair in enumerate(run.pairs):
        persona = pair.persona
        rows.append(
            {
                "pid": i,
                "sid": persona.id,
                "q": i,
                "order": order[i],
                **truth[i],
                "person_type": xc.persona_type(persona),
                "tenant": persona.tenant,
                "category": pair.category,
                "region": regions.get(pair.category, "company"),
                "original": int(i < original),
                "answerable": int(bool(pair.answerable)),
                "target": pair.target or "",
                "attack": pair.attack,
                "question": pair.question,
            }
        )
    extra = ["person_type", "tenant", "category", "region", "original", "answerable", "target", "attack", "question"]
    xc.write_pairs(out / "pairs.csv", rows, extra)
    np.save(out / "vectors.npy", vectors)
    np.save(out / "query_vectors.npy", qvecs)
    with gzip.open(out / "docs.jsonl.gz", "wt", encoding="utf-8") as handle:
        for d in run.docs:
            handle.write(json.dumps({f.name: getattr(d, f.name) for f in dataclasses.fields(d)}) + "\n")
    people = sorted({p.persona.id: p.persona for p in run.pairs}.values(), key=lambda p: p.id)
    records = [
        {"id": p.id, "tenant": p.tenant, "groups": list(p.groups), "role": p.role, "type": xc.persona_type(p)}
        for p in people
    ]
    xc.write_json(out / "people.json", records)
    readable = sorted(int(m.sum()) for m in masks.values())
    xc.write_json(
        out / "config.json",
        {
            "corpus": "e",
            "smoke": args.smoke,
            "model": E_MODEL,
            "query_prefix": QUERY_PREFIX,
            "chunks": len(ids),
            "dim": int(vectors.shape[1]),
            "people": len(people),
            "pairs": len(rows),
            "original_questions": original,
            "readable_min_median_max": [readable[0], readable[len(readable) // 2], readable[-1]],
            "vectors_sha256": xc.sha256_file(out / "vectors.npy"),
            "shards": [{k: m[k] for k in ("shard", "start", "end", "sha256")} for m in metas],
            "embedding_environment": metas[0]["environment"],
            "environment": versions(),
        },
    )
    sums = xc.write_checksums(out)
    log(f"E data written to {out}: {sums}")


# ---- M: MS MARCO with synthetic layouts --------------------------------------------------------------


def msmarco_passages(n: int) -> tuple[list[str], list[str]]:
    """The first n non-empty BEIR MS MARCO passages, title and text joined (benchmarks/load_bench.py)."""
    from datasets import load_dataset

    ids, texts = [], []
    for row in load_dataset("BeIR/msmarco", "corpus", split="corpus", streaming=True):
        text = f"{row['title']}\n{row['text']}".strip()
        if text:
            ids.append(str(row["_id"]))
            texts.append(text)
            if len(ids) % 200_000 == 0:
                log(f"  read {len(ids):,} passages")
            if len(ids) >= n:
                break
    if len(ids) < n:
        raise RuntimeError(f"BEIR MS MARCO gave {len(ids)} passages, not {n}")
    return ids, texts


def embed_m(args: argparse.Namespace) -> None:
    size = SIZES["smoke" if args.smoke else "full"]["m"]
    ids, texts = msmarco_passages(size["docs"])
    start, end = shard_range(len(ids), args.shard, args.shards)
    log(f"M shard {args.shard} of {args.shards}: passages {start:,} to {end:,} of {len(ids):,}")
    model = encoder(M_MODEL)
    vectors = encode(model, texts[start:end], batch=64)
    save_shard(args, "m", vectors, ids, start, end, M_MODEL)


def kmeans_labels(x: np.ndarray, k: int, seed: int) -> np.ndarray:
    """Spherical k-means (faiss, 20 iterations); fewer points than clusters get one cluster each."""
    if len(x) <= k:
        return np.arange(len(x)) % k
    import faiss

    km = faiss.Kmeans(x.shape[1], k, niter=20, seed=int(seed), spherical=True, verbose=False, min_points_per_centroid=1)
    data = np.ascontiguousarray(x, dtype=np.float32)
    km.train(data)
    _, labels = km.index.search(data, 1)
    return labels.ravel().astype(np.int64)


def uniform_layout(n: int, divisions: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """U: a random permutation cut into equal teams; ten teams a department, a hundred a division."""
    rng = np.random.default_rng([xc.SEED, 7, seed])
    teams = divisions * 100
    team = np.empty(n, dtype=np.int64)
    team[rng.permutation(n)] = (np.arange(n, dtype=np.int64) * teams) // n
    return team // 100, team // 10, team


def clustered_layout(vectors: np.ndarray, divisions: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """C: hierarchical k-means: divisions over everything, ten departments in each, ten teams in each."""
    started = time.perf_counter()
    div = kmeans_labels(vectors, divisions, 1 + seed)
    dept = np.empty_like(div)
    team = np.empty_like(div)
    for d in range(divisions):
        rows = np.flatnonzero(div == d)
        dept[rows] = d * 10 + kmeans_labels(vectors[rows], 10, 1000 + 1009 * seed + d)
    for e in range(divisions * 10):
        rows = np.flatnonzero(dept == e)
        if len(rows):
            team[rows] = e * 10 + kmeans_labels(vectors[rows], 10, 200_000 + 100_003 * seed + e)
    log(f"  clustered layout {seed}: {time.perf_counter() - started:.0f} s")
    return div, dept, team


def draw_grant(
    rng: np.random.Generator, sizes: tuple[np.ndarray, np.ndarray, np.ndarray], target: float
) -> tuple[set[int], set[int], set[int], int]:
    """PREREG section 2: divisions while at most 60% of the target, departments while at most 90%,
    then teams until at least 95% (a team may overshoot by at most the rest of the target, unless no
    team that small is left, when the smallest teams are taken)."""
    s_div, s_dept, s_team = sizes
    divs: set[int] = set()
    depts: set[int] = set()
    teams: set[int] = set()
    total = 0
    for d in rng.permutation(len(s_div)).tolist():
        if s_div[d] and total + s_div[d] <= 0.6 * target:
            divs.add(d)
            total += int(s_div[d])
    for e in rng.permutation(len(s_dept)).tolist():
        if e // 10 not in divs and s_dept[e] and total + s_dept[e] <= 0.9 * target:
            depts.add(e)
            total += int(s_dept[e])
    need = 0.95 * target

    def free(t: int) -> bool:
        return t // 100 not in divs and t // 10 not in depts and t not in teams and s_team[t] > 0

    for t in rng.permutation(len(s_team)).tolist():
        if total >= need:
            break
        if free(t) and s_team[t] <= 2 * (target - total):
            teams.add(t)
            total += int(s_team[t])
    if total < need:
        for t in np.argsort(s_team, kind="stable").tolist():
            if total >= need:
                break
            if free(t):
                teams.add(t)
                total += int(s_team[t])
    return divs, depts, teams, total


def size_stats(sizes: np.ndarray) -> dict[str, Any]:
    return {
        "min": int(sizes.min()),
        "median": float(np.median(sizes)),
        "max": int(sizes.max()),
        "empty": int((sizes == 0).sum()),
    }


def grant_mask(arrays: tuple[np.ndarray, np.ndarray, np.ndarray], tenant: np.ndarray, grant: xc.Grant) -> np.ndarray:
    div, dept, team = arrays
    mask = np.isin(team, list(grant.teams)) | np.isin(dept, list(grant.depts)) | np.isin(div, list(grant.divs))
    if grant.tenant is not None:
        mask &= tenant == "ab".index(grant.tenant)
    return mask


def pool_neighbours(qpool: np.ndarray, vectors: np.ndarray, depth: int) -> np.ndarray:
    """The `depth` nearest passages of every pool query, nearest first (int32)."""
    out = np.empty((len(qpool), depth), dtype=np.int32)
    started = time.perf_counter()
    for start in range(0, len(qpool), 64):
        sims = qpool[start : start + 64] @ vectors.T
        top = np.argpartition(-sims, depth - 1, axis=1)[:, :depth]
        ranked = np.take_along_axis(sims, top, axis=1)
        order = np.argsort(-ranked, axis=1, kind="stable")
        out[start : start + 64] = np.take_along_axis(top, order, axis=1)
        if (start // 64) % 50 == 0:
            log(f"  neighbours of {min(start + 64, len(qpool)):,} pool queries ({time.perf_counter() - started:.0f} s)")
    return out


def pick_queries(
    rng: np.random.Generator, regime: str, hits: np.ndarray | None, pool: int, count: int
) -> tuple[list[int], bool, list[float]]:
    """PREREG section 2: U at random; P with rho_100 >= 0.5; N with no readable passage among the
    1,000 nearest. Returns the queries, whether the criterion had to fall back, and their rho values."""
    if regime == "U" or hits is None:
        return rng.choice(pool, size=count, replace=False).tolist(), False, []
    rho100 = hits[:, :100].mean(axis=1)
    rho1000 = hits.mean(axis=1)
    if regime == "P":
        candidates = np.flatnonzero(rho100 >= P_RHO100)
        if len(candidates) >= count:
            chosen = rng.choice(candidates, size=count, replace=False)
            return chosen.tolist(), False, rho100[chosen].tolist()
        chosen = np.argsort(-rho100, kind="stable")[:count]
        return chosen.tolist(), True, rho100[chosen].tolist()
    candidates = np.flatnonzero(rho1000 == 0)
    if len(candidates) >= count:
        chosen = rng.choice(candidates, size=count, replace=False)
        return chosen.tolist(), False, rho1000[chosen].tolist()
    first = np.where(hits.any(axis=1), hits.argmax(axis=1), hits.shape[1])
    chosen = np.lexsort((-first, rho1000))[:count]
    return chosen.tolist(), True, rho1000[chosen].tolist()


def prepare_m(args: argparse.Namespace) -> None:
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    size = SIZES["smoke" if args.smoke else "full"]["m"]
    n_docs, n_pool, divisions = size["docs"], size["pool"], size["divisions"]
    seeds, per_cell, per_subject = size["seeds"], size["subjects"], size["queries"]
    ids, texts = msmarco_passages(n_docs)
    vectors, metas = merge_shards(args.shards, "m", ids)
    n = len(ids)
    log(f"M: {n:,} passages, {vectors.shape[1]} dimensions")

    from datasets import load_dataset

    questions = load_dataset("BeIR/msmarco", "queries", split="queries")
    unique = list(dict.fromkeys(q.strip() for q in questions["text"] if q and q.strip()))
    picked = np.random.default_rng(xc.SEED).choice(len(unique), size=n_pool, replace=False)
    pool_texts = [unique[int(i)] for i in picked]
    qpool = encode(encoder(M_MODEL), pool_texts, batch=64, prefix=QUERY_PREFIX)
    neighbours = pool_neighbours(qpool, vectors, min(xc.LOCAL_MS[-1], n))

    tenant = (np.random.default_rng([xc.SEED, 1]).random(n) < 0.5).astype(np.uint8)  # 0 = a, 1 = b
    arrays: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for seed in range(seeds):
        arrays[f"u{seed}"] = uniform_layout(n, divisions, seed)
        arrays[f"c{seed}"] = clustered_layout(vectors, divisions, seed)

    grants: list[xc.Grant] = []
    rows: list[dict[str, Any]] = []
    sizes_report: dict[str, Any] = {}
    started = time.perf_counter()
    for family in xc.FAMILIES:
        for seed in range(seeds):
            key = f"{family}{seed}"
            div, dept, team = arrays[key]
            sizes = (
                np.bincount(div, minlength=divisions),
                np.bincount(dept, minlength=divisions * 10),
                np.bincount(team, minlength=divisions * 100),
            )
            sizes_report[key] = {
                name: size_stats(s) for name, s in zip(("division", "department", "team"), sizes, strict=True)
            }
            for li, level in enumerate(xc.LEVELS):
                for si, shape in enumerate(xc.SHAPES):
                    if level == 1.0 and (shape == "tenant" or family == "c"):
                        continue
                    for j in range(per_cell):
                        rng = np.random.default_rng([xc.SEED, xc.FAMILIES.index(family), seed, li, si, j])
                        target = level * n * (2 if shape == "tenant" else 1)
                        if level == 1.0:
                            divs, depts, teams = set(range(divisions)), set(), set()
                        else:
                            divs, depts, teams, _ = draw_grant(rng, sizes, target)
                        grant = xc.Grant(
                            sid=f"{key}-{shape[0]}{li}-{j}",
                            family=family,
                            seed=seed,
                            level=li,
                            shape=shape,
                            tenant="a" if shape == "tenant" else None,
                            divs=frozenset(divs),
                            depts=frozenset(depts),
                            teams=frozenset(teams),
                        )
                        mask = grant_mask(arrays[key], tenant, grant)
                        grant.R = int(mask.sum())
                        grant.extra = {"sigma": grant.R / n, "nominal": level, "groups": len(grant.tags())}
                        grants.append(grant)
                        hits = mask[neighbours] if family == "c" else None
                        regimes = ("U",) if family == "u" else ("P", "N")
                        chosen: list[tuple[str, int, int, bool, float | None]] = []
                        for regime in regimes:
                            qs, fell, values = pick_queries(rng, regime, hits, n_pool, per_subject)
                            for qi, q in enumerate(qs):
                                chosen.append((regime, qi, q, fell, values[qi] if values else None))
                        sims = qpool[[c[2] for c in chosen]] @ vectors.T
                        for c, (regime, qi, q, fell, value) in enumerate(chosen):
                            rows.append(
                                {
                                    "sid": grant.sid,
                                    "q": q,
                                    **xc.pair_truth(sims[c], mask),
                                    "family": family,
                                    "seed": seed,
                                    "level": li,
                                    "nominal": level,
                                    "shape": shape,
                                    "regime": regime,
                                    "select_fallback": int(fell),
                                    "select_value": value,
                                    "stratum": f"{family}{seed}-{shape}-{li}-{regime}",
                                    "j": j,
                                    "qi": qi,
                                }
                            )
            seconds = time.perf_counter() - started
            log(f"  layout {key}: {len(grants)} subjects so far, {len(rows):,} pairs ({seconds:.0f} s)")
    strata = sorted({r["stratum"] for r in rows})
    stratum_rank = {s: i for i, s in enumerate(strata)}
    ranked = sorted(range(len(rows)), key=lambda i: (rows[i]["j"], rows[i]["qi"], stratum_rank[rows[i]["stratum"]]))
    for order, i in enumerate(ranked):
        rows[i]["order"] = order
    for pid, row in enumerate(rows):
        row["pid"] = pid
    extra = ["family", "seed", "level", "nominal", "shape", "regime", "select_fallback", "select_value", "stratum"]
    xc.write_pairs(out / "pairs.csv", rows, [*extra, "j", "qi"])
    np.save(out / "vectors.npy", vectors)
    np.save(out / "query_vectors.npy", qpool)
    xc.write_json(out / "queries.json", pool_texts)
    layout: dict[str, np.ndarray] = {"tenant": tenant}
    for key, (div, dept, team) in arrays.items():
        layout[f"{key}_div"], layout[f"{key}_dept"], layout[f"{key}_team"] = (
            div.astype(np.int16),
            dept.astype(np.int16),
            team.astype(np.int16),
        )
    np.savez(out / "layout.npz", **layout)
    xc.write_json(out / "subjects.json", [g.record() for g in grants])
    with gzip.open(out / "passages.jsonl.gz", "wt", encoding="utf-8") as handle:
        for doc_id, text in zip(ids, texts, strict=True):
            handle.write(json.dumps([doc_id, text]) + "\n")
    fallbacks = sum(r["select_fallback"] for r in rows)
    xc.write_json(
        out / "config.json",
        {
            "corpus": "m",
            "smoke": args.smoke,
            "model": M_MODEL,
            "query_prefix": QUERY_PREFIX,
            "chunks": n,
            "dim": int(vectors.shape[1]),
            "pool": n_pool,
            "divisions": divisions,
            "seeds": seeds,
            "subjects_per_cell": per_cell,
            "queries_per_subject": per_subject,
            "subjects": len(grants),
            "pairs": len(rows),
            "query_selection_fallbacks": fallbacks,
            "group_sizes": sizes_report,
            "tenant_a_share": float((tenant == 0).mean()),
            "vectors_sha256": xc.sha256_file(out / "vectors.npy"),
            "shards": [{k: m[k] for k in ("shard", "start", "end", "sha256")} for m in metas],
            "embedding_environment": metas[0]["environment"],
            "environment": versions(),
        },
    )
    sums = xc.write_checksums(out)
    log(f"M data written to {out}: {len(rows):,} pairs, {len(grants)} subjects, {fallbacks} selection fallbacks")
    log(f"checksums: {sums}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data for experiments X2 and X5")
    parser.add_argument("step", choices=("embed", "prepare"))
    parser.add_argument("--corpus", choices=("e", "m"), required=True)
    parser.add_argument("--shard", type=int, default=0)
    parser.add_argument("--shards", default=None, help="embed: the number of shards; prepare: their folder")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args(argv)
    if args.step == "embed":
        args.shards = int(args.shards or 1)
        if not 0 <= args.shard < args.shards:
            parser.error("--shard must be between 0 and --shards - 1")
    else:
        if not args.shards:
            parser.error("prepare needs --shards, the folder holding the embed step's output")
        args.shards = Path(args.shards)
    args.out.mkdir(parents=True, exist_ok=True)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started = time.perf_counter()
    log(f"x2x5_prepare {args.step} {args.corpus}: {versions()}")
    {("embed", "e"): embed_e, ("embed", "m"): embed_m, ("prepare", "e"): prepare_e, ("prepare", "m"): prepare_m}[
        (args.step, args.corpus)
    ](args)
    log(f"done in {time.perf_counter() - started:.0f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
