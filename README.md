# mini-whisper-mcp

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
uv run python -m mini_whisper_mcp --transport stdio
```

### HTTP

```bash
uv run python -m mini_whisper_mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker build -t mini-whisper-mcp .
docker run -p 8000:8000 mini-whisper-mcp
```

## Configuration

| Env var | Default | Description |
|---|---|---|
| `MCP_TRANSPORT` | `streamable-http` | `stdio` or `streamable-http` (Docker default) |
| `MCP_HOST` | `0.0.0.0` | Host for HTTP mode |
| `MCP_PORT` | `8000` | Port for HTTP mode |

## MCP Tools

### `health_check`
Basic server health check. Returns `"ok"`.

### `transcribe`

| Param | Type | Default | Description |
|---|---|---|---|
| `audio_b64` | string | — | Base64-encoded audio file content |
| `model` | string | `base` | `tiny`, `base`, `small`, `medium`, `large` |
| `suffix` | string | `.mp3` | File extension hint: `.mp3`, `.wav`, `.m4a`, etc. |

Models are cached in memory after first load. Larger models are more accurate but slower.

### Usage example (calling agent)

```python
import base64

with open("audio.mp3", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

result = await mcp_client.call_tool("transcribe", {
    "audio_b64": audio_b64,
    "model": "base",
    "suffix": ".mp3",
})
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run python -m mini_whisper_mcp --transport stdio
```

For HTTP, start the server first then connect Inspector to `http://localhost:8000/mcp`.

## Claude Desktop config (stdio)

```json
{
  "mcpServers": {
    "whisper": {
      "command": "uv",
      "args": ["--directory", "/path/to/mini-whisper-mcp", "run", "python", "-m", "mini_whisper_mcp", "--transport", "stdio"]
    }
  }
}
```

## Project structure

```
mini_whisper_mcp/
├── __main__.py   # CLI entrypoint (--transport, --host, --port)
├── server.py     # MCP tools
└── models.py     # Whisper model loader with CUDA fallback
```
