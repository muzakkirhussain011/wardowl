"""Shared plumbing for the X4 and X7 harnesses and their statistics.

Records (JSON lines), run information and versions, annotations, HTTP calls to the engines' admin
APIs, the engines themselves (an OPA process, OpenFGA and SpiceDB admin clients), Docker control,
the fault-injection proxy, an error log, and the bootstrap used by `x4_stats.py` and `x7_stats.py`.

Nothing here imports wardowl, and numpy is imported only where it is used, so the statistics
scripts run with the standard library and numpy alone.
"""

from __future__ import annotations

import collections
import contextlib
import importlib.metadata
import json
import math
import os
import platform
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA = 1
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
POLICIES = HERE / "x4x7_policies"
PROXY_SCRIPT = HERE / "x4x7_proxy.py"
RUN_ID = os.environ.get("GITHUB_RUN_ID", "local")
JOB = os.environ.get("X4X7_JOB", "local")

# The images the workflow starts (for the record; the workflow is where they are pinned).
IMAGES = {
    "openfga": "openfga/openfga:v1.22.0",
    "spicedb": "authzed/spicedb:v1.56.2",
    "cerbos": "ghcr.io/cerbos/cerbos:0.56.0",
    "postgres": "pgvector/pgvector:pg17",
    "qdrant": "qdrant/qdrant:v1.19.2",
    "redis": "redis:8.10.2-alpine",
    "opa": "1.21.2 (binary)",
}
PACKAGES = ("wardowl", "numpy", "faiss-cpu", "psycopg", "psycopg-pool", "qdrant-client", "redis", "httpx")

RESAMPLES = 10_000
BOOTSTRAP_SEED = 20261029

clock = time.perf_counter


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def log(message: str) -> None:
    print(f"[{now_iso()}] {message}", flush=True)


# ---- records ---------------------------------------------------------------------------------------


def _jsonable(value: Any) -> Any:
    if isinstance(value, (set, frozenset)):
        return sorted(value, key=str)
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, Mapping):
        return dict(value)
    return repr(value)


class Records:
    """Appends one JSON object per line to `<out>/<name>.jsonl`, from any thread."""

    def __init__(self, out: str | Path, name: str) -> None:
        self.path = Path(out) / f"{name}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self.count = 0

    def write(self, record: Mapping[str, Any]) -> None:
        line = json.dumps({"schema": SCHEMA, "job": JOB, "run": RUN_ID, **record}, default=_jsonable)
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            self.count += 1


def read_records(paths: Iterable[str | Path]) -> list[dict[str, Any]]:
    """Every record of the given JSON-lines files (a line that does not parse is skipped)."""
    out: list[dict[str, Any]] = []
    for path in paths:
        with Path(path).open(encoding="utf-8") as handle:
            for line in handle:
                with contextlib.suppress(ValueError):
                    out.append(json.loads(line))
    return out


def run_info(experiment: str, profile: str, settings: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "type": "run-start",
        "experiment": experiment,
        "profile": profile,
        "settings": dict(settings),
        "started": now_iso(),
        "commit": os.environ.get("GITHUB_SHA"),
        "ref": os.environ.get("GITHUB_REF_NAME"),
        "workflow_run": RUN_ID,
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpus": os.cpu_count(),
        "packages": package_versions(),
    }


def package_versions() -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for name in PACKAGES:
        try:
            found[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            found[name] = None
    return found


def command(*args: str, timeout: float = 60) -> str | None:
    """A command's output, or None when it cannot run or fails."""
    try:
        done = subprocess.run(list(args), capture_output=True, text=True, timeout=timeout, check=False)  # noqa: S603
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def image_info(container: str) -> dict[str, Any] | None:
    """The image a container runs, with its id and registry digests."""
    found = command("docker", "inspect", "--format", "{{.Config.Image}}|{{.Image}}", container)
    if not found or "|" not in found:
        return None
    image, image_id = found.split("|", 1)
    digests = command("docker", "image", "inspect", "--format", "{{json .RepoDigests}}", image_id)
    try:
        parsed = json.loads(digests) if digests else None
    except ValueError:
        parsed = digests
    return {"container": container, "image": image, "image_id": image_id, "digests": parsed}


def versions_record(containers: Sequence[str]) -> dict[str, Any]:
    opa = command("opa", "version")
    return {
        "type": "versions",
        "images": {name: image_info(name) for name in containers},
        "pinned": IMAGES,
        "opa": opa.splitlines()[:3] if opa else None,
        "packages": package_versions(),
    }


# ---- annotations and errors -------------------------------------------------------------------------


def _escape_data(text: str) -> str:
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _escape_property(text: str) -> str:
    return _escape_data(text).replace(":", "%3A").replace(",", "%2C")


def annotate(level: str, title: str, message: str, limit: int = 3800) -> None:
    """A GitHub Actions annotation (notice, warning or error). GitHub shows at most 10 of each level
    per step; the message is cut at `limit` characters."""
    if len(message) > limit:
        message = message[:limit] + f"... (+{len(message) - limit} characters)"
    print(f"::{level} title={_escape_property(title)}::{_escape_data(message)}", flush=True)


def error_info(error: BaseException) -> dict[str, Any]:
    frames = traceback.extract_tb(error.__traceback__)[-4:]
    cause = error.__cause__
    return {
        "class": f"{type(error).__module__}.{type(error).__qualname__}",
        "message": str(error)[:2000],
        "cause": None if cause is None else f"{type(cause).__qualname__}: {str(cause)[:300]}",
        "where": [f"{Path(f.filename).name}:{f.lineno} {f.name}" for f in frames],
    }


class Errors:
    """Distinct errors met by the harness, counted, for the log, the records and annotations."""

    def __init__(self) -> None:
        self.counts: collections.Counter[tuple[str, str, str]] = collections.Counter()
        self.first: dict[tuple[str, str, str], dict[str, Any]] = {}
        self._lock = threading.Lock()

    def add(self, where: str, error: BaseException) -> dict[str, Any]:
        info = error_info(error)
        key = (where, info["class"], info["message"][:160])
        with self._lock:
            if key not in self.first:
                log(f"error in {where}: {info['class']}: {info['message'][:400]} at {info['where']}")
            self.counts[key] += 1
            self.first.setdefault(key, info)
        return info

    def report(self, records: Records, title: str) -> None:
        for (where, cls, message), count in self.counts.most_common():
            records.write({"type": "harness-error", "where": where, "count": count, **self.first[(where, cls, message)]})
        top = self.counts.most_common(9)
        for (where, cls, message), count in top:
            info = self.first[(where, cls, message)]
            annotate("warning", f"{title}: {where} x{count}", f"{cls}: {info['message'][:1500]}\nat {info['where']}")
        if not self.counts:
            annotate("notice", f"{title}: no harness errors", "every call the harness made returned")


# ---- HTTP ------------------------------------------------------------------------------------------


class ServiceError(Exception):
    """An HTTP call failed; `status` is None when no answer came."""

    def __init__(self, message: str, status: int | None = None, body: str = "") -> None:
        super().__init__(message)
        self.status = status
        self.body = body


def call(
    method: str,
    url: str,
    payload: Any = None,
    *,
    text: str | None = None,
    token: str | None = None,
    headers: Mapping[str, str] | None = None,
    timeout: float = 60.0,
    lines: bool = False,
) -> Any:
    """An admin or raw API call: the decoded JSON answer ({} for none), or with `lines` a list with
    one decoded value per line of a newline-delimited answer."""
    data = None
    sent: dict[str, str] = dict(headers or {})
    if text is not None:
        data = text.encode()
        sent.setdefault("Content-Type", "text/plain")
    elif payload is not None:
        data = json.dumps(payload).encode()
        sent.setdefault("Content-Type", "application/json")
    if token:
        sent["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=sent, method=method)  # noqa: S310
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            body = response.read()
    except urllib.error.HTTPError as error:
        detail = error.read()[:600].decode("utf-8", "replace")
        raise ServiceError(f"{method} {url}: HTTP {error.code}: {detail}", error.code, detail) from None
    except (urllib.error.URLError, OSError) as error:
        raise ServiceError(f"{method} {url}: {error}") from None
    if lines:
        out = []
        for line in body.splitlines():
            if line.strip():
                try:
                    out.append(json.loads(line))
                except ValueError:
                    out.append({"unparsed": line[:200].decode("utf-8", "replace")})
        return out
    if not body.strip():
        return {}
    try:
        return json.loads(body)
    except ValueError:
        return body.decode("utf-8", "replace")


def wait_for(check: Callable[[], bool], timeout: float, interval: float = 0.25, what: str = "condition") -> float:
    """Seconds until `check()` is true; TimeoutError after `timeout`."""
    start = clock()
    while True:
        try:
            if check():
                return clock() - start
        except Exception:  # noqa: S110 - a check that raises is a check that is not yet true
            pass
        if clock() - start > timeout:
            raise TimeoutError(f"{what} not reached within {timeout:.0f} s")
        time.sleep(interval)


def healthy(url: str, timeout: float = 2.0) -> bool:
    try:
        call("GET", url, timeout=timeout)
    except ServiceError:
        return False
    return True


def parallel(function: Callable[[Any], Any], items: Sequence[Any], threads: int = 4) -> list[Any]:
    if threads <= 1 or len(items) <= 1:
        return [function(item) for item in items]
    with ThreadPoolExecutor(threads) as pool:
        return list(pool.map(function, items))


# ---- Docker ----------------------------------------------------------------------------------------


def docker(*args: str, timeout: float = 120) -> str:
    done = subprocess.run(["docker", *args], capture_output=True, text=True, timeout=timeout, check=False)  # noqa: S603, S607
    if done.returncode != 0:
        raise RuntimeError(f"docker {' '.join(args)}: {done.stderr.strip()[:500]}")
    return done.stdout.strip()


def container_running(name: str) -> bool:
    return command("docker", "inspect", "--format", "{{.State.Running}}", name) == "true"


# ---- engines ---------------------------------------------------------------------------------------


class OpaProcess:
    """An OPA server run by the harness, so that X7 can kill and restart it. With `files`, OPA loads
    them at start (policies and data), as a production server loads its bundle."""

    def __init__(self, port: int = 8181, files: Sequence[str | Path] = (), log_path: str | Path | None = None) -> None:
        self.port = port
        self.files = [str(f) for f in files]
        self.log_path = Path(log_path) if log_path else None
        self.process: subprocess.Popen[bytes] | None = None

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def start(self, timeout: float = 60) -> float:
        """Start OPA; the seconds until it answers its health check."""
        output: Any = subprocess.DEVNULL
        if self.log_path is not None:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            output = self.log_path.open("ab")
        started = clock()
        self.process = subprocess.Popen(  # noqa: S603
            ["opa", "run", "--server", f"--addr=127.0.0.1:{self.port}", "--log-level=error", *self.files],  # noqa: S607
            stdout=output,
            stderr=subprocess.STDOUT,
        )
        wait_for(lambda: healthy(f"{self.url}/health"), timeout, what="OPA health")
        return clock() - started

    def kill(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.kill()
            with contextlib.suppress(subprocess.TimeoutExpired):
                self.process.wait(10)
        self.process = None

    def put_policy(self, policy_id: str, text: str) -> None:
        call("PUT", f"{self.url}/v1/policies/{policy_id}", text=text)

    def put_data(self, path: str, value: Any) -> None:
        call("PUT", f"{self.url}/v1/data/{path}", value, timeout=300)


class OpenFGAAdmin:
    """OpenFGA's HTTP API for setup and raw measurements (wardowl's adapter is measured separately)."""

    def __init__(self, url: str) -> None:
        self.url = url.rstrip("/")

    def create_store(self, name: str) -> str:
        return str(call("POST", f"{self.url}/stores", {"name": name})["id"])

    def write_model(self, store: str, model: Mapping[str, Any]) -> str:
        return str(call("POST", f"{self.url}/stores/{store}/authorization-models", model)["authorization_model_id"])

    def write(
        self, store: str, model_id: str, writes: Sequence[Mapping[str, str]] = (), deletes: Sequence[Mapping[str, str]] = ()
    ) -> None:
        payload: dict[str, Any] = {"authorization_model_id": model_id}
        if writes:
            payload["writes"] = {"tuple_keys": list(writes)}
        if deletes:
            payload["deletes"] = {"tuple_keys": list(deletes)}
        call("POST", f"{self.url}/stores/{store}/write", payload)

    def write_all(self, store: str, model_id: str, tuples: Sequence[Mapping[str, str]], threads: int = 4) -> int:
        """Write every tuple, 100 per request (OpenFGA's default limit), `threads` requests at a time."""
        batches = [tuples[i : i + 100] for i in range(0, len(tuples), 100)]
        parallel(lambda batch: self.write(store, model_id, writes=batch), batches, threads)
        return len(tuples)

    def list_objects(
        self, store: str, model_id: str, *, type_: str, relation: str, user: str, consistency: str | None, timeout: float = 120
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"authorization_model_id": model_id, "type": type_, "relation": relation, "user": user}
        if consistency:
            payload["consistency"] = consistency
        started = clock()
        try:
            answer = call("POST", f"{self.url}/stores/{store}/list-objects", payload, timeout=timeout)
        except ServiceError as error:
            return {"status": error.status, "error": str(error)[:300], "elapsed_s": clock() - started}
        objects = answer.get("objects") if isinstance(answer, dict) else None
        return {
            "status": 200,
            "count": len(objects) if isinstance(objects, list) else None,
            "objects": objects if isinstance(objects, list) else [],
            "keys": sorted(answer) if isinstance(answer, dict) else None,
            "elapsed_s": clock() - started,
        }

    def streamed_list_objects(
        self, store: str, model_id: str, *, type_: str, relation: str, user: str, consistency: str | None, timeout: float = 120
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"authorization_model_id": model_id, "type": type_, "relation": relation, "user": user}
        if consistency:
            payload["consistency"] = consistency
        started = clock()
        try:
            lines = call("POST", f"{self.url}/stores/{store}/streamed-list-objects", payload, timeout=timeout, lines=True)
        except ServiceError as error:
            return {"status": error.status, "error": str(error)[:300], "elapsed_s": clock() - started}
        objects = [line["result"]["object"] for line in lines if isinstance(line.get("result"), dict) and "object" in line["result"]]
        errors = [line for line in lines if "error" in line or "unparsed" in line]
        return {
            "status": 200,
            "count": len(objects),
            "objects": objects,
            "lines": len(lines),
            "error_lines": errors[:3],
            "elapsed_s": clock() - started,
        }

    def delete_store(self, store: str) -> None:
        with contextlib.suppress(ServiceError):
            call("DELETE", f"{self.url}/stores/{store}")


class SpiceDBAdmin:
    """SpiceDB's HTTP gateway for setup and raw measurements."""

    def __init__(self, url: str, token: str) -> None:
        self.url = url.rstrip("/")
        self.token = token

    def api(self, path: str, payload: Any, *, lines: bool = False, timeout: float = 120) -> Any:
        return call("POST", f"{self.url}{path}", payload, token=self.token, lines=lines, timeout=timeout)

    def write_schema(self, schema: str) -> None:
        self.api("/v1/schema/write", {"schema": schema})

    def write(self, updates: Sequence[Mapping[str, Any]]) -> str:
        answer = self.api("/v1/relationships/write", {"updates": list(updates)})
        return str(answer["writtenAt"]["token"])

    def touch_all(self, relationships: Sequence[Mapping[str, Any]], threads: int = 4) -> int:
        """Write every relationship (OPERATION_TOUCH), 1,000 per request, `threads` at a time."""
        updates = [{"operation": "OPERATION_TOUCH", "relationship": r} for r in relationships]
        batches = [updates[i : i + 1000] for i in range(0, len(updates), 1000)]
        parallel(self.write, batches, threads)
        return len(updates)

    def lookup(
        self,
        resource_type: str,
        permission: str,
        subject: Mapping[str, Any],
        *,
        consistency: Mapping[str, Any],
        limit: int | None,
        timeout: float = 300,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "consistency": dict(consistency),
            "resourceObjectType": resource_type,
            "permission": permission,
            "subject": dict(subject),
        }
        if limit is not None:
            payload["optionalLimit"] = limit
        started = clock()
        try:
            lines = self.api("/v1/permissions/resources", payload, lines=True, timeout=timeout)
        except ServiceError as error:
            return {"status": error.status, "error": str(error)[:300], "elapsed_s": clock() - started}
        results = [line["result"] for line in lines if isinstance(line.get("result"), dict)]
        errors = [line for line in lines if "error" in line or "unparsed" in line]
        last = results[-1] if results else {}
        return {
            "status": 200,
            "count": len(results),
            "objects": [r.get("resourceObjectId") for r in results],
            "lines": len(lines),
            "error_lines": errors[:3],
            "result_keys": sorted(last) if last else [],
            "has_cursor": bool(last.get("afterResultCursor")),
            "elapsed_s": clock() - started,
        }


class ProxyProcess:
    """The fault-injection proxy (x4x7_proxy.py) in a process of its own."""

    def __init__(self, kind: str, listen_port: int, upstream: str, admin_port: int, log_path: str | Path) -> None:
        self.kind = kind
        self.listen_port = listen_port
        self.upstream = upstream
        self.admin_port = admin_port
        self.log_path = Path(log_path)
        self.process: subprocess.Popen[bytes] | None = None

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.listen_port}"

    @property
    def admin(self) -> str:
        return f"http://127.0.0.1:{self.admin_port}"

    def start(self) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        output = self.log_path.open("ab")
        self.process = subprocess.Popen(  # noqa: S603
            [
                sys.executable,
                str(PROXY_SCRIPT),
                "--kind",
                self.kind,
                "--listen",
                f"127.0.0.1:{self.listen_port}",
                "--upstream",
                self.upstream,
                "--admin",
                f"127.0.0.1:{self.admin_port}",
            ],
            stdout=output,
            stderr=subprocess.STDOUT,
        )
        wait_for(lambda: healthy(f"{self.admin}/health"), 30, what="proxy admin")

    def set(self, mode: str, delay_ms: float = 0) -> None:
        call("POST", f"{self.admin}/mode", {"mode": mode, "delay_ms": delay_ms}, timeout=30)

    def stop(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.kill()
            with contextlib.suppress(subprocess.TimeoutExpired):
                self.process.wait(10)
        self.process = None


# ---- statistics -------------------------------------------------------------------------------------


def zero_bound(n: int) -> float:
    """The one-sided 95% upper bound on a rate after zero events in n independent trials."""
    return 1.0 - 0.05 ** (1.0 / n) if n > 0 else 1.0


def _blocks(n: int, resamples: int, seed: int) -> Iterable[Any]:
    import numpy as np

    rng = np.random.default_rng(seed)
    block = max(1, min(resamples, 4_000_000 // max(n, 1)))
    done = 0
    while done < resamples:
        size = min(block, resamples - done)
        yield rng.integers(0, n, size=(size, n))
        done += size


def boot_ratio(
    numerators: Sequence[float], denominators: Sequence[float] | None = None, *, resamples: int = RESAMPLES
) -> tuple[float, float, float]:
    """sum(numerators) / sum(denominators) over clusters (one entry per cluster), with a 95% percentile
    interval from a cluster bootstrap. Without denominators, the mean of the numerators."""
    import numpy as np

    num = np.asarray(numerators, dtype=float)
    den = np.ones_like(num) if denominators is None else np.asarray(denominators, dtype=float)
    n = len(num)
    if n == 0 or den.sum() <= 0:
        return (math.nan, math.nan, math.nan)
    estimate = float(num.sum() / den.sum())
    values = []
    for idx in _blocks(n, resamples, BOOTSTRAP_SEED):
        top, bottom = num[idx].sum(axis=1), den[idx].sum(axis=1)
        keep = bottom > 0
        values.append(top[keep] / bottom[keep])
    flat = np.concatenate(values) if values else np.array([estimate])
    low, high = np.percentile(flat, [2.5, 97.5])
    return (estimate, float(low), float(high))


def boot_stat(values: Sequence[float], statistic: str = "median", *, resamples: int = RESAMPLES) -> tuple[float, float, float]:
    """A statistic ("median", "mean" or "max") of independent values, with a bootstrap interval."""
    import numpy as np

    data = np.asarray(values, dtype=float)
    n = len(data)
    if n == 0:
        return (math.nan, math.nan, math.nan)
    function = {"median": np.median, "mean": np.mean, "max": np.max}[statistic]
    estimate = float(function(data))
    values_out = [function(data[idx], axis=1) for idx in _blocks(n, resamples, BOOTSTRAP_SEED)]
    flat = np.concatenate(values_out)
    low, high = np.percentile(flat, [2.5, 97.5])
    return (estimate, float(low), float(high))


def quantile(values: Sequence[float], q: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    below = math.floor(position)
    above = min(below + 1, len(ordered) - 1)
    return ordered[below] + (ordered[above] - ordered[below]) * (position - below)


def fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        if math.isnan(value):
            return "n/a"
        if value != 0 and abs(value) < 10 ** (-digits):
            return f"{value:.1e}"
        return f"{value:.{digits}f}"
    return str(value)


def fmt_ci(triple: tuple[float, float, float], digits: int = 3) -> str:
    estimate, low, high = triple
    return f"{fmt(estimate, digits)} [{fmt(low, digits)}, {fmt(high, digits)}]"


def md_table(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def write_csv(path: str | Path, headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> None:
    import csv

    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


def publish_summary(markdown: str) -> None:
    """Append to the job summary when running in GitHub Actions."""
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with Path(target).open("a", encoding="utf-8") as handle:
            handle.write(markdown + "\n")


class Verdicts:
    """Each pre-registered hypothesis's verdict, with the numbers behind it."""

    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, name: str, verdict: str, detail: str) -> None:
        assert verdict in ("confirmed", "falsified", "inconclusive", "exploratory"), verdict
        self.rows.append((name, verdict, detail))
        print(f"VERDICT {name}: {verdict.upper()} ({detail})", flush=True)

    def markdown(self) -> str:
        return md_table(["Hypothesis", "Verdict", "Numbers"], [(n, v.upper(), d) for n, v, d in self.rows])

    def annotate(self, title: str) -> None:
        text = "\n".join(f"{n}: {v.upper()}: {d}" for n, v, d in self.rows)
        # Several notices if the verdicts do not fit in one.
        part, size, number = [], 0, 1
        for line in text.splitlines():
            if size + len(line) > 3500 and part:
                annotate("notice", f"{title} verdicts {number}", "\n".join(part))
                part, size, number = [], 0, number + 1
            part.append(line)
            size += len(line) + 1
        if part:
            annotate("notice", f"{title} verdicts {number}", "\n".join(part))
