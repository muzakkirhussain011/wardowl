# X3: filter-size scaling

957 records (0 unreadable lines), 200 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md.

## Health

| store | mode | seeds done | skipped | retrievals | errors | build s | setup error | seed errors | crashes (seed: status) |
|---|---|---|---|---|---|---|---|---|---|
| cassandra | smoke | [0] | [] | 42 | 0 | 14.400 | n/a | [] | {} |
| chroma | smoke | [] | [] | 27 | 9 | 4.600 | n/a | [] | {0: -11} |
| elasticsearch | smoke | [0] | [] | 42 | 0 | 6.300 | n/a | [] | {} |
| faiss | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] | {} |
| lancedb | smoke | [0] | [] | 42 | 0 | 0.700 | n/a | [] | {} |
| memory | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] | {} |
| milvus | smoke | [0] | [] | 42 | 0 | 7.900 | n/a | [] | {} |
| mongodb | smoke | [0] | [] | 42 | 0 | 3.000 | n/a | [] | {} |
| opensearch | smoke | [0] | [] | 42 | 0 | 6.800 | n/a | [] | {} |
| pgvector | smoke | [0] | [] | 42 | 0 | 3.400 | n/a | [] | {} |
| qdrant | smoke | [0] | [] | 42 | 0 | 10.800 | n/a | [] | {} |
| redis | smoke | [0] | [] | 42 | 0 | 1.300 | n/a | [] | {} |
| vespa | smoke | [0] | [] | 42 | 0 | 11.600 | n/a | [] | {} |
| weaviate | smoke | [0] | [] | 42 | 0 | 2.300 | n/a | [] | {} |

## Verdicts

| hypothesis | scope | outcome | evidence |
|---|---|---|---|
| X3-H1 | every store | inconclusive | 0 confirmed, 0 falsified, 84 inconclusive parts |
| X3-H2 | cassandra | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | chroma | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | elasticsearch | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | faiss | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | lancedb | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | memory | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | opensearch | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | pgvector | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H2 | qdrant | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H3a | pgvector | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H3b | faiss, memory | inconclusive | 0 confirmed, 0 falsified, 2 inconclusive parts |
| X3-H3c | cassandra | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | qdrant | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | elasticsearch | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | opensearch | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | redis | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | weaviate | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | milvus | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | mongodb | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | chroma | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | vespa | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |

## Levels

| store | G | outcome | ok share | p50 ms | p95 ms | p99 ms | recall | translation | translation ms | size | first error |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cassandra | 1 | accepts | 1.000 | 14.909 | 16.795 | 16.962 | 1.000 | ok | 0.048 | 19 |  |
| cassandra | 10 | accepts | 1.000 | 26.917 | 27.692 | 27.761 | 1.000 | ok | 0.167 | 20 |  |
| cassandra | 100 | accepts | 1.000 | 125 | 353 | 373 | 1.000 | ok | 1.223 | 21 |  |
| cassandra | 1000 | accepts | 1.000 | 116 | 116 | 116 | 1.000 | fallback | 5.731 | 39 |  |
| cassandra | 4000 | accepts | 1.000 | 117 | 117 | 117 | 1.000 | fallback | 18.858 | 39 |  |
| cassandra | 10000 | accepts | 1.000 | 113 | 145 | 148 | 1.000 | fallback | 48.406 | 39 |  |
| cassandra | 40000 | accepts | 1.000 | 254 | 258 | 259 | 1.000 | fallback | 154 | 39 |  |
| chroma | 1 | accepts | 1.000 | 448 | 451 | 451 | 1.000 | ok | 0.037 | 246 |  |
| chroma | 10 | accepts | 1.000 | 502 | 525 | 528 | 1.000 | ok | 0.038 | 727 |  |
| chroma | 100 | accepts | 1.000 | 872 | 872 | 872 | 1.000 | ok | 0.116 | 5879 |  |
| chroma | 1000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 1.019 | 60981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 4000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 4.317 | 249981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 10000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 11.579 | 647983 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 40000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 84.200 | 2657983 | the process crashed, exit status -11 |
| elasticsearch | 1 | accepts | 1.000 | 18.028 | 19.317 | 19.431 | 0.933 | ok | 0.032 | 203 |  |
| elasticsearch | 10 | accepts | 1.000 | 13.379 | 14.926 | 15.063 | 0.933 | ok | 0.057 | 484 |  |
| elasticsearch | 100 | accepts | 1.000 | 13.291 | 14.499 | 14.607 | 0.933 | ok | 0.069 | 3465 |  |
| elasticsearch | 1000 | accepts | 1.000 | 16.556 | 16.889 | 16.918 | 0.933 | ok | 1.040 | 35066 |  |
| elasticsearch | 4000 | accepts | 1.000 | 27.464 | 29.478 | 29.657 | 0.933 | ok | 4.894 | 143066 |  |
| elasticsearch | 10000 | accepts | 1.000 | 36.722 | 38.360 | 38.506 | 0.933 | ok | 10.187 | 369067 |  |
| elasticsearch | 40000 | accepts | 1.000 | 98.380 | 105 | 105 | 0.933 | ok | 40.111 | 1509067 |  |
| faiss | 1 | accepts | 1.000 | 27.445 | 27.565 | 27.576 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 10 | accepts | 1.000 | 27.886 | 27.946 | 27.951 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 100 | accepts | 1.000 | 27.758 | 28.217 | 28.258 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 1000 | accepts | 1.000 | 28.708 | 28.784 | 28.790 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 4000 | accepts | 1.000 | 33.278 | 33.404 | 33.415 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 10000 | accepts | 1.000 | 33.468 | 33.489 | 33.490 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 40000 | accepts | 1.000 | 50.623 | 50.740 | 50.751 | 1.000 | in-process | 0.001 | n/a |  |
| lancedb | 1 | accepts | 1.000 | 8.094 | 8.188 | 8.197 | 1.000 | ok | 0.029 | 208 |  |
| lancedb | 10 | accepts | 1.000 | 8.000 | 8.081 | 8.088 | 1.000 | ok | 0.043 | 644 |  |
| lancedb | 100 | accepts | 1.000 | 9.054 | 9.432 | 9.465 | 1.000 | ok | 0.103 | 5346 |  |
| lancedb | 1000 | accepts | 1.000 | 17.703 | 18.352 | 18.410 | 1.000 | ok | 0.922 | 55948 |  |
| lancedb | 4000 | accepts | 1.000 | 44.456 | 45.032 | 45.083 | 1.000 | ok | 4.463 | 229948 |  |
| lancedb | 10000 | accepts | 1.000 | 95.628 | 99.400 | 99.735 | 1.000 | ok | 12.407 | 597950 |  |
| lancedb | 40000 | accepts | 1.000 | 382 | 387 | 387 | 1.000 | ok | 52.972 | 2457950 |  |
| memory | 1 | accepts | 1.000 | 27.586 | 27.881 | 27.907 | n/a | in-process | 0.002 | n/a |  |
| memory | 10 | accepts | 1.000 | 27.679 | 27.907 | 27.927 | n/a | in-process | 0.001 | n/a |  |
| memory | 100 | accepts | 1.000 | 27.701 | 27.824 | 27.835 | n/a | in-process | 0.001 | n/a |  |
| memory | 1000 | accepts | 1.000 | 28.707 | 28.716 | 28.717 | n/a | in-process | 0.001 | n/a |  |
| memory | 4000 | accepts | 1.000 | 30.649 | 30.707 | 30.712 | n/a | in-process | 0.001 | n/a |  |
| memory | 10000 | accepts | 1.000 | 33.212 | 33.539 | 33.568 | n/a | in-process | 0.001 | n/a |  |
| memory | 40000 | accepts | 1.000 | 50.418 | 51.478 | 51.572 | n/a | in-process | 0.001 | n/a |  |
| milvus | 1 | accepts | 1.000 | 3.044 | 3.128 | 3.135 | 0.867 | ok | 0.030 | 196 |  |
| milvus | 10 | accepts | 1.000 | 2.916 | 3.075 | 3.089 | 0.867 | ok | 0.029 | 477 |  |
| milvus | 100 | accepts | 1.000 | 3.037 | 3.097 | 3.102 | 0.867 | ok | 0.084 | 3458 |  |
| milvus | 1000 | accepts | 1.000 | 5.260 | 5.280 | 5.282 | 0.867 | ok | 0.657 | 35059 |  |
| milvus | 4000 | accepts | 1.000 | 13.392 | 13.940 | 13.989 | 0.867 | ok | 2.581 | 143059 |  |
| milvus | 10000 | accepts | 1.000 | 29.704 | 29.926 | 29.946 | 0.867 | ok | 7.700 | 369060 |  |
| milvus | 40000 | accepts | 1.000 | 102 | 114 | 115 | 0.867 | ok | 36.432 | 1509060 |  |
| mongodb | 1 | accepts | 1.000 | 4.215 | 4.878 | 4.937 | 1.000 | ok | 0.022 | 159 |  |
| mongodb | 10 | accepts | 1.000 | 5.611 | 5.867 | 5.890 | 1.000 | ok | 0.017 | 440 |  |
| mongodb | 100 | accepts | 1.000 | 5.539 | 6.467 | 6.549 | 1.000 | ok | 0.059 | 3421 |  |
| mongodb | 1000 | accepts | 1.000 | 9.326 | 10.019 | 10.080 | 1.000 | ok | 0.379 | 35022 |  |
| mongodb | 4000 | accepts | 1.000 | 20.157 | 32.366 | 33.451 | 1.000 | ok | 1.989 | 143022 |  |
| mongodb | 10000 | accepts | 1.000 | 32.009 | 34.855 | 35.108 | 1.000 | ok | 8.572 | 369023 |  |
| mongodb | 40000 | accepts | 1.000 | 91.730 | 113 | 115 | 1.000 | ok | 24.174 | 1509023 |  |
| opensearch | 1 | accepts | 1.000 | 12.508 | 15.246 | 15.490 | 1.000 | ok | 0.036 | 203 |  |
| opensearch | 10 | accepts | 1.000 | 14.633 | 16.146 | 16.281 | 1.000 | ok | 0.036 | 484 |  |
| opensearch | 100 | accepts | 1.000 | 14.608 | 16.280 | 16.429 | 1.000 | ok | 0.107 | 3465 |  |
| opensearch | 1000 | accepts | 1.000 | 18.081 | 20.009 | 20.181 | 1.000 | ok | 1.143 | 35066 |  |
| opensearch | 4000 | accepts | 1.000 | 22.303 | 23.584 | 23.698 | 1.000 | ok | 4.710 | 143066 |  |
| opensearch | 10000 | accepts | 1.000 | 27.098 | 30.459 | 30.757 | 1.000 | ok | 12.328 | 369067 |  |
| opensearch | 40000 | accepts | 1.000 | 87.309 | 91.270 | 91.623 | 1.000 | ok | 40.633 | 1509067 |  |
| pgvector | 1 | accepts | 1.000 | 2.370 | 2.847 | 2.889 | 1.000 | ok | 0.052 | 368 |  |
| pgvector | 10 | accepts | 1.000 | 2.802 | 3.516 | 3.580 | 1.000 | ok | 0.078 | 1470 |  |
| pgvector | 100 | accepts | 1.000 | 3.715 | 4.902 | 5.007 | 1.000 | ok | 0.282 | 3453 |  |
| pgvector | 1000 | accepts | 1.000 | 18.873 | 28.260 | 29.094 | 1.000 | ok | 2.652 | 36055 |  |
| pgvector | 4000 | accepts | 1.000 | 71.635 | 125 | 130 | 1.000 | ok | 11.503 | 150055 |  |
| pgvector | 10000 | accepts | 1.000 | 173 | 252 | 259 | 1.000 | ok | 29.180 | 398057 |  |
| pgvector | 40000 | accepts | 1.000 | 708 | 1027 | 1055 | 1.000 | ok | 124 | 1658057 |  |
| qdrant | 1 | accepts | 1.000 | 1.489 | 1.559 | 1.565 | 1.000 | ok | 0.094 | 433 |  |
| qdrant | 10 | accepts | 1.000 | 1.734 | 3.576 | 3.739 | 1.000 | ok | 0.038 | 507 |  |
| qdrant | 100 | accepts | 1.000 | 1.597 | 1.601 | 1.601 | 1.000 | ok | 0.131 | 1418 |  |
| qdrant | 1000 | accepts | 1.000 | 2.465 | 2.508 | 2.512 | 1.000 | ok | 0.495 | 12319 |  |
| qdrant | 4000 | accepts | 1.000 | 5.505 | 5.574 | 5.580 | 1.000 | ok | 1.898 | 51319 |  |
| qdrant | 10000 | accepts | 1.000 | 12.735 | 12.918 | 12.935 | 1.000 | ok | 5.091 | 139320 |  |
| qdrant | 40000 | accepts | 1.000 | 55.676 | 55.927 | 55.949 | 1.000 | ok | 22.885 | 589320 |  |
| redis | 1 | accepts | 1.000 | 2.122 | 4.188 | 4.372 | 1.000 | ok | 0.034 | 172 |  |
| redis | 10 | accepts | 1.000 | 1.846 | 2.113 | 2.137 | 1.000 | ok | 0.044 | 599 |  |
| redis | 100 | accepts | 1.000 | 1.360 | 1.378 | 1.379 | 1.000 | ok | 0.179 | 5211 |  |
| redis | 1000 | accepts | 1.000 | 3.785 | 3.811 | 3.813 | 1.000 | ok | 0.821 | 54913 |  |
| redis | 4000 | accepts | 1.000 | 11.604 | 11.835 | 11.856 | 1.000 | ok | 3.920 | 225913 |  |
| redis | 10000 | accepts | 1.000 | 28.345 | 28.396 | 28.401 | 1.000 | ok | 11.968 | 587915 |  |
| redis | 40000 | accepts | 1.000 | 120 | 120 | 120 | 1.000 | ok | 58.527 | 2417915 |  |
| vespa | 1 | accepts | 1.000 | 8.562 | 9.813 | 9.924 | 0.933 | ok | 0.027 | 186 |  |
| vespa | 10 | accepts | 1.000 | 6.921 | 7.010 | 7.018 | 0.933 | ok | 0.028 | 640 |  |
| vespa | 100 | accepts | 1.000 | 9.306 | 10.802 | 10.935 | 0.933 | ok | 0.071 | 5522 |  |
| vespa | 1000 | accepts | 1.000 | 13.173 | 15.860 | 16.098 | 0.933 | ok | 0.568 | 57924 |  |
| vespa | 4000 | accepts | 1.000 | 21.524 | 25.113 | 25.432 | 0.933 | ok | 2.783 | 237924 |  |
| vespa | 10000 | accepts | 1.000 | 41.850 | 43.790 | 43.962 | 0.933 | ok | 6.662 | 617926 |  |
| vespa | 40000 | accepts | 1.000 | 144 | 145 | 145 | 0.933 | ok | 28.857 | 2537926 |  |
| weaviate | 1 | accepts | 1.000 | 1.447 | 1.504 | 1.509 | 1.000 | ok | 0.149 | 75 |  |
| weaviate | 10 | accepts | 1.000 | 1.569 | 1.639 | 1.645 | 1.000 | ok | 0.083 | 75 |  |
| weaviate | 100 | accepts | 1.000 | 2.218 | 2.293 | 2.299 | 1.000 | ok | 0.152 | 75 |  |
| weaviate | 1000 | accepts | 1.000 | 14.434 | 19.833 | 20.313 | 1.000 | ok | 0.738 | 75 |  |
| weaviate | 4000 | accepts | 1.000 | 25.845 | 25.989 | 26.002 | 1.000 | ok | 2.933 | 75 |  |
| weaviate | 10000 | accepts | 1.000 | 56.925 | 58.425 | 58.558 | 1.000 | ok | 8.096 | 75 |  |
| weaviate | 40000 | accepts | 1.000 | 241 | 250 | 251 | 1.000 | ok | 42.446 | 75 |  |

## Latency ratios (p50, paired by query)

| store | G top | G bottom | ratio | interval | pairs |
|---|---|---|---|---|---|
| pgvector | 40000 | 1 | 299 | [275.49, 366.30] | 3 |
| faiss | 40000 | 1 | 1.845 | [1.78, 1.85] | 3 |
| memory | 40000 | 1 | 1.828 | [1.82, 1.85] | 3 |
| cassandra | 100 | 1000 | 1.077 | [1.07, 3.25] | 3 |
| cassandra | 40000 | 1 | 17.034 | [14.22, 18.42] | 3 |
| elasticsearch | 40000 | 1 | 5.457 | [5.04, 5.85] | 3 |
| lancedb | 40000 | 1 | 47.161 | [45.02, 49.95] | 3 |
| milvus | 40000 | 1 | 33.378 | [32.22, 39.67] | 3 |
| mongodb | 40000 | 1 | 21.763 | [19.62, 23.28] | 3 |
| opensearch | 40000 | 1 | 6.980 | [5.90, 8.01] | 3 |
| qdrant | 40000 | 1 | 37.384 | [33.81, 37.57] | 3 |
| redis | 40000 | 1 | 56.405 | [27.15, 75.97] | 3 |
| vespa | 40000 | 1 | 16.865 | [14.00, 17.04] | 3 |
| weaviate | 40000 | 1 | 167 | [159.63, 181.19] | 3 |

## Recall differences (paired by query)

| store | G top | G bottom | difference | interval | pairs |
|---|---|---|---|---|---|
| qdrant | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| elasticsearch | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| opensearch | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| redis | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| weaviate | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| milvus | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| mongodb | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| vespa | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| pgvector | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |
| cassandra | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 3 |

## Every verdict part

| hypothesis | store | part | outcome | evidence |
|---|---|---|---|---|
| X3-H1 | cassandra | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | cassandra | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | cassandra | G=100 | inconclusive | 1 seeds, status ['ok'], median 1.2 ms |
| X3-H1 | cassandra | G=1000 | inconclusive | 1 seeds, status ['fallback'], median 5.7 ms |
| X3-H1 | cassandra | G=4000 | inconclusive | 1 seeds, status ['fallback'], median 18.9 ms |
| X3-H1 | cassandra | G=10000 | inconclusive | 1 seeds, status ['fallback'], median 48.4 ms |
| X3-H1 | cassandra | G=40000 | inconclusive | 1 seeds, status ['fallback'], median 154.3 ms |
| X3-H1 | chroma | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | chroma | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.0 ms |
| X3-H1 | chroma | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.3 ms |
| X3-H1 | chroma | G=10000 | inconclusive | 1 seeds, status ['ok'], median 11.6 ms |
| X3-H1 | chroma | G=40000 | inconclusive | 1 seeds, status ['ok'], median 84.2 ms |
| X3-H1 | elasticsearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | elasticsearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | elasticsearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.0 ms |
| X3-H1 | elasticsearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.9 ms |
| X3-H1 | elasticsearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 10.2 ms |
| X3-H1 | elasticsearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 40.1 ms |
| X3-H1 | lancedb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | lancedb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | lancedb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.5 ms |
| X3-H1 | lancedb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 12.4 ms |
| X3-H1 | lancedb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 53.0 ms |
| X3-H1 | milvus | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | milvus | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | milvus | G=4000 | inconclusive | 1 seeds, status ['ok'], median 2.6 ms |
| X3-H1 | milvus | G=10000 | inconclusive | 1 seeds, status ['ok'], median 7.7 ms |
| X3-H1 | milvus | G=40000 | inconclusive | 1 seeds, status ['ok'], median 36.4 ms |
| X3-H1 | mongodb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | mongodb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.4 ms |
| X3-H1 | mongodb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 2.0 ms |
| X3-H1 | mongodb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 8.6 ms |
| X3-H1 | mongodb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 24.2 ms |
| X3-H1 | opensearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | opensearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.1 ms |
| X3-H1 | opensearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.7 ms |
| X3-H1 | opensearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 12.3 ms |
| X3-H1 | opensearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 40.6 ms |
| X3-H1 | pgvector | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | pgvector | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | pgvector | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.3 ms |
| X3-H1 | pgvector | G=1000 | inconclusive | 1 seeds, status ['ok'], median 2.7 ms |
| X3-H1 | pgvector | G=4000 | inconclusive | 1 seeds, status ['ok'], median 11.5 ms |
| X3-H1 | pgvector | G=10000 | inconclusive | 1 seeds, status ['ok'], median 29.2 ms |
| X3-H1 | pgvector | G=40000 | inconclusive | 1 seeds, status ['ok'], median 124.0 ms |
| X3-H1 | qdrant | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | qdrant | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.5 ms |
| X3-H1 | qdrant | G=4000 | inconclusive | 1 seeds, status ['ok'], median 1.9 ms |
| X3-H1 | qdrant | G=10000 | inconclusive | 1 seeds, status ['ok'], median 5.1 ms |
| X3-H1 | qdrant | G=40000 | inconclusive | 1 seeds, status ['ok'], median 22.9 ms |
| X3-H1 | redis | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | redis | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.8 ms |
| X3-H1 | redis | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.9 ms |
| X3-H1 | redis | G=10000 | inconclusive | 1 seeds, status ['ok'], median 12.0 ms |
| X3-H1 | redis | G=40000 | inconclusive | 1 seeds, status ['ok'], median 58.5 ms |
| X3-H1 | vespa | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | vespa | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.6 ms |
| X3-H1 | vespa | G=4000 | inconclusive | 1 seeds, status ['ok'], median 2.8 ms |
| X3-H1 | vespa | G=10000 | inconclusive | 1 seeds, status ['ok'], median 6.7 ms |
| X3-H1 | vespa | G=40000 | inconclusive | 1 seeds, status ['ok'], median 28.9 ms |
| X3-H1 | weaviate | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | weaviate | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | weaviate | G=4000 | inconclusive | 1 seeds, status ['ok'], median 2.9 ms |
| X3-H1 | weaviate | G=10000 | inconclusive | 1 seeds, status ['ok'], median 8.1 ms |
| X3-H1 | weaviate | G=40000 | inconclusive | 1 seeds, status ['ok'], median 42.4 ms |
| X3-H2 | cassandra | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | chroma | G=40,000 predicted refuses | inconclusive | observed refuses in 1 seeds, ok share nan, first error the process crashed, exit status -11 |
| X3-H2 | elasticsearch | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | faiss | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | lancedb | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | memory | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | milvus | G=40,000 (no prediction) | reported | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | mongodb | G=40,000 (no prediction) | reported | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | opensearch | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | pgvector | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | qdrant | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | redis | G=40,000 (no prediction) | reported | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | vespa | G=40,000 (no prediction) | reported | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | weaviate | G=40,000 (no prediction) | reported | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H3a | pgvector | p50 G=40,000 / G=1 | inconclusive | {'store': 'pgvector', 'top': 40000, 'bottom': 1, 'ratio': 298.75782634376844, 'lo': 275.49156189351106, 'hi': 366.29528604434637, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 708.1158, 'p50_bottom_ms': 2.3702} |
| X3-H3b | faiss | p50 G=40,000 / G=1 | inconclusive | {'store': 'faiss', 'top': 40000, 'bottom': 1, 'ratio': 1.8445265474472767, 'lo': 1.777437742033736, 'hi': 1.8492559719003687, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 50.6234, 'p50_bottom_ms': 27.4452} |
| X3-H3b | memory | p50 G=40,000 / G=1 | inconclusive | {'store': 'memory', 'top': 40000, 'bottom': 1, 'ratio': 1.827660831644693, 'lo': 1.8195398984608535, 'hi': 1.8484143929840653, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 50.4184, 'p50_bottom_ms': 27.5863} |
| X3-H3c | cassandra | p50 G=100 / G=1,000 | inconclusive | {'store': 'cassandra', 'top': 100, 'bottom': 1000, 'ratio': 1.0772598829938227, 'lo': 1.0728865683897406, 'hi': 3.2468364433480272, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 125.1581, 'p50_bottom_ms': 116.1819} |
| X3-H4 | qdrant | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-H4 | elasticsearch | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-H4 | opensearch | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-H4 | redis | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-H4 | weaviate | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-H4 | milvus | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-H4 | mongodb | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-H4 | chroma | recall | inconclusive | no accepted level pair |
| X3-H4 | vespa | G=40,000 vs G=1 | inconclusive | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 3 queries |
| X3-sanity | faiss | G=1 recall is 1 | passed | 1.0000 |
| X3-sanity | faiss | G=10 recall is 1 | passed | 1.0000 |
| X3-sanity | faiss | G=100 recall is 1 | passed | 1.0000 |
| X3-sanity | faiss | G=1000 recall is 1 | passed | 1.0000 |
| X3-sanity | faiss | G=4000 recall is 1 | passed | 1.0000 |
| X3-sanity | faiss | G=10000 recall is 1 | passed | 1.0000 |
| X3-sanity | faiss | G=40000 recall is 1 | passed | 1.0000 |
| X3-sanity | lancedb | G=1 recall is 1 | passed | 1.0000 |
| X3-sanity | lancedb | G=10 recall is 1 | passed | 1.0000 |
| X3-sanity | lancedb | G=100 recall is 1 | passed | 1.0000 |
| X3-sanity | lancedb | G=1000 recall is 1 | passed | 1.0000 |
| X3-sanity | lancedb | G=4000 recall is 1 | passed | 1.0000 |
| X3-sanity | lancedb | G=10000 recall is 1 | passed | 1.0000 |
| X3-sanity | lancedb | G=40000 recall is 1 | passed | 1.0000 |

