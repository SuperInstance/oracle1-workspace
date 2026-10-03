# Polished: crab

**Date:** 2026-07-12
**Status:** ✅ Production-ready

## What was done
- Added MIT LICENSE
- Added 4 unit tests (`tests/test_crab.py`):
  - `enter_and_leave`: Enter a fake repo, verify stack, leave, verify empty
  - `status_empty`: Status reports 0 repos when empty
  - `enter_nonexistent`: Entering bad path returns False
  - `tool_not_found`: Running unknown tool returns None
- Added CI workflow (Python 3.12, runs tests)
- Added `.gitignore` for Python artifacts
- Removed committed `__pycache__/crab.cpython-310.pyc`
- Updated README: corrected test instructions, added MIT license reference

## Architecture
- Python tool for entering/leaving repos like MUD rooms
- CrabShell class with repo stack, tool registry, manifest parsing
- Supports MANIFEST.md (YAML frontmatter), MANIFEST.yaml, MANIFEST.json
- State persistence via `/tmp/crab-state/state.json`

## Test count
4 tests, all passing.

## Commit
`855c55e` — "Tier 3 polish: add tests, license, CI, cleanup"
