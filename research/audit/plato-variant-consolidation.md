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
| **PLATO-server link** | **None.** Standalone DCS engine. Complements `plato-kernel` but is architecturally parallel, not dependent. |
| **Purpose** | Fleet democracy engine: agents propose beliefs, accumulate locks, reach consensus dynamically when evidence warrants it |

**Key differentiator:** Consensus protocol that runs alongside tile processing. Agents disagree → evidence wins → locks accumulate. Distinct from kernel's tile lifecycle.

---

### 3. `plato-mythos` (Python)

| Field | Value |
|-------|-------|
| **PyPI** | plato-mythos 0.1.0 |
| **Language** | Python |
| **Last commit** | 2026-04-27 (6 days ago) |
| **Description** | PLATO-native Recurrent-Depth Transformer — maps PLATO concepts to Mythos generative modeling: Tiles→KV, Rooms→MoE experts, Deadbands→ACT halting, Shells→LoRA |
| **Tests** | **Yes.** `tests/test_model.py` (4KB) — model instantiation + forward pass smoke tests |
| **PLATO-server link** | **None.** Pure research prototype. Not connected to runtime server. No ability to query PLATO or emit tiles. |
| **Purpose** | Experimental transformer architecture that embodies PLATO control theory in a generative model. "Rooms as MoE experts" and "deadband as ACT halting" are interesting but not wired into any runtime. |

**Key differentiator:** The only generative/model variant. All other variants are about *using/managing* tiles; Mythos is about *training* models that understand the PLATO format. This is upstream R&D, not a server component.

---

### 4. `plato-edge` (Python)

| Field | Value |
|-------|-------|
| **PyPI** | plato-edge 0.1.0 |
| **Language** | Python (stdlib only, zero deps) |
| **Last commit** | 2026-04-27 (6 days ago) |
| **Description** | Edge-optimized fleet packages for ARM64 — pure Python, zero external deps, <50KB installed, <10MB RSS |
| **Tests** | **Yes.** `tests/test_smoke.py` (4.3KB) — smoke + unit tests for Tile, Deadband, Flywheel, Beacon, Tracer |
| **PLATO-server link** | **None.** Standalone edge modules. Designed for NVIDIA Jetson Orin deployment (onboat inference, camera sensors). Does not call home to port 8847. |
| **Purpose** | Embedded deployment for resource-constrained hardware. Replaces HTTP discovery with UDP beacon. Replaces external tile libraries with a minimal binary codec. |

**Key differentiator:** The only edge-embedded variant. Zero-dependency constraint means it runs anywhere Python runs with no pip install. Distinct deployment target, not a variant of the same thing.

---

## Maintenance Status

| Repo | Language | Last Push | Days Ago | Test Files | crates.io/PyPI |
|------|----------|-----------|----------|------------|----------------|
| `plato-kernel` | Rust | 2026-04-27 | 6 | ❌ None visible | ✅ 0.2.0 |
| `plato-dcs` | Rust | 2026-04-27 | 6 | ❌ None visible | ✅ 0.2.0 |
| `plato-mythos` | Python | 2026-04-27 | 6 | ✅ `test_model.py` | ✅ 0.1.0 |
| `plato-edge` | Python | 2026-04-27 | 6 | ✅ `test_smoke.py` | ✅ 0.1.0 |

**All four are actively maintained** (last commit within the last week). This is not an abandoned codebase.

---

## Relationship to Production Server (port 8847)

**None of the four variants are connected to `cocapn-plato` (port 8847).**

- `plato-kernel` and `plato-dcs` are Rust crates — `cocapn-plato` is Python with no Rust bindings
- `plato-mythos` is a research transformer — no runtime tile read/write
- `plato-edge` is embedded Python with no network dependency on the server

The production server (`cocapn-plato` on port 8847) is a **Python-first stack**. These four variants are a **parallel Rust/Python edge layer** that doesn't currently integrate with it.

**This is the actual consolidation opportunity:** bridging `plato-kernel`/`plato-dcs` Rust crates into `cocapn-plato` via PyO3, or exposing a gRPC interface the server can call.

---

## Recommendation

### NOT a consolidation problem. This is a layering problem.

These four repos are **complementary, not competing**. They cover four distinct concerns:

```
plato-kernel  → Rust tile lifecycle + belief engine (foundation)
plato-dcs     → Rust multi-agent consensus protocol (extension of kernel)
plato-mythos  → Python transformer research (upstream R&D)
plato-edge    → Python edge runtime for ARM64 (downstream deployment)
```

**No merge is warranted.** Each has a distinct purpose, language, and deployment target.

### Recommended Actions

| Action | Who | Why |
|--------|-----|-----|
| **Keep all four as separate packages** | — | No consolidation needed |
| **Add test suites to kernel + dcs** | FM | Both are missing unit tests; critical for a foundation crate |
| **Wire plato-kernel into cocapn-plato** | Oracle1/FM | PyO3 bindings or gRPC — bridge Rust core into the production Python server |
| **Wire plato-dcs into cocapn-plato** | Oracle1/FM | Same bridge path — consensus engine should work with the live tile store |
| **Mark plato-mythos as experimental** | FM | Add `plato-mythos/README.md` note: "Not connected to runtime PLATO. Research only." |
| **Keep plato-edge as-is** | — | Already properly scoped for edge deployment |
| **Create `plato-tile-spec` crate** | FM | Canonical tile format shared by kernel, dcs, edge — currently each has its own |

### Deprecation / Archive Paths

No deprecation recommended for any of the four. All are actively used:

- `plato-kernel` is the foundation other Rust crates depend on
- `plato-dcs` is the consensus engine for fleet democracy
- `plato-mythos` is the experimental transformer — keep for R&D
- `plato-edge` is the embedded deployment solution for ARM64 hardware

---

## Concrete Consolidation Plan (Integration, Not Merge)

### Step 1: Add Tests to Rust Crates (Week 1)
```
plato-kernel:  add src/belief_tests.rs, src/deadband_tests.rs
plato-dcs:     add src/dcs_tests.rs, src/consensus_tests.rs
```
These are missing unit tests. Foundation crates without tests are a liability.

### Step 2: Create `plato-tile-spec` Shared Crate (Week 1-2)
```
plato-tile-spec/
  src/
    lib.rs       → Tile { id, domain, question, answer, energy, tags }
    codec.rs     → binary encoding (from plato-edge's TileCodec)
    deadband.rs  → P0/P1/P2 priority gate (from plato-edge's DeadbandGate)
  depends on: nothing (no external deps)
```
Then make `plato-kernel`, `plato-dcs`, and `plato-edge` all depend on this shared spec.

### Step 3: Bridge Rust → Python (Week 2-3)
Options (pick one):
- **PyO3**: compile `plato-kernel` + `plato-dcs` as Python extensions via PyO3, importable from `cocapn-plato`
- **gRPC**: add a `plato-kernel-grpc` service that `cocapn-plato` calls for tile validation and belief scoring
- **Foreign function interface**: simpler but less type-safe than PyO3

### Step 4: Connect plato-edge to Server (Optional)
`plato-edge` modules (Flywheel, Beacon, TileCodec) could be added to `cocapn-plato` as optional edge extras — useful for agents running on Jetson hardware who need local tile caching.

---

## Decision Table

| Repo | Status | Action |
|------|--------|--------|
| `plato-kernel` | **Production** (foundation) | Keep. Add tests. Bridge to Python server. |
| `plato-dcs` | **Production** (consensus) | Keep. Add tests. Bridge to Python server. |
| `plato-mythos` | **Research** (not production) | Keep. Mark experimental in README. No runtime integration. |
| `plato-edge` | **Production** (edge deployment) | Keep as-is. Consider optional import into cocapn-plato. |

**Verdict:** No merges. No archives. All four have distinct non-overlapping roles. The gap is not consolidation — it's **integration** between the Rust core and the Python production server.

---

## What This Means for PLATO Stack Architecture

From the stack audit, the canonical Python runtime is `cocapn-plato` on port 8847. These four variants represent a **parallel Rust/embedded layer** that doesn't currently speak to it.

The real work is:
1. **Shared tile spec** so Python and Rust agree on the tile format
2. **PyO3 or gRPC bridge** so the server can use kernel + DCS
3. **Tests on Rust crates** before they become production dependencies

These four repos are correctly scoped. The problem isn't too many of them — it's that they don't yet connect to the running server.

---

*Generated by Oracle1 subagent. Data from GitHub API + crates.io + repo READMEs.*
