"""X7: revocation latency end to end, and fail-closed behaviour under faults (PREREG_X4_X7.md).

    python benchmarks/paper/x7_revocation_faults.py revocation --paths openfga,spicedb-ml --profile smoke --out results
    python benchmarks/paper/x7_revocation_faults.py faults --targets openfga --profile smoke --out results

`revocation` (X7a): for each path (a source of truth and a way to revoke in it) and cache condition, a
user reads one target chunk through one grant; the cache is warmed, the grant is revoked, and
retrieval is polled until the target stops appearing. `faults` (X7b): retrieval runs in a closed loop
while a fault is injected into the authorizer or the store (the server killed and restarted, or the
fault-injection proxy refusing, holding, delaying or altering its answers), and every answer is
checked against an oracle.

Every trial and episode is one JSON line in `<out>/x7-<job>.jsonl`. The servers come from
.github/workflows/paper-x4-x7.yml.
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import os
import random
import re
import sys
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from x4x7_common import (
    JOB,
    POLICIES,
    RUN_ID,
    Errors,
    OpaProcess,
    OpenFGAAdmin,
    ProxyProcess,
    Records,
    SpiceDBAdmin,
    annotate,
    clock,
    docker,
    healthy,
    log,
    run_info,
    versions_record,
    wait_for,
)
from x4x7_world import (
    LEVELS,
    OPENFGA_FULL_MODEL,
    SPICEDB_PREFIX,
    SPICEDB_SCHEMA,
    Fact,
    Model,
    World,
    WorldSize,
    clustered_vectors,
    exact_top,
    levels_for,
    make_world,
    metadata_for,
    model_for,
    openfga_tuple,
    rebac_facts,
    spicedb_relationship,
)

from wardowl import (
    AuthorizationError,
    CachingAuthorizer,
    Document,
    MetadataACLAuthorizer,
    PermissionedRetriever,
    Query,
    Subject,
)
from wardowl.authorizers._http import CircuitBreaker
from wardowl.authorizers.cerbos import CerbosAuthorizer
from wardowl.authorizers.opa import OPAAuthorizer
from wardowl.authorizers.openfga import OpenFGAAuthorizer
from wardowl.authorizers.spicedb import SpiceDBAuthorizer

OPENFGA_URL = os.environ.get("X4X7_OPENFGA_URL", "http://127.0.0.1:8080")
OPENFGA_CACHED_URL = os.environ.get("X4X7_OPENFGA_CACHED_URL", "http://127.0.0.1:8090")
SPICEDB_URL = os.environ.get("X4X7_SPICEDB_URL", "http://127.0.0.1:8443")
SPICEDB_TOKEN = os.environ.get("X4X7_SPICEDB_TOKEN", "wo-test")
CERBOS_URL = os.environ.get("X4X7_CERBOS_URL", "http://127.0.0.1:3592")
CERBOS_WATCH_DIR = Path(os.environ.get("X4X7_CERBOS_WATCH_DIR", "/tmp/cerbos-x7"))  # noqa: S108 - CI sets it
PG_URL = os.environ.get("X4X7_PG_URL", "postgresql://test:test@127.0.0.1:5432/test")
QDRANT_URL = os.environ.get("X4X7_QDRANT_URL", "http://127.0.0.1:6333")
REDIS_URL = os.environ.get("X4X7_REDIS_URL", "redis://127.0.0.1:6379/0")

SETTINGS: dict[str, dict[str, Any]] = {
    "full": {
        "seeds": 5,
        "trials": 8,
        "background": 100,
        "poll": 0.05,
        "settle": 3,
        "grace": 15.0,
        "episodes": 2,
        "baseline": 3.0,
        "fault": 12.0,
        "recover_max": 30.0,
        "recover_max_down": 90.0,
        "stable": 3.0,
        "watchdog": 10.0,
        "world": WorldSize(tenants=2, users_per_tenant=10, groups=10, folders=10, docs=300),
        "pairs": 10,
        "dim": 32,
    },
    "smoke": {
        "seeds": 1,
        "trials": 1,
        "background": 30,
        "poll": 0.05,
        "settle": 3,
        "grace": 15.0,
        "episodes": 1,
        "baseline": 1.5,
        "fault": 3.0,
        "recover_max": 10.0,
        "recover_max_down": 60.0,
        "stable": 1.0,
        "watchdog": 10.0,
        "world": WorldSize(tenants=2, users_per_tenant=6, groups=6, folders=6, docs=120),
        "pairs": 4,
        "dim": 16,
    },
}

CONDITIONS = ("nocache", "ttl5", "ttl30", "ttl30-inv", "ttl30-shared-inv")
CONDITION_CODES = {"nocache": "n", "ttl5": "a", "ttl30": "b", "ttl30-inv": "c", "ttl30-shared-inv": "d"}
# The cache's part of the stated bound: its ttl, nothing after invalidate(), local_ttl for a replica.
CACHE_BOUND = {"nocache": 0.0, "ttl5": 5.0, "ttl30": 30.0, "ttl30-inv": 0.0, "ttl30-shared-inv": 1.0}
LOCAL_TTL = 1.0

ENGINE_FAULTS = (
    "down",
    "refuse",
    "blackhole",
    "slow-200",
    "slow-1000",
    "slow-3000",
    "http500",
    "http503",
    "truncate",
    "empty",
    "garbage-json",
    "type-flip",
    "drop-last",
    "allow-all",
)
GUARDED_FAULTS = ("down", "refuse", "blackhole", "slow-3000", "http500")  # also under breaker and cache30
STORE_FAULTS = {
    "pgvector": ("down", "refuse", "blackhole", "slow-200", "slow-1000"),
    "qdrant": ("down", "refuse", "blackhole", "slow-200", "slow-1000", "http500", "http503", "truncate"),
}
HOST = re.compile(r"https?://|\b(?:\d{1,3}\.){3}\d{1,3}\b|localhost|\[::1\]|:\d{2,5}\b")


@dataclass
class Context:
    settings: dict[str, Any]
    records: Records
    errors: Errors
    out: Path
    profile: str

    def seeds(self) -> range:
        return range(self.settings["seeds"])


def _settings_for_record(settings: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(settings)
    out["world"] = vars(settings["world"])
    return out


def _normalized(vector: Any) -> list[float]:
    import numpy as np

    v = np.asarray(vector, dtype="float32")
    return (v / np.linalg.norm(v)).tolist()


def _redis() -> Any:
    import redis

    return redis.Redis.from_url(REDIS_URL)


# ==== X7a: revocation ==================================================================================


@dataclass
class Trial:
    seed: int
    condition: str
    index: int
    user: str
    target: str
    background: list[str]
    vector: list[float] = field(default_factory=list)


class RevocationPath:
    """A source of truth and a way to revoke in it (PREREG_X4_X7.md, X7a)."""

    name = ""
    staleness: float | None = 0.0  # None: no bound stated
    metadata_path = False

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.backend: Any = None
        self.vectors: dict[str, list[float]] = {}

    def setup(self) -> None:
        """Connect; load models or policies."""

    def provision(self, seed: int, trials: Sequence[Trial], docs: Sequence[str]) -> None:
        """Write every trial's grants and the store's chunks for one seed."""
        raise NotImplementedError

    def authorizer(self) -> Any:
        raise NotImplementedError

    def subject(self, trial: Trial) -> Subject:
        return Subject(trial.user)

    def revoke(self, trial: Trial) -> None:
        raise NotImplementedError

    def close(self) -> None:
        """Remove what the path made."""

    def bound(self, condition: str) -> float | None:
        if self.metadata_path:
            return 0.0
        if self.staleness is None:
            return None
        return CACHE_BOUND[condition] + self.staleness

    # A FAISS store, for the paths whose permissions live in an engine.
    def faiss(self, docs: Sequence[str], metadata: Callable[[str], dict[str, Any]]) -> Any:
        from wardowl.backends.faiss import FaissBackend

        dim = len(next(iter(self.vectors.values())))
        backend = FaissBackend(None, dim)
        backend.add([Document(d, "", metadata(d)) for d in docs], embeddings=[self.vectors[d] for d in docs])
        return backend


def _grants(trials: Sequence[Trial]) -> dict[str, list[str]]:
    """Document -> the users it is shared with."""
    shared: dict[str, list[str]] = collections.defaultdict(list)
    for t in trials:
        shared[t.target].append(t.user)
        for d in t.background:
            shared[d].append(t.user)
    return shared


class OpenFGAPath(RevocationPath):
    def __init__(self, ctx: Context, name: str, url: str, consistency: str, staleness: float) -> None:
        super().__init__(ctx)
        self.name = name
        self.url = url
        self.consistency = consistency
        self.staleness = staleness
        self.admin = OpenFGAAdmin(OPENFGA_URL)  # writes go to the plain server; both read one datastore
        self.store = ""
        self.model_id = ""

    def setup(self) -> None:
        self.store = self.admin.create_store(f"x7-{RUN_ID}-{self.name}")
        self.model_id = self.admin.write_model(self.store, OPENFGA_FULL_MODEL)

    def provision(self, seed: int, trials: Sequence[Trial], docs: Sequence[str]) -> None:
        tuples = [{"user": "tenant:rt0", "relation": "tenant", "object": f"document:{d}"} for d in docs]
        tuples += [{"user": f"user:{t.user}", "relation": "member", "object": "tenant:rt0"} for t in trials]
        for doc, users in _grants(trials).items():
            tuples += [{"user": f"user:{u}", "relation": "reader", "object": f"document:{doc}"} for u in users]
        self.admin.write_all(self.store, self.model_id, tuples)
        self.backend = self.faiss(docs, lambda d: {"doc_id": d})

    def authorizer(self) -> Any:
        return OpenFGAAuthorizer(self.url, self.store, authorization_model_id=self.model_id,
                                 consistency=self.consistency, contextual_groups=False)

    def revoke(self, trial: Trial) -> None:
        key = {"user": f"user:{trial.user}", "relation": "reader", "object": f"document:{trial.target}"}
        self.admin.write(self.store, self.model_id, deletes=[key])

    def close(self) -> None:
        if self.store:
            self.admin.delete_store(self.store)


class SpiceDBPath(RevocationPath):
    def __init__(self, ctx: Context, name: str, consistency: Mapping[str, Any], staleness: float) -> None:
        super().__init__(ctx)
        self.name = name
        self.consistency = dict(consistency)
        self.staleness = staleness
        self.admin = SpiceDBAdmin(SPICEDB_URL, SPICEDB_TOKEN)

    def setup(self) -> None:
        self.admin.write_schema(SPICEDB_SCHEMA)

    @staticmethod
    def _reader(user: str, doc: str) -> Fact:
        return ("document", doc, "reader", "user", user, "")

    def provision(self, seed: int, trials: Sequence[Trial], docs: Sequence[str]) -> None:
        facts: list[Fact] = [("document", d, "tenant", "tenant", "rt0", "") for d in docs]
        facts += [("tenant", "rt0", "member", "user", t.user, "") for t in trials]
        for doc, users in _grants(trials).items():
            facts += [self._reader(u, doc) for u in users]
        self.admin.touch_all([spicedb_relationship(f) for f in facts])
        time.sleep(6.0)  # past the 5-s quantization window, so minimizeLatency reads see the grants
        self.backend = self.faiss(docs, lambda d: {"doc_id": d})

    def authorizer(self) -> Any:
        return SpiceDBAuthorizer(SPICEDB_URL, SPICEDB_TOKEN, resource_type=f"{SPICEDB_PREFIX}/document",
                                 subject_type=f"{SPICEDB_PREFIX}/user", group_type=f"{SPICEDB_PREFIX}/group",
                                 consistency=self.consistency)

    def revoke(self, trial: Trial) -> None:
        relationship = spicedb_relationship(self._reader(trial.user, trial.target))
        self.admin.write([{"operation": "OPERATION_DELETE", "relationship": relationship}])


class OPAPath(RevocationPath):
    """OPA with the x4rel policy: `opa-data` revokes by replacing the document's sharing in OPA data,
    `opa-policy` by uploading a new version of the policy module that denies the user."""

    DENY_LINE = "deny_users := set() # x7: deny_users"

    def __init__(self, ctx: Context, name: str, opa: OpaProcess) -> None:
        super().__init__(ctx)
        self.name = name
        self.opa = opa
        self.package = "x7data" if name == "opa-data" else "x7pol"
        source = (POLICIES / "opa" / "x4rel.rego").read_text(encoding="utf-8")
        if self.DENY_LINE not in source:
            raise RuntimeError("x4rel.rego no longer has the deny_users line X7 rewrites")
        self.template = source.replace("package x4rel", f"package {self.package}").replace(
            "data.x4rel_world", f"data.{self.package}_world"
        )
        self.denied: list[str] = []
        self.shares: dict[str, list[str]] = {}

    def _policy(self) -> str:
        if not self.denied:
            return self.template
        names = ", ".join(f'"{u}"' for u in self.denied)
        return self.template.replace(self.DENY_LINE, f"deny_users := {{{names}}} # x7: deny_users")

    def setup(self) -> None:
        self.opa.put_policy(self.package, self._policy())

    def provision(self, seed: int, trials: Sequence[Trial], docs: Sequence[str]) -> None:
        self.shares = {d: sorted(u) for d, u in _grants(trials).items()}
        world = {
            "parents": {},
            "folders": {},
            "up": {},
            "shares": {d: {"users": users, "groups": [], "wildcard": False} for d, users in self.shares.items()},
        }
        self.opa.put_data(f"{self.package}_world", world)
        self.backend = self.faiss(
            docs, lambda d: {"doc_id": d, "tenant": "rt0", "owner": "nobody", "classification": LEVELS[0]}
        )

    def authorizer(self) -> Any:
        return OPAAuthorizer(self.opa.url, decisions_path=f"{self.package}/decisions", filter_path=f"{self.package}/filter")

    def subject(self, trial: Trial) -> Subject:
        return Subject(trial.user, (), {"tenant": "rt0", "clearance": 3})

    def revoke(self, trial: Trial) -> None:
        if self.name == "opa-data":
            users = [u for u in self.shares.get(trial.target, []) if u != trial.user]
            self.shares[trial.target] = users
            share = {"users": users, "groups": [], "wildcard": False}
            self.opa.put_data(f"{self.package}_world/shares/{trial.target}", share)
        else:
            self.denied.append(trial.user)
            self.opa.put_policy(self.package, self._policy())


class CerbosPath(RevocationPath):
    """Cerbos with a policy file it watches: each trial user has a role of its own, which the allow
    rule names; revoking rewrites the file without that role, and Cerbos reloads it."""

    name = "cerbos-policy"
    staleness = None

    def __init__(self, ctx: Context) -> None:
        super().__init__(ctx)
        self.roles: list[str] = []
        self.staging = CERBOS_WATCH_DIR.parent / f"{CERBOS_WATCH_DIR.name}-staging"

    @staticmethod
    def role(user: str) -> str:
        return f"r-{user}"

    def _write(self) -> None:
        roles = ", ".join(f'"{r}"' for r in ["keep", *self.roles])
        text = (
            "apiVersion: api.cerbos.dev/v1\n"
            "resourcePolicy:\n"
            "  version: default\n"
            "  resource: x7doc\n"
            "  rules:\n"
            '    - actions: ["read"]\n'
            "      effect: EFFECT_ALLOW\n"
            f"      roles: [{roles}]\n"
            "      condition:\n"
            "        match:\n"
            "          expr: request.principal.id in request.resource.attr.allowed_users\n"
        )
        self.staging.mkdir(parents=True, exist_ok=True)
        temporary = self.staging / "x7doc.yaml"
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, CERBOS_WATCH_DIR / "x7doc.yaml")  # atomic: Cerbos never reads half a file

    def setup(self) -> None:
        CERBOS_WATCH_DIR.mkdir(parents=True, exist_ok=True)
        wait_for(lambda: healthy(f"{CERBOS_URL}/_cerbos/health"), 60, what="Cerbos health")

    def provision(self, seed: int, trials: Sequence[Trial], docs: Sequence[str]) -> None:
        shares = _grants(trials)
        self.roles = [self.role(t.user) for t in trials]
        self._write()
        self.backend = self.faiss(docs, lambda d: {"doc_id": d, "allowed_users": sorted(shares.get(d, []))})
        # Wait until Cerbos has loaded this seed's file: the first trial's user reads its target.
        probe, check = trials[0], self.authorizer()
        hit = self.backend.search(Query(vector=self.vectors[probe.target]), 1)
        wait_for(lambda: check.check(self.subject(probe), hit) == [True], 60, what="Cerbos policy reload")

    def authorizer(self) -> Any:
        return CerbosAuthorizer(CERBOS_URL, resource_kind="x7doc", roles=lambda s: [self.role(s.id)])

    def revoke(self, trial: Trial) -> None:
        self.roles = [r for r in self.roles if r != self.role(trial.user)]
        self._write()


class MetadataPath(RevocationPath):
    """Permissions copied into chunk metadata: `MetadataACLAuthorizer`, and `set_metadata` revokes."""

    metadata_path = True

    def __init__(self, ctx: Context, name: str) -> None:
        super().__init__(ctx)
        self.name = name
        self.meta: dict[str, dict[str, Any]] = {}
        self.client: Any = None
        self.pool: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        if self.name == "acl-pgvector":
            import psycopg_pool

            self.pool = psycopg_pool.ConnectionPool(PG_URL, min_size=1, max_size=4, open=True, timeout=30)
        else:
            import qdrant_client

            self.client = qdrant_client.QdrantClient(url=QDRANT_URL, timeout=30)

    def provision(self, seed: int, trials: Sequence[Trial], docs: Sequence[str]) -> None:
        shares = _grants(trials)
        self.meta = {d: {"doc_id": d, "allowed_users": sorted(shares.get(d, [])), "allowed_groups": []} for d in docs}
        documents = [Document(d, "", self.meta[d]) for d in docs]
        embeddings = [self.vectors[d] for d in docs]
        dim = len(embeddings[0])
        name = f"x7acl_{seed}_{RUN_ID}".replace("-", "_")
        self.made.append(name)
        if self.name == "acl-pgvector":
            from wardowl.backends.pgvector import PgVectorBackend, create_schema

            create_schema(self.pool, dim, table=name, hnsw=False)
            self.backend = PgVectorBackend(self.pool, None, table=name, iterative_scan=None)
        else:
            from wardowl.backends.qdrant import QdrantBackend, create_collection

            create_collection(self.client, name, dim)
            self.backend = QdrantBackend(self.client, name)
        self.backend.add(documents, embeddings=embeddings)

    def authorizer(self) -> Any:
        return MetadataACLAuthorizer()

    def revoke(self, trial: Trial) -> None:
        new = dict(self.meta[trial.target])
        new["allowed_users"] = [u for u in new["allowed_users"] if u != trial.user]
        self.meta[trial.target] = new
        self.backend.set_metadata({trial.target: new})

    def close(self) -> None:
        for name in self.made:
            with contextlib.suppress(Exception):
                if self.pool is not None:
                    with self.pool.connection() as conn:
                        conn.execute(f'DROP TABLE IF EXISTS "{name}"')
                elif self.client is not None:
                    self.client.delete_collection(name)
        if self.pool is not None:
            self.pool.close()


def make_paths(ctx: Context, names: Sequence[str], opa: OpaProcess | None) -> list[RevocationPath]:
    paths: list[RevocationPath] = []
    for name in names:
        if name == "openfga":
            paths.append(OpenFGAPath(ctx, name, OPENFGA_URL, "HIGHER_CONSISTENCY", 0.0))
        elif name == "openfga-cached-hc":
            paths.append(OpenFGAPath(ctx, name, OPENFGA_CACHED_URL, "HIGHER_CONSISTENCY", 0.0))
        elif name == "openfga-cached-ml":
            paths.append(OpenFGAPath(ctx, name, OPENFGA_CACHED_URL, "MINIMIZE_LATENCY", 10.0))
        elif name == "spicedb-fc":
            paths.append(SpiceDBPath(ctx, name, {"fullyConsistent": True}, 0.0))
        elif name == "spicedb-ml":
            paths.append(SpiceDBPath(ctx, name, {"minimizeLatency": True}, 5.5))
        elif name in ("opa-data", "opa-policy"):
            assert opa is not None
            paths.append(OPAPath(ctx, name, opa))
        elif name == "cerbos-policy":
            paths.append(CerbosPath(ctx))
        elif name in ("acl-pgvector", "acl-qdrant"):
            paths.append(MetadataPath(ctx, name))
        else:
            raise ValueError(f"unknown path {name!r}")
    return paths


def _trials(path: RevocationPath, seed: int, settings: Mapping[str, Any]) -> tuple[list[Trial], list[str]]:
    rng = random.Random(f"x7a-{path.name}-{seed}")
    code = "".join(ch for ch in path.name if ch.isalnum())[:10]
    background = [f"r{seed}{code}bg{j}" for j in range(settings["background"])]
    trials: list[Trial] = []
    for condition in CONDITIONS:
        for i in range(settings["trials"]):
            user = f"r{seed}{code}{CONDITION_CODES[condition]}{i}u"
            picks = rng.sample(background, min(len(background), rng.randint(10, 20)))
            trials.append(Trial(seed, condition, i, user, f"{user}t", picks))
    docs = [t.target for t in trials] + background
    vectors = clustered_vectors(2000 + seed, len(docs), 1, settings["dim"]).corpus
    path.vectors = {d: vectors[j].tolist() for j, d in enumerate(docs)}
    for t in trials:
        t.vector = path.vectors[t.target]
    return trials, docs


def _authorizers(path: RevocationPath, trial: Trial, redis_client: Any) -> tuple[Any, Any | None]:
    """The authorizer the retrieval polls, and the one whose invalidate() is called (None: none)."""
    condition = trial.condition
    if condition == "nocache":
        return path.authorizer(), None
    if condition == "ttl30-shared-inv":
        from wardowl.caching import RedisCache

        namespace = f"x7-{RUN_ID}-{path.name}-{trial.seed}-{trial.index}"
        replica_a = CachingAuthorizer(path.authorizer(), ttl=30, shared=RedisCache(redis_client), namespace=namespace,
                                      local_ttl=LOCAL_TTL)
        replica_b = CachingAuthorizer(path.authorizer(), ttl=30, shared=RedisCache(redis_client), namespace=namespace,
                                      local_ttl=LOCAL_TTL)
        return replica_b, replica_a
    ttl = 5.0 if condition == "ttl5" else 30.0
    cache = CachingAuthorizer(path.authorizer(), ttl=ttl)
    return cache, (cache if condition == "ttl30-inv" else None)


def run_trial(ctx: Context, path: RevocationPath, trial: Trial, redis_client: Any) -> None:
    settings = ctx.settings
    bound = path.bound(trial.condition)
    ttl = CACHE_BOUND[trial.condition]
    horizon = (bound if bound is not None else ttl + 10.0) + settings["grace"]
    rec: dict[str, Any] = {
        "type": "x7a-trial",
        "path": path.name,
        "condition": trial.condition,
        "seed": trial.seed,
        "trial": trial.index,
        "bound_s": bound,
        "staleness_s": path.staleness,
        "horizon_s": horizon,
    }
    try:
        polled, invalidator = _authorizers(path, trial, redis_client)
        retriever = PermissionedRetriever(path.backend, polled)
        subject = path.subject(trial)
        noise = random.Random(f"x7a-query-{trial.user}")
        query = Query(vector=_normalized([v + 0.02 * noise.gauss(0.0, 1.0) for v in trial.vector]))
        warm = retriever.retrieve(query, subject, k=5)
    except Exception as error:
        info = ctx.errors.add(f"x7a {path.name} warm", error)
        rec.update({"valid": False, "error": f"{info['class']}: {info['message'][:300]}"})
        ctx.records.write(rec)
        return
    rec["warm_hits"] = len(warm.hits)
    rec["valid"] = trial.target in [h.id for h in warm.hits]
    if not rec["valid"]:
        ctx.records.write(rec)
        return
    t0 = clock()
    try:
        path.revoke(trial)
        rec["write_s"] = clock() - t0
        if invalidator is not None:
            started = clock()
            invalidator.invalidate(subject)
            rec["invalidate_s"] = clock() - started
    except Exception as error:
        info = ctx.errors.add(f"x7a {path.name} revoke", error)
        rec.update({"valid": False, "error": f"{info['class']}: {info['message'][:300]}"})
        ctx.records.write(rec)
        return
    polls = flaps = poll_errors = 0
    run_start: float | None = None
    run_length = 0
    first_error = None
    effect: float | None = None
    while clock() - t0 < horizon:
        started = clock()
        present: bool | None
        try:
            result = retriever.retrieve(query, subject, k=5)
            present = trial.target in [h.id for h in result.hits]
        except Exception as error:
            poll_errors += 1
            present = None
            if first_error is None:
                info = ctx.errors.add(f"x7a {path.name} poll", error)
                first_error = f"{info['class']}: {info['message'][:200]}"
        polls += 1
        if present is False:
            if run_length == 0:
                run_start = started
            run_length += 1
            if run_length >= settings["settle"]:
                assert run_start is not None
                effect = run_start - t0
                break
        else:
            if present is True and run_length > 0:
                flaps += 1
            run_length = 0
        time.sleep(settings["poll"])
    rec.update({
        "effect_s": effect,
        "horizon_hit": effect is None,
        "polls": polls,
        "flaps": flaps,
        "poll_errors": poll_errors,
        "first_poll_error": first_error,
        "violates_bound": None if bound is None else (effect is None or effect > bound + 1.0),
    })
    ctx.records.write(rec)


def revocation(ctx: Context, names: Sequence[str]) -> int:
    opa: OpaProcess | None = None
    if any(n.startswith("opa") for n in names):
        opa = OpaProcess(8181, log_path=ctx.out / "logs" / "opa-x7a.log")
        opa.start()
    redis_client = _redis()
    failed = 0
    try:
        for path in make_paths(ctx, names, opa):
            log(f"x7a {path.name}: start")
            started = clock()
            try:
                path.setup()
                for seed in ctx.seeds():
                    trials, docs = _trials(path, seed, ctx.settings)
                    path.provision(seed, trials, docs)
                    rng = random.Random(f"x7a-order-{path.name}-{seed}")
                    for i in range(ctx.settings["trials"]):
                        batch = [t for t in trials if t.index == i]
                        rng.shuffle(batch)
                        for trial in batch:
                            run_trial(ctx, path, trial, redis_client)
                    log(f"x7a {path.name} seed {seed}: {clock() - started:.0f} s")
            except Exception as error:
                info = ctx.errors.add(f"x7a {path.name}", error)
                ctx.records.write({"type": "path-failed", "path": path.name, **info})
                failed += 1
            finally:
                with contextlib.suppress(Exception):
                    path.close()
            ctx.records.write({"type": "path-end", "path": path.name, "seconds": clock() - started})
    finally:
        if opa is not None:
            opa.kill()
    return failed


# ==== X7b: faults ======================================================================================


@dataclass
class Target:
    """What one fault target needs: retrievers, the pairs to cycle, the oracle, and how to fail."""

    name: str
    kind: str  # "engine" or "store"
    pairs: list[tuple[Subject, Query]]
    expected: list[tuple[set[str], int]]  # per pair: T*_epsilon and min(k, |readable|)
    readable: list[set[str]]  # per pair
    make: Callable[[bool, str], Any]  # (through the proxy?, condition) -> retriever
    kill: Callable[[], None]
    start: Callable[[], None]
    ready: Callable[[], bool]
    proxy: ProxyProcess


class FaultTarget:
    name = ""
    kind = "engine"

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    def setup(self) -> None:
        """Start what the target needs (proxy included)."""

    def prepare(self, seed: int) -> Target:
        raise NotImplementedError

    def close(self) -> None:
        """Stop what was started."""


def _pairs_and_oracle(
    world: World, model: Model, vectors: Any, rng: random.Random, count: int, make_subject: Callable[[str], Subject]
) -> tuple[list[tuple[Subject, Query]], list[tuple[set[str], int]], list[set[str]]]:
    docs = list(world.docs)
    candidates = [u for u in sorted(world.users) if len(model.readable(u, docs)) >= 3] or sorted(world.users)
    pairs, expected, readable = [], [], []
    for j in range(count):
        user = candidates[rng.randrange(len(candidates))]
        can = model.readable(user, docs)
        rows = [docs.index(d) for d in sorted(can)]
        query = vectors.queries[j % len(vectors.queries)]
        truth, depth = exact_top(vectors.corpus, rows, query, 5)
        pairs.append((make_subject(user), Query(vector=query.tolist())))
        expected.append(({docs[r] for r in truth}, depth))
        readable.append(set(can))
    return pairs, expected, readable


class EngineFaultTarget(FaultTarget):
    """An engine behind the proxy, with FAISS (unaffected by faults) as the store."""

    container = ""
    port = 0
    proxy_port = 0
    profile = ""

    def setup(self) -> None:
        self.proxy = ProxyProcess("http", self.proxy_port, f"127.0.0.1:{self.port}", self.proxy_port + 1000,
                                  self.ctx.out / "logs" / f"proxy-{self.name}.log")
        self.proxy.start()

    def provision(self, seed: int, world: World) -> None:
        raise NotImplementedError

    def adapter(self, url: str, breaker: CircuitBreaker | None) -> Any:
        raise NotImplementedError

    def make_subject(self, world: World, uid: str) -> Subject:
        return Subject(uid)

    def kill(self) -> None:
        docker("kill", self.container)

    def start(self) -> None:
        docker("start", self.container)

    def ready(self) -> bool:
        return False

    def prepare(self, seed: int) -> Target:
        from wardowl.backends.faiss import FaissBackend

        settings = self.ctx.settings
        world = make_world(seed, settings["world"], prefix=f"f{self.name[:2]}")
        self.provision(seed, world)
        model = model_for(self.profile, world)
        docs = list(world.docs)
        vectors = clustered_vectors(3000 + seed, len(docs), settings["pairs"], settings["dim"])
        backend = FaissBackend(None, settings["dim"])
        backend.add([Document(d, "", metadata_for(self.profile, world.docs[d])) for d in docs], embeddings=vectors.corpus)
        rng = random.Random(f"x7b-pairs-{self.name}-{seed}")
        pairs, expected, readable = _pairs_and_oracle(world, model, vectors, rng, settings["pairs"],
                                                       lambda uid: self.make_subject(world, uid))
        direct = f"http://127.0.0.1:{self.port}"

        def make(proxied: bool, condition: str) -> Any:
            url = self.proxy.url if proxied else direct
            breaker = CircuitBreaker(failures=5, reset_after=5.0) if condition == "breaker" else None
            authorizer = self.adapter(url, breaker)
            if condition == "cache30":
                authorizer = CachingAuthorizer(authorizer, ttl=30)
            strategy = "postfilter" if condition == "allow-all" else "auto"
            return PermissionedRetriever(backend, authorizer, strategy=strategy)

        return Target(self.name, "engine", pairs, expected, readable, make, self.kill, self.start, self.ready, self.proxy)

    def close(self) -> None:
        self.proxy.stop()


class OpenFGAFaults(EngineFaultTarget):
    name = "openfga"
    container = "openfga"
    port = 8080
    proxy_port = 18080
    profile = "openfga"

    def provision(self, seed: int, world: World) -> None:
        admin = OpenFGAAdmin(OPENFGA_URL)
        self.store = admin.create_store(f"x7b-{RUN_ID}-{seed}")
        self.model_id = admin.write_model(self.store, OPENFGA_FULL_MODEL)
        admin.write_all(self.store, self.model_id, [openfga_tuple(f) for f in rebac_facts(world)])

    def adapter(self, url: str, breaker: CircuitBreaker | None) -> Any:
        return OpenFGAAuthorizer(url, self.store, authorization_model_id=self.model_id, consistency="HIGHER_CONSISTENCY",
                                 contextual_groups=False, circuit_breaker=breaker)

    def ready(self) -> bool:
        return healthy(f"http://127.0.0.1:{self.port}/healthz")


class SpiceDBFaults(EngineFaultTarget):
    name = "spicedb"
    container = "spicedb"
    port = 8443
    proxy_port = 18443
    profile = "spicedb"

    def setup(self) -> None:
        super().setup()
        SpiceDBAdmin(SPICEDB_URL, SPICEDB_TOKEN).write_schema(SPICEDB_SCHEMA)

    def provision(self, seed: int, world: World) -> None:
        SpiceDBAdmin(SPICEDB_URL, SPICEDB_TOKEN).touch_all([spicedb_relationship(f) for f in rebac_facts(world)])

    def adapter(self, url: str, breaker: CircuitBreaker | None) -> Any:
        return SpiceDBAuthorizer(url, SPICEDB_TOKEN, resource_type=f"{SPICEDB_PREFIX}/document",
                                 subject_type=f"{SPICEDB_PREFIX}/user", group_type=f"{SPICEDB_PREFIX}/group",
                                 consistency={"fullyConsistent": True}, circuit_breaker=breaker)

    def ready(self) -> bool:
        try:
            SpiceDBAdmin(SPICEDB_URL, SPICEDB_TOKEN).api("/v1/schema/read", {}, timeout=3)
        except Exception:
            return False
        return True


class OPAFaults(EngineFaultTarget):
    """OPA restarted with its policy and data files, as a production server reloads its bundle."""

    name = "opa"
    port = 8181
    proxy_port = 18181
    profile = "opa-rel-doc"

    def setup(self) -> None:
        super().setup()
        self.dir = self.ctx.out / "opa-x7b"
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "x4rel.rego").write_text((POLICIES / "opa" / "x4rel.rego").read_text(encoding="utf-8"), encoding="utf-8")
        self.opa: OpaProcess | None = None

    def provision(self, seed: int, world: World) -> None:
        import json

        (self.dir / "data.json").write_text(json.dumps({"x4rel_world": _opa_rel_world(world)}), encoding="utf-8")
        if self.opa is not None:
            self.opa.kill()
        self.opa = OpaProcess(self.port, files=[self.dir / "x4rel.rego", self.dir / "data.json"],
                              log_path=self.ctx.out / "logs" / "opa-x7b.log")
        self.opa.start()

    def make_subject(self, world: World, uid: str) -> Subject:
        u = world.users[uid]
        return Subject(uid, u.groups, {"tenant": u.tenant, "clearance": u.clearance})

    def adapter(self, url: str, breaker: CircuitBreaker | None) -> Any:
        return OPAAuthorizer(url, decisions_path="x4rel/decisions", filter_path="x4rel/filter", circuit_breaker=breaker)

    def kill(self) -> None:
        assert self.opa is not None
        self.opa.kill()

    def start(self) -> None:
        assert self.opa is not None
        self.opa.start()

    def ready(self) -> bool:
        return healthy(f"http://127.0.0.1:{self.port}/health")

    def close(self) -> None:
        super().close()
        if self.opa is not None:
            self.opa.kill()


def _opa_rel_world(world: World) -> dict[str, Any]:
    from x4x7_world import opa_world

    return opa_world(world, shares=True, bans=False)


class CerbosFaults(EngineFaultTarget):
    name = "cerbos"
    container = "cerbos"
    port = 3592
    proxy_port = 13592
    profile = "cerbos"

    def provision(self, seed: int, world: World) -> None:
        self.closure = Model(world, folders=False, bans=False, classification=False)

    def make_subject(self, world: World, uid: str) -> Subject:
        u = world.users[uid]
        return Subject(uid, self.closure.groups_of(uid), {"tenant": u.tenant, "levels": levels_for(u.clearance)})

    def adapter(self, url: str, breaker: CircuitBreaker | None) -> Any:
        return CerbosAuthorizer(url, resource_kind="x4doc", circuit_breaker=breaker)

    def ready(self) -> bool:
        return healthy(f"http://127.0.0.1:{self.port}/_cerbos/health")


class StoreFaultTarget(FaultTarget):
    """A store behind the proxy, with metadata ACLs (MetadataACLAuthorizer)."""

    kind = "store"

    def __init__(self, ctx: Context, name: str) -> None:
        super().__init__(ctx)
        self.name = name
        self.made: list[str] = []
        self.pools: list[Any] = []
        self.clients: list[Any] = []

    def setup(self) -> None:
        if self.name == "pgvector":
            self.proxy = ProxyProcess("tcp", 15432, "127.0.0.1:5432", 15433, self.ctx.out / "logs" / "proxy-pgvector.log")
        else:
            self.proxy = ProxyProcess("http", 16333, "127.0.0.1:6333", 16334, self.ctx.out / "logs" / "proxy-qdrant.log")
        self.proxy.start()

    @staticmethod
    def _metadata(world: World, doc_id: str) -> dict[str, Any]:
        d = world.docs[doc_id]
        groups = sorted(d.groups) + (["*"] if d.wildcard else [])
        return {"doc_id": doc_id, "allowed_users": sorted(d.users | {d.owner}), "allowed_groups": groups}

    def _pool(self, port: int) -> Any:
        import psycopg_pool

        url = PG_URL.replace(":5432/", f":{port}/")
        url += ("&" if "?" in url else "?") + "connect_timeout=3"
        try:
            pool = psycopg_pool.ConnectionPool(url, min_size=1, max_size=8, timeout=5, open=True,
                                               check=psycopg_pool.ConnectionPool.check_connection)
        except TypeError:  # an older psycopg-pool without `check`
            pool = psycopg_pool.ConnectionPool(url, min_size=1, max_size=8, timeout=5, open=True)
        self.pools.append(pool)
        return pool

    def prepare(self, seed: int) -> Target:
        settings = self.ctx.settings
        world = make_world(seed, settings["world"], prefix=f"f{self.name[:2]}")
        docs = list(world.docs)
        closure = Model(world, folders=False, bans=False, classification=False)
        vectors = clustered_vectors(3000 + seed, len(docs), settings["pairs"], settings["dim"])
        documents = [Document(d, "", self._metadata(world, d)) for d in docs]
        name = f"x7f_{self.name}_{seed}_{RUN_ID}".replace("-", "_")
        self.made.append(name)
        if self.name == "pgvector":
            from wardowl.backends.pgvector import PgVectorBackend, create_schema

            direct_pool, proxied_pool = self._pool(5432), self._pool(15432)
            create_schema(direct_pool, settings["dim"], table=name, hnsw=False)
            PgVectorBackend(direct_pool, None, table=name, iterative_scan=None).add(documents, embeddings=vectors.corpus)
            backends = {
                False: PgVectorBackend(direct_pool, None, table=name, iterative_scan=None),
                True: PgVectorBackend(proxied_pool, None, table=name, iterative_scan=None),
            }
        else:
            import qdrant_client

            from wardowl.backends.qdrant import QdrantBackend, create_collection

            direct = qdrant_client.QdrantClient(url=QDRANT_URL, timeout=5)
            proxied = qdrant_client.QdrantClient(url="http://127.0.0.1:16333", timeout=5)
            self.clients += [direct, proxied]
            create_collection(direct, name, settings["dim"])
            QdrantBackend(direct, name).add(documents, embeddings=vectors.corpus)
            backends = {False: QdrantBackend(direct, name), True: QdrantBackend(proxied, name)}

        def readable(uid: str) -> set[str]:
            groups = closure.groups_of(uid) | {"*"}
            return {d for d in docs if uid in self._metadata(world, d)["allowed_users"]
                    or groups & set(self._metadata(world, d)["allowed_groups"])}

        def subject(uid: str) -> Subject:
            return Subject(uid, closure.groups_of(uid))

        rng = random.Random(f"x7b-pairs-{self.name}-{seed}")
        candidates = [u for u in sorted(world.users) if len(readable(u)) >= 3] or sorted(world.users)
        pairs, expected, readable_sets = [], [], []
        for j in range(settings["pairs"]):
            user = candidates[rng.randrange(len(candidates))]
            can = readable(user)
            rows = [docs.index(d) for d in sorted(can)]
            query = vectors.queries[j % len(vectors.queries)]
            truth, depth = exact_top(vectors.corpus, rows, query, 5)
            pairs.append((subject(user), Query(vector=query.tolist())))
            expected.append(({docs[r] for r in truth}, depth))
            readable_sets.append(can)

        def make(proxied: bool, condition: str) -> Any:
            return PermissionedRetriever(backends[proxied], MetadataACLAuthorizer())

        container = "pgv" if self.name == "pgvector" else "qdrant"

        def ready() -> bool:
            try:
                backends[False].search(pairs[0][1], 1)
            except Exception:
                return False
            return True

        return Target(self.name, "store", pairs, expected, readable_sets, make,
                      lambda: docker("kill", container), lambda: docker("start", container), ready, self.proxy)

    def close(self) -> None:
        self.proxy.stop()
        for pool in self.pools:
            with contextlib.suppress(Exception):
                pool.close()


FAULT_TARGETS: dict[str, Callable[[Context], FaultTarget]] = {
    "openfga": OpenFGAFaults,
    "spicedb": SpiceDBFaults,
    "opa": OPAFaults,
    "cerbos": CerbosFaults,
    "pgvector": lambda ctx: StoreFaultTarget(ctx, "pgvector"),
    "qdrant": lambda ctx: StoreFaultTarget(ctx, "qdrant"),
}


def _proxy_mode(fault: str) -> tuple[str, float]:
    if fault.startswith("slow-"):
        return "slow", float(fault.split("-", 1)[1])
    return fault, 0.0


@dataclass
class Outcome:
    start: float
    end: float
    code: str  # ok, deviate, leak, authz, error, hang
    error: str | None = None
    error_class: str | None = None
    names_host: bool = False
    leaks: int = 0


def _retrieve(retriever: Any, target: Target, i: int) -> Outcome:
    subject, query = target.pairs[i]
    truth, depth = target.expected[i]
    started = clock()
    try:
        result = retriever.retrieve(query, subject, k=5)
    except BaseException as error:  # noqa: BLE001 - every failure is a result here
        message = str(error)
        return Outcome(started, clock(), "authz" if isinstance(error, AuthorizationError) else "error",
                       message[:200], f"{type(error).__module__}.{type(error).__qualname__}", bool(HOST.search(message)))
    ids = [h.id for h in result.hits]
    leaks = sum(1 for d in ids if d not in target.readable[i])
    if leaks:
        return Outcome(started, clock(), "leak", leaks=leaks)
    exact = len(set(ids) & truth) >= depth and len(ids) == depth
    return Outcome(started, clock(), "ok" if exact else "deviate")


def run_episode(
    ctx: Context, target: Target, fault: str, condition: str, seed: int, episode: int, pool: ThreadPoolExecutor
) -> None:
    settings = ctx.settings
    proxied = fault != "down"
    retriever = target.make(proxied, "allow-all" if fault == "allow-all" else condition)
    outcomes: list[Outcome] = []
    late: list[Outcome] = []
    times: dict[str, float] = {}
    done = threading.Event()

    def control() -> None:
        try:
            time.sleep(settings["baseline"])
            times["fault_on"] = clock()
            if fault == "down":
                target.kill()
            else:
                mode, delay = _proxy_mode(fault)
                target.proxy.set(mode, delay)
            times["fault_on_done"] = clock()
            time.sleep(max(0.0, times["fault_on"] + settings["fault"] - clock()))
            times["fault_off"] = clock()
            if fault == "down":
                target.start()
            else:
                target.proxy.set("pass")
            times["fault_off_done"] = clock()
        except Exception as error:
            info = ctx.errors.add(f"x7b {target.name} {fault} control", error)
            times["control_error"] = clock()
            times.setdefault("fault_on", clock())
            times.setdefault("fault_off", clock())
            ctx.records.write({"type": "x7b-control-error", "target": target.name, "fault": fault, **info})
        finally:
            done.set()

    origin = clock()
    controller = threading.Thread(target=control, daemon=True)
    controller.start()
    i = 0
    limit = settings["recover_max_down"] if fault == "down" else settings["recover_max"]
    while True:
        future = pool.submit(_retrieve, retriever, target, i % len(target.pairs))
        submitted = clock()
        try:
            outcomes.append(future.result(timeout=settings["watchdog"]))
        except FutureTimeout:
            outcomes.append(Outcome(submitted, clock(), "hang"))
            future.add_done_callback(lambda f: late.append(f.result()) if not f.cancelled() else None)
        i += 1
        if done.is_set():
            off = times["fault_off"]
            after = [o for o in outcomes if o.start >= off]
            if _stable(after, settings["stable"]) or clock() - off > limit:
                break
        time.sleep(0.02)
    controller.join(5)
    # Leave the target as it was: the proxy passing, the server answering.
    with contextlib.suppress(Exception):
        target.proxy.set("pass")
    if not _wait_ready(target, 120):
        with contextlib.suppress(Exception):
            target.start()
        _wait_ready(target, 120)
    ctx.records.write(_episode_record(ctx, target, fault, condition, seed, episode, origin, times, outcomes, late))


def _stable(outcomes: Sequence[Outcome], seconds: float) -> bool:
    """True when the last successful run of retrievals spans at least `seconds`."""
    run: list[Outcome] = []
    for o in outcomes:
        run = [*run, o] if o.code == "ok" else []
    return bool(run) and run[-1].end - run[0].start >= seconds


def _wait_ready(target: Target, timeout: float) -> bool:
    try:
        wait_for(target.ready, timeout, interval=0.5, what=f"{target.name} ready")
    except TimeoutError:
        return False
    return True


def _episode_record(
    ctx: Context,
    target: Target,
    fault: str,
    condition: str,
    seed: int,
    episode: int,
    origin: float,
    times: Mapping[str, float],
    outcomes: Sequence[Outcome],
    late: Sequence[Outcome],
) -> dict[str, Any]:
    on, off = times.get("fault_on", origin), times.get("fault_off", origin)
    baseline = [o for o in outcomes if o.end <= on]
    # Inside the fault: started at least 0.1 s after it began and ended before it was removed; a
    # hang (the watchdog's 10 s) counts when it started inside.
    inside = [o for o in outcomes if o.start >= on + 0.1 and (o.end <= off or (o.code == "hang" and o.start <= off))]
    after = [o for o in outcomes if o.start >= off]
    first_ok = next((o for o in after if o.code == "ok"), None)
    stable_from = None
    run: list[Outcome] = []
    for o in after:
        run = [*run, o] if o.code == "ok" else []
        if run and run[-1].end - run[0].start >= ctx.settings["stable"]:
            stable_from = run[0].start - off
            break
    failures = [o for o in outcomes if o.code in ("authz", "error")]
    errors = collections.Counter((o.error_class, o.error) for o in failures)
    codes = collections.Counter(o.code for o in outcomes)

    def latencies(items: Sequence[Outcome], codes_wanted: tuple[str, ...]) -> list[float]:
        return sorted(round(o.end - o.start, 4) for o in items if o.code in codes_wanted)

    return {
        "type": "x7b-episode",
        "target": target.name,
        "kind": target.kind,
        "fault": fault,
        "condition": condition,
        "seed": seed,
        "episode": episode,
        "fault_on_s": on - origin,
        "fault_off_s": off - origin,
        "inject_s": times.get("fault_on_done", on) - on,
        "remove_s": times.get("fault_off_done", off) - off,
        "control_error": "control_error" in times,
        "codes": dict(codes),
        "baseline_n": len(baseline),
        "baseline_ok": sum(o.code == "ok" for o in baseline),
        "inside_n": len(inside),
        "inside_fail": sum(o.code in ("authz", "error") for o in inside),
        "inside_hang": sum(o.code == "hang" for o in inside),
        "inside_ok": sum(o.code == "ok" for o in inside),
        "inside_deviate": sum(o.code == "deviate" for o in inside),
        "leaks": sum(o.leaks for o in outcomes) + sum(o.leaks for o in late),
        "leaking_requests": sum(o.code == "leak" for o in outcomes) + sum(o.code == "leak" for o in late),
        "late": len(late),
        "failures": len(failures),
        "failures_not_authz": sum(o.code == "error" for o in failures),
        "failures_naming_host": sum(o.names_host for o in failures),
        "errors": [{"class": c, "message": m, "count": n} for (c, m), n in errors.most_common(10)],
        "distinct_errors": len(errors),
        "baseline_ok_ms": latencies(baseline, ("ok",))[:200],
        "inside_ok_ms": latencies(inside, ("ok", "deviate"))[:400],
        "inside_fail_ms": latencies(inside, ("authz", "error"))[:400],
        "recovery_s": None if first_ok is None else first_ok.end - off,
        "stable_from_s": stable_from,
        "requests": [[round(o.start - origin, 3), round(o.end - o.start, 4), o.code] for o in outcomes][:3000],
    }


def faults(ctx: Context, names: Sequence[str]) -> int:
    failed = 0
    pool = ThreadPoolExecutor(max_workers=64)
    try:
        for name in names:
            runner = FAULT_TARGETS[name](ctx)
            started = clock()
            log(f"x7b {name}: start")
            try:
                runner.setup()
                if runner.kind == "store":
                    plan = [(f, "plain") for f in STORE_FAULTS[name]]
                else:
                    plan = [(f, "plain") for f in ENGINE_FAULTS]
                    plan += [(f, c) for c in ("breaker", "cache30") for f in GUARDED_FAULTS]
                for seed in ctx.seeds():
                    target = runner.prepare(seed)
                    _wait_ready(target, 120)
                    for episode in range(ctx.settings["episodes"]):
                        order = list(plan)
                        random.Random(f"x7b-order-{name}-{seed}-{episode}").shuffle(order)
                        for fault, condition in order:
                            try:
                                run_episode(ctx, target, fault, condition, seed, episode, pool)
                            except Exception as error:
                                info = ctx.errors.add(f"x7b {name} {fault} {condition}", error)
                                ctx.records.write({"type": "episode-failed", "target": name, "fault": fault,
                                                   "condition": condition, "seed": seed, **info})
                    log(f"x7b {name} seed {seed}: {clock() - started:.0f} s")
            except Exception as error:
                info = ctx.errors.add(f"x7b {name}", error)
                ctx.records.write({"type": "target-failed", "target": name, **info})
                failed += 1
            finally:
                with contextlib.suppress(Exception):
                    runner.close()
            ctx.records.write({"type": "target-end", "target": name, "seconds": clock() - started})
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
    return failed


# ==== main ==============================================================================================


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    rev = sub.add_parser("revocation", help="X7a")
    rev.add_argument("--paths", required=True)
    flt = sub.add_parser("faults", help="X7b")
    flt.add_argument("--targets", required=True)
    for p in (rev, flt):
        p.add_argument("--profile", choices=sorted(SETTINGS), default="smoke")
        p.add_argument("--out", default="results")
        p.add_argument("--containers", default="", help="containers whose images to record")
    args = parser.parse_args(argv)
    settings = SETTINGS[args.profile]
    out = Path(args.out)
    records = Records(out, f"x7-{JOB}")
    errors = Errors()
    ctx = Context(settings, records, errors, out, args.profile)
    names = [n.strip() for n in (args.paths if args.command == "revocation" else args.targets).split(",") if n.strip()]
    records.write(run_info("x7", args.profile, {**_settings_for_record(settings), "command": args.command, "names": names}))
    records.write(versions_record([c for c in args.containers.split(",") if c]))
    if args.command == "revocation":
        failed = revocation(ctx, names)
    else:
        failed = faults(ctx, names)
    records.write({"type": "run-end", "records": records.count, "failed": failed})
    errors.report(records, f"x7 {JOB}")
    annotate("notice", f"x7 {JOB} records", f"{records.count} records, {failed} failed paths or targets, in {records.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
