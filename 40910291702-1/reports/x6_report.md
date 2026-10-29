# X6: side channels of permission-aware retrieval

554 records (0 unreadable lines), 200 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md. AUC 0.5 means no advantage; the paired AUC is the differencing attacker's.

## Health

| store | mode | seeds done | skipped | retrievals | errors | stopped | build s | setup error | leaks |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | smoke | [0] | [] | 168 | {} | [] | {"w0": 4.0, "w1": 3.7, "sep": 2.0} | n/a | 0 |
| faiss | smoke | [0] | [] | 72 | {} | [] | {"w0": 0.1, "w1": 0.0, "sep": 0.0} | n/a | 0 |
| memory | smoke | [0] | [] | 16 | {} | [] | {"w0": 0.0, "w1": 0.0, "sep": 0.0} | n/a | 0 |
| pgvector | smoke | [0] | [] | 120 | {} | [] | {"w0": 5.0, "w1": 4.7, "sep": 3.8} | n/a | 0 |
| qdrant | smoke | [0] | [] | 120 | {} | [] | {"w0": 13.0, "w1": 11.9, "sep": 11.0} | n/a | 0 |

## Verdicts

| hypothesis | scope | outcome | evidence |
|---|---|---|---|
| H1 | vector stores | inconclusive | 0 confirmed, 0 falsified, 40 inconclusive parts |
| H2 | vector stores | inconclusive | 0 confirmed, 0 falsified, 16 inconclusive parts |
| H3a | pgvector | inconclusive | 0 confirmed, 0 falsified, 3 inconclusive parts |
| H3b | elasticsearch | inconclusive | 0 confirmed, 0 falsified, 2 inconclusive parts |
| H3c | qdrant | inconclusive | 0 confirmed, 0 falsified, 5 inconclusive parts |
| H4 | pgvector pre-exact | inconclusive | 0 confirmed, 0 falsified, 10 inconclusive parts |
| H4 | qdrant pre-exact | inconclusive | 0 confirmed, 0 falsified, 10 inconclusive parts |
| H4 | elasticsearch pre-exact | inconclusive | 0 confirmed, 0 falsified, 10 inconclusive parts |
| H4 | faiss pre | inconclusive | 0 confirmed, 0 falsified, 10 inconclusive parts |
| H4 | memory pre | inconclusive | 0 confirmed, 0 falsified, 8 inconclusive parts |
| H5a | elasticsearch | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| H5a | qdrant | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| H5b | pgvector | inconclusive | 0 confirmed, 0 falsified, 2 inconclusive parts |
| H5c | elasticsearch | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| H6 | every cell with a raw latency channel | inconclusive | 0 confirmed, 0 falsified, 0 inconclusive parts |

## Guards

| guard | store | config | passed | evidence |
|---|---|---|---|---|
| G1 | elasticsearch | bm25-pre | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G1 | elasticsearch | hybrid-exact | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | elasticsearch | hybrid-pre | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | elasticsearch | post | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G1 | elasticsearch | post-const | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G1 | elasticsearch | pre | n/a | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| G1 | elasticsearch | pre-exact | n/a | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| G1 | faiss | post | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | faiss | post-const | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | faiss | pre | n/a | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| G1 | memory | post | n/a | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| G1 | memory | pre | n/a | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| G1 | pgvector | bm25-pre | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | pgvector | post | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G1 | pgvector | post-const | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | pgvector | pre | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G1 | pgvector | pre-exact | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | qdrant | bm25-pre | n/a | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| G1 | qdrant | post | n/a | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| G1 | qdrant | post-const | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G1 | qdrant | pre | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G1 | qdrant | pre-exact | n/a | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| G2 | elasticsearch | pre-exact | True | pre-exact: change rate 0.0000 |
| G2 | faiss | pre | True | pre: change rate 0.0000 |
| G2 | pgvector | pre-exact | True | pre-exact: change rate 0.0000 |
| G2 | qdrant | pre-exact | True | pre-exact: change rate 0.0000 |

## Paired AUC (W1 against W0), pooled over selectivity

| store | config | m | latency | count | complete | recall | score | A/A latency |
|---|---|---|---|---|---|---|---|---|
| elasticsearch | bm25-pre | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] |
| elasticsearch | bm25-pre | all | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] |
| elasticsearch | hybrid-exact | 1000 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.33 [0.33, 0.33] | 0.33 [0.33, 0.33] |
| elasticsearch | hybrid-exact | all | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.33 [0.33, 0.33] | 0.33 [0.33, 0.33] |
| elasticsearch | hybrid-pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.33 [0.33, 0.33] | 0.33 [0.33, 0.33] |
| elasticsearch | hybrid-pre | all | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.33 [0.33, 0.33] | 0.33 [0.33, 0.33] |
| elasticsearch | post | 1000 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] |
| elasticsearch | post | all | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] |
| elasticsearch | post-const | 1000 | 0.33 [0.33, 0.33] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] |
| elasticsearch | post-const | all | 0.33 [0.33, 0.33] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] |
| elasticsearch | pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| elasticsearch | pre | all | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| elasticsearch | pre-exact | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| elasticsearch | pre-exact | all | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| faiss | post | 1000 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| faiss | post | all | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| faiss | post-const | 1000 | 0.33 [0.33, 0.33] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| faiss | post-const | all | 0.33 [0.33, 0.33] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| faiss | pre | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| faiss | pre | all | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| memory | post | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| memory | post | all | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| memory | pre | 1000 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| memory | pre | all | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| pgvector | bm25-pre | 1000 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| pgvector | bm25-pre | all | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| pgvector | post | 1000 | 0.67 [0.67, 0.67] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] |
| pgvector | post | all | 0.67 [0.67, 0.67] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] |
| pgvector | post-const | 1000 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| pgvector | post-const | all | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| pgvector | pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.17 [0.17, 0.17] | 0.17 [0.17, 0.17] | 0.67 [0.67, 0.67] |
| pgvector | pre | all | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.17 [0.17, 0.17] | 0.17 [0.17, 0.17] | 0.67 [0.67, 0.67] |
| pgvector | pre-exact | 1000 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| pgvector | pre-exact | all | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| qdrant | bm25-pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| qdrant | bm25-pre | all | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| qdrant | post | 1000 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| qdrant | post | all | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| qdrant | post-const | 1000 | 0.33 [0.33, 0.33] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] |
| qdrant | post-const | all | 0.33 [0.33, 0.33] | 1.00 [1.00, 1.00] | 0.83 [0.83, 0.83] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] |
| qdrant | pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |
| qdrant | pre | all | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |
| qdrant | pre-exact | 1000 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |
| qdrant | pre-exact | all | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |

## Mitigation costs (latency, ratio of means)

| store | mitigation | ratio | interval | median ratio | pairs |
|---|---|---|---|---|---|
| elasticsearch | M1/M2 post-const / post | 0.498 | [0.50, 0.50] | 0.437 | 6 |
| elasticsearch | M1/M2 pre-exact / pre | 0.917 | [0.92, 0.92] | 0.856 | 6 |
| elasticsearch | M3 separated / shared (bm25-pre) | 1.216 | [1.22, 1.22] | 1.303 | 3 |
| elasticsearch | M3 separated / shared (hybrid-exact) | 0.825 | [0.82, 0.82] | 0.764 | 3 |
| elasticsearch | M3 separated / shared (hybrid-pre) | 0.892 | [0.89, 0.89] | 0.807 | 3 |
| elasticsearch | M3 separated / shared (post) | 0.941 | [0.94, 0.94] | 0.966 | 3 |
| elasticsearch | M3 separated / shared (post-const) | 0.921 | [0.92, 0.92] | 0.942 | 3 |
| elasticsearch | M3 separated / shared (pre) | 1.294 | [1.29, 1.29] | 1.274 | 3 |
| elasticsearch | M3 separated / shared (pre-exact) | 1.099 | [1.10, 1.10] | 1.066 | 3 |
| faiss | M1/M2 post-const / post | 0.711 | [0.71, 0.71] | 0.637 | 6 |
| faiss | M3 separated / shared (post) | 1.797 | [1.80, 1.80] | 0.646 | 3 |
| faiss | M3 separated / shared (post-const) | 0.914 | [0.91, 0.91] | 0.909 | 3 |
| faiss | M3 separated / shared (pre) | 0.907 | [0.91, 0.91] | 0.907 | 3 |
| memory | M3 separated / shared (post) | 0.805 | [0.80, 0.80] | 0.805 | 1 |
| memory | M3 separated / shared (pre) | 0.810 | [0.81, 0.81] | 0.810 | 1 |
| pgvector | M1/M2 post-const / post | 0.702 | [0.70, 0.70] | 0.490 | 6 |
| pgvector | M1/M2 pre-exact / pre | 3.893 | [3.89, 3.89] | 2.560 | 6 |
| pgvector | M3 separated / shared (bm25-pre) | 1.014 | [1.01, 1.01] | 1.010 | 3 |
| pgvector | M3 separated / shared (post) | 0.864 | [0.86, 0.86] | 0.883 | 3 |
| pgvector | M3 separated / shared (post-const) | 0.926 | [0.93, 0.93] | 0.931 | 3 |
| pgvector | M3 separated / shared (pre) | 0.931 | [0.93, 0.93] | 0.912 | 3 |
| pgvector | M3 separated / shared (pre-exact) | 0.822 | [0.82, 0.82] | 0.834 | 3 |
| qdrant | M1/M2 post-const / post | 0.691 | [0.69, 0.69] | 0.504 | 6 |
| qdrant | M1/M2 pre-exact / pre | 0.964 | [0.96, 0.96] | 0.962 | 6 |
| qdrant | M3 separated / shared (bm25-pre) | 0.979 | [0.98, 0.98] | 0.998 | 3 |
| qdrant | M3 separated / shared (post) | 0.954 | [0.95, 0.95] | 0.972 | 3 |
| qdrant | M3 separated / shared (post-const) | 0.994 | [0.99, 0.99] | 0.993 | 3 |
| qdrant | M3 separated / shared (pre) | 1.016 | [1.02, 1.02] | 1.002 | 3 |
| qdrant | M3 separated / shared (pre-exact) | 0.984 | [0.98, 0.98] | 0.984 | 3 |

## Id-list change rate, W1 against W0 (deterministic configurations)

| store | config | m | rate | interval | A/A rate | pairs |
|---|---|---|---|---|---|---|
| elasticsearch | bm25-pre | all | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| elasticsearch | bm25-pre | 1000 | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| elasticsearch | hybrid-exact | all | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| elasticsearch | hybrid-exact | 1000 | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| elasticsearch | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| elasticsearch | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| faiss | pre | all | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| faiss | pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| memory | pre | all | 0.000 | [0.00, 0.00] | 0.000 | 1 |
| memory | pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 1 |
| pgvector | bm25-pre | all | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| pgvector | bm25-pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| pgvector | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| pgvector | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| qdrant | bm25-pre | all | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| qdrant | bm25-pre | 1000 | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| qdrant | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| qdrant | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |

## Every verdict part

| hypothesis | store | config | part | outcome | evidence |
|---|---|---|---|---|---|
| H1 | faiss | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | faiss | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | faiss | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | faiss | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | missing |
| H1 | faiss | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | missing |
| H1 | faiss | post | (c) m=1 no channel in latency | inconclusive | missing |
| H1 | faiss | post | (c) m=1 no channel in count | inconclusive | missing |
| H1 | faiss | post | (c) m=1 no channel in complete | inconclusive | missing |
| H1 | faiss | post | (c) m=1 no channel in recall | inconclusive | missing |
| H1 | faiss | post | (c) m=1 no channel in score | inconclusive | missing |
| H1 | pgvector | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | pgvector | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | pgvector | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | pgvector | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | missing |
| H1 | pgvector | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | missing |
| H1 | pgvector | post | (c) m=1 no channel in latency | inconclusive | missing |
| H1 | pgvector | post | (c) m=1 no channel in count | inconclusive | missing |
| H1 | pgvector | post | (c) m=1 no channel in complete | inconclusive | missing |
| H1 | pgvector | post | (c) m=1 no channel in recall | inconclusive | missing |
| H1 | pgvector | post | (c) m=1 no channel in score | inconclusive | missing |
| H1 | qdrant | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | qdrant | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | qdrant | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | qdrant | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | missing |
| H1 | qdrant | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | missing |
| H1 | qdrant | post | (c) m=1 no channel in latency | inconclusive | missing |
| H1 | qdrant | post | (c) m=1 no channel in count | inconclusive | missing |
| H1 | qdrant | post | (c) m=1 no channel in complete | inconclusive | missing |
| H1 | qdrant | post | (c) m=1 no channel in recall | inconclusive | missing |
| H1 | qdrant | post | (c) m=1 no channel in score | inconclusive | missing |
| H1 | elasticsearch | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | elasticsearch | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | missing |
| H1 | elasticsearch | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | missing |
| H1 | elasticsearch | post | (c) m=1 no channel in latency | inconclusive | missing |
| H1 | elasticsearch | post | (c) m=1 no channel in count | inconclusive | missing |
| H1 | elasticsearch | post | (c) m=1 no channel in complete | inconclusive | missing |
| H1 | elasticsearch | post | (c) m=1 no channel in recall | inconclusive | missing |
| H1 | elasticsearch | post | (c) m=1 no channel in score | inconclusive | missing |
| H2 | faiss | post-const | (a) no latency channel pooled | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | faiss | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | faiss | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | faiss | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | pgvector | post-const | (a) no latency channel pooled | inconclusive | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| H2 | pgvector | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| H2 | pgvector | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | pgvector | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | qdrant | post-const | (a) no latency channel pooled | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | qdrant | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | qdrant | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | qdrant | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (a) no latency channel pooled | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3a | pgvector | pre | m=1000 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3a | pgvector | pre | m=1000 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3a | pgvector | pre | m=100 p=50 latency >= 0.75 | inconclusive | missing |
| H3b | elasticsearch | pre | m=1000 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3b | elasticsearch | pre | m=1000 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in latency | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in count | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in complete | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in recall | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in score | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in latency pooled | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in latency pooled | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in latency pooled | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in latency pooled | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 latency upper <= 0.65 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in latency pooled | inconclusive | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 latency upper <= 0.65 | inconclusive | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H5a | elasticsearch | bm25-pre | m=1000 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H5a | qdrant | bm25-pre | m=1000 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H5b | pgvector | bm25-pre | no channel in the score | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H5b | pgvector | bm25-pre | id-list change rate <= 0.01 | inconclusive | change rate 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| H5c | elasticsearch | hybrid-exact | m=1000 change rate >= 0.25 | inconclusive | change rate 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |

