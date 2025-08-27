# MCP Commons Library

A shared Python library providing common infrastructure for MCP (Model Context Protocol) servers.

## Features

### MCP Result Adapter
- **Higher-order function pattern** for converting use case results to MCP format
- **Eliminates 500+ lines of boilerplate** per server
- **Framework-agnostic** - works with any use case pattern
- **Type-safe** with proper signature preservation
- **Extensible** for different result types

### Use Case Base Classes
- Standard `UseCaseResult` for consistent return types
- Error handling patterns
- Validation utilities

### Testing Utilities
- Mock factories for MCP testing
- Test harnesses for use case validation

## Installation

```bash
pip install mcp-commons
```

## Quick Start

```python
from mcp_commons import create_mcp_adapter, UseCaseResult

# Your use case
async def list_projects(instance_name: str) -> UseCaseResult:
    # Your business logic here
    return UseCaseResult.success(data=projects)

# Create MCP-compatible version
adapted_method = create_mcp_adapter(list_projects)
tool = Tool.from_function(adapted_method, name="list_projects")
```

## Architecture Benefits

- **Single Source of Truth**: One implementation of MCP adaptation logic
- **Consistency**: All servers use identical error handling and response formats  
- **Maintainability**: Updates to MCP protocol handled in one place
- **Testability**: Shared test utilities ensure consistent behavior
- **Versioning**: Servers can depend on specific library versions for stability
