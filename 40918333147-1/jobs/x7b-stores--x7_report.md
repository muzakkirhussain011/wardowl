# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 18. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 2894 requests: 0 leaks (one-sided bound 0.001035), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 1414 store-fault failures, 0 naming a host |
| X7-H7c pgvector blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector down | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector refuse | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b pgvector slow-1000 failing | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b pgvector slow-1000 latency rise | INCONCLUSIVE | median rise n/a [n/a, n/a] s against 1.0 s |
| X7-H7b pgvector slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 6 requests |
| X7-H7b pgvector slow-200 latency rise | INCONCLUSIVE | median rise 0.802 [0.802, 0.802] s against 0.2 s |
| X7-H7c qdrant blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c qdrant down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 276 requests |
| X7-H7c qdrant http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 276 requests |
| X7-H7c qdrant http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 277 requests |
| X7-H7c qdrant refuse | INCONCLUSIVE | 1.000 [1.000, 1.000] over 283 requests |
| X7-H7b qdrant slow-1000 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 4 requests |
| X7-H7b qdrant slow-1000 latency rise | INCONCLUSIVE | median rise 1.001 [1.001, 1.001] s against 1.0 s |
| X7-H7b qdrant slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 25 requests |
| X7-H7b qdrant slow-200 latency rise | INCONCLUSIVE | median rise 0.201 [0.201, 0.201] s against 0.2 s |
| X7-H7c qdrant truncate | INCONCLUSIVE | 1.000 [1.000, 1.000] over 262 requests |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

13 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.028 [0.028, 0.028] | n/a | {'ok': 115, 'error': 1} | psycopg.OperationalError: consuming input failed: server closed the connection unexpectedly 	This probably means the ser |
| pgvector | down | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.574 [0.574, 0.574] | n/a | {'ok': 119, 'error': 1} | psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | refuse | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.845 [0.845, 0.845] | n/a | {'ok': 117, 'error': 1} | psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | slow-1000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.058 [0.058, 0.058] | n/a | {'ok': 73} |  |
| pgvector | slow-200 | plain | 1 | 6 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.197 [0.197, 0.197] | n/a | {'ok': 124} |  |
| qdrant | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 2 | 0 | 0.025 [0.025, 0.025] | n/a | {'ok': 109, 'error': 2} | qdrant_client.http.exceptions.ResponseHandlingException: Server disconnected without sending a response.; qdrant_client.http.exceptions.ResponseHandlingException: timed out |
| qdrant | down | plain | 1 | 276 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 294 | 0 | 0.209 [0.209, 0.209] | 7.0e-04 | {'ok': 115, 'error': 294} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 104] Connection reset by peer; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | http500 | plain | 1 | 276 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 281 | 0 | 0.015 [0.015, 0.015] | 0.001 | {'ok': 112, 'error': 281} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 500 (Injected) Raw response content: b'{"error":" |
| qdrant | http503 | plain | 1 | 277 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 281 | 0 | 0.013 [0.013, 0.013] | 0.001 | {'ok': 112, 'error': 281} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 503 (Injected) Raw response content: b'{"error":" |
| qdrant | refuse | plain | 1 | 283 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 287 | 0 | 0.016 [0.016, 0.016] | 7.0e-04 | {'ok': 113, 'error': 287} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | slow-1000 | plain | 1 | 4 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.162 [0.162, 0.162] | n/a | {'ok': 119} |  |
| qdrant | slow-200 | plain | 1 | 25 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.054 [0.054, 0.054] | n/a | {'ok': 139} |  |
| qdrant | truncate | plain | 1 | 262 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 266 | 0 | 0.010 [0.010, 0.010] | 0.002 | {'ok': 113, 'error': 266} | json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 322 (char 321); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 269 (char 268); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 280 (char 279); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 282 (char 281); json.decoder.JSONDecodeError: Unterm |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
