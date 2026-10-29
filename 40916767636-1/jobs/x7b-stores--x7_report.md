# X7: revocation and faults

Profile: ['smoke']. Files: 1; records: 18. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 2172 requests: 0 leaks (one-sided bound 0.001378), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 707 store-fault failures, 0 naming a host |
| X7-H7c pgvector blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector down | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector refuse | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b pgvector slow-1000 failing | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7b pgvector slow-1000 latency rise | INCONCLUSIVE | median rise n/a [n/a, n/a] s against 1.0 s |
| X7-H7b pgvector slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 2 requests |
| X7-H7b pgvector slow-200 latency rise | INCONCLUSIVE | median rise 0.802 [0.802, 0.802] s against 0.2 s |
| X7-H7c qdrant blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c qdrant down | INCONCLUSIVE | 1.000 [1.000, 1.000] over 138 requests |
| X7-H7c qdrant http500 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 136 requests |
| X7-H7c qdrant http503 | INCONCLUSIVE | 1.000 [1.000, 1.000] over 136 requests |
| X7-H7c qdrant refuse | INCONCLUSIVE | 1.000 [1.000, 1.000] over 140 requests |
| X7-H7b qdrant slow-1000 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 1 requests |
| X7-H7b qdrant slow-1000 latency rise | INCONCLUSIVE | median rise 1.001 [1.001, 1.001] s against 1.0 s |
| X7-H7b qdrant slow-200 failing | INCONCLUSIVE | 0.000 [0.000, 0.000] over 12 requests |
| X7-H7b qdrant slow-200 latency rise | INCONCLUSIVE | median rise 0.201 [0.201, 0.201] s against 0.2 s |
| X7-H7c qdrant truncate | INCONCLUSIVE | 1.000 [1.000, 1.000] over 127 requests |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

13 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.026 [0.026, 0.026] | n/a | {'ok': 119, 'error': 1} | psycopg.OperationalError: consuming input failed: server closed the connection unexpectedly 	This probably means the ser |
| pgvector | down | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.322 [0.322, 0.322] | n/a | {'ok': 122} |  |
| pgvector | refuse | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 0.227 [0.227, 0.227] | n/a | {'ok': 120} |  |
| pgvector | slow-1000 | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 0 | 0 | 1.045 [1.045, 1.045] | n/a | {'ok': 73} |  |
| pgvector | slow-200 | plain | 1 | 2 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.107 [0.107, 0.107] | n/a | {'ok': 123} |  |
| qdrant | blackhole | plain | 1 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 1 | 0 | 0.040 [0.040, 0.040] | n/a | {'ok': 110, 'error': 1} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 104] Connection reset by peer |
| qdrant | down | plain | 1 | 138 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 149 | 0 | 0.168 [0.168, 0.168] | 8.0e-04 | {'ok': 114, 'error': 149} | qdrant_client.http.exceptions.ResponseHandlingException: Server disconnected without sending a response.; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 104] Connection reset by peer; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | http500 | plain | 1 | 136 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 140 | 0 | 0.015 [0.015, 0.015] | 0.001 | {'ok': 111, 'error': 140} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 500 (Injected) Raw response content: b'{"error":" |
| qdrant | http503 | plain | 1 | 136 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 140 | 0 | 0.006 [0.006, 0.006] | 0.001 | {'ok': 111, 'error': 140} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 503 (Injected) Raw response content: b'{"error":" |
| qdrant | refuse | plain | 1 | 140 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 145 | 0 | 0.023 [0.023, 0.023] | 6.0e-04 | {'ok': 112, 'error': 145} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | slow-1000 | plain | 1 | 1 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.090 [0.090, 0.090] | n/a | {'ok': 114} |  |
| qdrant | slow-200 | plain | 1 | 12 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.148 [0.148, 0.148] | n/a | {'ok': 125} |  |
| qdrant | truncate | plain | 1 | 127 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 131 | 0 | 0.021 [0.021, 0.021] | 0.003 | {'ok': 111, 'error': 131} | json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 322 (char 321); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 269 (char 268); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 280 (char 279); json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 282 (char 281); json.decoder.JSONDecodeError: Unterm |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
