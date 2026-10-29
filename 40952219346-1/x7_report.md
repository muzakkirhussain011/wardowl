# X7: revocation and faults

Profile: ['smoke']. Files: 5; records: 42. **Smoke data: not analysed for the hypotheses.**

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H3 cerbos-policy nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H1 cerbos-policy ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-inv | INCONCLUSIVE | median 3.876 [3.876, 3.876], limit 4.0; full run median 30.025 [30.019, 30.032], max 30.052 |
| A2-H1 cerbos-policy ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-shared-inv | INCONCLUSIVE | median 3.890 [3.890, 3.890], limit 5.0; full run median 31.039 [31.026, 31.047], max 31.066 |
| A2-H3 spicedb-ml nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| X7-H5 (replication) spicedb-ml staleness | INCONCLUSIVE | median 5.024 [5.024, 5.024], maximum 5.024 |
| A2-H3 spicedb-ml ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 16.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl5 | INCONCLUSIVE | median 5.017 [5.017, 5.017] against [4.0, 11.5] |
| A2-H3 spicedb-ml ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 41.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl30 | INCONCLUSIVE | median 30.001 [30.001, 30.001] against [29.0, 36.5] |
| A2-H1 spicedb-ml ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-inv | INCONCLUSIVE | median 3.177 [3.177, 3.177], limit 6.0; full run median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| A2-H1 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 12.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | median 4.785 [4.785, 4.785], limit 7.0; full run median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |
| A2-H4 pgvector blackhole plain | INCONCLUSIVE | 4 requests inside |
| A2-H4 pgvector blackhole stmt-timeout | INCONCLUSIVE | 0 requests inside |
| A2-H5 pgvector lock plain | INCONCLUSIVE | 0 requests inside |
| A2-H5 pgvector lock stmt-timeout | INCONCLUSIVE | 24 requests inside |
| A2-H6 spicedb empty | INCONCLUSIVE | failing 1.000 [1.000, 1.000], deviating 0.000 [0.000, 0.000] over 204 requests; full run 4,703 inside, failing 0.000; 4,746 deviating answers, 1 failure |
| A2-H6 spicedb empty-lookup exact | INCONCLUSIVE | 1.000 [1.000, 1.000] over 203 requests |
| A2-H7 store errors | INCONCLUSIVE | 236 failures, 236 SearchError with a fixed message, 0 naming a host, 0 leaks |
| A2-H8 fail closed | INCONCLUSIVE | 587 requests: 0 leaks (one-sided bound 0.005090), 0 failures not AuthorizationError, 0 naming a host |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 1 | 10.000 | 10.000 | 3.738 [3.738, 3.738] | 3.738 | 3.738 | 0 | 0 | 0 | median 2.549 [2.369, 3.219], max 4.035 |
| cerbos-policy | ttl30-inv | 1 | 10.000 | 10.000 | 3.876 [3.876, 3.876] | 3.876 | 3.876 | 0 | 0 | 0 | median 30.025 [30.019, 30.032], max 30.052 |
| cerbos-policy | ttl30-shared-inv | 1 | 10.000 | 11.000 | 3.890 [3.890, 3.890] | 3.890 | 3.890 | 0 | 0 | 0 | median 31.039 [31.026, 31.047], max 31.066 |
| spicedb-ml | nocache | 1 | 11.000 | 11.000 | 5.024 [5.024, 5.024] | 5.024 | 5.024 | 0 | 0 | 2 | median 3.251 [2.994, 3.371], max 8.742; 1 of 40 beyond 6.5 s |
| spicedb-ml | ttl5 | 1 | 11.000 | 16.000 | 5.017 [5.017, 5.017] | 5.017 | 5.017 | 0 | 0 | 0 | median 5.023 [5.021, 5.026], max 6.828 |
| spicedb-ml | ttl30 | 1 | 11.000 | 41.000 | 30.001 [30.001, 30.001] | 30.001 | 30.001 | 0 | 0 | 0 | median 30.018 [30.008, 30.031], max 30.044 |
| spicedb-ml | ttl30-inv | 1 | 11.000 | 11.000 | 3.177 [3.177, 3.177] | 3.177 | 3.177 | 0 | 0 | 0 | median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| spicedb-ml | ttl30-shared-inv | 1 | 11.000 | 12.000 | 4.785 [4.785, 4.785] | 4.785 | 4.785 | 0 | 0 | 0 | median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |

## Amendment 2: faults

14 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 5 | 5 | {'wardowl.retriever.SearchError': 5} | 0 | 0 | 0 inside (closed loop): 8 hangs, 5 pool timeouts across its edges |
| pgvector | blackhole | stmt-timeout | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | n/a | n/a | 5 | 5 | {'wardowl.retriever.SearchError': 5} | 0 | 0 |  |
| pgvector | down | plain | 1 | 3 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 9 | 9 | {'wardowl.retriever.SearchError': 9} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |
| pgvector | lock | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | n/a | n/a | 0 | 0 | {} | 0 | 0 |  |
| pgvector | lock | stmt-timeout | 1 | 24 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.003 | 1.003 | 26 | 26 | {'wardowl.retriever.SearchError': 26} | 0 | 0 |  |
| pgvector | refuse | plain | 1 | 4 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 10 | 10 | {'wardowl.retriever.SearchError': 10} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |
| qdrant | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.005 | 5.005 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 10 inside, failing 1.000; qdrant_client classes |
| qdrant | down | plain | 1 | 17 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 9.0e-04 | 9.0e-04 | 31 | 31 | {'wardowl.retriever.SearchError': 31} | 0 | 0 | 5,570 inside, failing 1.000; qdrant_client classes |
| qdrant | http500 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 | 0.001 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,553 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | http503 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 | 0.002 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,550 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | refuse | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 9.0e-04 | 9.0e-04 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,683 inside, failing 1.000; qdrant_client classes |
| qdrant | truncate | plain | 1 | 29 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.003 | 0.003 | 30 | 30 | {'wardowl.retriever.SearchError': 30} | 0 | 0 | 5,236 inside, failing 1.000; json.decoder.JSONDecodeError |
| spicedb | empty | plain | 1 | 204 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.008 | 0.008 | 208 | 0 | {'wardowl.authz.AuthorizationError': 208} | 0 | 0 | 4,703 inside, failing 0.000; 4,746 deviating answers, 1 failure |
| spicedb | empty-lookup | plain | 1 | 203 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | n/a | n/a | 0 | 0 | {} | 0 | 0 |  |

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 1 | 1 | 3.738 [3.738, 3.738] | 3.738 | 3.738 | n/a | 0 | 0 | 0 | 0 | 3.3e-04 |
| cerbos-policy | ttl30-inv | 1 | 1 | 3.876 [3.876, 3.876] | 3.876 | 3.876 | n/a | 0 | 0 | 0 | 0 | 4.3e-04 |
| cerbos-policy | ttl30-shared-inv | 1 | 1 | 3.890 [3.890, 3.890] | 3.890 | 3.890 | n/a | 0 | 0 | 0 | 0 | 3.9e-04 |
| spicedb-ml | nocache | 1 | 1 | 5.024 [5.024, 5.024] | 5.024 | 5.024 | 5.500 | 0 | 0 | 2 | 0 | 0.005 |
| spicedb-ml | ttl5 | 1 | 1 | 5.017 [5.017, 5.017] | 5.017 | 5.017 | 10.500 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | ttl30 | 1 | 1 | 30.001 [30.001, 30.001] | 30.001 | 30.001 | 35.500 | 0 | 0 | 0 | 0 | 0.006 |
| spicedb-ml | ttl30-inv | 1 | 1 | 3.177 [3.177, 3.177] | 3.177 | 3.177 | 5.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-shared-inv | 1 | 1 | 4.785 [4.785, 4.785] | 4.785 | 4.785 | 6.500 | 0 | 0 | 0 | 0 | 0.003 |

## X7b tables (registered rules, no verdicts)

14 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5 | 0 | 0.107 [0.107, 0.107] | 5.000 | {'ok': 40, 'error': 5} | wardowl.retriever.SearchError: search failed |
| pgvector | blackhole | stmt-timeout | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 5 | 0 | 0.108 [0.108, 0.108] | n/a | {'ok': 40, 'error': 5} | wardowl.retriever.SearchError: search failed |
| pgvector | down | plain | 1 | 3 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 9 | 0 | 0.844 [0.844, 0.844] | 5.000 | {'ok': 36, 'error': 9} | wardowl.retriever.SearchError: search failed |
| pgvector | lock | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.108 [0.108, 0.108] | n/a | {'ok': 45} |  |
| pgvector | lock | stmt-timeout | 1 | 24 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 26 | 0 | 0.108 [0.108, 0.108] | 1.003 | {'ok': 19, 'error': 26} | wardowl.retriever.SearchError: search failed |
| pgvector | refuse | plain | 1 | 4 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 10 | 0 | 1.061 [1.061, 1.061] | 5.000 | {'ok': 35, 'error': 10} | wardowl.retriever.SearchError: search failed |
| qdrant | blackhole | plain | 1 | 4 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 5.005 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | down | plain | 1 | 17 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 31 | 0 | 0.308 [0.308, 0.308] | 9.0e-04 | {'ok': 15, 'error': 31} | wardowl.retriever.SearchError: search failed |
| qdrant | http500 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 0.001 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | http503 | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 0.002 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | refuse | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.107 [0.107, 0.107] | 9.0e-04 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| qdrant | truncate | plain | 1 | 29 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.140 [0.140, 0.140] | 0.003 | {'ok': 15, 'error': 30} | wardowl.retriever.SearchError: search failed |
| spicedb | empty | plain | 1 | 204 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.019, 0.019] | 0.008 | {'ok': 88, 'authz': 208} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned invalid JSON |
| spicedb | empty-lookup | plain | 1 | 203 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.032 [0.032, 0.032] | n/a | {'ok': 291} |  |

## Harness

Runs: 5 job records; profile ['smoke']; commit ['b0f5fec'].
