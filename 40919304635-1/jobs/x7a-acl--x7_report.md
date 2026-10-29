# X7: revocation and faults

Profile: ['full']. Files: 1; records: 405.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 acl-pgvector nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector nocache | CONFIRMED | median 7.0e-04 [6.8e-04, 7.2e-04] |
| X7-H1 acl-pgvector ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl5 | CONFIRMED | median 6.8e-04 [6.6e-04, 7.0e-04] |
| X7-H1 acl-pgvector ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl30 | CONFIRMED | median 7.1e-04 [6.8e-04, 7.5e-04] |
| X7-H1 acl-pgvector ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-inv | CONFIRMED | median 6.9e-04 [6.6e-04, 7.2e-04], limit 0.5 |
| X7-H4 acl-pgvector ttl30-inv | CONFIRMED | median 6.9e-04 [6.6e-04, 7.2e-04] |
| X7-H1 acl-pgvector ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-shared-inv | CONFIRMED | median 0.001 [0.001, 0.001], limit 1.5 |
| X7-H4 acl-pgvector ttl30-shared-inv | CONFIRMED | median 0.001 [0.001, 0.001] |
| X7-H1 acl-qdrant nocache | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant nocache | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl5 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl5 | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30 | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl30 | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-inv | CONFIRMED | median 0.002 [0.002, 0.002], limit 0.5 |
| X7-H4 acl-qdrant ttl30-inv | CONFIRMED | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30-shared-inv | CONFIRMED | 40 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-shared-inv | CONFIRMED | median 0.003 [0.003, 0.003], limit 1.5 |
| X7-H4 acl-qdrant ttl30-shared-inv | CONFIRMED | median 0.003 [0.003, 0.003] |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| acl-pgvector | nocache | 40 | 40 | 7.0e-04 [6.8e-04, 7.2e-04] | 0.086 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 7.0e-04 |
| acl-pgvector | ttl5 | 40 | 40 | 6.8e-04 [6.6e-04, 7.0e-04] | 0.095 | 0.010 | 0.000 | 0 | 0 | 0 | 0 | 6.8e-04 |
| acl-pgvector | ttl30 | 40 | 40 | 7.1e-04 [6.8e-04, 7.5e-04] | 0.046 | 0.012 | 0.000 | 0 | 0 | 0 | 0 | 7.1e-04 |
| acl-pgvector | ttl30-inv | 40 | 40 | 6.9e-04 [6.6e-04, 7.2e-04] | 0.082 | 0.025 | 0.000 | 0 | 0 | 0 | 0 | 6.8e-04 |
| acl-pgvector | ttl30-shared-inv | 40 | 40 | 0.001 [0.001, 0.001] | 0.030 | 0.006 | 0.000 | 0 | 0 | 0 | 0 | 7.0e-04 |
| acl-qdrant | nocache | 40 | 40 | 0.002 [0.002, 0.002] | 0.009 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl5 | 40 | 40 | 0.002 [0.002, 0.002] | 0.010 | 0.007 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30 | 40 | 40 | 0.002 [0.002, 0.002] | 0.009 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30-inv | 40 | 40 | 0.002 [0.002, 0.002] | 0.010 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30-shared-inv | 40 | 40 | 0.003 [0.003, 0.003] | 0.010 | 0.009 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
