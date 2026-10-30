### X2 x2-m-pgvector-b2 (m, pgvector): done

| layout | build | setting | status | pairs | passes | recall@10 | empty | p50 ms | QPS |
|---|---|---|---|---|---|---|---|---|---|
| default | 2 | default | done | 6200 | 3 | 0.584 | 0.317 | 6.347 | 66.8 |
| default | 2 | ef40 | done | 6200 | 3 | 0.889 | 0.003 | 12.5 | 15.8 |
| default | 2 | ef100 | done | 6200 | 3 | 0.900 | 0.003 | 13.4 | 15.7 |
| default | 2 | ef200 | done | 6200 | 3 | 0.910 | 0.003 | 14.7 | 15.7 |
| default | 2 | ef400 | done | 6200 | 3 | 0.921 | 0.003 | 17.4 | 15.5 |
| default | 2 | ef1000 | done | 6200 | 3 | 0.930 | 0.003 | 25.6 | 14.5 |
| default | 2 | scan1m | done | 6200 | 3 | 0.949 | 0.000 | 13.8 | 12.2 |
| default | 2 | strict | done | 6200 | 3 | 0.882 | 0.003 | 13.3 | 15.8 |

- default build 2: loaded in 316.6 s
