# X7: revocation and faults

Profile: ['full']. Files: 1; records: 606.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 openfga nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga ttl5 | CONFIRMED | median 5.015 [5.013, 5.020] against [4.0, 6.0] |
| X7-H1 openfga ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga ttl30 | CONFIRMED | median 30.020 [30.014, 30.026] against [29.0, 31.0] |
| X7-H1 openfga ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga ttl30-inv | CONFIRMED | median 0.003 [0.002, 0.004], limit 0.5 |
| X7-H1 openfga ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga ttl30-shared-inv | CONFIRMED | median 1.014 [1.012, 1.015], limit 1.5 |
| X7-H1 openfga-cached-hc nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga-cached-hc ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga-cached-hc ttl5 | CONFIRMED | median 5.015 [5.015, 5.017] against [4.0, 6.0] |
| X7-H1 openfga-cached-hc ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga-cached-hc ttl30 | CONFIRMED | median 30.016 [30.009, 30.025] against [29.0, 31.0] |
| X7-H1 openfga-cached-hc ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga-cached-hc ttl30-inv | CONFIRMED | median 0.003 [0.002, 0.003], limit 0.5 |
| X7-H1 openfga-cached-hc ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga-cached-hc ttl30-shared-inv | CONFIRMED | median 1.015 [1.015, 1.016], limit 1.5 |
| X7-H1 openfga-cached-ml nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7 exploratory openfga-cached-ml nocache | EXPLORATORY | median 0.003 [0.002, 0.003], maximum 0.008 |
| X7-H1 openfga-cached-ml ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 15.0 |
| X7 exploratory openfga-cached-ml ttl5 | EXPLORATORY | median 5.015 [5.014, 5.016], maximum 5.045 |
| X7-H1 openfga-cached-ml ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 40.0 |
| X7 exploratory openfga-cached-ml ttl30 | EXPLORATORY | median 30.022 [30.014, 30.031], maximum 30.044 |
| X7-H1 openfga-cached-ml ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7-H3 openfga-cached-ml ttl30-inv | CONFIRMED | median 0.003 [0.002, 0.003], limit 10.5 |
| X7 exploratory openfga-cached-ml ttl30-inv | EXPLORATORY | median 0.003 [0.002, 0.003], maximum 0.006 |
| X7-H1 openfga-cached-ml ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 11.0 |
| X7-H3 openfga-cached-ml ttl30-shared-inv | CONFIRMED | median 1.015 [1.015, 1.016], limit 11.5 |
| X7 exploratory openfga-cached-ml ttl30-shared-inv | EXPLORATORY | median 1.015 [1.015, 1.016], maximum 1.022 |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openfga | nocache | 40 | 40 | 0.003 [0.003, 0.004] | 0.006 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl5 | 40 | 40 | 5.015 [5.013, 5.020] | 5.039 | 5.039 | 5.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30 | 40 | 40 | 30.020 [30.014, 30.026] | 30.042 | 30.038 | 30.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30-inv | 40 | 40 | 0.003 [0.002, 0.004] | 0.078 | 0.008 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30-shared-inv | 40 | 40 | 1.014 [1.012, 1.015] | 1.021 | 1.017 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | nocache | 40 | 40 | 0.003 [0.003, 0.003] | 0.007 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl5 | 40 | 40 | 5.015 [5.015, 5.017] | 5.039 | 5.034 | 5.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl30 | 40 | 40 | 30.016 [30.009, 30.025] | 30.043 | 30.040 | 30.000 | 0 | 0 | 0 | 0 | 0.002 |
| openfga-cached-hc | ttl30-inv | 40 | 40 | 0.003 [0.002, 0.003] | 0.006 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl30-shared-inv | 40 | 40 | 1.015 [1.015, 1.016] | 1.020 | 1.017 | 1.000 | 0 | 0 | 0 | 0 | 0.002 |
| openfga-cached-ml | nocache | 40 | 40 | 0.003 [0.002, 0.003] | 0.008 | 0.004 | 10.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl5 | 40 | 40 | 5.015 [5.014, 5.016] | 5.045 | 5.023 | 15.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl30 | 40 | 40 | 30.022 [30.014, 30.031] | 30.044 | 30.039 | 40.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl30-inv | 40 | 40 | 0.003 [0.002, 0.003] | 0.006 | 0.004 | 10.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl30-shared-inv | 40 | 40 | 1.015 [1.015, 1.016] | 1.022 | 1.019 | 11.000 | 0 | 0 | 0 | 0 | 0.002 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
