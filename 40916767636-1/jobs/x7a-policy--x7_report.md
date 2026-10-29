# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 21. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7 exploratory cerbos-policy nocache | EXPLORATORY | median 3.936 [3.936, 3.936], maximum 3.936 |
| X7 exploratory cerbos-policy ttl5 | EXPLORATORY | median 5.023 [5.023, 5.023], maximum 5.023 |
| X7 exploratory cerbos-policy ttl30 | EXPLORATORY | median 30.002 [30.002, 30.002], maximum 30.002 |
| X7 exploratory cerbos-policy ttl30-inv | EXPLORATORY | median n/a [n/a, n/a], maximum n/a |
| X7 exploratory cerbos-policy ttl30-shared-inv | EXPLORATORY | median n/a [n/a, n/a], maximum n/a |
| X7-H1 opa-data nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-data ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-data ttl5 | INCONCLUSIVE | median 5.043 [5.043, 5.043] against [4.0, 6.0] |
| X7-H1 opa-data ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-data ttl30 | INCONCLUSIVE | median 30.034 [30.034, 30.034] against [29.0, 31.0] |
| X7-H1 opa-data ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-data ttl30-inv | INCONCLUSIVE | median 0.001 [0.001, 0.001], limit 0.5 |
| X7-H1 opa-data ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-data ttl30-shared-inv | INCONCLUSIVE | median 1.019 [1.019, 1.019], limit 1.5 |
| X7-H1 opa-policy nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H1 opa-policy ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 5.0 |
| X7-H2 opa-policy ttl5 | INCONCLUSIVE | median 5.048 [5.048, 5.048] against [4.0, 6.0] |
| X7-H1 opa-policy ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 30.0 |
| X7-H2 opa-policy ttl30 | INCONCLUSIVE | median 30.033 [30.033, 30.033] against [29.0, 31.0] |
| X7-H1 opa-policy ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 opa-policy ttl30-inv | INCONCLUSIVE | median 0.013 [0.013, 0.013], limit 0.5 |
| X7-H1 opa-policy ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 1.0 |
| X7-H3 opa-policy ttl30-shared-inv | INCONCLUSIVE | median 1.032 [1.032, 1.032], limit 1.5 |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 1 | 1 | 3.936 [3.936, 3.936] | 3.936 | 3.936 | n/a | 0 | 0 | 0 | 0 | 3.7e-04 |
| cerbos-policy | ttl5 | 1 | 1 | 5.023 [5.023, 5.023] | 5.023 | 5.023 | n/a | 0 | 0 | 0 | 0 | 5.6e-04 |
| cerbos-policy | ttl30 | 1 | 1 | 30.002 [30.002, 30.002] | 30.002 | 30.002 | n/a | 0 | 0 | 0 | 0 | 5.1e-04 |
| cerbos-policy | ttl30-inv | 1 | 1 | n/a [n/a, n/a] | n/a | n/a | n/a | 0 | 1 | 0 | 0 | 5.2e-04 |
| cerbos-policy | ttl30-shared-inv | 1 | 1 | n/a [n/a, n/a] | n/a | n/a | n/a | 0 | 1 | 0 | 0 | 4.5e-04 |
| opa-data | nocache | 1 | 1 | 8.0e-04 [8.0e-04, 8.0e-04] | 8.0e-04 | 8.0e-04 | 0.000 | 0 | 0 | 0 | 0 | 8.0e-04 |
| opa-data | ttl5 | 1 | 1 | 5.043 [5.043, 5.043] | 5.043 | 5.043 | 5.000 | 0 | 0 | 0 | 0 | 7.7e-04 |
| opa-data | ttl30 | 1 | 1 | 30.034 [30.034, 30.034] | 30.034 | 30.034 | 30.000 | 0 | 0 | 0 | 0 | 7.1e-04 |
| opa-data | ttl30-inv | 1 | 1 | 0.001 [0.001, 0.001] | 0.001 | 0.001 | 0.000 | 0 | 0 | 0 | 0 | 9.8e-04 |
| opa-data | ttl30-shared-inv | 1 | 1 | 1.019 [1.019, 1.019] | 1.019 | 1.019 | 1.000 | 0 | 0 | 0 | 0 | 8.7e-04 |
| opa-policy | nocache | 1 | 1 | 0.014 [0.014, 0.014] | 0.014 | 0.014 | 0.000 | 0 | 0 | 0 | 0 | 0.014 |
| opa-policy | ttl5 | 1 | 1 | 5.048 [5.048, 5.048] | 5.048 | 5.048 | 5.000 | 0 | 0 | 0 | 0 | 0.014 |
| opa-policy | ttl30 | 1 | 1 | 30.033 [30.033, 30.033] | 30.033 | 30.033 | 30.000 | 0 | 0 | 0 | 0 | 0.013 |
| opa-policy | ttl30-inv | 1 | 1 | 0.013 [0.013, 0.013] | 0.013 | 0.013 | 0.000 | 0 | 0 | 0 | 0 | 0.013 |
| opa-policy | ttl30-shared-inv | 1 | 1 | 1.032 [1.032, 1.032] | 1.032 | 1.032 | 1.000 | 0 | 0 | 0 | 0 | 0.014 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
