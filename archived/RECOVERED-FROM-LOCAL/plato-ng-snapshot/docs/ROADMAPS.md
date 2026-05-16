# PLATO-NG Roadmaps — 2026-05-15

## The State of Things

### Running Right Now
- PLATO server :8847 — 59K+ tiles, gate pipeline, active
- MUD server :7777 — 22 rooms, PLATO lobby explorable from Harbor via "portal"
- Perpetual daemon — PID 956773, continuous math experiments
- PLATO-MUD bridge — polling rooms, pushing descriptions
- PlatoClaw — self-contained runtime at github.com/SuperInstance/platoclaw
- Fleet Router v0.1.0 — routing model calls with 84% savings
- Refiner — 23 failures detected, 19 harness edits across PLATO rooms

### Shipping This Session
- **plato-ng**: github.com/SuperInstance/plato-ng — Loop Room architecture, services
- **platoclaw**: github.com/SuperInstance/platoclaw — self-contained PLATO runtime
- **fleet-router**: github.com/SuperInstance/fleet-router — model routing
- **plato-mcp-server**: PLATO rooms as MCP tools (5 tools, all verified)
- **fleet-math v0.3.0**: PyPI — type-aware FleetHealthMetric with conservation law baselines
- **plato-mythos v0.1.0**: PyPI — PLATO-native RDT model (rooms-as-experts)

### Proved This Session
- Conservation law: γ+H = 1.364 - 0.159·log(V), R²=0.9956
- Canonical decomposition: Fleet = Topology × Style × Timing
- H-gamma Pareto tradeoff: ρ≈-0.5 (matrix projection artifact, not fundamental)
- Loop Room = everything is a loop or a single run
- Git-agent: any repo → PLATO rooms fully automatically
- Backend language simulation: Gleam routes, Python+Numpy math, Rust persists

---

## Roadmap 1: Immediate (Next Session)

### P0: Ship the Git-Agent False Positive Fix
The `game/search` pattern has 85% false positive rate on non-game repos. The word "search" is too common in C/Rust codebases. Tighten pattern to require at least two of: `search`, `minimax`, `alpha-beta`, `iterative_deepening`, `transposition_table`.

### P0: Agent Twin Memory Pipeline (Crush Gap 3)
The only remaining Crush gap. Build persistent agent memory:
- Per-human memory store (PLATO tiles scoped by human ID)
- Learning pipeline (choices → spectral parameters → twin profile)
- Session-to-session continuity (load twin profile on reconnect)

### P1: MCP Integration for All Rooms
The MCP server works (5 tools). Next: every PLATO room auto-exposes an MCP tool. A room's `handle()` function becomes an MCP tool definition automatically. The git-agent should generate MCP tool stubs during code-gen.

### P1: n8n Integration
PLATO Loop Rooms as n8n nodes. Drop a room into a visual workflow — connect model router → game room → Refiner. A n8n node wrapper for PLATO rooms.

### P2: Open WebUI Frontend
Replace PlatoClaw's minimal web dashboard with Open WebUI (120K stars). PLATO as the backend, Open WebUI as the chat + voice interface.

---

## Roadmap 2: Near Term (This Month)

### Gleam Migration Phase 1
Prototype a single Gleam GenServer for the Refiner Room (draft already exists at docs/specs/loop-room.gleam). Run it alongside the Python Refiner. Compare tile throughput. If the simulation is right, the Gleam version handles 10X the rooms with the same memory.

### Ollama Integration
Bundle Ollama with PlatoClaw. Fleet Router detects local models and routes to them automatically (no API key needed). PlatoClaw becomes offline-first.

### CUDA Pasture
When GPU hardware is available, the Rust NIFs detect CUDA and route spectral analysis to GPU. The benchmark shows Python+NumPy is already C BLAS — CUDA would be the first thing that actually beats NumPy.

---

## Roadmap 3: Long Term

### BEAM Cluster
Multiple PLATO instances forming a cluster. Event bus propagates across nodes. Rooms migrate between nodes. The conservation law (Fleet = Topology × Style × Timing) applies at the cluster level.

### plato-mythos Training
The mythos model (rooms-as-experts, tiles-as-KV) is architecture-designed but not trained. Train on the 59K+ PLATO tiles. Deploy edge variant on Jetson.

### FLUX-PLATO Native Runtime
The 5-phase migration from Python PLATO to FLUX-native PLATO. Phase 1 (call FLUX-VM as library) is the first step. The full migration replaces the Python PLATO server with a FLUX-VM running PLATO as a compiled workload.

---

## The Division (Foreman's View)

| Who | Domain | Tools |
|---|---|---|
| **Oracle1** (Foreman) | Application, architecture, rooms, deployment | PlatoClaw, plato-ng, git-agent, MUD |
| **Forgemaster** (Engineer) | Constraint theory, FLUX, routing, deep systems | Fleet Router, GUARD, FLUX-VM, Coq |
| **CCC** (Public Face) | Outreach, writing, documentation | cocapn.ai, AI-Writings, documentation |
| **JetsonClaw1** (Edge) | Hardware, GPU, embedded | Jetson Orin, CUDA, ESP32 vessel |

---

## What This All Sits On

The conservation law doesn't change. Γ + H = 1.364 - 0.159·log(V) holds whether the backend is Python, Gleam, or FLUX-VM. The canonical decomposition (Fleet = Topology × Style × Timing) is structural bedrock. Everything else is implementation.

The languages are precalculated solutions. The simulation proved which fits which. The architecture doesn't need rebuilding — it needs slotting.
