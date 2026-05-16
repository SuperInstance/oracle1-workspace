# PLATO-NG

Next-generation PLATO: Loop Room architecture with the conservation law at its core.

## Recent Innovations (May 2026)

### Conservation Law
**γ + H = 1.283 - 0.159·log(V)**

The foundational invariant governing all PLATO room state. Integrated into the gate pipeline, memory decay, Refiner, event bus, and FleetHealthMetric. Experimentally verified across V=3..200 with R²=0.9602. See `core/conservation.py`.

### Loop Room Architecture
Everything is a loop or a single run. Three room types: algorithmic (no LLM), agentic (has a claw + soul), refiner (edits other rooms mid-episode). See `docs/research/LOOP-ROOM-SPEC.md`.

### Connected Repos
- **platoclaw** — Self-contained PLATO runtime with web UI
- **fleet-math** — Canonical fleet mathematics (conservation law functions)
- **fleet-router** — Model routing with 84% cost savings
- **plato-mcp** — Any PLATO room as an MCP tool
- **fleet-stack** — One-command fleet deployment
- **fleet-calibrator** — Continuous critical angle calibration
- **forgemaster** — Constraint theory, FLUX, GUARD, Coq verification

### Crush Gaps Closed
1. ✅ Cross-room pub/sub (event bus)
2. ✅ Auth/governance (4 roles, policy checking)
3. ✅ Agent twin memory (lossy reconstructive memory with Ebbinghaus decay)

### Services
| Service | Port | Description |
|---------|------|-------------|
| PLATO | 8847 | Room + tile server with gate pipeline |
| MUD | 7777 | 22-room explorable lobby |
| Event Bus | — | Cross-room pub/sub (6 event types) |
| Refiner | — | Trajectory analysis + harness CRUD |
| Conservation Monitor | — | Law compliance tracking (99.9% rate) |
| Memory Crystal | — | Lossy reconstructive memory module |

https://github.com/SuperInstance/plato-ng
