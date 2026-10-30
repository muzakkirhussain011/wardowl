# X7: revocation and faults

Profile: ['full']. Files: 5; records: 480.

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H3 cerbos-policy nocache | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H1 cerbos-policy ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-inv | CONFIRMED | median 3.884 [3.879, 3.891], limit 4.0; full run median 30.025 [30.019, 30.032], max 30.052 |
| A2-H1 cerbos-policy ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-shared-inv | CONFIRMED | median 3.887 [3.876, 3.900], limit 5.0; full run median 31.039 [31.026, 31.047], max 31.066 |
| A2-H3 spicedb-ml nocache | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| X7-H5 (replication) spicedb-ml staleness | CONFIRMED | median 4.732 [4.627, 4.799], maximum 5.212 |
| A2-H3 spicedb-ml ttl5 | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 16.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl5 | CONFIRMED | median 5.040 [5.039, 5.040] against [4.0, 11.5] |
| A2-H3 spicedb-ml ttl30 | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 41.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl30 | CONFIRMED | median 30.017 [30.013, 30.024] against [29.0, 36.5] |
| A2-H1 spicedb-ml ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-inv | CONFIRMED | median 4.774 [4.708, 4.839], limit 6.0; full run median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| A2-H1 spicedb-ml ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 12.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-shared-inv | CONFIRMED | median 4.767 [4.684, 4.827], limit 7.0; full run median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |
| A2-H4b pgvector blackhole plain | CONFIRMED | 1.000 [1.000, 1.000] over 340 requests |
| A2-H4c pgvector blackhole plain | CONFIRMED | median latency of inside failures and hangs 5.000 s, at least 4.5 predicted |
| A2-H4b pgvector blackhole stmt-timeout | CONFIRMED | 1.000 [1.000, 1.000] over 340 requests |
| A2-H4c pgvector blackhole stmt-timeout | CONFIRMED | median latency of inside failures and hangs 5.000 s, at least 4.5 predicted |
| A2-H5 pgvector lock plain latency | CONFIRMED | median latency of inside failures and hangs 5.000 s, at least 4.5 predicted |
| A2-H5 pgvector lock stmt-timeout failing | CONFIRMED | 1.000 [1.000, 1.000] over 540 requests |
| A2-H5 pgvector lock stmt-timeout latency | CONFIRMED | 0 hangs; median latency of inside failures 1.003 s, at most 1.5 predicted |
| A2-H6 spicedb empty | CONFIRMED | failing 1.000 [1.000, 1.000], deviating 0.000 [0.000, 0.000] over 3520 requests; full run 4,703 inside, failing 0.000; 4,746 deviating answers, 1 failure |
| A2-H6 spicedb empty-lookup exact | CONFIRMED | 1.000 [1.000, 1.000] over 3180 requests |
| A2-H7 store errors | CONFIRMED | 6066 failures, 6066 SearchError with a fixed message, 0 naming a host, 0 leaks |
| A2-H8 fail closed | CONFIRMED | 10303 requests: 0 leaks (one-sided bound 0.000291), 0 failures not AuthorizationError, 0 naming a host |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 40 | 10.000 | 10.000 | 3.881 [3.876, 3.893] | 3.935 | 3.929 | 0 | 0 | 0 | median 2.549 [2.369, 3.219], max 4.035 |
| cerbos-policy | ttl30-inv | 40 | 10.000 | 10.000 | 3.884 [3.879, 3.891] | 3.919 | 3.916 | 0 | 0 | 0 | median 30.025 [30.019, 30.032], max 30.052 |
| cerbos-policy | ttl30-shared-inv | 40 | 10.000 | 11.000 | 3.887 [3.876, 3.900] | 3.927 | 3.926 | 0 | 0 | 0 | median 31.039 [31.026, 31.047], max 31.066 |
| spicedb-ml | nocache | 40 | 11.000 | 11.000 | 4.732 [4.627, 4.799] | 5.212 | 5.025 | 0 | 0 | 19 | median 3.251 [2.994, 3.371], max 8.742; 1 of 40 beyond 6.5 s |
| spicedb-ml | ttl5 | 40 | 11.000 | 16.000 | 5.040 [5.039, 5.040] | 10.088 | 10.087 | 0 | 0 | 0 | median 5.023 [5.021, 5.026], max 6.828 |
| spicedb-ml | ttl30 | 40 | 11.000 | 41.000 | 30.017 [30.013, 30.024] | 30.045 | 30.036 | 0 | 0 | 0 | median 30.018 [30.008, 30.031], max 30.044 |
| spicedb-ml | ttl30-inv | 40 | 11.000 | 11.000 | 4.774 [4.708, 4.839] | 5.226 | 5.058 | 0 | 0 | 28 | median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| spicedb-ml | ttl30-shared-inv | 40 | 11.000 | 12.000 | 4.767 [4.684, 4.827] | 5.187 | 4.998 | 0 | 0 | 16 | median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |

## Amendment 2: faults

140 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.850 [0.794, 0.906] | 51 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 360 | 360 | {'wardowl.retriever.SearchError': 360} | 0 | 0 | 0 inside (closed loop): 8 hangs, 5 pool timeouts across its edges |
| pgvector | blackhole | stmt-timeout | 10 | 340 | 1.000 [1.000, 1.000] | 0.856 [0.794, 0.918] | 49 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 360 | 360 | {'wardowl.retriever.SearchError': 360} | 0 | 0 |  |
| pgvector | down | plain | 10 | 330 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 471 | 471 | {'wardowl.retriever.SearchError': 471} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |
| pgvector | lock | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.765 [0.765, 0.765] | 80 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 261 | 261 | {'wardowl.retriever.SearchError': 261} | 0 | 0 |  |
| pgvector | lock | stmt-timeout | 10 | 540 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.003 | 1.003 | 540 | 540 | {'wardowl.retriever.SearchError': 540} | 0 | 0 |  |
| pgvector | refuse | plain | 10 | 340 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.000 | 5.000 | 473 | 473 | {'wardowl.retriever.SearchError': 473} | 0 | 0 | 10 inside, failing 1.000; client classes (psycopg, psycopg_pool) |
| qdrant | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 5.006 | 5.006 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 10 inside, failing 1.000; qdrant_client classes |
| qdrant | down | plain | 10 | 568 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 7.0e-04 | 7.0e-04 | 601 | 601 | {'wardowl.retriever.SearchError': 601} | 0 | 0 | 5,570 inside, failing 1.000; qdrant_client classes |
| qdrant | http500 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 | 0.001 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,553 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | http503 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 | 0.002 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,550 inside, failing 1.000; UnexpectedResponse with the raw response |
| qdrant | refuse | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 8.0e-04 | 8.0e-04 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,683 inside, failing 1.000; qdrant_client classes |
| qdrant | truncate | plain | 10 | 590 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.003 | 0.003 | 600 | 600 | {'wardowl.retriever.SearchError': 600} | 0 | 0 | 5,236 inside, failing 1.000; json.decoder.JSONDecodeError |
| spicedb | empty | plain | 10 | 3520 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.011 | 0.011 | 3549 | 0 | {'wardowl.authz.AuthorizationError': 3549} | 0 | 0 | 4,703 inside, failing 0.000; 4,746 deviating answers, 1 failure |
| spicedb | empty-lookup | plain | 10 | 3180 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | n/a | n/a | 0 | 0 | {} | 0 | 0 |  |

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 40 | 40 | 3.881 [3.876, 3.893] | 3.935 | 3.929 | n/a | 0 | 0 | 0 | 0 | 5.1e-04 |
| cerbos-policy | ttl30-inv | 40 | 40 | 3.884 [3.879, 3.891] | 3.919 | 3.916 | n/a | 0 | 0 | 0 | 0 | 5.2e-04 |
| cerbos-policy | ttl30-shared-inv | 40 | 40 | 3.887 [3.876, 3.900] | 3.927 | 3.926 | n/a | 0 | 0 | 0 | 0 | 5.0e-04 |
| spicedb-ml | nocache | 40 | 40 | 4.732 [4.627, 4.799] | 5.212 | 5.025 | 5.500 | 0 | 0 | 19 | 0 | 0.003 |
| spicedb-ml | ttl5 | 40 | 40 | 5.040 [5.039, 5.040] | 10.088 | 10.087 | 10.500 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | ttl30 | 40 | 40 | 30.017 [30.013, 30.024] | 30.045 | 30.036 | 35.500 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | ttl30-inv | 40 | 40 | 4.774 [4.708, 4.839] | 5.226 | 5.058 | 5.500 | 0 | 0 | 28 | 0 | 0.003 |
| spicedb-ml | ttl30-shared-inv | 40 | 40 | 4.767 [4.684, 4.827] | 5.187 | 4.998 | 6.500 | 0 | 0 | 16 | 0 | 0.003 |

## X7b tables (registered rules, no verdicts)

140 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 299 | 0 | 0.063 [0.057, 0.065] | 5.000 | {'ok': 560, 'hang': 61, 'error': 299} | wardowl.retriever.SearchError: search failed |
| pgvector | blackhole | stmt-timeout | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 301 | 0 | 0.070 [0.068, 0.072] | 5.000 | {'ok': 560, 'hang': 59, 'error': 301} | wardowl.retriever.SearchError: search failed |
| pgvector | down | plain | 10 | 330 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 471 | 0 | 2.417 [2.039, 2.759] | 5.000 | {'ok': 454, 'error': 471} | wardowl.retriever.SearchError: search failed |
| pgvector | lock | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 261 | 0 | 0.039 [0.037, 0.039] | 5.000 | {'ok': 579, 'hang': 80, 'error': 261} | wardowl.retriever.SearchError: search failed |
| pgvector | lock | stmt-timeout | 10 | 540 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 540 | 0 | 0.012 [0.011, 0.012] | 1.003 | {'ok': 380, 'error': 540} | wardowl.retriever.SearchError: search failed |
| pgvector | refuse | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 473 | 0 | 2.177 [1.911, 2.778] | 5.000 | {'ok': 452, 'error': 473} | wardowl.retriever.SearchError: search failed |
| qdrant | blackhole | plain | 10 | 340 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.010, 0.011] | 5.006 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | down | plain | 10 | 568 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 601 | 0 | 0.212 [0.211, 0.216] | 7.2e-04 | {'ok': 330, 'error': 601} | wardowl.retriever.SearchError: search failed |
| qdrant | http500 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.011, 0.011] | 0.001 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | http503 | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.010, 0.012] | 0.001 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | refuse | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.012 [0.011, 0.012] | 7.5e-04 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| qdrant | truncate | plain | 10 | 590 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 600 | 0 | 0.011 [0.010, 0.012] | 0.003 | {'ok': 320, 'error': 600} | wardowl.retriever.SearchError: search failed |
| spicedb | empty | plain | 10 | 3520 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.024, 0.049] | 0.012 | {'ok': 1790, 'authz': 3549} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned invalid JSON |
| spicedb | empty-lookup | plain | 10 | 3180 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.042 [0.029, 0.059] | n/a | {'ok': 4964} |  |

## Harness

Runs: 5 job records; profile ['full']; commit ['41292bd'].
