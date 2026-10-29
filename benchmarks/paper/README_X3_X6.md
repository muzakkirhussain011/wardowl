# Experiments X3 and X6

Two experiments of the wardowl paper, run entirely in GitHub Actions by the workflow
[`paper-x3-x6`](../../.github/workflows/paper-x3-x6.yml). Their hypotheses, predictions and the rules
that turn the data into confirmed, falsified or inconclusive were committed before any code or result
in [`PREREG_X3_X6.md`](PREREG_X3_X6.md) (commit 5da58ee, 2026-10-29).

- **X6, side channels.** Can an authenticated subject tell whether unreadable chunks lie near a query
  from what wardowl returns (hits, scores, count, `complete`) or how long it takes? A distinguishing
  game between two worlds that differ only in where m unreadable chunks lie (W1: next to the probe;
  W0: far away), on FiQA with all-MiniLM-L6-v2 embeddings, for widening post-filtering, approximate
  pre-filtering (pgvector, Qdrant, Elasticsearch), BM25 and hybrid statistics, and the controls
  (FAISS flat, in-memory), with four mitigations: constant-work widening, exact pre-filtering,
  per-tenant separation and latency padding.
- **X3, filter-size scaling.** How do 12 stores and two in-process controls behave when the
  permission filter is a disjunction over 1 to 40,000 groups, at a fixed 10% readable share:
  translation, acceptance (with the exact error), latency p50/p95/p99 and recall@10.

## Files

| File | What it does |
|---|---|
| [`PREREG_X3_X6.md`](PREREG_X3_X6.md) | The pre-registration: design, hypotheses, numeric rules, statistics, inconclusive conditions |
| [`x3x6_common.py`](x3x6_common.py) | Shared: records (JSON lines), run information, annotations, the data files, one adapter per store that builds an index and hands back wardowl backends, bootstrap helpers |
| [`x6_data.py`](x6_data.py) | The data job: downloads BEIR FiQA and SciDocs, embeds them on the CPU, computes X6's plans (probes, near sets, far chunks, buckets, exact answers) by exact search, so every store plays the identical game |
| [`x6_side_channels.py`](x6_side_channels.py) | X6 on one store: builds W0, W1 and SEP per seed, plays the game through wardowl's public API, writes `x6-<store>.jsonl` |
| [`x3_filter_scaling.py`](x3_filter_scaling.py) | X3 on one store: one index of 100,000 vectors per seed, every G level, writes `x3-<store>.jsonl` |
| [`x6_stats.py`](x6_stats.py), [`x3_stats.py`](x3_stats.py) | Statistics: cluster-bootstrap intervals, paired comparisons, the guards and the pre-registered verdicts; CSV tables and a Markdown report |

## The workflow

A push to `paper/x3-x6` starts it; the size comes from `X3X6_MODE` at the top of the workflow:

- **smoke**: 6,000 FiQA passages, one seed, one repetition, 3 to 7 queries or probes per level. It
  exists to find faults in the harness in minutes; its numbers are never analysed or reported.
- **full**: the pre-registered design.

Jobs:

1. **data** embeds the corpus and computes the plans (artifact `x3x6-data`).
2. **12 parallel jobs**, one per store family and experiment arm: `x6-pgvector`, `x6-qdrant`,
   `x6-elasticsearch`, `x6-faiss`, `x6-memory`, `x3-pgvector-redis`, `x3-cassandra`, `x3-search`
   (Elasticsearch, OpenSearch), `x3-vespa-qdrant`, `x3-milvus-weaviate`, `x3-mongodb`, `x3-embedded`
   (Chroma, LanceDB, FAISS, in-memory). Each starts its servers (the conformance campaign's images and
   versions), installs from `uv.lock` by hash, runs each target in its own process with its own time
   budget, and uploads `x3x6-results-<group>` whatever happened (records, logs, server logs).
3. **summary** runs both statistics scripts and writes `x3_report.md` and `x6_report.md` to its job
   summary, uploads them (artifact `x3x6-reports`), and prints the health, verdicts and headline cells
   as annotations.
4. **publish** commits the reports and CSV tables, the data job's manifest, the result of every job
   (`jobs.json`), crash records and the last 200 lines of every job's and server's log to the branch
   `results/x3-x6`, in the folder `<run id>-<attempt>/`. They can then be read with git alone, which
   has no API rate limit:

   ```
   git fetch origin results/x3-x6
   git show origin/results/x3-x6:<run id>-<attempt>/reports/x6_report.md
   ```

   The raw JSON lines stay in the artifacts `x3x6-results-*` (90 days), which are too large for git.

### Expected time (full)

| Job | Estimate |
|---|---|
| data | 30 to 60 min (about 76,000 texts embedded on 4 CPUs) |
| x6-pgvector, x6-qdrant | about 2 to 2.5 h each (3 builds of about 57,600 chunks per seed, about 26,000 retrievals per seed) |
| x6-elasticsearch | about 3 h (7 configurations) |
| x6-faiss, x6-memory | about 1.5 to 2 h each (pre-filtering and in-memory search scan the corpus in Python) |
| x3 jobs | 1 to 3 h each (5 builds of 100,000 vectors; pgvector at 40,000 groups takes seconds per query) |
| summary | 10 to 30 min (10,000 bootstrap resamples per cell) |

About 4 to 5 hours of wall time in all. Every job stops starting seeds when its budget runs out and
records what it skipped; a skipped seed makes the verdicts that need it inconclusive, and is never
silently dropped.

## Reading the results

- `x6_report.md`: health (seeds done, errors, build times), the verdicts, the guards (A/A null and
  exactness), the paired AUC of each observable per (store, configuration, m), the mitigations' costs
  and the id-list change rates. AUC 0.5 is no advantage; the paired AUC is the attacker who compares
  the same probe before and after; advantage is 2 x AUC - 1.
- `x3_report.md`: health, verdicts, then per (store, G) the outcome, latency percentiles, recall,
  translation status and time, and the first error message; latency ratios and recall differences
  paired by query.
- The CSV files beside them hold every cell with its interval, for the paper's tables and figures.

## Design decisions worth knowing

- **Far chunks come from another domain** (SciDocs) and are cut or extended to the same word count as
  the passage they replace, so the corpus size and total length match and BM25's length
  normalisation cannot tell the worlds apart; only the content differs.
- **Probes are placed so that no probe's secrets lie within another probe's zone** (its m + 1,000
  nearest passages), so each probe sees exactly its own m secrets within the depth the layer explores.
- **W0, W1 and SEP are live at once and queried in a fresh random order in every repetition**, so time
  drift, caches and garbage collection affect every world alike; SEP queried twice gives the A/A null
  that guards every latency verdict.
- **Exact pre-filtering** is measured with pgvector's index scans off, Qdrant's `exact=True`, and an
  Elasticsearch `script_score` backend written for the harness (a subclass of wardowl's
  `ElasticsearchBackend`): wardowl has no exact switch for Elasticsearch.
- **Qdrant's indexing threshold is lowered** so that every segment of these small collections has an
  HNSW graph, as a production collection's segments do; without it, small segments are searched
  exactly and the approximate behaviour under test would not be exercised.
- **Redis is queried over RESP3**, so a query its 500 ms default timeout cuts short comes back with a
  warning, which wardowl turns into an error, instead of passing for a complete result.
- **Latency padding is evaluated offline** from the measured latencies (an ideal padder; scheduler
  jitter is not modelled), with its budget fixed on seed 0 and its effect judged on seeds 1 to 4.
