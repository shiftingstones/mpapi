FROM docker.io/python:3.14.7-trixie

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY uv.lock .
COPY pyproject.toml .
RUN uv sync --frozen --no-install-project

COPY src/* .

EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
