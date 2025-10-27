# Dockerfile
FROM python:3.12-slim

# System deps for building wheels faster and SSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Use pip here for simplicity; uv also works but pip is fine for Render
RUN pip install --no-cache-dir --upgrade pip

# Copy project files
WORKDIR /app
COPY . /app

# Install dependencies:
# - mcp[cli]: official MCP Python SDK w/ HTTP transport support
# - uvicorn: tiny production ASGI server
# - install this project so "yfmcp" package is importable
RUN pip install --no-cache-dir "mcp[cli]" uvicorn && \
    pip install --no-cache-dir -e .

# Render provides PORT; default is 10000 if not set.
# You don't need to EXPOSE here for Render to work, but it's harmless.
ENV PORT=10000

# Start the HTTP server (listening on 0.0.0.0 so Render can reach it)
CMD ["uvicorn", "app_http:app", "--host", "0.0.0.0", "--port", "10000"]
