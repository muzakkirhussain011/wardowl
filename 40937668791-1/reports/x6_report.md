# X6: side channels of permission-aware retrieval

4,496 records (0 unreadable lines), 200 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md. AUC 0.5 means no advantage; the paired AUC is the differencing attacker's.

## Health

| store | mode | seeds done | skipped | retrievals | errors | stopped | build s | setup error | leaks |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | smoke | [0] | [] | 1512 | {} | [] | {"w1": 36.6, "sep": 26.8, "w0": 30.7} | n/a | 0 |
| faiss | smoke | [0] | [] | 648 | {} | [] | {"w1": 0.6, "sep": 0.5, "w0": 0.5} | n/a | 0 |
| memory | smoke | [0] | [] | 64 | {} | [] | {"w1": 0.3, "sep": 0.3, "w0": 0.3} | n/a | 0 |
| pgvector | smoke | [0] | [] | 1080 | {} | [] | {"w1": 37.3, "sep": 32.0, "w0": 37.7} | n/a | 0 |
| qdrant | smoke | [0] | [] | 1080 | {} | [] | {"w1": 61.0, "sep": 47.9, "w0": 58.0} | n/a | 0 |

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
| H5a | elasticsearch | inconclusive | 0 confirmed, 0 falsified, 4 inconclusive parts |
| H5a | qdrant | inconclusive | 0 confirmed, 0 falsified, 4 inconclusive parts |
| H5b | pgvector | inconclusive | 0 confirmed, 0 falsified, 2 inconclusive parts |
| H5c | elasticsearch | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| H6 | every cell with a raw latency channel | inconclusive | 0 confirmed, 0 falsified, 0 inconclusive parts |

## Guards

| guard | store | config | passed | evidence |
|---|---|---|---|---|
| G1 | elasticsearch | bm25-pre | n/a | 0.519 [0.333, 0.704] (9 clusters, 1 seeds) |
| G1 | elasticsearch | hybrid-exact | n/a | 0.481 [0.370, 0.556] (9 clusters, 1 seeds) |
| G1 | elasticsearch | hybrid-pre | n/a | 0.519 [0.333, 0.704] (9 clusters, 1 seeds) |
| G1 | elasticsearch | post | n/a | 0.481 [0.259, 0.705] (9 clusters, 1 seeds) |
| G1 | elasticsearch | post-const | n/a | 0.556 [0.406, 0.741] (9 clusters, 1 seeds) |
| G1 | elasticsearch | pre | n/a | 0.444 [0.370, 0.556] (9 clusters, 1 seeds) |
| G1 | elasticsearch | pre-exact | n/a | 0.556 [0.258, 0.815] (9 clusters, 1 seeds) |
| G1 | faiss | post | n/a | 0.444 [0.333, 0.593] (9 clusters, 1 seeds) |
| G1 | faiss | post-const | n/a | 0.556 [0.407, 0.704] (9 clusters, 1 seeds) |
| G1 | faiss | pre | n/a | 0.519 [0.333, 0.741] (9 clusters, 1 seeds) |
| G1 | memory | post | n/a | 0.000 [0.000, 0.000] (4 clusters, 1 seeds) |
| G1 | memory | pre | n/a | 1.000 [1.000, 1.000] (4 clusters, 1 seeds) |
| G1 | pgvector | bm25-pre | n/a | 0.481 [0.370, 0.667] (9 clusters, 1 seeds) |
| G1 | pgvector | post | n/a | 0.407 [0.333, 0.519] (9 clusters, 1 seeds) |
| G1 | pgvector | post-const | n/a | 0.593 [0.407, 0.815] (9 clusters, 1 seeds) |
| G1 | pgvector | pre | n/a | 0.370 [0.222, 0.519] (9 clusters, 1 seeds) |
| G1 | pgvector | pre-exact | n/a | 0.556 [0.370, 0.741] (9 clusters, 1 seeds) |
| G1 | qdrant | bm25-pre | n/a | 0.519 [0.370, 0.631] (9 clusters, 1 seeds) |
| G1 | qdrant | post | n/a | 0.556 [0.370, 0.741] (9 clusters, 1 seeds) |
| G1 | qdrant | post-const | n/a | 0.407 [0.259, 0.593] (9 clusters, 1 seeds) |
| G1 | qdrant | pre | n/a | 0.556 [0.407, 0.704] (9 clusters, 1 seeds) |
| G1 | qdrant | pre-exact | n/a | 0.556 [0.332, 0.778] (9 clusters, 1 seeds) |
| G2 | elasticsearch | pre-exact | True | pre-exact: change rate 0.0000 |
| G2 | faiss | pre | True | pre: change rate 0.0000 |
| G2 | pgvector | pre-exact | True | pre-exact: change rate 0.0000 |
| G2 | qdrant | pre-exact | True | pre-exact: change rate 0.0000 |

## Paired AUC (W1 against W0), pooled over selectivity

| store | config | m | latency | count | complete | recall | score | A/A latency |
|---|---|---|---|---|---|---|---|---|
| elasticsearch | bm25-pre | 1 | 0.56 [0.44, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.56 [0.33, 0.67] |
| elasticsearch | bm25-pre | 10 | 0.89 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.78 [0.33, 1.00] | 0.67 [0.44, 1.00] |
| elasticsearch | bm25-pre | 100 | 0.67 [0.33, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.50 [0.33, 0.67] |
| elasticsearch | bm25-pre | 1000 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| elasticsearch | bm25-pre | all | 0.67 [0.48, 0.85] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.93 [0.78, 1.00] | 0.52 [0.33, 0.70] |
| elasticsearch | hybrid-exact | 1 | 0.67 [0.33, 0.89] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.44 [0.33, 0.67] |
| elasticsearch | hybrid-exact | 10 | 0.67 [0.33, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.44 [0.33, 0.67] |
| elasticsearch | hybrid-exact | 100 | 0.67 [0.33, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.50 [0.33, 0.67] |
| elasticsearch | hybrid-exact | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |
| elasticsearch | hybrid-exact | all | 0.67 [0.44, 0.89] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.48 [0.37, 0.56] |
| elasticsearch | hybrid-pre | 1 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.56 [0.50, 0.67] | 0.67 [0.44, 0.89] |
| elasticsearch | hybrid-pre | 10 | 0.78 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.56 [0.33, 0.67] |
| elasticsearch | hybrid-pre | 100 | 0.50 [0.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.58 [0.50, 0.67] | 0.33 [0.00, 0.67] |
| elasticsearch | hybrid-pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| elasticsearch | hybrid-pre | all | 0.67 [0.48, 0.82] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.54 [0.50, 0.57] | 0.52 [0.33, 0.70] |
| elasticsearch | post | 1 | 0.89 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.17, 0.61] | 0.56 [0.33, 0.78] |
| elasticsearch | post | 10 | 0.56 [0.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.56 [0.50, 0.61] | 0.50 [0.33, 0.61] | 0.67 [0.67, 0.67] |
| elasticsearch | post | 100 | 1.00 [1.00, 1.00] | 0.58 [0.50, 0.67] | 0.50 [0.50, 0.50] | 0.25 [0.17, 0.33] | 0.08 [0.00, 0.17] | 0.33 [0.00, 0.67] |
| elasticsearch | post | 1000 | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] | 0.33 [0.33, 0.33] | 0.00 [0.00, 0.00] |
| elasticsearch | post | all | 0.78 [0.52, 0.96] | 0.56 [0.50, 0.63] | 0.52 [0.50, 0.57] | 0.48 [0.39, 0.56] | 0.37 [0.22, 0.50] | 0.48 [0.26, 0.70] |
| elasticsearch | post-const | 1 | 0.44 [0.11, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.33, 0.50] | 0.56 [0.33, 0.67] |
| elasticsearch | post-const | 10 | 0.56 [0.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.00, 0.67] |
| elasticsearch | post-const | 100 | 0.83 [0.67, 1.00] | 0.58 [0.50, 0.67] | 0.50 [0.50, 0.50] | 0.58 [0.50, 0.67] | 0.42 [0.33, 0.50] | 0.67 [0.67, 0.67] |
| elasticsearch | post-const | 1000 | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| elasticsearch | post-const | all | 0.59 [0.33, 0.85] | 0.56 [0.50, 0.61] | 0.52 [0.50, 0.56] | 0.56 [0.50, 0.63] | 0.46 [0.43, 0.50] | 0.56 [0.41, 0.74] |
| elasticsearch | pre | 1 | 0.78 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.39 [0.33, 0.45] | 0.28 [0.22, 0.33] | 0.44 [0.33, 0.67] |
| elasticsearch | pre | 10 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.33, 0.50] | 0.44 [0.00, 0.67] | 0.56 [0.44, 0.67] |
| elasticsearch | pre | 100 | 0.50 [0.33, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.17, 0.50] | 0.42 [0.17, 0.67] | 0.33 [0.33, 0.33] |
| elasticsearch | pre | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] | 0.33 [0.33, 0.33] |
| elasticsearch | pre | all | 0.70 [0.59, 0.81] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.41 [0.33, 0.48] | 0.37 [0.22, 0.52] | 0.44 [0.37, 0.56] |
| elasticsearch | pre-exact | 1 | 0.67 [0.44, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.11 [0.00, 0.23] |
| elasticsearch | pre-exact | 10 | 0.56 [0.33, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.89 [0.78, 1.00] |
| elasticsearch | pre-exact | 100 | 0.83 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.33, 1.00] |
| elasticsearch | pre-exact | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |
| elasticsearch | pre-exact | all | 0.67 [0.52, 0.81] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.56 [0.26, 0.81] |
| faiss | post | 1 | 0.44 [0.33, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| faiss | post | 10 | 0.44 [0.33, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.33, 0.89] |
| faiss | post | 100 | 0.83 [0.67, 1.00] | 0.58 [0.50, 0.67] | 0.50 [0.50, 0.50] | 0.58 [0.50, 0.67] | 0.42 [0.33, 0.50] | 0.33 [0.33, 0.33] |
| faiss | post | 1000 | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.83 [0.83, 0.83] | 0.83 [0.83, 0.83] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| faiss | post | all | 0.56 [0.41, 0.70] | 0.56 [0.50, 0.65] | 0.54 [0.50, 0.61] | 0.56 [0.50, 0.63] | 0.48 [0.44, 0.50] | 0.44 [0.33, 0.59] |
| faiss | post-const | 1 | 0.44 [0.33, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| faiss | post-const | 10 | 0.67 [0.33, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.89 [0.67, 1.00] |
| faiss | post-const | 100 | 0.33 [0.33, 0.33] | 0.58 [0.50, 0.67] | 0.50 [0.50, 0.50] | 0.58 [0.50, 0.67] | 0.42 [0.33, 0.50] | 0.50 [0.33, 0.67] |
| faiss | post-const | 1000 | 0.33 [0.33, 0.33] | 0.83 [0.83, 0.83] | 0.83 [0.83, 0.83] | 0.83 [0.83, 0.83] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| faiss | post-const | all | 0.48 [0.37, 0.63] | 0.56 [0.50, 0.65] | 0.54 [0.50, 0.61] | 0.56 [0.50, 0.63] | 0.48 [0.44, 0.50] | 0.56 [0.41, 0.70] |
| faiss | pre | 1 | 0.44 [0.33, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.78 [0.67, 1.00] |
| faiss | pre | 10 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| faiss | pre | 100 | 0.83 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.33, 1.00] |
| faiss | pre | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| faiss | pre | all | 0.56 [0.41, 0.74] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.52 [0.33, 0.74] |
| memory | post | 1 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| memory | post | 10 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| memory | post | 100 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| memory | post | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| memory | post | all | 0.25 [0.00, 0.75] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] |
| memory | pre | 1 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| memory | pre | 10 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| memory | pre | 100 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| memory | pre | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| memory | pre | all | 0.75 [0.25, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| pgvector | bm25-pre | 1 | 0.78 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.67 [0.33, 1.00] |
| pgvector | bm25-pre | 10 | 0.22 [0.00, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| pgvector | bm25-pre | 100 | 0.67 [0.33, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.50 [0.33, 0.67] |
| pgvector | bm25-pre | 1000 | 1.00 [1.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| pgvector | bm25-pre | all | 0.59 [0.37, 0.81] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.48 [0.37, 0.67] |
| pgvector | post | 1 | 0.44 [0.33, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.33, 0.67] |
| pgvector | post | 10 | 0.22 [0.00, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| pgvector | post | 100 | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.58 [0.50, 0.67] | 0.17 [0.17, 0.17] | 0.50 [0.33, 0.67] |
| pgvector | post | 1000 | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] | 0.33 [0.33, 0.33] | 0.33 [0.33, 0.33] |
| pgvector | post | all | 0.44 [0.30, 0.59] | 0.57 [0.52, 0.67] | 0.52 [0.50, 0.56] | 0.54 [0.50, 0.57] | 0.41 [0.31, 0.50] | 0.41 [0.33, 0.52] |
| pgvector | post-const | 1 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.00, 0.78] |
| pgvector | post-const | 10 | 0.33 [0.00, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.33, 1.00] |
| pgvector | post-const | 100 | 0.00 [0.00, 0.00] | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] | 0.33 [0.33, 0.33] | 0.50 [0.33, 0.67] |
| pgvector | post-const | 1000 | 0.00 [0.00, 0.00] | 0.83 [0.83, 0.83] | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| pgvector | post-const | all | 0.33 [0.15, 0.52] | 0.57 [0.52, 0.67] | 0.52 [0.50, 0.56] | 0.57 [0.50, 0.65] | 0.46 [0.43, 0.50] | 0.59 [0.41, 0.81] |
| pgvector | pre | 1 | 0.11 [0.00, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.33, 0.67] |
| pgvector | pre | 10 | 0.22 [0.00, 0.44] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.00, 0.67] |
| pgvector | pre | 100 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.42 [0.33, 0.50] | 0.33 [0.33, 0.33] | 0.33 [0.00, 0.67] |
| pgvector | pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.33 [0.33, 0.33] |
| pgvector | pre | all | 0.33 [0.15, 0.59] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.43 [0.30, 0.50] | 0.41 [0.30, 0.48] | 0.37 [0.22, 0.52] |
| pgvector | pre-exact | 1 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.33, 1.00] |
| pgvector | pre-exact | 10 | 0.22 [0.00, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.33, 0.67] |
| pgvector | pre-exact | 100 | 0.33 [0.00, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.33, 1.00] |
| pgvector | pre-exact | 1000 | 0.00 [0.00, 0.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| pgvector | pre-exact | all | 0.15 [0.00, 0.37] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.56 [0.37, 0.74] |
| qdrant | bm25-pre | 1 | 0.22 [0.00, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.56 [0.33, 0.78] |
| qdrant | bm25-pre | 10 | 0.67 [0.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.78 [0.55, 1.00] | 0.56 [0.33, 0.67] |
| qdrant | bm25-pre | 100 | 0.50 [0.33, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.33 [0.33, 0.33] |
| qdrant | bm25-pre | 1000 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] |
| qdrant | bm25-pre | all | 0.44 [0.22, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.93 [0.78, 1.00] | 0.52 [0.37, 0.63] |
| qdrant | post | 1 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.00, 0.67] |
| qdrant | post | 10 | 0.22 [0.00, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |
| qdrant | post | 100 | 1.00 [1.00, 1.00] | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.58 [0.50, 0.67] | 0.25 [0.17, 0.33] | 0.67 [0.33, 1.00] |
| qdrant | post | 1000 | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] | 0.33 [0.33, 0.33] | 0.67 [0.67, 0.67] |
| qdrant | post | all | 0.59 [0.41, 0.81] | 0.57 [0.50, 0.65] | 0.52 [0.50, 0.56] | 0.54 [0.50, 0.57] | 0.43 [0.35, 0.48] | 0.56 [0.37, 0.74] |
| qdrant | post-const | 1 | 0.44 [0.33, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.56 [0.33, 1.00] |
| qdrant | post-const | 10 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.22 [0.00, 0.33] |
| qdrant | post-const | 100 | 0.33 [0.00, 0.67] | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] | 0.33 [0.33, 0.33] | 0.50 [0.33, 0.67] |
| qdrant | post-const | 1000 | 0.33 [0.33, 0.33] | 0.83 [0.83, 0.83] | 0.67 [0.67, 0.67] | 0.83 [0.83, 0.83] | 0.50 [0.50, 0.50] | 0.33 [0.33, 0.33] |
| qdrant | post-const | all | 0.37 [0.22, 0.48] | 0.57 [0.52, 0.65] | 0.52 [0.50, 0.56] | 0.57 [0.52, 0.65] | 0.46 [0.43, 0.50] | 0.41 [0.26, 0.59] |
| qdrant | pre | 1 | 0.89 [0.67, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.44, 1.00] |
| qdrant | pre | 10 | 0.67 [0.44, 0.89] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.56 [0.33, 0.67] |
| qdrant | pre | 100 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.58 [0.50, 0.67] | 0.67 [0.67, 0.67] | 0.33 [0.33, 0.33] |
| qdrant | pre | 1000 | 0.67 [0.67, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] | 0.67 [0.67, 0.67] |
| qdrant | pre | all | 0.74 [0.59, 0.89] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.52 [0.50, 0.56] | 0.56 [0.50, 0.61] | 0.56 [0.41, 0.70] |
| qdrant | pre-exact | 1 | 0.44 [0.00, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.33 [0.11, 0.67] |
| qdrant | pre-exact | 10 | 0.44 [0.11, 1.00] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.44 [0.00, 0.67] |
| qdrant | pre-exact | 100 | 0.50 [0.33, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 1.00 [1.00, 1.00] |
| qdrant | pre-exact | 1000 | 0.33 [0.33, 0.33] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.67 [0.67, 0.67] |
| qdrant | pre-exact | all | 0.44 [0.26, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.56 [0.33, 0.78] |

## Mitigation costs (latency, ratio of means)

| store | mitigation | ratio | interval | median ratio | pairs |
|---|---|---|---|---|---|
| elasticsearch | M1/M2 post-const / post | 0.983 | [0.83, 1.14] | 2.275 | 54 |
| elasticsearch | M1/M2 pre-exact / pre | 1.270 | [1.09, 1.52] | 1.143 | 54 |
| elasticsearch | M3 separated / shared (bm25-pre) | 0.953 | [0.92, 1.00] | 1.020 | 27 |
| elasticsearch | M3 separated / shared (hybrid-exact) | 0.971 | [0.93, 1.02] | 1.000 | 27 |
| elasticsearch | M3 separated / shared (hybrid-pre) | 1.016 | [0.98, 1.05] | 1.012 | 27 |
| elasticsearch | M3 separated / shared (post) | 0.930 | [0.80, 1.03] | 0.988 | 27 |
| elasticsearch | M3 separated / shared (post-const) | 1.006 | [0.98, 1.03] | 0.995 | 27 |
| elasticsearch | M3 separated / shared (pre) | 0.979 | [0.95, 1.03] | 1.014 | 27 |
| elasticsearch | M3 separated / shared (pre-exact) | 0.978 | [0.92, 1.05] | 1.013 | 27 |
| faiss | M1/M2 post-const / post | 0.791 | [0.73, 0.85] | 1.227 | 54 |
| faiss | M3 separated / shared (post) | 0.836 | [0.74, 0.91] | 0.848 | 27 |
| faiss | M3 separated / shared (post-const) | 1.227 | [0.94, 1.80] | 0.946 | 27 |
| faiss | M3 separated / shared (pre) | 0.880 | [0.88, 0.89] | 0.875 | 27 |
| memory | M3 separated / shared (post) | 0.741 | [0.60, 0.86] | 0.833 | 4 |
| memory | M3 separated / shared (pre) | 0.963 | [0.96, 0.97] | 0.962 | 4 |
| pgvector | M1/M2 post-const / post | 1.189 | [1.01, 1.45] | 3.144 | 54 |
| pgvector | M1/M2 pre-exact / pre | 12.723 | [10.39, 15.19] | 7.747 | 54 |
| pgvector | M3 separated / shared (bm25-pre) | 0.758 | [0.69, 0.98] | 0.960 | 27 |
| pgvector | M3 separated / shared (post) | 0.946 | [0.88, 0.99] | 0.960 | 27 |
| pgvector | M3 separated / shared (post-const) | 0.924 | [0.82, 0.99] | 0.982 | 27 |
| pgvector | M3 separated / shared (pre) | 0.468 | [0.44, 0.50] | 0.904 | 27 |
| pgvector | M3 separated / shared (pre-exact) | 0.414 | [0.36, 0.55] | 0.264 | 27 |
| qdrant | M1/M2 post-const / post | 1.086 | [0.94, 1.33] | 2.717 | 54 |
| qdrant | M1/M2 pre-exact / pre | 1.592 | [1.56, 1.62] | 1.051 | 54 |
| qdrant | M3 separated / shared (bm25-pre) | 0.976 | [0.96, 0.99] | 0.973 | 27 |
| qdrant | M3 separated / shared (post) | 0.879 | [0.73, 1.00] | 0.972 | 27 |
| qdrant | M3 separated / shared (post-const) | 0.899 | [0.78, 0.99] | 0.982 | 27 |
| qdrant | M3 separated / shared (pre) | 0.976 | [0.96, 0.99] | 0.978 | 27 |
| qdrant | M3 separated / shared (pre-exact) | 0.979 | [0.96, 1.00] | 0.977 | 27 |

## Id-list change rate, W1 against W0 (deterministic configurations)

| store | config | m | rate | interval | A/A rate | pairs |
|---|---|---|---|---|---|---|
| elasticsearch | bm25-pre | all | 1.000 | [1.00, 1.00] | 0.000 | 27 |
| elasticsearch | bm25-pre | 1 | 1.000 | [1.00, 1.00] | 0.000 | 9 |
| elasticsearch | bm25-pre | 10 | 1.000 | [1.00, 1.00] | 0.000 | 9 |
| elasticsearch | bm25-pre | 100 | 1.000 | [1.00, 1.00] | 0.000 | 6 |
| elasticsearch | bm25-pre | 1000 | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| elasticsearch | hybrid-exact | all | 0.222 | [0.11, 0.30] | 0.000 | 27 |
| elasticsearch | hybrid-exact | 1 | 0.333 | [0.33, 0.33] | 0.000 | 9 |
| elasticsearch | hybrid-exact | 10 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| elasticsearch | hybrid-exact | 100 | 0.333 | [0.33, 0.33] | 0.000 | 6 |
| elasticsearch | hybrid-exact | 1000 | 0.333 | [0.33, 0.33] | 0.000 | 3 |
| elasticsearch | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 27 |
| elasticsearch | pre-exact | 1 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| elasticsearch | pre-exact | 10 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| elasticsearch | pre-exact | 100 | 0.000 | [0.00, 0.00] | 0.000 | 6 |
| elasticsearch | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| faiss | pre | all | 0.000 | [0.00, 0.00] | 0.000 | 27 |
| faiss | pre | 1 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| faiss | pre | 10 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| faiss | pre | 100 | 0.000 | [0.00, 0.00] | 0.000 | 6 |
| faiss | pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| memory | pre | all | 0.000 | [0.00, 0.00] | 0.000 | 4 |
| memory | pre | 1 | 0.000 | [0.00, 0.00] | 0.000 | 1 |
| memory | pre | 10 | 0.000 | [0.00, 0.00] | 0.000 | 1 |
| memory | pre | 100 | 0.000 | [0.00, 0.00] | 0.000 | 1 |
| memory | pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 1 |
| pgvector | bm25-pre | all | 0.000 | [0.00, 0.00] | 0.000 | 27 |
| pgvector | bm25-pre | 1 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| pgvector | bm25-pre | 10 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| pgvector | bm25-pre | 100 | 0.000 | [0.00, 0.00] | 0.000 | 6 |
| pgvector | bm25-pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| pgvector | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 27 |
| pgvector | pre-exact | 1 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| pgvector | pre-exact | 10 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| pgvector | pre-exact | 100 | 0.000 | [0.00, 0.00] | 0.000 | 6 |
| pgvector | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |
| qdrant | bm25-pre | all | 1.000 | [1.00, 1.00] | 0.000 | 27 |
| qdrant | bm25-pre | 1 | 1.000 | [1.00, 1.00] | 0.000 | 9 |
| qdrant | bm25-pre | 10 | 1.000 | [1.00, 1.00] | 0.000 | 9 |
| qdrant | bm25-pre | 100 | 1.000 | [1.00, 1.00] | 0.000 | 6 |
| qdrant | bm25-pre | 1000 | 1.000 | [1.00, 1.00] | 0.000 | 3 |
| qdrant | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 27 |
| qdrant | pre-exact | 1 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| qdrant | pre-exact | 10 | 0.000 | [0.00, 0.00] | 0.000 | 9 |
| qdrant | pre-exact | 100 | 0.000 | [0.00, 0.00] | 0.000 | 6 |
| qdrant | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 3 |

## Every verdict part

| hypothesis | store | config | part | outcome | evidence |
|---|---|---|---|---|---|
| H1 | faiss | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | faiss | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | faiss | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H1 | faiss | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | faiss | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | faiss | post | (c) m=1 no channel in latency | inconclusive | 0.444 [0.333, 0.558] (3 clusters, 1 seeds) |
| H1 | faiss | post | (c) m=1 no channel in count | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | faiss | post | (c) m=1 no channel in complete | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | faiss | post | (c) m=1 no channel in recall | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | faiss | post | (c) m=1 no channel in score | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | pgvector | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | pgvector | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | pgvector | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H1 | pgvector | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | pgvector | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in latency | inconclusive | 0.444 [0.333, 0.556] (3 clusters, 1 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in count | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in complete | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in recall | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in score | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | qdrant | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | qdrant | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | qdrant | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H1 | qdrant | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | qdrant | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in latency | inconclusive | 0.667 [0.667, 0.667] (3 clusters, 1 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in count | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in complete | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in recall | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in score | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=1 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H1 | elasticsearch | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | elasticsearch | post | (b) m=100 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in latency | inconclusive | 0.889 [0.667, 1.000] (3 clusters, 1 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in count | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in complete | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in recall | inconclusive | 0.500 [0.500, 0.500] (3 clusters, 1 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in score | inconclusive | 0.444 [0.167, 0.613] (3 clusters, 1 seeds) |
| H2 | faiss | post-const | (a) no latency channel pooled | inconclusive | 0.481 [0.370, 0.630] (9 clusters, 1 seeds) |
| H2 | faiss | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | faiss | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | faiss | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H2 | pgvector | post-const | (a) no latency channel pooled | inconclusive | 0.333 [0.148, 0.519] (9 clusters, 1 seeds) |
| H2 | pgvector | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| H2 | pgvector | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | pgvector | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H2 | qdrant | post-const | (a) no latency channel pooled | inconclusive | 0.370 [0.222, 0.481] (9 clusters, 1 seeds) |
| H2 | qdrant | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H2 | qdrant | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | qdrant | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (a) no latency channel pooled | inconclusive | 0.593 [0.333, 0.852] (9 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H2 | elasticsearch | post-const | (b) m=1000 p=50 count >= 0.95 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H3a | pgvector | pre | m=1000 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3a | pgvector | pre | m=1000 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3a | pgvector | pre | m=100 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H3b | elasticsearch | pre | m=1000 p=10 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3b | elasticsearch | pre | m=1000 p=50 latency >= 0.75 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in latency | inconclusive | 0.778 [0.611, 0.944] (9 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in count | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in complete | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in recall | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in score | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in latency pooled | inconclusive | 0.148 [0.000, 0.370] (9 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.000 [0.000, 0.000] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | pgvector | pre-exact | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in latency pooled | inconclusive | 0.444 [0.259, 0.667] (9 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | qdrant | pre-exact | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in latency pooled | inconclusive | 0.667 [0.519, 0.815] (9 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.667 [0.667, 0.667] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in latency pooled | inconclusive | 0.556 [0.406, 0.742] (9 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 latency upper <= 0.65 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in recall pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 recall upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | faiss | pre | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H4 | faiss | pre | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in latency pooled | inconclusive | 0.750 [0.250, 1.000] (4 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 latency upper <= 0.65 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in count pooled | inconclusive | 0.500 [0.500, 0.500] (4 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in complete pooled | inconclusive | 0.500 [0.500, 0.500] (4 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H4 | memory | pre | no channel in score pooled | inconclusive | 0.500 [0.500, 0.500] (4 clusters, 1 seeds) |
| H4 | memory | pre | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (1 clusters, 1 seeds) |
| H5a | elasticsearch | bm25-pre | m=1 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (3 clusters, 1 seeds) |
| H5a | elasticsearch | bm25-pre | m=10 score >= 0.90 | inconclusive | 0.778 [0.333, 1.000] (3 clusters, 1 seeds) |
| H5a | elasticsearch | bm25-pre | m=100 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H5a | elasticsearch | bm25-pre | m=1000 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H5a | qdrant | bm25-pre | m=1 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (3 clusters, 1 seeds) |
| H5a | qdrant | bm25-pre | m=10 score >= 0.90 | inconclusive | 0.778 [0.550, 1.000] (3 clusters, 1 seeds) |
| H5a | qdrant | bm25-pre | m=100 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (2 clusters, 1 seeds) |
| H5a | qdrant | bm25-pre | m=1000 score >= 0.90 | inconclusive | 1.000 [1.000, 1.000] (1 clusters, 1 seeds) |
| H5b | pgvector | bm25-pre | no channel in the score | inconclusive | 0.500 [0.500, 0.500] (9 clusters, 1 seeds) |
| H5b | pgvector | bm25-pre | id-list change rate <= 0.01 | inconclusive | change rate 0.000 [0.000, 0.000] (9 clusters, 1 seeds) |
| H5c | elasticsearch | hybrid-exact | m=1000 change rate >= 0.25 | inconclusive | change rate 0.333 [0.333, 0.333] (1 clusters, 1 seeds) |

