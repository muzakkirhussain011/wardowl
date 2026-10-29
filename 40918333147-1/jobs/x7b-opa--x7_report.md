# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'opa': 691} |
| X7-H6 fail closed | INCONCLUSIVE | 7145 requests: 0 leaks (one-sided bound 0.000419), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
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
| X7 exploratory opa drop-last | EXPLORATORY | {'ok': 100, 'authz': 237} |
| X7 exploratory opa empty | EXPLORATORY | {'ok': 100, 'authz': 271} |
| X7 exploratory opa garbage-json | EXPLORATORY | {'ok': 98, 'authz': 270} |
| X7 exploratory opa truncate | EXPLORATORY | {'ok': 99, 'authz': 270} |
| X7 exploratory opa type-flip | EXPLORATORY | {'ok': 98, 'authz': 234} |
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
| X7-H8b opa blackhole fail-fast | FALSIFIED | failed latency 2.003 s with breaker, 2.002 s without |
| X7-H9 opa blackhole | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa down | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa http500 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa refuse | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa slow-3000 | INCONCLUSIVE | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

24 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
