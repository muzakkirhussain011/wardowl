# X4: engine filters against engine checks

Profile: ['full']. Files: 5; records: 23849.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | CONFIRMED | control-oracle 600 subjects, none disagreeing; control-planted 600 subjects, counts exact |
| G2 encoding cerbos | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 cerbos | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| X4-H2 cerbos-drift | CONFIRMED | 569 false admits (569 on documents with a scalar ACL field), 0 false denials |
| X4-H3 cerbos-excl | CONFIRMED | 0 false admits; filter for 0 of 600 subjects (0.000) |
| X4-H3 availability cerbos-excl (predicted 0) | CONFIRMED | 0 false admits; filter for 0 of 600 subjects (0.000) |
| G2 encoding opa-acl-doc | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 opa-acl-doc | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| X4-H2 opa-acl-doc-drift | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| G2 encoding opa-rel-doc | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 opa-rel-doc | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| G2 encoding opa-rel-pe | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 opa-rel-pe | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| X4-H3 opa-rel-pe-excl | CONFIRMED | 0 false admits; filter for 0 of 600 subjects (0.000) |
| X4-H3 availability opa-rel-pe-excl (filter iff no ban in scope) | FALSIFIED | 527 of 600 subjects as predicted |
| G2 encoding openfga | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 openfga | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| G2 encoding openfga-ctx | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 openfga-ctx | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| G2 encoding spicedb | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 spicedb | CONFIRMED | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| X4-H4c opa quiet | CONFIRMED | 200 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b opa writer | CONFIRMED | 200 trials, trials disagreeing 0.130 [0.085, 0.180], 97 pairs, 97 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4c openfga quiet-hc | CONFIRMED | 200 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-hc | CONFIRMED | 200 trials, trials disagreeing 1.000 [1.000, 1.000], 9433 pairs, 9433 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-ml | CONFIRMED | 200 trials, trials disagreeing 1.000 [1.000, 1.000], 9972 pairs, 9972 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4c spicedb quiet-ml | CONFIRMED | 200 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b spicedb writer-fc | CONFIRMED | 200 trials, trials disagreeing 0.815 [0.760, 0.865], 2190 pairs, 2190 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b spicedb writer-ml | CONFIRMED | 200 trials, trials disagreeing 0.040 [0.015, 0.070], 228 pairs, 226 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4a spicedb writer-pinned | CONFIRMED | 200 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4d spicedb ml minus pinned | CONFIRMED | 200 pairs, difference 0.040 [0.015, 0.070] |
| X4-H5a openfga | CONFIRMED | 135 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | CONFIRMED | 135 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | CONFIRMED | 540 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | CONFIRMED | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c OPA routes exact (consistency check) | EXPLORATORY | 180 calls, 45 not exact: {'error': 45} |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [('openfga', 'full-direct', 100000), ('openfga', 'full-folder', 100000), ('spicedb', 'full-direct', 100000), ('spicedb', 'full-folder', 100000), ('spicedb', 'simple-direct', 100000)] |
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
| X4-H7 caching cerbos | INCONCLUSIVE | 1 cells; lowest median ratio 8.6 |
| X4-H7 caching opa | CONFIRMED | 20 cells; lowest median ratio 114.3 |
| X4-H7 caching openfga | CONFIRMED | 29 cells; lowest median ratio 20.2 |
| X4-H7 caching spicedb | CONFIRMED | 28 cells; lowest median ratio 17.5 |

## X4a: one revision

| profile | subjects | with filter | errors | pairs | false admits | false denials | reproduce | subjects disagreeing [95% CI] | zero bound | pair rate [95% CI] | check vs oracle | check vs oracle rate | seeds | false admits on scalar fields |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| cerbos-drift | 600 | 600 | 0 | 900000 | 569 | 0 | 569 | 0.525 [0.483, 0.563] | 0.0050 | 0.000632 [0.000570, 0.000696] | 569 | 0.000632 | 5 | 569 |
| cerbos-excl | 600 | 0 | 0 | 0 | 0 | 0 | 0 | n/a [n/a, n/a] | 1.0000 | n/a [n/a, n/a] | 0 | 0.000000 | 5 | 0 |
| control-oracle | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| control-planted | 600 | 600 | 0 | 900000 | 16774 | 1233 | 18007 | 1.000 [1.000, 1.000] | 0.0050 | 0.020008 [0.020002, 0.020014] | 0 | 0.000000 | 5 | 0 |
| opa-acl-doc | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| opa-acl-doc-drift | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| opa-rel-doc | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| opa-rel-pe | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| opa-rel-pe-excl | 600 | 0 | 0 | 0 | 0 | 0 | 0 | n/a [n/a, n/a] | 1.0000 | n/a [n/a, n/a] | 0 | 0.000000 | 5 | 0 |
| openfga | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| openfga-ctx | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| spicedb | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |

## X4b: unpinned, under a writer

| engine | condition | trials | trials disagreeing [95% CI] | pairs | skew-explained | explained share | reproduce | oracle mismatches | median writes in window | seeds |
|---|---|---|---|---|---|---|---|---|---|---|
| opa | quiet | 200 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 5 |
| opa | writer | 200 | 0.130 [0.085, 0.180] | 97 | 97 | 1.000 | 0 | 0 | 1.000 | 5 |
| openfga | quiet-hc | 200 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 5 |
| openfga | writer-hc | 200 | 1.000 [1.000, 1.000] | 9433 | 9433 | 1.000 | 0 | 0 | 59.000 | 5 |
| openfga | writer-ml | 200 | 1.000 [1.000, 1.000] | 9972 | 9972 | 1.000 | 0 | 0 | 208.000 | 5 |
| spicedb | quiet-ml | 200 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 5 |
| spicedb | writer-fc | 200 | 0.815 [0.760, 0.865] | 2190 | 2190 | 1.000 | 0 | 0 | 6.000 | 5 |
| spicedb | writer-ml | 200 | 0.040 [0.015, 0.070] | 228 | 226 | 0.991 | 0 | 0 | 114.000 | 5 |
| spicedb | writer-pinned | 200 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 5 |

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
| opa | opa-rel-doc | opa-share | 10 | 2.0 | 5 | {'exact': 5} | 0.666 |
| opa | opa-rel-doc | opa-share | 10 | 10.0 | 5 | {'exact': 5} | 0.676 |
| opa | opa-rel-doc | opa-share | 100 | 2.0 | 5 | {'exact': 5} | 0.699 |
| opa | opa-rel-doc | opa-share | 100 | 10.0 | 5 | {'exact': 5} | 0.694 |
| opa | opa-rel-doc | opa-share | 999 | 2.0 | 5 | {'exact': 5} | 0.707 |
| opa | opa-rel-doc | opa-share | 999 | 10.0 | 5 | {'exact': 5} | 0.682 |
| opa | opa-rel-doc | opa-share | 1000 | 2.0 | 5 | {'exact': 5} | 0.700 |
| opa | opa-rel-doc | opa-share | 1000 | 10.0 | 5 | {'exact': 5} | 0.689 |
| opa | opa-rel-doc | opa-share | 1001 | 2.0 | 5 | {'exact': 5} | 0.687 |
| opa | opa-rel-doc | opa-share | 1001 | 10.0 | 5 | {'exact': 5} | 0.671 |
| opa | opa-rel-doc | opa-share | 3000 | 2.0 | 5 | {'exact': 5} | 0.701 |
| opa | opa-rel-doc | opa-share | 3000 | 10.0 | 5 | {'exact': 5} | 0.687 |
| opa | opa-rel-doc | opa-share | 10000 | 2.0 | 5 | {'exact': 5} | 0.689 |
| opa | opa-rel-doc | opa-share | 10000 | 10.0 | 5 | {'exact': 5} | 0.675 |
| opa | opa-rel-doc | opa-share | 30000 | 2.0 | 5 | {'exact': 5} | 0.689 |
| opa | opa-rel-doc | opa-share | 30000 | 10.0 | 5 | {'exact': 5} | 0.644 |
| opa | opa-rel-doc | opa-share | 100000 | 2.0 | 5 | {'exact': 5} | 0.580 |
| opa | opa-rel-doc | opa-share | 100000 | 10.0 | 5 | {'exact': 5} | 0.568 |
| opa | opa-rel-pe | opa-share | 10 | 2.0 | 5 | {'error': 5} | 2.002 |
| opa | opa-rel-pe | opa-share | 10 | 10.0 | 5 | {'exact': 5} | 4.250 |
| opa | opa-rel-pe | opa-share | 100 | 2.0 | 5 | {'error': 5} | 2.003 |
| opa | opa-rel-pe | opa-share | 100 | 10.0 | 5 | {'exact': 5} | 4.284 |
| opa | opa-rel-pe | opa-share | 999 | 2.0 | 5 | {'error': 5} | 2.002 |
| opa | opa-rel-pe | opa-share | 999 | 10.0 | 5 | {'exact': 5} | 4.251 |
| opa | opa-rel-pe | opa-share | 1000 | 2.0 | 5 | {'error': 5} | 2.002 |
| opa | opa-rel-pe | opa-share | 1000 | 10.0 | 5 | {'exact': 5} | 4.355 |
| opa | opa-rel-pe | opa-share | 1001 | 2.0 | 5 | {'error': 5} | 2.002 |
| opa | opa-rel-pe | opa-share | 1001 | 10.0 | 5 | {'exact': 5} | 4.282 |
| opa | opa-rel-pe | opa-share | 3000 | 2.0 | 5 | {'error': 5} | 2.003 |
| opa | opa-rel-pe | opa-share | 3000 | 10.0 | 5 | {'exact': 5} | 4.425 |
| opa | opa-rel-pe | opa-share | 10000 | 2.0 | 5 | {'error': 5} | 2.003 |
| opa | opa-rel-pe | opa-share | 10000 | 10.0 | 5 | {'exact': 5} | 4.498 |
| opa | opa-rel-pe | opa-share | 30000 | 2.0 | 5 | {'error': 5} | 2.003 |
| opa | opa-rel-pe | opa-share | 30000 | 10.0 | 5 | {'exact': 5} | 4.676 |
| opa | opa-rel-pe | opa-share | 100000 | 2.0 | 5 | {'error': 5} | 2.002 |
| opa | opa-rel-pe | opa-share | 100000 | 10.0 | 5 | {'exact': 5} | 5.669 |
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
| opa | opa-rel-doc | opa-share | 10 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.643 |
| opa | opa-rel-doc | opa-share | 100 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.663 |
| opa | opa-rel-doc | opa-share | 999 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.662 |
| opa | opa-rel-doc | opa-share | 1000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.678 |
| opa | opa-rel-doc | opa-share | 1001 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.679 |
| opa | opa-rel-doc | opa-share | 3000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.672 |
| opa | opa-rel-doc | opa-share | 10000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.681 |
| opa | opa-rel-doc | opa-share | 30000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.620 |
| opa | opa-rel-doc | opa-share | 100000 | 150 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 150} | 1.355 |
| opa | opa-rel-pe | opa-share | 10 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 100 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 999 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 1000 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 1001 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 3000 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 10000 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 30000 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
| opa | opa-rel-pe | opa-share | 100000 | 150 | 150 | n/a [n/a, n/a] | 0 | 0 | {} | 2.003 |
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
| cerbos | cerbos | x4a-world | None | 50 | 1.225 | 0.131 | 94.4 [88.9, 99.5] | 8.6 [8.5, 8.7] |
| cerbos | cerbos-drift | x4a-world | None | 50 | 1.191 | 0.131 | 93.3 [86.1, 102.1] | 8.7 [8.4, 8.9] |
| cerbos | cerbos-excl | x4a-world | None | 50 | 1.306 | 0.138 | 102.6 [96.7, 106.8] | 7.6 [7.5, 7.7] |
| controls | control-oracle | x4a-world | None | 50 | 0.478 | 2.6e-04 | 75.2 [74.5, 75.8] | 4.0e-02 [3.8e-02, 4.5e-02] |
| controls | control-planted | x4a-world | None | 50 | 2.1e-04 | 2.7e-04 | 3.3e-02 [3.1e-02, 3.5e-02] | 4.1e-02 [3.9e-02, 4.3e-02] |
| opa | opa-acl-doc | x4a-world | None | 50 | 1.696 | 0.169 | 166.0 [158.6, 172.9] | 10.7 [10.5, 10.9] |
| opa | opa-acl-doc-drift | x4a-world | None | 50 | 1.671 | 0.164 | 164.1 [157.2, 168.3] | 10.6 [10.3, 10.9] |
| opa | opa-rel-doc | opa-share | 10 | 5 | 672.662 | 66.591 | 71288.7 [50126.7, 74108.4] | 6418.4 [4003.3, 6483.3] |
| opa | opa-rel-doc | opa-share | 100 | 5 | 679.717 | 67.994 | 75345.9 [50182.1, 81433.7] | 6311.3 [4090.6, 6640.9] |
| opa | opa-rel-doc | opa-share | 999 | 5 | 680.955 | 67.186 | 76760.1 [75980.3, 77354.8] | 6492.3 [6452.7, 6681.9] |
| opa | opa-rel-doc | opa-share | 1000 | 5 | 691.312 | 68.551 | 75314.6 [52818.1, 77661.4] | 6652.6 [6526.9, 6728.9] |
| opa | opa-rel-doc | opa-share | 1001 | 5 | 679.487 | 67.952 | 71762.9 [46507.5, 74421.0] | 6550.6 [6429.7, 6841.4] |
| opa | opa-rel-doc | opa-share | 3000 | 5 | 674.714 | 67.654 | 74115.8 [49132.9, 78078.3] | 6393.9 [4036.5, 6558.9] |
| opa | opa-rel-doc | opa-share | 10000 | 5 | 668.357 | 66.432 | 73096.4 [71360.1, 74448.4] | 6371.0 [6043.8, 6475.3] |
| opa | opa-rel-doc | opa-share | 30000 | 5 | 639.022 | 62.952 | 66826.7 [64223.7, 73657.6] | 6009.7 [5882.7, 6177.8] |
| opa | opa-rel-doc | opa-share | 100000 | 5 | 563.018 | 94.329 | 59870.1 [55262.1, 69782.4] | 8160.5 [7472.6, 8473.6] |
| opa | opa-rel-doc | x4a-world | None | 50 | 13.553 | 1.271 | 1330.2 [1243.5, 1388.2] | 114.3 [112.3, 117.9] |
| opa | opa-rel-pe | opa-share | 10 | 5 | 4230.694 | 66.893 | 450356.5 [313617.1, 464381.1] | 6193.2 [4001.7, 6640.0] |
| opa | opa-rel-pe | opa-share | 100 | 5 | 4238.133 | 67.574 | 459384.1 [195739.3, 494585.3] | 6536.9 [6429.3, 6875.4] |
| opa | opa-rel-pe | opa-share | 999 | 5 | 4249.384 | 68.315 | 469148.3 [311984.4, 482465.5] | 6661.3 [6424.5, 6964.7] |
| opa | opa-rel-pe | opa-share | 1000 | 5 | 4243.956 | 68.745 | 451230.8 [305615.6, 463405.3] | 6542.1 [6410.0, 6793.6] |
| opa | opa-rel-pe | opa-share | 1001 | 5 | 4278.579 | 67.975 | 466406.4 [311152.3, 470347.6] | 6592.6 [3947.0, 6791.9] |
| opa | opa-rel-pe | opa-share | 3000 | 5 | 4316.178 | 68.755 | 475176.9 [302550.7, 500030.4] | 6560.4 [4060.9, 6951.3] |
| opa | opa-rel-pe | opa-share | 10000 | 5 | 4387.536 | 66.736 | 481503.2 [465620.5, 484668.0] | 6295.2 [4144.7, 6382.1] |
| opa | opa-rel-pe | opa-share | 30000 | 5 | 4678.378 | 63.858 | 506372.8 [487201.1, 530899.5] | 6041.5 [5233.8, 6151.2] |
| opa | opa-rel-pe | opa-share | 100000 | 5 | 5507.207 | 92.311 | 604622.8 [545378.8, 626044.6] | 7963.2 [7621.9, 8291.2] |
| opa | opa-rel-pe | x4a-world | None | 50 | 115.537 | 1.436 | 10978.2 [10558.6, 11471.8] | 124.5 [117.3, 132.4] |
| opa | opa-rel-pe-excl | x4a-world | None | 50 | 121.694 | 1.376 | 11302.0 [11002.6, 11897.9] | 122.2 [118.6, 129.8] |
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
| openfga | openfga | x4a-world | None | 50 | 4.147 | 0.727 | 615.8 [476.2, 671.7] | 106.8 [103.5, 115.3] |
| openfga | openfga-ctx | x4a-world | None | 50 | 3.887 | 0.711 | 481.8 [410.0, 530.8] | 102.9 [97.9, 116.4] |
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
| spicedb | spicedb | x4a-world | None | 50 | 6.445 | 0.166 | 676.3 [528.5, 857.6] | 17.5 [17.5, 17.8] |

## Harness

Runs: 5 job records; profile ['full']; commit ['e66dffc'].

| job | where | count | error |
|---|---|---|---|
| x4-policy | ['retriever.py:285 retrieve', 'retriever.py:510 _run', 'x4_engines.py:234 filter_for', '_http.py:321 post_json'] | 1350 | wardowl.authz.AuthorizationError: OPA compile x4rel/allow timed out after 2.0 s |
| x4-policy | ['x4_engines.py:1235 _filter', 'x4_engines.py:234 filter_for', '_http.py:321 post_json'] | 45 | wardowl.authz.AuthorizationError: OPA compile x4rel/allow timed out after 2.0 s |
