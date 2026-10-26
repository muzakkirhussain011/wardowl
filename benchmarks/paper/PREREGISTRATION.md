# Pre-registration: experiment X1, under-retrieval under permission filters

- **Date:** 2026-10-26.
- **Commit:** this file is committed alone, on branch `paper/x1-underretrieval`, with the message
  `bench: pre-register the predictions of the under-retrieval experiment`. Nothing else is in that commit.
- **When:** before the X1 harness was written and before any X1 or X0 result existed. The only data
  seen so far are the published aggregates of the Kaggle run of 2026-10-24 (wardowl 2.1.0, notebook
  `notebookd8377caca8`): per-store recall, latency, hits checked and the failed checks. Its
  per-question output (`answers.jsonl`) has not been analysed yet; that is experiment X0.
- **Specification:** the investigation `filtered-recall-gaps.md` of the paper workspace (not in this
  repository), sections 6.1 to 6.6. Its hypotheses, in one line each:
  - **Q1** Qdrant's filtered HNSW search is confined to an islanded permitted subgraph; there are no
    payload edges for the tenant, `employees` and `contractors` values, which are too common.
  - **Q2** ACORN was not enabled, and its default gate (`max_selectivity` 0.4) engages unreliably.
  - **Q3** Planning and payload edges are per segment, so recall varies with segment layout.
  - **Q4** `hnsw_ef` 128 was too low (expected to be a minor factor).
  - **P1** pgvector's iterative scan stops at `hnsw.max_scan_tuples` or at
    `work_mem x hnsw.scan_mem_multiplier` before reaching any readable row: the empty results.
  - **P2** pgvector's recall gap is mis-retrieval from shallow, relaxed scans in a sparse neighbourhood.
  - **P3** The planner overestimates how many rows a `judy` filter passes.
  - **P4** Generic plans after psycopg prepares the statement (expected to make no difference).

## The predictions (section 6.6)

| Hypothesis | Prediction that would confirm | Result that would falsify |
|---|---|---|
| Q1 | Qdrant recall about 1 for judys and low for KB readers on company-document questions; misses are KB passages; ACORN at 1.0 or per-tenant graphs give recall at least 0.9 | Misses spread evenly over categories, or ACORN and m=0 give no gain |
| Q2 | ACORN at 0.4 engages for only part of the people (telemetry) and recovers less than 1.0 does | ACORN at 0.4 and at 1.0 give the same recall |
| Q3 | Recall varies between builds and with the segment count | Identical across builds and segment counts |
| Q4 | `hnsw_ef` 512 gains less than 0.05 | Gains of more than 0.15 |
| P1 | Empties only when r1 exceeds the scan's reach; removed by raising the binding limit | Empties persist at 1M tuples and 16x memory |
| P2 | Recall rises with `ef_search`, inner `LIMIT` and index quality; losses concentrated at rho_100 below 0.1; small similarity gap | No change with `ef_search` 1000 |
| P3 | EXPLAIN shows an estimate of about 10 times the actual rows for judys; exact plans fix the empties | Estimates within 2x |
| P4 | No difference between plan modes | Recall or plan changes with plan mode |

## How each verdict is decided

`x1_stats.py` applies these rules and nothing else. A verdict is **confirmed** when every confirming
criterion holds, **falsified** when the falsifying rule holds, and **inconclusive** otherwise,
including when a setting a rule needs is missing, unsupported by the installed store, or skipped for
time. The rules were fixed before any result; if a rule proves impossible to apply as written, the
paper reports that as a deviation rather than changing the rule.

### Definitions

- **Questions:** the original run's 1,105 questions of 189 people (seed 7, 208 variants, all of FiQA),
  plus the probe set of section 6.1: for each of the 8 groups `hr`, `finance`, `board`,
  `engineering`, `sre`, `legal`, `contractors`, `employees`, one person holding only that group in
  each of 3 generated tenants (24 people), each asking the 12 template questions of their tenant
  and 4 FiQA queries (384 questions).
- **Person types:** `judy` = the 18 generated people whose only group is `board`; `kb-reader` = the
  original people with `employees` or `contractors`, who read the FiQA knowledge base; `no-groups` =
  `mallory`; `probe-<group>` = the probe people.
- **Company-document question:** a `targeted` or `generic` question whose kind the person may read
  (`answerable`), asked by a `kb-reader`.
- **Scorable:** the person may read at least one chunk (R >= 1). Recall, ERR and the short-result
  rate are computed over scorable questions only.
- **Metrics** (per question, person, setting and build): recall@5 and @10 as the original run
  defines them (tie-aware, 1e-4); ERR = no hits; short = fewer hits than min(k, R); gross miss = the
  exact top 1 is absent; similarity gap = mean exact top-k similarity minus mean returned similarity;
  latency = median of 3 passes of the k=5 retrieval; wardowl's `complete`.
- **Estimate and interval:** the mean over questions of each question's value averaged over the
  builds a setting ran on; 95% percentile interval from a cluster bootstrap over persons, 10,000
  resamples, seed 20261026. A **difference** between two settings is computed per question on the
  builds they share (or the same replicate index for build-time variants) and bootstrapped the same
  way. Its interval "excludes 0" when both ends have the same sign.
- **Settings** (ids used below). pgvector, on index family `hnsw-m16-efc64` unless stated:
  `p-asrun` (ef_search 100, relaxed order, server defaults: the original run),
  `pa-t{20,100,1000}k-m{1,8}` and `pa-t1000k-m16` (`hnsw.max_scan_tuples` x `hnsw.scan_mem_multiplier`),
  `pb-wm64` (`work_mem` 64 MB), `pc-ef{40,200,400,1000}`, `pd-lim{4,10}` (inner LIMIT factor),
  `pe-strict`, `pg-custom` (`plan_cache_mode=force_custom_plan`), `pg-noprepare` (psycopg
  `prepare_threshold=None`), `ph-exact` (`enable_indexscan=off`); index family `hnsw-m32-efc200`.
  Qdrant, on layout `as-run` unless stated: `q-asrun` (hnsw_ef 128, no ACORN: the original run),
  `qa-acorn040`, `qa-acorn100` (ACORN with `max_selectivity` 0.4 and 1.0), `qb-ef64`, `qb-ef512`,
  `qc-exact`; layouts `is-tenant`, `tenant-m0` (`is_tenant` plus `m=0`, `payload_m=16`),
  `separate-kb`, `one-segment`.

### Rules

**Q1.** Confirmed when all of:
(i) `q-asrun` recall@10 for `judy` >= 0.95;
(ii) `q-asrun` recall@10 on company-document questions <= 0.75, with its interval's upper end below
the lower end of the `judy` interval;
(iii) of the top-5 hits that do not count towards recall on those questions, at least half are
`kb/` passages;
(iv) recall@10 over all scorable questions >= 0.90 for `qa-acorn100` or for `q-asrun` on `tenant-m0`.
Falsified when the miss rate (1 - recall@10) under `q-asrun` differs by less than 0.10 between the
categories with at least 30 scorable questions, or when neither `qa-acorn100` nor `tenant-m0`
improves recall@10 over all scorable questions by 0.02 or more.

**Q2.** Confirmed when the share of people whose searches took the ACORN path at least once under
`qa-acorn040`, among people whose searches took a graph path (Qdrant's telemetry counters
`filtered_acorn` and `filtered_large_cardinality`), lies strictly between 0.05 and 0.95, and the
difference `qa-acorn100` minus `qa-acorn040` in recall@10 has an interval above 0. If the
telemetry does not expose the ACORN counter, the share is inferred as the people whose top 5 differ
between `qa-acorn040` and `q-asrun` on the same build, and the report says so. Falsified when that
difference is below 0.01 in absolute value and its interval contains 0.

**Q3.** Confirmed when recall@10 of `q-asrun` over all scorable questions ranges over at least 0.01
between the three `as-run` builds, and `one-segment` minus `as-run` (`q-asrun`) has an interval that
excludes 0. Falsified when the range is below 0.002 and that difference is below 0.002 in absolute
value. Inconclusive, whatever the numbers, when both layouts end with the same segment count.

**Q4.** `qb-ef512` minus `q-asrun` in recall@10 over all scorable questions: confirmed below 0.05,
falsified above 0.15, inconclusive in between.

**P1.** Inconclusive when `p-asrun` reproduces no empty result. Otherwise confirmed when all of:
(a) at least 95% of the empty results under `p-asrun` have r1 (the unfiltered rank of the first
readable chunk) above half the scan's reach, the reach being the median number of rows the index
emitted (`Actual Rows` plus `Rows Removed by Filter` of EXPLAIN ANALYZE) on those empty results, or
10,000 if no such EXPLAIN exists;
(b) one of `pa-t100k-m1`, `pa-t20k-m8`, `pa-t100k-m8`, `pa-t1000k-m1`, `pa-t1000k-m8`,
`pa-t1000k-m16`, `pb-wm64` has an ERR of at most 10% of the ERR under `p-asrun`;
(c) that median number of emitted rows lies between 10,000 and 25,000.
The report names the binding limit from the single-limit raises (`pa-t100k-m1`, `pa-t1000k-m1`
raise only tuples; `pa-t20k-m8`, `pb-wm64` raise only memory). Falsified when the ERR under
`pa-t1000k-m16` is at least half the ERR under `p-asrun`.

**P2.** Confirmed when all of:
(a) `pc-ef1000` minus `p-asrun` in recall@10 is at least 0.02 with an interval above 0;
(b) `pd-lim10` minus `p-asrun` has an interval above 0;
(c) `p-asrun` on `hnsw-m32-efc200` minus `p-asrun` on `hnsw-m16-efc64` has an interval above 0;
(d) under `p-asrun`, the loss rate (1 - recall@10) of questions with rho_100 below 0.1 is at least
twice the loss rate of the others;
(e) under `p-asrun`, the mean similarity gap at k=10 over the questions with recall@10 below 1 is at
most 0.02.
Falsified when `pc-ef1000` minus `p-asrun` is below 0.01 in absolute value and its interval
contains 0.

**P3.** For each `judy`, the planner's row estimate for the filter alone (`EXPLAIN SELECT 1 FROM t
WHERE <filter>`) divided by R. Confirmed when the median ratio is at least 5 and `ph-exact` has no
empty result. Falsified when the median ratio lies between 0.5 and 2.

**P4.** Confirmed when `pg-custom` and `pg-noprepare` each differ from `p-asrun` by less than 0.005
in recall@10 and by less than 0.002 in ERR, and EXPLAIN gives the same plan shape for every fixed
query on every shared build. Falsified when either differs from `p-asrun` in recall@10 by 0.01 or
more with an interval that excludes 0, or in ERR with McNemar p below 0.05, or when any fixed query
gets a different plan shape. The count of generic plans PostgreSQL used (`pg_prepared_statements`)
is reported with the verdict.

## Fixed in advance

- Corpus, people and questions exactly as `acceptance/kaggle/enterprise_rag.py` builds them at the
  original run's settings, with the probe set above (its draws use the fixed seed 61).
- Three builds per build-time configuration. Every pgvector setting runs on every build of
  `hnsw-m16-efc64`, and `p-asrun`, `pc-ef400`, `pa-t1000k-m8`, `pd-lim10` on every build of
  `hnsw-m32-efc200`. Every Qdrant setting runs on every build of `as-run`, and `q-asrun`,
  `qa-acorn040`, `qa-acorn100` on every build of the other layouts. `ph-exact` and `qc-exact` run
  on the first build of each family or layout only, since they do not use the graph.
- k=5 and k=10 retrievals for every question; the k=5 retrieval is timed in three passes.
- Every hit is re-checked by wardowl and by the scenario's own oracle and canary detector, in every
  setting; any unreadable hit, canary or violation stops the run.
- Paired comparisons, McNemar tests for ERR and Wilcoxon signed-rank tests on per-question recall
  are reported alongside the intervals; the verdicts above use only the rules as written.
