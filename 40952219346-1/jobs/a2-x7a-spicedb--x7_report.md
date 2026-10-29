# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 9. **Smoke data: not analysed for the hypotheses.**

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H3 spicedb-ml nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| X7-H5 (replication) spicedb-ml staleness | INCONCLUSIVE | median 5.024 [5.024, 5.024], maximum 5.024 |
| A2-H3 spicedb-ml ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 16.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl5 | INCONCLUSIVE | median 5.017 [5.017, 5.017] against [4.0, 11.5] |
| A2-H3 spicedb-ml ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 41.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl30 | INCONCLUSIVE | median 30.001 [30.001, 30.001] against [29.0, 36.5] |
| A2-H1 spicedb-ml ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-inv | INCONCLUSIVE | median 3.177 [3.177, 3.177], limit 6.0; full run median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| A2-H1 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 12.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-shared-inv | INCONCLUSIVE | median 4.785 [4.785, 4.785], limit 7.0; full run median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb-ml | nocache | 1 | 11.000 | 11.000 | 5.024 [5.024, 5.024] | 5.024 | 5.024 | 0 | 0 | 2 | median 3.251 [2.994, 3.371], max 8.742; 1 of 40 beyond 6.5 s |
| spicedb-ml | ttl5 | 1 | 11.000 | 16.000 | 5.017 [5.017, 5.017] | 5.017 | 5.017 | 0 | 0 | 0 | median 5.023 [5.021, 5.026], max 6.828 |
| spicedb-ml | ttl30 | 1 | 11.000 | 41.000 | 30.001 [30.001, 30.001] | 30.001 | 30.001 | 0 | 0 | 0 | median 30.018 [30.008, 30.031], max 30.044 |
| spicedb-ml | ttl30-inv | 1 | 11.000 | 11.000 | 3.177 [3.177, 3.177] | 3.177 | 3.177 | 0 | 0 | 0 | median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| spicedb-ml | ttl30-shared-inv | 1 | 11.000 | 12.000 | 4.785 [4.785, 4.785] | 4.785 | 4.785 | 0 | 0 | 0 | median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |

## Amendment 2: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb-ml | nocache | 1 | 1 | 5.024 [5.024, 5.024] | 5.024 | 5.024 | 5.500 | 0 | 0 | 2 | 0 | 0.005 |
| spicedb-ml | ttl5 | 1 | 1 | 5.017 [5.017, 5.017] | 5.017 | 5.017 | 10.500 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | ttl30 | 1 | 1 | 30.001 [30.001, 30.001] | 30.001 | 30.001 | 35.500 | 0 | 0 | 0 | 0 | 0.006 |
| spicedb-ml | ttl30-inv | 1 | 1 | 3.177 [3.177, 3.177] | 3.177 | 3.177 | 5.500 | 0 | 0 | 0 | 0 | 0.004 |
| spicedb-ml | ttl30-shared-inv | 1 | 1 | 4.785 [4.785, 4.785] | 4.785 | 4.785 | 6.500 | 0 | 0 | 0 | 0 | 0.003 |

## X7b tables (registered rules, no verdicts)

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['smoke']; commit ['b0f5fec'].
