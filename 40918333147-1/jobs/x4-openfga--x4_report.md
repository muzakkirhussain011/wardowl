# X4: engine filters against engine checks

Profile: ['smoke']. Files: 1; records: 55. **Smoke data: not analysed for the hypotheses.**

## Verdicts

| Hypothesis | Verdict | Numbers |
|---|---|---|
| G1 controls | FALSIFIED | control-oracle 0 subjects, some disagreeing; control-planted 0 subjects, counts NOT exact |
| G2 encoding openfga | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 openfga | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| G2 encoding openfga-ctx | CONFIRMED | check vs oracle 0 of 1440 pairs |
| X4-H1 openfga-ctx | INCONCLUSIVE | 12 subjects with a filter, 0 false admits, 0 false denials, 0 reproduce; subject bound 0.2209 |
| X4-H4c openfga quiet-hc | INCONCLUSIVE | 6 trials, trials disagreeing 0.000 [0.000, 0.000], 0 pairs, 0 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-hc | INCONCLUSIVE | 6 trials, trials disagreeing 0.667 [0.333, 1.000], 16 pairs, 16 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4b openfga writer-ml | INCONCLUSIVE | 6 trials, trials disagreeing 0.333 [0.000, 0.667], 10 pairs, 10 skew-explained, 0 reproduce, 0 oracle mismatches |
| X4-H4d spicedb ml minus pinned | INCONCLUSIVE | 0 pairs, difference n/a [n/a, n/a] |
| X4-H5a openfga | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5b spicedb | INCONCLUSIVE | 0 calls, 0 with another count, 0 with keys besides objects |
| X4-H5c no silent truncation | INCONCLUSIVE | 0 calls, 0 silent short filters |
| X4-H5d filter below the limit, none at it | INCONCLUSIVE | 0 small-N calls without an exact filter, 0 large-N calls with a filter |
| X4c exploratory: list calls over 2 s | EXPLORATORY | [] |
| X4-H7 caching openfga | CONFIRMED | 2 cells; lowest median ratio 128.6 |

## X4a: one revision

| profile | subjects | with filter | errors | pairs | false admits | false denials | reproduce | subjects disagreeing [95% CI] | zero bound | pair rate [95% CI] | check vs oracle | check vs oracle rate | seeds | false admits on scalar fields |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openfga | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |
| openfga-ctx | 12 | 12 | 0 | 1440 | 0 | 0 | 0 | 0.000 [0.000, 0.000] | 0.2209 | 0.000000 [0.000000, 0.000000] | 0 | 0.000000 | 1 | 0 |

## X4b: unpinned, under a writer

| engine | condition | trials | trials disagreeing [95% CI] | pairs | skew-explained | explained share | reproduce | oracle mismatches | median writes in window | seeds |
|---|---|---|---|---|---|---|---|---|---|---|
| openfga | quiet-hc | 6 | 0.000 [0.000, 0.000] | 0 | 0 | n/a | 0 | 0 | n/a | 1 |
| openfga | writer-hc | 6 | 0.667 [0.333, 1.000] | 16 | 16 | 1.000 | 0 | 0 | 4.500 | 1 |
| openfga | writer-ml | 6 | 0.333 [0.000, 0.667] | 10 | 10 | 1.000 | 0 | 0 | 5.000 | 1 |

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
| openfga | openfga | x4a-world | None | 2 | 3.969 | 1.416 | 562.9 [484.2, 641.6] | 181.1 [103.3, 258.9] |
| openfga | openfga-ctx | x4a-world | None | 2 | 3.361 | 0.995 | 426.0 [410.2, 441.9] | 128.6 [109.4, 147.8] |

## Harness

Runs: 1 job records; profile ['smoke']; commit ['3f2cff0'].
