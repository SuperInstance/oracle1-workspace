# POLISHED: exocortex

**Date:** 2026-07-12  
**Commit:** `ba8414e` — "Tier 2 → Tier 1: fix CI, license, packaging"

## What Was Done

### License Fixed
- ❌ Was: README claimed MIT but NO LICENSE FILE existed — legally unusable
- ✅ Now: Proper MIT LICENSE file added

### CI Fixed
- ❌ Was: `pytest || true` — tests never gated merges
- ✅ Now: `pytest -v` (no `|| true`), installs package with `pip install -e ".[dev]"` first
- Tests now properly gate PRs

### Build Artifacts Removed
- ❌ Was: `exocortex.egg-info/` committed (5 files: PKG-INFO, SOURCES.txt, dependency_links, requires, top_level)
- ✅ Removed: `git rm --cached` and expanded `.gitignore` to prevent recommit

### .gitignore Expanded
- Added `build/`, `dist/`, `.eggs/` to prevent future build artifact commits

### README Polish
- Fixed broken badge links (were non-functional shields with missing URLs)
- Added proper CI badge and license badge

## Test Results

```
50 tests passed, 0 failed
- test_core.py: 32 tests (core types, resonance)
- test_phase2.py: 18 tests (k-means clustering, dream cycle, resonance)
```

## What Still Needs Work

- **Test coverage is thin**: 2 test files for 8 modules (bus, compute, config, core, memory, protocols, shadows, tui)
- **S3 compatibility unverified**: Claims S3-compatible memory but no test with actual S3/MinIO
- **Shadow agents undocumented**: What are they? How do they work?
- **Protocol layer undocumented**: What protocols are supported?
- **Docker not tested in CI**: Dockerfile + docker-compose exist but not validated
- **Heavy dependencies**: textual, FastAPI, numpy — should verify all are actually used
- **No PyPI publication**
