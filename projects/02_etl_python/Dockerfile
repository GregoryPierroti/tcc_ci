FROM ghcr.io/astral-sh/uv:0.10.7 AS uv
FROM python:3.11-slim

WORKDIR /app

COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --frozen --no-install-project

ENV PATH="/opt/venv/bin:${PATH}"

CMD ["python", "main.py"]
