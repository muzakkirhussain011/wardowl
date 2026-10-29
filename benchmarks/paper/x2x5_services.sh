#!/usr/bin/env bash
# Starts, waits for and logs the store of one X2/X5 job, on a GitHub Actions runner.
#
#   bash benchmarks/paper/x2x5_services.sh start pgvector
#   bash benchmarks/paper/x2x5_services.sh wait pgvector
#   bash benchmarks/paper/x2x5_services.sh logs out/logs
#
# Images and versions are those of the conformance campaign (paper-conformance.yml); memory is
# raised for a million chunks. LanceDB, Chroma and FAISS are embedded and start nothing.
set -euo pipefail

action=${1:?start, wait or logs}
store=${2:-}

ready() {
  local name=$1 tries=$2; shift 2
  for _ in $(seq 1 "$tries"); do
    if "$@" > /dev/null 2>&1; then echo "$name is ready"; return 0; fi
    sleep 2
  done
  echo "::error::$name did not answer"
  docker logs --tail 80 "$name" || true
  return 1
}

start() {
  case "$store" in
    pgvector)
      # Only shared_buffers and maintenance_work_mem differ from PostgreSQL's defaults (PREREG
      # section 4); the shared memory segment is for parallel index builds.
      docker run -d --name postgres --shm-size=1g -p 5432:5432 -e POSTGRES_USER=bench -e POSTGRES_PASSWORD=bench \
        -e POSTGRES_DB=bench pgvector/pgvector:pg17 -c shared_buffers=3GB -c maintenance_work_mem=2GB
      ;;
    qdrant)
      docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant:v1.19.2
      ;;
    elasticsearch)
      sudo sysctl -w vm.max_map_count=262144
      docker run -d --name elasticsearch -p 9200:9200 -e discovery.type=single-node \
        -e xpack.security.enabled=false -e ES_JAVA_OPTS="-Xms2g -Xmx2g" \
        docker.elastic.co/elasticsearch/elasticsearch:9.5.5
      ;;
    opensearch)
      sudo sysctl -w vm.max_map_count=262144
      docker run -d --name opensearch -p 9200:9200 -e discovery.type=single-node \
        -e DISABLE_SECURITY_PLUGIN=true -e DISABLE_INSTALL_DEMO_CONFIG=true \
        -e OPENSEARCH_JAVA_OPTS="-Xms2g -Xmx2g" opensearchproject/opensearch:3.9.0
      ;;
    weaviate)
      docker run -d --name weaviate -p 8079:8080 -p 50051:50051 -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
        -e PERSISTENCE_DATA_PATH=/var/lib/weaviate -e DEFAULT_VECTORIZER_MODULE=none -e CLUSTER_HOSTNAME=node1 \
        cr.weaviate.io/semitechnologies/weaviate:1.39.12
      ;;
    redis)
      docker run -d --name redis -p 6379:6379 redis:8.10.2-alpine
      ;;
    milvus)
      mkdir -p "$RUNNER_TEMP/milvus"
      printf '%s\n' 'listen-client-urls: http://0.0.0.0:2379' 'advertise-client-urls: http://0.0.0.0:2379' \
        'quota-backend-bytes: 4294967296' 'auto-compaction-mode: revision' "auto-compaction-retention: '1000'" \
        > "$RUNNER_TEMP/milvus/embedEtcd.yaml"
      touch "$RUNNER_TEMP/milvus/user.yaml"
      docker run -d --name milvus --security-opt seccomp:unconfined -p 19530:19530 -p 9091:9091 \
        -e ETCD_USE_EMBED=true -e ETCD_DATA_DIR=/var/lib/milvus/etcd \
        -e ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml -e COMMON_STORAGETYPE=local -e DEPLOY_MODE=STANDALONE \
        -v "$RUNNER_TEMP/milvus/embedEtcd.yaml:/milvus/configs/embedEtcd.yaml" \
        -v "$RUNNER_TEMP/milvus/user.yaml:/milvus/configs/user.yaml" \
        milvusdb/milvus:v3.0.2 milvus run standalone
      ;;
    mongodb)
      docker run -d --name mongodb -p 27017:27017 mongodb/mongodb-atlas-local:8.0.30
      ;;
    lancedb | chroma | faiss)
      echo "$store is embedded: nothing to start"
      ;;
    *)
      echo "::error::unknown store $store"; exit 2
      ;;
  esac
}

wait_for() {
  case "$store" in
    pgvector) ready postgres 120 docker exec postgres pg_isready -U bench -h 127.0.0.1 ;;
    qdrant) ready qdrant 90 curl -sf http://127.0.0.1:6333/readyz ;;
    elasticsearch | opensearch)
      ready "$store" 150 curl -sf "http://127.0.0.1:9200/_cluster/health?wait_for_status=yellow&timeout=2s"
      ;;
    weaviate) ready weaviate 90 curl -sf http://127.0.0.1:8079/v1/.well-known/ready ;;
    redis)
      ready redis 60 docker exec redis redis-cli ping
      # No snapshots while a store of several gigabytes is loaded and searched (a fork would copy it).
      docker exec redis redis-cli CONFIG SET save "" || true
      docker exec redis redis-cli CONFIG SET appendonly no || true
      docker exec redis redis-cli MODULE LIST || true
      ;;
    milvus) ready milvus 150 curl -sf http://127.0.0.1:9091/healthz ;;
    mongodb)
      healthy() { [ "$(docker inspect -f '{{.State.Health.Status}}' mongodb)" = healthy ]; }
      ready mongodb 150 healthy
      ;;
    lancedb | chroma | faiss) : ;;
    *) echo "::error::unknown store $store"; exit 2 ;;
  esac
}

logs() {
  local folder=${store:-logs}
  mkdir -p "$folder"
  for name in $(docker ps -a --format '{{.Names}}'); do
    docker logs --tail 400 "$name" > "$folder/$name.log" 2>&1 || true
  done
  docker stats --no-stream > "$folder/docker-stats.txt" 2>&1 || true
  free -m > "$folder/memory.txt" 2>&1 || true
  df -h > "$folder/disk.txt" 2>&1 || true
}

case "$action" in
  start) start ;;
  wait) wait_for ;;
  logs) logs ;;
  *) echo "unknown action $action"; exit 2 ;;
esac
