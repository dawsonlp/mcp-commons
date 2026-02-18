# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.4] - 2026-02-18

### Fixed
- **`__version__` in `__init__.py`** was stuck at `1.2.2` — now correctly set to `1.3.4`
- **README.md** had outdated version references:
  - "Current Version: 1.2.1" → updated to 1.3.4
  - "MCP SDK: 1.17.0+" → updated to 1.26.0+
  - "Pydantic 2.11.9+" → updated to 2.12.5+
  - Removed stale "What's New" sections for v1.2.0 and v1.2.1
  - Removed outdated roadmap section referencing future v1.3.0–v1.5.0
- **CHANGELOG.md** reference links only covered up to v1.1.0 — now covers all versions
- **CONTRIBUTING.md** — fixed test structure listing, updated release tag examples

### Removed
- **8 obsolete planning/historical documents** that contained heavily outdated version references:
  - `PHASE1_IMPLEMENTATION.md` — v1.1.0 implementation plan (completed)
  - `PHASE2_IMPLEMENTATION.md` — v1.2.0 implementation plan (completed)
  - `ARCHITECTURAL_EVALUATION.md` — v1.2.1 evaluation against SDK v1.17.0 (superseded)
  - `ARCHITECTURAL_EVALUATION_REVISED.md` — revision of the above (superseded)
  - `v1.17.0-changes.md` — MCP SDK v1.17.0 release notes (no longer relevant)
  - `DEVELOPMENT_CHECKLIST.md` — v1.1.0 checklist (completed)
  - `ROADMAP.md` — listed current version as 1.0.1 (entirely stale)
  - `IMPORT_STANDARDS.md` — import conventions (captured in CONTRIBUTING.md)

### Migration Notes
- **No breaking changes** — documentation-only fixes and cleanup
- To upgrade: `pip install --upgrade mcp-commons>=1.3.4`

## [1.3.3] - 2026-02-02

### Changed
- Updated MCP SDK dependency from 1.23.2 to 1.26.0
  - Latest stable release from 2026-01-24
  - Includes latest features and improvements from MCP SDK
- Updated GitHub Actions workflow to trigger releases on version tags
  - Releases now triggered by pushing `v*` tags (e.g., `git push origin v1.3.3`)
  - Previously triggered on every push to main branch
  - Provides better control over release timing

### Migration Notes
- **No breaking changes** - This is a dependency update and CI/CD improvement
- To upgrade: `pip install --upgrade mcp-commons>=1.3.3`
- All existing code continues to work without modifications

### Release Process
To release a new version:
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit changes: `git commit -m "chore: bump version to X.Y.Z"`
4. Tag the release: `git tag -a vX.Y.Z -m "Version X.Y.Z"`
5. Push: `git push origin main && git push origin vX.Y.Z`

## [1.3.2] - 2025-12-08

### Changed
- Updated MCP SDK dependency from 1.23.1 to 1.23.2
  - Latest patch release with bug fixes and improvements

### Migration Notes
- **No breaking changes** - This is a dependency update only
- To upgrade: `pip install --upgrade mcp-commons>=1.3.2`
- All existing code continues to work without modifications
- All 42 tests pass with updated dependency

## [1.3.1] - 2025-12-07

### Changed
- Updated dependencies to latest versions:
  - **mcp**: 1.21.1 → 1.23.1 (MCP SDK with latest features and improvements)
  - **pydantic**: 2.11.9 → 2.12.5 (data validation improvements)
  - **pytest**: 8.4.2 → 9.0.2 (testing framework updates)
  - **pytest-asyncio**: 1.2.0 → 1.3.0 (async testing improvements)
  - **black**: 25.9.0 → 25.12.0 (code formatter updates)
  - **isort**: 6.0.1 → 7.0.0 (import sorting improvements)
  - **ruff**: 0.13.2 → 0.14.8 (linter updates)
  - PyYAML and pytest-cov remain at current versions (already latest)

### Migration Notes
- **No breaking changes** - This is a dependency update only
- To upgrade: `pip install --upgrade mcp-commons>=1.3.1`
- All existing code continues to work without modifications
- All 42 tests pass with updated dependencies

## [1.3.0] - 2025-01-13

### Changed
- Updated MCP SDK dependency from `>=1.20.0` to `>=1.21.1`
  - Ensures compatibility with latest MCP SDK features and improvements
  - Includes all updates from MCP SDK v1.21.x series
  - No breaking changes to mcp-commons API

### Migration Notes
- **No breaking changes** - This is a dependency update only
- To upgrade: `pip install --upgrade mcp-commons>=1.3.0`
- All existing code continues to work without modifications
- MINOR version bump to indicate staying current with MCP SDK ecosystem

## [1.2.4] - 2025-10-31

### Changed
- Updated MCP SDK dependency from `>=1.19.0` to `>=1.20.0`
  - Ensures compatibility with latest MCP SDK features and improvements
  - No breaking changes to mcp-commons API

### Migration Notes
- **No breaking changes** - This is a dependency update only
- To upgrade: `pip install --upgrade mcp-commons>=1.2.4`
- All existing code continues to work without modifications

## [1.2.3] - 2025-01-23

### Changed
- Updated MCP SDK dependency from `>=1.17.0` to `>=1.19.0`
  - Ensures compatibility with latest MCP SDK features and improvements
  - No breaking changes to mcp-commons API

### Migration Notes
- **No breaking changes** - This is a dependency update only
- To upgrade: `pip install --upgrade mcp-commons>=1.2.3`
- All existing code continues to work without modifications

## [1.2.2] - 2025-01-15

### Changed
- **Documentation Accuracy** - Updated all documentation to accurately represent mcp-commons' relationship with FastMCP
  - Clarified that mcp-commons is a thin wrapper over FastMCP's existing methods (add_tool, remove_tool)
  - Updated README to show actual code implementations (what bulk operations really do)
  - Emphasized adapter pattern as the primary value (90%) vs convenience wrappers (10%)
  - Added comparison table showing FastMCP capabilities vs mcp-commons additions
  - Updated bulk_registration.py module docstring for transparency

### Fixed
- None - documentation accuracy improvements only

### Notes
- No code changes - this is purely a documentation release
- All functionality from v1.2.1 remains unchanged
- Users upgrading from v1.2.1 will see no breaking changes

## [1.2.1] - 2025-01-29

### Changed
- **Documentation Overhaul** - Professional-grade documentation following technical writing best practices
  - Comprehensive README.md with 15+ code examples, clear hierarchy, and progressive disclosure
  - New CONTRIBUTING.md with complete contributor guidelines and development workflow
  - Enhanced API reference with detailed function documentation
  - Added version badges and professional formatting throughout

### Fixed
- None - documentation-only release

## [1.2.0] - 2025-01-29

### Added
- **Tool Removal Features** - Leveraging MCP SDK v1.17.0's `remove_tool()` capability
  - `bulk_remove_tools()` - Remove multiple tools with detailed success/failure reporting
  - `bulk_replace_tools()` - Atomically replace tools (remove old, add new) for hot-reloading
  - `conditional_remove_tools()` - Remove tools matching a predicate function
  - `get_registered_tools()` - List all registered tool names
  - `tool_exists()` - Check if a specific tool is registered
  - `count_tools()` - Get count of registered tools
- Comprehensive test suite with 19 new tests in `tests/test_tool_removal.py`
- Phase 2 implementation guide (`PHASE2_IMPLEMENTATION.md`)

### Changed
- Updated exports in `__init__.py` to include new tool removal functions
- Enhanced `bulk_registration.py` with tool lifecycle management capabilities

### Fixed
- None

### Security
- None

### Migration Notes
- **No breaking changes** - All new features are additive
- To upgrade: `pip install --upgrade mcp-commons>=1.2.0`
- All existing code continues to work without modifications
- New tool removal features are opt-in

### Testing
- All 42 tests passing (18 adapter tests + 5 compatibility tests + 19 removal tests)
- Test coverage maintained at ~50% overall, 100% for new features
- Zero test warnings or failures

### Examples
```python
from mcp_commons import bulk_remove_tools, bulk_replace_tools, conditional_remove_tools

# Remove multiple tools
result = bulk_remove_tools(srv, ["old_tool1", "old_tool2"])
print(f"Removed {len(result['removed'])} tools")

# Replace tools atomically
result = bulk_replace_tools(
    srv,
    tools_to_remove=["old_tool"],
    tools_to_add={"new_tool": {"function": new_fn, "description": "New tool"}}
)

# Remove tools by pattern
removed = conditional_remove_tools(srv, lambda name: name.startswith("test_"))
```

## [1.1.0] - 2025-01-29

### Changed
- Updated MCP SDK dependency from `>=1.15.0` to `>=1.17.0`
  - Enables access to new tool removal capabilities (to be exposed in v1.2.0)
  - Provides new testing utilities via `create_connected_server_and_client_session()`
  - Includes OAuth RFC 9728 compliance improvements
- Updated test suite to verify compatibility with MCP SDK v1.17.0

### Added
- New compatibility test suite in `tests/test_mcp_sdk_compatibility.py`
- Comprehensive roadmap document (`ROADMAP.md`) outlining future development
- Phase 1 implementation guide (`PHASE1_IMPLEMENTATION.md`)
- Development checklist (`DEVELOPMENT_CHECKLIST.md`) for systematic implementation
- This CHANGELOG to track version history

### Fixed
- None

### Security
- None

### Migration Notes
- **No breaking changes** - This is a dependency update only
- To upgrade: `pip install --upgrade mcp-commons>=1.1.0`
- All existing code continues to work without modifications
- New MCP SDK features are available but not yet exposed in mcp-commons API

### Coming in v1.2.0
- `bulk_remove_tools()` - Remove multiple tools at once
- `bulk_replace_tools()` - Atomic tool replacement for hot-reloading
- `conditional_remove_tools()` - Pattern-based tool removal
- Enhanced testing utilities for users

## [1.0.1] - 2025-01-XX

### Initial Release
- Basic adapter pattern for MCP tools
- Bulk tool registration utilities
- MCPServerBuilder for standardized server setup
- Core functionality for eliminating MCP server boilerplate

[Unreleased]: https://github.com/dawsonlp/mcp-commons/compare/v1.3.4...HEAD
[1.3.4]: https://github.com/dawsonlp/mcp-commons/compare/v1.3.3...v1.3.4
[1.3.3]: https://github.com/dawsonlp/mcp-commons/compare/v1.3.2...v1.3.3
[1.3.2]: https://github.com/dawsonlp/mcp-commons/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/dawsonlp/mcp-commons/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/dawsonlp/mcp-commons/compare/v1.2.4...v1.3.0
[1.2.4]: https://github.com/dawsonlp/mcp-commons/compare/v1.2.3...v1.2.4
[1.2.3]: https://github.com/dawsonlp/mcp-commons/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/dawsonlp/mcp-commons/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/dawsonlp/mcp-commons/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/dawsonlp/mcp-commons/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/dawsonlp/mcp-commons/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/dawsonlp/mcp-commons/releases/tag/v1.0.1
