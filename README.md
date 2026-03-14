# basic-whisper-mcp-server

MCP server for audio transcription using [OpenAI Whisper](https://github.com/openai/whisper).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- `ffmpeg` (`apt install ffmpeg` / `brew install ffmpeg`)

## Install

```bash
uv sync
```

## Run

### stdio (for local agents)

```bash
uv run python -m basic_whisper_mcp_server --transport stdio
```

### HTTP

```bash
uv run python -m basic_whisper_mcp_server --transport streamable-http --host 0.0.0.0 --port 8000
```

### Help

```bash
uv run python -m basic_whisper_mcp_server --help
```

## Docker

```bash
docker build -t basic-whisper-mcp-server .

# HTTP mode (default in Docker)
docker run -p 8000:8000 -v /path/to/audio:/audio basic-whisper-mcp-server

# Override transport or port
docker run -p 9000:9000 -e MCP_PORT=9000 -v /path/to/audio:/audio basic-whisper-mcp-server
```

## Configuration

| Env var | Default | Description |
|---|---|---|
| `MCP_TRANSPORT` | `streamable-http` | `stdio` or `streamable-http` (Docker default) |
| `MCP_HOST` | `0.0.0.0` | Host for HTTP mode |
| `MCP_PORT` | `8000` | Port for HTTP mode |
| `WHISPER_MODEL` | `base` | Default Whisper model |

## Claude Desktop config (stdio)

```json
{
  "mcpServers": {
    "whisper": {
      "command": "uv",
      "args": ["--directory", "/path/to/basic-whisper-mcp-server", "run", "python", "-m", "basic_whisper_mcp_server", "--transport", "stdio"]
    }
  }
}
```

## Tools

### `health_check`
Basic server health check. Returns `"ok"`.

### `transcribe`

| Param | Type | Default | Description |
|---|---|---|---|
| `audio_path` | string | — | Absolute path to audio file (mp3, wav, m4a, …) |
| `model` | string | `base` | `tiny`, `base`, `small`, `medium`, `large` |

Models are cached in memory after first load. Larger models are more accurate but slower.

## Testing with MCP Inspector

[MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a visual tool to explore and test MCP servers interactively.

### stdio

```bash
npx @modelcontextprotocol/inspector uv run python -m basic_whisper_mcp_server --transport stdio
```

### HTTP

Start the server first:

```bash
uv run python -m basic_whisper_mcp_server --transport streamable-http --port 8000
```

Then open the inspector and connect to:

```
http://localhost:8000/mcp
```

Or launch it directly:

```bash
npx @modelcontextprotocol/inspector
```

In the UI, set transport to **Streamable HTTP** and URL to `http://localhost:8000/mcp`.

## Project structure

```
basic_whisper_mcp_server/
├── __main__.py   # CLI entrypoint (--transport, --host, --port)
├── server.py     # MCP tools
└── models.py     # Whisper model loader with CUDA fallback
```
