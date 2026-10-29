# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'spicedb': 328} |
| X7-H6 fail closed | INCONCLUSIVE | 4478 requests: 0 leaks (one-sided bound 0.000669), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
| X7-H7a spicedb blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7a spicedb down | INCONCLUSIVE | 0.952 [0.952, 0.952] over 42 requests |
| X7-H7a spicedb http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 141 requests |
| X7-H7a spicedb http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a spicedb refuse | INCONCLUSIVE | 0.000 [0.000, 0.000] over 103 requests |
| X7-H7b spicedb slow-1000 failing | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b spicedb slow-1000 latency rise | INCONCLUSIVE | median rise n/a [n/a, n/a] s against 1.0 s |
| X7-H7b spicedb slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 5 requests |
| X7-H7b spicedb slow-200 latency rise | INCONCLUSIVE | median rise 0.407 [0.407, 0.407] s against 0.2 s |
| X7-H7a spicedb slow-3000 | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7 exploratory spicedb drop-last | EXPLORATORY | {'ok': 88, 'authz': 107} |
| X7 exploratory spicedb empty | EXPLORATORY | {'ok': 89, 'deviate': 126} |
| X7 exploratory spicedb garbage-json | EXPLORATORY | {'ok': 89, 'authz': 126} |
| X7 exploratory spicedb truncate | EXPLORATORY | {'ok': 88, 'authz': 126} |
| X7 exploratory spicedb type-flip | EXPLORATORY | {'ok': 89, 'authz': 121} |
| X7-H8b spicedb blackhole recovery | INCONCLUSIVE | median recovery 0.143 [0.143, 0.143] |
| X7-H8a spicedb blackhole | INCONCLUSIVE | median recovery 0.152 [0.152, 0.152] |
| X7-H8b spicedb down recovery | INCONCLUSIVE | median recovery 2.416 [2.416, 2.416] |
| X7 exploratory recovery spicedb down | EXPLORATORY | median recovery 0.819 [0.819, 0.819] |
| X7-H8b spicedb http500 recovery | INCONCLUSIVE | median recovery 2.136 [2.136, 2.136] |
| X7-H8a spicedb http500 | INCONCLUSIVE | median recovery 0.022 [0.022, 0.022] |
| X7-H8a spicedb http503 | INCONCLUSIVE | median recovery 0.109 [0.109, 0.109] |
| X7-H8b spicedb refuse recovery | INCONCLUSIVE | median recovery 0.036 [0.036, 0.036] |
| X7-H8a spicedb refuse | INCONCLUSIVE | median recovery 0.032 [0.032, 0.032] |
| X7-H8b spicedb slow-3000 recovery | INCONCLUSIVE | median recovery 1.074 [1.074, 1.074] |
| X7-H8a spicedb slow-3000 | INCONCLUSIVE | median recovery 1.076 [1.076, 1.076] |
| X7-H9 spicedb blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

24 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb | allow-all | plain | 1 | 115 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 328 | 0 | 0 | 0.024 [0.024, 0.024] | n/a | {'ok': 100, 'leak': 119} |  |
| spicedb | blackhole | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.143 [0.143, 0.143] | n/a | {'ok': 90, 'authz': 1} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | blackhole | cache30 | 1 | 135 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.009 [0.009, 0.009] | n/a | {'ok': 255} |  |
| spicedb | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.152 [0.152, 0.152] | n/a | {'ok': 90, 'authz': 1} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | down | breaker | 1 | 132 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.416 [2.416, 2.416] | 1.0e-04 | {'ok': 90, 'authz': 250} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | down | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.016, 0.016] | n/a | {'ok': 255} |  |
| spicedb | down | plain | 1 | 42 | 0.952 [0.952, 0.952] | 0.048 [0.048, 0.048] | 0 | 0 | 0 | 0.819 [0.819, 0.819] | 0.051 | {'ok': 97, 'authz': 51} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionResetError |
| spicedb | drop-last | plain | 1 | 103 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.014 [0.014, 0.014] | 0.007 | {'ok': 88, 'authz': 107} | wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d22': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d59': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d67': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None fo |
| spicedb | empty | plain | 1 | 122 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.025 [0.025, 0.025] | n/a | {'ok': 89, 'deviate': 126} |  |
| spicedb | garbage-json | plain | 1 | 122 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.019, 0.019] | 0.003 | {'ok': 89, 'authz': 126} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: {'unexpected': True} |
| spicedb | http500 | breaker | 1 | 143 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.136 [2.136, 2.136] | 1.0e-04 | {'ok': 87, 'authz': 251} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | http500 | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.003 [0.003, 0.003] | n/a | {'ok': 257} |  |
| spicedb | http500 | plain | 1 | 141 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.022 [0.022, 0.022] | 4.0e-04 | {'ok': 90, 'authz': 145} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500 |
| spicedb | http503 | plain | 1 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.109 [0.109, 0.109] | 0.051 | {'ok': 91, 'authz': 42} | wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: HTTP 503 |
| spicedb | refuse | breaker | 1 | 105 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.036 [0.036, 0.036] | n/a | {'ok': 199} |  |
| spicedb | refuse | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.011 [0.011, 0.011] | n/a | {'ok': 260} |  |
| spicedb | refuse | plain | 1 | 103 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.032 [0.032, 0.032] | n/a | {'ok': 195} |  |
| spicedb | slow-1000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.098 [0.098, 0.098] | n/a | {'ok': 92} |  |
| spicedb | slow-200 | plain | 1 | 5 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.064 [0.064, 0.064] | n/a | {'ok': 98} |  |
| spicedb | slow-3000 | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.074 [1.074, 1.074] | n/a | {'ok': 90, 'authz': 2} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | slow-3000 | cache30 | 1 | 138 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.010 [0.010, 0.010] | n/a | {'ok': 258} |  |
| spicedb | slow-3000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.076 [1.076, 1.076] | n/a | {'ok': 90, 'authz': 2} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | truncate | plain | 1 | 122 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.015 [0.015, 0.015] | 0.003 | {'ok': 88, 'authz': 126} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned invalid JSON |
| spicedb | type-flip | plain | 1 | 117 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.019, 0.019] | 0.004 | {'ok': 89, 'authz': 121} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned 'X_UNKNOWN_VALUE' |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
