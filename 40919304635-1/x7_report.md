# X7: revocation and faults

Profile: ['full']. Files: 9; records: 3133.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 acl-pgvector nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector nocache | CONFIRMED | median 7.0e-04 [6.8e-04, 7.2e-04] |
| X7-H1 acl-pgvector ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl5 | CONFIRMED | median 6.8e-04 [6.6e-04, 7.0e-04] |
| X7-H1 acl-pgvector ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl30 | CONFIRMED | median 7.1e-04 [6.8e-04, 7.5e-04] |
| X7-H1 acl-pgvector ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-inv | CONFIRMED | median 6.9e-04 [6.6e-04, 7.2e-04], limit 0.5 |
| X7-H4 acl-pgvector ttl30-inv | CONFIRMED | median 6.9e-04 [6.6e-04, 7.2e-04] |
| X7-H1 acl-pgvector ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-shared-inv | CONFIRMED | median 0.001 [0.001, 0.001], limit 1.5 |
| X7-H4 acl-pgvector ttl30-shared-inv | CONFIRMED | median 0.001 [0.001, 0.001] |
| X7-H1 acl-qdrant nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant nocache | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl5 | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl30 | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-inv | CONFIRMED | median 0.002 [0.002, 0.002], limit 0.5 |
| X7-H4 acl-qdrant ttl30-inv | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-shared-inv | CONFIRMED | median 0.003 [0.003, 0.003], limit 1.5 |
| X7-H4 acl-qdrant ttl30-shared-inv | CONFIRMED | median 0.003 [0.003, 0.003] |
| X7 exploratory cerbos-policy nocache | EXPLORATORY | median 2.549 [2.369, 3.219], maximum 4.035 |
| X7 exploratory cerbos-policy ttl5 | EXPLORATORY | median 5.018 [5.010, 5.027], maximum 5.048 |
| X7 exploratory cerbos-policy ttl30 | EXPLORATORY | median 30.017 [30.011, 30.021], maximum 30.044 |
| X7 exploratory cerbos-policy ttl30-inv | EXPLORATORY | median 30.025 [30.019, 30.032], maximum 30.052 |
| X7 exploratory cerbos-policy ttl30-shared-inv | EXPLORATORY | median 31.039 [31.026, 31.047], maximum 31.066 |
| X7-H1 opa-data nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-data ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-data ttl5 | CONFIRMED | median 5.034 [5.032, 5.037] against [4.0, 6.0] |
| X7-H1 opa-data ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-data ttl30 | CONFIRMED | median 30.033 [30.020, 30.036] against [29.0, 31.0] |
| X7-H1 opa-data ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-data ttl30-inv | CONFIRMED | median 6.0e-04 [5.8e-04, 6.2e-04], limit 0.5 |
| X7-H1 opa-data ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-data ttl30-shared-inv | CONFIRMED | median 1.018 [1.017, 1.019], limit 1.5 |
| X7-H1 opa-policy nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-policy ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-policy ttl5 | CONFIRMED | median 5.021 [5.020, 5.022] against [4.0, 6.0] |
| X7-H1 opa-policy ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-policy ttl30 | CONFIRMED | median 30.030 [30.028, 30.032] against [29.0, 31.0] |
| X7-H1 opa-policy ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-policy ttl30-inv | CONFIRMED | median 0.009 [0.009, 0.010], limit 0.5 |
| X7-H1 opa-policy ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-policy ttl30-shared-inv | CONFIRMED | median 1.022 [1.021, 1.023], limit 1.5 |
| X7-H1 openfga nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga ttl5 | CONFIRMED | median 5.015 [5.013, 5.020] against [4.0, 6.0] |
| X7-H1 openfga ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga ttl30 | CONFIRMED | median 30.020 [30.014, 30.026] against [29.0, 31.0] |
| X7-H1 openfga ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga ttl30-inv | CONFIRMED | median 0.003 [0.002, 0.004], limit 0.5 |
| X7-H1 openfga ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga ttl30-shared-inv | CONFIRMED | median 1.014 [1.012, 1.015], limit 1.5 |
| X7-H1 openfga-cached-hc nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga-cached-hc ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga-cached-hc ttl5 | CONFIRMED | median 5.015 [5.015, 5.017] against [4.0, 6.0] |
| X7-H1 openfga-cached-hc ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga-cached-hc ttl30 | CONFIRMED | median 30.016 [30.009, 30.025] against [29.0, 31.0] |
| X7-H1 openfga-cached-hc ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga-cached-hc ttl30-inv | CONFIRMED | median 0.003 [0.002, 0.003], limit 0.5 |
| X7-H1 openfga-cached-hc ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga-cached-hc ttl30-shared-inv | CONFIRMED | median 1.015 [1.015, 1.016], limit 1.5 |
| X7-H1 openfga-cached-ml nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7 exploratory openfga-cached-ml nocache | EXPLORATORY | median 0.003 [0.002, 0.003], maximum 0.008 |
| X7-H1 openfga-cached-ml ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 15.0 |
| X7 exploratory openfga-cached-ml ttl5 | EXPLORATORY | median 5.015 [5.014, 5.016], maximum 5.045 |
| X7-H1 openfga-cached-ml ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 40.0 |
| X7 exploratory openfga-cached-ml ttl30 | EXPLORATORY | median 30.022 [30.014, 30.031], maximum 30.044 |
| X7-H1 openfga-cached-ml ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7-H3 openfga-cached-ml ttl30-inv | CONFIRMED | median 0.003 [0.002, 0.003], limit 10.5 |
| X7 exploratory openfga-cached-ml ttl30-inv | EXPLORATORY | median 0.003 [0.002, 0.003], maximum 0.006 |
| X7-H1 openfga-cached-ml ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 11.0 |
| X7-H3 openfga-cached-ml ttl30-shared-inv | CONFIRMED | median 1.015 [1.015, 1.016], limit 11.5 |
| X7 exploratory openfga-cached-ml ttl30-shared-inv | EXPLORATORY | median 1.015 [1.015, 1.016], maximum 1.022 |
| X7-H1 spicedb-fc nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 spicedb-fc ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 spicedb-fc ttl5 | CONFIRMED | median 5.021 [5.019, 5.024] against [4.0, 6.0] |
| X7-H1 spicedb-fc ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 spicedb-fc ttl30 | CONFIRMED | median 30.017 [30.005, 30.026] against [29.0, 31.0] |
| X7-H1 spicedb-fc ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 spicedb-fc ttl30-inv | CONFIRMED | median 0.004 [0.004, 0.005], limit 0.5 |
| X7-H1 spicedb-fc ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 spicedb-fc ttl30-shared-inv | CONFIRMED | median 1.017 [1.016, 1.018], limit 1.5 |
| X7-H1 spicedb-ml nocache | FALSIFIED | 40 valid trials, 1 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H5 spicedb-ml staleness | FALSIFIED | median 3.251 [2.994, 3.371], maximum 8.742 |
| X7-H1 spicedb-ml ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.5 |
| X7-H2 spicedb-ml ttl5 | CONFIRMED | median 5.023 [5.021, 5.026] against [4.0, 11.5] |
| X7-H1 spicedb-ml ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 35.5 |
| X7-H2 spicedb-ml ttl30 | CONFIRMED | median 30.018 [30.008, 30.031] against [29.0, 36.5] |
| X7-H1 spicedb-ml ttl30-inv | FALSIFIED | 40 valid trials, 40 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H3 spicedb-ml ttl30-inv | FALSIFIED | median 30.042 [30.031, 30.048], limit 6.0 |
| X7-H1 spicedb-ml ttl30-shared-inv | FALSIFIED | 40 valid trials, 39 beyond B + 1 s (0 never took effect), B = 6.5 |
| X7-H3 spicedb-ml ttl30-shared-inv | FALSIFIED | median 31.048 [31.033, 31.061], limit 7.0 |
| G3 leak detection (allow-all leaks) | CONFIRMED | {'opa': 17685, 'cerbos': 22790, 'openfga': 7427, 'spicedb': 17484} |
| X7-H6 fail closed | CONFIRMED | 623279 requests: 0 leaks (one-sided bound 0.000005), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 28125 store-fault failures, 0 naming a host |
| X7-H7a cerbos blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a cerbos down | CONFIRMED | 1.000 [1.000, 1.000] over 1663 requests |
| X7-H7a cerbos http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5823 requests |
| X7-H7a cerbos http503 | CONFIRMED | 1.000 [1.000, 1.000] over 1670 requests |
| X7-H7a cerbos refuse | CONFIRMED | 1.000 [1.000, 1.000] over 1675 requests |
| X7-H7b cerbos slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 41 requests |
| X7-H7b cerbos slow-1000 latency rise | CONFIRMED | median rise 2.002 [2.001, 2.002] s against 1.0 s |
| X7-H7b cerbos slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 270 requests |
| X7-H7b cerbos slow-200 latency rise | CONFIRMED | median rise 0.402 [0.401, 0.402] s against 0.2 s |
| X7-H7a cerbos slow-3000 | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a opa blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a opa down | CONFIRMED | 1.000 [1.000, 1.000] over 1664 requests |
| X7-H7a opa http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5729 requests |
| X7-H7a opa http503 | CONFIRMED | 1.000 [1.000, 1.000] over 1657 requests |
| X7-H7a opa refuse | CONFIRMED | 1.000 [1.000, 1.000] over 1668 requests |
| X7-H7b opa slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 41 requests |
| X7-H7b opa slow-1000 latency rise | CONFIRMED | median rise 2.000 [1.999, 2.000] s against 1.0 s |
| X7-H7b opa slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 262 requests |
| X7-H7b opa slow-200 latency rise | CONFIRMED | median rise 0.399 [0.399, 0.400] s against 0.2 s |
| X7-H7a opa slow-3000 | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a openfga blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a openfga down | CONFIRMED | 1.000 [1.000, 1.000] over 1661 requests |
| X7-H7a openfga http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5833 requests |
| X7-H7a openfga http503 | CONFIRMED | 1.000 [1.000, 1.000] over 1669 requests |
| X7-H7a openfga refuse | CONFIRMED | 1.000 [1.000, 1.000] over 1675 requests |
| X7-H7b openfga slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 41 requests |
| X7-H7b openfga slow-1000 latency rise | CONFIRMED | median rise 1.999 [1.998, 2.000] s against 1.0 s |
| X7-H7b openfga slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 261 requests |
| X7-H7b openfga slow-200 latency rise | CONFIRMED | median rise 0.398 [0.398, 0.399] s against 0.2 s |
| X7-H7a openfga slow-3000 | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a spicedb blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a spicedb down | CONFIRMED | 1.000 [1.000, 1.000] over 1644 requests |
| X7-H7a spicedb http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5803 requests |
| X7-H7a spicedb http503 | CONFIRMED | 1.000 [1.000, 1.000] over 1667 requests |
| X7-H7a spicedb refuse | CONFIRMED | 1.000 [1.000, 1.000] over 1670 requests |
| X7-H7b spicedb slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 43 requests |
| X7-H7b spicedb slow-1000 latency rise | CONFIRMED | median rise 2.013 [2.008, 2.017] s against 1.0 s |
| X7-H7b spicedb slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 259 requests |
| X7-H7b spicedb slow-200 latency rise | CONFIRMED | median rise 0.407 [0.405, 0.411] s against 0.2 s |
| X7-H7a spicedb slow-3000 | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7c pgvector blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector down | CONFIRMED | 1.000 [1.000, 1.000] over 10 requests |
| X7-H7c pgvector refuse | CONFIRMED | 1.000 [1.000, 1.000] over 10 requests |
| X7-H7b pgvector slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 19 requests |
| X7-H7b pgvector slow-1000 latency rise | CONFIRMED | median rise 4.002 [4.002, 4.002] s against 1.0 s |
| X7-H7b pgvector slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 133 requests |
| X7-H7b pgvector slow-200 latency rise | CONFIRMED | median rise 0.801 [0.801, 0.801] s against 0.2 s |
| X7-H7c qdrant blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 10 requests |
| X7-H7c qdrant down | CONFIRMED | 1.000 [1.000, 1.000] over 5570 requests |
| X7-H7c qdrant http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5553 requests |
| X7-H7c qdrant http503 | CONFIRMED | 1.000 [1.000, 1.000] over 5550 requests |
| X7-H7c qdrant refuse | CONFIRMED | 1.000 [1.000, 1.000] over 5683 requests |
| X7-H7b qdrant slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 100 requests |
| X7-H7b qdrant slow-1000 latency rise | CONFIRMED | median rise 1.001 [1.001, 1.001] s against 1.0 s |
| X7-H7b qdrant slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 520 requests |
| X7-H7b qdrant slow-200 latency rise | CONFIRMED | median rise 0.201 [0.201, 0.201] s against 0.2 s |
| X7-H7c qdrant truncate | CONFIRMED | 1.000 [1.000, 1.000] over 5236 requests |
| X7 exploratory cerbos drop-last | EXPLORATORY | {'ok': 2423, 'authz': 4845} |
| X7 exploratory cerbos empty | EXPLORATORY | {'ok': 2371, 'authz': 5429} |
| X7 exploratory cerbos garbage-json | EXPLORATORY | {'ok': 2395, 'authz': 5491} |
| X7 exploratory cerbos truncate | EXPLORATORY | {'ok': 2412, 'authz': 5508} |
| X7 exploratory cerbos type-flip | EXPLORATORY | {'ok': 2420, 'authz': 5477} |
| X7 exploratory opa drop-last | EXPLORATORY | {'ok': 1805, 'authz': 3579} |
| X7 exploratory opa empty | EXPLORATORY | {'ok': 1794, 'authz': 4756} |
| X7 exploratory opa garbage-json | EXPLORATORY | {'ok': 1798, 'authz': 4747} |
| X7 exploratory opa truncate | EXPLORATORY | {'ok': 1796, 'authz': 4749} |
| X7 exploratory opa type-flip | EXPLORATORY | {'ok': 1804, 'authz': 3571} |
| X7 exploratory openfga drop-last | EXPLORATORY | {'ok': 1854, 'authz': 3694} |
| X7 exploratory openfga empty | EXPLORATORY | {'ok': 1851, 'authz': 5272} |
| X7 exploratory openfga garbage-json | EXPLORATORY | {'ok': 1827, 'authz': 5261} |
| X7 exploratory openfga truncate | EXPLORATORY | {'ok': 1840, 'authz': 5267} |
| X7 exploratory openfga type-flip | EXPLORATORY | {'ok': 1859, 'authz': 3683} |
| X7 exploratory spicedb drop-last | EXPLORATORY | {'ok': 2003, 'authz': 3938} |
| X7 exploratory spicedb empty | EXPLORATORY | {'ok': 1965, 'deviate': 4746, 'authz': 1} |
| X7 exploratory spicedb garbage-json | EXPLORATORY | {'ok': 1983, 'authz': 4817} |
| X7 exploratory spicedb truncate | EXPLORATORY | {'ok': 1986, 'authz': 4698} |
| X7 exploratory spicedb type-flip | EXPLORATORY | {'ok': 1937, 'authz': 4455} |
| X7-H8b cerbos blackhole recovery | CONFIRMED | median recovery 3.123 [3.116, 3.132] |
| X7-H8a cerbos blackhole | CONFIRMED | median recovery 0.082 [0.080, 0.084] |
| X7-H8b cerbos down recovery | CONFIRMED | median recovery 3.515 [3.505, 3.527] |
| X7 exploratory recovery cerbos down | EXPLORATORY | median recovery 0.201 [0.170, 0.220] |
| X7-H8b cerbos http500 recovery | CONFIRMED | median recovery 3.131 [3.124, 3.137] |
| X7-H8a cerbos http500 | CONFIRMED | median recovery 0.022 [0.016, 0.026] |
| X7-H8a cerbos http503 | CONFIRMED | median recovery 0.034 [0.015, 0.051] |
| X7-H8b cerbos refuse recovery | CONFIRMED | median recovery 3.474 [3.463, 3.482] |
| X7-H8a cerbos refuse | CONFIRMED | median recovery 0.061 [0.010, 0.072] |
| X7-H8b cerbos slow-3000 recovery | CONFIRMED | median recovery 3.122 [3.117, 3.126] |
| X7-H8a cerbos slow-3000 | CONFIRMED | median recovery 0.151 [0.144, 0.155] |
| X7-H8b opa blackhole recovery | CONFIRMED | median recovery 3.133 [3.125, 3.136] |
| X7-H8a opa blackhole | CONFIRMED | median recovery 0.101 [0.099, 0.103] |
| X7-H8b opa down recovery | CONFIRMED | median recovery 3.492 [3.482, 3.501] |
| X7 exploratory recovery opa down | EXPLORATORY | median recovery 0.081 [0.063, 0.090] |
| X7-H8b opa http500 recovery | CONFIRMED | median recovery 3.148 [3.140, 3.157] |
| X7-H8a opa http500 | CONFIRMED | median recovery 0.022 [0.019, 0.030] |
| X7-H8a opa http503 | CONFIRMED | median recovery 0.058 [0.033, 0.078] |
| X7-H8b opa refuse recovery | CONFIRMED | median recovery 3.493 [3.482, 3.499] |
| X7-H8a opa refuse | CONFIRMED | median recovery 0.048 [0.026, 0.076] |
| X7-H8b opa slow-3000 recovery | CONFIRMED | median recovery 3.127 [3.119, 3.146] |
| X7-H8a opa slow-3000 | CONFIRMED | median recovery 0.165 [0.158, 0.169] |
| X7-H8b openfga blackhole recovery | CONFIRMED | median recovery 3.137 [3.116, 3.148] |
| X7-H8a openfga blackhole | CONFIRMED | median recovery 0.098 [0.095, 0.105] |
| X7-H8b openfga down recovery | CONFIRMED | median recovery 3.554 [3.542, 3.566] |
| X7 exploratory recovery openfga down | EXPLORATORY | median recovery 0.214 [0.195, 0.222] |
| X7-H8b openfga http500 recovery | CONFIRMED | median recovery 3.139 [3.126, 3.152] |
| X7-H8a openfga http500 | CONFIRMED | median recovery 0.020 [0.016, 0.029] |
| X7-H8a openfga http503 | CONFIRMED | median recovery 0.068 [0.055, 0.082] |
| X7-H8b openfga refuse recovery | CONFIRMED | median recovery 3.481 [3.469, 3.485] |
| X7-H8a openfga refuse | CONFIRMED | median recovery 0.064 [0.036, 0.081] |
| X7-H8b openfga slow-3000 recovery | CONFIRMED | median recovery 3.129 [3.120, 3.135] |
| X7-H8a openfga slow-3000 | CONFIRMED | median recovery 0.159 [0.153, 0.166] |
| X7-H8b spicedb blackhole recovery | CONFIRMED | median recovery 3.137 [3.128, 3.141] |
| X7-H8a spicedb blackhole | CONFIRMED | median recovery 0.116 [0.110, 0.125] |
| X7-H8b spicedb down recovery | CONFIRMED | median recovery 3.548 [3.531, 3.570] |
| X7 exploratory recovery spicedb down | EXPLORATORY | median recovery 0.465 [0.445, 0.551] |
| X7-H8b spicedb http500 recovery | CONFIRMED | median recovery 3.148 [3.137, 3.163] |
| X7-H8a spicedb http500 | CONFIRMED | median recovery 0.030 [0.026, 0.040] |
| X7-H8a spicedb http503 | CONFIRMED | median recovery 0.044 [0.033, 0.064] |
| X7-H8b spicedb refuse recovery | CONFIRMED | median recovery 3.505 [3.488, 3.514] |
| X7-H8a spicedb refuse | CONFIRMED | median recovery 0.095 [0.084, 0.104] |
| X7-H8b spicedb slow-3000 recovery | CONFIRMED | median recovery 3.143 [3.138, 3.153] |
| X7-H8a spicedb slow-3000 | CONFIRMED | median recovery 0.178 [0.164, 0.182] |
| X7-H8b openfga blackhole fail-fast | CONFIRMED | failed latency 0.000 s with breaker, 2.003 s without |
| X7-H8b spicedb blackhole fail-fast | CONFIRMED | failed latency 1.0e-04 s with breaker, 2.002 s without |
| X7-H8b opa blackhole fail-fast | CONFIRMED | failed latency 1.0e-04 s with breaker, 2.003 s without |
| X7-H8b cerbos blackhole fail-fast | CONFIRMED | failed latency 5.0e-05 s with breaker, 2.003 s without |
| X7-H9 cerbos blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| acl-pgvector | nocache | 40 | 40 | 7.0e-04 [6.8e-04, 7.2e-04] | 0.086 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 7.0e-04 |
| acl-pgvector | ttl5 | 40 | 40 | 6.8e-04 [6.6e-04, 7.0e-04] | 0.095 | 0.010 | 0.000 | 0 | 0 | 0 | 0 | 6.8e-04 |
| acl-pgvector | ttl30 | 40 | 40 | 7.1e-04 [6.8e-04, 7.5e-04] | 0.046 | 0.012 | 0.000 | 0 | 0 | 0 | 0 | 7.1e-04 |
| acl-pgvector | ttl30-inv | 40 | 40 | 6.9e-04 [6.6e-04, 7.2e-04] | 0.082 | 0.025 | 0.000 | 0 | 0 | 0 | 0 | 6.8e-04 |
| acl-pgvector | ttl30-shared-inv | 40 | 40 | 0.001 [0.001, 0.001] | 0.030 | 0.006 | 0.000 | 0 | 0 | 0 | 0 | 7.0e-04 |
| acl-qdrant | nocache | 40 | 40 | 0.002 [0.002, 0.002] | 0.009 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl5 | 40 | 40 | 0.002 [0.002, 0.002] | 0.010 | 0.007 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30 | 40 | 40 | 0.002 [0.002, 0.002] | 0.009 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30-inv | 40 | 40 | 0.002 [0.002, 0.002] | 0.010 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30-shared-inv | 40 | 40 | 0.003 [0.003, 0.003] | 0.010 | 0.009 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| cerbos-policy | nocache | 40 | 40 | 2.549 [2.369, 3.219] | 4.035 | 3.954 | n/a | 0 | 0 | 0 | 0 | 4.8e-04 |
| cerbos-policy | ttl5 | 40 | 40 | 5.018 [5.010, 5.027] | 5.048 | 5.046 | n/a | 0 | 0 | 0 | 0 | 4.7e-04 |
| cerbos-policy | ttl30 | 40 | 40 | 30.017 [30.011, 30.021] | 30.044 | 30.042 | n/a | 0 | 0 | 0 | 0 | 4.8e-04 |
| cerbos-policy | ttl30-inv | 40 | 40 | 30.025 [30.019, 30.032] | 30.052 | 30.046 | n/a | 0 | 0 | 0 | 0 | 4.7e-04 |
| cerbos-policy | ttl30-shared-inv | 40 | 40 | 31.039 [31.026, 31.047] | 31.066 | 31.061 | n/a | 0 | 0 | 0 | 0 | 4.8e-04 |
| opa-data | nocache | 40 | 40 | 6.0e-04 [5.7e-04, 6.2e-04] | 0.003 | 0.001 | 0.000 | 0 | 0 | 0 | 0 | 6.0e-04 |
| opa-data | ttl5 | 40 | 40 | 5.034 [5.032, 5.037] | 5.047 | 5.044 | 5.000 | 0 | 0 | 0 | 0 | 6.1e-04 |
| opa-data | ttl30 | 40 | 40 | 30.033 [30.020, 30.036] | 30.048 | 30.046 | 30.000 | 0 | 0 | 0 | 0 | 6.0e-04 |
| opa-data | ttl30-inv | 40 | 40 | 6.0e-04 [5.8e-04, 6.2e-04] | 0.003 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 5.9e-04 |
| opa-data | ttl30-shared-inv | 40 | 40 | 1.018 [1.017, 1.019] | 1.025 | 1.023 | 1.000 | 0 | 0 | 0 | 0 | 5.9e-04 |
| opa-policy | nocache | 40 | 40 | 0.010 [0.009, 0.010] | 0.015 | 0.011 | 0.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl5 | 40 | 40 | 5.021 [5.020, 5.022] | 5.045 | 5.034 | 5.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl30 | 40 | 40 | 30.030 [30.028, 30.032] | 30.045 | 30.041 | 30.000 | 0 | 0 | 0 | 0 | 0.009 |
| opa-policy | ttl30-inv | 40 | 40 | 0.009 [0.009, 0.010] | 0.017 | 0.012 | 0.000 | 0 | 0 | 0 | 0 | 0.009 |
| opa-policy | ttl30-shared-inv | 40 | 40 | 1.022 [1.021, 1.023] | 1.028 | 1.026 | 1.000 | 0 | 0 | 0 | 0 | 0.009 |
| openfga | nocache | 40 | 40 | 0.003 [0.003, 0.004] | 0.006 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl5 | 40 | 40 | 5.015 [5.013, 5.020] | 5.039 | 5.039 | 5.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30 | 40 | 40 | 30.020 [30.014, 30.026] | 30.042 | 30.038 | 30.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30-inv | 40 | 40 | 0.003 [0.002, 0.004] | 0.078 | 0.008 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30-shared-inv | 40 | 40 | 1.014 [1.012, 1.015] | 1.021 | 1.017 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | nocache | 40 | 40 | 0.003 [0.003, 0.003] | 0.007 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl5 | 40 | 40 | 5.015 [5.015, 5.017] | 5.039 | 5.034 | 5.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl30 | 40 | 40 | 30.016 [30.009, 30.025] | 30.043 | 30.040 | 30.000 | 0 | 0 | 0 | 0 | 0.002 |
| openfga-cached-hc | ttl30-inv | 40 | 40 | 0.003 [0.002, 0.003] | 0.006 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl30-shared-inv | 40 | 40 | 1.015 [1.015, 1.016] | 1.020 | 1.017 | 1.000 | 0 | 0 | 0 | 0 | 0.002 |
| openfga-cached-ml | nocache | 40 | 40 | 0.003 [0.002, 0.003] | 0.008 | 0.004 | 10.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl5 | 40 | 40 | 5.015 [5.014, 5.016] | 5.045 | 5.023 | 15.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl30 | 40 | 40 | 30.022 [30.014, 30.031] | 30.044 | 30.039 | 40.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl30-inv | 40 | 40 | 0.003 [0.002, 0.003] | 0.006 | 0.004 | 10.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl30-shared-inv | 40 | 40 | 1.015 [1.015, 1.016] | 1.022 | 1.019 | 11.000 | 0 | 0 | 0 | 0 | 0.002 |
| spicedb-fc | nocache | 40 | 40 | 0.004 [0.003, 0.004] | 0.008 | 0.006 | 0.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl5 | 40 | 40 | 5.021 [5.019, 5.024] | 5.039 | 5.028 | 5.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30 | 40 | 40 | 30.017 [30.005, 30.026] | 30.045 | 30.041 | 30.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30-inv | 40 | 40 | 0.004 [0.004, 0.005] | 0.069 | 0.006 | 0.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30-shared-inv | 40 | 40 | 1.017 [1.016, 1.018] | 1.029 | 1.020 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | nocache | 40 | 40 | 3.251 [2.994, 3.371] | 8.742 | 4.938 | 5.500 | 1 | 0 | 28 | 0 | 0.004 |
| spicedb-ml | ttl5 | 40 | 40 | 5.023 [5.021, 5.026] | 6.828 | 5.034 | 10.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30 | 40 | 40 | 30.018 [30.008, 30.031] | 30.044 | 30.041 | 35.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-inv | 40 | 40 | 30.042 [30.031, 30.048] | 38.419 | 30.056 | 5.500 | 40 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-shared-inv | 40 | 40 | 31.048 [31.033, 31.061] | 32.359 | 31.073 | 6.500 | 39 | 0 | 0 | 0 | 0.003 |

## X7b: faults

1090 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos | allow-all | plain | 10 | 4954 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 22790 | 0 | 0 | 0.036 [0.024, 0.048] | n/a | {'ok': 1677, 'leak': 4998} |  |
| cerbos | blackhole | breaker | 10 | 972 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.123 [3.116, 3.132] | 5.0e-05 | {'ok': 2405, 'authz': 2516} | wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | blackhole | cache30 | 10 | 5597 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.014 [0.007, 0.023] | n/a | {'ok': 8454} |  |
| cerbos | blackhole | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.082 [0.080, 0.084] | 2.003 | {'ok': 2445, 'authz': 50} | wardowl.authz.AuthorizationError: Cerbos CheckResources timed out after 2.0 s; wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | down | breaker | 10 | 5721 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.515 [3.505, 3.527] | 0.000 | {'ok': 2448, 'authz': 7472} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | down | cache30 | 10 | 5535 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.013 [0.009, 0.020] | n/a | {'ok': 8445} |  |
| cerbos | down | plain | 10 | 1663 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.201 [0.170, 0.220] | 0.050 | {'ok': 2439, 'authz': 1714} | wardowl.authz.AuthorizationError: Cerbos CheckResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionResetError |
| cerbos | drop-last | plain | 10 | 4804 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.011, 0.028] | 0.004 | {'ok': 2423, 'authz': 4845} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned an unexpected response |
| cerbos | empty | plain | 10 | 5382 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.018 [0.011, 0.023] | 0.002 | {'ok': 2371, 'authz': 5429} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned invalid JSON; wardowl.authz.AuthorizationError: Cerbos PlanResources returned invalid JSON |
| cerbos | garbage-json | plain | 10 | 5443 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.017 [0.013, 0.021] | 0.002 | {'ok': 2395, 'authz': 5491} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned an unexpected response; wardowl.authz.AuthorizationError: Cerbos PlanResources returned an unexpected response |
| cerbos | http500 | breaker | 10 | 5878 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.131 [3.124, 3.137] | 1.0e-04 | {'ok': 2375, 'authz': 7461} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | http500 | cache30 | 10 | 5595 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.012 [0.009, 0.016] | n/a | {'ok': 8437} |  |
| cerbos | http500 | plain | 10 | 5823 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.022 [0.016, 0.026] | 2.0e-04 | {'ok': 2400, 'authz': 5872} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned HTTP 500; wardowl.authz.AuthorizationError: Cerbos PlanResources returned HTTP 500 |
| cerbos | http503 | plain | 10 | 1670 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.034 [0.015, 0.051] | 0.051 | {'ok': 2411, 'authz': 1690} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: HTTP 503 |
| cerbos | refuse | breaker | 10 | 5744 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.474 [3.463, 3.482] | 0.000 | {'ok': 2404, 'authz': 7467} | wardowl.authz.AuthorizationError: Cerbos CheckResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | refuse | cache30 | 10 | 5588 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.013 [0.009, 0.017] | n/a | {'ok': 8432} |  |
| cerbos | refuse | plain | 10 | 1675 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.061 [0.010, 0.072] | 0.051 | {'ok': 2403, 'authz': 1695} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError |
| cerbos | slow-1000 | plain | 10 | 41 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.175 [0.171, 0.181] | n/a | {'ok': 2474} |  |
| cerbos | slow-200 | plain | 10 | 270 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.165 [0.154, 0.176] | n/a | {'ok': 2715} |  |
| cerbos | slow-3000 | breaker | 10 | 971 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.122 [3.117, 3.126] | 5.0e-05 | {'ok': 2384, 'authz': 2514} | wardowl.authz.AuthorizationError: Cerbos CheckResources timed out after 2.0 s; wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | slow-3000 | cache30 | 10 | 5596 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.013 [0.007, 0.016] | n/a | {'ok': 8440} |  |
| cerbos | slow-3000 | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.151 [0.144, 0.155] | 2.003 | {'ok': 2396, 'authz': 60} | wardowl.authz.AuthorizationError: Cerbos CheckResources timed out after 2.0 s; wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | truncate | plain | 10 | 5460 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.020 [0.011, 0.023] | 0.001 | {'ok': 2412, 'authz': 5508} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned invalid JSON |
| cerbos | type-flip | plain | 10 | 5430 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.012 [0.008, 0.018] | 0.001 | {'ok': 2420, 'authz': 5477} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned an unexpected response |
| opa | allow-all | plain | 10 | 4134 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 17685 | 0 | 0 | 0.032 [0.023, 0.045] | n/a | {'ok': 1495, 'leak': 4171} |  |
| opa | blackhole | breaker | 10 | 967 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.133 [3.125, 3.136] | 1.0e-04 | {'ok': 1796, 'authz': 2498} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | blackhole | cache30 | 10 | 5376 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.008 [0.006, 0.015] | n/a | {'ok': 8092} |  |
| opa | blackhole | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.101 [0.099, 0.103] | 2.003 | {'ok': 1809, 'authz': 50} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | down | breaker | 10 | 5700 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.492 [3.482, 3.501] | 1.0e-04 | {'ok': 1836, 'authz': 7412} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | down | cache30 | 10 | 5366 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.019 [0.011, 0.025] | n/a | {'ok': 8084} |  |
| opa | down | plain | 10 | 1664 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.081 [0.063, 0.090] | 0.051 | {'ok': 1829, 'authz': 1692} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError |
| opa | drop-last | plain | 10 | 3546 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.028 [0.023, 0.041] | 0.013 | {'ok': 1805, 'authz': 3579} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |
| opa | empty | plain | 10 | 4713 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.027 [0.018, 0.031] | 0.004 | {'ok': 1794, 'authz': 4756} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned invalid JSON; wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | garbage-json | plain | 10 | 4704 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.029 [0.023, 0.034] | 0.005 | {'ok': 1798, 'authz': 4747} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions is undefined; wardowl.authz.AuthorizationError: OPA decision x4rel/filter is undefined |
| opa | http500 | breaker | 10 | 5846 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.148 [3.140, 3.157] | 1.0e-04 | {'ok': 1796, 'authz': 7416} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned HTTP 500; wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | http500 | cache30 | 10 | 5372 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.010, 0.019] | n/a | {'ok': 8081} |  |
| opa | http500 | plain | 10 | 5729 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.022 [0.019, 0.030] | 5.0e-04 | {'ok': 1785, 'authz': 5776} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned HTTP 500; wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500 |
| opa | http503 | plain | 10 | 1657 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.058 [0.033, 0.078] | 0.051 | {'ok': 1805, 'authz': 1677} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: HTTP 503; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: HTTP 503 |
| opa | refuse | breaker | 10 | 5697 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.493 [3.482, 3.499] | 1.0e-04 | {'ok': 1787, 'authz': 7406} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | refuse | cache30 | 10 | 5367 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.014 [0.006, 0.019] | n/a | {'ok': 8075} |  |
| opa | refuse | plain | 10 | 1668 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.048 [0.026, 0.076] | 0.051 | {'ok': 1805, 'authz': 1688} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError |
| opa | slow-1000 | plain | 10 | 41 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.222 [0.215, 0.232] | n/a | {'ok': 1863} |  |
| opa | slow-200 | plain | 10 | 262 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.148 [0.137, 0.152] | n/a | {'ok': 2073} |  |
| opa | slow-3000 | breaker | 10 | 965 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.127 [3.119, 3.146] | 1.0e-04 | {'ok': 1804, 'authz': 2497} | wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | slow-3000 | cache30 | 10 | 5366 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.015 [0.012, 0.017] | n/a | {'ok': 8075} |  |
| opa | slow-3000 | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.165 [0.158, 0.169] | 2.003 | {'ok': 1800, 'authz': 60} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | truncate | plain | 10 | 4709 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.033 [0.023, 0.034] | 0.005 | {'ok': 1796, 'authz': 4749} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned invalid JSON; wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | type-flip | plain | 10 | 3537 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.023 [0.017, 0.033] | 0.013 | {'ok': 1804, 'authz': 3571} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |
| openfga | allow-all | plain | 10 | 2011 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 7427 | 0 | 0 | 0.117 [0.034, 0.246] | n/a | {'ok': 454, 'leak': 2027} |  |
| openfga | blackhole | breaker | 10 | 974 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.137 [3.116, 3.148] | 0.000 | {'ok': 1853, 'authz': 2521} | wardowl.authz.AuthorizationError: OpenFGA batch-check timed out after 2.0 s; wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | blackhole | cache30 | 10 | 5631 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.008 [0.006, 0.014] | n/a | {'ok': 8472} |  |
| openfga | blackhole | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.098 [0.095, 0.105] | 2.003 | {'ok': 1854, 'authz': 50} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | down | breaker | 10 | 5722 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.554 [3.542, 3.566] | 0.000 | {'ok': 1848, 'authz': 7477} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | down | cache30 | 10 | 5564 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.013 [0.008, 0.019] | n/a | {'ok': 8440} |  |
| openfga | down | plain | 10 | 1661 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.214 [0.195, 0.222] | 0.050 | {'ok': 1854, 'authz': 1712} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionResetError |
| openfga | drop-last | plain | 10 | 3660 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.021, 0.036] | 0.011 | {'ok': 1854, 'authz': 3694} | wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d202': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d261': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d265': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d293': None; wardowl.authz.AuthorizationError: OpenFGA could not  |
| openfga | empty | plain | 10 | 5229 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.027 [0.020, 0.030] | 0.002 | {'ok': 1851, 'authz': 5272} | wardowl.authz.AuthorizationError: OpenFGA batch-check returned invalid JSON; wardowl.authz.AuthorizationError: OpenFGA list-objects returned invalid JSON |
| openfga | garbage-json | plain | 10 | 5220 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.018, 0.026] | 0.002 | {'ok': 1827, 'authz': 5261} | wardowl.authz.AuthorizationError: OpenFGA batch-check returned no result; wardowl.authz.AuthorizationError: OpenFGA list-objects returned an unexpected response |
| openfga | http500 | breaker | 10 | 5895 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.139 [3.126, 3.152] | 0.000 | {'ok': 1849, 'authz': 7480} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | http500 | cache30 | 10 | 5636 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.012 [0.008, 0.014] | n/a | {'ok': 8474} |  |
| openfga | http500 | plain | 10 | 5833 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.020 [0.016, 0.029] | 2.0e-04 | {'ok': 1844, 'authz': 5878} | wardowl.authz.AuthorizationError: OpenFGA batch-check returned HTTP 500; wardowl.authz.AuthorizationError: OpenFGA list-objects returned HTTP 500 |
| openfga | http503 | plain | 10 | 1669 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.068 [0.055, 0.082] | 0.051 | {'ok': 1861, 'authz': 1689} | wardowl.authz.AuthorizationError: OpenFGA list-objects failed: HTTP 503 |
| openfga | refuse | breaker | 10 | 5755 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.481 [3.469, 3.485] | 0.000 | {'ok': 1837, 'authz': 7481} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | refuse | cache30 | 10 | 5657 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.010 [0.005, 0.015] | n/a | {'ok': 8495} |  |
| openfga | refuse | plain | 10 | 1675 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.064 [0.036, 0.081] | 0.050 | {'ok': 1854, 'authz': 1695} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError |
| openfga | slow-1000 | plain | 10 | 41 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.235 [0.210, 0.254] | n/a | {'ok': 1881} |  |
| openfga | slow-200 | plain | 10 | 261 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.085 [0.073, 0.137] | n/a | {'ok': 2154} |  |
| openfga | slow-3000 | breaker | 10 | 973 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.129 [3.120, 3.135] | 0.000 | {'ok': 1834, 'authz': 2518} | wardowl.authz.AuthorizationError: OpenFGA batch-check timed out after 2.0 s; wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | slow-3000 | cache30 | 10 | 5639 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.011 [0.002, 0.014] | n/a | {'ok': 8483} |  |
| openfga | slow-3000 | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.159 [0.153, 0.166] | 2.003 | {'ok': 1840, 'authz': 60} | wardowl.authz.AuthorizationError: OpenFGA batch-check timed out after 2.0 s; wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | truncate | plain | 10 | 5219 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.023 [0.017, 0.031] | 0.002 | {'ok': 1840, 'authz': 5267} | wardowl.authz.AuthorizationError: OpenFGA batch-check returned invalid JSON; wardowl.authz.AuthorizationError: OpenFGA list-objects returned invalid JSON |
| openfga | type-flip | plain | 10 | 3649 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.012, 0.026] | 0.011 | {'ok': 1859, 'authz': 3683} | wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d1': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d100': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d104': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d112': {'allowed': 'tr |
| pgvector | blackhole | plain | 10 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 5 | 0 | 0.555 [0.042, 2.880] | n/a | {'ok': 2235, 'hang': 8, 'error': 5} | psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | down | plain | 10 | 10 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 23 | 0 | 2.300 [1.963, 2.825] | 5.000 | {'ok': 2754, 'error': 23} | psycopg.OperationalError: consuming input failed: server closed the connection unexpectedly 	This probably means the ser; psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | refuse | plain | 10 | 10 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 23 | 0 | 2.617 [1.909, 3.278] | 5.000 | {'ok': 2432, 'error': 23} | psycopg.OperationalError: consuming input failed: server closed the connection unexpectedly 	This probably means the ser; psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | slow-1000 | plain | 10 | 19 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.110 [0.100, 0.115] | n/a | {'ok': 2285} |  |
| pgvector | slow-200 | plain | 10 | 133 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.168 [0.159, 0.175] | n/a | {'ok': 2887} |  |
| qdrant | blackhole | plain | 10 | 10 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.025 [0.025, 0.025] | 5.006 | {'ok': 2648, 'error': 30} | qdrant_client.http.exceptions.ResponseHandlingException: Server disconnected without sending a response.; qdrant_client.http.exceptions.ResponseHandlingException: timed out |
| qdrant | down | plain | 10 | 5570 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5829 | 0 | 0.287 [0.249, 0.310] | 7.0e-04 | {'ok': 2709, 'error': 5829} | qdrant_client.http.exceptions.ResponseHandlingException: Server disconnected without sending a response.; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 104] Connection reset by peer; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | http500 | plain | 10 | 5553 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5600 | 0 | 0.013 [0.008, 0.017] | 0.001 | {'ok': 2649, 'error': 5600} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 500 (Injected) Raw response content: b'{"error":" |
| qdrant | http503 | plain | 10 | 5550 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5599 | 0 | 0.014 [0.005, 0.018] | 0.001 | {'ok': 2652, 'error': 5599} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 503 (Injected) Raw response content: b'{"error":" |
| qdrant | refuse | plain | 10 | 5683 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5731 | 0 | 0.013 [0.010, 0.022] | 7.0e-04 | {'ok': 2648, 'error': 5731} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | slow-1000 | plain | 10 | 100 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.298 [0.293, 0.306] | n/a | {'ok': 2768} |  |
| qdrant | slow-200 | plain | 10 | 520 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.072 [0.067, 0.104] | n/a | {'ok': 3194} |  |
| qdrant | truncate | plain | 10 | 5236 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5285 | 0 | 0.013 [0.007, 0.020] | 0.002 | {'ok': 2646, 'error': 5285} | json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 315 (char 314); json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 319 (char 318); json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 321 (char 320); json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 322 (char 321); json.decoder.JSONDecodeError: Expecting ',' delimiter: line  |
| spicedb | allow-all | plain | 10 | 4846 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 17484 | 0 | 0 | 0.019 [0.008, 0.025] | n/a | {'ok': 2186, 'leak': 4887} |  |
| spicedb | blackhole | breaker | 10 | 971 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.137 [3.128, 3.141] | 1.0e-04 | {'ok': 1970, 'authz': 2509} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions timed out after 2.0 s; wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | blackhole | cache30 | 10 | 5604 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.018 [0.011, 0.021] | n/a | {'ok': 8424} |  |
| spicedb | blackhole | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.116 [0.110, 0.125] | 2.002 | {'ok': 1963, 'authz': 50} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | down | breaker | 10 | 5696 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.548 [3.531, 3.570] | 1.0e-04 | {'ok': 1939, 'authz': 7445} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionResetError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | down | cache30 | 10 | 5463 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.008, 0.020] | n/a | {'ok': 8424} |  |
| spicedb | down | plain | 10 | 1644 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.465 [0.445, 0.551] | 0.051 | {'ok': 2030, 'authz': 1745} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionResetError |
| spicedb | drop-last | plain | 10 | 3903 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.024 [0.013, 0.026] | 0.009 | {'ok': 2003, 'authz': 3938} | wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d181': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d254': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d299': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None |
| spicedb | empty | plain | 10 | 4703 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.026 [0.021, 0.030] | n/a | {'ok': 1965, 'deviate': 4746, 'authz': 1} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned invalid JSON |
| spicedb | garbage-json | plain | 10 | 4772 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.026 [0.021, 0.034] | 0.004 | {'ok': 1983, 'authz': 4817} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned an unexpected response; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: {'unexpected': True} |
| spicedb | http500 | breaker | 10 | 5872 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.148 [3.137, 3.163] | 5.0e-05 | {'ok': 1933, 'authz': 7449} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned HTTP 500; wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | http500 | cache30 | 10 | 5590 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.015 [0.008, 0.020] | n/a | {'ok': 8415} |  |
| spicedb | http500 | plain | 10 | 5803 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.026, 0.040] | 3.0e-04 | {'ok': 1923, 'authz': 5852} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned HTTP 500; wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500 |
| spicedb | http503 | plain | 10 | 1667 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.044 [0.033, 0.064] | 0.051 | {'ok': 1950, 'authz': 1687} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: HTTP 503; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: HTTP 503 |
| spicedb | refuse | breaker | 10 | 5732 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.505 [3.488, 3.514] | 0.000 | {'ok': 1969, 'authz': 7454} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | refuse | cache30 | 10 | 5607 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.010 [0.008, 0.016] | n/a | {'ok': 8428} |  |
| spicedb | refuse | plain | 10 | 1670 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.095 [0.084, 0.104] | 0.051 | {'ok': 1991, 'authz': 1690} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError |
| spicedb | slow-1000 | plain | 10 | 43 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.293 [0.266, 0.342] | n/a | {'ok': 2043} |  |
| spicedb | slow-200 | plain | 10 | 259 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.125 [0.082, 0.204] | n/a | {'ok': 2267} |  |
| spicedb | slow-3000 | breaker | 10 | 969 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.143 [3.138, 3.153] | 1.0e-04 | {'ok': 1925, 'authz': 2509} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions timed out after 2.0 s; wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | slow-3000 | cache30 | 10 | 5610 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.006 [0.004, 0.014] | n/a | {'ok': 8442} |  |
| spicedb | slow-3000 | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.178 [0.164, 0.182] | 2.003 | {'ok': 1973, 'authz': 60} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions timed out after 2.0 s; wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | truncate | plain | 10 | 4654 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.027 [0.020, 0.035] | 0.004 | {'ok': 1986, 'authz': 4698} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned invalid JSON; wardowl.authz.AuthorizationError: SpiceDB LookupResources returned invalid JSON |
| spicedb | type-flip | plain | 10 | 4414 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.037 [0.022, 0.041] | 0.006 | {'ok': 1937, 'authz': 4455} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned 'X_UNKNOWN_VALUE'; wardowl.authz.AuthorizationError: SpiceDB returned 'X_UNKNOWN_VALUE' for 'fsp3d145': no answer, or a caveat that needs c |

## Harness

Runs: 9 job records; profile ['full']; commit ['e66dffc'].
