import logging

from mcp.server.fastmcp import FastMCP

from basic_whisper_mcp_server.models import get_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

mcp = FastMCP("basic-whisper-mcp-server")


@mcp.tool()
def health_check() -> str:
    """Basic server health check."""
    return "ok"


@mcp.tool()
def transcribe(audio_path: str, model: str = "base") -> str:
    """Transcribe an audio file using Whisper. Returns the transcribed text.

    Args:
        audio_path: Absolute path to the audio file (mp3, wav, m4a, etc.)
        model: Whisper model to use: tiny, base, small, medium, large (default: base)
    """
    return get_model(model).transcribe(audio_path)["text"]
