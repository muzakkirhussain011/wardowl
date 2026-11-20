FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928 AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

# uv only exports the lock: pip installs every dependency, and the build backend, by hash.
FROM ghcr.io/astral-sh/uv:0.13.9@sha256:d3b601f0c7b118bc1753febf7c41cc80981df678445e0254284eecf84db79a7d AS uv

FROM base AS build
COPY --from=uv /uv /bin/uv
COPY pyproject.toml uv.lock README.md ./
COPY rampart ./rampart
RUN uv export --frozen --no-emit-project -o requirements.txt \
 && uv export --frozen --no-emit-project --only-group build -o build.txt \
 && pip install --require-hashes --no-deps -r build.txt \
 && pip wheel --wheel-dir /wheels --require-hashes --no-deps -r requirements.txt \
 && pip wheel --wheel-dir /wheels --no-deps --no-build-isolation .

FROM base AS runtime
RUN useradd --create-home --uid 10001 rampart
COPY --from=build /wheels /wheels
RUN pip install --no-index --no-deps /wheels/*.whl && rm -rf /wheels
# No principals file: API keys and who holds them are mounted at run time (docker-compose.yml),
# never baked into an image.
COPY samples ./samples
USER rampart
# 8080 is the API; 9464 serves Prometheus metrics, for the internal network only.
EXPOSE 8080 9464
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')"
CMD ["rampart", "serve", "--host", "0.0.0.0", "--port", "8080", "--metrics-host", "0.0.0.0"]

FROM base AS test
COPY --from=uv /uv /bin/uv
COPY pyproject.toml uv.lock README.md ./
COPY rampart ./rampart
RUN uv export --frozen --no-emit-project --extra dev --group build -o requirements-dev.txt \
 && pip install --require-hashes --no-deps -r requirements-dev.txt \
 && pip install --no-deps --no-build-isolation -e .
COPY . .
CMD ["pytest", "-q"]
