# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 10. **Smoke data: not analysed for the hypotheses.**

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H4 pgvector blackhole plain | INCONCLUSIVE | 4 requests inside |
| A2-H4 pgvector blackhole stmt-timeout | INCONCLUSIVE | 0 requests inside |
| A2-H5 pgvector lock plain | INCONCLUSIVE | 0 requests inside |
| A2-H5 pgvector lock stmt-timeout | INCONCLUSIVE | 24 requests inside |
| A2-H7 store errors | INCONCLUSIVE | 55 failures, 55 SearchError with a fixed message, 0 naming a host, 0 leaks |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Amendment 2: faults

6 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 5 | 5 | {'wardowl.retriever.SearchError': 5} | 0 | 0 | 0 inside (closed loop): 8 hangs, 5 pool timeouts across its edges |
| pgvector | blackhole | stmt-timeout | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | n/a | n/a | 5 | 5 | {'wardowl.retriever.SearchError': 5} | 0 | 0 |  |
| pgvector | down | plain | 1 | 3 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 9 | 9 | {'wardowl.retriever.SearchError': 9} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |
| pgvector | lock | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | n/a | n/a | 0 | 0 | {} | 0 | 0 |  |
| pgvector | lock | stmt-timeout | 1 | 24 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.003 | 1.003 | 26 | 26 | {'wardowl.retriever.SearchError': 26} | 0 | 0 |  |
| pgvector | refuse | plain | 1 | 4 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 10 | 10 | {'wardowl.retriever.SearchError': 10} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b tables (registered rules, no verdicts)

6 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5 | 0 | 0.107 [0.107, 0.107] | 5.000 | {'ok': 40, 'error': 5} | wardowl.retriever.SearchError: search failed |
| pgvector | blackhole | stmt-timeout | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 5 | 0 | 0.108 [0.108, 0.108] | n/a | {'ok': 40, 'error': 5} | wardowl.retriever.SearchError: search failed |
| pgvector | down | plain | 1 | 3 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 9 | 0 | 0.844 [0.844, 0.844] | 5.000 | {'ok': 36, 'error': 9} | wardowl.retriever.SearchError: search failed |
| pgvector | lock | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.108 [0.108, 0.108] | n/a | {'ok': 45} |  |
| pgvector | lock | stmt-timeout | 1 | 24 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 26 | 0 | 0.108 [0.108, 0.108] | 1.003 | {'ok': 19, 'error': 26} | wardowl.retriever.SearchError: search failed |
| pgvector | refuse | plain | 1 | 4 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 10 | 0 | 1.061 [1.061, 1.061] | 5.000 | {'ok': 35, 'error': 10} | wardowl.retriever.SearchError: search failed |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['b0f5fec'].
