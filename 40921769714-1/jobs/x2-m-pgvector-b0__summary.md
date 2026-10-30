### X2 x2-m-pgvector-b0 (m, pgvector): done

| layout | build | setting | status | pairs | passes | recall@10 | empty | p50 ms | QPS |
|---|---|---|---|---|---|---|---|---|---|
| default | 0 | default | done | 6200 | 3 | 0.578 | 0.320 | 6.272 | 75.4 |
| default | 0 | ef40 | done | 6200 | 3 | 0.887 | 0.002 | 12.4 | 16.2 |
| default | 0 | ef100 | done | 6200 | 3 | 0.900 | 0.002 | 13.1 | 16.1 |
| default | 0 | ef200 | done | 6200 | 3 | 0.908 | 0.002 | 14.2 | 16.1 |
| default | 0 | ef400 | done | 6200 | 3 | 0.919 | 0.002 | 16.6 | 15.8 |
| default | 0 | ef1000 | done | 6200 | 3 | 0.929 | 0.001 | 24.3 | 14.9 |
| default | 0 | scan1m | done | 6200 | 3 | 0.949 | 0.000 | 13.3 | 12.9 |
| default | 0 | strict | done | 6200 | 3 | 0.881 | 0.002 | 13.0 | 16.2 |
| default | 0 | exact | done | 998 | 2 | 1.000 | 0.000 | 636.0 | 0.265 |

- default build 0: loaded in 315.6 s
