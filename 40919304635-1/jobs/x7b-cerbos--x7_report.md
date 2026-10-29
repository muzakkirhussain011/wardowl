# X7: revocation and faults

Profile: ['full']. Files: 1; records: 244.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'cerbos': 22790} |
| X7-H6 fail closed | CONFIRMED | 151189 requests: 0 leaks (one-sided bound 0.000020), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
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
| X7 exploratory cerbos drop-last | EXPLORATORY | {'ok': 2423, 'authz': 4845} |
| X7 exploratory cerbos empty | EXPLORATORY | {'ok': 2371, 'authz': 5429} |
| X7 exploratory cerbos garbage-json | EXPLORATORY | {'ok': 2395, 'authz': 5491} |
| X7 exploratory cerbos truncate | EXPLORATORY | {'ok': 2412, 'authz': 5508} |
| X7 exploratory cerbos type-flip | EXPLORATORY | {'ok': 2420, 'authz': 5477} |
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
| X7-H8b cerbos blackhole fail-fast | CONFIRMED | failed latency 5.0e-05 s with breaker, 2.003 s without |
| X7-H9 cerbos blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

240 episodes; 0 excluded by G4 (baseline below 99% exact).

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

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
