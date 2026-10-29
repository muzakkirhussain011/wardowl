"""X1 run 2 on Kaggle, one session per role (amendment 2 of PREREGISTRATION.md, item 8).

A Kaggle script kernel clones this repository at a fixed commit and runs this file with its role.
The roles split run 2 into sessions that run side by side and share one set of vectors:

    python x1_run2_kaggle.py --role smoke     # every role's code path on a small corpus, in one session
    python x1_run2_kaggle.py --role prep      # (GPU) corpus, chunk and query vectors, exact baseline, questions
    python x1_run2_kaggle.py --role shard-a   # pgvector hnsw-m16-efc64 build 0, the replays first
    python x1_run2_kaggle.py --role shard-b   # pgvector hnsw-m16-efc64 builds 1 and 2
    python x1_run2_kaggle.py --role shard-c   # pgvector hnsw-m32-efc200 builds 0 to 2, then the Qdrant grid
    python x1_run2_kaggle.py --role stats     # the statistics over the three shards' folders

The shards attach prep's output, and the statistics kernel the shards' outputs, as kernel sources;
both are found under /kaggle/input. A shard that ran out of session time is continued by a kernel
that attaches its output as well: its folder is copied back and x1_underretrieval.py resumes it.
Outputs: /kaggle/working/x1run2 (prep and shards), /kaggle/working/x1run2-stats, /kaggle/working/smoke.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

START = time.time()
WORK = Path("/kaggle/working")
INPUT = Path("/kaggle/input")
REPO_URL = "https://github.com/muzakkirhussain011/wardowl.git"
SESSION_HOURS = 8.5  # no setting starts later than this into the session (amendment 2: 9 h per session)
SHARDS = {
    "shard-a": ["--stores", "pgvector", "--families", "hnsw-m16-efc64", "--reps", "0"],
    "shard-b": ["--stores", "pgvector", "--families", "hnsw-m16-efc64", "--reps", "1,2"],
    "shard-c": ["--stores", "pgvector,qdrant", "--families", "hnsw-m32-efc200"],
}
ROLES = ("smoke", "prep", *SHARDS, "stats")


def say(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def run(command: list[str], check: bool = True) -> int:
    """Runs a command, printing its output as it goes; stops the session on failure when `check`."""
    say("$ " + " ".join(command))
    code = subprocess.run(command, env={**os.environ, "PYTHONUNBUFFERED": "1"}, check=False).returncode  # noqa: S603
    say(f"exit code {code}")
    if check and code:
        raise SystemExit(code)
    return code


def install(src: Path) -> None:
    commit = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    sha = commit.stdout.strip()
    say(f"wardowl and the paper's scripts at {sha}")
    packages = [
        f"wardowl[pgvector,qdrant] @ git+{REPO_URL}@{sha}",
        "qdrant-client>=1.16",
        "sentence-transformers>=3",
        "datasets>=2.19",
        "psutil",
        "pyarrow",
        "scipy",
    ]
    run([sys.executable, "-m", "pip", "install", "-q", *packages])


def folders_with(name: str) -> list[Path]:
    """Folders under /kaggle/input holding `name` (a file or a folder), sorted."""
    return sorted({p.parent for p in INPUT.glob(f"**/{name}")}) if INPUT.is_dir() else []


def prep_folder() -> Path:
    """prep's output: the x1run2 folder with query vectors and no results of its own."""
    found = [f for f in folders_with("query_vectors.json") if not (f / "runs").is_dir()]
    if not found:
        raise SystemExit("prep's output is not attached: add the prep kernel as a kernel source")
    if len(found) > 1:
        say(f"several prep folders attached ({found}); using {found[0]}")
    return found[0]


def continue_shard(role: str, out: Path) -> None:
    """A continuation kernel attaches the unfinished shard's output: its folder is copied back."""
    earlier = [f for f in folders_with("role.txt") if (f / "role.txt").read_text(encoding="utf-8").strip() == role]
    if earlier and not out.exists():
        shutil.copytree(earlier[-1], out, ignore=shutil.ignore_patterns("stats"))
        say(f"continuing {role} from {earlier[-1]}")


def x1(src: Path, *args: str, check: bool = True) -> int:
    return run([sys.executable, str(src / "benchmarks" / "paper" / "x1_underretrieval.py"), *args], check=check)


def stats(src: Path, *args: str) -> int:
    return run([sys.executable, str(src / "benchmarks" / "paper" / "x1_stats.py"), *args], check=False)


def smoke(src: Path) -> int:
    """Every role in one session, on the small corpus: prep, the three shards, the statistics."""
    base = WORK / "smoke"
    cache = ["--cache", "/tmp/x1-cache"]  # noqa: S108 - a scratch folder, kept out of the output
    x1(src, "--smoke", "--prepare-only", "--out", str(base / "prep"), *cache)
    pin = ["--pin-from", str(base / "prep")]
    codes = [
        x1(src, "--smoke", *SHARDS["shard-a"], "--out", str(base / "a"), *pin, *cache, check=False),
        x1(src, "--smoke", *SHARDS["shard-b"][:-1], "1", "--out", str(base / "b"), *pin, *cache, check=False),
        x1(src, "--smoke", *SHARDS["shard-c"], "--out", str(base / "c"), *pin, *cache, check=False),
    ]
    folders = [str(base / s) for s in ("a", "b", "c")]
    codes.append(stats(src, "--in", *folders, "--out", str(base / "stats"), "--resamples", "200"))
    say(f"smoke exit codes (shard a, b, c, statistics): {codes}")
    return max(codes)


def main() -> int:
    parser = argparse.ArgumentParser(description="X1 run 2 on Kaggle, one session per role")
    parser.add_argument("--role", choices=ROLES, required=True)
    parser.add_argument("--src", type=Path, required=True, help="the clone of the wardowl repository")
    args = parser.parse_args()
    deadline = str(START + SESSION_HOURS * 3600)
    say(f"role {args.role}; no setting starts after {SESSION_HOURS} h of this session")
    install(args.src)
    if args.role == "smoke":
        return smoke(args.src)
    if args.role == "prep":  # on the CPU when no GPU session is free (amendment 2, item 8): about an hour
        return x1(args.src, "--prepare-only", "--allow-cpu-embedding", "--out", str(WORK / "x1run2"))
    if args.role == "stats":
        shards = [f for f in folders_with("role.txt") if (f / "runs").is_dir()]
        say(f"shard folders: {shards}")
        return stats(args.src, "--in", *map(str, shards), "--out", str(WORK / "x1run2-stats"))
    out = WORK / "x1run2"
    continue_shard(args.role, out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "role.txt").write_text(args.role + "\n", encoding="utf-8")
    common = ["--out", str(out), "--pin-from", str(prep_folder()), "--cache", "/tmp/x1-cache"]  # noqa: S108
    return x1(args.src, *SHARDS[args.role], *common, "--resume", "--deadline", deadline, check=False)


if __name__ == "__main__":
    raise SystemExit(main())
