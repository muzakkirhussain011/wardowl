# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 21. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7 exploratory cerbos-policy nocache | EXPLORATORY | median 3.927 [3.927, 3.927], maximum 3.927 |
| X7 exploratory cerbos-policy ttl5 | EXPLORATORY | median 5.011 [5.011, 5.011], maximum 5.011 |
| X7 exploratory cerbos-policy ttl30 | EXPLORATORY | median 30.039 [30.039, 30.039], maximum 30.039 |
| X7 exploratory cerbos-policy ttl30-inv | EXPLORATORY | median 30.042 [30.042, 30.042], maximum 30.042 |
| X7 exploratory cerbos-policy ttl30-shared-inv | EXPLORATORY | median 31.055 [31.055, 31.055], maximum 31.055 |
| X7-H1 opa-data nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-data ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-data ttl5 | INCONCLUSIVE | median 5.021 [5.021, 5.021] against [4.0, 6.0] |
| X7-H1 opa-data ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-data ttl30 | INCONCLUSIVE | median 30.032 [30.032, 30.032] against [29.0, 31.0] |
| X7-H1 opa-data ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-data ttl30-inv | INCONCLUSIVE | median 6.7e-04 [6.7e-04, 6.7e-04], limit 0.5 |
| X7-H1 opa-data ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-data ttl30-shared-inv | INCONCLUSIVE | median 0.987 [0.987, 0.987], limit 1.5 |
| X7-H1 opa-policy nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-policy ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-policy ttl5 | INCONCLUSIVE | median 5.029 [5.029, 5.029] against [4.0, 6.0] |
| X7-H1 opa-policy ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-policy ttl30 | INCONCLUSIVE | median 30.046 [30.046, 30.046] against [29.0, 31.0] |
| X7-H1 opa-policy ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-policy ttl30-inv | INCONCLUSIVE | median 0.010 [0.010, 0.010], limit 0.5 |
| X7-H1 opa-policy ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-policy ttl30-shared-inv | INCONCLUSIVE | median 1.030 [1.030, 1.030], limit 1.5 |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 1 | 1 | 3.927 [3.927, 3.927] | 3.927 | 3.927 | n/a | 0 | 0 | 0 | 0 | 3.4e-04 |
| cerbos-policy | ttl5 | 1 | 1 | 5.011 [5.011, 5.011] | 5.011 | 5.011 | n/a | 0 | 0 | 0 | 0 | 5.0e-04 |
| cerbos-policy | ttl30 | 1 | 1 | 30.039 [30.039, 30.039] | 30.039 | 30.039 | n/a | 0 | 0 | 0 | 0 | 4.5e-04 |
| cerbos-policy | ttl30-inv | 1 | 1 | 30.042 [30.042, 30.042] | 30.042 | 30.042 | n/a | 0 | 0 | 0 | 0 | 5.2e-04 |
| cerbos-policy | ttl30-shared-inv | 1 | 1 | 31.055 [31.055, 31.055] | 31.055 | 31.055 | n/a | 0 | 0 | 0 | 0 | 4.9e-04 |
| opa-data | nocache | 1 | 1 | 5.2e-04 [5.2e-04, 5.2e-04] | 5.2e-04 | 5.2e-04 | 0.000 | 0 | 0 | 0 | 0 | 5.2e-04 |
| opa-data | ttl5 | 1 | 1 | 5.021 [5.021, 5.021] | 5.021 | 5.021 | 5.000 | 0 | 0 | 0 | 0 | 6.1e-04 |
| opa-data | ttl30 | 1 | 1 | 30.032 [30.032, 30.032] | 30.032 | 30.032 | 30.000 | 0 | 0 | 0 | 0 | 6.0e-04 |
| opa-data | ttl30-inv | 1 | 1 | 6.7e-04 [6.7e-04, 6.7e-04] | 6.7e-04 | 6.7e-04 | 0.000 | 0 | 0 | 0 | 0 | 6.6e-04 |
| opa-data | ttl30-shared-inv | 1 | 1 | 0.987 [0.987, 0.987] | 0.987 | 0.987 | 1.000 | 0 | 0 | 0 | 0 | 7.4e-04 |
| opa-policy | nocache | 1 | 1 | 0.010 [0.010, 0.010] | 0.010 | 0.010 | 0.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl5 | 1 | 1 | 5.029 [5.029, 5.029] | 5.029 | 5.029 | 5.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl30 | 1 | 1 | 30.046 [30.046, 30.046] | 30.046 | 30.046 | 30.000 | 0 | 0 | 0 | 0 | 0.012 |
| opa-policy | ttl30-inv | 1 | 1 | 0.010 [0.010, 0.010] | 0.010 | 0.010 | 0.000 | 0 | 0 | 0 | 0 | 0.010 |
| opa-policy | ttl30-shared-inv | 1 | 1 | 1.030 [1.030, 1.030] | 1.030 | 1.030 | 1.000 | 0 | 0 | 0 | 0 | 0.009 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
