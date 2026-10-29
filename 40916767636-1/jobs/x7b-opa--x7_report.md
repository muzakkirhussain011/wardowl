# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 28. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'opa': 335} |
| X7-H6 fail closed | INCONCLUSIVE | 4585 requests: 0 leaks (one-sided bound 0.000653), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
| X7-H7a opa blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7a opa down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a opa http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 141 requests |
| X7-H7a opa http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a opa refuse | INCONCLUSIVE | 0.000 [0.000, 0.000] over 107 requests |
| X7-H7b opa slow-1000 failing | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b opa slow-1000 latency rise | INCONCLUSIVE | median rise n/a [n/a, n/a] s against 1.0 s |
| X7-H7b opa slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 6 requests |
| X7-H7b opa slow-200 latency rise | INCONCLUSIVE | median rise 0.401 [0.401, 0.401] s against 0.2 s |
| X7-H7a opa slow-3000 | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7 exploratory opa drop-last | EXPLORATORY | {'ok': 94, 'authz': 112} |
| X7 exploratory opa empty | EXPLORATORY | {'ok': 94, 'authz': 132} |
| X7 exploratory opa garbage-json | EXPLORATORY | {'ok': 94, 'authz': 133} |
| X7 exploratory opa truncate | EXPLORATORY | {'ok': 94, 'authz': 133} |
| X7 exploratory opa type-flip | EXPLORATORY | {'ok': 95, 'authz': 112} |
| X7-H8b opa blackhole recovery | INCONCLUSIVE | median recovery 0.117 [0.117, 0.117] |
| X7-H8a opa blackhole | INCONCLUSIVE | median recovery 0.117 [0.117, 0.117] |
| X7-H8b opa down recovery | INCONCLUSIVE | median recovery 2.359 [2.359, 2.359] |
| X7 exploratory recovery opa down | EXPLORATORY | median recovery 0.055 [0.055, 0.055] |
| X7-H8b opa http500 recovery | INCONCLUSIVE | median recovery 2.120 [2.120, 2.120] |
| X7-H8a opa http500 | INCONCLUSIVE | median recovery 0.012 [0.012, 0.012] |
| X7-H8a opa http503 | INCONCLUSIVE | median recovery 0.078 [0.078, 0.078] |
| X7-H8b opa refuse recovery | INCONCLUSIVE | median recovery 0.023 [0.023, 0.023] |
| X7-H8a opa refuse | INCONCLUSIVE | median recovery 0.020 [0.020, 0.020] |
| X7-H8b opa slow-3000 recovery | INCONCLUSIVE | median recovery 1.081 [1.081, 1.081] |
| X7-H8a opa slow-3000 | INCONCLUSIVE | median recovery 1.068 [1.068, 1.068] |
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
| opa | allow-all | plain | 1 | 117 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 335 | 0 | 0 | 0.027 [0.027, 0.027] | n/a | {'ok': 103, 'leak': 122} |  |
| opa | blackhole | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.117 [0.117, 0.117] | n/a | {'ok': 94, 'authz': 1} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s |
| opa | blackhole | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.004 [0.004, 0.004] | n/a | {'ok': 260} |  |
| opa | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.117 [0.117, 0.117] | n/a | {'ok': 94, 'authz': 1} | wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | down | breaker | 1 | 134 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.359 [2.359, 2.359] | 0.000 | {'ok': 97, 'authz': 251} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | down | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.012 [0.012, 0.012] | n/a | {'ok': 258} |  |
| opa | down | plain | 1 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.055 [0.055, 0.055] | 0.050 | {'ok': 96, 'authz': 43} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError |
| opa | drop-last | plain | 1 | 108 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.031 [0.031, 0.031] | 0.006 | {'ok': 94, 'authz': 112} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |
| opa | empty | plain | 1 | 128 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.015 [0.015, 0.015] | 0.002 | {'ok': 94, 'authz': 132} | wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | garbage-json | plain | 1 | 128 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.026 [0.026, 0.026] | 0.002 | {'ok': 94, 'authz': 133} | wardowl.authz.AuthorizationError: OPA decision x4rel/filter is undefined |
| opa | http500 | breaker | 1 | 143 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 2.120 [2.120, 2.120] | 0.000 | {'ok': 94, 'authz': 251} | wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | http500 | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.003 [0.003, 0.003] | n/a | {'ok': 258} |  |
| opa | http500 | plain | 1 | 141 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.012 [0.012, 0.012] | 3.0e-04 | {'ok': 94, 'authz': 145} | wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500 |
| opa | http503 | plain | 1 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.078 [0.078, 0.078] | 0.051 | {'ok': 94, 'authz': 42} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: HTTP 503 |
| opa | refuse | breaker | 1 | 108 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.023 [0.023, 0.023] | n/a | {'ok': 206} |  |
| opa | refuse | cache30 | 1 | 136 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.004 [0.004, 0.004] | n/a | {'ok': 257} |  |
| opa | refuse | plain | 1 | 107 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.020 [0.020, 0.020] | n/a | {'ok': 204} |  |
| opa | slow-1000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.066 [0.066, 0.066] | n/a | {'ok': 96} |  |
| opa | slow-200 | plain | 1 | 6 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.015 [0.015, 0.015] | n/a | {'ok': 103} |  |
| opa | slow-3000 | breaker | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.081 [1.081, 1.081] | n/a | {'ok': 95, 'authz': 2} | wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | slow-3000 | cache30 | 1 | 137 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.018 [0.018, 0.018] | n/a | {'ok': 260} |  |
| opa | slow-3000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.068 [1.068, 1.068] | n/a | {'ok': 94, 'authz': 2} | wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | truncate | plain | 1 | 129 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.026 [0.026, 0.026] | 0.002 | {'ok': 94, 'authz': 133} | wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | type-flip | plain | 1 | 108 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.028 [0.028, 0.028] | 0.006 | {'ok': 95, 'authz': 112} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
