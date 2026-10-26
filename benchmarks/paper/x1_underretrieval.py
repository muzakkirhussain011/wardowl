"""Experiment X1: under-retrieval under permission filters, in pgvector and Qdrant (retrieval only).

Sections 6.1 to 6.5 of the investigation (filtered-recall-gaps.md), with the predictions and the
rules that judge them fixed beforehand in PREREGISTRATION.md. It reuses the scenario of the Kaggle
run of 2026-10-24 (acceptance/kaggle/enterprise_rag.py, imported, not copied): the same 107,540
chunks, 189 people and 1,105 questions, the same embeddings (BAAI/bge-base-en-v1.5, cached under
/kaggle/working/cache, or taken from the original run's output when it is attached), the same exact
baseline and recall, and the same way of starting PostgreSQL + pgvector and Qdrant on Kaggle. The
language model is not loaded: nothing here generates an answer.

Added to the scenario:

* the probe set of section 6.1: one person holding a single group, for each of 8 groups, in 3
  generated tenants, each asking the 12 template questions of their tenant and 4 FiQA queries;
* the alignment variables of every (question, person), from exact GPU ranking: R (chunks the
  person may read), r1, r5 and r10 (unfiltered rank of the first, fifth and tenth readable chunk)
  and rho_100, rho_1000 (share of readable chunks among the 100 and 1,000 unfiltered nearest);
* the pgvector grid P-a to P-h of section 6.2 and the Qdrant grid Q-a to Q-e of section 6.3, each
  build-time variant built three times, every query-time setting run on every build of its
  family (see PREREGISTRATION.md for which settings run where);
* EXPLAIN (ANALYZE, BUFFERS) on every short pgvector result and on 50 fixed questions; Qdrant's
  per-segment search-path counters (/telemetry) per person;
* every metric of section 6.5 per (setting, build, question): recall@5 and @10, empty and short
  results, gross misses, the similarity gap, the share of kb/ hits, latency (median of 3 passes),
  and the `complete` flag wardowl reported, with the confusion against the exact answer.

Every retrieval goes through wardowl's PermissionedRetriever, which re-checks every hit, and every
hit is checked again against the scenario's oracle and canary detector. An unreadable hit, a canary
of an unreadable document or a violation stops the run at once (exit code 3, LEAK.json).

Settings wardowl's backends do not expose are set on the store by this harness and reported as
harness-level settings: pgvector's hnsw.max_scan_tuples, hnsw.scan_mem_multiplier, work_mem,
enable_indexscan, plan_cache_mode and the CTE's inner LIMIT (in a subclass of PgVectorBackend that
adds them as SET LOCAL statements and SQL, like the backend's own two settings), psycopg's
prepare_threshold, the HNSW build parameters m and ef_construction, and Qdrant's collection
layouts. Qdrant's hnsw_ef, exact and ACORN go through QdrantBackend's own `search_params`.

    python x1_underretrieval.py --smoke            # a small corpus, one build, every code path
    python x1_underretrieval.py --resume           # the full grid, both stores
    python x1_underretrieval.py --stores qdrant --resume

Outputs (default /kaggle/working/x1, or /kaggle/working/x1-smoke) are written after every setting,
so a crash keeps what finished; --resume skips what is done. README.md lists every file.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import gzip
import hashlib
import json
import math
import re
import shutil
import time
import traceback
import types
import urllib.request
from collections import Counter, defaultdict
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import paper_common as pc
from paper_common import log

from wardowl import PermissionedRetriever, Query
from wardowl.backends.pgvector import PgVectorBackend, filter_to_sql

NAME = "wardowl_enterprise"  # the scenario's table and collection name (checked against enterprise_rag.NAME)
COMPANY, KNOWLEDGE = f"{NAME}_company", f"{NAME}_kb"  # the two collections of the separate-kb layout
QDRANT_URL = "http://127.0.0.1:6333"
STORES = ("pgvector", "qdrant")

PROBE_GROUPS = ("hr", "finance", "board", "engineering", "sre", "legal", "contractors", "employees")
PROBE_TENANTS = 3  # generated tenants per probe group
PROBE_FIQA = 4  # FiQA queries per probe person
PROBE_SEED = 61  # fixed, so every run asks the same probe questions
SMOKE_PEOPLE = ("northwind-eu-judy", "contoso-judy", "fabrikam-judy", "dave", "carol", "frank", "mallory")
SMOKE_PROBE_GROUPS = ("board", "employees", "contractors", "hr")
TIE = 1e-4  # the original run's tie tolerance for recall
FIXED_QUOTAS = (("judy", 15), ("kb-reader", 25), ("probe", 10))  # the 50 fixed EXPLAIN questions
MEASURES = (  # the numeric metrics of one retrieval, suffixed with its k (recall5, recall10, ...)
    "n",
    "recall",
    "empty",
    "short",
    "gross_miss",
    "sim_gap",
    "kb_share",
    "noncounting",
    "noncounting_kb",
    "complete",
    "false_complete",
    "false_incomplete",
)

# pgvector settings wardowl's PgVectorBackend does not take, and the server setting each one is.
PG_GUCS: dict[str, str] = {
    "max_scan_tuples": "hnsw.max_scan_tuples",
    "scan_mem_multiplier": "hnsw.scan_mem_multiplier",
    "work_mem": "work_mem",
    "enable_indexscan": "enable_indexscan",
    "plan_cache_mode": "plan_cache_mode",
}
PG_ASRUN: dict[str, Any] = {"ef_search": 100, "iterative_scan": "relaxed_order"}  # the original run
PG_DEFAULT_FAMILY = "hnsw-m16-efc64"
PG_FAMILIES = ((PG_DEFAULT_FAMILY, 16, 64, False), ("hnsw-m32-efc200", 32, 200, True))  # name, m, efc, core grid

# Qdrant's per-segment search counters in /telemetry (VectorIndexSearchesTelemetry).
COUNTERS = frozenset(
    {
        "unfiltered_plain",
        "unfiltered_hnsw",
        "unfiltered_sparse",
        "unfiltered_exact",
        "filtered_plain",
        "filtered_small_cardinality",
        "filtered_large_cardinality",
        "filtered_acorn",
        "filtered_exact",
        "filtered_sparse",
    }
)
ASRUN_FIELDS = ("allowed_users", "allowed_groups", "tenant")  # the original run's keyword indexes
ONE_SEGMENT_KB = 1_000_000  # max_segment_size for one-segment: the corpus's 330 MB of vectors fit in one
LAYOUTS: dict[str, str] = {
    "as-run": "enterprise_rag.QdrantStore.load, as the original run: wardowl's create_collection with keyword "
    "indexes on allowed_users, allowed_groups, tenant and wardowl_id, default HNSW (m 16, ef_construct 100) "
    "and optimizer, every chunk through QdrantBackend.add",
    "is-tenant": "as-run, but the tenant index is created with is_tenant=true (harness-level)",
    "tenant-m0": "is-tenant, with hnsw_config m=0 and payload_m=16: one graph per tenant value and no global "
    "graph (harness-level)",
    "separate-kb": "company documents and notices in one collection, the FiQA base in another, both created as "
    "as-run; each search queries both under the same filter and merges the hits by cosine score (harness-level)",
    "one-segment": "as-run, with optimizers_config default_segment_number=1 and max_segment_size 1,000,000 KB "
    "so the optimizer can merge everything into one segment (harness-level)",
}


# ---- settings ------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Setting:
    """One query-time configuration of a store.

    `harness` names the parameters wardowl's backend does not expose: this harness sets them on the
    store itself, and they are reported as harness-level. `first_build_only` marks exact search,
    which does not use the graph, so one build is enough.
    """

    id: str
    experiments: tuple[str, ...]
    params: dict[str, Any] = field(default_factory=dict)
    harness: tuple[str, ...] = ()
    first_build_only: bool = False

    def describe(self) -> dict[str, Any]:
        return {
            "experiments": list(self.experiments),
            "params": self.params,
            "harness_level": list(self.harness),
            "first_build_only": self.first_build_only,
        }


def pg_settings(core: bool) -> list[Setting]:
    """Section 6.2's query-time grid; `core` is the subset run on the second index family."""
    scan = ("max_scan_tuples", "scan_mem_multiplier")
    every = ("as run", "P-a", "P-b", "P-c", "P-d", "P-e", "P-f", "P-g", "P-h")
    grid = [Setting("p-asrun", every, dict(PG_ASRUN))]
    limits = ((20_000, 8), (100_000, 1), (100_000, 8), (1_000_000, 1), (1_000_000, 8), (1_000_000, 16))
    for tuples, multiplier in limits:
        params = {**PG_ASRUN, "max_scan_tuples": tuples, "scan_mem_multiplier": float(multiplier)}
        grid.append(Setting(f"pa-t{tuples // 1000}k-m{multiplier}", ("P-a", "P1"), params, scan))
    grid.append(Setting("pb-wm64", ("P-b", "P1"), {**PG_ASRUN, "work_mem": "64MB"}, ("work_mem",)))
    for ef in (40, 200, 400, 1000):
        grid.append(Setting(f"pc-ef{ef}", ("P-c", "P2"), {**PG_ASRUN, "ef_search": ef}))
    for factor in (4, 10):
        grid.append(Setting(f"pd-lim{factor}", ("P-d", "P2"), {**PG_ASRUN, "limit_factor": factor}, ("limit_factor",)))
    grid.append(Setting("pe-strict", ("P-e", "P2"), {**PG_ASRUN, "iterative_scan": "strict_order"}))
    custom = {**PG_ASRUN, "plan_cache_mode": "force_custom_plan"}
    grid.append(Setting("pg-custom", ("P-g", "P4"), custom, ("plan_cache_mode",)))
    noprepare = {**PG_ASRUN, "prepare_threshold": "none"}
    grid.append(Setting("pg-noprepare", ("P-g", "P4"), noprepare, ("prepare_threshold",)))
    exact = {**PG_ASRUN, "enable_indexscan": "off"}
    grid.append(Setting("ph-exact", ("P-h", "P3"), exact, ("enable_indexscan",), first_build_only=True))
    if core:
        keep = {"p-asrun", "pc-ef400", "pa-t1000k-m8", "pd-lim10"}
        grid = [s for s in grid if s.id in keep]
    return grid


def qdrant_settings(full: bool) -> list[Setting]:
    """Section 6.3's query-time grid; the layouts other than as-run run the first three and exact."""
    acorn = {"hnsw_ef": 128, "acorn": True}
    grid = [
        Setting("q-asrun", ("as run", "Q-a", "Q-b", "Q-d", "Q-e"), {"hnsw_ef": 128}),
        Setting("qa-acorn040", ("Q-a", "Q2"), {**acorn, "max_selectivity": 0.4}),
        Setting("qa-acorn100", ("Q-a", "Q1", "Q2"), {**acorn, "max_selectivity": 1.0}),
    ]
    if full:
        grid += [Setting("qb-ef64", ("Q-b",), {"hnsw_ef": 64}), Setting("qb-ef512", ("Q-b", "Q4"), {"hnsw_ef": 512})]
    grid.append(Setting("qc-exact", ("Q-c",), {"exact": True}, first_build_only=True))
    return grid


# ---- errors, observers and harness-level backends ---------------------------------------------------


class LeakError(RuntimeError):
    """A hit the person may not read, a canary of an unreadable document, or a wardowl violation."""

    def __init__(self, detail: dict[str, Any]) -> None:
        super().__init__(json.dumps(detail, default=str)[:2000])
        self.detail = detail


class Unsupported(RuntimeError):
    """The installed store or client does not support a setting; it is recorded, never skipped quietly."""


class LastEvent:
    """A wardowl observer that keeps the latest RetrievalEvent, for the time spent in the backend."""

    def __init__(self) -> None:
        self.event: Any = None

    def __call__(self, event: Any) -> None:
        self.event = event

    def search_ms(self) -> float:
        return float(self.event.search_ms) if self.event is not None else math.nan


class HarnessPgVector(PgVectorBackend):
    """wardowl's PgVectorBackend, plus the pgvector settings it does not expose (harness-level).

    The extra settings are issued as SET LOCAL statements in the search's own transaction, exactly
    as the backend issues hnsw.ef_search and hnsw.iterative_scan, so they apply to that search only.
    With `limit_factor` above 1 the CTE takes `limit_factor * k` candidates and the outer query keeps
    the first k after its exact sort, the analogue of Elasticsearch's num_candidates. With 1 the
    backend's own SQL runs unchanged.
    """

    def __init__(self, pool: Any, setting: Setting, table: str) -> None:
        params = setting.params
        super().__init__(
            pool, None, table=table, iterative_scan=params["iterative_scan"], ef_search=params["ef_search"]
        )
        self.extra = [(guc, str(params[name])) for name, guc in PG_GUCS.items() if params.get(name) is not None]
        self.limit_factor = int(params.get("limit_factor", 1))

    def _settings(self) -> list[Any]:
        from psycopg import sql

        statements = super()._settings()
        for guc, value in self.extra:
            statements.append(sql.SQL("SET LOCAL {} = {}").format(sql.SQL(guc), sql.Literal(value)))
        return statements

    def _query(self, query_vector: str, k: int, f: Any) -> tuple[Any, list[Any]]:
        if self.limit_factor == 1:
            return super()._query(query_vector, k, f)
        from psycopg import sql

        condition, params = filter_to_sql(f)
        statement = sql.SQL(
            "WITH candidates AS MATERIALIZED ("
            " SELECT id, content, metadata, embedding <=> %s::vector AS distance FROM {t}"
            " WHERE {cond} ORDER BY distance LIMIT %s)"
            " SELECT id, content, metadata, distance FROM candidates ORDER BY distance, id LIMIT %s"
        ).format(t=sql.Identifier(self.table), cond=sql.SQL(condition))
        return statement, [query_vector, *params, k * self.limit_factor, k]


class MergedBackend:
    """Several wardowl backends searched under the same filter, their hits merged by score (harness-level).

    For the separate-kb layout: a Qdrant collection of company documents and one of the shared FiQA
    base, both cosine, so the scores compare. wardowl still re-checks every merged hit.
    """

    supports_filters = True

    def __init__(self, parts: Sequence[Any]) -> None:
        self.parts = list(parts)

    def search(self, query: Any, k: int, filter: Any = None) -> list[Any]:
        hits = [hit for part in self.parts for hit in part.search(query, k, filter)]
        hits.sort(key=lambda h: (-h.score, h.id))
        return hits[:k]


# ---- small helpers -------------------------------------------------------------------------------


def same_value(have: str, want: Any) -> bool:
    """Whether a setting PostgreSQL reports equals the one asked for (as text, or as a number)."""
    have, text = have.strip().lower(), str(want).strip().lower()
    if have == text:
        return True
    try:
        return float(have) == float(text)
    except ValueError:
        return False


_EXPLAIN_BINDING = {"client": False}  # set once EXPLAIN with server-side parameters has been refused


def explain_json(conn: Any, command: Any, params: Sequence[Any]) -> tuple[Any, str]:
    """Runs an EXPLAIN (FORMAT JSON) and returns its document and how the parameters were bound.

    Parameters are bound by the server first, as the search binds them; if PostgreSQL refuses that
    for EXPLAIN, psycopg's client-side binding is used from then on, and that is said loudly.
    """
    import psycopg

    if not _EXPLAIN_BINDING["client"]:
        try:
            with conn.transaction():  # a savepoint inside the caller's transaction
                document = conn.execute(command, params).fetchone()[0]
            return (json.loads(document) if isinstance(document, (str, bytes)) else document), "server-side parameters"
        except psycopg.Error as error:
            _EXPLAIN_BINDING["client"] = True
            reason = f"{type(error).__name__}: {error}"
            log.loud(f"EXPLAIN with server-side parameters failed ({reason}); binding them client-side from now on")
    cursor = psycopg.ClientCursor(conn)
    cursor.execute(command, params)
    document = cursor.fetchone()[0]
    return (json.loads(document) if isinstance(document, (str, bytes)) else document), "client-side binding"


def numbered(text: str, count: int) -> str:
    """psycopg's %s placeholders as PostgreSQL's $1, $2, ..., for EXPLAIN (GENERIC_PLAN)."""
    numbers = iter(range(1, count + 1))
    converted = re.sub(r"%s", lambda _: f"${next(numbers)}", text)
    if next(numbers, None) is not None or "%s" in converted:
        raise ValueError(f"the statement does not hold {count} placeholders")
    return converted


def plan_shape(document: Any) -> str:
    """A plan's node types, depth first, with the index each one uses."""
    root = document[0] if isinstance(document, list) else document
    nodes = plan_nodes(root["Plan"])
    return ">".join(n.get("Node Type", "?") + (f"[{n['Index Name']}]" if "Index Name" in n else "") for n in nodes)


def plan_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    """A plan's nodes, depth first, the node itself first."""
    nodes = [node]
    for child in node.get("Plans", []):
        nodes += plan_nodes(child)
    return nodes


def parse_plan(document: Any, table: str) -> dict[str, Any]:
    """What EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) says about the scan of `table`."""
    root = document[0] if isinstance(document, list) else document
    top = root["Plan"]
    nodes = plan_nodes(top)
    scan = next((n for n in nodes if n.get("Relation Name") == table), {})
    actual = scan.get("Actual Rows")
    removed = scan.get("Rows Removed by Filter", 0) if scan else None
    return {
        "plan_shape": plan_shape(document),
        "uses_hnsw": any(str(n.get("Index Name", "")).endswith("_embedding_hnsw") for n in nodes),
        "scan_node": scan.get("Node Type"),
        "estimated_rows": scan.get("Plan Rows"),
        "actual_rows": actual,
        "removed_by_filter": removed,
        "removed_by_recheck": scan.get("Rows Removed by Index Recheck"),
        "rows_emitted": (actual or 0) + (removed or 0) if scan else None,
        "shared_hit_blocks": top.get("Shared Hit Blocks"),
        "shared_read_blocks": top.get("Shared Read Blocks"),
        "planning_ms": root.get("Planning Time"),
        "execution_ms": root.get("Execution Time"),
    }


def search_counters(document: Any) -> Counter[tuple[str, str]]:
    """Qdrant's search counters in a /telemetry document, summed by (JSON path, counter).

    Keyed by path as well, so a counter Qdrant reports both per segment and in an aggregate is not
    added twice: x1_stats.py chooses the per-segment path.
    """
    found: Counter[tuple[str, str]] = Counter()
    stack: list[tuple[Any, str]] = [(document, "")]
    while stack:
        node, path = stack.pop()
        if isinstance(node, dict):
            for key, value in node.items():
                if key in COUNTERS and isinstance(value, dict) and isinstance(value.get("count"), int):
                    found[(path, key)] += value["count"]
                else:
                    stack.append((value, f"{path}/{key}" if path else str(key)))
        elif isinstance(node, list):
            stack.extend((item, path) for item in node)
    return found


def counter_rows(person: str, before: Counter | None, after: Counter | None) -> list[dict[str, Any]]:
    """The counters that changed while one person's questions ran."""
    if before is None or after is None:
        return []
    rows = []
    for (path, name), value in after.items():
        delta = value - before.get((path, name), 0)
        if delta:
            rows.append({"person": person, "path": path, "counter": name, "count": int(delta)})
    return rows


def model_json(model: Any) -> Any:
    """A qdrant-client (pydantic) model as plain JSON."""
    dump = getattr(model, "model_dump_json", None) or getattr(model, "json", None)
    return json.loads(dump()) if dump else str(model)


def http_json(url: str, timeout: float = 60) -> Any:
    with urllib.request.urlopen(url, timeout=timeout) as response:  # noqa: S310 - the local Qdrant this run started
        return json.loads(response.read())


# ---- the experiment ------------------------------------------------------------------------------


class Experiment:
    """The scenario, the probe set, the question table and the sweep every store setting runs through."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.out: Path = args.out
        self.out.mkdir(parents=True, exist_ok=True)
        log.to(self.out / "x1.log")
        self.started = time.time()
        limit = self.started + args.max_hours * 3600
        self.deadline = min(limit, args.deadline) if args.deadline else limit
        options = {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()}
        self.manifest = pc.Manifest(self.out / "manifest.json", "X1: under-retrieval under permission filters", options)
        self.er = pc.scenario(args.repo)
        if self.er.NAME != NAME:
            raise RuntimeError(f"enterprise_rag.NAME is {self.er.NAME!r}, not {NAME!r}: update x1_underretrieval.py")
        self.run: Any = None
        self.checked = 0  # scenario checks already looked at
        self.questions = pd.DataFrame()
        self.active: list[int] = []
        self.qids_of: dict[str, list[int]] = {}
        self.person_order: list[str] = []
        self.fixed: list[int] = []
        self.people: dict[str, Any] = {}
        self.authorizer = self.er.tenant_acl()
        self.filters: dict[str, Any] = {}
        self.is_kb = np.zeros(0, dtype=bool)  # per chunk row: whether it is a FiQA passage
        self.durations: dict[str, list[float]] = defaultdict(list)
        if not args.resume:
            self.refuse_overwrite()

    # ---- bookkeeping -------------------------------------------------------------------------

    def refuse_overwrite(self) -> None:
        runs = self.out / "runs"
        clash = [p.name for s in self.args.stores for p in runs.glob(f"{s}__*")] if runs.is_dir() else []
        if clash:
            raise SystemExit(
                f"{self.out} already holds {len(clash)} results of {self.args.stores}; pass --resume to continue "
                "them, or --out to start elsewhere"
            )

    def name(self, store: str, layout: str, build: str, setting: str | None = None) -> str:
        return "__".join([store, layout, build, *([setting] if setting else [])])

    def setting_done(self, store: str, layout: str, build: str, setting: Setting) -> bool:
        """Done, unsupported, or failed: a failure is retried only with --retry-failed, since retrying it
        means rebuilding the whole build (and redoing every setting of it)."""
        path = self.out / "meta" / f"{self.name(store, layout, build, setting.id)}.json"
        if not path.is_file():
            return False
        finished = ("done", "unsupported") if self.args.retry_failed else ("done", "unsupported", "failed")
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("status") in finished
        except ValueError:
            return False

    def build_done(self, store: str, layout: str, build: str, settings: Sequence[Setting]) -> bool:
        return all(self.setting_done(store, layout, build, s) for s in settings)

    def discard_partial(self, store: str, layout: str, build: str) -> None:
        """Moves aside what an interrupted earlier attempt left of this build: a rebuild is a new graph,
        and results of two graphs must never be mixed under one build name."""
        prefix = f"{self.name(store, layout, build)}__"
        target = self.out / "discarded" / time.strftime("%Y%m%d-%H%M%S")
        moved = []
        for kind in ("runs", "meta", "explain", "explain_raw", "telemetry"):
            for path in sorted((self.out / kind).glob(f"{prefix}*")):
                (target / kind).mkdir(parents=True, exist_ok=True)
                path.replace(target / kind / path.name)
                moved.append(f"{kind}/{path.name}")
        if moved:
            self.manifest.warn(f"{store} {build} was partly done; moved {len(moved)} files to {target}, redoing it")

    def time_for(self, label: str, store: str) -> bool:
        """Whether there is time to start one more setting of this store before the deadline."""
        durations = self.durations[store]
        estimate = max(durations) if durations else 0.0
        left = self.deadline - time.time()
        if left > estimate:
            return True
        message = (
            f"skipped {label}: {left / 60:.0f} min left before the deadline, and a {store} setting took up to "
            f"{estimate / 60:.0f} min"
        )
        log.loud(message)
        self.manifest.add("skipped", {"what": label, "reason": message})
        return False

    def register(self, store: str, layout: str, grid: Sequence[Setting]) -> None:
        self.manifest.entry["settings"][f"{store}/{layout}"] = {s.id: s.describe() for s in grid}
        self.manifest.save()

    def require(self, step: str) -> None:
        """Stops when one of the scenario's own checks failed in `step`: the experiment needs all of it."""
        checks = self.run.report.checks
        failed = [(name, detail) for name, ok, detail in checks[self.checked :] if not ok]
        self.checked = len(checks)
        if failed:
            raise RuntimeError(f"{step}: the scenario's own checks failed: {failed}")

    def filter_of(self, persona: Any) -> Any:
        """The filter wardowl's policy gives this person (the original run's AllOf(Tenant, MetadataACL))."""
        if persona.id not in self.filters:
            self.filters[persona.id] = self.authorizer.filter_for(self.er.person_subject(persona), "read")
        return self.filters[persona.id]

    # ---- environment, corpus, embeddings, baseline -------------------------------------------

    def environment(self) -> None:
        env = self.er.environment(self.args.repo)
        env.update(
            pc.versions(
                ["pandas", "pyarrow", "scipy", "psycopg", "psycopg-pool", "qdrant-client", "datasets", "torch"]
            )
        )
        env["hardware"] = pc.hardware()
        path = str(env.get("wardowl_path"))
        env["wardowl_installed"] = ("site-packages" in path or "dist-packages" in path) and not path.startswith(
            str(self.args.repo)
        )
        if not env["wardowl_installed"]:
            self.manifest.warn(f"wardowl is imported from {path}, not from an installed package")
        for key, value in env.items():
            log(f"{key}: {value}")
        self.manifest.set("environment", env)
        seeds = {"run": self.args.seed, "fixed_explain": self.args.seed + 1, "probe": PROBE_SEED}
        self.manifest.set("seeds", {**seeds, "scenario": self.er.Config.seed})
        self.manifest.set("qdrant_layouts", LAYOUTS)

    def prepare(self) -> None:
        er = self.er
        cfg = er.Config(work=str(self.out), repo=str(self.args.repo), stores=STORES, remote_authorizers=())
        if self.args.smoke:
            cfg.variants, cfg.kb_limit = 4, 2000
        with self.manifest.stage("corpus") as record:
            self.run = er.Run(cfg)
            self.run.cache = self.args.cache
            self.run.cache.mkdir(parents=True, exist_ok=True)
            self.run.build_corpus()
            self.require("corpus")
            self.add_probes()
            self.people = {p.id: p for p in self.run.people}
            record.update(
                chunks=len(self.run.docs),
                people=len(self.run.people),
                questions=len(self.run.pairs),
                scenario_config=dataclasses.asdict(cfg),
            )
        with self.manifest.stage("embeddings") as record:
            record["copied_from_input"] = self.reuse_cache()
            before = set(self.run.cache.glob("chunks-*.npy"))
            self.run.embed()
            self.require("embeddings")
            created = sorted(str(p) for p in set(self.run.cache.glob("chunks-*.npy")) - before)
            record["computed"] = created
            if created and record["copied_from_input"]:
                self.manifest.warn("no cached embedding file matched this corpus: the chunks were embedded again")
            self.pin_query_vectors()
        with self.manifest.stage("exact baseline"):
            self.run.baseline()
            self.require("exact baseline")
        with self.manifest.stage("alignment variables") as record:
            self.questions = self.question_table()
            self.save_questions()
            record["questions"] = len(self.questions)
        self.choose_active()

    def fiqa_queries(self) -> list[str]:
        """BEIR FiQA's queries, for the probe set; their absence is recorded, not hidden."""
        try:
            from datasets import load_dataset

            data = load_dataset("BeIR/fiqa", "queries", split="queries")
            texts = sorted({t.strip() for t in data["text"] if t and t.strip()})
        except Exception as error:
            reason = f"{type(error).__name__}: {error}"
            self.manifest.warn(f"the FiQA queries did not load ({reason}); the probe set has no FiQA questions")
            self.manifest.add("unsupported", {"what": "probe FiQA queries", "reason": reason})
            return []
        log(f"{len(texts):,} FiQA queries for the probe set")
        return texts

    def add_probes(self) -> None:
        """Section 6.1's probe set, appended to the scenario's people and questions before embedding."""
        er, run = self.er, self.run
        rng = np.random.default_rng(PROBE_SEED)
        generated = [t for t in er.TENANT_IDS if t not in er.enterprise.TENANTS]
        by_kind: dict[tuple[str, str], list[Any]] = defaultdict(list)
        for d in run.docs:
            if d.kind in er.KINDS:
                by_kind[(d.tenants[0], d.kind)].append(d)
        queries = self.fiqa_queries()
        people, pairs = [], []
        for g, group in enumerate(PROBE_GROUPS):
            for j in range(PROBE_TENANTS):
                tenant = generated[(PROBE_TENANTS * g + j) % len(generated)]
                persona = er.Persona(f"{tenant}-probe-{group}", tenant, (group,), f"probe: only {group}")
                people.append(persona)
                for kind in sorted(er.KINDS):
                    docs = by_kind[(tenant, kind)]
                    d = docs[int(rng.integers(len(docs)))]
                    answerable = er.readable(persona, d)
                    pairs.append(
                        er.Pair(persona, d.question or "", "probe-template", d.id, d.fact, (kind,), answerable)
                    )
                if queries:
                    reads_kb = bool(set(persona.groups) & set(er.KB_READERS))
                    for index in rng.choice(len(queries), size=PROBE_FIQA, replace=False):
                        pairs.append(er.Pair(persona, queries[int(index)], "probe-fiqa", None, None, ("kb",), reads_kb))
        run.people += people
        run.pairs += pairs
        log(f"probe set: {len(people)} people, {len(pairs)} questions")
        self.manifest.set(
            "probe_set",
            {
                "people": [p.id for p in people],
                "questions": len(pairs),
                "groups": PROBE_GROUPS,
                "tenants_per_group": PROBE_TENANTS,
                "fiqa_per_person": PROBE_FIQA if queries else 0,
                "kb_only_note": "every group that reads the FiQA base (employees, contractors) also reads at least two "
                "handbook templates, so no KB-only person exists under the original metadata; the contractors and "
                "employees probes are the closest (R_kb / R is recorded per question)",
            },
        )

    def reuse_cache(self) -> list[str]:
        """Copies cached chunk embeddings of an attached earlier run into the cache folder."""
        copied = []
        for saved in pc.input_files("**/cache/chunks-*.npy"):
            target = self.run.cache / saved.name
            if not target.exists():
                shutil.copy(saved, target)
                copied.append(str(saved))
        log(f"cached embeddings copied from /kaggle/input: {copied or 'none'}")
        return copied

    def pin_query_vectors(self) -> None:
        """Uses the same query vectors in every invocation that writes to this folder.

        The pgvector and Qdrant cells run in separate processes; pinning the query vectors keeps
        their exact baselines, and so their recall, identical to the last bit.
        """
        run = self.run
        digest = hashlib.sha256("\0".join(p.question for p in run.pairs).encode()).hexdigest()
        vectors, meta = self.out / "query_vectors.npy", self.out / "query_vectors.json"
        if vectors.is_file() and meta.is_file():
            saved_digest = json.loads(meta.read_text(encoding="utf-8")).get("digest")
            saved = np.load(vectors)
            if saved_digest == digest and saved.shape == run.qvecs.shape:
                drift = float(np.abs(saved - run.qvecs).max())
                log(f"query vectors pinned from {vectors} (largest difference from this encoding: {drift:.2e})")
                run.qvecs = saved
                run.queries = [Query(text=p.question, vector=v) for p, v in zip(run.pairs, saved, strict=True)]
                return
            self.manifest.warn(f"{vectors} belongs to other questions; replaced")
        np.save(vectors, run.qvecs)
        pc.write_json(meta, {"digest": digest, "questions": len(run.pairs)})

    def alignment(self) -> dict[int, dict[str, Any]]:
        """R, r1, r5, r10, rho_100 and rho_1000 of every question, from exact ranking on the GPU."""
        import torch

        run = self.run
        device = run.embed_device
        corpus = torch.from_numpy(run.vectors).to(device)
        is_kb = torch.from_numpy(self.is_kb).to(device)
        by_person: dict[str, list[int]] = defaultdict(list)
        for i, pair in enumerate(run.pairs):
            by_person[pair.persona.id].append(i)
        out: dict[int, dict[str, Any]] = {}
        for person, idx in by_person.items():
            mask = torch.from_numpy(run.masks[person]).to(device)
            scores = torch.from_numpy(run.qvecs[idx]).to(device) @ corpus.T
            order = torch.argsort(scores, dim=1, descending=True)
            readable = mask[order]  # row j: whether each chunk, nearest first, is readable
            cumulative = readable.to(torch.int64).cumsum(dim=1)
            totals = cumulative[:, -1].tolist()
            # The rank at which the k-th readable chunk appears: one more than the positions before it.
            ranks = {k: ((cumulative < k).sum(dim=1) + 1).tolist() for k in (1, 5, 10)}
            kb_top10 = is_kb[order[:, :10]].float().mean(dim=1).tolist()
            rho = {m: readable[:, :m].float().mean(dim=1).tolist() for m in (100, 1000)}
            for j, i in enumerate(idx):
                record: dict[str, Any] = {"R_gpu": int(totals[j]), "unfiltered_kb_share10": kb_top10[j]}
                for k in (1, 5, 10):
                    record[f"r{k}"] = int(ranks[k][j]) if totals[j] >= k else None
                for m in (100, 1000):
                    record[f"rho{m}"] = rho[m][j]
                out[i] = record
            del scores, order, readable, cumulative
        del corpus, is_kb
        torch.cuda.empty_cache()
        return out

    def question_table(self) -> pd.DataFrame:
        run = self.run
        self.is_kb = np.array([d.id.startswith(pc.KB_PREFIX) for d in run.docs])
        aligned = self.alignment()
        rows = []
        for i, pair in enumerate(run.pairs):
            persona = pair.persona
            mask = run.masks[persona.id]
            readable = int(mask.sum())
            a = aligned[i]
            if a["R_gpu"] != readable:
                raise RuntimeError(f"question {i}: the GPU counts {a['R_gpu']} readable chunks, the oracle {readable}")
            exact_rows, exact_scores = run.exact[i]
            exact_ids = [run.docs[r].id for r in exact_rows]
            rows.append(
                {
                    "qid": i,
                    "person": persona.id,
                    "tenant": persona.tenant,
                    "groups": "|".join(persona.groups),
                    "persona_type": pc.persona_type(persona),
                    "category": pair.category,
                    "attack": pair.attack,
                    "region": pc.region(pair.category),
                    "answerable": bool(pair.answerable),
                    "target": pair.target or "",
                    "kinds": "|".join(pair.kinds),
                    "question": pair.question,
                    "R": readable,
                    "R_kb": int((mask & self.is_kb).sum()),
                    "r1": a["r1"],
                    "r5": a["r5"],
                    "r10": a["r10"],
                    "rho100": a["rho100"],
                    "rho1000": a["rho1000"],
                    "unfiltered_kb_share10": a["unfiltered_kb_share10"],
                    "exact_top1": exact_scores[0] if exact_scores else math.nan,
                    "exact_kb_share5": float(np.mean([e.startswith(pc.KB_PREFIX) for e in exact_ids[:5]]))
                    if exact_ids
                    else math.nan,
                    "exact10_ids": "|".join(exact_ids),
                    "exact10_scores": "|".join(f"{s:.6f}" for s in exact_scores),
                }
            )
        return pd.DataFrame(rows)

    def save_questions(self) -> None:
        """Writes questions.*, or checks that an earlier invocation's copy describes the same questions."""
        stem = self.out / "questions"
        existing = pc.read_table(stem)
        if existing is not None:
            key = ["qid", "person", "question", "R", "exact10_ids"]
            mine = self.questions[key].reset_index(drop=True)
            theirs = existing[key].reset_index(drop=True)
            if len(mine) != len(theirs) or not mine.astype(str).equals(theirs.astype(str)):
                raise RuntimeError(f"{stem} describes other questions or another exact baseline: use another --out")
            log(f"{stem}: the same questions and exact baseline as the earlier invocation")
            return
        pc.write_table(self.questions, stem)
        people = self.questions.groupby(["person", "tenant", "groups", "persona_type"], sort=False)
        people[["R", "R_kb"]].first().reset_index().to_csv(self.out / "people.csv", index=False)

    def choose_active(self) -> None:
        """The questions this invocation asks (all, or a smoke subset), the order of people and the
        fixed EXPLAIN sample."""
        run = self.run
        qids = list(range(len(run.pairs)))
        if self.args.smoke:
            keep = set(SMOKE_PEOPLE)
            first_probe: dict[str, str] = {}
            for p in run.people:
                if "-probe-" in p.id and p.groups[0] in SMOKE_PROBE_GROUPS:
                    first_probe.setdefault(p.groups[0], p.id)
            keep |= set(first_probe.values())
            qids = [i for i in qids if run.pairs[i].persona.id in keep]
        self.active = qids
        self.qids_of = defaultdict(list)
        for i in qids:
            self.qids_of[run.pairs[i].persona.id].append(i)
        persons = list(self.qids_of)
        order = np.random.default_rng(self.args.seed).permutation(len(persons))
        self.person_order = [persons[int(j)] for j in order]
        self.fixed = self.fixed_queries()
        log(f"{len(self.active):,} questions of {len(persons)} people; {len(self.fixed)} fixed EXPLAIN questions")
        self.manifest.set(
            "questions", {"active": len(self.active), "people": len(persons), "fixed_explain": self.fixed}
        )

    def fixed_queries(self) -> list[int]:
        """Section 6.2's 50 fixed questions for EXPLAIN: judys, KB readers and probe people, seeded."""
        table = self.questions.set_index("qid")
        scorable = [i for i in self.active if table.at[i, "R"] >= 1]
        wanted = self.args.explain_fixed
        rng = np.random.default_rng(self.args.seed + 1)
        chosen: list[int] = []
        for kind, quota in FIXED_QUOTAS:
            pool = [i for i in scorable if str(table.at[i, "persona_type"]).startswith(kind)]
            take = min(len(pool), round(quota * wanted / 50))
            chosen += [pool[int(j)] for j in rng.choice(len(pool), size=take, replace=False)] if take else []
        taken = set(chosen)
        rest = [i for i in scorable if i not in taken]
        missing = wanted - len(chosen)
        if missing > 0 and rest:
            chosen += [rest[int(j)] for j in rng.choice(len(rest), size=min(missing, len(rest)), replace=False)]
        chosen = sorted(chosen)[:wanted]
        table.loc[chosen, ["person", "persona_type", "category", "question"]].reset_index().to_csv(
            self.out / "fixed_queries.csv", index=False
        )
        return chosen

    # ---- retrieval, checks and metrics -------------------------------------------------------

    def check_safety(self, i: int, k: int, result: Any, label: str) -> None:
        """Every hit readable by the oracle, no canary of an unreadable document, no violation."""
        run, er = self.run, self.er
        persona = run.pairs[i].persona
        problems = []
        if result.violations:
            problems.append(f"wardowl's re-check removed {result.violations} hits: the store ignored the filter")
        for hit in result.hits:
            row = run.row_of.get(hit.id)
            if row is None:
                problems.append(f"{hit.id} is not in the corpus")
            elif not er.readable(persona, run.docs[row]):
                problems.append(f"{hit.id} is not readable by {persona.id}")
            leaked = run.detector.leaks(persona, hit.text)
            if leaked:
                problems.append(f"{hit.id} holds canaries of {leaked}")
        if problems:
            raise LeakError({"setting": label, "question": i, "person": persona.id, "k": k, "problems": problems})

    def retrieve(self, retriever: Any, timer: LastEvent, i: int, k: int, label: str) -> tuple[Any, float, float]:
        pair = self.run.pairs[i]
        clock = time.perf_counter()
        result = retriever.retrieve(self.run.queries[i], self.er.person_subject(pair.persona), k=k)
        elapsed = (time.perf_counter() - clock) * 1000
        self.check_safety(i, k, result, label)
        return result, elapsed, timer.search_ms()

    def sweep(
        self, label: str, backend: Any, telemetry: Callable[[], Counter | None] | None = None
    ) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
        """Every active question under one setting: k=5 in `passes` timed passes, k=10 in the first.

        People take turns in a seeded order, each asking all their questions; Qdrant's counters
        are read after each person of the first pass, so they can be attributed to people.
        """
        timer = LastEvent()
        retriever = PermissionedRetriever(backend, self.er.tenant_acl(), observers=[timer])
        order = [i for person in self.person_order for i in self.qids_of[person]]
        for i in order[:10]:  # warm-up, untimed, as the original run did
            try:
                warm = retriever.retrieve(self.run.queries[i], self.er.person_subject(self.run.pairs[i].persona), k=5)
            except Exception as error:
                log(f"  {label}: warm-up error on question {i}: {type(error).__name__}: {error}")
                continue
            self.check_safety(i, 5, warm, f"{label} warm-up")

        first5: dict[int, Any] = {}
        first10: dict[int, Any] = {}
        times: dict[int, list[float]] = defaultdict(list)
        backend_ms: dict[int, list[float]] = defaultdict(list)
        unstable: set[int] = set()
        errors: dict[int, str] = {}
        telemetry_rows: list[dict[str, Any]] = []
        previous = telemetry() if telemetry else None
        started, calls = time.perf_counter(), 0
        for p in range(self.args.passes):
            done = 0
            for person in self.person_order:
                for i in self.qids_of[person]:
                    if i in errors:
                        continue
                    try:
                        r5, ms, search_ms = self.retrieve(retriever, timer, i, 5, label)
                        r10 = self.retrieve(retriever, timer, i, 10, label)[0] if p == 0 else None
                    except LeakError:
                        raise
                    except Exception as error:
                        errors[i] = f"pass {p + 1}: {type(error).__name__}: {error}"
                        continue
                    calls += 2 if p == 0 else 1
                    times[i].append(ms)
                    backend_ms[i].append(search_ms)
                    if p == 0:
                        first5[i], first10[i] = r5, r10
                    elif [h.id for h in r5.hits] != [h.id for h in first5[i].hits]:
                        unstable.add(i)
                    done += 1
                    if p == 0 and done % 250 == 0:
                        log(f"  {label}: {done} of {len(order)} questions ({time.perf_counter() - started:.0f} s)")
                if p == 0 and telemetry is not None:
                    current = telemetry()
                    telemetry_rows += counter_rows(person, previous, current)
                    previous = current
            log(f"  {label}: pass {p + 1} of {self.args.passes} ({time.perf_counter() - started:.0f} s)")
        if errors:
            examples = list(errors.values())[:3]
            self.manifest.warn(f"{label}: {len(errors)} of {len(order)} questions raised errors, e.g. {examples}")
        if order and len(errors) == len(order):
            raise RuntimeError(f"{label}: every retrieval failed, e.g. {next(iter(errors.values()))}")
        rows = [
            self.score(i, first5.get(i), first10.get(i), times[i], backend_ms[i], i in unstable, errors.get(i, ""))
            for i in self.active
        ]
        info = {
            "questions": len(order),
            "retrievals": calls,
            "errors": len(errors),
            "error_examples": list(errors.values())[:5],
            "unstable_k5": len(unstable),
            "passes": self.args.passes,
            "sweep_seconds": round(time.perf_counter() - started, 1),
        }
        return pd.DataFrame(rows), pd.DataFrame(telemetry_rows), info

    def score(
        self,
        i: int,
        r5: Any,
        r10: Any,
        times: list[float],
        backend_ms: list[float],
        unstable: bool,
        error: str,
    ) -> dict[str, Any]:
        pair = self.run.pairs[i]
        measured = [t for t in backend_ms if not math.isnan(t)]
        row: dict[str, Any] = {
            "qid": i,
            "person": pair.persona.id,
            "error": error,
            "latency_ms": float(np.median(times)) if times else math.nan,
            "latency_passes": "|".join(f"{t:.3f}" for t in times),
            "search_ms": float(np.median(measured)) if measured else math.nan,
            "unstable5": float(unstable),
        }
        row.update(self.measure(i, r5, 5))
        row.update(self.measure(i, r10, 10))
        ids = row["hits5"].split("|") if row["hits5"] else []
        found = pair.target and pair.answerable and r5 is not None
        row["target_found5"] = float(pair.target in ids) if found else math.nan
        return row

    def measure(self, i: int, result: Any, k: int) -> dict[str, Any]:
        """Section 6.5's metrics of one retrieval, against the exact top k of what the person may read."""
        if result is None:
            return {**{f"{n}{k}": math.nan for n in MEASURES}, f"strategy{k}": "", f"hits{k}": ""}
        run = self.run
        pair = run.pairs[i]
        mask, query = run.masks[pair.persona.id], run.qvecs[i]
        exact_rows, exact_scores = run.exact[i]
        want = min(k, len(exact_rows))
        hits = list(result.hits)[:k]
        floor = exact_scores[want - 1] - TIE if want else math.inf
        best = exact_scores[0] - TIE if want else math.inf
        sims: list[float] = []
        counting = noncounting = noncounting_kb = 0
        best_found = False
        for hit in hits:
            row = run.row_of.get(hit.id)
            sim = float(run.vectors[row] @ query) if row is not None else math.nan
            sims.append(sim)
            readable = row is not None and bool(mask[row])
            if readable and sim >= floor:
                counting += 1
            else:
                noncounting += 1
                noncounting_kb += hit.id.startswith(pc.KB_PREFIX)
            best_found = best_found or (readable and sim >= best)
        recall = run._recall(i, hits, k)  # the original run's recall, reused
        if recall is not None and abs(min(counting, want) / want - recall) > 1e-9:
            log.once("recall-mismatch", f"question {i}: this harness's count disagrees with enterprise_rag's recall")
        n = len(hits)
        exact_ok = recall == 1.0 if want else n == 0
        complete = bool(result.complete)
        finite = [s for s in sims if not math.isnan(s)]
        return {
            f"n{k}": n,
            f"recall{k}": math.nan if recall is None else float(recall),
            f"empty{k}": float(n == 0) if want else math.nan,
            f"short{k}": float(n < want) if want else math.nan,
            f"gross_miss{k}": float(not best_found) if want else math.nan,
            f"sim_gap{k}": float(np.mean(exact_scores[:want]) - np.mean(finite)) if want and finite else math.nan,
            f"kb_share{k}": sum(h.id.startswith(pc.KB_PREFIX) for h in hits) / n if n else math.nan,
            f"noncounting{k}": noncounting,
            f"noncounting_kb{k}": noncounting_kb,
            f"complete{k}": float(complete),
            f"false_complete{k}": float(complete and not exact_ok),
            f"false_incomplete{k}": float(not complete and exact_ok),
            f"strategy{k}": result.strategy,
            f"hits{k}": "|".join(h.id for h in hits),
        }

    # ---- one setting, written as soon as it is done ------------------------------------------

    def guarded(
        self, store: str, layout: str, build: str, rep: int, setting: Setting, action: Callable[..., dict[str, Any]]
    ) -> None:
        """Runs one setting and writes its tables and meta file; a failure is recorded and the run goes
        on, except a leak, which stops everything."""
        label = f"{store} {build} {setting.id}"
        if not self.time_for(label, store):
            return
        name = self.name(store, layout, build, setting.id)
        meta: dict[str, Any] = {
            "store": store,
            "layout": layout,
            "build": build,
            "rep": rep,
            "setting": setting.id,
            **setting.describe(),
            "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
        log(f"-- {label}: {setting.params}")
        clock = time.perf_counter()
        try:
            result = action(layout, build, rep, setting)
        except LeakError:
            raise
        except Unsupported as error:
            self.manifest.warn(f"{label} is not supported here: {error}")
            self.manifest.add("unsupported", {"setting": label, "reason": str(error)})
            pc.write_json(self.out / "meta" / f"{name}.json", {**meta, "status": "unsupported", "reason": str(error)})
            return
        except Exception as error:
            trace = traceback.format_exc()
            log(trace)
            self.manifest.warn(f"{label} failed: {type(error).__name__}: {error}")
            self.manifest.add("failures", {"setting": label, "error": f"{type(error).__name__}: {error}"})
            pc.write_json(self.out / "meta" / f"{name}.json", {**meta, "status": "failed", "trace": trace})
            return
        seconds = time.perf_counter() - clock
        self.durations[store].append(seconds)
        columns = {"store": store, "layout": layout, "build": build, "rep": rep, "setting": setting.id}
        files = {}
        for kind in ("runs", "explain", "telemetry"):
            frame = result.get(kind)
            if frame is None or frame.empty:
                continue
            frame = pd.concat([pd.DataFrame(columns, index=frame.index), frame], axis=1)
            files[kind] = str(pc.write_table(frame, self.out / kind / name))
        if result.get("explain_raw"):
            path = self.out / "explain_raw" / f"{name}.jsonl.gz"
            path.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(path, "wt", encoding="utf-8") as out:
                for record in result["explain_raw"]:
                    out.write(json.dumps(record, default=str) + "\n")
            files["explain_raw"] = str(path)
        runs = result["runs"]
        scorable = runs[runs["recall10"].notna()]
        summary = {
            "recall5": float(scorable["recall5"].mean()) if len(scorable) else None,
            "recall10": float(scorable["recall10"].mean()) if len(scorable) else None,
            "err5": float(scorable["empty5"].mean()) if len(scorable) else None,
            "short5": float(scorable["short5"].mean()) if len(scorable) else None,
            "latency_p50_ms": float(runs["latency_ms"].median()),
        }
        exact = setting.params.get("exact") or setting.params.get("enable_indexscan") == "off"
        if exact and summary["recall10"] is not None and summary["recall10"] < 0.999:
            self.manifest.warn(f"{label}: the exact reference reached recall@10 {summary['recall10']:.4f}, not 1.0")
        meta.update(
            status="done", seconds=round(seconds, 1), summary=summary, files=files, **result.get("meta", {})
        )
        pc.write_json(self.out / "meta" / f"{name}.json", meta)  # written last: it marks the setting done
        log(
            f"   {label}: recall@5 {summary['recall5']}, recall@10 {summary['recall10']}, ERR {summary['err5']}, "
            f"p50 {summary['latency_p50_ms']:.1f} ms, {seconds:.0f} s"
        )


# ---- pgvector ------------------------------------------------------------------------------------


class PgVectorStage:
    """Section 6.2: PostgreSQL + pgvector as enterprise_rag starts and loads it, then the grid."""

    store = "pgvector"

    def __init__(self, x: Experiment) -> None:
        self.x, self.er, self.run = x, x.er, x.run
        self.url = self.run.cfg.pg_url
        self.fresh_index = False  # whether the index enterprise_rag's load built is still in place

    def notice(self, diagnostic: Any) -> None:
        log(f"  PostgreSQL {diagnostic.severity}: {diagnostic.message_primary}")

    def configure(self, conn: Any) -> None:
        conn.add_notice_handler(self.notice)

    def execute(self) -> None:
        store = self.er.PgVectorStore(self.run)
        try:
            with self.x.manifest.stage("pgvector: start and load") as record:
                store.start()
                load = store.load()  # wardowl's create_schema, add and HNSW build, as the original run
                rows = store.count()
                if rows != len(self.run.docs):
                    raise RuntimeError(f"pgvector holds {rows} chunks, not {len(self.run.docs)}")
                self.fresh_index = True
                record.update(load=load, server=self.server_info())
            with self.x.manifest.stage("pgvector: filter estimates"):
                self.filter_estimates()
            for family, m, efc, core in PG_FAMILIES:
                grid = pg_settings(core)
                self.x.register(self.store, family, grid)
                for rep in range(self.x.args.builds):
                    self.build(family, m, efc, rep, grid, load)
        finally:
            store.stop()

    def server_info(self) -> dict[str, Any]:
        import psycopg

        names = (
            "shared_buffers",
            "work_mem",
            "maintenance_work_mem",
            "effective_cache_size",
            "max_parallel_workers_per_gather",
            "max_parallel_maintenance_workers",
            "jit",
            "random_page_cost",
            "plan_cache_mode",
            "enable_indexscan",
            "hnsw.ef_search",
            "hnsw.iterative_scan",
            "hnsw.max_scan_tuples",
            "hnsw.scan_mem_multiplier",
        )
        with psycopg.connect(self.url, autocommit=True) as conn:
            conn.execute("SELECT '[1]'::vector")  # loads pgvector, which defines the hnsw.* settings
            values = {n: conn.execute("SELECT current_setting(%s, true)", [n]).fetchone()[0] for n in names}
            values["server_version"] = conn.execute("SHOW server_version").fetchone()[0]
            version = conn.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'").fetchone()
            values["pgvector"] = version[0] if version else None
        for name in ("hnsw.max_scan_tuples", "hnsw.scan_mem_multiplier"):
            if values.get(name) is None:
                self.x.manifest.warn(f"pgvector {values['pgvector']} does not define {name}: P-a will be unsupported")
                self.x.manifest.add("unsupported", {"what": name, "reason": f"pgvector {values['pgvector']}"})
        log(f"PostgreSQL settings: {values}")
        return values

    def filter_estimates(self) -> None:
        """P3: the planner's row estimate for each person's filter alone, against the oracle's count."""
        import psycopg
        from psycopg import sql

        rows = []
        with psycopg.connect(self.url, autocommit=True) as conn:
            for person in self.x.person_order:
                persona = self.x.people[person]
                condition, params = filter_to_sql(self.x.filter_of(persona))
                command = sql.SQL("EXPLAIN (FORMAT JSON) SELECT 1 FROM {} WHERE {}").format(
                    sql.Identifier(NAME), sql.SQL(condition)
                )
                document, binding = explain_json(conn, command, params)
                plan = (document[0] if isinstance(document, list) else document)["Plan"]
                readable = int(self.run.masks[person].sum())
                rows.append(
                    {
                        "person": person,
                        "persona_type": pc.persona_type(persona),
                        "R": readable,
                        "estimated_rows": plan.get("Plan Rows"),
                        "plan_node": plan.get("Node Type"),
                        "ratio": plan.get("Plan Rows", math.nan) / readable if readable else math.nan,
                        "binding": binding,
                    }
                )
        pc.write_table(pd.DataFrame(rows), self.x.out / "pg_filter_estimates")

    def build(self, family: str, m: int, efc: int, rep: int, grid: list[Setting], load: dict[str, Any]) -> None:
        build = f"{family}-b{rep}"
        todo = [s for s in grid if rep == 0 or not s.first_build_only]
        if self.x.args.resume and self.x.build_done(self.store, family, build, todo):
            log(f"pgvector {build}: every setting is done already (--resume)")
            return
        if not self.x.time_for(f"pgvector {build}", self.store):
            return
        self.x.discard_partial(self.store, family, build)
        try:
            with self.x.manifest.stage(f"pgvector {build}") as record:
                record.update(self.index(family, m, efc, rep, load))
                pc.write_json(self.x.out / "builds" / f"{self.x.name(self.store, family, build)}.json", record)
                for setting in todo:
                    self.x.guarded(self.store, family, build, rep, setting, self.setting)
        except LeakError:
            raise
        except Exception as error:  # a failed build is recorded; the next one still runs
            log(traceback.format_exc())
            self.x.manifest.warn(f"pgvector {build} failed: {type(error).__name__}: {error}")
            failure = {"setting": f"pgvector {build}", "error": f"{type(error).__name__}: {error}"}
            self.x.manifest.add("failures", failure)

    def index(self, family: str, m: int, efc: int, rep: int, load: dict[str, Any]) -> dict[str, Any]:
        """The HNSW index of this build: enterprise_rag's own for the first default build, else rebuilt."""
        import psycopg
        from psycopg import sql

        index = f"{NAME}_embedding_hnsw"
        info: dict[str, Any] = {"store": self.store, "layout": family, "rep": rep, "m": m, "ef_construction": efc}
        if family == PG_DEFAULT_FAMILY and rep == 0 and self.fresh_index:
            info["builder"] = (
                "enterprise_rag.PgVectorStore.load: wardowl's create_schema(hnsw=True) after the bulk load, as the "
                "original run (pgvector's defaults m 16, ef_construction 64)"
            )
            info["seconds"] = load.get("index_s")
        else:
            with psycopg.connect(self.url, autocommit=True) as conn:
                conn.add_notice_handler(self.notice)
                conn.execute(sql.SQL("DROP INDEX IF EXISTS {}").format(sql.Identifier(index)))
                clock = time.perf_counter()
                create = sql.SQL(
                    "CREATE INDEX {} ON {} USING hnsw (embedding vector_cosine_ops)"
                    " WITH (m = {}, ef_construction = {})"
                )
                names = (sql.Identifier(index), sql.Identifier(NAME))
                conn.execute(create.format(*names, sql.Literal(m), sql.Literal(efc)))
                info["seconds"] = round(time.perf_counter() - clock, 1)
                conn.execute(sql.SQL("ANALYZE {}").format(sql.Identifier(NAME)))
            info["builder"] = (
                "harness: DROP INDEX, CREATE INDEX ... USING hnsw WITH (m, ef_construction), ANALYZE "
                "(wardowl's create_schema takes neither m nor ef_construction)"
            )
        self.fresh_index = False
        with psycopg.connect(self.url, autocommit=True) as conn:
            found = conn.execute(
                "SELECT pg_relation_size(c.oid), c.reloptions FROM pg_class c WHERE c.relname = %s", [index]
            ).fetchone()
        if found is None:
            raise RuntimeError(f"the index {index} is missing after the build")
        info.update(index_bytes=int(found[0]), reloptions=found[1])
        log(f"pgvector index {family} build {rep}: {info}")
        return info

    def setting(self, family: str, build: str, rep: int, setting: Setting) -> dict[str, Any]:
        from psycopg_pool import ConnectionPool

        # One connection, so prepared statements and their plans are observable; a fresh pool per
        # setting, so no setting inherits another's prepared statements.
        kwargs = {"prepare_threshold": None} if setting.params.get("prepare_threshold") == "none" else {}
        pool = ConnectionPool(
            self.url, min_size=1, max_size=1, open=True, kwargs=kwargs, max_lifetime=86_400.0, configure=self.configure
        )
        try:
            pool.wait(timeout=60)
            backend = HarnessPgVector(pool, setting, NAME)
            effective = self.effective(pool, backend, setting)
            label = f"pgvector {build} {setting.id}"
            runs, _, info = self.x.sweep(label, backend)
            info["prepared_statements"] = self.prepared(pool)
            explain, raw = self.explain_all(pool, backend, runs, label)
        finally:
            pool.close()
        return {"runs": runs, "explain": explain, "explain_raw": raw, "meta": {**info, "effective_settings": effective}}

    def effective(self, pool: Any, backend: HarnessPgVector, setting: Setting) -> dict[str, Any]:
        """The settings inside a search's transaction; a refused or ignored one makes the setting unsupported."""
        from psycopg import errors

        names = ["hnsw.ef_search", "hnsw.iterative_scan", *PG_GUCS.values()]
        # Only a refusal of the setting itself makes it unsupported; a lost connection is a failure.
        refused = (errors.UndefinedObject, errors.InvalidParameterValue, errors.InvalidName, errors.FeatureNotSupported)
        try:
            with pool.connection() as conn, conn.transaction():
                conn.execute("SELECT '[1]'::vector")
                for statement in backend._settings():
                    conn.execute(statement)
                values = {n: conn.execute("SELECT current_setting(%s, true)", [n]).fetchone()[0] for n in names}
                values["prepare_threshold"] = str(conn.prepare_threshold)
        except refused as error:
            raise Unsupported(f"PostgreSQL refused the settings: {type(error).__name__}: {error}") from error
        params = setting.params
        wanted = {"hnsw.ef_search": params["ef_search"], "hnsw.iterative_scan": params["iterative_scan"]}
        wanted |= {guc: params.get(name) for name, guc in PG_GUCS.items()}
        for guc, want in wanted.items():
            have = values.get(guc)
            if want is not None and (have is None or not same_value(have, want)):
                raise Unsupported(f"{guc} is {have!r} inside the search's transaction, not {want!r}")
        if params.get("prepare_threshold") == "none" and values["prepare_threshold"] != "None":
            raise Unsupported(f"psycopg's prepare_threshold is {values['prepare_threshold']}, not None")
        return values

    def prepared(self, pool: Any) -> dict[str, Any]:
        """P4: the search statements psycopg prepared on the connection, and how often PostgreSQL ran each
        with a generic and with a custom plan. Only statements of the search count: psycopg also
        prepares the SET LOCAL statements, which always run with a generic plan and mean nothing here."""
        with pool.connection() as conn:
            rows = conn.execute(
                "SELECT name, generic_plans, custom_plans, statement FROM pg_prepared_statements"
            ).fetchall()
        search = [
            {"name": name, "generic_plans": int(generic), "custom_plans": int(custom)}
            for name, generic, custom, statement in rows
            if "WITH candidates" in statement
        ]
        return {
            "statements": len(rows),
            "search_statements": len(search),
            "search_generic_plans": sum(s["generic_plans"] for s in search),
            "search_custom_plans": sum(s["custom_plans"] for s in search),
            "per_search_statement": search,
        }

    def explain_all(
        self, pool: Any, backend: HarnessPgVector, runs: pd.DataFrame, label: str
    ) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
        """EXPLAIN (ANALYZE, BUFFERS) of the fixed questions (k=5) and of every short result, empty ones
        first (P1 reads the scan's reach from them); for the fixed questions also the generic plan."""
        targets = [(i, 5, "fixed") for i in self.x.fixed]
        hits = runs.set_index("qid")
        shorts = [(int(i), k, "short") for k in (5, 10) for i in runs.loc[runs[f"short{k}"] == 1, "qid"]]
        shorts.sort(key=lambda t: (hits.at[t[0], f"n{t[1]}"] != 0, t[1], t[0]))
        cap = self.x.args.explain_short_cap
        if len(shorts) > cap:
            self.x.manifest.warn(f"{label}: {len(shorts)} short results; EXPLAIN covers {cap}, empty ones first")
            shorts = shorts[:cap]
        rows, raw = [], []
        for i, k, reason in [*targets, *shorts]:
            base = {"qid": i, "person": self.run.pairs[i].persona.id, "k": k, "reason": reason}
            base["n_hits"] = hits.at[i, f"n{k}"]
            try:
                document, binding = self.explain(pool, backend, i, k)
            except Exception as error:
                log.once(f"explain {label}", f"{label}: EXPLAIN failed ({type(error).__name__}: {error})")
                rows.append({**base, "error": f"{type(error).__name__}: {error}"})
                continue
            row = {**base, **parse_plan(document, NAME), "binding": binding, "error": ""}
            if reason == "fixed":
                try:
                    generic = self.generic_plan(pool, backend, i, k)
                    row.update(generic_plan_shape=plan_shape(generic), generic_error="")
                    raw.append({**base, "generic_plan": generic})
                except Exception as error:
                    reason_text = f"{type(error).__name__}: {error}"
                    log.once(f"generic {label}", f"{label}: EXPLAIN (GENERIC_PLAN) failed ({reason_text})")
                    row.update(generic_plan_shape="", generic_error=reason_text)
            rows.append(row)
            raw.append({**base, "plan": document})
        return pd.DataFrame(rows), raw

    def generic_plan(self, pool: Any, backend: HarnessPgVector, i: int, k: int) -> Any:
        """P4: the plan PostgreSQL would use for the search statement once it switches to a generic plan.

        EXPLAIN with bound values always shows a custom plan, so the statement is explained with
        GENERIC_PLAN (PostgreSQL 16) and $n placeholders, sent without values over the simple query
        protocol (prepare=False: preparing it would make PostgreSQL expect values).
        """
        vector = backend._query_vector(self.run.queries[i])
        statement, params = backend._query(vector, k, self.x.filter_of(self.run.pairs[i].persona))
        with pool.connection() as conn:
            command = "EXPLAIN (GENERIC_PLAN, FORMAT JSON) " + numbered(statement.as_string(conn), len(params))
            with conn.transaction():
                for setting in backend._settings():
                    conn.execute(setting)
                document = conn.execute(command, prepare=False).fetchone()[0]
        return json.loads(document) if isinstance(document, (str, bytes)) else document

    def explain(self, pool: Any, backend: HarnessPgVector, i: int, k: int) -> tuple[Any, str]:
        from psycopg import sql

        pair = self.run.pairs[i]
        vector = backend._query_vector(self.run.queries[i])
        statement, params = backend._query(vector, k, self.x.filter_of(pair.persona))
        command = sql.SQL("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ") + statement
        with pool.connection() as conn, conn.transaction():
            for setting in backend._settings():
                conn.execute(setting)
            return explain_json(conn, command, params)


# ---- Qdrant --------------------------------------------------------------------------------------


class QdrantStage:
    """Section 6.3: Qdrant as enterprise_rag starts it, each layout built three times, then the grid."""

    store = "qdrant"

    def __init__(self, x: Experiment) -> None:
        self.x, self.er, self.run = x, x.er, x.run
        self.holder: Any = None  # enterprise_rag.QdrantStore, whose client and load this stage uses
        self.acorn_counter_seen = False
        self.telemetry_failed = False
        self.company_rows = [r for r, d in enumerate(self.run.docs) if not d.id.startswith(pc.KB_PREFIX)]
        self.kb_rows = [r for r, d in enumerate(self.run.docs) if d.id.startswith(pc.KB_PREFIX)]

    @property
    def client(self) -> Any:
        return self.holder.client

    def execute(self) -> None:
        from qdrant_client import QdrantClient

        self.holder = self.er.QdrantStore(self.run)
        try:
            with self.x.manifest.stage("qdrant: start") as record:
                self.holder.start()  # benchmarks/kaggle_stores.sh qdrant: the release build of the original run
                self.holder.client = QdrantClient(url=QDRANT_URL, timeout=600)
                record["server"] = http_json(f"{QDRANT_URL}/")
                record["acorn_in_client"] = self.acorn_in_client()
                log(f"Qdrant server: {record['server']}")
            for layout in self.x.args.layouts:
                grid = qdrant_settings(full=layout == "as-run")
                self.x.register(self.store, layout, grid)
                for rep in range(self.x.args.builds):
                    self.build(layout, rep, grid)
        finally:
            with contextlib.suppress(Exception):
                self.drop()
            self.holder.stop()

    def acorn_in_client(self) -> bool:
        from qdrant_client import models

        fields = getattr(models.SearchParams, "model_fields", None) or getattr(models.SearchParams, "__fields__", {})
        supported = hasattr(models, "AcornSearchParams") and "acorn" in fields
        if not supported:
            self.x.manifest.warn("this qdrant-client has no ACORN search parameters: the ACORN settings will not run")
            missing = {"what": "ACORN in qdrant-client", "reason": "AcornSearchParams is missing"}
            self.x.manifest.add("unsupported", missing)
        return supported

    def build(self, layout: str, rep: int, grid: list[Setting]) -> None:
        build = f"{layout}-b{rep}"
        todo = [s for s in grid if rep == 0 or not s.first_build_only]
        if self.x.args.resume and self.x.build_done(self.store, layout, build, todo):
            log(f"qdrant {build}: every setting is done already (--resume)")
            return
        if not self.x.time_for(f"qdrant {build}", self.store):
            return
        self.x.discard_partial(self.store, layout, build)
        try:
            with self.x.manifest.stage(f"qdrant {build}") as record:
                record.update(self.load(layout, rep))
                pc.write_json(self.x.out / "builds" / f"{self.x.name(self.store, layout, build)}.json", record)
                for setting in todo:
                    self.x.guarded(self.store, layout, build, rep, setting, self.setting)
        except LeakError:
            raise
        except Exception as error:  # a failed build is recorded; the next one still runs
            log(traceback.format_exc())
            self.x.manifest.warn(f"qdrant {build} failed: {type(error).__name__}: {error}")
            failure = {"setting": f"qdrant {build}", "error": f"{type(error).__name__}: {error}"}
            self.x.manifest.add("failures", failure)
        finally:
            try:
                self.drop()
            except Exception as error:  # the next build's load will fail loudly if Qdrant is gone
                log(f"  could not drop the collections of {build}: {type(error).__name__}: {error}")

    def drop(self) -> None:
        if self.holder is None or getattr(self.holder, "client", None) is None:
            return
        for name in (NAME, COMPANY, KNOWLEDGE):
            if self.client.collection_exists(name):
                self.client.delete_collection(name)

    def load(self, layout: str, rep: int) -> dict[str, Any]:
        """Creates and fills this build's collections, then waits until Qdrant has indexed them."""
        self.drop()
        clock = time.perf_counter()
        if layout == "as-run":
            loaded = self.holder.load()  # wardowl's create_collection, add_all, wait until green: the original
            names = [NAME]
        else:
            names = self.create(layout)
            if layout == "separate-kb":
                loaded = {"company_s": self.add(COMPANY, self.company_rows), "kb_s": self.add(KNOWLEDGE, self.kb_rows)}
            else:
                loaded = {"load_s": self.add(NAME, None)}
        self.wait_indexed(names)
        counts = {n: int(self.client.count(n, exact=True).count) for n in names}
        if sum(counts.values()) != len(self.run.docs):
            raise RuntimeError(f"Qdrant holds {counts} points, not {len(self.run.docs)}")
        infos = {n: model_json(self.client.get_collection(n)) for n in names}
        snapshot = self.telemetry()
        if snapshot is not None:
            path = self.x.out / "telemetry_raw" / f"{self.x.name(self.store, layout, f'{layout}-b{rep}')}.json.gz"
            path.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(path, "wt", encoding="utf-8") as out:
                json.dump(snapshot, out)
        segments = {n: infos[n].get("segments_count") if isinstance(infos[n], dict) else None for n in names}
        log(f"qdrant {layout} build {rep}: {counts} points, segments {segments}")
        return {
            "store": self.store,
            "layout": layout,
            "rep": rep,
            "builder": LAYOUTS[layout],
            "loaded": loaded,
            "seconds": round(time.perf_counter() - clock, 1),
            "points": counts,
            "segments": segments,
            "collections": infos,
        }

    def create(self, layout: str) -> list[str]:
        """Harness-level collection layouts. wardowl's create_collection still makes the payload
        indexes: it creates a collection only when none exists, and adds the indexes either way."""
        from qdrant_client import models

        from wardowl.backends.qdrant import create_collection

        dim = self.run.dim
        if layout == "separate-kb":
            for name in (COMPANY, KNOWLEDGE):
                create_collection(self.client, name, dim, keyword_fields=ASRUN_FIELDS)
            return [COMPANY, KNOWLEDGE]
        vectors = models.VectorParams(size=dim, distance=models.Distance.COSINE)
        hnsw = models.HnswConfigDiff(m=0, payload_m=16) if layout == "tenant-m0" else None
        optimizers = None
        if layout == "one-segment":
            optimizers = models.OptimizersConfigDiff(default_segment_number=1, max_segment_size=ONE_SEGMENT_KB)
        self.client.create_collection(NAME, vectors_config=vectors, hnsw_config=hnsw, optimizers_config=optimizers)
        fields: tuple[str, ...] = ASRUN_FIELDS
        if layout in ("is-tenant", "tenant-m0"):
            tenant = models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True)
            self.client.create_payload_index(NAME, "metadata.tenant", field_schema=tenant)
            fields = ("allowed_users", "allowed_groups")
        create_collection(self.client, NAME, dim, keyword_fields=fields)
        return [NAME]

    def add(self, collection: str, rows: list[int] | None) -> float:
        """Writes chunks through wardowl's QdrantBackend.add, with enterprise_rag's own loader."""
        from wardowl.backends.qdrant import QdrantBackend

        source = self.run
        if rows is not None:
            source = types.SimpleNamespace(docs=[self.run.docs[r] for r in rows], vectors=self.run.vectors[rows])
        return float(self.er.add_all(QdrantBackend(self.client, collection, None), source))

    def wait_indexed(self, names: Sequence[str], timeout: float = 7200.0) -> None:
        """Until every collection is green with the same counts over four checks, 5 s apart."""
        deadline = time.monotonic() + timeout
        last: Any = None
        stable = 0
        while True:
            infos = [self.client.get_collection(n) for n in names]
            green = all(str(i.status).lower().endswith("green") for i in infos)
            state = tuple((i.points_count, i.indexed_vectors_count, i.segments_count) for i in infos)
            stable = stable + 1 if green and state == last else 0
            if stable >= 3:
                log(f"  Qdrant indexed: {dict(zip(names, state, strict=True))}")
                return
            if time.monotonic() > deadline:
                raise TimeoutError(f"Qdrant did not finish indexing {list(names)} within {timeout:.0f} s: {state}")
            last = state
            time.sleep(5)

    def telemetry(self) -> Any:
        try:
            return http_json(f"{QDRANT_URL}/telemetry?details_level=10")
        except (OSError, ValueError) as error:
            if not self.telemetry_failed:
                self.telemetry_failed = True
                self.x.manifest.warn(f"Qdrant's /telemetry did not answer ({type(error).__name__}: {error})")
                self.x.manifest.add("unsupported", {"what": "Qdrant telemetry", "reason": str(error)})
            return None

    def counters(self) -> Counter | None:
        document = self.telemetry()
        if document is None:
            return None
        found = search_counters(document)
        if any(name == "filtered_acorn" for _, name in found):
            self.acorn_counter_seen = True
        return found

    def search_params(self, setting: Setting) -> Any:
        from qdrant_client import models

        params = setting.params
        if params.get("exact"):
            return models.SearchParams(exact=True)
        if not params.get("acorn"):
            return models.SearchParams(hnsw_ef=params["hnsw_ef"])
        if not hasattr(models, "AcornSearchParams"):
            raise Unsupported("this qdrant-client has no AcornSearchParams")
        try:
            acorn = models.AcornSearchParams(enable=True, max_selectivity=params["max_selectivity"])
            return models.SearchParams(hnsw_ef=params["hnsw_ef"], acorn=acorn)
        except Exception as error:  # pydantic refuses a field this client does not know
            raise Unsupported(f"qdrant-client refused ACORN parameters: {type(error).__name__}: {error}") from error

    def backend(self, layout: str, params: Any) -> Any:
        from wardowl.backends.qdrant import QdrantBackend

        if layout == "separate-kb":
            parts = [QdrantBackend(self.client, c, None, search_params=params) for c in (COMPANY, KNOWLEDGE)]
            return MergedBackend(parts)
        return QdrantBackend(self.client, NAME, None, search_params=params)

    def setting(self, layout: str, build: str, rep: int, setting: Setting) -> dict[str, Any]:
        backend = self.backend(layout, self.search_params(setting))
        probe = self.x.fixed[0] if self.x.fixed else self.x.active[0]
        retriever = PermissionedRetriever(backend, self.er.tenant_acl())
        label = f"qdrant {build} {setting.id}"
        subject = self.er.person_subject(self.run.pairs[probe].persona)
        try:
            result = retriever.retrieve(self.run.queries[probe], subject)
        except Exception as error:
            # A refusal of the request (400, 422) means the server does not support the setting; any
            # other error (a timeout, a crash) is a failure, recorded as such and retried on request.
            if getattr(error, "status_code", None) in (400, 422):
                raise Unsupported(f"Qdrant refused {setting.params}: {type(error).__name__}: {error}") from error
            raise
        self.x.check_safety(probe, 5, result, f"{label} probe")
        runs, telemetry, info = self.x.sweep(label, backend, self.counters)
        if setting.params.get("acorn"):
            total = int(telemetry.loc[telemetry["counter"] == "filtered_acorn", "count"].sum()) if len(telemetry) else 0
            info["acorn_searches_counted"] = total
            info["acorn_counter_seen"] = self.acorn_counter_seen
            if not total:
                self.x.manifest.warn(
                    f"{label}: ACORN was asked for, but Qdrant's telemetry counted no ACORN search (its gate never "
                    "opened, or this version does not count them)"
                )
        info["telemetry"] = not self.telemetry_failed
        return {"runs": runs, "telemetry": telemetry, "meta": info}


# ---- main ----------------------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Experiment X1: under-retrieval under permission filters")
    parser.add_argument("--out", type=Path, default=None, help="default /kaggle/working/x1 (x1-smoke with --smoke)")
    parser.add_argument("--stores", default=",".join(STORES), help="pgvector, qdrant or both, comma-separated")
    parser.add_argument("--layouts", default=",".join(LAYOUTS), help="Qdrant layouts, comma-separated")
    parser.add_argument("--smoke", action="store_true", help="small corpus, few people, one build: every code path")
    parser.add_argument("--builds", type=int, default=None, help="builds per build-time variant (3; 1 with --smoke)")
    parser.add_argument("--passes", type=int, default=None, help="timed k=5 passes (3; 2 with --smoke)")
    parser.add_argument("--seed", type=int, default=pc.SEED, help="person order and the fixed EXPLAIN sample")
    parser.add_argument("--cache", type=Path, default=Path("/kaggle/working/cache"), help="embedding cache folder")
    parser.add_argument("--resume", action="store_true", help="skip settings already done in --out")
    parser.add_argument("--retry-failed", action="store_true", help="with --resume, redo builds with failed settings")
    parser.add_argument("--max-hours", type=float, default=10.0, help="start no setting after this many hours")
    parser.add_argument("--deadline", type=float, default=None, help="and none after this Unix time (the session's)")
    parser.add_argument("--explain-fixed", type=int, default=None, help="fixed EXPLAIN questions (50; 10 with --smoke)")
    parser.add_argument("--explain-short-cap", type=int, default=200, help="most short results EXPLAINed per setting")
    parser.add_argument("--repo", type=Path, default=pc.REPO, help="the wardowl checkout holding acceptance/kaggle")
    args = parser.parse_args(argv)
    args.stores = tuple(s.strip() for s in args.stores.split(",") if s.strip())
    args.layouts = tuple(s.strip() for s in args.layouts.split(",") if s.strip())
    unknown = sorted({*args.stores} - set(STORES)) + sorted({*args.layouts} - set(LAYOUTS))
    if unknown:
        parser.error(f"unknown stores or layouts: {unknown}")
    smoke = args.smoke
    args.out = args.out or Path("/kaggle/working/x1-smoke" if smoke else "/kaggle/working/x1")
    args.builds = args.builds or (1 if smoke else 3)
    args.passes = args.passes or (2 if smoke else 3)
    args.explain_fixed = args.explain_fixed if args.explain_fixed is not None else (10 if smoke else 50)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    x = Experiment(args)
    try:
        x.environment()
        x.prepare()
        stages = {"pgvector": PgVectorStage, "qdrant": QdrantStage}
        for store in args.stores:
            try:
                stages[store](x).execute()
            except LeakError:
                raise
            except Exception as error:
                trace = traceback.format_exc()
                log(trace)
                x.manifest.warn(f"{store} stopped: {type(error).__name__}: {error}")
                x.manifest.add("failures", {"setting": f"{store} stage", "error": f"{type(error).__name__}: {error}"})
    except LeakError as leak:
        pc.write_json(args.out / "LEAK.json", leak.detail)
        log.loud(f"A PERMISSION LEAK OR VIOLATION STOPPED THE RUN: {leak.detail} (details in {args.out / 'LEAK.json'})")
        x.manifest.finish("leak")
        return 3
    except BaseException:
        x.manifest.finish("failed")
        raise
    failures = x.manifest.entry["failures"]
    x.manifest.finish("done" if not failures else "done with failures")
    log(
        f"X1 finished in {(time.time() - x.started) / 3600:.2f} h: {len(failures)} failures, "
        f"{len(x.manifest.entry['unsupported'])} unsupported, {len(x.manifest.entry['skipped'])} skipped "
        f"(see {args.out / 'manifest.json'})"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
