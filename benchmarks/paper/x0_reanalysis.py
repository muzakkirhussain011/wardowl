"""Experiment X0: the outputs of the Kaggle run of 2026-10-24, re-analysed offline.

Section 6.0 of the investigation (filtered-recall-gaps.md), items 1 to 3, from the run's own
answers.jsonl and results.json, with no store and no GPU:

1. Empty results: every k=5 retrieval that returned nothing while FAISS, which is exact, returned
   something for the same person and question. pgvector's are the ones in question; every store's
   are listed.
2. Approximate recall@5 per store, by question category and by person type: the overlap of the
   store's top 5 with FAISS's top 5 for the same person and question. Ties are not credited, unlike
   the run's own recall, so these numbers can sit slightly below the run's.
3. The share of knowledge-base passages (kb/, BEIR FiQA) in each store's top 5 against FAISS's, for
   targeted questions, which ask about one of the person's own company documents.

answers.jsonl holds one line per store and question: the person, tenant, category, red-team attack,
question, target document and the ids of the k=5 hits, in the order of the run's questions. A
store's lines are matched to FAISS's by that order, checked against the person and question, and
matched by the question itself if the order does not line up.

    python x0_reanalysis.py [--input DIR] [--out /kaggle/working/x0]

On Kaggle, add the original notebook's output as input; its folder is found under /kaggle/input.
Writes CSV tables, summary.md, x0.log and manifest.json to the output folder. CPU only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import paper_common as pc
from paper_common import log

KEY = ["person", "category", "attack", "question", "target"]
REFERENCE = "faiss"
CATEGORIES = ("generic", "targeted", "forbidden", "redteam")
PER_EMPTY_QUESTION = 15  # hits a question yields when nothing is short: k=5 plus k=10


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as data:
        for block in iter(lambda: data.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_answers(path: Path) -> pd.DataFrame:
    """answers.jsonl as a table, with each line's position among its store's lines."""
    records = []
    with path.open(encoding="utf-8") as lines:
        for number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{number} is not valid JSON: {error}") from error
    frame = pd.DataFrame.from_records(records)
    missing = {"store", "person", "tenant", "category", "question", "hits"} - set(frame.columns)
    if missing:
        raise ValueError(f"{path} lacks the fields {sorted(missing)}")
    for column in ("attack", "target"):
        if column not in frame:
            frame[column] = ""
        frame[column] = frame[column].fillna("").astype(str)
    frame["hits"] = frame["hits"].apply(lambda hits: list(hits) if isinstance(hits, list) else [])
    frame["position"] = frame.groupby("store", sort=False).cumcount()
    counts = frame.groupby("store", sort=False).size().to_dict()
    log(f"{len(frame):,} lines from {path}: {counts}")
    if len(set(counts.values())) > 1:
        log.loud(f"the stores have different numbers of lines: {counts}")
    return frame


def with_reference(frame: pd.DataFrame) -> pd.DataFrame:
    """Each line with FAISS's hits for the same person and question, in the column `reference`."""
    reference = frame[frame["store"] == REFERENCE]
    if reference.empty:
        raise ValueError(f"answers.jsonl has no {REFERENCE} lines: the exact reference is missing")
    renamed = {"hits": "reference", **{c: f"ref_{c}" for c in KEY}}
    by_position = frame.merge(
        reference[["position", *KEY, "hits"]].rename(columns=renamed), on="position", how="left"
    )
    aligned = np.logical_and.reduce([(by_position[c] == by_position[f"ref_{c}"]).to_numpy() for c in KEY])
    if aligned.all():
        log("every store's lines line up with FAISS's by position, person and question")
        return by_position.drop(columns=[f"ref_{c}" for c in KEY])
    log.loud(f"{int((~aligned).sum())} lines do not line up with FAISS's by position; matching by question instead")
    frame = frame.assign(occurrence=frame.groupby(["store", *KEY], sort=False).cumcount())
    reference = frame[frame["store"] == REFERENCE][[*KEY, "occurrence", "hits"]].rename(columns={"hits": "reference"})
    merged = frame.merge(reference, on=[*KEY, "occurrence"], how="left")
    unmatched = int(merged["reference"].isna().sum())
    if unmatched:
        log.loud(f"{unmatched} lines have no FAISS line for the same person and question; they are left out")
        merged = merged[merged["reference"].notna()]
    return merged.drop(columns=["occurrence"])


def _overlap(hits: Sequence[str], reference: Sequence[str]) -> float:
    return len(set(hits) & set(reference)) / len(reference) if reference else np.nan


def _kb_share(hits: Sequence[str]) -> float:
    return sum(h.startswith(pc.KB_PREFIX) for h in hits) / len(hits) if hits else np.nan


def scored(frame: pd.DataFrame, people: Sequence[Any]) -> pd.DataFrame:
    """Overlap with FAISS's top 5, knowledge-base shares, emptiness and person type, per line."""
    out = frame.copy()
    out["n_hits"] = out["hits"].apply(len)
    out["n_reference"] = out["reference"].apply(len)
    out["overlap5"] = [_overlap(h, r) for h, r in zip(out["hits"], out["reference"], strict=True)]
    out["kb_share5"] = out["hits"].apply(_kb_share)
    out["reference_kb_share5"] = out["reference"].apply(_kb_share)
    out["empty"] = (out["n_hits"] == 0) & (out["n_reference"] > 0)
    types = {p.id: pc.persona_type(p) for p in people}
    unknown = sorted(set(out["person"]) - set(types))
    if unknown:
        log.loud(f"{len(unknown)} people of answers.jsonl are not in the scenario's people(): {unknown[:10]}")
    out["persona_type"] = out["person"].map(types).fillna("unknown")
    return out


def mean_table(frame: pd.DataFrame, by: Sequence[str], value: str) -> pd.DataFrame:
    """Mean of `value` and the number of lines it averages (NaN left out), by the columns `by`."""
    table = frame.groupby(list(by), sort=False)[value].agg(["mean", "count"]).reset_index()
    return table.rename(columns={"mean": value, "count": "n"})


def results_summary(path: Path) -> tuple[list[str], dict[str, Any]]:
    """The run's own per-store numbers from results.json, and the hit shortfall that implies empties."""
    if not path.is_file():
        log.loud(f"{path} is missing: the summary leaves out the run's own per-store numbers")
        return ["results.json was not found next to answers.jsonl.", ""], {}
    data = json.loads(path.read_text(encoding="utf-8"))
    stores = data.get("stores", [])
    expected = max((s.get("hits_checked") or 0 for s in stores), default=0)
    rows = []
    for s in stores:
        short = expected - (s.get("hits_checked") or 0)
        rows.append(
            [
                s.get("label"),
                s.get("recall@5"),
                s.get("recall@10"),
                s.get("hits_checked"),
                short,
                round(short / PER_EMPTY_QUESTION, 1),
                s.get("incomplete"),
                (s.get("retrieval_ms") or {}).get("p50"),
            ]
        )
    lines = [
        f"{data.get('passed')} checks passed; failed: "
        + ("; ".join(f"{f.get('check')} ({f.get('detail')})" for f in data.get("failed", [])) or "none"),
        "",
        *pc.markdown_table(
            [
                "Store",
                "Recall@5",
                "Recall@10",
                "Hits checked",
                "Hits short of the most",
                "Short / 15",
                "Incomplete",
                "p50 ms",
            ],
            rows,
        ),
    ]
    facts = {"hits_expected": expected, "stores": {s.get("label"): s.get("hits_checked") for s in stores}}
    return lines, facts


def pivot(
    table: pd.DataFrame, columns: str, value: str, stores: Sequence[str], order: Sequence[str] = ()
) -> pd.DataFrame:
    """One row per store, one column per value of `columns` (those in `order` first)."""
    wide = table.pivot(index="store", columns=columns, values=value).reindex(stores)
    first = [c for c in order if c in wide.columns]
    wide = wide[[*first, *(c for c in wide.columns if c not in first)]]
    return wide.reset_index()


def predictions(frame: pd.DataFrame) -> list[str]:
    """Section 6.0's predictions next to what the data show, without a verdict (X0 is exploratory)."""

    def mean(mask: pd.Series, column: str = "overlap5") -> float:
        values = frame.loc[mask, column].dropna()
        return float(values.mean()) if len(values) else float("nan")

    store, kind, category = frame["store"], frame["persona_type"], frame["category"]
    empties = frame[frame["empty"] & (store == "pgvector")]
    company = category.isin(["targeted", "generic"])
    rows = [
        [
            "pgvector empty results",
            "about 10 to 12, all judys, mostly forbidden questions",
            f"{len(empties)}; judys {int((empties['persona_type'] == 'judy').sum())}; "
            f"forbidden {int((empties['category'] == 'forbidden').sum())}",
        ],
        ["Qdrant overlap@5 for judys", "near 1", pc.cell(mean((store == "qdrant") & (kind == "judy")))],
        [
            "Qdrant overlap@5, KB readers, targeted and generic",
            "low",
            pc.cell(mean((store == "qdrant") & (kind == "kb-reader") & company)),
        ],
        [
            "pgvector overlap@5: targeted and generic / forbidden and red team",
            "loss concentrated in targeted and generic",
            f"{pc.cell(mean((store == 'pgvector') & company))} / {pc.cell(mean((store == 'pgvector') & ~company))}",
        ],
        [
            "kb/ share of the top 5 on targeted questions: Qdrant / FAISS",
            "Qdrant mostly kb/ where FAISS has tenant documents",
            f"{pc.cell(mean((store == 'qdrant') & (category == 'targeted'), 'kb_share5'))} / "
            f"{pc.cell(mean((store == REFERENCE) & (category == 'targeted'), 'kb_share5'))}",
        ],
    ]
    return pc.markdown_table(["Item", "Predicted (section 6.0)", "Observed"], rows)


def summary(frame: pd.DataFrame, folder: Path, results_lines: list[str]) -> str:
    stores = list(dict.fromkeys(frame["store"]))
    by_category = mean_table(frame, ["store", "category"], "overlap5")
    by_type = mean_table(frame, ["store", "persona_type"], "overlap5")
    targeted = frame[frame["category"] == "targeted"]
    kb = targeted.groupby("store", sort=False)[["kb_share5", "reference_kb_share5"]].mean().reindex(stores)
    empties = frame[frame["empty"]]
    lines = [
        "# X0: the 2026-10-24 Kaggle run, re-analysed",
        "",
        f"Input: `{folder}`. Overlap@5 is the share of FAISS's top 5 (exact) among a store's top 5 for the same "
        "person and question; ties are not credited, so it can sit slightly below the run's recall@5. Questions "
        "whose person may read nothing (FAISS returned nothing) are left out.",
        "",
        "## Predictions of section 6.0, and what the data show",
        "",
        *predictions(frame),
        "## The run's own numbers (results.json)",
        "",
        *results_lines,
        "## Empty results (k=5, FAISS non-empty)",
        "",
        *pc.frame_table(
            empties.groupby(["store", "persona_type", "category"], sort=False).size().reset_index(name="questions")
        ),
        "### pgvector",
        "",
        *pc.frame_table(
            empties[empties["store"] == "pgvector"], ["person", "tenant", "category", "attack", "target", "question"]
        ),
        "## Overlap@5 by category",
        "",
        *pc.frame_table(pivot(by_category, "category", "overlap5", stores, CATEGORIES)),
        "## Overlap@5 by person type",
        "",
        *pc.frame_table(pivot(by_type, "persona_type", "overlap5", stores)),
        "## kb/ share of the top 5, targeted questions",
        "",
        *pc.frame_table(kb.reset_index()),
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Experiment X0: re-analysis of the original run's outputs")
    parser.add_argument("--input", default=None, help="folder with answers.jsonl (default: found under /kaggle/input)")
    parser.add_argument("--out", type=Path, default=Path("/kaggle/working/x0"))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    log.to(args.out / "x0.log")
    started = time.perf_counter()

    folder = pc.find_original_output(args.input)
    answers, results = folder / "answers.jsonl", folder / "results.json"
    log(f"original run's output: {folder}")
    er = pc.scenario()
    frame = scored(with_reference(load_answers(answers)), er.people())

    columns = ["store", "position", "person", "persona_type", "tenant", "category", "attack", "target"]
    columns += ["n_hits", "n_reference", "overlap5", "kb_share5", "reference_kb_share5", "empty", "question"]
    outputs = {
        "per_question.csv": frame[columns],
        "empties.csv": frame.loc[frame["empty"], columns],
        "pgvector_empties.csv": frame.loc[frame["empty"] & (frame["store"] == "pgvector"), columns],
        "recall5_by_category.csv": mean_table(frame, ["store", "category"], "overlap5"),
        "recall5_by_person_type.csv": mean_table(frame, ["store", "persona_type"], "overlap5"),
        "recall5_by_category_and_person_type.csv": mean_table(frame, ["store", "category", "persona_type"], "overlap5"),
        "kb_share_targeted.csv": frame[frame["category"] == "targeted"]
        .groupby(["store", "persona_type"], sort=False)[["kb_share5", "reference_kb_share5"]]
        .agg(["mean", "count"])
        .pipe(lambda t: t.set_axis([f"{a}_{b}" for a, b in t.columns], axis=1))
        .reset_index(),
    }
    for name, table in outputs.items():
        table.to_csv(args.out / name, index=False)
        log(f"wrote {args.out / name} ({len(table):,} rows)")

    results_lines, facts = results_summary(results)
    (args.out / "summary.md").write_text(summary(frame, folder, results_lines), encoding="utf-8")
    pgvector_empties = int((frame["empty"] & (frame["store"] == "pgvector")).sum())
    if facts.get("stores", {}).get("pgvector") is not None:
        implied = (facts["hits_expected"] - facts["stores"]["pgvector"]) / PER_EMPTY_QUESTION
        log(f"pgvector: {pgvector_empties} empty k=5 results in answers.jsonl; the hit shortfall implies {implied:.1f}")

    inputs = {p.name: {"bytes": p.stat().st_size, "sha256": sha256(p)} for p in (answers, results) if p.is_file()}
    pc.write_json(
        args.out / "manifest.json",
        {
            "experiment": "X0: re-analysis of the 2026-10-24 Kaggle run (section 6.0)",
            "input": str(folder),
            "inputs": inputs,
            "lines": len(frame),
            "stores": list(dict.fromkeys(frame["store"])),
            "categories": sorted(frame["category"].unique()),
            "outputs": [*outputs, "summary.md", "x0.log"],
            "versions": pc.versions(["wardowl", "pandas", "numpy"]),
            "seconds": round(time.perf_counter() - started, 1),
        },
    )
    log(f"X0 done in {time.perf_counter() - started:.0f} s; summary: {args.out / 'summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
