### X2 x2-e-pgvector (e, pgvector): done

| layout | build | setting | status | pairs | passes | recall@10 | empty | p50 ms | QPS |
|---|---|---|---|---|---|---|---|---|---|
| default | 0 | default | done | 1489 | 3 | 0.129 | 0.606 | 2.195 | 452.4 |
| default | 0 | ef40 | done | 1489 | 3 | 0.642 | 0.095 | 16.9 | 42.9 |
| default | 0 | ef100 | done | 1489 | 3 | 0.660 | 0.095 | 17.2 | 42.6 |
| default | 0 | ef200 | done | 1489 | 3 | 0.668 | 0.095 | 17.6 | 41.6 |
| default | 0 | ef400 | done | 1489 | 3 | 0.751 | 0.036 | 13.0 | 51.7 |
| default | 0 | ef1000 | done | 1489 | 3 | 1.000 | 0.000 | 164.1 | 7.839 |
| default | 0 | scan1m | done | 1489 | 3 | 0.784 | 0.000 | 16.9 | 25.1 |
| default | 0 | strict | done | 1489 | 3 | 0.518 | 0.095 | 17.2 | 42.3 |
| default | 0 | exact | done | 1489 | 3 | 1.000 | 0.000 | 162.6 | 7.883 |
| default | 1 | default | done | 1489 | 3 | 0.117 | 0.621 | 2.114 | 469.7 |
| default | 1 | ef40 | done | 1489 | 3 | 0.640 | 0.106 | 17.2 | 45.1 |
| default | 1 | ef100 | done | 1489 | 3 | 0.665 | 0.105 | 17.3 | 45.6 |
| default | 1 | ef200 | done | 1489 | 3 | 0.674 | 0.105 | 18.1 | 44.2 |
| default | 1 | ef400 | done | 1489 | 3 | 0.754 | 0.048 | 13.1 | 52.3 |
| default | 1 | ef1000 | done | 1489 | 3 | 1.000 | 0.000 | 170.0 | 7.810 |
| default | 1 | scan1m | done | 1489 | 3 | 0.791 | 0.000 | 18.3 | 25.3 |
| default | 1 | strict | done | 1489 | 3 | 0.503 | 0.105 | 19.2 | 41.5 |
| default | 2 | default | done | 1489 | 3 | 0.092 | 0.621 | 2.127 | 468.4 |
| default | 2 | ef40 | done | 1489 | 3 | 0.641 | 0.091 | 16.9 | 44.0 |
| default | 2 | ef100 | done | 1489 | 3 | 0.657 | 0.091 | 18.2 | 41.3 |
| default | 2 | ef200 | done | 1489 | 3 | 0.669 | 0.091 | 17.6 | 41.0 |
| default | 2 | ef400 | done | 1489 | 3 | 0.756 | 0.026 | 13.6 | 47.3 |
| default | 2 | ef1000 | done | 1489 | 3 | 1.000 | 0.000 | 174.9 | 7.548 |
| default | 2 | scan1m | done | 1489 | 3 | 0.784 | 0.000 | 19.0 | 22.7 |
| default | 2 | strict | done | 1489 | 3 | 0.491 | 0.091 | 21.9 | 34.8 |

- default build 0: loaded in 31.6 s
- default build 1: loaded in 30.5 s
- default build 2: loaded in 27.5 s
