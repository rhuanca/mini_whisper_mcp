import whisper
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("whisper")
_models: dict[str, whisper.Whisper] = {}


def get_model(name: str) -> whisper.Whisper:
    if name not in _models:
        _models[name] = whisper.load_model(name)
    return _models[name]


@mcp.tool()
def transcribe(audio_path: str, model: str = "base") -> str:
    """Transcribe an audio file using Whisper. Returns the transcribed text.

    Args:
        audio_path: Absolute path to the audio file (mp3, wav, m4a, etc.)
        model: Whisper model to use: tiny, base, small, medium, large (default: base)
    """
    result = get_model(model).transcribe(audio_path)
    return result["text"]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
