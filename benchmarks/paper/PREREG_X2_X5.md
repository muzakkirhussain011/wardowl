# Pre-registration: experiments X2 and X5

X2: recall against throughput under permission-shaped filters (the paper's contribution C4).
X5: detecting and repairing under-retrieval (contribution C5).

- **Date:** 2026-10-29.
- **Commit:** this file is committed alone, on branch `paper/x2-x5` (from `feat/under-retrieval` at
  `db28517`), with the message `bench: pre-register experiments X2 and X5`. Nothing else is in that
  commit, and no X2 or X5 code exists yet.
- **What was seen before:** the published aggregates of the scenario run of 2026-10-24 (X0, its
  re-analysis in X1 run 1), the X1 run 1 verdicts and settings table (evidence file
  `x1-underretrieval-run1.md` of the paper workspace), and the repository's MS MARCO benchmarks of
  2026-10-22 (`benchmarks/results/msmarco-1m-*.md`). None of the layouts, subjects or queries
  defined below exists yet, and no store has been run on them.
- **Library under test:** wardowl at the head of this branch, which carries the API of PR #168:
  `PermissionedRetriever(short_results="report" | "count" | "exact" | "widen", max_exact_rows,
  wider, recall_sample_rate)`, the result fields `shortfall`, `fallback` and `sampled_recall`,
  pgvector's `max_scan_tuples`, `scan_mem_multiplier`, `work_mem`, `count` and exact search, and
  Qdrant's `count` and exact search.
- **Where it runs:** GitHub Actions hosted runners (4 vCPUs, 16 GB of memory), one store per job,
  the store in a Docker container on the same runner, one client thread. Throughput is compared
  only between settings of the same job; recall does not depend on the hardware and is compared
  across jobs.

## 1. Corpora

**E, the enterprise scenario.** `acceptance/kaggle/enterprise_rag.py` at its original settings
(seed 7, 208 variants per template, all of BEIR FiQA): 107,540 chunks in 20 tenants, embedded with
BAAI/bge-base-en-v1.5 (768 dimensions, unit length, float32 on CPU, the model's query
instruction), its real permission policy `AllOf(TenantAuthorizer(), MetadataACLAuthorizer())`, its
oracle (`readable`) and canary detector. People and questions: the original 189 people and 1,105
questions, plus X1's probe set (one person holding a single group, for each of 8 groups, in 3
generated tenants, each asking the 12 template questions of their tenant and 4 FiQA queries; seed
61): 213 people and 1,489 questions. E has one permission layout, the scenario's own; its
replication units are the index builds and the people.

**M, MS MARCO.** The first 1,000,000 non-empty passages of BEIR MS MARCO (`title` and `text`
joined, as `benchmarks/load_bench.py` reads them), embedded with **BAAI/bge-small-en-v1.5** (384
dimensions, unit length, float32 on CPU, at most 512 tokens; queries carry the model's retrieval
instruction). Why bge-small rather than bge-base:

1. The repository's own million-chunk benchmarks of 2026-10-22 used it, so X2's MS MARCO numbers
   connect to published ones.
2. Memory. The harness keeps the vectors to score every hit, the store keeps its copy and its
   index, and Redis keeps two copies (the hash and the index). At 384 dimensions a copy is 1.5 GB;
   at 768 it is 3.1 GB, and Redis, Weaviate and Milvus beside the harness would not fit in a 16 GB
   runner with room for the operating system and the store's working memory.
3. Time. Embedding on CPU takes about a third of bge-base's.

The cost is that E and M use different models. No claim compares a store across corpora through
the model; the corpora are analysed separately.

A query pool of 20,000 MS MARCO queries is drawn (seed 20261029) from the unique non-empty texts
of BEIR MS MARCO's `queries` split and embedded the same way.

**Embeddings are computed once**, in sharded CPU jobs; each shard records the SHA-256 of its
vectors and of the ids it embedded, the merge checks them, and the merged matrix's SHA-256 is
recorded. Every store job verifies every data file's SHA-256 before it loads anything. A later
run reuses the same files (downloaded from the run that made them) rather than embedding again.

## 2. Permission layouts over M

**Hierarchy.** 100 divisions, 10 departments in each, 10 teams in each department: 10,000 teams.
Every passage belongs to one team, and its permission field lists the three tags of its team,
department and division (as `benchmarks/permissions_bench.py` does).

- **U (uncorrelated), seed r:** a random permutation of the rows; the row at position p gets
  division p // 10,000, department p // 1,000, team p // 100. Groups are exactly balanced and
  unrelated to content.
- **C (clustered), seed r:** hierarchical spherical k-means (faiss, inner product on unit vectors,
  20 iterations, seed r): 100 divisions over all rows, 10 departments within each division, 10
  teams within each department. Groups are topical; their sizes vary and are recorded.
- **Tenant:** a field `tenant` in {a, b}, each row independently with probability 1/2 (seed
  20261029), the same for every layout seed.
- **Seeds:** r in 0..4 for each family. Every row carries all ten layouts at once (fields `u0` to
  `u4` and `c0` to `c4`, each a list of three tags, and `tenant`), so one load serves every
  layout, and a store is never reloaded to change layouts.

**Grants.** A subject's grant for a target of T passages is drawn coarse to fine at random:
divisions while the total stays at most 60% of T, then departments while it stays at most 90% of
T, then teams until it reaches 95% of T (a team may overshoot; nodes inside a granted node are
never added). Nominal selectivity levels s: **0.06%, 0.5%, 2%, 10%, 30%, 100%**; T = s x N. The
selectivity a subject really has is recorded and every analysis also bins by it.

**Filter shapes.**
- *groups:* `In(F<r>, grant)`, one OR over the subject's groups (between 1 and a few hundred
  values);
- *tenant:* `And(In(tenant, [a]), In(F<r>, grant))` with the grant drawn for 2T, so the
  conjunction passes about s; each clause alone passes far more than both, which is where store
  planners that multiply clause estimates go wrong.

At 100% the groups filter lists every division (it passes everything); the tenant shape and the C
family are not run at 100%.

**Correlation regimes.** For each subject, queries come from the pool:
- **U:** 4 queries drawn at random.
- **C, P (positively correlated):** 4 queries drawn from those whose 100 nearest passages are at
  least half readable by the subject (rho_100 >= 0.5).
- **C, N (negatively correlated):** 4 queries drawn from those with no readable passage among
  their 1,000 nearest (rho_1000 = 0).

If fewer than 4 queries qualify, the best ones by the criterion are taken (highest rho_100 for P,
lowest rho_1000 then the latest first readable rank for N) and the shortfall is recorded. P and N
queries of one C subject share its readable set, so P against N is paired within subjects.

**Cells and sizes.** 10 subjects per (family, seed, s, shape). U: 6 groups cells and 5 tenant
cells; C: 5 levels x 2 shapes, each subject with 4 P and 4 N queries. Per seed, 1,240 (query,
subject) pairs; over 5 seeds, **6,200 pairs**, 1,050 subjects.

## 3. Measured correlation axes

For every (query, subject) pair of both corpora, from exact scoring of the query against every
chunk (cosine similarity on unit vectors; d = 1 - similarity):

- **R**, the readable count, and global selectivity sigma_g = R / N;
- **ACORN query correlation:** E[g(q, random set of size R)] - g(q, readable set), with g the
  distance to the nearest member; the expectation over random sets is computed exactly from the
  ranked similarities (the probability that the best member of a random R-subset has rank j);
- **Global-Local Selectivity** (Amanbayev et al.): sigma_l = readable share of the 2,048 nearest
  chunks (their |N_q| = 2,048), r = sigma_l / sigma_g, GLS = (r - 1) / (r + 1);
- **HCBGen's over-fetch estimate** alpha_hat(q, K = 10) = (N / R) x (d_K(readable) / d_K(all)) x K
  (their Eq. 5; d_K is the distance to the K-th nearest member, or to the farthest if fewer than K
  are readable). HCBGen's full alpha-Hardness multiplies in a graph fetch cost (Steiner hardness)
  that needs a specific index; it is not computed, and the paper reports alpha_hat by that name;
- **local selectivity** rho_100 and rho_1000, the readable share of the 100 and 1,000 nearest
  chunks;
- **r1**, the unfiltered rank of the first readable chunk (1 + the chunks strictly more similar),
  and r10, of the tenth.

## 4. Stores and settings (X2)

Images and clients as the conformance campaign starts them: PostgreSQL 17 with pgvector
(`pgvector/pgvector:pg17`), Qdrant 1.19.2, Elasticsearch 9.5.5, OpenSearch 3.9.0 (Lucene engine),
Weaviate 1.39.12, Redis 8.10.2, Milvus (`milvusdb/milvus:v3.0.2` standalone), MongoDB Atlas Local
8.0.30, LanceDB 0.40.0 and Chroma 1.5.9 (embedded), and FAISS 1.15.1 flat, the exact reference
(wardowl's `FaissBackend`, one build, since a flat index has no build randomness). Client versions
come from `uv.lock`. Every chunk is written through the wardowl backend's own `add` and layout,
except two bulk paths with the same layout: pgvector by binary COPY into `create_schema`'s table,
then the GIN and HNSW indexes; LanceDB by `table.add` in the backend's row layout, then
`create_indexes` and the default vector index. pgvector runs with `shared_buffers` 3 GB and
`maintenance_work_mem` 2 GB, every other server setting at its default; every pgvector search is
planned with its own values (psycopg `prepare_threshold=None`; X1 run 1 showed that prepared
statements turn into generic plans that skip the HNSW index).

"Default" is what a user gets from the store when the search-effort knob is not set; where
wardowl's backend always sends a value (Elasticsearch, Milvus, MongoDB), the store's documented
default is sent instead, or wardowl's when the store documents none. "Sweep" is the store's
search-effort knob at five levels. "Exact" is the store's own exact search under the same filter.
"As run" marks the setting the 2026-10-24 scenario run used on E (for check V2).

| Store | Default | Sweep (5 levels) | Store-specific options | Exact |
|---|---|---|---|---|
| pgvector | `hnsw.iterative_scan` off, `ef_search` 40 | `relaxed_order` with `ef_search` 40 (wardowl's default), 100 (as run), 200, 400, 1000 | `max_scan_tuples` 1,000,000 with `scan_mem_multiplier` 16 (ef 100); `strict_order` (ef 100) | `enable_indexscan = off` |
| Qdrant | no search params (hnsw_ef = ef_construct, 100) | `hnsw_ef` 64, 128 (as run), 256, 512, 1024 | ACORN at the default gate (0.4); ACORN at gate 1.0 with `hnsw_ef` 512; the per-tenant layout (below) | `exact=True` |
| Elasticsearch | `num_candidates` 15 (1.5 k) | `num_candidates` 50, 100, 500 (as run), 2000, 10000 | index type: `bbq_hnsw` (the default above 384 dimensions) on M and E; `int8_hnsw` (as run) on E | `script_score` cosine under the filter |
| OpenSearch | no `ef_search` | `method_parameters.ef_search` 32, 64, 128, 256, 512 | none | `script_score` (`knn_score`) under the filter |
| Weaviate | `ef` -1 (dynamic), filter strategy ACORN, `flatSearchCutoff` 40,000 | fixed `ef` 64, 128, 256, 512, 1024 | filter strategy `sweeping`; `flatSearchCutoff` 0 | `flatSearchCutoff` above N |
| Redis | `EF_RUNTIME` 10, policy chosen by Redis | `EF_RUNTIME` 50, 100 (as run), 200, 500, 1000 | `HYBRID_POLICY BATCHES` (EF_RUNTIME 100) | `HYBRID_POLICY ADHOC_BF` |
| Milvus | no `ef` sent | `ef` 32, 64, 100 (wardowl's default), 256, 512 | none | none per query |
| MongoDB | `numCandidates` 100 (wardowl's; Atlas has none) | `numCandidates` 20, 50, 200, 1000, 10000 | none | `exact: true` |
| LanceDB | IVF_PQ, `nprobes` and `refine_factor` unset | `nprobes` 10, 50, 100, 200, 500 | `nprobes` 50 with `refine_factor` 30 (as run); post-filtering (`prefilter=False`) | `bypass_vector_index()` |
| Chroma | `ef_search` 100 | `ef_search` 10, 50, 200, 500, 1000 | none | none per query |
| FAISS | flat (exact) | none | none | the default |

On E, Chroma, OpenSearch and Weaviate ran at their defaults in the scenario run, which are the
as-run settings for V2.

**The per-tenant layout (Qdrant).** The tenant field indexed with `is_tenant=true`, and
`hnsw_config` m 0 with `payload_m` 16: one graph per tenant value and no global graph. On E the
field is the scenario's tenant; on M it is `tenant`, and only tenant-shape subjects are queried
on it. Settings: `hnsw_ef` 128, `hnsw_ef` 512, ACORN at gate 1.0, exact.

**Builds.** Three builds per (store, corpus, layout): each a fresh load and index build. On E a
job loads the three builds in turn; on M each build is its own job (a store's million-chunk load
takes up to an hour). Query-time settings run on every build; exact settings run on build 0 only,
since they do not use the index.

**Procedure for one setting.** k = 10. Twenty untimed warm-up retrievals. Pass 1 runs the setting's
query list once and records the hits; passes 2 and 3 run the same list again; a query's latency
is the median of its three, and a cell's throughput is its queries divided by the sum of their
latencies, the median over the three passes. Single client, one thread, end to end through
`PermissionedRetriever` (default `short_results="report"`), whose re-check sees every hit; the
time inside the store (`search_ms`) is recorded too. The query list is a fixed round-robin order
over cells, seeds and subjects (E: over people), so that any prefix is balanced. Each setting has a
time budget: a fair share of the job's remaining time; pass 1 may use 40% of it, and a setting cut
short keeps a balanced prefix, whose size is recorded. A budget never changes a setting; it only
shortens its list.

**Frontier.** Per store, corpus and cell: recall@10 against queries per second for every setting
of one job (one build). Frontier points are compared within a job; recall is also averaged over
builds.

## 5. Arms (X5)

pgvector and Qdrant, on E and M, base configuration as run: pgvector `relaxed_order`, `ef_search`
100, the scan limits at their defaults (20,000 tuples, `work_mem` 4 MB, multiplier 1); Qdrant
`hnsw_ef` 128, no ACORN. Every arm is a `PermissionedRetriever` configuration over the same
backend and build:

| Arm | Configuration |
|---|---|
| report | `short_results="report"` (the default) |
| count | `short_results="count"` |
| exact-1k, exact-10k, exact-inf | `short_results="exact"`, `max_exact_rows` 1,000, 10,000, None |
| widen | `short_results="widen"`, `wider` = pgvector with `max_scan_tuples` 1,000,000, `scan_mem_multiplier` 16, `ef_search` 400; Qdrant with `hnsw_ef` 512 and ACORN at gate 1.0 |
| monitor | `short_results="report"`, `recall_sample_rate` 0.01 (Python's random seeded per arm and pass) |
| native (pgvector) | report, with `max_scan_tuples` 1,000,000 on the backend alone |
| native (Qdrant) | report, with ACORN at gate 1.0 alone |
| native (Qdrant, per-tenant) | report, on the per-tenant layout (E: in the X5 job; M: X2's per-tenant jobs, recall and flags only) |

Pass 1 runs k = 5 and k = 10 for every query; passes 2 and 3 repeat k = 10, timed. Builds and
budgets as in X2.

## 6. Metrics

Per retrieval, against exact search over the readable set (FAISS-equivalent brute force in NumPy
over the same float32 vectors):

- **recall@k**: |H intersect T*_eps| / min(k, R) with the k-th exact score's tie tolerance
  eps = 1e-4 (background.tex), for k = 5 and 10;
- **maximal**: recall 1 (or no hit when R = 0); **empty**: no hit while R >= 1; **short**: fewer
  than min(k, R) hits; **gross miss**: the exact top 1 is absent; **similarity gap**: mean exact
  top-min(k,R) similarity minus mean returned similarity;
- **complete** as wardowl reports it, and the 2x2 confusion of complete against maximal;
  **false-completeness rate** = share of results with complete = True that are not maximal;
- X5: **shortfall** (first search short) and **trigger rate** (share of retrievals whose first
  search came back short, so that the arm counted); **repair rate** (fallback `exact` or
  `widened`); **detection rate** = share of truly short first searches flagged `missed`; **false
  alarm** = flagged `missed` while the first search was not truly short;
- **latency** (ms) end to end and in the store, p50, p95, p99 over queries of the per-query
  median of three passes; for X5 also on triggered retrievals (`shortfall_ms`); **QPS** as above.

Safety, in every setting and arm: every hit is checked by wardowl's re-check and by an
independent oracle (E: the scenario's `readable` and canary detector; M: the subject's grant
evaluated on the row's layout arrays in NumPy). An unreadable hit, a canary of an unreadable
document or a violation stops the job and is reported as a leak.

## 7. Statistics

- **Unit:** the (query, subject) pair. A pair's metric in a setting is its mean over the builds
  that setting ran on.
- **Intervals:** 95% percentile intervals from a cluster bootstrap over subjects (E: people; M:
  subjects, resampled within each (seed, family, level, shape) stratum, a C subject carrying its P
  and N queries together), 10,000 resamples (1,000 in the smoke run), seed 20261029.
- **Differences between settings or arms** of one store: per pair on the same queries and builds,
  the same bootstrap; an interval "excludes 0" when both ends have the same sign. Alongside: the
  Wilcoxon signed-rank test (normal approximation, zeros dropped) on per-pair recall, and McNemar's
  exact test on binary outcomes (empty, short, maximal). Verdicts use the rules below only.
- **Differences between regimes** (U against N): independent subject groups, each resampled in
  its strata, difference of means.
- **Seeds:** every M criterion below that names a direction must also hold in sign in at least 4
  of the 5 seeds (the same estimate computed per seed).
- **Builds:** the range and standard deviation of recall@10 over builds are reported per setting.
- **Latency** is compared only within a job; across stores only recall is compared.

## 8. Hypotheses and how each verdict is decided

A verdict is **confirmed** when its confirming rule holds, **falsified** when its falsifying rule
holds, and **inconclusive** otherwise, including when data a rule needs are missing (a store or
setting unsupported, failed, or cut by time), or event counts are below a stated minimum. The
"approximate stores" are the ten stores other than FAISS. The statistics script applies these
rules and nothing else; a rule that proves impossible to apply as written is reported as a
deviation, not rewritten.

### X2

**H2.1 Negative correlation costs recall at the defaults.** M, setting `default`, both shapes,
s in {2%, 10%, 30%} pooled. Per store, G = recall@10(U) - recall@10(C, N). A store shows a **gap**
when G >= 0.05, its interval excludes 0, and G > 0 in at least 4 of 5 seeds; **no gap** when
|G| < 0.02 and its interval lies within (-0.03, 0.03). *Confirmed* when at least 6 stores show a
gap; *falsified* when at least 5 show no gap. Prediction: confirmed.

**H2.2 Local axes predict recall better than global selectivity.** M, `default`, all cells. Per
store, D = |Spearman(recall@10, rho_1000)| - |Spearman(recall@10, sigma_g)| over pairs. A store is
**assessable** when at least 100 pairs have recall@10 below 1; **local** when D >= 0.05 with an
interval above 0; **global** when D < 0 with an interval below 0. *Confirmed* when at least 4
stores are assessable and at least two thirds of them are local; *falsified* when at least half of
the assessable stores are global. The same statistic for ACORN correlation, GLS, alpha_hat,
rho_100 and log r1 is reported, without a verdict. Prediction: confirmed.

**H2.3 Search effort narrows the correlation gap but does not close it.** For each store with a
gap in H2.1 and a sweep: at the sweep's highest level, (i) the gap is smaller than at the default
(G_default - G_max > 0 with an interval excluding 0) and (ii) still G_max >= 0.02 with an interval
above 0. *Confirmed* when (i) and (ii) hold for at least half of these stores and there are at
least 3 of them; *falsified* when G_max < 0.01 for at least half of them. Reported with it: for
U and N, the lowest sweep level reaching recall@10 >= 0.95 (pooled s 2% to 30%), and the QPS at
that level. Prediction: confirmed.

**H2.4 The hardest filters are the intermediate ones.** M, `default`, C with N queries, groups
shape. Per store, V = recall@10 at s = 0.06% minus the lowest recall@10 among s in {0.5%, 2%,
10%}. A store is **U-shaped** when V >= 0.05 with an interval above 0 (exact or brute-force
fallbacks for small filters); **monotone** when V <= 0. *Confirmed* when at least 5 stores are
U-shaped; *falsified* when at least 5 are monotone. Prediction: confirmed (pgvector's planner,
Qdrant's full-scan threshold, Weaviate's flat-search cutoff, Redis's ad hoc brute force,
Lucene's exact search below its visit limit).

### Validity checks (no hypothesis; failures are reported and their data flagged)

- **V1** Every exact setting, and FAISS, reaches recall@10 >= 0.999 on every pair it ran.
- **V2** On E's original 1,105 questions, each store's as-run setting reproduces the scenario
  run's recall@10 (X0: Redis 0.980, Elasticsearch 0.948, OpenSearch 0.938, Weaviate 0.892, Chroma
  0.883, LanceDB 0.860, pgvector 0.732, Qdrant 0.561, FAISS 1.000) within 0.03, for at least 7 of
  these 9 stores. (Differences expected: CPU float32 against GPU float16 embeddings, and fresh
  builds.)
- **V3** No leak, unreadable hit, canary or violation anywhere.
- **V4** For at least 90% of M subjects at s >= 0.5%, measured selectivity lies within 25% of the
  nominal level (relative).
- **V5** pgvector: the share of searches whose plan uses the HNSW index is reported per setting
  and cell (EXPLAIN of each first-pass search with the search's own settings); nothing is excluded,
  since the plan PostgreSQL chooses is the store's documented behaviour.

### X5

Counts below pool k = 5 and k = 10 retrievals of pass 1 unless stated.

**H5.1 A count certifies short results without false alarms.** Arm `count`, each (store, corpus)
with at least 10 truly short first searches: (a) no false alarm; (b) detection rate >= 0.99;
(c) every result flagged `exhausted` holds min(k, R) hits. *Confirmed* when (a), (b) and (c) hold
for every such (store, corpus) and there is at least one; *falsified* when any has a false alarm
or a detection rate below 0.95. Prediction: confirmed (the count is exact and the filters have no
false denials).

**H5.2 Exact repair removes empty and short results.** pgvector, E and M, `exact-inf` against
`report` on the same queries: (a) no scorable retrieval empty or short under `exact-inf`;
(b) recall@10 on triggered retrievals >= 0.999. *Confirmed* when both hold on every corpus where
`report` has at least 10 short results; *falsified* when either fails on such a corpus.
Prediction: confirmed. Qdrant is judged the same way only where its `report` arm has 10 short
results.

**H5.3 The repairs cost nothing on untriggered queries.** For each repair arm (count, exact-*,
widen) against `report`, same job: the median over untriggered pairs of the latency ratio (median
of three passes, k = 10) lies in [0.95, 1.05]. *Confirmed* when this holds for every repair arm of
both stores on both corpora; *falsified* when some arm's median ratio exceeds 1.10. Prediction:
confirmed.

**H5.4 Repairs do not touch mis-retrieval.** Qdrant on E, as-run layout: the false-completeness
rate at k = 10 under `report` is at least 0.20, and every repair arm's false-completeness rate
differs from `report`'s by less than 0.02 with an interval inside (-0.03, 0.03). *Confirmed* when
both hold; *falsified* when `report`'s rate is below 0.05, or a repair arm lowers it by 0.05 or
more with an interval excluding 0. Prediction: confirmed (X1: recall@10 0.619, no short results).

**H5.5 The recall monitor sees what complete cannot.** Arm `monitor`: (a) the sampled share of
pre-filtered retrievals lies inside the 99.9% binomial interval around 0.01, for each (store,
corpus); (b) on sampled retrievals, `sampled_recall` (id-based, against the store's own exact
search) agrees with the harness's id-based recall against NumPy exact search within 0.1 for at
least 95% of them, pooled; (c) for Qdrant on E and on M, the mean `sampled_recall` lies within
0.05 of the arm's mean id-based recall over all its retrievals. *Confirmed* when (a), (b) and (c)
hold; *falsified* when (b)'s agreement is below 80% or (c)'s difference exceeds 0.10 anywhere.
Prediction: confirmed, with wide intervals on E (about 45 samples per build).

**H5.6 Widening is not a certificate.** pgvector, E and M pooled, triggered retrievals: recall@10
under `exact-inf` minus under `widen` is at least 0.01 with an interval above 0. *Falsified* when
the difference is below 0.002 with an interval containing 0. Needs at least 20 triggered
retrievals in both arms, else inconclusive. Prediction: confirmed only weakly; a widened scan of
up to a million tuples may find every readable row on M.

**H5.7 Store-native layout fixes what library repairs cannot.** Qdrant on E: recall@10 of the
per-tenant layout >= 0.90 (X1: 0.943) while every library arm on the as-run layout stays <= 0.75.
*Falsified* when the per-tenant layout is below 0.85 or a library arm exceeds 0.85. Prediction:
confirmed. The other native arms (pgvector's raised tuple limit alone, Qdrant's ACORN alone) are
reported against the library arms on recall, empty-result rate, false completeness and latency,
without a verdict.

### Reported without a verdict

Every frontier; recall by measured axis (bins: sigma_g by decade; rho_1000 in {0, (0, 0.01],
(0.01, 0.1], (0.1, 0.5], (0.5, 1]}; GLS below -0.3, -0.3 to 0.3, above 0.3; log10 r1 by unit;
ACORN correlation and alpha_hat by quintile); the P against N difference within C subjects;
groups against tenant shape; build-to-build ranges; load and index times; pgvector plan shares;
Qdrant's search-path counters where available.

## 9. Fixed in advance

- Seeds: 20261029 for the query pool, tenant field, subjects and bootstrap; layout seeds 0 to 4;
  E as the scenario (7) and X1's probe set (61).
- k = 10 for X2; k = 5 and 10 for X5; tie tolerance 1e-4; three timed passes; 20 warm-ups.
- The smoke configuration (a few thousand chunks, 2 seeds, 2 subjects per cell, one build) checks
  every code path and judges nothing.
- Raw results are JSON lines, one per retrieval; the statistics script writes CSV and Markdown and
  prints every verdict with the numbers behind each criterion.
