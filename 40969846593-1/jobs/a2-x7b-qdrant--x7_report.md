# X7: revocation and faults

Profile: ['full']. Files: 1; records: 64.

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H7 store errors | CONFIRMED | 3601 failures, 3601 SearchError with a fixed message, 0 naming a host, 0 leaks |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Amendment 2: faults

60 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qdrant | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.006 | 5.006 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 10 inside, failing 1.000; qdrant_client classes |
| qdrant | down | plain | 10 | 568 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 7.0e-04 | 7.0e-04 | 601 | 601 | {'wardowl.retriever.SearchError': 601} | 0 | 0 | 5,570 inside, failing 1.000; qdrant_client classes |
| qdrant | http500 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 | 0.001 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,553 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | http503 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 | 0.002 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,550 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | refuse | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 8.0e-04 | 8.0e-04 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,683 inside, failing 1.000; qdrant_client classes |
| qdrant | truncate | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.003 | 0.003 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,236 inside, failing 1.000; json.decoder.JSONDecodeError |

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b tables (registered rules, no verdicts)

60 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qdrant | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.010, 0.011] | 5.006 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | down | plain | 10 | 568 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 601 | 0 | 0.212 [0.211, 0.216] | 7.2e-04 | {'ok': 330, 'error': 601} | wardowl.retriever.SearchError: search failed |
| qdrant | http500 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.011, 0.011] | 0.001 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | http503 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.010, 0.012] | 0.001 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | refuse | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.012 [0.011, 0.012] | 7.5e-04 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | truncate | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.010, 0.012] | 0.003 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |

## Harness

Runs: 1 job records; profile ['full']; commit ['41292bd'].
