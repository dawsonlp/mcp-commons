# Phase 1 Implementation Checklist - v1.1.0

**Start Date**: January 15, 2025  
**Target Completion**: January 29, 2025 (2 weeks)  
**Goal**: Update mcp-commons to use MCP SDK v1.17.0 with full compatibility

## Overview

This phase focuses on updating the MCP SDK dependency and ensuring full compatibility with v1.17.0, with no breaking changes for existing users. This is a foundation-building phase that prepares us for future feature additions.

## Pre-Implementation Checklist

- [x] Analyze MCP SDK v1.17.0 release notes
- [x] Create comprehensive roadmap document
- [ ] Review roadmap with team/stakeholders
- [ ] Set up testing environment with v1.17.0
- [ ] Create feature branch: `feature/mcp-sdk-1.17.0-upgrade`

## Implementation Tasks

### 1. Dependency Update

#### 1.1 Update pyproject.toml
- [ ] Change MCP SDK version from `>=1.15.0` to `>=1.17.0`
- [ ] Verify all other dependencies are compatible
- [ ] Update version classifiers if needed
- [ ] Document dependency rationale in comments

**File**: `pyproject.toml`
```toml
dependencies = [
    "pydantic>=2.11.9",
    "PyYAML>=6.0.3",
    "mcp>=1.17.0",  # Updated for tool removal and testing utilities
]
```

#### 1.2 Update Development Environment
- [ ] Create fresh virtual environment
- [ ] Install updated dependencies: `pip install -e ".[dev]"`
- [ ] Verify all imports work correctly
- [ ] Check for deprecation warnings

**Commands**:
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
python -c "import mcp; print(mcp.__version__)"
```

### 2. Test Suite Updates

#### 2.1 Investigate New Testing Utilities
- [ ] Review `create_connected_server_and_client_session()` API
- [ ] Understand how it differs from current test approach
- [ ] Identify which tests would benefit from in-memory transport
- [ ] Create test migration plan

#### 2.2 Update Existing Tests
- [ ] Run current test suite with v1.17.0
- [ ] Fix any breaking changes (expected: none)
- [ ] Document any behavioral differences
- [ ] Ensure 100% test coverage maintained

**Commands**:
```bash
pytest tests/ -v --cov=mcp_commons --cov-report=term-missing
```

#### 2.3 Add v1.17.0 Feature Tests
- [ ] Add test for tool removal capability (even if not exposed in API yet)
- [ ] Verify OAuth URL construction works correctly
- [ ] Test that in-memory transport is available
- [ ] Document test patterns for future use

**New Test File**: `tests/test_mcp_sdk_compatibility.py`
```python
"""Tests to verify compatibility with MCP SDK v1.17.0 features"""

import pytest
from mcp.server.fastmcp import FastMCP
from mcp.shared.memory import create_connected_server_and_client_session


async def test_tool_removal_capability():
    """Verify that tool removal works with v1.17.0"""
    # Test that remove_tool method exists and works
    pass


async def test_in_memory_transport():
    """Verify that create_connected_server_and_client_session works"""
    # Test the new testing utility
    pass
```

### 3. Code Compatibility Review

#### 3.1 Review All Imports
- [ ] Check `src/mcp_commons/__init__.py` for version-specific imports
- [ ] Verify no deprecated MCP SDK functions used
- [ ] Update type hints if SDK types changed
- [ ] Test all public APIs still work

**Files to Review**:
- `src/mcp_commons/adapters.py`
- `src/mcp_commons/bulk_registration.py`
- `src/mcp_commons/server.py`
- `src/mcp_commons/base.py`

#### 3.2 Test MCPServerBuilder
- [ ] Verify FastMCP instantiation still works
- [ ] Test tool registration methods
- [ ] Verify all builder methods function correctly
- [ ] Test server startup with both stdio and sse transports

#### 3.3 Test Bulk Registration
- [ ] Verify `bulk_register_tools` works with v1.17.0
- [ ] Test all registration variants
- [ ] Ensure error handling still works
- [ ] Verify logging output is correct

### 4. Documentation Updates

#### 4.1 Update README.md
- [ ] Update MCP SDK version requirement to 1.17.0+
- [ ] Add note about v1.17.0 compatibility
- [ ] Update any examples if needed
- [ ] Verify all code snippets still work

**Section to Update**:
```markdown
## Requirements

- Python 3.11+ (Python 3.13 recommended for optimal performance)
- MCP SDK 1.17.0+ (for tool removal and testing utilities)
- Pydantic 2.11.9+
- PyYAML 6.0.3+
```

#### 4.2 Create CHANGELOG.md
- [ ] Document v1.1.0 changes
- [ ] List dependency updates
- [ ] Note any behavioral changes
- [ ] Include migration notes

**New File**: `CHANGELOG.md`
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-01-29

### Changed
- Updated MCP SDK dependency from >=1.15.0 to >=1.17.0
- Updated test suite to be compatible with v1.17.0

### Added
- Compatibility tests for MCP SDK v1.17.0 features
- Documentation for v1.17.0 features

### Fixed
- None

### Migration Notes
- No breaking changes
- Simply update mcp-commons: `pip install --upgrade mcp-commons>=1.1.0`
```

#### 4.3 Update Version Number
- [ ] Bump version in `pyproject.toml` to 1.1.0
- [ ] Update `src/mcp_commons/__init__.py` if version is exported
- [ ] Tag the release appropriately

### 5. CI/CD Updates

#### 5.1 Update GitHub Actions (if exists)
- [ ] Update test matrix to include MCP SDK v1.17.0
- [ ] Add version compatibility tests
- [ ] Ensure CI runs against Python 3.11, 3.12, 3.13
- [ ] Add test for minimum and maximum dependency versions

#### 5.2 Create Release Workflow
- [ ] Automated version bumping
- [ ] Changelog generation
- [ ] PyPI publishing (if not already set up)
- [ ] GitHub release creation

### 6. Quality Assurance

#### 6.1 Manual Testing
- [ ] Create a test MCP server using mcp-commons
- [ ] Register tools using bulk registration
- [ ] Start server with stdio transport
- [ ] Start server with sse transport
- [ ] Verify tools work correctly
- [ ] Test error handling

**Test Script**: `tests/manual_test.py`
```python
"""Manual test script for v1.1.0 release"""

from mcp_commons import bulk_register_tools, MCPServerBuilder
from mcp.server.fastmcp import FastMCP


async def sample_tool() -> str:
    return "Hello from v1.1.0"


def test_basic_server():
    """Test basic server creation and tool registration"""
    builder = MCPServerBuilder("test-server")
    
    tools_config = {
        "sample_tool": {
            "function": sample_tool,
            "description": "A sample tool"
        }
    }
    
    builder.with_tools_config(tools_config)
    server = builder.build()
    
    print("✓ Server created successfully")
    print("✓ Tool registered successfully")
    return True


if __name__ == "__main__":
    test_basic_server()
    print("\n✓ All manual tests passed")
```

#### 6.2 Integration Testing
- [ ] Test with real MCP clients (Claude Desktop, Cline)
- [ ] Verify tools appear correctly in client
- [ ] Test tool execution end-to-end
- [ ] Verify error messages are helpful

#### 6.3 Performance Testing
- [ ] Benchmark tool registration time (should be similar to v1.0.1)
- [ ] Test server startup time
- [ ] Verify no memory leaks
- [ ] Check CPU usage during normal operation

### 7. Release Preparation

#### 7.1 Pre-Release Checklist
- [ ] All tests pass with 100% coverage
- [ ] Documentation is complete and accurate
- [ ] CHANGELOG.md is up to date
- [ ] Version numbers are correct
- [ ] No TODO comments in code
- [ ] Code is formatted with black
- [ ] Imports are sorted with isort
- [ ] Ruff linting passes

#### 7.2 Create Release PR
- [ ] Branch: `feature/mcp-sdk-1.17.0-upgrade` → `main`
- [ ] Title: "Release v1.1.0 - MCP SDK v1.17.0 Compatibility"
- [ ] Description includes full changelog
- [ ] All CI checks pass
- [ ] Request code review

#### 7.3 Release Steps
- [ ] Merge PR to main
- [ ] Tag release: `git tag -a v1.1.0 -m "Release v1.1.0"`
- [ ] Push tag: `git push origin v1.1.0`
- [ ] Create GitHub release with changelog
- [ ] Publish to PyPI: `python -m build && twine upload dist/*`
- [ ] Announce release (if applicable)

## Success Criteria

### Must Have
- ✓ All existing tests pass with MCP SDK v1.17.0
- ✓ No breaking changes for existing users
- ✓ Documentation accurately reflects v1.17.0 compatibility
- ✓ Version bumped to 1.1.0
- ✓ CHANGELOG.md created and complete

### Should Have
- ✓ Test coverage remains at 100%
- ✓ New compatibility tests added
- ✓ Manual testing completed successfully
- ✓ CI/CD pipeline updated

### Nice to Have
- ✓ Performance benchmarks documented
- ✓ Integration testing with real clients
- ✓ Community feedback collected

## Known Issues / Decisions

### Issue: Tool Removal Not Yet Exposed
**Decision**: Include SDK v1.17.0 but don't expose tool removal in public API yet. This will be added in v1.2.0 with proper bulk removal capabilities.

**Rationale**: We want to provide bulk operations consistently, not one-at-a-time operations.

### Issue: OAuth Features Not Used
**Decision**: Update to v1.17.0 but don't expose OAuth features yet. Consider for v1.4.0 as optional enterprise feature.

**Rationale**: OAuth is not core to mcp-commons mission. Focus on tool management first.

## Timeline

### Week 1 (Jan 15-21)
- Days 1-2: Dependency update and environment setup
- Days 3-4: Test suite updates and compatibility testing
- Days 5-7: Code review and documentation updates

### Week 2 (Jan 22-29)
- Days 1-2: CI/CD updates and quality assurance
- Days 3-4: Manual and integration testing
- Days 5-7: Release preparation and deployment

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Breaking changes in SDK | Comprehensive test suite catches issues early |
| Regression in functionality | Manual testing with real clients |
| Performance degradation | Benchmark tests before and after |
| User adoption issues | Clear migration guide and changelog |

## Post-Release Tasks

- [ ] Monitor PyPI download stats
- [ ] Watch for GitHub issues related to v1.1.0
- [ ] Collect user feedback
- [ ] Plan Phase 2 (tool removal features)
- [ ] Update roadmap based on learnings

## Notes

- This is a dependency update release with no new features
- Focus on stability and compatibility
- Sets foundation for v1.2.0 feature additions
- Should be transparent to existing users

---

**Phase Owner**: Development Team  
**Status**: Not Started  
**Last Updated**: January 15, 2025
