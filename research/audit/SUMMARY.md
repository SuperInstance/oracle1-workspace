# Research Session: audit

Original size: 141 KB

# plato-stack-audit.md
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

**Key distinction from `cocapn-plato`:** `plato-server` is the newer containerized version. `cocapn-plato`

---

# plato-variant-consolidation.md
# PLATO Variant Consolidation — Decision Document
**Date:** 2026-05-03
**Auditor:** Oracle1 (subagent)
**Repos reviewed:** plato-kernel, plato-dcs, plato-mythos, plato-edge

---

## Executive Summary

Four PLATO variant repos exist under SuperInstance — all published to crates.io and/or PyPI, all last updated within 7 days (April 27, 2026). They are **not** redundant with each other; each targets a different deployment layer. Consolidation into one crate is **not recommended**. They should be kept as separate packages with clarified roles.

---

## Variant Summaries

### 1. `plato-kernel` (Rust)

| Field | Value |
|-------|-------|
| **crates.io** | plato-kernel 0.2.0 |
| **Language** | Rust |
| **Last commit** | 2026-04-27 (6 days ago) |
| **Description** | Core state machine — DCS flywheel, belief scoring, tile processing, deadband governance |
| **Tests** | No test files visible in repo (single `belief.rs` + `constraint_engine/` + `deadband.rs` + `tile.rs` + `lib.rs` — unit structure only, no `#[cfg(test)]` confirmed) |
| **PLATO-server link** | **None.** Pure Rust foundation crate. Not connected to the Python server on port 8847. Other Rust crates (`plato-cli`, `plato-dcs`) depend on this. |
| **Purpose** | Foundation: event sourcing, constraint filtering, tile lifecycle, belief state machine |

**Key differentiator:** The only Rust-level tile lifecycle and belief engine. All other Rust PLATO crates should build on this. Zero Python involvement.

---

### 2. `plato-dcs` (Rust)

| Field | Value |
|-------|-------|
| **crates.io** | plato-dcs 0.2.0 |
| **Language** | Rust |
| **Last commit** | 2026-04-27 (6 days ago) |
| **Description** | Dynamic Consensus System — multi-agent belief tracking, lock accumulation, Divide-Conquer-Synthesize protocol |
| **Tests** | No visible test files. Single `src/lib.rs` (39KB) with `DCSFlywheel`, `Belief`, `DeployPolicy`, `DynamicConsensus` — production code only. |
| **PLATO-server link** | **None.** Standalone DCS engine. Compl

---

# holodeck-consolidation.md
# Holodeck Consolidation Audit

## Summary

**holodeck-rust** (v0.3.2) and **holodeck-core** (v0.1.0) share identical source files for the 8 overlapping modules — room, agent, comms, combat, gauge, permission, manual, npc. The sole difference is `uuid::Uuid::new_v4()` vs `SystemTime::now()` for ID generation.

**holodeck-core is not actually a no_std crate.** Both have identical dependencies (tokio, serde, serde_json, chrono). holodeck-rust adds `uuid` and `reqwest`.

holodeck-rust is the canonical repo. holodeck-core appears to be an abandoned attempt to publish on crates.io, but it's stale — same code, older version.

## Crates.io Status

| Crate | Max Version | Published |
|-------|-------------|-----------|
| holodeck-rust | 0.3.2 | ✅ |
| holodeck-core | 0.1.0 | ✅ |

## Code Overlap

- **8 identical modules**: room, agent, comms, combat, gauge, permission, manual, npc
- **holodeck-rust only**: holodeck (program runner), director, evolution, games, npc_refresh, plato_bridge, sentiment_npc, sonar_vision, main.rs binary
- **holodeck-core only**: stub comments indicating full versions live elsewhere (holodeck-combat, holodeck-programs, holodeck-bridge)

## Recommendation: **Merge — keep holodeck-rust, deprecate holodeck-core**

1. **holodeck-core is not used** — no imports of `holodeck_core` found in holodeck-rust
2. **Same code, no std isolation** — holodeck-core has no std exclusion, identical deps
3. **Stale version** — holodeck-rust (0.3.2) is 3x version ahead of holodeck-core (0.1.0)
4. **Confusing duplication** — devs may wonder which to use
5. **Stub comments in holodeck-core** say full impl is in other crates — it's not a clean extraction

### If keeping separate crates:
- holodeck-core should `cargo publish --dry-run` verify no actual extraction happened
- Version 0.1.0 is already out, so yank from crates.io or bump to 0.2.0 with a clear purpose

### If merging:
- holodeck-rust remains the single crate
- holodeck-core: `cargo owner add superinstance` then y

---

# agent-stack-audit.md
# SuperInstance Agent Stack Audit
*Generated: 2026-05-03 | Oracle1 Lighthouse Keeper*

---

## Overview

**1,431+ repos across SuperInstance + Lucineer | 9 active agents | 2,489+ FLUX tests | 18+ languages**

This audit covers every `-agent` and `-vessel` repo in the SuperInstance org, plus related infrastructure (greenhorn, FLUX, PLATO SDK). Landing pages exist for most domains. PLATO integration varies significantly by repo.

---

## I. Domain Agents — PLATO Fleet (12 agents)

All follow a standard pattern: Python package + PLATO tile writes/reads. Each maps to a domain at `[domain].ai` with matching `-ai-pages` landing page.

### ✅ PLATO-Integrated Agents (strong tile write/read)

| Agent | Domain | Landing Page | PLATO Room | Tile Schema | Last 5 Commits |
|-------|--------|-------------|------------|-------------|-----------------|
| `fishinglog-agent` | Commercial fishing | ✅ `fishinglog-ai-pages` | `fishinglog-ai` | lat/lon/depth/species/catch | CI→.gitignore→docs cross-links→"Healer archetype" CI commit→Initial |
| `studylog-agent` | Study/learning tracking | ✅ `studylog-ai-pages` | `studylog-ai` | topic/concepts/questions/level/session_notes | CI→.gitignore→docs cross-links→"Healer archetype" CI→link fix |
| `deckboss-agent` | Deck operations | ✅ `deckboss-ai-pages` | `deckboss-ai` | catch processing/crew/equipment | CI→.gitignore→docs cross-links→"Healer archetype" CI→Initial |
| `makerlog-agent` | Maker/project tracking | ✅ `makerlog-ai-pages` | ? | project/build logs/tools | CI→.gitignore→docs cross-links→"Healer archetype" CI→Initial |
| `dmlog-agent` | D&D/tabletop RPG | ✅ `dmlog-ai-pages` | ? | NPCs/factions/locations/encounters | .gitignore→docs cross-links→"Healer archetype" CI→Initial |
| `playerlog-agent` | Gaming/logging | ✅ `playerlog-ai-pages` | ? | game sessions/achievements | .gitignore→Initial→v0.1.0 |
| `luciddreamer-agent` | Lucid dreaming | ✅ `luciddreamer-ai-pages` | ? | dreams/sleep/triggers/dream signs | .gitignore→docs cross-links→Ini

---

# flux-stack-audit.md
# FLUX Runtime & Compiler Stack Audit

**Date:** 2026-05-03  
**Fleet:** Cocapn  
**Auditor:** Oracle1  
**Status:** Complete

---

## Executive Summary

FLUX is a layered computing ecosystem spanning from bytecode ISA to high-level agent compilation. The system has two parallel tracks:

1. **Rust Production Track** (`flux`) — High-performance production runtime with 64-register VM, SSA IR, and polyglot parser
2. **Python Research Track** (`flux-runtime`) — Self-assembling markdown-to-bytecode runtime with 2037 tests, vocabulary tiling system

Both tracks share the same ISA concept: a bytecode instruction set that abstracts across languages and maps to agent instincts. The "compiler" is dual-interpreter (DMN/ECN) rather than traditional syntax-driven compilation.

**Key insight:** FLUX is not a compiler in the traditional sense. It's a bridge between natural language intent and executable bytecode, with the DMN/ECN dual-interpreter architecture replacing the single-pass compiler. The "gradient" between creative and logical outputs IS the compilation signal.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FLUX ECOSYSTEM                                     │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     AGENT LAYER (Plane 5-6)                         │   │
│  │  git-agent, smartcrdt-git-agent, greenhorn-runtime, agentic-compiler│   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                      │
│  ┌──────────────────────────────────▼──────────────────────────────────┐   │
│  │              COMPILER LAYER (Dual-Interpreter)                      │   │
│  │                                                                        │   │
│  │  ┌───────

---

# fm-papers-plato-integration.md
# FM Papers → PLATO Tile Index + Semantic Compiler Audit

**Date:** 2026-05-03
**Task:** Index Forgemaster's 3 arXiv papers as PLATO tiles; audit constraint-theory-core for semantic compiler integration
**Status:** Draft — papers not yet pushed to GitHub; content reconstructed from bottle + existing MD files

---

## Part 1: Paper Content Summary

### Paper 1: "FLUX ISA: A Constraint Compilation Architecture"

**What it argues:** The FLUX ISA is not just an instruction set — it's a **constraint compilation target**. Agents don't write bytecode; they express constraints, and the ISA compiles those constraints to optimal execution paths. The 43-opcode table maps each opcode to a geometric constraint (e.g., `IADD` maps to SO(3) rotation composition; `TELL/ASK` map to agent communication manifolds).

**Key technical contributions:**
- Fixed 4-byte instruction format: `[opcode:1][operand_A:1][operand_B:1][operand_C:1]` — enables fast dispatch
- Opcode taxonomy: arithmetic (0x08-0x0F), memory (0x50-0x53), A2A (0x60-0x63), speculation (0x70-0x72)
- Register convention matching ARM64 (R0-R7 GP, R15 link register) — enables trivial JIT to ARM
- A2A opcodes as first-class instructions: `TELL`, `ASK`, `DELEGATE`, `BROADCAST`
- Speculative execution: `CLONE`, `ROLLBACK`, `PEEK` for agent experimentation without commitment
- YIELD/SLEEP for cooperative multitasking
- Bytecode size: factorial(7) = 24 bytes (6 instructions × 4 bytes) — 5% larger than v1 but 20-30% faster dispatch

**Connection to constraint-theory-core:** The manifold's Pythagorean snapping (a² + b² = c² on the unit circle) IS the geometric substrate for FLUX opcode dispatch. Snap accuracy determines how precisely constraints can be encoded. The DCS constants (Laman threshold=12, info bits=5.58, Ricci multiplier=1.692) define convergence bounds for FLUX agent coordination.

**PLATO room:** `flux-isa` — primary

---

### Paper 2: "PLATO: Quality-Gated Knowledge Integration"

**What it argues:** PLATO tiles are an I

---

# keeper-glue-integration-audit.md
# keeper-beacon × cocapn-glue-core Integration Audit

**Date:** 2026-05-03
**Analyst:** Oracle1 (subagent)
**Task:** Go/no-go on wiring keeper-beacon fleet discovery to cocapn-glue-core's Beacon protocol
**Status:** COMPLETE — READY FOR DECISION

---

## 0. Executive Summary

**Recommendation: LAYERED COEXISTENCE (not full replacement)**

| | keeper-beacon (Python) | cocapn-glue-core (Rust) |
|---|---|---|
| **Language** | Python 3.10 | Rust (no_std, ~22KB) |
| **Discovery model** | Centralized HTTP POST/Python dict | Decentralized broadcast/recv traits |
| **Capabilities** | String list matching | 6-bit u32 bitmask (NoStd/Async/CUDA/Plato/FFI/Python) |
| **Identity** | `agent_id` (arbitrary string) | `TierId` (8-byte fixed, tier-specific) |
| **Transport** | HTTP/JSON over TCP | Postcard binary over any `Transport` impl |
| **PLATO sync** | None (keeper stores agents, no rooms) | Snapshot/Delta/Invalidate via `PlatoSyncPayload` |
| **Provenance** | SHA-256 sig (16 hex chars) | Merkle tree over `VerificationTrace` |
| **Generations** | None | `SyncGeneration(u64)` monotonic |

These are **orthogonal layers**, not competing implementations:

- **keeper-beacon** = **fleet registry + HTTP API + capability matching + proximity scoring** (Python, Oracle1's runtime)
- **cocapn-glue-core** = **wire format + binary serialization + transport abstraction + PLATO sync payload** (Rust, embeddable)

You cannot "replace" one with the other. They solve different problems at different layers.

---

## 1. What Each System Actually Provides

### 1a. cocapn-glue-core Beacon Protocol

Source: `src/discovery/beacon.rs` + `src/discovery/capabilities.rs` + `src/discovery/peer.rs`

```rust
// Fixed 8-byte tier identifier (no heap)
pub struct TierId([u8; 8]);
impl TierId {
    pub const BROADCAST: TierId = TierId([0xFF; 8]);
    pub fn from_mac(mac: &[u8; 6]) -> Self;    // Mini tier
    pub fn from_pid_timestamp(pid: u32, ts: u32) -> Self;  // Std tier
    pub fn from_uuid_prefix(uuid: &[u

---

# fleet-audit-2026-04-23.md
# 🔍 THE FLEET SECURITY AUDIT — COMPLETE FINDINGS
**Auditor:** AUDITOR_KIMI  
**Date:** 2026-04-23  
**Scope:** PLATO Shell (8848), MUD/Crab-Trap (4042), Domain Rooms (4050), The Lock (4043), Arena (4044), Grammar Engine (4045), Fleet Dashboard (4046), Nexus (4047), PLATO Terminal (4060)  
**Methodology:** Black-box endpoint enumeration, input validation testing, privilege escalation, source code review via exposed endpoints, service discovery

---

## 🚨 CRITICAL (6 bugs)

### PLATO-001: Unauthenticated Remote Code Execution as ROOT
| | Detail |
|---|---|
| **Endpoint** | `POST /cmd`, `/cmd/shell`, `/cmd/kimi`, `/cmd/aider` |
| **Expected** | Commands require authentication and authorization |
| **Actual** | Any unauthenticated HTTP request executes arbitrary shell commands as user `ubuntu`, who has **passwordless sudo** to `root` |
| **Evidence** | `whoami` → `ubuntu`; `sudo -n whoami` → `root`; `id` → `uid=1001(ubuntu) groups=...27(sudo)...999(docker)`; `uname -a` → full kernel info |
| **Impact** | **Complete system compromise.** Any attacker gains root access with a single curl command. |
| **Fix** | Add API key/token auth to all /cmd endpoints. Run in sandboxed containers (seccomp, chroot). Drop sudo privileges. Use Unix socket instead of TCP. |

### PLATO-002: Command Blocklist Trivially Bypassable
| | Detail |
|---|---|
| **Endpoint** | `POST /cmd/shell` |
| **Expected** | Blocked patterns cannot be bypassed |
| **Actual** | String-based blocklist for `> /dev/` is trivially bypassed: `DEV=/dev/null; echo test > $DEV` ✅, `echo test | tee /dev/null` ✅, `echo test | dd of=/dev/null` ✅ |
| **Impact** | False sense of security. Blocklist provides no real protection. |
| **Fix** | Replace string filtering with sandboxing (containers, seccomp-bpf, Landlock). Blocklists are fundamentally insecure for command injection. |

### PLATO-003: Invalid Tool Parameter Still Executes
| | Detail |
|---|---|
| **Endpoint** | `POST /cmd` |
| **Expected** | Invalid `tool` values re
