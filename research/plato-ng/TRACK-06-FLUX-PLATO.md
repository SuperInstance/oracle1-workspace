# TRACK-06: FLUX-PLATO Native Runtime Architecture

**Date**: 2026-05-15
**Status**: Speculative Research
**Goal**: Map the incremental migration path from Python-based PLATO to FLUX-native PLATO-NG

---

## Executive Summary

The ultimate vision: **PLATO-NG runs ON the FLUX VM.** FLUX-C bytecode processes tiles directly. The FLUX ISA includes syscalls for PLATO operations — `room_read`, `tile_write`, `constraint_check` — as first-class opcodes. This document traces the path from today's Python PLATO server to tomorrow's FLUX-native runtime.

**Key insight**: The migration is NOT a rewrite. It's a series of nested migrations that can happen incrementally:
1. Move PLATO's constraint engine into FLUX bytecode (already partially done)
2. Add PLATO syscalls to FLUX-VM
3. Compile PLATO's deterministic operations to FLUX-C
4. Move PLATO server logic into FLUX-X (general compute)
5. Native FLUX-only PLATO

---

## 1. Current FLUX Capabilities — Inventory

### FLUX ISA Family

| ISA | Opcodes | Purpose | Status |
|-----|---------|---------|--------|
| **FLUX-VM** | 50 | Core constraint VM with temporal + security | Spec'd |
| **FLUX-C** | 42 | Certifiable subset (aviation/medical) | Spec'd |
| **FLUX-X** | 247 | General compute, full TrustZone bridge | Spec'd |
| **flux-runtime v2.1** | 16 | Python reference (agentic bytecode) | Working |
| **flux-runtime-c** | ~36 | C99 VM for edge | Working |
| **CUDA FLUX-VM** | 20 | GPU-parallel batch execution | Working |

### Existing Backend Implementations

| Backend | Technology | Use Case |
|---------|-----------|----------|
| x86_64 CPU | AVX-512, JIT | Batch constraint checking (70B/s) |
| NVIDIA GPU | CUDA (5 kernels) | Parallel CSP solving, sonar physics |
| FPGA | SystemVerilog | Deterministic edge hardware |
| WebGPU | WGSL shader | Browser-based constraint validation |
| Vulkan | SPIR-V compute | Cross-vendor GPU |
| eBPF | XDP/socket filter | Network constraint firewalls |
| Fortran | OpenMP | Scientific computing |

### Existing Toolchain

```
GUARD DSL (declarative constraints)
    │
    ▼
guardc compiler (LLVM backend)
    │
    ├──► FLUX bytecode
    ├──► C runtime checkers
    ├──► SystemVerilog assertions
    ├──► eBPF XDP rules
    └──► Python test harnesses
```

### Formal Verification Stack

- **Coq proofs**: Reference implementation correctness
- **SymbiYosys**: FPGA RTL formal verification
- **Dual-solver**: Z3 + CVC5 cross-verification
- **Proof certificates**: Full solver traces for replay

---

## 2. PLATO-NG: Required Syscalls from FLUX

If PLATO-NG is to run natively on the FLUX VM, the ISA needs a new class of syscalls. Here's the minimal set, grouped by subsystem.

### 2.1 Room Operations (Core PLATO)

```asm
; PLATO Room Syscalls — FLUX ISA Extension (opcodes 0x80-0x8F)

SYS_ROOM_READ  0x80  ; room_id (reg) → tiles in output buffer
SYS_ROOM_WRITE 0x81  ; room_id, tile_key, tile_value → provenance
SYS_ROOM_OPEN  0x82  ; room_name → room_id (create or lookup)
SYS_ROOM_CLOSE 0x83  ; room_id → flush & release
SYS_ROOM_LIST  0x84  ; pattern → matching room_ids
SYS_ROOM_STAT  0x85  ; room_id → Φ (phi), tile count, coherence
```

**Rationale**: These replace the current HTTP-based room server. A FLUX-VM compiled PLATO kernel calls `SYS_ROOM_READ` instead of `curl localhost:8847/room/{id}`. The VM traps to the runtime or the hardware-backed room store.

### 2.2 Tile Operations (Data Layer)

```asm
; Tile Syscalls — opcodes 0x90-0x9F

SYS_TILE_GET     0x90  ; room_id, tile_key → tile bytes
SYS_TILE_PUT     0x91  ; room_id, tile_key, tile → OK/error
SYS_TILE_QUERY   0x92  ; room_id, predicate → tile set (iterator)
SYS_TILE_DELETE  0x93  ; room_id, tile_key → OK/error
SYS_TILE_MERGE   0x94  ; room_id, keys[], merge_fn → merged tile
SYS_TILE_DOMAIN  0x95  ; tile_id → TileDomain enum
SYS_TILE_PROV    0x96  ; tile_id → provenance chain
```

**Key design choice**: `SYS_TILE_QUERY` returns an iterator over tiles matching a predicate (expressed as a compiled FLUX constraint block, not a string). This allows the VM to iterate tiles without materializing full result sets.

### 2.3 Constraint Operations (Safety Layer)

```asm
; Constraint Syscalls — opcodes 0xA0-0xAF

SYS_CONSTRAINT_CHECK    0xA0  ; constraint_blob, tile → boolean + trace
SYS_CONSTRAINT_REGISTER 0xA1  ; constraint_id, bytecode → OK
SYS_CONSTRAINT_BATCH    0xA2  ; constraint_blob, tiles[] → violation mask
SYS_CONSTRAINT_VERIFY   0xA3  ; proof_blob → verified/not
SYS_CONSTRAINT_REJECT   0xA4  ; constraint_id → deactivate
```

**Critical point**: This is where FLUX's existing strength directly powers PLATO. The `SYS_CONSTRAINT_CHECK` syscall can dispatch to FLUX's AVX-512 JIT, CUDA batch, or FPGA backend depending on hardware — transparent to the PLATO programmer.

### 2.4 Render/Output Operations (Display Layer)

```asm
; Render Syscalls — opcodes 0xB0-0xBF

SYS_RENDER_ROOM  0xB0  ; room_id, format → output buffer
SYS_RENDER_TILE  0xB1  ; tile_id, format → display string
SYS_RENDER_GRAPH 0xB2  ; room_id → graphviz/JSON adjacency
SYS_RENDER_LOG   0xB3  ; room_id, since_tick → event log
```

### 2.5 Temporal & Provenance (PLATO-Afterlife)

```asm
; Temporal/Tombstone Syscalls — opcodes 0xC0-0xCF

SYS_TEMPORAL_SNAP   0xC0  ; room_id → snapshot at current tick
SYS_TEMPORAL_DIFF   0xC1  ; room_id, tick_a, tick_b → tile diff
SYS_TOMBSTONE_WRITE 0xC2  ; agent_id, ghost_tile → necropolis
SYS_TOMBSTONE_READ  0xC3  ; agent_id → ghost tiles
SYS_PROVENANCE_TRACE 0xC4 ; tile_id → full provenance chain
```

---

## 3. How FLUX Backends Enable PLATO-NG

### 3.1 LLVM Backend ↔ PLATO Server Integration

Today: PLATO server is Python, calling `guardc compile --target c` to generate C checkers, which then run as subprocesses.

```
┌──────────────────┐     HTTP/JSON     ┌──────────────────┐
│  PLATO Server    │ ────────────────► │  FLUX Compiler   │
│  (Python)        │ ◄──────────────── │  (LLVM backend)  │
│                  │   compiled .so    │                  │
│  room_phi.py     │                   │  guardc + llvm   │
│  compute_phi()   │                   │  Z3 + CVC5       │
└──────────────────┘                   └──────────────────┘
```

**In PLATO-NG, this becomes:**

```
┌───────────────────────────────────────┐
│  PLATO-NG Server                      │
│  (FLUX-VM + PLATO syscall handlers)  │
│                                       │
│  ┌─────────────────────────────────┐  │
│  │ FLUX ISA Execution Core        │  │
│  │   - 50 opcodes (VM) or 247 (X) │  │
│  │   - PLATO syscalls (0x80-0xCF) │  │
│  │   - JIT compilation to host    │  │
│  │     native (LLVM ORC JIT)      │  │
│  └──────────────┬──────────────────┘  │
│                 │                      │
│  ┌──────────────▼──────────────────┐  │
│  │ LLVM ORC JIT (Runtime)         │  │
│  │   - FLUX bytecode → native     │  │
│  │   - Specialized per constraint │  │
│  │   - Inline PLATO syscalls      │  │
│  └─────────────────────────────────┘  │
│                                       │
│  ┌─────────────────────────────────┐  │
│  │ Z3 Prover (Constraint Engine)  │  │
│  │   - SMT solving for constraints│  │
│  │   - Rejection proof generation │  │
│  │   - Deadband P0/P1/P2 analysis │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘
```

**Key integration points:**
1. **LLVM ORC JIT at runtime, not compile-time**. Constraints compile once, JIT on first call, cache native code.
2. **Z3 as co-processor**. Heavy constraint satisfaction doesn't live in the VM — it's a syscall out to the SMT solver. The VM orchestrates; Z3 computes.
3. **AVX-512 for tile batch processing**. Tile queries (`SYS_TILE_QUERY`) with numeric domains use FLUX's existing AVX-512 backend for batch comparison — 22B comparisons/s.

### 3.2 FLUX-CUDA for PLATO-NG

The existing CUDA backend already runs batch VM execution. For PLATO-NG:

- **Batch room processing**: Compile a "room profile" as FLUX bytecode. Execute 10,000 tile constraints in parallel on GPU.
- **Parallel CSP solving**: Room coherence (Φ) is inherently a constraint satisfaction problem. Uses existing `flux_cuda_csp_solve()`.
- **Arc consistency**: Room constraint propagation uses existing `flux_cuda_arc_consistency()`.
- **Edge deployment**: FLUX-CUDA on Jetson Xavier NX (JetsonClaw1's hardware) provides PLATO-NG capability at sea.

### 3.3 FLUX-X TrustZone Bridge (Security Layer)

FLUX-X is the general-compute superset (247 opcodes) with a TrustZone bridge. For PLATO-NG:

```
┌───────────────────────────────────────────────────────┐
│                    TrustZone Secure World              │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │ FLUX-X Secure Kernel                           │  │
│  │   - PLATO syscall handlers (verified)           │  │
│  │   - Tile data encryption/decryption             │  │
│  │   - Provenance chain integrity (Merkle)         │  │
│  │   - Deadband P0 constraint enforcement          │  │
│  └──────────────────────┬──────────────────────────┘  │
│                         │                              │
│                         │ Secure IPC                   │
│                         │                              │
│  ┌──────────────────────▼──────────────────────────┐  │
│  │ FLUX-X Normal World                            │  │
│  │   - Room query execution                        │  │
│  │   - Tile generation                             │  │
│  │   - Render/compute                              │  │
│  │   - Agent communication (Bottle Protocol)        │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

**Critical**: The TrustZone bridge means DEADBAND (P0 safety constraints) can run in the secure world, isolated from tile manipulation. Even if PLATO-NG's normal-world VM is compromised, P0 constraints hold.

---

## 4. Incremental Migration Path: Python → FLUX-Native

This is the most important section. The migration happens in **5 phases**, each independently shippable.

### Phase 1: FLUX-PLATO Bridge (2-4 weeks)

**Current state**: PLATO server calls constraints via Python subprocess.

**Phase 1 goal**: PLATO server sends constraints as FLUX bytecode to the FLUX-VM library (linked directly, not subprocess).

```
┌──────────────────┐  direct API call  ┌──────────────────┐
│  PLATO Server    │ ────────────────► │  libflux.so      │
│  (Python)        │  FLUX bytecode    │  (C99 VM)        │
│                  │ ◄──────────────── │                  │
│  room_server.py  │  constraint result│  flux_vm_execute │
└──────────────────┘                   └──────────────────┘
```

**What ships**:
- Python `ctypes` bindings to `libflux.so` (or Rust `libflux.rlib` via PyO3)
- `plato_flux_bridge` package — drop-in replacement for current constraint functions
- Existing PLATO doesn't change; just the constraint execution path

**Test**: Same tiles, same rooms, same PLATO server — but constraints run through FLUX VM. Measure pass/fail parity.

### Phase 2: SQLite → FLUX Tile Store (3-5 weeks)

**Current state**: PLATO rooms backed by SQLite or in-memory dict.

**Phase 2 goal**: Replace tile storage backend with a FLUX-native tile store exposed via a local VM syscall handler.

```
┌──────────────────┐     FLUX bytecode    ┌────────────────────┐
│  PLATO Server    │ ───────────────────► │  FLUX Tile VM     │
│  (Python)        │  SYS_TILE_GET/PUT   │  (extended VM)    │
│                  │ ◄────────────────── │                    │
│                  │  tile data          │  room.tile_store   │
└──────────────────┘                     └────────────────────┘
```

**What ships**:
- `plato_flux_store` — a shared library embedding a tile store with FLUX syscall handlers
- Replaces `plato_room_phi`'s storage backend
- PLATO server still Python, calling tile operations through compiled FLUX bytecode

**Why do this before PHASE 3?**: So that tile operations go through the same bytecode pipeline as constraints. Once all data flows through FLUX, adding more syscalls is mechanical.

### Phase 3: Deterministic Logic Migration (4-6 weeks)

**Current state**: Room scoring, query, rendering in Python.

**Phase 3 goal**: Compile PLATO's deterministic logic to FLUX-C (42 opcodes, certifiable). FLUX-C is the certifiable subset — ideal for PLATO's core guarantees (provenance, deadband, temporal validity).

**What migrates**:

| PLATO Component | Migration Target | Reason |
|-----------------|------------------|--------|
| `room_phi()` | FLUX-C + CUDA CSP | Φ is CSP — FLUX-GPU handles parallel |
| `tile_coherence()` | FLUX-C compare ops | Fast JIT-compiled numeric ops |
| `deadband_check()` | FLUX-C constraint ops | Safety-critical → certifiable subset |
| `provenance_verify()` | FLUX-C hash/chain ops | Integrity → deterministic |
| `temporal_validity()` | FLUX-C temporal syscalls | Time-bounded checks |
| `agent_state()` | FLUX-X (general) | Complex state machine |
| `render()` | FLUX-X (I/O) | Non-deterministic output |

**What stays in Python**:
- I/O boundary (HTTP server, CLI, WebSocket)
- Model inference (ML/LLM calls)
- Human interaction loops

**Architecture**:

```
┌──────────────┐     FLUX-C bytecode    ┌────────────────────┐
│  Python      │ ───────────────────► │  FLUX-C Runtime     │
│  PLATO I/O   │  (compiled PLATO     │                     │
│  Layer       │   logic)             │  certifiable subset │
│              │ ◄────────────────── │  42 opcodes         │
│  (thin)      │  results             │  No dynamic alloc   │
│              │                      │  Bounded loops      │
└──────────────┘                      └────────────────────┘
```

**Validation**: FLUX's existing formal verification stack (Coq + SymbiYosys + dual-solver) certifies the migrated PLATO logic. This is a **strict upgrade** — the Python version wasn't formally verified.

### Phase 4: PLATO-NG Server (4-8 weeks)

**Current state**: Multiple independent repos (plato-kernel, plato-lab-guard, plato-afterlife, etc.).

**Phase 4 goal**: A single FLUX-X runtime that implements ALL PLATO syscalls. The "PLATO-NG server" is just a FLUX-X process with the PLATO syscall handler plugin loaded.

**New Component**: `plato-ng` — the unified PLATO server

```
┌────────────────────────────────────────────────────┐
│  plato-ng                                          │
│  (FLUX-X binary + PLATO syscall handler plugin)    │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │  FLUX-X Core (247 opcodes)                  │  │
│  │    - Standard ISA (arithmetic, logic, I/O)   │  │
│  │    - PLATO syscalls (0x80-0xCF)             │  │
│  │    - TrustZone bridge (P0 isolation)         │  │
│  │    - LLVM ORC JIT tier                      │  │
│  └──────────────────┬───────────────────────────┘  │
│                     │                               │
│  ┌──────────────────▼───────────────────────────┐  │
│  │  PLATO Syscall Handler Plugin               │  │
│  │    - Room store (LMDB/RocksDB/SQLite)        │  │
│  │    - Constraint engine (Z3 + FLUX backends)  │  │
│  │    - Provenance chain (Merkle tree)          │  │
│  │    - Rendering pipeline                      │  │
│  └──────────────────────────────────────────────┘  │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │  Transport Layer                             │  │
│  │    - HTTP/JSON (backward compat)              │  │
│  │    - WebSocket (live tiles)                   │  │
│  │    - FLUX binary protocol (native clients)    │  │
│  │    - Bottle Protocol (git)                    │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

**Key design decisions**:
- **Single binary**: `plato-ng` replaces `plato-kernel` + `plato-lab-guard` + `plato-afterlife` + `plato-relay` at the server level
- **Plugin architecture**: PLATO syscall handlers are a loadable plugin to FLUX-X (`.so` or `.wasm`)
- **Backward compatible**: Phase 4 still serves the same HTTP API as current PLATO. Phase 5 drops it.

### Phase 5: Full PLATO-NG (6-12 weeks)

**Current state**: Python PLATO server still runs I/O.

**Phase 5 goal**: PLATO logic runs entirely on FLUX-VM. The Python layer is replaced by a thin transport proxy (or removed entirely if using FLUX-X's I/O opcodes).

```
┌──────────────────────────────────────────────────────┐
│  Device / Client                                     │
│  (Agent, Web UI, CLI)                                │
│         │                                            │
│  ┌──────▼─────────────────────────────────────────┐  │
│  │  Transport Proxy (optional, thin)              │  │
│  │  - HTTP → FLUX binary transcoding              │  │
│  │  - WebSocket → FLUX stream                     │  │
│  │  - Can be nginx/wasm or FLUX-X's I/O layer     │  │
│  └──────┬─────────────────────────────────────────┘  │
│         │ FLUX binary protocol                       │
│  ┌──────▼─────────────────────────────────────────┐  │
│  │  plato-ng                                      │  │
│  │  (FLUX-X + PLATO syscall handlers)             │  │
│  │                                                 │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │  SYS_ROOM_READ → query tile store       │   │  │
│  │  │  SYS_CONSTRAINT_CHECK → dispatch Z3     │   │  │
│  │  │  SYS_TILE_QUERY → iter over matching    │   │  │
│  │  │  SYS_RENDER_ROOM → format output        │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

**What dies**:
- No more Python PLATO server
- No more HTTP/JSON for internal communication
- No more separate plato-kernel, plato-lab-guard, plato-afterlife, plato-relay repos (merged into plato-ng)

**What stays**:
- PLATO tile specification (unchanged)
- PLATO rooms, tiles, constraints (unchanged)
- PLATO SDK for agents (unchanged API, new backend)
- Bottle Protocol for inter-agent communication

---

## 5. Formal Verification Implications

FLUX's formal verification stack already exists. When PLATO runs on FLUX, it inherits those guarantees.

### What Gets Formally Verified

| Component | Current | FLUX-Native |
|-----------|---------|-------------|
| Constraint checking | Python unit tests | Coq proofs + Z3 cross-verify |
| Tile provenance | Hash chain (ad-hoc) | Coq-verified Merkle chain |
| Deadband enforcement | Integration tests | Formal isolation proof |
| Temporal validity | Python datetime | FLUX temporal opcodes (verified) |
| Room coherence (Φ) | Numeric algorithm | Coq-verified Φ computation |
| Tile merge | Python dict merge | Verified deterministic merge |
| Syscall handlers | N/A | Verified against FLUX ISA spec |

### Formal Verification Layers

```
Layer 3: PLATO-NG Application Properties
    - "Room Φ monotonically increases with coherent tiles"
    - "Temporal validity never allows past-referencing tiles"
    - "Deadband P0 constraints always reject before P1/P2"

Layer 2: PLATO Syscall Specifications
    - "SYS_ROOM_READ returns exactly matching tiles"
    - "SYS_CONSTRAINT_CHECK returns boolean matching Z3 result"
    - "SYS_TILE_PUT preserves room coherence"

Layer 1: FLUX ISA Formal Semantics
    - "Each opcode preserves stack invariants"
    - "Temporal ops correctly handle timestamps"
    - "TrustZone bridge prevents normal-world access to secure tiles"

Layer 0: Hardware Backend Integrity
    - Coq proof: C VM matches ISA spec
    - SymbiYosys: FPGA RTL matches C reference
    - Differential tests: All backends produce identical results
```

---

## 6. Where Does PLATO-NG Run?

### Edge: JetsonClaw1 (Jetson Xavier NX)
- **Current**: Python PLATO + CUDA for sonar physics
- **Future**: FLUX-CUDA runs PLATO tile queries on GPU, sonar physics in same kernel
- **Mix fix cost**: $0 — FLUX already has CUDA backend

### Cloud: Oracle1 (ARM64 server)
- **Current**: PLATO room server (Python) on 4 ARM cores
- **Future**: FLUX-VM with JIT-compiled PLATO operations
- **Challenge**: No AVX-512 on ARM. FLUX needs NEON-optimized backend
- **Workaround**: PLATO-NG on ARM still faster than Python due to native code + reduced context switches

### Browser: WebGPU PLATO
- **Current**: No browser PLATO
- **Future**: PLATO-NG via WebGPU backend (FLUX already has WGSL shaders)
- **Use case**: Fleet dashboard, visualization, educational tools

### FPGA: Hardware PLATO
- **Current**: FLUX constraint checker fits in 1,717 LUTs on Artix-7
- **Future**: PLATO syscall handlers on FPGA for latency-critical ops
- **Use case**: Safety-critical deadband enforcement in hardware

---

## 7. Risks and Mitigations

### Risk 1: FLUX-VM is not a general-purpose runtime
**Problem**: PLATO-NG needs string operations, variable-length data, I/O. FLUX-VM is designed for numeric constraints.
**Mitigation**: FLUX-X (247 opcodes) is the right baseline for PLATO-NG. It includes string, I/O, and memory operations. FLUX-VM handles constraints only; FLUX-X handles everything else.

### Risk 2: Syscall overhead
**Problem**: Each `SYS_TILE_GET` traps from VM to handler, potentially slower than Python dict access.
**Mitigation**: 
- Batch syscalls: `SYS_TILE_QUERY` returns iterators, not individual tiles
- Cache tile store in VM memory (like a filesystem cache)
- LLVM JIT can inline syscall handlers for hot paths (Phase 4+)

### Risk 3: Z3 as co-processor latency
**Problem**: Calling Z3 for every constraint check kills throughput.
**Mitigation**:
- FLUX's SIMD constraint checking handles 70B/s for numeric constraints. Z3 only needed for:
  - SMT-level constraint satisfaction (cross-tile invariants)
  - Proof certificate generation
  - Structural constraint analysis (deadband P0)
- 90% of constraint checks use FLUX's fast path, not Z3

### Risk 4: Python ecosystem loss
**Problem**: PLATO relies on Python ML libraries, HuggingFace transformers, PyTorch.
**Mitigation**: Model inference stays outside FLUX (at Phase 5, still through transport proxy). FLUX handles:
- Deterministic operations only
- Constraint checking
- Tile storage and query
- Provenance and temporal validation
- Agent state management

ML inference is a co-processor to PLATO-NG, not a FLUX core operation.

### Risk 5: Migration fatigue
**Problem**: 5 phases over months — teams lose momentum.
**Mitigation**: Each phase is independently shippable and valuable:
- Phase 1: Faster constraint checking (shippable, no API change)
- Phase 2: Deterministic tile store (more reliable, no API change)
- Phase 3: Formally verified core logic (safety upgrade, no API change)
- Phase 4: Single-binary deployment (operational win)
- Phase 5: Full PLATO-NG (performance + security win)

---

## 8. Open Questions

1. **Should PLATO syscalls be part of the FLUX ISA specification or a vendor extension?**
   - If ISA: FLUX-X defines PLATO syscalls as standard. Every FLUX-X implementation supports PLATO.
   - If extension: PLATO-* syscalls are a plugin. Only agents that load the PLATO handler support them.
   - **Recommendation**: Start as extension plugin (Phase 2-3), standardize as ISA extension when Phase 4 ships.

2. **What is the FLUX bytecode format for tile data?**
   - Tiles are JSON/JSON-LD currently. FLUX bytecode operates on doubles and integers.
   - **Option A**: Encode tiles as byte buffers, string operations via FLUX-X string opcodes
   - **Option B**: Define a compact binary tile format (protobuf/flatbuffers) with FLUX reader/writer opcodes
   - **Recommendation**: Option B — a packed binary tile format avoids JSON parsing overhead and maps naturally to FLUX's register model.

3. **Does PLATO-NG need a WASM-based syscall handler instead of native code?**
   - WASM gives sandboxing. Native .so gives performance.
   - **Recommendation**: Start with native .so (simpler, fastest), add WASM fallback for untrusted/third-party handlers.

4. **Do we need the Three-Tier (P0/P1/P2) Deadband at the ISA level?**
   - **Yes**. P0 constraints should be compile-time guaranteed by FLUX's trusted toolchain. The ISA should have a `DEADBAND_P0` opcode that the TrustZone bridge enforces autonomously.

---

## 9. Summary of the Path

```
Today: Python PLATO + FLUX as separate tools
    │
    ▼
Phase 1: PLATO calls FLUX as a library (same architecture, faster constraints)
    │
    ▼
Phase 2: Tiles store behind FLUX syscalls (same API, deterministic storage)
    │
    ▼
Phase 3: Deterministic logic compiled to FLUX-C (formally verified subset)
    │
    ▼
Phase 4: Single plato-ng binary (FLUX-X + PLATO syscall handler plugin)
    │
    ▼
Phase 5: Python removed. PLATO runs entirely on FLUX-VM.
         Transport proxy for I/O boundary.
```

**Each phase is independently shippable and adds value.** No phase requires the next to be useful. This is the "hermit crab" approach to architecture migration — grow into the new shell one molt at a time.

---

## Appendix: Relevant Existing Assets

| Asset | Location | Relevance |
|-------|----------|-----------|
| FLUX C99 VM | `flux-hardware/flux-isa-c/` | Current constraint VM |
| FLUX CUDA | `flux-hardware/flux-cuda/` | GPU batch execution |
| FLUX docs | `flux-docs/` | ISA spec, tutorials, strategy |
| FLUX Compiler | `flux-compiler/` | 6-plane abstraction compiler |
| PLATO Integration Map | `docs/PLATO-INTEGRATION-MAP.md` | Current PLATO architecture |
| Neural Plato ADR | `docs/ADR-001-NEURAL-PLATO.md` | Multi-agent coordination framework |
| PLATO Boot Sequence | `docs/NEURAL-PLATO-v0.1-BOOT-SEQUENCE.md` | Hardware memory layout |
| PLATO Kernel | `research/flux-runtime/` (cocapn/flux-runtime) | Current deterministic runtime |
| PLATO Architecture Research | `research/plato-arch/` | MUD-first PLATO design docs |
| GUARD DSL Tutorial | `flux-docs/tutorials/guard-dsl-tutorial.md` | Constraint language reference |
| FLUX Security Threat Model | `flux-docs/strategy/security-threat-model.md` | Formal verification stack |
| FLUX Community Hub Architecture | `flux-docs/strategy/flux-community-hub.md` | FLUX-PLATO bridge plans |
| PLATO Room Phi | `repos/plato-room-phi/` | Φ computation for rooms |
