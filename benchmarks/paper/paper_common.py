"""What the paper's experiment scripts share: x0_reanalysis.py, x1_underretrieval.py and x1_stats.py.

Logging that also goes to a file, finding the original run's outputs under /kaggle/input, the
scenario module acceptance/kaggle/enterprise_rag.py, person types, tidy tables, Markdown tables and
the JSON manifest. Nothing here starts a store or uses a GPU.
"""

from __future__ import annotations

import contextlib
import json
import math
import os
import sys
import time
import traceback
from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path
from typing import Any

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
KAGGLE_INPUT = Path("/kaggle/input")
SEED = 20261026  # the run-level seed: person order, fixed EXPLAIN sample, bootstrap
KB_PREFIX = "kb/"  # ids of the shared FiQA knowledge base


# ---- logging -------------------------------------------------------------------------------------


class Log:
    """Prints timestamped lines, and appends them to a file once `to` names one."""

    def __init__(self) -> None:
        self.path: Path | None = None
        self.warned: set[str] = set()

    def to(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path

    def __call__(self, message: str) -> None:
        line = f"[{time.strftime('%H:%M:%S')}] {message}"
        print(line, flush=True)
        if self.path is not None:
            with self.path.open("a", encoding="utf-8") as out:
                out.write(line + "\n")

    def loud(self, message: str) -> None:
        """A warning that must not scroll past unnoticed: framed, and kept in the log file."""
        bar = "!" * 100
        for line in (bar, f"WARNING: {message}", bar):
            self(line)

    def once(self, key: str, message: str) -> None:
        """`loud`, the first time `key` is seen."""
        if key not in self.warned:
            self.warned.add(key)
            self.loud(message)


log = Log()


# ---- inputs ----------------------------------------------------------------------------------------


def find_original_output(explicit: str | Path | None = None) -> Path:
    """The folder holding the original run's answers.jsonl (and results.json).

    `explicit` wins. Otherwise /kaggle/input is searched, since Kaggle mounts an attached notebook
    output under a path that depends on the owner and the notebook's slug. A folder that also holds
    results.json is preferred; finding several is reported, never silently resolved.
    """
    if explicit:
        folder = Path(explicit)
        if not (folder / "answers.jsonl").is_file():
            raise FileNotFoundError(f"{folder} has no answers.jsonl")
        return folder
    found = sorted(KAGGLE_INPUT.glob("**/answers.jsonl"))
    if not found:
        raise FileNotFoundError(
            "no answers.jsonl under /kaggle/input: add the original run's output "
            "(notebook notebookd8377caca8) to this notebook as input, or pass its folder"
        )
    complete = [p.parent for p in found if (p.parent / "results.json").is_file()]
    chosen = complete[0] if complete else found[0].parent
    if len(found) > 1:
        log.loud(f"{len(found)} answers.jsonl files under /kaggle/input ({[str(p) for p in found]}); using {chosen}")
    return chosen


def input_files(pattern: str) -> list[Path]:
    """Files under /kaggle/input matching a glob pattern, sorted."""
    return sorted(KAGGLE_INPUT.glob(pattern)) if KAGGLE_INPUT.is_dir() else []


def scenario(repo: Path = REPO) -> Any:
    """acceptance/kaggle/enterprise_rag.py of this checkout, imported as a module.

    Only its folder goes on sys.path (enterprise_rag adds acceptance/ itself), never the repository
    root, whose wardowl/ would shadow the installed wardowl.
    """
    folder = repo / "acceptance" / "kaggle"
    if not (folder / "enterprise_rag.py").is_file():
        raise FileNotFoundError(f"{folder / 'enterprise_rag.py'} is missing: is {repo} the wardowl repository?")
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
    import enterprise_rag

    return enterprise_rag


# ---- people and questions ------------------------------------------------------------------------


def persona_type(persona: Any) -> str:
    """judy (only `board`), kb-reader (reads the shared FiQA base), no-groups (mallory), probe-<group>."""
    if "-probe-" in persona.id:
        return f"probe-{persona.groups[0]}"
    groups = set(persona.groups)
    if not groups:
        return "no-groups"
    if groups == {"board"}:
        return "judy"
    if groups & {"employees", "contractors"}:
        return "kb-reader"
    return "other"


def region(category: str) -> str:
    """Where a question's answer lives: company documents, the FiQA base, or nowhere (red team)."""
    if category == "probe-fiqa":
        return "kb"
    if category == "redteam":
        return "redteam"
    return "company"


# ---- tables -------------------------------------------------------------------------------------


def _has_pyarrow() -> bool:
    from importlib.util import find_spec

    return find_spec("pyarrow") is not None


def write_table(frame: pd.DataFrame, stem: Path) -> Path:
    """Writes `frame` as <stem>.parquet, or <stem>.csv when pyarrow is missing (said loudly).

    The file is written under a temporary name and renamed, so a crash never leaves a half-written
    table that a resumed run would trust. `stem` may contain dots: the suffix is appended, not swapped.
    """
    stem.parent.mkdir(parents=True, exist_ok=True)
    if _has_pyarrow():
        path = stem.parent / f"{stem.name}.parquet"
        partial = stem.parent / f"{stem.name}.parquet.partial"
        frame.to_parquet(partial, index=False)
    else:
        log.once("pyarrow", "pyarrow is not installed: tables are written as CSV instead of Parquet")
        path = stem.parent / f"{stem.name}.csv"
        partial = stem.parent / f"{stem.name}.csv.partial"
        frame.to_csv(partial, index=False)
    partial.replace(path)
    return path


def read_tables(folder: Path) -> pd.DataFrame:
    """Every table x1 wrote into `folder` (Parquet or CSV), concatenated; empty if there is none."""
    paths = sorted([*folder.glob("*.parquet"), *folder.glob("*.csv")]) if folder.is_dir() else []
    frames = [pd.read_parquet(p) if p.suffix == ".parquet" else pd.read_csv(p) for p in paths]
    frames = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def read_table(stem: Path) -> pd.DataFrame | None:
    """<stem>.parquet or <stem>.csv, whichever exists, or None."""
    for suffix in (".parquet", ".csv"):
        path = stem.parent / f"{stem.name}{suffix}"
        if path.is_file():
            return pd.read_parquet(path) if suffix == ".parquet" else pd.read_csv(path)
    return None


def write_json(path: Path, data: Any) -> None:
    """JSON written under a temporary name and renamed into place."""
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.parent / f"{path.name}.partial"
    partial.write_text(json.dumps(data, indent=2, default=str, allow_nan=True) + "\n", encoding="utf-8")
    partial.replace(path)


def cell(value: Any) -> str:
    """A table cell: shares to three places, larger numbers to one, missing as n/a."""
    if value is None:
        return "n/a"
    if isinstance(value, float):
        if math.isnan(value):
            return "n/a"
        return f"{value:.3f}" if abs(value) < 10 else f"{value:.1f}"
    return str(value).replace("|", "/")


def markdown_table(header: Sequence[str], rows: Iterable[Sequence[Any]]) -> list[str]:
    """A Markdown table as lines, followed by a blank line."""
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return [*lines, ""]


def frame_table(frame: pd.DataFrame, columns: Sequence[str] | None = None) -> list[str]:
    """`markdown_table` of a DataFrame's columns."""
    columns = list(columns or frame.columns)
    rows = [[row[c] for c in columns] for row in frame.to_dict("records")]
    return markdown_table(columns, rows)


# ---- the manifest --------------------------------------------------------------------------------


class Manifest:
    """manifest.json of one output folder: one entry per invocation, rewritten after every change.

    Several invocations may write to the same folder (pgvector in one notebook cell, Qdrant in the
    next, or a resumed run), so earlier entries are kept and this one is appended.
    """

    def __init__(self, path: Path, experiment: str, options: dict[str, Any]) -> None:
        self.path = path
        self.data: dict[str, Any] = {"experiment": experiment, "invocations": []}
        if path.is_file():
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                broken = path.parent / f"{path.name}.unreadable-{int(time.time())}"
                path.replace(broken)
                log.loud(f"{path} was not valid JSON; kept as {broken} and started a new manifest")
                self.data = {"experiment": experiment, "invocations": []}
        self.entry: dict[str, Any] = {
            "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "argv": sys.argv,
            "options": options,
            "status": "running",
            "stages": {},
            "settings": {},
            "unsupported": [],
            "failures": [],
            "skipped": [],
            "warnings": [],
        }
        self.data.setdefault("invocations", []).append(self.entry)
        self.save()

    def save(self) -> None:
        write_json(self.path, self.data)

    def set(self, key: str, value: Any) -> None:
        self.entry[key] = value
        self.save()

    def add(self, key: str, item: Any) -> None:
        self.entry.setdefault(key, []).append(item)
        self.save()

    def warn(self, message: str) -> None:
        """A loud warning, also kept in the manifest."""
        log.loud(message)
        self.add("warnings", message)

    @contextlib.contextmanager
    def stage(self, name: str) -> Iterator[dict[str, Any]]:
        """Records a stage's start, end, duration and outcome; an exception is recorded, then re-raised."""
        record: dict[str, Any] = {"status": "running", "started": time.strftime("%H:%M:%S")}
        self.entry["stages"][name] = record
        self.save()
        clock = time.perf_counter()
        log(f"== stage {name}")
        try:
            yield record
        except BaseException as error:
            record.update(status="failed", error=f"{type(error).__name__}: {error}", trace=traceback.format_exc())
            raise
        else:
            record["status"] = "done"
        finally:
            record["seconds"] = round(time.perf_counter() - clock, 1)
            self.save()
            log(f"== stage {name}: {record['status']} in {record['seconds']:.0f} s")

    def finish(self, status: str) -> None:
        self.entry["status"] = status
        self.entry["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.save()


def versions(packages: Sequence[str]) -> dict[str, str | None]:
    """Installed versions of these distributions (None when absent)."""
    from importlib import metadata

    found: dict[str, str | None] = {}
    for package in packages:
        try:
            found[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            found[package] = None
    return found


def hardware() -> dict[str, Any]:
    """CPUs, memory, GPUs and free disk, as far as the installed packages can tell."""
    info: dict[str, Any] = {"cpus": os.cpu_count()}
    with contextlib.suppress(ImportError):
        import psutil

        info["memory_gib"] = round(psutil.virtual_memory().total / 2**30, 1)
        info["disk_free_gib"] = round(psutil.disk_usage("/").free / 2**30, 1)
    with contextlib.suppress(ImportError):
        import torch

        info["gpus"] = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
        info["cuda"] = torch.version.cuda
    return info
