# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 7. **Smoke data: not analysed for the hypotheses.**

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H3 cerbos-policy nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H1 cerbos-policy ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 10.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-inv | INCONCLUSIVE | median 3.876 [3.876, 3.876], limit 4.0; full run median 30.025 [30.019, 30.032], max 30.052 |
| A2-H1 cerbos-policy ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B2 + 1 s (0 never took effect), B2 = 11.000 (D = 10.000) |
| A2-H2 cerbos-policy ttl30-shared-inv | INCONCLUSIVE | median 3.890 [3.890, 3.890], limit 5.0; full run median 31.039 [31.026, 31.047], max 31.066 |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 1 | 10.000 | 10.000 | 3.738 [3.738, 3.738] | 3.738 | 3.738 | 0 | 0 | 0 | median 2.549 [2.369, 3.219], max 4.035 |
| cerbos-policy | ttl30-inv | 1 | 10.000 | 10.000 | 3.876 [3.876, 3.876] | 3.876 | 3.876 | 0 | 0 | 0 | median 30.025 [30.019, 30.032], max 30.052 |
| cerbos-policy | ttl30-shared-inv | 1 | 10.000 | 11.000 | 3.890 [3.890, 3.890] | 3.890 | 3.890 | 0 | 0 | 0 | median 31.039 [31.026, 31.047], max 31.066 |

## Amendment 2: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos-policy | nocache | 1 | 1 | 3.738 [3.738, 3.738] | 3.738 | 3.738 | n/a | 0 | 0 | 0 | 0 | 3.3e-04 |
| cerbos-policy | ttl30-inv | 1 | 1 | 3.876 [3.876, 3.876] | 3.876 | 3.876 | n/a | 0 | 0 | 0 | 0 | 4.3e-04 |
| cerbos-policy | ttl30-shared-inv | 1 | 1 | 3.890 [3.890, 3.890] | 3.890 | 3.890 | n/a | 0 | 0 | 0 | 0 | 3.9e-04 |

## X7b tables (registered rules, no verdicts)

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['smoke']; commit ['b0f5fec'].
