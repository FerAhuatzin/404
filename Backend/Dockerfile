FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /api

# Copy only the dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies with cache
ENV UV_HTTP_TIMEOUT=50
ENV UV_CACHE_DIR=/root/.cache/uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy the rest of the application
COPY . .

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Run the application
CMD ["/api/.venv/bin/uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]