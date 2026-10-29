# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 10. **Smoke data: not analysed for the hypotheses.**

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H7 store errors | INCONCLUSIVE | 181 failures, 181 SearchError with a fixed message, 0 naming a host, 0 leaks |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Amendment 2: faults

6 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qdrant | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.005 | 5.005 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 10 inside, failing 1.000; qdrant_client classes |
| qdrant | down | plain | 1 | 17 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 9.0e-04 | 9.0e-04 | 31 | 31 | {'wardowl.retriever.SearchError': 31} | 0 | 0 | 5,570 inside, failing 1.000; qdrant_client classes |
| qdrant | http500 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 | 0.001 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,553 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | http503 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 | 0.002 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,550 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | refuse | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 9.0e-04 | 9.0e-04 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,683 inside, failing 1.000; qdrant_client classes |
| qdrant | truncate | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.003 | 0.003 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,236 inside, failing 1.000; json.decoder.JSONDecodeError |

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b tables (registered rules, no verdicts)

6 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qdrant | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 5.005 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | down | plain | 1 | 17 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 31 | 0 | 0.308 [0.308, 0.308] | 9.0e-04 | {'ok': 15, 'error': 31} | wardowl.retriever.SearchError: search failed |
| qdrant | http500 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 0.001 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | http503 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 0.002 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | refuse | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 9.0e-04 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | truncate | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.140 [0.140, 0.140] | 0.003 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['b0f5fec'].
