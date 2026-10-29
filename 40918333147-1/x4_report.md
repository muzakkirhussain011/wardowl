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
| X4-H4b openfga writer-hc | INCONCLUSIVE | 6 trials, trials disagreeing 0.667 [0.333, 1.000], 16 pairs, 16 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-ml | INCONCLUSIVE | 6 trials, trials disagreeing 0.333 [0.000, 0.667], 10 pairs, 10 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4c spicedb quiet-ml | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b spicedb writer-fc | INCONCLUSIVE | 6 trials, trials disagreeing 0.167 [0.000, 0.500], 11 pairs, 11 skew-explained, 0 reproduce, 0 oracle mismatches |
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
| X4-H7 caching cerbos | INCONCLUSIVE | 1 cells; lowest median ratio 5.9 |
| X4-H7 caching opa | CONFIRMED | 12 cells; lowest median ratio 13.3 |
| X4-H7 caching openfga | CONFIRMED | 17 cells; lowest median ratio 20.2 |
| X4-H7 caching spicedb | CONFIRMED | 16 cells; lowest median ratio 18.0 |

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
| openfga | writer-hc | 6 | 0.667 [0.333, 1.000] | 16 | 16 | 1.000 | 0 | 0 | 4.500 | 1 |
| openfga | writer-ml | 6 | 0.333 [0.000, 0.667] | 10 | 10 | 1.000 | 0 | 0 | 5.000 | 1 |
| spicedb | quiet-ml | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |
| spicedb | writer-fc | 6 | 0.167 [0.000, 0.500] | 11 | 11 | 1.000 | 0 | 0 | 1.000 | 1 |
| spicedb | writer-ml | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | 0.000 | 1 |
| spicedb | writer-pinned | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |

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
| opa | opa-rel-doc | opa-share | 10 | 2.0 | 1 | {'exact': 1} | 0.035 |
| opa | opa-rel-doc | opa-share | 10 | 10.0 | 1 | {'exact': 1} | 0.047 |
| opa | opa-rel-doc | opa-share | 999 | 2.0 | 1 | {'exact': 1} | 0.033 |
| opa | opa-rel-doc | opa-share | 999 | 10.0 | 1 | {'exact': 1} | 0.037 |
| opa | opa-rel-doc | opa-share | 1000 | 2.0 | 1 | {'exact': 1} | 0.035 |
| opa | opa-rel-doc | opa-share | 1000 | 10.0 | 1 | {'exact': 1} | 0.037 |
| opa | opa-rel-doc | opa-share | 1001 | 2.0 | 1 | {'exact': 1} | 0.032 |
| opa | opa-rel-doc | opa-share | 1001 | 10.0 | 1 | {'exact': 1} | 0.032 |
| opa | opa-rel-doc | opa-share | 3000 | 2.0 | 1 | {'exact': 1} | 0.029 |
| opa | opa-rel-doc | opa-share | 3000 | 10.0 | 1 | {'exact': 1} | 0.028 |
| opa | opa-rel-pe | opa-share | 10 | 2.0 | 1 | {'exact': 1} | 0.276 |
| opa | opa-rel-pe | opa-share | 10 | 10.0 | 1 | {'exact': 1} | 0.291 |
| opa | opa-rel-pe | opa-share | 999 | 2.0 | 1 | {'exact': 1} | 0.253 |
| opa | opa-rel-pe | opa-share | 999 | 10.0 | 1 | {'exact': 1} | 0.256 |
| opa | opa-rel-pe | opa-share | 1000 | 2.0 | 1 | {'exact': 1} | 0.254 |
| opa | opa-rel-pe | opa-share | 1000 | 10.0 | 1 | {'exact': 1} | 0.255 |
| opa | opa-rel-pe | opa-share | 1001 | 2.0 | 1 | {'exact': 1} | 0.256 |
| opa | opa-rel-pe | opa-share | 1001 | 10.0 | 1 | {'exact': 1} | 0.247 |
| opa | opa-rel-pe | opa-share | 3000 | 2.0 | 1 | {'exact': 1} | 0.309 |
| opa | opa-rel-pe | opa-share | 3000 | 10.0 | 1 | {'exact': 1} | 0.291 |
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
| opa | opa-rel-doc | opa-share | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.112 |
| opa | opa-rel-doc | opa-share | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.088 |
| opa | opa-rel-doc | opa-share | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.088 |
| opa | opa-rel-doc | opa-share | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.086 |
| opa | opa-rel-doc | opa-share | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.083 |
| opa | opa-rel-pe | opa-share | 10 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.312 |
| opa | opa-rel-pe | opa-share | 999 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.341 |
| opa | opa-rel-pe | opa-share | 1000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.330 |
| opa | opa-rel-pe | opa-share | 1001 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.325 |
| opa | opa-rel-pe | opa-share | 3000 | 4 | 0 | 1.000 [1.000, 1.000] | 0 | 0 | {'prefilter': 4} | 0.352 |
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
| cerbos | cerbos | x4a-world | None | 2 | 2.162 | 0.265 | 59.2 [49.4, 69.0] | 5.9 [5.9, 5.9] |
| cerbos | cerbos-drift | x4a-world | None | 2 | 2.059 | 0.205 | 120.2 [100.2, 140.1] | 9.8 [9.8, 9.8] |
| cerbos | cerbos-excl | x4a-world | None | 2 | 2.125 | 0.223 | 120.0 [104.2, 135.8] | 8.7 [8.3, 9.2] |
| controls | control-oracle | x4a-world | None | 2 | 0.064 | 5.3e-04 | 6.7 [6.3, 7.0] | 5.6e-02 [5.6e-02, 5.7e-02] |
| controls | control-planted | x4a-world | None | 2 | 2.8e-04 | 5.3e-04 | 3.1e-02 [3.0e-02, 3.1e-02] | 5.7e-02 [5.5e-02, 6.0e-02] |
| opa | opa-acl-doc | x4a-world | None | 2 | 0.886 | 0.100 | 59.0 [48.1, 69.9] | 4.3 [3.9, 4.6] |
| opa | opa-acl-doc-drift | x4a-world | None | 2 | 0.804 | 0.094 | 54.0 [51.1, 56.8] | 3.9 [3.9, 4.0] |
| opa | opa-rel-doc | opa-share | 10 | 1 | 34.767 | 3.658 | 1539.6 [1539.6, 1539.6] | 149.2 [149.2, 149.2] |
| opa | opa-rel-doc | opa-share | 999 | 1 | 32.087 | 3.068 | 2314.1 [2314.1, 2314.1] | 213.3 [213.3, 213.3] |
| opa | opa-rel-doc | opa-share | 1000 | 1 | 34.715 | 3.197 | 2220.4 [2220.4, 2220.4] | 153.1 [153.1, 153.1] |
| opa | opa-rel-doc | opa-share | 1001 | 1 | 31.936 | 3.253 | 2452.9 [2452.9, 2452.9] | 224.1 [224.1, 224.1] |
| opa | opa-rel-doc | opa-share | 3000 | 1 | 28.463 | 2.432 | 2171.1 [2171.1, 2171.1] | 166.6 [166.6, 166.6] |
| opa | opa-rel-doc | x4a-world | None | 2 | 2.166 | 0.243 | 139.3 [112.9, 165.7] | 14.8 [11.3, 18.3] |
| opa | opa-rel-pe | opa-share | 10 | 1 | 231.587 | 3.263 | 18215.9 [18215.9, 18215.9] | 200.0 [200.0, 200.0] |
| opa | opa-rel-pe | opa-share | 999 | 1 | 257.857 | 3.342 | 19243.0 [19243.0, 19243.0] | 228.1 [228.1, 228.1] |
| opa | opa-rel-pe | opa-share | 1000 | 1 | 253.025 | 3.304 | 17931.0 [17931.0, 17931.0] | 227.4 [227.4, 227.4] |
| opa | opa-rel-pe | opa-share | 1001 | 1 | 251.899 | 3.136 | 19985.6 [19985.6, 19985.6] | 215.9 [215.9, 215.9] |
| opa | opa-rel-pe | opa-share | 3000 | 1 | 292.402 | 2.629 | 21102.9 [21102.9, 21102.9] | 178.8 [178.8, 178.8] |
| opa | opa-rel-pe | x4a-world | None | 2 | 21.336 | 0.210 | 1382.4 [1273.8, 1491.0] | 13.3 [11.7, 14.9] |
| opa | opa-rel-pe-excl | x4a-world | None | 2 | 22.953 | 0.210 | 1297.8 [976.5, 1619.1] | 11.7 [10.2, 13.2] |
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
| openfga | openfga | x4a-world | None | 2 | 3.969 | 1.416 | 562.9 [484.2, 641.6] | 181.1 [103.3, 258.9] |
| openfga | openfga-ctx | x4a-world | None | 2 | 3.361 | 0.995 | 426.0 [410.2, 441.9] | 128.6 [109.4, 147.8] |
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
| spicedb | spicedb | x4a-world | None | 2 | 3.036 | 0.131 | 428.1 [287.7, 568.5] | 19.6 [18.2, 21.0] |

## Harness

Runs: 5 job records; profile ['smoke']; commit ['3f2cff0'].
