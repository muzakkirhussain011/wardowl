# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 21. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 openfga nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga ttl5 | INCONCLUSIVE | median 4.993 [4.993, 4.993] against [4.0, 6.0] |
| X7-H1 openfga ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga ttl30 | INCONCLUSIVE | median 29.997 [29.997, 29.997] against [29.0, 31.0] |
| X7-H1 openfga ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga ttl30-inv | INCONCLUSIVE | median 0.003 [0.003, 0.003], limit 0.5 |
| X7-H1 openfga ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga ttl30-shared-inv | INCONCLUSIVE | median 1.019 [1.019, 1.019], limit 1.5 |
| X7-H1 openfga-cached-hc nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 openfga-cached-hc ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 openfga-cached-hc ttl5 | INCONCLUSIVE | median 5.036 [5.036, 5.036] against [4.0, 6.0] |
| X7-H1 openfga-cached-hc ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 openfga-cached-hc ttl30 | INCONCLUSIVE | median 29.997 [29.997, 29.997] against [29.0, 31.0] |
| X7-H1 openfga-cached-hc ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 openfga-cached-hc ttl30-inv | INCONCLUSIVE | median 0.005 [0.005, 0.005], limit 0.5 |
| X7-H1 openfga-cached-hc ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 openfga-cached-hc ttl30-shared-inv | INCONCLUSIVE | median 1.024 [1.024, 1.024], limit 1.5 |
| X7-H1 openfga-cached-ml nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7 exploratory openfga-cached-ml nocache | EXPLORATORY | median 0.003 [0.003, 0.003], maximum 0.003 |
| X7-H1 openfga-cached-ml ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 15.0 |
| X7 exploratory openfga-cached-ml ttl5 | EXPLORATORY | median 4.990 [4.990, 4.990], maximum 4.990 |
| X7-H1 openfga-cached-ml ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 40.0 |
| X7 exploratory openfga-cached-ml ttl30 | EXPLORATORY | median 29.990 [29.990, 29.990], maximum 29.990 |
| X7-H1 openfga-cached-ml ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.0 |
| X7-H3 openfga-cached-ml ttl30-inv | INCONCLUSIVE | median 0.004 [0.004, 0.004], limit 10.5 |
| X7 exploratory openfga-cached-ml ttl30-inv | EXPLORATORY | median 0.004 [0.004, 0.004], maximum 0.004 |
| X7-H1 openfga-cached-ml ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 11.0 |
| X7-H3 openfga-cached-ml ttl30-shared-inv | INCONCLUSIVE | median 1.020 [1.020, 1.020], limit 11.5 |
| X7 exploratory openfga-cached-ml ttl30-shared-inv | EXPLORATORY | median 1.020 [1.020, 1.020], maximum 1.020 |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openfga | nocache | 1 | 1 | 0.006 [0.006, 0.006] | 0.006 | 0.006 | 0.000 | 0 | 0 | 0 | 0 | 0.006 |
| openfga | ttl5 | 1 | 1 | 4.993 [4.993, 4.993] | 4.993 | 4.993 | 5.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30 | 1 | 1 | 29.997 [29.997, 29.997] | 29.997 | 29.997 | 30.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30-inv | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga | ttl30-shared-inv | 1 | 1 | 1.019 [1.019, 1.019] | 1.019 | 1.019 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | nocache | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl5 | 1 | 1 | 5.036 [5.036, 5.036] | 5.036 | 5.036 | 5.000 | 0 | 0 | 0 | 0 | 0.005 |
| openfga-cached-hc | ttl30 | 1 | 1 | 29.997 [29.997, 29.997] | 29.997 | 29.997 | 30.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-hc | ttl30-inv | 1 | 1 | 0.005 [0.005, 0.005] | 0.005 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.005 |
| openfga-cached-hc | ttl30-shared-inv | 1 | 1 | 1.024 [1.024, 1.024] | 1.024 | 1.024 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | nocache | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 10.000 | 0 | 0 | 0 | 0 | 0.003 |
| openfga-cached-ml | ttl5 | 1 | 1 | 4.990 [4.990, 4.990] | 4.990 | 4.990 | 15.000 | 0 | 0 | 0 | 0 | 0.005 |
| openfga-cached-ml | ttl30 | 1 | 1 | 29.990 [29.990, 29.990] | 29.990 | 29.990 | 40.000 | 0 | 0 | 0 | 0 | 0.008 |
| openfga-cached-ml | ttl30-inv | 1 | 1 | 0.004 [0.004, 0.004] | 0.004 | 0.004 | 10.000 | 0 | 0 | 0 | 0 | 0.004 |
| openfga-cached-ml | ttl30-shared-inv | 1 | 1 | 1.020 [1.020, 1.020] | 1.020 | 1.020 | 11.000 | 0 | 0 | 0 | 0 | 0.003 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
