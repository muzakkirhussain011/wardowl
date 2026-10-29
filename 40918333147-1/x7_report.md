# X7: revocation and faults

Profile: ['smoke']. Files: 9; records: 202. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 acl-pgvector nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector nocache | INCONCLUSIVE | median 9.9e-04 [9.9e-04, 9.9e-04] |
| X7-H1 acl-pgvector ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl5 | INCONCLUSIVE | median 8.8e-04 [8.8e-04, 8.8e-04] |
| X7-H1 acl-pgvector ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl30 | INCONCLUSIVE | median 9.1e-04 [9.1e-04, 9.1e-04] |
| X7-H1 acl-pgvector ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-inv | INCONCLUSIVE | median 9.7e-04 [9.7e-04, 9.7e-04], limit 0.5 |
| X7-H4 acl-pgvector ttl30-inv | INCONCLUSIVE | median 9.7e-04 [9.7e-04, 9.7e-04] |
| X7-H1 acl-pgvector ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-shared-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002], limit 1.5 |
| X7-H4 acl-pgvector ttl30-shared-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant nocache | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl5 | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl30 | INCONCLUSIVE | median 0.003 [0.003, 0.003] |
| X7-H1 acl-qdrant ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002], limit 0.5 |
| X7-H4 acl-qdrant ttl30-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-shared-inv | INCONCLUSIVE | median 0.003 [0.003, 0.003], limit 1.5 |
| X7-H4 acl-qdrant ttl30-shared-inv | INCONCLUSIVE | median 0.003 [0.003, 0.003] |
| X7 exploratory cerbos-policy nocache | EXPLORATORY | median 3.927 [3.927, 3.927], maximum 3.927 |
| X7 exploratory cerbos-policy ttl5 | EXPLORATORY | median 5.011 [5.011, 5.011], maximum 5.011 |
| X7 exploratory cerbos-policy ttl30 | EXPLORATORY | median 30.039 [30.039, 30.039], maximum 30.039 |
| X7 exploratory cerbos-policy ttl30-inv | EXPLORATORY | median 30.042 [30.042, 30.042], maximum 30.042 |
| X7 exploratory cerbos-policy ttl30-shared-inv | EXPLORATORY | median 31.055 [31.055, 31.055], maximum 31.055 |
| X7-H1 opa-data nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-data ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-data ttl5 | INCONCLUSIVE | median 5.021 [5.021, 5.021] against [4.0, 6.0] |
| X7-H1 opa-data ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-data ttl30 | INCONCLUSIVE | median 30.032 [30.032, 30.032] against [29.0, 31.0] |
| X7-H1 opa-data ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-data ttl30-inv | INCONCLUSIVE | median 6.7e-04 [6.7e-04, 6.7e-04], limit 0.5 |
| X7-H1 opa-data ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-data ttl30-shared-inv | INCONCLUSIVE | median 0.987 [0.987, 0.987], limit 1.5 |
| X7-H1 opa-policy nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-policy ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-policy ttl5 | INCONCLUSIVE | median 5.029 [5.029, 5.029] against [4.0, 6.0] |
| X7-H1 opa-policy ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-policy ttl30 | INCONCLUSIVE | median 30.046 [30.046, 30.046] against [29.0, 31.0] |
| X7-H1 opa-policy ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-policy ttl30-inv | INCONCLUSIVE | median 0.010 [0.010, 0.010], limit 0.5 |
| X7-H1 opa-policy ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-policy ttl30-shared-inv | INCONCLUSIVE | median 1.030 [1.030, 1.030], limit 1.5 |
| X7-H1 openfga nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga ttl5 | INCONCLUSIVE | median 4.964 [4.964, 4.964] against [4.0, 6.0] |
| X7-H1 openfga ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga ttl30 | INCONCLUSIVE | median 30.026 [30.026, 30.026] against [29.0, 31.0] |
| X7-H1 openfga ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga ttl30-inv | INCONCLUSIVE | median 0.004 [0.004, 0.004], limit 0.5 |
| X7-H1 openfga ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga ttl30-shared-inv | INCONCLUSIVE | median 1.016 [1.016, 1.016], limit 1.5 |
| X7-H1 openfga-cached-hc nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga-cached-hc ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga-cached-hc ttl5 | INCONCLUSIVE | median 5.014 [5.014, 5.014] against [4.0, 6.0] |
| X7-H1 openfga-cached-hc ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga-cached-hc ttl30 | INCONCLUSIVE | median 29.963 [29.963, 29.963] against [29.0, 31.0] |
| X7-H1 openfga-cached-hc ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga-cached-hc ttl30-inv | INCONCLUSIVE | median 0.004 [0.004, 0.004], limit 0.5 |
| X7-H1 openfga-cached-hc ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga-cached-hc ttl30-shared-inv | INCONCLUSIVE | median 1.015 [1.015, 1.015], limit 1.5 |
| X7-H1 openfga-cached-ml nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7 exploratory openfga-cached-ml nocache | EXPLORATORY | median 0.004 [0.004, 0.004], maximum 0.004 |
| X7-H1 openfga-cached-ml ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 15.0 |
| X7 exploratory openfga-cached-ml ttl5 | EXPLORATORY | median 5.016 [5.016, 5.016], maximum 5.016 |
| X7-H1 openfga-cached-ml ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 40.0 |
| X7 exploratory openfga-cached-ml ttl30 | EXPLORATORY | median 29.996 [29.996, 29.996], maximum 29.996 |
| X7-H1 openfga-cached-ml ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7-H3 openfga-cached-ml ttl30-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002], limit 10.5 |
| X7 exploratory openfga-cached-ml ttl30-inv | EXPLORATORY | median 0.002 [0.002, 0.002], maximum 0.002 |
| X7-H1 openfga-cached-ml ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 11.0 |
| X7-H3 openfga-cached-ml ttl30-shared-inv | INCONCLUSIVE | median 1.017 [1.017, 1.017], limit 11.5 |
| X7 exploratory openfga-cached-ml ttl30-shared-inv | EXPLORATORY | median 1.017 [1.017, 1.017], maximum 1.017 |
| X7-H1 spicedb-fc nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 spicedb-fc ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 spicedb-fc ttl5 | INCONCLUSIVE | median 5.030 [5.030, 5.030] against [4.0, 6.0] |
| X7-H1 spicedb-fc ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 spicedb-fc ttl30 | INCONCLUSIVE | median 30.017 [30.017, 30.017] against [29.0, 31.0] |
| X7-H1 spicedb-fc ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 spicedb-fc ttl30-inv | INCONCLUSIVE | median 0.003 [0.003, 0.003], limit 0.5 |
| X7-H1 spicedb-fc ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 spicedb-fc ttl30-shared-inv | INCONCLUSIVE | median 1.018 [1.018, 1.018], limit 1.5 |
| X7-H1 spicedb-ml nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H5 spicedb-ml staleness | INCONCLUSIVE | median 4.604 [4.604, 4.604], maximum 4.604 |
| X7-H1 spicedb-ml ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.5 |
| X7-H2 spicedb-ml ttl5 | INCONCLUSIVE | median 5.017 [5.017, 5.017] against [4.0, 11.5] |
| X7-H1 spicedb-ml ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 35.5 |
| X7-H2 spicedb-ml ttl30 | INCONCLUSIVE | median 30.011 [30.011, 30.011] against [29.0, 36.5] |
| X7-H1 spicedb-ml ttl30-inv | FALSIFIED | 1 valid trials, 1 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H3 spicedb-ml ttl30-inv | INCONCLUSIVE | median 30.036 [30.036, 30.036], limit 6.0 |
| X7-H1 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 6.5 |
| X7-H3 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | median 1.017 [1.017, 1.017], limit 7.0 |
| G3 leak detection (allow-all leaks) | CONFIRMED | {'spicedb': 619, 'cerbos': 831, 'opa': 691, 'openfga': 500} |
| X7-H6 fail closed | INCONCLUSIVE | 30307 requests: 0 leaks (one-sided bound 0.000099), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 1414 store-fault failures, 0 naming a host |
| X7-H7a cerbos blackhole | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7a cerbos down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 81 requests |
| X7-H7a cerbos http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 286 requests |
| X7-H7a cerbos http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7a cerbos refuse | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7b cerbos slow-1000 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 1 requests |
| X7-H7b cerbos slow-1000 latency rise | INCONCLUSIVE | median rise 2.002 [2.002, 2.002] s against 1.0 s |
| X7-H7b cerbos slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 13 requests |
| X7-H7b cerbos slow-200 latency rise | INCONCLUSIVE | median rise 0.401 [0.401, 0.401] s against 0.2 s |
| X7-H7a cerbos slow-3000 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7a opa blackhole | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7a opa down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7a opa http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 287 requests |
| X7-H7a opa http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7a opa refuse | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7b opa slow-1000 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 1 requests |
| X7-H7b opa slow-1000 latency rise | INCONCLUSIVE | median rise 2.001 [2.001, 2.001] s against 1.0 s |
| X7-H7b opa slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 13 requests |
| X7-H7b opa slow-200 latency rise | INCONCLUSIVE | median rise 0.400 [0.400, 0.400] s against 0.2 s |
| X7-H7a opa slow-3000 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7a openfga blackhole | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7a openfga down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 80 requests |
| X7-H7a openfga http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 286 requests |
| X7-H7a openfga http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7a openfga refuse | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7b openfga slow-1000 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 1 requests |
| X7-H7b openfga slow-1000 latency rise | INCONCLUSIVE | median rise 2.000 [2.000, 2.000] s against 1.0 s |
| X7-H7b openfga slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 12 requests |
| X7-H7b openfga slow-200 latency rise | INCONCLUSIVE | median rise 0.397 [0.397, 0.397] s against 0.2 s |
| X7-H7a openfga slow-3000 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7a spicedb blackhole | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7a spicedb down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 81 requests |
| X7-H7a spicedb http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 286 requests |
| X7-H7a spicedb http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7a spicedb refuse | INCONCLUSIVE | 1.000 [1.000, 1.000] over 82 requests |
| X7-H7b spicedb slow-1000 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 1 requests |
| X7-H7b spicedb slow-1000 latency rise | INCONCLUSIVE | median rise 2.004 [2.004, 2.004] s against 1.0 s |
| X7-H7b spicedb slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 12 requests |
| X7-H7b spicedb slow-200 latency rise | INCONCLUSIVE | median rise 0.401 [0.401, 0.401] s against 0.2 s |
| X7-H7a spicedb slow-3000 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 1 requests |
| X7-H7c pgvector blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector down | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector refuse | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b pgvector slow-1000 failing | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b pgvector slow-1000 latency rise | INCONCLUSIVE | median rise n/a [n/a, n/a] s against 1.0 s |
| X7-H7b pgvector slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 6 requests |
| X7-H7b pgvector slow-200 latency rise | INCONCLUSIVE | median rise 0.802 [0.802, 0.802] s against 0.2 s |
| X7-H7c qdrant blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c qdrant down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 276 requests |
| X7-H7c qdrant http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 276 requests |
| X7-H7c qdrant http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 277 requests |
| X7-H7c qdrant refuse | INCONCLUSIVE | 1.000 [1.000, 1.000] over 283 requests |
| X7-H7b qdrant slow-1000 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 4 requests |
| X7-H7b qdrant slow-1000 latency rise | INCONCLUSIVE | median rise 1.001 [1.001, 1.001] s against 1.0 s |
| X7-H7b qdrant slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 25 requests |
| X7-H7b qdrant slow-200 latency rise | INCONCLUSIVE | median rise 0.201 [0.201, 0.201] s against 0.2 s |
| X7-H7c qdrant truncate | INCONCLUSIVE | 1.000 [1.000, 1.000] over 262 requests |
| X7 exploratory cerbos drop-last | EXPLORATORY | {'ok': 96, 'authz': 227} |
| X7 exploratory cerbos empty | EXPLORATORY | {'ok': 98, 'authz': 270} |
| X7 exploratory cerbos garbage-json | EXPLORATORY | {'ok': 96, 'authz': 265} |
| X7 exploratory cerbos truncate | EXPLORATORY | {'ok': 97, 'authz': 267} |
| X7 exploratory cerbos type-flip | EXPLORATORY | {'ok': 96, 'authz': 266} |
| X7 exploratory opa drop-last | EXPLORATORY | {'ok': 100, 'authz': 237} |
| X7 exploratory opa empty | EXPLORATORY | {'ok': 100, 'authz': 271} |
| X7 exploratory opa garbage-json | EXPLORATORY | {'ok': 98, 'authz': 270} |
| X7 exploratory opa truncate | EXPLORATORY | {'ok': 99, 'authz': 270} |
| X7 exploratory opa type-flip | EXPLORATORY | {'ok': 98, 'authz': 234} |
| X7 exploratory openfga drop-last | EXPLORATORY | {'ok': 76, 'authz': 177} |
| X7 exploratory openfga empty | EXPLORATORY | {'ok': 70, 'authz': 255} |
| X7 exploratory openfga garbage-json | EXPLORATORY | {'ok': 74, 'authz': 253} |
| X7 exploratory openfga truncate | EXPLORATORY | {'ok': 74, 'authz': 254} |
| X7 exploratory openfga type-flip | EXPLORATORY | {'ok': 74, 'authz': 178} |
| X7 exploratory spicedb drop-last | EXPLORATORY | {'ok': 81, 'authz': 191} |
| X7 exploratory spicedb empty | EXPLORATORY | {'ok': 79, 'deviate': 235} |
| X7 exploratory spicedb garbage-json | EXPLORATORY | {'ok': 81, 'authz': 235} |
| X7 exploratory spicedb truncate | EXPLORATORY | {'ok': 81, 'authz': 233} |
| X7 exploratory spicedb type-flip | EXPLORATORY | {'ok': 82, 'authz': 228} |
| X7-H8b cerbos blackhole recovery | INCONCLUSIVE | median recovery 0.030 [0.030, 0.030] |
| X7-H8a cerbos blackhole | INCONCLUSIVE | median recovery 0.030 [0.030, 0.030] |
| X7-H8b cerbos down recovery | INCONCLUSIVE | median recovery 4.492 [4.492, 4.492] |
| X7 exploratory recovery cerbos down | EXPLORATORY | median recovery 0.275 [0.275, 0.275] |
| X7-H8b cerbos http500 recovery | INCONCLUSIVE | median recovery 4.144 [4.144, 4.144] |
| X7-H8a cerbos http500 | INCONCLUSIVE | median recovery 0.016 [0.016, 0.016] |
| X7-H8a cerbos http503 | INCONCLUSIVE | median recovery 0.079 [0.079, 0.079] |
| X7-H8b cerbos refuse recovery | INCONCLUSIVE | median recovery 4.438 [4.438, 4.438] |
| X7-H8a cerbos refuse | INCONCLUSIVE | median recovery 0.052 [0.052, 0.052] |
| X7-H8b cerbos slow-3000 recovery | INCONCLUSIVE | median recovery 0.086 [0.086, 0.086] |
| X7-H8a cerbos slow-3000 | INCONCLUSIVE | median recovery 0.088 [0.088, 0.088] |
| X7-H8b opa blackhole recovery | INCONCLUSIVE | median recovery 0.030 [0.030, 0.030] |
| X7-H8a opa blackhole | INCONCLUSIVE | median recovery 0.029 [0.029, 0.029] |
| X7-H8b opa down recovery | INCONCLUSIVE | median recovery 4.430 [4.430, 4.430] |
| X7 exploratory recovery opa down | EXPLORATORY | median recovery 0.044 [0.044, 0.044] |
| X7-H8b opa http500 recovery | INCONCLUSIVE | median recovery 4.117 [4.117, 4.117] |
| X7-H8a opa http500 | INCONCLUSIVE | median recovery 0.017 [0.017, 0.017] |
| X7-H8a opa http503 | INCONCLUSIVE | median recovery 0.009 [0.009, 0.009] |
| X7-H8b opa refuse recovery | INCONCLUSIVE | median recovery 4.420 [4.420, 4.420] |
| X7-H8a opa refuse | INCONCLUSIVE | median recovery 0.060 [0.060, 0.060] |
| X7-H8b opa slow-3000 recovery | INCONCLUSIVE | median recovery 0.093 [0.093, 0.093] |
| X7-H8a opa slow-3000 | INCONCLUSIVE | median recovery 0.094 [0.094, 0.094] |
| X7-H8b openfga blackhole recovery | INCONCLUSIVE | median recovery 0.105 [0.105, 0.105] |
| X7-H8a openfga blackhole | INCONCLUSIVE | median recovery 0.089 [0.089, 0.089] |
| X7-H8b openfga down recovery | INCONCLUSIVE | median recovery 4.531 [4.531, 4.531] |
| X7 exploratory recovery openfga down | EXPLORATORY | median recovery 0.261 [0.261, 0.261] |
| X7-H8b openfga http500 recovery | INCONCLUSIVE | median recovery 4.144 [4.144, 4.144] |
| X7-H8a openfga http500 | INCONCLUSIVE | median recovery 0.031 [0.031, 0.031] |
| X7-H8a openfga http503 | INCONCLUSIVE | median recovery 0.083 [0.083, 0.083] |
| X7-H8b openfga refuse recovery | INCONCLUSIVE | median recovery 4.433 [4.433, 4.433] |
| X7-H8a openfga refuse | INCONCLUSIVE | median recovery 0.052 [0.052, 0.052] |
| X7-H8b openfga slow-3000 recovery | INCONCLUSIVE | median recovery 0.099 [0.099, 0.099] |
| X7-H8a openfga slow-3000 | INCONCLUSIVE | median recovery 0.088 [0.088, 0.088] |
| X7-H8b spicedb blackhole recovery | INCONCLUSIVE | median recovery 0.123 [0.123, 0.123] |
| X7-H8a spicedb blackhole | INCONCLUSIVE | median recovery 0.096 [0.096, 0.096] |
| X7-H8b spicedb down recovery | INCONCLUSIVE | median recovery 4.518 [4.518, 4.518] |
| X7 exploratory recovery spicedb down | EXPLORATORY | median recovery 0.326 [0.326, 0.326] |
| X7-H8b spicedb http500 recovery | INCONCLUSIVE | median recovery 4.160 [4.160, 4.160] |
| X7-H8a spicedb http500 | INCONCLUSIVE | median recovery 0.030 [0.030, 0.030] |
| X7-H8a spicedb http503 | INCONCLUSIVE | median recovery 0.139 [0.139, 0.139] |
| X7-H8b spicedb refuse recovery | INCONCLUSIVE | median recovery 4.444 [4.444, 4.444] |
| X7-H8a spicedb refuse | INCONCLUSIVE | median recovery 0.085 [0.085, 0.085] |
| X7-H8b spicedb slow-3000 recovery | INCONCLUSIVE | median recovery 0.108 [0.108, 0.108] |
| X7-H8a spicedb slow-3000 | INCONCLUSIVE | median recovery 0.093 [0.093, 0.093] |
| X7-H8b openfga blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.003 s without |
| X7-H8b spicedb blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.003 s without |
| X7-H8b opa blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.002 s without |
| X7-H8b cerbos blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.003 s without |
| X7-H9 cerbos blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| acl-pgvector | nocache | 1 | 1 | 9.9e-04 [9.9e-04, 9.9e-04] | 9.9e-04 | 9.9e-04 | 0.000 | 0 | 0 | 0 | 0 | 9.9e-04 |
| acl-pgvector | ttl5 | 1 | 1 | 8.8e-04 [8.8e-04, 8.8e-04] | 8.8e-04 | 8.8e-04 | 0.000 | 0 | 0 | 0 | 0 | 8.8e-04 |
| acl-pgvector | ttl30 | 1 | 1 | 9.1e-04 [9.1e-04, 9.1e-04] | 9.1e-04 | 9.1e-04 | 0.000 | 0 | 0 | 0 | 0 | 9.0e-04 |
| acl-pgvector | ttl30-inv | 1 | 1 | 9.7e-04 [9.7e-04, 9.7e-04] | 9.7e-04 | 9.7e-04 | 0.000 | 0 | 0 | 0 | 0 | 9.6e-04 |
| acl-pgvector | ttl30-shared-inv | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 9.5e-04 |
| acl-qdrant | nocache | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl5 | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30 | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| acl-qdrant | ttl30-inv | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30-shared-inv | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| cerbos-policy | nocache | 1 | 1 | 3.927 [3.927, 3.927] | 3.927 | 3.927 | n/a | 0 | 0 | 0 | 0 | 3.4e-04 |
| cerbos-policy | ttl5 | 1 | 1 | 5.011 [5.011, 5.011] | 5.011 | 5.011 | n/a | 0 | 0 | 0 | 0 | 5.0e-04 |
| cerbos-policy | ttl30 | 1 | 1 | 30.039 [30.039, 30.039] | 30.039 | 30.039 | n/a | 0 | 0 | 0 | 0 | 4.5e-04 |
| cerbos-policy | ttl30-inv | 1 | 1 | 30.042 [30.042, 30.042] | 30.042 | 30.042 | n/a | 0 | 0 | 0 | 0 | 5.2e-04 |
| cerbos-policy | ttl30-shared-inv | 1 | 1 | 31.055 [31.055, 31.055] | 31.055 | 31.055 | n/a | 0 | 0 | 0 | 0 | 4.9e-04 |
| opa-data | nocache | 1 | 1 | 5.2e-04 [5.2e-04, 5.2e-04] | 5.2e-04 | 5.2e-04 | 0.000 | 0 | 0 | 0 | 0 | 5.2e-04 |
| opa-data | ttl5 | 1 | 1 | 5.021 [5.021, 5.021] | 5.021 | 5.021 | 5.000 | 0 | 0 | 0 | 0 | 6.1e-04 |
| opa-data | ttl30 | 1 | 1 | 30.032 [30.032, 30.032] | 30.032 | 30.032 | 30.000 | 0 | 0 | 0 | 0 | 6.0e-04 |
| opa-data | ttl30-inv | 1 | 1 | 6.7e-04 [6.7e-04, 6.7e-04] | 6.7e-04 | 6.7e-04 | 0.000 | 0 | 0 | 0 | 0 | 6.6e-04 |
| opa-data | ttl30-shared-inv | 1 | 1 | 0.987 [0.987, 0.987] | 0.987 | 0.987 | 1.000 | 0 | 0 | 0 | 0 | 7.4e-04 |
| opa-policy | nocache | 1 | 1 | 0.010 [0.010, 0.010] | 0.010 | 0.010 | 0.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl5 | 1 | 1 | 5.029 [5.029, 5.029] | 5.029 | 5.029 | 5.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl30 | 1 | 1 | 30.046 [30.046, 30.046] | 30.046 | 30.046 | 30.000 | 0 | 0 | 0 | 0 | 0.012 |
| opa-policy | ttl30-inv | 1 | 1 | 0.010 [0.010, 0.010] | 0.010 | 0.010 | 0.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl30-shared-inv | 1 | 1 | 1.030 [1.030, 1.030] | 1.030 | 1.030 | 1.000 | 0 | 0 | 0 | 0 | 0.009 |
| openfga | nocache | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl5 | 1 | 1 | 4.964 [4.964, 4.964] | 4.964 | 4.964 | 5.000 | 0 | 0 | 0 | 0 | 0.004 |
| openfga | ttl30 | 1 | 1 | 30.026 [30.026, 30.026] | 30.026 | 30.026 | 30.000 | 0 | 0 | 0 | 0 | 0.005 |
| openfga | ttl30-inv | 1 | 1 | 0.004 [0.004, 0.004] | 0.004 | 0.004 | 0.000 | 0 | 0 | 0 | 0 | 0.004 |
| openfga | ttl30-shared-inv | 1 | 1 | 1.016 [1.016, 1.016] | 1.016 | 1.016 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | nocache | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl5 | 1 | 1 | 5.014 [5.014, 5.014] | 5.014 | 5.014 | 5.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl30 | 1 | 1 | 29.963 [29.963, 29.963] | 29.963 | 29.963 | 30.000 | 0 | 0 | 0 | 0 | 0.004 |
| openfga-cached-hc | ttl30-inv | 1 | 1 | 0.004 [0.004, 0.004] | 0.004 | 0.004 | 0.000 | 0 | 0 | 0 | 0 | 0.004 |
| openfga-cached-hc | ttl30-shared-inv | 1 | 1 | 1.015 [1.015, 1.015] | 1.015 | 1.015 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | nocache | 1 | 1 | 0.004 [0.004, 0.004] | 0.004 | 0.004 | 10.000 | 0 | 0 | 0 | 0 | 0.004 |
| openfga-cached-ml | ttl5 | 1 | 1 | 5.016 [5.016, 5.016] | 5.016 | 5.016 | 15.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl30 | 1 | 1 | 29.996 [29.996, 29.996] | 29.996 | 29.996 | 40.000 | 0 | 0 | 0 | 0 | 0.007 |
| openfga-cached-ml | ttl30-inv | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 10.000 | 0 | 0 | 0 | 0 | 0.002 |
| openfga-cached-ml | ttl30-shared-inv | 1 | 1 | 1.017 [1.017, 1.017] | 1.017 | 1.017 | 11.000 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-fc | nocache | 1 | 1 | 0.005 [0.005, 0.005] | 0.005 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.005 |
| spicedb-fc | ttl5 | 1 | 1 | 5.030 [5.030, 5.030] | 5.030 | 5.030 | 5.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30 | 1 | 1 | 30.017 [30.017, 30.017] | 30.017 | 30.017 | 30.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30-inv | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-fc | ttl30-shared-inv | 1 | 1 | 1.018 [1.018, 1.018] | 1.018 | 1.018 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | nocache | 1 | 1 | 4.604 [4.604, 4.604] | 4.604 | 4.604 | 5.500 | 0 | 0 | 1 | 0 | 0.006 |
| spicedb-ml | ttl5 | 1 | 1 | 5.017 [5.017, 5.017] | 5.017 | 5.017 | 10.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30 | 1 | 1 | 30.011 [30.011, 30.011] | 30.011 | 30.011 | 35.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-inv | 1 | 1 | 30.036 [30.036, 30.036] | 30.036 | 30.036 | 5.500 | 1 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-shared-inv | 1 | 1 | 1.017 [1.017, 1.017] | 1.017 | 1.017 | 6.500 | 0 | 0 | 0 | 0 | 0.004 |

## X7b: faults

109 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos | allow-all | plain | 1 | 233 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 831 | 0 | 0 | 0.023 [0.023, 0.023] | n/a | {'ok': 78, 'leak': 237} |  |
| cerbos | blackhole | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.030, 0.030] | 2.003 | {'ok': 95, 'authz': 3} | wardowl.authz.AuthorizationError: Cerbos CheckResources timed out after 2.0 s; wardowl.authz.AuthorizationError: Cerbos PlanResources failed: RemoteDisconnected; wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | blackhole | cache30 | 1 | 275 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.025 [0.025, 0.025] | n/a | {'ok': 398} |  |
| cerbos | blackhole | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.030, 0.030] | 2.003 | {'ok': 97, 'authz': 3} | wardowl.authz.AuthorizationError: Cerbos CheckResources timed out after 2.0 s; wardowl.authz.AuthorizationError: Cerbos PlanResources failed: RemoteDisconnected; wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | down | breaker | 1 | 275 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.492 [4.492, 4.492] | 1.0e-04 | {'ok': 98, 'authz': 497} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | down | cache30 | 1 | 270 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.017 [0.017, 0.017] | n/a | {'ok': 398} |  |
| cerbos | down | plain | 1 | 81 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.275 [0.275, 0.275] | 0.051 | {'ok': 97, 'authz': 87} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionResetError |
| cerbos | drop-last | plain | 1 | 223 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.012 [0.012, 0.012] | 0.006 | {'ok': 96, 'authz': 227} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned an unexpected response |
| cerbos | empty | plain | 1 | 265 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.021 [0.021, 0.021] | 0.002 | {'ok': 98, 'authz': 270} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned invalid JSON |
| cerbos | garbage-json | plain | 1 | 261 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.018 [0.018, 0.018] | 0.002 | {'ok': 96, 'authz': 265} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned an unexpected response |
| cerbos | http500 | breaker | 1 | 291 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.144 [4.144, 4.144] | 1.0e-04 | {'ok': 96, 'authz': 498} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | http500 | cache30 | 1 | 274 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.004 [0.004, 0.004] | n/a | {'ok': 394} |  |
| cerbos | http500 | plain | 1 | 286 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.016 [0.016, 0.016] | 4.0e-04 | {'ok': 93, 'authz': 291} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned HTTP 500 |
| cerbos | http503 | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.079 [0.079, 0.079] | 0.051 | {'ok': 96, 'authz': 84} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: HTTP 503 |
| cerbos | refuse | breaker | 1 | 278 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.438 [4.438, 4.438] | 1.0e-04 | {'ok': 98, 'authz': 497} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | refuse | cache30 | 1 | 277 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.009 [0.009, 0.009] | n/a | {'ok': 399} |  |
| cerbos | refuse | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.052 [0.052, 0.052] | 0.051 | {'ok': 98, 'authz': 84} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError |
| cerbos | slow-1000 | plain | 1 | 1 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.105 [0.105, 0.105] | n/a | {'ok': 102} |  |
| cerbos | slow-200 | plain | 1 | 13 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.222 [0.222, 0.222] | n/a | {'ok': 112} |  |
| cerbos | slow-3000 | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.086 [0.086, 0.086] | 2.003 | {'ok': 96, 'authz': 3} | wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | slow-3000 | cache30 | 1 | 275 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.021 [0.021, 0.021] | n/a | {'ok': 394} |  |
| cerbos | slow-3000 | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.088 [0.088, 0.088] | 2.003 | {'ok': 96, 'authz': 3} | wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | truncate | plain | 1 | 262 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.012 [0.012, 0.012] | 0.002 | {'ok': 97, 'authz': 267} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned invalid JSON; wardowl.authz.AuthorizationError: Cerbos PlanResources returned invalid JSON |
| cerbos | type-flip | plain | 1 | 262 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.023 [0.023, 0.023] | 0.002 | {'ok': 96, 'authz': 266} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned an unexpected response |
| opa | allow-all | plain | 1 | 246 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 691 | 0 | 0 | 0.024 [0.024, 0.024] | n/a | {'ok': 105, 'leak': 251} |  |
| opa | blackhole | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.030, 0.030] | 2.003 | {'ok': 99, 'authz': 3} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: RemoteDisconnected; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | blackhole | cache30 | 1 | 279 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.013 [0.013, 0.013] | n/a | {'ok': 402} |  |
| opa | blackhole | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.029 [0.029, 0.029] | 2.002 | {'ok': 97, 'authz': 3} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: RemoteDisconnected; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | down | breaker | 1 | 278 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.430 [4.430, 4.430] | 1.0e-04 | {'ok': 101, 'authz': 497} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | down | cache30 | 1 | 278 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.022 [0.022, 0.022] | n/a | {'ok': 402} |  |
| opa | down | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.044 [0.044, 0.044] | 0.051 | {'ok': 102, 'authz': 85} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError |
| opa | drop-last | plain | 1 | 233 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.023 [0.023, 0.023] | 0.004 | {'ok': 100, 'authz': 237} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |
| opa | empty | plain | 1 | 267 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.018 [0.018, 0.018] | 0.002 | {'ok': 100, 'authz': 271} | wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | garbage-json | plain | 1 | 265 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.017 [0.017, 0.017] | 0.002 | {'ok': 98, 'authz': 270} | wardowl.authz.AuthorizationError: OPA decision x4rel/filter is undefined |
| opa | http500 | breaker | 1 | 291 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.117 [4.117, 4.117] | 1.0e-04 | {'ok': 99, 'authz': 498} | wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | http500 | cache30 | 1 | 279 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | n/a | {'ok': 403} |  |
| opa | http500 | plain | 1 | 287 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.017 [0.017, 0.017] | 4.0e-04 | {'ok': 98, 'authz': 292} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned HTTP 500; wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500 |
| opa | http503 | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.009 [0.009, 0.009] | 0.051 | {'ok': 97, 'authz': 84} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: HTTP 503 |
| opa | refuse | breaker | 1 | 279 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.420 [4.420, 4.420] | 1.0e-04 | {'ok': 98, 'authz': 497} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | refuse | cache30 | 1 | 279 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.011 [0.011, 0.011] | n/a | {'ok': 403} |  |
| opa | refuse | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.060 [0.060, 0.060] | 0.051 | {'ok': 100, 'authz': 84} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError |
| opa | slow-1000 | plain | 1 | 1 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.105 [0.105, 0.105] | n/a | {'ok': 103} |  |
| opa | slow-200 | plain | 1 | 13 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.191 [0.191, 0.191] | n/a | {'ok': 113} |  |
| opa | slow-3000 | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.093 [0.093, 0.093] | 2.003 | {'ok': 100, 'authz': 3} | wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | slow-3000 | cache30 | 1 | 279 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.002 [0.002, 0.002] | n/a | {'ok': 403} |  |
| opa | slow-3000 | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.094 [0.094, 0.094] | 2.003 | {'ok': 99, 'authz': 3} | wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | truncate | plain | 1 | 266 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.019, 0.019] | 0.002 | {'ok': 99, 'authz': 270} | wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | type-flip | plain | 1 | 230 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.017 [0.017, 0.017] | 0.005 | {'ok': 98, 'authz': 234} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |
| openfga | allow-all | plain | 1 | 132 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 500 | 0 | 0 | 0.023 [0.023, 0.023] | n/a | {'ok': 33, 'leak': 134} |  |
| openfga | blackhole | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.105 [0.105, 0.105] | 2.003 | {'ok': 74, 'authz': 2} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | blackhole | cache30 | 1 | 280 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.017 [0.017, 0.017] | n/a | {'ok': 403} |  |
| openfga | blackhole | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.089 [0.089, 0.089] | 2.003 | {'ok': 74, 'authz': 3} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | down | breaker | 1 | 277 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.531 [4.531, 4.531] | 0.000 | {'ok': 72, 'authz': 498} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | down | cache30 | 1 | 273 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.026 [0.026, 0.026] | n/a | {'ok': 401} |  |
| openfga | down | plain | 1 | 80 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.261 [0.261, 0.261] | 0.050 | {'ok': 72, 'authz': 87} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionResetError |
| openfga | drop-last | plain | 1 | 174 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.050 [0.050, 0.050] | 0.013 | {'ok': 76, 'authz': 177} | wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d53': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d67': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d88': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d9': None; wardowl.authz.AuthorizationError: OpenFGA could not decid |
| openfga | empty | plain | 1 | 249 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.035 [0.035, 0.035] | 0.004 | {'ok': 70, 'authz': 255} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned invalid JSON |
| openfga | garbage-json | plain | 1 | 249 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.024 [0.024, 0.024] | 0.004 | {'ok': 74, 'authz': 253} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned an unexpected response |
| openfga | http500 | breaker | 1 | 290 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.144 [4.144, 4.144] | 0.000 | {'ok': 74, 'authz': 498} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | http500 | cache30 | 1 | 278 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 8.7e-04 [8.7e-04, 8.7e-04] | n/a | {'ok': 400} |  |
| openfga | http500 | plain | 1 | 286 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.031 [0.031, 0.031] | 4.0e-04 | {'ok': 73, 'authz': 291} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned HTTP 500 |
| openfga | http503 | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.083 [0.083, 0.083] | 0.051 | {'ok': 75, 'authz': 84} | wardowl.authz.AuthorizationError: OpenFGA list-objects failed: HTTP 503 |
| openfga | refuse | breaker | 1 | 279 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.433 [4.433, 4.433] | 0.000 | {'ok': 74, 'authz': 498} | wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | refuse | cache30 | 1 | 280 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.003 [0.003, 0.003] | n/a | {'ok': 403} |  |
| openfga | refuse | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.052 [0.052, 0.052] | 0.050 | {'ok': 76, 'authz': 84} | wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError |
| openfga | slow-1000 | plain | 1 | 1 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.130 [0.130, 0.130] | n/a | {'ok': 77} |  |
| openfga | slow-200 | plain | 1 | 12 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.078 [0.078, 0.078] | n/a | {'ok': 88} |  |
| openfga | slow-3000 | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.099 [0.099, 0.099] | 2.003 | {'ok': 70, 'authz': 3} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | slow-3000 | cache30 | 1 | 279 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.018 [0.018, 0.018] | n/a | {'ok': 402} |  |
| openfga | slow-3000 | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.088 [0.088, 0.088] | 2.003 | {'ok': 74, 'authz': 3} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | truncate | plain | 1 | 250 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.035 [0.035, 0.035] | 0.004 | {'ok': 74, 'authz': 254} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned invalid JSON |
| openfga | type-flip | plain | 1 | 175 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.018 [0.018, 0.018] | 0.013 | {'ok': 74, 'authz': 178} | wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d100': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d103': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d105': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d17': {'allowed': 't |
| pgvector | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.028 [0.028, 0.028] | n/a | {'ok': 115, 'error': 1} | psycopg.OperationalError: consuming input failed: server closed the connection unexpectedly 	This probably means the ser |
| pgvector | down | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.574 [0.574, 0.574] | n/a | {'ok': 119, 'error': 1} | psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | refuse | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.845 [0.845, 0.845] | n/a | {'ok': 117, 'error': 1} | psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | slow-1000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.058 [0.058, 0.058] | n/a | {'ok': 73} |  |
| pgvector | slow-200 | plain | 1 | 6 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.197 [0.197, 0.197] | n/a | {'ok': 124} |  |
| qdrant | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 2 | 0 | 0.025 [0.025, 0.025] | n/a | {'ok': 109, 'error': 2} | qdrant_client.http.exceptions.ResponseHandlingException: Server disconnected without sending a response.; qdrant_client.http.exceptions.ResponseHandlingException: timed out |
| qdrant | down | plain | 1 | 276 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 294 | 0 | 0.209 [0.209, 0.209] | 7.0e-04 | {'ok': 115, 'error': 294} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 104] Connection reset by peer; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | http500 | plain | 1 | 276 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 281 | 0 | 0.015 [0.015, 0.015] | 0.001 | {'ok': 112, 'error': 281} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 500 (Injected) Raw response content: b'{"error":" |
| qdrant | http503 | plain | 1 | 277 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 281 | 0 | 0.013 [0.013, 0.013] | 0.001 | {'ok': 112, 'error': 281} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 503 (Injected) Raw response content: b'{"error":" |
| qdrant | refuse | plain | 1 | 283 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 287 | 0 | 0.016 [0.016, 0.016] | 7.0e-04 | {'ok': 113, 'error': 287} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | slow-1000 | plain | 1 | 4 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.162 [0.162, 0.162] | n/a | {'ok': 119} |  |
| qdrant | slow-200 | plain | 1 | 25 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.054 [0.054, 0.054] | n/a | {'ok': 139} |  |
| qdrant | truncate | plain | 1 | 262 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 266 | 0 | 0.010 [0.010, 0.010] | 0.002 | {'ok': 113, 'error': 266} | json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 322 (char 321); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 269 (char 268); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 280 (char 279); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 282 (char 281); json.decoder.JSONDecodeError: Unterm |
| spicedb | allow-all | plain | 1 | 222 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 619 | 0 | 0 | 0.024 [0.024, 0.024] | n/a | {'ok': 95, 'leak': 225} |  |
| spicedb | blackhole | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.123 [0.123, 0.123] | 2.003 | {'ok': 85, 'authz': 3} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | blackhole | cache30 | 1 | 277 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | n/a | {'ok': 394} |  |
| spicedb | blackhole | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.096 [0.096, 0.096] | 2.003 | {'ok': 85, 'authz': 3} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | down | breaker | 1 | 275 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.518 [4.518, 4.518] | 1.0e-04 | {'ok': 83, 'authz': 495} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | down | cache30 | 1 | 267 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.019 [0.019, 0.019] | n/a | {'ok': 392} |  |
| spicedb | down | plain | 1 | 81 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.326 [0.326, 0.326] | 0.051 | {'ok': 86, 'authz': 88} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionResetError |
| spicedb | drop-last | plain | 1 | 188 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.034 [0.034, 0.034] | 0.010 | {'ok': 81, 'authz': 191} | wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d22': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d59': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d67': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None fo |
| spicedb | empty | plain | 1 | 231 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.016, 0.016] | n/a | {'ok': 79, 'deviate': 235} |  |
| spicedb | garbage-json | plain | 1 | 231 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.036 [0.036, 0.036] | 0.005 | {'ok': 81, 'authz': 235} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: {'unexpected': True} |
| spicedb | http500 | breaker | 1 | 289 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.160 [4.160, 4.160] | 1.0e-04 | {'ok': 84, 'authz': 497} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | http500 | cache30 | 1 | 276 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.005 [0.005, 0.005] | n/a | {'ok': 398} |  |
| spicedb | http500 | plain | 1 | 286 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.030, 0.030] | 3.0e-04 | {'ok': 84, 'authz': 291} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500 |
| spicedb | http503 | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.139 [0.139, 0.139] | 0.051 | {'ok': 86, 'authz': 84} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: HTTP 503 |
| spicedb | refuse | breaker | 1 | 279 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 4.444 [4.444, 4.444] | 1.0e-04 | {'ok': 80, 'authz': 497} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | refuse | cache30 | 1 | 277 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.014 [0.014, 0.014] | n/a | {'ok': 398} |  |
| spicedb | refuse | plain | 1 | 82 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.085 [0.085, 0.085] | 0.051 | {'ok': 86, 'authz': 84} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError |
| spicedb | slow-1000 | plain | 1 | 1 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.155 [0.155, 0.155] | n/a | {'ok': 85} |  |
| spicedb | slow-200 | plain | 1 | 12 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.137 [0.137, 0.137] | n/a | {'ok': 100} |  |
| spicedb | slow-3000 | breaker | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.108 [0.108, 0.108] | 2.003 | {'ok': 87, 'authz': 3} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | slow-3000 | cache30 | 1 | 278 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.019 [0.019, 0.019] | n/a | {'ok': 396} |  |
| spicedb | slow-3000 | plain | 1 | 1 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.093 [0.093, 0.093] | 2.002 | {'ok': 82, 'authz': 3} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | truncate | plain | 1 | 229 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.032 [0.032, 0.032] | 0.005 | {'ok': 81, 'authz': 233} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned invalid JSON |
| spicedb | type-flip | plain | 1 | 224 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.023 [0.023, 0.023] | 0.005 | {'ok': 82, 'authz': 228} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned 'X_UNKNOWN_VALUE' |

## Harness

Runs: 9 job records; profile ['smoke']; commit ['3f2cff0'].
