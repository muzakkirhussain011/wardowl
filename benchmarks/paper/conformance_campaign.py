"""The paper's differential conformance campaign: wardowl's conformance kit against real stores and engines.

For each target (a vector store, an authorization engine with a policy, or a control) and each
seed, it runs `wardowl.testing.check_backend` or `wardowl.testing.check_authorizer` on the kit's
own adversarial data and on stress variants of that data: larger corpora, deeper and wider filters,
very long strings, Unicode and case confusables, numeric-looking strings and odd field names for
the stores; many groups, many hits, confusable and long identifiers and scalar permission fields
for the engines. A variant changes only what the kit generates. The checks, the reference
semantics (`wardowl.filters.matches`) and the kit's oracle are the kit's, unchanged.

Every (target, seed, variant) is one JSON line in results/campaign.jsonl, whatever happens:

* pass: the kit found nothing;
* conformance-violation: the kit raised ConformanceError (the first disagreement it found), with
  the kind of disagreement and a reproducer (documents, filter, expected and returned ids);
* refused-ValueError: wardowl's adapter refused the data or a filter with ValueError (a store that
  cannot express a field name or a filter may refuse; it may not answer wrongly);
* error: anything else (a crash, a server error, a timeout), with its class and message.

    python benchmarks/paper/conformance_campaign.py run --targets memory,metadata-acl --seeds 2
    python benchmarks/paper/conformance_campaign.py summarize results/campaign.jsonl --summary results/summary.md
    python benchmarks/paper/conformance_campaign.py check results/campaign.jsonl

The servers come from .github/workflows/paper-conformance.yml, which runs this in GitHub Actions.
What it tests and how to read and use the results: CONFORMANCE.md, next to this file.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import importlib.metadata
import json
import os
import platform
import random
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import Counter, defaultdict
from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA = 1
ROOT = Path(__file__).resolve().parents[2]
POLICIES = ROOT / "acceptance" / "policies"
DIM = 16  # HashingEmbedder's default, and the vector size of the Vespa application in examples/vespa

PASS = "pass"
VIOLATION = "conformance-violation"
REFUSED = "refused-ValueError"
ERROR = "error"
OUTCOMES = (PASS, VIOLATION, REFUSED, ERROR)
RANK = {PASS: 0, REFUSED: 1, ERROR: 2, VIOLATION: 3}

MESSAGE_LIMIT = 4000  # characters of an error message kept in a record
STRING_LIMIT = 300  # characters of one string kept in a reproducer
LIST_LIMIT = 40  # items of one list kept in a reproducer
DOCUMENT_LIMIT = 40  # documents kept in a reproducer

GROUP = os.environ.get("CAMPAIGN_GROUP", "local")
RUN_ID = os.environ.get("GITHUB_RUN_ID", "local")
SCRIPT = "benchmarks/paper/conformance_campaign.py"

# A ValueError raised in these modules comes from the harness's own data, not from an adapter.
HARNESS_MODULES = ("wardowl.testing", "wardowl.types", "wardowl.filters")
# What the variants patch in wardowl.testing; the run stops if the kit no longer has one of them.
KIT_NAMES = ("_STRINGS", "_INTS", "_FIELDS", "_ODD_FIELDS", "_USERS", "_GROUPS", "_MANY", "random_filter")
KIT_GENERATORS = ("_subject", "_acl_documents", "check_backend", "check_authorizer", "ConformanceError")


# ---- the stress variants's data --------------------------------------------------------------


def _long(length: int, end: str, fill: str = "x") -> str:
    """A string of `length` characters that differs from its siblings only in its last one."""
    return fill * (length - len(end)) + end


E_ACUTE = "\N{LATIN SMALL LETTER E WITH ACUTE}"
E_ACUTE_DECOMPOSED = "e\N{COMBINING ACUTE ACCENT}"
SHARP_S = "\N{LATIN SMALL LETTER SHARP S}"

# Strings a filter must keep apart: equal only for a store that folds case, normalises Unicode
# (NFC or NFKC), trims spaces or drops zero-width characters.
UNICODE_STRINGS = (
    "a",
    "A",
    E_ACUTE,
    E_ACUTE_DECOMPOSED,
    SHARP_S,
    "ss",  # what case folding makes of the sharp s
    "SS",
    "\N{LATIN CAPITAL LETTER SHARP S}",
    "\N{LATIN SMALL LIGATURE FI}",
    "fi",  # what NFKC makes of the ligature
    "\N{FULLWIDTH LATIN CAPITAL LETTER A}",
    "\N{KELVIN SIGN}",  # K under NFC
    "K",
    "k",
    "\N{ANGSTROM SIGN}",
    "\N{LATIN CAPITAL LETTER A WITH RING ABOVE}",
    "A\N{COMBINING RING ABOVE}",  # the three are one letter under NFC
    "\N{LATIN CAPITAL LETTER I WITH DOT ABOVE}",
    "i\N{COMBINING DOT ABOVE}",
    "\N{LATIN SMALL LETTER DOTLESS I}",
    "I",
    "i",
    "\N{HANGUL SYLLABLE HAN}",
    "\N{HANGUL CHOSEONG HIEUH}\N{HANGUL JUNGSEONG A}\N{HANGUL JONGSEONG NIEUN}",  # the same syllable as jamo
    "e\N{COMBINING ACUTE ACCENT}\N{COMBINING DOT BELOW}",
    "e\N{COMBINING DOT BELOW}\N{COMBINING ACUTE ACCENT}",  # the same two marks: equal after NFC
    "a\N{ZERO WIDTH SPACE}",
    "a ",
    " a",
    "\N{GRINNING FACE}",  # outside the Basic Multilingual Plane
)
UNICODE_USERS = (
    "bob",
    "Bob",
    "BOB",
    "zo\N{LATIN SMALL LETTER E WITH DIAERESIS}",
    "zoe\N{COMBINING DIAERESIS}",
    f"stra{SHARP_S}e",
    "strasse",
    "\N{LATIN SMALL LIGATURE FI}ona",
    "fiona",
    "\N{KELVIN SIGN}ate",
    "Kate",
)
UNICODE_GROUPS = (
    "eng",
    "Eng",
    "ENG",
    "\N{FULLWIDTH LATIN SMALL LETTER E}\N{FULLWIDTH LATIN SMALL LETTER N}\N{FULLWIDTH LATIN SMALL LETTER G}",
    "hr",
    "HR",
    SHARP_S,
    "ss",
    E_ACUTE,
    E_ACUTE_DECOMPOSED,
    "1",
)

# Strings that read as numbers, beside integers at the edges of 32-bit, 53-bit (a double's exact
# integers) and 64-bit storage: equal only for a store that converts types or rounds.
NUMERIC_STRINGS = (
    "1",
    "01",
    "1.0",
    "1e0",
    "+1",
    " 1",
    "1 ",
    "0",
    "-0",
    "0x1",
    "\N{ARABIC-INDIC DIGIT ONE}",
    "\N{FULLWIDTH DIGIT ONE}",
    "\N{SUPERSCRIPT ONE}",
    "true",
    "True",
    "null",
    "NaN",
    "Infinity",
    "9007199254740993",
    "9223372036854775808",
)
NUMERIC_INTS = (0, 1, -1, 10, 2**31 - 1, 2**31, 2**53, 2**53 + 1, 2**63 - 1, -(2**63))
NUMERIC_USERS = ("7", "007", "7.0", "\N{ARABIC-INDIC DIGIT SEVEN}", "alice")
NUMERIC_GROUPS = ("1", "01", "1.0", "\N{ARABIC-INDIC DIGIT ONE}", "\N{FULLWIDTH DIGIT ONE}", "0", "-0", "true")

LONG_STRINGS = (
    *(_long(length, end) for length in (256, 1024, 8192) for end in "ab"),
    _long(3001, "a", E_ACUTE),  # 3,000 two-byte letters, then the one that differs
    _long(3001, "b", E_ACUTE),
)
HUGE_STRINGS = (
    _long(32766, "a"),  # Lucene's longest term, in bytes
    _long(32766, "b"),
    _long(40000, "a"),
    _long(20001, "a", E_ACUTE),  # 40,001 bytes in UTF-8
)
LONG_USERS = ("u" * 64, _long(256, "a", "u"), _long(256, "b", "u"), "u" * 1024, "u" * 4096)
LONG_GROUPS = ("g" * 64, _long(256, "a", "g"), _long(256, "b", "g"), "g" * 1024, "g" * 4096)

# Field names a query language may read as syntax, or that collide with what a store keeps beside
# the metadata. A store may refuse to filter on them (ValueError); it may not answer wrongly.
ODD_FIELDS = (
    "a.b.c",
    ".lead",
    "trail.",
    "metadata.team",
    "metadata",
    "allowed_groups.0",
    "tags[]",
    'say"hi',
    "a'b",
    "a\\b",
    "a/b",
    "a:b",
    "team name",
    " team",
    "$in",
    "$where",
    "_id",
    "id",
    "content",
    "embedding",
    "text",
    "wardowl_terms",
    "Team",
    "TEAM",
    "\N{CJK UNIFIED IDEOGRAPH-65E5}\N{CJK UNIFIED IDEOGRAPH-672C}\N{CJK UNIFIED IDEOGRAPH-8A9E}",  # "Japanese"
    "gr\N{LATIN SMALL LETTER O WITH DIAERESIS}" + SHARP_S + "e",  # composed
    "gro\N{COMBINING DIAERESIS}" + SHARP_S + "e",  # the same name, decomposed
)

DECOY_GROUPS = tuple(f"grp-{i:04d}" for i in range(1000))
TENANTS = ("northwind", "globex", "Northwind", "acme")


def _decoys(count: int) -> list[str | int]:
    """`count` filter values no generated document holds, strings and integers."""
    half = count // 2
    return [*(f"grp-{i:04d}" for i in range(half)), *range(100_000, 100_000 + count - half)]


def _leaf(rng: random.Random, kit: Any) -> Any:
    """One In, drawn as the kit draws it (reading the kit's current pools)."""
    from wardowl.filters import In

    values: list[str | int] = [rng.choice((*kit._STRINGS, *kit._INTS)) for _ in range(rng.randint(0, 3))]
    if rng.random() < 0.1:
        values += kit._MANY
    return In(rng.choice(kit._FIELDS), values)


def _kit_like_filter(rng: random.Random, depth: int, kit: Any) -> Any:
    """The kit's random_filter, recursing into itself rather than into whatever is patched in."""
    from wardowl.filters import And, Or

    if depth <= 0 or rng.random() < 0.4:
        return _leaf(rng, kit)
    clauses = [_kit_like_filter(rng, depth - 1, kit) for _ in range(rng.randint(1, 3))]
    return And(*clauses) if rng.random() < 0.5 else Or(*clauses)


def _deep_filter(rng: random.Random, depth: int, kit: Any) -> Any:
    from wardowl.filters import And, Or

    if depth <= 0 or rng.random() < 0.2:
        return _leaf(rng, kit)
    clauses = [_deep_filter(rng, depth - 1, kit) for _ in range(rng.randint(1, 4))]
    return And(*clauses) if rng.random() < 0.5 else Or(*clauses)


def _wide_filter(rng: random.Random, depth: int, kit: Any) -> Any:
    """Filters the shape of a subject in many groups: In over 100 or 1,000 values, Or over 100 or
    1,000 one-value clauses, or such an In under an And; one in ten is the kit's own."""
    from wardowl.filters import And, In, Or

    real = rng.sample((*kit._STRINGS, *kit._INTS), rng.randint(1, 3))
    field = "allowed_groups" if rng.random() < 0.5 else rng.choice(kit._FIELDS)
    shape = rng.random()
    if shape < 0.2:
        return In(field, [*real, *_decoys(100 - len(real))])
    if shape < 0.4:
        return In(field, [*real, *_decoys(1000 - len(real))])
    if shape < 0.75:
        values = [*real, *_decoys((100 if shape < 0.6 else 1000) - len(real))]
        rng.shuffle(values)
        return Or(*(In(field, [value]) for value in values))
    if shape < 0.9:
        return And(_leaf(rng, kit), In(field, [*real, *_decoys(1000 - len(real))]))
    return _kit_like_filter(rng, depth, kit)


def _patch_deep(kit: Any) -> dict[str, Any]:
    return {"random_filter": lambda rng, depth=2: _deep_filter(rng, rng.randint(3, 6), kit)}


def _patch_wide(kit: Any) -> dict[str, Any]:
    return {"random_filter": lambda rng, depth=2: _wide_filter(rng, depth, kit)}


def _patch_long(kit: Any) -> dict[str, Any]:
    return {
        "_STRINGS": (*kit._STRINGS, *LONG_STRINGS),
        "_USERS": (*kit._USERS, *LONG_USERS),
        "_GROUPS": (*kit._GROUPS, *LONG_GROUPS),
    }


def _patch_huge(kit: Any) -> dict[str, Any]:
    return {"_STRINGS": (*kit._STRINGS, *HUGE_STRINGS)}


def _patch_unicode(kit: Any) -> dict[str, Any]:
    return {"_STRINGS": UNICODE_STRINGS, "_USERS": UNICODE_USERS, "_GROUPS": UNICODE_GROUPS}


def _patch_numeric(kit: Any) -> dict[str, Any]:
    return {"_STRINGS": NUMERIC_STRINGS, "_INTS": NUMERIC_INTS, "_USERS": NUMERIC_USERS, "_GROUPS": NUMERIC_GROUPS}


def _patch_odd(kit: Any) -> dict[str, Any]:
    # Every new name may be refused, as the kit's own odd names may; a wrong answer is still a violation.
    return {"_ODD_FIELDS": (*kit._ODD_FIELDS, *ODD_FIELDS), "_FIELDS": (*kit._FIELDS, *ODD_FIELDS)}


STORE_VARIANTS: dict[str, str] = {
    "default": "the kit unchanged: corpora of up to 20 documents, four filters each, nested two levels deep",
    "large-corpus": "corpora of up to --large-documents documents (150 by default), six filters each",
    "deep-filters": "And and Or nested three to six levels deep, one to four clauses each",
    "wide-or": "In over 100 and 1,000 values and Or over 100 and 1,000 one-value clauses, half on allowed_groups",
    "long-strings": "values, users and groups of 256, 1,024 and 8,192 characters that differ only in the last one",
    "huge-strings": "values of 32,766 and 40,000 characters, and of 40,001 bytes in UTF-8",
    "unicode-case": "values, users and groups equal only under case folding, NFC or NFKC, trimming or "
    "zero-width removal",
    "numeric-strings": "numeric-looking strings and integers at the 32-, 53- and 64-bit edges",
    "odd-fields": "field names with dots, quotes, slashes, spaces, $, case variants, non-ASCII letters (composed "
    "and decomposed) and the stores' own field names",
}
STORE_PATCHES: dict[str, Callable[[Any], dict[str, Any]]] = {
    "deep-filters": _patch_deep,
    "wide-or": _patch_wide,
    "long-strings": _patch_long,
    "huge-strings": _patch_huge,
    "unicode-case": _patch_unicode,
    "numeric-strings": _patch_numeric,
    "odd-fields": _patch_odd,
}
ENGINE_VARIANTS: dict[str, str] = {
    "default": "the kit unchanged: the 12 subjects and 30 chunks check_authorizer draws from the seed",
    "many-groups": "3 subjects in 1,000 more groups each, 10 chunks, some shared with one of those groups",
    "many-hits": "4 subjects, 300 chunks: past every batch size",
    "unicode-case": "user and group names equal only under case folding or Unicode normalisation",
    "numeric-strings": "numeric-looking user and group names",
    "long-ids": "user and group names of 64 to 4,096 characters, document ids of up to 1,100 more",
    "scalar-fields": "permission fields holding one string, an integer, mixed lists, nested lists, null, true or "
    "an object, in place of a list of strings; the tenant as a list or missing",
}
ENGINE_SIZES = {
    "default": (12, 30),
    "many-groups": (3, 10),
    "many-hits": (4, 300),
    "unicode-case": (8, 30),
    "numeric-strings": (8, 30),
    "long-ids": (8, 30),
    "scalar-fields": (8, 30),
}
ENGINE_POOLS: dict[str, dict[str, Any]] = {
    "unicode-case": {"_USERS": UNICODE_USERS, "_GROUPS": UNICODE_GROUPS},
    "numeric-strings": {"_USERS": NUMERIC_USERS, "_GROUPS": NUMERIC_GROUPS},
    "long-ids": {"_USERS": ("alice", "bob", *LONG_USERS), "_GROUPS": ("eng", "hr", *LONG_GROUPS)},
}
VARIANT_ORDER = [*STORE_VARIANTS, *(v for v in ENGINE_VARIANTS if v not in STORE_VARIANTS)]


def _variant_index(variant: str) -> int:
    return VARIANT_ORDER.index(variant) if variant in VARIANT_ORDER else len(VARIANT_ORDER)


@contextlib.contextmanager
def patched(module: Any, values: Mapping[str, Any]) -> Iterator[None]:
    """Replace module globals for the duration of the block, and put the originals back."""
    saved = {name: getattr(module, name) for name in values}
    try:
        for name, value in values.items():
            setattr(module, name, value)
        yield
    finally:
        for name, value in saved.items():
            setattr(module, name, value)


# ---- the engines' data ---------------------------------------------------------------------------


def _odd_value(rng: random.Random, pool: Sequence[str]) -> Any:
    kind = rng.randrange(8)
    if kind == 0:
        return rng.sample(pool, rng.randint(0, 2))  # a list of strings, as the documentation asks
    if kind == 1:
        return rng.choice(pool)  # one string
    if kind == 2:
        return 1
    if kind == 3:
        return [rng.choice(pool), 1]
    if kind == 4:
        return [[rng.choice(pool)]]
    if kind == 5:
        return None
    if kind == 6:
        return True
    return {"id": rng.choice(pool)}


def _odd_acl(rng: random.Random, kit: Any) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    if rng.random() < 0.8:
        metadata["allowed_users"] = _odd_value(rng, kit._USERS)
    if rng.random() < 0.8:
        metadata["allowed_groups"] = _odd_value(rng, (*kit._GROUPS, "*"))
    return metadata


def _with_decoy_group(rng: random.Random, metadata: Mapping[str, Any]) -> dict[str, Any]:
    groups = metadata.get("allowed_groups")
    if isinstance(groups, list) and rng.random() < 0.5:
        return {**metadata, "allowed_groups": [*groups, rng.choice(DECOY_GROUPS)]}
    return dict(metadata)


def _with_tenant(rng: random.Random, metadata: Mapping[str, Any], *, odd: bool) -> dict[str, Any]:
    value: Any = rng.choice(TENANTS)
    if odd:
        shape = rng.random()
        if shape < 0.15:
            value = [value]
        elif shape < 0.25:
            return dict(metadata)  # no tenant at all
        elif shape < 0.3:
            value = 1
    return {**metadata, "tenant": value}


def _long_id(rng: random.Random, doc_id: str) -> str:
    length = rng.choice((0, 0, 238, 260, 1100))
    return f"{doc_id}-{'d' * length}" if length else doc_id


def engine_dataset(kit: Any, seed: int, variant: str, *, tenant: bool) -> tuple[list[Any], list[Any]]:
    """The subjects and chunks of one engine run. Each chunk's `doc_id` is its own id."""
    from wardowl import Document, Hit, Subject

    subjects_count, hits_count = ENGINE_SIZES[variant]
    # The default variant draws exactly what check_authorizer(authorizer, seed=seed) draws itself.
    rng = random.Random(seed) if variant == "default" else random.Random(f"{variant}:{seed}")  # noqa: S311
    with patched(kit, ENGINE_POOLS.get(variant, {})):
        subjects = [kit._subject(rng) for _ in range(subjects_count)]
        documents = kit._acl_documents(rng, hits_count)
    if variant == "many-groups":
        subjects = [Subject(s.id, [*s.groups, *DECOY_GROUPS]) for s in subjects]
        documents = [Document(d.id, d.text, _with_decoy_group(rng, d.metadata)) for d in documents]
    elif variant == "scalar-fields":
        documents = [Document(d.id, d.text, _odd_acl(rng, kit)) for d in documents]
    elif variant == "long-ids":
        documents = [Document(_long_id(rng, d.id), d.text, d.metadata) for d in documents]
    hits = [Hit(d.id, d.text, 1.0, {**d.metadata, "doc_id": d.id}) for d in documents]
    if tenant:
        place = random.Random(f"tenant:{variant}:{seed}")  # noqa: S311
        subjects = [Subject(s.id, s.groups, {"tenant": place.choice(TENANTS)}) for s in subjects]
        odd = variant == "scalar-fields"
        hits = [Hit(h.id, h.text, h.score, _with_tenant(place, h.metadata, odd=odd)) for h in hits]
    return subjects, hits


def _strings(value: Any) -> list[str]:
    """The strings a permission field names: its string elements, or the string itself."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set, frozenset)):
        return [v for v in value if isinstance(v, str)]
    return []


def _unique(items: Sequence[Any]) -> list[Any]:
    found: dict[str, Any] = {}
    for item in items:
        found.setdefault(json.dumps(item, sort_keys=True), item)
    return list(found.values())


# ---- small tools ---------------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _env(name: str, default: str) -> str:
    return os.environ.get(name) or default


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else f"{text[:limit]}...(+{len(text) - limit} characters)"


def _scrub(text: str) -> str:
    """`text` without the value of any environment variable whose name ends in KEY, TOKEN, SECRET or PASSWORD."""
    for name, value in os.environ.items():
        if re.search(r"(KEY|TOKEN|SECRET|PASSWORD)$", name.upper()) and len(value) >= 6:
            text = text.replace(value, "***")
    return text


def _clip(value: Any) -> Any:
    """`value` with long strings and lists shortened, for a record a person reads."""
    if isinstance(value, str):
        return _truncate(value, STRING_LIMIT)
    if isinstance(value, Mapping):
        return {_truncate(str(k), STRING_LIMIT): _clip(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        items = sorted(value, key=repr) if isinstance(value, (set, frozenset)) else list(value)
        clipped = [_clip(v) for v in items[:LIST_LIMIT]]
        if len(items) > LIST_LIMIT:
            clipped.append(f"...(+{len(items) - LIST_LIMIT} more)")
        return clipped
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return repr(value)


def _literal(text: str) -> Any:
    for parse in (json.loads, ast.literal_eval):
        with contextlib.suppress(Exception):
            return parse(text)
    return text


def _find(data: Any, key: str) -> Any:
    """The first value stored under `key` anywhere in nested JSON."""
    if isinstance(data, Mapping):
        if key in data and not isinstance(data[key], (Mapping, list)):
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


def _versions(*names: str) -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for name in names:
        try:
            found[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            found[name] = None
    return found


def _command(*command: str) -> str | None:
    """A command's output, or None when it cannot run or fails (docker and opa, for their versions)."""
    try:
        done = subprocess.run(list(command), capture_output=True, text=True, timeout=30, check=False)  # noqa: S603
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def _image(container: str) -> dict[str, Any] | None:
    """The image a container runs, with its id and registry digests."""
    found = _command("docker", "inspect", "--format", "{{.Config.Image}}|{{.Image}}", container)
    if not found or "|" not in found:
        return None
    image, image_id = found.split("|", 1)
    digests = _command("docker", "image", "inspect", "--format", "{{json .RepoDigests}}", image_id)
    return {
        "container": container,
        "image": image,
        "image_id": image_id,
        "digests": _literal(digests) if digests else None,
    }


class ServiceError(Exception):
    """An HTTP call to a server's admin API failed; `status` is None when no answer came."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status

    @property
    def refused(self) -> bool:
        return self.status is not None and 400 <= self.status < 500


def _call(
    method: str,
    url: str,
    payload: Any = None,
    *,
    text: str | None = None,
    token: str | None = None,
    timeout: float = 30.0,
) -> Any:
    """An admin API call (writing tuples, policies and data): the JSON answer, {} for none."""
    data = None
    headers = {}
    if text is not None:
        data, headers["Content-Type"] = text.encode(), "text/plain"
    elif payload is not None:
        data, headers["Content-Type"] = json.dumps(payload).encode(), "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)  # noqa: S310
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            body = response.read()
    except urllib.error.HTTPError as error:
        detail = error.read()[:300].decode("utf-8", "replace")
        raise ServiceError(f"{method} {url}: HTTP {error.code}: {detail}", error.code) from None
    except (urllib.error.URLError, OSError) as error:
        raise ServiceError(f"{method} {url}: {error}") from None
    if not body.strip():
        return {}
    try:
        return json.loads(body)
    except ValueError:
        return body.decode("utf-8", "replace")


def _write_batched(send: Callable[[list[Any]], Any], items: Sequence[Any], size: int) -> dict[str, int]:
    """Write `items` in batches. A batch the server refuses (HTTP 4xx) is written again one item at a
    time, and the items it still refuses are counted, not written: an engine that cannot hold an id
    simply does not grant it."""
    written = refused = 0
    for start in range(0, len(items), size):
        batch = list(items[start : start + size])
        try:
            send(batch)
            written += len(batch)
        except ServiceError as error:
            if not error.refused:
                raise
            for item in batch:
                try:
                    send([item])
                    written += 1
                except ServiceError as single:
                    if not single.refused:
                        raise
                    refused += 1
    return {"written": written, "refused": refused}


class CallTimeout(BaseException):
    """A call ran past its time limit. A BaseException, so code that catches Exception cannot swallow it."""


@contextlib.contextmanager
def time_limit(seconds: float) -> Iterator[None]:
    """Raise CallTimeout in the block after `seconds` (on Linux and macOS; no limit elsewhere)."""
    if seconds <= 0 or not hasattr(signal, "setitimer"):
        yield
        return

    def expire(signum: int, frame: Any) -> None:
        raise CallTimeout(f"no answer within {seconds:.0f} s")

    previous = signal.signal(signal.SIGALRM, expire)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


class TargetSkipped(Exception):
    """The target cannot run here, for a reason that is not a failure (a missing secret)."""


def _embedder() -> Any:
    from wardowl.testing import HashingEmbedder

    return HashingEmbedder(DIM)


# ---- vector stores -------------------------------------------------------------------------------


class Store:
    """A vector store: `make(documents)` returns a backend holding exactly those documents."""

    family = "store"
    exact = True  # checked exactly, as CI checks it; False for an index that is approximate even on small corpora
    tenant = False
    container: str | None = None  # the Docker container, for its image and digest
    clients: tuple[str, ...] = ()  # the Python packages that talk to it, for their versions
    notes = ""

    def setup(self) -> None:
        """Connect; raises when the store cannot be reached."""

    def make(self, documents: Sequence[Any]) -> Any:
        raise NotImplementedError

    def reset(self) -> None:
        """Called after a run that did not pass, so the next run starts clean."""

    def close(self) -> None:
        """Remove what the target made and disconnect. Safe to call more than once."""

    def reported(self) -> dict[str, Any]:
        """The version the store reports about itself, where it reports one."""
        return {}


class Memory(Store):
    notes = "InMemoryBackend, the reference semantics: the positive control"

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl import InMemoryBackend

        return InMemoryBackend(documents)


class PgVector(Store):
    container = "postgres"
    clients = ("psycopg", "psycopg-pool")
    notes = "exact search (no HNSW index, iterative_scan=None), one table truncated for every corpus, as CI"

    def __init__(self) -> None:
        self.pool: Any = None
        self.backend: Any = None

    def setup(self) -> None:
        import psycopg_pool

        from wardowl.backends.pgvector import PgVectorBackend, create_schema

        url = _env("WARDOWL_TEST_DATABASE_URL", "postgresql://test:test@localhost:5432/test")
        self.pool = psycopg_pool.ConnectionPool(url, min_size=1, max_size=4, open=True, timeout=30)
        create_schema(self.pool, DIM, table="wo_campaign", hnsw=False)
        self.backend = PgVectorBackend(self.pool, _embedder(), table="wo_campaign", iterative_scan=None)

    def make(self, documents: Sequence[Any]) -> Any:
        with self.pool.connection() as conn:
            conn.execute("TRUNCATE wo_campaign")
        self.backend.add(documents)
        return self.backend

    def close(self) -> None:
        if self.pool is not None:
            with contextlib.suppress(Exception), self.pool.connection() as conn:
                conn.execute("DROP TABLE IF EXISTS wo_campaign")
            self.pool.close()
            self.pool = None

    def reported(self) -> dict[str, Any]:
        with self.pool.connection() as conn:
            server = conn.execute("SELECT version()").fetchone()
            vector = conn.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'").fetchone()
        return {"postgresql": server[0] if server else None, "pgvector": vector[0] if vector else None}


class Redis(Store):
    container = "redis"
    clients = ("redis",)
    notes = "a FLAT (exact) index and prefix for every corpus, as CI checks exactly"

    def __init__(self) -> None:
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import redis

        self.client = redis.Redis.from_url(_env("WARDOWL_TEST_REDIS_URL", "redis://127.0.0.1:6379/0"))
        self.client.ping()

    def _drop(self) -> None:
        for name in self.made:
            with contextlib.suppress(Exception):
                self.client.execute_command("FT.DROPINDEX", name, "DD")  # DD deletes the hashes too
        self.made = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.redis import RedisBackend, create_index

        self._drop()
        name = f"wo_{uuid.uuid4().hex}"
        self.made = [name]
        create_index(self.client, name, DIM, prefix=f"{name}:", algorithm="FLAT")
        backend = RedisBackend(self.client, name, _embedder(), prefix=f"{name}:")
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.client is not None:
            self._drop()
            self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        info = self.client.info("server")
        modules: dict[str, Any] = {}
        with contextlib.suppress(Exception):
            for entry in self.client.execute_command("MODULE", "LIST"):
                fields = {_text(k): v for k, v in zip(entry[::2], entry[1::2], strict=False)}
                modules[_text(fields.get("name"))] = _text(fields.get("ver"))
        return {"redis": info.get("redis_version"), "modules": modules}


def _text(value: Any) -> Any:
    return value.decode("utf-8", "replace") if isinstance(value, bytes) else value


class Cassandra(Store):
    container = "cassandra"
    clients = ("cassandra-driver",)
    exact = False
    notes = "sound-only (exact=False), as CI checks it: the jvector index is approximate; a table per corpus"
    keyspace = "wardowl_campaign"

    def __init__(self) -> None:
        self.cluster: Any = None
        self.session: Any = None
        self.tables: list[str] = []

    def setup(self) -> None:
        from cassandra.cluster import Cluster

        self.cluster = Cluster([_env("WARDOWL_TEST_CASSANDRA_HOST", "127.0.0.1")])
        self.session = self.cluster.connect()
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS wardowl_campaign "
            "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
        )

    def _drop(self) -> None:
        for table in self.tables:
            with contextlib.suppress(Exception):
                self.session.execute(f"DROP TABLE IF EXISTS {self.keyspace}.{table}")
        self.tables = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.cassandra import CassandraBackend, create_table

        self._drop()
        table = f"chunks_{uuid.uuid4().hex[:12]}"
        self.tables = [table]
        create_table(self.session, self.keyspace, table, DIM)
        backend = CassandraBackend(self.session, self.keyspace, table, _embedder())
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.session is not None:
            self._drop()
        if self.cluster is not None:
            self.cluster.shutdown()
            self.cluster = self.session = None

    def reported(self) -> dict[str, Any]:
        row = self.session.execute("SELECT release_version FROM system.local").one()
        return {"cassandra": row.release_version if row else None}


class SearchEngine(Store):
    """Elasticsearch or OpenSearch: an index for every corpus, as CI."""

    def __init__(self, kind: str) -> None:
        self.kind = kind
        self.container = kind
        self.clients = ("elasticsearch",) if kind == "elasticsearch" else ("opensearch-py",)
        default = "http://127.0.0.1:9200" if kind == "elasticsearch" else "http://127.0.0.1:9201"
        self.url = _env(f"WARDOWL_TEST_{kind.upper()}_URL", default)
        self.client: Any = None
        self.indexes: list[str] = []
        self.notes = "an index for every corpus, as CI"

    def setup(self) -> None:
        if self.kind == "elasticsearch":
            import elasticsearch

            self.client = elasticsearch.Elasticsearch(self.url)
        else:
            import opensearchpy

            self.client = opensearchpy.OpenSearch(hosts=[self.url])
        self.client.info()

    def _drop(self) -> None:
        for name in self.indexes:
            with contextlib.suppress(Exception):
                self.client.indices.delete(index=name)
        self.indexes = []

    def make(self, documents: Sequence[Any]) -> Any:
        module = importlib.import_module(f"wardowl.backends.{self.kind}")
        kind = module.ElasticsearchBackend if self.kind == "elasticsearch" else module.OpenSearchBackend
        self._drop()
        name = f"wo-{uuid.uuid4().hex}"
        self.indexes = [name]
        module.create_index(self.client, name, DIM)
        backend = kind(self.client, name, _embedder())
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.client is not None:
            self._drop()
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        answer = _call("GET", f"{self.url}/")
        version = answer.get("version", {}) if isinstance(answer, dict) else {}
        keep = ("number", "distribution", "lucene_version", "build_hash")
        return {key: version.get(key) for key in keep if key in version}


class Vespa(Store):
    container = "vespa"
    clients = ("httpx",)
    notes = "the application in examples/vespa, exact search (approximate=False), as CI checks exactly"

    def __init__(self) -> None:
        self.url = _env("WARDOWL_TEST_VESPA_URL", "http://127.0.0.1:8090")
        self.client: Any = None
        self.stored: set[str] = set()
        self.ever: set[str] = set()
        self.dirty = False

    def setup(self) -> None:
        import httpx

        self.client = httpx.Client(timeout=30)
        if self.client.get(f"{self.url}/").status_code >= 500:
            raise RuntimeError("Vespa's container answers with a server error")

    def _backend(self) -> Any:
        from wardowl.backends.vespa import VespaBackend

        return VespaBackend(self.url, _embedder(), approximate=False, client=self.client)

    def make(self, documents: Sequence[Any]) -> Any:
        backend = self._backend()
        # Every id the last corpus wrote, or every id ever written after a failure, and the id
        # the kit's set_metadata must not create: one Vespa holds every corpus in turn.
        backend.delete(sorted({*(self.ever if self.dirty else self.stored), "not-stored"}))
        self.dirty = False
        self.stored = {d.id for d in documents}
        self.ever |= self.stored
        backend.add(documents)
        return backend

    def reset(self) -> None:
        self.dirty = True

    def close(self) -> None:
        if self.client is not None:
            with contextlib.suppress(Exception):
                self._backend().delete(sorted({*self.ever, "not-stored"}))
            self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        for path in ("/state/v1/version", "/ApplicationStatus"):
            with contextlib.suppress(ServiceError):
                version = _find(_call("GET", f"{self.url}{path}"), "version")
                if version:
                    return {"vespa": version}
        return {}


class Qdrant(Store):
    container = "qdrant"
    clients = ("qdrant-client",)
    notes = "the server, a collection for every corpus, as CI"

    def __init__(self) -> None:
        self.url = _env("WARDOWL_TEST_QDRANT_URL", "http://127.0.0.1:6333")
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import qdrant_client

        self.client = qdrant_client.QdrantClient(url=self.url)
        self.client.get_collections()

    def _drop(self) -> None:
        for name in self.made:
            with contextlib.suppress(Exception):
                self.client.delete_collection(name)
        self.made = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.qdrant import QdrantBackend, create_collection

        self._drop()
        name = f"wo_{uuid.uuid4().hex}"
        self.made = [name]
        create_collection(self.client, name, DIM)
        backend = QdrantBackend(self.client, name, _embedder())
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.client is not None:
            self._drop()
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        answer = _call("GET", f"{self.url}/")
        return {"qdrant": answer.get("version") if isinstance(answer, dict) else None}


class Milvus(Store):
    container = "milvus"
    clients = ("pymilvus",)
    notes = "standalone, a collection for every corpus, as CI"

    def __init__(self) -> None:
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import pymilvus

        self.client = pymilvus.MilvusClient(uri=_env("WARDOWL_TEST_MILVUS_URL", "http://127.0.0.1:19530"))
        self.client.list_collections()

    def _drop(self) -> None:
        for name in self.made:
            with contextlib.suppress(Exception):
                self.client.drop_collection(name)
        self.made = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.milvus import MilvusBackend, create_collection

        self._drop()
        name = f"wo_{uuid.uuid4().hex}"
        self.made = [name]
        create_collection(self.client, name, DIM)
        backend = MilvusBackend(self.client, name, _embedder())
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.client is not None:
            self._drop()
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        return {"milvus": self.client.get_server_version()}


class Weaviate(Store):
    container = "weaviate"
    clients = ("weaviate-client",)
    notes = "vectors from the client, a collection for every corpus, as CI"

    def __init__(self) -> None:
        self.url = _env("WARDOWL_TEST_WEAVIATE_URL", "http://127.0.0.1:8079")
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import weaviate

        parts = urllib.parse.urlsplit(self.url)
        grpc_port = int(_env("WARDOWL_TEST_WEAVIATE_GRPC_PORT", "50051"))
        self.client = weaviate.connect_to_local(host=parts.hostname, port=parts.port, grpc_port=grpc_port)

    def _drop(self) -> None:
        for name in self.made:
            with contextlib.suppress(Exception):
                self.client.collections.delete(name)
        self.made = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.weaviate import WeaviateBackend, create_collection

        self._drop()
        name = f"Wo{uuid.uuid4().hex}"  # collection names start with an upper-case letter
        self.made = [name]
        create_collection(self.client, name)
        backend = WeaviateBackend(self.client, name, _embedder())
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.client is not None:
            self._drop()
            with contextlib.suppress(Exception):
                self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        answer = _call("GET", f"{self.url}/v1/meta")
        return {"weaviate": answer.get("version") if isinstance(answer, dict) else None}


class MongoDB(Store):
    container = "mongodb"
    clients = ("pymongo",)
    notes = "a local Atlas deployment, one collection and vector index for every corpus in turn, as CI"

    def __init__(self) -> None:
        self.client: Any = None
        self.collection: Any = None
        self.backend: Any = None
        self.previous: list[str] = []
        self.ever: set[str] = set()
        self.dirty = False

    def setup(self) -> None:
        import pymongo

        from wardowl.backends.mongodb import MongoDBBackend, create_search_index

        url = _env("WARDOWL_TEST_MONGODB_URL", "mongodb://127.0.0.1:27017/?directConnection=true")
        self.client = pymongo.MongoClient(url, serverSelectionTimeoutMS=10_000)
        self.client.admin.command("ping")
        self.collection = self.client["wardowl_campaign"][f"c_{uuid.uuid4().hex}"]
        create_search_index(self.collection, DIM)
        self.backend = MongoDBBackend(self.collection, _embedder())

    def make(self, documents: Sequence[Any]) -> Any:
        # Every id the last corpus wrote, or every id ever written after a failure, and the id the
        # kit's set_metadata must not create; then wait for the new corpus, as CI's factory does.
        self.backend.delete(sorted({*(self.ever if self.dirty else self.previous), "not-stored"}))
        self.dirty = False
        self.previous = [d.id for d in documents]
        self.ever.update(self.previous)
        self.backend.add(documents)
        return self.backend

    def reset(self) -> None:
        self.dirty = True

    def close(self) -> None:
        if self.collection is not None:
            with contextlib.suppress(Exception):
                self.collection.drop()
            self.collection = None
        if self.client is not None:
            self.client.close()
            self.client = None

    def reported(self) -> dict[str, Any]:
        return {"mongodb": self.client.server_info().get("version")}


class Chroma(Store):
    clients = ("chromadb",)
    notes = "embedded (EphemeralClient), a collection for every corpus, as CI"

    def __init__(self) -> None:
        self.client: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import chromadb

        self.client = chromadb.EphemeralClient()

    def _drop(self) -> None:
        for name in self.made:
            with contextlib.suppress(Exception):
                self.client.delete_collection(name)
        self.made = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.chroma import ChromaBackend

        self._drop()
        name = f"wo_{uuid.uuid4().hex}"
        self.made = [name]
        collection = self.client.create_collection(name, embedding_function=None)
        backend = ChromaBackend(collection, _embedder())
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.client is not None:
            self._drop()
            self.client = None


class LanceDB(Store):
    clients = ("lancedb", "pylance", "pyarrow")
    notes = "embedded, in a temporary directory, a table for every corpus, as CI"

    def __init__(self) -> None:
        self.directory = ""
        self.db: Any = None
        self.made: list[str] = []

    def setup(self) -> None:
        import lancedb

        self.directory = tempfile.mkdtemp(prefix="wo-lancedb-", dir=os.environ.get("RUNNER_TEMP") or None)
        self.db = lancedb.connect(self.directory)

    def _drop(self) -> None:
        for name in self.made:
            with contextlib.suppress(Exception):
                self.db.drop_table(name)
        self.made = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.lancedb import LanceDBBackend, create_table

        self._drop()
        name = f"wo_{uuid.uuid4().hex}"
        self.made = [name]
        backend = LanceDBBackend(create_table(self.db, name, DIM), _embedder())
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.db is not None:
            self._drop()
            self.db = None
        if self.directory:
            shutil.rmtree(self.directory, ignore_errors=True)
            self.directory = ""


class Faiss(Store):
    clients = ("faiss-cpu", "numpy")
    notes = "in process, a new flat index for every corpus, as CI"

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.faiss import FaissBackend

        backend = FaissBackend(_embedder(), DIM)
        backend.add(documents)
        return backend


class Pinecone(Store):
    clients = ("httpx",)
    notes = "the service: CI's index wardowl-ci, a namespace for every corpus, writes waited for up to 60 s"
    index_name = "wardowl-ci"
    api_version = "2026-07"

    def __init__(self) -> None:
        self.key = os.environ.get("WARDOWL_TEST_PINECONE_API_KEY", "")
        self.host = ""
        self.spaces: list[str] = []
        self.described: dict[str, Any] = {}

    def setup(self) -> None:
        if not self.key:
            raise TargetSkipped("the PINECONE_API_KEY secret is not set")
        import httpx

        headers = {"Api-Key": self.key, "X-Pinecone-Api-Version": self.api_version}
        index: dict[str, Any] = {}
        with httpx.Client(base_url="https://api.pinecone.io", headers=headers, timeout=30) as api:
            if api.get(f"/indexes/{self.index_name}").status_code == 404:  # created as CI creates it
                spec = {"_values": {"type": "dense_vector", "dimension": DIM, "metric": "cosine"}}
                deployment = {"deployment_type": "managed", "cloud": "aws", "region": "us-east-1"}
                body = {"name": self.index_name, "deployment": deployment, "schema": {"fields": spec}}
                api.post("/indexes", json=body).raise_for_status()
            for _ in range(60):
                index = api.get(f"/indexes/{self.index_name}").json()
                if index.get("status", {}).get("ready"):
                    break
                time.sleep(3)
        self.host = index["host"]
        self.described = {key: index.get(key) for key in ("status", "deployment", "schema") if key in index}

    def _clear(self) -> None:
        from wardowl.backends.pinecone import PineconeBackend

        for space in self.spaces:
            with contextlib.suppress(Exception):
                PineconeBackend(self.host, self.key, _embedder(), namespace=space).clear()
        self.spaces = []

    def make(self, documents: Sequence[Any]) -> Any:
        from wardowl.backends.pinecone import PineconeBackend

        self._clear()
        space = f"wo-campaign-{uuid.uuid4().hex[:12]}"
        self.spaces = [space]
        backend = PineconeBackend(self.host, self.key, _embedder(), namespace=space, wait=60.0)
        backend.add(documents)
        return backend

    def close(self) -> None:
        if self.host:
            self._clear()

    def reported(self) -> dict[str, Any]:
        return {"api_version": self.api_version, "index": self.index_name, **self.described}


# ---- authorization engines -----------------------------------------------------------------------

# The metadata ACL model of wardowl's own tests, written natively in each engine.
OPENFGA_ACL_MODEL = {
    "schema_version": "1.1",
    "type_definitions": [
        {"type": "user"},
        {
            "type": "group",
            "relations": {"member": {"this": {}}},
            "metadata": {"relations": {"member": {"directly_related_user_types": [{"type": "user"}]}}},
        },
        {
            "type": "document",
            "relations": {"viewer": {"this": {}}},
            "metadata": {
                "relations": {
                    "viewer": {
                        "directly_related_user_types": [
                            {"type": "user"},
                            {"type": "user", "wildcard": {}},
                            {"type": "group", "relation": "member"},
                        ]
                    }
                }
            },
        },
    ],
}
SPICEDB_ACL_SCHEMA = """
definition PREFIX/user {}

definition PREFIX/group {
    relation member: PREFIX/user
}

definition PREFIX/document {
    relation viewer: PREFIX/user | PREFIX/user:* | PREFIX/group#member
    permission view = viewer
}
"""
CEDAR_ACL = """
permit (principal, action == Action::"read", resource)
when { resource has allowed_users && resource.allowed_users.contains(principal.id) };

permit (principal, action == Action::"read", resource)
when {
  resource has allowed_groups &&
  (resource.allowed_groups.contains("*") || resource.allowed_groups.containsAny(principal.groups))
};
"""
CASBIN_ACL_MODEL = """
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = (g(r.sub, p.sub) || p.sub == "*") && r.obj == p.obj && r.act == p.act
"""


class Engine:
    """An authorization engine with a policy: `prepare(subjects, hits)` writes what the engine needs to
    know about them (tuples, data) and returns the authorizer to check."""

    family = "engine"
    exact = None
    tenant = False
    container: str | None = None
    clients: tuple[str, ...] = ()
    notes = ""

    def __init__(self) -> None:
        self.case: dict[str, Any] = {}  # what prepare wrote, for the record

    def setup(self) -> None:
        """Connect and load the policy; raises when the engine cannot be reached."""

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        raise NotImplementedError

    def finish(self) -> None:
        """Called after every run, whatever happened."""

    def close(self) -> None:
        """Remove what the target made. Safe to call more than once."""

    def reported(self) -> dict[str, Any]:
        return {}

    def reference(self, subject: Any, metadata: Mapping[str, Any]) -> bool:
        """The reference answer for the target's rule, by `wardowl.filters.matches`, to tell which side
        of a filter-and-check disagreement gives it: the metadata ACL rule (a listed user, a shared
        group, or "*" for everyone), and for the tenant profiles the acceptance rule (the subject's
        tenant, and a listed user or a shared group, without "*")."""
        from wardowl.filters import And, In, Or, matches

        groups = sorted(subject.groups)
        if not self.tenant:
            return matches(Or(In("allowed_users", [subject.id]), In("allowed_groups", [*groups, "*"])), metadata)
        tenant = subject.attributes.get("tenant")
        if not isinstance(tenant, str):
            return False
        shared = Or(In("allowed_users", [subject.id]), In("allowed_groups", groups))
        return matches(And(In("tenant", [tenant]), shared), metadata)


class MetadataACL(Engine):
    notes = "MetadataACLAuthorizer, in process: the positive control"

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        from wardowl import MetadataACLAuthorizer

        return MetadataACLAuthorizer()


class OPA(Engine):
    def __init__(self, *, tenant: bool) -> None:
        super().__init__()
        self.tenant = tenant
        self.url = _env("WARDOWL_TEST_OPA_URL", "http://127.0.0.1:8181")
        tag = re.sub(r"[^a-z0-9]", "", f"{RUN_ID}{uuid.uuid4().hex[:8]}".lower())
        self.package = f"campaign_{tag}"
        self.notes = (
            "acceptance/policies/opa/documents.rego, uploaded under a package of the run's own, with the "
            "sharing of every chunk pushed as OPA data; its filter_path returns an In on doc_id"
            if tenant
            else "examples/opa/wardowl.rego, loaded at startup as CI loads it, with filter_path wardowl/filter"
        )

    def setup(self) -> None:
        _call("GET", f"{self.url}/health")
        if self.tenant:
            rego = (POLICIES / "opa" / "documents.rego").read_text(encoding="utf-8")
            _call("PUT", f"{self.url}/v1/policies/{self.package}", text=rego.replace("acme_s02", self.package))

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        from wardowl.authorizers.opa import OPAAuthorizer

        if not self.tenant:
            return OPAAuthorizer(self.url, filter_path="wardowl/filter")
        sharing = {}
        for hit in hits:
            doc = hit.metadata.get("doc_id")
            if isinstance(doc, str):
                sharing[doc] = {
                    "tenant": hit.metadata.get("tenant"),
                    "users": _strings(hit.metadata.get("allowed_users")),
                    "groups": _strings(hit.metadata.get("allowed_groups")),
                }
        _call("PUT", f"{self.url}/v1/data/{self.package}_data/sharing", sharing)
        self.case = {"documents_shared": len(sharing)}
        return OPAAuthorizer(
            self.url,
            decisions_path=f"{self.package}/documents/decisions",
            filter_path=f"{self.package}/documents/filter",
        )

    def close(self) -> None:
        if self.tenant:
            with contextlib.suppress(ServiceError):
                _call("DELETE", f"{self.url}/v1/policies/{self.package}")
            with contextlib.suppress(ServiceError):
                _call("DELETE", f"{self.url}/v1/data/{self.package}_data")

    def reported(self) -> dict[str, Any]:
        found: dict[str, Any] = {}
        cli = _command("opa", "version")
        if cli:
            found["opa"] = cli.splitlines()[0]
        with contextlib.suppress(ServiceError):
            config = _call("GET", f"{self.url}/v1/config")
            found["server"] = _find(config, "version")
        return found


class OpenFGA(Engine):
    container = "openfga"

    def __init__(self, *, tenant: bool) -> None:
        super().__init__()
        self.tenant = tenant
        self.url = _env("WARDOWL_TEST_OPENFGA_URL", "http://127.0.0.1:8080")
        source = POLICIES / "openfga" / "model.json"
        self.model = json.loads(source.read_text(encoding="utf-8")) if tenant else OPENFGA_ACL_MODEL
        self.store = ""
        self.notes = (
            "acceptance/policies/openfga/model.json (a tenant intersection), a store per run, tuples for each "
            "subject's tenant and each chunk's tenant and readers; groups as contextual tuples; HIGHER_CONSISTENCY"
            if tenant
            else "the model of wardowl's tests (user, user:*, group#member viewers), a store per run, a tuple per "
            "grant in the chunks' ACLs; groups as contextual tuples; HIGHER_CONSISTENCY"
        )

    def setup(self) -> None:
        _call("GET", f"{self.url}/stores")

    def _tuples(self, subjects: Sequence[Any], hits: Sequence[Any]) -> list[dict[str, str]]:
        tuples: list[dict[str, str]] = []
        if self.tenant:
            for subject in subjects:
                place = subject.attributes.get("tenant")
                if isinstance(place, str):
                    tuples.append({"user": f"user:{subject.id}", "relation": "member", "object": f"tenant:{place}"})
        for hit in hits:
            doc = hit.metadata.get("doc_id")
            if not isinstance(doc, str):
                continue
            obj = f"document:{doc}"
            relation = "reader" if self.tenant else "viewer"
            place = hit.metadata.get("tenant")
            if self.tenant and isinstance(place, str):
                tuples.append({"user": f"tenant:{place}", "relation": "tenant", "object": obj})
            for user in _strings(hit.metadata.get("allowed_users")):
                tuples.append({"user": f"user:{user}", "relation": relation, "object": obj})
            for group in _strings(hit.metadata.get("allowed_groups")):
                who = "user:*" if group == "*" and not self.tenant else f"group:{group}#member"
                tuples.append({"user": who, "relation": relation, "object": obj})
        return _unique(tuples)

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        from wardowl.authorizers.openfga import OpenFGAAuthorizer

        self.store = _call("POST", f"{self.url}/stores", {"name": f"wo-campaign-{uuid.uuid4().hex[:12]}"})["id"]
        models = f"{self.url}/stores/{self.store}/authorization-models"
        model_id = _call("POST", models, self.model)["authorization_model_id"]

        def send(batch: list[Any]) -> Any:
            payload = {"writes": {"tuple_keys": batch}, "authorization_model_id": model_id}
            return _call("POST", f"{self.url}/stores/{self.store}/write", payload)

        self.case = {"tuples": _write_batched(send, self._tuples(subjects, hits), 100)}
        return OpenFGAAuthorizer(
            self.url, self.store, authorization_model_id=model_id, consistency="HIGHER_CONSISTENCY"
        )

    def finish(self) -> None:
        if self.store:
            with contextlib.suppress(ServiceError):
                _call("DELETE", f"{self.url}/stores/{self.store}")
            self.store = ""

    def close(self) -> None:
        self.finish()


class SpiceDB(Engine):
    container = "spicedb"

    def __init__(self, *, tenant: bool) -> None:
        super().__init__()
        self.tenant = tenant
        self.url = _env("WARDOWL_TEST_SPICEDB_URL", "http://127.0.0.1:8443")
        self.token = os.environ.get("WARDOWL_TEST_SPICEDB_TOKEN", "")
        self.prefix = "camptn" if tenant else "campacl"
        if tenant:
            schema = (POLICIES / "spicedb" / "schema.zed").read_text(encoding="utf-8")
            self.schema = schema.replace("acme/", f"{self.prefix}/")
        else:
            self.schema = SPICEDB_ACL_SCHEMA.replace("PREFIX/", f"{self.prefix}/")
        self.notes = (
            "acceptance/policies/spicedb/schema.zed (view = reader & tenant->member), memberships stored in "
            "SpiceDB, group_subjects=False, fully consistent"
            if tenant
            else "the schema of wardowl's tests (user, user:*, group#member viewers), groups checked as subject "
            "sets (group_subjects=True), fully consistent"
        )

    def _api(self, path: str, payload: Any) -> Any:
        return _call("POST", f"{self.url}{path}", payload, token=self.token)

    def setup(self) -> None:
        # WriteSchema replaces the whole schema, and SpiceDB refuses to drop a definition that still has
        # relationships: empty every definition on the server first (this job's SpiceDB is its own).
        try:
            answer = self._api("/v1/schema/read", {})
            current = answer.get("schemaText", "") if isinstance(answer, dict) else ""
        except ServiceError as error:
            if error.status is None:
                raise
            current = ""  # a new server holds no schema yet
        for name in re.findall(r"definition\s+([\w/]+)", current):
            with contextlib.suppress(ServiceError):
                self._api("/v1/relationships/delete", {"relationshipFilter": {"resourceType": name}})
        self._api("/v1/schema/write", {"schema": self.schema})

    def _rel(self, kind: str, obj: str, relation: str, who_kind: str, who: str, who_relation: str = "") -> Any:
        subject: dict[str, Any] = {"object": {"objectType": f"{self.prefix}/{who_kind}", "objectId": who}}
        if who_relation:
            subject["optionalRelation"] = who_relation
        resource = {"objectType": f"{self.prefix}/{kind}", "objectId": obj}
        return {"resource": resource, "relation": relation, "subject": subject}

    def _relationships(self, subjects: Sequence[Any], hits: Sequence[Any]) -> list[Any]:
        found = []
        if self.tenant:
            for subject in subjects:
                place = subject.attributes.get("tenant")
                if isinstance(place, str):
                    found.append(self._rel("tenant", place, "member", "user", subject.id))
                    found += [
                        self._rel("group", f"{place}/{group}", "member", "user", subject.id)
                        for group in sorted(subject.groups)
                    ]
        for hit in hits:
            doc = hit.metadata.get("doc_id")
            if not isinstance(doc, str):
                continue
            users = _strings(hit.metadata.get("allowed_users"))
            groups = _strings(hit.metadata.get("allowed_groups"))
            if self.tenant:
                place = hit.metadata.get("tenant")
                if not isinstance(place, str):
                    continue  # no tenant: the schema's intersection denies it whatever the grants
                found.append(self._rel("document", doc, "tenant", "tenant", place))
                found += [self._rel("document", doc, "reader", "user", user) for user in users]
                found += [
                    self._rel("document", doc, "reader", "group", f"{place}/{group}", "member") for group in groups
                ]
            else:
                found += [self._rel("document", doc, "viewer", "user", user) for user in users]
                found += [
                    self._rel("document", doc, "viewer", "user", "*")
                    if group == "*"
                    else self._rel("document", doc, "viewer", "group", group, "member")
                    for group in groups
                ]
        return _unique(found)

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        from wardowl.authorizers.spicedb import SpiceDBAuthorizer

        for kind in ("document", "group", "tenant") if self.tenant else ("document",):
            self._api("/v1/relationships/delete", {"relationshipFilter": {"resourceType": f"{self.prefix}/{kind}"}})

        def send(batch: list[Any]) -> Any:
            updates = [{"operation": "OPERATION_TOUCH", "relationship": r} for r in batch]
            return self._api("/v1/relationships/write", {"updates": updates})

        self.case = {"relationships": _write_batched(send, self._relationships(subjects, hits), 100)}
        return SpiceDBAuthorizer(
            self.url,
            self.token,
            resource_type=f"{self.prefix}/document",
            subject_type=f"{self.prefix}/user",
            group_type=f"{self.prefix}/group",
            group_subjects=not self.tenant,
            consistency={"fullyConsistent": True},
        )


class Cerbos(Engine):
    def __init__(self, *, tenant: bool) -> None:
        super().__init__()
        self.tenant = tenant
        if tenant:
            self.container = "cerbos-tenant"
            self.url = _env("WARDOWL_CAMPAIGN_CERBOS_TENANT_URL", "http://127.0.0.1:3593")
            self.notes = "acceptance/policies/cerbos/document.yaml (tenant equality and sharing), loaded at startup"
        else:
            self.container = "cerbos"
            self.url = _env("WARDOWL_TEST_CERBOS_URL", "http://127.0.0.1:3592")
            self.notes = "examples/cerbos/policies/document.yaml (metadata ACLs), loaded at startup as CI loads it"

    def setup(self) -> None:
        _call("GET", f"{self.url}/_cerbos/health")

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        from wardowl.authorizers.cerbos import CerbosAuthorizer

        return CerbosAuthorizer(self.url)

    def reported(self) -> dict[str, Any]:
        with contextlib.suppress(ServiceError):
            answer = _call("GET", f"{self.url}/api/server_info")
            if isinstance(answer, dict):
                return {key: answer.get(key) for key in ("version", "commit", "buildDate") if key in answer}
        return {}


class Keto(Engine):
    container = "keto"
    notes = (
        "acceptance/policies/keto (Document#view of users and Group#members), tuples replaced for every run, "
        "groups checked as subject sets (group_subjects=True), Keto's default batch limit of 10"
    )

    def __init__(self) -> None:
        super().__init__()
        self.read = _env("WARDOWL_TEST_KETO_URL", "http://127.0.0.1:4466")
        self.write = _env("WARDOWL_TEST_KETO_WRITE_URL", "http://127.0.0.1:4467")

    def setup(self) -> None:
        _call("GET", f"{self.read}/health/ready")
        _call("GET", f"{self.write}/health/ready")

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        from wardowl.authorizers.keto import KetoAuthorizer

        for namespace in ("Document", "Group"):
            query = urllib.parse.urlencode({"namespace": namespace})
            _call("DELETE", f"{self.write}/admin/relation-tuples?{query}")
        tuples = []
        for hit in hits:
            doc = hit.metadata.get("doc_id")
            if not isinstance(doc, str):
                continue
            view = {"namespace": "Document", "object": doc, "relation": "view"}
            tuples += [{**view, "subject_id": user} for user in _strings(hit.metadata.get("allowed_users"))]
            tuples += [
                {**view, "subject_set": {"namespace": "Group", "object": group, "relation": "members"}}
                for group in _strings(hit.metadata.get("allowed_groups"))
            ]

        def send(batch: list[Any]) -> Any:
            changes = [{"action": "insert", "relation_tuple": t} for t in batch]
            return _call("PATCH", f"{self.write}/admin/relation-tuples", changes)

        self.case = {"tuples": _write_batched(send, _unique(tuples), 100)}
        return KetoAuthorizer(self.read, group_subjects=True)

    def reported(self) -> dict[str, Any]:
        with contextlib.suppress(ServiceError):
            answer = _call("GET", f"{self.read}/version")
            if isinstance(answer, dict):
                return {"keto": answer.get("version")}
        return {}


class Cedar(Engine):
    clients = ("cedarpy",)

    def __init__(self, *, tenant: bool) -> None:
        super().__init__()
        self.tenant = tenant
        self.notes = (
            "acceptance/policies/cedar/documents.cedar (sharing, and a forbid across tenants), in process"
            if tenant
            else "the metadata ACL policy of wardowl's tests, in process"
        )

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        from wardowl.authorizers.cedar import CedarAuthorizer

        if self.tenant:
            return CedarAuthorizer((POLICIES / "cedar" / "documents.cedar").read_text(encoding="utf-8"))
        return CedarAuthorizer(CEDAR_ACL)


def _casbin_tenant_request(subject: Any, hit: Any, action: str) -> tuple[str, str, str, str]:
    """The request of the RBAC-with-domains model: (user, tenant, document id, action), as the
    acceptance scenario builds it."""
    from wardowl import AuthorizationError

    if subject.id.startswith("group:"):
        raise AuthorizationError(f"subject id {subject.id!r} could pass for a group")
    doc = hit.metadata.get("doc_id")
    place = subject.attributes.get("tenant")
    return (subject.id, place if isinstance(place, str) else "", doc if isinstance(doc, str) else "", action)


class Casbin(Engine):
    clients = ("casbin",)

    def __init__(self, *, tenant: bool) -> None:
        super().__init__()
        self.tenant = tenant
        self.notes = (
            "acceptance/policies/casbin/model.conf (RBAC with a domain per tenant), a policy row per grant and a "
            "grouping row per membership, in process"
            if tenant
            else "the RBAC model of wardowl's tests with '*' for everyone, a policy row per grant, groups from the "
            "subject (group_subjects=True), in process"
        )

    def prepare(self, subjects: Sequence[Any], hits: Sequence[Any]) -> Any:
        import casbin
        from casbin.model import Model

        from wardowl.authorizers.casbin import CasbinAuthorizer

        model = Model()
        if self.tenant:
            model.load_model(str(POLICIES / "casbin" / "model.conf"))
        else:
            model.load_model_from_text(CASBIN_ACL_MODEL)
        enforcer = casbin.Enforcer(model)
        rows: list[list[str]] = []
        memberships: list[list[str]] = []
        for hit in hits:
            doc = hit.metadata.get("doc_id")
            place = hit.metadata.get("tenant")
            if not isinstance(doc, str) or (self.tenant and not isinstance(place, str)):
                continue
            scope = [place] if self.tenant else []
            rows += [[user, *scope, doc, "read"] for user in _strings(hit.metadata.get("allowed_users"))]
            for group in _strings(hit.metadata.get("allowed_groups")):
                name = group if group == "*" and not self.tenant else f"group:{group}"
                rows.append([name, *scope, doc, "read"])
        if self.tenant:
            for subject in subjects:
                place = subject.attributes.get("tenant")
                if isinstance(place, str):
                    memberships += [[subject.id, f"group:{group}", place] for group in sorted(subject.groups)]
        rows, memberships = _unique(rows), _unique(memberships)
        if rows and not enforcer.add_policies(rows):
            raise RuntimeError("Casbin did not add the policy rows")
        if memberships and not enforcer.add_grouping_policies(memberships):
            raise RuntimeError("Casbin did not add the grouping rows")
        self.case = {"policies": len(rows), "groupings": len(memberships)}
        if self.tenant:
            return CasbinAuthorizer(enforcer, request=_casbin_tenant_request)
        return CasbinAuthorizer(enforcer, group_subjects=True)


TARGETS: dict[str, Callable[[], Store | Engine]] = {
    "memory": Memory,
    "pgvector": PgVector,
    "redis": Redis,
    "cassandra": Cassandra,
    "elasticsearch": lambda: SearchEngine("elasticsearch"),
    "opensearch": lambda: SearchEngine("opensearch"),
    "vespa": Vespa,
    "qdrant": Qdrant,
    "milvus": Milvus,
    "weaviate": Weaviate,
    "mongodb": MongoDB,
    "chroma": Chroma,
    "lancedb": LanceDB,
    "faiss": Faiss,
    "pinecone": Pinecone,
    "metadata-acl": MetadataACL,
    "opa": lambda: OPA(tenant=False),
    "opa-tenant": lambda: OPA(tenant=True),
    "openfga": lambda: OpenFGA(tenant=False),
    "openfga-tenant": lambda: OpenFGA(tenant=True),
    "spicedb": lambda: SpiceDB(tenant=False),
    "spicedb-tenant": lambda: SpiceDB(tenant=True),
    "cerbos": lambda: Cerbos(tenant=False),
    "cerbos-tenant": lambda: Cerbos(tenant=True),
    "keto": Keto,
    "cedar": lambda: Cedar(tenant=False),
    "cedar-tenant": lambda: Cedar(tenant=True),
    "casbin": lambda: Casbin(tenant=False),
    "casbin-tenant": lambda: Casbin(tenant=True),
}
TARGET_ORDER = list(TARGETS)
CONTROLS = ("memory", "metadata-acl")
# Pinecone waits up to a minute for every write to show: fewer and smaller corpora.
TARGET_CAPS = {"pinecone": {"examples": 4, "stress_examples": 2, "large_documents": 40}}


# ---- outcomes ------------------------------------------------------------------------------------

_KINDS = (
    ("should not match", "leak"),
    ("may not read", "retrieval-leak"),
    ("failed the re-check", "recheck-violation"),
    ("missed documents", "missed"),
    ("matching documents for k=", "missed"),
    ("readable documents asked for", "missed"),
    ("metadata changed", "metadata-changed"),
    ("text changed", "text-changed"),
    ("not ordered best first", "order"),
    ("scores must be finite", "scores"),
    ("hits for k=", "k-exceeded"),
    ("more than once", "duplicates"),
    ("where retrieve returned", "drivers-disagree"),
    ("different answers for some hits", "filter-check-disagree"),
    ("depended on the other hits", "batch-dependent"),
    ("did not return []", "malformed-answer"),
)
PRIORITY = (
    "leak",
    "retrieval-leak",
    "recheck-violation",
    "filter-check-disagree",
    "metadata-changed",
    "text-changed",
    "drivers-disagree",
    "async-refusal",
    "async-mismatch",
    "batch-dependent",
    "duplicates",
    "k-exceeded",
    "malformed-answer",
    "order",
    "scores",
    "missed",
    "other",
)
# Kinds where an answer admitted what the reference denies or altered what a re-check reads.
WRONG_ANSWERS = (
    "leak",
    "retrieval-leak",
    "recheck-violation",
    "filter-check-disagree",
    "metadata-changed",
    "text-changed",
)
SET_METADATA = "after-set-metadata:"


def parse_failure(message: str) -> dict[str, Any]:
    """A ConformanceError's message, read back into its parts: what failed, the example, the
    problems, the details (filter, k, expected, returned, subject...) and the documents."""
    lines = message.splitlines()
    head = lines[0] if lines else ""
    found = re.search(r"\(seed=(\d+), example (\d+)", head)
    parsed: dict[str, Any] = {
        "what": head.split(" (seed=")[0],
        "example": int(found.group(2)) if found else None,
        "problems": [],
        "details": {},
        "documents": {},
    }
    in_documents = False
    for line in lines[1:]:
        if line.startswith("  - "):
            parsed["problems"].append(line[4:])
        elif line.startswith("  documents ("):
            in_documents = True
        elif in_documents and line.startswith("    "):
            doc_id, _, metadata = line.strip().partition(": ")
            parsed["documents"][doc_id] = _literal(metadata)
        elif line.startswith("  "):
            key, _, value = line.strip().partition(": ")
            parsed["details"][key] = _literal(value)
    return parsed


def violation_kinds(parsed: Mapping[str, Any]) -> list[str]:
    what = str(parsed.get("what", ""))
    problems = [str(p) for p in parsed.get("problems", [])]
    if what.startswith(("asearch and search", "acheck and check", "afilter_for and", "ascope_for and")):
        kinds = ["async-refusal" if any("refused the filter" in p for p in problems) else "async-mismatch"]
    else:
        kinds = []
        fallback = "malformed-answer" if what == "check" else "other"
        for problem in problems:
            kind = next((k for text, k in _KINDS if text in problem), fallback)
            if kind not in kinds:
                kinds.append(kind)
    if "after set_metadata" in what:
        kinds = [f"{SET_METADATA}{kind}" for kind in kinds]
    return kinds or ["other"]


def _base_kind(kind: str) -> str:
    return kind.removeprefix(SET_METADATA)


def primary_kind(kinds: Sequence[str]) -> str:
    def rank(kind: str) -> int:
        base = _base_kind(kind)
        return PRIORITY.index(base) if base in PRIORITY else len(PRIORITY)

    return min(kinds, key=rank)


def _reproducer(parsed: Mapping[str, Any]) -> dict[str, Any]:
    """The parts of a failure needed to replay it by hand: the problems, the filter and k, expected
    against returned ids, and the documents those ids name (all of them for a small corpus)."""
    details = parsed.get("details", {})
    named: set[str] = set()
    for key in ("expected", "returned", "readable", "search", "asearch", "hits"):
        value = details.get(key)
        if isinstance(value, list):
            named.update(v for v in value if isinstance(v, str))
    for problem in parsed.get("problems", []):
        named.update(re.findall(r"'([^']+)'", str(problem)))
        named.update(re.findall(r"\b(doc-\d{3}\S*?)(?=[:,\]\s]|$)", str(problem)))
    documents = parsed.get("documents", {})
    chosen = {i: documents[i] for i in sorted(named) if i in documents}
    if len(documents) <= DOCUMENT_LIMIT:
        chosen = dict(documents)
    return _clip(
        {
            "what": parsed.get("what"),
            "example": parsed.get("example"),
            "problems": parsed.get("problems"),
            **details,
            "documents": dict(list(chosen.items())[:DOCUMENT_LIMIT]),
            "documents_in_example": len(documents),
        }
    )


def _class_name(error: BaseException) -> str:
    kind = type(error)
    module = kind.__module__
    return kind.__qualname__ if module in ("builtins", "__main__") else f"{module}.{kind.__qualname__}"


def _raised_in(error: BaseException) -> str:
    """The module of the frame that raised `error`."""
    tb = error.__traceback__
    module = ""
    while tb is not None:
        module = str(tb.tb_frame.f_globals.get("__name__", ""))
        tb = tb.tb_next
    return module


def classify(error: BaseException) -> str:
    from wardowl.testing import ConformanceError

    if isinstance(error, ConformanceError):
        return VIOLATION
    origin = _raised_in(error)
    if isinstance(error, ValueError) and origin.startswith("wardowl.") and not origin.startswith(HARNESS_MODULES):
        return REFUSED
    return ERROR


def _where(error: BaseException) -> list[str]:
    frames = traceback.extract_tb(error.__traceback__)[-4:]
    return [f"{Path(f.filename).parent.name}/{Path(f.filename).name}:{f.lineno} {f.name}" for f in frames]


def _outcome(error: BaseException, *, keep: bool = False) -> dict[str, Any]:
    """What a failure was. With `keep`, the whole message too, under `full_message`, which `_emit`
    writes to the findings file and leaves out of campaign.jsonl."""
    outcome = classify(error)
    message = _scrub(str(error))
    info: dict[str, Any] = {
        "outcome": outcome,
        "error_class": _class_name(error),
        "raised_in": _raised_in(error),
        "message": _truncate(message, MESSAGE_LIMIT),
    }
    if keep:
        info["full_message"] = message
    if outcome == VIOLATION:
        parsed = parse_failure(message)
        info["kinds"] = violation_kinds(parsed)
        info["kind"] = primary_kind(info["kinds"])
        info["reproducer"] = _reproducer(parsed)
    else:
        info["where"] = _where(error)
        cause = error.__cause__ or error.__context__
        if cause is not None:
            info["cause"] = f"{_class_name(cause)}: {_truncate(_scrub(str(cause)), 500)}"
    return info


# ---- results -------------------------------------------------------------------------------------


class Results:
    """campaign.jsonl, appended to and flushed after every record, so a crash keeps what was done."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, record: Mapping[str, Any]) -> None:
        line = json.dumps({"schema": SCHEMA, **record}, ensure_ascii=False, default=repr)
        with self.path.open("a", encoding="utf-8", errors="backslashreplace") as out:
            out.write(line + "\n")
            out.flush()
            os.fsync(out.fileno())

    def finding(self, record: Mapping[str, Any], message: str) -> None:
        """A run that did not pass, with its whole message, uncut, in findings/<target>.txt beside
        campaign.jsonl: the documents, the filter and every value as the kit printed them."""
        folder = self.path.parent / "findings"
        folder.mkdir(parents=True, exist_ok=True)
        what = record.get("kind") or _short_class(record.get("error_class"))
        lines = [
            f"==== {record.get('target')} seed {record.get('seed')} {record.get('variant')} ({record.get('mode')}): "
            f"{record.get('outcome')} {what}",
            f"replay: {record.get('replay', '')}",
        ]
        if record.get("subject"):
            lines.append(f"subject: {json.dumps(record['subject'], ensure_ascii=False, default=repr)}")
        disagreements = _disagreement_lines(record, DISAGREEMENT_LIMIT)
        if disagreements:
            lines += [f"disagreeing hits ({record.get('disagreements_total')}):", *(f"  {d}" for d in disagreements)]
        lines += ["message:", message, ""]
        target = re.sub(r"[^\w.-]", "_", str(record.get("target")))
        with (folder / f"{target}.txt").open("a", encoding="utf-8", errors="backslashreplace") as out:
            out.write("\n".join(lines) + "\n")


def _run_info() -> dict[str, Any]:
    import wardowl

    return {
        "wardowl": wardowl.__version__,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_ref": os.environ.get("GITHUB_REF_NAME"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "started": _now(),
    }


def _replay(name: str, seed: int, variant: str, settings: Mapping[str, int], *, sound: bool = False) -> str:
    command = (
        f"python {SCRIPT} run --targets {name} --seed-list {seed} --variants {variant} "
        f"--examples {settings['examples']} --stress-examples {settings['stress_examples']} "
        f"--large-documents {settings['large_documents']}"
    )
    return f"{command} --sound-only" if sound else command


def _annotate(level: str, title: str, message: str) -> None:
    """A GitHub Actions annotation (plain text elsewhere)."""
    text = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    print(f"::{level} title={title.replace(':', ' ').replace(',', ' ')}::{text}", flush=True)


BRIEF_LINES = 12  # lines of the head of a message in the log and in an annotation


def _said(answer: Any) -> str:
    return "allows" if answer else "denies"


def _disagreement_lines(record: Mapping[str, Any], limit: int) -> list[str]:
    """One line per disagreeing hit: who, the hit's metadata, the filter's and check's answers, and
    which of them gives the reference answer."""
    lines = []
    for d in (record.get("disagreements") or [])[:limit]:
        side = d.get("matches_reference")
        verdict = f"the reference {_said(d.get('reference'))}, as the {side} does" if side else "no reference"
        metadata = json.dumps(d.get("metadata"), ensure_ascii=False, sort_keys=True, default=repr)
        lines.append(
            f"{d.get('subject')}, {d.get('hit')} {metadata}: the filter {_said(d.get('filter'))}, "
            f"check {_said(d.get('check'))}; {verdict}"
        )
    return lines


def _brief(record: Mapping[str, Any], message: str) -> str:
    """A failure in a few lines, for the log and the annotation: the head of the message, each line cut
    at STRING_LIMIT characters, then the disagreeing hits, or the documents the problems name, with
    their metadata (the kit lists every document after the head, so a cut message hid them)."""
    head: list[str] = []
    for line in message.splitlines():
        if line.startswith("  documents ("):
            break
        head.append(_truncate(line, STRING_LIMIT))
    named = _disagreement_lines(record, 5)
    if not named:
        reproducer = record.get("reproducer") or {}
        documents = reproducer.get("documents") or {}
        ids = {i for p in reproducer.get("problems") or [] for i in re.findall(r"'([^']+)'", str(p))}
        named = [
            f"{i}: {_truncate(json.dumps(documents[i], ensure_ascii=False, sort_keys=True, default=repr), 600)}"
            for i in sorted(ids)
            if i in documents
        ][:5]
    return "\n".join([*head[:BRIEF_LINES], *named])


def _log(name: str, record: Mapping[str, Any], message: str) -> None:
    outcome = record["outcome"]
    what = record.get("kind") or (record.get("error_class") if outcome != PASS else "") or ""
    subjects = f" subjects {record['subjects']}" if "subjects" in record else ""
    refusals = f" ({record['filter_refusals']} filters refused)" if record.get("filter_refusals") else ""
    print(
        f"[{name}] seed {record['seed']} {record['variant']} ({record['mode']}): {outcome} {what}{subjects}"
        f"{refusals} in {record['duration_s']:.1f} s",
        flush=True,
    )
    if outcome == PASS:
        return
    brief = _brief(record, message or str(record.get("message", "")))
    for line in brief.splitlines():
        print(f"    {line}", flush=True)
    if outcome == VIOLATION:
        _annotate("warning", f"{name} {record['variant']} seed {record['seed']}", brief)
    elif name in CONTROLS:
        _annotate("error", f"control {name} did not pass", brief)


def _emit(name: str, results: Results, base: Mapping[str, Any], record: dict[str, Any], counts: Counter[str]) -> None:
    # The whole message goes to findings/<target>.txt; campaign.jsonl keeps the first MESSAGE_LIMIT characters.
    message = record.pop("full_message", None)
    results.write({**base, **record})
    if message is not None:
        results.finding({**base, **record}, message)
    counts[f"{record['mode']} {record['outcome']}"] += 1
    _log(name, record, message or "")


# ---- running -------------------------------------------------------------------------------------


class _Counting:
    """A backend as the kit sees it, counting the filters its `search` refuses with ValueError."""

    def __init__(self, inner: Any, counter: Counter[str]) -> None:
        self._inner = inner
        self._counter = counter

    def search(self, query: Any, k: int, filter: Any = None) -> Any:
        try:
            return self._inner.search(query, k, filter)
        except ValueError:
            if filter is not None:
                self._counter["filter_refusals"] += 1
            raise

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)


def _counting_factory(store: Store, counter: Counter[str]) -> Callable[[Sequence[Any]], Any]:
    def factory(documents: Sequence[Any]) -> Any:
        return _Counting(store.make(documents), counter)

    return factory


def _require_kit(kit: Any) -> None:
    missing = [name for name in (*KIT_NAMES, *KIT_GENERATORS) if not hasattr(kit, name)]
    if missing:
        raise RuntimeError(f"wardowl.testing no longer has {missing}: the campaign's variants need updating")


def _limit(args: argparse.Namespace, deadline: float) -> float:
    """The time limit of one call: --call-timeout, but not much past the target's deadline."""
    return max(60.0, min(args.call_timeout, deadline - time.time() + 60.0))


def _store_run(
    name: str,
    store: Store,
    kit: Any,
    seed: int,
    variant: str,
    settings: Mapping[str, int],
    *,
    exact: bool,
    limit: float,
) -> dict[str, Any]:
    examples = settings["examples"] if variant == "default" else settings["stress_examples"]
    max_documents = settings["large_documents"] if variant == "large-corpus" else 20
    filters = 6 if variant == "large-corpus" else 4
    counter: Counter[str] = Counter()
    started = time.monotonic()
    failure: BaseException | None = None
    try:
        patch = STORE_PATCHES[variant](kit) if variant in STORE_PATCHES else {}
        with patched(kit, patch), time_limit(limit):
            kit.check_backend(
                _counting_factory(store, counter),
                examples=examples,
                seed=seed,
                max_documents=max_documents,
                filters_per_example=filters,
                exact=exact,
            )
    except (Exception, CallTimeout) as error:
        failure = error
    record: dict[str, Any] = {
        "type": "result",
        "seed": seed,
        "variant": variant,
        "mode": "exact" if exact else "sound",
        "examples": examples,
        "max_documents": max_documents,
        "filters_per_example": filters,
        "duration_s": round(time.monotonic() - started, 3),
        "filter_refusals": counter["filter_refusals"],
    }
    record.update({"outcome": PASS} if failure is None else _outcome(failure, keep=True))
    record["replay"] = _replay(name, seed, variant, settings, sound=not exact and store.exact)
    return record


def _only_missed(record: Mapping[str, Any]) -> bool:
    kinds = record.get("kinds") or []
    return bool(kinds) and all(_base_kind(k) == "missed" for k in kinds)


def _reset(target: Store | Engine) -> None:
    if isinstance(target, Store):
        with contextlib.suppress(Exception):
            target.reset()


def _run_store(
    name: str,
    store: Store,
    variants: Sequence[str],
    seeds: Sequence[int],
    settings: Mapping[str, int],
    args: argparse.Namespace,
    results: Results,
    deadline: float,
    base: Mapping[str, Any],
    counts: Counter[str],
    progress: dict[str, int],
) -> None:
    from wardowl import testing as kit

    _require_kit(kit)
    exact = store.exact and not args.sound_only
    for seed in seeds:  # seeds outside, variants inside: a run cut short covers every variant
        for variant in variants:
            if time.time() >= deadline:
                print(f"[{name}] the time budget is spent after {progress['done']} runs", flush=True)
                return
            record = _store_run(name, store, kit, seed, variant, settings, exact=exact, limit=_limit(args, deadline))
            _emit(name, results, base, record, counts)
            progress["done"] += 1
            if record["outcome"] != PASS:
                _reset(store)
            # A short answer from an exact check may be an approximate index: run the same seed
            # sound-only, so wrong answers behind the short one are still found.
            retry = record["outcome"] == VIOLATION and exact and not args.no_sound_retry and _only_missed(record)
            if retry and time.time() < deadline:
                again = _store_run(name, store, kit, seed, variant, settings, exact=False, limit=_limit(args, deadline))
                again["mode"] = "sound-retry"
                _emit(name, results, base, again, counts)
                if again["outcome"] != PASS:
                    _reset(store)


def _combine(answers: Sequence[tuple[Any, BaseException | None]]) -> dict[str, Any]:
    """One record for a run's subjects: the worst outcome among them, and how many had each."""
    tally: Counter[str] = Counter()
    classes: Counter[str] = Counter()
    worst: tuple[Any, BaseException, str] | None = None
    for subject, failure in answers:
        outcome = PASS if failure is None else classify(failure)
        tally[outcome] += 1
        if failure is not None:
            classes[_class_name(failure)] += 1
            if worst is None or RANK[outcome] > RANK[worst[2]]:
                worst = (subject, failure, outcome)
    info: dict[str, Any] = {"subjects": dict(tally), "error_classes": dict(classes)}
    if worst is None:
        info["outcome"] = PASS
        return info
    subject, failure, _ = worst
    info.update(_outcome(failure, keep=True))
    who = {"id": subject.id, "groups": sorted(subject.groups), "attributes": dict(subject.attributes)}
    info["subject"] = _clip(who)
    return info


DISAGREEMENT_LIMIT = 100  # disagreeing hits kept in one record


def _disagreements(engine: Engine, subject: Any, failure: BaseException | None, hits: Sequence[Any]) -> list[Any]:
    """For a filter-and-check disagreement, each disagreeing hit: its metadata, what the filter and
    check said, the reference answer for the target's rule, and which of the two gives it."""
    from wardowl.filters import filter_from_dict, matches
    from wardowl.testing import ConformanceError

    if not isinstance(failure, ConformanceError):
        return []
    parsed = parse_failure(str(failure))
    ids = parsed["details"].get("hits")
    if parsed["what"] != "filter_for and check disagree" or not isinstance(ids, list):
        return []
    try:
        pushed = filter_from_dict(parsed["details"].get("filter"))
    except (TypeError, ValueError):
        return []
    by_id = {hit.id: hit for hit in hits}
    found = []
    for hit_id in ids:
        hit = by_id.get(hit_id)
        if hit is None:
            continue
        by_filter = matches(pushed, hit.metadata)
        reference = engine.reference(subject, hit.metadata)
        found.append(
            {
                "subject": _clip(subject.id),
                "hit": _clip(hit_id),
                "metadata": _clip(dict(hit.metadata)),
                "filter": by_filter,
                "check": not by_filter,  # the kit reports the hits where the two differ
                "reference": reference,
                "matches_reference": None if reference is None else ("filter" if reference == by_filter else "check"),
            }
        )
    return found


def _engine_run(
    name: str, engine: Engine, kit: Any, seed: int, variant: str, settings: Mapping[str, int], limit: float
) -> dict[str, Any]:
    started = time.monotonic()
    record: dict[str, Any] = {"type": "result", "seed": seed, "variant": variant, "mode": "consistency"}
    engine.case = {}
    try:
        subjects, hits = engine_dataset(kit, seed, variant, tenant=engine.tenant)
        record.update({"subjects_total": len(subjects), "hits_total": len(hits)})
        with time_limit(limit):
            authorizer = engine.prepare(subjects, hits)
    except (Exception, CallTimeout) as error:
        record.update(_outcome(error, keep=True))
        record["stage"] = "prepare"
    else:
        answers: list[tuple[Any, BaseException | None]] = []
        for subject in subjects:  # one subject at a time: one subject's failure hides no other's
            failure: BaseException | None = None
            try:
                with time_limit(limit):
                    kit.check_authorizer(authorizer, [subject], hits, seed=seed)
            except (Exception, CallTimeout) as error:
                failure = error
            answers.append((subject, failure))
        record.update(_combine(answers))
        found = [d for subject, failure in answers for d in _disagreements(engine, subject, failure, hits)]
        if found:
            # Every subject's disagreeing hits, and which side gives the reference answer for each.
            record["disagreements"] = found[:DISAGREEMENT_LIMIT]
            record["disagreements_total"] = len(found)
            record["reference_side"] = dict(Counter(str(d["matches_reference"]) for d in found))
    finally:
        with contextlib.suppress(Exception):
            engine.finish()
    record["case"] = dict(engine.case)
    record["duration_s"] = round(time.monotonic() - started, 3)
    record["replay"] = _replay(name, seed, variant, settings)
    return record


def _run_engine(
    name: str,
    engine: Engine,
    variants: Sequence[str],
    seeds: Sequence[int],
    settings: Mapping[str, int],
    args: argparse.Namespace,
    results: Results,
    deadline: float,
    base: Mapping[str, Any],
    counts: Counter[str],
    progress: dict[str, int],
) -> None:
    from wardowl import testing as kit

    _require_kit(kit)
    for seed in seeds:
        for variant in variants:
            if time.time() >= deadline:
                print(f"[{name}] the time budget is spent after {progress['done']} runs", flush=True)
                return
            record = _engine_run(name, engine, kit, seed, variant, settings, _limit(args, deadline))
            _emit(name, results, base, record, counts)
            progress["done"] += 1


def _settings(name: str, args: argparse.Namespace) -> dict[str, int]:
    examples = max(1, args.examples)
    settings = {
        "examples": examples,
        "stress_examples": args.stress_examples if args.stress_examples > 0 else max(2, examples // 3),
        "large_documents": max(1, args.large_documents),
    }
    for key, cap in TARGET_CAPS.get(name, {}).items():
        settings[key] = min(settings[key], cap)
    return settings


def _deadline(args: argparse.Namespace, remaining: int) -> float:
    """When the target must stop starting runs: its own budget, or a fair share of what is left of
    the group's, whichever comes first. Targets that finish early leave their time to the rest."""
    now = time.time()
    deadline = now + args.budget_minutes * 60
    if args.group_deadline:
        share = (args.group_deadline - now) / max(1, remaining)
        deadline = min(deadline, now + max(share, 60.0))
    return deadline


def _setup(target: Store | Engine, timeout: float) -> int:
    """Set the target up, trying again for up to `timeout` seconds while its server boots."""
    started = time.monotonic()
    attempt = 0
    while True:
        attempt += 1
        try:
            with time_limit(max(60.0, timeout)):
                target.setup()
            return attempt
        except TargetSkipped:
            raise
        except (Exception, CallTimeout) as error:
            if time.monotonic() - started > timeout:
                raise
            print(f"  setup attempt {attempt}: {_class_name(error)}: {_truncate(_scrub(str(error)), 300)}", flush=True)
            with contextlib.suppress(Exception):
                target.close()
            time.sleep(10)


def _target_versions(target: Store | Engine, *, reachable: bool) -> dict[str, Any]:
    found: dict[str, Any] = {
        "client": _versions("wardowl", *target.clients),
        "image": _image(target.container) if target.container else None,
        "reported": None,
    }
    if reachable:
        try:
            with time_limit(60):
                found["reported"] = _clip(target.reported())
        except (Exception, CallTimeout) as error:
            found["reported"] = {"error": f"{_class_name(error)}: {_truncate(_scrub(str(error)), 300)}"}
    return found


def run_target(
    name: str,
    args: argparse.Namespace,
    results: Results,
    seeds: Sequence[int],
    chosen: set[str],
    remaining: int,
) -> None:
    target = TARGETS[name]()
    catalogue = STORE_VARIANTS if target.family == "store" else ENGINE_VARIANTS
    variants = [v for v in catalogue if v in chosen]
    settings = _settings(name, args)
    deadline = _deadline(args, remaining)
    base = {"target": name, "family": target.family, "group": GROUP, "run_id": RUN_ID}
    started = time.monotonic()
    until = datetime.fromtimestamp(deadline, UTC).strftime("%H:%M:%S")
    print(f"==> {name} ({target.family}): {len(seeds)} seeds x {len(variants)} variants, until {until} UTC", flush=True)
    results.write(
        {
            **base,
            "type": "target-start",
            "run": _run_info(),
            "notes": target.notes,
            "exact": target.exact,
            "tenant": target.tenant,
            "container": target.container,
            "seeds": list(seeds),
            "variants": variants,
            "settings": settings,
            "deadline": datetime.fromtimestamp(deadline, UTC).isoformat(timespec="seconds"),
        }
    )
    status, problem, attempts = "ok", None, 0
    try:
        attempts = _setup(target, args.setup_timeout)
    except TargetSkipped as skipped:
        status, problem = "skipped", {"message": str(skipped)}
    except (Exception, CallTimeout) as error:
        status, problem = "setup-error", _outcome(error)
    results.write({**base, "type": "versions", **_target_versions(target, reachable=status == "ok")})
    counts: Counter[str] = Counter()
    progress = {"done": 0}
    if status == "ok":
        try:
            if isinstance(target, Store):
                _run_store(name, target, variants, seeds, settings, args, results, deadline, base, counts, progress)
            else:
                _run_engine(name, target, variants, seeds, settings, args, results, deadline, base, counts, progress)
        except (Exception, CallTimeout) as error:  # a fault in the driver: recorded, and the next target runs
            status, problem = "driver-error", _outcome(error)
            traceback.print_exc()
    with contextlib.suppress(Exception):
        target.close()
    planned = len(seeds) * len(variants)
    results.write(
        {
            **base,
            "type": "target-end",
            "status": status,
            "problem": problem,
            "setup_attempts": attempts,
            "runs_planned": planned,
            "runs_done": progress["done"],
            "runs_not_started": planned - progress["done"],
            "outcomes": dict(counts),
            "duration_s": round(time.monotonic() - started, 1),
        }
    )
    print(f"<== {name}: {status}, {progress['done']} of {planned} runs, {dict(counts)}", flush=True)
    if status in ("setup-error", "driver-error"):
        _annotate("error", f"{name} {status}", str((problem or {}).get("message", ""))[:600])


def _chosen_variants(text: str) -> set[str] | None:
    known = {*STORE_VARIANTS, *ENGINE_VARIANTS}
    if text.strip() in ("", "all"):
        return known
    chosen = {v.strip() for v in text.split(",") if v.strip()}
    unknown = chosen - known
    if unknown:
        print(f"unknown variants {sorted(unknown)}; known: {', '.join(VARIANT_ORDER)}", file=sys.stderr)
        return None
    return chosen


def run(args: argparse.Namespace) -> int:
    names = [n.strip() for n in args.targets.split(",") if n.strip()]
    unknown = [n for n in names if n not in TARGETS]
    if unknown or not names:
        print(f"unknown targets {unknown}; known: {', '.join(TARGET_ORDER)}", file=sys.stderr)
        return 2
    chosen = _chosen_variants(args.variants)
    if chosen is None:
        return 2
    if args.seed_list:
        seeds = [int(s) for s in args.seed_list.split(",") if s.strip()]
    else:
        seeds = list(range(args.seed_start, args.seed_start + args.seeds))
    results = Results(Path(args.out) / "campaign.jsonl")
    for index, name in enumerate(names):
        remaining = args.remaining if len(names) == 1 else len(names) - index
        run_target(name, args, results, seeds, chosen, remaining)
    return 0


# ---- summary -------------------------------------------------------------------------------------


def _read(paths: Sequence[str]) -> tuple[list[dict[str, Any]], int]:
    records: list[dict[str, Any]] = []
    unreadable = 0
    for path in paths:
        source = Path(path)
        if not source.is_file():
            print(f"no such file: {path}", file=sys.stderr)
            continue
        with source.open(encoding="utf-8", errors="replace") as lines:
            for line in lines:
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except ValueError:
                    unreadable += 1
                else:
                    if isinstance(value, dict):
                        records.append(value)
    return records, unreadable


def _cell(text: Any, limit: int = 160) -> str:
    flat = " ".join(str(text).split())
    return _truncate(flat, limit).replace("|", "\\|")


def _ranges(numbers: Sequence[int]) -> str:
    """0-4, 7, 9-10."""
    values = sorted(set(numbers))
    parts: list[str] = []
    start = previous = None
    for value in [*values, None]:
        if start is not None and (value is None or value != previous + 1):
            parts.append(str(start) if start == previous else f"{start}-{previous}")
            start = None
        if value is not None and start is None:
            start = value
        previous = value
    return ", ".join(parts)


def _short_class(name: Any) -> str:
    return str(name or "?").rsplit(".", 1)[-1]


def _version_text(versions: Mapping[str, Any] | None) -> str:
    if not versions:
        return ""
    parts = []
    image = (versions.get("image") or {}).get("image")
    if image:
        parts.append(f"`{image}`")
    reported = versions.get("reported")
    if isinstance(reported, dict) and reported and "error" not in reported:
        parts.append(json.dumps(reported, ensure_ascii=False, sort_keys=True))
    if not parts:
        clients = {k: v for k, v in (versions.get("client") or {}).items() if k != "wardowl" and v}
        parts.append(", ".join(f"{k} {v}" for k, v in clients.items()))
    return _cell("; ".join(parts), 140)


def _status(start: Mapping[str, Any] | None, end: Mapping[str, Any] | None, crashes: Sequence[Any]) -> str:
    if crashes:
        return f"driver stopped (exit {crashes[-1].get('exit_status')})"
    if end is None:
        return "incomplete" if start else "no records"
    status = end.get("status")
    problem = end.get("problem") or {}
    if status == "ok":
        missing = end.get("runs_not_started") or 0
        return f"time budget: {missing} of {end.get('runs_planned')} runs not started" if missing else "complete"
    if status == "skipped":
        return _cell(f"skipped: {problem.get('message', '')}", 90)
    first = str(problem.get("message", "")).splitlines()[:1]
    return _cell(f"{status}: {_short_class(problem.get('error_class'))}: {first[0] if first else ''}", 120)


def _count_text(runs: Sequence[Mapping[str, Any]], outcome: str, key: str) -> str:
    chosen = [r for r in runs if r.get("outcome") == outcome]
    if not chosen:
        return "0"
    tally = Counter(_short_class(r.get(key)) if key == "error_class" else str(r.get(key)) for r in chosen)
    return f"{len(chosen)} ({', '.join(f'{k} {n}' for k, n in tally.most_common())})"


def _controls_section(runs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[str]:
    lines = ["## Controls", ""]
    for name in CONTROLS:
        chosen = runs.get(name) or []
        if not chosen:
            lines.append(f"- {name}: not in these results.")
            continue
        bad = [r for r in chosen if r.get("outcome") != PASS]
        verdict = " **The control failed: fix the harness before reading any other row.**" if bad else ""
        lines.append(f"- {name}: {len(chosen) - len(bad)} of {len(chosen)} runs pass.{verdict}")
    return [*lines, ""]


def _findings_section(names: Sequence[str], runs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[str]:
    wrong: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    other: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for name in names:
        for record in runs.get(name) or []:
            if record.get("outcome") != VIOLATION:
                continue
            kind = str(record.get("kind", "other"))
            (wrong if _base_kind(kind) in WRONG_ANSWERS else other)[(name, kind)].append(record)

    def order(key: tuple[str, str]) -> tuple[int, str]:
        return (TARGET_ORDER.index(key[0]) if key[0] in TARGET_ORDER else len(TARGET_ORDER), key[1])

    lines = ["## Violations", ""]
    sections = (("Wrong answers (leaks, filter and check disagreeing, altered metadata)", wrong), ("Others", other))
    for title, found in sections:
        lines.append(f"{title}:")
        lines.append("")
        if not found:
            lines.append("- none")
        for key in sorted(found, key=order):
            name, kind = key
            records = found[key]
            variants = sorted({str(r.get("variant")) for r in records}, key=_variant_index)
            seeds = _ranges([int(r.get("seed", 0)) for r in records])
            lines.append(f"- {name}: {kind} in {len(records)} runs (variants {', '.join(variants)}; seeds {seeds})")
            sides: Counter[str] = Counter()
            for record in records:
                sides.update(record.get("reference_side") or {})
            if sides:
                lines.append(
                    f"  - {sum(sides.values())} disagreeing hits: the filter gives the reference answer for "
                    f"{sides.get('filter', 0)}, check for {sides.get('check', 0)}"
                )
        lines.append("")
    return lines


def _overview_section(
    names: Sequence[str],
    starts: Mapping[str, Mapping[str, Any]],
    versions: Mapping[str, Mapping[str, Any]],
    ends: Mapping[str, Mapping[str, Any]],
    crashes: Mapping[str, Sequence[Any]],
    runs: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[str]:
    lines = [
        "## Targets",
        "",
        "Runs count one (seed, variant) each; sound-only retries of short exact answers are not counted here.",
        "",
        "| Target | Family | Version | Status | Seeds | Runs | Pass | Violations | Refused | Errors |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in names:
        chosen = [r for r in runs.get(name) or [] if r.get("mode") != "sound-retry"]
        tally = Counter(r.get("outcome") for r in chosen)
        family = (starts.get(name) or {}).get("family", "")
        lines.append(
            f"| {name} | {family} | {_version_text(versions.get(name))} | "
            f"{_status(starts.get(name), ends.get(name), crashes.get(name) or [])} | "
            f"{len({r.get('seed') for r in chosen})} | {len(chosen)} | {tally[PASS]} | {tally[VIOLATION]} | "
            f"{tally[REFUSED]} | {tally[ERROR]} |"
        )
    return [*lines, ""]


def _target_section(
    name: str,
    start: Mapping[str, Any] | None,
    versions: Mapping[str, Any] | None,
    runs: Sequence[Mapping[str, Any]],
) -> list[str]:
    lines = [f"## {name}", ""]
    if start:
        settings = start.get("settings") or {}
        lines.append(f"{start.get('notes', '')}.")
        lines.append("")
        lines.append(
            f"Seeds {_ranges(start.get('seeds') or [])}; {settings.get('examples')} corpora per seed for the default "
            f"variant, {settings.get('stress_examples')} for the others; large corpora of up to "
            f"{settings.get('large_documents')} documents."
        )
        lines.append("")
    if versions:
        image = versions.get("image") or {}
        if image:
            lines.append(f"Image `{image.get('image')}`, id `{image.get('image_id')}`, digests {image.get('digests')}.")
        if versions.get("reported"):
            lines.append(f"Reported: `{json.dumps(versions['reported'], ensure_ascii=False, sort_keys=True)}`.")
        clients = {k: v for k, v in (versions.get("client") or {}).items() if v}
        lines.append(f"Python packages: {', '.join(f'{k} {v}' for k, v in clients.items())}.")
        lines.append("")
    if not runs:
        return [*lines, "No runs.", ""]
    engine = (start or {}).get("family") == "engine" or any("subjects" in r for r in runs)
    last = "Subjects passing" if engine else "Filters refused"
    lines += [
        f"| Variant | Mode | Seeds | Pass | Violations | Refused | Errors | {last} |",
        "|---|---|---:|---:|---|---|---|---:|",
    ]
    rows: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for record in runs:
        rows[(str(record.get("variant")), str(record.get("mode")))].append(record)

    def order(key: tuple[str, str]) -> tuple[int, str]:
        return (_variant_index(key[0]), key[1])

    for variant, mode in sorted(rows, key=order):
        chosen = rows[(variant, mode)]
        if engine:
            passing = sum((r.get("subjects") or {}).get(PASS, 0) for r in chosen)
            total = sum(sum((r.get("subjects") or {}).values()) for r in chosen)
            extra = f"{passing}/{total}"
        else:
            extra = str(sum(int(r.get("filter_refusals") or 0) for r in chosen))
        lines.append(
            f"| {variant} | {mode} | {len({r.get('seed') for r in chosen})} | "
            f"{sum(1 for r in chosen if r.get('outcome') == PASS)} | {_count_text(chosen, VIOLATION, 'kind')} | "
            f"{_count_text(chosen, REFUSED, 'error_class')} | {_count_text(chosen, ERROR, 'error_class')} | {extra} |"
        )
    lines.append("")
    first: dict[tuple[str, str, str, str], Mapping[str, Any]] = {}
    for record in sorted(runs, key=lambda r: (order((str(r.get("variant")), str(r.get("mode")))), r.get("seed", 0))):
        if record.get("outcome") != PASS:
            what = str(record.get("kind") or _short_class(record.get("error_class")))
            key = (str(record.get("variant")), str(record.get("mode")), str(record.get("outcome")), what)
            first.setdefault(key, record)
    if first:
        lines += ["The first run of each kind of failure:", ""]
        for (variant, mode, outcome, what), record in list(first.items())[:30]:
            message = str(record.get("message", "")).splitlines()[:1]
            lines.append(
                f"- {variant} ({mode}), seed {record.get('seed')}: **{outcome}** {what}. "
                f"{_cell(message[0] if message else '', 300)}"
            )
            lines += [f"  Disagreeing hit: {_cell(d, 400)}" for d in _disagreement_lines(record, 3)]
            lines.append(f"  Replay: `{record.get('replay', '')}`")
        lines.append("")
    return lines


_STATUS_RANK = {"ok": 0, "skipped": 1, "setup-error": 2, "driver-error": 3}


def _merge_start(previous: Mapping[str, Any] | None, record: Mapping[str, Any]) -> Mapping[str, Any]:
    """One target-start for a target whose seeds ran in several jobs: the first, with every job's seeds."""
    if previous is None:
        return record
    return {**previous, "seeds": sorted({*(previous.get("seeds") or []), *(record.get("seeds") or [])})}


def _merge_end(previous: Mapping[str, Any] | None, record: Mapping[str, Any]) -> Mapping[str, Any]:
    """One target-end for a target whose seeds ran in several jobs: runs and outcomes added up, and
    the worst status kept, so a part that stopped early is not hidden by one that finished."""
    if previous is None:
        return record
    rank = _STATUS_RANK.get(str(record.get("status")), len(_STATUS_RANK))
    worse = record if rank > _STATUS_RANK.get(str(previous.get("status")), len(_STATUS_RANK)) else previous
    merged = dict(worse)
    for key in ("runs_planned", "runs_done", "runs_not_started"):
        merged[key] = int(previous.get(key) or 0) + int(record.get(key) or 0)
    outcomes: Counter[str] = Counter(previous.get("outcomes") or {})
    outcomes.update(record.get("outcomes") or {})
    merged["outcomes"] = dict(outcomes)
    return merged


def summarize_records(records: Sequence[Mapping[str, Any]], unreadable: int = 0) -> str:
    starts: dict[str, Mapping[str, Any]] = {}
    versions: dict[str, Mapping[str, Any]] = {}
    ends: dict[str, Mapping[str, Any]] = {}
    crashes: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    runs: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for record in records:
        name = str(record.get("target", "?"))
        kind = record.get("type")
        if kind == "target-start":
            starts[name] = _merge_start(starts.get(name), record)
        elif kind == "versions":
            versions[name] = record
        elif kind == "target-end":
            ends[name] = _merge_end(ends.get(name), record)
        elif kind == "crash":
            crashes[name].append(record)
        elif kind == "result":
            runs[name].append(record)
    names = sorted(
        {*starts, *ends, *runs, *crashes},
        key=lambda n: (TARGET_ORDER.index(n) if n in TARGET_ORDER else len(TARGET_ORDER), n),
    )
    run = next((s["run"] for s in starts.values() if isinstance(s.get("run"), dict)), {})
    total = sum(1 for rs in runs.values() for r in rs if r.get("mode") != "sound-retry")
    lines = [
        "# Conformance campaign",
        "",
        f"wardowl {run.get('wardowl', '?')} at commit `{run.get('github_sha') or '?'}`, workflow run "
        f"{run.get('github_run_id') or 'local'}, Python {run.get('python', '?')}: {len(names)} targets, {total} runs.",
        "",
        "Outcomes: **pass**, the kit found nothing; **conformance-violation**, the kit's first disagreement with "
        "the reference; **refused-ValueError**, wardowl refused the data or a filter; **error**, anything else. "
        "Engines are checked one subject at a time; a run takes its worst subject's outcome. Every run "
        "that did not pass is in its group's artifact, findings/<target>.txt, with the whole message. "
        "See benchmarks/paper/CONFORMANCE.md.",
        "",
    ]
    if unreadable:
        lines += [f"{unreadable} lines could not be read and were left out.", ""]
    lines += _controls_section(runs)
    lines += _findings_section(names, runs)
    lines += _overview_section(names, starts, versions, ends, crashes, runs)
    for name in names:
        lines += _target_section(name, starts.get(name), versions.get(name), runs.get(name) or [])
    return "\n".join(lines) + "\n"


def summarize(args: argparse.Namespace) -> int:
    records, unreadable = _read(args.inputs)
    if args.merged:
        merged = Path(args.merged)
        merged.parent.mkdir(parents=True, exist_ok=True)
        with merged.open("w", encoding="utf-8", errors="backslashreplace") as out:
            for record in records:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
    summary = Path(args.summary)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(summarize_records(records, unreadable), encoding="utf-8")
    print(f"{len(records)} records from {len(args.inputs)} files; summary in {summary}")
    return 0


def check(args: argparse.Namespace) -> int:
    """Exit 1 when a target could not run to its end: a setup error, a driver fault or a crash.
    Violations, refusals and errors inside runs are results, not failures of the campaign."""
    records, _ = _read(args.inputs)
    started = {str(r.get("target")) for r in records if r.get("type") == "target-start"}
    ended: set[str] = set()
    problems: list[str] = []
    for record in records:
        name = str(record.get("target"))
        if record.get("type") == "target-end":
            ended.add(name)
            if record.get("status") in ("setup-error", "driver-error"):
                message = str((record.get("problem") or {}).get("message", "")).splitlines()[:1]
                problems.append(f"{name}: {record.get('status')}: {message[0] if message else ''}")
        elif record.get("type") == "crash":
            problems.append(f"{name}: the driver stopped with exit status {record.get('exit_status')}")
    problems += [f"{name}: started but never finished" for name in sorted(started - ended)]
    if not records:
        problems.append("no records")
    for problem in problems:
        _annotate("error", "campaign", problem)
    print(f"{len(started)} targets started, {len(ended)} finished, {len(problems)} problems")
    return 1 if problems else 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)

    runner = commands.add_parser("run", help="run targets and append their records to OUT/campaign.jsonl")
    runner.add_argument("--targets", required=True, help=f"comma-separated, of: {', '.join(TARGET_ORDER)}")
    runner.add_argument("--seeds", type=int, default=20, help="seeds per target and variant (default 20)")
    runner.add_argument("--seed-start", type=int, default=0, help="the first seed (default 0)")
    runner.add_argument("--seed-list", default="", help="comma-separated seeds, in place of --seeds (to replay)")
    runner.add_argument("--examples", type=int, default=10, help="corpora per seed, default variant (default 10)")
    runner.add_argument(
        "--stress-examples", type=int, default=0, help="corpora per seed, other variants (default: a third, at least 2)"
    )
    runner.add_argument("--large-documents", type=int, default=150, help="corpus size of large-corpus (default 150)")
    runner.add_argument("--variants", default="all", help=f"comma-separated, or all: {', '.join(VARIANT_ORDER)}")
    runner.add_argument("--budget-minutes", type=float, default=90.0, help="time budget per target (default 90)")
    runner.add_argument("--group-deadline", type=float, default=0.0, help="Unix time when the job's targets must stop")
    runner.add_argument("--remaining", type=int, default=1, help="targets left in the job, this one included")
    runner.add_argument("--call-timeout", type=float, default=900.0, help="limit of one kit call, seconds (900)")
    runner.add_argument("--setup-timeout", type=float, default=300.0, help="how long to wait for a server (300)")
    runner.add_argument("--sound-only", action="store_true", help="check every store sound-only (exact=False)")
    runner.add_argument("--no-sound-retry", action="store_true", help="no sound-only rerun after a short answer")
    runner.add_argument("--out", default="results", help="directory of campaign.jsonl (default results)")

    summary = commands.add_parser("summarize", help="write the summary of one or more campaign.jsonl files")
    summary.add_argument("inputs", nargs="+")
    summary.add_argument("--summary", default="results/summary.md")
    summary.add_argument("--merged", default="", help="also write every record into this one file")

    checker = commands.add_parser("check", help="exit 1 if a target could not run to its end")
    checker.add_argument("inputs", nargs="+")

    args = parser.parse_args(argv)
    if args.command == "run":
        return run(args)
    if args.command == "summarize":
        return summarize(args)
    return check(args)


if __name__ == "__main__":
    sys.exit(main())
