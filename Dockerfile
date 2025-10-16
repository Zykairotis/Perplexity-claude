FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY requirements.txt .

# Create non-root user
RUN useradd -r -m webhook-mcp && chown -R webhook-mcp:webhook-mcp /app
USER webhook-mcp


# Default command - run modular MCP server
CMD ["python", "-m", "src.perplexity_mcp_server.server"]
