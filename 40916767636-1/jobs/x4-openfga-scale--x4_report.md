# X4: engine filters against engine checks

Profile: ['smoke']. Files: 1; records: 141. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | FALSIFIED | control-oracle 0 subjects, some disagreeing; control-planted 0 subjects, counts NOT exact |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | INCONCLUSIVE | 5 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | INCONCLUSIVE | 30 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | INCONCLUSIVE | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [] |
| X4-H6 openfga full-direct (a) N<=999 recall 1 | INCONCLUSIVE | 0 queries below 1 |
| X4-H6 openfga full-direct (b) N in 1000-1001 recall below 1 | INCONCLUSIVE | mean 1.000 [1.000, 1.000] over 8 queries |
| X4-H6 openfga full-direct (c) N>=10000 recall >= 0.99 | INCONCLUSIVE | {} |
| X4-H6 openfga full-direct (d) no false completeness | INCONCLUSIVE | 0 false-complete results |
| X4-H6 openfga full-folder (a) N<=999 recall 1 | INCONCLUSIVE | 0 queries below 1 |
| X4-H6 openfga full-folder (b) N in 1000-1001 recall below 1 | INCONCLUSIVE | mean 1.000 [1.000, 1.000] over 8 queries |
| X4-H6 openfga full-folder (c) N>=10000 recall >= 0.99 | INCONCLUSIVE | {} |
| X4-H6 openfga full-folder (d) no false completeness | INCONCLUSIVE | 0 false-complete results |
| X4-H6 openfga simple-direct (a) N<=999 recall 1 | INCONCLUSIVE | 0 queries below 1 |
| X4-H6 openfga simple-direct (b) N in 1000-1001 recall below 1 | INCONCLUSIVE | mean 1.000 [1.000, 1.000] over 8 queries |
| X4-H6 openfga simple-direct (c) N>=10000 recall >= 0.99 | INCONCLUSIVE | {} |
| X4-H6 openfga simple-direct (d) no false completeness | INCONCLUSIVE | 0 false-complete results |
| X4-H7 caching openfga | CONFIRMED | 15 cells; lowest median ratio 20.2 |

## X4a: one revision

| profile | subjects | with filter | errors | pairs | false admits | false denials | reproduce | subjects disagreeing [95% CI] | zero bound | pair rate [95% CI] | check vs oracle | check vs oracle rate | seeds | false admits on scalar fields |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## X4b: unpinned, under a writer

| engine | condition | trials | trials disagreeing [95% CI] | pairs | skew-explained | explained share | reproduce | oracle mismatches | median writes in window | seeds |
|---|---|---|---|---|---|---|---|---|---|---|

## X4c: truncation

#### Engine list calls

| engine | structure | N | api | calls | status 200 | counts | median s | missing | extra | with cursor | error lines | answer keys |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openfga | full-direct | 10 | list-objects | 1 | 1 | [10] | 0.022 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 10 | streamed-list-objects | 1 | 1 | [10] | 0.014 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 999 | list-objects | 1 | 1 | [999] | 0.014 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 999 | streamed-list-objects | 1 | 1 | [999] | 0.032 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 1000 | list-objects | 1 | 1 | [1000] | 0.016 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 1000 | streamed-list-objects | 1 | 1 | [1000] | 0.035 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 1001 | list-objects | 1 | 1 | [1000] | 0.016 | 1 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 1001 | streamed-list-objects | 1 | 1 | [1001] | 0.039 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 3000 | list-objects | 1 | 1 | [1000] | 0.019 | 2000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 3000 | streamed-list-objects | 1 | 1 | [3000] | 0.070 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 10 | list-objects | 1 | 1 | [10] | 0.011 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 10 | streamed-list-objects | 1 | 1 | [10] | 0.014 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 999 | list-objects | 1 | 1 | [999] | 0.027 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 999 | streamed-list-objects | 1 | 1 | [999] | 0.049 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 1000 | list-objects | 1 | 1 | [1000] | 0.026 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 1000 | streamed-list-objects | 1 | 1 | [1000] | 0.049 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 1001 | list-objects | 1 | 1 | [1000] | 0.024 | 1 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 1001 | streamed-list-objects | 1 | 1 | [1001] | 0.043 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 3000 | list-objects | 1 | 1 | [1000] | 0.031 | 2000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 3000 | streamed-list-objects | 1 | 1 | [3000] | 0.101 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 10 | list-objects | 1 | 1 | [10] | 0.002 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 10 | streamed-list-objects | 1 | 1 | [10] | 0.002 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 999 | list-objects | 1 | 1 | [999] | 0.004 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 999 | streamed-list-objects | 1 | 1 | [999] | 0.027 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 1000 | list-objects | 1 | 1 | [1000] | 0.005 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 1000 | streamed-list-objects | 1 | 1 | [1000] | 0.027 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 1001 | list-objects | 1 | 1 | [1000] | 0.006 | 1 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 1001 | streamed-list-objects | 1 | 1 | [1001] | 0.021 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 3000 | list-objects | 1 | 1 | [1000] | 0.007 | 2000 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 3000 | streamed-list-objects | 1 | 1 | [3000] | 0.066 | 0 | 0 | 0 | 0 | [()] |

#### wardowl's filter_for

| engine | route | structure | N | timeout s | calls | outcomes | median s |
|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.015 |
| openfga | adapter | full-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.015 |
| openfga | adapter | full-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.017 |
| openfga | adapter | full-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.017 |
| openfga | adapter | full-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.014 |
| openfga | adapter | full-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.014 |
| openfga | adapter | full-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.021 |
| openfga | adapter | full-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.015 |
| openfga | adapter | full-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.018 |
| openfga | adapter | full-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.017 |
| openfga | adapter | full-folder | 10 | 2.0 | 1 | {'exact': 1} | 0.010 |
| openfga | adapter | full-folder | 10 | 10.0 | 1 | {'exact': 1} | 0.013 |
| openfga | adapter | full-folder | 999 | 2.0 | 1 | {'exact': 1} | 0.021 |
| openfga | adapter | full-folder | 999 | 10.0 | 1 | {'exact': 1} | 0.021 |
| openfga | adapter | full-folder | 1000 | 2.0 | 1 | {'none': 1} | 0.027 |
| openfga | adapter | full-folder | 1000 | 10.0 | 1 | {'none': 1} | 0.024 |
| openfga | adapter | full-folder | 1001 | 2.0 | 1 | {'none': 1} | 0.024 |
| openfga | adapter | full-folder | 1001 | 10.0 | 1 | {'none': 1} | 0.036 |
| openfga | adapter | full-folder | 3000 | 2.0 | 1 | {'none': 1} | 0.030 |
| openfga | adapter | full-folder | 3000 | 10.0 | 1 | {'none': 1} | 0.032 |
| openfga | adapter | simple-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.001 |
| openfga | adapter | simple-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| openfga | adapter | simple-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.005 |
| openfga | adapter | simple-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.005 |
| openfga | adapter | simple-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.005 |
| openfga | adapter | simple-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.005 |
| openfga | adapter | simple-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.004 |
| openfga | adapter | simple-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.004 |
| openfga | adapter | simple-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.006 |
| openfga | adapter | simple-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.005 |

#### Permission-recall@10 through wardowl

| engine | route | structure | N | queries | failed | recall@10 [95% CI] | false complete | leaks | strategies | median s |
|---|---|---|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.036 |
| openfga | adapter | full-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.032 |
| openfga | adapter | full-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.121 |
| openfga | adapter | full-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.209 |
| openfga | adapter | full-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.071 |
| openfga | adapter | full-folder | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.030 |
| openfga | adapter | full-folder | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.037 |
| openfga | adapter | full-folder | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.212 |
| openfga | adapter | full-folder | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.204 |
| openfga | adapter | full-folder | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.072 |
| openfga | adapter | simple-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.009 |
| openfga | adapter | simple-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.015 |
| openfga | adapter | simple-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.025 |
| openfga | adapter | simple-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.057 |
| openfga | adapter | simple-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.034 |

## X4d: latency and caching

| engine | route | structure | N | records | filter_for uncached ms (median) | check per hit ms | filter speedup cached [95% CI] | check speedup cached [95% CI] |
|---|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 1 | 14.369 | 1.021 | 1467.8 [1467.8, 1467.8] | 108.4 [108.4, 108.4] |
| openfga | adapter | full-direct | 999 | 1 | 14.332 | 0.910 | 1227.4 [1227.4, 1227.4] | 96.9 [96.9, 96.9] |
| openfga | adapter | full-direct | 1000 | 1 | 18.087 | 1.093 | 2034.2 [2034.2, 2034.2] | 120.7 [120.7, 120.7] |
| openfga | adapter | full-direct | 1001 | 1 | 16.725 | 1.200 | 1152.0 [1152.0, 1152.0] | 130.8 [130.8, 130.8] |
| openfga | adapter | full-direct | 3000 | 1 | 17.170 | 1.230 | 1869.0 [1869.0, 1869.0] | 137.3 [137.3, 137.3] |
| openfga | adapter | full-folder | 10 | 1 | 12.727 | 0.889 | 1257.1 [1257.1, 1257.1] | 94.8 [94.8, 94.8] |
| openfga | adapter | full-folder | 999 | 1 | 20.361 | 0.856 | 2152.8 [2152.8, 2152.8] | 89.4 [89.4, 89.4] |
| openfga | adapter | full-folder | 1000 | 1 | 27.157 | 0.986 | 2804.6 [2804.6, 2804.6] | 102.8 [102.8, 102.8] |
| openfga | adapter | full-folder | 1001 | 1 | 22.842 | 0.932 | 2487.6 [2487.6, 2487.6] | 101.4 [101.4, 101.4] |
| openfga | adapter | full-folder | 3000 | 1 | 31.066 | 0.959 | 3368.6 [3368.6, 3368.6] | 102.8 [102.8, 102.8] |
| openfga | adapter | simple-direct | 10 | 1 | 1.303 | 0.190 | 132.4 [132.4, 132.4] | 20.2 [20.2, 20.2] |
| openfga | adapter | simple-direct | 999 | 1 | 4.076 | 0.316 | 432.1 [432.1, 432.1] | 34.5 [34.5, 34.5] |
| openfga | adapter | simple-direct | 1000 | 1 | 4.777 | 0.392 | 341.1 [341.1, 341.1] | 25.6 [25.6, 25.6] |
| openfga | adapter | simple-direct | 1001 | 1 | 4.318 | 0.313 | 467.7 [467.7, 467.7] | 33.6 [33.6, 33.6] |
| openfga | adapter | simple-direct | 3000 | 1 | 6.451 | 0.602 | 677.0 [677.0, 677.0] | 64.3 [64.3, 64.3] |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
