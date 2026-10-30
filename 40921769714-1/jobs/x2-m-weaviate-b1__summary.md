### X2 x2-m-weaviate-b1 (m, weaviate): done

| layout | build | setting | status | pairs | passes | recall@10 | empty | p50 ms | QPS |
|---|---|---|---|---|---|---|---|---|---|
| default | 1 | default | done | 6200 | 3 | 0.968 | 0.000 | 7.921 | 124.0 |
| default | 1 | ef64 | done | 6200 | 3 | 0.956 | 0.000 | 7.489 | 126.5 |
| default | 1 | ef128 | done | 6200 | 3 | 0.973 | 0.000 | 8.346 | 119.5 |
| default | 1 | ef256 | done | 6200 | 3 | 0.985 | 0.000 | 10.2 | 105.1 |
| default | 1 | ef512 | done | 6200 | 3 | 0.991 | 0.000 | 11.1 | 86.0 |
| default | 1 | ef1024 | done | 6200 | 3 | 0.994 | 0.000 | 11.9 | 69.4 |
| default | 1 | sweeping | done | 6200 | 3 | 0.995 | 0.000 | 8.233 | 92.7 |
| default | 1 | noflat | done | 6200 | 3 | 0.812 | 0.000 | 7.386 | 128.3 |

- default build 1: loaded in 715.7 s
