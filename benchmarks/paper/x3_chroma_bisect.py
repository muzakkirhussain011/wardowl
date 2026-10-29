"""X3 follow-up, exploratory (PREREG_X3_X6.md, amendment 4, part B, item 6): Chroma's crash threshold.

    python x3_chroma_bisect.py --data x6data --out results [--mode full|smoke] [--gdb]

In run 40940385704, Chroma refused filters of 1,000 to 10,000 groups with SQLite's expression-depth
error and its process ended with signal 11 at 40,000 groups. This script builds seed 0's X3 corpus
(x3_filter_scaling.py, unchanged) in a fresh process for each level and runs one retrieval through
wardowl's public API with a subject holding the first G of the 40,000-level groups, so the filter
has G + 1 group values on keys the documents hold. It tries G = 40,000 first, then bisects between
10,000 and 40,000 to 1,000 groups or at most six levels, and, with --gdb, runs G = 40,000 once more
under gdb for the native stack. Every child runs with Python's fault handler on (except under gdb,
which catches the signal first); its stdout and stderr are kept in the records.

Writes <out>/x3bisect-chroma.jsonl (exp "x3bisect", so x3_stats.py does not read it).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import x3_filter_scaling as x3
import x3x6_common as common
from x3x6_common import log

TOP = 40_000
LOW = 10_000
STEPS = {"full": 6, "smoke": 2}
CHILD_TIMEOUT_S = 1800


def child(args: argparse.Namespace) -> int:
    """One level in this process: build, translate, retrieve once, record what happened."""
    from wardowl import MetadataACLAuthorizer, PermissionedRetriever, Query, Subject
    from wardowl.backends.chroma import filter_to_where

    records = common.Records(Path(args.out) / "x3bisect-chroma.jsonl", base(args))
    level = args.level
    semantic, query_pool, described = x3.load(Path(args.data))
    settings = x3.MODES[args.mode]
    world = x3.corpus(0, settings["docs"], semantic, query_pool, settings["queries"])
    docs, vectors = x3.documents(world)
    target = common.make_target("chroma")
    common.connect(target)
    clock = time.monotonic()
    built = target.build(common.unique_base("x3bis"), docs, vectors)
    build_s = round(time.monotonic() - clock, 1)
    authorizer = MetadataACLAuthorizer()
    subject = Subject(f"reader-{level}", [f"L{TOP}-{j}" for j in range(level)])
    f = authorizer.filter_for(subject)
    clock = time.perf_counter()
    where = filter_to_where(f)
    translate_ms = round((time.perf_counter() - clock) * 1000, 3)
    size = common.size_of(where)
    retriever = PermissionedRetriever(built.vector, authorizer, strategy="prefilter")
    query = Query(text=x3.QUERY_TEXT, vector=world["queries"][0])
    records.write({"type": "attempt", "G": level, "corpus": described, "docs": len(docs), "build_s": build_s,
                   "translate_ms": translate_ms, "translation_chars": size})  # fmt: skip
    print(f"child G={level}: built in {build_s} s, where of {size:,} characters, querying", flush=True)
    observed = x3.measure(retriever, query, subject, set(), 0)
    outcome = "error" if observed.get("error") else "answer"
    records.write({"type": "level", "G": level, "outcome": outcome, **observed})
    print(f"child G={level}: {outcome} {observed.get('error') or ''}", flush=True)
    records.close()
    target.close()
    return 0


def base(args: argparse.Namespace) -> dict[str, Any]:
    return {"exp": "x3bisect", "store": "chroma", "mode": args.mode, "run": common.RUN_ID}


def attempt(args: argparse.Namespace, records: common.Records, level: int, *, gdb: bool = False) -> str:
    """Run one level in a child process; returns 'crash', 'error', 'answer' or 'other'."""
    command = [sys.executable, str(Path(__file__).resolve()), "--child", "--level", str(level),
               "--data", args.data, "--out", args.out, "--mode", args.mode]  # fmt: skip
    env = dict(os.environ)
    if gdb:
        env.pop("PYTHONFAULTHANDLER", None)
        command = ["gdb", "-q", "-batch", "-ex", "set pagination off", "-ex", "set print thread-events off",
                   "-ex", "run", "-ex", "info threads", "-ex", "bt 40", "-ex", "bt -15", "--args", *command]  # fmt: skip
    else:
        env["PYTHONFAULTHANDLER"] = "1"
    log(f"x3 bisect: G={level:,}{' under gdb' if gdb else ''}")
    started = time.monotonic()
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=CHILD_TIMEOUT_S, env=env, check=False)  # noqa: S603
        code, out, err = done.returncode, done.stdout or "", done.stderr or ""
    except subprocess.TimeoutExpired as error:
        code = -999
        out = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        err = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
    seconds = round(time.monotonic() - started, 1)
    print(out[-8000:], flush=True)
    print(err[-8000:], file=sys.stderr, flush=True)
    text = out + "\n" + err
    if gdb:
        crashed = "SIGSEGV" in text or "signal SIG" in text
    else:
        crashed = code < 0 and code != -999
    if crashed:
        result = "crash"
    elif f"child G={level}: error" in out:
        result = "error"
    elif f"child G={level}: answer" in out:
        result = "answer"
    else:
        result = "other"
    records.write({"type": "probe", "G": level, "gdb": gdb, "returncode": code, "result": result, "seconds": seconds,
                   "stdout_tail": out[-12000:], "stderr_tail": err[-12000:]})  # fmt: skip
    log(f"x3 bisect: G={level:,}: {result} (exit status {code}, {seconds:.0f} s)")
    return result


def run(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    records = common.Records(out / "x3bisect-chroma.jsonl", base(args))
    records.write({"type": "start", "args": vars(args), "host": common.host(), "top": TOP, "low": LOW,
                   "steps": STEPS[args.mode]})  # fmt: skip
    found: dict[int, str] = {TOP: attempt(args, records, TOP)}
    lo, hi = LOW, TOP
    if found[TOP] == "crash":
        for _ in range(STEPS[args.mode]):
            if hi - lo <= 1000:
                break
            mid = int(round((lo + hi) / 2 / 250) * 250)
            found[mid] = attempt(args, records, mid)
            if found[mid] == "crash":
                hi = mid
            elif found[mid] in ("error", "answer"):
                lo = mid
            else:
                break  # neither: the bisection cannot go on soundly
    gdb_result = None
    if args.gdb:
        if shutil.which("gdb"):
            gdb_result = attempt(args, records, TOP, gdb=True)
        else:
            records.write({"type": "gdb-missing"})
    records.write({"type": "end", "found": {str(k): v for k, v in sorted(found.items())}, "last_ok": lo,
                   "first_crash": hi if found.get(hi) == "crash" else None, "gdb": gdb_result})  # fmt: skip
    records.close()
    common.annotate("notice", "x3 chroma bisect", f"{dict(sorted(found.items()))}; bracket [{lo:,}, {hi:,}]")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", default="x6data")
    parser.add_argument("--out", default="results")
    parser.add_argument("--mode", choices=sorted(x3.MODES), default="full")
    parser.add_argument("--gdb", action="store_true")
    parser.add_argument("--child", action="store_true")
    parser.add_argument("--level", type=int, default=TOP)
    args = parser.parse_args(argv)
    try:
        return child(args) if args.child else run(args)
    except BaseException as error:
        if not isinstance(error, SystemExit):
            common.fail_loudly("x3 bisect", error)
        raise


if __name__ == "__main__":
    sys.exit(main())
