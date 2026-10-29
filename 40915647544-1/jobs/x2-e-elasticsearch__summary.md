### X2 x2-e-elasticsearch (e, elasticsearch): done

| layout | build | setting | status | pairs | passes | recall@10 | empty | p50 ms | QPS |
|---|---|---|---|---|---|---|---|---|---|
| default | 0 | default | done | 169 | 3 | 0.978 | 0.000 | 7.647 | 130.6 |
| default | 0 | nc50 | done | 169 | 3 | 0.978 | 0.000 | 4.915 | 205.1 |
| default | 0 | nc100 | done | 169 | 3 | 0.978 | 0.000 | 3.888 | 250.8 |
| default | 0 | nc500 | done | 169 | 3 | 0.978 | 0.000 | 3.297 | 305.2 |
| default | 0 | nc2000 | done | 169 | 3 | 0.978 | 0.000 | 3.374 | 304.0 |
| default | 0 | nc10000 | done | 169 | 3 | 0.978 | 0.000 | 3.295 | 309.2 |
| default | 0 | exact | done | 169 | 3 | 1.000 | 0.000 | 3.653 | 278.2 |
| int8 | 0 | default | done | 169 | 3 | 0.949 | 0.000 | 3.766 | 264.6 |
| int8 | 0 | nc50 | done | 169 | 3 | 0.959 | 0.000 | 3.083 | 325.4 |
| int8 | 0 | nc100 | done | 169 | 3 | 0.982 | 0.000 | 3.072 | 332.5 |
| int8 | 0 | nc500 | done | 169 | 3 | 0.993 | 0.000 | 3.038 | 330.0 |
| int8 | 0 | nc2000 | done | 169 | 3 | 0.993 | 0.000 | 2.864 | 364.5 |
| int8 | 0 | nc10000 | done | 169 | 3 | 0.993 | 0.000 | 3.053 | 340.3 |
| int8 | 0 | exact | done | 169 | 3 | 1.000 | 0.000 | 2.908 | 362.2 |

- default build 0: loaded in 4.5 s
- int8 build 0: loaded in 3.7 s
