import base64
import logging
import tempfile

import whisper
from fastmcp import FastMCP

from mini_whisper_mcp.models import get_model, loaded_models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

import os

STATELESS = os.getenv("MCP_STATELESS", "false").lower() == "true"
mcp = FastMCP("mini-whisper-mcp", stateless_http=STATELESS)

# Model metadata: (parameters, relative speed, multilingual)
_MODEL_INFO: dict[str, dict] = {
    "tiny":           {"params": "39M",  "speed": "~32x", "multilingual": False, "english_only": "tiny.en"},
    "tiny.en":        {"params": "39M",  "speed": "~32x", "multilingual": False, "english_only": True},
    "base":           {"params": "74M",  "speed": "~16x", "multilingual": True,  "english_only": "base.en"},
    "base.en":        {"params": "74M",  "speed": "~16x", "multilingual": False, "english_only": True},
    "small":          {"params": "244M", "speed": "~6x",  "multilingual": True,  "english_only": "small.en"},
    "small.en":       {"params": "244M", "speed": "~6x",  "multilingual": False, "english_only": True},
    "medium":         {"params": "769M", "speed": "~2x",  "multilingual": True,  "english_only": "medium.en"},
    "medium.en":      {"params": "769M", "speed": "~2x",  "multilingual": False, "english_only": True},
    "large-v1":       {"params": "1550M","speed": "1x",   "multilingual": True,  "english_only": False},
    "large-v2":       {"params": "1550M","speed": "1x",   "multilingual": True,  "english_only": False},
    "large-v3":       {"params": "1550M","speed": "1x",   "multilingual": True,  "english_only": False},
    "large":          {"params": "1550M","speed": "1x",   "multilingual": True,  "english_only": False},
    "large-v3-turbo": {"params": "809M", "speed": "~8x",  "multilingual": True,  "english_only": False},
    "turbo":          {"params": "809M", "speed": "~8x",  "multilingual": True,  "english_only": False},
}


# ── Resources ──────────────────────────────────────────────────────────────────

@mcp.resource("whisper://models")
def list_models() -> str:
    """List all available Whisper models with size and speed info."""
    lines = ["model            params   speed    multilingual"]
    lines.append("-" * 48)
    for name in whisper.available_models():
        info = _MODEL_INFO.get(name, {})
        lines.append(
            f"{name:<16}  {info.get('params','?'):<8} {info.get('speed','?'):<8} {info.get('multilingual','?')}"
        )
    return "\n".join(lines)


@mcp.resource("whisper://models/{name}")
def get_model_info(name: str) -> str:
    """Get details for a specific Whisper model."""
    available = whisper.available_models()
    if name not in available:
        return f"Unknown model '{name}'. Available: {', '.join(available)}"
    info = _MODEL_INFO.get(name, {})
    loaded = name in loaded_models()
    lines = [
        f"Model:        {name}",
        f"Parameters:   {info.get('params', '?')}",
        f"Speed:        {info.get('speed', '?')} (relative to large)",
        f"Multilingual: {info.get('multilingual', '?')}",
        f"Loaded:       {loaded}",
    ]
    return "\n".join(lines)


@mcp.resource("whisper://languages")
def list_languages() -> str:
    """List all languages supported by Whisper."""
    langs = sorted(whisper.tokenizer.LANGUAGES.items())
    lines = [f"{code}: {name}" for code, name in langs]
    return "\n".join(lines)


@mcp.resource("whisper://health")
def health() -> str:
    """Server status and currently loaded models."""
    loaded = loaded_models()
    lines = ["status: ok", f"loaded models ({len(loaded)}): {', '.join(loaded) if loaded else 'none'}"]
    return "\n".join(lines)


# ── Tools ──────────────────────────────────────────────────────────────────────

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
