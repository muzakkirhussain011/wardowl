"""The X4 and X7 worlds: tenants, users, nested groups, folders and documents, how each engine holds
them, and an oracle that evaluates the model in plain Python.

The model (PREREG_X4_X7.md, "The world"): a user may view a document of their own tenant that they
own, read directly, read through a group (nested), read because it is everyone-readable, or read
through a folder (nested), unless they are banned from it directly or through a group. Engines that
see attributes add: the document's classification is at most the user's clearance. Each profile
encodes a part of it (`Model` says which), and the oracle evaluates exactly that part.

Nothing here imports wardowl at module level, so the statistics scripts can import the module too.
The oracle never uses wardowl's filter code.
"""

from __future__ import annotations

import bisect
import random
import threading
from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

LEVELS = ("L0", "L1", "L2", "L3")
SPICEDB_PREFIX = "wox4"  # SpiceDB object type prefixes need at least 3 characters
SPICEDB_SIMPLE_PREFIX = "wox4s"


# ---- the world -------------------------------------------------------------------------------------


@dataclass
class User:
    id: str
    tenant: str
    clearance: int
    groups: frozenset[str]  # direct memberships


@dataclass
class Folder:
    id: str
    parent: str | None
    users: frozenset[str]
    groups: frozenset[str]
    wildcard: bool


@dataclass
class Doc:
    id: str
    tenant: str
    folder: str | None
    owner: str
    users: frozenset[str]
    groups: frozenset[str]
    wildcard: bool
    classification: int
    banned_users: frozenset[str]
    banned_groups: frozenset[str]
    drift: bool = False  # stores one-value ACL lists as scalars in the drift profiles


@dataclass
class World:
    seed: int
    tenants: list[str]
    users: dict[str, User]
    groups: dict[str, tuple[str, ...]]  # group -> its parent groups (a member of it is a member of them)
    folders: dict[str, Folder]
    docs: dict[str, Doc]

    def users_of(self, tenant: str) -> list[str]:
        return [u.id for u in self.users.values() if u.tenant == tenant]


@dataclass(frozen=True)
class WorldSize:
    tenants: int = 3
    users_per_tenant: int = 40
    groups: int = 60
    folders: int = 80
    docs: int = 1500


def _sample(rng: random.Random, pool: Sequence[str], low: int, high: int) -> frozenset[str]:
    count = min(len(pool), rng.randint(low, high))
    return frozenset(rng.sample(list(pool), count))


def make_world(seed: int, size: WorldSize, prefix: str = "s") -> World:
    """The seeded world of PREREG_X4_X7.md. Ids carry `prefix` and the seed (letters and digits only,
    valid in every engine)."""
    rng = random.Random(f"x4x7-world-{prefix}-{seed}")
    tag = f"{prefix}{seed}"
    tenants = [f"{tag}t{j}" for j in range(size.tenants)]
    group_ids = [f"{tag}g{j}" for j in range(size.groups)]

    # Groups: 0, 1 or 2 parents among earlier groups, at most 4 levels of nesting.
    groups: dict[str, tuple[str, ...]] = {}
    height: dict[str, int] = {}
    for j, g in enumerate(group_ids):
        parents: list[str] = []
        if j > 0:
            wanted = rng.choices((0, 1, 2), weights=(0.5, 0.35, 0.15))[0]
            for candidate in rng.sample(group_ids[:j], min(wanted, j)):
                if height[candidate] + 1 <= 3:
                    parents.append(candidate)
        groups[g] = tuple(sorted(parents))
        height[g] = 0 if not parents else 1 + max(height[p] for p in parents)

    users: dict[str, User] = {}
    for t in tenants:
        for j in range(size.users_per_tenant):
            uid = f"{t}u{j}"
            users[uid] = User(uid, t, rng.randrange(4), _sample(rng, group_ids, 0, 4))
    user_ids = list(users)

    folders: dict[str, Folder] = {}
    depth: dict[str, int] = {}
    folder_ids = [f"{tag}f{j}" for j in range(size.folders)]
    for j, f in enumerate(folder_ids):
        parent = None
        if j > 0 and rng.random() < 0.7:
            candidates = [c for c in folder_ids[:j] if depth[c] < 3]
            if candidates:
                parent = rng.choice(candidates)
        depth[f] = 0 if parent is None else depth[parent] + 1
        folders[f] = Folder(
            f, parent, _sample(rng, user_ids, 0, 2), _sample(rng, group_ids, 0, 2), rng.random() < 0.02
        )

    world = World(seed, tenants, users, groups, folders, {})
    plain = Model(world, folders=True, bans=False, classification=False)
    for j in range(size.docs):
        did = f"{tag}d{j}"
        tenant = rng.choice(tenants)
        folder = rng.choice(folder_ids) if rng.random() < 0.6 else None
        local = world.users_of(tenant)
        owner = rng.choice(local) if rng.random() < 0.9 else rng.choice(user_ids)
        doc = Doc(
            id=did,
            tenant=tenant,
            folder=folder,
            owner=owner,
            users=_sample(rng, user_ids, 0, 3),
            groups=_sample(rng, group_ids, 0, 2),
            wildcard=rng.random() < 0.03,
            classification=rng.randrange(4),
            banned_users=frozenset(),
            banned_groups=frozenset(),
        )
        world.docs[did] = doc
        if rng.random() < 0.1:
            readers = [u for u in local if plain.allows(u, did)]
            pool = readers or local
            doc.banned_users = _sample(rng, pool, 1, 2)
        if rng.random() < 0.03:
            doc.banned_groups = frozenset({rng.choice(group_ids)})
        doc.drift = rng.random() < 0.1
    return world


# ---- facts that change (X4b's writer, X7's revocations) --------------------------------------------

# A mutable fact family names a set-valued attribute of one object.
DOC_USERS = "doc_users"  # a document's direct readers
DOC_BANNED = "doc_banned"  # a document's banned users
FOLDER_USERS = "folder_users"  # a folder's direct viewers
USER_GROUPS = "user_groups"  # a user's direct groups


class History:
    """Every change to the mutable facts, numbered from 1 in commit order. State i is the world after
    the first i changes; state 0 is the world as generated."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: dict[tuple[str, str], tuple[list[int], list[frozenset[str]]]] = {}
        self.count = 0

    def record(self, family: str, key: str, value: frozenset[str]) -> int:
        with self._lock:
            self.count += 1
            indexes, values = self._entries.setdefault((family, key), ([], []))
            indexes.append(self.count)
            values.append(value)
            return self.count

    def value(self, family: str, key: str, state: int | None, base: frozenset[str]) -> frozenset[str]:
        entry = self._entries.get((family, key))
        if entry is None:
            return base
        indexes, values = entry
        if state is None:
            return values[-1]
        position = bisect.bisect_right(indexes, state) - 1
        return values[position] if position >= 0 else base


class Model:
    """The model as one profile encodes it, evaluated in Python (the oracle).

    `folders`: folder grants count; `bans`: banned users and groups exclude; `classification`: the
    document's level must be at most the user's clearance. `history` and a `state` give the world
    after that many changes.
    """

    def __init__(
        self,
        world: World,
        *,
        folders: bool,
        bans: bool,
        classification: bool,
        history: History | None = None,
    ) -> None:
        self.world = world
        self.folders = folders
        self.bans = bans
        self.classification = classification
        self.history = history
        self._closures: dict[frozenset[str], frozenset[str]] = {}

    def _value(self, family: str, key: str, state: int | None, base: frozenset[str]) -> frozenset[str]:
        if self.history is None:
            return base
        return self.history.value(family, key, state, base)

    def closure(self, direct: Iterable[str]) -> frozenset[str]:
        """The groups in `direct` and every group they are nested in."""
        start = frozenset(direct)
        known = self._closures.get(start)
        if known is not None:
            return known
        seen: set[str] = set()
        stack = list(start)
        while stack:
            g = stack.pop()
            if g in seen:
                continue
            seen.add(g)
            stack.extend(self.world.groups.get(g, ()))
        result = frozenset(seen)
        self._closures[start] = result
        return result

    def groups_of(self, user: str, state: int | None = None) -> frozenset[str]:
        base = self.world.users[user].groups
        return self.closure(self._value(USER_GROUPS, user, state, base))

    def folder_view(self, user: str, groups: frozenset[str], folder: str | None, state: int | None) -> bool:
        while folder is not None:
            info = self.world.folders[folder]
            viewers = self._value(FOLDER_USERS, folder, state, info.users)
            if user in viewers or groups & info.groups or info.wildcard:
                return True
            folder = info.parent
        return False

    def allows(self, user: str, doc_id: str, state: int | None = None) -> bool:
        u = self.world.users[user]
        doc = self.world.docs[doc_id]
        if doc.tenant != u.tenant:
            return False
        if self.classification and doc.classification > u.clearance:
            return False
        groups = self.groups_of(user, state)
        readers = self._value(DOC_USERS, doc_id, state, doc.users)
        read = (
            doc.owner == user
            or user in readers
            or bool(groups & doc.groups)
            or doc.wildcard
            or (self.folders and self.folder_view(user, groups, doc.folder, state))
        )
        if not read:
            return False
        if self.bans:
            banned = self._value(DOC_BANNED, doc_id, state, doc.banned_users)
            if user in banned or groups & doc.banned_groups:
                return False
        return True

    def readable(self, user: str, docs: Iterable[str], state: int | None = None) -> set[str]:
        return {d for d in docs if self.allows(user, d, state)}


# ---- how each profile sees the model -----------------------------------------------------------------

# Which parts of the model each X4 profile encodes (PREREG_X4_X7.md, "Profiles").
PROFILE_MODEL: dict[str, dict[str, bool]] = {
    "openfga": {"folders": True, "bans": True, "classification": False},
    "openfga-ctx": {"folders": True, "bans": True, "classification": False},
    "spicedb": {"folders": True, "bans": True, "classification": False},
    "opa-acl-doc": {"folders": True, "bans": False, "classification": True},
    "opa-acl-doc-drift": {"folders": True, "bans": False, "classification": True},
    "opa-rel-doc": {"folders": True, "bans": False, "classification": True},
    "opa-rel-pe": {"folders": True, "bans": False, "classification": True},
    "opa-rel-pe-excl": {"folders": True, "bans": True, "classification": True},
    "cerbos": {"folders": False, "bans": False, "classification": True},
    "cerbos-drift": {"folders": False, "bans": False, "classification": True},
    "cerbos-excl": {"folders": False, "bans": True, "classification": True},
    "control-oracle": {"folders": True, "bans": True, "classification": False},
    "control-planted": {"folders": True, "bans": True, "classification": False},
}


def model_for(profile: str, world: World, history: History | None = None) -> Model:
    return Model(world, history=history, **PROFILE_MODEL[profile])


def _acl_value(values: Sequence[str], drift: bool) -> Any:
    """A list ACL field, or its one value as a scalar for a drift document."""
    return values[0] if drift and len(values) == 1 else list(values)


def metadata_for(profile: str, doc: Doc) -> dict[str, Any]:
    """The chunk metadata a profile's store holds for `doc`."""
    if profile.startswith(("openfga", "spicedb", "control")):
        return {"doc_id": doc.id}
    level = LEVELS[doc.classification]
    if profile.startswith("opa-rel"):
        meta: dict[str, Any] = {"doc_id": doc.id, "tenant": doc.tenant, "owner": doc.owner, "classification": level}
        if doc.folder is not None:
            meta["folder"] = doc.folder
        return meta
    drift = doc.drift and profile.endswith("-drift")
    groups = sorted(doc.groups) + (["*"] if doc.wildcard else [])
    meta = {
        "doc_id": doc.id,
        "tenant": doc.tenant,
        "owner": doc.owner,
        "classification": level,
        "allowed_users": _acl_value(sorted(doc.users), drift),
        "allowed_groups": _acl_value(groups, drift),
    }
    if doc.folder is not None and profile.startswith("opa"):
        meta["folder"] = doc.folder
    if profile == "cerbos-excl":
        meta["banned_users"] = sorted(doc.banned_users)
        meta["banned_groups"] = sorted(doc.banned_groups)
    return meta


def has_scalar_acl(metadata: Mapping[str, Any]) -> bool:
    """True when an ACL field of the metadata holds one value rather than a list."""
    return any(
        name in metadata and not isinstance(metadata[name], list) for name in ("allowed_users", "allowed_groups")
    )


def levels_for(clearance: int) -> list[str]:
    return list(LEVELS[: clearance + 1])


# ---- relationship tuples (OpenFGA and SpiceDB) ---------------------------------------------------------

Fact = tuple[str, str, str, str, str, str]  # object type, object id, relation, subject type, subject id, subject relation


def rebac_facts(world: World, *, stored_groups: bool = True) -> list[Fact]:
    """Every relationship of the ReBAC encoding. Direct group memberships are left out when they are
    sent as contextual tuples instead (`stored_groups=False`)."""
    out: list[Fact] = []
    for u in world.users.values():
        out.append(("tenant", u.tenant, "member", "user", u.id, ""))
        if stored_groups:
            out += [("group", g, "member", "user", u.id, "") for g in sorted(u.groups)]
    for g, parents in world.groups.items():
        out += [("group", p, "member", "group", g, "member") for p in parents]
    for f in world.folders.values():
        if f.parent is not None:
            out.append(("folder", f.id, "parent", "folder", f.parent, ""))
        out += [("folder", f.id, "viewer", "user", u, "") for u in sorted(f.users)]
        out += [("folder", f.id, "viewer", "group", g, "member") for g in sorted(f.groups)]
        if f.wildcard:
            out.append(("folder", f.id, "viewer", "user", "*", ""))
    for d in world.docs.values():
        out.append(("document", d.id, "tenant", "tenant", d.tenant, ""))
        if d.folder is not None:
            out.append(("document", d.id, "parent", "folder", d.folder, ""))
        out.append(("document", d.id, "owner", "user", d.owner, ""))
        out += [("document", d.id, "reader", "user", u, "") for u in sorted(d.users)]
        out += [("document", d.id, "reader", "group", g, "member") for g in sorted(d.groups)]
        if d.wildcard:
            out.append(("document", d.id, "reader", "user", "*", ""))
        out += [("document", d.id, "banned", "user", u, "") for u in sorted(d.banned_users)]
        out += [("document", d.id, "banned", "group", g, "member") for g in sorted(d.banned_groups)]
    return list(dict.fromkeys(out))


def openfga_tuple(fact: Fact) -> dict[str, str]:
    otype, oid, relation, stype, sid, srel = fact
    user = f"{stype}:{sid}" + (f"#{srel}" if srel else "")
    return {"user": user, "relation": relation, "object": f"{otype}:{oid}"}


def spicedb_relationship(fact: Fact, prefix: str = SPICEDB_PREFIX) -> dict[str, Any]:
    otype, oid, relation, stype, sid, srel = fact
    subject: dict[str, Any] = {"object": {"objectType": f"{prefix}/{stype}", "objectId": sid}}
    if srel:
        subject["optionalRelation"] = srel
    return {
        "resource": {"objectType": f"{prefix}/{otype}", "objectId": oid},
        "relation": relation,
        "subject": subject,
    }


def _this() -> dict[str, Any]:
    return {"this": {}}


def _computed(relation: str) -> dict[str, Any]:
    return {"computedUserset": {"object": "", "relation": relation}}


def _from(tupleset: str, relation: str) -> dict[str, Any]:
    return {
        "tupleToUserset": {
            "tupleset": {"object": "", "relation": tupleset},
            "computedUserset": {"object": "", "relation": relation},
        }
    }


_USERS = [{"type": "user"}, {"type": "user", "wildcard": {}}, {"type": "group", "relation": "member"}]

# The X4 model in OpenFGA (schema 1.1, JSON as the API takes it).
OPENFGA_FULL_MODEL: dict[str, Any] = {
    "schema_version": "1.1",
    "type_definitions": [
        {"type": "user"},
        {
            "type": "tenant",
            "relations": {"member": _this()},
            "metadata": {"relations": {"member": {"directly_related_user_types": [{"type": "user"}]}}},
        },
        {
            "type": "group",
            "relations": {"member": _this()},
            "metadata": {
                "relations": {
                    "member": {"directly_related_user_types": [{"type": "user"}, {"type": "group", "relation": "member"}]}
                }
            },
        },
        {
            "type": "folder",
            "relations": {"parent": _this(), "viewer": {"union": {"child": [_this(), _from("parent", "viewer")]}}},
            "metadata": {
                "relations": {
                    "parent": {"directly_related_user_types": [{"type": "folder"}]},
                    "viewer": {"directly_related_user_types": _USERS},
                }
            },
        },
        {
            "type": "document",
            "relations": {
                "tenant": _this(),
                "parent": _this(),
                "owner": _this(),
                "banned": _this(),
                "reader": {"union": {"child": [_this(), _computed("owner"), _from("parent", "viewer")]}},
                "viewer": {
                    "difference": {
                        "base": {"intersection": {"child": [_computed("reader"), _from("tenant", "member")]}},
                        "subtract": _computed("banned"),
                    }
                },
            },
            "metadata": {
                "relations": {
                    "tenant": {"directly_related_user_types": [{"type": "tenant"}]},
                    "parent": {"directly_related_user_types": [{"type": "folder"}]},
                    "owner": {"directly_related_user_types": [{"type": "user"}]},
                    "banned": {
                        "directly_related_user_types": [{"type": "user"}, {"type": "group", "relation": "member"}]
                    },
                    "reader": {"directly_related_user_types": _USERS},
                }
            },
        },
    ],
}

# X4c's simple-direct structure: one direct relation, nothing to intersect or exclude.
OPENFGA_SIMPLE_MODEL: dict[str, Any] = {
    "schema_version": "1.1",
    "type_definitions": [
        {"type": "user"},
        {
            "type": "document",
            "relations": {"viewer": _this()},
            "metadata": {"relations": {"viewer": {"directly_related_user_types": [{"type": "user"}]}}},
        },
    ],
}

SPICEDB_SCHEMA = f"""
definition {SPICEDB_PREFIX}/user {{}}

definition {SPICEDB_PREFIX}/tenant {{
    relation member: {SPICEDB_PREFIX}/user
}}

definition {SPICEDB_PREFIX}/group {{
    relation member: {SPICEDB_PREFIX}/user | {SPICEDB_PREFIX}/group#member
}}

definition {SPICEDB_PREFIX}/folder {{
    relation parent: {SPICEDB_PREFIX}/folder
    relation viewer: {SPICEDB_PREFIX}/user | {SPICEDB_PREFIX}/user:* | {SPICEDB_PREFIX}/group#member
    permission view = viewer + parent->view
}}

definition {SPICEDB_PREFIX}/document {{
    relation tenant: {SPICEDB_PREFIX}/tenant
    relation parent: {SPICEDB_PREFIX}/folder
    relation owner: {SPICEDB_PREFIX}/user
    relation reader: {SPICEDB_PREFIX}/user | {SPICEDB_PREFIX}/user:* | {SPICEDB_PREFIX}/group#member
    relation banned: {SPICEDB_PREFIX}/user | {SPICEDB_PREFIX}/group#member
    permission read = reader + owner + parent->view
    permission view = (read & tenant->member) - banned
}}

definition {SPICEDB_SIMPLE_PREFIX}/user {{}}

definition {SPICEDB_SIMPLE_PREFIX}/document {{
    relation viewer: {SPICEDB_SIMPLE_PREFIX}/user
    permission view = viewer
}}
"""


# ---- OPA data ------------------------------------------------------------------------------------------


def opa_world(world: World, *, shares: bool, bans: bool = False) -> dict[str, Any]:
    """The OPA data document: group nesting, folders (with each folder's path upwards) and, for the
    relational profiles, each document's sharing and bans."""
    data: dict[str, Any] = {
        "parents": {g: list(p) for g, p in world.groups.items()},
        "folders": {f.id: opa_folder(f) for f in world.folders.values()},
        "up": {f.id: [f.parent] if f.parent else [] for f in world.folders.values()},
    }
    if shares:
        data["shares"] = {
            d.id: {"users": sorted(d.users), "groups": sorted(d.groups), "wildcard": d.wildcard}
            for d in world.docs.values()
        }
    if bans:
        data["bans"] = {
            d.id: {"users": sorted(d.banned_users), "groups": sorted(d.banned_groups)}
            for d in world.docs.values()
            if d.banned_users or d.banned_groups
        }
    return data


def opa_folder(folder: Folder, users: Iterable[str] | None = None) -> dict[str, Any]:
    return {
        "parent": folder.parent,
        "users": sorted(folder.users if users is None else users),
        "groups": sorted(folder.groups),
        "wildcard": folder.wildcard,
    }


# ---- vectors -------------------------------------------------------------------------------------------


@dataclass
class Vectors:
    """Seeded clustered unit vectors (float32): `corpus` rows and `queries` rows."""

    corpus: Any
    queries: Any
    centres: Any = field(repr=False, default=None)


def clustered_vectors(seed: int, n: int, n_queries: int, dim: int, clusters: int = 200) -> Vectors:
    """Each vector is a cluster centre plus Gaussian noise of norm about 0.5, normalized."""
    import numpy as np

    rng = np.random.default_rng(seed)
    centres = rng.standard_normal((clusters, dim)).astype("float32")
    centres /= np.linalg.norm(centres, axis=1, keepdims=True)

    def draw(count: int) -> Any:
        picks = rng.integers(0, clusters, size=count)
        noise = rng.standard_normal((count, dim)).astype("float32") * (0.5 / np.sqrt(dim))
        rows = centres[picks] + noise
        rows /= np.linalg.norm(rows, axis=1, keepdims=True)
        return rows.astype("float32")

    return Vectors(draw(n), draw(n_queries), centres)


def exact_top(vectors: Any, readable: Sequence[int], query: Any, k: int, epsilon: float = 1e-4) -> tuple[set[int], int]:
    """T*_epsilon over the readable rows (PREREG_X4_X7.md, permission-recall@k): the rows within
    epsilon of the k-th best score, and min(k, |readable|)."""
    import numpy as np

    if not readable:
        return set(), 0
    rows = np.asarray(readable, dtype="int64")
    scores = vectors[rows] @ query
    depth = min(k, len(rows))
    kth = np.partition(scores, len(rows) - depth)[len(rows) - depth]
    chosen = rows[scores >= kth - epsilon]
    return {int(r) for r in chosen}, depth


def chunks(items: Sequence[Any], size: int) -> Iterator[Sequence[Any]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]
