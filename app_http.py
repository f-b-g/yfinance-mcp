# app_http.py
# Purpose: Wrap the yfinance-mcp server with an HTTP endpoint that MCP clients can reach.
# This uses the official MCP Python SDK's "streamable HTTP" transport.

import os
from mcp.server.fastmcp import FastMCP

#
# Try to reuse the server defined inside yfinance-mcp.
# Many MCP servers expose a module-level `mcp` FastMCP instance.
#
server = None
try:
    # common case: the package exposes `mcp`
    from yfmcp import mcp as server  # type: ignore
except Exception:
    try:
        # some templates put it under yfmcp.server
        from yfmcp.server import mcp as server  # type: ignore
    except Exception:
        pass

if server is None:
    # Fallback: create an empty server with a health tool so the service still starts.
    # (If you see only this tool when testing, the package layout changed —
    #  update the imports above or redeploy. Your service is still reachable.)
    mcp = FastMCP("Yahoo Finance MCP (adapter)")
    @mcp.tool()
    def ping() -> str:
        """Basic health check."""
        return "pong"
    server = mcp

# Create an ASGI app that serves the MCP HTTP endpoint at /mcp
# (default path used by the SDK)
app = server.streamable_http_app()

# Optional: if you prefer the endpoint to be exactly `/`
# uncomment the next line:
# server.settings.streamable_http_path = "/"

# On Render, the process manager (uvicorn below) will call `app` and bind to $PORT.
