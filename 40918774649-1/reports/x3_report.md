# X3: filter-size scaling

957 records (0 unreadable lines), 200 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md.

## Health

| store | mode | seeds done | skipped | retrievals | errors | build s | setup error | seed errors | crashes (seed: status) |
|---|---|---|---|---|---|---|---|---|---|
| cassandra | smoke | [0] | [] | 42 | 0 | 13.200 | n/a | [] | {} |
| chroma | smoke | [] | [] | 27 | 9 | 3.600 | n/a | [] | {0: -11} |
| elasticsearch | smoke | [0] | [] | 42 | 0 | 6.600 | n/a | [] | {} |
| faiss | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] | {} |
| lancedb | smoke | [0] | [] | 42 | 0 | 0.700 | n/a | [] | {} |
| memory | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] | {} |
| milvus | smoke | [0] | [] | 42 | 0 | 7.600 | n/a | [] | {} |
| mongodb | smoke | [0] | [] | 42 | 0 | 3.700 | n/a | [] | {} |
| opensearch | smoke | [0] | [] | 42 | 0 | 7.600 | n/a | [] | {} |
| pgvector | smoke | [0] | [] | 42 | 0 | 3.500 | n/a | [] | {} |
| qdrant | smoke | [0] | [] | 42 | 0 | 1805 | n/a | [] | {} |
| redis | smoke | [0] | [] | 42 | 0 | 1.300 | n/a | [] | {} |
| vespa | smoke | [0] | [] | 42 | 0 | 20.100 | n/a | [] | {} |
| weaviate | smoke | [0] | [] | 42 | 0 | 3.000 | n/a | [] | {} |

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
| cassandra | 1 | accepts | 1.000 | 13.475 | 19.059 | 19.555 | 1.000 | ok | 0.057 | 19 |  |
| cassandra | 10 | accepts | 1.000 | 23.933 | 30.470 | 31.051 | 1.000 | ok | 0.085 | 20 |  |
| cassandra | 100 | accepts | 1.000 | 136 | 330 | 347 | 1.000 | ok | 1.077 | 21 |  |
| cassandra | 1000 | accepts | 1.000 | 109 | 118 | 119 | 1.000 | fallback | 4.544 | 39 |  |
| cassandra | 4000 | accepts | 1.000 | 109 | 109 | 109 | 1.000 | fallback | 15.869 | 39 |  |
| cassandra | 10000 | accepts | 1.000 | 131 | 150 | 152 | 1.000 | fallback | 42.914 | 39 |  |
| cassandra | 40000 | accepts | 1.000 | 245 | 248 | 248 | 1.000 | fallback | 141 | 39 |  |
| chroma | 1 | accepts | 1.000 | 437 | 444 | 444 | 1.000 | ok | 0.029 | 246 |  |
| chroma | 10 | accepts | 1.000 | 465 | 468 | 468 | 1.000 | ok | 0.058 | 727 |  |
| chroma | 100 | accepts | 1.000 | 771 | 774 | 774 | 1.000 | ok | 0.118 | 5879 |  |
| chroma | 1000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 0.815 | 60981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 4000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 3.562 | 249981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 10000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 9.281 | 647983 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 40000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 81.727 | 2657983 | the process crashed, exit status -11 |
| elasticsearch | 1 | accepts | 1.000 | 15.299 | 16.732 | 16.860 | 0.933 | ok | 0.034 | 203 |  |
| elasticsearch | 10 | accepts | 1.000 | 16.521 | 18.115 | 18.256 | 0.933 | ok | 0.037 | 484 |  |
| elasticsearch | 100 | accepts | 1.000 | 13.183 | 13.221 | 13.224 | 0.933 | ok | 0.137 | 3465 |  |
| elasticsearch | 1000 | accepts | 1.000 | 18.129 | 19.974 | 20.138 | 0.933 | ok | 0.832 | 35066 |  |
| elasticsearch | 4000 | accepts | 1.000 | 24.053 | 25.938 | 26.106 | 0.933 | ok | 3.179 | 143066 |  |
| elasticsearch | 10000 | accepts | 1.000 | 38.031 | 39.686 | 39.834 | 0.933 | ok | 8.985 | 369067 |  |
| elasticsearch | 40000 | accepts | 1.000 | 110 | 119 | 119 | 0.933 | ok | 41.604 | 1509067 |  |
| faiss | 1 | accepts | 1.000 | 22.080 | 22.113 | 22.116 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 10 | accepts | 1.000 | 22.489 | 22.770 | 22.795 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 100 | accepts | 1.000 | 22.361 | 22.457 | 22.466 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 1000 | accepts | 1.000 | 23.253 | 23.474 | 23.493 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 4000 | accepts | 1.000 | 24.035 | 24.101 | 24.107 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 10000 | accepts | 1.000 | 26.488 | 26.583 | 26.591 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 40000 | accepts | 1.000 | 42.067 | 43.369 | 43.485 | 1.000 | in-process | 0.001 | n/a |  |
| lancedb | 1 | accepts | 1.000 | 6.447 | 6.499 | 6.503 | 1.000 | ok | 0.028 | 208 |  |
| lancedb | 10 | accepts | 1.000 | 6.282 | 6.287 | 6.287 | 1.000 | ok | 0.031 | 644 |  |
| lancedb | 100 | accepts | 1.000 | 6.985 | 7.088 | 7.098 | 1.000 | ok | 0.116 | 5346 |  |
| lancedb | 1000 | accepts | 1.000 | 13.692 | 13.764 | 13.770 | 1.000 | ok | 0.690 | 55948 |  |
| lancedb | 4000 | accepts | 1.000 | 35.594 | 35.694 | 35.703 | 1.000 | ok | 3.447 | 229948 |  |
| lancedb | 10000 | accepts | 1.000 | 78.001 | 80.985 | 81.250 | 1.000 | ok | 9.490 | 597950 |  |
| lancedb | 40000 | accepts | 1.000 | 315 | 324 | 324 | 1.000 | ok | 41.198 | 2457950 |  |
| memory | 1 | accepts | 1.000 | 22.152 | 22.252 | 22.261 | n/a | in-process | 0.001 | n/a |  |
| memory | 10 | accepts | 1.000 | 24.046 | 24.626 | 24.677 | n/a | in-process | 0.002 | n/a |  |
| memory | 100 | accepts | 1.000 | 22.718 | 23.489 | 23.557 | n/a | in-process | 0.001 | n/a |  |
| memory | 1000 | accepts | 1.000 | 23.879 | 24.251 | 24.284 | n/a | in-process | 0.001 | n/a |  |
| memory | 4000 | accepts | 1.000 | 25.043 | 25.791 | 25.857 | n/a | in-process | 0.001 | n/a |  |
| memory | 10000 | accepts | 1.000 | 29.430 | 29.581 | 29.595 | n/a | in-process | 0.001 | n/a |  |
| memory | 40000 | accepts | 1.000 | 46.082 | 46.459 | 46.492 | n/a | in-process | 0.001 | n/a |  |
| milvus | 1 | accepts | 1.000 | 2.986 | 3.035 | 3.040 | 0.867 | ok | 0.029 | 196 |  |
| milvus | 10 | accepts | 1.000 | 2.913 | 3.016 | 3.025 | 0.867 | ok | 0.034 | 477 |  |
| milvus | 100 | accepts | 1.000 | 3.208 | 3.267 | 3.272 | 0.867 | ok | 0.111 | 3458 |  |
| milvus | 1000 | accepts | 1.000 | 5.756 | 5.776 | 5.778 | 0.867 | ok | 0.777 | 35059 |  |
| milvus | 4000 | accepts | 1.000 | 15.428 | 15.801 | 15.834 | 0.867 | ok | 3.159 | 143059 |  |
| milvus | 10000 | accepts | 1.000 | 33.833 | 35.387 | 35.525 | 0.867 | ok | 8.839 | 369060 |  |
| milvus | 40000 | accepts | 1.000 | 123 | 137 | 138 | 0.867 | ok | 41.673 | 1509060 |  |
| mongodb | 1 | accepts | 1.000 | 6.146 | 6.397 | 6.420 | 1.000 | ok | 0.021 | 159 |  |
| mongodb | 10 | accepts | 1.000 | 6.370 | 7.136 | 7.204 | 1.000 | ok | 0.022 | 440 |  |
| mongodb | 100 | accepts | 1.000 | 6.643 | 7.120 | 7.163 | 1.000 | ok | 0.048 | 3421 |  |
| mongodb | 1000 | accepts | 1.000 | 9.605 | 10.432 | 10.506 | 1.000 | ok | 0.399 | 35022 |  |
| mongodb | 4000 | accepts | 1.000 | 16.777 | 19.250 | 19.469 | 1.000 | ok | 2.041 | 143022 |  |
| mongodb | 10000 | accepts | 1.000 | 25.879 | 26.299 | 26.336 | 1.000 | ok | 5.295 | 369023 |  |
| mongodb | 40000 | accepts | 1.000 | 82.892 | 83.743 | 83.818 | 1.000 | ok | 25.400 | 1509023 |  |
| opensearch | 1 | accepts | 1.000 | 13.655 | 14.672 | 14.763 | 1.000 | ok | 0.036 | 203 |  |
| opensearch | 10 | accepts | 1.000 | 18.930 | 22.157 | 22.443 | 1.000 | ok | 0.036 | 484 |  |
| opensearch | 100 | accepts | 1.000 | 10.733 | 16.370 | 16.871 | 1.000 | ok | 0.078 | 3465 |  |
| opensearch | 1000 | accepts | 1.000 | 14.429 | 14.723 | 14.749 | 1.000 | ok | 0.736 | 35066 |  |
| opensearch | 4000 | accepts | 1.000 | 22.213 | 23.755 | 23.892 | 1.000 | ok | 3.107 | 143066 |  |
| opensearch | 10000 | accepts | 1.000 | 41.767 | 54.314 | 55.429 | 1.000 | ok | 8.467 | 369067 |  |
| opensearch | 40000 | accepts | 1.000 | 92.393 | 94.128 | 94.282 | 1.000 | ok | 40.821 | 1509067 |  |
| pgvector | 1 | accepts | 1.000 | 2.594 | 3.106 | 3.151 | 1.000 | ok | 0.050 | 368 |  |
| pgvector | 10 | accepts | 1.000 | 3.059 | 3.929 | 4.007 | 1.000 | ok | 0.143 | 1470 |  |
| pgvector | 100 | accepts | 1.000 | 3.930 | 5.570 | 5.716 | 1.000 | ok | 0.284 | 3453 |  |
| pgvector | 1000 | accepts | 1.000 | 19.900 | 30.143 | 31.054 | 1.000 | ok | 2.659 | 36055 |  |
| pgvector | 4000 | accepts | 1.000 | 71.548 | 109 | 112 | 1.000 | ok | 11.510 | 150055 |  |
| pgvector | 10000 | accepts | 1.000 | 179 | 267 | 275 | 1.000 | ok | 29.362 | 398057 |  |
| pgvector | 40000 | accepts | 1.000 | 718 | 1076 | 1107 | 1.000 | ok | 123 | 1658057 |  |
| qdrant | 1 | accepts | 1.000 | 3.261 | 3.436 | 3.452 | 1.000 | ok | 0.139 | 433 |  |
| qdrant | 10 | accepts | 1.000 | 2.880 | 2.942 | 2.947 | 1.000 | ok | 0.080 | 507 |  |
| qdrant | 100 | accepts | 1.000 | 3.226 | 3.382 | 3.396 | 1.000 | ok | 0.135 | 1418 |  |
| qdrant | 1000 | accepts | 1.000 | 5.772 | 5.787 | 5.788 | 1.000 | ok | 0.956 | 12319 |  |
| qdrant | 4000 | accepts | 1.000 | 12.168 | 12.302 | 12.314 | 1.000 | ok | 55.239 | 51319 |  |
| qdrant | 10000 | accepts | 1.000 | 26.208 | 29.289 | 29.563 | 1.000 | ok | 9.147 | 139320 |  |
| qdrant | 40000 | accepts | 1.000 | 102 | 104 | 104 | 1.000 | ok | 45.465 | 589320 |  |
| redis | 1 | accepts | 1.000 | 1.650 | 1.680 | 1.682 | 1.000 | ok | 0.043 | 172 |  |
| redis | 10 | accepts | 1.000 | 1.692 | 1.777 | 1.784 | 1.000 | ok | 0.043 | 599 |  |
| redis | 100 | accepts | 1.000 | 2.010 | 2.793 | 2.862 | 1.000 | ok | 0.168 | 5211 |  |
| redis | 1000 | accepts | 1.000 | 3.601 | 3.743 | 3.756 | 1.000 | ok | 0.854 | 54913 |  |
| redis | 4000 | accepts | 1.000 | 11.628 | 11.885 | 11.907 | 1.000 | ok | 3.954 | 225913 |  |
| redis | 10000 | accepts | 1.000 | 29.181 | 29.326 | 29.338 | 1.000 | ok | 11.782 | 587915 |  |
| redis | 40000 | accepts | 1.000 | 121 | 123 | 124 | 1.000 | ok | 54.778 | 2417915 |  |
| vespa | 1 | accepts | 1.000 | 15.337 | 19.141 | 19.480 | 1.000 | ok | 0.035 | 186 |  |
| vespa | 10 | accepts | 1.000 | 11.756 | 11.757 | 11.757 | 1.000 | ok | 0.052 | 640 |  |
| vespa | 100 | accepts | 1.000 | 14.129 | 14.624 | 14.668 | 1.000 | ok | 0.166 | 5522 |  |
| vespa | 1000 | accepts | 1.000 | 19.965 | 20.615 | 20.672 | 1.000 | ok | 0.945 | 57924 |  |
| vespa | 4000 | accepts | 1.000 | 40.741 | 47.215 | 47.791 | 1.000 | ok | 4.769 | 237924 |  |
| vespa | 10000 | accepts | 1.000 | 75.878 | 76.864 | 76.952 | 1.000 | ok | 15.473 | 617926 |  |
| vespa | 40000 | accepts | 1.000 | 274 | 278 | 278 | 1.000 | ok | 56.199 | 2537926 |  |
| weaviate | 1 | accepts | 1.000 | 1.780 | 1.785 | 1.786 | 1.000 | ok | 0.170 | 75 |  |
| weaviate | 10 | accepts | 1.000 | 1.889 | 1.956 | 1.962 | 1.000 | ok | 0.077 | 75 |  |
| weaviate | 100 | accepts | 1.000 | 3.046 | 3.178 | 3.189 | 1.000 | ok | 0.125 | 75 |  |
| weaviate | 1000 | accepts | 1.000 | 12.195 | 19.315 | 19.948 | 1.000 | ok | 0.894 | 75 |  |
| weaviate | 4000 | accepts | 1.000 | 40.416 | 40.574 | 40.588 | 1.000 | ok | 3.820 | 75 |  |
| weaviate | 10000 | accepts | 1.000 | 98.653 | 107 | 107 | 1.000 | ok | 10.213 | 75 |  |
| weaviate | 40000 | accepts | 1.000 | 400 | 407 | 408 | 1.000 | ok | 47.808 | 75 |  |

## Latency ratios (p50, paired by query)

| store | G top | G bottom | ratio | interval | pairs |
|---|---|---|---|---|---|
| pgvector | 40000 | 1 | 277 | [251.90, 352.64] | 3 |
| faiss | 40000 | 1 | 1.905 | [1.86, 1.97] | 3 |
| memory | 40000 | 1 | 2.080 | [2.06, 2.09] | 3 |
| cassandra | 100 | 1000 | 1.245 | [1.05, 2.95] | 3 |
| cassandra | 40000 | 1 | 18.163 | [12.44, 18.39] | 3 |
| elasticsearch | 40000 | 1 | 7.209 | [6.11, 8.00] | 3 |
| lancedb | 40000 | 1 | 48.889 | [48.46, 50.32] | 3 |
| milvus | 40000 | 1 | 41.130 | [39.08, 47.00] | 3 |
| mongodb | 40000 | 1 | 13.488 | [12.23, 14.31] | 3 |
| opensearch | 40000 | 1 | 6.766 | [6.25, 7.67] | 3 |
| qdrant | 40000 | 1 | 31.389 | [29.63, 31.91] | 3 |
| redis | 40000 | 1 | 73.385 | [73.39, 78.18] | 3 |
| vespa | 40000 | 1 | 17.866 | [14.01, 21.81] | 3 |
| weaviate | 40000 | 1 | 225 | [219.42, 229.13] | 3 |

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
| X3-H1 | cassandra | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | cassandra | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | cassandra | G=100 | inconclusive | 1 seeds, status ['ok'], median 1.1 ms |
| X3-H1 | cassandra | G=1000 | inconclusive | 1 seeds, status ['fallback'], median 4.5 ms |
| X3-H1 | cassandra | G=4000 | inconclusive | 1 seeds, status ['fallback'], median 15.9 ms |
| X3-H1 | cassandra | G=10000 | inconclusive | 1 seeds, status ['fallback'], median 42.9 ms |
| X3-H1 | cassandra | G=40000 | inconclusive | 1 seeds, status ['fallback'], median 141.3 ms |
| X3-H1 | chroma | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | chroma | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | chroma | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.8 ms |
| X3-H1 | chroma | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.6 ms |
| X3-H1 | chroma | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.3 ms |
| X3-H1 | chroma | G=40000 | inconclusive | 1 seeds, status ['ok'], median 81.7 ms |
| X3-H1 | elasticsearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | elasticsearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.8 ms |
| X3-H1 | elasticsearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.2 ms |
| X3-H1 | elasticsearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.0 ms |
| X3-H1 | elasticsearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 41.6 ms |
| X3-H1 | lancedb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | lancedb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | lancedb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.4 ms |
| X3-H1 | lancedb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.5 ms |
| X3-H1 | lancedb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 41.2 ms |
| X3-H1 | milvus | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | milvus | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.8 ms |
| X3-H1 | milvus | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.2 ms |
| X3-H1 | milvus | G=10000 | inconclusive | 1 seeds, status ['ok'], median 8.8 ms |
| X3-H1 | milvus | G=40000 | inconclusive | 1 seeds, status ['ok'], median 41.7 ms |
| X3-H1 | mongodb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.4 ms |
| X3-H1 | mongodb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 2.0 ms |
| X3-H1 | mongodb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 5.3 ms |
| X3-H1 | mongodb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 25.4 ms |
| X3-H1 | opensearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | opensearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | opensearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.1 ms |
| X3-H1 | opensearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 8.5 ms |
| X3-H1 | opensearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 40.8 ms |
| X3-H1 | pgvector | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | pgvector | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | pgvector | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.3 ms |
| X3-H1 | pgvector | G=1000 | inconclusive | 1 seeds, status ['ok'], median 2.7 ms |
| X3-H1 | pgvector | G=4000 | inconclusive | 1 seeds, status ['ok'], median 11.5 ms |
| X3-H1 | pgvector | G=10000 | inconclusive | 1 seeds, status ['ok'], median 29.4 ms |
| X3-H1 | pgvector | G=40000 | inconclusive | 1 seeds, status ['ok'], median 122.8 ms |
| X3-H1 | qdrant | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.0 ms |
| X3-H1 | qdrant | G=4000 | inconclusive | 1 seeds, status ['ok'], median 55.2 ms |
| X3-H1 | qdrant | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.1 ms |
| X3-H1 | qdrant | G=40000 | inconclusive | 1 seeds, status ['ok'], median 45.5 ms |
| X3-H1 | redis | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | redis | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | redis | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.0 ms |
| X3-H1 | redis | G=10000 | inconclusive | 1 seeds, status ['ok'], median 11.8 ms |
| X3-H1 | redis | G=40000 | inconclusive | 1 seeds, status ['ok'], median 54.8 ms |
| X3-H1 | vespa | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | vespa | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | vespa | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | vespa | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.8 ms |
| X3-H1 | vespa | G=10000 | inconclusive | 1 seeds, status ['ok'], median 15.5 ms |
| X3-H1 | vespa | G=40000 | inconclusive | 1 seeds, status ['ok'], median 56.2 ms |
| X3-H1 | weaviate | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | weaviate | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | weaviate | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.8 ms |
| X3-H1 | weaviate | G=10000 | inconclusive | 1 seeds, status ['ok'], median 10.2 ms |
| X3-H1 | weaviate | G=40000 | inconclusive | 1 seeds, status ['ok'], median 47.8 ms |
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
| X3-H3a | pgvector | p50 G=40,000 / G=1 | inconclusive | {'store': 'pgvector', 'top': 40000, 'bottom': 1, 'ratio': 276.7114717446612, 'lo': 251.90359262971245, 'hi': 352.64225637134007, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 717.8449, 'p50_bottom_ms': 2.5942} |
| X3-H3b | faiss | p50 G=40,000 / G=1 | inconclusive | {'store': 'faiss', 'top': 40000, 'bottom': 1, 'ratio': 1.9052564358049966, 'lo': 1.8551468323701519, 'hi': 1.9674544574913977, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 42.0673, 'p50_bottom_ms': 22.0796} |
| X3-H3b | memory | p50 G=40,000 / G=1 | inconclusive | {'store': 'memory', 'top': 40000, 'bottom': 1, 'ratio': 2.080230584496488, 'lo': 2.059171731525522, 'hi': 2.08867059240993, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 46.0821, 'p50_bottom_ms': 22.1524} |
| X3-H3c | cassandra | p50 G=100 / G=1,000 | inconclusive | {'store': 'cassandra', 'top': 100, 'bottom': 1000, 'ratio': 1.2454696188806285, 'lo': 1.0528651649452345, 'hi': 2.9539859553840353, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 135.8836, 'p50_bottom_ms': 109.1023} |
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

