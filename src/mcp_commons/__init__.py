"""
MCP Commons - Shared infrastructure for MCP servers.

This library provides reusable components for building MCP (Model Context Protocol) servers,
eliminating boilerplate and ensuring consistency across server implementations.
"""

from .adapters import create_mcp_adapter, validate_use_case_result, AdapterStats
from .base import UseCaseResult, BaseUseCase
from .exceptions import McpCommonsError, UseCaseError, AdapterError
from .bulk_registration import (
    bulk_register_tools, 
    bulk_register_with_adapter_pattern,
    bulk_register_tuple_format,
    log_registration_summary,
    validate_tools_config,
    register_tools,
    BulkRegistrationError
)
from .server import (
    MCPServerBuilder,
    setup_logging,
    run_mcp_server,
    create_mcp_app,
    print_mcp_help
)
from .config import (
    MCPConfig,
    ConfigurationError,
    create_config,
    load_dotenv_file
)

__version__ = "1.0.0"
__all__ = [
    # Core adapter functionality
    "create_mcp_adapter",
    "validate_use_case_result", 
    "AdapterStats",
    
    # Base classes
    "UseCaseResult",
    "BaseUseCase",
    
    # Bulk registration functionality
    "bulk_register_tools",
    "bulk_register_with_adapter_pattern", 
    "bulk_register_tuple_format",
    "log_registration_summary",
    "validate_tools_config",
    "register_tools",
    "BulkRegistrationError",
    
    # Server utilities
    "MCPServerBuilder",
    "setup_logging",
    "run_mcp_server",
    "create_mcp_app",
    "print_mcp_help",
    
    # Configuration management
    "MCPConfig",
    "ConfigurationError",
    "create_config",
    "load_dotenv_file",
    
    # Exceptions
    "McpCommonsError",
    "UseCaseError", 
    "AdapterError",
]
