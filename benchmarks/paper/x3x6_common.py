"""What the X3 and X6 scripts share: logging, records, run information, the data files of the data
job, and one adapter per store that builds an index from documents and vectors and hands back
wardowl backends for it.

Nothing here imports wardowl or a store client at module level, so the data job, which installs only
the embedding stack, can import it. See PREREG_X3_X6.md for the design and README_X3_X6.md for how
to run it.
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.parse
import uuid
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np

DIM = 384
SCHEMA = 1
SEED_BASE = 20261029  # every seeded draw of X3 and X6 starts from this and the seed
K = 10
MAX_CANDIDATES = 1000  # wardowl's default cap on post-filter candidates
TOKEN = re.compile(r"\w+")
RUN_ID = os.environ.get("GITHUB_RUN_ID", "local")
SECRET_META = {"allowed_users": ["owner-secret"], "allowed_groups": ["g-secret"]}


def env(name: str, default: str) -> str:
    return os.environ.get(name) or default


# ---- logging and records -------------------------------------------------------------------------


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def annotate(level: str, title: str, message: str, limit: int = 3500, chunks: int = 3) -> None:
    """A GitHub Actions annotation (error, warning or notice), readable through the public API.

    A long message is split into at most `chunks` annotations of `limit` characters: GitHub keeps
    only 10 annotations of each level per step."""
    title = title.replace("%", "%25").replace("\r", " ").replace("\n", " ").replace(":", "%3A").replace(",", "%2C")
    parts = [message[i : i + limit] for i in range(0, max(len(message), 1), limit)] or [""]
    for number, chunk in enumerate(parts[:chunks], 1):
        text = chunk.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        suffix = f" ({number}/{len(parts)})" if len(parts) > 1 else ""
        print(f"::{level} title={title}{suffix}::{text}", flush=True)


def short(error: BaseException, limit: int = 600) -> str:
    text = f"{type(error).__name__}: {error}"
    return text if len(text) <= limit else text[:limit] + "..."


class Records:
    """Appends JSON lines to one file, each with the fields of `base`."""

    def __init__(self, path: Path, base: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.base = dict(base)
        self.handle = path.open("a", encoding="utf-8")

    def write(self, record: Mapping[str, Any]) -> None:
        line = json.dumps({"schema": SCHEMA, **self.base, **record}, default=_jsonable)
        self.handle.write(line + "\n")
        self.handle.flush()

    def close(self) -> None:
        self.handle.close()


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (set, frozenset)):
        return sorted(value)
    return str(value)


def read_records(paths: Sequence[Path]) -> tuple[list[dict[str, Any]], int]:
    """Every JSON line of these files, and how many lines could not be read."""
    records: list[dict[str, Any]] = []
    unreadable = 0
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except ValueError:
                    unreadable += 1
    return records, unreadable


# ---- run information -----------------------------------------------------------------------------


def versions(*names: str) -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for name in names:
        try:
            found[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            found[name] = None
    return found


def _command(*command: str) -> str | None:
    try:
        done = subprocess.run(list(command), capture_output=True, text=True, timeout=30, check=False)  # noqa: S603
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def image(container: str | None) -> dict[str, Any] | None:
    """The image a container runs, with its id and registry digests."""
    if not container:
        return None
    found = _command("docker", "inspect", "--format", "{{.Config.Image}}|{{.Image}}", container)
    if not found or "|" not in found:
        return None
    name, image_id = found.split("|", 1)
    digests = _command("docker", "image", "inspect", "--format", "{{json .RepoDigests}}", image_id)
    try:
        parsed = json.loads(digests) if digests else None
    except ValueError:
        parsed = digests
    return {"container": container, "image": name, "image_id": image_id, "digests": parsed}


def host() -> dict[str, Any]:
    memory = None
    with contextlib.suppress(OSError, ValueError, IndexError):
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                memory = round(int(line.split()[1]) / 2**20, 1)
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cpus": os.cpu_count(),
        "memory_gib": memory,
        "runner": os.environ.get("RUNNER_NAME"),
        "image_os": os.environ.get("ImageOS"),
        "image_version": os.environ.get("ImageVersion"),
        "commit": os.environ.get("GITHUB_SHA"),
        "run_id": RUN_ID,
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
    }


def deadline_for(budget_minutes: float, group_deadline: float, remaining: int) -> float:
    """When a target must stop starting seeds: its own budget, or a fair share of what is left of the
    job's time, whichever comes first. Targets that finish early leave their time to the rest."""
    now = time.time()
    deadline = now + budget_minutes * 60
    if group_deadline:
        share = (group_deadline - now) / max(1, remaining)
        deadline = min(deadline, now + max(share, 60.0))
    return deadline


def seed_list(count: int, chosen: str) -> list[int]:
    """The seeds a job runs: those of `chosen` ("0,1,2" or "3-4"), or 0 to count - 1 when it is empty,
    so that a slow store's seeds can be shared between jobs without leaving one out."""
    if not chosen.strip():
        return list(range(count))
    seeds: list[int] = []
    for part in chosen.split(","):
        part = part.strip()
        if "-" in part:
            first, last = part.split("-", 1)
            seeds += range(int(first), int(last) + 1)
        elif part:
            seeds.append(int(part))
    return sorted(set(seeds))


def connect(target: Target, timeout: float = 600.0) -> int:
    """Set the target up, trying again while its server boots. Returns the number of attempts."""
    started = time.monotonic()
    attempt = 0
    while True:
        attempt += 1
        try:
            target.setup()
            return attempt
        except Exception as error:
            if time.monotonic() - started > timeout:
                raise
            log(f"  setup attempt {attempt}: {short(error, 300)}")
            with contextlib.suppress(Exception):
                target.close()
            time.sleep(10)


# ---- data of the data job ------------------------------------------------------------------------


class Texts:
    """Ids, texts and vectors of one file pair (<name>.jsonl, <name>.npy) written by x6_data.py."""

    def __init__(self, folder: Path, name: str) -> None:
        self.ids: list[str] = []
        self.texts: list[str] = []
        with (folder / f"{name}.jsonl").open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                self.ids.append(row["id"])
                self.texts.append(row["text"])
        self.vectors = np.load(folder / f"{name}.npy")
        if self.vectors.shape != (len(self.ids), DIM):
            raise ValueError(f"{name}: {self.vectors.shape} vectors for {len(self.ids)} texts of {DIM} dimensions")


def data_ready(folder: Path) -> bool:
    return (folder / "manifest.json").is_file() and (folder / "fiqa_corpus.npy").is_file()


def count_tokens(text: str) -> int:
    return len(TOKEN.findall(text))


def far_text(texts: Sequence[str], start: int, n_tokens: int) -> str:
    """`n_tokens` word tokens taken from `texts[start]` on (the following passages when it is shorter),
    joined by spaces: a far chunk exactly as long, in word tokens, as the near passage it replaces."""
    if n_tokens <= 0 or not texts:
        return ""
    words: list[str] = []
    for step in range(len(texts)):
        words.extend(TOKEN.findall(texts[(start + step) % len(texts)]))
        if len(words) >= n_tokens:
            break
    return " ".join(words[:n_tokens])


def plan_path(folder: Path, seed: int) -> Path:
    return folder / f"plan_seed{seed}.json"


# ---- store adapters --------------------------------------------------------------------------------


class Built:
    """One index of a store and the wardowl backends that search it."""

    def __init__(self, name: str, vector: Any, *, exact: Any = None, keyword: Any = None, **state: Any) -> None:
        self.name = name
        self.vector = vector
        self.exact = exact
        self.keyword = keyword
        self.state = state
        self.info: dict[str, Any] = {}


class Target:
    """A store. `build` writes documents with their vectors into a new index and returns a `Built`;
    `drop` removes it. `keyword` asks for the keyword (BM25 or full-text) index as well."""

    name = "store"
    container: str | None = None
    clients: tuple[str, ...] = ()
    exact_index = False  # True when the vector search is exhaustive (FAISS flat, LanceDB without an index)

    def setup(self) -> None:
        """Connect; raises when the store cannot be reached."""

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        raise NotImplementedError

    def drop(self, built: Built) -> None:
        """Remove the index."""

    def close(self) -> None:
        """Remove what the target made and disconnect. Safe to call more than once."""

    def reported(self) -> dict[str, Any]:
        """The version the store reports about itself."""
        return {}

    def translate(self, f: Any) -> Any:
        """The store's own translation of a wardowl filter (X3). None for in-process stores."""
        return None


class PgVector(Target):
    name = "pgvector"
    container = "postgres"
    clients = ("psycopg", "psycopg-binary", "psycopg-pool")

    def __init__(self) -> None:
        self.url = env("WARDOWL_TEST_DATABASE_URL", "postgresql://test:test@localhost:5432/test")
        self.pool: Any = None  # builds: no statement timeout
        self.search_pool: Any = None  # searches: a 120 s statement timeout, as every X3 retrieval has
        self.tables: list[str] = []

    def setup(self) -> None:
        import psycopg_pool

        self.pool = psycopg_pool.ConnectionPool(self.url, min_size=1, max_size=2, open=True, timeout=120)
        self.search_pool = psycopg_pool.ConnectionPool(
            self.url, min_size=1, max_size=2, open=True, timeout=120, kwargs={"options": "-c statement_timeout=120000"}
        )
        with self.pool.connection() as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from psycopg import sql

        from wardowl.backends.pgvector import PgVectorBackend, create_schema

        table = base
        self.tables.append(table)
        create_schema(self.pool, DIM, table=table, hnsw=False)
        PgVectorBackend(self.pool, table=table).add(docs, vectors)
        # The indexes are built once the rows are in, as a bulk load would build them.
        create_schema(self.pool, DIM, table=table, hnsw=True, text_search="english" if keyword else None)
        with self.pool.connection() as conn:
            conn.execute(sql.SQL("ANALYZE {}").format(sql.Identifier(table)))
        vector = PgVectorBackend(self.search_pool, table=table)
        exact = _exact_pgvector()(self.search_pool, table=table)
        words = None
        if keyword:
            words = PgVectorBackend(self.search_pool, table=table, mode="keyword", text_search="english")
        return Built(table, vector, exact=exact, keyword=words)

    def drop(self, built: Built) -> None:
        from psycopg import sql

        with contextlib.suppress(Exception), self.pool.connection() as conn:
            conn.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(built.name)))
        if built.name in self.tables:
            self.tables.remove(built.name)

    def close(self) -> None:
        if self.pool is not None:
            for table in list(self.tables):
                self.drop(Built(table, None))
            self.pool.close()
            self.pool = None
        if self.search_pool is not None:
            self.search_pool.close()
            self.search_pool = None

    def reported(self) -> dict[str, Any]:
        with self.pool.connection() as conn:
            server = conn.execute("SELECT version()").fetchone()
            vector = conn.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'").fetchone()
            settings = conn.execute(
                "SELECT name, setting FROM pg_settings WHERE name IN ('shared_buffers', 'maintenance_work_mem',"
                " 'work_mem', 'max_parallel_maintenance_workers', 'hnsw.ef_search', 'hnsw.max_scan_tuples',"
                " 'hnsw.scan_mem_multiplier', 'hnsw.iterative_scan')"
            ).fetchall()
        return {
            "postgresql": server[0] if server else None,
            "pgvector": vector[0] if vector else None,
            "settings": {name: value for name, value in settings},
        }

    def translate(self, f: Any) -> Any:
        from wardowl.backends.pgvector import filter_to_sql

        return filter_to_sql(f)

    def explain(self, backend: Any, query: Any, k: int, f: Any) -> dict[str, Any]:
        """EXPLAIN ANALYZE of the statement `backend.search` would run, in the same transaction
        settings: the plan's nodes and the rows each scanned and removed by the filter."""
        from psycopg import sql

        from wardowl.types import Query

        q = Query.of(query)
        statement, params = backend._statement(q, backend._query_vector(q), k, f)
        with backend.pool.connection() as conn, conn.transaction():
            for setting in backend._settings():
                conn.execute(setting)
            row = conn.execute(sql.SQL("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ") + statement, params).fetchone()
        document = row[0]
        if isinstance(document, str):
            document = json.loads(document)
        top = document[0]
        return {"nodes": _plan_nodes(top["Plan"]), "execution_ms": top.get("Execution Time")}


def _plan_nodes(node: Mapping[str, Any], depth: int = 0) -> list[dict[str, Any]]:
    keep = (
        "Node Type",
        "Index Name",
        "Actual Rows",
        "Actual Loops",
        "Rows Removed by Filter",
        "Rows Removed by Index Recheck",
    )
    found = [{"depth": depth, **{key: node[key] for key in keep if key in node}}]
    for child in node.get("Plans", []) or []:
        found += _plan_nodes(child, depth + 1)
    return found


def _exact_pgvector() -> Any:
    """PgVectorBackend with index scans off: the HNSW index is not used, so the search scores every
    row the filter admits (through the GIN index or a sequential scan) and is exact."""
    from psycopg import sql

    from wardowl.backends.pgvector import PgVectorBackend

    class ExactPgVector(PgVectorBackend):
        exact_search = True

        def _settings(self) -> list[Any]:
            return [*super()._settings(), sql.SQL("SET LOCAL enable_indexscan = off")]

    return ExactPgVector


class Qdrant(Target):
    name = "qdrant"
    container = "qdrant"
    clients = ("qdrant-client",)

    def __init__(self) -> None:
        self.url = env("WARDOWL_TEST_QDRANT_URL", "http://127.0.0.1:6333")
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import qdrant_client

        self.client = qdrant_client.QdrantClient(url=self.url, timeout=180)
        self.client.get_collections()

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from qdrant_client import models

        from wardowl.backends.qdrant import QdrantBackend, create_collection

        self.made.append(base)
        create_collection(self.client, base, DIM, text_search=keyword)
        # Every segment HNSW-indexed, as in a production collection (a stated deviation from the
        # default indexing threshold, which leaves small segments unindexed). 10 KB is a few vectors.
        self.client.update_collection(base, optimizers_config=models.OptimizersConfigDiff(indexing_threshold=10))
        QdrantBackend(self.client, base, text_search=keyword).add(docs, vectors)
        info = self._wait(base)
        vector = QdrantBackend(self.client, base)
        exact = QdrantBackend(self.client, base, search_params=models.SearchParams(exact=True))
        exact.exact_search = True
        words = QdrantBackend(self.client, base, mode="keyword") if keyword else None
        built = Built(base, vector, exact=exact, keyword=words)
        built.info = info
        return built

    def _wait(self, name: str, timeout: float = 1800.0) -> dict[str, Any]:
        """Wait until the optimizer is done: the collection green, and either its vectors indexed on two
        polls in a row, or its indexed count unchanged for a minute (a last appendable segment can stay
        below the threshold). The optimizer may not have started when the last upsert returns, and a
        collection with sparse vectors counts those as indexed at once. The indexed count is recorded."""
        started = time.monotonic()
        time.sleep(5)
        settled = 0
        stable_since = time.monotonic()
        last = -1
        while True:
            info = self.client.get_collection(name)
            points = info.points_count or 0
            indexed = info.indexed_vectors_count or 0
            status = str(getattr(info.status, "value", info.status)).lower()
            optimizer = str(getattr(info.optimizer_status, "value", info.optimizer_status)).lower()
            state = {
                "points": points,
                "indexed_vectors": indexed,
                "segments": info.segments_count,
                "status": status,
                "optimizer": optimizer,
                "wait_s": round(time.monotonic() - started, 1),
            }
            green = status == "green"
            if indexed != last or not green:
                stable_since, last = time.monotonic(), indexed
            settled = settled + 1 if green and indexed >= 0.99 * points else 0
            if settled >= 2:
                return state
            if green and time.monotonic() - stable_since >= 60:
                return {**state, "stable": True}
            if time.monotonic() - started > timeout:
                log(f"  qdrant {name}: not settled after {timeout:.0f} s: {state}")
                return {**state, "timed_out": True}
            time.sleep(3)

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.client.delete_collection(built.name)
        if built.name in self.made:
            self.made.remove(built.name)

    def close(self) -> None:
        if self.client is not None:
            for name in list(self.made):
                self.drop(Built(name, None))
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        import urllib.request

        with urllib.request.urlopen(f"{self.url}/", timeout=30) as response:  # noqa: S310
            answer = json.loads(response.read())
        return {"qdrant": answer.get("version") if isinstance(answer, dict) else None}

    def translate(self, f: Any) -> Any:
        from wardowl.backends.qdrant import filter_to_qdrant

        return filter_to_qdrant(f)


class SearchEngine(Target):
    """Elasticsearch or OpenSearch: one index per build, one shard, no replica."""

    def __init__(self, kind: str) -> None:
        self.name = kind
        self.container = kind
        self.clients = ("elasticsearch",) if kind == "elasticsearch" else ("opensearch-py",)
        default = "http://127.0.0.1:9200" if kind == "elasticsearch" else "http://127.0.0.1:9201"
        self.url = env(f"WARDOWL_TEST_{kind.upper()}_URL", default)
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        if self.name == "elasticsearch":
            import elasticsearch

            self.client = elasticsearch.Elasticsearch(self.url, request_timeout=180)
        else:
            import opensearchpy

            self.client = opensearchpy.OpenSearch(hosts=[self.url], timeout=180)
        self.client.info()

    def _module(self) -> Any:
        import importlib

        return importlib.import_module(f"wardowl.backends.{self.name}")

    def _backend(self, index: str, **options: Any) -> Any:
        module = self._module()
        kind = module.ElasticsearchBackend if self.name == "elasticsearch" else module.OpenSearchBackend
        return kind(self.client, index, None, **options)

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        module = self._module()
        self.made.append(base)
        module.create_index(self.client, base, DIM, settings={"number_of_shards": 1, "number_of_replicas": 0})
        self._backend(base, refresh=False).add(docs, vectors)
        self.client.indices.refresh(index=base)
        exact = _exact_elasticsearch()(self.client, base, None) if self.name == "elasticsearch" else None
        words = self._backend(base, mode="keyword") if keyword else None
        built = Built(base, self._backend(base), exact=exact, keyword=words)
        built.info = self._describe(base)
        return built

    def _describe(self, index: str) -> dict[str, Any]:
        info: dict[str, Any] = {}
        with contextlib.suppress(Exception):
            mapping = _body(self.client.indices.get_mapping(index=index))
            info["vector_mapping"] = mapping[index]["mappings"]["properties"]["embedding"]
        with contextlib.suppress(Exception):
            segments = _body(self.client.indices.segments(index=index))
            shards = segments["indices"][index]["shards"]
            info["segments"] = sum(len(copy.get("segments", {})) for copies in shards.values() for copy in copies)
        with contextlib.suppress(Exception):
            info["docs"] = int(_body(self.client.count(index=index))["count"])
        return info

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.client.indices.delete(index=built.name)
        if built.name in self.made:
            self.made.remove(built.name)

    def close(self) -> None:
        if self.client is not None:
            for name in list(self.made):
                self.drop(Built(name, None))
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        version = _body(self.client.info()).get("version", {})
        keep = ("number", "distribution", "lucene_version", "build_hash")
        return {key: version.get(key) for key in keep if key in version}

    def translate(self, f: Any) -> Any:
        return self._module().filter_to_query(f)


def _body(response: Any) -> Any:
    """The JSON body of a search-engine client's response (elasticsearch-py wraps it, opensearch-py does not)."""
    return getattr(response, "body", response)


def _exact_elasticsearch() -> Any:
    """ElasticsearchBackend searched exhaustively: `script_score` cosine over every chunk the filter
    admits, instead of the approximate kNN search. The score is the cosine similarity plus 1."""
    from wardowl.backends.elasticsearch import ElasticsearchBackend

    class ExactElasticsearch(ElasticsearchBackend):
        exact_search = True

        def _search_request(self, vector: list[float], k: int, query: dict[str, Any] | None) -> dict[str, Any]:
            inner: dict[str, Any] = {"bool": {"filter": [query]}} if query is not None else {"match_all": {}}
            script = {"source": f"cosineSimilarity(params.q, '{self.vector_field}') + 1.0", "params": {"q": vector}}
            return {
                "query": {"script_score": {"query": inner, "script": script}},
                "size": k,
                "source_excludes": [self.vector_field],
            }

    return ExactElasticsearch


class Redis(Target):
    name = "redis"
    container = "redis"
    clients = ("redis",)

    def __init__(self) -> None:
        self.url = env("WARDOWL_TEST_REDIS_URL", "redis://127.0.0.1:6379/0")
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import redis

        # RESP3, so that a query the server's timeout cut short arrives with its warning, which
        # wardowl turns into an error instead of passing partial results off as complete.
        self.client = redis.Redis.from_url(self.url, protocol=3, socket_timeout=180)
        self.client.ping()

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.redis import RedisBackend, create_index

        self.made.append(base)
        create_index(self.client, base, DIM, prefix=f"{base}:")
        backend = RedisBackend(self.client, base, prefix=f"{base}:")
        backend.add(docs, vectors)
        built = Built(base, backend)
        with contextlib.suppress(Exception):
            raw = self.client.execute_command("FT.INFO", base)
            if isinstance(raw, Mapping):
                built.info = {"num_docs": _text(raw.get("num_docs", raw.get(b"num_docs")))}
        return built

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.client.execute_command("FT.DROPINDEX", built.name, "DD")
        if built.name in self.made:
            self.made.remove(built.name)

    def close(self) -> None:
        if self.client is not None:
            for name in list(self.made):
                self.drop(Built(name, None))
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        info = self.client.info("server")
        found: dict[str, Any] = {"redis": info.get("redis_version")}
        with contextlib.suppress(Exception):
            timeout = self.client.execute_command("CONFIG", "GET", "search-timeout")
            found["search-timeout"] = _text_tree(timeout)
        return found

    def translate(self, f: Any) -> Any:
        from wardowl.backends.redis import filter_to_query

        return filter_to_query(f)


def _text(value: Any) -> Any:
    return value.decode("utf-8", "replace") if isinstance(value, bytes) else value


def _text_tree(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {_text(k): _text_tree(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_text_tree(v) for v in value]
    return _text(value)


class Cassandra(Target):
    name = "cassandra"
    container = "cassandra"
    clients = ("cassandra-driver",)
    keyspace = "wardowl_x3x6"

    def __init__(self) -> None:
        self.cluster: Any = None
        self.session: Any = None
        self.tables: list[str] = []

    def setup(self) -> None:
        from cassandra.cluster import Cluster

        self.cluster = Cluster([env("WARDOWL_TEST_CASSANDRA_HOST", "127.0.0.1")])
        self.session = self.cluster.connect()
        self.session.default_timeout = 180
        self.session.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {self.keyspace} "
            "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
        )

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.cassandra import CassandraBackend, create_table

        self.tables.append(base)
        create_table(self.session, self.keyspace, base, DIM)
        backend = CassandraBackend(self.session, self.keyspace, base, None)
        backend.add(docs, vectors)
        return Built(base, backend)

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.session.execute(f"DROP TABLE IF EXISTS {self.keyspace}.{built.name}")
        if built.name in self.tables:
            self.tables.remove(built.name)

    def close(self) -> None:
        if self.session is not None:
            for name in list(self.tables):
                self.drop(Built(name, None))
        if self.cluster is not None:
            self.cluster.shutdown()
            self.cluster = self.session = None

    def reported(self) -> dict[str, Any]:
        row = self.session.execute("SELECT release_version FROM system.local").one()
        return {"cassandra": row.release_version if row else None}

    def translate(self, f: Any) -> Any:
        from wardowl.backends.cassandra import TooManyQueries, filter_to_conjunctions, required_terms

        try:
            return {"conjunctions": len(filter_to_conjunctions(f, 256))}
        except TooManyQueries:
            # The backend's documented fallback: one ANN query on the terms every match must have.
            return {"fallback": True, "required_terms": len(required_terms(f))}


class Vespa(Target):
    name = "vespa"
    container = "vespa"
    clients = ("httpx",)

    def __init__(self) -> None:
        self.url = env("WARDOWL_TEST_VESPA_URL", "http://127.0.0.1:8090")
        self.client: Any = None
        self.stored: list[str] = []

    def setup(self) -> None:
        import httpx

        self.client = httpx.Client(timeout=180)
        if self.client.get(f"{self.url}/").status_code >= 500:
            raise RuntimeError("Vespa's container answers with a server error")

    def _backend(self) -> Any:
        from wardowl.backends.vespa import VespaBackend

        return VespaBackend(self.url, None, client=self.client, timeout=120.0, concurrency=16)

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        # One Vespa application holds one document type, so a build is the set of documents stored.
        backend = self._backend()
        self.stored = [d.id for d in docs]
        backend.add(docs, vectors)
        return Built(base, backend, ids=list(self.stored))

    def drop(self, built: Built) -> None:
        ids = built.state.get("ids") or []
        if ids:
            with contextlib.suppress(Exception):
                self._backend().delete(ids)
        self.stored = []

    def close(self) -> None:
        if self.client is not None:
            if self.stored:
                with contextlib.suppress(Exception):
                    self._backend().delete(self.stored)
            self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        for path in ("/state/v1/version", "/ApplicationStatus"):
            with contextlib.suppress(Exception):
                answer = self.client.get(f"{self.url}{path}").json()
                version = _find(answer, "version")
                if version:
                    return {"vespa": version}
        return {}

    def translate(self, f: Any) -> Any:
        from wardowl.backends.vespa import filter_to_yql

        return filter_to_yql(f)


def _find(data: Any, key: str) -> Any:
    if isinstance(data, Mapping):
        if key in data and isinstance(data[key], (str, int, float)):
            return data[key]
        for value in data.values():
            found = _find(value, key)
            if found is not None:
                return found
    elif isinstance(data, list):
        for value in data:
            found = _find(value, key)
            if found is not None:
                return found
    return None


class Milvus(Target):
    name = "milvus"
    container = "milvus"
    clients = ("pymilvus",)

    def __init__(self) -> None:
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import pymilvus

        self.client = pymilvus.MilvusClient(uri=env("WARDOWL_TEST_MILVUS_URL", "http://127.0.0.1:19530"), timeout=180)
        self.client.list_collections()

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.milvus import MilvusBackend, create_collection

        self.made.append(base)
        create_collection(self.client, base, DIM)
        backend = MilvusBackend(self.client, base)
        backend.add(docs, vectors)
        built = Built(base, backend)
        built.info = self._wait(base)
        return built

    def _wait(self, name: str, timeout: float = 1200.0) -> dict[str, Any]:
        """Flush, then wait until the vector index covers every row (best effort: recorded either way)."""
        started = time.monotonic()
        state: dict[str, Any] = {}
        with contextlib.suppress(Exception):
            self.client.flush(name)
        while time.monotonic() - started < timeout:
            try:
                described = self.client.describe_index(name, "embedding")
            except Exception as error:
                return {"index_state": f"not described: {short(error, 200)}"}
            state = {key: described.get(key) for key in ("indexed_rows", "total_rows", "pending_index_rows", "state")}
            pending = described.get("pending_index_rows")
            indexed, total = described.get("indexed_rows"), described.get("total_rows")
            if pending == 0 and indexed is not None and total is not None and indexed >= total:
                break
            time.sleep(3)
        return {**state, "wait_s": round(time.monotonic() - started, 1)}

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.client.drop_collection(built.name)
        if built.name in self.made:
            self.made.remove(built.name)

    def close(self) -> None:
        if self.client is not None:
            for name in list(self.made):
                self.drop(Built(name, None))
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        return {"milvus": self.client.get_server_version()}

    def translate(self, f: Any) -> Any:
        from wardowl.backends.milvus import filter_to_expression

        return filter_to_expression(f)


class Weaviate(Target):
    name = "weaviate"
    container = "weaviate"
    clients = ("weaviate-client",)

    def __init__(self) -> None:
        self.url = env("WARDOWL_TEST_WEAVIATE_URL", "http://127.0.0.1:8079")
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import weaviate
        from weaviate.classes.init import AdditionalConfig, Timeout

        parts = urllib.parse.urlsplit(self.url)
        grpc_port = int(env("WARDOWL_TEST_WEAVIATE_GRPC_PORT", "50051"))
        self.client = weaviate.connect_to_local(
            host=parts.hostname or "127.0.0.1",
            port=parts.port or 8080,
            grpc_port=grpc_port,
            additional_config=AdditionalConfig(timeout=Timeout(init=60, query=180, insert=180)),
        )

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.weaviate import WeaviateBackend, create_collection

        name = "W" + base  # collection names start with an upper-case letter
        self.made.append(name)
        create_collection(self.client, name)
        backend = WeaviateBackend(self.client, name)
        backend.add(docs, vectors)
        return Built(name, backend)

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.client.collections.delete(built.name)
        if built.name in self.made:
            self.made.remove(built.name)

    def close(self) -> None:
        if self.client is not None:
            for name in list(self.made):
                self.drop(Built(name, None))
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        import urllib.request

        with urllib.request.urlopen(f"{self.url}/v1/meta", timeout=30) as response:  # noqa: S310
            answer = json.loads(response.read())
        return {"weaviate": answer.get("version") if isinstance(answer, dict) else None}

    def translate(self, f: Any) -> Any:
        from wardowl.backends.weaviate import filter_to_weaviate

        return filter_to_weaviate(f)


class MongoDB(Target):
    name = "mongodb"
    container = "mongodb"
    clients = ("pymongo",)

    def __init__(self) -> None:
        self.client: Any = None
        self.made: list[Any] = []

    def setup(self) -> None:
        import pymongo

        url = env("WARDOWL_TEST_MONGODB_URL", "mongodb://127.0.0.1:27017/?directConnection=true")
        self.client = pymongo.MongoClient(url, serverSelectionTimeoutMS=10_000, socketTimeoutMS=180_000)
        self.client.admin.command("ping")

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.mongodb import MongoDBBackend, create_search_index

        collection = self.client["wardowl_x3x6"][base]
        self.made.append(collection)
        create_search_index(collection, DIM, timeout=900.0)
        backend = MongoDBBackend(collection, None, wait_timeout=900.0)
        backend.add(docs, vectors)
        return Built(base, backend, collection=collection)

    def drop(self, built: Built) -> None:
        collection = built.state.get("collection")
        if collection is not None:
            with contextlib.suppress(Exception):
                collection.drop()
            if collection in self.made:
                self.made.remove(collection)

    def close(self) -> None:
        for collection in list(self.made):
            with contextlib.suppress(Exception):
                collection.drop()
        self.made = []
        if self.client is not None:
            self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        return {"mongodb": self.client.server_info().get("version")}

    def translate(self, f: Any) -> Any:
        from wardowl.backends.mongodb import filter_to_mongo

        return filter_to_mongo(f)


class Chroma(Target):
    name = "chroma"
    clients = ("chromadb",)

    def __init__(self) -> None:
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import chromadb

        self.client = chromadb.EphemeralClient()

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.chroma import ChromaBackend

        self.made.append(base)
        collection = self.client.create_collection(base, embedding_function=None)
        backend = ChromaBackend(collection)
        backend.add(docs, vectors)
        return Built(base, backend)

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.client.delete_collection(built.name)
        if built.name in self.made:
            self.made.remove(built.name)

    def close(self) -> None:
        if self.client is not None:
            for name in list(self.made):
                self.drop(Built(name, None))
            self.client = None

    def translate(self, f: Any) -> Any:
        from wardowl.backends.chroma import filter_to_where

        return filter_to_where(f)


class LanceDB(Target):
    name = "lancedb"
    clients = ("lancedb", "pylance", "pyarrow")
    exact_index = True  # no ANN index is created: LanceDB compares the query with every row

    def __init__(self) -> None:
        self.directory = ""
        self.db: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import lancedb

        self.directory = tempfile.mkdtemp(prefix="wo-x3x6-lancedb-", dir=os.environ.get("RUNNER_TEMP") or None)
        self.db = lancedb.connect(self.directory)

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.lancedb import LanceDBBackend, create_indexes, create_table

        self.made.append(base)
        table = create_table(self.db, base, DIM)
        backend = LanceDBBackend(table)
        backend.add(docs, vectors)
        create_indexes(table)
        return Built(base, backend)

    def drop(self, built: Built) -> None:
        with contextlib.suppress(Exception):
            self.db.drop_table(built.name)
        if built.name in self.made:
            self.made.remove(built.name)

    def close(self) -> None:
        if self.db is not None:
            for name in list(self.made):
                self.drop(Built(name, None))
            self.db = None
        if self.directory:
            shutil.rmtree(self.directory, ignore_errors=True)
            self.directory = ""

    def translate(self, f: Any) -> Any:
        from wardowl.backends.lancedb import filter_to_sql

        return filter_to_sql(f)


class Faiss(Target):
    name = "faiss"
    clients = ("faiss-cpu", "numpy")
    exact_index = True

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl.backends.faiss import FaissBackend

        backend = FaissBackend(None, DIM)
        backend.add(docs, vectors)
        # The flat index is exact: the vector backend is its own exact search.
        return Built(base, backend, exact=backend)


class Memory(Target):
    """wardowl's InMemoryBackend, the reference semantics. It ranks by keyword overlap, not vectors."""

    name = "memory"
    clients = ()
    exact_index = True

    def build(self, base: str, docs: Sequence[Any], vectors: np.ndarray, *, keyword: bool = False) -> Built:
        from wardowl import InMemoryBackend

        backend = InMemoryBackend(docs)
        return Built(base, backend, exact=backend)


def make_target(name: str) -> Target:
    factories: dict[str, Any] = {
        "pgvector": PgVector,
        "qdrant": Qdrant,
        "elasticsearch": lambda: SearchEngine("elasticsearch"),
        "opensearch": lambda: SearchEngine("opensearch"),
        "redis": Redis,
        "cassandra": Cassandra,
        "vespa": Vespa,
        "milvus": Milvus,
        "weaviate": Weaviate,
        "mongodb": MongoDB,
        "chroma": Chroma,
        "lancedb": LanceDB,
        "faiss": Faiss,
        "memory": Memory,
    }
    if name not in factories:
        raise SystemExit(f"unknown store {name!r}; known: {', '.join(sorted(factories))}")
    target: Target = factories[name]()
    return target


def target_versions(target: Target, *, reachable: bool) -> dict[str, Any]:
    found: dict[str, Any] = {
        "client": versions("wardowl", "numpy", *target.clients),
        "image": image(target.container),
        "reported": None,
    }
    if reachable:
        try:
            found["reported"] = target.reported()
        except Exception as error:
            found["reported"] = {"error": short(error, 300)}
    return found


def unique_base(prefix: str) -> str:
    """A lowercase name, letters and digits only, unique to this run: valid in every store."""
    return f"{prefix}{uuid.uuid4().hex[:8]}"


def size_of(value: Any) -> int | None:
    """The size, in characters, of a translated filter."""
    try:
        if hasattr(value, "model_dump_json"):
            return len(value.model_dump_json())
        return len(json.dumps(value, default=str))
    except Exception:
        try:
            return len(str(value))
        except Exception:
            return None


# ---- statistics shared by the stats scripts --------------------------------------------------------


def rng_for(seed: int, *parts: Any) -> np.random.Generator:
    """A generator seeded by the run's seed and what is being estimated, so every interval is
    reproducible on its own, whatever else is computed."""
    import zlib

    return np.random.default_rng([seed, zlib.crc32("/".join(map(str, parts)).encode())])


def cluster_weights(clusters: np.ndarray, resamples: int, rng: np.random.Generator) -> Iterator[np.ndarray]:
    """Blocks of bootstrap weights per item: whole clusters drawn with replacement."""
    _, inverse = np.unique(clusters, return_inverse=True)
    count = int(inverse.max()) + 1 if len(inverse) else 0
    done = 0
    while done < resamples:
        block = min(1000, resamples - done)
        drawn = rng.multinomial(count, np.full(count, 1.0 / count), size=block).astype(float)
        yield drawn[:, inverse]
        done += block


def percentile_interval(values: np.ndarray) -> tuple[float, float]:
    values = values[np.isfinite(values)]
    if not len(values):
        return math.nan, math.nan
    low, high = np.percentile(values, [2.5, 97.5])
    return float(low), float(high)


def markdown_table(header: Sequence[str], rows: Sequence[Sequence[Any]]) -> list[str]:
    def cell(value: Any) -> str:
        if value is None:
            return "n/a"
        if isinstance(value, float):
            if math.isnan(value):
                return "n/a"
            if math.isinf(value):
                return "inf" if value > 0 else "-inf"
            return f"{value:.3f}" if abs(value) < 100 else f"{value:.0f}"
        return str(value).replace("|", "/").replace("\n", " ")

    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return [*lines, ""]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    import csv

    path.parent.mkdir(parents=True, exist_ok=True)
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(row.get(key)) for key in columns})


def _csv_value(value: Any) -> Any:
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, default=str)
    return value


def fail_loudly(name: str, error: BaseException) -> None:
    """An error annotation with the traceback's end, then the trace on stdout."""
    trace = traceback.format_exc()
    annotate("error", name, f"{short(error, 800)}\n{trace[-2500:]}")
    print(trace, flush=True)
