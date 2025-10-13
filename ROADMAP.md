# MCP Commons Roadmap - Post v1.17.0 Analysis

**Date**: January 15, 2025  
**SDK Version Analyzed**: v1.17.0  
**Current mcp-commons Version**: 1.0.1  
**Current MCP SDK Dependency**: >=1.15.0

## Executive Summary

The MCP SDK v1.17.0 release introduces several features that create opportunities for mcp-commons to expand its utility while maintaining its core mission of eliminating boilerplate code. The most significant addition is dynamic tool removal, which complements our existing bulk registration capabilities.

## Key Findings

### 1. Tool Removal Capability (HIGH PRIORITY)
**SDK Feature**: `remove_tool()` method added to FastMCP and ToolManager

**Impact on mcp-commons**: 
- We provide bulk registration but no corresponding bulk removal
- Creates asymmetry in the API - can add many tools at once but must remove one at a time
- Missing opportunity for dynamic tool management patterns

**Recommendation**: Add bulk tool removal capabilities

### 2. OAuth RFC 9728 Compliance (LOW PRIORITY)
**SDK Feature**: Improved OAuth protected resource metadata URL construction

**Impact on mcp-commons**:
- Currently not used by mcp-commons
- MCPServerBuilder doesn't expose OAuth configuration
- Could be valuable for enterprise deployments

**Recommendation**: Consider adding OAuth support to MCPServerBuilder as optional feature

### 3. Testing Infrastructure (MEDIUM PRIORITY)
**SDK Feature**: New `create_connected_server_and_client_session()` utility

**Impact on mcp-commons**:
- Our test suite doesn't use the new in-memory testing approach
- Missing opportunity to showcase testing patterns for users
- Documentation lacks testing examples

**Recommendation**: Update test suite and add testing documentation

### 4. Documentation Patterns (MEDIUM PRIORITY)
**SDK Feature**: Comprehensive testing.md, installation.md, concepts.md guides

**Impact on mcp-commons**:
- Our documentation is minimal compared to SDK standards
- Missing testing guide for users
- No comprehensive examples of mcp-commons patterns

**Recommendation**: Expand documentation following SDK patterns

## Proposed Roadmap

### Phase 1: Immediate Updates (v1.1.0)
**Timeline**: 1-2 weeks

- [ ] Update MCP SDK dependency from `>=1.15.0` to `>=1.17.0`
- [ ] Verify compatibility with v1.17.0 API changes
- [ ] Update test suite to use `create_connected_server_and_client_session()`
- [ ] Run full test suite and verify all tests pass
- [ ] Update CI/CD to test against v1.17.0

**Success Criteria**:
- All existing tests pass with v1.17.0
- No breaking changes for existing users
- Clean CI/CD pipeline

### Phase 2: Tool Removal Features (v1.2.0)
**Timeline**: 2-3 weeks

#### 2.1 Core Tool Removal API
Add complementary bulk removal capabilities to match bulk registration:

```python
# New functions in bulk_registration.py

def bulk_remove_tools(
    srv: FastMCP, 
    tool_names: list[str]
) -> dict[str, Any]:
    """
    Remove multiple tools from a running MCP server.
    
    Returns dict with:
    - removed: List of successfully removed tools
    - failed: List of (tool_name, error) tuples
    - success_rate: Percentage of successful removals
    """

def bulk_replace_tools(
    srv: FastMCP,
    tools_to_remove: list[str],
    tools_to_add: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """
    Atomically replace tools - remove old ones and add new ones.
    Useful for hot-reloading tool configurations.
    """

def conditional_remove_tools(
    srv: FastMCP,
    condition: Callable[[str], bool]
) -> list[str]:
    """
    Remove tools matching a condition.
    Example: Remove all tools with "deprecated" in name
    """
```

#### 2.2 MCPServerBuilder Enhancements
Add tool lifecycle management to the builder:

```python
class MCPServerBuilder:
    def enable_hot_reload(self, reload_interval: int = 60) -> "MCPServerBuilder":
        """Enable automatic tool configuration reloading"""
        
    def with_tool_lifecycle_hooks(
        self,
        on_add: Callable | None = None,
        on_remove: Callable | None = None
    ) -> "MCPServerBuilder":
        """Add callbacks for tool lifecycle events"""
```

**Deliverables**:
- [ ] Implement bulk_remove_tools with proper error handling
- [ ] Implement bulk_replace_tools for atomic updates
- [ ] Implement conditional_remove_tools for pattern-based removal
- [ ] Add comprehensive tests for all removal scenarios
- [ ] Update documentation with removal examples
- [ ] Add migration guide from v1.1 to v1.2

**Success Criteria**:
- Can remove multiple tools efficiently
- Proper error handling and reporting
- No memory leaks from removed tools
- Backward compatible with v1.1

### Phase 3: Testing Infrastructure (v1.2.1)
**Timeline**: 1-2 weeks

#### 3.1 Update Test Suite
- [ ] Migrate all tests to use `create_connected_server_and_client_session()`
- [ ] Add snapshot testing for tool responses
- [ ] Add integration tests using the new patterns
- [ ] Create test fixtures for common scenarios

#### 3.2 Testing Utilities for Users
Create testing helpers that users can import:

```python
# New module: mcp_commons/testing.py

async def create_test_server(
    tools_config: dict[str, dict[str, Any]]
) -> tuple[FastMCP, ClientSession]:
    """
    Create a test server with tools for easy testing.
    Returns server and connected client session.
    """

class MCPTestHarness:
    """
    Test harness that simplifies testing MCP tools.
    Provides utilities for mocking, assertions, and fixtures.
    """
```

**Deliverables**:
- [ ] New testing.py module with user-facing utilities
- [ ] Updated test suite using new patterns
- [ ] Testing guide documentation
- [ ] Example test files for users

**Success Criteria**:
- All tests use modern MCP SDK testing patterns
- Users have clear testing examples
- Test coverage remains at 100%

### Phase 4: Documentation Expansion (v1.3.0)
**Timeline**: 2-3 weeks

#### 4.1 Create Comprehensive Guides
Following SDK documentation structure:

**docs/testing.md**:
- How to test MCP servers built with mcp-commons
- Using create_test_server() helper
- Snapshot testing for tool results
- Integration testing patterns
- Mocking use cases and dependencies

**docs/advanced_usage.md**:
- Dynamic tool management (add/remove/replace)
- Hot-reloading tool configurations
- Tool lifecycle hooks
- Conditional tool availability
- Performance optimization tips

**docs/migration.md**:
- Migrating from raw FastMCP to mcp-commons
- Version upgrade guides
- Breaking changes and deprecations

**docs/examples.md**:
- Complete working examples
- Common patterns and use cases
- Anti-patterns to avoid
- Performance considerations

#### 4.2 API Reference
- [ ] Generate complete API reference from docstrings
- [ ] Add type hints to all public APIs
- [ ] Document all exceptions and error cases
- [ ] Add code examples to all major functions

**Deliverables**:
- [ ] Four new documentation files
- [ ] Updated README with links to docs
- [ ] API reference page
- [ ] Updated CONTRIBUTING.md with documentation standards

**Success Criteria**:
- Documentation covers all features
- Clear examples for common use cases
- Easy to find information

### Phase 5: OAuth and Enterprise Features (v1.4.0)
**Timeline**: 3-4 weeks (OPTIONAL)

#### 5.1 OAuth Support in MCPServerBuilder

```python
class MCPServerBuilder:
    def with_oauth(
        self,
        resource_server_url: str,
        client_id: str,
        client_secret: str
    ) -> "MCPServerBuilder":
        """Configure RFC 9728-compliant OAuth authentication"""
        
    def with_custom_auth(
        self,
        auth_handler: Callable
    ) -> "MCPServerBuilder":
        """Configure custom authentication"""
```

#### 5.2 Enterprise Configuration Management

```python
# New module: mcp_commons/config_manager.py

class ConfigurationManager:
    """
    Manage server configurations with:
    - Environment-specific configs
    - Secret management
    - Configuration validation
    - Hot-reload support
    """
```

**Deliverables**:
- [ ] OAuth configuration in MCPServerBuilder
- [ ] ConfigurationManager for enterprise deployments
- [ ] Examples of OAuth-secured servers
- [ ] Documentation for enterprise features
- [ ] Security best practices guide

**Success Criteria**:
- RFC 9728 compliant OAuth
- Secure secret management
- Clear security documentation

## Version Compatibility Matrix

| mcp-commons | MCP SDK | Python | Status |
|-------------|---------|--------|--------|
| 1.0.1 | >=1.15.0 | >=3.11 | Current |
| 1.1.0 | >=1.17.0 | >=3.11 | Planned |
| 1.2.0 | >=1.17.0 | >=3.11 | Planned |
| 1.3.0 | >=1.17.0 | >=3.11 | Planned |
| 1.4.0 | >=1.17.0 | >=3.11 | Optional |

## Breaking Changes

### v1.1.0
- None expected (dependency update only)

### v1.2.0
- None expected (additive features only)

### v1.3.0
- None expected (documentation only)

### v1.4.0
- May introduce new required dependencies for OAuth support
- Will be clearly marked as optional features

## Migration Strategy

### For Existing Users

#### Upgrading to v1.1.0
```bash
# Update dependency
pip install --upgrade mcp-commons>=1.1.0

# No code changes required
# All existing code continues to work
```

#### Upgrading to v1.2.0
```python
# Before (v1.1.0)
tools = bulk_register_tools(srv, tools_config)

# After (v1.2.0) - backward compatible, new features optional
tools = bulk_register_tools(srv, tools_config)

# New feature: bulk removal
removed = bulk_remove_tools(srv, ["old_tool1", "old_tool2"])

# New feature: atomic replacement
result = bulk_replace_tools(
    srv,
    tools_to_remove=["old_tool"],
    tools_to_add={"new_tool": {...}}
)
```

## Immediate Action Items

### This Week
1. Update pyproject.toml to require `mcp>=1.17.0`
2. Run test suite against v1.17.0
3. Create initial testing.md documentation
4. Plan v1.2.0 tool removal API design

### Next Week
1. Implement bulk_remove_tools
2. Update test suite to use new SDK testing patterns
3. Write migration guide for v1.1.0

### This Month
1. Release v1.1.0 (SDK update)
2. Complete tool removal features
3. Begin documentation expansion

## Success Metrics

### Technical Metrics
- Test coverage: Maintain 100%
- Performance: No regression from v1.0.1
- API stability: Zero breaking changes in minor versions
- Documentation: 100% of public API documented

### User Metrics
- Adoption: Track pip install counts
- Issues: Maintain <48 hour response time
- Satisfaction: Collect feedback on new features

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking changes in MCP SDK | Low | High | Comprehensive test suite, pin to specific version |
| Performance degradation with bulk operations | Low | Medium | Benchmark tests, optimize critical paths |
| Complex OAuth implementation | Medium | Medium | Make optional, provide clear examples |
| Documentation falling behind features | High | Low | Document as we build, not after |

## Decision Log

### Decision: Update to v1.17.0
**Date**: January 15, 2025  
**Rationale**: Tool removal capability is natural complement to bulk registration  
**Trade-offs**: Must maintain backward compatibility, adds test burden  
**Alternatives Considered**: Stay on v1.15.0 (rejected - missing valuable features)

### Decision: Phase OAuth Support
**Date**: January 15, 2025  
**Rationale**: Not core to mcp-commons mission, can be added later  
**Trade-offs**: Some enterprise users may need to wait  
**Alternatives Considered**: Build now (rejected - focus on core features first)

### Decision: Prioritize Tool Removal
**Date**: January 15, 2025  
**Rationale**: Direct extension of existing bulk registration functionality  
**Trade-offs**: Delays documentation work  
**Alternatives Considered**: Documentation first (rejected - features more urgent)

## Community Engagement

### Communication Plan
1. Create GitHub issue announcing v1.17.0 analysis
2. Post roadmap for community feedback
3. Create RFC for tool removal API design
4. Regular updates on progress

### Feedback Channels
- GitHub Issues for feature requests
- GitHub Discussions for general questions
- Pull requests welcome for all phases

## Conclusion

The MCP SDK v1.17.0 release provides excellent opportunities for mcp-commons to expand its capabilities while staying true to its mission of eliminating boilerplate code. The proposed roadmap prioritizes:

1. **Immediate compatibility** with v1.17.0
2. **Natural extensions** (bulk tool removal)
3. **Better testing** infrastructure
4. **Improved documentation**
5. **Optional enterprise** features

This approach ensures we deliver value incrementally while maintaining stability for existing users.

## Next Steps

1. Review this roadmap with stakeholders
2. Create GitHub issues for each phase
3. Begin Phase 1 implementation
4. Update project board with roadmap items
5. Communicate plan to community

---

**Document Owner**: Development Team  
**Last Updated**: January 15, 2025  
**Next Review**: After v1.1.0 release
