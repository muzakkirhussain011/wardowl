# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'cerbos': 435} |
| X7-H6 fail closed | INCONCLUSIVE | 4808 requests: 0 leaks (one-sided bound 0.000623), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
| X7-H7a cerbos blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7a cerbos down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 41 requests |
| X7-H7a cerbos http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 141 requests |
| X7-H7a cerbos http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a cerbos refuse | INCONCLUSIVE | 0.000 [0.000, 0.000] over 117 requests |
| X7-H7b cerbos slow-1000 failing | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b cerbos slow-1000 latency rise | INCONCLUSIVE | median rise n/a [n/a, n/a] s against 1.0 s |
| X7-H7b cerbos slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 6 requests |
| X7-H7b cerbos slow-200 latency rise | INCONCLUSIVE | median rise 0.402 [0.402, 0.402] s against 0.2 s |
| X7-H7a cerbos slow-3000 | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7 exploratory cerbos drop-last | EXPLORATORY | {'ok': 101, 'authz': 122} |
| X7 exploratory cerbos empty | EXPLORATORY | {'ok': 102, 'authz': 137} |
| X7 exploratory cerbos garbage-json | EXPLORATORY | {'ok': 102, 'authz': 138} |
| X7 exploratory cerbos truncate | EXPLORATORY | {'ok': 102, 'authz': 137} |
| X7 exploratory cerbos type-flip | EXPLORATORY | {'ok': 103, 'authz': 137} |
| X7-H8b cerbos blackhole recovery | INCONCLUSIVE | median recovery 0.123 [0.123, 0.123] |
| X7-H8a cerbos blackhole | INCONCLUSIVE | median recovery 0.112 [0.112, 0.112] |
| X7-H8b cerbos down recovery | INCONCLUSIVE | median recovery 2.396 [2.396, 2.396] |
| X7 exploratory recovery cerbos down | EXPLORATORY | median recovery 0.216 [0.216, 0.216] |
| X7-H8b cerbos http500 recovery | INCONCLUSIVE | median recovery 2.091 [2.091, 2.091] |
| X7-H8a cerbos http500 | INCONCLUSIVE | median recovery 0.008 [0.008, 0.008] |
| X7-H8a cerbos http503 | INCONCLUSIVE | median recovery 0.067 [0.067, 0.067] |
| X7-H8b cerbos refuse recovery | INCONCLUSIVE | median recovery 0.020 [0.020, 0.020] |
| X7-H8a cerbos refuse | INCONCLUSIVE | median recovery 0.030 [0.030, 0.030] |
| X7-H8b cerbos slow-3000 recovery | INCONCLUSIVE | median recovery 1.069 [1.069, 1.069] |
| X7-H8a cerbos slow-3000 | INCONCLUSIVE | median recovery 1.069 [1.069, 1.069] |
| X7-H9 cerbos blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 cerbos slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

24 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos | allow-all | plain | 1 | 121 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 435 | 0 | 0 | 0.021 [0.021, 0.021] | n/a | {'ok': 86, 'leak': 125} |  |
| cerbos | blackhole | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.123 [0.123, 0.123] | n/a | {'ok': 104, 'authz': 1} | wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | blackhole | cache30 | 1 | 138 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | n/a | {'ok': 260} |  |
| cerbos | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.112 [0.112, 0.112] | n/a | {'ok': 103, 'authz': 1} | wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | down | breaker | 1 | 133 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.396 [2.396, 2.396] | 1.0e-04 | {'ok': 104, 'authz': 251} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | down | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.017 [0.017, 0.017] | n/a | {'ok': 261} |  |
| cerbos | down | plain | 1 | 41 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.216 [0.216, 0.216] | 0.051 | {'ok': 103, 'authz': 44} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: Cerbos PlanResources failed: ConnectionResetError |
| cerbos | drop-last | plain | 1 | 118 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.011 [0.011, 0.011] | 0.004 | {'ok': 101, 'authz': 122} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned an unexpected response |
| cerbos | empty | plain | 1 | 133 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.019 [0.019, 0.019] | 0.002 | {'ok': 102, 'authz': 137} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned invalid JSON |
| cerbos | garbage-json | plain | 1 | 132 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.024 [0.024, 0.024] | 0.002 | {'ok': 102, 'authz': 138} | wardowl.authz.AuthorizationError: Cerbos CheckResources returned an unexpected response; wardowl.authz.AuthorizationError: Cerbos PlanResources returned an unexpected response |
| cerbos | http500 | breaker | 1 | 144 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.091 [2.091, 2.091] | 1.0e-04 | {'ok': 102, 'authz': 251} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| cerbos | http500 | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.008 [0.008, 0.008] | n/a | {'ok': 259} |  |
| cerbos | http500 | plain | 1 | 141 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.008 [0.008, 0.008] | 3.0e-04 | {'ok': 101, 'authz': 146} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned HTTP 500 |
| cerbos | http503 | plain | 1 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.067 [0.067, 0.067] | 0.051 | {'ok': 103, 'authz': 42} | wardowl.authz.AuthorizationError: Cerbos PlanResources failed: HTTP 503 |
| cerbos | refuse | breaker | 1 | 118 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | n/a | {'ok': 225} |  |
| cerbos | refuse | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.007 [0.007, 0.007] | n/a | {'ok': 260} |  |
| cerbos | refuse | plain | 1 | 117 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.030 [0.030, 0.030] | n/a | {'ok': 225} |  |
| cerbos | slow-1000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.054 [0.054, 0.054] | n/a | {'ok': 103} |  |
| cerbos | slow-200 | plain | 1 | 6 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.209 [0.209, 0.209] | n/a | {'ok': 110} |  |
| cerbos | slow-3000 | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.069 [1.069, 1.069] | n/a | {'ok': 103, 'authz': 2} | wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | slow-3000 | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.016, 0.016] | n/a | {'ok': 259} |  |
| cerbos | slow-3000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.069 [1.069, 1.069] | n/a | {'ok': 102, 'authz': 2} | wardowl.authz.AuthorizationError: Cerbos PlanResources timed out after 2.0 s |
| cerbos | truncate | plain | 1 | 133 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | 0.002 | {'ok': 102, 'authz': 137} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned invalid JSON |
| cerbos | type-flip | plain | 1 | 133 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | 0.002 | {'ok': 103, 'authz': 137} | wardowl.authz.AuthorizationError: Cerbos PlanResources returned an unexpected response |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
