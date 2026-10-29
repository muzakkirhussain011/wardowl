# Pre-registration: experiments X3 (filter-size scaling) and X6 (side channels)

- **Date:** 2026-10-29.
- **Commit:** this file is committed alone, on branch `paper/x3-x6` (from `main` at 438a176, wardowl
  2.1.0 plus PR #166, honest `complete`), with the message
  `bench: pre-register the X3 and X6 experiments`. Nothing else is in that commit.
- **When:** before any X3 or X6 harness code was written and before any X3 or X6 result existed.
- **Where it runs:** GitHub Actions only, in the workflow `.github/workflows/paper-x3-x6.yml`
  (hosted `ubuntu-24.04` runners: 4 vCPUs, 16 GB, 6 hours per job). A **smoke** configuration of the
  same workflow (small corpus, one seed, one repetition) runs first to find faults in the harness. Its
  numbers are never analysed for the hypotheses below and are not reported as results; only the
  **full** configuration described here is.
- **Paper context:** contribution C7 (side channels) and the filter-size part of C4, section
  "Side channels" of the problem statement: Proposition 1 (security reduces to the check API) says
  nothing about what the timing or shape of an answer reveals.

## X6: side channels of permission-aware retrieval

**Question.** Can an authenticated subject learn whether unreadable chunks exist near a query from
what wardowl returns or how it behaves?

### The distinguishing game

Two worlds of equal size differ only in where `m` unreadable chunks lie. In **W1**, `m` secret
chunks are the `m` passages most similar to a probe query. In **W0**, those passages are absent and
`m` far-away unreadable chunks take their place. The readable set of every attacker is identical in
both worlds. The attacker issues the probe and observes only what a caller observes:

| Observable | Exposed by | Direction predicted for W1 |
|---|---|---|
| wall-clock latency of the retrieval (ms) | timing | higher |
| result count | MCP tool, HTTP service, Python API | lower |
| `complete` flag | MCP tool (`complete`), HTTP service (`complete`), Python API | lower (more often False) |
| permission-recall@10 against the exact readable top 10 (an attacker can compute it: it can read and embed its own readable set) | ids and order of the hits | lower |
| mean score of the returned hits (an empty result counts as minus infinity) | MCP tool and HTTP service return each hit's score | lower |

The widening rounds, candidates examined and denied, and the time spent in the store and the
authorizer are recorded as mechanism variables, not as observables.

Two attackers are scored. The **differencing attacker** (primary) sees the same probe in both worlds,
as one who repeats a query before and after a document is uploaded, and must say which observation is
W1: its success is the **paired AUC** (two-alternative forced choice), the share of probes whose W1
observation lies further in the predicted direction than their W0 observation, ties counting one
half. The **one-shot attacker** (secondary) sees one observation and thresholds it: its success is the
**pooled AUC** (Mann-Whitney) over all W1 against all W0 observations of a cell. Advantage is
2 x AUC - 1. The largest TPR - FPR over thresholds (the classical distinguishing advantage) is also
reported, as a point estimate.

### Data

- **Corpus:** BEIR FiQA-2018, all 57,638 passages and all 6,648 queries, from the Hugging Face hub
  (`BeIR/fiqa`), with the BEIR mirror at UKP as fallback. **Far pool:** a fixed random subset of
  12,000 passages of BEIR SciDocs (another domain: computer-science abstracts).
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions), sentence-transformers
  5.0.0 on torch 2.8.0 (CPU), `max_seq_length` 256, normalized, embedded once per run in the workflow
  and shared with every job as an artifact; the model's hub revision is recorded. The text of a
  passage is its title and text joined.
- **Plans** (computed once, in the data job, by exact search, and shared, so every store runs the
  identical game): for each seed, probe queries are drawn greedily, in a seeded random order over all
  6,648 queries, into four levels: **m = 1, 10, 100, 1,000** with up to **24, 24, 16 and 8** probes
  per seed. A probe's *near set* is its m most similar passages; its *zone* is its m + 1,000 most
  similar passages. A probe is accepted only if its near set meets no accepted probe's zone and its
  zone meets no accepted probe's near set, so no probe sees another probe's secrets within the depth
  the layer can explore (the post-filter cap is 1,000). Levels are filled from m = 1,000 down.
  Fewer probes are recorded, never silently replaced, when the greedy runs out.
- **Worlds:** the union U of the near sets is removed from the background. W1 = background + U with a
  secret ACL. W0 = background + |U| SciDocs-derived chunks with the same secret ACL, each matched to
  one near passage and cut (or extended with the following SciDocs passages) to the same number of
  word tokens (`\w+`), so the corpus size and the total text length are equal in both worlds and BM25
  length normalisation does not differ. A far chunk's vector is its first SciDocs passage's
  embedding. Only SciDocs passages less similar to every probe than that probe's zone boundary are
  eligible. Both worlds insert the extra chunks at the same seeded random positions of the same
  seeded background order.
- **Permissions:** each background passage gets a bucket 0 to 99 (seeded); its metadata is
  `allowed_users: ["owner<bucket>"]`, `allowed_groups: ["g<bucket>"]`. Secrets and far chunks carry
  `allowed_users: ["owner-secret"]`, `allowed_groups: ["g-secret"]`. Three attackers, with groups
  `g00` to `g<p-1>`, read **p = 1%, 10% and 50%** of the background (selectivity). The authorizer is
  `MetadataACLAuthorizer`; its filter is `Or(In(allowed_users, [id]), In(allowed_groups, groups + "*"))`.
- **Exact reference:** for each (seed, probe, p), the exact readable top 10 by cosine similarity and
  the tie-aware set T* (every readable passage within 1e-4 of the 10th score), identical in all worlds.
- **Seeds:** 5 (0 to 4). A seed fixes the probe order, buckets, far sampling, insertion order and
  measurement order. Every seed is a fresh build of every index.

### Stores and configurations (k = 10)

Server images are those of the conformance campaign: `pgvector/pgvector:pg17`,
`qdrant/qdrant:v1.19.2`, `docker.elastic.co/elasticsearch/elasticsearch:9.5.5`; clients from
`uv.lock`; FAISS 1.15.1 and wardowl's `InMemoryBackend` in process.

| Config | Meaning | Stores |
|---|---|---|
| `pre` | pre-filter, the store's approximate filtered search at documented defaults | pgvector (HNSW m=16, ef_construction=64, ef_search 40, iterative scan `relaxed_order`, `hnsw.max_scan_tuples` 20,000), Qdrant (default HNSW, payload indexes on both permission fields), Elasticsearch (default `dense_vector` index options for 384 dimensions, `num_candidates` 100); FAISS flat and in-memory (exact: controls) |
| `post` | post-filter, wardowl defaults: fetch 4k, widen x4 until k permitted, the store runs out, or 1,000 candidates | pgvector, Qdrant, Elasticsearch, FAISS, in-memory |
| `post-const` | **mitigation M1, constant-work widening:** overfetch 100, so every retrieval fetches the cap of 1,000 in one round | pgvector, Qdrant, Elasticsearch, FAISS |
| `pre-exact` | **mitigation M2, exact pre-filtered search:** pgvector with `enable_indexscan = off`; Qdrant `exact=True`; Elasticsearch `script_score` cosine over the filter | pgvector, Qdrant, Elasticsearch |
| `bm25-pre` | keyword search under the pre-filter (channel c) | Elasticsearch (BM25), Qdrant (sparse vectors with the IDF modifier), pgvector (`ts_rank_cd`, which uses no collection statistics: a negative control) |
| `hybrid-pre` | `RankFusion` of the `pre` vector search and BM25 | Elasticsearch |
| `hybrid-exact` | `RankFusion` of the exact vector search and BM25 (both halves deterministic) | Elasticsearch |

Deviation from defaults, stated in advance: Qdrant's `indexing_threshold` is lowered to 1,000 KB so
that every segment of these small collections is HNSW-indexed, as the segments of a production
collection are; pgvector runs with `shared_buffers` 2 GB and `maintenance_work_mem` 1 GB (build
settings only); Elasticsearch has 1 shard, 0 replicas and a 2 GB heap.

**Mitigation M3, per-tenant separation:** a third index per seed, **SEP**, holds the background only,
as the attacker's tenant would if the secrets lived in another tenant's index. Under separation the
attacker's index is the same in W0 and W1, so its advantage is the advantage between two series of
measurements of one index. SEP is measured twice per repetition (SEPa, SEPb); their comparison is
both M3's measured advantage and the harness's **A/A null**. **Mitigation M4, latency padding:** each
retrieval's latency is padded to the next multiple of a budget T, fixed per (store, config) as the
largest latency of seed 0 rounded up to the next millisecond; padding is evaluated on seeds 1 to 4
only, from the measured latencies (an ideal padder: scheduler jitter is not modelled).

**The in-memory control** ranks by keyword overlap, re-scoring the whole corpus in Python on every
search (about a second at this size), so it runs a reduced design: the first 3 probes of each level,
p = 10% only, `pre` and `post`, 3 timed repetitions. It is not a vector store; H1 and H2 do not
apply to it.

### Measurement

For each seed, store, probe (in a seeded random order), attacker and configuration: one warm-up and
**5 timed repetitions**; each repetition runs the four slots W0, W1, SEPa, SEPb in a fresh random
order, so drift affects every world alike. One client thread. Per (slot, probe, attacker, config)
the observation is the median latency of the 5 repetitions, the median count, the share of
repetitions with `complete` True, the mean recall and the mean of the mean score. Every retrieval is
re-checked by wardowl; any hit outside the attacker's readable set stops the run (none is expected).

### Statistics

- **Cell:** (store, config, m, p), or pooled over p or over m and p where a rule says so.
  **Cluster:** a (seed, probe) pair.
- **Intervals:** 95% percentile intervals from a cluster bootstrap over (seed, probe), 10,000
  resamples, seed 20261029. Paired and pooled AUCs are recomputed on each resample.
- **"Channel present"** for a cell and observable: paired AUC at or above the rule's threshold and
  its interval's lower end above 0.55. **"No channel"**: the interval lies within [0.40, 0.60].
- **Paired comparisons between configurations** on the same probes: the difference in paired AUC
  between an unmitigated configuration and its mitigation (`post` - `post-const`, `pre` -
  `pre-exact`, shared - SEP, raw - padded latency), and the latency cost of each mitigation (ratio of
  means, and median of per-probe ratios), bootstrapped jointly on the same resamples.
- **Id-list change rate:** the share of (probe, p) whose ordered hit ids differ between W1 and W0
  (first timed repetition). Interpreted only for deterministic configurations (`pre-exact`, FAISS and
  in-memory `pre`, `bm25-pre`, `hybrid-exact`); for approximate indexes W0 and W1 are different
  builds, so a change is confounded with build randomness and is not interpreted.

### Guards (checked before any verdict)

- **G1 (A/A):** for each (store, config), the latency paired AUC of SEPb against SEPa, pooled over m
  and p, has its interval within [0.40, 0.60]. If not, every latency-based part of that
  configuration's verdicts is inconclusive.
- **G2 (exactness):** the W1-against-W0 id-list change rate of `pre-exact` and FAISS `pre` is at most
  0.01. If not, the harness or data is at fault and that store's X6 verdicts are inconclusive.

### Hypotheses, predictions and rules

**H1, widening (channel a).** `post` on each vector store (FAISS, pgvector, Qdrant, Elasticsearch):
(a) at m = 1,000 the count paired AUC is at least 0.95 at every p (the 1,000 nearest candidates are
the secrets, so the widening ends at the cap with nothing readable);
(b) at m = 100 the latency paired AUC is at least 0.75, with the channel present, at p = 10% and 50%
(one more widening round);
(c) at m = 1 there is no channel in any observable (pooled over p).
**Confirmed** when (a), (b) and (c) hold on every vector store; **falsified** when on some store the
count AUC at m = 1,000 is below 0.80 at some p, or the latency AUC interval at m = 100, p = 50% lies
below 0.60, or some observable has a channel present at m = 1 (interval above 0.60).

**H2, constant-work widening (M1).** `post-const` on each vector store: (a) no latency channel,
pooled over m and p, and at m = 1,000 (pooled over p) the latency interval's upper end is at most
0.65; (b) the count paired AUC at m = 1,000 is still at least 0.95 at p = 10% and 50% (the cap is
exhausted by secrets in one round instead of four). **Confirmed** when both hold on every vector
store; **falsified** when the latency interval lies above 0.60 (pooled, or at m = 1,000) on some store,
or the count AUC at m = 1,000 is below 0.80.

**H3, approximate pre-filtering (channel b).** Each part is judged on its own:
(a) pgvector `pre`: latency paired AUC at least 0.75 with the channel present at m = 1,000 for
p = 10% and 50%, and at m = 100 for p = 50% (the iterative scan must pass the secrets, which fail
the filter, before it reaches readable rows); falsified when the interval at m = 1,000, p = 50% lies
below 0.60;
(b) Elasticsearch `pre`: latency paired AUC at least 0.75 with the channel present at m = 1,000 for
p = 10% and 50%; falsified when the interval at m = 1,000, p = 50% lies below 0.60;
(c) Qdrant `pre`: no channel in any observable at p = 1% and 10% (pooled over m and those p), where
the filter's cardinality is low enough for Qdrant to score it exactly through the payload index;
falsified when some observable has an interval above 0.60.
p = 1% for pgvector and Elasticsearch, and p = 50% for Qdrant, are exploratory (no prediction).

**H4, exact pre-filtering (M2) and the controls.** For pgvector, Qdrant and Elasticsearch
`pre-exact`, FAISS `pre` and in-memory `pre`: no channel in any observable pooled over m and p, and
at m = 1,000 (pooled over p) every interval's upper end is at most 0.65. Judged per store and
configuration; **falsified** when some observable's interval lies above 0.60 pooled, or above 0.65
at m = 1,000.

**H5, collection statistics (channel c).**
(a) Elasticsearch and Qdrant `bm25-pre`: the score paired AUC is at least 0.90 at every m, pooled
over p, including m = 1 (one more on-topic document lowers the IDF of the probe's terms, and the
API returns exact scores); falsified when the interval at m = 1,000 lies below 0.70. Judged per store.
(b) pgvector `bm25-pre` (`ts_rank_cd`): no channel in the score, pooled over m and p, and an id-list
change rate of at most 0.01; falsified when the score interval lies above 0.60 or the change rate
exceeds 0.05. Its latency is exploratory.
(c) Elasticsearch `hybrid-exact`: id-list change rate at m = 1,000 (pooled over p) of at least 0.25;
falsified below 0.05.

**H6, latency padding (M4).** In every cell (store, config, m, pooled over p) whose unpadded latency
paired AUC on seeds 1 to 4 is at least 0.75, padding gives no latency channel. **Confirmed** when that
holds in every such cell; **falsified** when some such cell keeps a padded latency interval above 0.60.
Its cost (mean padded latency over mean raw latency) is reported; no prediction.

M3 (separation) is reported with its A/A advantage and its latency cost against the shared index;
the advantage is zero by construction, so there is no hypothesis beyond G1.

## X3: filter-size scaling

**Question.** How do stores behave when the permission filter is a disjunction over many groups, as
for a user in thousands of directory groups?

### Design

- **Corpus per seed:** 100,000 vectors of 384 dimensions: the 57,638 FiQA passage embeddings above
  (the semantic subset) and 42,362 synthetic vectors (seeded: 200 cluster centres on the unit sphere,
  each vector a normalized centre plus Gaussian noise, sigma 0.06 per dimension). If the data job
  failed, all 100,000 are synthetic, and that is recorded and reported. Placeholder text only.
- **Queries per seed:** 30 FiQA query embeddings (seeded sample), k = 10.
- **Groups per subject:** **G = 1, 10, 100, 1,000, 4,000, 10,000, 40,000**. The filter is
  `MetadataACLAuthorizer`'s, `Or(In(allowed_users, [u]), In(allowed_groups, groups + "*"))`, so it
  holds G + 1 group values.
- **Fixed selectivity:** a seeded 10% of the corpus (the pool) is readable at every G. Each document
  carries one user and seven groups: a pool document holds, for each level G, one group drawn from
  that level's G groups; every other document holds seven groups from a disjoint namespace. The
  subject at level G holds exactly that level's G groups, so its readable set is the pool at every G
  and only the filter's size changes.
- **Stores** (the campaign's images and clients; default index settings): pgvector, Redis 8.10.2,
  Cassandra 5.0.9, Elasticsearch 9.5.5, OpenSearch 3.9.0, Vespa 8.763.13 (the example application
  with 384 dimensions, `approximate=True`), Qdrant v1.19.2, Milvus v3.0.2, Weaviate 1.39.12, MongoDB
  Atlas Local 8.0.30, Chroma 1.5.9 (embedded), LanceDB 0.40.0 (embedded, no ANN index: exact), and
  the controls FAISS flat and in-memory (in-memory ranks by keywords, so its recall is not defined).
  A store the job cannot start is reported as not started.
- **Seeds:** 5, each a fresh corpus, ACL, query set, insertion order and build.
- **Per (seed, G):** the store's translator is called on the filter (median of 3 timings, output
  size); then one warm-up pass and 3 timed passes over the queries. If the first warm-up retrieval
  takes more than 2 s, the timed passes use the first 10 queries only (recorded). A retrieval has
  120 s; a level that times out ends the seed's larger levels (recorded as not run).
- **Metrics:** translation success and time; acceptance (the exact error class and message when the
  store refuses); end-to-end latency p50, p95 and p99, each computed per pass over the queries and
  reported as the median of the 3 passes; tie-aware recall@10 against exact search over the pool
  (epsilon 1e-4). For pgvector, EXPLAIN ANALYZE of the first query of each level (plan node types and
  rows removed by the filter).
- **Statistics:** 95% cluster-bootstrap intervals over (seed, query), 10,000 resamples, seed
  20261029; latency ratios and recall differences between levels are paired by query.

### Documented limits that could bind (from the stores' documentation, checked by the run)

| Store | Limit | What wardowl sends |
|---|---|---|
| Elasticsearch, OpenSearch | `index.max_terms_count` 65,536 terms per `terms` query; `indices.query.bool.max_clause_count` (OpenSearch default 1,024) | one `terms` query per `In`: 2 clauses |
| PostgreSQL | 65,535 bind parameters per statement | above 100 values, two array parameters per `In` (wardowl's `MANY_VALUES`) |
| SQLite under Chroma | 32,766 host parameters and an expression depth of 1,000 (SQLite defaults) | `$in` plus one `$eq` per value |
| Cassandra (wardowl) | at most 256 ANN queries per filter (`max_queries`), ANN `LIMIT` 1,000 | above 254 groups, one unfiltered 1,000-row ANN query filtered locally (documented fallback) |
| MongoDB | 16 MB per command | one `$in` |
| Qdrant | 32 MB per REST request | one `MatchAny` |
| Redis, Weaviate, Milvus, Vespa, LanceDB | none known to us | one disjunction |

### Hypotheses, predictions and rules

**X3-H1, translation.** Every translator returns for every G up to 40,000 in under 1 s (median),
Cassandra's `TooManyQueries` counting as its documented fallback. **Falsified** when a translator
raises anything else, or takes 5 s or more, at some G; inconclusive in between.

**X3-H2, acceptance at G = 40,000.** A store **accepts** a level when at least 95% of its timed
retrievals return without error over the seeds run, and **refuses** it when the first retrieval of the
level fails in every seed. Predictions: accepts: Elasticsearch, OpenSearch, Qdrant, pgvector,
LanceDB, Cassandra (through the fallback), FAISS, in-memory; refuses: Chroma; no prediction: Redis,
Weaviate, Milvus, MongoDB, Vespa. Each predicted store is judged on its own (confirmed when the
outcome matches, falsified when it is the other, inconclusive when mixed).

**X3-H3, latency.** Ratios are of p50 at G = 40,000 over p50 at G = 1, paired by query.
(a) pgvector: ratio at least 50 with the interval's lower end at least 20 (above 100 values the
filter is an array test on `metadata -> field` that the GIN index cannot serve, evaluated per scanned
row); falsified when the interval's upper end is below 10.
(b) FAISS and in-memory: ratio at most 2 (each chunk is matched with a set lookup); falsified when
the interval's lower end is above 3.
(c) Cassandra: p50 at G = 100 is higher than at G = 1,000 (102 ANN queries against one with the
fallback): the ratio's interval lies above 1; falsified when it lies below 1.

**X3-H4, recall does not depend on the filter's size.** For Qdrant, Elasticsearch, OpenSearch,
Redis, Weaviate, Milvus, MongoDB, Chroma and Vespa, among the levels a store accepts: the mean
paired difference in recall@10 between G = 40,000 (or the largest accepted level, if at least 1,000)
and G = 1 lies within [-0.02, 0.02] with its interval within [-0.05, 0.05]. Judged per store;
falsified when the interval excludes 0 and the difference exceeds 0.05 in absolute value. FAISS and
LanceDB are exact: recall 1.0 at every level is a sanity check. pgvector (its plan may change when
the filter crosses 100 values) and Cassandra (fallback) are exploratory.

Exploratory, with no prediction: the shape of latency against G (slopes on log scales), p95 and p99,
the error messages, payload sizes and pgvector's plans.

## Verdicts, inconclusive results and deviations

`x6_stats.py` and `x3_stats.py` apply these rules and nothing else. A verdict is **confirmed** when
every confirming criterion holds, **falsified** when a falsifying rule holds, and **inconclusive**
otherwise, including when:

- a store did not start, or a cell the rule needs is missing or has fewer than 20 clusters, or fewer
  than 5 seeds completed for it;
- more than 5% of the retrievals of a cell the rule needs failed;
- a guard (G1, G2) fails for the configuration;
- an interval straddles a threshold so that neither the confirming nor the falsifying criterion holds.

Every interval is reported per cell without adjustment for multiplicity; the verdicts use only the
cells the rules name. The rules were fixed before any result. If a rule proves impossible to apply as
written, the paper reports a deviation rather than changing the rule; any change made before the
full results exist is committed on its own as a dated amendment below, so the rules stay readable as
first written. A scope that cannot be run in full is cut only by such an amendment, never silently.

## Amendment 1 (2026-10-29, after the smoke runs, before any full result)

Made the same day, after two smoke runs of the harness (small data, one seed, never analysed) and
before the full configuration ran. It is committed on its own, so the design above stays readable as
first written. No hypothesis, prediction, threshold, statistic or verdict rule changes.

1. **X6 probes are placed in groups, and W0 is built per group.** As first written, all probes of a
   seed shared one W0, and no probe's secrets could lie in any other probe's zone. The smoke run
   placed one probe of seven, and the rule cannot be met at full scale either: a zone of 1,000 or
   more passages almost always meets one of thousands of other probes' secrets, through topical
   overlap and through hub passages, which lie among the nearest neighbours of most queries. Instead,
   each seed has **8 groups of 9 probes** (one at m = 1,000, two at m = 100, three at m = 10, three at
   m = 1: still 8, 16, 24 and 24 probes per seed). **W1** is one index holding every group's secrets.
   For each group g, **W0_g** holds the same chunks except group g's secrets, each replaced by its far
   chunk at the same insertion position. A probe of group g is compared between W1 and W0_g, which
   differ only in group g's own secrets; other groups' secrets are unreadable chunks present in both,
   part of the background. The zone rule applies within a group (no probe's near set meets a group
   mate's zone, in either direction), and near sets are disjoint across all probes of the seed. SEP is
   unchanged. A seed builds W1, SEP and the 8 W0_g indexes, each W0_g live while its group is
   measured, with W1 and SEP; the slots and their random order per repetition are as before (the W0
   slot is W0_g). Far chunks are drawn without replacement across groups. A group the greedy cannot
   fill is recorded as such, as before.
2. **Hub passages are never secrets.** A hub is one of the 1% of passages that appear among the
   2,000 nearest passages of the most queries (all 6,648). A probe's near set is its m nearest
   passages that are not hubs; its zone is every passage up to the rank of its m-th near passage,
   plus 1,000. Hubs stay in the background, with their buckets, in every world.
3. **X3 runs each seed in its own process**, so a store that crashes the client process (the smoke
   run's Chroma ended with a segmentation fault at G = 40,000) loses that level only, not the seeds
   after it. For X3-H2, a level whose process crashed counts as a level whose first retrieval failed,
   and the report names the crash.
4. **Smoke runs embed the full corpus** (cached between runs) and plan every seed's groups as the full
   run does, so they test probe placement at full scale; they measure group 0 of seed 0 only. This
   changes the smoke procedure, not the full design.

## Amendment 2 (2026-10-29, after the third smoke run, before any full result)

Committed on its own, before the full configuration ran. No hypothesis, prediction, threshold,
statistic or verdict rule changes.

1. **Near sets may be shared between groups.** Amendment 1 required every passage to be a secret of
   at most one probe in the seed. At full scale (57,638 passages) that placed every probe at m = 100,
   10 and 1, but only 2 of the 8 at m = 1,000: after two sets of 1,000 passages, no other question's
   1,000 nearest passages avoid them. The rule is not needed. A secret held by several groups gets one
   far chunk, which replaces it in the W0 of each of those groups, so W1 and W0_g still differ in
   group g's secrets only, and every probe's comparison is unchanged. The zone rule within a group
   stays. The plan records how many secrets belong to more than one group.
2. **Qdrant's indexing threshold is 10 KB, not 1,000 KB.** At 1,000 KB a last appendable segment
   (320 of 8,000 vectors in the X3 smoke run) stayed below the threshold and unindexed; 10 KB, a few
   vectors, indexes every segment, which is what the design states. A build is ready when the
   collection is green and either its vectors are indexed on two polls in a row or its indexed count
   has not changed for a minute; the indexed count is recorded with every build.

## Amendment 3 (2026-10-29, after the fourth smoke run, before any full result)

Committed on its own, before the full configuration ran. No hypothesis, prediction, threshold,
statistic or verdict rule changes.

1. **A group that cannot be filled is placed again with another m = 1,000 probe.** In the fourth
   smoke run every group got its m = 1,000 and m = 100 probes, but one group lacked one m = 10 and
   three m = 1 probes (68 of 72): its m = 1,000 probe's secrets lay inside the zones of every
   remaining candidate. Now, when a group cannot be completed, its m = 1,000 probe is set aside and
   the group is placed again from the next candidate, up to 25 times; the most complete placement is
   kept, and any shortfall is still recorded.
