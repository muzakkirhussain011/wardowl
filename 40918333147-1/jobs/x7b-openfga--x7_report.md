# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'openfga': 500} |
| X7-H6 fail closed | INCONCLUSIVE | 6518 requests: 0 leaks (one-sided bound 0.000460), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
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
| X7 exploratory openfga drop-last | EXPLORATORY | {'ok': 76, 'authz': 177} |
| X7 exploratory openfga empty | EXPLORATORY | {'ok': 70, 'authz': 255} |
| X7 exploratory openfga garbage-json | EXPLORATORY | {'ok': 74, 'authz': 253} |
| X7 exploratory openfga truncate | EXPLORATORY | {'ok': 74, 'authz': 254} |
| X7 exploratory openfga type-flip | EXPLORATORY | {'ok': 74, 'authz': 178} |
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
| X7-H8b openfga blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.003 s without |
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

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
