# X7: revocation and faults

Profile: ['full']. Files: 1; records: 124.

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H3 cerbos-policy nocache | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H1 cerbos-policy ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-inv | CONFIRMED | median 3.884 [3.879, 3.891], limit 4.0; full run median 30.025 [30.019, 30.032], max 30.052 |
| A2-H1 cerbos-policy ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-shared-inv | CONFIRMED | median 3.887 [3.876, 3.900], limit 5.0; full run median 31.039 [31.026, 31.047], max 31.066 |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 40 | 10.000 | 10.000 | 3.881 [3.876, 3.893] | 3.935 | 3.929 | 0 | 0 | 0 | median 2.549 [2.369, 3.219], max 4.035 |
| cerbos-policy | ttl30-inv | 40 | 10.000 | 10.000 | 3.884 [3.879, 3.891] | 3.919 | 3.916 | 0 | 0 | 0 | median 30.025 [30.019, 30.032], max 30.052 |
| cerbos-policy | ttl30-shared-inv | 40 | 10.000 | 11.000 | 3.887 [3.876, 3.900] | 3.927 | 3.926 | 0 | 0 | 0 | median 31.039 [31.026, 31.047], max 31.066 |

## Amendment 2: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 40 | 40 | 3.881 [3.876, 3.893] | 3.935 | 3.929 | n/a | 0 | 0 | 0 | 0 | 5.1e-04 |
| cerbos-policy | ttl30-inv | 40 | 40 | 3.884 [3.879, 3.891] | 3.919 | 3.916 | n/a | 0 | 0 | 0 | 0 | 5.2e-04 |
| cerbos-policy | ttl30-shared-inv | 40 | 40 | 3.887 [3.876, 3.900] | 3.927 | 3.926 | n/a | 0 | 0 | 0 | 0 | 5.0e-04 |

## X7b tables (registered rules, no verdicts)

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['full']; commit ['41292bd'].
