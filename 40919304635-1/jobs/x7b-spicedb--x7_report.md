# X7: revocation and faults

Profile: ['full']. Files: 1; records: 244.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | CONFIRMED | {'spicedb': 17484} |
| X7-H6 fail closed | CONFIRMED | 138988 requests: 0 leaks (one-sided bound 0.000022), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |
| X7-H7a spicedb blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7-H7a spicedb down | CONFIRMED | 1.000 [1.000, 1.000] over 1644 requests |
| X7-H7a spicedb http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5803 requests |
| X7-H7a spicedb http503 | CONFIRMED | 1.000 [1.000, 1.000] over 1667 requests |
| X7-H7a spicedb refuse | CONFIRMED | 1.000 [1.000, 1.000] over 1670 requests |
| X7-H7b spicedb slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 43 requests |
| X7-H7b spicedb slow-1000 latency rise | CONFIRMED | median rise 2.013 [2.008, 2.017] s against 1.0 s |
| X7-H7b spicedb slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 259 requests |
| X7-H7b spicedb slow-200 latency rise | CONFIRMED | median rise 0.407 [0.405, 0.411] s against 0.2 s |
| X7-H7a spicedb slow-3000 | CONFIRMED | 1.000 [1.000, 1.000] over 40 requests |
| X7 exploratory spicedb drop-last | EXPLORATORY | {'ok': 2003, 'authz': 3938} |
| X7 exploratory spicedb empty | EXPLORATORY | {'ok': 1965, 'deviate': 4746, 'authz': 1} |
| X7 exploratory spicedb garbage-json | EXPLORATORY | {'ok': 1983, 'authz': 4817} |
| X7 exploratory spicedb truncate | EXPLORATORY | {'ok': 1986, 'authz': 4698} |
| X7 exploratory spicedb type-flip | EXPLORATORY | {'ok': 1937, 'authz': 4455} |
| X7-H8b spicedb blackhole recovery | CONFIRMED | median recovery 3.137 [3.128, 3.141] |
| X7-H8a spicedb blackhole | CONFIRMED | median recovery 0.116 [0.110, 0.125] |
| X7-H8b spicedb down recovery | CONFIRMED | median recovery 3.548 [3.531, 3.570] |
| X7 exploratory recovery spicedb down | EXPLORATORY | median recovery 0.465 [0.445, 0.551] |
| X7-H8b spicedb http500 recovery | CONFIRMED | median recovery 3.148 [3.137, 3.163] |
| X7-H8a spicedb http500 | CONFIRMED | median recovery 0.030 [0.026, 0.040] |
| X7-H8a spicedb http503 | CONFIRMED | median recovery 0.044 [0.033, 0.064] |
| X7-H8b spicedb refuse recovery | CONFIRMED | median recovery 3.505 [3.488, 3.514] |
| X7-H8a spicedb refuse | CONFIRMED | median recovery 0.095 [0.084, 0.104] |
| X7-H8b spicedb slow-3000 recovery | CONFIRMED | median recovery 3.143 [3.138, 3.153] |
| X7-H8a spicedb slow-3000 | CONFIRMED | median recovery 0.178 [0.164, 0.182] |
| X7-H8b spicedb blackhole fail-fast | CONFIRMED | failed latency 1.0e-04 s with breaker, 2.002 s without |
| X7-H9 spicedb blackhole | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb down | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb http500 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb refuse | CONFIRMED | succeeding 1.000 [1.000, 1.000] |
| X7-H9 spicedb slow-3000 | CONFIRMED | succeeding 1.000 [1.000, 1.000] |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

240 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb | allow-all | plain | 10 | 4846 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 17484 | 0 | 0 | 0.019 [0.008, 0.025] | n/a | {'ok': 2186, 'leak': 4887} |  |
| spicedb | blackhole | breaker | 10 | 971 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.137 [3.128, 3.141] | 1.0e-04 | {'ok': 1970, 'authz': 2509} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions timed out after 2.0 s; wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | blackhole | cache30 | 10 | 5604 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.018 [0.011, 0.021] | n/a | {'ok': 8424} |  |
| spicedb | blackhole | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.116 [0.110, 0.125] | 2.002 | {'ok': 1963, 'authz': 50} | wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | down | breaker | 10 | 5696 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.548 [3.531, 3.570] | 1.0e-04 | {'ok': 1939, 'authz': 7445} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionResetError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | down | cache30 | 10 | 5463 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.016 [0.008, 0.020] | n/a | {'ok': 8424} |  |
| spicedb | down | plain | 10 | 1644 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.465 [0.445, 0.551] | 0.051 | {'ok': 2030, 'authz': 1745} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionResetError |
| spicedb | drop-last | plain | 10 | 3903 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.024 [0.013, 0.026] | 0.009 | {'ok': 2003, 'authz': 3938} | wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d181': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d254': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None for 'fsp0d299': no answer, or a caveat that needs context; wardowl.authz.AuthorizationError: SpiceDB returned None |
| spicedb | empty | plain | 10 | 4703 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.026 [0.021, 0.030] | n/a | {'ok': 1965, 'deviate': 4746, 'authz': 1} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned invalid JSON |
| spicedb | garbage-json | plain | 10 | 4772 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.026 [0.021, 0.034] | 0.004 | {'ok': 1983, 'authz': 4817} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned an unexpected response; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: {'unexpected': True} |
| spicedb | http500 | breaker | 10 | 5872 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.148 [3.137, 3.163] | 5.0e-05 | {'ok': 1933, 'authz': 7449} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned HTTP 500; wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | http500 | cache30 | 10 | 5590 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.015 [0.008, 0.020] | n/a | {'ok': 8415} |  |
| spicedb | http500 | plain | 10 | 5803 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.026, 0.040] | 3.0e-04 | {'ok': 1923, 'authz': 5852} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned HTTP 500; wardowl.authz.AuthorizationError: SpiceDB LookupResources returned HTTP 500 |
| spicedb | http503 | plain | 10 | 1667 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.044 [0.033, 0.064] | 0.051 | {'ok': 1950, 'authz': 1687} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: HTTP 503; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: HTTP 503 |
| spicedb | refuse | breaker | 10 | 5732 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.505 [3.488, 3.514] | 0.000 | {'ok': 1969, 'authz': 7454} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | refuse | cache30 | 10 | 5607 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.010 [0.008, 0.016] | n/a | {'ok': 8428} |  |
| spicedb | refuse | plain | 10 | 1670 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.095 [0.084, 0.104] | 0.051 | {'ok': 1991, 'authz': 1690} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions failed: ConnectionRefusedError; wardowl.authz.AuthorizationError: SpiceDB LookupResources failed: ConnectionRefusedError |
| spicedb | slow-1000 | plain | 10 | 43 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.293 [0.266, 0.342] | n/a | {'ok': 2043} |  |
| spicedb | slow-200 | plain | 10 | 259 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.125 [0.082, 0.204] | n/a | {'ok': 2267} |  |
| spicedb | slow-3000 | breaker | 10 | 969 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 3.143 [3.138, 3.153] | 1.0e-04 | {'ok': 1925, 'authz': 2509} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions timed out after 2.0 s; wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s; wardowl.authz.AuthorizationError: the permission service keeps failing; requests are paused (circuit open) |
| spicedb | slow-3000 | cache30 | 10 | 5610 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.006 [0.004, 0.014] | n/a | {'ok': 8442} |  |
| spicedb | slow-3000 | plain | 10 | 40 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.178 [0.164, 0.182] | 2.003 | {'ok': 1973, 'authz': 60} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions timed out after 2.0 s; wardowl.authz.AuthorizationError: SpiceDB LookupResources timed out after 2.0 s |
| spicedb | truncate | plain | 10 | 4654 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.027 [0.020, 0.035] | 0.004 | {'ok': 1986, 'authz': 4698} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned invalid JSON; wardowl.authz.AuthorizationError: SpiceDB LookupResources returned invalid JSON |
| spicedb | type-flip | plain | 10 | 4414 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.037 [0.022, 0.041] | 0.006 | {'ok': 1937, 'authz': 4455} | wardowl.authz.AuthorizationError: SpiceDB LookupResources returned 'X_UNKNOWN_VALUE'; wardowl.authz.AuthorizationError: SpiceDB returned 'X_UNKNOWN_VALUE' for 'fsp3d145': no answer, or a caveat that needs c |

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
