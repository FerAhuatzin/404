FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /api

# Install the application dependencies.
WORKDIR /api
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/api/.venv/bin/uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]