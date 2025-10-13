# Import Standards for mcp-commons

## Summary

✅ **Current import organization is CORRECT and follows Python best practices (PEP 8).**

## Import Rules

### Rule 1: Use Relative Imports WITHIN the Package

**Inside `src/mcp_commons/` modules:**
```python
# ✅ CORRECT - adapters.py importing from base.py
from .base import UseCaseResult
from .exceptions import AdapterError

# ❌ WRONG - Don't do this inside the package
from mcp_commons.base import UseCaseResult  # Anti-pattern!
```

### Rule 2: Use Absolute Imports OUTSIDE the Package

**In tests and external code:**
```python
# ✅ CORRECT - tests importing from the package
from mcp_commons import UseCaseResult
from mcp_commons import create_mcp_adapter

# ❌ WRONG - Can't use relative imports from outside
from .mcp_commons import UseCaseResult  # Won't work!
```

## Why This Matters

### Benefits of Relative Imports (within package):

1. **PEP 8 Compliance** - Official Python style guide recommends relative imports within packages
2. **Package Relocatability** - Can rename/move the package without changing internal imports
3. **Avoids Circular Dependencies** - Relative imports help prevent circular import issues
4. **Clear Intent** - The `.` explicitly shows "from this package"
5. **IDE Support** - Better refactoring support in modern IDEs

### Why NOT to use absolute imports internally:

```python
# ❌ ANTI-PATTERN inside src/mcp_commons/adapters.py:
from mcp_commons.base import UseCaseResult

# Problems:
# 1. Circular dependency risk
# 2. Harder to refactor/rename
# 3. Unnecessary package name repetition
# 4. Not following PEP 8 recommendations
```

## Current State (All Correct ✅)

### Package Internal Imports (src/mcp_commons/)

```python
# __init__.py - Uses relative imports ✅
from .adapters import create_mcp_adapter
from .base import UseCaseResult
from .bulk_registration import bulk_register_tools
from .config import MCPConfig
from .exceptions import McpCommonsError
from .server import MCPServerBuilder

# adapters.py - Uses relative imports ✅
from .base import UseCaseResult

# config.py - Uses relative imports ✅
from .exceptions import McpCommonsError

# server.py - Uses relative imports ✅
from .bulk_registration import bulk_register_tools
```

### Test Imports (tests/)

```python
# test_adapters.py - Uses absolute imports ✅
from mcp_commons import UseCaseResult, create_mcp_adapter

# test_mcp_sdk_compatibility.py - Uses absolute imports ✅
from mcp_commons import UseCaseResult, create_mcp_adapter
from mcp_commons import bulk_register_tools
```

## Import Organization (enforced by isort)

### Within any file, imports are organized:

1. **Standard library** imports (e.g., `import logging`, `from typing import Any`)
2. **Third-party** imports (e.g., `from mcp.server.fastmcp import FastMCP`)
3. **Local relative** imports (e.g., `from .base import UseCaseResult`)

Example from `adapters.py`:
```python
# 1. Standard library
import inspect
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

# 2. Third-party (none in this file)

# 3. Local relative
from .base import UseCaseResult
```

## Common Misconceptions

### ❓ "Relative imports are bad"
**FALSE** - Relative imports are recommended by PEP 8 for **within-package** imports.

### ❓ "Everything should be absolute imports"  
**FALSE** - Absolute imports should be used **outside** the package. Inside the package, use relative imports.

### ❓ "from .module means it's wrong"
**FALSE** - The `.` dot notation is Python's syntax for relative imports and is the **correct** way to import within a package.

## References

- [PEP 8 - Imports](https://peps.python.org/pep-0008/#imports)
- [PEP 328 - Absolute and Relative Imports](https://peps.python.org/pep-0328/)
- [Python Packaging Guide](https://packaging.python.org/en/latest/)

## Verification Commands

Check that internal imports use relative syntax:
```bash
# Should find relative imports (from .) in source files
grep -n "^from \." src/mcp_commons/*.py

# Should NOT find absolute package imports in source files
grep -n "^from mcp_commons" src/mcp_commons/*.py
# Expected: No results (or only in commented examples)
```

Check that tests use absolute imports:
```bash
# Should find absolute imports in tests
grep -n "^from mcp_commons" tests/*.py
# Expected: Multiple results (correct!)
```

## Conclusion

✅ **Our current import organization is correct and follows Python best practices.**

No changes needed. The relative imports like `from .base import UseCaseResult` inside the package are exactly how they should be!
