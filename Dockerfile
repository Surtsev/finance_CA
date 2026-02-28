FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv venv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN uv sync --no-dev

COPY src/ ./src/

RUN uv pip install --no-deps -e .

CMD ["uv", "run", "src/main.py"]
