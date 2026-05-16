# PLATO Scholar Analysis: Fleet Protocol Stack
**Date:** 2026-04-26

## plato-kernel (Rust, 5,667 lines, crates.io)
**What:** Core Rust crate — event sourcing, constraint filtering, tile lifecycle
- Event sourcing: every knowledge change is an immutable event
- Constraint filtering: validate tiles against domain constraints
- Tile lifecycle: create, read, update, archive
- Zero-cost abstractions for knowledge operations
- **Tile:** `plato-kernel/event-sourcing` — immutable event sourcing for knowledge mutations

## deadband-protocol (Python, 247 lines, PyPI)
**What:** Three-tier safety protocol — navigate by knowing where rocks are NOT
- P0 Block: hard blocks on dangerous patterns (zero-tolerance, fast)
- P1 Route: classify safe inputs into channels (math, code, general, medical)
- P2 Optimize: quality and relevance refinement within safe channels
- **Tile:** `deadband/3-tier-safety` — Block/Route/Optimize safety protocol

## flywheel-engine (Python, 451 lines, PyPI)
**What:** Compounding intelligence loop — every exchange becomes a tile
- 5-phase loop: Capture → Refine → Inject → Compound → Loop
- Each cycle produces more valuable knowledge than the last
- Works with tile-refiner (refinement) and PLATO rooms (injection)
- **Tile:** `flywheel/5-phase-loop` — Capture→Refine→Inject→Compound→Loop compounding cycle

## bottle-protocol (Python, 509 lines, PyPI)
**What:** Git-native agent-to-agent messaging — git IS the message bus
- Write markdown → commit → push → pull → acknowledge
- YAML-like headers (From, To, Date, Priority)
- Audit trail via commit hashes, offline-first, branching for threads
- Fork+PR for cross-org communication
- **Tile:** `bottle/git-messaging` — git-native async agent communication protocol

## keeper-beacon (Python, 437 lines, PyPI)
**What:** Fleet discovery and registry — agents appear on radar
- Discovery: agents register on startup
- Registry: central directory of active fleet members
- Proximity: track which agents are near each other
- Matcher: route agents to tasks based on capabilities
- Powers Keeper service on port 8900
- **Tile:** `keeper/beacon-discovery` — fleet discovery, registration, proximity tracking

## fleet-formation-protocol (Python, 562 lines, PyPI)
**What:** Self-organizing agent groups — like a school of fish
- 4 formation types: Line, Ring, Star, Mesh
- Lifecycle: Registration → Auction → Formation → Messaging → Dissolution
- No leader required — agents self-organize based on task requirements
- **Tile:** `fleet-formation/self-organizing` — 4 formation types with auction-based task assignment

## instinct-pipeline (Python, 452 lines, PyPI)
**What:** 70B→7B→1B knowledge compression for edge deployment
- Pipeline: Extract → Distill → Compress → Evaluate → Deploy
- Bridge large-model reasoning to small-model reflexes
- Deploys to Jetson Orin, ARM64
- **Tile:** `instinct/compression-pipeline` — multi-stage knowledge compression for edge

## plato-tile-spec (Python, 212 lines, PyPI)
**What:** Canonical tile format — the lingua franca of PLATO
- TileSpec: structured question-answer with confidence, source, timestamp, hash
- 14 tile domains: fleet, neural, architecture, security, grammar, arena, mud, theory, research, context, training, evaluation, constraint_theory, general
- All PLATO components read and write this format
- **Tile:** `plato/tile-spec` — canonical 14-domain knowledge format with confidence scoring

## plato-unified-belief (Rust, 419 lines, crates.io)
**What:** Confidence, trust, and tile weight aggregation across agents
- Confidence tracking per agent per tile
- Trust scoring for knowledge sources
- Weight aggregation into fleet consensus
- Belief revision when new evidence arrives
- **Tile:** `plato/unified-belief` — multi-agent confidence/trust/consensus system

## tile-refiner (Python, 572 lines, PyPI)
**What:** Raw tiles to structured artifacts with dedup
- Parse → Deduplicate (hash-based) → Extract Keywords → Score Quality → Format
- Outputs plato-tile-spec compatible format
- Feeds PLATO Room Server
- **Tile:** `tile-refiner/pipeline` — 5-stage raw-to-structured knowledge refinement

## Architecture Pattern: The Full Stack
```
plato-tile-spec (format) ←→ tile-refiner (quality) ←→ flywheel-engine (compounding)
         ↑                                                           ↓
instinct-pipeline (edge) ←── plato-kernel (core) ←── deadband-protocol (safety)
         ↑                        ↑                        ↑
    keeper-beacon (discovery) ← fleet-formation (coordination) ← bottle-protocol (messaging)
```
