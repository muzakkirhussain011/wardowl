# X4: engine filters against engine checks

Profile: ['full']. Files: 1; records: 9904.

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
| X4-H4c opa quiet | CONFIRMED | 200 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b opa writer | CONFIRMED | 200 trials, trials disagreeing 0.130 [0.085, 0.180], 97 pairs, 97 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | INCONCLUSIVE | 0 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | INCONCLUSIVE | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c OPA routes exact (consistency check) | EXPLORATORY | 180 calls, 45 not exact: {'error': 45} |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [] |
| X4-H7 caching cerbos | INCONCLUSIVE | 1 cells; lowest median ratio 8.6 |
| X4-H7 caching opa | CONFIRMED | 20 cells; lowest median ratio 114.3 |

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

## X4b: unpinned, under a writer

| engine | condition | trials | trials disagreeing [95% CI] | pairs | skew-explained | explained share | reproduce | oracle mismatches | median writes in window | seeds |
|---|---|---|---|---|---|---|---|---|---|---|
| opa | quiet | 200 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 5 |
| opa | writer | 200 | 0.130 [0.085, 0.180] | 97 | 97 | 1.000 | 0 | 0 | 1.000 | 5 |

## X4c: truncation

#### Engine list calls

| engine | structure | N | api | calls | status 200 | counts | median s | missing | extra | with cursor | error lines | answer keys |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

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

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].

| job | where | count | error |
|---|---|---|---|
| x4-policy | ['retriever.py:285 retrieve', 'retriever.py:510 _run', 'x4_engines.py:234 filter_for', '_http.py:321 post_json'] | 1350 | wardowl.authz.AuthorizationError: OPA compile x4rel/allow timed out after 2.0 s |
| x4-policy | ['x4_engines.py:1235 _filter', 'x4_engines.py:234 filter_for', '_http.py:321 post_json'] | 45 | wardowl.authz.AuthorizationError: OPA compile x4rel/allow timed out after 2.0 s |
