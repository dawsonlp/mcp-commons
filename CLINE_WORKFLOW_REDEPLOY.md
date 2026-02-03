# Cline Workflow: Redeploy mcp-commons with Version Bump

This workflow guides you through redeploying mcp-commons with the appropriate version number based on the type of changes made.

## Semantic Versioning Quick Reference

mcp-commons follows [Semantic Versioning 2.0.0](https://semver.org/):

| Version Type | Format | When to Use | Example |
|--------------|--------|-------------|---------|
| **MAJOR** | X.0.0 | Breaking changes to public API | 1.2.3 → 2.0.0 |
| **MINOR** | 0.X.0 | New features (backward compatible) | 1.2.3 → 1.3.0 |
| **PATCH** | 0.0.X | Bug fixes, dependency updates, docs | 1.2.3 → 1.2.4 |

### Common Scenarios

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Upgrade MCP SDK dependency | **PATCH** | 1.2.3 → 1.2.4 |
| Update other dependencies | **PATCH** | 1.2.3 → 1.2.4 |
| Fix bugs, improve docs | **PATCH** | 1.2.3 → 1.2.4 |
| Add new utility functions | **MINOR** | 1.2.3 → 1.3.0 |
| Change function signatures | **MAJOR** | 1.2.3 → 2.0.0 |
| Remove public functions | **MAJOR** | 1.2.3 → 2.0.0 |

## Current Version

**Check current version**: Look in `pyproject.toml` for the `version = "X.Y.Z"` line.

## Workflow Steps

### Step 1: Determine Version Bump

**Prompt for Cline:**
```
Check pyproject.toml for the current version, then determine the appropriate 
version bump following semantic versioning based on my changes: [DESCRIBE YOUR CHANGES].
Explain your reasoning using the semantic versioning rules.
```

**For Dependency Updates:**
- **Version Bump**: PATCH (X.Y.Z → X.Y.Z+1)
- **Reasoning**: Dependency updates without API changes = PATCH

**For New Features:**
- **Version Bump**: MINOR (X.Y.Z → X.Y+1.0)
- **Reasoning**: New backward-compatible functionality = MINOR

**For Breaking Changes:**
- **Version Bump**: MAJOR (X.Y.Z → X+1.0.0)
- **Reasoning**: Breaking API changes = MAJOR

### Step 2: Update pyproject.toml

**Prompt for Cline:**
```
Update the version number in pyproject.toml from {CURRENT_VERSION} to {NEW_VERSION}
```

**File to modify**: `pyproject.toml`
**Line to change**: `version = "{CURRENT_VERSION}"` → `version = "{NEW_VERSION}"`

### Step 3: Update CHANGELOG.md

**Prompt for Cline:**
```
Update CHANGELOG.md with a new entry for version {NEW_VERSION}. The changes are:
[DESCRIBE YOUR CHANGES]

Follow the existing changelog format with appropriate sections 
(Added/Changed/Fixed/Security/Deprecated/Removed).
Add the entry under "## [Unreleased]" and create a new dated section.
Include Migration Notes if there are breaking changes or important notices.
```

**Template Format:**
```markdown
## [Unreleased]

## [{NEW_VERSION}] - {TODAY'S_DATE}

### [Changed/Added/Fixed/etc.]
- [Description of changes]
  - [Additional context]
  - [Impact on users]

### Migration Notes (if applicable)
- **Breaking changes** (for MAJOR) / **No breaking changes** (for MINOR/PATCH)
- To upgrade: `pip install --upgrade mcp-commons>={NEW_VERSION}`
- [Any specific migration instructions]
```

### Step 4: Make Code Changes (if applicable)

**Prompt for Cline:**
```
[Make your code changes - e.g., update dependencies in pyproject.toml]
Then install the updated dependencies:
pip install -e ".[dev]"
```

### Step 5: Run Tests

**Prompt for Cline:**
```
Run the full test suite to ensure all tests pass:
pytest -v

If any tests fail, investigate and fix before proceeding.
```

**Expected Result**: All tests passing

### Step 6: Run Tests Again

**Prompt for Cline:**
```
Run the full test suite again to verify compatibility with the updated dependency:
pytest -v --cov=mcp_commons --cov-report=term-missing

Ensure all tests still pass and coverage is maintained.
```

### Step 7: Git Commit and Tag

**Prompt for Cline:**
```
Create a git commit for the version bump and tag it:

git add pyproject.toml CHANGELOG.md [OTHER_CHANGED_FILES]
git commit -m "chore: bump version to {NEW_VERSION} - [BRIEF DESCRIPTION]"
git tag -a v{NEW_VERSION} -m "Version {NEW_VERSION} - [BRIEF DESCRIPTION]"
git push origin main
git push origin v{NEW_VERSION}
```

### Step 8: Build and Publish to PyPI

**Prompt for Cline:**
```
Build the distribution packages and publish to PyPI:

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution packages
python -m build

# Upload to PyPI (requires PyPI credentials)
python -m twine upload dist/*

Alternatively, if using poetry:
poetry build
poetry publish
```

**Prerequisites:**
- PyPI account with credentials configured
- `build` package installed: `pip install build`
- `twine` package installed: `pip install twine`

### Step 9: Verify Deployment

**Prompt for Cline:**
```
Verify the new version is available on PyPI:

# Check PyPI page
open https://pypi.org/project/mcp-commons/

# Test installation in a clean environment
python -m venv test_env
source test_env/bin/activate
pip install mcp-commons=={NEW_VERSION}
python -c "import mcp_commons; print(mcp_commons.__version__)"
deactivate
rm -rf test_env
```

## Complete Workflow Template (Adapt to your changes)

**Replace placeholders before executing:**
- `{CURRENT_VERSION}` - Current version from pyproject.toml
- `{NEW_VERSION}` - New version based on semantic versioning rules
- `{CHANGE_DESCRIPTION}` - Brief description of changes
- `{DATE}` - Today's date in YYYY-MM-DD format

```bash
# 1. Check current version in pyproject.toml
grep 'version = ' pyproject.toml

# 2. Determine new version using semantic versioning rules
# PATCH for bug fixes/deps, MINOR for features, MAJOR for breaking changes

# 3. Update pyproject.toml version
# Edit: version = "{CURRENT_VERSION}" → version = "{NEW_VERSION}"

# 4. Update CHANGELOG.md
# Add new section for {NEW_VERSION} with {DATE}

# 5. Make your code changes (if any)
# E.g., update dependencies, fix bugs, add features

# 6. Install updated dependencies
pip install -e ".[dev]"

# 7. Run tests
pytest -v --cov=mcp_commons --cov-report=term-missing

# 8. Commit and tag
git add pyproject.toml CHANGELOG.md [other-files]
git commit -m "chore: bump version to {NEW_VERSION} - {CHANGE_DESCRIPTION}"
git tag -a v{NEW_VERSION} -m "Version {NEW_VERSION} - {CHANGE_DESCRIPTION}"

# 9. Push to remote
git push origin main
git push origin v{NEW_VERSION}

# 10. Build and publish
rm -rf dist/ build/ *.egg-info
python -m build
python -m twine upload dist/*

# 11. Verify
pip install --upgrade mcp-commons
python -c "import mcp_commons; print('Successfully installed')"
```

## Troubleshooting

### Tests Fail After Dependency Update
```
# Investigate which tests are failing
pytest -v -x  # Stop at first failure

# Check for API changes in updated dependency
# Review dependency's changelog
# Update code if needed
# Re-run tests
```

### PyPI Upload Fails
```
# Check credentials
cat ~/.pypirc

# Or use token authentication
# Create token at https://pypi.org/manage/account/token/
# Use __token__ as username and token value as password
```

### Version Already Exists on PyPI
```
# Cannot republish same version
# Must bump version number again
# Edit pyproject.toml and CHANGELOG.md
# Increment PATCH version (e.g., X.Y.Z → X.Y.Z+1)
# Rebuild and republish
```

## Quick Reference: Version Bump Decision Tree

```
Is there a breaking change?
├─ YES → MAJOR bump (X.Y.Z → X+1.0.0)
└─ NO
   └─ Is there a new feature?
      ├─ YES → MINOR bump (X.Y.Z → X.Y+1.0)
      └─ NO
         └─ Is there a bug fix, docs update, or dependency update?
            ├─ YES → PATCH bump (X.Y.Z → X.Y.Z+1)
            └─ NO → No version bump needed
```

## Notes

- **Always run tests** before publishing
- **Update CHANGELOG.md** for every release
- **Use semantic versioning** strictly
- **Tag releases** in git for traceability
- **Test installation** from PyPI after publishing
- **Document breaking changes** clearly in CHANGELOG
- **Keep dependencies updated** but test compatibility

## Last Updated

2025-10-31 - Created workflow document
