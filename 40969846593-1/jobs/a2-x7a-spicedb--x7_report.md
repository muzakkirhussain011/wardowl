# X7: revocation and faults

Profile: ['full']. Files: 1; records: 204.

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H3 spicedb-ml nocache | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| X7-H5 (replication) spicedb-ml staleness | CONFIRMED | median 4.732 [4.627, 4.799], maximum 5.212 |
| A2-H3 spicedb-ml ttl5 | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 16.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl5 | CONFIRMED | median 5.040 [5.039, 5.040] against [4.0, 11.5] |
| A2-H3 spicedb-ml ttl30 | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 41.000 (D = 11.000) |
| X7-H2 (replication) spicedb-ml ttl30 | CONFIRMED | median 30.017 [30.013, 30.024] against [29.0, 36.5] |
| A2-H1 spicedb-ml ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-inv | CONFIRMED | median 4.774 [4.708, 4.839], limit 6.0; full run median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| A2-H1 spicedb-ml ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 12.000 (D = 11.000) |
| A2-H2 spicedb-ml ttl30-shared-inv | CONFIRMED | median 4.767 [4.684, 4.827], limit 7.0; full run median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb-ml | nocache | 40 | 11.000 | 11.000 | 4.732 [4.627, 4.799] | 5.212 | 5.025 | 0 | 0 | 19 | median 3.251 [2.994, 3.371], max 8.742; 1 of 40 beyond 6.5 s |
| spicedb-ml | ttl5 | 40 | 11.000 | 16.000 | 5.040 [5.039, 5.040] | 10.088 | 10.087 | 0 | 0 | 0 | median 5.023 [5.021, 5.026], max 6.828 |
| spicedb-ml | ttl30 | 40 | 11.000 | 41.000 | 30.017 [30.013, 30.024] | 30.045 | 30.036 | 0 | 0 | 0 | median 30.018 [30.008, 30.031], max 30.044 |
| spicedb-ml | ttl30-inv | 40 | 11.000 | 11.000 | 4.774 [4.708, 4.839] | 5.226 | 5.058 | 0 | 0 | 28 | median 30.042 [30.031, 30.048], max 38.419; 40 of 40 beyond 6.5 s |
| spicedb-ml | ttl30-shared-inv | 40 | 11.000 | 12.000 | 4.767 [4.684, 4.827] | 5.187 | 4.998 | 0 | 0 | 16 | median 31.048 [31.033, 31.061], max 32.359; 39 of 40 beyond 7.5 s |

## Amendment 2: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb-ml | nocache | 40 | 40 | 4.732 [4.627, 4.799] | 5.212 | 5.025 | 5.500 | 0 | 0 | 19 | 0 | 0.003 |
| spicedb-ml | ttl5 | 40 | 40 | 5.040 [5.039, 5.040] | 10.088 | 10.087 | 10.500 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | ttl30 | 40 | 40 | 30.017 [30.013, 30.024] | 30.045 | 30.036 | 35.500 | 0 | 0 | 0 | 0 | 0.003 |
| spicedb-ml | ttl30-inv | 40 | 40 | 4.774 [4.708, 4.839] | 5.226 | 5.058 | 5.500 | 0 | 0 | 28 | 0 | 0.003 |
| spicedb-ml | ttl30-shared-inv | 40 | 40 | 4.767 [4.684, 4.827] | 5.187 | 4.998 | 6.500 | 0 | 0 | 16 | 0 | 0.003 |

## X7b tables (registered rules, no verdicts)

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['full']; commit ['41292bd'].
