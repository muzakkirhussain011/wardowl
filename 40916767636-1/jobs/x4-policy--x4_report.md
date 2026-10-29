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
| X4-H7 caching cerbos | INCONCLUSIVE | 1 cells; lowest median ratio 9.4 |
| X4-H7 caching opa | CONFIRMED | 12 cells; lowest median ratio 13.1 |

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

## Harness

Runs: 1 job records; profile ['smoke']; commit ['62a587a'].
