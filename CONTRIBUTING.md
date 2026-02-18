# Contributing to MCP Commons

Thank you for your interest in contributing to MCP Commons! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

---

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

### Prerequisites

- Python 3.11 or higher (3.13 recommended)
- Git
- pip or uv for package management

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/mcp-commons.git
cd mcp-commons
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/dawsonlp/mcp-commons.git
```

### Development Setup

```bash
# Create a virtual environment
python3.13 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import mcp_commons; print(mcp_commons.__version__)"
```

---

## Development Workflow

### Branch Strategy

- `main` - Stable release branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Creating a Feature Branch

```bash
# Update your local main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. **Write Tests First** - Follow TDD principles when possible
2. **Make Small Commits** - One logical change per commit
3. **Write Clear Commit Messages** - Follow conventional commits format
4. **Keep PRs Focused** - One feature or fix per pull request

### Conventional Commits

We use conventional commits for clear change history:

```
feat: add bulk_remove_tools function
fix: correct error handling in adapter
docs: update README with new examples
test: add integration tests for tool removal
chore: update dependencies
refactor: simplify bulk registration logic
```

---

## Coding Standards

### Python Style Guide

We follow PEP 8 with these tools:

- **black** - Code formatting (line length: 88)
- **isort** - Import sorting
- **ruff** - Fast linting

### Running Code Quality Checks

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check linting
ruff check src/ tests/

# Run all checks
./scripts/check_code_quality.sh  # If available
```

### Type Hints

- Use type hints for all public APIs
- Use Python 3.11+ type hint syntax
- Document complex types in docstrings

```python
from typing import Any

def bulk_remove_tools(
    server: FastMCP,
    tool_names: list[str]
) -> dict[str, Any]:
    """Remove multiple tools from server.
    
    Args:
        server: FastMCP server instance
        tool_names: List of tool names to remove
        
    Returns:
        Dictionary with removed, failed, and success_rate keys
    """
    ...
```

### Documentation Strings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 10) -> dict:
    """Brief description of function.
    
    Longer description providing more context and usage examples.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter with default value
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Example:
        >>> result = example_function("test", 20)
        >>> print(result)
        {'status': 'success'}
    """
    ...
```

### Code Organization

Follow these principles:

1. **DRY (Don't Repeat Yourself)** - Extract common patterns
2. **KISS (Keep It Simple)** - Prefer simple solutions
3. **Single Responsibility** - One clear purpose per function/class
4. **Explicit Over Implicit** - Clear variable and function names

---

## Testing Guidelines

### Test Structure

```
tests/
├── test_adapters.py               # Adapter pattern tests
├── test_tool_removal.py           # Tool removal and lifecycle tests
└── test_mcp_sdk_compatibility.py  # SDK compatibility tests
```

### Writing Tests

Use pytest with these patterns:

```python
import pytest
from mcp_commons import create_mcp_adapter, UseCaseResult

class TestCreateMcpAdapter:
    """Test suite for create_mcp_adapter function."""
    
    @pytest.mark.asyncio
    async def test_successful_adaptation(self):
        """Test adapter with successful use case result."""
        async def sample_use_case() -> UseCaseResult:
            return UseCaseResult.success_with_data({"value": 42})
        
        adapter = create_mcp_adapter(sample_use_case)
        result = await adapter()
        
        assert result["success"] is True
        assert result["data"]["value"] == 42
        assert result["error"] is None
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_adapters.py -v

# Run with coverage
pytest tests/ --cov=mcp_commons --cov-report=html

# Run specific test
pytest tests/test_adapters.py::TestCreateMcpAdapter::test_successful_adaptation -v
```

### Test Coverage

- Maintain overall coverage above 80%
- New features must include tests
- Critical paths require 100% coverage

```bash
# Generate coverage report
pytest --cov=mcp_commons --cov-report=term-missing
```

---

## Documentation

### Types of Documentation

1. **Code Comments** - Explain "why", not "what"
2. **Docstrings** - API documentation
3. **README** - Quick start and overview
4. **Guides** - Detailed tutorials and examples
5. **API Reference** - Complete function documentation

### Updating Documentation

When adding features:

1. Update relevant docstrings
2. Add examples to README
3. Update CHANGELOG.md
4. Create or update guides
5. Add to API reference

### Documentation Style

- Use active voice
- Keep sentences concise
- Include code examples
- Test all code examples
- Use proper Markdown formatting

---

## Submitting Changes

### Before Submitting

1. **Run Tests**: Ensure all tests pass
   ```bash
   pytest tests/ -v
   ```

2. **Check Code Quality**: Run linting and formatting
   ```bash
   black src/ tests/
   isort src/ tests/
   ruff check src/ tests/
   ```

3. **Update Documentation**: Add/update relevant docs

4. **Write Good Commit Messages**: Follow conventional commits

### Pull Request Process

1. **Push Your Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub with:
   - Clear title following conventional commits
   - Description of changes
   - Link to related issues
   - Test results
   - Screenshots (if UI changes)

3. **PR Template** should include:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] All tests pass
   - [ ] Added new tests
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No new warnings
   ```

4. **Code Review**: Address feedback promptly

5. **Merge**: Maintainer will merge once approved

### After Merge

1. **Update Your Fork**:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

2. **Delete Feature Branch**:
   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

---

## Release Process

Maintainers follow this process for releases:

### Version Numbering

Follow Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md with release date
3. Run full test suite
4. Create release branch
5. Tag release: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
6. Push tag: `git push origin vX.Y.Z`
7. GitHub Actions automatically deploys to PyPI
8. Create GitHub release with notes

---

## Getting Help

- 📖 Read the [documentation](https://github.com/dawsonlp/mcp-commons/wiki)
- 💬 Ask questions in [Discussions](https://github.com/dawsonlp/mcp-commons/discussions)
- 🐛 Report bugs via [Issues](https://github.com/dawsonlp/mcp-commons/issues)
- 📧 Contact maintainers for security issues

---

## License

By contributing to MCP Commons, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MCP Commons! 🎉
