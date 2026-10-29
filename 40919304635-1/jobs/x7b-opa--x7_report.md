# X7: revocation and faults

Profile: ['full']. Files: 1; records: 244.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'opa': 17685} |
| X7-H6 fail closed | CONFIRMED | 132766 requests: 0 leaks (one-sided bound 0.000023), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
| X7-H7a opa blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a opa down | CONFIRMED | 1.000 [1.000, 1.000] over 1664 requests |
| X7-H7a opa http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5729 requests |
| X7-H7a opa http503 | CONFIRMED | 1.000 [1.000, 1.000] over 1657 requests |
| X7-H7a opa refuse | CONFIRMED | 1.000 [1.000, 1.000] over 1668 requests |
| X7-H7b opa slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 41 requests |
| X7-H7b opa slow-1000 latency rise | CONFIRMED | median rise 2.000 [1.999, 2.000] s against 1.0 s |
| X7-H7b opa slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 262 requests |
| X7-H7b opa slow-200 latency rise | CONFIRMED | median rise 0.399 [0.399, 0.400] s against 0.2 s |
| X7-H7a opa slow-3000 | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7 exploratory opa drop-last | EXPLORATORY | {'ok': 1805, 'authz': 3579} |
| X7 exploratory opa empty | EXPLORATORY | {'ok': 1794, 'authz': 4756} |
| X7 exploratory opa garbage-json | EXPLORATORY | {'ok': 1798, 'authz': 4747} |
| X7 exploratory opa truncate | EXPLORATORY | {'ok': 1796, 'authz': 4749} |
| X7 exploratory opa type-flip | EXPLORATORY | {'ok': 1804, 'authz': 3571} |
| X7-H8b opa blackhole recovery | CONFIRMED | median recovery 3.133 [3.125, 3.136] |
| X7-H8a opa blackhole | CONFIRMED | median recovery 0.101 [0.099, 0.103] |
| X7-H8b opa down recovery | CONFIRMED | median recovery 3.492 [3.482, 3.501] |
| X7 exploratory recovery opa down | EXPLORATORY | median recovery 0.081 [0.063, 0.090] |
| X7-H8b opa http500 recovery | CONFIRMED | median recovery 3.148 [3.140, 3.157] |
| X7-H8a opa http500 | CONFIRMED | median recovery 0.022 [0.019, 0.030] |
| X7-H8a opa http503 | CONFIRMED | median recovery 0.058 [0.033, 0.078] |
| X7-H8b opa refuse recovery | CONFIRMED | median recovery 3.493 [3.482, 3.499] |
| X7-H8a opa refuse | CONFIRMED | median recovery 0.048 [0.026, 0.076] |
| X7-H8b opa slow-3000 recovery | CONFIRMED | median recovery 3.127 [3.119, 3.146] |
| X7-H8a opa slow-3000 | CONFIRMED | median recovery 0.165 [0.158, 0.169] |
| X7-H8b opa blackhole fail-fast | CONFIRMED | failed latency 1.0e-04 s with breaker, 2.003 s without |
| X7-H9 opa blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 opa slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

240 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| opa | allow-all | plain | 10 | 4134 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 17685 | 0 | 0 | 0.032 [0.023, 0.045] | n/a | {'ok': 1495, 'leak': 4171} |  |
| opa | blackhole | breaker | 10 | 967 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.133 [3.125, 3.136] | 1.0e-04 | {'ok': 1796, 'authz': 2498} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | blackhole | cache30 | 10 | 5376 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.008 [0.006, 0.015] | n/a | {'ok': 8092} |  |
| opa | blackhole | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.101 [0.099, 0.103] | 2.003 | {'ok': 1809, 'authz': 50} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | down | breaker | 10 | 5700 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.492 [3.482, 3.501] | 1.0e-04 | {'ok': 1836, 'authz': 7412} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | down | cache30 | 10 | 5366 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.019 [0.011, 0.025] | n/a | {'ok': 8084} |  |
| opa | down | plain | 10 | 1664 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.081 [0.063, 0.090] | 0.051 | {'ok': 1829, 'authz': 1692} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError |
| opa | drop-last | plain | 10 | 3546 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.028 [0.023, 0.041] | 0.013 | {'ok': 1805, 'authz': 3579} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |
| opa | empty | plain | 10 | 4713 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.027 [0.018, 0.031] | 0.004 | {'ok': 1794, 'authz': 4756} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned invalid JSON; wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | garbage-json | plain | 10 | 4704 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.029 [0.023, 0.034] | 0.005 | {'ok': 1798, 'authz': 4747} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions is undefined; wardowl.authz.AuthorizationError: OPA decision x4rel/filter is undefined |
| opa | http500 | breaker | 10 | 5846 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.148 [3.140, 3.157] | 1.0e-04 | {'ok': 1796, 'authz': 7416} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned HTTP 500; wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | http500 | cache30 | 10 | 5372 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.010, 0.019] | n/a | {'ok': 8081} |  |
| opa | http500 | plain | 10 | 5729 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.022 [0.019, 0.030] | 5.0e-04 | {'ok': 1785, 'authz': 5776} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned HTTP 500; wardowl.authz.AuthorizationError: OPA x4rel/filter returned HTTP 500 |
| opa | http503 | plain | 10 | 1657 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.058 [0.033, 0.078] | 0.051 | {'ok': 1805, 'authz': 1677} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: HTTP 503; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: HTTP 503 |
| opa | refuse | breaker | 10 | 5697 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.493 [3.482, 3.499] | 1.0e-04 | {'ok': 1787, 'authz': 7406} | wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | refuse | cache30 | 10 | 5367 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.014 [0.006, 0.019] | n/a | {'ok': 8075} |  |
| opa | refuse | plain | 10 | 1668 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.048 [0.026, 0.076] | 0.051 | {'ok': 1805, 'authz': 1688} | wardowl.authz.AuthorizationError: OPA x4rel/decisions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: OPA x4rel/filter failed: ConnectionRefusedError |
| opa | slow-1000 | plain | 10 | 41 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.222 [0.215, 0.232] | n/a | {'ok': 1863} |  |
| opa | slow-200 | plain | 10 | 262 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.148 [0.137, 0.152] | n/a | {'ok': 2073} |  |
| opa | slow-3000 | breaker | 10 | 965 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.127 [3.119, 3.146] | 1.0e-04 | {'ok': 1804, 'authz': 2497} | wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| opa | slow-3000 | cache30 | 10 | 5366 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.015 [0.012, 0.017] | n/a | {'ok': 8075} |  |
| opa | slow-3000 | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.165 [0.158, 0.169] | 2.003 | {'ok': 1800, 'authz': 60} | wardowl.authz.AuthorizationError: OPA x4rel/decisions timed out after 2.0 s; wardowl.authz.AuthorizationError: OPA x4rel/filter timed out after 2.0 s |
| opa | truncate | plain | 10 | 4709 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.033 [0.023, 0.034] | 0.005 | {'ok': 1796, 'authz': 4749} | wardowl.authz.AuthorizationError: OPA x4rel/decisions returned invalid JSON; wardowl.authz.AuthorizationError: OPA x4rel/filter returned invalid JSON |
| opa | type-flip | plain | 10 | 3537 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.023 [0.017, 0.033] | 0.013 | {'ok': 1804, 'authz': 3571} | wardowl.authz.AuthorizationError: OPA decision x4rel/decisions must be one boolean per resource |

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
