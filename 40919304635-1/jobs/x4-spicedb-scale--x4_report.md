# X4: engine filters against engine checks

Profile: ['full']. Files: 1; records: 5275.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | FALSIFIED | control-oracle 0 subjects, some disagreeing; control-planted 0 subjects, counts NOT exact |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | CONFIRMED | 135 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | CONFIRMED | 270 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | CONFIRMED | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [('spicedb', 'full-direct', 100000), ('spicedb', 'full-folder', 100000), ('spicedb', 'simple-direct', 100000)] |
| X4-H6 spicedb full-direct (a) N<=999 recall 1 | CONFIRMED | 0 queries below 1 |
| X4-H6 spicedb full-direct (b) N in 1000-1001 recall below 1 | CONFIRMED | mean 0.885 [0.865, 0.905] over 300 queries |
| X4-H6 spicedb full-direct (c) N>=10000 recall >= 0.99 | CONFIRMED | {10000: '1.000', 30000: '1.000', 100000: '1.000'} |
| X4-H6 spicedb full-direct (d) no false completeness | CONFIRMED | 0 false-complete results |
| X4-H6 spicedb full-folder (a) N<=999 recall 1 | CONFIRMED | 0 queries below 1 |
| X4-H6 spicedb full-folder (b) N in 1000-1001 recall below 1 | CONFIRMED | mean 0.877 [0.858, 0.896] over 300 queries |
| X4-H6 spicedb full-folder (c) N>=10000 recall >= 0.99 | CONFIRMED | {10000: '1.000', 30000: '1.000', 100000: '1.000'} |
| X4-H6 spicedb full-folder (d) no false completeness | CONFIRMED | 0 false-complete results |
| X4-H6 spicedb simple-direct (a) N<=999 recall 1 | CONFIRMED | 0 queries below 1 |
| X4-H6 spicedb simple-direct (b) N in 1000-1001 recall below 1 | CONFIRMED | mean 0.869 [0.849, 0.889] over 300 queries |
| X4-H6 spicedb simple-direct (c) N>=10000 recall >= 0.99 | CONFIRMED | {10000: '1.000', 30000: '1.000', 100000: '1.000'} |
| X4-H6 spicedb simple-direct (d) no false completeness | CONFIRMED | 0 false-complete results |
| X4-H7 caching spicedb | CONFIRMED | 27 cells; lowest median ratio 20.1 |

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
| spicedb | full-direct | 10 | lookup-limit | 15 | 15 | [10] | 0.002 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 10 | lookup-unlimited | 15 | 15 | [10] | 0.001 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 100 | lookup-limit | 15 | 15 | [100] | 0.003 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 100 | lookup-unlimited | 15 | 15 | [100] | 0.003 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 999 | lookup-limit | 15 | 15 | [999] | 0.029 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 999 | lookup-unlimited | 15 | 15 | [999] | 0.027 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1000 | lookup-limit | 15 | 15 | [1000] | 0.027 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1000 | lookup-unlimited | 15 | 15 | [1000] | 0.028 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1001 | lookup-limit | 15 | 15 | [1000] | 0.030 | 15 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 1001 | lookup-unlimited | 15 | 15 | [1001] | 0.027 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 3000 | lookup-limit | 15 | 15 | [1000] | 0.030 | 30000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 3000 | lookup-unlimited | 15 | 15 | [3000] | 0.083 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 10000 | lookup-limit | 15 | 15 | [1000] | 0.030 | 135000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 10000 | lookup-unlimited | 15 | 15 | [10000] | 0.266 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 30000 | lookup-limit | 15 | 15 | [1000] | 0.144 | 435000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 30000 | lookup-unlimited | 15 | 15 | [30000] | 0.811 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 100000 | lookup-limit | 15 | 15 | [1000] | 0.280 | 1485000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-direct | 100000 | lookup-unlimited | 15 | 15 | [100000] | 3.674 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10 | lookup-limit | 15 | 15 | [10] | 0.001 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10 | lookup-unlimited | 15 | 15 | [10] | 0.001 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 100 | lookup-limit | 15 | 15 | [100] | 0.004 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 100 | lookup-unlimited | 15 | 15 | [100] | 0.004 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 999 | lookup-limit | 15 | 15 | [999] | 0.029 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 999 | lookup-unlimited | 15 | 15 | [999] | 0.027 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1000 | lookup-limit | 15 | 15 | [1000] | 0.032 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1000 | lookup-unlimited | 15 | 15 | [1000] | 0.030 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1001 | lookup-limit | 15 | 15 | [1000] | 0.027 | 15 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 1001 | lookup-unlimited | 15 | 15 | [1001] | 0.030 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 3000 | lookup-limit | 15 | 15 | [1000] | 0.035 | 30000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 3000 | lookup-unlimited | 15 | 15 | [3000] | 0.079 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10000 | lookup-limit | 15 | 15 | [1000] | 0.035 | 135000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 10000 | lookup-unlimited | 15 | 15 | [10000] | 0.290 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 30000 | lookup-limit | 15 | 15 | [1000] | 0.031 | 435000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 30000 | lookup-unlimited | 15 | 15 | [30000] | 0.822 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 100000 | lookup-limit | 15 | 15 | [1000] | 0.771 | 1485000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | full-folder | 100000 | lookup-unlimited | 15 | 15 | [100000] | 3.419 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10 | lookup-limit | 15 | 15 | [10] | 0.001 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10 | lookup-unlimited | 15 | 15 | [10] | 0.001 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 100 | lookup-limit | 15 | 15 | [100] | 0.004 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 100 | lookup-unlimited | 15 | 15 | [100] | 0.004 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 999 | lookup-limit | 15 | 15 | [999] | 0.028 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 999 | lookup-unlimited | 15 | 15 | [999] | 0.027 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1000 | lookup-limit | 15 | 15 | [1000] | 0.026 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1000 | lookup-unlimited | 15 | 15 | [1000] | 0.027 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1001 | lookup-limit | 15 | 15 | [1000] | 0.027 | 15 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 1001 | lookup-unlimited | 15 | 15 | [1001] | 0.027 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 3000 | lookup-limit | 15 | 15 | [1000] | 0.026 | 30000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 3000 | lookup-unlimited | 15 | 15 | [3000] | 0.075 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10000 | lookup-limit | 15 | 15 | [1000] | 0.031 | 135000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 10000 | lookup-unlimited | 15 | 15 | [10000] | 0.255 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 30000 | lookup-limit | 15 | 15 | [1000] | 0.029 | 435000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 30000 | lookup-unlimited | 15 | 15 | [30000] | 0.761 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 100000 | lookup-limit | 15 | 15 | [1000] | 0.186 | 1485000 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |
| spicedb | simple-direct | 100000 | lookup-unlimited | 15 | 15 | [100000] | 2.643 | 0 | 0 | 15 | 0 | [('afterResultCursor', 'lookedUpAt', 'partialCaveatInfo', 'permissionship', 'resourceObjectId')] |

#### wardowl's filter_for

| engine | route | structure | N | timeout s | calls | outcomes | median s |
|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 2.0 | 5 | {'exact': 5} | 0.001 |
| spicedb | adapter | full-direct | 10 | 10.0 | 5 | {'exact': 5} | 0.002 |
| spicedb | adapter | full-direct | 100 | 2.0 | 5 | {'exact': 5} | 0.003 |
| spicedb | adapter | full-direct | 100 | 10.0 | 5 | {'exact': 5} | 0.004 |
| spicedb | adapter | full-direct | 999 | 2.0 | 5 | {'exact': 5} | 0.027 |
| spicedb | adapter | full-direct | 999 | 10.0 | 5 | {'exact': 5} | 0.034 |
| spicedb | adapter | full-direct | 1000 | 2.0 | 5 | {'none': 5} | 0.026 |
| spicedb | adapter | full-direct | 1000 | 10.0 | 5 | {'none': 5} | 0.026 |
| spicedb | adapter | full-direct | 1001 | 2.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | full-direct | 1001 | 10.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | full-direct | 3000 | 2.0 | 5 | {'none': 5} | 0.032 |
| spicedb | adapter | full-direct | 3000 | 10.0 | 5 | {'none': 5} | 0.028 |
| spicedb | adapter | full-direct | 10000 | 2.0 | 5 | {'none': 5} | 0.031 |
| spicedb | adapter | full-direct | 10000 | 10.0 | 5 | {'none': 5} | 0.026 |
| spicedb | adapter | full-direct | 30000 | 2.0 | 5 | {'none': 5} | 0.026 |
| spicedb | adapter | full-direct | 30000 | 10.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | full-direct | 100000 | 2.0 | 5 | {'none': 5} | 0.267 |
| spicedb | adapter | full-direct | 100000 | 10.0 | 5 | {'none': 5} | 0.026 |
| spicedb | adapter | full-folder | 10 | 2.0 | 5 | {'exact': 5} | 0.001 |
| spicedb | adapter | full-folder | 10 | 10.0 | 5 | {'exact': 5} | 0.002 |
| spicedb | adapter | full-folder | 100 | 2.0 | 5 | {'exact': 5} | 0.003 |
| spicedb | adapter | full-folder | 100 | 10.0 | 5 | {'exact': 5} | 0.004 |
| spicedb | adapter | full-folder | 999 | 2.0 | 5 | {'exact': 5} | 0.027 |
| spicedb | adapter | full-folder | 999 | 10.0 | 5 | {'exact': 5} | 0.032 |
| spicedb | adapter | full-folder | 1000 | 2.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | full-folder | 1000 | 10.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | full-folder | 1001 | 2.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | full-folder | 1001 | 10.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | full-folder | 3000 | 2.0 | 5 | {'none': 5} | 0.032 |
| spicedb | adapter | full-folder | 3000 | 10.0 | 5 | {'none': 5} | 0.026 |
| spicedb | adapter | full-folder | 10000 | 2.0 | 5 | {'none': 5} | 0.029 |
| spicedb | adapter | full-folder | 10000 | 10.0 | 5 | {'none': 5} | 0.024 |
| spicedb | adapter | full-folder | 30000 | 2.0 | 5 | {'none': 5} | 0.029 |
| spicedb | adapter | full-folder | 30000 | 10.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | full-folder | 100000 | 2.0 | 5 | {'none': 5} | 0.702 |
| spicedb | adapter | full-folder | 100000 | 10.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | simple-direct | 10 | 2.0 | 5 | {'exact': 5} | 0.001 |
| spicedb | adapter | simple-direct | 10 | 10.0 | 5 | {'exact': 5} | 0.002 |
| spicedb | adapter | simple-direct | 100 | 2.0 | 5 | {'exact': 5} | 0.003 |
| spicedb | adapter | simple-direct | 100 | 10.0 | 5 | {'exact': 5} | 0.004 |
| spicedb | adapter | simple-direct | 999 | 2.0 | 5 | {'exact': 5} | 0.029 |
| spicedb | adapter | simple-direct | 999 | 10.0 | 5 | {'exact': 5} | 0.027 |
| spicedb | adapter | simple-direct | 1000 | 2.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | simple-direct | 1000 | 10.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | simple-direct | 1001 | 2.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | simple-direct | 1001 | 10.0 | 5 | {'none': 5} | 0.026 |
| spicedb | adapter | simple-direct | 3000 | 2.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | simple-direct | 3000 | 10.0 | 5 | {'none': 5} | 0.027 |
| spicedb | adapter | simple-direct | 10000 | 2.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | simple-direct | 10000 | 10.0 | 5 | {'none': 5} | 0.024 |
| spicedb | adapter | simple-direct | 30000 | 2.0 | 5 | {'none': 5} | 0.024 |
| spicedb | adapter | simple-direct | 30000 | 10.0 | 5 | {'none': 5} | 0.025 |
| spicedb | adapter | simple-direct | 100000 | 2.0 | 5 | {'none': 5} | 0.172 |
| spicedb | adapter | simple-direct | 100000 | 10.0 | 5 | {'none': 5} | 0.025 |

#### Permission-recall@10 through wardowl

| engine | route | structure | N | queries | failed | recall@10 [95% CI] | false complete | leaks | strategies | median s |
|---|---|---|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.037 |
| spicedb | adapter | full-direct | 100 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.043 |
| spicedb | adapter | full-direct | 999 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.067 |
| spicedb | adapter | full-direct | 1000 | 150 | 0 | 0.885 [0.856, 0.913] | 0 | 0 | {'postfilter': 150} | 0.120 |
| spicedb | adapter | full-direct | 1001 | 150 | 0 | 0.885 [0.857, 0.912] | 0 | 0 | {'postfilter': 150} | 0.122 |
| spicedb | adapter | full-direct | 3000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.090 |
| spicedb | adapter | full-direct | 10000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.107 |
| spicedb | adapter | full-direct | 30000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.075 |
| spicedb | adapter | full-direct | 100000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.067 |
| spicedb | adapter | full-folder | 10 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.037 |
| spicedb | adapter | full-folder | 100 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.043 |
| spicedb | adapter | full-folder | 999 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.066 |
| spicedb | adapter | full-folder | 1000 | 150 | 0 | 0.876 [0.848, 0.902] | 0 | 0 | {'postfilter': 150} | 0.118 |
| spicedb | adapter | full-folder | 1001 | 150 | 0 | 0.879 [0.852, 0.905] | 0 | 0 | {'postfilter': 150} | 0.123 |
| spicedb | adapter | full-folder | 3000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.090 |
| spicedb | adapter | full-folder | 10000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.107 |
| spicedb | adapter | full-folder | 30000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.070 |
| spicedb | adapter | full-folder | 100000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.063 |
| spicedb | adapter | simple-direct | 10 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.036 |
| spicedb | adapter | simple-direct | 100 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.041 |
| spicedb | adapter | simple-direct | 999 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.062 |
| spicedb | adapter | simple-direct | 1000 | 150 | 0 | 0.884 [0.857, 0.910] | 0 | 0 | {'postfilter': 150} | 0.084 |
| spicedb | adapter | simple-direct | 1001 | 150 | 0 | 0.855 [0.826, 0.883] | 0 | 0 | {'postfilter': 150} | 0.085 |
| spicedb | adapter | simple-direct | 3000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.068 |
| spicedb | adapter | simple-direct | 10000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.088 |
| spicedb | adapter | simple-direct | 30000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.063 |
| spicedb | adapter | simple-direct | 100000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.062 |

## X4d: latency and caching

| engine | route | structure | N | records | filter_for uncached ms (median) | check per hit ms | filter speedup cached [95% CI] | check speedup cached [95% CI] |
|---|---|---|---|---|---|---|---|---|
| spicedb | adapter | full-direct | 10 | 5 | 1.227 | 0.113 | 247.2 [188.0, 322.4] | 20.9 [20.3, 44.8] |
| spicedb | adapter | full-direct | 100 | 5 | 3.734 | 0.121 | 730.9 [710.5, 818.2] | 22.8 [22.3, 25.6] |
| spicedb | adapter | full-direct | 999 | 5 | 25.252 | 0.111 | 5057.6 [4548.4, 5260.9] | 21.2 [19.9, 25.2] |
| spicedb | adapter | full-direct | 1000 | 5 | 24.257 | 0.106 | 4942.8 [4142.0, 5329.2] | 20.7 [20.6, 20.8] |
| spicedb | adapter | full-direct | 1001 | 5 | 27.929 | 0.110 | 5657.2 [4380.8, 5810.0] | 21.6 [19.8, 24.1] |
| spicedb | adapter | full-direct | 3000 | 5 | 26.294 | 0.114 | 5286.5 [4465.6, 6213.7] | 22.1 [20.7, 34.2] |
| spicedb | adapter | full-direct | 10000 | 5 | 23.693 | 0.106 | 4489.0 [4215.4, 5661.3] | 20.3 [19.1, 21.6] |
| spicedb | adapter | full-direct | 30000 | 5 | 25.212 | 0.114 | 4897.5 [4810.6, 6206.6] | 21.4 [20.9, 22.5] |
| spicedb | adapter | full-direct | 100000 | 5 | 25.034 | 0.195 | 5101.7 [4176.2, 6162.5] | 32.7 [30.3, 38.3] |
| spicedb | adapter | full-folder | 10 | 5 | 1.117 | 0.106 | 229.9 [221.2, 273.2] | 20.3 [14.9, 20.9] |
| spicedb | adapter | full-folder | 100 | 5 | 3.564 | 0.113 | 656.6 [500.4, 738.8] | 21.9 [18.8, 29.6] |
| spicedb | adapter | full-folder | 999 | 5 | 25.694 | 0.117 | 5175.6 [4972.3, 5347.1] | 22.9 [19.8, 27.4] |
| spicedb | adapter | full-folder | 1000 | 5 | 26.566 | 0.114 | 5190.7 [4510.0, 5619.5] | 22.2 [17.6, 22.8] |
| spicedb | adapter | full-folder | 1001 | 5 | 25.157 | 0.110 | 5110.6 [4735.0, 5220.9] | 22.1 [20.4, 25.6] |
| spicedb | adapter | full-folder | 3000 | 5 | 21.948 | 0.110 | 4326.8 [4200.7, 5792.6] | 20.6 [19.0, 32.4] |
| spicedb | adapter | full-folder | 10000 | 5 | 24.675 | 0.108 | 4754.9 [4556.2, 6159.1] | 20.1 [19.4, 27.9] |
| spicedb | adapter | full-folder | 30000 | 5 | 29.005 | 0.107 | 4982.4 [4349.7, 6245.4] | 20.8 [19.4, 23.6] |
| spicedb | adapter | full-folder | 100000 | 5 | 29.409 | 0.217 | 5730.0 [5119.9, 7497.2] | 37.2 [33.4, 39.9] |
| spicedb | adapter | simple-direct | 10 | 5 | 1.145 | 0.103 | 218.9 [211.3, 271.3] | 20.2 [19.7, 26.2] |
| spicedb | adapter | simple-direct | 100 | 5 | 3.514 | 0.110 | 566.9 [450.7, 797.3] | 21.0 [12.9, 22.9] |
| spicedb | adapter | simple-direct | 999 | 5 | 23.774 | 0.108 | 4966.3 [4327.0, 5359.4] | 20.5 [20.0, 24.2] |
| spicedb | adapter | simple-direct | 1000 | 5 | 24.438 | 0.109 | 4744.9 [4414.0, 5200.7] | 20.9 [19.4, 24.8] |
| spicedb | adapter | simple-direct | 1001 | 5 | 24.810 | 0.106 | 4723.1 [4463.5, 5699.8] | 21.0 [20.5, 27.4] |
| spicedb | adapter | simple-direct | 3000 | 5 | 23.712 | 0.112 | 4672.8 [4495.3, 5219.1] | 21.5 [19.5, 38.9] |
| spicedb | adapter | simple-direct | 10000 | 5 | 25.144 | 0.109 | 4879.1 [4369.2, 5323.6] | 20.5 [19.3, 22.3] |
| spicedb | adapter | simple-direct | 30000 | 5 | 27.370 | 0.107 | 5444.1 [4813.8, 6074.5] | 20.8 [20.5, 21.8] |
| spicedb | adapter | simple-direct | 100000 | 5 | 26.698 | 0.200 | 5151.0 [4009.2, 6498.7] | 32.2 [31.0, 34.6] |

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
