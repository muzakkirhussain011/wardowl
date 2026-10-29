# X7: revocation and faults

Profile: ['full']. Files: 1; records: 244.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'openfga': 7427} |
| X7-H6 fail closed | CONFIRMED | 137696 requests: 0 leaks (one-sided bound 0.000022), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
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
| X7 exploratory openfga drop-last | EXPLORATORY | {'ok': 1854, 'authz': 3694} |
| X7 exploratory openfga empty | EXPLORATORY | {'ok': 1851, 'authz': 5272} |
| X7 exploratory openfga garbage-json | EXPLORATORY | {'ok': 1827, 'authz': 5261} |
| X7 exploratory openfga truncate | EXPLORATORY | {'ok': 1840, 'authz': 5267} |
| X7 exploratory openfga type-flip | EXPLORATORY | {'ok': 1859, 'authz': 3683} |
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
| X7-H8b openfga blackhole fail-fast | CONFIRMED | failed latency 0.000 s with breaker, 2.003 s without |
| X7-H9 openfga blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 openfga slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

240 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
