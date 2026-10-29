"""The job matrices of the paper-x2-x5 workflow, from benchmarks/paper/x2x5_config.json.

Standard library only (it runs before anything is installed):

    python3 benchmarks/paper/x2x5_plan.py --out "$GITHUB_OUTPUT"

The mode (smoke or full) and the run whose data to reuse come from the config file, or from the
workflow_dispatch inputs (INPUT_MODE, INPUT_DATA_RUN) when they are set. Each output is one line,
`name=value`; the matrices are JSON lists of `include` entries.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
X2_STORES = ("pgvector", "qdrant", "elasticsearch", "opensearch", "weaviate", "redis", "milvus", "mongodb", "lancedb",
             "chroma")  # fmt: skip
E_LAYOUTS = {"qdrant": "as-run,tenant", "elasticsearch": "default,int8"}
M_LAYOUTS = {"qdrant": "as-run"}
SIZES = {
    "smoke": {"e_shards": 2, "m_shards": 2, "builds": [0], "minutes": 25, "resamples": 1000},
    "full": {"e_shards": 6, "m_shards": 8, "builds": [0, 1, 2], "minutes": 320, "resamples": 10000},
}


def plan(mode: str) -> dict[str, object]:
    size = SIZES[mode]
    builds = size["builds"]
    every = ",".join(str(b) for b in builds)
    embed_e = [{"corpus": "e", "shard": i, "shards": size["e_shards"]} for i in range(size["e_shards"])]
    embed_m = [{"corpus": "m", "shard": i, "shards": size["m_shards"]} for i in range(size["m_shards"])]
    x2e = [{"store": s, "layouts": E_LAYOUTS.get(s, "default"), "builds": every, "label": s} for s in X2_STORES]
    x2e.append({"store": "faiss", "layouts": "default", "builds": "0", "label": "faiss"})
    x2m = []
    for s in X2_STORES:
        for b in builds:
            x2m.append({"store": s, "layouts": M_LAYOUTS.get(s, "default"), "builds": str(b), "label": f"{s}-b{b}"})
    for b in builds:
        x2m.append({"store": "qdrant", "layouts": "tenant", "builds": str(b), "label": f"qdrant-tenant-b{b}"})
    x2m.append({"store": "faiss", "layouts": "default", "builds": "0", "label": "faiss"})
    x5e = [
        {"store": "pgvector", "layouts": "default", "builds": every, "label": "pgvector"},
        {"store": "qdrant", "layouts": "as-run,tenant", "builds": every, "label": "qdrant"},
    ]
    x5m = [
        {"store": s, "layouts": "default" if s == "pgvector" else "as-run", "builds": str(b), "label": f"{s}-b{b}"}
        for s in ("pgvector", "qdrant")
        for b in builds
    ]
    return {
        "mode": mode,
        "smoke": "--smoke" if mode == "smoke" else "",
        "minutes": size["minutes"],
        "resamples": size["resamples"],
        "embed_e": embed_e,
        "embed_m": embed_m,
        "x2e": x2e,
        "x2m": x2m,
        "x5e": x5e,
        "x5m": x5m,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="the file GITHUB_OUTPUT names")
    parser.add_argument("--config", type=Path, default=HERE / "x2x5_config.json")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    mode = os.environ.get("INPUT_MODE") or config.get("mode", "smoke")
    data_run = os.environ.get("INPUT_DATA_RUN") or str(config.get("data_run_id") or "")
    if mode not in SIZES:
        raise SystemExit(f"unknown mode {mode!r}")
    if data_run and not data_run.isdigit():
        raise SystemExit(f"data_run_id must be a workflow run id, not {data_run!r}")
    outputs = {**plan(mode), "data_run": data_run}
    with args.out.open("a", encoding="utf-8") as out:
        for name, value in outputs.items():
            text = value if isinstance(value, str) else json.dumps(value, separators=(",", ":"))
            out.write(f"{name}={text}\n")
    print(json.dumps(outputs, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
