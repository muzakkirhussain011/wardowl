# X4: engine filters against engine checks

Profile: ['full']. Files: 1; records: 5275.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | FALSIFIED | control-oracle 0 subjects, some disagreeing; control-planted 0 subjects, counts NOT exact |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | CONFIRMED | 135 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | CONFIRMED | 270 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | CONFIRMED | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [('openfga', 'full-direct', 100000), ('openfga', 'full-folder', 100000)] |
| X4-H6 openfga full-direct (a) N<=999 recall 1 | CONFIRMED | 0 queries below 1 |
| X4-H6 openfga full-direct (b) N in 1000-1001 recall below 1 | CONFIRMED | mean 0.884 [0.865, 0.902] over 300 queries |
| X4-H6 openfga full-direct (c) N>=10000 recall >= 0.99 | CONFIRMED | {10000: '1.000', 30000: '1.000', 100000: '1.000'} |
| X4-H6 openfga full-direct (d) no false completeness | CONFIRMED | 0 false-complete results |
| X4-H6 openfga full-folder (a) N<=999 recall 1 | CONFIRMED | 0 queries below 1 |
| X4-H6 openfga full-folder (b) N in 1000-1001 recall below 1 | CONFIRMED | mean 0.885 [0.866, 0.904] over 300 queries |
| X4-H6 openfga full-folder (c) N>=10000 recall >= 0.99 | CONFIRMED | {10000: '1.000', 30000: '1.000', 100000: '1.000'} |
| X4-H6 openfga full-folder (d) no false completeness | CONFIRMED | 0 false-complete results |
| X4-H6 openfga simple-direct (a) N<=999 recall 1 | CONFIRMED | 0 queries below 1 |
| X4-H6 openfga simple-direct (b) N in 1000-1001 recall below 1 | CONFIRMED | mean 0.877 [0.856, 0.897] over 300 queries |
| X4-H6 openfga simple-direct (c) N>=10000 recall >= 0.99 | CONFIRMED | {10000: '1.000', 30000: '1.000', 100000: '1.000'} |
| X4-H6 openfga simple-direct (d) no false completeness | CONFIRMED | 0 false-complete results |
| X4-H7 caching openfga | CONFIRMED | 27 cells; lowest median ratio 20.2 |

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
| openfga | full-direct | 10 | list-objects | 15 | 15 | [10] | 0.161 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 10 | streamed-list-objects | 15 | 15 | [10] | 0.157 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 100 | list-objects | 15 | 15 | [100] | 0.159 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 100 | streamed-list-objects | 15 | 15 | [100] | 0.155 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 999 | list-objects | 15 | 15 | [999] | 0.155 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 999 | streamed-list-objects | 15 | 15 | [999] | 0.169 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 1000 | list-objects | 15 | 15 | [1000] | 0.159 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 1000 | streamed-list-objects | 15 | 15 | [1000] | 0.177 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 1001 | list-objects | 15 | 15 | [1000] | 0.157 | 15 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 1001 | streamed-list-objects | 15 | 15 | [1001] | 0.171 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 3000 | list-objects | 15 | 15 | [1000] | 0.151 | 30000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 3000 | streamed-list-objects | 15 | 15 | [3000] | 0.196 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 10000 | list-objects | 15 | 15 | [1000] | 0.163 | 135000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 10000 | streamed-list-objects | 15 | 15 | [10000] | 0.311 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 30000 | list-objects | 15 | 15 | [1000] | 0.184 | 435000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 30000 | streamed-list-objects | 15 | 15 | [30000] | 0.679 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-direct | 100000 | list-objects | 15 | 15 | [1000] | 0.273 | 1485000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-direct | 100000 | streamed-list-objects | 15 | 15 | [100000] | 1.933 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 10 | list-objects | 15 | 15 | [10] | 0.152 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 10 | streamed-list-objects | 15 | 15 | [10] | 0.153 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 100 | list-objects | 15 | 15 | [100] | 0.156 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 100 | streamed-list-objects | 15 | 15 | [100] | 0.159 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 999 | list-objects | 15 | 15 | [999] | 0.161 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 999 | streamed-list-objects | 15 | 15 | [999] | 0.171 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 1000 | list-objects | 15 | 15 | [1000] | 0.166 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 1000 | streamed-list-objects | 15 | 15 | [1000] | 0.175 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 1001 | list-objects | 15 | 15 | [1000] | 0.152 | 15 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 1001 | streamed-list-objects | 15 | 15 | [1001] | 0.167 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 3000 | list-objects | 15 | 15 | [1000] | 0.157 | 30000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 3000 | streamed-list-objects | 15 | 15 | [3000] | 0.203 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 10000 | list-objects | 15 | 15 | [1000] | 0.179 | 135000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 10000 | streamed-list-objects | 15 | 15 | [10000] | 0.338 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 30000 | list-objects | 15 | 15 | [1000] | 0.214 | 435000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 30000 | streamed-list-objects | 15 | 15 | [30000] | 0.713 | 0 | 0 | 0 | 0 | [()] |
| openfga | full-folder | 100000 | list-objects | 15 | 15 | [1000] | 0.335 | 1485000 | 0 | 0 | 0 | [('objects',)] |
| openfga | full-folder | 100000 | streamed-list-objects | 15 | 15 | [100000] | 2.026 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 10 | list-objects | 15 | 15 | [10] | 0.001 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 10 | streamed-list-objects | 15 | 15 | [10] | 0.001 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 100 | list-objects | 15 | 15 | [100] | 0.001 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 100 | streamed-list-objects | 15 | 15 | [100] | 0.003 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 999 | list-objects | 15 | 15 | [999] | 0.004 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 999 | streamed-list-objects | 15 | 15 | [999] | 0.016 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 1000 | list-objects | 15 | 15 | [1000] | 0.004 | 0 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 1000 | streamed-list-objects | 15 | 15 | [1000] | 0.017 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 1001 | list-objects | 15 | 15 | [1000] | 0.004 | 15 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 1001 | streamed-list-objects | 15 | 15 | [1001] | 0.016 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 3000 | list-objects | 15 | 15 | [1000] | 0.005 | 30000 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 3000 | streamed-list-objects | 15 | 15 | [3000] | 0.047 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 10000 | list-objects | 15 | 15 | [1000] | 0.012 | 135000 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 10000 | streamed-list-objects | 15 | 15 | [10000] | 0.159 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 30000 | list-objects | 15 | 15 | [1000] | 0.033 | 435000 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 30000 | streamed-list-objects | 15 | 15 | [30000] | 0.515 | 0 | 0 | 0 | 0 | [()] |
| openfga | simple-direct | 100000 | list-objects | 15 | 15 | [1000] | 0.116 | 1485000 | 0 | 0 | 0 | [('objects',)] |
| openfga | simple-direct | 100000 | streamed-list-objects | 15 | 15 | [100000] | 1.736 | 0 | 0 | 0 | 0 | [()] |

#### wardowl's filter_for

| engine | route | structure | N | timeout s | calls | outcomes | median s |
|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 2.0 | 5 | {'exact': 5} | 0.161 |
| openfga | adapter | full-direct | 10 | 10.0 | 5 | {'exact': 5} | 0.157 |
| openfga | adapter | full-direct | 100 | 2.0 | 5 | {'exact': 5} | 0.149 |
| openfga | adapter | full-direct | 100 | 10.0 | 5 | {'exact': 5} | 0.160 |
| openfga | adapter | full-direct | 999 | 2.0 | 5 | {'exact': 5} | 0.160 |
| openfga | adapter | full-direct | 999 | 10.0 | 5 | {'exact': 5} | 0.151 |
| openfga | adapter | full-direct | 1000 | 2.0 | 5 | {'none': 5} | 0.160 |
| openfga | adapter | full-direct | 1000 | 10.0 | 5 | {'none': 5} | 0.156 |
| openfga | adapter | full-direct | 1001 | 2.0 | 5 | {'none': 5} | 0.161 |
| openfga | adapter | full-direct | 1001 | 10.0 | 5 | {'none': 5} | 0.153 |
| openfga | adapter | full-direct | 3000 | 2.0 | 5 | {'none': 5} | 0.159 |
| openfga | adapter | full-direct | 3000 | 10.0 | 5 | {'none': 5} | 0.154 |
| openfga | adapter | full-direct | 10000 | 2.0 | 5 | {'none': 5} | 0.167 |
| openfga | adapter | full-direct | 10000 | 10.0 | 5 | {'none': 5} | 0.168 |
| openfga | adapter | full-direct | 30000 | 2.0 | 5 | {'none': 5} | 0.199 |
| openfga | adapter | full-direct | 30000 | 10.0 | 5 | {'none': 5} | 0.197 |
| openfga | adapter | full-direct | 100000 | 2.0 | 5 | {'none': 5} | 0.266 |
| openfga | adapter | full-direct | 100000 | 10.0 | 5 | {'none': 5} | 0.274 |
| openfga | adapter | full-folder | 10 | 2.0 | 5 | {'exact': 5} | 0.154 |
| openfga | adapter | full-folder | 10 | 10.0 | 5 | {'exact': 5} | 0.152 |
| openfga | adapter | full-folder | 100 | 2.0 | 5 | {'exact': 5} | 0.158 |
| openfga | adapter | full-folder | 100 | 10.0 | 5 | {'exact': 5} | 0.157 |
| openfga | adapter | full-folder | 999 | 2.0 | 5 | {'exact': 5} | 0.160 |
| openfga | adapter | full-folder | 999 | 10.0 | 5 | {'exact': 5} | 0.160 |
| openfga | adapter | full-folder | 1000 | 2.0 | 5 | {'none': 5} | 0.157 |
| openfga | adapter | full-folder | 1000 | 10.0 | 5 | {'none': 5} | 0.164 |
| openfga | adapter | full-folder | 1001 | 2.0 | 5 | {'none': 5} | 0.154 |
| openfga | adapter | full-folder | 1001 | 10.0 | 5 | {'none': 5} | 0.159 |
| openfga | adapter | full-folder | 3000 | 2.0 | 5 | {'none': 5} | 0.160 |
| openfga | adapter | full-folder | 3000 | 10.0 | 5 | {'none': 5} | 0.163 |
| openfga | adapter | full-folder | 10000 | 2.0 | 5 | {'none': 5} | 0.175 |
| openfga | adapter | full-folder | 10000 | 10.0 | 5 | {'none': 5} | 0.172 |
| openfga | adapter | full-folder | 30000 | 2.0 | 5 | {'none': 5} | 0.216 |
| openfga | adapter | full-folder | 30000 | 10.0 | 5 | {'none': 5} | 0.215 |
| openfga | adapter | full-folder | 100000 | 2.0 | 5 | {'none': 5} | 0.322 |
| openfga | adapter | full-folder | 100000 | 10.0 | 5 | {'none': 5} | 0.332 |
| openfga | adapter | simple-direct | 10 | 2.0 | 5 | {'exact': 5} | 0.001 |
| openfga | adapter | simple-direct | 10 | 10.0 | 5 | {'exact': 5} | 0.002 |
| openfga | adapter | simple-direct | 100 | 2.0 | 5 | {'exact': 5} | 0.001 |
| openfga | adapter | simple-direct | 100 | 10.0 | 5 | {'exact': 5} | 0.002 |
| openfga | adapter | simple-direct | 999 | 2.0 | 5 | {'exact': 5} | 0.004 |
| openfga | adapter | simple-direct | 999 | 10.0 | 5 | {'exact': 5} | 0.004 |
| openfga | adapter | simple-direct | 1000 | 2.0 | 5 | {'none': 5} | 0.004 |
| openfga | adapter | simple-direct | 1000 | 10.0 | 5 | {'none': 5} | 0.003 |
| openfga | adapter | simple-direct | 1001 | 2.0 | 5 | {'none': 5} | 0.003 |
| openfga | adapter | simple-direct | 1001 | 10.0 | 5 | {'none': 5} | 0.003 |
| openfga | adapter | simple-direct | 3000 | 2.0 | 5 | {'none': 5} | 0.005 |
| openfga | adapter | simple-direct | 3000 | 10.0 | 5 | {'none': 5} | 0.004 |
| openfga | adapter | simple-direct | 10000 | 2.0 | 5 | {'none': 5} | 0.011 |
| openfga | adapter | simple-direct | 10000 | 10.0 | 5 | {'none': 5} | 0.010 |
| openfga | adapter | simple-direct | 30000 | 2.0 | 5 | {'none': 5} | 0.035 |
| openfga | adapter | simple-direct | 30000 | 10.0 | 5 | {'none': 5} | 0.032 |
| openfga | adapter | simple-direct | 100000 | 2.0 | 5 | {'none': 5} | 0.110 |
| openfga | adapter | simple-direct | 100000 | 10.0 | 5 | {'none': 5} | 0.114 |

#### Permission-recall@10 through wardowl

| engine | route | structure | N | queries | failed | recall@10 [95% CI] | false complete | leaks | strategies | median s |
|---|---|---|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.210 |
| openfga | adapter | full-direct | 100 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.209 |
| openfga | adapter | full-direct | 999 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.211 |
| openfga | adapter | full-direct | 1000 | 150 | 0 | 0.880 [0.853, 0.905] | 0 | 0 | {'postfilter': 150} | 0.798 |
| openfga | adapter | full-direct | 1001 | 150 | 0 | 0.889 [0.861, 0.914] | 0 | 0 | {'postfilter': 150} | 0.781 |
| openfga | adapter | full-direct | 3000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.548 |
| openfga | adapter | full-direct | 10000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.311 |
| openfga | adapter | full-direct | 30000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.264 |
| openfga | adapter | full-direct | 100000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.334 |
| openfga | adapter | full-folder | 10 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.207 |
| openfga | adapter | full-folder | 100 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.208 |
| openfga | adapter | full-folder | 999 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.212 |
| openfga | adapter | full-folder | 1000 | 150 | 0 | 0.880 [0.853, 0.906] | 0 | 0 | {'postfilter': 150} | 0.796 |
| openfga | adapter | full-folder | 1001 | 150 | 0 | 0.891 [0.865, 0.916] | 0 | 0 | {'postfilter': 150} | 0.778 |
| openfga | adapter | full-folder | 3000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.558 |
| openfga | adapter | full-folder | 10000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.325 |
| openfga | adapter | full-folder | 30000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.282 |
| openfga | adapter | full-folder | 100000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.402 |
| openfga | adapter | simple-direct | 10 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.047 |
| openfga | adapter | simple-direct | 100 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.047 |
| openfga | adapter | simple-direct | 999 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 0.051 |
| openfga | adapter | simple-direct | 1000 | 150 | 0 | 0.878 [0.847, 0.907] | 0 | 0 | {'postfilter': 150} | 0.109 |
| openfga | adapter | simple-direct | 1001 | 150 | 0 | 0.875 [0.846, 0.903] | 0 | 0 | {'postfilter': 150} | 0.103 |
| openfga | adapter | simple-direct | 3000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.072 |
| openfga | adapter | simple-direct | 10000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.085 |
| openfga | adapter | simple-direct | 30000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.074 |
| openfga | adapter | simple-direct | 100000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'postfilter': 150} | 0.145 |

## X4d: latency and caching

| engine | route | structure | N | records | filter_for uncached ms (median) | check per hit ms | filter speedup cached [95% CI] | check speedup cached [95% CI] |
|---|---|---|---|---|---|---|---|---|
| openfga | adapter | full-direct | 10 | 5 | 147.127 | 0.534 | 22930.3 [21494.0, 28351.1] | 80.0 [76.2, 97.4] |
| openfga | adapter | full-direct | 100 | 5 | 155.026 | 0.548 | 22979.6 [21132.1, 24954.6] | 80.9 [74.3, 87.2] |
| openfga | adapter | full-direct | 999 | 5 | 154.356 | 0.585 | 23860.8 [20836.9, 25515.6] | 84.8 [82.5, 88.2] |
| openfga | adapter | full-direct | 1000 | 5 | 157.781 | 0.564 | 24415.4 [23118.1, 25203.2] | 85.0 [75.0, 90.3] |
| openfga | adapter | full-direct | 1001 | 5 | 158.546 | 0.556 | 21919.9 [21291.4, 24760.5] | 83.6 [77.9, 88.8] |
| openfga | adapter | full-direct | 3000 | 5 | 154.795 | 0.518 | 21377.9 [20470.5, 25420.8] | 79.0 [73.9, 86.5] |
| openfga | adapter | full-direct | 10000 | 5 | 169.923 | 0.505 | 24860.7 [22093.8, 27230.0] | 74.9 [74.3, 88.5] |
| openfga | adapter | full-direct | 30000 | 5 | 193.312 | 0.522 | 27151.2 [19025.8, 30953.0] | 78.2 [75.3, 83.1] |
| openfga | adapter | full-direct | 100000 | 5 | 274.461 | 0.564 | 40378.3 [39547.7, 45868.7] | 73.6 [55.9, 85.4] |
| openfga | adapter | full-folder | 10 | 5 | 159.318 | 0.692 | 22505.6 [20003.7, 24495.4] | 104.3 [93.4, 106.9] |
| openfga | adapter | full-folder | 100 | 5 | 151.538 | 0.633 | 22819.9 [15813.8, 23297.4] | 93.5 [89.2, 96.1] |
| openfga | adapter | full-folder | 999 | 5 | 156.715 | 0.603 | 23723.1 [22578.0, 24507.3] | 89.8 [88.0, 100.3] |
| openfga | adapter | full-folder | 1000 | 5 | 157.532 | 0.616 | 23512.5 [21779.6, 24372.7] | 91.0 [87.9, 99.6] |
| openfga | adapter | full-folder | 1001 | 5 | 152.934 | 0.628 | 21863.4 [16934.4, 24912.2] | 90.4 [82.1, 95.1] |
| openfga | adapter | full-folder | 3000 | 5 | 160.196 | 0.587 | 24218.9 [22770.7, 26101.3] | 86.9 [63.9, 87.7] |
| openfga | adapter | full-folder | 10000 | 5 | 176.639 | 0.602 | 25824.4 [22738.0, 29358.1] | 88.6 [83.1, 97.9] |
| openfga | adapter | full-folder | 30000 | 5 | 215.134 | 0.609 | 30985.9 [29805.5, 33816.1] | 89.4 [80.8, 100.7] |
| openfga | adapter | full-folder | 100000 | 5 | 323.799 | 0.675 | 49325.0 [47342.5, 55291.2] | 87.5 [84.7, 115.6] |
| openfga | adapter | simple-direct | 10 | 5 | 0.874 | 0.140 | 130.4 [82.4, 136.2] | 21.1 [20.4, 22.5] |
| openfga | adapter | simple-direct | 100 | 5 | 1.144 | 0.140 | 164.4 [155.1, 173.2] | 20.8 [19.9, 22.0] |
| openfga | adapter | simple-direct | 999 | 5 | 3.838 | 0.137 | 548.6 [482.0, 575.7] | 20.7 [19.9, 23.9] |
| openfga | adapter | simple-direct | 1000 | 5 | 3.198 | 0.139 | 486.6 [306.7, 551.7] | 20.9 [20.6, 22.5] |
| openfga | adapter | simple-direct | 1001 | 5 | 3.093 | 0.138 | 454.6 [430.2, 512.6] | 20.4 [19.8, 24.3] |
| openfga | adapter | simple-direct | 3000 | 5 | 4.995 | 0.134 | 749.6 [648.9, 773.8] | 20.2 [19.2, 23.9] |
| openfga | adapter | simple-direct | 10000 | 5 | 12.080 | 0.148 | 1838.7 [1503.2, 2212.4] | 22.8 [17.5, 24.2] |
| openfga | adapter | simple-direct | 30000 | 5 | 30.697 | 0.136 | 4662.0 [2858.1, 5166.2] | 20.8 [19.9, 22.1] |
| openfga | adapter | simple-direct | 100000 | 5 | 110.050 | 0.232 | 16161.3 [13204.6, 19912.8] | 30.5 [28.5, 34.7] |

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
