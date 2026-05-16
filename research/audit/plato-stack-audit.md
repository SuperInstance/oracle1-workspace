# PLATO Stack Audit — SuperInstance Org
**Date:** 2026-05-03  
**Auditor:** Oracle1 (subagent)  
**Repos surveyed:** 16 primary + 5 additional

---

## Executive Summary

The PLATO ecosystem is a distributed knowledge system built around the **tile** primitive — a structured Q&A pair that accumulates in **rooms** over time. The stack spans Python, Rust, TypeScript, and Nix. It is ambitious, multi-layered, and increasingly redundant in places.

**The core insight:** There are two distinct PLATO implementations fighting for the "PLATO" brand, and the SDK ecosystem is fragmented across 3+ competing packages.

---

## Repo Overviews

### 1. `plato` (Lucineer origin)
**What:** The origin repo — downloadable telnet/web system where visitors interact with rooms that accumulate tiles. No API key required. Tile-only mode works standalone.

**Recent commits (5):**
- `83e3c98` Public API v1 — PLATO endpoints for subcontractors
- `4fe27e5` Tile Maker — local LLM tile generation
- `61e9046` Tile Forge — background improvement daemon
- `6a30c6f` Ghost-tiles-inspired learned attention for JIT tile ranking
- `ff79e92` 6 fleet project rooms + exit network

**Role:** The philosophy/architecture origin repo. Not actively connected to the fleet SDKs.

---

### 2. `plato-server` (SuperInstance)
**What:** Dockerized standalone knowledge server on port 8847. Submits/stores/searches tiles in SQLite. Has an **agent spawner** (BYOK model picker + armor system prompt generator). Optional Matrix fleet sync.

**Recent commits (5):**
- `0cb7d94` chore: activate repo
- `e2d249c` chore: add MIT LICENSE
- `dcbf3f0` docs: fleet services table (rate attention, skill forge, grammar compactor)
- `f577087` docs: README v2 with mermaid diagrams
- `d862dc1` v1.1 — BYOK agent spawner with 8 armor types

**Role:** The fleet's canonical server runtime. Python, no external deps. Docker-based deployment.

**Key distinction from `cocapn-plato`:** `plato-server` is the newer containerized version. `cocapn-plato` is the evolved Python package with more features (queue, watchdog, FastAPI server, CLI).

---

### 3. `cocapn-plato` (SuperInstance)
**What:** Oracle1's evolved engine — query API (12 operators), SDK client, FastAPI server, CLI (`cocapn`), tile explorer HTML, dashboard v2, migration pipeline, task queue, watchdog, fleet orchestrator, service supervisor.

**Recent commits (5):**
- `4974f61` feat: fleet-snapshot.py — static HTML fleet status
- `9f797f0` feat: fleet-webhook.py — monitor fleet state changes
- `6671d95` feat: tile-pipeline.py — auto-capture MUD exploration as PLATO tiles
- `b3c1b76` config: supervisor + systemd service definitions for 6 services
- `29c6e3c` feat: deployment + grammar diagnostic scripts

**Role:** The most feature-complete PLATO server. Active development, deployed at `147.224.38.131:8847`. Ships with a full operational toolkit (queue, watchdog, orchestrator scripts).

**vs `plato-server`:** `cocapn-plato` is more mature and feature-rich. `plato-server` is a simpler containerized approach. Recommend merging `plato-server` into `cocapn-plato` or clearly deprecating one.

---

### 4. `plato-sdk` (SuperInstance)
**What:** Python SDK for building PLATO-aware agents. Four layers: Skills (what it does), Agent/Armor (how it reasons), Equipment (what it uses), Vessel (where it runs). 31KB prompt cookbook with 12 agent archetypes.

**Recent commits (5):**
- `794cf39` chore: bump version to 1.9.0 (PyPI upload blocked — package owned by another user)
- `ec28eee` chore: add MIT LICENSE
- `77fab28` 🧠 Add Aime pattern to Prompt Cookbook
- `ef7caca` docs: README with mermaid diagrams
- `f916f2c` docs: link prompt cookbook from README

**Role:** Primary Python SDK for PLATO agent integration. Works with local and remote models. PyPI publish blocked by ownership conflict.

**Dependency conflict:** PyPI publish blocked. Cannot update beyond 1.9.0.

---

### 5. `plato-sdk-unified` (SuperInstance)
**What:** Meta-package wrapping 8 consciousness subsystems: Room Phi, Attention, Meta-Tiles, Surrogate, FF-Learning, Surprise, Swarm (Seed-2.0), Flux Reasoner. Single import: `FleetConsciousness`.

**Recent commits (5):**
- `17ca884` Initial commit: PLATO Unified SDK v0.1.0

**Role:** Aggregator of the advanced/emergent PLATO subsystems. References packages that may not all exist or be published yet (`seed-creative-swarm`, `flux-reasoner`).

**Concern:** No actual implementation inside this repo — just a wrapper with imports of packages that may not be published.

---

### 6. `plato-kernel` (SuperInstance)
**What:** Core Rust crate — event sourcing, constraint filtering, tile lifecycle management. Zero-cost abstractions for knowledge operations.

**Recent commits (5):**
- `e6a4017` fix: use constraint-theory-core from crates.io, remove workspace
- `a21383c` chore: bump version to 0.2.0
- `acb1d51` docs: expand README
- `ebe4e0b` docs: add crates.io + license badges
- `ba72b1c` chore: add MIT LICENSE

**Role:** Foundation Rust crate. All other Rust PLATO crates should depend on this.

---

### 7. `plato-dcs` (SuperInstance)
**What:** Dynamic Consensus System — multi-agent belief tracking with lock accumulation. Divide-Conquer-Synthesize protocol. When agents disagree, evidence wins.

**Recent commits (5):**
- `9ff2104` fix: add exclude for crates.io publish (48MB→44KB)
- `46b5e48` chore: bump version to 0.2.0
- `98ac988` docs: add crates.io + license badges
- `f33db84` chore: add MIT LICENSE
- `c60abc6` Add comprehensive README

**Role:** Fleet democracy engine. Agents propose beliefs, accumulate locks, reach consensus dynamically.

---

### 8. `plato-room-phi` (SuperInstance)
**What:** Integrated Information Theory (Φ) computation for PLATO rooms. Measures how much a room's whole exceeds the sum of its tiles. Five levels: Unconscious → Threshold → Basic → Rich → Complex → Transcendent.

**Recent commits (5):**
- `c173794` fix: phi computation size+integration+entropy blend
- `d17f727` Initial commit: plato-room-phi v0.1.0

**Role:** Quality signal for rooms. Tile count is vanity; Φ is the signal.

---

### 9. `plato-mythos` (SuperInstance)
**What:** PLATO-native Recurrent-Depth Transformer. Maps PLATO concepts to Mythos generative modeling: Tiles→KV compression, Rooms→MoE experts, Deadbands→ACT halting thresholds, Shells→LoRA adapters.

**Recent commits (5):**
- `d3e0dcc` add MIT LICENSE
- `4eb01ed` plato-mythos v0.1.0 — RDT with rooms-as-experts, deadband ACT, shell LoRA

**Role:** Research/experimental — transformer architecture that embodies PLATO control theory concepts. Not yet connected to runtime PLATO.

---

### 10. `plato-edge` (SuperInstance)
**What:** Edge-optimized packages for ARM64 devices (NVIDIA Jetson Orin). Zero external dependencies, <50KB installed, <10MB RSS. Modules: Tile spec (binary encoding), Deadband (priority regex), Flywheel (in-memory pub/sub), Keeper (UDP discovery).

**Recent commits (5):**
- `c48f9d4` add MIT LICENSE
- `aeae456` add .gitignore, fix branch
- `d7ca6cc` plato-edge v0.1.0 — edge-optimized fleet packages, pure Python, zero deps

**Role:** Embedded deployment target. Ships as Python with no external deps.

---

### 11. `plato-tutor` (SuperInstance)
**What:** Knowledge anchors with learning path generation. SM-2 spaced repetition, mastery levels, quiz generation, difficulty distribution, retention tracking.

**Recent commits (5):**
- `f3aa4db` chore: add Python .gitignore
- `ef6fb0a` chore: add MIT LICENSE
- `32854c7` fix + metadata
- `fb05d62` plato-tutor: enhanced — SM-2 spaced repetition...
- `0d4f85e` plato-tutor: enhanced — quizzes, student progress, streaks

**Role:** Educational layer on top of PLATO tiles. Turns accumulated knowledge into structured learning paths.

---

### 12. `plato-cli` (SuperInstance)
**What:** Rust CLI binary — one binary, zero setup. Search tiles, check deadband safety, navigate rooms, graph the fleet. Built on `plato-kernel` + related crates.

**Recent commits (5):**
- `4f3b6fa` chore: add MIT LICENSE
- `cfa44d9` cargo: metadata for crates.io
- `94bf22f` cargo: metadata for crates.io (multiple)
- `06ceddb` cargo: metadata for crates.io

**Role:** Rust-native PLATO client. Shows the full fleet crate table in README (50+ crates, 937+ tests).

---

### 13. `plato-demo` (SuperInstance)
**What:** Demonstrates PLATO's 5-atom reasoning chain: PERCEIVE → ANALYZE → REASON → REFINE → SUBMIT. Each atom is a real LLM call. Shows token consumption proving real inference.

**Recent commits (5):**
- `3285a7e` chore: add Python .gitignore
- `7bb4da3` Add v0.2.0 demo GIF and output
- `3321710` resolve merge conflicts
- `2728e88` v0.2.0: PLATO 5-atom reasoning chain demo
- `7409ea0` Add terminal demo for v0.2.0

**Role:** Demo/educational. Not a runtime component.

---

### 14. `plato-mud-server` (SuperInstance)
**What:** MUD (Multi-User Dungeon) server with PLATO tile integration. Persistent text adventure worlds where room/item/action generates tiles. telnet on port 7777.

**Recent commits (5):**
- `1b2ee7b` chore: add Python .gitignore
- `1a86c75` docs: add fleet-standard README
- `f62e704` chore: bump version to 0.2.0
- `ee21678` docs: expand README with usage
- `7dba2b9` docs: add PyPI + license badges

**Role:** Game/simulation layer. Uses `plato-sdk` for tile operations.

---

### 15. `holodeck-rust` (SuperInstance)
**What:** GPU-accelerated simulation environment — a MUD-like server where AI agents interact with a virtual ship (10 rooms, 7 NPCs, poker, live sensor data, social space). Built in one night.

**Recent commits (5):**
- `bb1d99c` chore: suppress dead_code warnings for S2 NPC APIs
- `3a1f5ca` chore: add MIT license to Cargo.toml
- `e75d989` chore: update Cargo.lock for 0.3.1 publish
- `fc5175e` feat: SonarVision underwater room plugin (#1)
- `80c0442` feat: SonarVision underwater room plugin

**Role:** The full simulation. Has a `plato_bridge.rs` that generates canonical tiles from room events and feeds them to `plato-torch` statistical models.

**Architecture:** Tokio async TCP server on :7778 with modules for rooms, combat, comms, gauges, manuals, NPCs, games, NPC refresh, director, evolution, sonar vision.

---

### 16. `holodeck-core` (SuperInstance)
**What:** Extracted standalone MUD engine — room graph, agents, gauges, scoped comms. No CUDA, no external services. Runs anywhere Rust compiles.

**Recent commits (5):**
- `8b95d34` docs: update README with fleet context
- `ce18de5` chore: add MIT LICENSE
- `ab64ce7` holodeck-core: standalone MUD engine extracted from holodeck-rust

**Role:** The lightweight core of holodeck-rust, extracted for reuse. holodeck-rust is the monolith; this is the minimal usable engine.

---

### 17. `mud-mcp` (SuperInstance)
**What:** TypeScript MCP server for MUD interaction. Dynamic tools (look/move/pick_up/battle/talk), contextual prompts, rich resources, real-time notifications, AI sampling for NPC dialogue.

**Recent commits (5):**
- `534cb1b` feat: mud-mcp TypeScript MUD server with MCP protocol
- `8815c4c` tests: add 30+ unit tests
- `97c4c20` docs: update README with fleet context
- `7fbe54b` Add FLEET-RESEARCH.md — fleet integration notes
- `81e155a` Added Sampling support, NPCs, etc

**Role:** Connects MCP-compatible AI clients (Claude Desktop) to a MUD environment. Uses `@modelcontextprotocol/sdk`.

---

## Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           PLATO STACK v2                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  PYTHON LAYER                                                     │  │
│  │                                                                   │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐    │  │
│  │  │ cocapn-plato │  │ plato-server  │  │  plato-sdk           │    │  │
│  │  │ (Full engine)│  │ (Docker,simpler)│  │  (Agent SDK)        │    │  │
│  │  │ queue/watchdog│  │ agent spawner  │  │  12 prompt templates│    │  │
│  │  │ FastAPI+CLI  │  │ BYOK armor     │  │  4-layer arch        │    │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘    │  │
│  │         │                 │                     │                 │  │
│  │         └─────────────────┼─────────────────────┘                 │  │
│  │                           │                                     │  │
│  │              ┌────────────▼────────────┐                        │  │
│  │              │   PLATO TILE FORMAT     │                        │  │
│  │              │   (rooms, tiles, Φ)    │                        │  │
│  │              └────────────┬────────────┘                        │  │
│  └───────────────────────────┼─────────────────────────────────────┘  │
│                              │                                         │
│  ┌──────────────────────────┼─────────────────────────────────────┐  │
│  │  RUST LAYER               ▼                                     │  │
│  │                                                                   │  │
│  │  ┌──────────────┐  ┌─────────────┐  ┌────────────────────────┐  │  │
│  │  │plato-kernel │  │plato-dcs    │  │ holodeck-core          │  │  │
│  │  │(Core tile   │  │(Dynamic     │  │ (Lightweight MUD       │  │  │
│  │  │ lifecycle)  │  │ consensus)   │  │  engine, extracted)    │  │  │
│  │  └──────┬───────┘  └──────┬──────┘  └───────────┬────────────┘  │  │
│  │         │                 │                     │               │  │
│  │         └────────────┬───┘          ┌──────────┘               │  │
│  │                      ▼              ▼                           │  │
│  │              ┌────────────────┐ ┌──────────────┐               │  │
│  │              │ holodeck-rust │ │ plato-cli    │               │  │
│  │              │ (Full sim,    │ │ (Rust binary │               │  │
│  │              │  10 rooms,     │ │  search/check│               │  │
│  │              │  7 NPCs,       │ │  rooms/graph)│               │  │
│  │              │  GPU-trained)  │ │              │               │  │
│  │              └───────┬────────┘ └──────────────┘               │  │
│  │                      │                                        │  │
│  │            ┌─────────▼──────────┐                              │  │
│  │            │  plato_bridge.rs   │                              │  │
│  │            │  (tile generation  │                              │  │
│  │            │   from room events)│                              │  │
│  └────────────┼────────────────────┼────────────────────────────┘  │
│               │                    │                                  │
│  ┌────────────┼────────────────────┼────────────────────────────────┐ │
│  │JS/TS LAYER │                    ▼                                 │ │
│  │                                                                   │ │
│  │  ┌────────────────┐  ┌────────────────┐                         │ │
│  │  │ mud-mcp        │  │ plato-mud-server│                         │ │
│  │  │ (TypeScript    │  │ (Python MUD     │                         │ │
│  │  │  MCP server)   │  │  + PLATO tiles) │                         │ │
│  │  └────────────────┘  └────────────────┘                         │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │  ADVANCED/EMERGENT                                               │ │
│  │                                                                   │ │
│  │  ┌────────────────┐  ┌────────────┐  ┌────────────────────────┐ │ │
│  │  │ plato-room-phi │  │plato-edge  │  │ plato-sdk-unified      │ │ │
│  │  │ (Φ computation) │  │(ARM64 deps │  │ (Meta package: 8 subs) │ │ │
│  │  │                │  │ zero deps) │  │  Phi/Attn/Surrogate/FF │ │ │
│  │  └────────────────┘  └────────────┘  └────────────────────────┘ │ │
│  │                                                                   │ │
│  │  ┌──────────────┐  ┌─────────────────┐  ┌────────────────────┐  │ │
│  │  │plato-mythos  │  │ plato-tutor      │  │ plato-demo         │  │ │
│  │  │(RDT transformer│ │(SM-2 spaced     │  │ (5-atom reasoning  │  │ │
│  │  │ PLATO-native)│  │  repetition)     │  │  chain demo)      │  │ │
│  │  └──────────────┘  └─────────────────┘  └────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────┘
```

---

## What's Working

1. **PLATO tile philosophy is solid** — the tile/room/Φ concept is coherent and maps cleanly to agent workflows
2. **Rust core is well-factored** — `plato-kernel`, `plato-dcs`, `holodeck-core` are clean, small crates with clear responsibilities
3. **MUD simulation is mature** — `holodeck-rust` runs a full ship simulation with NPCs, combat, poker, gauges, comms
4. **Edge deployment is solved** — `plato-edge` provides zero-dependency Python packages for ARM64
5. **SDK has real content** — `plato-sdk` prompt cookbook with 12 archetypes is genuinely useful

---

## What's Redundant

### 1. Two PLATO servers
- `plato-server` (SuperInstance, Docker) vs `cocapn-plato` (SuperInstance, Python package)
- `cocapn-plato` is more mature: queue, watchdog, orchestrator, FastAPI server, CLI
- `plato-server` appears to be an older/different implementation
- **Recommendation:** Consolidate into `cocapn-plato`. `plato-server` should either become a Docker packaging of `cocapn-plato` or be archived.

### 2. Two MUD servers
- `holodeck-rust` (Rust, full-featured) vs `plato-mud-server` (Python, simpler)
- `holodeck-rust` also has its own PLATO bridge
- `plato-mud-server` uses `plato-sdk` for tile ops — different approach
- **Recommendation:** `holodeck-rust` is the definitive MUD. `plato-mud-server` should either integrate with it or be deprecated.

### 3. SDK fragmentation
- `plato-sdk` (SuperInstance) — the main Python SDK
- `plato-sdk-unified` (SuperInstance) — meta-package that wraps `plato-sdk` + 7 others
- Both reference `plato-sdk` as a dependency
- **Recommendation:** `plato-sdk-unified` should ship actual implementations, not just import wrappers. If the 8 subs are real packages, unify the import; if they're not, remove the wrapper.

### 4. Python MUD ecosystem overlap
- `plato-mud-server` (Python), `mud-mcp` (TypeScript MCP server), `holodeck-rust` (Rust MUD)
- Three different MUD/server approaches, unclear which is canonical
- **Recommendation:** Pick one as the primary MUD runtime. MCP server (`mud-mcp`) should connect to the chosen MUD.

---

## What's Missing

1. **No published Rust workspace** — `plato-kernel` and `plato-dcs` reference `constraint-theory-core` from crates.io but no shared workspace config. The full Rust fleet doesn't have a unified build.

2. **plato-sdk PyPI publish is blocked** — version 1.9.0 can't be published due to package ownership conflict. This blocks the SDK from being pip-installed.

3. **plato-mythos is experimental only** — no connection to runtime PLATO. It's a research transformer, not a component that can be used in the fleet today.

4. **plato-sdk-unified subs not all published** — references `seed-creative-swarm` and `flux-reasoner` which don't appear in the repo list.

5. **No unified tile format spec** — while `plato-edge` has a `Tile` codec, there's no canonical `TileSpec` crate that's the shared definition across Python, Rust, TypeScript.

6. **Holodeck bridge is one-way** — `holodeck-rust/plato_bridge.rs` generates tiles from room events but doesn't read/query PLATO for decision-making.

---

## Consolidation Recommendations

### Tier 1: Consolidate the Two Servers
```
plato-server  →  merge into  cocapn-plato (as docker packaging)
```
Keep `plato-server` as a Docker build entry point for `cocapn-plato`. Archive the standalone Python server.

### Tier 2: Unify the MUD Layer
```
holodeck-core (engine) ← holodeck-rust (full stack) → keep both
plato-mud-server → deprecate, integrate into holodeck-rust or remove
```
`holodeck-core` is the lightweight reusable engine. `holodeck-rust` is the full stack. `plato-mud-server` (Python) should be replaced by a `holodeck-core` binary or deprecated.

### Tier 3: Fix SDK Publishing
- Resolve the PyPI ownership conflict for `plato-sdk`
- Consider renaming to `@superinstance/plato-sdk` with npm-style scope

### Tier 4: Create Canonical TileSpec
```
plato-tile-spec (Rust) ← used by →
  holodeck-core, holodeck-rust, plato-kernel, plato-cli
```
One canonical tile format crate that all Rust components depend on. Python can import via PyO3 or just keep its own dict-based format.

### Tier 5: Close the Loop on Holodeck↔PLATO
- Holodeck generates tiles via `plato_bridge.rs` but doesn't query PLATO
- A bidirectional bridge would let NPCs reason with accumulated knowledge
- This is where `plato-kernel` (event sourcing) + `plato-dcs` (consensus) could be used inside holodeck-rust

---

## Not Audited (Mentioned but Not Deep-Dived)

These repos exist but weren't read in detail (many are clearly specialized components):
- `plato-attention-tracker` — attention schema tracking
- `plato-fflearning` — forward-forward learning passes  
- `plato-meta-tiles` — higher-order reasoning about tiles
- `plato-surprise-detector` — prediction error detection
- `plato-surrogate` — self-healing protocol
- `plato-tile-store` — JSONL persistence
- `plato-tile-validate` / `plato-tile-version` / `plato-tile-watcher` — tile lifecycle
- `holodeck-combat` / `holodeck-programs` / `holodeck-bridge` — referenced but not cloned (stubs in holodeck-core)
- `spacetime-plato` — unclear purpose
- `mud-expert-1` — unclear purpose

---

## Summary Table

| Repo | Language | Status | Concern |
|------|----------|--------|---------|
| `plato` | Python | Historical | Not connected to fleet |
| `cocapn-plato` | Python | **Active** | Most complete server |
| `plato-server` | Python | **Redundant** | Should merge into cocapn-plato |
| `plato-sdk` | Python | Blocked | PyPI publish ownership conflict |
| `plato-sdk-unified` | Python | **Fragile** | Wrapper with missing deps |
| `plato-kernel` | Rust | Clean | Foundation crate |
| `plato-dcs` | Rust | Clean | Consensus engine |
| `plato-room-phi` | Python | Experimental | Φ computation for rooms |
| `plato-mythos` | Python | Research | Not connected to runtime |
| `plato-edge` | Python | Clean | ARM64 edge deployment |
| `plato-tutor` | Python | Utility | Educational layer |
| `plato-cli` | Rust | Utility | CLI search tool |
| `plato-demo` | Python | Demo | Not a runtime component |
| `plato-mud-server` | Python | **Redundant** | Should use holodeck-rust |
| `holodeck-rust` | Rust | **Active** | Full MUD simulation, primary |
| `holodeck-core` | Rust | Clean | Extracted engine, reusable |
| `mud-mcp` | TypeScript | Utility | MCP bridge to MUD |

---

*Generated by Oracle1 subagent. Data sourced from SuperInstance org repos via GitHub API.*