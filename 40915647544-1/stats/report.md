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

### X2 settings (recall@10 with 95% interval; latency in its own job)

| corpus | store | layout | setting | pairs | builds | recall@10 | lo | hi | empty | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|
| e | chroma | default | default | 148 | 1 | 0.990 | 0.984 | 0.997 | 0.000 | 25.5 |
| e | chroma | default | ef10 | 148 | 1 | 0.990 | 0.984 | 0.997 | 0.000 | 25.4 |
| e | chroma | default | ef1000 | 148 | 1 | 0.990 | 0.984 | 0.997 | 0.000 | 25.6 |
| e | chroma | default | ef200 | 148 | 1 | 0.990 | 0.984 | 0.997 | 0.000 | 25.6 |
| e | chroma | default | ef50 | 148 | 1 | 0.990 | 0.984 | 0.997 | 0.000 | 25.2 |
| e | chroma | default | ef500 | 148 | 1 | 0.990 | 0.984 | 0.997 | 0.000 | 25.6 |
| e | elasticsearch | default | default | 148 | 1 | 0.978 | 0.966 | 0.991 | 0.000 | 7.647 |
| e | elasticsearch | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.653 |
| e | elasticsearch | default | nc100 | 148 | 1 | 0.978 | 0.966 | 0.991 | 0.000 | 3.888 |
| e | elasticsearch | default | nc10000 | 148 | 1 | 0.978 | 0.966 | 0.991 | 0.000 | 3.295 |
| e | elasticsearch | default | nc2000 | 148 | 1 | 0.978 | 0.966 | 0.991 | 0.000 | 3.374 |
| e | elasticsearch | default | nc50 | 148 | 1 | 0.978 | 0.966 | 0.991 | 0.000 | 4.915 |
| e | elasticsearch | default | nc500 | 148 | 1 | 0.978 | 0.966 | 0.991 | 0.000 | 3.297 |
| e | elasticsearch | int8 | default | 148 | 1 | 0.949 | 0.927 | 0.980 | 0.000 | 3.766 |
| e | elasticsearch | int8 | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.908 |
| e | elasticsearch | int8 | nc100 | 148 | 1 | 0.982 | 0.975 | 0.993 | 0.000 | 3.072 |
| e | elasticsearch | int8 | nc10000 | 148 | 1 | 0.993 | 0.990 | 0.998 | 0.000 | 3.053 |
| e | elasticsearch | int8 | nc2000 | 148 | 1 | 0.993 | 0.990 | 0.998 | 0.000 | 2.864 |
| e | elasticsearch | int8 | nc50 | 148 | 1 | 0.959 | 0.941 | 0.984 | 0.000 | 3.083 |
| e | elasticsearch | int8 | nc500 | 148 | 1 | 0.993 | 0.990 | 0.998 | 0.000 | 3.038 |
| e | faiss | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 14.8 |
| e | lancedb | default | default | 148 | 1 | 0.706 | 0.624 | 0.841 | 0.000 | 2.626 |
| e | lancedb | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.761 |
| e | lancedb | default | np10 | 148 | 1 | 0.706 | 0.624 | 0.841 | 0.000 | 2.580 |
| e | lancedb | default | np100 | 148 | 1 | 0.706 | 0.624 | 0.841 | 0.000 | 2.571 |
| e | lancedb | default | np200 | 148 | 1 | 0.706 | 0.624 | 0.841 | 0.000 | 2.613 |
| e | lancedb | default | np50 | 148 | 1 | 0.706 | 0.624 | 0.841 | 0.000 | 2.613 |
| e | lancedb | default | np500 | 148 | 1 | 0.706 | 0.624 | 0.841 | 0.000 | 2.517 |
| e | lancedb | default | postfilter | 148 | 1 | 0.063 | 0.027 | 0.118 | 0.736 | 2.284 |
| e | lancedb | default | refine | 148 | 1 | 0.997 | 0.995 | 1.000 | 0.000 | 3.952 |
| e | milvus | default | default | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.990 |
| e | milvus | default | ef100 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 5.262 |
| e | milvus | default | ef256 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.754 |
| e | milvus | default | ef32 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.852 |
| e | milvus | default | ef512 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.010 |
| e | milvus | default | ef64 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 5.094 |
| e | mongodb | default | default | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 5.111 |
| e | mongodb | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.269 |
| e | mongodb | default | nc1000 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.552 |
| e | mongodb | default | nc10000 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.158 |
| e | mongodb | default | nc20 | 148 | 1 | 0.965 | 0.948 | 0.988 | 0.000 | 2.979 |
| e | mongodb | default | nc200 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.429 |
| e | mongodb | default | nc50 | 148 | 1 | 0.995 | 0.989 | 0.999 | 0.000 | 2.920 |
| e | opensearch | default | default | 148 | 1 | 0.998 | 0.997 | 1.000 | 0.000 | 3.051 |
| e | opensearch | default | ef128 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.762 |
| e | opensearch | default | ef256 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.532 |
| e | opensearch | default | ef32 | 148 | 1 | 0.987 | 0.982 | 0.995 | 0.000 | 2.199 |
| e | opensearch | default | ef512 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.513 |
| e | opensearch | default | ef64 | 148 | 1 | 0.993 | 0.990 | 0.997 | 0.000 | 2.021 |
| e | opensearch | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.206 |
| e | pgvector | default | default | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 10.4 |
| e | pgvector | default | ef100 | 148 | 1 | 0.955 | 0.938 | 0.981 | 0.000 | 2.778 |
| e | pgvector | default | ef1000 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 11.0 |
| e | pgvector | default | ef200 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 11.1 |
| e | pgvector | default | ef40 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 10.9 |
| e | pgvector | default | ef400 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 10.9 |
| e | pgvector | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 10.9 |
| e | pgvector | default | scan1m | 148 | 1 | 0.955 | 0.938 | 0.981 | 0.000 | 3.151 |
| e | pgvector | default | strict | 148 | 1 | 0.865 | 0.816 | 0.944 | 0.000 | 2.845 |
| e | qdrant | as-run | acorn | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.801 |
| e | qdrant | as-run | acorn-max | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.786 |
| e | qdrant | as-run | default | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.873 |
| e | qdrant | as-run | ef1024 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.776 |
| e | qdrant | as-run | ef128 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.052 |
| e | qdrant | as-run | ef256 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.066 |
| e | qdrant | as-run | ef512 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.032 |
| e | qdrant | as-run | ef64 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.675 |
| e | qdrant | as-run | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.727 |
| e | qdrant | tenant | acorn-max | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.887 |
| e | qdrant | tenant | ef128 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.756 |
| e | qdrant | tenant | ef512 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.007 |
| e | qdrant | tenant | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 3.863 |
| e | redis | default | batches | 148 | 1 | 0.968 | 0.954 | 0.987 | 0.000 | 1.323 |
| e | redis | default | default | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.335 |
| e | redis | default | ef100 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.320 |
| e | redis | default | ef1000 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.306 |
| e | redis | default | ef200 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.307 |
| e | redis | default | ef50 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.294 |
| e | redis | default | ef500 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.312 |
| e | redis | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.302 |
| e | weaviate | default | default | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.249 |
| e | weaviate | default | ef1024 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.211 |
| e | weaviate | default | ef128 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.205 |
| e | weaviate | default | ef256 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.206 |
| e | weaviate | default | ef512 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.225 |
| e | weaviate | default | ef64 | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.200 |
| e | weaviate | default | exact | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.199 |
| e | weaviate | default | noflat | 148 | 1 | 0.989 | 0.984 | 0.996 | 0.000 | 2.357 |
| e | weaviate | default | sweeping | 148 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.228 |
| m | chroma | default | default | 241 | 1 | 1.000 | 0.999 | 1.000 | 0.000 | 205.9 |
| m | chroma | default | ef10 | 228 | 1 | 1.000 | 0.999 | 1.000 | 0.000 | 206.7 |
| m | chroma | default | ef200 | 218 | 1 | 1.000 | 0.999 | 1.000 | 0.000 | 200.6 |
| m | chroma | default | ef50 | 224 | 1 | 1.000 | 0.999 | 1.000 | 0.000 | 200.9 |
| m | chroma | default | ef500 | 203 | 1 | 1.000 | 0.999 | 1.000 | 0.000 | 199.6 |
| m | elasticsearch | default | default | 248 | 1 | 0.930 | 0.921 | 0.938 | 0.000 | 5.077 |
| m | elasticsearch | default | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.409 |
| m | elasticsearch | default | nc100 | 248 | 1 | 0.922 | 0.914 | 0.931 | 0.000 | 2.454 |
| m | elasticsearch | default | nc10000 | 248 | 1 | 0.927 | 0.920 | 0.935 | 0.000 | 2.044 |
| m | elasticsearch | default | nc2000 | 248 | 1 | 0.927 | 0.920 | 0.935 | 0.000 | 2.096 |
| m | elasticsearch | default | nc50 | 248 | 1 | 0.922 | 0.914 | 0.931 | 0.000 | 3.029 |
| m | elasticsearch | default | nc500 | 248 | 1 | 0.927 | 0.920 | 0.935 | 0.000 | 2.123 |
| m | faiss | default | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 27.0 |
| m | lancedb | default | default | 248 | 1 | 0.612 | 0.597 | 0.626 | 0.000 | 4.428 |
| m | lancedb | default | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 5.858 |
| m | lancedb | default | np10 | 248 | 1 | 0.612 | 0.597 | 0.626 | 0.000 | 4.514 |
| m | lancedb | default | np100 | 248 | 1 | 0.612 | 0.597 | 0.626 | 0.000 | 4.785 |
| m | lancedb | default | np200 | 248 | 1 | 0.612 | 0.597 | 0.626 | 0.000 | 4.578 |
| m | lancedb | default | np50 | 248 | 1 | 0.612 | 0.597 | 0.626 | 0.000 | 4.523 |
| m | lancedb | default | np500 | 248 | 1 | 0.612 | 0.597 | 0.626 | 0.000 | 4.324 |
| m | lancedb | default | postfilter | 248 | 1 | 0.167 | 0.158 | 0.175 | 0.560 | 4.358 |
| m | lancedb | default | refine | 248 | 1 | 0.996 | 0.993 | 0.998 | 0.000 | 6.729 |
| m | milvus | default | default | 248 | 1 | 0.727 | 0.706 | 0.750 | 0.000 | 7.071 |
| m | milvus | default | ef100 | 248 | 1 | 0.999 | 0.998 | 1.000 | 0.000 | 2.934 |
| m | milvus | default | ef256 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.833 |
| m | milvus | default | ef32 | 248 | 1 | 0.752 | 0.735 | 0.771 | 0.000 | 3.123 |
| m | milvus | default | ef512 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.704 |
| m | milvus | default | ef64 | 248 | 1 | 0.997 | 0.995 | 0.998 | 0.000 | 3.026 |
| m | mongodb | default | default | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.448 |
| m | mongodb | default | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.172 |
| m | mongodb | default | nc1000 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.421 |
| m | mongodb | default | nc10000 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.365 |
| m | mongodb | default | nc20 | 248 | 1 | 0.998 | 0.997 | 0.999 | 0.000 | 2.552 |
| m | mongodb | default | nc200 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.423 |
| m | mongodb | default | nc50 | 248 | 1 | 0.998 | 0.996 | 1.000 | 0.000 | 2.520 |
| m | opensearch | default | default | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 4.438 |
| m | opensearch | default | ef128 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.397 |
| m | opensearch | default | ef256 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.310 |
| m | opensearch | default | ef32 | 248 | 1 | 0.999 | 0.998 | 1.000 | 0.000 | 3.245 |
| m | opensearch | default | ef512 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.274 |
| m | opensearch | default | ef64 | 248 | 1 | 1.000 | 0.999 | 1.000 | 0.000 | 2.557 |
| m | opensearch | default | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.649 |
| m | qdrant | as-run | acorn | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.218 |
| m | qdrant | as-run | acorn-max | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.300 |
| m | qdrant | as-run | default | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.255 |
| m | qdrant | as-run | ef1024 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.244 |
| m | qdrant | as-run | ef128 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.281 |
| m | qdrant | as-run | ef256 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.297 |
| m | qdrant | as-run | ef512 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.204 |
| m | qdrant | as-run | ef64 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.318 |
| m | qdrant | as-run | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.324 |
| m | qdrant | tenant | acorn-max | 120 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.559 |
| m | qdrant | tenant | ef128 | 120 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.619 |
| m | qdrant | tenant | ef512 | 120 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.529 |
| m | qdrant | tenant | exact | 120 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.536 |
| m | redis | default | batches | 248 | 1 | 0.992 | 0.988 | 0.995 | 0.000 | 1.930 |
| m | redis | default | default | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.575 |
| m | redis | default | ef100 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.559 |
| m | redis | default | ef1000 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.542 |
| m | redis | default | ef200 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.579 |
| m | redis | default | ef50 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.557 |
| m | redis | default | ef500 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.597 |
| m | redis | default | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 0.570 |
| m | weaviate | default | default | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.100 |
| m | weaviate | default | ef1024 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.984 |
| m | weaviate | default | ef128 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.190 |
| m | weaviate | default | ef256 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.971 |
| m | weaviate | default | ef512 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.970 |
| m | weaviate | default | ef64 | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.179 |
| m | weaviate | default | exact | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.225 |
| m | weaviate | default | noflat | 248 | 1 | 0.936 | 0.926 | 0.946 | 0.000 | 3.258 |
| m | weaviate | default | sweeping | 248 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 2.056 |

### X5 arms

| corpus | store | layout | arm | recall5 | recall10 | err10 | short10 | trigger10 | detection10 | false_complete10 | p50_ms | triggered_p95_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e | pgvector | default | count | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.249 | 2.278 | 3.565 |
| e | pgvector | default | exact-10k | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.249 | 2.177 | 0.912 |
| e | pgvector | default | exact-1k | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.249 | 2.261 | 0.943 |
| e | pgvector | default | exact-inf | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.249 | 2.266 | 3.489 |
| e | pgvector | default | monitor | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.318 | 2.256 | 0.000 |
| e | pgvector | default | native-scan1m | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.318 | 2.260 | 0.000 |
| e | pgvector | default | report | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.318 | 2.090 | 0.000 |
| e | pgvector | default | widen | 0.955 | 0.956 | 0.000 | 0.000 | 0.219 | n/a | 0.249 | 2.268 | 3.561 |
| e | qdrant | as-run | count | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.289 | 1.569 |
| e | qdrant | as-run | exact-10k | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.227 | 1.564 |
| e | qdrant | as-run | exact-1k | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.245 | 1.567 |
| e | qdrant | as-run | exact-inf | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.207 | 1.596 |
| e | qdrant | as-run | monitor | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.135 | 0.000 |
| e | qdrant | as-run | native-acorn | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.154 | 0.000 |
| e | qdrant | as-run | report | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.193 | 0.000 |
| e | qdrant | as-run | widen | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.221 | 1.530 |
| e | qdrant | tenant | native-tenant | 1.000 | 1.000 | 0.000 | 0.000 | 0.219 | n/a | 0.000 | 3.438 | 0.000 |
| m | qdrant | as-run | count | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.522 | 1.537 |
| m | qdrant | as-run | exact-10k | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.519 | 1.549 |
| m | qdrant | as-run | exact-1k | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.559 | 1.516 |
| m | qdrant | as-run | exact-inf | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.559 | 1.512 |
| m | qdrant | as-run | monitor | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.553 | 0.000 |
| m | qdrant | as-run | native-acorn | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.568 | 0.000 |
| m | qdrant | as-run | report | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.542 | 0.000 |
| m | qdrant | as-run | widen | 1.000 | 1.000 | 0.000 | 0.000 | 0.016 | n/a | 0.000 | 2.558 | 1.495 |

### H2.1: falsified

- qdrant: G 0.0000 [0.0000, 0.0000], positive in 0 of 5 seeds: no gap
- elasticsearch: G 0.0875 [0.0458, 0.1312], positive in 2 of 5 seeds: unclear
- opensearch: G 0.0000 [0.0000, 0.0000], positive in 0 of 5 seeds: no gap
- weaviate: G 0.0000 [0.0000, 0.0000], positive in 0 of 5 seeds: no gap
- redis: G 0.0000 [0.0000, 0.0000], positive in 0 of 5 seeds: no gap
- milvus: G 0.2396 [0.1646, 0.3104], positive in 2 of 5 seeds: unclear
- mongodb: G 0.0000 [0.0000, 0.0000], positive in 0 of 5 seeds: no gap
- lancedb: G 0.2042 [0.1562, 0.2521], positive in 2 of 5 seeds: unclear
- chroma: G -0.0023 [-0.0047, 0.0000], positive in 0 of 5 seeds: no gap
- stores with a gap: 0 (confirm at 6); with no gap: 6 (falsify at 5)

### H2.2: falsified

- qdrant: D nan [nan, nan], 0 pairs below 1: not assessable
- elasticsearch: D -0.4143 [-0.4408, -0.3822], 96 pairs below 1: not assessable
- opensearch: D nan [nan, nan], 0 pairs below 1: not assessable
- weaviate: D nan [nan, nan], 0 pairs below 1: not assessable
- redis: D nan [nan, nan], 0 pairs below 1: not assessable
- milvus: D 0.3148 [0.2543, 0.3790], 180 pairs below 1: local
- mongodb: D nan [nan, nan], 0 pairs below 1: not assessable
- lancedb: D -0.4345 [-0.4709, -0.4001], 241 pairs below 1: global
- chroma: D -0.0057 [-0.0107, -0.0033], 1 pairs below 1: not assessable
- assessable 2, local 1, global 1

### H2.3: inconclusive

- stores with a gap and a sweep: 0; narrowed and remaining: 0; closed: 0

### H2.4: falsified

- qdrant: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- elasticsearch: V 0.1625 [0.1250, 0.2000], 2 seeds: neither
- opensearch: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- weaviate: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- redis: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- milvus: V 0.5375 [0.4500, 0.6875], 2 seeds: neither
- mongodb: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- lancedb: V 0.4750 [0.4000, 0.5625], 2 seeds: neither
- chroma: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- U-shaped 0 (confirm at 5), monotone 6 (falsify at 5)

### H5.1: inconclusive

- e pgvector: 0 truly short first searches (< 10): not judged
- e qdrant: 0 truly short first searches (< 10): not judged
- m qdrant: 0 truly short first searches (< 10): not judged

### H5.2: inconclusive

- pgvector e: report has 0 short results (< 10) or no exact-inf: not judged
- pgvector m: report has 0 short results (< 10) or no exact-inf: not judged
- qdrant e: report has 0 short results (< 10) or no exact-inf: not judged
- qdrant m: report has 0 short results (< 10) or no exact-inf: not judged

### H5.3: confirmed

- e pgvector b0 count: median latency ratio on 132 untriggered pairs 1.0365
- e pgvector b0 exact-1k: median latency ratio on 132 untriggered pairs 1.0236
- e pgvector b0 exact-10k: median latency ratio on 132 untriggered pairs 0.9785
- e pgvector b0 exact-inf: median latency ratio on 132 untriggered pairs 1.0138
- e pgvector b0 widen: median latency ratio on 132 untriggered pairs 1.0148
- e qdrant b0 count: median latency ratio on 132 untriggered pairs 1.0114
- e qdrant b0 exact-1k: median latency ratio on 132 untriggered pairs 0.9949
- e qdrant b0 exact-10k: median latency ratio on 132 untriggered pairs 0.9867
- e qdrant b0 exact-inf: median latency ratio on 132 untriggered pairs 0.9926
- e qdrant b0 widen: median latency ratio on 132 untriggered pairs 0.9880
- m qdrant b0 count: median latency ratio on 244 untriggered pairs 0.9749
- m qdrant b0 exact-1k: median latency ratio on 244 untriggered pairs 0.9980
- m qdrant b0 exact-10k: median latency ratio on 244 untriggered pairs 0.9838
- m qdrant b0 exact-inf: median latency ratio on 244 untriggered pairs 0.9954
- m qdrant b0 widen: median latency ratio on 244 untriggered pairs 0.9957

### H5.4: falsified

- report: false-completeness 0.0000 (confirm needs >= 0.20)
- count: 0.0000, minus report 0.0000 [0.0000, 0.0000]
- exact-1k: 0.0000, minus report 0.0000 [0.0000, 0.0000]
- exact-10k: 0.0000, minus report 0.0000 [0.0000, 0.0000]
- exact-inf: 0.0000, minus report 0.0000 [0.0000, 0.0000]
- widen: 0.0000, minus report 0.0000 [0.0000, 0.0000]

### H5.5: confirmed

- (a) x5-e-pgvector default b0: 5 of 676 sampled: inside the 99.9% interval
- (a) x5-e-qdrant as-run b0: 9 of 676 sampled: inside the 99.9% interval
- (a) x5-m-qdrant-b0 as-run b0: 11 of 992 sampled: inside the 99.9% interval
- (b) agreement within 0.1 on 25 sampled retrievals: 1.0000
- (c) Qdrant e: mean sampled 1.0000 on 9, population 1.0000, difference 0.0000
- (c) Qdrant m: mean sampled 1.0000 on 11, population 1.0000, difference 0.0000

### H5.6: falsified

- exact-inf minus widen on 37 triggered pairs: 0.0000 [0.0000, 0.0000], Wilcoxon p nan

### H5.7: falsified

- per-tenant layout recall@10 1.0000; best library arm 1.0000

