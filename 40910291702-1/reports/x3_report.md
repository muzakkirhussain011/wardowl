# X3: filter-size scaling

857 records (0 unreadable lines), 200 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md.

## Health

| store | mode | seeds done | skipped | retrievals | errors | build s | setup error | seed errors |
|---|---|---|---|---|---|---|---|---|
| cassandra | smoke | [0] | [] | 42 | 0 | 14.600 | n/a | [] |
| chroma | smoke | [] | [] | 27 | 9 | 4.300 | n/a | [] |
| elasticsearch | smoke | [0] | [] | 42 | 0 | 6.400 | n/a | [] |
| faiss | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] |
| lancedb | smoke | [0] | [] | 42 | 0 | 0.800 | n/a | [] |
| memory | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] |
| milvus | smoke | [0] | [] | 42 | 0 | 7.700 | n/a | [] |
| mongodb | smoke | [0] | [] | 42 | 0 | 4.000 | n/a | [] |
| opensearch | smoke | [0] | [] | 42 | 0 | 7.400 | n/a | [] |
| pgvector | smoke | [0] | [] | 42 | 0 | 3.000 | n/a | [] |
| qdrant | smoke | [0] | [] | 42 | 0 | 1805 | n/a | [] |
| redis | smoke | [0] | [] | 42 | 0 | 1.000 | n/a | [] |
| vespa | smoke | [0] | [] | 42 | 0 | 20.600 | n/a | [] |
| weaviate | smoke | [0] | [] | 42 | 0 | 3.100 | n/a | [] |

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
| cassandra | 1 | accepts | 1.000 | 16.389 | 17.725 | 17.844 | 1.000 | ok | 0.087 | 19 |  |
| cassandra | 10 | accepts | 1.000 | 35.586 | 39.908 | 40.293 | 1.000 | ok | 0.127 | 20 |  |
| cassandra | 100 | accepts | 1.000 | 172 | 431 | 454 | 1.000 | ok | 1.657 | 21 |  |
| cassandra | 1000 | accepts | 1.000 | 134 | 138 | 138 | 1.000 | fallback | 4.510 | 39 |  |
| cassandra | 4000 | accepts | 1.000 | 124 | 130 | 130 | 1.000 | fallback | 22.868 | 39 |  |
| cassandra | 10000 | accepts | 1.000 | 150 | 168 | 170 | 1.000 | fallback | 55.570 | 39 |  |
| cassandra | 40000 | accepts | 1.000 | 266 | 291 | 293 | 1.000 | fallback | 172 | 39 |  |
| chroma | 1 | accepts | 1.000 | 432 | 445 | 446 | 1.000 | ok | 0.033 | 246 |  |
| chroma | 10 | accepts | 1.000 | 473 | 477 | 477 | 1.000 | ok | 0.036 | 727 |  |
| chroma | 100 | accepts | 1.000 | 843 | 844 | 844 | 1.000 | ok | 0.152 | 5879 |  |
| chroma | 1000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 1.542 | 60981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 4000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 4.425 | 249981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 10000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 12.027 | 647983 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 40000 | not run | n/a | n/a | n/a | n/a | n/a | ok | 99.230 | 2657983 |  |
| elasticsearch | 1 | accepts | 1.000 | 16.053 | 17.769 | 17.921 | 1.000 | ok | 0.040 | 203 |  |
| elasticsearch | 10 | accepts | 1.000 | 21.829 | 24.318 | 24.539 | 1.000 | ok | 0.038 | 484 |  |
| elasticsearch | 100 | accepts | 1.000 | 16.707 | 17.930 | 18.039 | 1.000 | ok | 0.146 | 3465 |  |
| elasticsearch | 1000 | accepts | 1.000 | 23.979 | 25.724 | 25.879 | 1.000 | ok | 1.337 | 35066 |  |
| elasticsearch | 4000 | accepts | 1.000 | 32.860 | 34.724 | 34.890 | 1.000 | ok | 5.611 | 143066 |  |
| elasticsearch | 10000 | accepts | 1.000 | 55.069 | 55.740 | 55.799 | 1.000 | ok | 15.259 | 369067 |  |
| elasticsearch | 40000 | accepts | 1.000 | 118 | 133 | 135 | 1.000 | ok | 41.453 | 1509067 |  |
| faiss | 1 | accepts | 1.000 | 32.485 | 32.786 | 32.812 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 10 | accepts | 1.000 | 32.472 | 32.479 | 32.480 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 100 | accepts | 1.000 | 32.743 | 32.770 | 32.773 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 1000 | accepts | 1.000 | 33.667 | 33.795 | 33.806 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 4000 | accepts | 1.000 | 35.224 | 35.883 | 35.941 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 10000 | accepts | 1.000 | 39.279 | 39.472 | 39.489 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 40000 | accepts | 1.000 | 57.639 | 57.961 | 57.989 | 1.000 | in-process | 0.002 | n/a |  |
| lancedb | 1 | accepts | 1.000 | 8.994 | 9.532 | 9.580 | 1.000 | ok | 0.032 | 208 |  |
| lancedb | 10 | accepts | 1.000 | 8.360 | 8.641 | 8.666 | 1.000 | ok | 0.044 | 644 |  |
| lancedb | 100 | accepts | 1.000 | 9.386 | 9.665 | 9.690 | 1.000 | ok | 0.112 | 5346 |  |
| lancedb | 1000 | accepts | 1.000 | 17.479 | 18.374 | 18.454 | 1.000 | ok | 0.883 | 55948 |  |
| lancedb | 4000 | accepts | 1.000 | 45.976 | 47.116 | 47.217 | 1.000 | ok | 4.340 | 229948 |  |
| lancedb | 10000 | accepts | 1.000 | 103 | 107 | 107 | 1.000 | ok | 12.651 | 597950 |  |
| lancedb | 40000 | accepts | 1.000 | 412 | 430 | 431 | 1.000 | ok | 56.517 | 2457950 |  |
| memory | 1 | accepts | 1.000 | 32.993 | 33.207 | 33.226 | n/a | in-process | 0.003 | n/a |  |
| memory | 10 | accepts | 1.000 | 33.568 | 33.610 | 33.614 | n/a | in-process | 0.001 | n/a |  |
| memory | 100 | accepts | 1.000 | 33.200 | 33.371 | 33.387 | n/a | in-process | 0.001 | n/a |  |
| memory | 1000 | accepts | 1.000 | 34.983 | 35.230 | 35.252 | n/a | in-process | 0.001 | n/a |  |
| memory | 4000 | accepts | 1.000 | 36.010 | 36.133 | 36.143 | n/a | in-process | 0.001 | n/a |  |
| memory | 10000 | accepts | 1.000 | 40.154 | 40.280 | 40.291 | n/a | in-process | 0.002 | n/a |  |
| memory | 40000 | accepts | 1.000 | 58.031 | 58.518 | 58.561 | n/a | in-process | 0.002 | n/a |  |
| milvus | 1 | accepts | 1.000 | 3.982 | 4.080 | 4.088 | 0.867 | ok | 0.030 | 196 |  |
| milvus | 10 | accepts | 1.000 | 3.721 | 3.758 | 3.761 | 0.867 | ok | 0.040 | 477 |  |
| milvus | 100 | accepts | 1.000 | 4.075 | 4.261 | 4.278 | 0.867 | ok | 0.116 | 3458 |  |
| milvus | 1000 | accepts | 1.000 | 6.836 | 6.869 | 6.872 | 0.867 | ok | 0.827 | 35059 |  |
| milvus | 4000 | accepts | 1.000 | 17.066 | 17.502 | 17.541 | 0.867 | ok | 3.206 | 143059 |  |
| milvus | 10000 | accepts | 1.000 | 36.151 | 36.304 | 36.318 | 0.867 | ok | 9.165 | 369060 |  |
| milvus | 40000 | accepts | 1.000 | 126 | 151 | 153 | 0.867 | ok | 47.611 | 1509060 |  |
| mongodb | 1 | accepts | 1.000 | 6.608 | 7.110 | 7.155 | 1.000 | ok | 0.022 | 159 |  |
| mongodb | 10 | accepts | 1.000 | 8.426 | 10.960 | 11.186 | 1.000 | ok | 0.022 | 440 |  |
| mongodb | 100 | accepts | 1.000 | 8.427 | 8.487 | 8.493 | 1.000 | ok | 0.071 | 3421 |  |
| mongodb | 1000 | accepts | 1.000 | 13.548 | 14.026 | 14.068 | 1.000 | ok | 0.654 | 35022 |  |
| mongodb | 4000 | accepts | 1.000 | 26.432 | 28.172 | 28.326 | 1.000 | ok | 3.382 | 143022 |  |
| mongodb | 10000 | accepts | 1.000 | 29.478 | 46.273 | 47.765 | 1.000 | ok | 9.009 | 369023 |  |
| mongodb | 40000 | accepts | 1.000 | 89.206 | 93.465 | 93.844 | 1.000 | ok | 23.959 | 1509023 |  |
| opensearch | 1 | accepts | 1.000 | 16.435 | 21.213 | 21.637 | 1.000 | ok | 0.037 | 203 |  |
| opensearch | 10 | accepts | 1.000 | 18.953 | 21.645 | 21.885 | 1.000 | ok | 0.037 | 484 |  |
| opensearch | 100 | accepts | 1.000 | 18.420 | 22.790 | 23.178 | 1.000 | ok | 0.122 | 3465 |  |
| opensearch | 1000 | accepts | 1.000 | 18.403 | 18.813 | 18.850 | 1.000 | ok | 1.213 | 35066 |  |
| opensearch | 4000 | accepts | 1.000 | 28.497 | 28.521 | 28.523 | 1.000 | ok | 5.420 | 143066 |  |
| opensearch | 10000 | accepts | 1.000 | 32.928 | 47.882 | 49.211 | 1.000 | ok | 8.573 | 369067 |  |
| opensearch | 40000 | accepts | 1.000 | 103 | 106 | 106 | 1.000 | ok | 41.558 | 1509067 |  |
| pgvector | 1 | accepts | 1.000 | 1.802 | 2.005 | 2.023 | 1.000 | ok | 0.042 | 368 |  |
| pgvector | 10 | accepts | 1.000 | 2.472 | 2.614 | 2.626 | 1.000 | ok | 0.064 | 1470 |  |
| pgvector | 100 | accepts | 1.000 | 3.037 | 3.360 | 3.389 | 1.000 | ok | 0.236 | 3453 |  |
| pgvector | 1000 | accepts | 1.000 | 15.011 | 16.131 | 16.231 | 1.000 | ok | 2.083 | 36055 |  |
| pgvector | 4000 | accepts | 1.000 | 57.813 | 58.447 | 58.503 | 1.000 | ok | 8.873 | 150055 |  |
| pgvector | 10000 | accepts | 1.000 | 147 | 148 | 148 | 1.000 | ok | 22.878 | 398057 |  |
| pgvector | 40000 | accepts | 1.000 | 591 | 592 | 592 | 1.000 | ok | 96.845 | 1658057 |  |
| qdrant | 1 | accepts | 1.000 | 3.281 | 3.435 | 3.449 | 1.000 | ok | 0.150 | 433 |  |
| qdrant | 10 | accepts | 1.000 | 3.083 | 3.145 | 3.151 | 1.000 | ok | 0.082 | 507 |  |
| qdrant | 100 | accepts | 1.000 | 3.271 | 3.313 | 3.317 | 1.000 | ok | 0.176 | 1418 |  |
| qdrant | 1000 | accepts | 1.000 | 5.062 | 5.132 | 5.139 | 1.000 | ok | 0.924 | 12319 |  |
| qdrant | 4000 | accepts | 1.000 | 11.223 | 11.779 | 11.828 | 1.000 | ok | 47.889 | 51319 |  |
| qdrant | 10000 | accepts | 1.000 | 25.110 | 25.395 | 25.420 | 1.000 | ok | 9.131 | 139320 |  |
| qdrant | 40000 | accepts | 1.000 | 95.569 | 98.618 | 98.889 | 1.000 | ok | 43.077 | 589320 |  |
| redis | 1 | accepts | 1.000 | 1.670 | 1.677 | 1.678 | 1.000 | ok | 0.038 | 172 |  |
| redis | 10 | accepts | 1.000 | 0.750 | 0.790 | 0.794 | 1.000 | ok | 0.034 | 599 |  |
| redis | 100 | accepts | 1.000 | 0.965 | 0.967 | 0.967 | 1.000 | ok | 0.071 | 5211 |  |
| redis | 1000 | accepts | 1.000 | 2.740 | 2.842 | 2.851 | 1.000 | ok | 0.671 | 54913 |  |
| redis | 4000 | accepts | 1.000 | 8.749 | 8.760 | 8.761 | 1.000 | ok | 3.253 | 225913 |  |
| redis | 10000 | accepts | 1.000 | 23.152 | 23.247 | 23.255 | 1.000 | ok | 8.562 | 587915 |  |
| redis | 40000 | accepts | 1.000 | 96.619 | 96.642 | 96.644 | 1.000 | ok | 45.285 | 2417915 |  |
| vespa | 1 | accepts | 1.000 | 12.153 | 14.886 | 15.129 | 0.933 | ok | 0.034 | 186 |  |
| vespa | 10 | accepts | 1.000 | 14.307 | 14.357 | 14.362 | 0.933 | ok | 0.028 | 640 |  |
| vespa | 100 | accepts | 1.000 | 13.108 | 14.610 | 14.744 | 0.933 | ok | 0.164 | 5522 |  |
| vespa | 1000 | accepts | 1.000 | 21.377 | 22.786 | 22.911 | 0.933 | ok | 1.036 | 57924 |  |
| vespa | 4000 | accepts | 1.000 | 50.791 | 53.004 | 53.200 | 0.933 | ok | 6.057 | 237924 |  |
| vespa | 10000 | accepts | 1.000 | 70.135 | 70.162 | 70.164 | 0.933 | ok | 12.479 | 617926 |  |
| vespa | 40000 | accepts | 1.000 | 254 | 280 | 282 | 0.933 | ok | 55.116 | 2537926 |  |
| weaviate | 1 | accepts | 1.000 | 1.790 | 1.810 | 1.812 | 1.000 | ok | 0.166 | 75 |  |
| weaviate | 10 | accepts | 1.000 | 1.958 | 1.991 | 1.994 | 1.000 | ok | 0.099 | 75 |  |
| weaviate | 100 | accepts | 1.000 | 2.844 | 2.915 | 2.921 | 1.000 | ok | 0.194 | 75 |  |
| weaviate | 1000 | accepts | 1.000 | 10.277 | 10.333 | 10.338 | 1.000 | ok | 0.895 | 75 |  |
| weaviate | 4000 | accepts | 1.000 | 40.789 | 41.532 | 41.598 | 1.000 | ok | 4.007 | 75 |  |
| weaviate | 10000 | accepts | 1.000 | 102 | 108 | 109 | 1.000 | ok | 10.511 | 75 |  |
| weaviate | 40000 | accepts | 1.000 | 407 | 416 | 417 | 1.000 | ok | 48.779 | 75 |  |

## Latency ratios (p50, paired by query)

| store | G top | G bottom | ratio | interval | pairs |
|---|---|---|---|---|---|
| pgvector | 40000 | 1 | 328 | [292.01, 328.21] | 3 |
| faiss | 40000 | 1 | 1.774 | [1.76, 1.81] | 3 |
| memory | 40000 | 1 | 1.759 | [1.72, 1.79] | 3 |
| cassandra | 100 | 1000 | 1.288 | [1.29, 3.33] | 3 |
| cassandra | 40000 | 1 | 16.219 | [15.63, 16.49] | 3 |
| elasticsearch | 40000 | 1 | 7.374 | [6.78, 7.52] | 3 |
| lancedb | 40000 | 1 | 45.801 | [42.95, 49.85] | 3 |
| milvus | 40000 | 1 | 31.550 | [30.72, 38.49] | 3 |
| mongodb | 40000 | 1 | 13.500 | [11.75, 15.75] | 3 |
| opensearch | 40000 | 1 | 6.276 | [4.38, 7.66] | 3 |
| qdrant | 40000 | 1 | 29.129 | [27.68, 30.47] | 3 |
| redis | 40000 | 1 | 57.866 | [57.57, 67.83] | 3 |
| vespa | 40000 | 1 | 20.915 | [18.62, 23.15] | 3 |
| weaviate | 40000 | 1 | 227 | [207.48, 232.95] | 3 |

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
| X3-H1 | cassandra | G=100 | inconclusive | 1 seeds, status ['ok'], median 1.7 ms |
| X3-H1 | cassandra | G=1000 | inconclusive | 1 seeds, status ['fallback'], median 4.5 ms |
| X3-H1 | cassandra | G=4000 | inconclusive | 1 seeds, status ['fallback'], median 22.9 ms |
| X3-H1 | cassandra | G=10000 | inconclusive | 1 seeds, status ['fallback'], median 55.6 ms |
| X3-H1 | cassandra | G=40000 | inconclusive | 1 seeds, status ['fallback'], median 172.1 ms |
| X3-H1 | chroma | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | chroma | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.5 ms |
| X3-H1 | chroma | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.4 ms |
| X3-H1 | chroma | G=10000 | inconclusive | 1 seeds, status ['ok'], median 12.0 ms |
| X3-H1 | chroma | G=40000 | inconclusive | 1 seeds, status ['ok'], median 99.2 ms |
| X3-H1 | elasticsearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | elasticsearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.3 ms |
| X3-H1 | elasticsearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 5.6 ms |
| X3-H1 | elasticsearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 15.3 ms |
| X3-H1 | elasticsearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 41.5 ms |
| X3-H1 | lancedb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | lancedb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | lancedb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.3 ms |
| X3-H1 | lancedb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 12.7 ms |
| X3-H1 | lancedb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 56.5 ms |
| X3-H1 | milvus | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | milvus | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.8 ms |
| X3-H1 | milvus | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.2 ms |
| X3-H1 | milvus | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.2 ms |
| X3-H1 | milvus | G=40000 | inconclusive | 1 seeds, status ['ok'], median 47.6 ms |
| X3-H1 | mongodb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | mongodb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | mongodb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.4 ms |
| X3-H1 | mongodb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.0 ms |
| X3-H1 | mongodb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 24.0 ms |
| X3-H1 | opensearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | opensearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.2 ms |
| X3-H1 | opensearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 5.4 ms |
| X3-H1 | opensearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 8.6 ms |
| X3-H1 | opensearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 41.6 ms |
| X3-H1 | pgvector | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | pgvector | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | pgvector | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | pgvector | G=1000 | inconclusive | 1 seeds, status ['ok'], median 2.1 ms |
| X3-H1 | pgvector | G=4000 | inconclusive | 1 seeds, status ['ok'], median 8.9 ms |
| X3-H1 | pgvector | G=10000 | inconclusive | 1 seeds, status ['ok'], median 22.9 ms |
| X3-H1 | pgvector | G=40000 | inconclusive | 1 seeds, status ['ok'], median 96.8 ms |
| X3-H1 | qdrant | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | qdrant | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | qdrant | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | qdrant | G=4000 | inconclusive | 1 seeds, status ['ok'], median 47.9 ms |
| X3-H1 | qdrant | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.1 ms |
| X3-H1 | qdrant | G=40000 | inconclusive | 1 seeds, status ['ok'], median 43.1 ms |
| X3-H1 | redis | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | redis | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | redis | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.3 ms |
| X3-H1 | redis | G=10000 | inconclusive | 1 seeds, status ['ok'], median 8.6 ms |
| X3-H1 | redis | G=40000 | inconclusive | 1 seeds, status ['ok'], median 45.3 ms |
| X3-H1 | vespa | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | vespa | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.0 ms |
| X3-H1 | vespa | G=4000 | inconclusive | 1 seeds, status ['ok'], median 6.1 ms |
| X3-H1 | vespa | G=10000 | inconclusive | 1 seeds, status ['ok'], median 12.5 ms |
| X3-H1 | vespa | G=40000 | inconclusive | 1 seeds, status ['ok'], median 55.1 ms |
| X3-H1 | weaviate | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | weaviate | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | weaviate | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | weaviate | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.0 ms |
| X3-H1 | weaviate | G=10000 | inconclusive | 1 seeds, status ['ok'], median 10.5 ms |
| X3-H1 | weaviate | G=40000 | inconclusive | 1 seeds, status ['ok'], median 48.8 ms |
| X3-H2 | cassandra | G=40,000 predicted accepts | inconclusive | observed accepts in 1 seeds, ok share 1.000, first error None |
| X3-H2 | chroma | G=40,000 predicted refuses | inconclusive | observed not run in 0 seeds, ok share nan, first error None |
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
| X3-H3a | pgvector | p50 G=40,000 / G=1 | inconclusive | {'store': 'pgvector', 'top': 40000, 'bottom': 1, 'ratio': 328.20802352680056, 'lo': 292.0066587747855, 'hi': 328.20802352680056, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 591.4965, 'p50_bottom_ms': 1.8022} |
| X3-H3b | faiss | p50 G=40,000 / G=1 | inconclusive | {'store': 'faiss', 'top': 40000, 'bottom': 1, 'ratio': 1.7743365419838633, 'lo': 1.7562898208044755, 'hi': 1.8057237880176495, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 57.6395, 'p50_bottom_ms': 32.4851} |
| X3-H3b | memory | p50 G=40,000 / G=1 | inconclusive | {'store': 'memory', 'top': 40000, 'bottom': 1, 'ratio': 1.7588989112776119, 'lo': 1.724674621206422, 'hi': 1.78879054966131, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 58.031, 'p50_bottom_ms': 32.9928} |
| X3-H3c | cassandra | p50 G=100 / G=1,000 | inconclusive | {'store': 'cassandra', 'top': 100, 'bottom': 1000, 'ratio': 1.2879926622073778, 'lo': 1.2879926622073778, 'hi': 3.3291135940679375, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 172.2989, 'p50_bottom_ms': 133.7732} |
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

