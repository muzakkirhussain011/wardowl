# X7: revocation and faults

Profile: ['full']. Files: 1; records: 135.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G3 leak detection (allow-all leaks) | FALSIFIED | {} |
| X7-H6 fail closed | INCONCLUSIVE | 62640 requests: 0 leaks (one-sided bound 0.000048), 0 engine failures not AuthorizationError, 0 naming a host |
| X7 store errors (reported) | EXPLORATORY | 28125 store-fault failures, 0 naming a host |
| X7-H7c pgvector blackhole | INCONCLUSIVE | n/a [n/a, n/a] over 0 requests |
| X7-H7c pgvector down | CONFIRMED | 1.000 [1.000, 1.000] over 10 requests |
| X7-H7c pgvector refuse | CONFIRMED | 1.000 [1.000, 1.000] over 10 requests |
| X7-H7b pgvector slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 19 requests |
| X7-H7b pgvector slow-1000 latency rise | CONFIRMED | median rise 4.002 [4.002, 4.002] s against 1.0 s |
| X7-H7b pgvector slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 133 requests |
| X7-H7b pgvector slow-200 latency rise | CONFIRMED | median rise 0.801 [0.801, 0.801] s against 0.2 s |
| X7-H7c qdrant blackhole | CONFIRMED | 1.000 [1.000, 1.000] over 10 requests |
| X7-H7c qdrant down | CONFIRMED | 1.000 [1.000, 1.000] over 5570 requests |
| X7-H7c qdrant http500 | CONFIRMED | 1.000 [1.000, 1.000] over 5553 requests |
| X7-H7c qdrant http503 | CONFIRMED | 1.000 [1.000, 1.000] over 5550 requests |
| X7-H7c qdrant refuse | CONFIRMED | 1.000 [1.000, 1.000] over 5683 requests |
| X7-H7b qdrant slow-1000 failing | CONFIRMED | 0.000 [0.000, 0.000] over 100 requests |
| X7-H7b qdrant slow-1000 latency rise | CONFIRMED | median rise 1.001 [1.001, 1.001] s against 1.0 s |
| X7-H7b qdrant slow-200 failing | CONFIRMED | 0.000 [0.000, 0.000] over 520 requests |
| X7-H7b qdrant slow-200 latency rise | CONFIRMED | median rise 0.201 [0.201, 0.201] s against 0.2 s |
| X7-H7c qdrant truncate | CONFIRMED | 1.000 [1.000, 1.000] over 5236 requests |

## X7a: revocation latency

| path | condition | trials | valid | median s [95% CI] | max s | p95 s | bound B s | beyond B + 1 s | never took effect | flaps | poll errors | median write s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X7b: faults

130 episodes; 0 excluded by G4 (baseline below 99% exact).

| target | fault | condition | episodes | requests inside | failing [95% CI] | succeeding [95% CI] | leaks | failures not AuthorizationError | failures naming a host | recovery s [95% CI] | median failed latency s | codes | errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | blackhole | plain | 10 | 0 | n/a [n/a, n/a] | n/a [n/a, n/a] | 0 | 5 | 0 | 0.555 [0.042, 2.880] | n/a | {'ok': 2235, 'hang': 8, 'error': 5} | psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | down | plain | 10 | 10 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 23 | 0 | 2.300 [1.963, 2.825] | 5.000 | {'ok': 2754, 'error': 23} | psycopg.OperationalError: consuming input failed: server closed the connection unexpectedly 	This probably means the ser; psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | refuse | plain | 10 | 10 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 23 | 0 | 2.617 [1.909, 3.278] | 5.000 | {'ok': 2432, 'error': 23} | psycopg.OperationalError: consuming input failed: server closed the connection unexpectedly 	This probably means the ser; psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec |
| pgvector | slow-1000 | plain | 10 | 19 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.110 [0.100, 0.115] | n/a | {'ok': 2285} |  |
| pgvector | slow-200 | plain | 10 | 133 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.168 [0.159, 0.175] | n/a | {'ok': 2887} |  |
| qdrant | blackhole | plain | 10 | 10 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 30 | 0 | 0.025 [0.025, 0.025] | 5.006 | {'ok': 2648, 'error': 30} | qdrant_client.http.exceptions.ResponseHandlingException: Server disconnected without sending a response.; qdrant_client.http.exceptions.ResponseHandlingException: timed out |
| qdrant | down | plain | 10 | 5570 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5829 | 0 | 0.287 [0.249, 0.310] | 7.0e-04 | {'ok': 2709, 'error': 5829} | qdrant_client.http.exceptions.ResponseHandlingException: Server disconnected without sending a response.; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 104] Connection reset by peer; qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | http500 | plain | 10 | 5553 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5600 | 0 | 0.013 [0.008, 0.017] | 0.001 | {'ok': 2649, 'error': 5600} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 500 (Injected) Raw response content: b'{"error":" |
| qdrant | http503 | plain | 10 | 5550 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5599 | 0 | 0.014 [0.005, 0.018] | 0.001 | {'ok': 2652, 'error': 5599} | qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 503 (Injected) Raw response content: b'{"error":" |
| qdrant | refuse | plain | 10 | 5683 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5731 | 0 | 0.013 [0.010, 0.022] | 7.0e-04 | {'ok': 2648, 'error': 5731} | qdrant_client.http.exceptions.ResponseHandlingException: [Errno 111] Connection refused |
| qdrant | slow-1000 | plain | 10 | 100 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.298 [0.293, 0.306] | n/a | {'ok': 2768} |  |
| qdrant | slow-200 | plain | 10 | 520 | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0 | 0 | 0 | 0.072 [0.067, 0.104] | n/a | {'ok': 3194} |  |
| qdrant | truncate | plain | 10 | 5236 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0 | 5285 | 0 | 0.013 [0.007, 0.020] | 0.002 | {'ok': 2646, 'error': 5285} | json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 315 (char 314); json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 319 (char 318); json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 321 (char 320); json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 322 (char 321); json.decoder.JSONDecodeError: Expecting ',' delimiter: line  |

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
