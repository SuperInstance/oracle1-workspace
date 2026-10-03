# Deep Audit: exocortex

**Repo:** SuperInstance/exocortex  
**Tier:** 2 — Near-Ready 🔧  
**Language:** Python  
**License:** None ⚠️  
**Audited:** 2026-07-12  

---

## Overview

Persistent cognitive substrate for multi-agent systems. S3-compatible distributed memory with TUI interface, compute bus, shadow agents, and protocol layer.

## Metadata

| Metric | Value |
|--------|-------|
| Stars | 0 |
| Forks | 0 |
| Size | 103 KB |
| Open Issues | 0 |
| Last Pushed | 2026-06-08 |
| Python | >=3.10 |
| Dependencies | textual, FastAPI, uvicorn, httpx, numpy |

## Structure

```
exocortex/
├── src/
│   ├── core/           # Core cognitive substrate
│   ├── memory/         # Memory persistence
│   ├── bus/            # Compute bus
│   ├── compute/        # Compute engine
│   ├── protocols/      # Communication protocols
│   ├── shadows/        # Shadow agents
│   ├── config/         # Configuration
│   ├── tui/            # Terminal UI (textual)
│   └── main.py         # Entry point
├── tests/
│   ├── test_core.py    # Core functionality tests
│   └── test_phase2.py  # Phase 2 tests
├── demo.py             # Demo script
├── .cortex.toml        # Configuration
├── Dockerfile
├── docker-compose.yml
├── .devcontainer/
├── pyproject.toml
├── AGENT.md
└── CI: ci.yml
```

## Dependencies

Substantial stack:
- **textual** >= 0.40 — Terminal UI framework
- **FastAPI** >= 0.115 — Web API
- **uvicorn** >= 0.34 — ASGI server
- **httpx** >= 0.28 — HTTP client
- **numpy** >= 1.24 — Numerical computing

Optional:
- **scikit-learn** >= 1.6 — ML support

## What It Needs

1. **LICENSE** — No license file. Must add one.
2. **Test expansion** — Only 2 test files for 8 modules (bus, compute, config, core, memory, protocols, shadows, tui)
3. **S3 compatibility verification** — Claims S3-compatible; test with actual S3 or MinIO
4. **Shadow agents documentation** — What are shadow agents? How do they work?
5. **Protocol documentation** — What protocols are supported?
6. **Performance testing** — Memory substrate latency benchmarks
7. **Docker CI** — Dockerfile exists; add container testing to CI

## Verdict

The module structure is impressive (8 subsystems) and the dependency stack (FastAPI, textual, numpy) shows real application design. But 2 tests for 8 modules is severely under-tested. The concept of "persistent cognitive substrate" is genuinely interesting for multi-agent systems.
