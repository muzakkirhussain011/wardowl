# The paper's experiments

Scripts for the experiments of the wardowl paper. The first, **X1**, asks why two stores fell short
in the enterprise RAG acceptance run of 2026-10-24 (wardowl 2.1.0, Kaggle, 107,540 chunks, 189
people): Qdrant reached recall@10 0.561, and pgvector returned nothing at all to ten board members
who could read documents, while wardowl reported every result complete. Its specification is the
investigation `filtered-recall-gaps.md` of the paper workspace (sections 6.0 to 6.6). Its
predictions, and the exact rules that turn the data into confirmed, falsified or inconclusive, were
committed before any code or result in [`PREREGISTRATION.md`](PREREGISTRATION.md).

Everything runs on Kaggle (2 x T4, 4 CPUs, 31 GB, 12-hour sessions), from
[`x1_underretrieval.ipynb`](x1_underretrieval.ipynb). Nothing here needs to run on a laptop.

## Files

| File | What it does | Reads | Writes |
|---|---|---|---|
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | The predictions of section 6.6 and the rules that judge them, dated 2026-10-26 | | |
| [`paper_common.py`](paper_common.py) | Shared helpers: logging to a file, finding the original run's output under `/kaggle/input`, importing `acceptance/kaggle/enterprise_rag.py`, person types, tidy tables, the manifest | | |
| [`x0_reanalysis.py`](x0_reanalysis.py) | **X0** (section 6.0, items 1 to 3), offline, CPU only: pgvector's empty results; approximate recall@5 per store by category and person type (overlap with FAISS's exact top 5); the share of `kb/` passages in each store's top 5 against FAISS's on targeted questions | `answers.jsonl`, `results.json` of the original run | `/kaggle/working/x0/` |
| [`x1_underretrieval.py`](x1_underretrieval.py) | **X1** (sections 6.1 to 6.5), retrieval only: the probe set, the alignment variables, the pgvector grid P-a to P-h and the Qdrant grid Q-a to Q-e, every metric per (setting, build, question) | the scenario of `acceptance/kaggle/enterprise_rag.py`; cached embeddings if attached | `/kaggle/working/x1/` (or `x1-smoke/`) |
| [`x1_stats.py`](x1_stats.py) | Statistics: cluster-bootstrap intervals over persons, paired comparisons, McNemar for the empty-result rate, Wilcoxon on per-question recall, and the verdict on each prediction | `/kaggle/working/x1/` | `/kaggle/working/x1/stats/` |
| [`x1_underretrieval.ipynb`](x1_underretrieval.ipynb) | The Kaggle notebook: installs the stores and packages as the original notebook does, installs wardowl from this branch, runs X0, X1 smoke (and its statistics), X1 on pgvector, X1 on Qdrant, then the statistics | | |

## Run it on Kaggle

1. **Import the notebook.** On Kaggle, *Create, New Notebook*, then *File, Import Notebook*, and paste
   `https://github.com/muzakkirhussain011/wardowl/blob/paper/x1-underretrieval/benchmarks/paper/x1_underretrieval.ipynb`.
2. **Settings.** Accelerator *GPU T4 x2*; *Internet on*.
3. **Input.** *Add Input*, *Your Work*, *Notebooks*: the original run, `notebookd8377caca8`. X0 needs
   its `answers.jsonl` and `results.json`; X1 copies its cached embeddings (`cache/chunks-*.npy`)
   and so skips about ten minutes of embedding. Without this input X0 fails (the other steps still
   run) and X1 embeds the corpus again.
4. **Run.** *Save Version*, *Save & Run All (Commit)*. The steps run in order; the smoke run is a
   gate: if it or its statistics fail, the notebook stops before the long run.
5. **Read the results.** In the version's *Output*: `x0/summary.md`, `x1/stats/report.md` (the
   verdicts), and the tables beside them. The manifests list every setting that was unsupported,
   skipped for time or failed.

**If the session ends early,** start a new version with the earlier version's output added as input
as well. The notebook copies its `x1/` folder, and X1 (with `--resume`) skips every build that
finished. A build left half done is redone from a fresh build, because a rebuilt graph is a
different graph; its partial results are moved to `x1/discarded/`. A setting that failed counts as
finished (retrying it means rebuilding its whole build); `--retry-failed` redoes such builds.

### Expected time

| Step | Estimate |
|---|---|
| Clone, install, PostgreSQL and pgvector built from source | 5 to 10 min |
| X0 | under 1 min |
| X1 smoke and its statistics | 15 to 25 min |
| X1 pgvector: load, 3 builds x 18 settings of the default index, 3 builds x 4 settings of m=32/ef_construction=200 | about 3 to 3.5 h |
| X1 Qdrant: 5 layouts x 3 builds, 6 settings on as-run and 3 on the others | about 2.5 to 3 h |
| Statistics | 5 to 10 min |

About 6.5 to 7.5 hours in all. These are estimates from the original run's latencies (pgvector p50
6.5 ms, Qdrant 4.3 ms, loads of 1 to 2 minutes); the slow settings are exact search, `ef_search`
1000, ACORN at 1.0 and the `tenant-m0` build. `--deadline` (the session's start plus 11.25 h) and
`--max-hours` (5.5 h for the pgvector cell) stop X1 from starting a setting it cannot finish; what
is left out is recorded as skipped, never silently dropped.

## X1 in detail

**Scenario.** `enterprise_rag.Run` builds the corpus, people and questions, embeds them and computes
the exact baseline exactly as the original run did (seed 7, 208 variants, all of FiQA,
BAAI/bge-base-en-v1.5). The language model is not loaded. X1 adds:

- **The probe set** (section 6.1): for each of `hr`, `finance`, `board`, `engineering`, `sre`,
  `legal`, `contractors`, `employees`, one person holding only that group in 3 generated tenants
  (24 people), each asking the 12 template questions of their tenant and 4 FiQA queries (384
  questions; draws seeded with 61).
- **Alignment variables** of every (question, person), from exact ranking on the GPU: `R` (chunks
  the person may read), `R_kb` (of which FiQA), `r1`, `r5`, `r10` (unfiltered rank of the first,
  fifth and tenth readable chunk), `rho100`, `rho1000` (readable share of the 100 and 1,000
  unfiltered nearest).

**pgvector** (section 6.2). PostgreSQL 16 and pgvector 0.8.7 from `benchmarks/kaggle_setup.sh` with
`PG_TUNE=1`, loaded by `enterprise_rag.PgVectorStore.load` (wardowl's `create_schema` and `add`, then
the HNSW index with pgvector's defaults). Query-time settings, on every build of the default index:

| Id | Experiment | Setting |
|---|---|---|
| `p-asrun` | reference | `ef_search` 100, relaxed order, server defaults: the original run |
| `pa-t{20,100,1000}k-m{1,8}`, `pa-t1000k-m16` | P-a | `hnsw.max_scan_tuples` x `hnsw.scan_mem_multiplier` |
| `pb-wm64` | P-b | `work_mem` 64 MB |
| `pc-ef{40,200,400,1000}` | P-c | `hnsw.ef_search` |
| `pd-lim{4,10}` | P-d | the CTE's inner LIMIT at 4k and 10k, outer LIMIT k |
| `pe-strict` | P-e | `hnsw.iterative_scan = strict_order` |
| `pg-custom`, `pg-noprepare` | P-g | `plan_cache_mode = force_custom_plan`; psycopg `prepare_threshold=None` |
| `ph-exact` | P-h | `enable_indexscan = off` (first build only) |

`pa-t20k-m1` would be pgvector's default limits, so it is `p-asrun`.

Build-time variant P-f: the index rebuilt with `m=32, ef_construction=200`, three times, with
`p-asrun`, `pc-ef400`, `pa-t1000k-m8` and `pd-lim10`. Instrumentation: `EXPLAIN (ANALYZE, BUFFERS,
FORMAT JSON)` on every short result (up to 200 per setting) and on 50 fixed questions (15 judy, 25 KB
reader, 10 probe, seeded), the fixed ones also with `EXPLAIN (GENERIC_PLAN)`, the plan PostgreSQL
would use once it switches to a generic plan; the planner's estimate for each person's filter alone;
and how often PostgreSQL ran the search statement with a generic and with a custom plan
(`pg_prepared_statements`, search statement only; see amendment 1 of the pre-registration).

**Qdrant** (section 6.3). Qdrant 1.19.2 from `benchmarks/kaggle_stores.sh`. Layouts, each built three
times: `as-run` (`enterprise_rag.QdrantStore.load`), `is-tenant`, `tenant-m0` (`is_tenant` plus `m=0`,
`payload_m=16`), `separate-kb` (company documents and the FiQA base in two collections, merged by
score) and `one-segment`. Settings: `q-asrun` (hnsw_ef 128, the original run), `qa-acorn040` and
`qa-acorn100` (ACORN with `max_selectivity` 0.4 and 1.0), `qb-ef64`, `qb-ef512`, and `qc-exact`
(first build only); the layouts other than `as-run` run the first three and `qc-exact`.
Instrumentation: collection info after each build (`segments_count`, `indexed_vectors_count`, the
config), the raw `/telemetry` document after each build, and the per-segment search-path counters
(`filtered_small_cardinality`, `filtered_large_cardinality`, `filtered_acorn`, ...) per person.

**Metrics** (section 6.5), per (setting, build, question): recall@5 and @10 (the original run's own
tie-aware recall), empty and short results, gross miss (the exact top 1 absent), similarity gap,
target found, `kb/` share, the top-5 hits that do not count towards recall and how many are `kb/`,
latency (median of 3 timed passes of the k=5 retrieval, and the backend's share from wardowl's
`RetrievalEvent`), wardowl's `complete` and its confusion against the exact answer, and whether the
top 5 changed between passes.

**Safety.** Every retrieval goes through `PermissionedRetriever`, which re-checks every hit. Every hit
is checked again against the scenario's oracle (`readable`) and canary detector. One unreadable
hit, one canary of an unreadable document or one violation stops the run with exit code 3 and
`LEAK.json`.

### Settings wardowl does not expose (harness-level)

These are set by the harness on the store itself, and marked as harness-level in each setting's
record:

- pgvector: `hnsw.max_scan_tuples`, `hnsw.scan_mem_multiplier`, `work_mem`, `enable_indexscan` and
  `plan_cache_mode`, as `SET LOCAL` in the search's own transaction, by a subclass of
  `PgVectorBackend` (`HarnessPgVector`) that adds them to the backend's own two; the inner LIMIT
  factor, in the same subclass's SQL; psycopg's `prepare_threshold`, on the connection pool; the
  index build parameters `m` and `ef_construction` (`create_schema` takes neither).
- Qdrant: the collection layouts (`is_tenant`, `m=0` with `payload_m`, the second collection and
  the merge, `default_segment_number`). `hnsw_ef`, `exact` and ACORN go through
  `QdrantBackend(search_params=...)`, which wardowl passes to Qdrant unchanged.

A setting the installed store or client refuses, or silently ignores (checked with
`current_setting` inside the search's transaction for pgvector, and with a probe query for Qdrant),
is recorded as unsupported in the manifest and in its record, and said loudly in the log.

### Choices the plan left open

- **No KB-only person.** Every group that reads the FiQA base (`employees`, `contractors`) also
  reads at least two handbook templates, so section 6.1's KB-only people cannot exist without
  changing the original metadata. The `contractors` and `employees` probes are the closest; `R_kb`
  and `R` are recorded per question.
- **Question order.** People take turns in a seeded order, each asking all their questions, so
  that Qdrant's counters can be read per person. The original run shuffled questions.
- **Latency.** Three full passes of the k=5 retrieval, the median per question; k=10 runs once.
- **One connection per pgvector setting** (a fresh pool of one), so prepared statements and the
  plans PostgreSQL chose for them can be read; the original used a pool of up to four.
- **Qdrant readiness.** After the original's wait for a green status, X1 also waits until the
  point, indexed-vector and segment counts stay the same for 15 seconds.
- **`one-segment`** also raises `max_segment_size` to 1,000,000 KB, so the optimizer can merge the
  330 MB of vectors into one segment; the segment counts reached are recorded.
- **Exact search** runs once per graph-independent case: `ph-exact` on the first build of the
  default index only (it does not use the index), `qc-exact` on the first build of each layout.
- Not done: the optional pgvector build with `-DHNSW_MEMORY` (section 6.2), and the OPA and
  OpenFGA passes of the original run, which test authorizers rather than stores.

## Outputs of X1

| Path | Content |
|---|---|
| `manifest.json` | One entry per invocation: options, versions, hardware, seeds, every stage's time and status, every setting's definition, and the unsupported, skipped and failed lists |
| `x1.log` | The log, warnings framed in `!` |
| `questions.parquet`, `people.csv` | Every question with its person, type, category, the alignment variables and the exact top 10 |
| `fixed_queries.csv` | The fixed EXPLAIN questions |
| `query_vectors.npy` | The query vectors every invocation into this folder uses, so the pgvector and Qdrant cells share one exact baseline |
| `runs/<store>__<layout>__<build>__<setting>.parquet` | One row per question: every metric of section 6.5 and the hit ids |
| `meta/...json` | Each setting's status, effective settings, timings, errors, prepared statements, ACORN counts; written last, so it marks the setting done |
| `builds/...json` | Each build: how it was built, time, index size or Qdrant collection info and segments |
| `explain/...parquet`, `explain_raw/...jsonl.gz` | pgvector's EXPLAIN, parsed and raw |
| `pg_filter_estimates.parquet` | The planner's row estimate for each person's filter, against R |
| `telemetry/...parquet`, `telemetry_raw/...json.gz` | Qdrant's search-path counters per person; the raw telemetry after each build |
| `stats/` | `x1_stats.py`'s tables, `report.md` and `predictions.csv` |

Tables are Parquet, or CSV if pyarrow is missing (said in the log). Exit codes: 0 done; 1 done, with
failed settings or stages (see the manifest); 3 a leak or violation stopped the run.

## Running a script by hand

```bash
python benchmarks/paper/x0_reanalysis.py --input /path/to/original/output --out x0
python benchmarks/paper/x1_underretrieval.py --smoke --out x1-smoke   # needs PostgreSQL, Qdrant's script, a GPU
python benchmarks/paper/x1_underretrieval.py --stores pgvector --resume --deadline <unix time>
python benchmarks/paper/x1_stats.py --in x1 --resamples 10000 --seed 20261026
```

`x1_underretrieval.py --help` lists every option (`--builds`, `--passes`, `--layouts`,
`--explain-fixed`, `--explain-short-cap`, `--max-hours`, `--retry-failed`, `--cache`, `--repo`).
