"""CLI entrypoint for basic-whisper-mcp-server."""

import argparse

from basic_whisper_mcp_server.server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Run basic-whisper-mcp-server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport mode",
    )
    parser.add_argument("--host", default="127.0.0.1", help="HTTP host")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port")
    args = parser.parse_args()

    if args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
