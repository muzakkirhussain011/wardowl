# X4: engine filters against engine checks

Profile: ['full']. Files: 1; records: 1925.

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | FALSIFIED | control-oracle 0 subjects, some disagreeing; control-planted 0 subjects, counts NOT exact |
| G2 encoding openfga | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 openfga | INCONCLUSIVE | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| G2 encoding openfga-ctx | CONFIRMED | check vs oracle 0 of 900000 pairs |
| X4-H1 openfga-ctx | INCONCLUSIVE | 600 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.0050 |
| X4-H4c openfga quiet-hc | CONFIRMED | 200 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-hc | CONFIRMED | 200 trials, trials disagreeing 1.000 [1.000, 1.000], 9433 pairs, 9433 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-ml | CONFIRMED | 200 trials, trials disagreeing 1.000 [1.000, 1.000], 9972 pairs, 9972 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | INCONCLUSIVE | 0 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | INCONCLUSIVE | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [] |
| X4-H7 caching openfga | CONFIRMED | 2 cells; lowest median ratio 102.9 |

## X4a: one revision

| profile | subjects | with filter | errors | pairs | false admits | false denials | reproduce | subjects disagreeing [95% CI] | zero bound | pair rate [95% CI] | check vs oracle | check vs oracle rate | seeds | false admits on scalar fields |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openfga | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |
| openfga-ctx | 600 | 600 | 0 | 900000 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.0050 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 5 | 0 |

## X4b: unpinned, under a writer

| engine | condition | trials | trials disagreeing [95% CI] | pairs | skew-explained | explained share | reproduce | oracle mismatches | median writes in window | seeds |
|---|---|---|---|---|---|---|---|---|---|---|
| openfga | quiet-hc | 200 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 5 |
| openfga | writer-hc | 200 | 1.000 [1.000, 1.000] | 9433 | 9433 | 1.000 | 0 | 0 | 59.000 | 5 |
| openfga | writer-ml | 200 | 1.000 [1.000, 1.000] | 9972 | 9972 | 1.000 | 0 | 0 | 208.000 | 5 |

## X4c: truncation

#### Engine list calls

| engine | structure | N | api | calls | status 200 | counts | median s | missing | extra | with cursor | error lines | answer keys |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

#### wardowl's filter_for

| engine | route | structure | N | timeout s | calls | outcomes | median s |
|---|---|---|---|---|---|---|---|

#### Permission-recall@10 through wardowl

| engine | route | structure | N | queries | failed | recall@10 [95% CI] | false complete | leaks | strategies | median s |
|---|---|---|---|---|---|---|---|---|---|---|

## X4d: latency and caching

| engine | route | structure | N | records | filter_for uncached ms (median) | check per hit ms | filter speedup cached [95% CI] | check speedup cached [95% CI] |
|---|---|---|---|---|---|---|---|---|
| openfga | openfga | x4a-world | None | 50 | 4.147 | 0.727 | 615.8 [476.2, 671.7] | 106.8 [103.5, 115.3] |
| openfga | openfga-ctx | x4a-world | None | 50 | 3.887 | 0.711 | 481.8 [410.0, 530.8] | 102.9 [97.9, 116.4] |

## Harness

Runs: 1 job records; profile ['full']; commit ['e66dffc'].
