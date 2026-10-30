### X2 x2-m-weaviate-b2 (m, weaviate): done

| layout | build | setting | status | pairs | passes | recall@10 | empty | p50 ms | QPS |
|---|---|---|---|---|---|---|---|---|---|
| default | 2 | default | done | 6200 | 3 | 0.968 | 0.000 | 6.048 | 153.9 |
| default | 2 | ef64 | done | 6200 | 3 | 0.955 | 0.000 | 5.754 | 155.6 |
| default | 2 | ef128 | done | 6200 | 3 | 0.973 | 0.000 | 7.069 | 136.2 |
| default | 2 | ef256 | done | 6200 | 3 | 0.985 | 0.000 | 8.393 | 124.8 |
| default | 2 | ef512 | done | 6200 | 3 | 0.991 | 0.000 | 9.376 | 106.8 |
| default | 2 | ef1024 | done | 6200 | 3 | 0.994 | 0.000 | 9.780 | 85.0 |
| default | 2 | sweeping | done | 6200 | 3 | 0.995 | 0.000 | 6.184 | 114.1 |
| default | 2 | noflat | done | 6200 | 3 | 0.812 | 0.000 | 5.564 | 172.0 |

- default build 2: loaded in 628.6 s
