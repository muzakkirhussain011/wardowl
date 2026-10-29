# paper-x2-x5 run 40915647544, attempt 1

- run: https://github.com/muzakkirhussain011/wardowl/actions/runs/40915647544
- commit: c1e20f84bad6b7e9c1c9b9a85b113fd06c391dd6 (paper/x2-x5)
- mode: smoke; data from run: this run
- jobs: embed-e=success embed-m=success prepare-e=success prepare-m=success x2-e=success x2-m=failure x5-e=success x5-m=failure stats=success
- finished: 2026-10-29T17:25:36Z
## X2 and X5: pre-registered verdicts

| hypothesis | verdict |
|---|---|
| H2.1 | falsified |
| H2.2 | falsified |
| H2.3 | inconclusive |
| H2.4 | falsified |
| H5.1 | inconclusive |
| H5.2 | inconclusive |
| H5.3 | confirmed |
| H5.4 | falsified |
| H5.5 | confirmed |
| H5.6 | falsified |
| H5.7 | falsified |

Validity: {"V1": true, "V2": "2 of 9 stores within 0.03", "V2_holds": false, "V3": true, "V4": [1.0]}

### Jobs

| exp | job | status | failures | skipped |
|---|---|---|---|---|
| x2 | x2-e-chroma | done | 0 | 0 |
| x2 | x2-e-elasticsearch | done | 0 | 0 |
| x2 | x2-e-faiss | done | 0 | 0 |
| x2 | x2-e-lancedb | done | 0 | 0 |
| x2 | x2-e-milvus | done | 0 | 0 |
| x2 | x2-e-mongodb | done | 0 | 0 |
| x2 | x2-e-opensearch | done | 0 | 0 |
| x2 | x2-e-pgvector | done | 0 | 0 |
| x2 | x2-e-qdrant | done | 0 | 0 |
| x2 | x2-e-redis | done | 0 | 0 |
| x2 | x2-e-weaviate | done | 0 | 0 |
| x2 | x2-m-chroma-b0 | done | 0 | 1 |
| x2 | x2-m-elasticsearch-b0 | done | 0 | 0 |
| x2 | x2-m-faiss | done | 0 | 0 |
| x2 | x2-m-lancedb-b0 | done | 0 | 0 |
| x2 | x2-m-milvus-b0 | done | 0 | 0 |
| x2 | x2-m-mongodb-b0 | done | 0 | 0 |
| x2 | x2-m-opensearch-b0 | done | 0 | 0 |
| x2 | x2-m-pgvector-b0 | done with failures | 1 | 0 |
| x2 | x2-m-qdrant-b0 | done | 0 | 0 |
| x2 | x2-m-qdrant-tenant-b0 | done | 0 | 0 |
| x2 | x2-m-redis-b0 | done | 0 | 0 |
| x2 | x2-m-weaviate-b0 | done | 0 | 0 |
| x5 | x5-e-pgvector | done | 0 | 0 |
| x5 | x5-e-qdrant | done | 0 | 0 |
| x5 | x5-m-pgvector-b0 | done with failures | 1 | 0 |
| x5 | x5-m-qdrant-b0 | done | 0 | 0 |

