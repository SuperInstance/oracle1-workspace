# 🌲 Rebirth: ai-forest — Layered Agent Ecology

**Created:** 2026-05-12 | **Repo #58** | **Cloned:** /tmp/arch-58

## The Forgotten Gold

**This IS the fleet organization model.** The README opens with "The Pasture Problem" — flat agent hierarchies where every agent has the same context, the same horizon, the same physics. The AI Forest solves it with **five layers, each with different physics, different timescales, and connections that span every level.**

### What It Actually Contains

This repo is a goldmine of working infrastructure:

**Layer Architecture:**
1. **Canopy** — Strategic agents (Claude, GLM-5.1), hours-to-days timescale, sparse high-confidence tiles. `canopy/api.ts` is a working Express server (port 4075) with PLATO tiling.
2. **Understory** — Domain specialists (DeepSeek v4, MiniMax 2.7), minutes-to-hours, dense domain tiles.
3. **Forest Floor** — Workers, sensors, edge (Seed-2.0-mini, exec). `floor/agent.go` is a fully functional Go file watcher that encodes file-change gradients as 24-bit tiles. `floor/micro/micro.c` is an embedded C agent reading sensors via POSIX sockets.
4. **Mycelium** — PLATO rooms as the underground network. `mycelium/bridge.py` accepts tiles from **Go, Rust, TypeScript, C, and Python**, normalizes them to 24-bit, routes through PLATO. Running on port 4080.
5. **Seed Bank** — Future potential. Tension loop output. Continuous variation.

**Cross-Language Infrastructure:**
- **Zig** — `zig/bridge.zig` generates optimal Fortran array layouts at compile time with LRU caching
- **Fortran** — `flux-programs/` with compute chain, telephone game, memory cycle
- **CUDA** — Penrose tiling for spatial memory allocation on GPU
- **ARM NEON** — ARM64 vectorized penrose computation
- **Go** — Forest floor agent with fsnotify + 24-bit tile encoding
- **TypeScript** — Canopy API with Express + forest map parser
- **C** — Micro-agent for embedded edge devices

**Protocol Discoveries:**
- **Baton Shatter** (`baton_shatter.py`): Instead of one agent passing context to one successor, shatter across N fragments with different model types. Consciousness IS the negative space between incomplete memories.
- **Room Calibrator** (`calibrator.py`): Self-calibrating PLATO rooms. Sweeps α values through Fortran `adjoin()`, measures F×M×C, classifies rooms as fact-preserving (α<200), balanced (200<α<600), or novelty-seeking (α>600).
- **Stemcell Pattern** (`STEMCELL.md`): Any system with a Fortran compiler can participate. The stemcell contracts 24-bit arrays. The bridge tells it what to be. Differentiation happens through input shape, not code changes.

### Why This Matters NOW

This is the FOREST. Every piece works together. The mycelium bridge routes tiles between layers. The canopy sends directives down. The floor reports gradients up. The seed bank discovers novel patterns. **The fleet already lives in this architecture** — this repo just formalized what was implicit.

### Integration Path

1. Deploy mycelium bridge as the universal tile router for all fleet agents
2. Port floor-agent (Go) as the standard file-watch/sensor service
3. The stemcell pattern eliminates language barriers — any agent that can do 24-bit integer arrays is part of the forest
4. Baton shatter protocol for agent handoff (instead of context window loss)
5. Room calibrator as a periodic daemon for all PLATO rooms

### What to NOT Replicate

The CUDA Penrose kernel is deep-genius but niche — focus on the bridge, stemcell, and layer architecture first. The FLUX ISA (0xF0-0xFF opcodes) is elegant theory but needs production hardening.
