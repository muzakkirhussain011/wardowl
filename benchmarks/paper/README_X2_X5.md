# Experiments X2 and X5

X2 measures recall against throughput under permission-shaped filters in ten vector stores, with
FAISS flat as the exact reference. X5 measures how well wardowl's `short_results` (report, count,
exact, widen) and recall monitor detect and repair under-retrieval in pgvector and Qdrant, beside
the stores' own remedies. The design, the statistics and every verdict rule are fixed in
[`PREREG_X2_X5.md`](PREREG_X2_X5.md), committed before any of this code.

Everything runs in GitHub Actions ([`paper-x2-x5.yml`](../../.github/workflows/paper-x2-x5.yml)),
on hosted runners: nothing here needs a GPU.

## Files

| File | What it does |
|---|---|
| `PREREG_X2_X5.md` | The pre-registration: corpora, layouts, settings, arms, metrics, statistics, hypotheses |
| `x2x5_config.json` | What a push to `paper/x2-x5` runs: `mode` (`smoke` or `full`) and `data_run_id` |
| `x2x5_plan.py` | The workflow's job matrices (standard library only) |
| `x2x5_prepare.py` | `embed`: one shard of a corpus on the CPU; `prepare`: merge, check, layouts, subjects, exact baseline, axes |
| `x2x5_common.py` | Corpora, the oracle, the metrics, the measured axes and the sweep every setting runs through |
| `x2x5_stores.py` | One adapter per store: load, settings, backend per setting |
| `x2x5_services.sh` | Starts and waits for one store's container on a runner, and keeps its logs |
| `x2_frontiers.py` | X2: one store, its layouts and builds, every setting |
| `x5_mitigation.py` | X5: pgvector or Qdrant, every arm |
| `x2x5_stats.py` | Tables, cluster-bootstrap intervals, paired tests and the pre-registered verdicts |

## How a run goes

1. `plan` reads `x2x5_config.json` (or the dispatch inputs) and writes the matrices.
2. `embed-e` (6 shards, bge-base-en-v1.5) and `embed-m` (8 shards, bge-small-en-v1.5) embed the
   two corpora on CPUs; each shard records the SHA-256 of its vectors and of the ids it embedded.
3. `prepare-e` and `prepare-m` build each corpus again, check every shard against it, merge them,
   embed the queries, draw M's layouts and subjects, compute the exact top 10 and the measured axes
   of every (query, subject) pair, and upload `x2x5-data-<corpus>` with `checksums.json`.
4. `x2-e`, `x2-m`, `x5-e`, `x5-m` call `paper-x2-x5-store.yml` once per store (E: one job per
   store, its three builds in turn; M: one job per store and build). Each job verifies the data's
   checksums before loading anything.
5. `stats` applies the rules; `publish` commits the reports, the job records and the last 200
   lines of every job's log to the branch `results/x2-x5`, under `<run id>-<attempt>/`.

The raw rows (one JSON line per setting and pair) stay in the run's artifacts
(`x2x5-res-<experiment>-<corpus>-<job>`, 90 days).

## Reusing the data of an earlier run

Embedding takes about an hour of runner time. To rerun the stores on the same vectors, set
`data_run_id` in `x2x5_config.json` (or the dispatch input) to the run that made them: the data
jobs are skipped and every store job downloads `x2x5-data-<corpus>` from that run, checking its
checksums. Artifacts expire after 90 days.

## Reading the results

```bash
git fetch origin results/x2-x5
git log --oneline origin/results/x2-x5
git show origin/results/x2-x5:<run>/RUN.md
git show origin/results/x2-x5:<run>/stats/report.md
```

`stats/` holds `verdicts.json`, `report.md` and the CSV tables (`x2_settings`, `x2_frontier`,
`x2_axes`, `x2_builds`, `x2_pgvector_plans`, `x2_h21` to `x2_h24`, `validity`, `x5_arms`,
`x5_confusion`, `x5_paired_tests`); `jobs/` each job's `job.json` (load times, settings as the
store reported them, failures, skipped settings) and summary; `logs/` the log tails.

## Settings the harness sets itself

Reported as harness-level in every setting record: pgvector's plan control (psycopg
`prepare_threshold=None`, so PostgreSQL plans each search with its values; X1 run 1 found generic
plans that skip the HNSW index); Elasticsearch's and OpenSearch's exact `script_score`;
OpenSearch's `method_parameters.ef_search`; Redis's `HYBRID_POLICY` and its `search-on-timeout
fail` and `search-timeout 60000`; LanceDB's post-filtering and `bypass_vector_index()`;
Weaviate's `ef`, filter strategy and flat-search cutoff (collection configuration, read back
before each setting runs); Chroma's `ef_search` (collection configuration); Qdrant's per-tenant
layout. pgvector loads by binary COPY and LanceDB by `table.add`, in the backends' own layouts;
every other store loads through its wardowl backend's `add`.

## Smoke run

`mode: smoke` builds E from 4 variants per template and 2,000 FiQA passages (about 3,000 chunks)
and M from 20,000 passages with 2 layout seeds, 2 subjects per cell and 2 queries per subject; one
build per store, 25 minutes per job. It exercises every code path and judges nothing.
