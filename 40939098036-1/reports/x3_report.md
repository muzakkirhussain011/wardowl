# X3: filter-size scaling

957 records (0 unreadable lines), 200 bootstrap resamples, seed 20261029. Verdicts follow PREREG_X3_X6.md.

## Health

| store | mode | seeds done | skipped | retrievals | errors | build s | setup error | seed errors | crashes (seed: status) |
|---|---|---|---|---|---|---|---|---|---|
| cassandra | smoke | [0] | [] | 42 | 0 | 13.600 | n/a | [] | {} |
| chroma | smoke | [] | [] | 27 | 9 | 3.600 | n/a | [] | {0: -11} |
| elasticsearch | smoke | [0] | [] | 42 | 0 | 6.600 | n/a | [] | {} |
| faiss | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] | {} |
| lancedb | smoke | [0] | [] | 42 | 0 | 0.700 | n/a | [] | {} |
| memory | smoke | [0] | [] | 42 | 0 | 0.100 | n/a | [] | {} |
| milvus | smoke | [0] | [] | 42 | 0 | 8.100 | n/a | [] | {} |
| mongodb | smoke | [0] | [] | 42 | 0 | 5.400 | n/a | [] | {} |
| opensearch | smoke | [0] | [] | 42 | 0 | 7.200 | n/a | [] | {} |
| pgvector | smoke | [0] | [] | 42 | 0 | 2.300 | n/a | [] | {} |
| qdrant | smoke | [0] | [] | 42 | 0 | 12.900 | n/a | [] | {} |
| redis | smoke | [0] | [] | 42 | 0 | 0.700 | n/a | [] | {} |
| vespa | smoke | [0] | [] | 42 | 0 | 20.200 | n/a | [] | {} |
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
| cassandra | 1 | accepts | 1.000 | 13.720 | 14.082 | 14.114 | 1.000 | ok | 0.053 | 19 |  |
| cassandra | 10 | accepts | 1.000 | 25.426 | 26.300 | 26.378 | 1.000 | ok | 0.101 | 20 |  |
| cassandra | 100 | accepts | 1.000 | 132 | 360 | 380 | 1.000 | ok | 0.866 | 21 |  |
| cassandra | 1000 | accepts | 1.000 | 113 | 114 | 114 | 1.000 | fallback | 5.229 | 39 |  |
| cassandra | 4000 | accepts | 1.000 | 115 | 120 | 120 | 1.000 | fallback | 16.323 | 39 |  |
| cassandra | 10000 | accepts | 1.000 | 139 | 164 | 166 | 1.000 | fallback | 43.087 | 39 |  |
| cassandra | 40000 | accepts | 1.000 | 256 | 259 | 259 | 1.000 | fallback | 238 | 39 |  |
| chroma | 1 | accepts | 1.000 | 427 | 430 | 430 | 1.000 | ok | 0.028 | 246 |  |
| chroma | 10 | accepts | 1.000 | 458 | 466 | 467 | 1.000 | ok | 0.030 | 727 |  |
| chroma | 100 | accepts | 1.000 | 766 | 767 | 767 | 1.000 | ok | 0.116 | 5879 |  |
| chroma | 1000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 0.968 | 60981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 4000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 3.662 | 249981 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 10000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 9.116 | 647983 | InternalError: Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000) |
| chroma | 40000 | refuses | n/a | n/a | n/a | n/a | n/a | ok | 82.202 | 2657983 | the process crashed, exit status -11 |
| elasticsearch | 1 | accepts | 1.000 | 19.033 | 20.735 | 20.886 | 0.933 | ok | 0.029 | 203 |  |
| elasticsearch | 10 | accepts | 1.000 | 14.620 | 15.410 | 15.480 | 0.933 | ok | 0.028 | 484 |  |
| elasticsearch | 100 | accepts | 1.000 | 12.827 | 13.993 | 14.097 | 0.933 | ok | 0.075 | 3465 |  |
| elasticsearch | 1000 | accepts | 1.000 | 18.996 | 23.361 | 23.749 | 0.933 | ok | 0.747 | 35066 |  |
| elasticsearch | 4000 | accepts | 1.000 | 32.192 | 34.419 | 34.617 | 0.933 | ok | 3.057 | 143066 |  |
| elasticsearch | 10000 | accepts | 1.000 | 53.874 | 55.480 | 55.623 | 0.933 | ok | 15.425 | 369067 |  |
| elasticsearch | 40000 | accepts | 1.000 | 109 | 110 | 110 | 0.933 | ok | 40.420 | 1509067 |  |
| faiss | 1 | accepts | 1.000 | 23.596 | 25.957 | 26.167 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 10 | accepts | 1.000 | 22.699 | 24.572 | 24.739 | 1.000 | in-process | 0.002 | n/a |  |
| faiss | 100 | accepts | 1.000 | 23.082 | 23.833 | 23.899 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 1000 | accepts | 1.000 | 24.093 | 25.172 | 25.268 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 4000 | accepts | 1.000 | 26.017 | 26.217 | 26.234 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 10000 | accepts | 1.000 | 29.730 | 31.264 | 31.400 | 1.000 | in-process | 0.001 | n/a |  |
| faiss | 40000 | accepts | 1.000 | 45.380 | 46.335 | 46.420 | 1.000 | in-process | 0.001 | n/a |  |
| lancedb | 1 | accepts | 1.000 | 6.686 | 6.706 | 6.708 | 1.000 | ok | 0.027 | 208 |  |
| lancedb | 10 | accepts | 1.000 | 6.585 | 6.786 | 6.803 | 1.000 | ok | 0.033 | 644 |  |
| lancedb | 100 | accepts | 1.000 | 6.911 | 7.077 | 7.092 | 1.000 | ok | 0.119 | 5346 |  |
| lancedb | 1000 | accepts | 1.000 | 13.728 | 13.728 | 13.728 | 1.000 | ok | 0.722 | 55948 |  |
| lancedb | 4000 | accepts | 1.000 | 35.308 | 35.402 | 35.410 | 1.000 | ok | 3.465 | 229948 |  |
| lancedb | 10000 | accepts | 1.000 | 77.448 | 80.236 | 80.484 | 1.000 | ok | 9.698 | 597950 |  |
| lancedb | 40000 | accepts | 1.000 | 300 | 301 | 301 | 1.000 | ok | 41.511 | 2457950 |  |
| memory | 1 | accepts | 1.000 | 22.868 | 24.062 | 24.168 | n/a | in-process | 0.002 | n/a |  |
| memory | 10 | accepts | 1.000 | 22.603 | 22.890 | 22.915 | n/a | in-process | 0.002 | n/a |  |
| memory | 100 | accepts | 1.000 | 22.813 | 23.301 | 23.345 | n/a | in-process | 0.001 | n/a |  |
| memory | 1000 | accepts | 1.000 | 24.229 | 24.496 | 24.520 | n/a | in-process | 0.001 | n/a |  |
| memory | 4000 | accepts | 1.000 | 26.014 | 26.450 | 26.488 | n/a | in-process | 0.001 | n/a |  |
| memory | 10000 | accepts | 1.000 | 29.165 | 29.678 | 29.723 | n/a | in-process | 0.001 | n/a |  |
| memory | 40000 | accepts | 1.000 | 45.967 | 46.636 | 46.696 | n/a | in-process | 0.001 | n/a |  |
| milvus | 1 | accepts | 1.000 | 2.904 | 3.261 | 3.292 | 0.867 | ok | 0.029 | 196 |  |
| milvus | 10 | accepts | 1.000 | 3.153 | 3.214 | 3.219 | 0.867 | ok | 0.033 | 477 |  |
| milvus | 100 | accepts | 1.000 | 3.167 | 3.437 | 3.461 | 0.867 | ok | 0.105 | 3458 |  |
| milvus | 1000 | accepts | 1.000 | 5.951 | 5.985 | 5.988 | 0.867 | ok | 0.798 | 35059 |  |
| milvus | 4000 | accepts | 1.000 | 16.683 | 17.283 | 17.336 | 0.867 | ok | 3.192 | 143059 |  |
| milvus | 10000 | accepts | 1.000 | 36.910 | 37.427 | 37.473 | 0.867 | ok | 9.224 | 369060 |  |
| milvus | 40000 | accepts | 1.000 | 125 | 147 | 149 | 0.867 | ok | 42.698 | 1509060 |  |
| mongodb | 1 | accepts | 1.000 | 8.681 | 8.854 | 8.869 | 1.000 | ok | 0.021 | 159 |  |
| mongodb | 10 | accepts | 1.000 | 10.896 | 13.319 | 13.534 | 1.000 | ok | 0.029 | 440 |  |
| mongodb | 100 | accepts | 1.000 | 10.150 | 11.153 | 11.242 | 1.000 | ok | 0.109 | 3421 |  |
| mongodb | 1000 | accepts | 1.000 | 19.222 | 20.280 | 20.374 | 1.000 | ok | 1.161 | 35022 |  |
| mongodb | 4000 | accepts | 1.000 | 53.867 | 59.115 | 59.582 | 1.000 | ok | 5.333 | 143022 |  |
| mongodb | 10000 | accepts | 1.000 | 39.207 | 40.111 | 40.192 | 1.000 | ok | 15.221 | 369023 |  |
| mongodb | 40000 | accepts | 1.000 | 140 | 189 | 194 | 1.000 | ok | 38.887 | 1509023 |  |
| opensearch | 1 | accepts | 1.000 | 17.542 | 20.681 | 20.960 | 1.000 | ok | 0.036 | 203 |  |
| opensearch | 10 | accepts | 1.000 | 19.502 | 20.278 | 20.347 | 1.000 | ok | 0.042 | 484 |  |
| opensearch | 100 | accepts | 1.000 | 18.447 | 19.187 | 19.253 | 1.000 | ok | 0.117 | 3465 |  |
| opensearch | 1000 | accepts | 1.000 | 17.249 | 17.450 | 17.468 | 1.000 | ok | 1.327 | 35066 |  |
| opensearch | 4000 | accepts | 1.000 | 27.986 | 28.548 | 28.598 | 1.000 | ok | 5.436 | 143066 |  |
| opensearch | 10000 | accepts | 1.000 | 29.384 | 34.288 | 34.724 | 1.000 | ok | 15.319 | 369067 |  |
| opensearch | 40000 | accepts | 1.000 | 103 | 109 | 110 | 1.000 | ok | 41.200 | 1509067 |  |
| pgvector | 1 | accepts | 1.000 | 1.252 | 1.428 | 1.443 | 1.000 | ok | 0.038 | 368 |  |
| pgvector | 10 | accepts | 1.000 | 1.438 | 1.779 | 1.809 | 1.000 | ok | 0.045 | 1470 |  |
| pgvector | 100 | accepts | 1.000 | 1.833 | 2.589 | 2.657 | 1.000 | ok | 0.183 | 3453 |  |
| pgvector | 1000 | accepts | 1.000 | 10.549 | 15.275 | 15.695 | 1.000 | ok | 1.591 | 36055 |  |
| pgvector | 4000 | accepts | 1.000 | 38.439 | 56.299 | 57.887 | 1.000 | ok | 6.775 | 150055 |  |
| pgvector | 10000 | accepts | 1.000 | 101 | 142 | 146 | 1.000 | ok | 24.178 | 398057 |  |
| pgvector | 40000 | accepts | 1.000 | 406 | 625 | 644 | 1.000 | ok | 72.597 | 1658057 |  |
| qdrant | 1 | accepts | 1.000 | 2.760 | 2.806 | 2.810 | 1.000 | ok | 0.133 | 433 |  |
| qdrant | 10 | accepts | 1.000 | 2.660 | 2.661 | 2.661 | 1.000 | ok | 0.055 | 507 |  |
| qdrant | 100 | accepts | 1.000 | 2.939 | 2.984 | 2.988 | 1.000 | ok | 0.118 | 1418 |  |
| qdrant | 1000 | accepts | 1.000 | 4.446 | 4.509 | 4.515 | 1.000 | ok | 0.874 | 12319 |  |
| qdrant | 4000 | accepts | 1.000 | 10.666 | 10.785 | 10.795 | 1.000 | ok | 3.518 | 51319 |  |
| qdrant | 10000 | accepts | 1.000 | 24.285 | 24.842 | 24.891 | 1.000 | ok | 9.450 | 139320 |  |
| qdrant | 40000 | accepts | 1.000 | 96.784 | 97.265 | 97.308 | 1.000 | ok | 40.566 | 589320 |  |
| redis | 1 | accepts | 1.000 | 0.816 | 1.599 | 1.669 | 1.000 | ok | 0.040 | 172 |  |
| redis | 10 | accepts | 1.000 | 0.533 | 0.584 | 0.588 | 1.000 | ok | 0.025 | 599 |  |
| redis | 100 | accepts | 1.000 | 0.696 | 0.730 | 0.733 | 1.000 | ok | 0.056 | 5211 |  |
| redis | 1000 | accepts | 1.000 | 2.029 | 2.126 | 2.135 | 1.000 | ok | 0.506 | 54913 |  |
| redis | 4000 | accepts | 1.000 | 6.237 | 6.274 | 6.277 | 1.000 | ok | 2.362 | 225913 |  |
| redis | 10000 | accepts | 1.000 | 16.100 | 16.178 | 16.185 | 1.000 | ok | 7.111 | 587915 |  |
| redis | 40000 | accepts | 1.000 | 72.584 | 72.702 | 72.713 | 1.000 | ok | 33.370 | 2417915 |  |
| vespa | 1 | accepts | 1.000 | 12.216 | 15.019 | 15.268 | 0.933 | ok | 0.029 | 186 |  |
| vespa | 10 | accepts | 1.000 | 11.665 | 11.812 | 11.826 | 0.933 | ok | 0.029 | 640 |  |
| vespa | 100 | accepts | 1.000 | 11.182 | 11.580 | 11.616 | 0.933 | ok | 0.181 | 5522 |  |
| vespa | 1000 | accepts | 1.000 | 23.653 | 24.442 | 24.512 | 0.933 | ok | 1.105 | 57924 |  |
| vespa | 4000 | accepts | 1.000 | 40.527 | 44.809 | 45.190 | 0.933 | ok | 4.374 | 237924 |  |
| vespa | 10000 | accepts | 1.000 | 74.092 | 96.386 | 98.367 | 0.933 | ok | 13.959 | 617926 |  |
| vespa | 40000 | accepts | 1.000 | 253 | 254 | 254 | 0.933 | ok | 55.499 | 2537926 |  |
| weaviate | 1 | accepts | 1.000 | 1.670 | 1.733 | 1.738 | 1.000 | ok | 0.209 | 75 |  |
| weaviate | 10 | accepts | 1.000 | 1.923 | 1.944 | 1.946 | 1.000 | ok | 0.102 | 75 |  |
| weaviate | 100 | accepts | 1.000 | 3.160 | 3.192 | 3.195 | 1.000 | ok | 0.141 | 75 |  |
| weaviate | 1000 | accepts | 1.000 | 10.956 | 11.204 | 11.226 | 1.000 | ok | 0.891 | 75 |  |
| weaviate | 4000 | accepts | 1.000 | 40.110 | 40.363 | 40.385 | 1.000 | ok | 3.544 | 75 |  |
| weaviate | 10000 | accepts | 1.000 | 104 | 107 | 107 | 1.000 | ok | 10.536 | 75 |  |
| weaviate | 40000 | accepts | 1.000 | 400 | 403 | 403 | 1.000 | ok | 45.807 | 75 |  |

## Latency ratios (p50, paired by query)

| store | G top | G bottom | ratio | interval | pairs |
|---|---|---|---|---|---|
| pgvector | 40000 | 1 | 324 | [301.99, 448.67] | 3 |
| faiss | 40000 | 1 | 1.923 | [1.73, 1.97] | 3 |
| memory | 40000 | 1 | 2.010 | [1.90, 2.09] | 3 |
| cassandra | 100 | 1000 | 1.176 | [1.18, 3.39] | 3 |
| cassandra | 40000 | 1 | 18.662 | [18.36, 19.30] | 3 |
| elasticsearch | 40000 | 1 | 5.725 | [4.96, 6.65] | 3 |
| lancedb | 40000 | 1 | 44.897 | [44.12, 45.09] | 3 |
| milvus | 40000 | 1 | 43.098 | [37.12, 51.45] | 3 |
| mongodb | 40000 | 1 | 16.081 | [16.08, 21.95] | 3 |
| opensearch | 40000 | 1 | 5.876 | [4.90, 6.96] | 3 |
| qdrant | 40000 | 1 | 35.071 | [33.88, 35.56] | 3 |
| redis | 40000 | 1 | 89.006 | [43.04, 98.54] | 3 |
| vespa | 40000 | 1 | 20.677 | [16.38, 25.49] | 3 |
| weaviate | 40000 | 1 | 240 | [231.66, 240.33] | 3 |

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
| X3-H1 | cassandra | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | cassandra | G=1000 | inconclusive | 1 seeds, status ['fallback'], median 5.2 ms |
| X3-H1 | cassandra | G=4000 | inconclusive | 1 seeds, status ['fallback'], median 16.3 ms |
| X3-H1 | cassandra | G=10000 | inconclusive | 1 seeds, status ['fallback'], median 43.1 ms |
| X3-H1 | cassandra | G=40000 | inconclusive | 1 seeds, status ['fallback'], median 237.6 ms |
| X3-H1 | chroma | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | chroma | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | chroma | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.0 ms |
| X3-H1 | chroma | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.7 ms |
| X3-H1 | chroma | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.1 ms |
| X3-H1 | chroma | G=40000 | inconclusive | 1 seeds, status ['ok'], median 82.2 ms |
| X3-H1 | elasticsearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | elasticsearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | elasticsearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | elasticsearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.1 ms |
| X3-H1 | elasticsearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 15.4 ms |
| X3-H1 | elasticsearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 40.4 ms |
| X3-H1 | lancedb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | lancedb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | lancedb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.7 ms |
| X3-H1 | lancedb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.5 ms |
| X3-H1 | lancedb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.7 ms |
| X3-H1 | lancedb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 41.5 ms |
| X3-H1 | milvus | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | milvus | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | milvus | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.8 ms |
| X3-H1 | milvus | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.2 ms |
| X3-H1 | milvus | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.2 ms |
| X3-H1 | milvus | G=40000 | inconclusive | 1 seeds, status ['ok'], median 42.7 ms |
| X3-H1 | mongodb | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | mongodb | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | mongodb | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.2 ms |
| X3-H1 | mongodb | G=4000 | inconclusive | 1 seeds, status ['ok'], median 5.3 ms |
| X3-H1 | mongodb | G=10000 | inconclusive | 1 seeds, status ['ok'], median 15.2 ms |
| X3-H1 | mongodb | G=40000 | inconclusive | 1 seeds, status ['ok'], median 38.9 ms |
| X3-H1 | opensearch | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | opensearch | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | opensearch | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.3 ms |
| X3-H1 | opensearch | G=4000 | inconclusive | 1 seeds, status ['ok'], median 5.4 ms |
| X3-H1 | opensearch | G=10000 | inconclusive | 1 seeds, status ['ok'], median 15.3 ms |
| X3-H1 | opensearch | G=40000 | inconclusive | 1 seeds, status ['ok'], median 41.2 ms |
| X3-H1 | pgvector | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | pgvector | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | pgvector | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | pgvector | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.6 ms |
| X3-H1 | pgvector | G=4000 | inconclusive | 1 seeds, status ['ok'], median 6.8 ms |
| X3-H1 | pgvector | G=10000 | inconclusive | 1 seeds, status ['ok'], median 24.2 ms |
| X3-H1 | pgvector | G=40000 | inconclusive | 1 seeds, status ['ok'], median 72.6 ms |
| X3-H1 | qdrant | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | qdrant | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | qdrant | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.5 ms |
| X3-H1 | qdrant | G=10000 | inconclusive | 1 seeds, status ['ok'], median 9.4 ms |
| X3-H1 | qdrant | G=40000 | inconclusive | 1 seeds, status ['ok'], median 40.6 ms |
| X3-H1 | redis | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | redis | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | redis | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.5 ms |
| X3-H1 | redis | G=4000 | inconclusive | 1 seeds, status ['ok'], median 2.4 ms |
| X3-H1 | redis | G=10000 | inconclusive | 1 seeds, status ['ok'], median 7.1 ms |
| X3-H1 | redis | G=40000 | inconclusive | 1 seeds, status ['ok'], median 33.4 ms |
| X3-H1 | vespa | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.0 ms |
| X3-H1 | vespa | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | vespa | G=1000 | inconclusive | 1 seeds, status ['ok'], median 1.1 ms |
| X3-H1 | vespa | G=4000 | inconclusive | 1 seeds, status ['ok'], median 4.4 ms |
| X3-H1 | vespa | G=10000 | inconclusive | 1 seeds, status ['ok'], median 14.0 ms |
| X3-H1 | vespa | G=40000 | inconclusive | 1 seeds, status ['ok'], median 55.5 ms |
| X3-H1 | weaviate | G=1 | inconclusive | 1 seeds, status ['ok'], median 0.2 ms |
| X3-H1 | weaviate | G=10 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=100 | inconclusive | 1 seeds, status ['ok'], median 0.1 ms |
| X3-H1 | weaviate | G=1000 | inconclusive | 1 seeds, status ['ok'], median 0.9 ms |
| X3-H1 | weaviate | G=4000 | inconclusive | 1 seeds, status ['ok'], median 3.5 ms |
| X3-H1 | weaviate | G=10000 | inconclusive | 1 seeds, status ['ok'], median 10.5 ms |
| X3-H1 | weaviate | G=40000 | inconclusive | 1 seeds, status ['ok'], median 45.8 ms |
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
| X3-H3a | pgvector | p50 G=40,000 / G=1 | inconclusive | {'store': 'pgvector', 'top': 40000, 'bottom': 1, 'ratio': 324.1550994329526, 'lo': 301.9886590527913, 'hi': 448.67088170259814, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 405.8746, 'p50_bottom_ms': 1.2521} |
| X3-H3b | faiss | p50 G=40,000 / G=1 | inconclusive | {'store': 'faiss', 'top': 40000, 'bottom': 1, 'ratio': 1.9232187356964856, 'lo': 1.7307868339753614, 'hi': 1.9682313651697774, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 45.3795, 'p50_bottom_ms': 23.5956} |
| X3-H3b | memory | p50 G=40,000 / G=1 | inconclusive | {'store': 'memory', 'top': 40000, 'bottom': 1, 'ratio': 2.0100883771575004, 'lo': 1.8998896434284112, 'hi': 2.086692368516277, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 45.9665, 'p50_bottom_ms': 22.8679} |
| X3-H3c | cassandra | p50 G=100 / G=1,000 | inconclusive | {'store': 'cassandra', 'top': 100, 'bottom': 1000, 'ratio': 1.1756021811242847, 'lo': 1.1756021811242847, 'hi': 3.386430188493528, 'pairs': 3, 'seeds': 1, 'p50_top_ms': 132.3326, 'p50_bottom_ms': 112.5658} |
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

