# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'spicedb': 619} |
| X7-H6 fail closed | INCONCLUSIVE | 6665 requests: 0 leaks (one-sided bound 0.000449), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
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
| X7 exploratory spicedb drop-last | EXPLORATORY | {'ok': 81, 'authz': 191} |
| X7 exploratory spicedb empty | EXPLORATORY | {'ok': 79, 'deviate': 235} |
| X7 exploratory spicedb garbage-json | EXPLORATORY | {'ok': 81, 'authz': 235} |
| X7 exploratory spicedb truncate | EXPLORATORY | {'ok': 81, 'authz': 233} |
| X7 exploratory spicedb type-flip | EXPLORATORY | {'ok': 82, 'authz': 228} |
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
| X7-H8b spicedb blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.003 s without |
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

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
