"""Filters an authorizer builds itself, deeper or wider than any policy writes.

`filter_from_dict` refuses a document nested more than 100 levels deep (tests/test_filters.py), but
`And`, `Or` and `In` build a filter of any depth and width, and an authorizer's `filter_for` or
`scope_for` hands the retriever what it built. The retriever refuses one nested more than 100
levels deep with `AuthorizationError` on every path that takes it, before anything is searched, and
searches with a very wide `In`. The property and the generated shapes come from the fuzz target
fuzz/constructed_filters_fuzzer.py.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from wardowl import And, Filter, Hit, In, Or, Subject, matches

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fuzz"))
from constructed_filters_fuzzer import CORPUS, LIMIT, PATHS, Given, build, check_constructed


class NativeAsync(Given):
    """The same answers through the async methods `aretrieve` prefers to a worker thread."""

    async def acheck(self, subject: Subject, hits: Sequence[Hit], action: str = "read") -> list[bool]:
        return self.check(subject, hits, action)

    async def afilter_for(self, subject: Subject, action: str = "read") -> Filter | None:
        return self.filter_for(subject, action)

    async def ascope_for(self, subject: Subject, action: str = "read") -> Filter | None:
        return self.scope_for(subject, action)


def chain(op: Callable[[Filter], Filter], depth: int) -> Filter:
    """An `In` inside `depth - 1` one-clause `And`s or `Or`s, built without recursion."""
    f: Filter = In("allowed_groups", ["eng"])
    for _ in range(depth - 1):
        f = op(f)
    return f


SHAPES: dict[str, Callable[[int], Filter]] = {
    "And": lambda depth: chain(And, depth),
    "Or": lambda depth: chain(Or, depth),
    "And and Or, with In beside each level": lambda depth: build(depth, siblings=2, wide=0, seed=depth),
}
PATH_IDS = [f"{strategy}, {source}" + ("" if recheck else ", recheck=False") for strategy, source, recheck in PATHS]
# The first depth refused, and one past Python's recursion limit, which no recursive walk could take.
PAST_THE_LIMIT = [LIMIT + 1, sys.getrecursionlimit() + 1]


@pytest.mark.parametrize("path", PATHS, ids=PATH_IDS)
@pytest.mark.parametrize("shape", SHAPES)
@pytest.mark.parametrize("depth", PAST_THE_LIMIT)
@pytest.mark.parametrize("authorizer", [Given, NativeAsync], ids=["sync", "native async"])
def test_a_constructed_filter_nested_more_than_a_hundred_levels_is_refused_on_every_path(
    path, shape, depth, authorizer
):
    # retrieve and aretrieve both raise AuthorizationError, and the store is never searched.
    check_constructed(SHAPES[shape](depth), depth, [path], run_async=True, authorizer=authorizer)


@pytest.mark.parametrize("path", PATHS, ids=PATH_IDS)
@pytest.mark.parametrize("shape", SHAPES)
def test_a_constructed_filter_a_hundred_levels_deep_is_searched_on_every_path(path, shape):
    f = SHAPES[shape](LIMIT)
    check_constructed(f, LIMIT, [path], run_async=True)
    check_constructed(f, LIMIT, [path], run_async=True, authorizer=NativeAsync)


@pytest.mark.parametrize("width", [10_000, 100_000])
def test_a_very_wide_in_is_searched_on_every_path(width):
    # A subject in many groups: thousands of values that match nothing, and one that does.
    wide = In("allowed_groups", [*(f"group-{i + 100}" for i in range(width - 1)), "eng"])
    assert {d.id for d in CORPUS if matches(wide, d.metadata)} == {"eng", "scalar"}
    check_constructed(wide, 1, run_async=True)
    # Many wide clauses, as an authorizer that ORs one In per source of grants.
    many = Or(*(In("allowed_groups", [f"source-{j}/group-{i}" for i in range(2_000)]) for j in range(50)), wide)
    check_constructed(many, 2, run_async=True)
    check_constructed(And(In("tenant", ["acme"]), many), 3, run_async=True)


depths = st.one_of(
    st.integers(1, 8),
    st.integers(LIMIT - 4, LIMIT + 8),
    st.integers(sys.getrecursionlimit() + 1, sys.getrecursionlimit() + 64),
)
widths = st.one_of(st.integers(0, 6), st.sampled_from([10_000, 60_000]))


@settings(max_examples=150, deadline=None)
@given(depths, st.integers(0, 3), widths, st.integers(0, 2**64 - 1), st.text(max_size=8))
def test_generated_constructed_filters_are_refused_or_searched(depth, siblings, wide, seed, text):
    check_constructed(build(depth, siblings, wide, seed, text), depth)
