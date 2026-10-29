# X4: engine filters against engine checks

Profile: ['smoke']. Files: 1; records: 141. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | FALSIFIED | control-oracle 0 subjects, some disagreeing; control-planted 0 subjects, counts NOT exact |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 5 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | INCONCLUSIVE | 30 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | INCONCLUSIVE | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [] |
| X4-H6 spicedb full-direct (a) N<=999 recall 1 | INCONCLUSIVE | 0 queries below 1 |
| X4-H6 spicedb full-direct (b) N in 1000-1001 recall below 1 | INCONCLUSIVE | mean 1.000 [1.000, 1.000] over 8 queries |
| X4-H6 spicedb full-direct (c) N>=10000 recall >= 0.99 | INCONCLUSIVE | {} |
| X4-H6 spicedb full-direct (d) no false completeness | INCONCLUSIVE | 0 false-complete results |
| X4-H6 spicedb full-folder (a) N<=999 recall 1 | INCONCLUSIVE | 0 queries below 1 |
| X4-H6 spicedb full-folder (b) N in 1000-1001 recall below 1 | INCONCLUSIVE | mean 1.000 [1.000, 1.000] over 8 queries |
| X4-H6 spicedb full-folder (c) N>=10000 recall >= 0.99 | INCONCLUSIVE | {} |
| X4-H6 spicedb full-folder (d) no false completeness | INCONCLUSIVE | 0 false-complete results |
| X4-H6 spicedb simple-direct (a) N<=999 recall 1 | INCONCLUSIVE | 0 queries below 1 |
| X4-H6 spicedb simple-direct (b) N in 1000-1001 recall below 1 | INCONCLUSIVE | mean 1.000 [1.000, 1.000] over 8 queries |
| X4-H6 spicedb simple-direct (c) N>=10000 recall >= 0.99 | INCONCLUSIVE | {} |
| X4-H6 spicedb simple-direct (d) no false completeness | INCONCLUSIVE | 0 false-complete results |
| X4-H7 caching spicedb | CONFIRMED | 15 cells; lowest median ratio 21.4 |

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
| spicedb | full-direct | 10 | lookup-limit | 1 | 1 | [10] | 0.009 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 10 | lookup-unlimited | 1 | 1 | [10] | 0.003 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 999 | lookup-limit | 1 | 1 | [999] | 0.049 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 999 | lookup-unlimited | 1 | 1 | [999] | 0.029 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1000 | lookup-limit | 1 | 1 | [1000] | 0.044 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1000 | lookup-unlimited | 1 | 1 | [1000] | 0.033 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1001 | lookup-limit | 1 | 1 | [1000] | 0.049 | 1 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1001 | lookup-unlimited | 1 | 1 | [1001] | 0.031 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 3000 | lookup-limit | 1 | 1 | [1000] | 0.070 | 2000 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 3000 | lookup-unlimited | 1 | 1 | [3000] | 0.091 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10 | lookup-limit | 1 | 1 | [10] | 0.005 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10 | lookup-unlimited | 1 | 1 | [10] | 0.004 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 999 | lookup-limit | 1 | 1 | [999] | 0.049 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 999 | lookup-unlimited | 1 | 1 | [999] | 0.035 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1000 | lookup-limit | 1 | 1 | [1000] | 0.060 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1000 | lookup-unlimited | 1 | 1 | [1000] | 0.029 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1001 | lookup-limit | 1 | 1 | [1000] | 0.053 | 1 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1001 | lookup-unlimited | 1 | 1 | [1001] | 0.041 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 3000 | lookup-limit | 1 | 1 | [1000] | 0.074 | 2000 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 3000 | lookup-unlimited | 1 | 1 | [3000] | 0.086 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10 | lookup-limit | 1 | 1 | [10] | 0.003 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10 | lookup-unlimited | 1 | 1 | [10] | 0.002 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 999 | lookup-limit | 1 | 1 | [999] | 0.030 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 999 | lookup-unlimited | 1 | 1 | [999] | 0.032 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1000 | lookup-limit | 1 | 1 | [1000] | 0.031 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1000 | lookup-unlimited | 1 | 1 | [1000] | 0.025 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1001 | lookup-limit | 1 | 1 | [1000] | 0.029 | 1 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1001 | lookup-unlimited | 1 | 1 | [1001] | 0.035 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 3000 | lookup-limit | 1 | 1 | [1000] | 0.030 | 2000 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 3000 | lookup-unlimited | 1 | 1 | [3000] | 0.076 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |

#### wardowl's filter_for

| engine | route | structure | N | timeout s | calls | outcomes | median s |
|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.002 |
| spicedb | adapter | full-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | full-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.029 |
| spicedb | adapter | full-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.024 |
| spicedb | adapter | full-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.025 |
| spicedb | adapter | full-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.025 |
| spicedb | adapter | full-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.032 |
| spicedb | adapter | full-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.043 |
| spicedb | adapter | full-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.031 |
| spicedb | adapter | full-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.027 |
| spicedb | adapter | full-folder | 10 | 2.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | full-folder | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | full-folder | 999 | 2.0 | 1 | {'exact': 1} | 0.025 |
| spicedb | adapter | full-folder | 999 | 10.0 | 1 | {'exact': 1} | 0.025 |
| spicedb | adapter | full-folder | 1000 | 2.0 | 1 | {'none': 1} | 0.024 |
| spicedb | adapter | full-folder | 1000 | 10.0 | 1 | {'none': 1} | 0.028 |
| spicedb | adapter | full-folder | 1001 | 2.0 | 1 | {'none': 1} | 0.052 |
| spicedb | adapter | full-folder | 1001 | 10.0 | 1 | {'none': 1} | 0.045 |
| spicedb | adapter | full-folder | 3000 | 2.0 | 1 | {'none': 1} | 0.044 |
| spicedb | adapter | full-folder | 3000 | 10.0 | 1 | {'none': 1} | 0.027 |
| spicedb | adapter | simple-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | simple-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | simple-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.024 |
| spicedb | adapter | simple-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.025 |
| spicedb | adapter | simple-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.023 |
| spicedb | adapter | simple-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.031 |
| spicedb | adapter | simple-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.028 |
| spicedb | adapter | simple-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.029 |
| spicedb | adapter | simple-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.026 |
| spicedb | adapter | simple-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.031 |

#### Permission-recall@10 through wardowl

| engine | route | structure | N | queries | failed | recall@10 [95% CI] | false complete | leaks | strategies | median s |
|---|---|---|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.008 |
| spicedb | adapter | full-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.035 |
| spicedb | adapter | full-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.041 |
| spicedb | adapter | full-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.051 |
| spicedb | adapter | full-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.036 |
| spicedb | adapter | full-folder | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.007 |
| spicedb | adapter | full-folder | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.038 |
| spicedb | adapter | full-folder | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.050 |
| spicedb | adapter | full-folder | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.052 |
| spicedb | adapter | full-folder | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.035 |
| spicedb | adapter | simple-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.007 |
| spicedb | adapter | simple-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.033 |
| spicedb | adapter | simple-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.042 |
| spicedb | adapter | simple-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.041 |
| spicedb | adapter | simple-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.032 |

## X4d: latency and caching

| engine | route | structure | N | records | filter_for uncached ms (median) | check per hit ms | filter speedup cached [95% CI] | check speedup cached [95% CI] |
|---|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 1 | 1.900 | 0.105 | 388.0 [388.0, 388.0] | 21.8 [21.8, 21.8] |
| spicedb | adapter | full-direct | 999 | 1 | 24.200 | 0.113 | 5124.9 [5124.9, 5124.9] | 23.4 [23.4, 23.4] |
| spicedb | adapter | full-direct | 1000 | 1 | 22.571 | 0.118 | 4604.4 [4604.4, 4604.4] | 25.0 [25.0, 25.0] |
| spicedb | adapter | full-direct | 1001 | 1 | 23.014 | 0.121 | 4727.5 [4727.5, 4727.5] | 24.5 [24.5, 24.5] |
| spicedb | adapter | full-direct | 3000 | 1 | 23.836 | 0.122 | 4896.9 [4896.9, 4896.9] | 24.5 [24.5, 24.5] |
| spicedb | adapter | full-folder | 10 | 1 | 1.428 | 0.118 | 283.1 [283.1, 283.1] | 24.0 [24.0, 24.0] |
| spicedb | adapter | full-folder | 999 | 1 | 24.692 | 0.113 | 4829.3 [4829.3, 4829.3] | 22.9 [22.9, 22.9] |
| spicedb | adapter | full-folder | 1000 | 1 | 27.109 | 0.110 | 5575.2 [5575.2, 5575.2] | 22.8 [22.8, 22.8] |
| spicedb | adapter | full-folder | 1001 | 1 | 30.275 | 0.117 | 6156.0 [6156.0, 6156.0] | 23.4 [23.4, 23.4] |
| spicedb | adapter | full-folder | 3000 | 1 | 24.705 | 0.120 | 5160.4 [5160.4, 5160.4] | 24.0 [24.0, 24.0] |
| spicedb | adapter | simple-direct | 10 | 1 | 1.561 | 0.107 | 314.1 [314.1, 314.1] | 21.4 [21.4, 21.4] |
| spicedb | adapter | simple-direct | 999 | 1 | 22.885 | 0.110 | 4588.1 [4588.1, 4588.1] | 23.4 [23.4, 23.4] |
| spicedb | adapter | simple-direct | 1000 | 1 | 23.169 | 0.132 | 4453.5 [4453.5, 4453.5] | 25.8 [25.8, 25.8] |
| spicedb | adapter | simple-direct | 1001 | 1 | 22.623 | 0.139 | 4126.0 [4126.0, 4126.0] | 28.0 [28.0, 28.0] |
| spicedb | adapter | simple-direct | 3000 | 1 | 22.827 | 0.125 | 4758.6 [4758.6, 4758.6] | 25.4 [25.4, 25.4] |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
