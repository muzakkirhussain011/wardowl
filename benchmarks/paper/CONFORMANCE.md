# The conformance campaign

The paper claims a differential conformance-testing method for permission filters across 14 vector
stores and 7 authorization engines. Its fault table records what review, the security audit and the
acceptance runs found during development; it credits nothing to the conformance kit. This campaign
produces the missing evidence: what `wardowl.testing` finds against current releases, run the same
way for every target, with fixed versions, seeds and counts, and with every outcome kept, a target
where the kit finds nothing included.

| File | What it is |
|---|---|
| [`conformance_campaign.py`](conformance_campaign.py) | The driver: runs the kit per target, seed and variant, writes `campaign.jsonl`, summarizes, checks |
| [`../../.github/workflows/paper-conformance.yml`](../../.github/workflows/paper-conformance.yml) | Starts the servers and runs the driver in GitHub Actions, by hand only |

## What it tests

### The kit, unchanged

For a store, `check_backend` fills a fresh store with each generated corpus and compares it with the
reference semantics, `wardowl.filters.matches`: searches without and with a filter (no document
outside the expected set, all of them when k allows, at most k, no duplicates, finite scores best
first, text and metadata exactly as stored), `asearch` against `search`, `set_metadata`, and
retrieval through `PermissionedRetriever` with `MetadataACLAuthorizer`, pre-filtered and
post-filtered, through `retrieve` and `aretrieve`, against an oracle of who may read what written
without the library's filter code. It stops at the first disagreement and raises `ConformanceError`.

For an engine, `check_authorizer` checks that `check` gives one boolean per chunk, that a chunk's
answer does not depend on the rest of the batch or its order, that the async methods agree with the
sync ones, and, when the engine offers a filter, that `check` agrees with `matches(filter, metadata)`
on every chunk. That last check is the engine's filter-versus-check disagreement, which pre-filtered
and post-filtered retrieval would show as different results. It is a consistency check, not a check
that the policy is right: an engine that lets everyone read everything passes.

### What a variant changes

A variant changes only what the kit generates, by replacing, for the length of one call, the pools
and the filter generator inside `wardowl.testing` (`_STRINGS`, `_INTS`, `_FIELDS`, `_ODD_FIELDS`,
`_USERS`, `_GROUPS`, `random_filter`) and putting the originals back afterwards. The checks, the
reference semantics and the oracle are the kit's, untouched. The `default` variant is the kit exactly
as it ships; every result can be replayed from its seed.

Stores:

| Variant | What the kit generates |
|---|---|
| `default` | The kit unchanged: corpora of up to 20 documents, four filters each, nested two levels deep |
| `large-corpus` | Corpora of up to 150 documents, six filters each |
| `deep-filters` | And and Or nested three to six levels deep, one to four clauses each |
| `wide-or` | In over 100 and over 1,000 values, Or over 100 and over 1,000 one-value clauses, and such an In under an And; half on `allowed_groups` |
| `long-strings` | Values, users and groups of 256, 1,024 and 8,192 characters that differ only in the last one, and 3,001 two-byte letters |
| `huge-strings` | Values of 32,766 and 40,000 characters, and of 40,001 bytes in UTF-8 (past Lucene's longest term) |
| `unicode-case` | Values, users and groups equal only under case folding, NFC or NFKC, trimming or zero-width removal: sharp s and ss, the fi ligature, fullwidth letters, the Kelvin and angstrom signs, dotted and dotless i, Hangul composed and as jamo, combining marks in either order |
| `numeric-strings` | `"1"`, `"01"`, `"1.0"`, `"1e0"`, `" 1"`, Arabic-Indic, fullwidth and superscript digits, `"true"`, `"null"`, and integers at the 32-, 53- and 64-bit edges (2^53 and 2^53 + 1) |
| `odd-fields` | Field names with dots, quotes, backslashes, slashes, colons, spaces and `$`, case variants, non-ASCII names composed and decomposed, and the stores' own names (`metadata`, `content`, `embedding`, `_id`, `wardowl_terms`) |

Engines (subjects and chunks; each chunk's `doc_id` is its own id):

| Variant | What is generated |
|---|---|
| `default` | Exactly the 12 subjects and 30 chunks `check_authorizer(authorizer, seed=seed)` draws by itself |
| `many-groups` | 3 subjects in 1,000 more groups each, 10 chunks, some shared with one of those groups |
| `many-hits` | 4 subjects, 300 chunks: past every batch size (Keto 10, OpenFGA 50, Cerbos 50, SpiceDB 100) |
| `unicode-case` | User and group names equal only under case folding or Unicode normalisation |
| `numeric-strings` | Numeric-looking user and group names |
| `long-ids` | User and group names of 64 to 4,096 characters, document ids up to 1,100 characters longer |
| `scalar-fields` | Permission fields holding one string, an integer, mixed or nested lists, null, true or an object instead of a list of strings, and a tenant held in a list or missing. The documentation asks for lists of strings, so a finding here is a documented limit unless the adapter claims otherwise |

### Targets

| Group (job) | Target | Configuration |
|---|---|---|
| sql-and-kv | `pgvector` | `pgvector/pgvector:pg17`; exact search (no HNSW index), one table truncated per corpus |
| | `redis` | `redis:8.10.2-alpine`; a FLAT (exact) index per corpus |
| | `cassandra` | `cassandra:5.0.9`; sound-only, as CI: its vector index is approximate even on small corpora |
| search-engines | `elasticsearch` | `elasticsearch:9.5.5`; an index per corpus |
| | `opensearch` | `opensearch:3.9.0`; an index per corpus |
| | `vespa` | `vespa:8.763.13`, the application in `examples/vespa`; exact search (`approximate=False`) |
| vector-dbs | `qdrant` | `qdrant:v1.19.2`, the server; a collection per corpus |
| | `milvus` | `milvus:v3.0.2` standalone; a collection per corpus |
| | `weaviate` | `weaviate:1.39.12`; a collection per corpus |
| | `mongodb` | `mongodb-atlas-local:8.0.30`; one collection and vector index, emptied between corpora |
| embedded | `memory` | `InMemoryBackend`, the reference: the positive control |
| | `chroma`, `lancedb`, `faiss` | In process; a collection, table or index per corpus |
| cloud | `pinecone` | The service, CI's index `wardowl-ci`, a namespace per corpus; at most 4 corpora per seed (2 for the stress variants) of at most 40 documents, since every write is waited for |
| engines | `metadata-acl` | `MetadataACLAuthorizer`: the positive control |
| | `opa` | OPA 1.21.2 with `examples/opa/wardowl.rego` (metadata ACLs; `filter_path` returns a filter) |
| | `opa-tenant` | `acceptance/policies/opa/documents.rego` uploaded under a run's own package, with every chunk's sharing as OPA data; its filter is an In on `doc_id` |
| | `openfga` | `openfga:v1.22.0`, the model of wardowl's tests (`user`, `user:*` and `group#member` viewers), a store per run; groups as contextual tuples; `HIGHER_CONSISTENCY`; filter from ListObjects |
| | `openfga-tenant` | `acceptance/policies/openfga/model.json` (viewer = reader and member of the document's tenant) |
| | `spicedb` | `spicedb:v1.56.2`, the schema of wardowl's tests, groups checked as subject sets, fully consistent; filter from LookupResources |
| | `spicedb-tenant` | `acceptance/policies/spicedb/schema.zed` (view = reader & tenant->member), memberships stored in SpiceDB |
| | `cerbos` | `cerbos:0.56.0` with `examples/cerbos/policies` (metadata ACLs); filter from the query plan |
| | `cerbos-tenant` | A second Cerbos with `acceptance/policies/cerbos` (tenant equality and sharing) |
| | `keto` | `keto:v26.2.0` with `acceptance/policies/keto`, groups checked as subject sets; no filter |
| | `cedar`, `cedar-tenant` | In process: the ACL policy of wardowl's tests, and `acceptance/policies/cedar/documents.cedar`; no filter |
| | `casbin`, `casbin-tenant` | In process: the RBAC model of wardowl's tests, and `acceptance/policies/casbin/model.conf` (a domain per tenant); no filter |

The images are ci.yml's test job's, started with its options; the run records each container's image
id and registry digest, and the version each server reports about itself where it reports one.
Relationship engines get a tuple for every grant in the chunks' metadata (and, for the tenant
profiles, for every subject's tenant and memberships); a tuple the engine refuses (an id outside its
syntax) is counted in the record, not written, so that engine never grants it.

Keto, Cedar and Casbin offer no filter, so for them the kit checks only well-formed,
batch-independent and async-consistent answers. For OPA, OpenFGA, SpiceDB and Cerbos it also checks
the filter against `check`, which is the measurement of contribution C3.

### Outcomes

Every (target, seed, variant) is one record:

| Outcome | Meaning |
|---|---|
| `pass` | The kit found nothing |
| `conformance-violation` | The kit raised `ConformanceError`: its first disagreement in that run, with the kind of disagreement and a reproducer |
| `refused-ValueError` | A `ValueError` raised inside one of wardowl's adapters (not the harness): the store or engine refused the data or a filter it cannot express. Refusing is allowed; answering wrongly is not |
| `error` | Anything else: a server error, a crash, a client library's own `ValueError`, a time-out (`CallTimeout`), an engine's `AuthorizationError` (fail-closed) |

Violation kinds, the first one being the record's `kind`: `leak` (a filtered search returned a
document the filter does not match), `retrieval-leak` (retrieval returned a chunk the oracle denies),
`recheck-violation`, `filter-check-disagree` (an engine's filter and check differ), `metadata-changed`
and `text-changed` (what a re-check reads was altered), `drivers-disagree`, `async-mismatch`,
`async-refusal`, `batch-dependent`, `duplicates`, `k-exceeded`, `malformed-answer`, `order`,
`scores`, and `missed` (fewer matching documents than k allows). A kind prefixed `after-set-metadata:`
happened after the metadata was replaced. The first six are wrong answers; the summary lists them
apart.

When an exact check fails only by `missed`, the same seed and variant run again sound-only
(`exact=False`, mode `sound-retry`), so that a short answer from an approximate index does not hide
a wrong one behind it. In `odd-fields`, every new name may be refused like the kit's own odd names;
the record counts such refusals (`filter_refusals`).

Engines are checked one subject at a time, so one subject's failure hides no other's; a run takes its
worst subject's outcome (violation, then error, then refusal) and records how many subjects had each.

### What it cannot show

- That a policy is right: `check_authorizer` checks consistency only.
- More than the first disagreement of a store run: the kit stops there, so other faults of the same
  seed and variant stay hidden until that one is fixed or the seed is changed.
- Recall of approximate indexes beyond small corpora: Cassandra is checked sound-only, and a
  `missed` in exact mode on another store may be its index; the paper measures recall separately.
- Seeds a time budget left out: the summary says how many runs did not start.

## Running it

Actions > paper-conformance > Run workflow, then pick the branch to test. GitHub offers that button
(and `gh workflow run`) only for a workflow whose file is on the default branch, so the workflow
file must reach `main` first; after that, any branch's version of the driver can be run from the
branch picker, for example `gh workflow run paper-conformance.yml --ref paper/conformance-campaign`.

| Input | Default | Meaning |
|---|---|---|
| `seeds` | 20 | Seeds 0 to N-1 for every target and variant |
| `examples` | 10 | Corpora per seed for the store `default` variant; the stress variants run a third (at least 2). The kit's own default is 25 |
| `variants` | `all` | Or a comma-separated list, for example `default,wide-or` |
| `budget_minutes` | 90 | Time per target; each target also gets at most a fair share of what is left of 320 minutes in its job |
| `pinecone` | true | Run the Pinecone job (it needs the `PINECONE_API_KEY` secret, and records the target as skipped without it) |

Six jobs run in parallel (sql-and-kv, search-engines, vector-dbs, embedded, engines, and cloud for
Pinecone), then `summary` merges them. Seeds are the outer loop and variants the inner one, so a run
cut short by its budget still covers every variant for the seeds it reached.

To replay one record, start the same server as the workflow does (its `docker run` line and the
environment variables at the top of the job) and run the `replay` command the record carries, for
example:

```
python benchmarks/paper/conformance_campaign.py run --targets qdrant --seed-list 7 --variants wide-or \
  --examples 10 --stress-examples 3 --large-documents 150
```

## Reading the results

Each job uploads `conformance-<group>`: `campaign.jsonl`, `summary.md` and the servers' logs
(`logs/`). The `summary` job uploads `conformance-summary`: every group's records in one
`campaign.jsonl` and one `summary.md`, which is also the run's job summary.

`campaign.jsonl` holds one JSON object per line, with `type`:

- `target-start`: the run (wardowl version, commit, workflow run id, Python), the configuration,
  seeds, variants and settings;
- `versions`: the container's image, image id and digests, the version the server reports, and the
  Python client packages;
- `result`: one (seed, variant): `outcome`, `mode` (`exact`, `sound`, `sound-retry` or `consistency`),
  `duration_s`, `kind` and `kinds` with a `reproducer` (the problems, the filter, k, expected and
  returned ids, the documents) for a violation, `error_class`, `raised_in`, `message`, `where` and
  `cause` otherwise, `subjects` and `subject` for an engine, `case` (tuples written and refused), and
  `replay`;
- `target-end`: `status` (`ok`, `skipped`, `setup-error` or `driver-error`), runs planned, done and not
  started, and the outcome counts;
- `crash`: the driver process stopped (the workflow writes this).

Messages are cut at 4,000 characters, strings in reproducers at 300 and lists at 40 items; the seed
and the replay command reproduce everything exactly. Values of environment variables named like
secrets are replaced by `***`.

`summary.md` starts with the controls (`memory` and `metadata-acl` must pass every run; if one does
not, the harness is at fault and nothing else should be read), then the violations, wrong answers
first, then one row per target and a section per target with a row per variant and the first run of
each kind of failure, with its replay command.

A job turns red only when a target could not run to its end (a setup error, a driver fault or a
crash); violations, refusals and errors inside runs are results and leave it green.

## From a finding to a row in the fault table

1. **Check the controls.** If `memory` or `metadata-acl` failed, fix the harness first.
2. **Reproduce.** Run the record's `replay` command against the same image (the record has its
   digest) and the same wardowl commit. A finding that does not reproduce is reported as flaky, with
   its counts, and not entered.
3. **Minimise.** Cut the reproducer to the fewest documents, the smallest filter and the smallest k
   that still fail. Then reproduce the minimal case against the store's or engine's own API, without
   wardowl (the raw query or request the adapter sends), to tell the store's semantics from a fault in
   wardowl's translation.
4. **Classify.** Give it the table's effect (Leak, Leak\*, Leak†, Recall, Stale, Wrong rows, Avail.)
   and say whether it is the store's or engine's behaviour or an adapter fault (*None (adapter)* in
   the Upstream column).
5. **Confirm against the documentation** of the version run. Behaviour the documentation states is a
   semantic gap; behaviour that contradicts it is a bug. Cite the page.
6. **Report it before publication**: upstream for the store's or engine's behaviour (an issue with
   the minimal case, the version and the image digest), or as a wardowl issue and fix for an adapter
   fault. Put the link in the Upstream column.
7. **Enter the row** with *Found by* "Kit (campaign)", and keep the evidence in the paper
   repository's `evidence/`: the workflow run URL, the commit, `campaign.jsonl`, `summary.md` and the
   minimal reproducer.

Negative results go into the paper too: for every target, the runs, seeds, variants and versions in
which the kit found nothing, and the refusals and errors it met, are part of the result, not noise to
drop.
