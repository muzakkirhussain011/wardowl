"""The stores of experiments X2 and X5 behind one interface (PREREG_X2_X5.md, section 4).

Each adapter loads a prepared corpus through the wardowl backend's own `add` and layout (pgvector
by binary COPY into `create_schema`'s table, and LanceDB by `table.add` in the backend's row
layout, as benchmarks/stores.py does), waits until the store has indexed it, lists the settings of
its corpus and layout, and makes the backend for one setting. Settings wardowl's backends do not
expose are set by small subclasses here and reported as harness-level: Elasticsearch's and
OpenSearch's exact `script_score`, OpenSearch's `method_parameters.ef_search`, Redis's
`HYBRID_POLICY`, LanceDB's post-filtering and `bypass_vector_index`, Weaviate's HNSW settings and
Chroma's `ef_search` (collection configuration), and Qdrant's per-tenant layout.

Servers are started by the workflow; their addresses come from X2X5_* environment variables.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import time
import urllib.request
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import x2x5_common as xc
from x2x5_common import log

NAME = "wardowl_x2x5"
COLLECTION = "WardowlX2x5"  # Weaviate collection names start with a capital
LOAD_BLOCK = 5000  # chunks per call to a backend's add


@dataclass(frozen=True)
class Setting:
    """One search configuration of a store. `kind` is default, sweep, specific or exact; `level`
    orders the sweep (1 to 5); `asrun` marks the scenario run's setting on E (check V2); `build0`
    runs on the first build only (exact search does not use the index)."""

    id: str
    kind: str
    params: dict[str, Any] = field(default_factory=dict)
    level: int | None = None
    asrun: bool = False
    build0: bool = False
    harness: tuple[str, ...] = ()

    def describe(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "params": self.params,
            "level": self.level,
            "asrun": self.asrun,
            "build0": self.build0,
            "harness_level": list(self.harness),
        }


def sweep_settings(
    name: str, values: Sequence[Any], params: dict[str, Any], key: str, asrun: Any = None, harness: Sequence[str] = ()
) -> list[Setting]:
    return [
        Setting(f"{name}{v}", "sweep", {**params, key: v}, level=i + 1, asrun=v == asrun, harness=tuple(harness))
        for i, v in enumerate(values)
    ]


def add_corpus(backend: Any, corpus: xc.Corpus, block: int = LOAD_BLOCK, **options: Any) -> float:
    """Writes every chunk through the backend's own `add`, with the corpus's vectors; returns seconds."""
    started, total = time.perf_counter(), len(corpus)
    step = max(block, (total // 10) // block * block)
    for start in range(0, total, block):
        end = min(start + block, total)
        vectors = np.asarray(corpus.vectors[start:end], dtype=np.float32).tolist()
        backend.add(corpus.documents(start, end), embeddings=vectors, **options)
        if end == total or end % step < block:
            log(f"  loaded {end:,} of {total:,} chunks ({time.perf_counter() - started:.0f} s)")
    return round(time.perf_counter() - started, 1)


def wait_until(condition: Any, what: str, timeout: float = 7200.0, every: float = 2.0) -> float:
    started = time.monotonic()
    while not condition():
        if time.monotonic() - started > timeout:
            raise TimeoutError(f"{what} did not finish within {timeout:.0f} s")
        time.sleep(every)
    return round(time.monotonic() - started, 1)


def http_json(url: str, timeout: float = 60.0) -> Any:
    with urllib.request.urlopen(url, timeout=timeout) as response:  # noqa: S310 - the server this job started
        return json.loads(response.read())


class AlwaysExact:
    """A backend whose every search is its exact search (`search(..., exact=True)`)."""

    supports_filters = True
    exact_search = True

    def __init__(self, inner: Any) -> None:
        self.inner = inner

    def search(self, query: Any, k: int, filter: Any = None) -> list[Any]:
        return self.inner.search(query, k, filter, exact=True)


class Store:
    """One store: load a corpus, list its settings, make a backend per setting."""

    name = ""
    layouts: tuple[str, ...] = ("default",)

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        if layout not in self.layouts:
            raise ValueError(f"{self.name} has no layout {layout!r}; it has {self.layouts}")
        self.corpus, self.layout, self.work = corpus, layout, work
        self.work.mkdir(parents=True, exist_ok=True)

    def load(self, build: int) -> dict[str, Any]:
        raise NotImplementedError

    def settings(self) -> list[Setting]:
        raise NotImplementedError

    def backend(self, setting: Setting) -> Any:
        raise NotImplementedError

    def effective(self, backend: Any, setting: Setting) -> dict[str, Any]:
        """What the store reports for the setting, where it can tell (recorded with the setting)."""
        return {}

    def release(self, backend: Any) -> None:
        """Frees what `backend` holds (a connection pool)."""

    def plan(self, backend: Any, pair: xc.Pair, k: int) -> str:
        return ""

    def counters(self) -> dict[str, int] | None:
        return None

    def drop(self) -> None:
        """Deletes the loaded data."""

    def close(self) -> None:
        with contextlib.suppress(Exception):
            self.drop()

    def pairs(self, pairs: Sequence[xc.Pair]) -> list[xc.Pair]:
        """The pairs this layout is queried with (all but for Qdrant's per-tenant layout on M)."""
        return list(pairs)


# ---- pgvector ---------------------------------------------------------------------------------------


def plan_kind(document: Any) -> str:
    """hnsw, gin, seq or other: which access path an EXPLAIN (FORMAT JSON) plan uses for the table."""
    root = document[0] if isinstance(document, list) else document
    stack, nodes = [root["Plan"]], []
    while stack:
        node = stack.pop()
        nodes.append(node)
        stack.extend(node.get("Plans", []))
    names = [str(n.get("Index Name", "")) for n in nodes]
    if any(n.endswith("_embedding_hnsw") for n in names):
        return "hnsw"
    if any(n.endswith("_metadata_gin") for n in names):
        return "gin"
    if any(n.get("Node Type") == "Seq Scan" for n in nodes):
        return "seq"
    return "other"


class PgVector(Store):
    name = "pgvector"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        self.url = os.environ.get("X2X5_PG_URL", "postgresql://bench:bench@127.0.0.1:5432/bench")
        self.pools: dict[int, Any] = {}
        self.filters: dict[str, Any] = {}

    def load(self, build: int) -> dict[str, Any]:
        import psycopg
        from pgvector.psycopg import register_vector
        from psycopg import sql
        from psycopg.types.json import Jsonb
        from psycopg_pool import ConnectionPool

        from wardowl.backends.pgvector import create_schema

        corpus, table = self.corpus, sql.Identifier(NAME)
        with psycopg.connect(self.url, autocommit=True) as conn:
            conn.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(table))
        pool = ConnectionPool(self.url, min_size=1, max_size=1, open=True)
        try:
            create_schema(pool, corpus.dim, table=NAME, hnsw=False)  # the table and its GIN index
            started = time.perf_counter()
            with psycopg.connect(self.url, autocommit=True) as conn:
                register_vector(conn)
                copy = sql.SQL("COPY {} (id, content, metadata, embedding) FROM STDIN WITH (FORMAT BINARY)")
                with conn.cursor() as cur, cur.copy(copy.format(table)) as writer:
                    writer.set_types(["text", "text", "jsonb", "vector"])
                    for start in range(0, len(corpus), LOAD_BLOCK):
                        end = min(start + LOAD_BLOCK, len(corpus))
                        block = np.asarray(corpus.vectors[start:end], dtype=np.float32)
                        for row in range(start, end):
                            writer.write_row(
                                (corpus.ids[row], corpus.text(row), Jsonb(corpus.metadata(row)), block[row - start])
                            )
            copied = time.perf_counter()
            create_schema(pool, corpus.dim, table=NAME, hnsw=True)  # wardowl's HNSW index, pgvector's defaults
            indexed = time.perf_counter()
        finally:
            pool.close()
        with psycopg.connect(self.url, autocommit=True) as conn:
            conn.execute(sql.SQL("VACUUM (ANALYZE) {}").format(table))
            rows = conn.execute(sql.SQL("SELECT count(*) FROM {}").format(table)).fetchone()[0]
            size = conn.execute("SELECT pg_total_relation_size(%s)", [NAME]).fetchone()[0]
            names = (
                "server_version", "shared_buffers", "work_mem", "maintenance_work_mem", "effective_cache_size",
                "max_parallel_maintenance_workers", "hnsw.ef_search", "hnsw.iterative_scan", "hnsw.max_scan_tuples",
                "hnsw.scan_mem_multiplier", "plan_cache_mode",
            )  # fmt: skip
            server = {n: conn.execute("SELECT current_setting(%s, true)", [n]).fetchone()[0] for n in names}
            version = conn.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'").fetchone()
            server["pgvector"] = version[0] if version else None
        if rows != len(corpus):
            raise RuntimeError(f"pgvector holds {rows} rows, not {len(corpus)}")
        return {
            "rows": int(rows),
            "copy_s": round(copied - started, 1),
            "hnsw_index_s": round(indexed - copied, 1),
            "bytes": int(size),
            "server": server,
            "index": "HNSW (vector_cosine_ops) with pgvector's defaults (m 16, ef_construction 64), GIN jsonb_path_ops",
        }

    def settings(self) -> list[Setting]:
        relaxed = {"iterative_scan": "relaxed_order"}
        out = [Setting("default", "default", {"iterative_scan": None})]
        out += sweep_settings("ef", (40, 100, 200, 400, 1000), relaxed, "ef_search", asrun=100)
        out += [
            Setting(
                "scan1m", "specific", {**relaxed, "ef_search": 100, "max_scan_tuples": 1_000_000, "scan_mem_multiplier": 16}
            ),
            Setting("strict", "specific", {"iterative_scan": "strict_order", "ef_search": 100}),
            Setting("exact", "exact", {"exact": True}, build0=True),
        ]
        return out

    def make(self, params: dict[str, Any]) -> Any:
        """A PgVectorBackend with these parameters, on a pool of its own that never prepares
        statements, so PostgreSQL plans every search with its own values (X1 run 1, amendment 2)."""
        from psycopg_pool import ConnectionPool

        from wardowl.backends.pgvector import PgVectorBackend

        pool = ConnectionPool(self.url, min_size=1, max_size=1, open=True, kwargs={"prepare_threshold": None})
        pool.wait(timeout=60)
        backend = PgVectorBackend(
            pool,
            None,
            table=NAME,
            iterative_scan=params.get("iterative_scan"),
            ef_search=params.get("ef_search"),
            max_scan_tuples=params.get("max_scan_tuples"),
            scan_mem_multiplier=params.get("scan_mem_multiplier"),
            work_mem=params.get("work_mem"),
        )
        self.pools[id(backend)] = pool
        return backend

    def backend(self, setting: Setting) -> Any:
        backend = self.make(setting.params)
        if setting.params.get("exact"):
            wrapped = AlwaysExact(backend)
            self.pools[id(wrapped)] = self.pools.pop(id(backend))
            return wrapped
        return backend

    def inner(self, backend: Any) -> tuple[Any, bool]:
        return (backend.inner, True) if isinstance(backend, AlwaysExact) else (backend, False)

    def effective(self, backend: Any, setting: Setting) -> dict[str, Any]:
        inner, exact = self.inner(backend)
        names = ("hnsw.ef_search", "hnsw.iterative_scan", "hnsw.max_scan_tuples", "hnsw.scan_mem_multiplier",
                 "work_mem", "enable_indexscan", "plan_cache_mode")  # fmt: skip
        with inner.pool.connection() as conn, conn.transaction():
            conn.execute("SELECT '[1]'::vector")
            for statement in inner._settings(exact):
                conn.execute(statement)
            values = {n: conn.execute("SELECT current_setting(%s, true)", [n]).fetchone()[0] for n in names}
            values["prepare_threshold"] = str(conn.prepare_threshold)
        return values

    def filter_of(self, sid: str) -> Any:
        if sid not in self.filters:
            self.filters[sid] = self.corpus.authorizer.filter_for(self.corpus.subject(sid), "read")
        return self.filters[sid]

    def plan(self, backend: Any, pair: xc.Pair, k: int) -> str:
        """The access path PostgreSQL plans for this search, with its own values and settings."""
        from psycopg import sql

        inner, exact = self.inner(backend)
        query = self.corpus.query(pair)
        statement, params = inner._statement(query, inner._query_vector(query), k, self.filter_of(pair.sid))
        try:
            with inner.pool.connection() as conn, conn.transaction():
                for setting in inner._settings(exact):
                    conn.execute(setting)
                document = conn.execute(sql.SQL("EXPLAIN (FORMAT JSON) ") + statement, params).fetchone()[0]
        except Exception as error:  # a plan is a diagnostic: its failure is recorded, never fatal
            return f"error: {type(error).__name__}"
        return plan_kind(json.loads(document) if isinstance(document, (str, bytes)) else document)

    def release(self, backend: Any) -> None:
        pool = self.pools.pop(id(backend), None)
        if pool is not None:
            pool.close()

    def drop(self) -> None:
        import psycopg
        from psycopg import sql

        for pool in self.pools.values():
            with contextlib.suppress(Exception):
                pool.close()
        self.pools.clear()
        with psycopg.connect(self.url, autocommit=True) as conn:
            conn.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(NAME)))


# ---- Qdrant -----------------------------------------------------------------------------------------

QDRANT_COUNTERS = frozenset(
    {"filtered_plain", "filtered_small_cardinality", "filtered_large_cardinality", "filtered_acorn", "filtered_exact"}
)


class Qdrant(Store):
    name = "qdrant"
    layouts = ("as-run", "tenant")

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        from qdrant_client import QdrantClient

        self.url = os.environ.get("X2X5_QDRANT_URL", "http://127.0.0.1:6333")
        self.client = QdrantClient(url=self.url, timeout=600)

    def drop(self) -> None:
        if self.client.collection_exists(NAME):
            self.client.delete_collection(NAME)

    def load(self, build: int) -> dict[str, Any]:
        from qdrant_client import models

        from wardowl.backends.qdrant import QdrantBackend, create_collection

        self.drop()
        corpus = self.corpus
        if self.layout == "tenant":
            vectors = models.VectorParams(size=corpus.dim, distance=models.Distance.COSINE)
            hnsw = models.HnswConfigDiff(m=0, payload_m=16)
            self.client.create_collection(NAME, vectors_config=vectors, hnsw_config=hnsw)
            tenant = models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True)
            self.client.create_payload_index(NAME, f"metadata.{corpus.tenant_field}", field_schema=tenant)
            fields = tuple(f for f in corpus.keyword_fields if f != corpus.tenant_field)
        else:
            fields = corpus.keyword_fields
        create_collection(self.client, NAME, corpus.dim, keyword_fields=fields)  # the payload indexes
        load_s = add_corpus(QdrantBackend(self.client, NAME, None), corpus)
        index_s = self.wait_indexed()
        info = self.client.get_collection(NAME)
        if int(info.points_count or 0) != len(corpus):
            raise RuntimeError(f"Qdrant holds {info.points_count} points, not {len(corpus)}")
        return {
            "load_s": load_s,
            "index_s": index_s,
            "points": int(info.points_count or 0),
            "indexed_vectors": int(info.indexed_vectors_count or 0),
            "segments": int(info.segments_count or 0),
            "server": http_json(f"{self.url}/"),
            "layout": "wardowl's create_collection, keyword indexes on the permission fields"
            if self.layout == "as-run"
            else "tenant field is_tenant=true, hnsw m 0 and payload_m 16 (harness-level), other fields as as-run",
            "keyword_fields": list(fields),
        }

    def wait_indexed(self, timeout: float = 7200.0) -> float:
        """Until the collection is green with the same counts over four checks, 5 s apart; a grey
        collection gets an empty optimizer update, which starts its optimizations (as X1 does)."""
        from qdrant_client import models

        started = time.monotonic()
        last: Any = None
        stable = 0
        nudged = 0.0
        while True:
            info = self.client.get_collection(NAME)
            status = str(info.status).lower()
            if status.endswith("grey") and time.monotonic() - nudged > 60:
                self.client.update_collection(NAME, optimizers_config=models.OptimizersConfigDiff())
                nudged = time.monotonic()
            state = (info.points_count, info.indexed_vectors_count, info.segments_count)
            stable = stable + 1 if status.endswith("green") and state == last else 0
            if stable >= 3:
                return round(time.monotonic() - started, 1)
            if time.monotonic() - started > timeout:
                raise TimeoutError(f"Qdrant did not finish indexing within {timeout:.0f} s: {state}")
            last = state
            time.sleep(5)

    def settings(self) -> list[Setting]:
        if self.layout == "tenant":
            return [
                Setting("ef128", "sweep", {"hnsw_ef": 128}, level=2, harness=("layout",)),
                Setting("ef512", "sweep", {"hnsw_ef": 512}, level=4, harness=("layout",)),
                Setting("acorn-max", "specific", {"hnsw_ef": 512, "acorn": 1.0}, harness=("layout",)),
                Setting("exact", "exact", {"exact": True}, build0=True, harness=("layout",)),
            ]
        out = [Setting("default", "default", {})]
        out += sweep_settings("ef", (64, 128, 256, 512, 1024), {}, "hnsw_ef", asrun=128)
        out += [
            Setting("acorn", "specific", {"hnsw_ef": None, "acorn": "default"}),
            Setting("acorn-max", "specific", {"hnsw_ef": 512, "acorn": 1.0}),
            Setting("exact", "exact", {"exact": True}, build0=True),
        ]
        return out

    @staticmethod
    def params(p: dict[str, Any]) -> Any:
        from qdrant_client import models

        if p.get("exact"):
            return models.SearchParams(exact=True)
        acorn = None
        if p.get("acorn") == "default":
            acorn = models.AcornSearchParams(enable=True)  # Qdrant's default gate, max_selectivity 0.4
        elif p.get("acorn") is not None:
            acorn = models.AcornSearchParams(enable=True, max_selectivity=float(p["acorn"]))
        if p.get("hnsw_ef") is None and acorn is None:
            return None
        return models.SearchParams(hnsw_ef=p.get("hnsw_ef"), acorn=acorn)

    def backend(self, setting: Setting) -> Any:
        from wardowl.backends.qdrant import QdrantBackend

        return QdrantBackend(self.client, NAME, None, search_params=self.params(setting.params))

    def effective(self, backend: Any, setting: Setting) -> dict[str, Any]:
        params = backend.search_params
        dump = getattr(params, "model_dump", None)
        return {"search_params": dump(exclude_none=True) if dump else None}

    def counters(self) -> dict[str, int] | None:
        """Qdrant's per-segment filtered-search counters (/telemetry), summed per counter."""
        try:
            document = http_json(f"{self.url}/telemetry?details_level=10")
        except (OSError, ValueError):
            return None
        found: Counter[str] = Counter()
        stack: list[tuple[Any, str]] = [(document, "")]
        while stack:
            node, path = stack.pop()
            if isinstance(node, dict):
                for key, value in node.items():
                    if key in QDRANT_COUNTERS and isinstance(value, dict) and isinstance(value.get("count"), int):
                        if "segments" in path:  # per segment only, so aggregates are not added twice
                            found[key] += value["count"]
                    else:
                        stack.append((value, f"{path}/{key}"))
            elif isinstance(node, list):
                stack.extend((item, path) for item in node)
        return dict(found)

    def pairs(self, pairs: Sequence[xc.Pair]) -> list[xc.Pair]:
        if self.layout == "tenant" and self.corpus.name == xc.M_NAME:
            return [p for p in pairs if p.shape == "tenant"]
        return list(pairs)


# ---- Elasticsearch and OpenSearch ---------------------------------------------------------------------


def _script_filter(query: dict[str, Any] | None) -> dict[str, Any]:
    return {"bool": {"filter": [query if query is not None else {"match_all": {}}]}}


def es_classes() -> tuple[type, type]:
    from wardowl.backends.elasticsearch import ElasticsearchBackend

    class ExactElasticsearch(ElasticsearchBackend):
        """Exact search: cosine similarity of every chunk the filter admits (`script_score`)."""

        def _search_request(self, vector: list[float], k: int, query: dict[str, Any] | None) -> dict[str, Any]:
            script = {
                "source": f"cosineSimilarity(params.query_vector, '{self.vector_field}') + 1.0",
                "params": {"query_vector": vector},
            }
            return {
                "query": {"script_score": {"query": _script_filter(query), "script": script}},
                "size": k,
                "source_excludes": [self.vector_field],
            }

    return ElasticsearchBackend, ExactElasticsearch


def os_classes() -> tuple[type, type, type]:
    from wardowl.backends.opensearch import OpenSearchBackend

    class EfOpenSearch(OpenSearchBackend):
        """The k-NN query with `method_parameters.ef_search` (OpenSearch 2.16 and later)."""

        ef_search = 100

        def _search_request(self, vector: list[float], k: int, query: dict[str, Any] | None) -> dict[str, Any]:
            request = super()._search_request(vector, k, query)
            request["body"]["query"]["knn"][self.vector_field]["method_parameters"] = {"ef_search": self.ef_search}
            return request

    class ExactOpenSearch(OpenSearchBackend):
        """Exact search: the k-NN scoring script over every chunk the filter admits."""

        def _search_request(self, vector: list[float], k: int, query: dict[str, Any] | None) -> dict[str, Any]:
            script = {
                "source": "knn_score",
                "lang": "knn",
                "params": {"field": self.vector_field, "query_value": vector, "space_type": "cosinesimil"},
            }
            body = {
                "size": k,
                "query": {"script_score": {"query": _script_filter(query), "script": script}},
                "_source": {"excludes": [self.vector_field]},
            }
            return {"body": body}

    return OpenSearchBackend, EfOpenSearch, ExactOpenSearch


class Elasticsearch(Store):
    name = "elasticsearch"
    layouts = ("default", "int8")

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        from elasticsearch import Elasticsearch as Client

        self.client = Client(os.environ.get("X2X5_ES_URL", "http://127.0.0.1:9200"), request_timeout=600)

    def drop(self) -> None:
        if self.client.indices.exists(index=NAME):
            self.client.indices.delete(index=NAME)

    def load(self, build: int) -> dict[str, Any]:
        from wardowl.backends.elasticsearch import create_index

        self.drop()
        options = {"type": "int8_hnsw"} if self.layout == "int8" else None  # None: the store's default
        create_index(self.client, NAME, self.corpus.dim, index_options=options)
        backend_class, _ = es_classes()
        load_s = add_corpus(backend_class(self.client, NAME, None, refresh=False), self.corpus)
        started = time.perf_counter()
        self.client.indices.refresh(index=NAME)
        refresh_s = round(time.perf_counter() - started, 1)
        stats = self.client.indices.stats(index=NAME)["indices"][NAME]["total"]
        mapping = self.client.indices.get_mapping(index=NAME)[NAME]["mappings"]["properties"]["embedding"]
        segments = self.client.indices.segments(index=NAME)
        count = sum(len(shard[0]["segments"]) for shard in segments["indices"][NAME]["shards"].values())
        if int(stats["docs"]["count"]) != len(self.corpus):
            raise RuntimeError(f"Elasticsearch holds {stats['docs']['count']} documents, not {len(self.corpus)}")
        info = self.client.info()
        return {
            "load_s": load_s,
            "refresh_s": refresh_s,
            "documents": int(stats["docs"]["count"]),
            "bytes": int(stats["store"]["size_in_bytes"]),
            "segments": count,
            "vector_mapping": mapping,
            "version": info["version"]["number"],
        }

    def settings(self) -> list[Setting]:
        asrun = 500 if self.layout == "int8" and self.corpus.name == xc.E_NAME else None
        out = [Setting("default", "default", {"num_candidates": 15})]  # Elasticsearch's 1.5 k at k = 10
        out += sweep_settings("nc", (50, 100, 500, 2000, 10000), {}, "num_candidates", asrun=asrun)
        out.append(Setting("exact", "exact", {"exact": True}, build0=True, harness=("script_score",)))
        return out

    def backend(self, setting: Setting) -> Any:
        plain, exact = es_classes()
        if setting.params.get("exact"):
            return exact(self.client, NAME, None)
        return plain(self.client, NAME, None, num_candidates=int(setting.params["num_candidates"]))


class OpenSearch(Store):
    name = "opensearch"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        from opensearchpy import OpenSearch as Client

        self.client = Client(hosts=[os.environ.get("X2X5_OS_URL", "http://127.0.0.1:9200")], timeout=600)

    def drop(self) -> None:
        if self.client.indices.exists(index=NAME):
            self.client.indices.delete(index=NAME)

    def load(self, build: int) -> dict[str, Any]:
        from wardowl.backends.opensearch import create_index

        self.drop()
        create_index(self.client, NAME, self.corpus.dim)
        plain, _, _ = os_classes()
        load_s = add_corpus(plain(self.client, NAME, None, refresh=False), self.corpus)
        started = time.perf_counter()
        self.client.indices.refresh(index=NAME)
        refresh_s = round(time.perf_counter() - started, 1)
        stats = self.client.indices.stats(index=NAME)["indices"][NAME]["total"]
        if int(stats["docs"]["count"]) != len(self.corpus):
            raise RuntimeError(f"OpenSearch holds {stats['docs']['count']} documents, not {len(self.corpus)}")
        segments = self.client.indices.segments(index=NAME)
        count = sum(len(shard[0]["segments"]) for shard in segments["indices"][NAME]["shards"].values())
        return {
            "load_s": load_s,
            "refresh_s": refresh_s,
            "documents": int(stats["docs"]["count"]),
            "bytes": int(stats["store"]["size_in_bytes"]),
            "segments": count,
            "version": self.client.info()["version"]["number"],
        }

    def settings(self) -> list[Setting]:
        out = [Setting("default", "default", {}, asrun=self.corpus.name == xc.E_NAME)]
        out += sweep_settings("ef", (32, 64, 128, 256, 512), {}, "ef_search", harness=("method_parameters",))
        out.append(Setting("exact", "exact", {"exact": True}, build0=True, harness=("script_score",)))
        return out

    def backend(self, setting: Setting) -> Any:
        plain, ef, exact = os_classes()
        if setting.params.get("exact"):
            return exact(self.client, NAME, None)
        if setting.params.get("ef_search") is not None:
            backend = ef(self.client, NAME, None)
            backend.ef_search = int(setting.params["ef_search"])
            return backend
        return plain(self.client, NAME, None)


# ---- Weaviate -----------------------------------------------------------------------------------------


class Weaviate(Store):
    name = "weaviate"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        from urllib.parse import urlsplit

        import weaviate

        parts = urlsplit(os.environ.get("X2X5_WEAVIATE_URL", "http://127.0.0.1:8079"))
        grpc = int(os.environ.get("X2X5_WEAVIATE_GRPC_PORT", "50051"))
        self.client = weaviate.connect_to_local(host=parts.hostname, port=parts.port or 8080, grpc_port=grpc)

    def drop(self) -> None:
        if self.client.collections.exists(COLLECTION):
            self.client.collections.delete(COLLECTION)

    def close(self) -> None:
        super().close()
        with contextlib.suppress(Exception):
            self.client.close()

    def load(self, build: int) -> dict[str, Any]:
        from wardowl.backends.weaviate import WeaviateBackend, create_collection

        self.drop()
        create_collection(self.client, COLLECTION)
        load_s = add_corpus(WeaviateBackend(self.client, COLLECTION, None), self.corpus, block=2000)
        handle = self.client.collections.get(COLLECTION)
        count = int(handle.aggregate.over_all(total_count=True).total_count)
        if count != len(self.corpus):
            raise RuntimeError(f"Weaviate holds {count} objects, not {len(self.corpus)}")
        return {"load_s": load_s, "objects": count, "config": self.read_config(), "version": self.version()}

    def version(self) -> Any:
        with contextlib.suppress(Exception):
            return self.client.get_meta().get("version")
        return None

    def settings(self) -> list[Setting]:
        base = {"ef": -1, "strategy": "acorn", "cutoff": 40_000}
        harness = ("collection configuration",)
        out = [Setting("default", "default", dict(base), asrun=self.corpus.name == xc.E_NAME)]
        out += sweep_settings("ef", (64, 128, 256, 512, 1024), base, "ef", harness=harness)
        out += [
            Setting("sweeping", "specific", {**base, "strategy": "sweeping"}, harness=harness),
            Setting("noflat", "specific", {**base, "cutoff": 0}, harness=harness),
            Setting("exact", "exact", {**base, "cutoff": 100_000_000}, build0=True, harness=harness),
        ]
        return out

    def read_config(self) -> dict[str, Any]:
        try:
            config = self.client.collections.get(COLLECTION).config.get()
            index = config.vector_config["embedding"].vector_index_config
            strategy = getattr(index, "filter_strategy", None)
            return {
                "ef": getattr(index, "ef", None),
                "flat_search_cutoff": getattr(index, "flat_search_cutoff", None),
                "filter_strategy": str(getattr(strategy, "value", strategy)).lower(),
                "dynamic_ef": [getattr(index, n, None) for n in ("dynamic_ef_min", "dynamic_ef_max", "dynamic_ef_factor")],
            }
        except Exception as error:  # recorded, so a setting that did not take effect is visible
            return {"error": f"{type(error).__name__}: {error}"}

    def backend(self, setting: Setting) -> Any:
        from weaviate.classes.config import Reconfigure, VectorFilterStrategy

        from wardowl.backends.weaviate import WeaviateBackend

        p = setting.params
        strategy = VectorFilterStrategy.ACORN if p["strategy"] == "acorn" else VectorFilterStrategy.SWEEPING
        handle = self.client.collections.get(COLLECTION)
        handle.config.update(
            vector_config=Reconfigure.Vectors.update(
                name="embedding",
                vector_index_config=Reconfigure.VectorIndex.hnsw(
                    ef=int(p["ef"]), filter_strategy=strategy, flat_search_cutoff=int(p["cutoff"])
                ),
            )
        )

        def applied() -> bool:
            found = self.read_config()
            return found.get("ef") == p["ef"] and found.get("flat_search_cutoff") == p["cutoff"] and (
                str(found.get("filter_strategy")) == p["strategy"]
            )

        wait_until(applied, f"Weaviate's configuration for {setting.id}", timeout=120, every=1)
        return WeaviateBackend(self.client, COLLECTION, None)

    def effective(self, backend: Any, setting: Setting) -> dict[str, Any]:
        return self.read_config()


# ---- Redis ---------------------------------------------------------------------------------------------


def redis_class() -> type:
    from wardowl.backends.redis import RedisBackend

    class HybridRedis(RedisBackend):
        """The KNN clause with `HYBRID_POLICY` (BATCHES or ADHOC_BF, Redis's brute force over the
        chunks the filter admits), when one is set."""

        policy: str | None = None

        def _command(self, query: Any, k: int, f: Any) -> list[Any] | None:
            command = super()._command(query, k, f)
            if command is None or not self.policy or self.mode != "vector":
                return command
            command = list(command)
            command[2] = command[2].replace(" AS ", f" HYBRID_POLICY {self.policy} AS ", 1)
            return command

    return HybridRedis


class Redis(Store):
    name = "redis"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        import redis

        self.client = redis.Redis.from_url(os.environ.get("X2X5_REDIS_URL", "redis://127.0.0.1:6379/0"), socket_timeout=600)
        self.prefix = f"{NAME}:"

    def info(self) -> dict[str, Any]:
        reply = self.client.execute_command("FT.INFO", NAME)
        pairs = reply.items() if isinstance(reply, dict) else zip(reply[::2], reply[1::2], strict=True)
        return {(k.decode() if isinstance(k, bytes) else str(k)): v for k, v in pairs}

    def drop(self) -> None:
        names = [n.decode() if isinstance(n, bytes) else str(n) for n in self.client.execute_command("FT._LIST")]
        if NAME in names:
            self.client.execute_command("FT.DROPINDEX", NAME, "DD")

    def load(self, build: int) -> dict[str, Any]:
        from wardowl.backends.redis import create_index

        self.drop()
        config = {}
        # What the integration docs advise: a search that runs out of time fails rather than returns
        # partial results; and a long limit, so that brute force over a large filter can finish.
        for key, value in (("search-on-timeout", "fail"), ("search-timeout", "60000")):
            try:
                self.client.config_set(key, value)
                config[key] = value
            except Exception as error:
                config[key] = f"not set: {type(error).__name__}: {error}"
        create_index(self.client, NAME, self.corpus.dim, prefix=self.prefix)
        load_s = add_corpus(redis_class()(self.client, NAME, None, prefix=self.prefix), self.corpus)
        index_s = wait_until(lambda: float(self.info().get("indexing", 0)) == 0, "Redis indexing")
        docs = self.info().get("num_docs", 0)
        count = int(docs.decode() if isinstance(docs, bytes) else docs)
        if count != len(self.corpus):
            raise RuntimeError(f"Redis indexed {count} documents, not {len(self.corpus)}")
        memory = self.client.info("memory").get("used_memory_human")
        return {"load_s": load_s, "index_s": index_s, "documents": count, "used_memory": memory, "config": config,
                "version": self.client.info("server").get("redis_version")}  # fmt: skip

    def settings(self) -> list[Setting]:
        out = [Setting("default", "default", {})]
        out += sweep_settings("ef", (50, 100, 200, 500, 1000), {}, "ef_runtime", asrun=100)
        out += [
            Setting("batches", "specific", {"ef_runtime": 100, "policy": "BATCHES"}, harness=("HYBRID_POLICY",)),
            Setting("exact", "exact", {"policy": "ADHOC_BF"}, build0=True, harness=("HYBRID_POLICY",)),
        ]
        return out

    def backend(self, setting: Setting) -> Any:
        backend = redis_class()(self.client, NAME, None, prefix=self.prefix, ef_runtime=setting.params.get("ef_runtime"))
        backend.policy = setting.params.get("policy")
        return backend


# ---- Milvus --------------------------------------------------------------------------------------------


class Milvus(Store):
    name = "milvus"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        from pymilvus import MilvusClient

        self.client = MilvusClient(uri=os.environ.get("X2X5_MILVUS_URL", "http://127.0.0.1:19530"), timeout=600)

    def drop(self) -> None:
        if self.client.has_collection(NAME):
            self.client.drop_collection(NAME)

    def load(self, build: int) -> dict[str, Any]:
        from wardowl.backends.milvus import MilvusBackend, create_collection

        self.drop()
        create_collection(self.client, NAME, self.corpus.dim)
        load_s = add_corpus(MilvusBackend(self.client, NAME, None), self.corpus)
        self.client.flush(NAME)
        (index_name,) = self.client.list_indexes(NAME, field_name="embedding")

        def indexed() -> bool:
            info = self.client.describe_index(NAME, index_name=index_name)
            return str(info.get("state")) == "Finished" and not int(info.get("pending_index_rows", 0))

        index_s = wait_until(indexed, "Milvus indexing")
        stats = self.client.get_collection_stats(NAME)
        rows = int(stats.get("row_count", 0))
        if rows != len(self.corpus):
            raise RuntimeError(f"Milvus holds {rows} rows, not {len(self.corpus)}")
        return {"load_s": load_s, "index_s": index_s, "rows": rows, "index": "HNSW (M 16, efConstruction 200)"}

    def settings(self) -> list[Setting]:
        out = [Setting("default", "default", {"server_default": True})]
        out += sweep_settings("ef", (32, 64, 100, 256, 512), {}, "ef")
        return out

    def backend(self, setting: Setting) -> Any:
        from wardowl.backends.milvus import MilvusBackend

        if setting.params.get("server_default"):
            return MilvusBackend(self.client, NAME, None, search_params={"params": {}})
        return MilvusBackend(self.client, NAME, None, ef=int(setting.params["ef"]))


# ---- MongoDB Atlas Local -------------------------------------------------------------------------------


class MongoDB(Store):
    name = "mongodb"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        from pymongo import MongoClient

        url = os.environ.get("X2X5_MONGO_URL", "mongodb://127.0.0.1:27017/?directConnection=true")
        self.client = MongoClient(url)
        self.collection = self.client["wardowl_x2x5"][NAME]

    def drop(self) -> None:
        self.collection.drop()

    def close(self) -> None:
        super().close()
        with contextlib.suppress(Exception):
            self.client.close()

    def load(self, build: int) -> dict[str, Any]:
        from wardowl.backends.mongodb import MongoDBBackend, create_search_index

        self.drop()
        self.collection.database.create_collection(NAME)
        corpus = self.corpus
        last = max(0, len(corpus) - LOAD_BLOCK)
        started = time.perf_counter()
        writer = MongoDBBackend(self.collection, None, wait_timeout=3600)
        for start in range(0, last, LOAD_BLOCK):
            end = min(start + LOAD_BLOCK, last)
            vectors = np.asarray(corpus.vectors[start:end], dtype=np.float32).tolist()
            writer.add(corpus.documents(start, end), embeddings=vectors, wait=False)
        bulk_s = round(time.perf_counter() - started, 1)
        started = time.perf_counter()
        create_search_index(self.collection, corpus.dim, wait=True, timeout=7200)  # queryable after its initial sync
        index_s = round(time.perf_counter() - started, 1)
        started = time.perf_counter()
        vectors = np.asarray(corpus.vectors[last:], dtype=np.float32).tolist()
        writer.add(corpus.documents(last, len(corpus)), embeddings=vectors)  # waits until the index shows these
        settle_s = round(time.perf_counter() - started, 1)
        count = self.collection.count_documents({})
        if count != len(corpus):
            raise RuntimeError(f"MongoDB holds {count} documents, not {len(corpus)}")
        version = self.client.server_info().get("version")
        return {"bulk_s": bulk_s, "index_s": index_s, "settle_s": settle_s, "documents": count, "version": version}

    def settings(self) -> list[Setting]:
        out = [Setting("default", "default", {"num_candidates": 100})]
        out += sweep_settings("nc", (20, 50, 200, 1000, 10000), {}, "num_candidates")
        out.append(Setting("exact", "exact", {"exact": True}, build0=True))
        return out

    def backend(self, setting: Setting) -> Any:
        from wardowl.backends.mongodb import MongoDBBackend

        if setting.params.get("exact"):
            return MongoDBBackend(self.collection, None, exact=True)
        return MongoDBBackend(self.collection, None, num_candidates=int(setting.params["num_candidates"]))


# ---- LanceDB ------------------------------------------------------------------------------------------


def lancedb_class() -> type:
    from wardowl.backends.lancedb import LanceDBBackend, _predicate
    from wardowl.types import Query

    class TunedLanceDB(LanceDBBackend):
        """LanceDB's vector search as the backend runs it, plus post-filtering (`prefilter=False`) and
        exact search (`bypass_vector_index()`)."""

        prefilter = True
        bypass = False

        def search(self, query: Any, k: int, filter: Any = None) -> list[Any]:
            if k < 1:
                return []
            where = None
            if filter is not None:
                where = _predicate(filter)
                if where is None:
                    return []  # nothing can match
            columns = ["id", self.content_field, self.metadata_field]
            vector = Query.of(query).embedded(self.embed)
            builder = self.table.search(vector, vector_column_name=self.vector_field)
            builder = builder.distance_type("cosine").select(columns).limit(k)
            if self.bypass:
                builder = builder.bypass_vector_index()
            else:
                if self.nprobes is not None:
                    builder = builder.nprobes(self.nprobes)
                if self.refine_factor is not None:
                    builder = builder.refine_factor(self.refine_factor)
            if where is not None:
                builder = builder.where(where, prefilter=self.prefilter)
            hits = [self._hit(row) for row in builder.to_list()]
            hits.sort(key=lambda h: (-h.score, h.id))
            return hits

    return TunedLanceDB


class LanceDB(Store):
    name = "lancedb"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        import lancedb

        self.path = work / f"lancedb-{layout}"
        shutil.rmtree(self.path, ignore_errors=True)
        self.db = lancedb.connect(str(self.path))
        self.table: Any = None

    def drop(self) -> None:
        self.db.drop_table(NAME, ignore_missing=True)
        self.table = None

    def load(self, build: int) -> dict[str, Any]:
        import pyarrow as pa

        from wardowl.backends.lancedb import KEY_FIELD, TERMS_FIELD, create_indexes, create_table, permission_terms

        self.drop()
        corpus = self.corpus
        table = create_table(self.db, NAME, corpus.dim)
        started = time.perf_counter()
        for start in range(0, len(corpus), 100_000):
            end = min(start + 100_000, len(corpus))
            metadata = [corpus.metadata(r) for r in range(start, end)]
            block = np.ascontiguousarray(corpus.vectors[start:end], dtype=np.float32)
            rows = pa.table(
                {
                    "id": corpus.ids[start:end],
                    KEY_FIELD: [i.encode("utf-8").hex() for i in corpus.ids[start:end]],
                    "content": [corpus.text(r) for r in range(start, end)],
                    "metadata": [json.dumps(m) for m in metadata],
                    TERMS_FIELD: [permission_terms(m) for m in metadata],
                    "vector": pa.FixedSizeListArray.from_arrays(pa.array(block.ravel()), corpus.dim),
                },
                schema=table.schema,
            )
            table.add(rows)
            log(f"  loaded {end:,} of {len(corpus):,} chunks ({time.perf_counter() - started:.0f} s)")
        load_s = round(time.perf_counter() - started, 1)
        started = time.perf_counter()
        create_indexes(table)
        table.create_index(metric="cosine", vector_column_name="vector")
        index_s = round(time.perf_counter() - started, 1)
        self.table = table
        indices = []
        with contextlib.suppress(Exception):
            indices = [str(i) for i in table.list_indices()]
        if table.count_rows() != len(corpus):
            raise RuntimeError(f"LanceDB holds {table.count_rows()} rows, not {len(corpus)}")
        return {"load_s": load_s, "index_s": index_s, "rows": int(table.count_rows()), "indices": indices,
                "detail": "bulk table.add in the backend's row layout; the default vector index (IVF_PQ), cosine"}  # fmt: skip

    def settings(self) -> list[Setting]:
        out = [Setting("default", "default", {})]
        out += sweep_settings("np", (10, 50, 100, 200, 500), {}, "nprobes")
        out += [
            Setting("refine", "specific", {"nprobes": 50, "refine_factor": 30}, asrun=self.corpus.name == xc.E_NAME),
            Setting("postfilter", "specific", {"prefilter": False}, harness=("prefilter=False",)),
            Setting("exact", "exact", {"bypass": True}, build0=True, harness=("bypass_vector_index",)),
        ]
        return out

    def backend(self, setting: Setting) -> Any:
        p = setting.params
        backend = lancedb_class()(self.table, None, nprobes=p.get("nprobes"), refine_factor=p.get("refine_factor"))
        backend.prefilter = bool(p.get("prefilter", True))
        backend.bypass = bool(p.get("bypass", False))
        return backend


# ---- Chroma -------------------------------------------------------------------------------------------


class Chroma(Store):
    name = "chroma"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        self.path = work / "chroma"
        self.client: Any = None
        self.collection: Any = None

    def drop(self) -> None:
        if self.client is not None:
            with contextlib.suppress(Exception):
                self.client.delete_collection(NAME)
        self.client = self.collection = None

    def load(self, build: int) -> dict[str, Any]:
        import chromadb

        from wardowl.backends.chroma import ChromaBackend

        self.drop()
        # A folder of its own per build: chromadb keeps one system per path for the whole process.
        self.path = self.work / f"chroma-b{build}"
        shutil.rmtree(self.path, ignore_errors=True)
        self.client = chromadb.PersistentClient(path=str(self.path))
        self.collection = self.client.get_or_create_collection(NAME, configuration={"hnsw": {"space": "cosine"}})
        load_s = add_corpus(ChromaBackend(self.collection), self.corpus)
        count = int(self.collection.count())
        if count != len(self.corpus):
            raise RuntimeError(f"Chroma holds {count} records, not {len(self.corpus)}")
        return {"load_s": load_s, "records": count, "version": chromadb.__version__, "config": self.read_config()}

    def read_config(self) -> Any:
        try:
            return json.loads(json.dumps(self.collection.configuration, default=str))
        except Exception as error:
            return {"error": f"{type(error).__name__}: {error}"}

    def settings(self) -> list[Setting]:
        harness = ("collection configuration",)
        out = [Setting("default", "default", {"ef_search": 100}, asrun=self.corpus.name == xc.E_NAME)]
        out += sweep_settings("ef", (10, 50, 200, 500, 1000), {}, "ef_search", harness=harness)
        return out

    def backend(self, setting: Setting) -> Any:
        from wardowl.backends.chroma import ChromaBackend

        self.collection.modify(configuration={"hnsw": {"ef_search": int(setting.params["ef_search"])}})
        return ChromaBackend(self.collection)

    def effective(self, backend: Any, setting: Setting) -> dict[str, Any]:
        return {"configuration": self.read_config()}


# ---- FAISS --------------------------------------------------------------------------------------------


class Faiss(Store):
    name = "faiss"

    def __init__(self, corpus: xc.Corpus, layout: str, work: Path) -> None:
        super().__init__(corpus, layout, work)
        self.index: Any = None

    def load(self, build: int) -> dict[str, Any]:
        from wardowl.backends.faiss import FaissBackend

        self.index = FaissBackend(None, dim=self.corpus.dim)
        load_s = add_corpus(self.index, self.corpus)
        return {"load_s": load_s, "rows": len(self.index), "detail": "IndexFlatIP (exact), metadata matched in Python"}

    def settings(self) -> list[Setting]:
        return [Setting("exact", "exact", {}, asrun=True, build0=True)]

    def backend(self, setting: Setting) -> Any:
        return self.index

    def drop(self) -> None:
        self.index = None


STORES: dict[str, type[Store]] = {
    "pgvector": PgVector,
    "qdrant": Qdrant,
    "elasticsearch": Elasticsearch,
    "opensearch": OpenSearch,
    "weaviate": Weaviate,
    "redis": Redis,
    "milvus": Milvus,
    "mongodb": MongoDB,
    "lancedb": LanceDB,
    "chroma": Chroma,
    "faiss": Faiss,
}


def make_store(name: str, corpus: xc.Corpus, layout: str, work: Path) -> Store:
    if name not in STORES:
        raise ValueError(f"unknown store {name!r}; known: {sorted(STORES)}")
    return STORES[name](corpus, layout, work)
