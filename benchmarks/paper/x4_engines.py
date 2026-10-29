"""X4: do authorization engines' filters agree with their checks? (PREREG_X4_X7.md)

    python benchmarks/paper/x4_engines.py --engines openfga --parts a,b --profile smoke --out results

Engines: `openfga`, `spicedb`, `opa`, `cerbos` and `controls` (in process). Parts:

* `a`: filter against check at one revision, for every profile of the engine, against an oracle;
  the latency of filter and check on the same worlds, cached and not (part of X4d);
* `b`: the same without pinning, under a concurrent writer (OpenFGA, SpiceDB, OPA);
* `c`: list truncation as the readable set grows, what wardowl does about it, the recall it costs,
  and latency at every size (X4c and X4d; OpenFGA, SpiceDB, OPA).

Every measurement is one JSON line in `<out>/x4-<job>.jsonl`. The servers come from
.github/workflows/paper-x4-x7.yml; the URLs can be changed with X4X7_* environment variables.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import threading
import time
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from x4x7_common import (
    JOB,
    POLICIES,
    RUN_ID,
    Errors,
    OpaProcess,
    OpenFGAAdmin,
    Records,
    SpiceDBAdmin,
    annotate,
    clock,
    log,
    run_info,
    versions_record,
)
from x4x7_world import (
    DOC_BANNED,
    DOC_USERS,
    FOLDER_USERS,
    LEVELS,
    OPENFGA_FULL_MODEL,
    OPENFGA_SIMPLE_MODEL,
    SPICEDB_PREFIX,
    SPICEDB_SCHEMA,
    SPICEDB_SIMPLE_PREFIX,
    USER_GROUPS,
    Fact,
    History,
    Model,
    World,
    WorldSize,
    clustered_vectors,
    exact_top,
    has_scalar_acl,
    levels_for,
    make_world,
    metadata_for,
    model_for,
    openfga_tuple,
    opa_folder,
    opa_world,
    rebac_facts,
    spicedb_relationship,
)

from wardowl import CachingAuthorizer, Document, FunctionAuthorizer, Hit, PermissionedRetriever, Query, Subject
from wardowl.authorizers._http import JsonClient
from wardowl.authorizers.cerbos import CerbosAuthorizer
from wardowl.authorizers.opa import OPAAuthorizer
from wardowl.authorizers.opa import _subject as opa_subject
from wardowl.authorizers.openfga import OpenFGAAuthorizer
from wardowl.authorizers.spicedb import SpiceDBAuthorizer
from wardowl.authz import AuthorizationError
from wardowl.filters import And, Filter, In, Or, matches

OPENFGA_URL = os.environ.get("X4X7_OPENFGA_URL", "http://127.0.0.1:8080")
SPICEDB_URL = os.environ.get("X4X7_SPICEDB_URL", "http://127.0.0.1:8443")
SPICEDB_TOKEN = os.environ.get("X4X7_SPICEDB_TOKEN", "wo-test")
CERBOS_URL = os.environ.get("X4X7_CERBOS_URL", "http://127.0.0.1:3592")

SETTINGS: dict[str, dict[str, Any]] = {
    "full": {
        "seeds": 5,
        "world": WorldSize(),
        "b_users": 40,
        "b_rate": 20.0,
        "latency_users": 10,
        "c_docs": 100_000,
        "c_levels": [10, 100, 999, 1000, 1001, 3000, 10_000, 30_000, 100_000],
        "c_queries": 30,
        "c_reps": 3,
        "dim": 64,
    },
    "smoke": {
        "seeds": 1,
        "world": WorldSize(tenants=2, users_per_tenant=6, groups=8, folders=8, docs=120),
        "b_users": 6,
        "b_rate": 20.0,
        "latency_users": 2,
        "c_docs": 5000,
        "c_levels": [10, 999, 1000, 1001, 3000],
        "c_queries": 4,
        "c_reps": 1,
        "dim": 32,
    },
}

NEVER = In("wardowl:nothing", [])  # matches no chunk
STALENESS = {  # seconds an unpinned read may lag (PREREG_X4_X7.md, X4b)
    ("openfga", "writer-hc"): 0.0,
    ("openfga", "writer-ml"): 10.0,
    ("spicedb", "writer-fc"): 0.0,
    ("spicedb", "writer-ml"): 5.5,
    ("opa", "writer"): 0.0,
}


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


# ---- filters ---------------------------------------------------------------------------------------


def filter_size(f: Filter | None) -> int | None:
    """The number of values in a filter, every `In` counted."""
    if f is None:
        return None
    if isinstance(f, In):
        return len(f.values)
    return sum(filter_size(c) or 0 for c in f.clauses)


class Untranslatable(Exception):
    """A UCAST node the wardowl filter language cannot express exactly."""


def _plain(value: Any) -> bool:
    return isinstance(value, (str, int)) and not isinstance(value, bool)


def _column(name: Any) -> str:
    if not isinstance(name, str) or not name:
        raise Untranslatable(f"field {name!r}")
    return name.rsplit(".", 1)[-1]  # "doc.tenant" (the unknown input.doc as a table) -> "tenant"


def _join(op: str, parts: list[Filter]) -> Filter:
    if len(parts) == 1:
        return parts[0]
    return And(*parts) if op == "and" else Or(*parts)


def _field_condition(field: str, operator: Any, value: Any) -> Filter:
    if operator == "eq" and _plain(value):
        return In(field, [value])
    if operator == "in" and isinstance(value, list) and all(_plain(v) for v in value):
        return In(field, value)
    raise Untranslatable(f"field operator {operator!r} with {type(value).__name__}")


def ucast_to_filter(node: Any) -> Filter:
    """OPA's UCAST conditions as a wardowl filter: `eq` and `in` on a column become `In`, `and` and
    `or` become `And` and `Or`; anything else (`not`, `ne`, `nin`, comparisons, column references)
    raises `Untranslatable`, and the authorizer then gives no filter."""
    if not isinstance(node, dict):
        raise Untranslatable(f"node {node!r:.100}")
    if "type" in node:
        kind, operator, value = node.get("type"), node.get("operator"), node.get("value")
        if kind == "compound":
            if operator in ("and", "or") and isinstance(value, list) and value:
                return _join(operator, [ucast_to_filter(v) for v in value])
            raise Untranslatable(f"compound {operator!r}")
        if kind == "field":
            return _field_condition(_column(node.get("field")), operator, value)
        raise Untranslatable(f"node type {kind!r}")
    parts: list[Filter] = []  # the concise form
    for key, value in node.items():
        if key in ("and", "or"):
            if not isinstance(value, list) or not value:
                raise Untranslatable(f"concise {key}")
            parts.append(_join(key, [ucast_to_filter(v) for v in value]))
        elif key == "not":
            raise Untranslatable("not")
        elif isinstance(value, dict):
            if len(value) != 1:
                raise Untranslatable(f"concise field {key!r}")
            ((operator, operand),) = value.items()
            parts.append(_field_condition(_column(key), operator, operand))
        else:
            parts.append(_field_condition(_column(key), "eq", value))
    if not parts:
        raise Untranslatable("empty conditions")
    return _join("and", parts)


class OpaCompileAuthorizer(OPAAuthorizer):
    """`OPAAuthorizer` whose filter comes from OPA's Compile API (partial evaluation, UCAST target)
    instead of a filter document. `last` keeps the outcome of the last compile, for the records."""

    UCAST = "application/vnd.opa.ucast.all+json"

    def __init__(self, url: str, *, decisions_path: str, compile_path: str, timeout: float = 2.0) -> None:
        super().__init__(url, decisions_path=decisions_path, timeout=timeout)
        self.compile_path = compile_path.strip("/")
        self._compile = JsonClient(url, service="OPA", timeout=timeout, headers={"Accept": self.UCAST})
        self.last: dict[str, Any] = {}

    def filter_for(self, subject: Subject, action: str = "read") -> Filter | None:
        payload = {"input": {"subject": opa_subject(subject), "action": action}, "unknowns": ["input.doc"]}
        answer = self._compile.post_json(f"/v1/compile/{self.compile_path}", payload, f"OPA compile {self.compile_path}")
        result = answer.get("result") if isinstance(answer, dict) else None
        if not isinstance(result, dict):
            raise AuthorizationError(f"OPA compile {self.compile_path} returned an unexpected response")
        if "query" not in result:
            self.last = {"outcome": "always-denied"}
            return NEVER
        query = result["query"]
        if query in ({}, "", None):
            self.last = {"outcome": "always-allowed"}
            return None
        try:
            translated = ucast_to_filter(query)
        except Untranslatable as error:
            self.last = {"outcome": "untranslatable", "reason": str(error)[:200], "query": str(query)[:400]}
            return None
        self.last = {"outcome": "translated"}
        return translated


# ---- measuring filter against check ---------------------------------------------------------------


def _timed_filter(ctx: Context, authorizer: Any, subject: Subject, where: str) -> tuple[Filter | None, str, float, str | None]:
    started = clock()
    try:
        f = authorizer.filter_for(subject)
    except Exception as error:
        info = ctx.errors.add(where, error)
        return None, "error", (clock() - started) * 1000, f"{info['class']}: {info['message'][:300]}"
    return f, ("none" if f is None else "filter"), (clock() - started) * 1000, None


def _compare(
    hits: Sequence[Hit], admitted: Sequence[bool] | None, decisions: Sequence[bool], oracle: Sequence[bool]
) -> tuple[dict[str, Any], list[int]]:
    out: dict[str, Any] = {
        "check_true": sum(decisions),
        "oracle_true": sum(oracle),
        "co_fa": sum(1 for c, o in zip(decisions, oracle, strict=True) if c and not o),
        "co_fd": sum(1 for c, o in zip(decisions, oracle, strict=True) if o and not c),
    }
    if admitted is None:
        out.update({"filter_true": None, "fa": 0, "fd": 0, "fo_fa": 0, "fo_fd": 0, "fa_scalar": 0, "fd_scalar": 0})
        return out, []
    n = len(hits)
    fa = [i for i in range(n) if admitted[i] and not decisions[i]]
    fd = [i for i in range(n) if decisions[i] and not admitted[i]]
    out.update(
        {
            "filter_true": sum(admitted),
            "fa": len(fa),
            "fd": len(fd),
            "fo_fa": sum(1 for a, o in zip(admitted, oracle, strict=True) if a and not o),
            "fo_fd": sum(1 for a, o in zip(admitted, oracle, strict=True) if o and not a),
            "fa_scalar": sum(1 for i in fa if has_scalar_acl(hits[i].metadata)),
            "fd_scalar": sum(1 for i in fd if has_scalar_acl(hits[i].metadata)),
            "examples": [
                {
                    "doc": hits[i].id,
                    "filter": admitted[i],
                    "check": decisions[i],
                    "oracle": oracle[i],
                    "metadata": dict(hits[i].metadata),
                }
                for i in (fa + fd)[:10]
            ],
        }
    )
    return out, fa + fd


def _reproduce(
    authorizer: Any, subject: Subject, hits: Sequence[Hit], indexes: Sequence[int], admitted: Sequence[bool], decisions: Sequence[bool]
) -> dict[str, Any]:
    """Ask twice more about the disagreeing pairs; a pair reproduces when both answers repeat."""
    same = dict.fromkeys(indexes, 0)
    for _ in range(2):
        f = authorizer.filter_for(subject)
        again = authorizer.check(subject, [hits[i] for i in indexes])
        for j, i in enumerate(indexes):
            a = matches(f, hits[i].metadata) if f is not None else None
            if a == admitted[i] and again[j] == decisions[i]:
                same[i] += 1
    reproduced = [i for i in indexes if same[i] == 2]
    return {
        "repro_checked": len(indexes),
        "repro_fa": sum(1 for i in reproduced if admitted[i]),
        "repro_fd": sum(1 for i in reproduced if not admitted[i]),
    }


def measure_subjects(
    ctx: Context,
    *,
    engine: str,
    profile: str,
    seed: int,
    authorizer: Any,
    users: Sequence[str],
    hits: Sequence[Hit],
    model: Model,
    make_subject: Callable[[str], Subject],
    planted: Mapping[str, tuple[int, int]] | None = None,
) -> None:
    """X4a for one profile and world: one record per user."""
    metas = [h.metadata for h in hits]
    latency_users = ctx.settings["latency_users"]
    totals = {"subjects": 0, "with_filter": 0, "fa": 0, "fd": 0, "co": 0, "errors": 0}
    for index, uid in enumerate(users):
        subject = make_subject(uid)
        rec: dict[str, Any] = {
            "type": "x4a-subject",
            "engine": engine,
            "profile": profile,
            "seed": seed,
            "user": uid,
            "n_docs": len(hits),
        }
        f, rec["filter_status"], rec["filter_ms"], problem = _timed_filter(ctx, authorizer, subject, f"{profile} filter_for")
        if problem:
            rec["filter_error"] = problem
        if isinstance(authorizer, OpaCompileAuthorizer):
            rec["compile"] = dict(authorizer.last)
        rec["filter_values"] = filter_size(f)
        started = clock()
        try:
            decisions = list(authorizer.check(subject, hits))
        except Exception as error:
            info = ctx.errors.add(f"{profile} check", error)
            rec["check_error"] = f"{info['class']}: {info['message'][:300]}"
            ctx.records.write(rec)
            totals["errors"] += 1
            continue
        rec["check_ms"] = (clock() - started) * 1000
        oracle = [model.allows(uid, h.id) for h in hits]
        admitted = [matches(f, m) for m in metas] if f is not None else None
        compared, disagreeing = _compare(hits, admitted, decisions, oracle)
        rec.update(compared)
        if disagreeing and admitted is not None:
            try:
                rec.update(_reproduce(authorizer, subject, hits, disagreeing[:200], admitted, decisions))
            except Exception as error:
                info = ctx.errors.add(f"{profile} reproduce", error)
                rec["repro_error"] = f"{info['class']}: {info['message'][:300]}"
        if planted is not None:
            rec["planted_fa"], rec["planted_fd"] = planted[uid]
        if profile.endswith("-excl"):
            # Documents the user is banned from, directly or through a group (X4-H3's prediction).
            groups = model.groups_of(uid)
            rec["banned_docs"] = sum(
                1 for d in model.world.docs.values() if uid in d.banned_users or groups & d.banned_groups
            )
        ctx.records.write(rec)
        totals["subjects"] += 1
        totals["with_filter"] += f is not None
        totals["fa"] += rec["fa"]
        totals["fd"] += rec["fd"]
        totals["co"] += rec["co_fa"] + rec["co_fd"]
        if index < latency_users:
            batch = list(hits[:: max(1, len(hits) // 10)][:10])
            latency(ctx, engine=engine, route=profile, seed=seed, structure="x4a-world", n=None,
                    authorizer=authorizer, subject=subject, batch=batch)
    log(f"x4a {profile} seed {seed}: {totals}")


def latency(
    ctx: Context,
    *,
    engine: str,
    route: str,
    seed: int,
    structure: str,
    n: int | None,
    authorizer: Any,
    subject: Subject,
    batch: Sequence[Hit],
    filters: bool = True,
) -> None:
    """X4d: filter_for and check of a batch, uncached and through CachingAuthorizer (a miss, then
    10 hits). Times in milliseconds."""
    rec: dict[str, Any] = {
        "type": "x4d-latency",
        "engine": engine,
        "route": route,
        "seed": seed,
        "structure": structure,
        "n": n,
        "batch": len(batch),
    }

    def timed(function: Callable[[], Any]) -> float:
        started = clock()
        function()
        return (clock() - started) * 1000

    try:
        if filters:
            rec["filter_uncached_ms"] = [timed(lambda: authorizer.filter_for(subject)) for _ in range(3)]
        rec["check_uncached_ms"] = [timed(lambda: authorizer.check(subject, batch)) for _ in range(5)]
        cache = CachingAuthorizer(authorizer, ttl=600)
        if filters:
            rec["filter_miss_ms"] = timed(lambda: cache.filter_for(subject))
            rec["filter_hit_ms"] = [timed(lambda: cache.filter_for(subject)) for _ in range(10)]
        rec["check_miss_ms"] = timed(lambda: cache.check(subject, batch))
        rec["check_hit_ms"] = [timed(lambda: cache.check(subject, batch)) for _ in range(10)]
    except Exception as error:
        info = ctx.errors.add(f"{route} latency", error)
        rec["error"] = f"{info['class']}: {info['message'][:300]}"
    ctx.records.write(rec)


def _hits(world: World, profile: str) -> list[Hit]:
    return [Hit(d.id, "", 1.0, metadata_for(profile, d)) for d in world.docs.values()]


# ---- X4b: the writer ----------------------------------------------------------------------------------


class Writer:
    """One thread that commits `rate` toggles a second to the engine and logs each with its times.
    Half of the toggles concern the user being measured (`current_user`)."""

    def __init__(
        self,
        ctx: Context,
        world: World,
        history: History,
        apply: Callable[[Fact, bool, frozenset[str]], str | None],
        families: Sequence[tuple[str, float]],
        rate: float,
        seed: int,
    ) -> None:
        self.ctx = ctx
        self.world = world
        self.history = history
        self.apply = apply
        self.families = [f for f, _ in families]
        self.weights = [w for _, w in families]
        self.interval = 1.0 / rate
        self.rng = random.Random(f"x4b-writer-{seed}")
        self.users = sorted(world.users)
        self.docs_by_tenant: dict[str, list[str]] = {}
        for d in world.docs.values():
            self.docs_by_tenant.setdefault(d.tenant, []).append(d.id)
        self.folders = sorted(world.folders)
        self.groups = sorted(world.groups)
        self.lock = threading.Lock()
        self.log: list[tuple[int, float, float]] = []  # (state index, start, end)
        self.inflight: float | None = None  # start of the write being sent, until it is logged
        self.latest: tuple[int, str | None] = (0, None)
        self.current_user: str | None = None
        self.failures = 0
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def _base(self, family: str, key: str) -> frozenset[str]:
        if family == DOC_USERS:
            return self.world.docs[key].users
        if family == DOC_BANNED:
            return self.world.docs[key].banned_users
        if family == FOLDER_USERS:
            return self.world.folders[key].users
        return self.world.users[key].groups

    def _choose(self) -> tuple[str, str, str, Fact]:
        family = self.rng.choices(self.families, self.weights)[0]
        current = self.current_user
        user = current if current is not None and self.rng.random() < 0.5 else self.rng.choice(self.users)
        if family in (DOC_USERS, DOC_BANNED):
            doc = self.rng.choice(self.docs_by_tenant[self.world.users[user].tenant])
            relation = "reader" if family == DOC_USERS else "banned"
            return family, doc, user, ("document", doc, relation, "user", user, "")
        if family == FOLDER_USERS:
            folder = self.rng.choice(self.folders)
            return family, folder, user, ("folder", folder, "viewer", "user", user, "")
        group = self.rng.choice(self.groups)
        return family, user, group, ("group", group, "member", "user", user, "")

    def start(self, token: str | None) -> None:
        self.latest = (self.history.count, token)
        self._thread = threading.Thread(target=self._run, name="x4b-writer", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(30)

    def _run(self) -> None:
        while not self._stop.is_set():
            tick = clock()
            family, key, member, fact = self._choose()
            current = self.history.value(family, key, None, self._base(family, key))
            adding = member not in current
            new = current | {member} if adding else current - {member}
            started = clock()
            with self.lock:
                self.inflight = started
            try:
                token = self.apply(fact, adding, frozenset(new))
            except Exception as error:
                with self.lock:
                    self.inflight = None
                self.failures += 1
                self.ctx.errors.add("x4b writer", error)
                time.sleep(0.05)
                continue
            ended = clock()
            index = self.history.record(family, key, frozenset(new))
            with self.lock:
                self.log.append((index, started, ended))
                self.latest = (index, token)
                self.inflight = None
            pause = self.interval - (clock() - tick)
            if pause > 0:
                self._stop.wait(pause)

    def window(self, after: float, before: float, base: int) -> tuple[int, int]:
        """The candidate states of a trial: from the last write that ended by `after` to the last
        write that started by `before`. A write still being sent that started by `before` may already
        be visible, so it is waited for (at most 10 s) and counted."""
        deadline = clock() + 10.0
        while True:
            with self.lock:
                pending = self.inflight
                entries = list(self.log)
            if pending is None or pending > before or clock() > deadline:
                break
            time.sleep(0.005)
        low = max((i for i, _, end in entries if end <= after), default=base)
        high = max((i for i, start, _ in entries if start <= before), default=base)
        return low, max(low, high)


def run_trials(
    ctx: Context,
    *,
    engine: str,
    phase: str,
    seed: int,
    conditions: Mapping[str, Callable[[tuple[int, str | None]], Any]],
    users: Sequence[str],
    hits: Sequence[Hit],
    model: Model,
    make_subject: Callable[[str], Subject],
    writer: Writer | None,
    history: History,
) -> None:
    """X4b: each user once under every condition, in a seeded random order."""
    rng = random.Random(f"x4b-order-{engine}-{phase}-{seed}")
    metas = [h.metadata for h in hits]
    for uid in users:
        order = list(conditions)
        rng.shuffle(order)
        for condition in order:
            if writer is not None:
                writer.current_user = uid
                pin = writer.latest
            else:
                pin = (history.count, None)
            subject = make_subject(uid)
            rec: dict[str, Any] = {
                "type": "x4b-trial",
                "engine": engine,
                "phase": phase,
                "condition": condition,
                "seed": seed,
                "user": uid,
                "n_docs": len(hits),
                "pin": pin[0],
            }
            try:
                authorizer = conditions[condition](pin)
                t0 = clock()
                f = authorizer.filter_for(subject)
                t1 = clock()
                decisions = list(authorizer.check(subject, hits))
                t2 = clock()
            except Exception as error:
                info = ctx.errors.add(f"x4b {engine} {condition}", error)
                rec["error"] = f"{info['class']}: {info['message'][:300]}"
                ctx.records.write(rec)
                continue
            rec.update({"filter_status": "none" if f is None else "filter", "filter_ms": (t1 - t0) * 1000,
                        "check_ms": (t2 - t1) * 1000})
            if f is None:
                ctx.records.write(rec)
                continue
            admitted = [matches(f, m) for m in metas]
            disagreeing = [i for i in range(len(hits)) if admitted[i] != decisions[i]]
            rec["disagree"] = len(disagreeing)
            rec["fa"] = sum(1 for i in disagreeing if admitted[i])
            rec["fd"] = len(disagreeing) - rec["fa"]
            pinned = writer is None or condition == "writer-pinned"
            if pinned:
                state = pin[0]
                oracle = [model.allows(uid, h.id, state) for h in hits]
                rec["oracle_mismatch_filter"] = sum(1 for a, o in zip(admitted, oracle, strict=True) if a != o)
                rec["oracle_mismatch_check"] = sum(1 for c, o in zip(decisions, oracle, strict=True) if c != o)
                if disagreeing:
                    try:
                        rec.update(_reproduce(authorizer, subject, hits, disagreeing[:200], admitted, decisions))
                    except Exception as error:
                        info = ctx.errors.add(f"x4b {engine} reproduce", error)
                        rec["repro_error"] = f"{info['class']}: {info['message'][:300]}"
            else:
                staleness = STALENESS[(engine, condition)]
                low, high = writer.window(t0 - staleness, t2, pin[0]) if writer else (pin[0], pin[0])
                explained = 0
                for i in disagreeing:
                    answers = {model.allows(uid, hits[i].id, state) for state in range(low, high + 1)}
                    explained += len(answers) > 1
                rec.update({"window": [low, high], "writes_in_window": high - low, "explained": explained,
                            "unexplained": len(disagreeing) - explained, "staleness_s": staleness})
            if disagreeing:
                rec["examples"] = [
                    {"doc": hits[i].id, "filter": admitted[i], "check": decisions[i]} for i in disagreeing[:5]
                ]
            ctx.records.write(rec)


# ---- the engines ---------------------------------------------------------------------------------------


class Runner:
    engine = ""

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.size: WorldSize = ctx.settings["world"]

    def setup(self) -> None:
        """Connect and load models or policies."""

    def worlds(self) -> Iterator[tuple[int, World]]:
        for seed in self.ctx.seeds():
            yield seed, make_world(seed, self.size)

    def part_a(self) -> None:
        raise NotImplementedError

    def part_b(self) -> None:
        self.ctx.records.write({"type": "part-skipped", "engine": self.engine, "part": "b"})

    def part_c(self) -> None:
        self.ctx.records.write({"type": "part-skipped", "engine": self.engine, "part": "c"})

    def close(self) -> None:
        """Stop what the runner started."""


def _setup_record(ctx: Context, **fields: Any) -> None:
    ctx.records.write({"type": "setup", **fields})


class OpenFGARunner(Runner):
    engine = "openfga"

    def setup(self) -> None:
        self.admin = OpenFGAAdmin(OPENFGA_URL)
        self.stores: list[str] = []

    def _store(self, name: str, model: Mapping[str, Any], facts: Sequence[Fact]) -> tuple[str, str]:
        store = self.admin.create_store(f"x4-{RUN_ID}-{name}")
        self.stores.append(store)
        model_id = self.admin.write_model(store, model)
        started = clock()
        self.admin.write_all(store, model_id, [openfga_tuple(f) for f in facts])
        _setup_record(self.ctx, engine=self.engine, what=name, tuples=len(facts), seconds=clock() - started)
        return store, model_id

    def part_a(self) -> None:
        for seed, world in self.worlds():
            users = sorted(world.users)
            hits = _hits(world, "openfga")
            for profile in ("openfga", "openfga-ctx"):
                stored = profile == "openfga"
                store, model_id = self._store(f"a-{seed}-{profile}", OPENFGA_FULL_MODEL, rebac_facts(world, stored_groups=stored))
                authorizer = OpenFGAAuthorizer(
                    OPENFGA_URL, store, authorization_model_id=model_id, consistency="HIGHER_CONSISTENCY",
                    contextual_groups=not stored,
                )

                def make_subject(uid: str, world: World = world, stored: bool = stored) -> Subject:
                    return Subject(uid) if stored else Subject(uid, world.users[uid].groups)

                measure_subjects(self.ctx, engine=self.engine, profile=profile, seed=seed, authorizer=authorizer,
                                 users=users, hits=hits, model=model_for(profile, world), make_subject=make_subject)
                self.admin.delete_store(store)

    def part_b(self) -> None:
        settings = self.ctx.settings
        for seed, world in self.worlds():
            history = History()
            store, model_id = self._store(f"b-{seed}", OPENFGA_FULL_MODEL, rebac_facts(world))
            hits = _hits(world, "openfga")
            model = model_for("openfga", world, history)
            users = random.Random(f"x4b-users-{seed}").sample(sorted(world.users), min(settings["b_users"], len(world.users)))
            cache: dict[str, Any] = {}

            def factory(consistency: str, store: str = store, model_id: str = model_id) -> Callable[[tuple[int, str | None]], Any]:
                def make(_pin: tuple[int, str | None]) -> Any:
                    if consistency not in cache:
                        cache[consistency] = OpenFGAAuthorizer(
                            OPENFGA_URL, store, authorization_model_id=model_id, consistency=consistency,
                            contextual_groups=False,
                        )
                    return cache[consistency]

                return make

            def apply(fact: Fact, adding: bool, _new: frozenset[str], store: str = store, model_id: str = model_id) -> None:
                key = openfga_tuple(fact)
                if adding:
                    self.admin.write(store, model_id, writes=[key])
                else:
                    self.admin.write(store, model_id, deletes=[key])

            common = {"engine": self.engine, "seed": seed, "users": users, "hits": hits, "model": model,
                      "make_subject": Subject, "history": history}
            run_trials(self.ctx, phase="quiet", conditions={"quiet-hc": factory("HIGHER_CONSISTENCY")}, writer=None, **common)
            writer = Writer(self.ctx, world, history, apply,
                            [(DOC_USERS, 0.4), (DOC_BANNED, 0.2), (FOLDER_USERS, 0.2), (USER_GROUPS, 0.2)],
                            settings["b_rate"], seed)
            writer.start(None)
            try:
                run_trials(self.ctx, phase="writer", writer=writer,
                           conditions={"writer-hc": factory("HIGHER_CONSISTENCY"), "writer-ml": factory("MINIMIZE_LATENCY")},
                           **common)
            finally:
                writer.stop()
            _setup_record(self.ctx, engine=self.engine, what=f"b-{seed} writer", writes=history.count, failures=writer.failures)
            self.admin.delete_store(store)

    def part_c(self) -> None:
        Scale(self.ctx, OpenFGAScale(self.ctx)).run()

    def close(self) -> None:
        for store in self.stores:
            self.admin.delete_store(store)


class SpiceDBRunner(Runner):
    engine = "spicedb"
    token = SPICEDB_TOKEN

    def setup(self) -> None:
        self.admin = SpiceDBAdmin(SPICEDB_URL, self.token)
        self.admin.write_schema(SPICEDB_SCHEMA)

    def _write_world(self, world: World, tag: str) -> str:
        started = clock()
        facts = rebac_facts(world)
        self.admin.touch_all([spicedb_relationship(f) for f in facts])
        sentinel = ("tenant", f"x4sentinel{tag}", "member", "user", f"x4sentinel{tag}", "")
        token = self.admin.write([{"operation": "OPERATION_TOUCH", "relationship": spicedb_relationship(sentinel)}])
        _setup_record(self.ctx, engine=self.engine, what=tag, relationships=len(facts), seconds=clock() - started)
        return token

    def _authorizer(self, consistency: Mapping[str, Any]) -> SpiceDBAuthorizer:
        return SpiceDBAuthorizer(
            SPICEDB_URL, self.token, resource_type=f"{SPICEDB_PREFIX}/document", subject_type=f"{SPICEDB_PREFIX}/user",
            group_type=f"{SPICEDB_PREFIX}/group", consistency=consistency,
        )

    def part_a(self) -> None:
        for seed, world in self.worlds():
            token = self._write_world(world, f"a{seed}")
            authorizer = self._authorizer({"atExactSnapshot": {"token": token}})
            measure_subjects(self.ctx, engine=self.engine, profile="spicedb", seed=seed, authorizer=authorizer,
                             users=sorted(world.users), hits=_hits(world, "spicedb"), model=model_for("spicedb", world),
                             make_subject=Subject)

    def part_b(self) -> None:
        settings = self.ctx.settings
        for seed in self.ctx.seeds():
            # Worlds of their own (prefix "b"), so part a's relationships cannot interfere.
            world = make_world(seed, self.size, prefix="b")
            history = History()
            token = self._write_world(world, f"b{seed}")
            time.sleep(6.0)  # past the 5-s quantization window, so minimizeLatency reads see every write
            hits = _hits(world, "spicedb")
            model = model_for("spicedb", world, history)
            users = random.Random(f"x4b-users-{seed}").sample(sorted(world.users), min(settings["b_users"], len(world.users)))
            fixed = {
                "fc": self._authorizer({"fullyConsistent": True}),
                "ml": self._authorizer({"minimizeLatency": True}),
            }

            def pinned(pin: tuple[int, str | None]) -> Any:
                return self._authorizer({"atExactSnapshot": {"token": pin[1]}})

            def apply(fact: Fact, adding: bool, _new: frozenset[str]) -> str:
                operation = "OPERATION_TOUCH" if adding else "OPERATION_DELETE"
                return self.admin.write([{"operation": operation, "relationship": spicedb_relationship(fact)}])

            common = {"engine": self.engine, "seed": seed, "users": users, "hits": hits, "model": model,
                      "make_subject": Subject, "history": history}
            run_trials(self.ctx, phase="quiet", conditions={"quiet-ml": lambda _pin: fixed["ml"]}, writer=None, **common)
            writer = Writer(self.ctx, world, history, apply,
                            [(DOC_USERS, 0.4), (DOC_BANNED, 0.2), (FOLDER_USERS, 0.2), (USER_GROUPS, 0.2)],
                            settings["b_rate"], seed)
            writer.start(token)
            try:
                run_trials(self.ctx, phase="writer", writer=writer, conditions={
                    "writer-pinned": pinned,
                    "writer-fc": lambda _pin: fixed["fc"],
                    "writer-ml": lambda _pin: fixed["ml"],
                }, **common)
            finally:
                writer.stop()
            _setup_record(self.ctx, engine=self.engine, what=f"b-{seed} writer", writes=history.count, failures=writer.failures)

    def part_c(self) -> None:
        Scale(self.ctx, SpiceDBScale(self.ctx, self.admin, self.token)).run()


class OPARunner(Runner):
    engine = "opa"
    profiles = ("opa-acl-doc", "opa-acl-doc-drift", "opa-rel-doc", "opa-rel-pe", "opa-rel-pe-excl")

    def setup(self) -> None:
        self.opa = OpaProcess(8181, log_path=self.ctx.out / "logs" / "opa-x4.log")
        self.opa.start()
        for name in ("x4acl", "x4rel", "x4relx"):
            self.opa.put_policy(name, (POLICIES / "opa" / f"{name}.rego").read_text(encoding="utf-8"))

    def authorizer(self, profile: str, timeout: float = 2.0) -> Any:
        url = self.opa.url
        if profile.startswith("opa-acl-doc"):
            return OPAAuthorizer(url, decisions_path="x4acl/decisions", filter_path="x4acl/filter", timeout=timeout)
        if profile == "opa-rel-doc":
            return OPAAuthorizer(url, decisions_path="x4rel/decisions", filter_path="x4rel/filter", timeout=timeout)
        if profile == "opa-rel-pe":
            return OpaCompileAuthorizer(url, decisions_path="x4rel/decisions", compile_path="x4rel/allow", timeout=timeout)
        return OpaCompileAuthorizer(url, decisions_path="x4relx/decisions", compile_path="x4relx/allow", timeout=timeout)

    @staticmethod
    def subject(world: World, uid: str) -> Subject:
        u = world.users[uid]
        return Subject(uid, u.groups, {"tenant": u.tenant, "clearance": u.clearance})

    def _load(self, world: World) -> None:
        self.opa.put_data("x4acl_world", opa_world(world, shares=False))
        self.opa.put_data("x4rel_world", opa_world(world, shares=True, bans=True))

    def part_a(self) -> None:
        for seed, world in self.worlds():
            self._load(world)
            users = sorted(world.users)
            for profile in self.profiles:
                authorizer = self.authorizer(profile)
                measure_subjects(self.ctx, engine=self.engine, profile=profile, seed=seed, authorizer=authorizer,
                                 users=users, hits=_hits(world, profile), model=model_for(profile, world),
                                 make_subject=lambda uid, world=world: self.subject(world, uid))
                if profile.endswith("-pe"):
                    self._diagnose_compile(world, users[0])

    def _diagnose_compile(self, world: World, uid: str) -> None:
        """The raw answer of one compile call, for the record (an error's body included)."""
        from x4x7_common import ServiceError, call

        payload = {"input": {"subject": opa_subject(self.subject(world, uid)), "action": "read"}, "unknowns": ["input.doc"]}
        try:
            answer = call("POST", f"{self.opa.url}/v1/compile/x4rel/allow", payload,
                          headers={"Accept": OpaCompileAuthorizer.UCAST}, timeout=30)
            self.ctx.records.write({"type": "opa-compile-sample", "user": uid, "answer": str(answer)[:3000]})
        except ServiceError as error:
            self.ctx.records.write({"type": "opa-compile-sample", "user": uid, "status": error.status, "body": error.body})
            annotate("warning", "x4 opa compile", f"HTTP {error.status}: {error.body[:1500]}")

    def part_b(self) -> None:
        settings = self.ctx.settings
        for seed, world in self.worlds():
            self._load(world)
            history = History()
            hits = _hits(world, "opa-acl-doc")
            model = model_for("opa-acl-doc", world, history)
            users = random.Random(f"x4b-users-{seed}").sample(sorted(world.users), min(settings["b_users"], len(world.users)))
            authorizer = self.authorizer("opa-acl-doc")

            def apply(fact: Fact, _adding: bool, new: frozenset[str], world: World = world) -> None:
                folder = world.folders[fact[1]]
                self.opa.put_data(f"x4acl_world/folders/{folder.id}", opa_folder(folder, new))

            common = {"engine": self.engine, "seed": seed, "users": users, "hits": hits, "model": model,
                      "make_subject": lambda uid, world=world: self.subject(world, uid), "history": history}
            run_trials(self.ctx, phase="quiet", conditions={"quiet": lambda _pin: authorizer}, writer=None, **common)
            writer = Writer(self.ctx, world, history, apply, [(FOLDER_USERS, 1.0)], settings["b_rate"], seed)
            writer.start(None)
            try:
                run_trials(self.ctx, phase="writer", writer=writer, conditions={"writer": lambda _pin: authorizer}, **common)
            finally:
                writer.stop()
            _setup_record(self.ctx, engine=self.engine, what=f"b-{seed} writer", writes=history.count, failures=writer.failures)

    def part_c(self) -> None:
        Scale(self.ctx, OPAScale(self.ctx, self)).run()

    def close(self) -> None:
        self.opa.kill()


class CerbosRunner(Runner):
    engine = "cerbos"

    def part_a(self) -> None:
        for seed, world in self.worlds():
            closure = Model(world, folders=False, bans=False, classification=False)
            users = sorted(world.users)

            def make_subject(uid: str, world: World = world, closure: Model = closure) -> Subject:
                u = world.users[uid]
                return Subject(uid, closure.groups_of(uid), {"tenant": u.tenant, "levels": levels_for(u.clearance)})

            for profile in ("cerbos", "cerbos-drift", "cerbos-excl"):
                kind = "x4docx" if profile == "cerbos-excl" else "x4doc"
                authorizer = CerbosAuthorizer(CERBOS_URL, resource_kind=kind)
                measure_subjects(self.ctx, engine=self.engine, profile=profile, seed=seed, authorizer=authorizer,
                                 users=users, hits=_hits(world, profile), model=model_for(profile, world),
                                 make_subject=make_subject)


class ControlsRunner(Runner):
    engine = "controls"

    def part_a(self) -> None:
        for seed, world in self.worlds():
            model = model_for("control-oracle", world)
            users = sorted(world.users)
            hits = _hits(world, "control-oracle")
            docs = [h.id for h in hits]

            def check(subject: Subject, batch: Sequence[Hit], _action: str, model: Model = model) -> list[bool]:
                return [model.allows(subject.id, h.id) for h in batch]

            oracle = FunctionAuthorizer(check, lambda s, _a, model=model, docs=docs: In("doc_id", model.readable(s.id, docs)))
            measure_subjects(self.ctx, engine=self.engine, profile="control-oracle", seed=seed, authorizer=oracle,
                             users=users, hits=hits, model=model, make_subject=Subject)
            rng = random.Random(f"x4a-planted-{seed}")
            filters: dict[str, Filter] = {}
            planted: dict[str, tuple[int, int]] = {}
            for uid in users:
                readable = sorted(model.readable(uid, docs))
                unreadable = sorted(set(docs) - set(readable))
                drop = rng.sample(readable, max(1, round(0.02 * len(readable)))) if readable else []
                add = rng.sample(unreadable, max(1, round(0.02 * len(unreadable)))) if unreadable else []
                filters[uid] = In("doc_id", (set(readable) - set(drop)) | set(add))
                planted[uid] = (len(add), len(drop))
            authorizer = FunctionAuthorizer(check, lambda s, _a, filters=filters: filters[s.id])
            measure_subjects(self.ctx, engine=self.engine, profile="control-planted", seed=seed, authorizer=authorizer,
                             users=users, hits=hits, model=model, make_subject=Subject, planted=planted)


# ---- X4c: truncation at scale ------------------------------------------------------------------------


STRUCTURES = ("simple-direct", "full-direct", "full-folder")
CODES = {"simple-direct": "sd", "full-direct": "fd", "full-folder": "ff", "opa-share": "os"}


class ScaleEngine:
    """What X4c needs from one engine."""

    engine = ""
    structures: tuple[str, ...] = STRUCTURES
    routes: tuple[str, ...] = ("adapter",)

    def setup_corpus(self, n_docs: int, folder_of: Sequence[int]) -> None:
        """Write what every seed shares: documents' tenant and folder relationships."""

    def grant(self, seed: int, grants: Mapping[tuple[str, int], tuple[str, set[int], list[int], list[int]]]) -> None:
        """Write the seed's grants: (structure, N) -> (subject, readable docs, direct docs, folders)."""
        raise NotImplementedError

    def raw(self, structure: str, subject: str, expected: set[str], reps: int) -> list[dict[str, Any]]:
        return []

    def authorizer(self, structure: str, route: str, timeout: float) -> Any:
        raise NotImplementedError

    def subject(self, structure: str, subject: str) -> Subject:
        return Subject(subject)

    def metadata(self, doc: int) -> dict[str, Any]:
        return {"doc_id": f"c{doc}"}


class OpenFGAScale(ScaleEngine):
    engine = "openfga"

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.admin = OpenFGAAdmin(OPENFGA_URL)
        self.simple = self.admin.create_store(f"x4c-{RUN_ID}-simple")
        self.simple_model = self.admin.write_model(self.simple, OPENFGA_SIMPLE_MODEL)
        self.full = self.admin.create_store(f"x4c-{RUN_ID}-full")
        self.full_model = self.admin.write_model(self.full, OPENFGA_FULL_MODEL)

    def setup_corpus(self, n_docs: int, folder_of: Sequence[int]) -> None:
        tuples = [{"user": "tenant:ct0", "relation": "tenant", "object": f"document:c{d}"} for d in range(n_docs)]
        tuples += [{"user": f"folder:cf{folder_of[d]}", "relation": "parent", "object": f"document:c{d}"} for d in range(n_docs)]
        self.admin.write_all(self.full, self.full_model, tuples)

    def grant(self, seed: int, grants: Mapping[tuple[str, int], tuple[str, set[int], list[int], list[int]]]) -> None:
        simple: list[dict[str, str]] = []
        full: list[dict[str, str]] = []
        for (structure, _n), (subject, _readable, direct, folders) in grants.items():
            if structure == "simple-direct":
                simple += [{"user": f"user:{subject}", "relation": "viewer", "object": f"document:c{d}"} for d in direct]
                continue
            full.append({"user": f"user:{subject}", "relation": "member", "object": "tenant:ct0"})
            full += [{"user": f"user:{subject}", "relation": "reader", "object": f"document:c{d}"} for d in direct]
            full += [{"user": f"user:{subject}", "relation": "viewer", "object": f"folder:cf{f}"} for f in folders]
        self.admin.write_all(self.simple, self.simple_model, simple)
        self.admin.write_all(self.full, self.full_model, full)

    def _store(self, structure: str) -> tuple[str, str]:
        return (self.simple, self.simple_model) if structure == "simple-direct" else (self.full, self.full_model)

    def raw(self, structure: str, subject: str, expected: set[str], reps: int) -> list[dict[str, Any]]:
        store, model = self._store(structure)
        out = []
        for rep in range(reps):
            for api in ("list-objects", "streamed-list-objects"):
                method = self.admin.list_objects if api == "list-objects" else self.admin.streamed_list_objects
                answer = method(store, model, type_="document", relation="viewer", user=f"user:{subject}",
                                consistency="HIGHER_CONSISTENCY")
                found = {o.split(":", 1)[1] for o in answer.pop("objects", []) if isinstance(o, str) and ":" in o}
                answer.update({"api": api, "rep": rep, "missing": len(expected - found), "extra": len(found - expected)})
                out.append(answer)
        return out

    def authorizer(self, structure: str, route: str, timeout: float) -> Any:
        store, model = self._store(structure)
        return OpenFGAAuthorizer(OPENFGA_URL, store, authorization_model_id=model, consistency="HIGHER_CONSISTENCY",
                                 contextual_groups=False, timeout=timeout)


class SpiceDBScale(ScaleEngine):
    engine = "spicedb"

    def __init__(self, ctx: Context, admin: SpiceDBAdmin, token: str) -> None:
        self.ctx = ctx
        self.admin = admin
        self.token = token

    @staticmethod
    def _prefix(structure: str) -> str:
        return SPICEDB_SIMPLE_PREFIX if structure == "simple-direct" else SPICEDB_PREFIX

    def setup_corpus(self, n_docs: int, folder_of: Sequence[int]) -> None:
        facts: list[Fact] = [("document", f"c{d}", "tenant", "tenant", "ct0", "") for d in range(n_docs)]
        facts += [("document", f"c{d}", "parent", "folder", f"cf{folder_of[d]}", "") for d in range(n_docs)]
        self.admin.touch_all([spicedb_relationship(f) for f in facts])

    def grant(self, seed: int, grants: Mapping[tuple[str, int], tuple[str, set[int], list[int], list[int]]]) -> None:
        relationships: list[dict[str, Any]] = []
        for (structure, _n), (subject, _readable, direct, folders) in grants.items():
            if structure == "simple-direct":
                relationships += [
                    spicedb_relationship(("document", f"c{d}", "viewer", "user", subject, ""), SPICEDB_SIMPLE_PREFIX)
                    for d in direct
                ]
                continue
            facts: list[Fact] = [("tenant", "ct0", "member", "user", subject, "")]
            facts += [("document", f"c{d}", "reader", "user", subject, "") for d in direct]
            facts += [("folder", f"cf{f}", "viewer", "user", subject, "") for f in folders]
            relationships += [spicedb_relationship(f) for f in facts]
        self.admin.touch_all(relationships)

    def raw(self, structure: str, subject: str, expected: set[str], reps: int) -> list[dict[str, Any]]:
        prefix = self._prefix(structure)
        who = {"object": {"objectType": f"{prefix}/user", "objectId": subject}}
        out = []
        for rep in range(reps):
            for api, limit in (("lookup-limit", 1000), ("lookup-unlimited", None)):
                answer = self.admin.lookup(f"{prefix}/document", "view", who, consistency={"fullyConsistent": True}, limit=limit)
                found = {o for o in answer.pop("objects", []) if isinstance(o, str)}
                answer.update({"api": api, "rep": rep, "missing": len(expected - found), "extra": len(found - expected)})
                out.append(answer)
        return out

    def authorizer(self, structure: str, route: str, timeout: float) -> Any:
        prefix = self._prefix(structure)
        return SpiceDBAuthorizer(SPICEDB_URL, self.token, resource_type=f"{prefix}/document", subject_type=f"{prefix}/user",
                                 group_type=f"{prefix}/group", consistency={"fullyConsistent": True}, timeout=timeout)


class OPAScale(ScaleEngine):
    """OPA shares N documents with the subject through OPA data (the x4rel policy): no list limit to
    truncate, so X4c checks that both routes return exactly N values, and measures latency."""

    engine = "opa"
    structures = ("opa-share",)
    routes = ("opa-rel-doc", "opa-rel-pe")

    def __init__(self, ctx: Context, runner: OPARunner) -> None:
        self.ctx = ctx
        self.runner = runner

    def grant(self, seed: int, grants: Mapping[tuple[str, int], tuple[str, set[int], list[int], list[int]]]) -> None:
        shares: dict[str, list[str]] = {}
        for (_structure, _n), (subject, readable, _direct, _folders) in grants.items():
            for d in readable:
                shares.setdefault(f"c{d}", []).append(subject)
        world = {
            "parents": {},
            "folders": {},
            "up": {},
            "shares": {d: {"users": users, "groups": [], "wildcard": False} for d, users in shares.items()},
        }
        self.runner.opa.put_data("x4rel_world", world)

    def authorizer(self, structure: str, route: str, timeout: float) -> Any:
        return self.runner.authorizer(route, timeout)

    def subject(self, structure: str, subject: str) -> Subject:
        return Subject(subject, (), {"tenant": "ct0", "clearance": 3})

    def metadata(self, doc: int) -> dict[str, Any]:
        return {"doc_id": f"c{doc}", "tenant": "ct0", "owner": "nobody", "classification": LEVELS[0]}


class Scale:
    """X4c and X4d at scale for one engine: a corpus, then per seed new subjects, grants, vectors and
    queries; per (structure, N) the raw list APIs, wardowl's filter_for, retrieval and latency."""

    def __init__(self, ctx: Context, engine: ScaleEngine) -> None:
        self.ctx = ctx
        self.engine = engine
        self.n_docs = ctx.settings["c_docs"]
        self.levels = [n for n in ctx.settings["c_levels"] if n <= self.n_docs]
        self.folder_count = self.n_docs // 10
        order = random.Random("x4c-folders").sample(range(self.n_docs), self.n_docs)
        self.folder_of = [0] * self.n_docs
        self.members: list[list[int]] = [[] for _ in range(self.folder_count)]
        for position, doc in enumerate(order):
            folder = min(position // 10, self.folder_count - 1)
            self.folder_of[doc] = folder
            self.members[folder].append(doc)
        self.metas = [engine.metadata(d) for d in range(self.n_docs)]

    def _grants(self, seed: int) -> dict[tuple[str, int], tuple[str, set[int], list[int], list[int]]]:
        rng = random.Random(f"x4c-grants-{self.engine.engine}-{seed}")
        grants: dict[tuple[str, int], tuple[str, set[int], list[int], list[int]]] = {}
        for structure in self.engine.structures:
            for n in self.levels:
                subject = f"c{seed}{CODES[structure]}{n}"
                if structure == "full-folder":
                    folders = rng.sample(range(self.folder_count), min(n // 10, self.folder_count))
                    readable = {d for f in folders for d in self.members[f]}
                    outside = [d for d in range(self.n_docs) if d not in readable]
                    direct = rng.sample(outside, min(n - len(readable), len(outside)))
                    readable |= set(direct)
                    grants[(structure, n)] = (subject, readable, direct, folders)
                else:
                    direct = rng.sample(range(self.n_docs), n)
                    grants[(structure, n)] = (subject, set(direct), direct, [])
        return grants

    def run(self) -> None:
        from wardowl.backends.faiss import FaissBackend

        ctx, engine = self.ctx, self.engine
        started = clock()
        engine.setup_corpus(self.n_docs, self.folder_of)
        _setup_record(ctx, engine=engine.engine, what="c corpus", docs=self.n_docs, seconds=clock() - started)
        dim = ctx.settings["dim"]
        for seed in ctx.seeds():
            started = clock()
            grants = self._grants(seed)
            engine.grant(seed, grants)
            _setup_record(ctx, engine=engine.engine, what=f"c grants {seed}", seconds=clock() - started,
                          grants=sum(len(g[2]) + len(g[3]) for g in grants.values()))
            vectors = clustered_vectors(1000 + seed, self.n_docs, ctx.settings["c_queries"], dim)
            backend = FaissBackend(None, dim)
            backend.add([Document(f"c{d}", "", engine.metadata(d)) for d in range(self.n_docs)], embeddings=vectors.corpus)
            for (structure, n), (subject_id, readable, _direct, _folders) in sorted(grants.items(), key=lambda kv: (kv[0][1], kv[0][0])):
                expected = {f"c{d}" for d in readable}
                subject = engine.subject(structure, subject_id)
                base = {"engine": engine.engine, "seed": seed, "structure": structure, "n": n, "readable": len(readable)}
                for answer in engine.raw(structure, subject_id, expected, ctx.settings["c_reps"]):
                    ctx.records.write({"type": "x4c-engine-call", **base, **answer})
                for route in engine.routes:
                    for timeout in (2.0, 10.0):
                        self._filter(base, route, timeout, structure, subject, n, expected)
                    self._retrieve(base, route, structure, subject, readable, backend, vectors)
                    batch_docs = sorted(readable)[:5] + [d for d in range(self.n_docs) if d not in readable][:5]
                    batch = [Hit(f"c{d}", "", 1.0, engine.metadata(d)) for d in batch_docs]
                    latency(ctx, engine=engine.engine, route=route, seed=seed, structure=structure, n=n,
                            authorizer=engine.authorizer(structure, route, 30.0), subject=subject, batch=batch)
            log(f"x4c {engine.engine} seed {seed} done")

    def _filter(self, base: Mapping[str, Any], route: str, timeout: float, structure: str, subject: Subject,
                n: int, expected: set[str]) -> None:
        authorizer = self.engine.authorizer(structure, route, timeout)
        rec: dict[str, Any] = {"type": "x4c-filter", **base, "route": route, "timeout": timeout}
        started = clock()
        try:
            f = authorizer.filter_for(subject)
        except Exception as error:
            rec["elapsed_s"] = clock() - started
            info = self.ctx.errors.add(f"x4c {route} filter_for", error)
            rec.update({"outcome": "error", "error": f"{info['class']}: {info['message'][:300]}"})
            self.ctx.records.write(rec)
            return
        rec["elapsed_s"] = clock() - started
        if f is None:
            rec["outcome"] = "none"
        else:
            # What the filter admits, evaluated on every document (OPA's filters are composite).
            admitted = {f"c{d}" for d, meta in enumerate(self.metas) if matches(f, meta)}
            rec["values"] = filter_size(f)
            rec["admitted"] = len(admitted)
            rec["missing"] = len(expected - admitted)
            rec["extra"] = len(admitted - expected)
            if not rec["missing"] and not rec["extra"]:
                rec["outcome"] = "exact"
            else:
                rec["outcome"] = "short" if rec["missing"] else "over"
        if isinstance(authorizer, OpaCompileAuthorizer):
            rec["compile"] = dict(authorizer.last)
        self.ctx.records.write(rec)

    def _retrieve(self, base: Mapping[str, Any], route: str, structure: str, subject: Subject, readable: set[int],
                  backend: Any, vectors: Any) -> None:
        retriever = PermissionedRetriever(backend, self.engine.authorizer(structure, route, 2.0))
        rows = sorted(readable)
        for q, query in enumerate(vectors.queries):
            rec: dict[str, Any] = {"type": "x4c-query", **base, "route": route, "query": q}
            truth, depth = exact_top(vectors.corpus, rows, query, 10)
            started = clock()
            try:
                result = retriever.retrieve(Query(vector=query.tolist()), subject, k=10)
            except Exception as error:
                rec["elapsed_s"] = clock() - started
                info = self.ctx.errors.add(f"x4c {route} retrieve", error)
                rec["error"] = f"{info['class']}: {info['message'][:300]}"
                self.ctx.records.write(rec)
                continue
            rec["elapsed_s"] = clock() - started
            found = [int(h.id[1:]) for h in result.hits]
            rec.update({
                "depth": depth,
                "n_hits": len(found),
                "recall": (len(set(found) & truth) / depth) if depth else None,
                "leaks": sum(1 for d in found if d not in readable),
                "strategy": result.strategy,
                "complete": result.complete,
                "examined": result.examined,
                "violations": result.violations,
            })
            self.ctx.records.write(rec)


# ---- main ----------------------------------------------------------------------------------------------

RUNNERS: dict[str, type[Runner]] = {
    "openfga": OpenFGARunner,
    "spicedb": SpiceDBRunner,
    "opa": OPARunner,
    "cerbos": CerbosRunner,
    "controls": ControlsRunner,
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--engines", required=True, help="comma-separated: " + ", ".join(RUNNERS))
    parser.add_argument("--parts", default="a,b,c")
    parser.add_argument("--profile", choices=sorted(SETTINGS), default="smoke")
    parser.add_argument("--out", default="results")
    args = parser.parse_args(argv)
    settings = SETTINGS[args.profile]
    out = Path(args.out)
    records = Records(out, f"x4-{JOB}")
    errors = Errors()
    ctx = Context(settings, records, errors, out, args.profile)
    engines = [e.strip() for e in args.engines.split(",") if e.strip()]
    parts = [p.strip() for p in args.parts.split(",") if p.strip()]
    records.write(run_info("x4", args.profile, {**_settings_for_record(settings), "engines": engines, "parts": parts}))
    containers = [c for c in ("openfga", "spicedb", "cerbos") if c in engines]
    if "openfga" in engines or "spicedb" in engines:
        containers.append("enginedb")
    records.write(versions_record(containers))
    failed = 0
    for name in engines:
        runner = RUNNERS[name](ctx)
        try:
            runner.setup()
        except Exception as error:
            info = errors.add(f"{name} setup", error)
            records.write({"type": "setup-failed", "engine": name, **info})
            failed += 1
            continue
        try:
            for part in parts:
                started = clock()
                log(f"x4 {name} part {part}: start")
                try:
                    getattr(runner, f"part_{part}")()
                except Exception as error:
                    info = errors.add(f"{name} part {part}", error)
                    records.write({"type": "part-failed", "engine": name, "part": part, **info})
                    failed += 1
                records.write({"type": "part-end", "engine": name, "part": part, "seconds": clock() - started})
                log(f"x4 {name} part {part}: {clock() - started:.0f} s")
        finally:
            try:
                runner.close()
            except Exception as error:
                errors.add(f"{name} close", error)
    records.write({"type": "run-end", "records": records.count, "failed_parts": failed})
    errors.report(records, f"x4 {JOB}")
    annotate("notice", f"x4 {JOB} records", f"{records.count} records, {failed} failed setups or parts, in {records.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
