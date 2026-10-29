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
| openfga | full-direct | 10 | list-objects | 1 | 1 | [10] | 0.024 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 10 | streamed-list-objects | 1 | 1 | [10] | 0.016 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 999 | list-objects | 1 | 1 | [999] | 0.016 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 999 | streamed-list-objects | 1 | 1 | [999] | 0.042 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 1000 | list-objects | 1 | 1 | [1000] | 0.015 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 1000 | streamed-list-objects | 1 | 1 | [1000] | 0.039 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 1001 | list-objects | 1 | 1 | [1000] | 0.016 | 1 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 1001 | streamed-list-objects | 1 | 1 | [1001] | 0.049 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 3000 | list-objects | 1 | 1 | [1000] | 0.018 | 2000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 3000 | streamed-list-objects | 1 | 1 | [3000] | 0.080 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 10 | list-objects | 1 | 1 | [10] | 0.013 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 10 | streamed-list-objects | 1 | 1 | [10] | 0.014 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 999 | list-objects | 1 | 1 | [999] | 0.026 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 999 | streamed-list-objects | 1 | 1 | [999] | 0.038 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 1000 | list-objects | 1 | 1 | [1000] | 0.024 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 1000 | streamed-list-objects | 1 | 1 | [1000] | 0.053 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 1001 | list-objects | 1 | 1 | [1000] | 0.027 | 1 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 1001 | streamed-list-objects | 1 | 1 | [1001] | 0.046 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 3000 | list-objects | 1 | 1 | [1000] | 0.032 | 2000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 3000 | streamed-list-objects | 1 | 1 | [3000] | 0.111 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 10 | list-objects | 1 | 1 | [10] | 0.002 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 10 | streamed-list-objects | 1 | 1 | [10] | 0.002 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 999 | list-objects | 1 | 1 | [999] | 0.004 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 999 | streamed-list-objects | 1 | 1 | [999] | 0.025 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 1000 | list-objects | 1 | 1 | [1000] | 0.006 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 1000 | streamed-list-objects | 1 | 1 | [1000] | 0.033 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 1001 | list-objects | 1 | 1 | [1000] | 0.004 | 1 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 1001 | streamed-list-objects | 1 | 1 | [1001] | 0.021 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 3000 | list-objects | 1 | 1 | [1000] | 0.006 | 2000 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 3000 | streamed-list-objects | 1 | 1 | [3000] | 0.066 | 0 | 0 | 0 | 0 | [()] |

#### wardowl's filter_for

| engine | route | structure | N | timeout s | calls | outcomes | median s |
|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.012 |
| openfga | adapter | full-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.011 |
| openfga | adapter | full-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.015 |
| openfga | adapter | full-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.015 |
| openfga | adapter | full-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.016 |
| openfga | adapter | full-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.014 |
| openfga | adapter | full-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.019 |
| openfga | adapter | full-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.018 |
| openfga | adapter | full-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.018 |
| openfga | adapter | full-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.016 |
| openfga | adapter | full-folder | 10 | 2.0 | 1 | {'exact': 1} | 0.013 |
| openfga | adapter | full-folder | 10 | 10.0 | 1 | {'exact': 1} | 0.012 |
| openfga | adapter | full-folder | 999 | 2.0 | 1 | {'exact': 1} | 0.019 |
| openfga | adapter | full-folder | 999 | 10.0 | 1 | {'exact': 1} | 0.024 |
| openfga | adapter | full-folder | 1000 | 2.0 | 1 | {'none': 1} | 0.030 |
| openfga | adapter | full-folder | 1000 | 10.0 | 1 | {'none': 1} | 0.020 |
| openfga | adapter | full-folder | 1001 | 2.0 | 1 | {'none': 1} | 0.022 |
| openfga | adapter | full-folder | 1001 | 10.0 | 1 | {'none': 1} | 0.025 |
| openfga | adapter | full-folder | 3000 | 2.0 | 1 | {'none': 1} | 0.037 |
| openfga | adapter | full-folder | 3000 | 10.0 | 1 | {'none': 1} | 0.027 |
| openfga | adapter | simple-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.001 |
| openfga | adapter | simple-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| openfga | adapter | simple-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.005 |
| openfga | adapter | simple-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.004 |
| openfga | adapter | simple-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.004 |
| openfga | adapter | simple-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.004 |
| openfga | adapter | simple-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.004 |
| openfga | adapter | simple-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.004 |
| openfga | adapter | simple-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.006 |
| openfga | adapter | simple-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.005 |

#### Permission-recall@10 through wardowl

| engine | route | structure | N | queries | failed | recall@10 [95% CI] | false complete | leaks | strategies | median s |
|---|---|---|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.037 |
| openfga | adapter | full-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.033 |
| openfga | adapter | full-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.117 |
| openfga | adapter | full-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.208 |
| openfga | adapter | full-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.065 |
| openfga | adapter | full-folder | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.031 |
| openfga | adapter | full-folder | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.037 |
| openfga | adapter | full-folder | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.199 |
| openfga | adapter | full-folder | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.184 |
| openfga | adapter | full-folder | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.075 |
| openfga | adapter | simple-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.009 |
| openfga | adapter | simple-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.014 |
| openfga | adapter | simple-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.028 |
| openfga | adapter | simple-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.055 |
| openfga | adapter | simple-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.032 |

## X4d: latency and caching

| engine | route | structure | N | records | filter_for uncached ms (median) | check per hit ms | filter speedup cached [95% CI] | check speedup cached [95% CI] |
|---|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 1 | 11.868 | 0.926 | 1173.5 [1173.5, 1173.5] | 98.3 [98.3, 98.3] |
| openfga | adapter | full-direct | 999 | 1 | 15.088 | 0.912 | 1618.4 [1618.4, 1618.4] | 95.4 [95.4, 95.4] |
| openfga | adapter | full-direct | 1000 | 1 | 19.319 | 1.115 | 1253.0 [1253.0, 1253.0] | 117.7 [117.7, 117.7] |
| openfga | adapter | full-direct | 1001 | 1 | 16.087 | 0.976 | 1645.2 [1645.2, 1645.2] | 106.1 [106.1, 106.1] |
| openfga | adapter | full-direct | 3000 | 1 | 17.385 | 1.177 | 1824.6 [1824.6, 1824.6] | 125.7 [125.7, 125.7] |
| openfga | adapter | full-folder | 10 | 1 | 12.903 | 0.861 | 1364.4 [1364.4, 1364.4] | 91.5 [91.5, 91.5] |
| openfga | adapter | full-folder | 999 | 1 | 19.330 | 0.853 | 1907.6 [1907.6, 1907.6] | 87.6 [87.6, 87.6] |
| openfga | adapter | full-folder | 1000 | 1 | 24.566 | 1.072 | 1722.6 [1722.6, 1722.6] | 70.2 [70.2, 70.2] |
| openfga | adapter | full-folder | 1001 | 1 | 18.382 | 0.861 | 1904.3 [1904.3, 1904.3] | 92.2 [92.2, 92.2] |
| openfga | adapter | full-folder | 3000 | 1 | 31.171 | 0.872 | 3359.8 [3359.8, 3359.8] | 91.1 [91.1, 91.1] |
| openfga | adapter | simple-direct | 10 | 1 | 1.920 | 0.190 | 186.5 [186.5, 186.5] | 20.2 [20.2, 20.2] |
| openfga | adapter | simple-direct | 999 | 1 | 4.557 | 0.336 | 495.0 [495.0, 495.0] | 35.6 [35.6, 35.6] |
| openfga | adapter | simple-direct | 1000 | 1 | 4.444 | 0.347 | 304.7 [304.7, 304.7] | 37.2 [37.2, 37.2] |
| openfga | adapter | simple-direct | 1001 | 1 | 3.692 | 0.323 | 352.3 [352.3, 352.3] | 34.9 [34.9, 34.9] |
| openfga | adapter | simple-direct | 3000 | 1 | 5.048 | 0.606 | 521.6 [521.6, 521.6] | 65.1 [65.1, 65.1] |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
