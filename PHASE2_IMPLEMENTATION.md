# Phase 2 Implementation Guide: Tool Removal Features (v1.2.0)

**Version**: v1.2.0  
**Timeline**: 2-3 weeks  
**Status**: Planning  
**Dependencies**: Phase 1 (v1.1.0) completed, MCP SDK >=1.17.0

## Overview

Phase 2 adds comprehensive tool removal and lifecycle management capabilities to mcp-commons, leveraging the new `FastMCP.remove_tool()` method introduced in MCP SDK v1.17.0.

## Implementation Checklist

### Week 1: Core Tool Removal Functions

#### Day 1-2: Setup and Planning
- [ ] Create feature branch `feature/phase2-tool-removal-v1.2.0`
- [ ] Review MCP SDK v1.17.0 `remove_tool()` documentation
- [ ] Design error handling strategy for tool removal
- [ ] Create test file `tests/test_tool_removal.py`
- [ ] Update version to 1.2.0-dev in `pyproject.toml`

#### Day 3-4: Implement `bulk_remove_tools()`
- [ ] Add function signature to `src/mcp_commons/bulk_registration.py`
- [ ] Implement core removal logic using `srv.remove_tool()`
- [ ] Add comprehensive error handling (ToolError, KeyError)
- [ ] Return structured dict with `removed`, `failed`, `success_rate`
- [ ] Add docstring with usage examples
- [ ] Write unit tests for:
  - [ ] Successful removal of multiple tools
  - [ ] Partial failure scenarios
  - [ ] Empty tool list edge case
  - [ ] Non-existent tool handling
  - [ ] Return value structure validation

#### Day 5: Implement `bulk_replace_tools()`
- [ ] Add function signature to `src/mcp_commons/bulk_registration.py`
- [ ] Implement atomic replacement logic (remove then add)
- [ ] Add rollback mechanism if additions fail
- [ ] Handle edge cases (empty lists, overlapping names)
- [ ] Add docstring with usage examples
- [ ] Write unit tests for:
  - [ ] Successful replacement of multiple tools
  - [ ] Rollback on add failure
  - [ ] Partial overlap scenarios
  - [ ] Empty list handling

### Week 2: Advanced Features

#### Day 6-7: Implement `conditional_remove_tools()`
- [ ] Add function signature to `src/mcp_commons/bulk_registration.py`
- [ ] Implement predicate-based filtering logic
- [ ] Get list of registered tools from server
- [ ] Apply condition and remove matching tools
- [ ] Return list of removed tool names
- [ ] Add docstring with usage examples
- [ ] Write unit tests for:
  - [ ] Pattern matching predicates
  - [ ] Complex condition functions
  - [ ] No matches scenario
  - [ ] All tools match scenario

#### Day 8-9: MCPServerBuilder Enhancements
- [ ] Add `enable_hot_reload()` method to `MCPServerBuilder`
- [ ] Implement configuration file watching
- [ ] Add automatic tool reloading on config change
- [ ] Add `with_tool_lifecycle_hooks()` method
- [ ] Implement callback execution for add/remove events
- [ ] Add docstrings and usage examples
- [ ] Write integration tests for:
  - [ ] Hot reload functionality
  - [ ] Lifecycle hook execution
  - [ ] Multiple hooks handling
  - [ ] Hook error handling

#### Day 10: Tool Introspection Utilities
- [ ] Add `get_registered_tools()` helper function
- [ ] Add `tool_exists()` helper function
- [ ] Add `count_tools()` helper function
- [ ] Add docstrings with examples
- [ ] Write unit tests for all helpers

### Week 3: Testing, Documentation, and Release

#### Day 11-12: Comprehensive Testing
- [ ] Run full test suite with `pytest -v`
- [ ] Verify 100% test coverage maintained
- [ ] Add integration tests for real-world scenarios:
  - [ ] Hot-swapping tool configurations
  - [ ] Graceful degradation on errors
  - [ ] Memory leak verification
- [ ] Test backward compatibility with v1.1.0 code
- [ ] Performance testing for bulk operations

#### Day 13-14: Documentation
- [ ] Update `README.md` with Phase 2 features
- [ ] Add code examples for all new functions
- [ ] Update `CHANGELOG.md` with v1.2.0 entry
- [ ] Add migration guide from v1.1.0 to v1.2.0
- [ ] Update API reference documentation
- [ ] Add troubleshooting section for common issues

#### Day 15: Release Preparation
- [ ] Update version to 1.2.0 in `pyproject.toml`
- [ ] Update version in `src/mcp_commons/__init__.py`
- [ ] Create release branch `release/v1.2.0`
- [ ] Run final test suite
- [ ] Create pull request with detailed description
- [ ] Tag release as `v1.2.0` after merge

## Detailed Implementation Specifications

### 1. bulk_remove_tools()

```python
def bulk_remove_tools(
    srv: FastMCP,
    tool_names: list[str]
) -> dict[str, Any]:
    """
    Remove multiple tools from a running MCP server.
    
    Args:
        srv: FastMCP server instance
        tool_names: List of tool names to remove
        
    Returns:
        Dictionary containing:
        - removed: List of successfully removed tool names
        - failed: List of (tool_name, error_message) tuples
        - success_rate: Float percentage (0.0-100.0)
        
    Example:
        >>> result = bulk_remove_tools(srv, ["tool1", "tool2", "tool3"])
        >>> print(f"Removed {len(result['removed'])} tools")
        >>> print(f"Success rate: {result['success_rate']:.1f}%")
    """
    removed = []
    failed = []
    
    for tool_name in tool_names:
        try:
            srv.remove_tool(tool_name)
            removed.append(tool_name)
        except Exception as e:
            failed.append((tool_name, str(e)))
    
    total = len(tool_names)
    success_rate = (len(removed) / total * 100) if total > 0 else 0.0
    
    return {
        "removed": removed,
        "failed": failed,
        "success_rate": success_rate
    }
```

### 2. bulk_replace_tools()

```python
def bulk_replace_tools(
    srv: FastMCP,
    tools_to_remove: list[str],
    tools_to_add: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """
    Atomically replace tools - remove old ones and add new ones.
    
    If any addition fails, attempts to rollback removals where possible.
    Useful for hot-reloading tool configurations.
    
    Args:
        srv: FastMCP server instance
        tools_to_remove: List of tool names to remove
        tools_to_add: Dictionary of tools to add (same format as bulk_register_tools)
        
    Returns:
        Dictionary containing:
        - removed: List of successfully removed tool names
        - added: List of successfully added tool names
        - rollback_performed: Boolean indicating if rollback occurred
        - errors: List of error messages if any
        
    Example:
        >>> result = bulk_replace_tools(
        ...     srv,
        ...     ["old_tool1", "old_tool2"],
        ...     {"new_tool1": {...}, "new_tool2": {...}}
        ... )
        >>> print(f"Replaced {len(result['removed'])} tools with {len(result['added'])}")
    """
    errors = []
    removed = []
    added = []
    rollback_performed = False
    
    # Phase 1: Remove old tools
    removal_result = bulk_remove_tools(srv, tools_to_remove)
    removed = removal_result["removed"]
    errors.extend([f"Remove failed: {e}" for _, e in removal_result["failed"]])
    
    # Phase 2: Add new tools
    try:
        addition_result = bulk_register_tools(srv, tools_to_add)
        added = [name for name, _ in addition_result]
    except Exception as e:
        errors.append(f"Addition failed: {str(e)}")
        # Attempt rollback - re-add removed tools if we have their configs
        rollback_performed = True
        # Note: Full rollback requires storing original tool configs
    
    return {
        "removed": removed,
        "added": added,
        "rollback_performed": rollback_performed,
        "errors": errors
    }
```

### 3. conditional_remove_tools()

```python
def conditional_remove_tools(
    srv: FastMCP,
    condition: Callable[[str], bool]
) -> list[str]:
    """
    Remove tools matching a condition.
    
    Args:
        srv: FastMCP server instance
        condition: Callable that takes tool name and returns True to remove
        
    Returns:
        List of removed tool names
        
    Example:
        >>> # Remove all deprecated tools
        >>> removed = conditional_remove_tools(
        ...     srv,
        ...     lambda name: "deprecated" in name.lower()
        ... )
        
        >>> # Remove tools by prefix
        >>> removed = conditional_remove_tools(
        ...     srv,
        ...     lambda name: name.startswith("test_")
        ... )
    """
    # Get list of registered tools (need to implement get_registered_tools())
    all_tools = get_registered_tools(srv)
    
    tools_to_remove = [name for name in all_tools if condition(name)]
    
    result = bulk_remove_tools(srv, tools_to_remove)
    return result["removed"]
```

### 4. Helper Functions

```python
def get_registered_tools(srv: FastMCP) -> list[str]:
    """
    Get list of all registered tool names.
    
    Args:
        srv: FastMCP server instance
        
    Returns:
        List of tool names
    """
    # Implementation depends on FastMCP internal API
    # May need to access srv._tools or similar
    pass

def tool_exists(srv: FastMCP, tool_name: str) -> bool:
    """
    Check if a tool is registered.
    
    Args:
        srv: FastMCP server instance
        tool_name: Name of tool to check
        
    Returns:
        True if tool exists, False otherwise
    """
    return tool_name in get_registered_tools(srv)

def count_tools(srv: FastMCP) -> int:
    """
    Count registered tools.
    
    Args:
        srv: FastMCP server instance
        
    Returns:
        Number of registered tools
    """
    return len(get_registered_tools(srv))
```

### 5. MCPServerBuilder Enhancements

```python
class MCPServerBuilder:
    # Existing methods...
    
    def enable_hot_reload(
        self,
        config_path: str,
        reload_interval: int = 60
    ) -> "MCPServerBuilder":
        """
        Enable automatic tool configuration reloading.
        
        Args:
            config_path: Path to watch for changes
            reload_interval: Check interval in seconds
            
        Returns:
            Self for method chaining
        """
        self._hot_reload_enabled = True
        self._config_path = config_path
        self._reload_interval = reload_interval
        return self
    
    def with_tool_lifecycle_hooks(
        self,
        on_add: Callable[[str], None] | None = None,
        on_remove: Callable[[str], None] | None = None
    ) -> "MCPServerBuilder":
        """
        Add callbacks for tool lifecycle events.
        
        Args:
            on_add: Called when tool is added (receives tool name)
            on_remove: Called when tool is removed (receives tool name)
            
        Returns:
            Self for method chaining
            
        Example:
            >>> builder = MCPServerBuilder("my-server")
            >>> builder.with_tool_lifecycle_hooks(
            ...     on_add=lambda name: print(f"Added: {name}"),
            ...     on_remove=lambda name: print(f"Removed: {name}")
            ... )
        """
        self._lifecycle_hooks = {
            "on_add": on_add,
            "on_remove": on_remove
        }
        return self
```

## Test Strategy

### Unit Tests
- **Location**: `tests/test_tool_removal.py`
- **Coverage Target**: 100% for new functions
- **Key Scenarios**:
  - Successful operations
  - Partial failures
  - Edge cases (empty lists, None values)
  - Error propagation

### Integration Tests
- **Location**: `tests/test_tool_lifecycle_integration.py`
- **Focus Areas**:
  - Hot reload with file watching
  - Lifecycle hooks execution order
  - Memory management (no leaks)
  - Performance benchmarks

### Backward Compatibility Tests
- **Location**: `tests/test_backward_compatibility.py`
- **Verification**:
  - v1.1.0 code still works
  - No breaking changes in existing APIs
  - Import compatibility

## Success Criteria

### Functional Requirements
- ✅ Can remove multiple tools efficiently
- ✅ Proper error handling and reporting
- ✅ Atomic replacement works correctly
- ✅ Conditional removal with flexible predicates
- ✅ Hot reload functionality

### Non-Functional Requirements
- ✅ No memory leaks from removed tools
- ✅ Performance: <100ms for 100 tool operations
- ✅ Backward compatible with v1.1.0
- ✅ 100% test coverage maintained
- ✅ Comprehensive documentation

### Quality Gates
- ✅ All tests pass (`pytest -v`)
- ✅ Coverage report shows 100% (`pytest --cov`)
- ✅ Type checking passes (`mypy src/`)
- ✅ Linting passes (`ruff check src/`)
- ✅ Import organization correct (`isort --check src/`)

## Risk Mitigation

### Potential Issues
1. **Tool removal may fail silently**: Ensure proper error reporting
2. **Memory leaks**: Test with large numbers of add/remove cycles
3. **Race conditions in hot reload**: Use file locking or debouncing
4. **Breaking changes**: Comprehensive backward compatibility testing

### Mitigation Strategies
1. Explicit error handling with detailed messages
2. Memory profiling during testing
3. Implement proper synchronization primitives
4. Maintain v1.1.0 compatibility test suite

## Migration Guide (v1.1.0 → v1.2.0)

### New Features Available
```python
# Old way (v1.1.0): Manual tool management
srv = FastMCP("my-server")
# No built-in way to remove tools

# New way (v1.2.0): Bulk removal
from mcp_commons import bulk_remove_tools

result = bulk_remove_tools(srv, ["old_tool1", "old_tool2"])
print(f"Removed {len(result['removed'])} tools")

# New way: Hot reload
builder = MCPServerBuilder("my-server")
builder.enable_hot_reload("config.yaml", reload_interval=30)
```

### Breaking Changes
**None** - v1.2.0 is fully backward compatible with v1.1.0

### Recommended Updates
1. Consider using `bulk_replace_tools()` for configuration updates
2. Enable hot reload for development environments
3. Add lifecycle hooks for logging/monitoring

## Timeline Summary

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1 | Core removal functions | `bulk_remove_tools`, `bulk_replace_tools` |
| 2 | Advanced features | `conditional_remove_tools`, builder enhancements |
| 3 | Polish and release | Tests, docs, v1.2.0 release |

## Next Steps After Phase 2

See `ROADMAP.md` for Phase 3 (v1.3.0) - Error Handling & Observability enhancements.

---

**Document Version**: 1.0  
**Created**: [Current Date]  
**Last Updated**: [Current Date]  
**Author**: Development Team
