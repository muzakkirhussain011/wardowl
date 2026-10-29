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
| X4-H7 caching spicedb | CONFIRMED | 15 cells; lowest median ratio 18.0 |

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
| spicedb | full-direct | 10 | lookup-limit | 1 | 1 | [10] | 0.017 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 10 | lookup-unlimited | 1 | 1 | [10] | 0.003 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 999 | lookup-limit | 1 | 1 | [999] | 0.071 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 999 | lookup-unlimited | 1 | 1 | [999] | 0.033 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1000 | lookup-limit | 1 | 1 | [1000] | 0.044 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1000 | lookup-unlimited | 1 | 1 | [1000] | 0.031 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1001 | lookup-limit | 1 | 1 | [1000] | 0.045 | 1 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1001 | lookup-unlimited | 1 | 1 | [1001] | 0.032 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 3000 | lookup-limit | 1 | 1 | [1000] | 0.072 | 2000 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 3000 | lookup-unlimited | 1 | 1 | [3000] | 0.082 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10 | lookup-limit | 1 | 1 | [10] | 0.004 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10 | lookup-unlimited | 1 | 1 | [10] | 0.003 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 999 | lookup-limit | 1 | 1 | [999] | 0.045 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 999 | lookup-unlimited | 1 | 1 | [999] | 0.030 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1000 | lookup-limit | 1 | 1 | [1000] | 0.060 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1000 | lookup-unlimited | 1 | 1 | [1000] | 0.034 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1001 | lookup-limit | 1 | 1 | [1000] | 0.051 | 1 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1001 | lookup-unlimited | 1 | 1 | [1001] | 0.034 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 3000 | lookup-limit | 1 | 1 | [1000] | 0.064 | 2000 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 3000 | lookup-unlimited | 1 | 1 | [3000] | 0.079 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10 | lookup-limit | 1 | 1 | [10] | 0.003 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10 | lookup-unlimited | 1 | 1 | [10] | 0.005 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 999 | lookup-limit | 1 | 1 | [999] | 0.027 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 999 | lookup-unlimited | 1 | 1 | [999] | 0.031 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1000 | lookup-limit | 1 | 1 | [1000] | 0.026 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1000 | lookup-unlimited | 1 | 1 | [1000] | 0.030 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1001 | lookup-limit | 1 | 1 | [1000] | 0.032 | 1 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1001 | lookup-unlimited | 1 | 1 | [1001] | 0.027 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 3000 | lookup-limit | 1 | 1 | [1000] | 0.027 | 2000 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 3000 | lookup-unlimited | 1 | 1 | [3000] | 0.069 | 0 | 0 | 1 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |

#### wardowl's filter_for

| engine | route | structure | N | timeout s | calls | outcomes | median s |
|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | full-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | full-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.022 |
| spicedb | adapter | full-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.029 |
| spicedb | adapter | full-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.023 |
| spicedb | adapter | full-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.023 |
| spicedb | adapter | full-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.025 |
| spicedb | adapter | full-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.033 |
| spicedb | adapter | full-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.026 |
| spicedb | adapter | full-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.023 |
| spicedb | adapter | full-folder | 10 | 2.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | full-folder | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | full-folder | 999 | 2.0 | 1 | {'exact': 1} | 0.023 |
| spicedb | adapter | full-folder | 999 | 10.0 | 1 | {'exact': 1} | 0.023 |
| spicedb | adapter | full-folder | 1000 | 2.0 | 1 | {'none': 1} | 0.021 |
| spicedb | adapter | full-folder | 1000 | 10.0 | 1 | {'none': 1} | 0.027 |
| spicedb | adapter | full-folder | 1001 | 2.0 | 1 | {'none': 1} | 0.025 |
| spicedb | adapter | full-folder | 1001 | 10.0 | 1 | {'none': 1} | 0.024 |
| spicedb | adapter | full-folder | 3000 | 2.0 | 1 | {'none': 1} | 0.040 |
| spicedb | adapter | full-folder | 3000 | 10.0 | 1 | {'none': 1} | 0.021 |
| spicedb | adapter | simple-direct | 10 | 2.0 | 1 | {'exact': 1} | 0.002 |
| spicedb | adapter | simple-direct | 10 | 10.0 | 1 | {'exact': 1} | 0.001 |
| spicedb | adapter | simple-direct | 999 | 2.0 | 1 | {'exact': 1} | 0.025 |
| spicedb | adapter | simple-direct | 999 | 10.0 | 1 | {'exact': 1} | 0.026 |
| spicedb | adapter | simple-direct | 1000 | 2.0 | 1 | {'none': 1} | 0.026 |
| spicedb | adapter | simple-direct | 1000 | 10.0 | 1 | {'none': 1} | 0.025 |
| spicedb | adapter | simple-direct | 1001 | 2.0 | 1 | {'none': 1} | 0.023 |
| spicedb | adapter | simple-direct | 1001 | 10.0 | 1 | {'none': 1} | 0.028 |
| spicedb | adapter | simple-direct | 3000 | 2.0 | 1 | {'none': 1} | 0.028 |
| spicedb | adapter | simple-direct | 3000 | 10.0 | 1 | {'none': 1} | 0.028 |

#### Permission-recall@10 through wardowl

| engine | route | structure | N | queries | failed | recall@10 [95% CI] | false complete | leaks | strategies | median s |
|---|---|---|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.007 |
| spicedb | adapter | full-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.038 |
| spicedb | adapter | full-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.039 |
| spicedb | adapter | full-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.046 |
| spicedb | adapter | full-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.031 |
| spicedb | adapter | full-folder | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.007 |
| spicedb | adapter | full-folder | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.035 |
| spicedb | adapter | full-folder | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.045 |
| spicedb | adapter | full-folder | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.039 |
| spicedb | adapter | full-folder | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.030 |
| spicedb | adapter | simple-direct | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.005 |
| spicedb | adapter | simple-direct | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.029 |
| spicedb | adapter | simple-direct | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.039 |
| spicedb | adapter | simple-direct | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.038 |
| spicedb | adapter | simple-direct | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 4} | 0.030 |

## X4d: latency and caching

| engine | route | structure | N | records | filter_for uncached ms (median) | check per hit ms | filter speedup cached [95% CI] | check speedup cached [95% CI] |
|---|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 1 | 2.781 | 0.113 | 550.3 [550.3, 550.3] | 22.5 [22.5, 22.5] |
| spicedb | adapter | full-direct | 999 | 1 | 25.822 | 0.116 | 5255.8 [5255.8, 5255.8] | 22.8 [22.8, 22.8] |
| spicedb | adapter | full-direct | 1000 | 1 | 25.427 | 0.102 | 4983.8 [4983.8, 4983.8] | 19.8 [19.8, 19.8] |
| spicedb | adapter | full-direct | 1001 | 1 | 23.355 | 0.105 | 4769.2 [4769.2, 4769.2] | 20.8 [20.8, 20.8] |
| spicedb | adapter | full-direct | 3000 | 1 | 21.629 | 0.101 | 4420.9 [4420.9, 4420.9] | 19.9 [19.9, 19.9] |
| spicedb | adapter | full-folder | 10 | 1 | 2.077 | 0.100 | 420.7 [420.7, 420.7] | 20.0 [20.0, 20.0] |
| spicedb | adapter | full-folder | 999 | 1 | 23.405 | 0.100 | 4750.0 [4750.0, 4750.0] | 19.9 [19.9, 19.9] |
| spicedb | adapter | full-folder | 1000 | 1 | 21.110 | 0.097 | 4328.0 [4328.0, 4328.0] | 19.5 [19.5, 19.5] |
| spicedb | adapter | full-folder | 1001 | 1 | 23.884 | 0.108 | 4709.0 [4709.0, 4709.0] | 21.4 [21.4, 21.4] |
| spicedb | adapter | full-folder | 3000 | 1 | 22.951 | 0.096 | 4671.5 [4671.5, 4671.5] | 18.8 [18.8, 18.8] |
| spicedb | adapter | simple-direct | 10 | 1 | 1.506 | 0.101 | 283.5 [283.5, 283.5] | 19.9 [19.9, 19.9] |
| spicedb | adapter | simple-direct | 999 | 1 | 26.364 | 0.104 | 4916.0 [4916.0, 4916.0] | 20.3 [20.3, 20.3] |
| spicedb | adapter | simple-direct | 1000 | 1 | 21.639 | 0.100 | 4166.9 [4166.9, 4166.9] | 19.8 [19.8, 19.8] |
| spicedb | adapter | simple-direct | 1001 | 1 | 21.288 | 0.091 | 4107.7 [4107.7, 4107.7] | 18.0 [18.0, 18.0] |
| spicedb | adapter | simple-direct | 3000 | 1 | 23.121 | 0.098 | 4755.4 [4755.4, 4755.4] | 19.3 [19.3, 19.3] |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
