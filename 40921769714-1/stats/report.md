## X2 and X5: pre-registered verdicts

| hypothesis | verdict |
|---|---|
| H2.1 | inconclusive |
| H2.2 | falsified |
| H2.3 | confirmed |
| H2.4 | confirmed |
| H5.1 | confirmed |
| H5.2 | confirmed |
| H5.3 | inconclusive |
| H5.4 | confirmed |
| H5.5 | confirmed |
| H5.6 | confirmed |
| H5.7 | confirmed |

Validity: {"V1": true, "V2": "8 of 9 stores within 0.03", "V2_holds": true, "V3": true, "V4": [1.0]}

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
| x2 | x2-m-chroma-b0 | done | 0 | 0 |
| x2 | x2-m-chroma-b1 | done | 0 | 2 |
| x2 | x2-m-chroma-b2 | running | 0 | 1 |
| x2 | x2-m-elasticsearch-b0 | done | 0 | 0 |
| x2 | x2-m-elasticsearch-b1 | done | 0 | 0 |
| x2 | x2-m-elasticsearch-b2 | done | 0 | 0 |
| x2 | x2-m-faiss | done | 0 | 0 |
| x2 | x2-m-lancedb-b0 | done | 0 | 0 |
| x2 | x2-m-lancedb-b1 | done | 0 | 0 |
| x2 | x2-m-lancedb-b2 | done | 0 | 0 |
| x2 | x2-m-milvus-b0 | done | 0 | 0 |
| x2 | x2-m-milvus-b1 | done | 0 | 0 |
| x2 | x2-m-milvus-b2 | done | 0 | 0 |
| x2 | x2-m-mongodb-b0 | done | 0 | 0 |
| x2 | x2-m-mongodb-b1 | done | 0 | 0 |
| x2 | x2-m-mongodb-b2 | done | 0 | 0 |
| x2 | x2-m-opensearch-b0 | done | 0 | 0 |
| x2 | x2-m-opensearch-b1 | done | 0 | 0 |
| x2 | x2-m-opensearch-b2 | done | 0 | 0 |
| x2 | x2-m-pgvector-b0 | done | 0 | 0 |
| x2 | x2-m-pgvector-b1 | done | 0 | 0 |
| x2 | x2-m-pgvector-b2 | done | 0 | 0 |
| x2 | x2-m-qdrant-b0 | done | 0 | 0 |
| x2 | x2-m-qdrant-b1 | done | 0 | 0 |
| x2 | x2-m-qdrant-b2 | done | 0 | 0 |
| x2 | x2-m-qdrant-tenant-b0 | done | 0 | 0 |
| x2 | x2-m-qdrant-tenant-b1 | done | 0 | 0 |
| x2 | x2-m-qdrant-tenant-b2 | done | 0 | 0 |
| x2 | x2-m-redis-b0 | done | 0 | 0 |
| x2 | x2-m-redis-b1 | done | 0 | 0 |
| x2 | x2-m-redis-b2 | done | 0 | 0 |
| x2 | x2-m-weaviate-b0 | done | 0 | 0 |
| x2 | x2-m-weaviate-b1 | done | 0 | 0 |
| x2 | x2-m-weaviate-b2 | done | 0 | 0 |
| x5 | x5-e-pgvector | done | 0 | 0 |
| x5 | x5-e-qdrant | done | 0 | 0 |
| x5 | x5-m-pgvector-b0 | done | 0 | 0 |
| x5 | x5-m-pgvector-b1 | done | 0 | 0 |
| x5 | x5-m-pgvector-b2 | done | 0 | 0 |
| x5 | x5-m-qdrant-b0 | done | 0 | 0 |
| x5 | x5-m-qdrant-b1 | done | 0 | 0 |
| x5 | x5-m-qdrant-b2 | done | 0 | 0 |

### X2 settings (recall@10 with 95% interval; latency in its own job)

| corpus | store | layout | setting | pairs | builds | recall@10 | lo | hi | empty | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|
| e | chroma | default | default | 407 | 3 | 0.983 | 0.976 | 0.990 | 0.000 | 998.0 |
| e | chroma | default | ef10 | 402 | 3 | 0.983 | 0.975 | 0.989 | 0.000 | 996.2 |
| e | chroma | default | ef1000 | 381 | 3 | 0.984 | 0.976 | 0.990 | 0.000 | 999.9 |
| e | chroma | default | ef200 | 394 | 3 | 0.983 | 0.975 | 0.989 | 0.000 | 1000.4 |
| e | chroma | default | ef50 | 396 | 3 | 0.983 | 0.975 | 0.989 | 0.000 | 996.7 |
| e | chroma | default | ef500 | 387 | 3 | 0.984 | 0.976 | 0.990 | 0.000 | 996.3 |
| e | elasticsearch | default | default | 1468 | 3 | 0.815 | 0.805 | 0.825 | 0.000 | 3.380 |
| e | elasticsearch | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 20.2 |
| e | elasticsearch | default | nc100 | 1468 | 3 | 0.841 | 0.833 | 0.849 | 0.000 | 3.328 |
| e | elasticsearch | default | nc10000 | 1468 | 3 | 0.881 | 0.874 | 0.888 | 0.000 | 4.804 |
| e | elasticsearch | default | nc2000 | 1468 | 3 | 0.873 | 0.866 | 0.880 | 0.000 | 4.171 |
| e | elasticsearch | default | nc50 | 1468 | 3 | 0.826 | 0.817 | 0.835 | 0.000 | 3.309 |
| e | elasticsearch | default | nc500 | 1468 | 3 | 0.867 | 0.860 | 0.874 | 0.000 | 3.531 |
| e | elasticsearch | int8 | default | 1468 | 3 | 0.888 | 0.876 | 0.899 | 0.000 | 3.391 |
| e | elasticsearch | int8 | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 21.8 |
| e | elasticsearch | int8 | nc100 | 1468 | 3 | 0.940 | 0.932 | 0.946 | 0.000 | 3.544 |
| e | elasticsearch | int8 | nc10000 | 1468 | 3 | 0.988 | 0.987 | 0.989 | 0.000 | 6.918 |
| e | elasticsearch | int8 | nc2000 | 1468 | 3 | 0.975 | 0.972 | 0.978 | 0.000 | 4.798 |
| e | elasticsearch | int8 | nc50 | 1468 | 3 | 0.919 | 0.910 | 0.928 | 0.000 | 3.448 |
| e | elasticsearch | int8 | nc500 | 1468 | 3 | 0.966 | 0.961 | 0.970 | 0.000 | 3.957 |
| e | faiss | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 276.8 |
| e | lancedb | default | default | 1468 | 3 | 0.439 | 0.423 | 0.456 | 0.000 | 8.777 |
| e | lancedb | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 141.1 |
| e | lancedb | default | np10 | 1468 | 3 | 0.432 | 0.416 | 0.450 | 0.016 | 7.358 |
| e | lancedb | default | np100 | 1468 | 3 | 0.439 | 0.423 | 0.456 | 0.000 | 8.807 |
| e | lancedb | default | np200 | 1468 | 3 | 0.439 | 0.423 | 0.456 | 0.000 | 8.799 |
| e | lancedb | default | np50 | 1468 | 3 | 0.439 | 0.423 | 0.456 | 0.000 | 8.941 |
| e | lancedb | default | np500 | 1468 | 3 | 0.439 | 0.423 | 0.456 | 0.000 | 8.763 |
| e | lancedb | default | postfilter | 1468 | 3 | 0.043 | 0.036 | 0.051 | 0.790 | 6.365 |
| e | lancedb | default | refine | 1468 | 3 | 0.896 | 0.884 | 0.909 | 0.000 | 10.9 |
| e | milvus | default | default | 1468 | 3 | 0.864 | 0.847 | 0.881 | 0.000 | 6.165 |
| e | milvus | default | ef100 | 1468 | 3 | 0.920 | 0.909 | 0.931 | 0.000 | 5.613 |
| e | milvus | default | ef256 | 1468 | 3 | 0.968 | 0.963 | 0.973 | 0.000 | 5.662 |
| e | milvus | default | ef32 | 1468 | 3 | 0.905 | 0.893 | 0.917 | 0.000 | 5.693 |
| e | milvus | default | ef512 | 1468 | 3 | 0.983 | 0.980 | 0.986 | 0.000 | 7.472 |
| e | milvus | default | ef64 | 1468 | 3 | 0.928 | 0.917 | 0.938 | 0.000 | 5.380 |
| e | mongodb | default | default | 1468 | 3 | 0.953 | 0.946 | 0.959 | 0.000 | 9.553 |
| e | mongodb | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 19.6 |
| e | mongodb | default | nc1000 | 1468 | 3 | 0.995 | 0.994 | 0.996 | 0.000 | 22.8 |
| e | mongodb | default | nc10000 | 1468 | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 53.3 |
| e | mongodb | default | nc20 | 1468 | 3 | 0.873 | 0.856 | 0.889 | 0.000 | 6.466 |
| e | mongodb | default | nc200 | 1468 | 3 | 0.972 | 0.968 | 0.976 | 0.000 | 11.7 |
| e | mongodb | default | nc50 | 1468 | 3 | 0.927 | 0.918 | 0.937 | 0.000 | 7.516 |
| e | opensearch | default | default | 1468 | 3 | 0.948 | 0.941 | 0.956 | 0.000 | 3.107 |
| e | opensearch | default | ef128 | 1468 | 3 | 0.954 | 0.948 | 0.961 | 0.000 | 2.899 |
| e | opensearch | default | ef256 | 1468 | 3 | 0.970 | 0.965 | 0.975 | 0.000 | 3.233 |
| e | opensearch | default | ef32 | 1468 | 3 | 0.914 | 0.903 | 0.925 | 0.000 | 2.707 |
| e | opensearch | default | ef512 | 1468 | 3 | 0.982 | 0.979 | 0.985 | 0.000 | 3.587 |
| e | opensearch | default | ef64 | 1468 | 3 | 0.938 | 0.929 | 0.946 | 0.000 | 2.743 |
| e | opensearch | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 54.2 |
| e | pgvector | default | default | 1468 | 3 | 0.112 | 0.098 | 0.128 | 0.616 | 2.140 |
| e | pgvector | default | ef100 | 1468 | 3 | 0.661 | 0.629 | 0.693 | 0.097 | 17.5 |
| e | pgvector | default | ef1000 | 1468 | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 169.7 |
| e | pgvector | default | ef200 | 1468 | 3 | 0.670 | 0.638 | 0.702 | 0.097 | 17.9 |
| e | pgvector | default | ef40 | 1468 | 3 | 0.641 | 0.611 | 0.671 | 0.097 | 17.0 |
| e | pgvector | default | ef400 | 1468 | 3 | 0.754 | 0.725 | 0.781 | 0.037 | 13.2 |
| e | pgvector | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 162.6 |
| e | pgvector | default | scan1m | 1468 | 3 | 0.787 | 0.766 | 0.807 | 0.000 | 18.0 |
| e | pgvector | default | strict | 1468 | 3 | 0.504 | 0.477 | 0.531 | 0.097 | 19.2 |
| e | qdrant | as-run | acorn | 1468 | 3 | 0.830 | 0.809 | 0.850 | 0.000 | 4.995 |
| e | qdrant | as-run | acorn-max | 1468 | 3 | 0.953 | 0.946 | 0.960 | 0.000 | 8.962 |
| e | qdrant | as-run | default | 1468 | 3 | 0.641 | 0.600 | 0.680 | 0.000 | 4.782 |
| e | qdrant | as-run | ef1024 | 1468 | 3 | 0.864 | 0.844 | 0.883 | 0.000 | 10.3 |
| e | qdrant | as-run | ef128 | 1468 | 3 | 0.663 | 0.624 | 0.700 | 0.000 | 4.893 |
| e | qdrant | as-run | ef256 | 1468 | 3 | 0.727 | 0.693 | 0.758 | 0.000 | 5.884 |
| e | qdrant | as-run | ef512 | 1468 | 3 | 0.794 | 0.767 | 0.819 | 0.000 | 7.461 |
| e | qdrant | as-run | ef64 | 1468 | 3 | 0.604 | 0.560 | 0.646 | 0.000 | 4.208 |
| e | qdrant | as-run | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 25.5 |
| e | qdrant | tenant | acorn-max | 1468 | 3 | 0.983 | 0.979 | 0.987 | 0.000 | 8.603 |
| e | qdrant | tenant | ef128 | 1468 | 3 | 0.941 | 0.931 | 0.951 | 0.000 | 4.672 |
| e | qdrant | tenant | ef512 | 1468 | 3 | 0.983 | 0.979 | 0.987 | 0.000 | 8.846 |
| e | qdrant | tenant | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 21.5 |
| e | redis | default | batches | 1468 | 3 | 0.865 | 0.849 | 0.881 | 0.000 | 4.648 |
| e | redis | default | default | 1468 | 3 | 0.987 | 0.984 | 0.991 | 0.000 | 19.0 |
| e | redis | default | ef100 | 1468 | 3 | 0.991 | 0.987 | 0.993 | 0.000 | 18.8 |
| e | redis | default | ef1000 | 1468 | 3 | 0.995 | 0.992 | 0.997 | 0.000 | 4.682 |
| e | redis | default | ef200 | 1468 | 3 | 0.994 | 0.991 | 0.997 | 0.000 | 2.694 |
| e | redis | default | ef50 | 1468 | 3 | 0.990 | 0.987 | 0.993 | 0.000 | 18.9 |
| e | redis | default | ef500 | 1468 | 3 | 0.993 | 0.990 | 0.996 | 0.000 | 3.409 |
| e | redis | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 19.9 |
| e | weaviate | default | default | 1468 | 3 | 0.923 | 0.913 | 0.933 | 0.000 | 4.074 |
| e | weaviate | default | ef1024 | 1468 | 3 | 0.991 | 0.990 | 0.993 | 0.000 | 15.6 |
| e | weaviate | default | ef128 | 1468 | 3 | 0.934 | 0.925 | 0.943 | 0.000 | 4.263 |
| e | weaviate | default | ef256 | 1468 | 3 | 0.963 | 0.958 | 0.968 | 0.000 | 6.475 |
| e | weaviate | default | ef512 | 1468 | 3 | 0.979 | 0.976 | 0.982 | 0.000 | 10.3 |
| e | weaviate | default | ef64 | 1468 | 3 | 0.892 | 0.878 | 0.906 | 0.000 | 3.557 |
| e | weaviate | default | exact | 1468 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 20.0 |
| e | weaviate | default | noflat | 1468 | 3 | 0.837 | 0.806 | 0.865 | 0.000 | 3.888 |
| e | weaviate | default | sweeping | 1468 | 3 | 0.923 | 0.913 | 0.933 | 0.000 | 3.901 |
| m | elasticsearch | default | default | 6200 | 3 | 0.806 | 0.803 | 0.810 | 0.000 | 4.548 |
| m | elasticsearch | default | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 6.796 |
| m | elasticsearch | default | nc100 | 6200 | 3 | 0.833 | 0.829 | 0.836 | 0.000 | 4.184 |
| m | elasticsearch | default | nc10000 | 6200 | 3 | 0.878 | 0.875 | 0.881 | 0.000 | 6.033 |
| m | elasticsearch | default | nc2000 | 6200 | 3 | 0.873 | 0.870 | 0.876 | 0.000 | 5.562 |
| m | elasticsearch | default | nc50 | 6200 | 3 | 0.826 | 0.823 | 0.830 | 0.000 | 4.556 |
| m | elasticsearch | default | nc500 | 6200 | 3 | 0.862 | 0.859 | 0.865 | 0.000 | 4.782 |
| m | faiss | default | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 993.2 |
| m | lancedb | default | default | 6200 | 3 | 0.437 | 0.433 | 0.441 | 0.002 | 11.6 |
| m | lancedb | default | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 73.7 |
| m | lancedb | default | np10 | 6200 | 3 | 0.424 | 0.420 | 0.427 | 0.010 | 8.782 |
| m | lancedb | default | np100 | 6200 | 3 | 0.450 | 0.446 | 0.454 | 0.000 | 34.6 |
| m | lancedb | default | np200 | 6200 | 3 | 0.450 | 0.447 | 0.454 | 0.000 | 40.7 |
| m | lancedb | default | np50 | 6200 | 3 | 0.447 | 0.443 | 0.451 | 0.000 | 20.5 |
| m | lancedb | default | np500 | 6200 | 3 | 0.450 | 0.447 | 0.454 | 0.000 | 40.7 |
| m | lancedb | default | postfilter | 6200 | 3 | 0.175 | 0.172 | 0.178 | 0.534 | 6.833 |
| m | lancedb | default | refine | 6200 | 3 | 0.908 | 0.905 | 0.911 | 0.000 | 23.7 |
| m | milvus | default | default | 6200 | 3 | 0.972 | 0.971 | 0.973 | 0.000 | 12.7 |
| m | milvus | default | ef100 | 6200 | 3 | 0.994 | 0.993 | 0.995 | 0.000 | 5.274 |
| m | milvus | default | ef256 | 6200 | 3 | 0.998 | 0.998 | 0.998 | 0.000 | 5.898 |
| m | milvus | default | ef32 | 6200 | 3 | 0.982 | 0.980 | 0.983 | 0.000 | 11.8 |
| m | milvus | default | ef512 | 6200 | 3 | 0.999 | 0.999 | 0.999 | 0.000 | 6.543 |
| m | milvus | default | ef64 | 6200 | 3 | 0.989 | 0.989 | 0.990 | 0.000 | 5.203 |
| m | mongodb | default | default | 6200 | 3 | 0.996 | 0.995 | 0.996 | 0.000 | 20.5 |
| m | mongodb | default | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 31.3 |
| m | mongodb | default | nc1000 | 6200 | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 45.6 |
| m | mongodb | default | nc10000 | 6200 | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 48.5 |
| m | mongodb | default | nc20 | 6200 | 3 | 0.979 | 0.978 | 0.980 | 0.000 | 18.1 |
| m | mongodb | default | nc200 | 6200 | 3 | 0.998 | 0.998 | 0.998 | 0.000 | 24.5 |
| m | mongodb | default | nc50 | 6200 | 3 | 0.992 | 0.991 | 0.993 | 0.000 | 19.4 |
| m | opensearch | default | default | 6200 | 3 | 0.998 | 0.997 | 0.998 | 0.000 | 7.254 |
| m | opensearch | default | ef128 | 6200 | 3 | 0.998 | 0.997 | 0.998 | 0.000 | 7.075 |
| m | opensearch | default | ef256 | 6200 | 3 | 0.999 | 0.998 | 0.999 | 0.000 | 7.449 |
| m | opensearch | default | ef32 | 6200 | 3 | 0.995 | 0.994 | 0.996 | 0.000 | 5.963 |
| m | opensearch | default | ef512 | 6200 | 3 | 0.999 | 0.999 | 1.000 | 0.000 | 6.630 |
| m | opensearch | default | ef64 | 6200 | 3 | 0.997 | 0.996 | 0.998 | 0.000 | 6.715 |
| m | opensearch | default | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 16.0 |
| m | pgvector | default | default | 6200 | 3 | 0.575 | 0.570 | 0.581 | 0.324 | 5.564 |
| m | pgvector | default | ef100 | 6200 | 3 | 0.897 | 0.893 | 0.901 | 0.003 | 12.0 |
| m | pgvector | default | ef1000 | 6200 | 3 | 0.927 | 0.923 | 0.931 | 0.003 | 23.5 |
| m | pgvector | default | ef200 | 6200 | 3 | 0.907 | 0.902 | 0.911 | 0.003 | 13.4 |
| m | pgvector | default | ef40 | 6200 | 3 | 0.885 | 0.880 | 0.889 | 0.003 | 11.5 |
| m | pgvector | default | ef400 | 6200 | 3 | 0.917 | 0.913 | 0.921 | 0.003 | 15.7 |
| m | pgvector | default | exact | 998 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 636.0 |
| m | pgvector | default | scan1m | 6200 | 3 | 0.949 | 0.947 | 0.952 | 0.000 | 12.3 |
| m | pgvector | default | strict | 6200 | 3 | 0.878 | 0.874 | 0.883 | 0.003 | 11.9 |
| m | qdrant | as-run | acorn | 6200 | 3 | 0.983 | 0.982 | 0.984 | 0.000 | 13.6 |
| m | qdrant | as-run | acorn-max | 6200 | 3 | 0.997 | 0.997 | 0.998 | 0.000 | 32.3 |
| m | qdrant | as-run | default | 6200 | 3 | 0.799 | 0.796 | 0.803 | 0.000 | 5.126 |
| m | qdrant | as-run | ef1024 | 6200 | 3 | 0.898 | 0.896 | 0.901 | 0.000 | 12.3 |
| m | qdrant | as-run | ef128 | 6200 | 3 | 0.813 | 0.810 | 0.817 | 0.000 | 5.503 |
| m | qdrant | as-run | ef256 | 6200 | 3 | 0.849 | 0.846 | 0.852 | 0.000 | 6.725 |
| m | qdrant | as-run | ef512 | 6200 | 3 | 0.878 | 0.875 | 0.881 | 0.000 | 8.456 |
| m | qdrant | as-run | ef64 | 6200 | 3 | 0.771 | 0.767 | 0.774 | 0.000 | 4.506 |
| m | qdrant | as-run | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 16.0 |
| m | qdrant | tenant | acorn-max | 3000 | 3 | 0.919 | 0.916 | 0.922 | 0.000 | 8.812 |
| m | qdrant | tenant | ef128 | 3000 | 3 | 0.854 | 0.850 | 0.858 | 0.000 | 6.090 |
| m | qdrant | tenant | ef512 | 3000 | 3 | 0.919 | 0.916 | 0.922 | 0.000 | 9.068 |
| m | qdrant | tenant | exact | 3000 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 17.6 |
| m | redis | default | batches | 6200 | 3 | 0.960 | 0.959 | 0.962 | 0.000 | 7.759 |
| m | redis | default | default | 6200 | 3 | 0.971 | 0.969 | 0.973 | 0.000 | 4.132 |
| m | redis | default | ef100 | 6200 | 3 | 0.988 | 0.987 | 0.989 | 0.000 | 4.346 |
| m | redis | default | ef1000 | 6200 | 3 | 0.999 | 0.998 | 0.999 | 0.000 | 5.787 |
| m | redis | default | ef200 | 6200 | 3 | 0.993 | 0.992 | 0.994 | 0.000 | 4.528 |
| m | redis | default | ef50 | 6200 | 3 | 0.982 | 0.981 | 0.984 | 0.000 | 4.268 |
| m | redis | default | ef500 | 6200 | 3 | 0.997 | 0.997 | 0.998 | 0.000 | 5.051 |
| m | redis | default | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 17.8 |
| m | weaviate | default | default | 6200 | 3 | 0.968 | 0.966 | 0.969 | 0.000 | 6.845 |
| m | weaviate | default | ef1024 | 6200 | 3 | 0.994 | 0.994 | 0.995 | 0.000 | 10.9 |
| m | weaviate | default | ef128 | 6200 | 3 | 0.973 | 0.972 | 0.974 | 0.000 | 7.247 |
| m | weaviate | default | ef256 | 6200 | 3 | 0.985 | 0.984 | 0.986 | 0.000 | 8.779 |
| m | weaviate | default | ef512 | 6200 | 3 | 0.991 | 0.990 | 0.992 | 0.000 | 9.904 |
| m | weaviate | default | ef64 | 6200 | 3 | 0.955 | 0.954 | 0.957 | 0.000 | 6.389 |
| m | weaviate | default | exact | 6200 | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 12.6 |
| m | weaviate | default | noflat | 6200 | 3 | 0.812 | 0.808 | 0.815 | 0.000 | 6.535 |
| m | weaviate | default | sweeping | 6200 | 3 | 0.995 | 0.994 | 0.996 | 0.000 | 7.301 |

### X5 arms

| corpus | store | layout | arm | recall5 | recall10 | err10 | short10 | trigger10 | detection10 | false_complete10 | p50_ms | triggered_p95_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e | pgvector | default | count | 0.639 | 0.667 | 0.089 | 0.116 | 0.129 | 1.000 | 0.542 | 17.7 | 25.6 |
| e | pgvector | default | exact-10k | 0.747 | 0.782 | 0.000 | 0.000 | 0.129 | 1.000 | 0.480 | 17.3 | 30.3 |
| e | pgvector | default | exact-1k | 0.747 | 0.782 | 0.000 | 0.000 | 0.129 | 1.000 | 0.480 | 17.6 | 30.6 |
| e | pgvector | default | exact-inf | 0.747 | 0.782 | 0.000 | 0.000 | 0.129 | 1.000 | 0.480 | 17.2 | 40.2 |
| e | pgvector | default | monitor | 0.639 | 0.667 | 0.089 | 0.116 | 0.129 | 0.000 | 0.551 | 17.6 | 0.000 |
| e | pgvector | default | native-scan1m | 0.664 | 0.694 | 0.072 | 0.090 | 0.103 | 0.000 | 0.543 | 17.6 | 0.000 |
| e | pgvector | default | report | 0.639 | 0.667 | 0.089 | 0.116 | 0.129 | 0.000 | 0.551 | 17.3 | 0.000 |
| e | pgvector | default | widen | 0.739 | 0.775 | 0.000 | 0.000 | 0.129 | 1.000 | 0.498 | 17.9 | 360.9 |
| e | qdrant | as-run | count | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.573 | 4.600 | 1.842 |
| e | qdrant | as-run | exact-10k | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.573 | 4.588 | 1.797 |
| e | qdrant | as-run | exact-1k | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.573 | 4.604 | 1.719 |
| e | qdrant | as-run | exact-inf | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.573 | 4.601 | 1.757 |
| e | qdrant | as-run | monitor | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.581 | 4.715 | 0.000 |
| e | qdrant | as-run | native-acorn | 0.857 | 0.855 | 0.000 | 0.000 | 0.014 | n/a | 0.388 | 4.842 | 0.000 |
| e | qdrant | as-run | report | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.581 | 4.716 | 0.000 |
| e | qdrant | as-run | widen | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.573 | 4.595 | 1.695 |
| e | qdrant | tenant | native-tenant | 0.938 | 0.939 | 0.000 | 0.000 | 0.014 | n/a | 0.235 | 4.688 | 0.000 |
| m | pgvector | default | count | 0.896 | 0.900 | 0.003 | 0.017 | 0.017 | 1.000 | 0.301 | 9.832 | 87.7 |
| m | pgvector | default | exact-10k | 0.909 | 0.915 | 0.000 | 0.001 | 0.017 | 1.000 | 0.296 | 10.0 | 365.8 |
| m | pgvector | default | exact-1k | 0.900 | 0.904 | 0.001 | 0.012 | 0.017 | 1.000 | 0.299 | 9.819 | 129.2 |
| m | pgvector | default | exact-inf | 0.909 | 0.915 | 0.000 | 0.000 | 0.017 | 1.000 | 0.296 | 10.0 | 220.7 |
| m | pgvector | default | monitor | 0.896 | 0.900 | 0.003 | 0.017 | 0.017 | 0.000 | 0.301 | 10.2 | 0.000 |
| m | pgvector | default | native-scan1m | 0.899 | 0.903 | 0.003 | 0.016 | 0.016 | 0.000 | 0.299 | 10.0 | 0.000 |
| m | pgvector | default | report | 0.896 | 0.900 | 0.003 | 0.017 | 0.017 | 0.000 | 0.301 | 9.874 | 0.000 |
| m | pgvector | default | widen | 0.907 | 0.913 | 0.000 | 0.000 | 0.017 | 1.000 | 0.306 | 9.889 | 1572.7 |
| m | qdrant | as-run | count | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 1.000 | 0.356 | 6.022 | 28.2 |
| m | qdrant | as-run | exact-10k | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 1.000 | 0.356 | 5.953 | 27.9 |
| m | qdrant | as-run | exact-1k | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 1.000 | 0.356 | 5.804 | 28.3 |
| m | qdrant | as-run | exact-inf | 0.833 | 0.842 | 0.000 | 0.000 | 0.035 | 1.000 | 0.343 | 6.103 | 50.4 |
| m | qdrant | as-run | monitor | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 0.000 | 0.356 | 5.155 | 0.000 |
| m | qdrant | as-run | native-acorn | 0.987 | 0.986 | 0.000 | 0.000 | 0.000 | n/a | 0.085 | 15.9 | n/a |
| m | qdrant | as-run | report | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 0.000 | 0.356 | 6.074 | 0.000 |
| m | qdrant | as-run | widen | 0.833 | 0.841 | 0.000 | 0.000 | 0.035 | 1.000 | 0.349 | 5.559 | 148.5 |

### H2.1: inconclusive

- pgvector: G 0.4242 [0.4154, 0.4332], positive in 5 of 5 seeds: gap
- qdrant: G 0.0343 [0.0196, 0.0487], positive in 5 of 5 seeds: unclear
- elasticsearch: G 0.1371 [0.1242, 0.1500], positive in 5 of 5 seeds: gap
- opensearch: G -0.0014 [-0.0029, 0.0001], positive in 2 of 5 seeds: no gap
- weaviate: G 0.0549 [0.0478, 0.0618], positive in 5 of 5 seeds: gap
- redis: G -0.0794 [-0.0871, -0.0719], positive in 0 of 5 seeds: unclear
- milvus: G 0.0136 [0.0080, 0.0194], positive in 5 of 5 seeds: no gap
- mongodb: G -0.0037 [-0.0055, -0.0019], positive in 0 of 5 seeds: no gap
- lancedb: G 0.2535 [0.2423, 0.2649], positive in 5 of 5 seeds: gap
- stores with a gap: 4 (confirm at 6); with no gap: 3 (falsify at 5)

### H2.2: falsified

- pgvector: D 0.3650 [0.3321, 0.3989], 3578 pairs below 1: local
- qdrant: D -0.2032 [-0.2194, -0.1876], 2760 pairs below 1: global
- elasticsearch: D 0.2439 [0.2116, 0.2754], 4600 pairs below 1: local
- opensearch: D -0.0601 [-0.0793, -0.0411], 94 pairs below 1: not assessable
- weaviate: D -0.3900 [-0.4159, -0.3644], 1294 pairs below 1: global
- redis: D -0.0757 [-0.0870, -0.0647], 899 pairs below 1: global
- milvus: D -0.5307 [-0.5469, -0.5140], 1545 pairs below 1: global
- mongodb: D -0.0804 [-0.1016, -0.0593], 318 pairs below 1: global
- lancedb: D 0.5382 [0.5080, 0.5674], 6198 pairs below 1: local
- assessable 8, local 3, global 5

### H2.3: confirmed

- pgvector (ef1000): G 0.4242 -> 0.1721 [0.1611, 0.1830], narrowing [0.2383, 0.2661]
- elasticsearch (nc10000): G 0.1371 -> 0.1617 [0.1506, 0.1727], narrowing [-0.0342, -0.0147]
- weaviate (ef1024): G 0.0549 -> 0.0041 [0.0014, 0.0068], narrowing [0.0448, 0.0567]
- lancedb (np500): G 0.2535 -> 0.2523 [0.2411, 0.2636], narrowing [0.0002, 0.0022]
- stores with a gap and a sweep: 4; narrowed and remaining: 2; closed: 1

### H2.4: confirmed

- pgvector: V 0.9267 [0.8867, 0.9600], 5 seeds: U-shaped
- qdrant: V 0.5403 [0.5165, 0.5653], 5 seeds: U-shaped
- elasticsearch: V 0.2338 [0.2032, 0.2650], 5 seeds: U-shaped
- opensearch: V 0.0005 [0.0000, 0.0015], 1 seeds: neither
- weaviate: V 0.1780 [0.1578, 0.1980], 5 seeds: U-shaped
- redis: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- milvus: V 0.1037 [0.0925, 0.1150], 5 seeds: U-shaped
- mongodb: V 0.0012 [0.0005, 0.0020], 4 seeds: neither
- lancedb: V -0.0098 [-0.0332, 0.0212], 3 seeds: monotone
- U-shaped 5 (confirm at 5), monotone 2 (falsify at 5)

### H5.1: confirmed

- e pgvector: false alarms 0, detection 1.0000 of 992, exhausted without min(k, R) hits 0
- e qdrant: 0 truly short first searches (< 10): not judged
- m pgvector: false alarms 0, detection 1.0000 of 574, exhausted without min(k, R) hits 0
- m qdrant: false alarms 0, detection 1.0000 of 1091, exhausted without min(k, R) hits 0

### H5.2: confirmed

- pgvector e: report short 992; exact-inf empty or short 0; recall@10 on 576 triggered 1.0000
- pgvector m: report short 574; exact-inf empty or short 0; recall@10 on 323 triggered 1.0000
- qdrant e: report has 0 short results (< 10) or no exact-inf: not judged
- qdrant m: report short 1091; exact-inf empty or short 0; recall@10 on 644 triggered 1.0000

### H5.3: inconclusive

- e pgvector b0 count: median latency ratio on 1300 untriggered pairs 1.0038
- e pgvector b0 exact-1k: median latency ratio on 1300 untriggered pairs 1.0010
- e pgvector b0 exact-10k: median latency ratio on 1300 untriggered pairs 0.9852
- e pgvector b0 exact-inf: median latency ratio on 1300 untriggered pairs 1.0190
- e pgvector b0 widen: median latency ratio on 1300 untriggered pairs 1.0103
- e pgvector b1 count: median latency ratio on 1293 untriggered pairs 1.0188
- e pgvector b1 exact-1k: median latency ratio on 1293 untriggered pairs 1.0281
- e pgvector b1 exact-10k: median latency ratio on 1293 untriggered pairs 0.9980
- e pgvector b1 exact-inf: median latency ratio on 1293 untriggered pairs 1.0052
- e pgvector b1 widen: median latency ratio on 1293 untriggered pairs 1.0493
- e pgvector b2 count: median latency ratio on 1298 untriggered pairs 1.0153
- e pgvector b2 exact-1k: median latency ratio on 1298 untriggered pairs 1.0068
- e pgvector b2 exact-10k: median latency ratio on 1298 untriggered pairs 0.9773
- e pgvector b2 exact-inf: median latency ratio on 1298 untriggered pairs 0.9427
- e pgvector b2 widen: median latency ratio on 1298 untriggered pairs 0.9876
- e qdrant b0 count: median latency ratio on 1468 untriggered pairs 0.9932
- e qdrant b0 exact-1k: median latency ratio on 1468 untriggered pairs 0.9992
- e qdrant b0 exact-10k: median latency ratio on 1468 untriggered pairs 1.0005
- e qdrant b0 exact-inf: median latency ratio on 1468 untriggered pairs 0.9982
- e qdrant b0 widen: median latency ratio on 1468 untriggered pairs 0.9971
- e qdrant b1 count: median latency ratio on 1468 untriggered pairs 0.9758
- e qdrant b1 exact-1k: median latency ratio on 1468 untriggered pairs 0.9750
- e qdrant b1 exact-10k: median latency ratio on 1468 untriggered pairs 0.9638
- e qdrant b1 exact-inf: median latency ratio on 1468 untriggered pairs 0.9699
- e qdrant b1 widen: median latency ratio on 1468 untriggered pairs 0.9673
- e qdrant b2 count: median latency ratio on 1468 untriggered pairs 0.9509
- e qdrant b2 exact-1k: median latency ratio on 1468 untriggered pairs 0.9433
- e qdrant b2 exact-10k: median latency ratio on 1468 untriggered pairs 0.9443
- e qdrant b2 exact-inf: median latency ratio on 1468 untriggered pairs 0.9446
- e qdrant b2 widen: median latency ratio on 1468 untriggered pairs 0.9480
- m pgvector b0 count: median latency ratio on 6097 untriggered pairs 0.9991
- m pgvector b0 exact-1k: median latency ratio on 6097 untriggered pairs 1.0014
- m pgvector b0 exact-10k: median latency ratio on 6097 untriggered pairs 1.0060
- m pgvector b0 exact-inf: median latency ratio on 6097 untriggered pairs 1.0071
- m pgvector b0 widen: median latency ratio on 6097 untriggered pairs 1.0080
- m pgvector b1 count: median latency ratio on 6072 untriggered pairs 1.0002
- m pgvector b1 exact-1k: median latency ratio on 6072 untriggered pairs 1.0003
- m pgvector b1 exact-10k: median latency ratio on 6072 untriggered pairs 1.0076
- m pgvector b1 exact-inf: median latency ratio on 6072 untriggered pairs 1.0133
- m pgvector b1 widen: median latency ratio on 6072 untriggered pairs 1.0111
- m pgvector b2 count: median latency ratio on 6108 untriggered pairs 0.9678
- m pgvector b2 exact-1k: median latency ratio on 6108 untriggered pairs 0.9663
- m pgvector b2 exact-10k: median latency ratio on 6108 untriggered pairs 1.0269
- m pgvector b2 exact-inf: median latency ratio on 6108 untriggered pairs 0.9663
- m pgvector b2 widen: median latency ratio on 6108 untriggered pairs 0.9184
- m qdrant b0 count: median latency ratio on 5870 untriggered pairs 0.9521
- m qdrant b0 exact-1k: median latency ratio on 5870 untriggered pairs 0.8795
- m qdrant b0 exact-10k: median latency ratio on 5870 untriggered pairs 0.9238
- m qdrant b0 exact-inf: median latency ratio on 5870 untriggered pairs 0.9746
- m qdrant b0 widen: median latency ratio on 5870 untriggered pairs 0.8662
- m qdrant b1 count: median latency ratio on 5907 untriggered pairs 0.9438
- m qdrant b1 exact-1k: median latency ratio on 5907 untriggered pairs 0.9464
- m qdrant b1 exact-10k: median latency ratio on 5907 untriggered pairs 0.9324
- m qdrant b1 exact-inf: median latency ratio on 5907 untriggered pairs 0.9478
- m qdrant b1 widen: median latency ratio on 5907 untriggered pairs 0.8700
- m qdrant b2 count: median latency ratio on 6179 untriggered pairs 0.9960
- m qdrant b2 exact-1k: median latency ratio on 6179 untriggered pairs 1.0033
- m qdrant b2 exact-10k: median latency ratio on 6179 untriggered pairs 1.0542
- m qdrant b2 exact-inf: median latency ratio on 6179 untriggered pairs 1.0039
- m qdrant b2 widen: median latency ratio on 6179 untriggered pairs 0.9882

### H5.4: confirmed

- report: false-completeness 0.5808 (confirm needs >= 0.20)
- count: 0.5726, minus report -0.0082 [-0.0270, 0.0000]
- exact-1k: 0.5726, minus report -0.0082 [-0.0270, 0.0000]
- exact-10k: 0.5726, minus report -0.0082 [-0.0270, 0.0000]
- exact-inf: 0.5726, minus report -0.0082 [-0.0270, 0.0000]
- widen: 0.5726, minus report -0.0082 [-0.0270, 0.0000]

### H5.5: confirmed

- (a) x5-e-pgvector default b0: 52 of 5956 sampled: inside the 99.9% interval
- (a) x5-e-pgvector default b1: 56 of 5956 sampled: inside the 99.9% interval
- (a) x5-e-pgvector default b2: 55 of 5956 sampled: inside the 99.9% interval
- (a) x5-e-qdrant as-run b0: 48 of 5956 sampled: inside the 99.9% interval
- (a) x5-e-qdrant as-run b1: 65 of 5956 sampled: inside the 99.9% interval
- (a) x5-e-qdrant as-run b2: 53 of 5956 sampled: inside the 99.9% interval
- (a) x5-m-pgvector-b0 default b0: 255 of 24800 sampled: inside the 99.9% interval
- (a) x5-m-pgvector-b1 default b1: 239 of 24800 sampled: inside the 99.9% interval
- (a) x5-m-pgvector-b2 default b2: 219 of 24800 sampled: inside the 99.9% interval
- (a) x5-m-qdrant-b0 as-run b0: 210 of 24800 sampled: inside the 99.9% interval
- (a) x5-m-qdrant-b1 as-run b1: 267 of 24800 sampled: inside the 99.9% interval
- (a) x5-m-qdrant-b2 as-run b2: 248 of 24800 sampled: inside the 99.9% interval
- (b) agreement within 0.1 on 1767 sampled retrievals: 1.0000
- (c) Qdrant e: mean sampled 0.6843 on 166, population 0.6541, difference 0.0302
- (c) Qdrant m: mean sampled 0.8116 on 725, population 0.8074, difference 0.0042

### H5.6: confirmed

- exact-inf minus widen on 421 triggered pairs: 0.0849 [0.0640, 0.1096], Wilcoxon p 5.582e-30

### H5.7: confirmed

- per-tenant layout recall@10 0.9386; best library arm 0.6535

