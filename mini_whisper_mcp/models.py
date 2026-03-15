import logging

import whisper

logger = logging.getLogger(__name__)
_cache: dict[str, whisper.Whisper] = {}


def get_model(name: str) -> whisper.Whisper:
    """Load and cache a Whisper model, falling back to CPU on CUDA errors."""
    if name not in _cache:
        try:
            logger.info("Loading Whisper model: %s", name)
            _cache[name] = whisper.load_model(name)
        except RuntimeError as exc:
            if "CUDA" not in str(exc):
                raise
            logger.warning("CUDA unavailable, retrying on CPU: %s", exc)
            _cache[name] = whisper.load_model(name, device="cpu")
    return _cache[name]
