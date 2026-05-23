"""
Common server startup utilities for MCP servers.

This module provides standardized server initialization, configuration management,
and startup patterns that can be shared across all MCP servers.
"""

import logging
import sys
from logging import FileHandler, StreamHandler
from pathlib import Path
from typing import Any, TextIO

from mcp.server.fastmcp import FastMCP

from .bulk_registration import bulk_register_tools, log_registration_summary

# Set up logging
logger = logging.getLogger(__name__)


class MCPServerBuilder:
    """
    Builder class for creating standardized MCP servers with common patterns.

    This eliminates duplicated server setup code across different MCP server implementations.
    """

    def __init__(self, server_name: str):
        """
        Initialize the MCP server builder.

        Args:
            server_name: Name of the MCP server
        """
        self.server_name = server_name
        self.server_instance: FastMCP | None = None
        self.tools_config: dict[str, dict[str, Any]] = {}

    def with_tools_config(
        self, tools_config: dict[str, dict[str, Any]]
    ) -> "MCPServerBuilder":
        """
        Configure the tools that will be registered with the server.

        Args:
            tools_config: Dictionary mapping tool names to their configuration

        Returns:
            Self for method chaining
        """
        self.tools_config = tools_config
        return self

    def build(self) -> FastMCP:
        """
        Build and configure the MCP server instance.

        Returns:
            Configured FastMCP server instance
        """
        # Create the MCP server
        self.server_instance = FastMCP(self.server_name)

        # Register tools if provided
        if self.tools_config:
            registered_tools = bulk_register_tools(
                self.server_instance, self.tools_config
            )
            log_registration_summary(
                registered_tools, len(self.tools_config), self.server_name
            )

        logger.info(f"{self.server_name} MCP server built successfully")
        return self.server_instance


def setup_logging(
    log_level: str = "INFO",
    *,
    stream: TextIO | None = None,
    log_file: str | Path | None = None,
    transport: str | None = None,
) -> None:
    """
    Configure logging for an MCP server.

    Default behavior is now stderr (was stdout). stdout corrupts the
    JSON-RPC protocol when the server runs over stdio transport, which
    is the dominant deployment shape for MCP servers.

    Args:
        log_level: Logging level (DEBUG/INFO/WARNING/ERROR).
        stream: Explicit stream to log to. Defaults to sys.stderr.
            Pass sys.stdout only if you understand the stdio implication.
            Ignored if log_file is set.
        log_file: If set, log to this file via FileHandler instead of a stream.
            Useful for SSE servers running as containers/daemons.
        transport: Optional transport hint ("stdio" | "sse" | "streamable-http").
            Reserved for future per-transport defaults; ignored today.
            Callers should pass it for forward-compat.
    """
    handler: logging.Handler
    if log_file is not None:
        handler = FileHandler(str(log_file), mode="a")
    else:
        handler = StreamHandler(stream if stream is not None else sys.stderr)
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[handler],
    )


def run_mcp_server(
    server_name: str,
    tools_config: dict[str, dict[str, Any]],
    config: dict[str, Any] | None = None,
    transport: str = "sse",
    host: str = "localhost",
    port: int = 7501,
) -> None:
    """
    Run an MCP server with standardized configuration.

    This function eliminates boilerplate server startup code that's common
    across all MCP server implementations.

    Args:
        server_name: Name of the MCP server
        tools_config: Dictionary mapping tool names to their configuration
        config: Optional server configuration dictionary
        transport: Transport type ("sse" or "stdio")
        host: Host for SSE transport (default: localhost)
        port: Port for SSE transport (default: 7501)
    """
    # Set up logging
    setup_logging()

    # Build the server
    builder = MCPServerBuilder(server_name)
    builder.with_tools_config(tools_config)

    server = builder.build()

    # Configure transport settings
    if transport == "sse":
        server.settings.host = host
        server.settings.port = port
        logger.info(f"Starting {server_name} with HTTP+SSE transport on {host}:{port}")
    else:  # stdio
        logger.info(f"Starting {server_name} with stdio transport")

    # Run the server
    server.run(transport)


def create_mcp_app(
    server_name: str,
    tools_config: dict[str, dict[str, Any]],
    config: dict[str, Any] | None = None,
) -> Any:
    """
    Create an ASGI application for use with an external ASGI server.

    This function standardizes ASGI app creation across MCP servers.

    Args:
        server_name: Name of the MCP server
        tools_config: Dictionary mapping tool names to their configuration
        config: Optional server configuration dictionary

    Returns:
        ASGI application instance
    """
    # Build the server
    builder = MCPServerBuilder(server_name)
    builder.with_tools_config(tools_config)

    server = builder.build()

    logger.info(f"{server_name} ASGI app created successfully")
    return server.sse_app()


def print_mcp_help(server_name: str, description: str = "MCP Server") -> None:
    """
    Print standardized help information for MCP servers.

    Args:
        server_name: Name of the MCP server
        description: Description of what the server does
    """
    help_text = f"""
{server_name} {description} Usage Guide
{'=' * (len(server_name) + len(description) + 13)}

BASIC USAGE:
-----------
  python main.py sse        # Run as HTTP+SSE server (for network/container use)
  python main.py stdio      # Run as stdio server (for local development)
  python main.py help       # Show this help message

CONNECTING TO CLAUDE/CLINE:
------------------------
To connect this MCP server to Claude Desktop or Cline in VS Code:

1. First make sure your MCP server is running with the sse transport:
   python main.py sse

2. For Cline in VS Code, edit the settings file:
   ~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

   Example configuration:
   {{
     "mcpServers": {{
       "{server_name}": {{
         "url": "http://localhost:7501/sse",
         "apiKey": "example_key",
         "disabled": false,
         "autoApprove": []
       }}
     }}
   }}

3. For Claude Desktop, go to:
   Settings → Advanced → MCP Servers → Add MCP Server

   Enter:
   - Name: {server_name}
   - URL: http://localhost:7501
   - API Key: example_key (or your custom API key)

4. Restart Claude/VS Code to apply the changes

DEPLOYMENT:
----------
- For local development: Use 'stdio' transport
- For Docker/containers: Use 'sse' transport with port 7501
- Configure with environment variables or .env file

For more information, see the MCP SDK documentation at:
https://github.com/modelcontextprotocol/python-sdk
"""
    print(help_text)


def run_cli(
    server_name: str,
    tools_config: dict[str, dict[str, Any]],
    *,
    description: str = "",
    host: str = "localhost",
    port: int = 7501,
    transports: tuple[str, ...] = ("stdio", "sse"),
    log_level: str = "INFO",
    log_file: str | Path | None = None,
    argv: list[str] | None = None,
) -> None:
    """
    Standardized argv -> transport dispatcher for MCP server `main()` entry points.

    Reads argv[0] (defaults to sys.argv[1:]) and:
      - "help" / "--help" / "-h"  -> print_mcp_help and return
      - "--transport <value>"     -> use <value> (jira-helper style)
      - "<value>"                 -> use <value> (worldcontext style)
      - anything else             -> print usage + sys.exit(2)

    Valid transport values are constrained by the `transports` tuple. The
    default ("stdio", "sse") covers the common case; jira-helper-style servers
    can pass ("stdio", "sse", "streamable-http").

    Logging is set up before the server runs:
      - stdio transport             -> log to stderr (default)
      - non-stdio transport         -> log to stderr OR log_file if provided

    Args:
        server_name: Name of the MCP server (passed to print_mcp_help and
            internally to MCPServerBuilder).
        tools_config: Tool registration dictionary (same shape as
            run_mcp_server expects).
        description: Optional short tagline shown by print_mcp_help.
        host: Network bind address for non-stdio transports.
        port: Network bind port for non-stdio transports.
        transports: Whitelist of accepted transport names.
        log_level: Forwarded to setup_logging.
        log_file: Forwarded to setup_logging.
        argv: Override sys.argv for tests. Pass the equivalent of sys.argv[1:].

    Exit codes:
        0  - server ran and exited cleanly
        2  - bad transport argument (unknown or missing)
    """
    args = argv if argv is not None else sys.argv[1:]
    if not args or args[0] in ("help", "--help", "-h"):
        print_mcp_help(server_name, description or "MCP Server")
        return

    if args[0] == "--transport":
        if len(args) < 2:
            print("--transport requires a value", file=sys.stderr)
            sys.exit(2)
        transport = args[1]
    else:
        transport = args[0]

    if transport not in transports:
        print(
            f"Unknown transport: {transport!r}. "
            f"Valid choices: {', '.join(transports)} (or 'help').",
            file=sys.stderr,
        )
        sys.exit(2)

    setup_logging(log_level=log_level, log_file=log_file, transport=transport)

    kwargs: dict[str, Any] = {
        "server_name": server_name,
        "tools_config": tools_config,
        "transport": transport,
    }
    if transport != "stdio":
        kwargs["host"] = host
        kwargs["port"] = port
    run_mcp_server(**kwargs)
