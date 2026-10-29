# X7: revocation and faults

Profile: ['full']. Files: 1; records: 606.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7 exploratory cerbos-policy nocache | EXPLORATORY | median 2.549 [2.369, 3.219], maximum 4.035 |
| X7 exploratory cerbos-policy ttl5 | EXPLORATORY | median 5.018 [5.010, 5.027], maximum 5.048 |
| X7 exploratory cerbos-policy ttl30 | EXPLORATORY | median 30.017 [30.011, 30.021], maximum 30.044 |
| X7 exploratory cerbos-policy ttl30-inv | EXPLORATORY | median 30.025 [30.019, 30.032], maximum 30.052 |
| X7 exploratory cerbos-policy ttl30-shared-inv | EXPLORATORY | median 31.039 [31.026, 31.047], maximum 31.066 |
| X7-H1 opa-data nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-data ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-data ttl5 | CONFIRMED | median 5.034 [5.032, 5.037] against [4.0, 6.0] |
| X7-H1 opa-data ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-data ttl30 | CONFIRMED | median 30.033 [30.020, 30.036] against [29.0, 31.0] |
| X7-H1 opa-data ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-data ttl30-inv | CONFIRMED | median 6.0e-04 [5.8e-04, 6.2e-04], limit 0.5 |
| X7-H1 opa-data ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-data ttl30-shared-inv | CONFIRMED | median 1.018 [1.017, 1.019], limit 1.5 |
| X7-H1 opa-policy nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-policy ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-policy ttl5 | CONFIRMED | median 5.021 [5.020, 5.022] against [4.0, 6.0] |
| X7-H1 opa-policy ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-policy ttl30 | CONFIRMED | median 30.030 [30.028, 30.032] against [29.0, 31.0] |
| X7-H1 opa-policy ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-policy ttl30-inv | CONFIRMED | median 0.009 [0.009, 0.010], limit 0.5 |
| X7-H1 opa-policy ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-policy ttl30-shared-inv | CONFIRMED | median 1.022 [1.021, 1.023], limit 1.5 |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 40 | 40 | 2.549 [2.369, 3.219] | 4.035 | 3.954 | n/a | 0 | 0 | 0 | 0 | 4.8e-04 |
| cerbos-policy | ttl5 | 40 | 40 | 5.018 [5.010, 5.027] | 5.048 | 5.046 | n/a | 0 | 0 | 0 | 0 | 4.7e-04 |
| cerbos-policy | ttl30 | 40 | 40 | 30.017 [30.011, 30.021] | 30.044 | 30.042 | n/a | 0 | 0 | 0 | 0 | 4.8e-04 |
| cerbos-policy | ttl30-inv | 40 | 40 | 30.025 [30.019, 30.032] | 30.052 | 30.046 | n/a | 0 | 0 | 0 | 0 | 4.7e-04 |
| cerbos-policy | ttl30-shared-inv | 40 | 40 | 31.039 [31.026, 31.047] | 31.066 | 31.061 | n/a | 0 | 0 | 0 | 0 | 4.8e-04 |
| opa-data | nocache | 40 | 40 | 6.0e-04 [5.7e-04, 6.2e-04] | 0.003 | 0.001 | 0.000 | 0 | 0 | 0 | 0 | 6.0e-04 |
| opa-data | ttl5 | 40 | 40 | 5.034 [5.032, 5.037] | 5.047 | 5.044 | 5.000 | 0 | 0 | 0 | 0 | 6.1e-04 |
| opa-data | ttl30 | 40 | 40 | 30.033 [30.020, 30.036] | 30.048 | 30.046 | 30.000 | 0 | 0 | 0 | 0 | 6.0e-04 |
| opa-data | ttl30-inv | 40 | 40 | 6.0e-04 [5.8e-04, 6.2e-04] | 0.003 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 5.9e-04 |
| opa-data | ttl30-shared-inv | 40 | 40 | 1.018 [1.017, 1.019] | 1.025 | 1.023 | 1.000 | 0 | 0 | 0 | 0 | 5.9e-04 |
| opa-policy | nocache | 40 | 40 | 0.010 [0.009, 0.010] | 0.015 | 0.011 | 0.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl5 | 40 | 40 | 5.021 [5.020, 5.022] | 5.045 | 5.034 | 5.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl30 | 40 | 40 | 30.030 [30.028, 30.032] | 30.045 | 30.041 | 30.000 | 0 | 0 | 0 | 0 | 0.009 |
| opa-policy | ttl30-inv | 40 | 40 | 0.009 [0.009, 0.010] | 0.017 | 0.012 | 0.000 | 0 | 0 | 0 | 0 | 0.009 |
| opa-policy | ttl30-shared-inv | 40 | 40 | 1.022 [1.021, 1.023] | 1.028 | 1.026 | 1.000 | 0 | 0 | 0 | 0 | 0.009 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
