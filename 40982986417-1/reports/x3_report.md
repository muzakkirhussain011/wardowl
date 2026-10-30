# X3: filter-size scaling

57,462 records (0 unreadable lines), 10,000 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md.

## Health

| store | mode | seeds done | skipped | retrievals | errors | build s | setup error | seed errors | crashes (seed: status) |
|---|---|---|---|---|---|---|---|---|---|
| cassandra | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 209 | n/a | [] | {} |
| chroma | full | [] | [3, 4] | 1050 | 450 | 136 | n/a | [] | {3: -11, 4: -11, 0: -11, 1: -11, 2: -11} |
| elasticsearch | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 55.900 | n/a | [] | {} |
| faiss | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 1.300 | n/a | [] | {} |
| lancedb | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 9.800 | n/a | [] | {} |
| memory | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 1.100 | n/a | [] | {} |
| milvus | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 43.200 | n/a | [] | {} |
| mongodb | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 37.100 | n/a | [] | {} |
| opensearch | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 70.500 | n/a | [] | {} |
| pgvector | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 42.000 | n/a | [] | {} |
| qdrant | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 78.200 | n/a | [] | {} |
| redis | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 23.900 | n/a | [] | {} |
| vespa | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 207 | n/a | [] | {} |
| weaviate | full | [0, 1, 2, 3, 4] | [] | 4200 | 0 | 47.300 | n/a | [] | {} |

## Verdicts

| hypothesis | scope | outcome | evidence |
|---|---|---|---|
| X3-H1 | every store | confirmed | 84 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | cassandra | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | chroma | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | elasticsearch | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | faiss | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | lancedb | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | memory | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | opensearch | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | pgvector | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H2 | qdrant | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H3a | pgvector | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H3b | faiss, memory | confirmed | 2 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H3c | cassandra | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | qdrant | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | elasticsearch | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | opensearch | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | redis | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | weaviate | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | milvus | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | mongodb | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |
| X3-H4 | chroma | inconclusive | 0 confirmed, 0 falsified, 1 inconclusive parts |
| X3-H4 | vespa | confirmed | 1 confirmed, 0 falsified, 0 inconclusive parts |

## Levels

| store | G | outcome | ok share | p50 ms | p95 ms | p99 ms | recall | translation | translation ms | size | first error |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cassandra | 1 | accepts | 1.000 | 109 | 133 | 138 | 0.996 | ok | 0.021 | 19 |  |
| cassandra | 10 | accepts | 1.000 | 42.199 | 48.032 | 51.952 | 1.000 | ok | 0.076 | 20 |  |
| cassandra | 100 | accepts | 1.000 | 166 | 222 | 231 | 1.000 | ok | 1.299 | 21 |  |
| cassandra | 1000 | accepts | 1.000 | 90.707 | 97.082 | 99.488 | 1.000 | fallback | 4.208 | 39 |  |
| cassandra | 4000 | accepts | 1.000 | 100 | 124 | 126 | 1.000 | fallback | 11.265 | 39 |  |
| cassandra | 10000 | accepts | 1.000 | 124 | 152 | 154 | 1.000 | fallback | 29.999 | 39 |  |
| cassandra | 40000 | accepts | 1.000 | 308 | 321 | 330 | 1.000 | fallback | 197 | 39 |  |
| chroma | 1 | accepts | 1.000 | 4340 | 4401 | 4436 | 1.000 | ok | 0.012 | 246 |  |
| chroma | 10 | accepts | 1.000 | 5005 | 5110 | 5137 | 1.000 | ok | 0.025 | 727 |  |
| chroma | 100 | accepts | 1.000 | 10627 | 10802 | 10818 | 1.000 | ok | 0.124 | 5879 |  |
| chroma | 1000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 1.070 | 60981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 4000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 4.443 | 249981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 10000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 12.015 | 647983 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 40000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 101 | 2657983 | the process crashed, exit status -11 |
| elasticsearch | 1 | accepts | 1.000 | 3.358 | 3.726 | 3.784 | 0.939 | ok | 0.009 | 203 |  |
| elasticsearch | 10 | accepts | 1.000 | 2.728 | 3.532 | 3.619 | 0.939 | ok | 0.012 | 484 |  |
| elasticsearch | 100 | accepts | 1.000 | 2.782 | 3.389 | 3.502 | 0.939 | ok | 0.068 | 3465 |  |
| elasticsearch | 1000 | accepts | 1.000 | 3.954 | 4.503 | 4.785 | 0.939 | ok | 0.513 | 35066 |  |
| elasticsearch | 4000 | accepts | 1.000 | 8.734 | 10.391 | 11.533 | 0.939 | ok | 2.426 | 143066 |  |
| elasticsearch | 10000 | accepts | 1.000 | 19.345 | 20.678 | 23.245 | 0.939 | ok | 6.388 | 369067 |  |
| elasticsearch | 40000 | accepts | 1.000 | 78.798 | 80.103 | 82.322 | 0.939 | ok | 31.152 | 1509067 |  |
| faiss | 1 | accepts | 1.000 | 385 | 395 | 398 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 10 | accepts | 1.000 | 391 | 401 | 404 | 1.000 | in-process | 0.000 | n/a |  |
| faiss | 100 | accepts | 1.000 | 390 | 404 | 407 | 1.000 | in-process | 0.000 | n/a |  |
| faiss | 1000 | accepts | 1.000 | 403 | 413 | 418 | 1.000 | in-process | 0.000 | n/a |  |
| faiss | 4000 | accepts | 1.000 | 416 | 426 | 436 | 1.000 | in-process | 0.000 | n/a |  |
| faiss | 10000 | accepts | 1.000 | 424 | 433 | 436 | 1.000 | in-process | 0.000 | n/a |  |
| faiss | 40000 | accepts | 1.000 | 454 | 488 | 510 | 1.000 | in-process | 0.000 | n/a |  |
| lancedb | 1 | accepts | 1.000 | 53.627 | 55.730 | 57.436 | 1.000 | ok | 0.012 | 208 |  |
| lancedb | 10 | accepts | 1.000 | 54.726 | 61.319 | 62.823 | 1.000 | ok | 0.018 | 644 |  |
| lancedb | 100 | accepts | 1.000 | 56.967 | 61.840 | 62.994 | 1.000 | ok | 0.114 | 5346 |  |
| lancedb | 1000 | accepts | 1.000 | 66.287 | 68.681 | 69.972 | 1.000 | ok | 0.891 | 55948 |  |
| lancedb | 4000 | accepts | 1.000 | 94.574 | 96.264 | 97.894 | 1.000 | ok | 4.005 | 229948 |  |
| lancedb | 10000 | accepts | 1.000 | 149 | 152 | 156 | 1.000 | ok | 10.912 | 597950 |  |
| lancedb | 40000 | accepts | 1.000 | 424 | 440 | 457 | 1.000 | ok | 49.352 | 2457950 |  |
| memory | 1 | accepts | 1.000 | 432 | 494 | 523 | n/a | in-process | 0.001 | n/a |  |
| memory | 10 | accepts | 1.000 | 438 | 492 | 530 | n/a | in-process | 0.000 | n/a |  |
| memory | 100 | accepts | 1.000 | 439 | 499 | 535 | n/a | in-process | 0.000 | n/a |  |
| memory | 1000 | accepts | 1.000 | 451 | 508 | 547 | n/a | in-process | 0.000 | n/a |  |
| memory | 4000 | accepts | 1.000 | 465 | 522 | 556 | n/a | in-process | 0.000 | n/a |  |
| memory | 10000 | accepts | 1.000 | 475 | 535 | 571 | n/a | in-process | 0.000 | n/a |  |
| memory | 40000 | accepts | 1.000 | 503 | 597 | 614 | n/a | in-process | 0.000 | n/a |  |
| milvus | 1 | accepts | 1.000 | 4.849 | 5.257 | 5.384 | 0.987 | ok | 0.010 | 196 |  |
| milvus | 10 | accepts | 1.000 | 4.240 | 4.705 | 4.780 | 0.987 | ok | 0.014 | 477 |  |
| milvus | 100 | accepts | 1.000 | 4.305 | 4.755 | 5.124 | 0.987 | ok | 0.059 | 3458 |  |
| milvus | 1000 | accepts | 1.000 | 7.532 | 8.514 | 8.695 | 0.988 | ok | 0.491 | 35059 |  |
| milvus | 4000 | accepts | 1.000 | 18.640 | 21.218 | 25.036 | 0.989 | ok | 2.320 | 143059 |  |
| milvus | 10000 | accepts | 1.000 | 35.199 | 39.765 | 43.559 | 0.996 | ok | 6.824 | 369060 |  |
| milvus | 40000 | accepts | 1.000 | 127 | 142 | 147 | 0.999 | ok | 33.824 | 1509060 |  |
| mongodb | 1 | accepts | 1.000 | 10.474 | 12.595 | 13.308 | 1.000 | ok | 0.009 | 159 |  |
| mongodb | 10 | accepts | 1.000 | 10.627 | 11.437 | 13.516 | 1.000 | ok | 0.016 | 440 |  |
| mongodb | 100 | accepts | 1.000 | 9.754 | 10.345 | 10.421 | 1.000 | ok | 0.062 | 3421 |  |
| mongodb | 1000 | accepts | 1.000 | 12.092 | 13.482 | 14.788 | 1.000 | ok | 0.628 | 35022 |  |
| mongodb | 4000 | accepts | 1.000 | 21.896 | 23.119 | 26.271 | 1.000 | ok | 2.993 | 143022 |  |
| mongodb | 10000 | accepts | 1.000 | 41.668 | 44.914 | 45.975 | 1.000 | ok | 8.268 | 369023 |  |
| mongodb | 40000 | accepts | 1.000 | 142 | 151 | 152 | 1.000 | ok | 37.665 | 1509023 |  |
| opensearch | 1 | accepts | 1.000 | 6.062 | 7.338 | 7.886 | 1.000 | ok | 0.010 | 203 |  |
| opensearch | 10 | accepts | 1.000 | 6.377 | 7.342 | 7.679 | 1.000 | ok | 0.014 | 484 |  |
| opensearch | 100 | accepts | 1.000 | 6.269 | 7.520 | 7.651 | 1.000 | ok | 0.081 | 3465 |  |
| opensearch | 1000 | accepts | 1.000 | 7.627 | 8.836 | 9.157 | 1.000 | ok | 0.502 | 35066 |  |
| opensearch | 4000 | accepts | 1.000 | 10.862 | 13.988 | 14.474 | 1.000 | ok | 2.434 | 143066 |  |
| opensearch | 10000 | accepts | 1.000 | 20.171 | 22.742 | 23.566 | 1.000 | ok | 6.749 | 369067 |  |
| opensearch | 40000 | accepts | 1.000 | 71.605 | 73.263 | 78.552 | 1.000 | ok | 31.603 | 1509067 |  |
| pgvector | 1 | accepts | 1.000 | 2.860 | 3.990 | 4.137 | 0.967 | ok | 0.027 | 368 |  |
| pgvector | 10 | accepts | 1.000 | 3.590 | 4.477 | 4.705 | 0.967 | ok | 0.067 | 1470 |  |
| pgvector | 100 | accepts | 1.000 | 4.509 | 5.873 | 5.956 | 0.967 | ok | 0.286 | 3453 |  |
| pgvector | 1000 | accepts | 1.000 | 22.195 | 28.108 | 28.368 | 0.967 | ok | 2.673 | 36055 |  |
| pgvector | 4000 | accepts | 1.000 | 81.323 | 102 | 105 | 0.967 | ok | 11.207 | 150055 |  |
| pgvector | 10000 | accepts | 1.000 | 201 | 248 | 254 | 0.967 | ok | 29.099 | 398057 |  |
| pgvector | 40000 | accepts | 1.000 | 797 | 989 | 1013 | 0.967 | ok | 120 | 1658057 |  |
| qdrant | 1 | accepts | 1.000 | 3.495 | 4.091 | 4.149 | 0.999 | ok | 0.026 | 433 |  |
| qdrant | 10 | accepts | 1.000 | 4.295 | 4.540 | 4.719 | 0.999 | ok | 0.034 | 507 |  |
| qdrant | 100 | accepts | 1.000 | 4.355 | 4.797 | 4.808 | 0.999 | ok | 0.081 | 1418 |  |
| qdrant | 1000 | accepts | 1.000 | 6.297 | 6.934 | 7.061 | 0.999 | ok | 0.515 | 12319 |  |
| qdrant | 4000 | accepts | 1.000 | 13.250 | 14.061 | 14.336 | 0.999 | ok | 2.354 | 51319 |  |
| qdrant | 10000 | accepts | 1.000 | 27.332 | 28.671 | 29.334 | 0.999 | ok | 6.385 | 139320 |  |
| qdrant | 40000 | accepts | 1.000 | 101 | 108 | 109 | 0.999 | ok | 34.829 | 589320 |  |
| redis | 1 | accepts | 1.000 | 1.189 | 4.783 | 5.838 | 0.969 | ok | 0.018 | 172 |  |
| redis | 10 | accepts | 1.000 | 1.244 | 4.115 | 6.151 | 0.969 | ok | 0.027 | 599 |  |
| redis | 100 | accepts | 1.000 | 1.752 | 4.986 | 7.136 | 0.969 | ok | 0.122 | 5211 |  |
| redis | 1000 | accepts | 1.000 | 4.882 | 9.579 | 11.897 | 0.969 | ok | 0.844 | 54913 |  |
| redis | 4000 | accepts | 1.000 | 14.370 | 21.799 | 22.978 | 0.969 | ok | 3.907 | 225913 |  |
| redis | 10000 | accepts | 1.000 | 33.093 | 40.282 | 43.076 | 0.969 | ok | 10.127 | 587915 |  |
| redis | 40000 | accepts | 1.000 | 123 | 131 | 133 | 0.969 | ok | 47.501 | 2417915 |  |
| vespa | 1 | accepts | 1.000 | 3.029 | 3.573 | 3.671 | 0.887 | ok | 0.009 | 186 |  |
| vespa | 10 | accepts | 1.000 | 3.233 | 3.899 | 4.077 | 0.887 | ok | 0.016 | 640 |  |
| vespa | 100 | accepts | 1.000 | 4.085 | 4.912 | 5.149 | 0.887 | ok | 0.091 | 5522 |  |
| vespa | 1000 | accepts | 1.000 | 9.610 | 10.436 | 10.799 | 0.887 | ok | 0.735 | 57924 |  |
| vespa | 4000 | accepts | 1.000 | 27.258 | 28.881 | 29.719 | 0.887 | ok | 3.210 | 237924 |  |
| vespa | 10000 | accepts | 1.000 | 60.287 | 64.360 | 65.042 | 0.887 | ok | 8.708 | 617926 |  |
| vespa | 40000 | accepts | 1.000 | 225 | 284 | 294 | 0.887 | ok | 46.121 | 2537926 |  |
| weaviate | 1 | accepts | 1.000 | 4.788 | 5.245 | 5.325 | 1.000 | ok | 0.028 | 75 |  |
| weaviate | 10 | accepts | 1.000 | 4.831 | 5.189 | 5.289 | 1.000 | ok | 0.040 | 75 |  |
| weaviate | 100 | accepts | 1.000 | 5.739 | 6.356 | 6.583 | 1.000 | ok | 0.073 | 75 |  |
| weaviate | 1000 | accepts | 1.000 | 14.336 | 15.449 | 15.751 | 1.000 | ok | 0.601 | 75 |  |
| weaviate | 4000 | accepts | 1.000 | 38.438 | 41.740 | 57.200 | 1.000 | ok | 2.854 | 75 |  |
| weaviate | 10000 | accepts | 1.000 | 82.710 | 98.087 | 111 | 1.000 | ok | 7.657 | 75 |  |
| weaviate | 40000 | accepts | 1.000 | 306 | 323 | 326 | 1.000 | ok | 36.676 | 75 |  |

## Latency ratios (p50, paired by query)

| store | G top | G bottom | ratio | interval | pairs |
|---|---|---|---|---|---|
| pgvector | 40000 | 1 | 272 | [264.42, 287.67] | 150 |
| faiss | 40000 | 1 | 1.191 | [1.18, 1.19] | 150 |
| memory | 40000 | 1 | 1.169 | [1.16, 1.18] | 150 |
| cassandra | 100 | 1000 | 1.849 | [1.82, 1.87] | 150 |
| cassandra | 40000 | 1 | 2.782 | [2.72, 2.86] | 150 |
| elasticsearch | 40000 | 1 | 24.987 | [24.21, 27.05] | 150 |
| lancedb | 40000 | 1 | 7.938 | [7.91, 7.97] | 150 |
| milvus | 40000 | 1 | 26.535 | [25.72, 27.48] | 150 |
| mongodb | 40000 | 1 | 13.654 | [13.57, 13.77] | 150 |
| opensearch | 40000 | 1 | 11.526 | [10.78, 12.22] | 150 |
| qdrant | 40000 | 1 | 27.547 | [26.41, 28.31] | 150 |
| redis | 40000 | 1 | 99.176 | [93.71, 101.44] | 150 |
| vespa | 40000 | 1 | 76.139 | [72.24, 79.73] | 150 |
| weaviate | 40000 | 1 | 64.057 | [63.06, 65.57] | 150 |

## Recall differences (paired by query)

| store | G top | G bottom | difference | interval | pairs |
|---|---|---|---|---|---|
| qdrant | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 150 |
| elasticsearch | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 150 |
| opensearch | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 150 |
| redis | 40000 | 1 | 0.000 | [-0.0007, 0.0007] | 150 |
| weaviate | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 150 |
| milvus | 40000 | 1 | 0.012 | [0.0060, 0.0187] | 150 |
| mongodb | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 150 |
| vespa | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 150 |
| pgvector | 40000 | 1 | 0.000 | [0.0000, 0.0000] | 150 |
| cassandra | 40000 | 1 | 0.004 | [0.0007, 0.0093] | 150 |

## Every verdict part

| hypothesis | store | part | outcome | evidence |
|---|---|---|---|---|
| X3-H1 | cassandra | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | cassandra | G=10 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | cassandra | G=100 | confirmed | 5 seeds, status ['ok'], median 1.3 ms |
| X3-H1 | cassandra | G=1000 | confirmed | 5 seeds, status ['fallback'], median 4.2 ms |
| X3-H1 | cassandra | G=4000 | confirmed | 5 seeds, status ['fallback'], median 11.3 ms |
| X3-H1 | cassandra | G=10000 | confirmed | 5 seeds, status ['fallback'], median 30.0 ms |
| X3-H1 | cassandra | G=40000 | confirmed | 5 seeds, status ['fallback'], median 196.9 ms |
| X3-H1 | chroma | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | chroma | G=1000 | confirmed | 5 seeds, status ['ok'], median 1.1 ms |
| X3-H1 | chroma | G=4000 | confirmed | 5 seeds, status ['ok'], median 4.4 ms |
| X3-H1 | chroma | G=10000 | confirmed | 5 seeds, status ['ok'], median 12.0 ms |
| X3-H1 | chroma | G=40000 | confirmed | 5 seeds, status ['ok'], median 100.9 ms |
| X3-H1 | elasticsearch | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | elasticsearch | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.5 ms |
| X3-H1 | elasticsearch | G=4000 | confirmed | 5 seeds, status ['ok'], median 2.4 ms |
| X3-H1 | elasticsearch | G=10000 | confirmed | 5 seeds, status ['ok'], median 6.4 ms |
| X3-H1 | elasticsearch | G=40000 | confirmed | 5 seeds, status ['ok'], median 31.2 ms |
| X3-H1 | lancedb | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | lancedb | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | lancedb | G=4000 | confirmed | 5 seeds, status ['ok'], median 4.0 ms |
| X3-H1 | lancedb | G=10000 | confirmed | 5 seeds, status ['ok'], median 10.9 ms |
| X3-H1 | lancedb | G=40000 | confirmed | 5 seeds, status ['ok'], median 49.4 ms |
| X3-H1 | milvus | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | milvus | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.5 ms |
| X3-H1 | milvus | G=4000 | confirmed | 5 seeds, status ['ok'], median 2.3 ms |
| X3-H1 | milvus | G=10000 | confirmed | 5 seeds, status ['ok'], median 6.8 ms |
| X3-H1 | milvus | G=40000 | confirmed | 5 seeds, status ['ok'], median 33.8 ms |
| X3-H1 | mongodb | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | mongodb | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.6 ms |
| X3-H1 | mongodb | G=4000 | confirmed | 5 seeds, status ['ok'], median 3.0 ms |
| X3-H1 | mongodb | G=10000 | confirmed | 5 seeds, status ['ok'], median 8.3 ms |
| X3-H1 | mongodb | G=40000 | confirmed | 5 seeds, status ['ok'], median 37.7 ms |
| X3-H1 | opensearch | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | opensearch | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.5 ms |
| X3-H1 | opensearch | G=4000 | confirmed | 5 seeds, status ['ok'], median 2.4 ms |
| X3-H1 | opensearch | G=10000 | confirmed | 5 seeds, status ['ok'], median 6.7 ms |
| X3-H1 | opensearch | G=40000 | confirmed | 5 seeds, status ['ok'], median 31.6 ms |
| X3-H1 | pgvector | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | pgvector | G=10 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | pgvector | G=100 | confirmed | 5 seeds, status ['ok'], median 0.3 ms |
| X3-H1 | pgvector | G=1000 | confirmed | 5 seeds, status ['ok'], median 2.7 ms |
| X3-H1 | pgvector | G=4000 | confirmed | 5 seeds, status ['ok'], median 11.2 ms |
| X3-H1 | pgvector | G=10000 | confirmed | 5 seeds, status ['ok'], median 29.1 ms |
| X3-H1 | pgvector | G=40000 | confirmed | 5 seeds, status ['ok'], median 120.1 ms |
| X3-H1 | qdrant | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | qdrant | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | qdrant | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.5 ms |
| X3-H1 | qdrant | G=4000 | confirmed | 5 seeds, status ['ok'], median 2.4 ms |
| X3-H1 | qdrant | G=10000 | confirmed | 5 seeds, status ['ok'], median 6.4 ms |
| X3-H1 | qdrant | G=40000 | confirmed | 5 seeds, status ['ok'], median 34.8 ms |
| X3-H1 | redis | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | redis | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.8 ms |
| X3-H1 | redis | G=4000 | confirmed | 5 seeds, status ['ok'], median 3.9 ms |
| X3-H1 | redis | G=10000 | confirmed | 5 seeds, status ['ok'], median 10.1 ms |
| X3-H1 | redis | G=40000 | confirmed | 5 seeds, status ['ok'], median 47.5 ms |
| X3-H1 | vespa | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | vespa | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | vespa | G=4000 | confirmed | 5 seeds, status ['ok'], median 3.2 ms |
| X3-H1 | vespa | G=10000 | confirmed | 5 seeds, status ['ok'], median 8.7 ms |
| X3-H1 | vespa | G=40000 | confirmed | 5 seeds, status ['ok'], median 46.1 ms |
| X3-H1 | weaviate | G=1 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | weaviate | G=10 | confirmed | 5 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | weaviate | G=100 | confirmed | 5 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=1000 | confirmed | 5 seeds, status ['ok'], median 0.6 ms |
| X3-H1 | weaviate | G=4000 | confirmed | 5 seeds, status ['ok'], median 2.9 ms |
| X3-H1 | weaviate | G=10000 | confirmed | 5 seeds, status ['ok'], median 7.7 ms |
| X3-H1 | weaviate | G=40000 | confirmed | 5 seeds, status ['ok'], median 36.7 ms |
| X3-H2 | cassandra | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | chroma | G=40,000 predicted refuses | confirmed | observed refuses in 5 seeds, ok share nan, first error the process crashed, exit status -11 |
| X3-H2 | elasticsearch | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | faiss | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | lancedb | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | memory | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | milvus | G=40,000 (no prediction) | reported | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | mongodb | G=40,000 (no prediction) | reported | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | opensearch | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | pgvector | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | qdrant | G=40,000 predicted accepts | confirmed | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | redis | G=40,000 (no prediction) | reported | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | vespa | G=40,000 (no prediction) | reported | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H2 | weaviate | G=40,000 (no prediction) | reported | observed accepts in 5 seeds, ok share 1.000, first error None |
| X3-H3a | pgvector | p50 G=40,000 / G=1 | confirmed | ratio 272.22 [264.42, 287.67], 150 queries, 5 seeds |
| X3-H3b | faiss | p50 G=40,000 / G=1 | confirmed | ratio 1.19 [1.18, 1.19], 150 queries, 5 seeds |
| X3-H3b | memory | p50 G=40,000 / G=1 | confirmed | ratio 1.17 [1.16, 1.18], 150 queries, 5 seeds |
| X3-H3c | cassandra | p50 G=100 / G=1,000 | confirmed | ratio 1.85 [1.82, 1.87], 150 queries, 5 seeds |
| X3-H4 | qdrant | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 150 queries |
| X3-H4 | elasticsearch | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 150 queries |
| X3-H4 | opensearch | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 150 queries |
| X3-H4 | redis | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0000 [-0.0007, 0.0007], 150 queries |
| X3-H4 | weaviate | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 150 queries |
| X3-H4 | milvus | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0120 [0.0060, 0.0187], 150 queries |
| X3-H4 | mongodb | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 150 queries |
| X3-H4 | chroma | recall | inconclusive | no accepted level pair |
| X3-H4 | vespa | G=40,000 vs G=1 | confirmed | recall G=40,000 minus G=1: 0.0000 [0.0000, 0.0000], 150 queries |
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

