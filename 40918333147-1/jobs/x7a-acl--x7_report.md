# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 15. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| X7-H1 acl-pgvector nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector nocache | INCONCLUSIVE | median 9.9e-04 [9.9e-04, 9.9e-04] |
| X7-H1 acl-pgvector ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl5 | INCONCLUSIVE | median 8.8e-04 [8.8e-04, 8.8e-04] |
| X7-H1 acl-pgvector ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-pgvector ttl30 | INCONCLUSIVE | median 9.1e-04 [9.1e-04, 9.1e-04] |
| X7-H1 acl-pgvector ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-inv | INCONCLUSIVE | median 9.7e-04 [9.7e-04, 9.7e-04], limit 0.5 |
| X7-H4 acl-pgvector ttl30-inv | INCONCLUSIVE | median 9.7e-04 [9.7e-04, 9.7e-04] |
| X7-H1 acl-pgvector ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-pgvector ttl30-shared-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002], limit 1.5 |
| X7-H4 acl-pgvector ttl30-shared-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant nocache | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant nocache | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl5 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl5 | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30 | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H4 acl-qdrant ttl30 | INCONCLUSIVE | median 0.003 [0.003, 0.003] |
| X7-H1 acl-qdrant ttl30-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002], limit 0.5 |
| X7-H4 acl-qdrant ttl30-inv | INCONCLUSIVE | median 0.002 [0.002, 0.002] |
| X7-H1 acl-qdrant ttl30-shared-inv | INCONCLUSIVE | 1 valid trials, 0 beyond B + 1 s (0 never took effect), B = 0.0 |
| X7-H3 acl-qdrant ttl30-shared-inv | INCONCLUSIVE | median 0.003 [0.003, 0.003], limit 1.5 |
| X7-H4 acl-qdrant ttl30-shared-inv | INCONCLUSIVE | median 0.003 [0.003, 0.003] |
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 0 requests: 0 leaks (one-sided bound 1.000000), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 0 store-fault failures, 0 naming a host |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| acl-pgvector | nocache | 1 | 1 | 9.9e-04 [9.9e-04, 9.9e-04] | 9.9e-04 | 9.9e-04 | 0.000 | 0 | 0 | 0 | 0 | 9.9e-04 |
| acl-pgvector | ttl5 | 1 | 1 | 8.8e-04 [8.8e-04, 8.8e-04] | 8.8e-04 | 8.8e-04 | 0.000 | 0 | 0 | 0 | 0 | 8.8e-04 |
| acl-pgvector | ttl30 | 1 | 1 | 9.1e-04 [9.1e-04, 9.1e-04] | 9.1e-04 | 9.1e-04 | 0.000 | 0 | 0 | 0 | 0 | 9.0e-04 |
| acl-pgvector | ttl30-inv | 1 | 1 | 9.7e-04 [9.7e-04, 9.7e-04] | 9.7e-04 | 9.7e-04 | 0.000 | 0 | 0 | 0 | 0 | 9.6e-04 |
| acl-pgvector | ttl30-shared-inv | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 9.5e-04 |
| acl-qdrant | nocache | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl5 | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30 | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.003 |
| acl-qdrant | ttl30-inv | 1 | 1 | 0.002 [0.002, 0.002] | 0.002 | 0.002 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |
| acl-qdrant | ttl30-shared-inv | 1 | 1 | 0.003 [0.003, 0.003] | 0.003 | 0.003 | 0.000 | 0 | 0 | 0 | 0 | 0.002 |

## X7b: faults

0 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
