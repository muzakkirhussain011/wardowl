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

## Amendment 1 (2026-10-26, before any result)

Made the same day, after a review of the harness and before any X0 or X1 result existed. It is
committed on its own with the message `bench: amend the pre-registration before any result exists`,
so the rules above stay readable as first written.

1. **P4's plan criterion is replaced.** As first written, it compared the plan shapes EXPLAIN shows
   under `p-asrun`, `pg-custom` and `pg-noprepare`. EXPLAIN with bound values always plans with
   those values (a custom plan), whatever `plan_cache_mode` or psycopg's preparing does to the
   search itself, so those shapes cannot differ and the criterion could neither confirm nor falsify
   anything. Instead, under `p-asrun`: count how often PostgreSQL ran the search statement with a
   generic plan (`pg_prepared_statements`, search statement only), and for each fixed question
   compare the generic plan (`EXPLAIN (GENERIC_PLAN)`) with the custom plan (EXPLAIN ANALYZE with
   the values). The plan part of P4 is confirmed when no generic plan of the search statement ran,
   or when no fixed question's generic plan has another shape; it is falsified when some ran and
   some fixed question's generic plan has another shape. The recall and ERR parts of P4 are
   unchanged. The count of generic plans reported with the verdict is the search statement's only:
   psycopg also prepares the `SET LOCAL` statements, which always run with a generic plan.
2. **`ph-exact` runs on the first build of `hnsw-m16-efc64` only**, not on each index family: with
   `enable_indexscan` off it does not use the HNSW index, so another family adds nothing. `qc-exact`
   still runs on the first build of each Qdrant layout, since the layouts change what it searches.
3. **`pa-t20k-m1` is `p-asrun`**: its limits are pgvector's defaults, so it is not run twice.
4. P2 (d) is applied as written also when the other questions lose nothing (twice zero is zero).
5. Q2's share is inferred from the hits only when the telemetry never shows the ACORN counter; when
   it does, a person whose searches never took the ACORN path counts as not engaged.
6. P1's reach comes from EXPLAIN of empty results: when a setting has more than 200 short results,
   the EXPLAINs cover the empty ones first.

Items 1 to 3 change the plan; items 4 to 6 say how the code applies rules already written.

## Amendment 2 (2026-10-29, after run 1, before run 2)

Run 1 (Kaggle notebook `notebook11401c38ff`, 2026-10-26) finished with 12 pgvector items skipped for
time. It also showed that most of its pgvector searches did not use the HNSW index. Under `p-asrun`,
PostgreSQL ran the search statement with a generic plan 5,852 times, which is all but about ten
executions per distinct statement text. For all 50 fixed questions the generic plan had another
shape than the custom plan EXPLAIN showed. Recall and latency did not move with `ef_search` (40 to
400), `hnsw.max_scan_tuples` (20,000 to 1,000,000), scan memory or `work_mem`, and `p-asrun` reached
recall@5 0.998 at a p50 of 391 ms, against 0.691 and 6.5 ms in the original run. The diagnosis is in
the paper workspace (`investigations/x0-x1-pgvector-gap.md`). In short: after psycopg prepares the
statement (its 6th execution on a connection) and PostgreSQL has made five custom plans, the
planner keeps a generic plan whenever its estimated cost is lower. The generic plan cannot see the
jsonb filter values or the LIMIT, so it assumes a very selective filter and sorts the rows the GIN
index returns, an exact search. Run 1's P-a to P-c settings therefore measured that exact plan, not
the HNSW scan that P1 and P2 are about. In Qdrant, the `one-segment` layout ended with two segments.

This amendment is committed on its own, before any code of run 2 is written, with the message
`bench: amend the pre-registration for X1 run 2`. Run 2 writes to a new folder; run 1's results are
kept and reported as run 1.

1. **Plan control.** Every pgvector setting of P-a to P-e, and the new setting `pg-custom` described
   below, sets `plan_cache_mode = force_custom_plan` in the search's own transaction
   (harness-level), so every search is planned with its own values, as the original run's searches
   evidently were. `pg-custom` was already pre-registered as `p-asrun` with that plan mode; in run 2
   it is also the reference for P1 and P2. `p-asrun` keeps the server default (`auto`) and the
   psycopg default, as the original run did, and remains the reference for P4. `pg-noprepare` and
   `ph-exact` are unchanged.
2. **P1 and P2 read `pg-custom` wherever they say `p-asrun`.** In P2 (c) that is `pg-custom` on
   both index families, so `pg-custom` joins the core grid of `hnsw-m32-efc200` (which keeps
   `p-asrun`, `pc-ef400`, `pa-t1000k-m8` and `pd-lim10`). P3 and P4 are unchanged. The rules
   themselves, their thresholds and their wording are otherwise unchanged.
3. **Executed plans are recorded.** EXPLAIN with the search's values always shows a custom plan, so
   it cannot show what a prepared search ran. Run 2 loads PostgreSQL's `auto_explain` in each
   setting's session (log level NOTICE, JSON, plan only) and keeps the plan PostgreSQL executed for
   every search of the first pass (k=5 and k=10): whether it used the HNSW index, and whether it is
   a generic plan (parameter symbols left in the plan). After the timed passes, the 50 fixed
   questions run once more with `auto_explain`'s ANALYZE and BUFFERS (reason `executed`). The
   EXPLAINs of run 1 stay as they were. **Rule:** a setting meant to search the HNSW graph (every
   pgvector setting except `ph-exact`) whose captured plans used the HNSW index in fewer than half
   of its searches is flagged "ran mostly exact" in the log, in its record and in the report, and
   P1 and P2 do not use it: a criterion that needs it counts as missing. If no plan can be captured,
   the report says so and nothing is excluded.
4. **Two replays of the original run (new settings, descriptive).** Both run on the first build of
   `hnsw-m16-efc64`, before every other setting. `p-x0` replays the original pgvector pass as it
   was: `enterprise_rag`'s own backend object on the connection pool its load created (at most four
   connections, psycopg's defaults), started right after the load; the original 1,105 questions in
   the original order (the seed-7 shuffle); 10 untimed warm-ups; then per question the k=5
   retrieval (timed) and the k=10 retrieval; one pass, as the original did. `p-x0v` is the same
   replay on a fresh pool of the same kind after `VACUUM (ANALYZE)` of the table. Both record how
   often PostgreSQL used generic plans, the executed plans, the table's vacuum and analyze history,
   and the GIN index's metapage (pending-list pages and entry statistics) before and after. They
   have no verdict of their own; they enter P5's notes and the gap analysis.
5. **New hypothesis P5: the plan cache decides whether pgvector searches the graph.** On the
   original questions (every person type but `probe-*`), and with "HNSW share" the share of captured
   first-pass plans that used the HNSW index:
   confirmed when all of (a) the HNSW share is at least 0.9 under `pg-custom` and at most 0.1 under
   `p-asrun`; (b) recall@5 under `pg-custom` lies within 0.08 of the original run's 0.691; (c) recall@5
   under `p-asrun` is at least 0.99 and its median latency at least ten times `pg-custom`'s (on the
   builds and in the shard they share). Falsified when `pg-custom` has an HNSW share of at least 0.9
   and a recall@5 of at least 0.95 (HNSW plans do not reproduce the original loss), or when `p-asrun`
   has an HNSW share of at least 0.5 (run 1's reading was wrong). Prediction: confirmed.
6. **Qdrant's `one-segment` layout, fixed.** The collection is created with
   `default_segment_number` 1, `max_segment_size` 1,000,000 KB and `indexing_threshold` 0, which
   turns indexing off (Qdrant 1.19.2, `get_indexing_threshold_kb`), so the upload fills one segment.
   Then `indexing_threshold` is set back to Qdrant's default, 10,000 KB, and the run waits until
   every vector is indexed and the collection is green (an empty optimizer update restarts a
   collection left grey). Qdrant keeps an empty appendable segment beside the optimized one (its
   merge optimizer's documentation), so `segments_count` stays at 2 by construction. In Q3, "segment
   count" therefore means the number of segments holding points, read per segment from
   `/telemetry` (`num_points`) and recorded with every build, for every layout, as `data_segments`,
   with the whole per-segment list.
7. **Scope and repetitions: the full design.** Run 2 reruns the whole pgvector grid (every setting
   on every one of three builds of `hnsw-m16-efc64`; the core grid on three builds of
   `hnsw-m32-efc200`; `ph-exact` on the first build) and the whole Qdrant grid (five layouts, three
   builds each), on all 1,489 questions, with three timed passes. Only the two replays run one
   pass, because the original did. All eight pre-registered verdicts and P5 are judged on run 2's
   data alone.
8. **Where it runs (shards).** On Kaggle, account `muzakkirhussain1`. One session (`prep`) builds
   the corpus, embeds the chunks and the questions, and computes the exact baseline and the
   question table; it runs on the CPU when no GPU session is free (bge-base in float32 instead of
   float16; every shard uses `prep`'s vectors, so all of run 2 searches and scores with the same
   ones, and the manifest records which device embedded them). Three sessions, each attaching
   `prep`'s output, run the store grids in parallel: shard A, `hnsw-m16-efc64` build 0 (the
   replays first); shard B,
   `hnsw-m16-efc64` builds 1 and 2; shard C, `hnsw-m32-efc200` builds 0 to 2, then the Qdrant grid.
   Every shard uses `prep`'s chunk and query vectors, recomputes the exact baseline from them and
   checks that its question table matches `prep`'s (same questions, persons and R, the same exact
   top-10 scores within 1e-4). Each shard starts PostgreSQL and loads the table as the original run
   did. Builds keep the numbers b0 to b2 whichever shard ran them. The statistics merge the shards'
   folders and refuse a setting and build that two shards both report. **Latency is compared only
   within a shard** (paired comparisons and P5 (c) use settings of the same shard); recall, ERR and
   the other retrieval metrics do not depend on the hardware and are compared across shards. A
   shard that runs out of session time continues in a further session with `--resume`; the
   manifests record each session.
9. **Time guard.** A setting is started only if the time left exceeds the longest earlier run of
   the same setting in that session, or of any setting of the store if it has not run yet. The
   guard skips; it never shortens a setting.

Predictions stated now for run 2, beside the pre-registered ones: `pg-custom` gives about the
original run's recall@5 (0.691) and an ERR near 0.01 (the original had 10 to 12 empties among 1,084
scorable questions), so P1 has enough events to judge; `p-asrun` runs generic, exact plans again
(recall@5 about 1.0, P5 (c)); P4 as pre-registered predicted no difference, and run 2 is expected to
falsify it on recall; `p-x0v` runs generic, exact plans after its first ten executions per
statement; for `p-x0` no prediction is made, because its plan depends on what autovacuum has done
to the table when its statements first switch.
