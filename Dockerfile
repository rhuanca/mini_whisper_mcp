FROM python:3.11-slim

# ffmpeg is required by whisper
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml README.md ./
COPY mini_whisper_mcp ./mini_whisper_mcp

RUN uv pip install --system --no-cache -e .

EXPOSE 8000

ENV MCP_TRANSPORT="streamable-http"
ENV MCP_HOST="0.0.0.0"
ENV MCP_PORT="8000"

CMD ["sh", "-c", "python -m mini_whisper_mcp --transport ${MCP_TRANSPORT} --host ${MCP_HOST} --port ${MCP_PORT}"]
