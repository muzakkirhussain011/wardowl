# X6: side channels of permission-aware retrieval

520,970 records (0 unreadable lines), 10,000 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md. AUC 0.5 means no advantage; the paired AUC is the differencing attacker's.

## Health

| store | mode | seeds done | skipped | retrievals | errors | stopped | build s | setup error | leaks |
|---|---|---|---|---|---|---|---|---|---|
| elasticsearch | full | [0, 1, 2, 3, 4] | [] | 181440 | {} | [] | {"w1": 26.7, "sep": 22.1, "w0": 26.0} | n/a | 0 |
| faiss | full | [0, 1, 2, 3, 4] | [] | 77760 | {} | [] | {"w1": 0.6, "sep": 0.5, "w0": 0.6} | n/a | 0 |
| memory | full | [0, 1, 2, 3, 4] | [] | 1920 | {} | [] | {"w1": 0.4, "sep": 0.3, "w0": 0.4} | n/a | 0 |
| pgvector | full | [0, 1, 2, 3, 4] | [] | 129600 | {} | [] | {"w1": 23.7, "sep": 19.9, "w0": 23.4} | n/a | 0 |
| qdrant | full | [0, 1, 2, 3, 4] | [] | 129600 | {} | [] | {"w1": 57.6, "sep": 48.3, "w0": 57.8} | n/a | 0 |

## Verdicts

| hypothesis | scope | outcome | evidence |
|---|---|---|---|
| H1 | vector stores | falsified | 29 confirmed, 5 falsified, 6 inconclusive parts |
| H2 | vector stores | falsified | 2 confirmed, 4 falsified, 10 inconclusive parts |
| H3a | pgvector | confirmed | 3 confirmed, 0 falsified, 0 inconclusive parts |
| H3b | elasticsearch | inconclusive | 1 confirmed, 0 falsified, 1 inconclusive parts |
| H3c | qdrant | confirmed | 5 confirmed, 0 falsified, 0 inconclusive parts |
| H4 | pgvector pre-exact | inconclusive | 8 confirmed, 0 falsified, 2 inconclusive parts |
| H4 | qdrant pre-exact | inconclusive | 9 confirmed, 0 falsified, 1 inconclusive parts |
| H4 | elasticsearch pre-exact | inconclusive | 9 confirmed, 0 falsified, 1 inconclusive parts |
| H4 | faiss pre | inconclusive | 8 confirmed, 0 falsified, 2 inconclusive parts |
| H4 | memory pre | inconclusive | 3 confirmed, 0 falsified, 5 inconclusive parts |
| H5a | elasticsearch | inconclusive | 2 confirmed, 0 falsified, 2 inconclusive parts |
| H5a | qdrant | inconclusive | 2 confirmed, 0 falsified, 2 inconclusive parts |
| H5b | pgvector | confirmed | 2 confirmed, 0 falsified, 0 inconclusive parts |
| H5c | elasticsearch | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| H6 | every cell with a raw latency channel | inconclusive | 0 confirmed, 0 falsified, 7 inconclusive parts |

## Guards

| guard | store | config | passed | evidence |
|---|---|---|---|---|
| G1 | elasticsearch | bm25-pre | True | 0.491 [0.462, 0.521] (360 clusters, 5 seeds) |
| G1 | elasticsearch | hybrid-exact | True | 0.463 [0.436, 0.492] (360 clusters, 5 seeds) |
| G1 | elasticsearch | hybrid-pre | True | 0.513 [0.481, 0.544] (360 clusters, 5 seeds) |
| G1 | elasticsearch | post | True | 0.499 [0.467, 0.530] (360 clusters, 5 seeds) |
| G1 | elasticsearch | post-const | True | 0.513 [0.483, 0.542] (360 clusters, 5 seeds) |
| G1 | elasticsearch | pre | True | 0.500 [0.470, 0.530] (360 clusters, 5 seeds) |
| G1 | elasticsearch | pre-exact | True | 0.507 [0.478, 0.536] (360 clusters, 5 seeds) |
| G1 | faiss | post | True | 0.499 [0.468, 0.529] (360 clusters, 5 seeds) |
| G1 | faiss | post-const | True | 0.514 [0.483, 0.544] (360 clusters, 5 seeds) |
| G1 | faiss | pre | True | 0.504 [0.473, 0.535] (360 clusters, 5 seeds) |
| G1 | memory | post | False | 0.533 [0.400, 0.650] (60 clusters, 5 seeds) |
| G1 | memory | pre | False | 0.500 [0.367, 0.633] (60 clusters, 5 seeds) |
| G1 | pgvector | bm25-pre | True | 0.536 [0.507, 0.563] (360 clusters, 5 seeds) |
| G1 | pgvector | post | True | 0.493 [0.463, 0.523] (360 clusters, 5 seeds) |
| G1 | pgvector | post-const | True | 0.484 [0.454, 0.515] (360 clusters, 5 seeds) |
| G1 | pgvector | pre | True | 0.504 [0.472, 0.535] (360 clusters, 5 seeds) |
| G1 | pgvector | pre-exact | True | 0.506 [0.478, 0.535] (360 clusters, 5 seeds) |
| G1 | qdrant | bm25-pre | True | 0.492 [0.461, 0.522] (360 clusters, 5 seeds) |
| G1 | qdrant | post | True | 0.495 [0.466, 0.525] (360 clusters, 5 seeds) |
| G1 | qdrant | post-const | True | 0.517 [0.486, 0.545] (360 clusters, 5 seeds) |
| G1 | qdrant | pre | True | 0.505 [0.474, 0.535] (360 clusters, 5 seeds) |
| G1 | qdrant | pre-exact | True | 0.499 [0.470, 0.529] (360 clusters, 5 seeds) |
| G2 | elasticsearch | pre-exact | True | pre-exact: change rate 0.0000 |
| G2 | faiss | pre | True | pre: change rate 0.0000 |
| G2 | pgvector | pre-exact | True | pre-exact: change rate 0.0000 |
| G2 | qdrant | pre-exact | True | pre-exact: change rate 0.0000 |

## Paired AUC (W1 against W0), pooled over selectivity

| store | config | m | latency | count | complete | recall | score | A/A latency |
|---|---|---|---|---|---|---|---|---|
| elasticsearch | bm25-pre | 1 | 0.41 [0.35, 0.47] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.79 [0.73, 0.86] | 0.52 [0.47, 0.57] |
| elasticsearch | bm25-pre | 10 | 0.45 [0.38, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.88 [0.82, 0.93] | 0.47 [0.42, 0.52] |
| elasticsearch | bm25-pre | 100 | 0.43 [0.36, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.98 [0.95, 1.00] | 0.51 [0.44, 0.59] |
| elasticsearch | bm25-pre | 1000 | 0.40 [0.30, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.99 [0.97, 1.00] | 0.44 [0.38, 0.51] |
| elasticsearch | bm25-pre | all | 0.43 [0.39, 0.46] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.89 [0.85, 0.91] | 0.49 [0.46, 0.52] |
| elasticsearch | hybrid-exact | 1 | 0.46 [0.40, 0.52] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.48, 0.51] | 0.48 [0.43, 0.53] |
| elasticsearch | hybrid-exact | 10 | 0.43 [0.37, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.48 [0.47, 0.50] | 0.47 [0.41, 0.52] |
| elasticsearch | hybrid-exact | 100 | 0.47 [0.40, 0.54] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.52 [0.50, 0.54] | 0.44 [0.39, 0.49] |
| elasticsearch | hybrid-exact | 1000 | 0.47 [0.35, 0.58] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.53 [0.51, 0.55] | 0.46 [0.37, 0.54] |
| elasticsearch | hybrid-exact | all | 0.45 [0.42, 0.49] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.49, 0.51] | 0.46 [0.44, 0.49] |
| elasticsearch | hybrid-pre | 1 | 0.49 [0.43, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.48 [0.46, 0.51] | 0.50 [0.45, 0.56] |
| elasticsearch | hybrid-pre | 10 | 0.49 [0.42, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.48 [0.46, 0.50] | 0.54 [0.49, 0.59] |
| elasticsearch | hybrid-pre | 100 | 0.45 [0.37, 0.53] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.52 [0.49, 0.55] | 0.50 [0.44, 0.57] |
| elasticsearch | hybrid-pre | 1000 | 0.49 [0.38, 0.60] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.53 [0.50, 0.55] | 0.50 [0.40, 0.60] |
| elasticsearch | hybrid-pre | all | 0.48 [0.44, 0.52] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.48, 0.51] | 0.51 [0.48, 0.54] |
| elasticsearch | post | 1 | 0.48 [0.41, 0.54] | 0.50 [0.49, 0.51] | 0.50 [0.49, 0.50] | 0.51 [0.49, 0.52] | 0.51 [0.48, 0.53] | 0.49 [0.44, 0.53] |
| elasticsearch | post | 10 | 0.58 [0.51, 0.65] | 0.51 [0.50, 0.52] | 0.50 [0.50, 0.50] | 0.49 [0.47, 0.52] | 0.48 [0.45, 0.51] | 0.51 [0.45, 0.57] |
| elasticsearch | post | 100 | 0.76 [0.70, 0.82] | 0.58 [0.56, 0.60] | 0.51 [0.50, 0.53] | 0.43 [0.39, 0.46] | 0.28 [0.24, 0.31] | 0.50 [0.43, 0.56] |
| elasticsearch | post | 1000 | 0.86 [0.81, 0.91] | 0.84 [0.81, 0.88] | 0.72 [0.69, 0.77] | 0.69 [0.65, 0.73] | 0.34 [0.26, 0.42] | 0.51 [0.40, 0.61] |
| elasticsearch | post | all | 0.62 [0.58, 0.65] | 0.56 [0.55, 0.57] | 0.53 [0.52, 0.54] | 0.51 [0.49, 0.52] | 0.43 [0.41, 0.45] | 0.50 [0.47, 0.53] |
| elasticsearch | post-const | 1 | 0.57 [0.51, 0.64] | 0.50 [0.49, 0.51] | 0.50 [0.49, 0.50] | 0.51 [0.50, 0.52] | 0.51 [0.49, 0.52] | 0.49 [0.44, 0.54] |
| elasticsearch | post-const | 10 | 0.57 [0.51, 0.63] | 0.51 [0.50, 0.52] | 0.50 [0.50, 0.50] | 0.51 [0.49, 0.52] | 0.50 [0.48, 0.51] | 0.53 [0.48, 0.58] |
| elasticsearch | post-const | 100 | 0.55 [0.47, 0.64] | 0.58 [0.56, 0.60] | 0.51 [0.50, 0.53] | 0.57 [0.55, 0.59] | 0.41 [0.39, 0.44] | 0.55 [0.48, 0.61] |
| elasticsearch | post-const | 1000 | 0.62 [0.52, 0.72] | 0.84 [0.81, 0.88] | 0.72 [0.68, 0.76] | 0.84 [0.80, 0.88] | 0.45 [0.38, 0.51] | 0.47 [0.38, 0.56] |
| elasticsearch | post-const | all | 0.57 [0.54, 0.61] | 0.56 [0.55, 0.57] | 0.53 [0.52, 0.54] | 0.56 [0.54, 0.57] | 0.48 [0.46, 0.49] | 0.51 [0.48, 0.54] |
| elasticsearch | pre | 1 | 0.49 [0.43, 0.55] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.48, 0.53] | 0.50 [0.46, 0.53] | 0.55 [0.50, 0.60] |
| elasticsearch | pre | 10 | 0.50 [0.44, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.51 [0.48, 0.54] | 0.51 [0.48, 0.55] | 0.45 [0.40, 0.49] |
| elasticsearch | pre | 100 | 0.48 [0.40, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.46 [0.43, 0.50] | 0.48 [0.43, 0.53] | 0.49 [0.42, 0.55] |
| elasticsearch | pre | 1000 | 0.60 [0.50, 0.68] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.49 [0.44, 0.54] | 0.47 [0.40, 0.53] | 0.54 [0.45, 0.63] |
| elasticsearch | pre | all | 0.50 [0.46, 0.54] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.48, 0.51] | 0.50 [0.47, 0.52] | 0.50 [0.47, 0.53] |
| elasticsearch | pre-exact | 1 | 0.50 [0.44, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.51 [0.46, 0.56] |
| elasticsearch | pre-exact | 10 | 0.48 [0.42, 0.55] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.52 [0.47, 0.57] |
| elasticsearch | pre-exact | 100 | 0.47 [0.40, 0.54] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.46 [0.40, 0.51] |
| elasticsearch | pre-exact | 1000 | 0.47 [0.37, 0.57] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.57 [0.48, 0.65] |
| elasticsearch | pre-exact | all | 0.49 [0.45, 0.52] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.51 [0.48, 0.54] |
| faiss | post | 1 | 0.67 [0.62, 0.72] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.49 [0.43, 0.54] |
| faiss | post | 10 | 0.67 [0.62, 0.72] | 0.51 [0.50, 0.52] | 0.50 [0.50, 0.51] | 0.51 [0.50, 0.52] | 0.49 [0.48, 0.50] | 0.49 [0.44, 0.54] |
| faiss | post | 100 | 0.80 [0.76, 0.85] | 0.59 [0.57, 0.61] | 0.52 [0.51, 0.53] | 0.59 [0.57, 0.61] | 0.41 [0.39, 0.43] | 0.50 [0.44, 0.56] |
| faiss | post | 1000 | 0.76 [0.72, 0.81] | 0.87 [0.83, 0.90] | 0.74 [0.70, 0.78] | 0.87 [0.83, 0.90] | 0.48 [0.41, 0.55] | 0.54 [0.44, 0.64] |
| faiss | post | all | 0.71 [0.68, 0.74] | 0.56 [0.55, 0.58] | 0.53 [0.52, 0.54] | 0.56 [0.55, 0.58] | 0.47 [0.46, 0.48] | 0.50 [0.47, 0.53] |
| faiss | post-const | 1 | 0.63 [0.57, 0.68] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.49 [0.44, 0.54] |
| faiss | post-const | 10 | 0.57 [0.52, 0.62] | 0.51 [0.50, 0.52] | 0.50 [0.50, 0.51] | 0.51 [0.50, 0.52] | 0.49 [0.48, 0.50] | 0.53 [0.48, 0.59] |
| faiss | post-const | 100 | 0.46 [0.40, 0.52] | 0.59 [0.57, 0.61] | 0.52 [0.51, 0.53] | 0.59 [0.57, 0.61] | 0.41 [0.39, 0.43] | 0.51 [0.45, 0.58] |
| faiss | post-const | 1000 | 0.13 [0.07, 0.20] | 0.87 [0.83, 0.91] | 0.74 [0.70, 0.78] | 0.87 [0.83, 0.90] | 0.48 [0.40, 0.55] | 0.53 [0.45, 0.60] |
| faiss | post-const | all | 0.52 [0.48, 0.55] | 0.56 [0.55, 0.58] | 0.53 [0.52, 0.54] | 0.56 [0.55, 0.58] | 0.47 [0.46, 0.48] | 0.51 [0.48, 0.54] |
| faiss | pre | 1 | 0.25 [0.20, 0.30] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.55 [0.50, 0.60] |
| faiss | pre | 10 | 0.30 [0.24, 0.36] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.47 [0.42, 0.53] |
| faiss | pre | 100 | 0.25 [0.19, 0.30] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.49 [0.43, 0.55] |
| faiss | pre | 1000 | 0.35 [0.25, 0.45] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.47 [0.39, 0.57] |
| faiss | pre | all | 0.28 [0.25, 0.31] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.47, 0.54] |
| memory | post | 1 | 0.33 [0.13, 0.60] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.53 [0.27, 0.80] |
| memory | post | 10 | 0.40 [0.13, 0.67] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.60 [0.33, 0.80] |
| memory | post | 100 | 0.47 [0.20, 0.73] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.60 [0.33, 0.87] |
| memory | post | 1000 | 0.67 [0.40, 0.87] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.40 [0.20, 0.67] |
| memory | post | all | 0.47 [0.33, 0.60] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.53 [0.40, 0.65] |
| memory | pre | 1 | 0.47 [0.20, 0.73] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.47 [0.20, 0.73] |
| memory | pre | 10 | 0.53 [0.27, 0.80] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.47 [0.20, 0.73] |
| memory | pre | 100 | 0.33 [0.13, 0.60] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.60 [0.33, 0.87] |
| memory | pre | 1000 | 0.20 [0.00, 0.40] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.47 [0.20, 0.73] |
| memory | pre | all | 0.38 [0.27, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.50 [0.37, 0.63] |
| pgvector | bm25-pre | 1 | 0.45 [0.40, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.56 [0.51, 0.61] |
| pgvector | bm25-pre | 10 | 0.47 [0.41, 0.53] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.53 [0.48, 0.57] |
| pgvector | bm25-pre | 100 | 0.50 [0.43, 0.58] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.49 [0.42, 0.55] |
| pgvector | bm25-pre | 1000 | 0.70 [0.58, 0.81] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.58 [0.50, 0.67] |
| pgvector | bm25-pre | all | 0.50 [0.46, 0.53] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.50 [0.50, 0.50] | 0.54 [0.51, 0.56] |
| pgvector | post | 1 | 0.37 [0.32, 0.42] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.48, 0.51] | 0.50 [0.48, 0.51] | 0.51 [0.46, 0.55] |
| pgvector | post | 10 | 0.38 [0.33, 0.43] | 0.50 [0.50, 0.51] | 0.50 [0.50, 0.50] | 0.48 [0.47, 0.50] | 0.48 [0.46, 0.50] | 0.49 [0.44, 0.54] |
| pgvector | post | 100 | 0.57 [0.53, 0.62] | 0.58 [0.56, 0.60] | 0.51 [0.50, 0.52] | 0.41 [0.38, 0.44] | 0.25 [0.22, 0.28] | 0.46 [0.39, 0.53] |
| pgvector | post | 1000 | 0.68 [0.67, 0.69] | 0.85 [0.82, 0.89] | 0.73 [0.69, 0.78] | 0.71 [0.67, 0.75] | 0.35 [0.27, 0.42] | 0.53 [0.42, 0.62] |
| pgvector | post | all | 0.45 [0.42, 0.48] | 0.56 [0.54, 0.57] | 0.53 [0.52, 0.54] | 0.50 [0.48, 0.51] | 0.42 [0.40, 0.43] | 0.49 [0.46, 0.52] |
| pgvector | post-const | 1 | 0.29 [0.24, 0.34] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.49 [0.49, 0.50] | 0.50 [0.49, 0.50] | 0.46 [0.41, 0.52] |
| pgvector | post-const | 10 | 0.22 [0.18, 0.26] | 0.50 [0.50, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.51] | 0.50 [0.49, 0.50] | 0.47 [0.42, 0.53] |
| pgvector | post-const | 100 | 0.07 [0.05, 0.11] | 0.58 [0.56, 0.60] | 0.51 [0.50, 0.52] | 0.58 [0.56, 0.60] | 0.42 [0.40, 0.44] | 0.51 [0.44, 0.57] |
| pgvector | post-const | 1000 | 0.02 [0.00, 0.05] | 0.85 [0.82, 0.89] | 0.73 [0.69, 0.78] | 0.86 [0.83, 0.90] | 0.44 [0.37, 0.51] | 0.53 [0.45, 0.62] |
| pgvector | post-const | all | 0.19 [0.16, 0.21] | 0.56 [0.54, 0.57] | 0.53 [0.52, 0.54] | 0.56 [0.54, 0.57] | 0.47 [0.46, 0.48] | 0.48 [0.45, 0.51] |
| pgvector | pre | 1 | 0.33 [0.29, 0.38] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.49 [0.47, 0.50] | 0.49 [0.47, 0.50] | 0.49 [0.44, 0.55] |
| pgvector | pre | 10 | 0.44 [0.39, 0.49] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.47 [0.45, 0.49] | 0.47 [0.44, 0.49] | 0.49 [0.44, 0.54] |
| pgvector | pre | 100 | 0.79 [0.75, 0.82] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.31 [0.29, 0.34] | 0.32 [0.29, 0.35] | 0.51 [0.44, 0.58] |
| pgvector | pre | 1000 | 0.88 [0.82, 0.93] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.22 [0.17, 0.27] | 0.22 [0.17, 0.28] | 0.57 [0.50, 0.65] |
| pgvector | pre | all | 0.53 [0.50, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.41 [0.40, 0.43] | 0.41 [0.40, 0.43] | 0.50 [0.47, 0.54] |
| pgvector | pre-exact | 1 | 0.17 [0.13, 0.22] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.53 [0.49, 0.58] |
| pgvector | pre-exact | 10 | 0.14 [0.09, 0.19] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.48 [0.43, 0.53] |
| pgvector | pre-exact | 100 | 0.13 [0.08, 0.19] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.51 [0.45, 0.58] |
| pgvector | pre-exact | 1000 | 0.12 [0.07, 0.19] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.47 [0.39, 0.57] |
| pgvector | pre-exact | all | 0.15 [0.12, 0.17] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.51 [0.48, 0.53] |
| qdrant | bm25-pre | 1 | 0.47 [0.42, 0.53] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.81 [0.74, 0.87] | 0.50 [0.45, 0.55] |
| qdrant | bm25-pre | 10 | 0.46 [0.41, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.89 [0.83, 0.93] | 0.53 [0.47, 0.58] |
| qdrant | bm25-pre | 100 | 0.48 [0.42, 0.55] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.98 [0.95, 1.00] | 0.49 [0.42, 0.55] |
| qdrant | bm25-pre | 1000 | 0.55 [0.47, 0.63] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 1.00 [1.00, 1.00] | 0.37 [0.28, 0.45] |
| qdrant | bm25-pre | all | 0.48 [0.45, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] |  | 0.89 [0.86, 0.92] | 0.49 [0.46, 0.52] |
| qdrant | post | 1 | 0.47 [0.42, 0.53] | 0.51 [0.50, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.48, 0.52] | 0.49 [0.47, 0.50] | 0.49 [0.44, 0.55] |
| qdrant | post | 10 | 0.46 [0.41, 0.51] | 0.51 [0.50, 0.52] | 0.50 [0.50, 0.50] | 0.51 [0.49, 0.53] | 0.49 [0.47, 0.51] | 0.48 [0.43, 0.54] |
| qdrant | post | 100 | 0.75 [0.70, 0.80] | 0.58 [0.56, 0.60] | 0.51 [0.50, 0.52] | 0.49 [0.45, 0.53] | 0.32 [0.28, 0.36] | 0.50 [0.45, 0.56] |
| qdrant | post | 1000 | 0.78 [0.73, 0.83] | 0.87 [0.83, 0.90] | 0.75 [0.71, 0.79] | 0.80 [0.76, 0.84] | 0.44 [0.36, 0.52] | 0.52 [0.42, 0.61] |
| qdrant | post | all | 0.57 [0.53, 0.60] | 0.56 [0.55, 0.58] | 0.53 [0.52, 0.54] | 0.53 [0.52, 0.55] | 0.45 [0.43, 0.46] | 0.50 [0.47, 0.53] |
| qdrant | post-const | 1 | 0.47 [0.42, 0.53] | 0.51 [0.50, 0.51] | 0.50 [0.50, 0.50] | 0.51 [0.50, 0.52] | 0.49 [0.48, 0.50] | 0.49 [0.44, 0.54] |
| qdrant | post-const | 10 | 0.47 [0.42, 0.53] | 0.51 [0.50, 0.52] | 0.50 [0.50, 0.50] | 0.51 [0.50, 0.52] | 0.49 [0.49, 0.50] | 0.51 [0.46, 0.56] |
| qdrant | post-const | 100 | 0.45 [0.38, 0.53] | 0.58 [0.56, 0.60] | 0.51 [0.50, 0.52] | 0.58 [0.56, 0.60] | 0.42 [0.40, 0.44] | 0.56 [0.50, 0.62] |
| qdrant | post-const | 1000 | 0.35 [0.23, 0.48] | 0.87 [0.83, 0.90] | 0.75 [0.70, 0.79] | 0.88 [0.84, 0.91] | 0.48 [0.41, 0.55] | 0.52 [0.43, 0.60] |
| qdrant | post-const | all | 0.46 [0.42, 0.49] | 0.56 [0.55, 0.58] | 0.53 [0.52, 0.54] | 0.56 [0.55, 0.58] | 0.48 [0.47, 0.49] | 0.52 [0.49, 0.55] |
| qdrant | pre | 1 | 0.47 [0.42, 0.53] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.49, 0.52] | 0.50 [0.49, 0.52] | 0.53 [0.48, 0.58] |
| qdrant | pre | 10 | 0.43 [0.38, 0.48] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.53 [0.52, 0.55] | 0.54 [0.52, 0.55] | 0.49 [0.43, 0.54] |
| qdrant | pre | 100 | 0.47 [0.41, 0.54] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.53 [0.50, 0.56] | 0.54 [0.51, 0.57] | 0.50 [0.44, 0.57] |
| qdrant | pre | 1000 | 0.57 [0.45, 0.68] | 0.50 [0.50, 0.51] | 0.50 [0.50, 0.51] | 0.60 [0.56, 0.62] | 0.57 [0.53, 0.62] | 0.48 [0.41, 0.56] |
| qdrant | pre | all | 0.47 [0.44, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.53 [0.52, 0.54] | 0.53 [0.52, 0.54] | 0.50 [0.47, 0.54] |
| qdrant | pre-exact | 1 | 0.45 [0.40, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.49 [0.44, 0.54] |
| qdrant | pre-exact | 10 | 0.46 [0.41, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.48 [0.43, 0.53] |
| qdrant | pre-exact | 100 | 0.50 [0.43, 0.56] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.51 [0.45, 0.57] |
| qdrant | pre-exact | 1000 | 0.42 [0.33, 0.51] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.55 [0.47, 0.62] |
| qdrant | pre-exact | all | 0.46 [0.43, 0.49] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.47, 0.53] |

## Mitigation costs (latency, ratio of means)

| store | mitigation | ratio | interval | median ratio | pairs |
|---|---|---|---|---|---|
| elasticsearch | M1/M2 post-const / post | 1.106 | [1.08, 1.13] | 3.012 | 2160 |
| elasticsearch | M1/M2 pre-exact / pre | 2.014 | [1.99, 2.03] | 1.393 | 2160 |
| elasticsearch | M3 separated / shared (bm25-pre) | 0.902 | [0.89, 0.91] | 0.897 | 1080 |
| elasticsearch | M4 padded / raw (bm25-pre) | 4.588 | [4.48, 4.71] | 4.686 | 1728 |
| elasticsearch | M3 separated / shared (hybrid-exact) | 0.940 | [0.94, 0.94] | 0.934 | 1080 |
| elasticsearch | M4 padded / raw (hybrid-exact) | 2.246 | [2.22, 2.27] | 2.627 | 1728 |
| elasticsearch | M3 separated / shared (hybrid-pre) | 0.927 | [0.92, 0.93] | 0.924 | 1080 |
| elasticsearch | M4 padded / raw (hybrid-pre) | 3.248 | [3.20, 3.29] | 3.277 | 1728 |
| elasticsearch | M3 separated / shared (post) | 0.901 | [0.88, 0.92] | 0.971 | 1080 |
| elasticsearch | M4 padded / raw (post) | 5.224 | [5.09, 5.36] | 14.139 | 1728 |
| elasticsearch | M3 separated / shared (post-const) | 0.986 | [0.98, 0.99] | 0.986 | 1080 |
| elasticsearch | M4 padded / raw (post-const) | 3.675 | [3.66, 3.69] | 3.707 | 1728 |
| elasticsearch | M3 separated / shared (pre) | 0.948 | [0.94, 0.95] | 0.952 | 1080 |
| elasticsearch | M4 padded / raw (pre) | 6.265 | [6.23, 6.29] | 6.093 | 1728 |
| elasticsearch | M3 separated / shared (pre-exact) | 0.942 | [0.94, 0.94] | 0.942 | 1080 |
| elasticsearch | M4 padded / raw (pre-exact) | 3.083 | [3.07, 3.09] | 4.293 | 1728 |
| faiss | M1/M2 post-const / post | 0.740 | [0.73, 0.75] | 1.257 | 2160 |
| faiss | M3 separated / shared (post) | 0.855 | [0.84, 0.87] | 0.900 | 1080 |
| faiss | M4 padded / raw (post) | 6.651 | [6.53, 6.78] | 11.127 | 1728 |
| faiss | M3 separated / shared (post-const) | 0.965 | [0.96, 0.97] | 0.965 | 1080 |
| faiss | M4 padded / raw (post-const) | 7.745 | [7.73, 7.76] | 7.768 | 1728 |
| faiss | M3 separated / shared (pre) | 0.874 | [0.87, 0.87] | 0.869 | 1080 |
| faiss | M4 padded / raw (pre) | 1.332 | [1.33, 1.33] | 1.402 | 1728 |
| memory | M3 separated / shared (post) | 0.779 | [0.74, 0.81] | 0.835 | 60 |
| memory | M4 padded / raw (post) | 1.422 | [1.35, 1.49] | 1.546 | 96 |
| memory | M3 separated / shared (pre) | 0.946 | [0.94, 0.95] | 0.950 | 60 |
| memory | M4 padded / raw (pre) | 1.688 | [1.67, 1.71] | 1.683 | 96 |
| pgvector | M1/M2 post-const / post | 1.226 | [1.20, 1.25] | 3.432 | 2160 |
| pgvector | M1/M2 pre-exact / pre | 8.099 | [7.73, 8.48] | 6.475 | 2160 |
| pgvector | M3 separated / shared (bm25-pre) | 1.073 | [0.98, 1.18] | 0.953 | 1080 |
| pgvector | M4 padded / raw (bm25-pre) | 15.727 | [10.09, 26.74] | 57.570 | 1728 |
| pgvector | M3 separated / shared (post) | 0.862 | [0.85, 0.88] | 0.897 | 1080 |
| pgvector | M4 padded / raw (post) | 6.910 | [6.70, 7.14] | 18.390 | 1728 |
| pgvector | M3 separated / shared (post-const) | 0.947 | [0.94, 0.95] | 0.951 | 1080 |
| pgvector | M4 padded / raw (post-const) | 5.566 | [5.50, 5.63] | 5.568 | 1728 |
| pgvector | M3 separated / shared (pre) | 0.452 | [0.43, 0.47] | 0.794 | 1080 |
| pgvector | M4 padded / raw (pre) | 5.216 | [4.99, 5.46] | 9.501 | 1728 |
| pgvector | M3 separated / shared (pre-exact) | 0.592 | [0.57, 0.62] | 0.799 | 1080 |
| pgvector | M4 padded / raw (pre-exact) | 4.448 | [4.31, 4.59] | 10.642 | 1728 |
| qdrant | M1/M2 post-const / post | 1.052 | [1.03, 1.07] | 2.673 | 2160 |
| qdrant | M1/M2 pre-exact / pre | 1.525 | [1.52, 1.53] | 1.006 | 2160 |
| qdrant | M3 separated / shared (bm25-pre) | 0.964 | [0.96, 0.97] | 0.965 | 1080 |
| qdrant | M4 padded / raw (bm25-pre) | 27.148 | [26.59, 27.72] | 31.666 | 1728 |
| qdrant | M3 separated / shared (post) | 0.904 | [0.89, 0.92] | 0.976 | 1080 |
| qdrant | M4 padded / raw (post) | 6.402 | [6.23, 6.57] | 15.949 | 1728 |
| qdrant | M3 separated / shared (post-const) | 0.989 | [0.99, 0.99] | 0.989 | 1080 |
| qdrant | M4 padded / raw (post-const) | 4.234 | [4.20, 4.26] | 4.243 | 1728 |
| qdrant | M3 separated / shared (pre) | 0.967 | [0.97, 0.97] | 0.971 | 1080 |
| qdrant | M4 padded / raw (pre) | 2.215 | [2.21, 2.22] | 2.258 | 1728 |
| qdrant | M3 separated / shared (pre-exact) | 0.938 | [0.94, 0.94] | 0.944 | 1080 |
| qdrant | M4 padded / raw (pre-exact) | 20.124 | [20.09, 20.16] | 26.366 | 1728 |

## Id-list change rate, W1 against W0 (deterministic configurations)

| store | config | m | rate | interval | A/A rate | pairs |
|---|---|---|---|---|---|---|
| elasticsearch | bm25-pre | all | 1.000 | [1.00, 1.00] | 0.000 | 1080 |
| elasticsearch | bm25-pre | 1 | 1.000 | [1.00, 1.00] | 0.000 | 360 |
| elasticsearch | bm25-pre | 10 | 1.000 | [1.00, 1.00] | 0.000 | 360 |
| elasticsearch | bm25-pre | 100 | 1.000 | [1.00, 1.00] | 0.000 | 240 |
| elasticsearch | bm25-pre | 1000 | 1.000 | [1.00, 1.00] | 0.000 | 120 |
| elasticsearch | hybrid-exact | all | 0.308 | [0.28, 0.34] | 0.000 | 1080 |
| elasticsearch | hybrid-exact | 1 | 0.269 | [0.22, 0.32] | 0.000 | 360 |
| elasticsearch | hybrid-exact | 10 | 0.267 | [0.22, 0.32] | 0.000 | 360 |
| elasticsearch | hybrid-exact | 100 | 0.300 | [0.24, 0.36] | 0.000 | 240 |
| elasticsearch | hybrid-exact | 1000 | 0.567 | [0.48, 0.65] | 0.000 | 120 |
| elasticsearch | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 1080 |
| elasticsearch | pre-exact | 1 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| elasticsearch | pre-exact | 10 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| elasticsearch | pre-exact | 100 | 0.000 | [0.00, 0.00] | 0.000 | 240 |
| elasticsearch | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 120 |
| faiss | pre | all | 0.000 | [0.00, 0.00] | 0.000 | 1080 |
| faiss | pre | 1 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| faiss | pre | 10 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| faiss | pre | 100 | 0.000 | [0.00, 0.00] | 0.000 | 240 |
| faiss | pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 120 |
| memory | pre | all | 0.000 | [0.00, 0.00] | 0.000 | 60 |
| memory | pre | 1 | 0.000 | [0.00, 0.00] | 0.000 | 15 |
| memory | pre | 10 | 0.000 | [0.00, 0.00] | 0.000 | 15 |
| memory | pre | 100 | 0.000 | [0.00, 0.00] | 0.000 | 15 |
| memory | pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 15 |
| pgvector | bm25-pre | all | 0.002 | [0.00, 0.00] | 0.000 | 1080 |
| pgvector | bm25-pre | 1 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| pgvector | bm25-pre | 10 | 0.003 | [0.00, 0.01] | 0.000 | 360 |
| pgvector | bm25-pre | 100 | 0.004 | [0.00, 0.01] | 0.000 | 240 |
| pgvector | bm25-pre | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 120 |
| pgvector | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 1080 |
| pgvector | pre-exact | 1 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| pgvector | pre-exact | 10 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| pgvector | pre-exact | 100 | 0.000 | [0.00, 0.00] | 0.000 | 240 |
| pgvector | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 120 |
| qdrant | bm25-pre | all | 1.000 | [1.00, 1.00] | 0.000 | 1080 |
| qdrant | bm25-pre | 1 | 1.000 | [1.00, 1.00] | 0.000 | 360 |
| qdrant | bm25-pre | 10 | 1.000 | [1.00, 1.00] | 0.000 | 360 |
| qdrant | bm25-pre | 100 | 1.000 | [1.00, 1.00] | 0.000 | 240 |
| qdrant | bm25-pre | 1000 | 1.000 | [1.00, 1.00] | 0.000 | 120 |
| qdrant | pre-exact | all | 0.000 | [0.00, 0.00] | 0.000 | 1080 |
| qdrant | pre-exact | 1 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| qdrant | pre-exact | 10 | 0.000 | [0.00, 0.00] | 0.000 | 360 |
| qdrant | pre-exact | 100 | 0.000 | [0.00, 0.00] | 0.000 | 240 |
| qdrant | pre-exact | 1000 | 0.000 | [0.00, 0.00] | 0.000 | 120 |

## Every verdict part

| hypothesis | store | config | part | outcome | evidence |
|---|---|---|---|---|---|
| H1 | faiss | post | (a) m=1000 p=1 count >= 0.95 | confirmed | 1.000 [1.000, 1.000] (40 clusters, 5 seeds) |
| H1 | faiss | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 0.925 [0.863, 0.975] (40 clusters, 5 seeds) |
| H1 | faiss | post | (a) m=1000 p=50 count >= 0.95 | falsified | 0.688 [0.613, 0.762] (40 clusters, 5 seeds) |
| H1 | faiss | post | (b) m=100 p=10 latency >= 0.75 | confirmed | 0.850 [0.762, 0.925] (80 clusters, 5 seeds) |
| H1 | faiss | post | (b) m=100 p=50 latency >= 0.75 | confirmed | 0.975 [0.938, 1.000] (80 clusters, 5 seeds) |
| H1 | faiss | post | (c) m=1 no channel in latency | falsified | 0.667 [0.617, 0.717] (120 clusters, 5 seeds) |
| H1 | faiss | post | (c) m=1 no channel in count | confirmed | 0.500 [0.500, 0.500] (120 clusters, 5 seeds) |
| H1 | faiss | post | (c) m=1 no channel in complete | confirmed | 0.500 [0.500, 0.500] (120 clusters, 5 seeds) |
| H1 | faiss | post | (c) m=1 no channel in recall | confirmed | 0.500 [0.500, 0.500] (120 clusters, 5 seeds) |
| H1 | faiss | post | (c) m=1 no channel in score | confirmed | 0.500 [0.500, 0.500] (120 clusters, 5 seeds) |
| H1 | pgvector | post | (a) m=1000 p=1 count >= 0.95 | confirmed | 1.000 [1.000, 1.000] (40 clusters, 5 seeds) |
| H1 | pgvector | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 0.912 [0.850, 0.963] (40 clusters, 5 seeds) |
| H1 | pgvector | post | (a) m=1000 p=50 count >= 0.95 | falsified | 0.650 [0.588, 0.725] (40 clusters, 5 seeds) |
| H1 | pgvector | post | (b) m=100 p=10 latency >= 0.75 | inconclusive | 0.662 [0.550, 0.762] (80 clusters, 5 seeds) |
| H1 | pgvector | post | (b) m=100 p=50 latency >= 0.75 | confirmed | 0.950 [0.900, 0.988] (80 clusters, 5 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in latency | inconclusive | 0.369 [0.322, 0.417] (120 clusters, 5 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in count | confirmed | 0.499 [0.496, 0.500] (120 clusters, 5 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in complete | confirmed | 0.500 [0.500, 0.500] (120 clusters, 5 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in recall | confirmed | 0.496 [0.483, 0.507] (120 clusters, 5 seeds) |
| H1 | pgvector | post | (c) m=1 no channel in score | confirmed | 0.496 [0.482, 0.510] (120 clusters, 5 seeds) |
| H1 | qdrant | post | (a) m=1000 p=1 count >= 0.95 | confirmed | 1.000 [1.000, 1.000] (40 clusters, 5 seeds) |
| H1 | qdrant | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 0.925 [0.863, 0.975] (40 clusters, 5 seeds) |
| H1 | qdrant | post | (a) m=1000 p=50 count >= 0.95 | falsified | 0.688 [0.613, 0.762] (40 clusters, 5 seeds) |
| H1 | qdrant | post | (b) m=100 p=10 latency >= 0.75 | confirmed | 0.800 [0.713, 0.887] (80 clusters, 5 seeds) |
| H1 | qdrant | post | (b) m=100 p=50 latency >= 0.75 | confirmed | 0.950 [0.900, 0.988] (80 clusters, 5 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in latency | confirmed | 0.475 [0.419, 0.531] (120 clusters, 5 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in count | confirmed | 0.506 [0.497, 0.514] (120 clusters, 5 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in complete | confirmed | 0.500 [0.496, 0.504] (120 clusters, 5 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in recall | confirmed | 0.501 [0.483, 0.518] (120 clusters, 5 seeds) |
| H1 | qdrant | post | (c) m=1 no channel in score | confirmed | 0.487 [0.471, 0.504] (120 clusters, 5 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=1 count >= 0.95 | confirmed | 1.000 [1.000, 1.000] (40 clusters, 5 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=10 count >= 0.95 | inconclusive | 0.912 [0.850, 0.963] (40 clusters, 5 seeds) |
| H1 | elasticsearch | post | (a) m=1000 p=50 count >= 0.95 | falsified | 0.613 [0.550, 0.675] (40 clusters, 5 seeds) |
| H1 | elasticsearch | post | (b) m=100 p=10 latency >= 0.75 | confirmed | 0.825 [0.738, 0.900] (80 clusters, 5 seeds) |
| H1 | elasticsearch | post | (b) m=100 p=50 latency >= 0.75 | confirmed | 0.925 [0.863, 0.975] (80 clusters, 5 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in latency | confirmed | 0.481 [0.414, 0.544] (120 clusters, 5 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in count | confirmed | 0.503 [0.493, 0.512] (120 clusters, 5 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in complete | confirmed | 0.499 [0.494, 0.503] (120 clusters, 5 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in recall | confirmed | 0.508 [0.494, 0.524] (120 clusters, 5 seeds) |
| H1 | elasticsearch | post | (c) m=1 no channel in score | confirmed | 0.507 [0.485, 0.529] (120 clusters, 5 seeds) |
| H2 | faiss | post-const | (a) no latency channel pooled | confirmed | 0.517 [0.484, 0.549] (360 clusters, 5 seeds) |
| H2 | faiss | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.133 [0.075, 0.200] (40 clusters, 5 seeds) |
| H2 | faiss | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 0.925 [0.863, 0.975] (40 clusters, 5 seeds) |
| H2 | faiss | post-const | (b) m=1000 p=50 count >= 0.95 | falsified | 0.688 [0.613, 0.762] (40 clusters, 5 seeds) |
| H2 | pgvector | post-const | (a) no latency channel pooled | inconclusive | 0.188 [0.163, 0.214] (360 clusters, 5 seeds) |
| H2 | pgvector | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.017 [0.000, 0.050] (40 clusters, 5 seeds) |
| H2 | pgvector | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 0.912 [0.850, 0.963] (40 clusters, 5 seeds) |
| H2 | pgvector | post-const | (b) m=1000 p=50 count >= 0.95 | falsified | 0.650 [0.588, 0.725] (40 clusters, 5 seeds) |
| H2 | qdrant | post-const | (a) no latency channel pooled | confirmed | 0.456 [0.422, 0.491] (360 clusters, 5 seeds) |
| H2 | qdrant | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.350 [0.225, 0.483] (40 clusters, 5 seeds) |
| H2 | qdrant | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 0.925 [0.863, 0.975] (40 clusters, 5 seeds) |
| H2 | qdrant | post-const | (b) m=1000 p=50 count >= 0.95 | falsified | 0.688 [0.613, 0.762] (40 clusters, 5 seeds) |
| H2 | elasticsearch | post-const | (a) no latency channel pooled | inconclusive | 0.573 [0.536, 0.610] (360 clusters, 5 seeds) |
| H2 | elasticsearch | post-const | (a) m=1000 latency upper <= 0.65 | inconclusive | 0.625 [0.517, 0.725] (40 clusters, 5 seeds) |
| H2 | elasticsearch | post-const | (b) m=1000 p=10 count >= 0.95 | inconclusive | 0.912 [0.850, 0.963] (40 clusters, 5 seeds) |
| H2 | elasticsearch | post-const | (b) m=1000 p=50 count >= 0.95 | falsified | 0.613 [0.550, 0.675] (40 clusters, 5 seeds) |
| H3a | pgvector | pre | m=1000 p=10 latency >= 0.75 | confirmed | 1.000 [1.000, 1.000] (40 clusters, 5 seeds) |
| H3a | pgvector | pre | m=1000 p=50 latency >= 0.75 | confirmed | 1.000 [1.000, 1.000] (40 clusters, 5 seeds) |
| H3a | pgvector | pre | m=100 p=50 latency >= 0.75 | confirmed | 1.000 [1.000, 1.000] (80 clusters, 5 seeds) |
| H3b | elasticsearch | pre | m=1000 p=10 latency >= 0.75 | confirmed | 0.800 [0.675, 0.925] (40 clusters, 5 seeds) |
| H3b | elasticsearch | pre | m=1000 p=50 latency >= 0.75 | inconclusive | 0.613 [0.463, 0.750] (40 clusters, 5 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in latency | confirmed | 0.460 [0.424, 0.496] (360 clusters, 5 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in count | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in complete | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in recall | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H3c | qdrant | pre | p in (1, 10): no channel in score | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | no channel in latency pooled | inconclusive | 0.147 [0.123, 0.172] (360 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.125 [0.067, 0.192] (40 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | no channel in count pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | m=1000 count upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | no channel in complete pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | m=1000 complete upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | no channel in recall pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | m=1000 recall upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | no channel in score pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | pgvector | pre-exact | m=1000 score upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | no channel in latency pooled | confirmed | 0.461 [0.431, 0.490] (360 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.417 [0.325, 0.508] (40 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | no channel in count pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | m=1000 count upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | no channel in complete pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | m=1000 complete upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | no channel in recall pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | m=1000 recall upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | no channel in score pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | qdrant | pre-exact | m=1000 score upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | no channel in latency pooled | confirmed | 0.486 [0.450, 0.521] (360 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 latency upper <= 0.65 | inconclusive | 0.467 [0.367, 0.575] (40 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | no channel in count pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 count upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | no channel in complete pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 complete upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | no channel in recall pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 recall upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | no channel in score pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | elasticsearch | pre-exact | m=1000 score upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | faiss | pre | no channel in latency pooled | inconclusive | 0.276 [0.246, 0.306] (360 clusters, 5 seeds) |
| H4 | faiss | pre | m=1000 latency upper <= 0.65 | inconclusive | 0.350 [0.250, 0.450] (40 clusters, 5 seeds) |
| H4 | faiss | pre | no channel in count pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | faiss | pre | m=1000 count upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | faiss | pre | no channel in complete pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | faiss | pre | m=1000 complete upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | faiss | pre | no channel in recall pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | faiss | pre | m=1000 recall upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | faiss | pre | no channel in score pooled | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H4 | faiss | pre | m=1000 score upper <= 0.65 | confirmed | 0.500 [0.500, 0.500] (40 clusters, 5 seeds) |
| H4 | memory | pre | no channel in latency pooled | inconclusive | 0.383 [0.267, 0.500] (60 clusters, 5 seeds) |
| H4 | memory | pre | m=1000 latency upper <= 0.65 | inconclusive | 0.200 [0.000, 0.400] (15 clusters, 5 seeds) |
| H4 | memory | pre | no channel in count pooled | confirmed | 0.500 [0.500, 0.500] (60 clusters, 5 seeds) |
| H4 | memory | pre | m=1000 count upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (15 clusters, 5 seeds) |
| H4 | memory | pre | no channel in complete pooled | confirmed | 0.500 [0.500, 0.500] (60 clusters, 5 seeds) |
| H4 | memory | pre | m=1000 complete upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (15 clusters, 5 seeds) |
| H4 | memory | pre | no channel in score pooled | confirmed | 0.500 [0.500, 0.500] (60 clusters, 5 seeds) |
| H4 | memory | pre | m=1000 score upper <= 0.65 | inconclusive | 0.500 [0.500, 0.500] (15 clusters, 5 seeds) |
| H5a | elasticsearch | bm25-pre | m=1 score >= 0.90 | inconclusive | 0.794 [0.728, 0.858] (120 clusters, 5 seeds) |
| H5a | elasticsearch | bm25-pre | m=10 score >= 0.90 | inconclusive | 0.875 [0.819, 0.928] (120 clusters, 5 seeds) |
| H5a | elasticsearch | bm25-pre | m=100 score >= 0.90 | confirmed | 0.983 [0.954, 1.000] (80 clusters, 5 seeds) |
| H5a | elasticsearch | bm25-pre | m=1000 score >= 0.90 | confirmed | 0.992 [0.975, 1.000] (40 clusters, 5 seeds) |
| H5a | qdrant | bm25-pre | m=1 score >= 0.90 | inconclusive | 0.811 [0.744, 0.872] (120 clusters, 5 seeds) |
| H5a | qdrant | bm25-pre | m=10 score >= 0.90 | inconclusive | 0.886 [0.833, 0.933] (120 clusters, 5 seeds) |
| H5a | qdrant | bm25-pre | m=100 score >= 0.90 | confirmed | 0.979 [0.950, 1.000] (80 clusters, 5 seeds) |
| H5a | qdrant | bm25-pre | m=1000 score >= 0.90 | confirmed | 1.000 [1.000, 1.000] (40 clusters, 5 seeds) |
| H5b | pgvector | bm25-pre | no channel in the score | confirmed | 0.500 [0.500, 0.500] (360 clusters, 5 seeds) |
| H5b | pgvector | bm25-pre | id-list change rate <= 0.01 | confirmed | change rate 0.002 [0.000, 0.005] (360 clusters, 5 seeds) |
| H5c | elasticsearch | hybrid-exact | m=1000 change rate >= 0.25 | confirmed | change rate 0.567 [0.483, 0.650] (40 clusters, 5 seeds) |
| H6 | elasticsearch | post | m=1000 padded latency: no channel | inconclusive | raw 0.844 [0.781, 0.896] (32 clusters, 4 seeds); padded 0.500 [0.500, 0.500] (32 clusters, 4 seeds) |
| H6 | faiss | post | m=100 padded latency: no channel | inconclusive | raw 0.833 [0.786, 0.880] (64 clusters, 4 seeds); padded 0.500 [0.500, 0.500] (64 clusters, 4 seeds) |
| H6 | faiss | post | m=1000 padded latency: no channel | inconclusive | raw 0.781 [0.729, 0.833] (32 clusters, 4 seeds); padded 0.500 [0.500, 0.500] (32 clusters, 4 seeds) |
| H6 | pgvector | pre | m=100 padded latency: no channel | inconclusive | raw 0.807 [0.766, 0.849] (64 clusters, 4 seeds); padded 0.500 [0.500, 0.500] (64 clusters, 4 seeds) |
| H6 | pgvector | pre | m=1000 padded latency: no channel | inconclusive | raw 0.927 [0.875, 0.969] (32 clusters, 4 seeds); padded 0.500 [0.500, 0.500] (32 clusters, 4 seeds) |
| H6 | qdrant | post | m=100 padded latency: no channel | inconclusive | raw 0.755 [0.698, 0.812] (64 clusters, 4 seeds); padded 0.500 [0.500, 0.500] (64 clusters, 4 seeds) |
| H6 | qdrant | post | m=1000 padded latency: no channel | inconclusive | raw 0.781 [0.729, 0.833] (32 clusters, 4 seeds); padded 0.500 [0.500, 0.500] (32 clusters, 4 seeds) |

