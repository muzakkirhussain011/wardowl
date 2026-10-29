# X4: engine filters against engine checks

Profile: ['smoke']. Files: 1; records: 242. **Smoke data: not analysed for the hypotheses.**

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
| X4-H4c opa quiet | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b opa writer | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | INCONCLUSIVE | 0 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | INCONCLUSIVE | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c OPA routes exact (consistency check) | EXPLORATORY | 20 calls, 0 not exact: {} |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [] |
| X4-H7 caching cerbos | INCONCLUSIVE | 1 cells; lowest median ratio 5.9 |
| X4-H7 caching opa | CONFIRMED | 12 cells; lowest median ratio 13.3 |

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

## X4b: unpinned, under a writer

| engine | condition | trials | trials disagreeing [95% CI] | pairs | skew-explained | explained share | reproduce | oracle mismatches | median writes in window | seeds |
|---|---|---|---|---|---|---|---|---|---|---|
| opa | quiet | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |
| opa | writer | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | 0.000 | 1 |

## X4c: truncation

#### Engine list calls

| engine | structure | N | api | calls | status 200 | counts | median s | missing | extra | with cursor | error lines | answer keys |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

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

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
