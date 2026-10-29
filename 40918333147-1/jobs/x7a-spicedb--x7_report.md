# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 15. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 spicedb-fc nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 spicedb-fc ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 spicedb-fc ttl5 | INCONCLUSIVE | median 5.030 [5.030, 5.030] against [4.0, 6.0] |
| X7-H1 spicedb-fc ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 spicedb-fc ttl30 | INCONCLUSIVE | median 30.017 [30.017, 30.017] against [29.0, 31.0] |
| X7-H1 spicedb-fc ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 spicedb-fc ttl30-inv | INCONCLUSIVE | median 0.003 [0.003, 0.003], limit 0.5 |
| X7-H1 spicedb-fc ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 spicedb-fc ttl30-shared-inv | INCONCLUSIVE | median 1.018 [1.018, 1.018], limit 1.5 |
| X7-H1 spicedb-ml nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H5 spicedb-ml staleness | INCONCLUSIVE | median 4.604 [4.604, 4.604], maximum 4.604 |
| X7-H1 spicedb-ml ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 10.5 |
| X7-H2 spicedb-ml ttl5 | INCONCLUSIVE | median 5.017 [5.017, 5.017] against [4.0, 11.5] |
| X7-H1 spicedb-ml ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 35.5 |
| X7-H2 spicedb-ml ttl30 | INCONCLUSIVE | median 30.011 [30.011, 30.011] against [29.0, 36.5] |
| X7-H1 spicedb-ml ttl30-inv | FALSIFIED | 1 valid trials, 1 beyond B + 1 s (0 never took effect), B = 5.5 |
| X7-H3 spicedb-ml ttl30-inv | INCONCLUSIVE | median 30.036 [30.036, 30.036], limit 6.0 |
| X7-H1 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 6.5 |
| X7-H3 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | median 1.017 [1.017, 1.017], limit 7.0 |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb-fc | nocache | 1 | 1 | 0.005 [0.005, 0.005] | 0.005 | 0.005 | 0.000 | 0 | 0 | 0 | 0 | 0.005 |
| spicedb-fc | ttl5 | 1 | 1 | 5.030 [5.030, 5.030] | 5.030 | 5.030 | 5.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30 | 1 | 1 | 30.017 [30.017, 30.017] | 30.017 | 30.017 | 30.000 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-fc | ttl30-inv | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-fc | ttl30-shared-inv | 1 | 1 | 1.018 [1.018, 1.018] | 1.018 | 1.018 | 1.000 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | nocache | 1 | 1 | 4.604 [4.604, 4.604] | 4.604 | 4.604 | 5.500 | 0 | 0 | 1 | 0 | 0.006 |
| spicedb-ml | ttl5 | 1 | 1 | 5.017 [5.017, 5.017] | 5.017 | 5.017 | 10.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30 | 1 | 1 | 30.011 [30.011, 30.011] | 30.011 | 30.011 | 35.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-inv | 1 | 1 | 30.036 [30.036, 30.036] | 30.036 | 30.036 | 5.500 | 1 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-shared-inv | 1 | 1 | 1.017 [1.017, 1.017] | 1.017 | 1.017 | 6.500 | 0 | 0 | 0 | 0 | 0.004 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
