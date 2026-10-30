# X7: revocation and faults

Profile: ['full']. Files: 1; records: 64.

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H4b pgvector blackhole plain | CONFIRMED | 1.000 [1.000, 1.000] over 340 requests |
| A2-H4c pgvector blackhole plain | CONFIRMED | median latency of inside failures and hangs 5.000 s, at least 4.5 predicted |
| A2-H4b pgvector blackhole stmt-timeout | CONFIRMED | 1.000 [1.000, 1.000] over 340 requests |
| A2-H4c pgvector blackhole stmt-timeout | CONFIRMED | median latency of inside failures and hangs 5.000 s, at least 4.5 predicted |
| A2-H5 pgvector lock plain latency | CONFIRMED | median latency of inside failures and hangs 5.000 s, at least 4.5 predicted |
| A2-H5 pgvector lock stmt-timeout failing | CONFIRMED | 1.000 [1.000, 1.000] over 540 requests |
| A2-H5 pgvector lock stmt-timeout latency | CONFIRMED | 0 hangs; median latency of inside failures 1.003 s, at most 1.5 predicted |
| A2-H7 store errors | CONFIRMED | 2465 failures, 2465 SearchError with a fixed message, 0 naming a host, 0 leaks |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Amendment 2: faults

60 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.850 [0.794, 0.906] | 51 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 360 | 360 | {'wardowl.retriever.SearchError': 360} | 0 | 0 | 0 inside (closed loop): 8 hangs, 5 pool timeouts across its edges |
| pgvector | blackhole | stmt-timeout | 10 | 340 | 1.000 [1.000, 1.000] | 0.856 [0.794, 0.918] | 49 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 360 | 360 | {'wardowl.retriever.SearchError': 360} | 0 | 0 |  |
| pgvector | down | plain | 10 | 330 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 471 | 471 | {'wardowl.retriever.SearchError': 471} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |
| pgvector | lock | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.765 [0.765, 0.765] | 80 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 261 | 261 | {'wardowl.retriever.SearchError': 261} | 0 | 0 |  |
| pgvector | lock | stmt-timeout | 10 | 540 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.003 | 1.003 | 540 | 540 | {'wardowl.retriever.SearchError': 540} | 0 | 0 |  |
| pgvector | refuse | plain | 10 | 340 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 473 | 473 | {'wardowl.retriever.SearchError': 473} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b tables (registered rules, no verdicts)

60 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 299 | 0 | 0.063 [0.057, 0.065] | 5.000 | {'ok': 560, 'hang': 61, 'error': 299} | wardowl.retriever.SearchError: search failed |
| pgvector | blackhole | stmt-timeout | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 301 | 0 | 0.070 [0.068, 0.072] | 5.000 | {'ok': 560, 'hang': 59, 'error': 301} | wardowl.retriever.SearchError: search failed |
| pgvector | down | plain | 10 | 330 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 471 | 0 | 2.417 [2.039, 2.759] | 5.000 | {'ok': 454, 'error': 471} | wardowl.retriever.SearchError: search failed |
| pgvector | lock | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 261 | 0 | 0.039 [0.037, 0.039] | 5.000 | {'ok': 579, 'hang': 80, 'error': 261} | wardowl.retriever.SearchError: search failed |
| pgvector | lock | stmt-timeout | 10 | 540 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 540 | 0 | 0.012 [0.011, 0.012] | 1.003 | {'ok': 380, 'error': 540} | wardowl.retriever.SearchError: search failed |
| pgvector | refuse | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 473 | 0 | 2.177 [1.911, 2.778] | 5.000 | {'ok': 452, 'error': 473} | wardowl.retriever.SearchError: search failed |

## Harness

Runs: 1 job records; profile ['full']; commit ['41292bd'].
