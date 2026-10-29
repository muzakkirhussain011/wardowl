# Pre-registration: experiments X4 (engine filters against engine checks) and X7 (revocation and faults)

- **Date:** 2026-10-29.
- **Commit:** this file is committed alone, on branch `paper/x4-x7` (from `fix/engine-limits` at
  e7776f0: wardowl 2.1.0, PR #166 and the `UnsupportedSubject` refusals of OpenFGA and SpiceDB), with
  the message `bench: pre-register the X4 and X7 experiments`. Nothing else is in that commit.
- **When:** before any X4 or X7 harness code was written and before any X4 or X7 result existed.
- **Where it runs:** GitHub Actions only, in the workflow `.github/workflows/paper-x4-x7.yml`
  (hosted `ubuntu-latest` runners: 4 vCPUs, 16 GB, 6 hours per job). A **smoke** configuration of the
  same workflow (one seed, small worlds, short phases) runs first to find faults in the harness. Its
  numbers are never analysed for the hypotheses below and are not reported as results; only the
  **full** configuration described here is. A final job publishes the reports, the raw records and
  the tail of every job's log to the branch `results/x4-x7`, under `<run id>-<run attempt>/`.
- **Paper context:** section "Do Authorization Engines' Filters Agree With Their Checks?"
  (contribution C3), and threat model items (iii) (authorizer outages, slow and malformed answers)
  and (v) (revocation). Proposition 1 makes security depend on the check API alone; a disagreement
  between the filter API and the check API is a translation fault only when both read one revision.

## Systems

| Component | Version or image | Notes |
|---|---|---|
| wardowl | this branch (`fix/engine-limits` e7776f0 plus the harness), installed with `pip install -e .` | the adapters as shipped: `OPAAuthorizer`, `OpenFGAAuthorizer`, `SpiceDBAuthorizer`, `CerbosAuthorizer`, `CachingAuthorizer`, `RedisCache`, `CircuitBreaker`, `PermissionedRetriever` |
| OPA | 1.21.2 (binary from `open-policy-agent/setup-opa`) | started by the harness |
| OpenFGA | `openfga/openfga:v1.22.0` | Postgres datastore, server defaults: ListObjects result limit 1,000 and deadline 3 s, BatchCheck at most 50 checks, no caches; one extra server with the check-query cache (TTL 10 s) for X7 |
| SpiceDB | `authzed/spicedb:v1.56.2` | Postgres datastore, HTTP gateway, server defaults (revision quantization 5 s) |
| Cerbos | `ghcr.io/cerbos/cerbos:0.56.0` | disk policies; X7's policy-change path watches the directory for changes |
| Postgres (engine datastore; pgvector store) | `pgvector/pgvector:pg17` | |
| Qdrant | `qdrant/qdrant:v1.19.2` | |
| Redis (shared cache) | `redis:8.10.2-alpine` | |
| FAISS | faiss-cpu from `uv.lock` | flat inner-product index (exact search) |

These are the conformance campaign's images and versions. One deviation from the campaign, stated in
advance: OpenFGA and SpiceDB use a Postgres datastore instead of their in-memory one, so that a
restarted engine keeps its data (X7) and timings reflect a production datastore (X4).

## X4: do authorization engines' filters agree with their checks?

**Question.** For OPA, OpenFGA, SpiceDB and Cerbos, does the filter wardowl compiles from the
engine's filter API (`filter_for`) admit exactly the chunks the engine's check API (`check`) allows?
When they differ, is it a translation fault, revision skew, or truncation?

### The world (X4a, X4b)

Generated per seed (seeds 0 to 4), with ids that carry the seed:

- **Tenants:** 3. **Users:** 40 per tenant, each with a clearance 0 to 3 (uniform) and 0 to 4 direct
  groups drawn from all groups.
- **Groups:** 60. Group j > 0 has 0, 1 or 2 parent groups (probabilities 0.5, 0.35, 0.15) among
  groups with a smaller index; a parent that would make nesting deeper than 4 levels is not added. A
  member of a group is a member of its parents.
- **Folders:** 80. Folder j > 0 has a parent folder with probability 0.7 among earlier folders, at
  most 4 levels deep. Each folder grants view to 0 to 2 users and 0 to 2 groups, and to everyone with
  probability 0.02. A folder's grant applies to the documents under it and under its descendants.
- **Documents:** 1,500. Tenant uniform; a folder with probability 0.6; an owner (a user of the
  document's tenant with probability 0.9, else any user); 0 to 3 direct readers and 0 to 2 reader
  groups; everyone-readable with probability 0.03; classification `L0` to `L3` (uniform); with
  probability 0.1, 1 or 2 banned users (chosen among the users who could otherwise read it, when there
  are any); with probability 0.03, one banned group.
- **The model.** A user may view a document of their own tenant that they own, read directly, read
  through a group (nested), read because it is everyone-readable, or read through a folder (nested),
  unless they are banned from it directly or through a group. Engines that see attributes (OPA,
  Cerbos) add: the document's classification is at most the user's clearance.

### Profiles (X4a)

Every profile is the model above written natively in one engine, measured through wardowl's adapter:

| Profile | Filter route (`filter_for`) | Check route | What the engine holds |
|---|---|---|---|
| `openfga` | ListObjects, non-streaming; `HIGHER_CONSISTENCY` | BatchCheck | everything as tuples; users, groups (nested through `group#member`), tenants, folders (`viewer from parent`), wildcard `user:*`, `viewer: (reader and member from tenant) but not banned`; `contextual_groups=False` |
| `openfga-ctx` | as `openfga` | as `openfga` | as `openfga`, but each user's direct groups are sent as contextual tuples (wardowl's default) and not stored |
| `spicedb` | LookupResources | CheckBulkPermissions | the same model as a SpiceDB schema (`view = (read & tenant->member) - banned`); both calls at `atExactSnapshot` of the token of the last write |
| `opa-acl-doc` | a filter document returned by the policy (`filter_path`) | the policy's `decisions` | ACL lists in chunk metadata (`allowed_users`, `allowed_groups` with `"*"`), tenant, classification, folder; nested groups and folders in OPA data; no bans (the filter language has no negation) |
| `opa-rel-doc` | a filter document | `decisions` | scalar columns in chunk metadata (`doc_id`, `tenant`, `owner`, `folder`, `classification`); each document's sharing, nested groups and folders in OPA data; no bans |
| `opa-rel-pe` | OPA's Compile API (`POST /v1/compile/<package>/allow`, UCAST target), translated by the harness: `eq` and `in` on a column to `In`, `and` and `or` to `And` and `Or`, anything else to no filter | `decisions` | as `opa-rel-doc` |
| `cerbos` | PlanResources, `plan_to_filter` | CheckResources | ACL lists, tenant and classification as resource attributes; the principal carries its tenant, its readable classification labels and its groups already flattened (as an identity provider sends them); no folders, no bans |

Stress profiles, run on the same worlds:

| Profile | Change |
|---|---|
| `cerbos-drift`, `opa-acl-doc-drift` | each document independently with probability 0.1 stores every ACL list field holding exactly one value as that value (a scalar), the slip an ingestion pipeline makes |
| `cerbos-excl` | bans as an `EFFECT_DENY` rule (`request.principal.id in request.resource.attr.banned_users`); every document carries `banned_users` |
| `opa-rel-pe-excl` | bans in OPA data and `not input.doc.doc_id in banned_docs` in the rule compiled |

Controls (in process): `control-oracle`, whose filter and check are both the oracle (no disagreement
may be reported), and `control-planted`, whose filter drops 2% of each subject's readable documents
(at least one) and adds 2% of the unreadable ones (at least one): the harness must report exactly
those counts.

**Oracle.** An independent Python evaluation of the model on the world as the profile encodes it
(folders and bans only where the profile has them; classification only for OPA and Cerbos), written
without wardowl's filter code. For the drift profiles the oracle is the model as intended (a scalar
counts as a one-element list).

### X4a: disagreement at one revision

For each seed, profile and user (120 per seed): `filter_for(user)`, then `check(user, all 1,500
documents)`, both at one revision (SpiceDB: the snapshot token; OpenFGA: no write between setup and
measurement, `HIGHER_CONSISTENCY`; OPA and Cerbos: no change to policy or data). For each (user,
document) pair: `f` = the filter admits the document's metadata (`wardowl.filters.matches`), `c` = the
check allows, `o` = the oracle allows. A **false admit** is `f` and not `c`; a **false denial** is `c`
and not `f`. Both are also counted against the oracle (`f` against `o`, `c` against `o`). Every
disagreeing pair is asked again twice (filter and check, same revision): it **reproduces** when both
repetitions disagree the same way.

### X4b: the same, unpinned, under a concurrent writer

For each seed, 40 users (seeded), measured in two phases: **quiet** (no writes) and **writer** (one
writer thread commits 20 writes per second; each toggles one fact: a direct reader of a document
(40%), a ban (20%), a folder viewer (20%), a direct group membership (20%); with probability 0.5 the
fact concerns the user being measured; OPA's writer toggles folder viewers only, its other facts
being chunk metadata or the subject's own groups). Within a phase, each user is measured once under
every condition of the engine, in a seeded random order:

| Engine | Quiet | Writer |
|---|---|---|
| OpenFGA (`openfga` profile) | `quiet-hc` | `writer-hc` (`HIGHER_CONSISTENCY`), `writer-ml` (`MINIMIZE_LATENCY`) |
| SpiceDB | `quiet-ml` | `writer-pinned` (both calls `atExactSnapshot` of the writer's latest token), `writer-fc` (`fullyConsistent`), `writer-ml` (`minimizeLatency`, wardowl's default) |
| OPA (`opa-acl-doc`) | `quiet` | `writer` |

Each write is logged with its start and end times. A disagreeing pair of an unpinned trial is
**skew-explained** when the oracle's answer for that pair changes across the world states between the
last write that ended before `t_filter_start - S` and the last write that started before
`t_check_end`, where S is the engine's stated staleness: 0 for `HIGHER_CONSISTENCY`,
`fullyConsistent` and OPA, 10 s for OpenFGA `MINIMIZE_LATENCY` (the check-query cache TTL, should a
cache apply), 5.5 s for SpiceDB `minimizeLatency` (5-s quantization plus 10%). A pinned trial is
compared with the oracle at the pinned write.

### X4c: truncation of list APIs

One corpus of 100,000 documents per job; per seed, new subjects with new grants, new vectors and new
queries. For each **structure** and readable-set size **N = 10, 100, 999, 1,000, 1,001, 3,000,
10,000, 30,000, 100,000**, a subject reads exactly N documents (seeded):

| Structure | Model | How the subject reads N documents |
|---|---|---|
| `simple-direct` | `document: viewer: [user]` (OpenFGA store of its own; SpiceDB definitions of their own) | N direct viewer grants |
| `full-direct` | the X4 model (tenant intersection, ban exclusion) | N direct reader grants, all documents in the subject's tenant |
| `full-folder` | the X4 model | N div 10 folders of 10 documents each (folders are a seeded partition), plus N mod 10 direct grants |

Engines: OpenFGA and SpiceDB; OPA (`opa-rel-doc` and `opa-rel-pe`, sharing N documents to the
subject) for correctness and latency only. Measured per (seed, structure, N):

- **Engine level** (the raw API, 3 repetitions): OpenFGA non-streaming ListObjects and streamed
  ListObjects (`streamed-list-objects`, which wardowl does not use) and SpiceDB LookupResources with
  `optionalLimit` 1,000 (as wardowl sends it) and without a limit: objects returned, elapsed time,
  HTTP status, and every field of the answer that could signal truncation (top-level keys, cursors,
  error lines).
- **wardowl level:** `filter_for` with the adapter's default timeout (2 s) and with 10 s: a filter of
  N values (exact), a filter of fewer than N values (**silent truncation**), no filter (wardowl's
  limit or deadline rule), or `AuthorizationError` (timeout; retrieval fails closed).
- **Retrieval:** 30 queries per (seed, structure, N), `PermissionedRetriever` with wardowl's defaults
  (k = 10, overfetch 4, `max_candidates` 1,000, re-check on, default timeout) over FAISS flat (64
  dimensions; vectors and queries from 200 seeded cluster centres, normalized centre plus Gaussian
  noise of norm about 0.5). **Permission-recall@10** against exact search over the readable set (tie
  epsilon 1e-4), the strategy used, `complete`, candidates examined and errors.

### X4d: latency

At every X4c level (OpenFGA, SpiceDB, OPA) and on the X4a worlds (every engine and profile):
`filter_for` and `check` of a batch of 10 documents, uncached (3 and 5 repetitions) and through
`CachingAuthorizer` (a miss, then 10 hits). Per-hit check latency is the batch time over 10.

### Hypotheses, predictions and rules

**X4-H1, agreement at one revision.** For each of `openfga`, `openfga-ctx`, `spicedb`,
`opa-acl-doc`, `opa-rel-doc`, `opa-rel-pe` and `cerbos`: no disagreement reproduces. **Confirmed**
when no pair disagrees reproducibly, at least 500 (seed, user) clusters received a filter, and guards
G1 and G2 hold; the subject-level one-sided 95% upper bound `1 - 0.05^(1/n)` is reported.
**Falsified** when at least one disagreement reproduces. Inconclusive otherwise (disagreements that
do not reproduce, fewer than 500 clusters with a filter, a guard failing).

**X4-H2, shape drift.** `cerbos-drift`: at least one disagreement occurs, every disagreement is a
false admit, and every disagreeing document holds a scalar-valued ACL field (CEL's `in` and
`hasIntersection` need lists; wardowl's `In` matches a scalar as itself). **Falsified** when a false
denial occurs, when no disagreement occurs, or when a disagreeing document holds no scalar ACL field.
`opa-acl-doc-drift` (its policy reads one value or a list): judged as X4-H1.

**X4-H3, negation is never dropped.** `cerbos-excl` and `opa-rel-pe-excl`: no false admit at all.
Predicted further: `cerbos-excl` returns no filter for any user (the plan keeps a `not`), and
`opa-rel-pe-excl` returns a filter only to users with no ban in their scope (partial evaluation
removes `x in []`). **Falsified** by any false admit; the availability predictions are judged
separately (confirmed or falsified by the share of users with a filter, 0 and the share without bans
respectively).

**X4-H4, revision skew.**
(a) SpiceDB `writer-pinned`: no pair disagrees (filter, check and oracle at the pinned write).
Falsified by one disagreement that reproduces at the same token.
(b) Every unpinned writer condition (`writer-hc`, `writer-ml` for OpenFGA; `writer-fc`, `writer-ml`
for SpiceDB; OPA `writer`): the share of trials with a disagreement is above 0 with its interval's
lower end above 0, and at least 95% of the disagreeing pairs (pooled per condition) are
skew-explained. Confirmed when both hold; falsified when the explained share is below 90% with at
least 20 disagreeing pairs; inconclusive with fewer than 20 disagreeing pairs or in between.
(c) Quiet conditions: no reproducible disagreement (a replication of X4-H1).
(d) Paired by (seed, user): the trial disagreement rate of SpiceDB `writer-ml` minus `writer-pinned`
is above 0, its interval excluding 0. Falsified when the interval lies at or below 0.

**X4-H5, truncation and its detection.**
(a) OpenFGA non-streaming ListObjects, `simple-direct`: returns exactly min(N, 1,000) objects when it
answers in under 2.5 s, and its answer has no top-level key but `objects` (no truncation signal).
Falsified by a count that differs, or by a key that signals truncation.
(b) SpiceDB LookupResources with `optionalLimit` 1,000, `simple-direct`: returns exactly min(N, 1,000)
results. Falsified by a count that differs.
(c) **wardowl never truncates silently:** over both engines, every structure, N, seed and timeout,
`filter_for` never returns a filter with fewer values than N. Confirmed with zero; falsified by one.
(d) wardowl returns a filter of exactly N values for every N <= 999 whose list call ended within the
timeout and in under 3 s, and no filter for every N >= 1,000. Falsified by a counterexample.
Exploratory: the N and structure at which a list call first exceeds 2 s and 3 s, the share of calls
that fail closed on wardowl's default 2-s timeout, streamed ListObjects counts against N, and
unlimited LookupResources times.

**X4-H6, recall after the fallback** (per engine and structure, FAISS exact, k = 10).
(a) N <= 999: recall is 1 for every query. (b) N in {1,000, 1,001} (pooled): mean recall below 1 with
its interval's upper end below 1 (about 1% of the corpus is readable, so the post-filter's 1,000
candidates hold about 10 readable chunks). (c) N >= 10,000: mean recall at least 0.99. (d) No result
with recall below 1 reports `complete=True`. Falsified by a query with recall below 1 in (a), by a
false-complete result in (d), by an interval upper end at 1 or above in (b) or by a mean below 0.97
in (c). A level where more than 5% of retrievals fail is inconclusive for (a) to (c); failures are
reported as availability.

**X4-H7, caching.** For OpenFGA, SpiceDB, OPA (`opa-rel-doc`, `opa-rel-pe`) and Cerbos, at every
level measured: the median ratio of uncached to cached latency is at least 10, with the interval's
lower end at least 5, for `filter_for` and for `check` per hit. Falsified when an interval's upper
end is below 5. Exploratory: uncached latency against N (log-log slope).

### Guards

- **G1 (controls):** `control-oracle` reports no disagreement and `control-planted` reports exactly
  the planted false admits and false denials for every user. If not, every X4 verdict is
  inconclusive.
- **G2 (encoding):** in X4a and the quiet conditions, a well-formed profile's `check` agrees with the
  oracle on at least 99.9% of pairs. If not, that profile's X4-H1 is inconclusive (the encoding or
  the oracle is at fault, not the filter), and the disagreement with the oracle is reported.

## X7: revocation and faults

### X7a: revocation latency end to end

**Paths** (a path is a source of truth and a way to revoke in it):

| Path | Authorizer and store | Revocation | Stated engine staleness S |
|---|---|---|---|
| `acl-pgvector` | `MetadataACLAuthorizer`, pgvector (exact search) | `set_metadata` removes the user | 0 |
| `acl-qdrant` | `MetadataACLAuthorizer`, Qdrant | `set_metadata` removes the user | 0 |
| `openfga` | `OpenFGAAuthorizer` (`HIGHER_CONSISTENCY`), FAISS | delete the reader tuple | 0 |
| `openfga-cached-hc` | the same, against the OpenFGA server with the check-query cache | delete the tuple | 0 (`HIGHER_CONSISTENCY` skips the cache) |
| `openfga-cached-ml` | the same, `MINIMIZE_LATENCY` | delete the tuple | 10 s (cache TTL) |
| `spicedb-fc` | `SpiceDBAuthorizer`, `fullyConsistent`, FAISS | delete the relationship | 0 |
| `spicedb-ml` | `SpiceDBAuthorizer`, `minimizeLatency` (wardowl's default), FAISS | delete the relationship | 5.5 s |
| `opa-data` | `OPAAuthorizer` (filter document), FAISS | replace the document's sharing in OPA data | 0 |
| `opa-policy` | `OPAAuthorizer`, FAISS | upload a new policy module that denies the user | 0 |
| `cerbos-policy` | `CerbosAuthorizer`, FAISS | rewrite the policy file so the rule no longer names the user's role; Cerbos reloads it | none stated |

**Cache conditions:** `nocache` (no `CachingAuthorizer`; its ttl must be positive, so ttl 0 means
none), `ttl5`, `ttl30`, `ttl30-inv` (`invalidate(user)` right after the revocation returns), and
`ttl30-shared-inv` (two `CachingAuthorizer` replicas sharing `RedisCache`, `local_ttl` 1 s: replica A
invalidates, replica B is polled).

**Trial.** Each trial has a user of its own who reads one target chunk only through the grant that
will be revoked, plus 10 to 20 background chunks. The query is the target's own vector with small
noise, so the target ranks first while readable; k = 5. The cache is warmed by one retrieval (the
trial is valid only if the target is returned), the revocation is sent at once (t0 = just before the
write), and retrieval is then polled every 50 ms. **Time to effect** is the start of the first of 3
consecutive polls without the target, minus t0. Polling stops at B + 15 s. A target that reappears
after an absent poll is counted as a flap.

**Stated bound B** = ttl (0 without a cache, 0 after `invalidate`, `local_ttl` = 1 s for the shared
replica) + S. For the metadata paths B = 0 in every condition: `CachingAuthorizer` keys each decision
by the chunk's metadata, and the filter is applied by the store to the metadata it holds now.

**Design:** 5 seeds, 8 trials per (seed, path, condition): 40 trials per cell.

### X7b: faults

**Engines:** OpenFGA, SpiceDB, OPA and Cerbos (each with a small X4 world and FAISS), and the stores
pgvector and Qdrant (with `MetadataACLAuthorizer`). Faults are injected by stopping the server
(`docker kill`, then `docker start`; for OPA, the process, restarted with its policy and data files)
or by a proxy the harness runs between wardowl and the server (HTTP for engines and Qdrant, TCP for
Postgres):

| Fault | What happens |
|---|---|
| `down` | the server is killed, then started again |
| `refuse` | the proxy closes its listener and every connection: connections are refused |
| `blackhole` | the proxy accepts and reads requests and never answers |
| `slow-200`, `slow-1000`, `slow-3000` | the proxy waits 200, 1,000 or 3,000 ms before forwarding each request (wardowl's default timeout is 2 s) |
| `http500`, `http503` | the proxy answers every request with that status |
| `truncate`, `empty`, `garbage-json`, `type-flip`, `drop-last` | the proxy alters each answer: cut in half; empty body; `{"unexpected": true}`; booleans and decision enums turned into strings or unknown values; the last element of the answer's list (or the last line of a streamed answer) removed |
| `allow-all` (control) | every denial in a check answer turned into an allow; retrieval post-filters (no pre-filter), so only the check decides |

Stores get `down`, `refuse`, `blackhole`, `slow-200` and `slow-1000`, and Qdrant also `http500`,
`http503` and `truncate`.

**Conditions:** `plain` (wardowl defaults) for every fault; `breaker` (`CircuitBreaker(failures=5,
reset_after=5)`) and `cache30` (`CachingAuthorizer(ttl=30)`) for `down`, `refuse`, `blackhole`,
`slow-3000` and `http500` on the engines.

**Episode:** a closed loop of retrievals (a 20-ms pause between them) cycling 10 fixed (user, query)
pairs whose exact answers are known: baseline 3 s, fault 12 s, then recovery until 3 s of
consecutive successes (at most 30 s; 90 s after `down`). Each retrieval runs under a 10-s watchdog
(a store has no timeout of its own); one that does not return counts as a **hang**. Every returned
hit is checked against the oracle: one outside the user's readable set is a **leak**; an answer that
differs from the exact one is a **deviation**. **Time to recover** is the end of the first successful
retrieval that started after the fault was removed (or `docker start` was issued), minus that moment.
5 seeds, 2 episodes per seed: 10 episodes per (target, fault, condition).

### Hypotheses, predictions and rules

**X7-H1, the stated bound holds.** For every path except `cerbos-policy` and every condition, every
valid trial's time to effect is at most B + 1 s. **Confirmed** when no trial exceeds it in a cell
with at least 30 valid trials; **falsified** when one trial exceeds B + 1 s or never takes effect
within B + 15 s; inconclusive with fewer than 30 valid trials.

**X7-H2, the ttl is the realized delay.** For `openfga`, `openfga-cached-hc`, `spicedb-fc`,
`spicedb-ml`, `opa-data` and `opa-policy` under `ttl5` and `ttl30`: the median time to effect lies in
[ttl - 1, ttl + S + 1] (a decision warmed just before the revocation is served until it expires).
Falsified when the median lies below ttl - 2 or above ttl + S + 2.

**X7-H3, invalidation.** `ttl30-inv`: median at most S + 0.5 s; `ttl30-shared-inv`: median at most
1 + S + 0.5 s, for every path with S stated. Falsified when a median exceeds its limit by more than
0.5 s.

**X7-H4, metadata paths ignore the ttl.** `acl-pgvector` and `acl-qdrant`: median at most 0.5 s in
every condition. Falsified when a median exceeds 1 s.

**X7-H5, engine staleness is real and bounded.** `spicedb-ml` under `nocache`: median at least
0.5 s and maximum at most 6.5 s. Falsified when the median is below 0.25 s or the maximum above
6.5 s. Exploratory: `openfga-cached-ml` (whether the check-query cache reaches ListObjects or
BatchCheck), `cerbos-policy` (Cerbos's reload delay).

**X7-H6, fail closed.** For every engine, fault (the `allow-all` control excepted) and condition,
and every store fault: no leak; every retrieval that does not return hits raised an exception, and,
for engine faults, that exception is an `AuthorizationError` whose message names no URL, IP address,
host name or port. **Confirmed** with zero exceptions to these rules; the per-request one-sided 95%
upper bound on the leak rate is reported. **Falsified** by one leak, one engine-fault failure of
another class, or one message naming a host. Store faults are reported, not judged, on the class and
text of their errors: wardowl documents fixed messages for authorizer failures only.

**X7-H7, availability cost.** Under `plain`, among retrievals that start at least 0.1 s after the
fault begins and end before it is removed:
(a) transport faults (`down`, `refuse`, `blackhole`, `slow-3000`, `http500`, `http503`) on every
engine: at least 99% fail (pooled over episodes) with the interval's lower end at least 95%;
(b) `slow-200` and `slow-1000` on every engine and store: at most 1% fail, and the median latency
rises by at least the injected delay;
(c) stores: `down`, `refuse`, `http500`, `http503` and `truncate` at least 99% fail; `blackhole` at
least 99% fail or hang.
Falsified when a share lies on the wrong side of its threshold with its interval excluding it.
Content faults on engines (`truncate`, `empty`, `garbage-json`, `type-flip`, `drop-last`) are
exploratory: we report whether each fails closed or deviates silently (fewer hits, never more).

**X7-H8, recovery and the circuit breaker.** (a) `plain`: median time to recover at most 1 s after
`refuse`, `blackhole`, `slow-3000`, `http500` and `http503` (exploratory after `down`, which includes
the server's start). (b) `breaker`: median time to recover at most 6 s (reset_after + 1 s), and under
`blackhole` the median latency of a failed retrieval at most 0.1 s, against at least 1.9 s under
`plain` (paired by seed and episode). Falsified when a median lies on the wrong side.

**X7-H9, a warm cache masks an outage.** `cache30`: at least 99% of retrievals inside the fault
window succeed, for every engine and fault in that condition. Falsified below 95%.

### Guards

- **G3 (leak detection):** the `allow-all` control leaks at least once on every engine. If not, leak
  detection is broken and X7-H6 is inconclusive.
- **G4 (baseline):** an episode whose baseline phase has fewer than 99% exact answers is excluded and
  reported. A trial whose warm retrieval misses the target is excluded and reported.

## Statistics

- **Clusters:** X4a and X4b: (seed, user); X4c: (seed, query) within a level; X4d: (seed, user or
  level, repetition); X7a: trial; X7b: episode.
- **Intervals:** 95% percentile intervals from a cluster bootstrap, 10,000 resamples, seed 20261029.
  For zero events among n clusters, the one-sided 95% upper bound `1 - 0.05^(1/n)`.
- **Paired comparisons:** X4b conditions on the same (seed, user); X4d cached against uncached on
  the same calls; X7b `breaker` against `plain` on the same (seed, episode, fault).
- Every rate is reported per cell without adjustment for multiplicity; the verdicts use only the cells
  the rules name.

## Verdicts, inconclusive results and deviations

`x4_stats.py` and `x7_stats.py` apply these rules and nothing else. A verdict is **confirmed** when
every confirming criterion holds, **falsified** when a falsifying rule holds, and **inconclusive**
otherwise, including when a server did not start, a cell the rule needs is missing or has fewer
clusters than the rule asks, fewer than 5 seeds completed, more than 5% of a cell's calls failed
for a reason other than the fault under test, or a guard fails.

The rules were fixed before any result. If a rule proves impossible to apply as written, the paper
reports a deviation rather than changing the rule; any change made before the full results exist is
committed on its own as a dated amendment below, so the rules stay readable as first written. A scope
that cannot be run in full is cut only by such an amendment, never silently.
