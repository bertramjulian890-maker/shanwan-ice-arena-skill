from __future__ import annotations

import os
import sys

from ice_arena_mcp.server import mcp


def main() -> None:
    transport = os.environ.get("ICE_ARENA_MCP_TRANSPORT", "stdio")
    if transport not in ("stdio", "sse", "streamable-http"):
        print(
            "ICE_ARENA_MCP_TRANSPORT must be one of: stdio, sse, streamable-http",
            file=sys.stderr,
        )
        raise SystemExit(2)
    host = os.environ.get("ICE_ARENA_MCP_HOST", "127.0.0.1")
    port = int(os.environ.get("ICE_ARENA_MCP_PORT", "8710"))
    mcp.settings.host = host
    mcp.settings.port = port
    # Streamable HTTP 默认要求 Accept 同时包含 application/json 与 text/event-stream。
    # 部分网关只发 application/json，会导致 POST /mcp → 406；开启后仅要求 application/json（与 FastMCP 的 json_response 一致）。
    _jr = os.environ.get("ICE_ARENA_MCP_JSON_RESPONSE", "").strip().lower()
    if _jr in ("1", "true", "yes", "on"):
        mcp.settings.json_response = True
    mcp.run(transport=transport)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
