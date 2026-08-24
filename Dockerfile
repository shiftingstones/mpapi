FROM docker.io/python:3.14.7-trixie AS dev
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY uv.lock .
COPY pyproject.toml .
RUN uv sync --frozen --no-install-project
COPY mpapi ./mpapi
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "--no-access-log", "mpapi.app:app"]

FROM dev AS test
COPY tests ./tests
CMD ["uv", "run", "pytest"]
