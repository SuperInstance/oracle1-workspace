# SHIPPED: plato-server

**Date:** 2026-07-12
**Commit:** `a57dfd5` on `main`
**Clone:** `git clone https://github.com/SuperInstance/plato-server`

## What It Is

Standalone knowledge system — SQLite-backed HTTP server for room-based Q&A tile management with optional Matrix fleet sync. Pure Python stdlib, zero runtime dependencies. Runs on port 8847.

## What Was Done

### CI Fix
- **Removed `|| true`** from pytest step — tests now gate merges
- Removed non-gating flake8 pass (`--exit-zero`) — lint failures now block
- CI runs on Python 3.10/3.11/3.12 matrix

### License
- MIT — already present, verified ✓

### Packaging (pyproject.toml)
- Fixed broken entry point: was `plato_server = "test_server:main"` (function didn't exist) → now `plato-server = "server:main"`
- Added proper description, keywords, classifiers, project URLs
- Added `[tool.hatch.build]` section
- Added `__main__.py` fix so `python -m plato-server` works

### Entry Point Fix
- Added `main()` function to `server.py` (was only runnable via `if __name__` block)
- Fixed `__main__.py` to import from `server` not `test_server`

### Publish Workflow
- Added `.github/workflows/publish.yml` — PyPI trusted publishing on GitHub release

### README
- Fixed dependency: was "python3, flask" → "python3 (stdlib only)"

### .gitignore
- Expanded: build artifacts, venvs, data files, .env

## Test Results

```
2 passed in 0.05s
```

Tests cover: tile submit/read/search/stats cycle + gate validation (blocked words, min answer length).

## How to Use

```bash
# Install
pip install -e .

# Run
plato-server                    # starts on :8847
PLATO_PORT=9000 plato-server    # custom port

# Or Docker
docker run -p 8847:8847 -v plato-data:/data ghcr.io/superinstance/plato-server

# Submit knowledge
curl -X POST http://localhost:8847/submit -H "Content-Type: application/json" \
  -d '{"room":"my-project","domain":"arch","question":"Why X?","answer":"Because Y, specifically Z.","agent":"me"}'

# Search
curl http://localhost:8847/search?q=architecture
```

## Genuinely Usable?
Yes. Pure stdlib (no dependencies to break), real HTTP API, SQLite persistence, Docker support. Someone can clone and run in 30 seconds.
