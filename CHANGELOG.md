# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/dawsonlp/mcp-commons/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/dawsonlp/mcp-commons/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/dawsonlp/mcp-commons/releases/tag/v1.0.1
