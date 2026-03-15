"""CLI entrypoint for mini-whisper-mcp."""

import argparse

from mini_whisper_mcp.server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Run mini-whisper-mcp")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport mode",
    )
    parser.add_argument("--host", default="127.0.0.1", help="HTTP host")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port")
    parser.add_argument("--stateless", action="store_true", help="Run in stateless HTTP mode (no session required)")
    args = parser.parse_args()

    if args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port, stateless_http=args.stateless)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
