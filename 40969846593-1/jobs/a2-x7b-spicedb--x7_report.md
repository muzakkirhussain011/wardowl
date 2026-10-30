# X7: revocation and faults

Profile: ['full']. Files: 1; records: 24.

Amendment 2: the targeted rerun, wardowl from ['3c6559f3ecfd850bcd59416f14237d85887ba498'].

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| A2-H6 spicedb empty | CONFIRMED | failing 1.000 [1.000, 1.000], deviating 0.000 [0.000, 0.000] over 3520 requests; full run 4,703 inside, failing 0.000; 4,746 deviating answers, 1 failure |
| A2-H6 spicedb empty-lookup exact | CONFIRMED | 1.000 [1.000, 1.000] over 3180 requests |
| A2-H8 fail closed | CONFIRMED | 10303 requests: 0 leaks (one-sided bound 0.000291), 0 failures not AuthorizationError, 0 naming a host |

## Amendment 2: revocation

| path | condition | valid | D s | B2 s | median s [95% CI] | max s | p95 s | beyond B2 + 1 s | never took effect | flaps | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Amendment 2: faults

20 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing or hanging [95% CI] | failing [95% CI] | hangs | exact [95% CI] | deviating [95% CI] | median failing or hanging s | median failing s | failures | SearchError, fixed message | failure classes | naming a host | leaks | full run (comparison) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb | empty | plain | 10 | 3520 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.011 | 0.011 | 3549 | 0 | {'wardowl.authz.AuthorizationError': 3549} | 0 | 0 | 4,703 inside, failing 0.000; 4,746 deviating answers, 1 failure |
| spicedb | empty-lookup | plain | 10 | 3180 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | n/a | n/a | 0 | 0 | {} | 0 | 0 |  |

## X7a tables (registered rules, no verdicts)

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b tables (registered rules, no verdicts)

20 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spicedb | empty | plain | 10 | 3520 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 0 | 0 | 0.030 [0.024, 0.049] | 0.012 | {'ok': 1790, 'authz': 3549} | wardowl.authz.AuthorizationError: SpiceDB CheckBulkPermissions returned invalid JSON |
| spicedb | empty-lookup | plain | 10 | 3180 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.042 [0.029, 0.059] | n/a | {'ok': 4964} |  |

## Harness

Runs: 1 job records; profile ['full']; commit ['41292bd'].
