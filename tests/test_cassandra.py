"""Cassandra: the OR of ANDs, settings, and the conformance kit against a real Cassandra."""

from __future__ import annotations

import os
import uuid

import pytest
from helpers import long_value_outcomes

from wardowl import And, Document, In, MetadataACLAuthorizer, Or, PermissionedRetriever, Query, Subject
from wardowl.backends._engines import tag
from wardowl.backends.cassandra import (
    CassandraBackend,
    TooManyQueries,
    create_table,
    filter_to_conjunctions,
    required_terms,
)
from wardowl.testing import QUERY, HashingEmbedder, check_backend

EMBED = HashingEmbedder()
HOST = os.environ.get("WARDOWL_TEST_CASSANDRA_HOST")


# ---- the OR of ANDs and settings (no server) ---------------------------------------------------


def test_filters_become_an_or_of_ands():
    a, b, c = tag("a", "x"), tag("b", "y"), tag("c", 1)
    assert filter_to_conjunctions(In("a", ["x"])) == [frozenset({a})]
    assert filter_to_conjunctions(And(In("a", ["x"]), Or(In("b", ["y"]), In("c", [1])))) == sorted(
        [frozenset({a, b}), frozenset({a, c})], key=sorted
    )
    assert filter_to_conjunctions(Or(In("a", ["x"]), In("a", ["x"]))) == [frozenset({a})]
    assert filter_to_conjunctions(In("a", [])) == []
    assert filter_to_conjunctions(And(In("a", ["x"]), In("b", []))) == []
    with pytest.raises(ValueError):
        filter_to_conjunctions(In("a\x1fb", ["x"]))
    with pytest.raises(TypeError):
        filter_to_conjunctions("a")
    wide = In("g", range(1000))
    with pytest.raises(ValueError, match="more than 10000"):
        filter_to_conjunctions(And(wide, In("h", range(1000))))
    with pytest.raises(ValueError, match="more than 5"):
        filter_to_conjunctions(wide, 5)
    assert filter_to_conjunctions(Or(In("a", ["x"]), And(In("a", ["x"]), In("b", ["y"])))) == [frozenset({a})]
    assert required_terms(And(In("a", ["x"]), Or(And(In("b", ["y"]), In("c", [1])), In("b", ["y"])))) == {a, b}
    assert required_terms(In("a", ["x", "z"])) == frozenset()
    with pytest.raises(TypeError):
        required_terms("a")


class NoSession:
    def __getattr__(self, name):
        raise AssertionError(f"Cassandra was asked: {name}")


def test_settings_and_searches_that_need_no_query():
    backend = CassandraBackend(NoSession(), "ks", "chunks", EMBED, max_queries=2)
    assert backend.search("q", 0) == [] and backend.search("q", 3, In("team", [])) == []
    backend.add([])
    backend.delete([])
    with pytest.raises(TooManyQueries):
        filter_to_conjunctions(In("team", ["a", "b", "c"]), 2)
    for bad in ({"keyspace": "Ks"}, {"table": "a;b"}):
        with pytest.raises(ValueError):
            CassandraBackend(NoSession(), **{"keyspace": "ks", "table": "t", **bad}, embed=EMBED)
    with pytest.raises(ValueError):
        CassandraBackend(NoSession(), "ks", "t", EMBED, similarity="manhattan")
    with pytest.raises(ValueError):
        CassandraBackend(NoSession(), "ks", "t", EMBED, concurrency=0)
    for args in (("ks", "t", 0), ("ks", "T", 4)):
        with pytest.raises(ValueError):
            create_table(NoSession(), *args)
    with pytest.raises(ValueError):
        create_table(NoSession(), "ks", "t", 4, similarity="manhattan")


def test_k_above_what_one_ann_query_returns_raises_instead_of_truncating():
    backend = CassandraBackend(NoSession(), "ks", "chunks", EMBED)
    assert backend.search("q", 1000, In("team", [])) == []
    with pytest.raises(ValueError, match="1,000"):
        backend.search("q", 1001)


def test_set_metadata_updates_the_rows_found_with_plain_writes(monkeypatch):
    calls = []

    class Found:
        def __init__(self, row):
            self.row = row

        def one(self):
            return self.row

    # The rows as Cassandra holds them after the update: "a" kept its text, and "b", deleted between
    # the lookup and the update, is a row the update made, with metadata and terms but no text.
    rows = {
        "a": {"id": "a", "text": "leave", "metadata": '{"allowed_groups": ["hr"]}'},
        "b": {"id": "b", "text": None, "metadata": '{"allowed_groups": ["hr"]}'},
    }

    def run(self, cql, args, *, write=False):
        calls.append((cql, list(args), write))
        return [Found(rows.get(a[0])) for a in args] if cql.startswith("SELECT") else []

    monkeypatch.setattr(CassandraBackend, "_run", run)
    backend = CassandraBackend(NoSession(), "ks", "chunks", EMBED)
    hr = {"allowed_groups": ["hr"]}
    assert backend.set_metadata({"a": hr, "b": hr, "gone": {}}) == {"a"}
    lookup, update, read_back = calls
    assert lookup == ("SELECT id FROM ks.chunks WHERE id = ?", [("a",), ("b",), ("gone",)], False)
    # No lightweight transaction: its Paxos timestamp would not order with the plain writes of add and delete.
    hr_row = ('{"allowed_groups": ["hr"]}', {tag("allowed_groups", "hr")})
    assert update == (
        "UPDATE ks.chunks SET metadata = ?, wardowl_terms = ? WHERE id = ?",
        [(*hr_row, "a"), (*hr_row, "b")],
        True,
    )
    assert read_back == ("SELECT metadata, text FROM ks.chunks WHERE id = ?", [("a",), ("b",)], False)
    # A row whose metadata is not what was written is not counted either.
    rows["a"] = {"id": "a", "text": "leave", "metadata": '{"allowed_groups": ["eng"]}'}
    assert backend.set_metadata({"a": hr}) == frozenset()
    calls.clear()
    assert backend.delete(["gone", "a", "a"]) == {"a"}  # what the lookup just before found stored
    assert calls == [
        ("SELECT id FROM ks.chunks WHERE id = ?", [("a",), ("gone",)], False),
        ("DELETE FROM ks.chunks WHERE id = ?", [("a",), ("gone",)], True),
    ]


def test_a_row_whose_metadata_is_not_a_json_object_carries_no_permissions(monkeypatch):
    # As another tool could store it: JSON that is not an object, text that is not JSON, or nothing.
    odd = ["[]", '["allowed_groups"]', "1", '"x"', "null", "not json", "", None]
    rows = [{"id": f"d{i}", "text": "t", "metadata": stored, "score": 0.5} for i, stored in enumerate(odd)]
    rows.append({"id": "ok", "text": "t", "metadata": '{"allowed_groups": ["eng"]}', "score": 0.25})

    def run(self, cql, args, *, write=False):
        return [rows for _ in args]  # every ANN query finds every row

    monkeypatch.setattr(CassandraBackend, "_run", run)
    backend = CassandraBackend(NoSession(), "ks", "chunks", EMBED)
    assert [h.metadata for h in backend.search("q", 20)] == [{}] * len(odd) + [{"allowed_groups": ["eng"]}]
    # Denied and counted, with or without the re-check, where it failed the whole retrieval.
    for recheck in (True, False):
        retriever = PermissionedRetriever(backend, MetadataACLAuthorizer(), recheck=recheck)
        result = retriever.retrieve("q", Subject("ann", ["eng"]), k=20)
        assert [h.id for h in result.hits] == ["ok"] and result.violations == len(odd)
    # A filter applied here, past max_queries, leaves them out like any other row it does not match.
    wide = CassandraBackend(NoSession(), "ks", "chunks", EMBED, max_queries=1)
    assert [h.id for h in wide.search("q", 20, In("allowed_groups", ["eng", "hr"]))] == ["ok"]


# ---- a real Cassandra --------------------------------------------------------------------------

needs_cassandra = pytest.mark.skipif(not HOST, reason="set WARDOWL_TEST_CASSANDRA_HOST to run against Cassandra")
_TABLES: list[str] = []


@pytest.fixture(scope="module")
def session():
    cluster_module = pytest.importorskip("cassandra.cluster")
    cluster = cluster_module.Cluster([HOST])
    session = cluster.connect()
    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS wardowl_test "
        "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
    )
    yield session
    cluster.shutdown()


def _factory(session, *, vectors=False):
    def make(docs):
        # A new table for each corpus: rows deleted from the one before must not linger in its index.
        for old in _TABLES:
            session.execute(f"DROP TABLE IF EXISTS wardowl_test.{old}")
        _TABLES[:] = [f"chunks_{uuid.uuid4().hex[:12]}"]
        create_table(session, "wardowl_test", _TABLES[0], EMBED.dim)
        # The kit's deeply nested filters pass max_queries, so they also take the one-query path.
        backend = CassandraBackend(session, "wardowl_test", _TABLES[0], None if vectors else EMBED)
        backend.add(docs, [EMBED(d.text) for d in docs] if vectors else None)
        return backend

    return make


@needs_cassandra
def test_the_conformance_kit(session):
    # Cassandra's vector index (jvector) is approximate: a search can miss a matching row now and then,
    # even with k as large as the table. The kit still requires every hit to match the filter.
    check_backend(_factory(session), exact=False)


@needs_cassandra
def test_the_conformance_kit_with_query_vectors(session):
    check_backend(_factory(session, vectors=True), examples=8, query=Query(vector=EMBED(QUERY)), exact=False)


@needs_cassandra
def test_pre_filtering_and_changes_against_cassandra(session):
    backend = _factory(session)(
        [
            Document("eng", "engineering launch plan", {"allowed_groups": ["eng"]}),
            Document("hr", "pay bands for the launch", {"allowed_groups": ["hr"]}),
            Document("all", "launch date for everyone", {"allowed_groups": ["*"]}),
        ]
    )
    retriever = PermissionedRetriever(backend, MetadataACLAuthorizer(), strategy="prefilter")
    assert {h.id for h in retriever.retrieve("launch", Subject("ann", ["eng"]), k=3).hits} == {"eng", "all"}
    assert backend.set_metadata({"hr": {"allowed_groups": ["eng"]}, "missing": {"allowed_groups": ["eng"]}}) == {"hr"}
    assert {h.id for h in retriever.retrieve("launch", Subject("ann", ["eng"]), k=3).hits} == {"eng", "hr", "all"}
    assert backend.search("launch", 3, In("allowed_groups", ["eng"])) and len(backend.search("launch", 10)) == 3
    assert backend.delete(["all", "missing"]) == {"all"} and backend.delete(["all"]) == frozenset()
    assert {h.id for h in backend.search("launch", 10)} == {"eng", "hr"}


@needs_cassandra
def test_long_permission_values_against_cassandra(session):
    # Cassandra 5.0's SAI guardrail on string terms warns above 1 KiB and fails above 8 KiB by default.
    extra = len(tag("allowed_groups", "").encode())
    values = {
        "term of 1,025 bytes": "g" * (1025 - extra),
        "term of 8,192 bytes": "g" * (8192 - extra),
        "term of 8,193 bytes": "g" * (8193 - extra),
        "40,000 characters": "g" * 40_000,
    }
    outcomes = long_value_outcomes(_factory(session), values)
    assert outcomes == dict.fromkeys(values, "found"), "\n".join(f"{k}: {v}" for k, v in outcomes.items())
