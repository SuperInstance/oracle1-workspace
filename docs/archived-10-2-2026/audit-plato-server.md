# Deep Audit: plato-server

**Repo:** SuperInstance/plato-server  
**Tier:** 1 — Ship-Ready ✅  
**Language:** Python  
**License:** MIT  
**Audited:** 2026-07-12  

---

## Overview

Standalone PLATO knowledge system server. SQLite-backed HTTP server for room-based Q&A tile management with optional Matrix fleet sync. Each PLATO instance runs locally with its own database and can optionally federate.

## Metadata

| Metric | Value |
|--------|-------|
| Stars | 2 |
| Forks | 0 |
| Size | 50 KB |
| Open Issues | 0 |
| Last Pushed | 2026-05-09 |
| Python | >=3.10 |
| Dependencies | stdlib only |

## Structure

```
plato-server/
├── server.py          # Main server (HTTP + SQLite + Matrix sync)
├── agent.py           # Agent integration
├── __main__.py        # Entry point
├── test_server.py     # Test suite
├── pyproject.toml     # Build config (hatchling)
├── Dockerfile         # Container deployment
├── start.sh           # Quick start script
├── .github/workflows/
│   └── ci-python.yml  # CI
└── README.md
```

## API

```
GET  /                — System status
GET  /rooms           — All rooms with tile counts
GET  /room/{name}     — Room details + recent tiles
GET  /tiles/recent    — Last 50 tiles across all rooms
GET  /search?q=X      — Keyword search
POST /submit          — Submit a tile {domain, question, answer, agent}
GET  /sync/status     — Matrix federation status
POST /sync/toggle     — Enable/disable fleet sync
GET  /stats           — Usage statistics
```

## Test Suite

2 test functions:
1. **test_submit_and_read** — Full CRUD cycle: submit tile → read rooms → read tiles → search → stats
2. **test_gate_validation** — Gate rules: too-short answers rejected, blocked words rejected, valid answers accepted

Tests use in-memory SQLite (`:memory:`) — clean and fast.

## CI

- **ci-python.yml** — Matrix: Python 3.10/3.11/3.12. Runs flake8 + pytest.
- Note: pytest uses `|| true` — **tests don't gate merges. Fix this.**

## Key Features

- Thread-safe SQLite with proper locking (`self.lock`)
- Tile hashing with SHA-256
- Gate validation blocks absolute language ("always", "never", "impossible", "guaranteed", "nobody")
- Minimum answer length enforcement (20 chars)
- Optional Matrix federation for fleet sync
- Instance identification by hostname

## What It Needs

1. **Fix CI** — Remove `|| true` from pytest line
2. **More tests** — Only 2 test functions; need edge cases (empty rooms, concurrent access, search edge cases)
3. **Authentication** — HTTP API has no auth
4. **Rate limiting** — No protection against abuse
5. **Matrix sync testing** — Federation code exists but untested
6. **PyPI publication** — Properly packaged but not published
7. **API documentation** — OpenAPI/Swagger spec

## Verdict

**Functional, runnable knowledge server.** Clone it, `pip install -e .`, `python server.py`, and you have a working PLATO instance. The code is clean Python stdlib (no dependencies needed). Needs auth and more tests for real deployment.
