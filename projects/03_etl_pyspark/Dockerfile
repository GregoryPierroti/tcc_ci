FROM ghcr.io/astral-sh/uv:0.10.7 AS uv
FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jdk-headless curl procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

WORKDIR /app

COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --frozen --no-install-project

ENV PATH="/opt/venv/bin:${PATH}"

RUN mkdir -p /opt/spark/jars \
    && curl --fail --location --silent --show-error \
      --output /opt/spark/jars/postgresql-42.7.3.jar \
      https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

COPY src/ /app/src/

WORKDIR /app/src
CMD ["python", "main.py"]
