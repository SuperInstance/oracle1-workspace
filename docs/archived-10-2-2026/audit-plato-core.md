# Deep Audit: plato-core

**Repo:** SuperInstance/plato-core  
**Tier:** 2 — Near-Ready 🔧  
**Language:** Python  
**License:** None ⚠️  
**Audited:** 2026-07-12  

---

## Overview

Core type system for PLATO — TrainingTile, TileType, TileLifecycle, LamportClock, MeshRegistry, content hashing.

## Metadata

| Metric | Value |
|--------|-------|
| Stars | 1 |
| Forks | 0 |
| Size | 30,437 KB |
| Open Issues | 0 |
| Last Pushed | 2026-06-08 |

## Structure

```
plato-core/
├── plato_core/
│   ├── __init__.py
│   ├── types.py       # TrainingTile, TileType, TileLifecycle, LamportClock, content_hash
│   └── registry.py    # MeshRegistry, register_core
├── tests/
│   ├── test_types.py      # Type system tests
│   ├── test_registry.py   # Registry tests
│   └── test_advanced.py   # Advanced lifecycle, tile supersession, serialization
├── docs/
├── npm/               # npm packaging (unusual for Python repo)
├── memory/
├── AGENT.md
├── pyproject.toml
└── CI: ci.yml
```

## Test Suite

3 test files:
- **test_types.py** — TileType values, TileLifecycle values, content_hash, LamportClock, TrainingTile creation
- **test_registry.py** — MeshRegistry operations
- **test_advanced.py** — Multiple lifecycle transitions, reactivation after supersede, parent-child links, serialization edge cases

Tests are well-structured with clear assertions and docstrings.

## What It Needs

1. **LICENSE** — No license = all rights reserved. Must add MIT or Apache-2.0
2. **30MB size** — Extremely bloated for 3 Python files. Check for data artifacts.
3. **npm/ directory** — Remove if not used (Python project)
4. **PyPI publication** — Types and registry are reusable; publish as package
5. **Type annotations** — Add mypy/pyright annotations
6. **More modules** — types.py and registry.py are focused but the package could expand

## Verdict

Clean Python type system with good test coverage. The LamportClock and lifecycle management are real distributed systems primitives. But **no license** makes it legally unusable.
