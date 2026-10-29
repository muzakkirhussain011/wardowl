# X4: engine filters against engine checks

Profile: ['smoke']. Files: 5; records: 625. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | CONFIRMED | control-oracle 12 subjects, none disagreeing; control-planted 12 subjects, counts exact |
| G2 encoding cerbos | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 cerbos | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| X4-H2 cerbos-drift | INCONCLUSIVE | 2 false admits (2 on documents with a scalar ACL field), 0 false denials |
| X4-H3 cerbos-excl | INCONCLUSIVE | 0 false admits; filter for 0 of 12 subjects (0.000) |
| X4-H3 availability cerbos-excl (predicted 0) | CONFIRMED | 0 false admits; filter for 0 of 12 subjects (0.000) |
| G2 encoding opa-acl-doc | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 opa-acl-doc | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| X4-H2 opa-acl-doc-drift | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| G2 encoding opa-rel-doc | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 opa-rel-doc | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| G2 encoding opa-rel-pe | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 opa-rel-pe | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| X4-H3 opa-rel-pe-excl | INCONCLUSIVE | 0 false admits; filter for 0 of 12 subjects (0.000) |
| X4-H3 availability opa-rel-pe-excl (filter iff no ban in scope) | FALSIFIED | 10 of 12 subjects as predicted |
| G2 encoding openfga | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 openfga | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| G2 encoding openfga-ctx | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 openfga-ctx | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| G2 encoding spicedb | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 spicedb | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| X4-H4c opa quiet | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b opa writer | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4c openfga quiet-hc | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-hc | INCONCLUSIVE | 6 trials, trials disagreeing 0.667 [0.333, 1.000], 30 pairs, 30 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-ml | INCONCLUSIVE | 6 trials, trials disagreeing 0.667 [0.333, 1.000], 26 pairs, 26 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4c spicedb quiet-ml | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b spicedb writer-fc | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b spicedb writer-ml | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4a spicedb writer-pinned | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4d spicedb ml minus pinned | FALSIFIED | 6 pairs, difference 0.000 [0.000, 0.000] |
| X4-H5a openfga | INCONCLUSIVE | 5 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 5 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | INCONCLUSIVE | 60 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | INCONCLUSIVE | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c OPA routes exact (consistency check) | EXPLORATORY | 20 calls, 0 not exact: {} |
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
| X4-H7 caching cerbos | INCONCLUSIVE | 1 cells; lowest median ratio 9.4 |
| X4-H7 caching opa | CONFIRMED | 12 cells; lowest median ratio 13.1 |
| X4-H7 caching openfga | CONFIRMED | 17 cells; lowest median ratio 20.2 |
| X4-H7 caching spicedb | CONFIRMED | 16 cells; lowest median ratio 21.4 |

## X4a: one revision

| profile | subjects | with filter | errors | pairs | false admits | false denials | reproduce | subjects disagreeing [95% CI] | zero bound | pair rate [95% CI] | check vs oracle | check vs oracle rate | seeds | false admits on scalar fields |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cerbos | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| cerbos-drift | 12 | 12 | 0 | 1440 | 2 | 0 | 2 | 0.083 [0.000, 0.250] | 0.2209 | 0.001389 [0.000000, 0.004167] | 2 | 0.001389 | 1 | 2 |
| cerbos-excl | 12 | 0 | 0 | 0 | 0 | 0 | 0 | n/a [n/a, n/a] | 1.0000 | n/a [n/a, n/a] | 0 | 0.000000 | 1 | 0 |
| control-oracle | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| control-planted | 12 | 12 | 0 | 1440 | 22 | 12 | 34 | 1.000 [1.000, 1.000] | 0.2209 | 0.023611 [0.021528, 0.025000] | 0 | 0.000000 | 1 | 0 |
| opa-acl-doc | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| opa-acl-doc-drift | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| opa-rel-doc | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| opa-rel-pe | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| opa-rel-pe-excl | 12 | 0 | 0 | 0 | 0 | 0 | 0 | n/a [n/a, n/a] | 1.0000 | n/a [n/a, n/a] | 0 | 0.000000 | 1 | 0 |
| openfga | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| openfga-ctx | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| spicedb | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |

## X4b: unpinned, under a writer

| engine | condition | trials | trials disagreeing [95% CI] | pairs | skew-explained | explained share | reproduce | oracle mismatches | median writes in window | seeds |
|---|---|---|---|---|---|---|---|---|---|---|
| opa | quiet | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |
| opa | writer | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | 0.000 | 1 |
| openfga | quiet-hc | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |
| openfga | writer-hc | 6 | 0.667 [0.333, 1.000] | 30 | 30 | 1.000 | 0 | 0 | 5.000 | 1 |
| openfga | writer-ml | 6 | 0.667 [0.333, 1.000] | 26 | 26 | 1.000 | 0 | 0 | 5.000 | 1 |
| spicedb | quiet-ml | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |
| spicedb | writer-fc | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | 0.500 | 1 |
| spicedb | writer-ml | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | 0.500 | 1 |
| spicedb | writer-pinned | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |

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
| opa | opa-rel-doc | opa-share | 10 | 2.0 | 1 | {'exact': 1} | 0.021 |
| opa | opa-rel-doc | opa-share | 10 | 10.0 | 1 | {'exact': 1} | 0.019 |
| opa | opa-rel-doc | opa-share | 999 | 2.0 | 1 | {'exact': 1} | 0.018 |
| opa | opa-rel-doc | opa-share | 999 | 10.0 | 1 | {'exact': 1} | 0.025 |
| opa | opa-rel-doc | opa-share | 1000 | 2.0 | 1 | {'exact': 1} | 0.018 |
| opa | opa-rel-doc | opa-share | 1000 | 10.0 | 1 | {'exact': 1} | 0.017 |
| opa | opa-rel-doc | opa-share | 1001 | 2.0 | 1 | {'exact': 1} | 0.017 |
| opa | opa-rel-doc | opa-share | 1001 | 10.0 | 1 | {'exact': 1} | 0.019 |
| opa | opa-rel-doc | opa-share | 3000 | 2.0 | 1 | {'exact': 1} | 0.016 |
| opa | opa-rel-doc | opa-share | 3000 | 10.0 | 1 | {'exact': 1} | 0.015 |
| opa | opa-rel-pe | opa-share | 10 | 2.0 | 1 | {'exact': 1} | 0.120 |
| opa | opa-rel-pe | opa-share | 10 | 10.0 | 1 | {'exact': 1} | 0.122 |
| opa | opa-rel-pe | opa-share | 999 | 2.0 | 1 | {'exact': 1} | 0.127 |
| opa | opa-rel-pe | opa-share | 999 | 10.0 | 1 | {'exact': 1} | 0.128 |
| opa | opa-rel-pe | opa-share | 1000 | 2.0 | 1 | {'exact': 1} | 0.174 |
| opa | opa-rel-pe | opa-share | 1000 | 10.0 | 1 | {'exact': 1} | 0.135 |
| opa | opa-rel-pe | opa-share | 1001 | 2.0 | 1 | {'exact': 1} | 0.131 |
| opa | opa-rel-pe | opa-share | 1001 | 10.0 | 1 | {'exact': 1} | 0.147 |
| opa | opa-rel-pe | opa-share | 3000 | 2.0 | 1 | {'exact': 1} | 0.157 |
| opa | opa-rel-pe | opa-share | 3000 | 10.0 | 1 | {'exact': 1} | 0.153 |
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
| opa | opa-rel-doc | opa-share | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.048 |
| opa | opa-rel-doc | opa-share | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.058 |
| opa | opa-rel-doc | opa-share | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.048 |
| opa | opa-rel-doc | opa-share | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.050 |
| opa | opa-rel-doc | opa-share | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.044 |
| opa | opa-rel-pe | opa-share | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.174 |
| opa | opa-rel-pe | opa-share | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.169 |
| opa | opa-rel-pe | opa-share | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.178 |
| opa | opa-rel-pe | opa-share | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.179 |
| opa | opa-rel-pe | opa-share | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.186 |
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
| cerbos | cerbos | x4a-world | None | 2 | 0.990 | 0.106 | 107.0 [96.4, 117.6] | 9.4 [9.1, 9.8] |
| cerbos | cerbos-drift | x4a-world | None | 2 | 1.101 | 0.107 | 123.3 [93.0, 153.6] | 9.6 [8.8, 10.4] |
| cerbos | cerbos-excl | x4a-world | None | 2 | 1.096 | 0.112 | 123.1 [103.4, 142.9] | 8.4 [8.1, 8.7] |
| controls | control-oracle | x4a-world | None | 2 | 0.032 | 2.9e-04 | 6.3 [6.2, 6.5] | 5.7e-02 [5.4e-02, 6.0e-02] |
| controls | control-planted | x4a-world | None | 2 | 1.4e-04 | 2.7e-04 | 2.9e-02 [2.9e-02, 3.0e-02] | 5.5e-02 [5.4e-02, 5.6e-02] |
| opa | opa-acl-doc | x4a-world | None | 2 | 0.409 | 0.051 | 57.4 [45.9, 68.9] | 4.4 [4.4, 4.5] |
| opa | opa-acl-doc-drift | x4a-world | None | 2 | 0.632 | 0.059 | 86.6 [64.5, 108.7] | 5.0 [4.6, 5.4] |
| opa | opa-rel-doc | opa-share | 10 | 1 | 16.602 | 1.851 | 2425.4 [2425.4, 2425.4] | 237.2 [237.2, 237.2] |
| opa | opa-rel-doc | opa-share | 999 | 1 | 17.211 | 1.713 | 2357.4 [2357.4, 2357.4] | 222.1 [222.1, 222.1] |
| opa | opa-rel-doc | opa-share | 1000 | 1 | 18.183 | 1.725 | 2548.2 [2548.2, 2548.2] | 228.4 [228.4, 228.4] |
| opa | opa-rel-doc | opa-share | 1001 | 1 | 18.378 | 2.031 | 2770.0 [2770.0, 2770.0] | 277.9 [277.9, 277.9] |
| opa | opa-rel-doc | opa-share | 3000 | 1 | 13.875 | 1.397 | 2032.8 [2032.8, 2032.8] | 184.0 [184.0, 184.0] |
| opa | opa-rel-doc | x4a-world | None | 2 | 1.086 | 0.109 | 122.3 [104.5, 140.1] | 13.1 [12.8, 13.5] |
| opa | opa-rel-pe | opa-share | 10 | 1 | 153.451 | 2.337 | 14648.5 [14648.5, 14648.5] | 195.7 [195.7, 195.7] |
| opa | opa-rel-pe | opa-share | 999 | 1 | 136.158 | 1.872 | 19993.8 [19993.8, 19993.8] | 244.0 [244.0, 244.0] |
| opa | opa-rel-pe | opa-share | 1000 | 1 | 129.082 | 1.783 | 18815.3 [18815.3, 18815.3] | 237.3 [237.3, 237.3] |
| opa | opa-rel-pe | opa-share | 1001 | 1 | 135.787 | 1.773 | 20101.7 [20101.7, 20101.7] | 239.2 [239.2, 239.2] |
| opa | opa-rel-pe | opa-share | 3000 | 1 | 152.120 | 1.428 | 24033.6 [24033.6, 24033.6] | 183.6 [183.6, 183.6] |
| opa | opa-rel-pe | x4a-world | None | 2 | 11.580 | 0.113 | 1466.5 [1443.6, 1489.4] | 13.9 [13.8, 13.9] |
| opa | opa-rel-pe-excl | x4a-world | None | 2 | 13.065 | 0.118 | 1876.2 [1634.3, 2118.0] | 14.5 [14.4, 14.6] |
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
| openfga | openfga | x4a-world | None | 2 | 3.176 | 0.765 | 508.5 [467.3, 549.7] | 151.0 [100.6, 201.5] |
| openfga | openfga-ctx | x4a-world | None | 2 | 2.495 | 0.658 | 459.2 [395.7, 522.8] | 128.6 [122.1, 135.1] |
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
| spicedb | spicedb | x4a-world | None | 2 | 3.752 | 0.196 | 412.8 [324.8, 500.8] | 27.5 [18.0, 37.0] |

## Harness

Runs: 5 job records; profile ['smoke']; commit ['62a587a'].
