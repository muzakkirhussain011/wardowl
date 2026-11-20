"""Fuzz target: filters an authorizer builds itself, of any depth and width, given to the retriever.

ClusterFuzzLite builds and runs this with Atheris (see .clusterfuzzlite/), beside
filters_fuzzer.py, which parses and translates filters no deeper than four levels. `filter_from_dict`
refuses a document nested more than 100 levels deep, but `And`, `Or` and `In` build a filter of any
depth and width, and an authorizer's `filter_for` or `scope_for` hands the retriever what it built.
`build` makes such a filter from a few numbers, as deep as past Python's recursion limit and with an
`In` of tens of thousands of values, and `check_constructed` holds the property, so the test suite
runs it on generated inputs too (tests/test_filters_deep_and_wide.py):

* on every path that takes the authorizer's filter or scope (pre-filtering with and without the
  re-check, "auto", post-filtering inside a scope, `aretrieve`), a filter nested more than 100
  levels deep is refused with `AuthorizationError` before anything is searched;
* any other filter is searched in the in-memory store without an exception, and the result is
  exactly the chunks it matches.
"""

from __future__ import annotations

import asyncio
import sys
from collections.abc import Iterator, Sequence
from typing import Any

from wardowl import (
    And,
    AuthorizationError,
    Document,
    Filter,
    Hit,
    In,
    InMemoryBackend,
    Or,
    PermissionedRetriever,
    Query,
    Subject,
    matches,
)

LIMIT = 100  # the depth the retriever accepts, as filter_from_dict does
REFUSED = f"nested more than {LIMIT} levels deep"
FIELDS = ("allowed_groups", "allowed_users", "tenant", "level")
VALUES: tuple[str | int, ...] = ("eng", "hr", "*", "alice", "bob", "acme", "globex", "group-7", 1, 2)
QUERY = "leave"  # in every chunk, so a search finds every chunk a filter matches
K = 10  # more than the corpus holds: a result is every chunk the filter matches
CORPUS = [
    Document("open", "leave policy", {"allowed_groups": ["*"], "tenant": "acme"}),
    Document("eng", "leave rota for eng", {"allowed_groups": ["eng"], "allowed_users": ["bob"], "tenant": "acme"}),
    Document("hr", "leave cases", {"allowed_groups": ["hr"], "tenant": "globex", "level": 2}),
    Document("named", "leave request", {"allowed_users": ["alice"], "tenant": "acme", "level": 1}),
    Document("scalar", "leave notes", {"allowed_groups": "eng", "tenant": "acme"}),
    Document("many", "leave of a large group", {"allowed_groups": ["group-7", "sales"], "tenant": "globex"}),
    Document("odd", "leave with odd values", {"allowed_groups": [True, 1.0, None], "level": True}),
    Document("bare", "leave without permissions", {}),
]
SUBJECT = Subject("alice", ["eng"], {"tenant": "acme"})
# (strategy, where the authorizer's answer comes from, recheck): every path that takes it.
PATHS: tuple[tuple[str, str, bool], ...] = (
    ("prefilter", "filter", True),
    ("prefilter", "filter", False),
    ("auto", "filter", True),
    ("postfilter", "scope", True),
    ("postfilter", "scope", False),
    ("auto", "scope", True),
)


def _numbers(seed: int) -> Iterator[int]:
    """Reproducible numbers for a filter's shape, from a 64-bit linear congruential generator."""
    state = seed & 0xFFFF_FFFF_FFFF_FFFF
    while True:
        state = (state * 6364136223846793005 + 1442695040888963407) & 0xFFFF_FFFF_FFFF_FFFF
        yield state >> 33


def build(depth: int, siblings: int, wide: int, seed: int, text: str = "") -> Filter:
    """A filter exactly `depth` levels deep, built without recursion: a spine of `And` and `Or`, each
    level with up to `siblings` `In` clauses beside the next, so its size grows with its depth, not
    exponentially. With `wide` > 0, one `In` holds `wide` values, as for a subject in thousands of
    groups. `seed` picks the rest; `text`, from the fuzzer, is one more field name and value."""
    numbers = _numbers(seed)
    fields = (*FIELDS, text) if text else FIELDS
    values = (*VALUES, text)

    def pick(options: Sequence[Any]) -> Any:
        return options[next(numbers) % len(options)]

    def leaf(width: int = 0) -> In:
        if width:  # many values that match nothing, and one that may
            return In(pick(fields), [*(f"group-{i + 100}" for i in range(width - 1)), pick(values)])
        return In(pick(fields), [pick(values) for _ in range(next(numbers) % 4)])

    widened = next(numbers) % depth if wide else -1  # the level that holds the wide In
    node: Filter = leaf(wide if widened == 0 else 0)
    for level in range(1, depth):
        clauses: list[Filter] = [node, *(leaf() for _ in range(next(numbers) % (siblings + 1)))]
        if level == widened:
            clauses.append(leaf(wide))
        turn = next(numbers) % len(clauses)
        clauses = clauses[turn:] + clauses[:turn]
        node = And(*clauses) if next(numbers) % 2 else Or(*clauses)
    return node


class Given:
    """An authorizer whose answer is `f`: as its filter, or as its scope with no filter. Its check
    decides each chunk by `f` as well, so every path's result is the chunks `f` matches."""

    def __init__(self, f: Filter, source: str) -> None:
        self.f = f
        self.source = source

    def check(self, subject: Subject, hits: Sequence[Hit], action: str = "read") -> list[bool]:
        return [matches(self.f, h.metadata) for h in hits]

    def filter_for(self, subject: Subject, action: str = "read") -> Filter | None:
        return self.f if self.source == "filter" else None

    def scope_for(self, subject: Subject, action: str = "read") -> Filter | None:
        return self.f if self.source == "scope" else None


class Counted(InMemoryBackend):
    """The in-memory store, counting its searches."""

    def __init__(self, documents: Sequence[Document]) -> None:
        super().__init__(documents)
        self.searches = 0

    def search(self, query: str | Query, k: int, filter: Filter | None = None) -> list[Hit]:
        self.searches += 1
        return super().search(query, k, filter)


def check_constructed(
    f: Filter,
    depth: int,
    paths: Sequence[tuple[str, str, bool]] = PATHS,
    *,
    run_async: bool = False,
    authorizer: type[Given] = Given,
) -> None:
    """The property for a filter `depth` levels deep, on each of `paths`, with `aretrieve` as well
    when `run_async` is set."""
    for strategy, source, recheck in paths:
        backend = Counted(CORPUS)
        retriever = PermissionedRetriever(backend, authorizer(f, source), strategy=strategy, recheck=recheck)
        runs = [lambda r=retriever: r.retrieve(QUERY, SUBJECT, k=K)]
        if run_async:
            runs.append(lambda r=retriever: asyncio.run(r.aretrieve(QUERY, SUBJECT, k=K)))
        for run in runs:
            try:
                result = run()
            except AuthorizationError as error:
                assert depth > LIMIT, f"{strategy}/{source}: refused a filter {depth} levels deep: {error}"
                assert REFUSED in str(error), str(error)
                assert backend.searches == 0, f"{strategy}/{source}: searched before refusing"
                continue
            assert depth <= LIMIT, f"{strategy}/{source}: took a filter {depth} levels deep"
            ids = [h.id for h in result.hits]
            expected = {d.id for d in CORPUS if matches(f, d.metadata)}
            assert len(ids) == len(set(ids)) == min(K, len(expected)), (strategy, source, ids, expected)
            assert set(ids) <= expected and result.violations == 0, (strategy, source, ids, expected)


def TestOneInput(data: bytes) -> None:  # the name Atheris looks for
    import atheris

    fdp = atheris.FuzzedDataProvider(data)
    path = PATHS[fdp.ConsumeIntInRange(0, len(PATHS) - 1)]
    bucket = fdp.ConsumeIntInRange(0, 7)
    if bucket == 0:  # just past the retriever's limit
        depth = LIMIT + fdp.ConsumeIntInRange(1, 8)
    elif bucket == 1:  # past Python's recursion limit, where recursing into it would fail
        depth = sys.getrecursionlimit() + fdp.ConsumeIntInRange(1, 64)
    elif bucket == 2:  # at the limit or just under it
        depth = LIMIT - fdp.ConsumeIntInRange(0, 4)
    else:
        depth = fdp.ConsumeIntInRange(1, 8)
    siblings = fdp.ConsumeIntInRange(0, 3)
    wide = fdp.ConsumeIntInRange(10_000, 60_000) if fdp.ConsumeIntInRange(0, 15) == 0 else fdp.ConsumeIntInRange(0, 6)
    seed = fdp.ConsumeInt(8)
    run_async = fdp.ConsumeIntInRange(0, 15) == 0
    text = fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(0, 12))
    check_constructed(build(depth, siblings, wide, seed, text), depth, (path,), run_async=run_async)


def main() -> None:
    import atheris

    atheris.instrument_all()
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
