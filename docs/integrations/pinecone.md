# Pinecone

[Pinecone](https://www.pinecone.io) is a managed vector database. `PineconeBackend` writes and
searches through the index's data plane API (version 2026-07), with the permission filter in the
query, so Pinecone applies it inside the search: pre-filtering is exact.

```bash
pip install "wardowl[pinecone]"
```

```python
import os

from wardowl import MetadataACLAuthorizer, PermissionedRetriever
from wardowl.backends.pinecone import PineconeBackend

backend = PineconeBackend(
    "my-index-abc123.svc.aped-1234.pinecone.io",  # the index's host, from the console
    os.environ["PINECONE_API_KEY"],
    embed,
    namespace="tenant-a",
)
backend.add(chunks)  # or backend.add(chunks, embeddings) with vectors you computed
retriever = PermissionedRetriever(backend, MetadataACLAuthorizer())
```

The index must be a vector index, created with a dimension and a metric (or, in API 2026-07, the
reserved `_values` field). Document indexes do not serve the vector API.

## How filtering works

Each record's metadata holds the chunk's id, its text, its metadata as JSON (returned exactly as
written), and a tagged term for every string or integer in its metadata (the field name, the
value's type and the value), hex-encoded, in the list `wardowl_terms`. A filter becomes `$in`
conditions on those terms joined with `$and` and `$or`. The terms keep `1` and `"1"` apart, as the
reference semantics do, and no metadata value can change the filter's structure.

## Production notes

- **Consistency:** serverless indexes are eventually consistent; a write usually shows within a
  few seconds. By default (`wait=30.0`) `add`, `delete` and `set_metadata` wait, up to that many
  seconds, until a search sees the change, and raise `TimeoutError` otherwise, so a revoked
  permission or a deleted chunk is out of searches when the call returns. `wait=None` returns at
  once; searches may then see the old permissions for a few seconds.
- **The API key** is sent only in the `Api-Key` header and never appears in errors or `repr`.
  Pass `client=httpx.Client(...)` for proxies or custom TLS.
- **Ids:** Pinecone record ids are printable ASCII of at most 512 characters; other chunk ids, and
  ids that start with `sha256-`, are stored under `sha256-` and their SHA-256, and returned as
  written. No two chunk ids share a record. `set_metadata` and `delete` first fetch the records
  (`GET /vectors/fetch`) and leave alone any record that holds another chunk id.
- **What writes return:** Pinecone's [update](https://docs.pinecone.io/reference/api/2025-10/data-plane/update)
  and [delete](https://docs.pinecone.io/reference/api/2025-10/data-plane/delete) by id answer with
  no ids. With `wait`, `set_metadata` returns the ids that the last search of its wait shows holding
  the new metadata; with `wait=None` it reads nothing back and returns None. `delete` returns the
  ids whose records the fetch before it showed holding them: a record that another writer deletes
  between the fetch and the delete is among them too, and one written moments before may not show
  in the fetch yet ([Checking that a change reached the chunks](../operations.md#checking-that-a-change-reached-the-chunks)).
- **Limits:** Pinecone allows 40 KB of metadata per record, which includes the chunk's text, and
  10,000 results per query: a search with `k` above 10,000 raises `ValueError` rather than return
  10,000 hits as if no more matched. Writes go in batches of 100, 8 requests at a time. The
  permission terms are hex-encoded, so each string or integer in the metadata takes twice the UTF-8
  bytes of its tagged term (field name, separator, type and value) there, on top of the JSON copy
  of the metadata: long permission values reach the 40 KB sooner than their length suggests
  ([operation limits](https://docs.pinecone.io/reference/api/database-limits/operation-limits)).
  CI's tests of values up to 40,000 characters run against the other stores, not Pinecone; the
  conformance kit stores values of 1,000 characters.
- **What CI tests:** the filter translation, the requests and the handling of replies, against a
  scripted stand-in for the API, on every change. The tests against Pinecone's service, the
  conformance kit among them, run on `main` and by hand only when the `PINECONE_API_KEY` secret is
  set, and are skipped without it. As of November 2026 the repository has no such secret, so they do not run in
  CI.
- **Translating filters yourself:** `filter_to_pinecone` raises `NothingMatches` for a filter that
  can match nothing, since Pinecone reads a missing filter as "match everything".
- **Namespaces** keep tenants or corpora apart; `clear()` removes every chunk in the backend's
  namespace.
