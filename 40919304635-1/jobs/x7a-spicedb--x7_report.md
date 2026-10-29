# X7: revocation and faults

Profile: ['full']. Files: 1; records: 405.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 spicedb-fc nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 spicedb-fc ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 spicedb-fc ttl5 | CONFIRMED | median 5.021 [5.019, 5.024] against [4.0, 6.0] |
| X7-H1 spicedb-fc ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 spicedb-fc ttl30 | CONFIRMED | median 30.017 [30.005, 30.026] against [29.0, 31.0] |
| X7-H1 spicedb-fc ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 spicedb-fc ttl30-inv | CONFIRMED | median 0.004 [0.004, 0.005], limit 0.5 |
| X7-H1 spicedb-fc ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 spicedb-fc ttl30-shared-inv | CONFIRMED | median 1.017 [1.016, 1.018], limit 1.5 |
| X7-H1 spicedb-ml nocache | FALSIFIED | 40 valid trials, 1 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H5 spicedb-ml staleness | FALSIFIED | median 3.251 [2.994, 3.371], maximum 8.742 |
| X7-H1 spicedb-ml ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.5 |
| X7-H2 spicedb-ml ttl5 | CONFIRMED | median 5.023 [5.021, 5.026] against [4.0, 11.5] |
| X7-H1 spicedb-ml ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 35.5 |
| X7-H2 spicedb-ml ttl30 | CONFIRMED | median 30.018 [30.008, 30.031] against [29.0, 36.5] |
| X7-H1 spicedb-ml ttl30-inv | FALSIFIED | 40 valid trials, 40 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H3 spicedb-ml ttl30-inv | FALSIFIED | median 30.042 [30.031, 30.048], limit 6.0 |
| X7-H1 spicedb-ml ttl30-shared-inv | FALSIFIED | 40 valid trials, 39 beyond B + 1 s (0 never took effect), B = 6.5 |
| X7-H3 spicedb-ml ttl30-shared-inv | FALSIFIED | median 31.048 [31.033, 31.061], limit 7.0 |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb-fc | nocache | 40 | 40 | 0.004 [0.003, 0.004] | 0.008 | 0.006 | 0.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl5 | 40 | 40 | 5.021 [5.019, 5.024] | 5.039 | 5.028 | 5.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30 | 40 | 40 | 30.017 [30.005, 30.026] | 30.045 | 30.041 | 30.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30-inv | 40 | 40 | 0.004 [0.004, 0.005] | 0.069 | 0.006 | 0.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30-shared-inv | 40 | 40 | 1.017 [1.016, 1.018] | 1.029 | 1.020 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | nocache | 40 | 40 | 3.251 [2.994, 3.371] | 8.742 | 4.938 | 5.500 | 1 | 0 | 28 | 0 | 0.004 |
| spicedb-ml | ttl5 | 40 | 40 | 5.023 [5.021, 5.026] | 6.828 | 5.034 | 10.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30 | 40 | 40 | 30.018 [30.008, 30.031] | 30.044 | 30.041 | 35.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-inv | 40 | 40 | 30.042 [30.031, 30.048] | 38.419 | 30.056 | 5.500 | 40 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-shared-inv | 40 | 40 | 31.048 [31.033, 31.061] | 32.359 | 31.073 | 6.500 | 39 | 0 | 0 | 0 | 0.003 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
