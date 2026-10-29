# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'openfga': 277} |
| X7-H6 fail closed | INCONCLUSIVE | 4098 requests: 0 leaks (one-sided bound 0.000731), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
| X7-H7a openfga blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7a openfga down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a openfga http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 141 requests |
| X7-H7a openfga http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a openfga refuse | INCONCLUSIVE | 0.000 [0.000, 0.000] over 86 requests |
| X7-H7b openfga slow-1000 failing | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b openfga slow-1000 latency rise | INCONCLUSIVE | median rise n/a [n/a, n/a] s against 1.0 s |
| X7-H7b openfga slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 5 requests |
| X7-H7b openfga slow-200 latency rise | INCONCLUSIVE | median rise 0.398 [0.398, 0.398] s against 0.2 s |
| X7-H7a openfga slow-3000 | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7 exploratory openfga drop-last | EXPLORATORY | {'ok': 75, 'authz': 89} |
| X7 exploratory openfga empty | EXPLORATORY | {'ok': 71, 'authz': 122} |
| X7 exploratory openfga garbage-json | EXPLORATORY | {'ok': 74, 'authz': 122} |
| X7 exploratory openfga truncate | EXPLORATORY | {'ok': 74, 'authz': 123} |
| X7 exploratory openfga type-flip | EXPLORATORY | {'ok': 76, 'authz': 89} |
| X7-H8b openfga blackhole recovery | INCONCLUSIVE | median recovery 0.137 [0.137, 0.137] |
| X7-H8a openfga blackhole | INCONCLUSIVE | median recovery 0.140 [0.140, 0.140] |
| X7-H8b openfga down recovery | INCONCLUSIVE | median recovery 2.455 [2.455, 2.455] |
| X7 exploratory recovery openfga down | EXPLORATORY | median recovery 0.240 [0.240, 0.240] |
| X7-H8b openfga http500 recovery | INCONCLUSIVE | median recovery 2.132 [2.132, 2.132] |
| X7-H8a openfga http500 | INCONCLUSIVE | median recovery 0.036 [0.036, 0.036] |
| X7-H8a openfga http503 | INCONCLUSIVE | median recovery 0.025 [0.025, 0.025] |
| X7-H8b openfga refuse recovery | INCONCLUSIVE | median recovery 0.041 [0.041, 0.041] |
| X7-H8a openfga refuse | INCONCLUSIVE | median recovery 0.044 [0.044, 0.044] |
| X7-H8b openfga slow-3000 recovery | INCONCLUSIVE | median recovery 1.064 [1.064, 1.064] |
| X7-H8a openfga slow-3000 | INCONCLUSIVE | median recovery 1.076 [1.076, 1.076] |
| X7-H9 openfga blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

24 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openfga | allow-all | plain | 1 | 70 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 277 | 0 | 0 | 0.052 [0.052, 0.052] | n/a | {'ok': 39, 'leak': 74} |  |
| openfga | blackhole | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.137 [0.137, 0.137] | n/a | {'ok': 76, 'authz': 1} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | blackhole | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.016, 0.016] | n/a | {'ok': 258} |  |
| openfga | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.140 [0.140, 0.140] | n/a | {'ok': 76, 'authz': 1} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | down | breaker | 1 | 133 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.455 [2.455, 2.455] | 1.0e-04 | {'ok': 74, 'authz': 250} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | down | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.018 [0.018, 0.018] | n/a | {'ok': 257} |  |
| openfga | down | plain | 1 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.240 [0.240, 0.240] | 0.051 | {'ok': 73, 'authz': 44} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: ConnectionResetError |
| openfga | drop-last | plain | 1 | 85 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.040 [0.040, 0.040] | 0.014 | {'ok': 75, 'authz': 89} | wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d47': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d53': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d67': None; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d88': None; wardowl.authz.AuthorizationError: OpenFGA could not deci |
| openfga | empty | plain | 1 | 118 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.017 [0.017, 0.017] | 0.004 | {'ok': 71, 'authz': 122} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned invalid JSON |
| openfga | garbage-json | plain | 1 | 118 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.015 [0.015, 0.015] | 0.004 | {'ok': 74, 'authz': 122} | wardowl.authz.AuthorizationError: OpenFGA batch-check returned no result; wardowl.authz.AuthorizationError: OpenFGA list-objects returned an unexpected response |
| openfga | http500 | breaker | 1 | 143 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.132 [2.132, 2.132] | 1.0e-04 | {'ok': 75, 'authz': 250} | wardowl.authz.AuthorizationError: OpenFGA list-objects returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| openfga | http500 | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | n/a | {'ok': 256} |  |
| openfga | http500 | plain | 1 | 141 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.036 [0.036, 0.036] | 4.0e-04 | {'ok': 74, 'authz': 146} | wardowl.authz.AuthorizationError: OpenFGA batch-check returned HTTP 500; wardowl.authz.AuthorizationError: OpenFGA list-objects returned HTTP 500 |
| openfga | http503 | plain | 1 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.025 [0.025, 0.025] | 0.051 | {'ok': 72, 'authz': 42} | wardowl.authz.AuthorizationError: OpenFGA batch-check failed: HTTP 503; wardowl.authz.AuthorizationError: OpenFGA list-objects failed: HTTP 503 |
| openfga | refuse | breaker | 1 | 85 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.041 [0.041, 0.041] | n/a | {'ok': 165} |  |
| openfga | refuse | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.002 [0.002, 0.002] | n/a | {'ok': 258} |  |
| openfga | refuse | plain | 1 | 86 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.044 [0.044, 0.044] | n/a | {'ok': 165} |  |
| openfga | slow-1000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.113 [0.113, 0.113] | n/a | {'ok': 77} |  |
| openfga | slow-200 | plain | 1 | 5 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.063 [0.063, 0.063] | n/a | {'ok': 83} |  |
| openfga | slow-3000 | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.064 [1.064, 1.064] | n/a | {'ok': 71, 'authz': 2} | wardowl.authz.AuthorizationError: OpenFGA batch-check timed out after 2.0 s; wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | slow-3000 | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.025 [0.025, 0.025] | n/a | {'ok': 259} |  |
| openfga | slow-3000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.076 [1.076, 1.076] | n/a | {'ok': 76, 'authz': 2} | wardowl.authz.AuthorizationError: OpenFGA list-objects timed out after 2.0 s |
| openfga | truncate | plain | 1 | 118 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.037 [0.037, 0.037] | 0.004 | {'ok': 74, 'authz': 123} | wardowl.authz.AuthorizationError: OpenFGA batch-check returned invalid JSON; wardowl.authz.AuthorizationError: OpenFGA list-objects returned invalid JSON |
| openfga | type-flip | plain | 1 | 85 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.033 [0.033, 0.033] | 0.013 | {'ok': 76, 'authz': 89} | wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d100': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d103': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d105': {'allowed': 'true'}; wardowl.authz.AuthorizationError: OpenFGA could not decide access to 'fop0d17': {'allowed': 't |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
