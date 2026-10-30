### X2 x2-m-pgvector-b1 (m, pgvector): done

| layout | build | setting | status | pairs | passes | recall@10 | empty | p50 ms | QPS |
|---|---|---|---|---|---|---|---|---|---|
| default | 1 | default | done | 6200 | 3 | 0.565 | 0.335 | 4.852 | 117.2 |
| default | 1 | ef40 | done | 6200 | 3 | 0.878 | 0.005 | 9.832 | 20.7 |
| default | 1 | ef100 | done | 6200 | 3 | 0.891 | 0.005 | 10.5 | 20.3 |
| default | 1 | ef200 | done | 6200 | 3 | 0.901 | 0.005 | 11.7 | 20.2 |
| default | 1 | ef400 | done | 6200 | 3 | 0.911 | 0.005 | 13.7 | 19.9 |
| default | 1 | ef1000 | done | 6200 | 3 | 0.921 | 0.004 | 21.0 | 17.8 |
| default | 1 | scan1m | done | 6200 | 3 | 0.949 | 0.000 | 10.6 | 15.0 |
| default | 1 | strict | done | 6200 | 3 | 0.872 | 0.005 | 10.5 | 20.5 |

- default build 1: loaded in 315.4 s
