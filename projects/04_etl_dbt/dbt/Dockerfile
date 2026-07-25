FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install --yes --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    dbt-core==1.9.0 \
    dbt-postgres==1.9.0
WORKDIR /app
