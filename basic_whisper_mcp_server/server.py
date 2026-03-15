import base64
import logging
import tempfile

from fastmcp import FastMCP

from basic_whisper_mcp_server.models import get_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("basic-whisper-mcp-server")


@mcp.tool()
def health_check() -> str:
    """Basic server health check."""
    return "ok"


@mcp.tool()
def transcribe(audio_b64: str, model: str = "base", suffix: str = ".mp3") -> str:
    """Transcribe a base64-encoded audio file using Whisper.

    Args:
        audio_b64: Base64-encoded audio file content
        model: Whisper model to use: tiny, base, small, medium, large (default: base)
        suffix: File extension hint for the audio format, e.g. .mp3, .wav, .m4a (default: .mp3)
    """
    audio_bytes = base64.b64decode(audio_b64)
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        logger.info("Transcribing %s bytes via model '%s'", len(audio_bytes), model)
        return get_model(model).transcribe(tmp.name)["text"]
