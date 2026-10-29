# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'cerbos': 831} |
| X7-H6 fail closed | INCONCLUSIVE | 7085 requests: 0 leaks (one-sided bound 0.000423), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
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
| X7 exploratory cerbos drop-last | EXPLORATORY | {'ok': 96, 'authz': 227} |
| X7 exploratory cerbos empty | EXPLORATORY | {'ok': 98, 'authz': 270} |
| X7 exploratory cerbos garbage-json | EXPLORATORY | {'ok': 96, 'authz': 265} |
| X7 exploratory cerbos truncate | EXPLORATORY | {'ok': 97, 'authz': 267} |
| X7 exploratory cerbos type-flip | EXPLORATORY | {'ok': 96, 'authz': 266} |
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
| X7-H8b cerbos blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.003 s without |
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

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
