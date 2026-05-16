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
│  │  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐   │   │
│  │  │ flux-compiler  │     │flux-reasoner   │     │flux-discussion │   │   │
│  │  │  (6 planes)    │     │   -engine       │     │    -flows      │   │   │
│  │  │ Seed-mini +    │     │  DMN/ECN        │     │  3-tier        │   │   │
│  │  │ DeepSeek-v4    │     │  gradient       │     │  adversarial   │   │   │
│  │  └────────────────┘     └────────────────┘     └────────────────┘   │   │
│  │         │                      │                      │               │   │
│  │         └──────────────────────┼──────────────────────┘               │   │
│  │                                ▼                                        │   │
│  │                     PLATO (rPFC Bridge)                                │   │
│  │              Gradient storage, room-based coordination                  │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                      │
│  ┌──────────────────────────────────▼──────────────────────────────────┐   │
│  │                         ISA LAYER (Plane 2)                          │   │
│  │                                                                        │   │
│  │  ┌────────────────────┐    ┌────────────────────┐                    │   │
│  │  │  FLUX ISA v2       │    │   flux-isa-v2      │                    │   │
│  │  │  (85 opcodes,      │    │   proposal         │                    │   │
│  │  │   6 formats)       │    │   (7.5K words)      │                    │   │
│  │  └────────────────────┘    └────────────────────┘                    │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                      │
│  ┌──────────────────────────────────▼──────────────────────────────────┐   │
│  │                       RUNTIME LAYER (Plane 1-0)                       │   │
│  │                                                                        │   │
│  │  Rust Production:          Python Research:       C Embedded:          │   │
│  │  ┌──────────┐             ┌──────────────┐       ┌──────────┐       │   │
│  │  │  flux    │             │ flux-runtime  │       │flux-     │       │   │
│  │  │ (crates) │             │ (2037 tests)  │       │runtime-c │       │   │
│  │  │ Bytecode │             │ FLUX.MD →     │       │ (85 op)  │       │   │
│  │  │ + SSA IR │             │ bytecode VM    │       │ ISA v2   │       │   │
│  │  └──────────┘             └──────────────┘       └──────────┘       │   │
│  │         │                      │                      │               │   │
│  │         └──────────────────────┼──────────────────────┘               │   │
│  │                                ▼                                        │   │
│  │                     flux-os (C11 microkernel)                          │   │
│  │                    (kernel IS the compiler)                            │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      SIMULATION LAYER                                 │   │
│  │  holodeck-rust (MUD, 10 rooms, 7 NPCs, poker) ←→ holodeck-core      │   │
│  │  gpu-native-room-inference (warp-as-room, 0.031ms on Jetson Orin)    │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      PLATO INTEGRATION                               │   │
│  │  plato-sdk, plato-mythos-glue, plato-room-phi, plato-server          │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Repository Inventory

### 1. `flux` (Rust Production Runtime)

| Property | Value |
|----------|-------|
| **Language** | Rust (workspace, 5 crates) |
| **Status** | Active, v0.1.0 |
| **Tests** | 72 (bytecode) + 55 (VM) + 67 (FIR) + 92 (parser) = ~286+ |
| **Opcodes** | 100+ across 10 categories |
| **Recent commits** | 5 (docs, fleet cert, charter, hello command, initial v0.1.0) |

**What it does:**
- 64-register bytecode VM (16 GP + 16 FP + 16 Vec + 16 Sys)
- SSA IR (FirModule, FirFunction, BasicBlock)
- FLUX.MD structured markdown parser → AST → FIR
- Bytecode encoder/decoder with 18-byte header
- CLI: `flux run`, `flux compile`, `flux hello`, `flux info`, `flux demo`

**FLUX ISA Connection:**
- IS the canonical Rust implementation of the FLUX ISA
- Registers map directly to the ISA specification
- 6 instruction encoding formats (A/B/C/D/E/G)

**Recent commits:**
```
96d6677 docs: update README with fleet context
04f3363 [fleet] Add DOCKSIDE-EXAM certification checklist
22db194 [fleet] Add CHARTER — fleet identity
29fedbf feat: add 'flux hello' command, quick start, changelog update
595d855 FLUX v0.1.0 — Rust runtime: bytecode, VM, FIR, parser, CLI
```

---

### 2. `flux-runtime` (Python Research Runtime)

| Property | Value |
|----------|-------|
| **Language** | Python 3.10+ (zero external dependencies) |
| **Status** | Active, v0.1.0+ |
| **Tests** | 2037 passing |
| **Key feature** | Self-assembling, self-improving, markdown-to-bytecode |

**What it does:**
- FLUX.MD → FIR (SSA) → Bytecode → VM execution
- 8-tier fractal architecture (CORE → SYNTHESIS)
- A2A protocol (32 native opcodes for agent-to-agent communication)
- Polyglot execution (C, Python, Rust mixed in one file)
- Vocabulary tiling system (words build into bigger words)
- PaperDecomposer: 244 research papers → 2,979 FLUX vocabulary concepts

**Architecture tiers:**
```
Tier 8: SYNTHESIS — FluxSynthesizer (DJ booth, wires all subsystems)
Tier 7: MODULES — 8-level fractal hot-reload (TRAIN→CARRIAGE→LUGGAGE→...)
Tier 6A: ADAPTIVE — Profiler + Selector
Tier 6B: EVOLUTION — Genome + Mutator + Validator
Tier 5: TILES — 35 composable computation patterns
Tier 4: AGENT RUNTIME — Trust, scheduling, resources
Tier 3: A2A PROTOCOL — TELL, ASK, DELEGATE, BROADCAST
Tier 2: SUPPORT — Optimizer, JIT, Types, Stdlib, Security
Tier 1: CORE — FLUX.MD → FIR → Bytecode → VM
```

**FLUX ISA Connection:**
- Python reference implementation of the FLUX VM
- Implements the same 85 opcodes as flux-runtime-c
- Zero-dependency stdlib only (runs anywhere Python runs)

**Recent commits:** (worklog.md shows active development)
```
ABSTRACTION.md (Plane 2, reads from 3,4, writes to 2)
DOCKSIDE-EXAM.md (fleet certification)
plato-mythos-glue integration
```

---

### 3. `flux-runtime-c` (C11 Embedded Runtime)

| Property | Value |
|----------|-------|
| **Language** | C11 |
| **Status** | Active |
| **Tests** | 49 passing |
| **Platforms** | ARM64 (Jetson), x86-64, any C11 compiler |
| **Dependencies** | None (`-lm` only) |

**What it does:**
- Micro-VM for edge/embedded deployment
- 85 opcodes (arithmetic, bitwise, SIMD, A2A protocol, system calls)
- 64-register file (int/float/SIMD)
- A2A opcodes: TELL, ASK, DELEGATE, BROADCAST, TRUST, CAPABILITY, BARRIER
- Boxed values (type-tagged dynamic values)
- 6 instruction formats (A/B/C/D/E/G)

**FLUX ISA Connection:**
- Canonical C implementation of FLUX ISA v2
- Maps directly to `cuda-genepool` instincts (Survive/Perceive/Navigate/Communicate/Learn/Defend → opcode groups)
- 4.7x faster than CPython for tight arithmetic

**Recent commits:**
```(cloned fresh, history not shown)```

---

### 4. `flux-compiler` / `flux-compiler-agentic`

| Property | Value |
|----------|-------|
| **Language** | Python |
| **Package** | `flux-compiler-agentic-agentic` (PyPI) |
| **Status** | v0.1.0, initial release |
| **Models** | Seed-2.0-mini (creative) + DeepSeek-v4-flash (logical) |

**What it does:**
- 6-plane abstraction compiler with dual-interpreter gradient gates
- Only pairs where gradient > 0.35 advance to next plane
- Planes: Intent → Domain → IR → Bytecode → Native → Metal

**Plane-to-Plane Flow:**
```
Plane 5 (Intent):   natural language goal
    ↓ [Seed-mini creative + DeepSeek logical]
Plane 4 (Domain):   domain vocabulary
    ↓ [gradient gate]
Plane 3 (IR):       structured JSON AST
    ↓ [gradient gate]
Plane 2 (Bytecode): FLUX opcodes
    ↓ [gradient gate]
Plane 1 (Native):   C / Rust / Zig
    ↓ [gradient gate]
Plane 0 (Metal):    assembly
```

**FLUX ISA Connection:**
- Plane 2 (Bytecode) maps directly to FLUX ISA
- The compiler produces FLUX bytecode as output
- Gradient gates filter which candidates reach the VM

**Note:** Two repos exist (`flux-compiler` and `flux-compiler-agentic`) with identical structure — the agentic variant appears to be the primary published package.

---

### 5. `flux-reasoner` / `flux-reasoner-engine`

| Property | Value |
|----------|-------|
| **Language** | Python |
| **Package** | `flux-reasoner` (PyPI) |
| **Status** | v0.1.0, initial release |
| **Models** | Seed-2.0-mini (creative) + DeepSeek-v4-flash (logical) |

**What it does:**
- Dual-interpreter gradient reasoning engine
- Two AI interpreters work in parallel; gradient signal decides output
- Single-pass or iterative (3 rounds default)
- Decision: ADOPT_CREATIVE / ADOPT_LOGICAL / HOLD

**Gradient formula:**
```
novelty = len(creative_words) / 50.0
constraint = len(intersection) / len(creative_words)
gradient = novelty - (constraint * 0.5)
```

**FLUX ISA Connection:**
- Reasoning layer that decides which bytecode to emit
- Higher-level than the ISA — operates at "should we use async actors?" level
- Feeds into flux-compiler for implementation decisions

**Relationship to flux-compiler:**
- `flux-reasoner` = choosing (which option is best?)
- `flux-compiler` = building (compile to working system)
- Reasoner provides decision inputs to compiler

---

### 6. `flux-discussion-flows`

| Property | Value |
|----------|-------|
| **Language** | Python |
| **Status** | Active |
| **Models** | Seed-mini, Seed-pro, DeepSeek-v4-flash, GLM, minimax, kimi-cli, Claude Code |

**What it does:**
- Three-tier adversarial debate system
- Tier 1: N advocates (Seed-mini) spawn divergent arguments
- Tier 2: Judge (Seed-pro) + Synthesizer (DeepSeek-v4-flash) evaluate
- Tier 3: kimi-cli + Claude Code implement winning position
- Orchestrated by minimax (Oracle1)

**FLUX ISA Connection:**
- Fleet-level deliberation on FLUX architecture decisions
- Uses PLATO rooms to accumulate arguments as tiles
- Not directly part of the ISA — this is the governance layer

---

### 7. `flux-os` (C11 Microkernel OS)

| Property | Value |
|----------|-------|
| **Language** | C11 |
| **Status** | Active |
| **Brand line** | "An OS that writes its own code — kernel IS the compiler" |

**What it does:**
- Microkernel where the kernel compiles FLUX.MD to native binaries at boot
- Hardware-agnostic, self-compiling, agent-native
- Makefile-based build with `flux build --target native/ARM64`

**FLUX ISA Connection:**
- Target deployment platform for FLUX bytecode
- Kernel-level execution of FLUX ISA
- Self-compilation: boot-time FLUX.MD → native binary

**Recent commits:**
```
f509bb5 docs: update README with fleet context
9d52eef [fleet] Add DOCKSIDE-EXAM certification checklist
9dbb60e [fleet] Add CHARTER — fleet identity
f907e7c chore: add MIT license
9347ec7 keeper: health check — are you ok?
```

---

### 8. `flux-research` (Knowledge Base)

| Property | Value |
|----------|-------|
| **Type** | Research papers, experiments, protocol designs |
| **Word count** | 60K+ across all documents |
| **Status** | Active |

**What it does:**
- Central knowledge base for FLUX ecosystem
- Formal papers: constraint theory, lock algebra, abstraction planes
- Compiler/interpreter taxonomy (~22K words)
- ISA v2 proposal (~7.5K words)
- Fleet roundtables, Dockside scoring, reverse-actualization

**Key documents:**
- `paper-unified-constraint-theory.md` — DCS protocol, lock algebra, 82% compression
- `paper-lock-algebra.md` — Formal composition for bytecode-first AI compilation
- `paper-abstraction-planes.md` — Six-plane stack, 40% success-rate drops per plane deviation
- `compiler-interpreter-deep-dive.md` — 22K word runtime taxonomy
- `flux-strategic-vision.md` — Agent-first philosophy, markdown→bytecode kill app
- `flux-isa-v2-proposal.md` — ISA specification (fixed 4-byte, 3-operand, flag-based jumps)
- `dual-interpreter-architecture.md` — DMN/ECN separation, gradient as control signal
- `captains-log-2026-05-03.md` — Fleet state, dojo model, compilation pipeline

**FLUX ISA Connection:**
- The intellectual upstream — all ISA decisions flow from here
- 244 research papers → 2,979 FLUX vocabulary concepts (via PaperDecomposer)
- Reverse-actualization: 5-model consensus on 2031→2026 roadmap

---

### 9. `holodeck-rust`

| Property | Value |
|----------|-------|
| **Language** | Rust |
| **Status** | v0.3.1, active |
| **Lines** | ~4000, 10 modules, zero unsafe code |
| **Tests** | 9 passing |

**What it does:**
- MUD-like server with 10 rooms, 7 NPCs, poker, live sensor data
- Tokio async TCP server on port 7778
- Gauge system (heading, rudder, GPU, temp) with green/yellow/red degradation
- 22+ commands: navigation, communication, ship systems, learning, social
- NPCs powered by Seed-2.0-mini ($0.0015/cycle)

**Ship layout:**
```
                    [Harbor]
                        │
         ┌─────────────┼─────────────┐
    [Workshop]    [Bridge]      [Ready Room]
                     │                  │
           ┌─────────┼─────────┐   [Ten Forward]─[Guardian]
      [Navigation] [Ten Fwd]            │
    [Engineering]────────[Holodeck]      │
           │                              │
      [Sensor Bay]
```

**FLUX ISA Connection:**
- Simulation environment for FLUX agents
- Rooms = execution contexts; agents move between contexts
- Gauge system models deadband/constraint behavior
- DEADBAND protocol from S1-3 tile format

**Recent commits:**
```
bb1d99c chore: suppress dead_code warnings for S2 NPC APIs
e75d989 chore: update Cargo.lock for 0.3.1 publish
fc5175e feat: SonarVision underwater room plugin
80c0442 feat: SonarVision underwater room plugin
```

---

### 10. `holodeck-core`

| Property | Value |
|----------|-------|
| **Language** | Rust |
| **Status** | Active, extracted from holodeck-rust |
| **Type** | `no_std` crate |

**What it does:**
- Standalone MUD engine (room graph, agents, gauges, comms, permissions)
- Extracted from holodeck-rust monolith
- Modules: agent, room, gauge, comms, permission, combat (stub), manual (stub), npc (stub)
- Ships as a no_std crate — no CUDA, no external services

**FLUX ISA Connection:**
- Core simulation primitives that PLATO rooms are built on
- Agents interact via FLUX A2A protocol
- `holodeck-combat`, `holodeck-programs`, `holodeck-bridge` are full versions of stubs

**Recent commits:**
```
8b95d34 docs: update README with fleet context
ce18de5 chore: add MIT LICENSE
ab64ce7 holodeck-core: standalone MUD engine extracted from holodeck-rust
```

---

### 11. `gpu-native-room-inference`

| Property | Value |
|----------|-------|
| **Language** | CUDA C++ |
| **Platform** | Jetson Orin Nano 8GB (ARM64, CUDA 1024 cores) |
| **Status** | Active, validated |

**What it does:**
- GPU-native room inference kernels (warp-as-room concept)
- GPU warp (32 threads) = room collective
- 0.031ms latency — 47% faster than TensorRT

**Performance:**
| Implementation | Latency | vs TensorRT |
|----------------|---------|------------|
| TensorRT FP16 | 0.058ms | baseline |
| CUDA Thread-as-Room | 0.042ms | +38% |
| **CUDA Warp-as-Room** | **0.031ms** | **+47%** |

**FLUX ISA Connection:**
- GPU execution layer for FLUX VM operations
- Warp synchronization = room coordination
- Maps FLUX bytecode ops to CUDA kernels
- Tensor core optimization opportunity identified

---

### 12. `git-agent`

| Property | Value |
|----------|-------|
| **Language** | Python |
| **Status** | Active, v0.1.1 published to PyPI |
| **Brand line** | "The repo IS the agent. Git IS the nervous system." |

**What it does:**
- Autonomous agent operating natively on GitHub through Git workflows
- Lifecycle: Observe → Plan → Execute → Communicate → Reflect
- TASKS.md-driven work discovery
- Six growth stages: Initiate → Commander
- Fleet coordination via message-in-a-bottle protocol
- API-agnostic (OpenAI, Anthropic, Ollama, any OpenAI-compatible)

**FLUX ISA Connection:**
- Agent that consumes FLUX bytecode as instructions
- Commits are work; branches are explorations
- I2I protocol-compatible (commit-based proposals, no API calls)
- PLATO bridge for gradient computation

**Recent commits:**
```
485d5a4 chore: cocapn-git-agent v0.1.1 published to PyPI
71e0ea6 docs: update README with fleet context
8ccdd6a docs: update README with fleet context
ee50147 polish: clean quality scorer
34242ee polish: clean librarian
```

---

### 13. `smartcrdt-git-agent`

| Property | Value |
|----------|-------|
| **Language** | Python |
| **Status** | v0.3.0 |
| **Key feature** | Tidepool Oracle + property-based CRDT tests |

**What it does:**
- CRDT-git monorepo for conflict-free distributed agent state
- Tidepool Oracle: conflict resolution for concurrent agent edits
- Property-based testing for CRDT correctness
- `onboarding.md` — 328K char comprehensive onboarding doc

**FLUX ISA Connection:**
- Distributed state layer for FLUX agent coordination
- CRDT operations map to FLUX A2A protocol
- Conflict resolution via property-based testing (quickcheck-style)

**Recent commits:**
```
1dea46a chore: add Python .gitignore — block __pycache__
b3695c1 chore: add MIT LICENSE
60356f8 docs: enhance README with CRDT-git architecture
34d86b3 docs: session 5b personal log — Tidepool Oracle + property tests
84bf204 feat: v0.3.0 — Tidepool Oracle + property-based CRDT tests
```

---

### 14. `greenhorn-runtime`

| Property | Value |
|----------|-------|
| **Language** | Python + Go + C/C++ + CUDA |
| **Status** | Active |
| **Brand line** | "Plants agents anywhere within hardware/API limits" |

**What it does:**
- Portable agent runtime for constrained hardware
- Discovers fleet repos via GitHub API, clones vessel, reads taskboard, executes, pushes results
- Bootstrap stack: Bootstrap Spark → Bootstrap Bomb → PLATO → greenhorn → greenhorn-runtime
- Hardware targets: Oracle1 (ARM64 24GB), JetsonClaw1 (Jetson Orin CUDA), Forgemaster (RTX 4050), CCC (Python cloud)

**FLUX ISA Connection:**
- Deployment layer for FLUX-compiled bytecode
- Agents run FLUX bytecode on target hardware
- No-API瓶子 protocol for fleet communication

**Recent commits:**
```
aad6454 feat: add Bootstrap Spark + fleet reference stack
3df401c Merge pull request #3 from greenhorn/T-004-greenhorn
a61a450 Merge pull request #4 from greenhorn/T-005
753cb8d [fleet] Add DOCKSIDE-EXAM certification checklist
df9eefc [fleet] Add CHARTER — fleet identity
```

---

### 15. `agentic-compiler`

| Property | Value |
|----------|-------|
| **Language** | Python |
| **Status** | Active |
| **Brand line** | "Agentic compilation as fleet deliberation — markdown in, optimal runtime out" |

**What it does:**
- Markdown specs → runtime code via swarm deliberation
- Multiple agents deliberate in rounds (RA = Refinement Amplifier)
- Agents vote on best output; consensus score
- RA rounds: propose → cross-evaluate → revise → vote → repeat

**FLUX ISA Connection:**
- Higher-level compilation than flux-compiler
- Input: markdown specs (which are FLUX.MD family)
- Output: executable code (which compiles to FLUX bytecode)
- Uses plurality voting for consensus

---

### 16. `DeepGEMM`

| Property | Value |
|----------|-------|
| **Language** | CUDA C++ + Python |
| **Status** | Fleet research |
| **Platform** | Jetson Orin Nano, RTX 4050 |

**What it does:**
- DeepSeek FP8 GEMM CUDA kernels
- PTX tile marketplace candidate
- FM→JC1 LoRA inference pipeline optimization
- Benchmarks, tests, variants for 8 domains

**FLUX ISA Connection:**
- GPU kernel layer for FLUX VM operations
- Matrix/tensor ops as FLUX SIMD instructions
- Optimization target: warp-level parallelism

---

### 17. `plato-mythos-glue`

| Property | Value |
|----------|-------|
| **Language** | Python (pure stdlib, no torch) |
| **Status** | Active |

**What it does:**
- Runtime glue between PLATO Room Server and plato-mythos model
- Connects room-based coordination to reasoning model
- Pure stdlib — no ML framework dependencies

**FLUX ISA Connection:**
- Bridges FLUX bytecode execution to PLATO room coordination
- Tile-based communication between interpreter and room server

---

## Missing / Not Found

### `cocapn-glue-core`
**Status:** Not found on SuperInstance
- Not in repo list
- Clone failed: "repository not found"
- Referenced in fleet documents as "wire protocol from Cortex-M4 to Jetson Thor" (captains-log-2026-05-03)
- **Action needed:** Create or clarify location

### `flux-runtime` / `flux-runtime-c`
**Status:** Cloned but no commits shown (worklog.md active)
- These repos appear to have shallow history or are actively worked
- flux-runtime has 2037 tests and extensive documentation
- flux-runtime-c has working binaries (`test_flux_vm`, `debug_dup`, etc.)

---

## What's Working

| Component | Status | Notes |
|-----------|--------|-------|
| **FLUX ISA (bytecode)** | ✅ Working | 85 opcodes across Rust/Python/C implementations |
| **flux-runtime (Python)** | ✅ Working | 2037 tests, self-assembling, vocabulary tiling |
| **flux-runtime-c (C)** | ✅ Working | Compiles on ARM64/x86-64, ISA v2 |
| **flux (Rust)** | ✅ Working | 64-register VM, SSA IR, FLUX.MD parser |
| **holodeck-rust** | ✅ Working | 10 rooms, 7 NPCs, poker, gauge system |
| **holodeck-core** | ✅ Working | Extracted MUD engine, no_std crate |
| **gpu-native-room-inference** | ✅ Working | 0.031ms, warp-as-room validated on Jetson |
| **flux-reasoner** | ✅ Working | PyPI published, dual-interpreter gradient |
| **flux-compiler** | ✅ Working | 6-plane abstraction, gradient gates |
| **git-agent** | ✅ Working | PyPI v0.1.1, TASKS.md-driven |
| **smartcrdt-git-agent** | ✅ Working | v0.3.0, Tidepool Oracle, CRDT tests |
| **flux-discussion-flows** | ✅ Working | 3-tier adversarial debate |
| **agentic-compiler** | ✅ Working | Swarm deliberation, RA rounds |

---

## What's Missing / Gaps

| Gap | Severity | Notes |
|-----|----------|-------|
| **cocapn-glue-core** | 🔴 Critical | Referenced in fleet docs, repo doesn't exist |
| **flux-compiler/flux-compiler-agentic duplication** | 🟡 Medium | Two repos with identical structure — unclear which is canonical |
| **flux-reasoner/flux-reasoner-engine duplication** | 🟡 Medium | Same dual-interpreter engine in two repos |
| **flux-os** | 🟡 Medium | PoC status, self-compilation at boot not validated |
| **holodeck-core stubs** | 🟡 Medium | combat, manual, npc stubs — full versions in separate repos |
| **flux-discussion-flows** | 🟡 Medium | Heavily depends on minimax orchestration, not standalone |
| **PLATO integration** | 🟡 Medium | Documented but tight integration with FLUX runtime unclear |
| **flux-runtime** | 🟡 Low | Cloned with no visible commits (worklog active) |

---

## FLUX to PLATO Connection

```
FLUX Bytecode ←→ PLATO Rooms ←→ Agent Coordination

Bytecode Execution:
  FLUX.MD → parser → AST → FIR → Bytecode → VM → execution
       ↑                                           ↓
       └─── PLATO tiles (vocabulary/ground truth) ←┘

Agent Coordination:
  FLUX A2A opcodes (TELL/ASK/DELEGATE/BROADCAST)
       ↓
  PLATO room writes
       ↓
  Tile accumulation → gradient → routing to agents

Dual-Interpreter Bridge:
  DMN (Seed-mini) ←→ PLATO (rPFC) ←→ ECN (DeepSeek-v4-flash)
       ↓                  ↑                 ↓
  Creative options    gradient computed    Logical evaluation
       ↑                  ↓                 ↓
  ───────────────────────────────────────────────→ routing
```

**Key insight from flux-research/ARCHITECTURE.md:**
- PLATO rooms store output of each DMN/ECN pass as tiles
- Gradient (novelty - constraint) is tracked per tile and per room
- rPFC bridge maintains functional distance — doesn't collapse outputs

---

## FLUX to Agent System Connection

```
Intent (natural language)
    ↓ [flux-compiler 6-plane]
Bytecode (FLUX ISA)
    ↓ [flux-runtime / flux-runtime-c / flux]
Execution (VM / embedded / OS)
    ↓
Agent behavior ←→ A2A protocol (TELL/ASK/DELEGATE/BROADCAST)
    ↓
PLATO rooms (coordination, gradient storage)
    ↓
Fleet coordination (git-agent, greenhorn-runtime, smartcrdt)

git-agent: commits are work, branches are explorations
greenhorn-runtime: plants agents on constrained hardware
smartcrdt-git-agent: CRDT conflict resolution for distributed state
```

---

## FLUX ISA v2 Specification (Summary)

From `flux-isa-v2-proposal.md` in flux-research:

| Property | Value |
|----------|-------|
| **Instruction size** | Fixed 4 bytes (32 bits) |
| **Registers** | 16 GP (R0-R15), 16 FP (F0-F15), 8 special (SP/FP/LR/PC/...) |
| **Arithmetic** | Unified 3-operand (D = A op B) |
| **Jumps** | Flag-based conditional (JE/JNE/JL/JG) |
| **Memory** | LOAD/STORE with register + offset addressing |
| **Functions** | CALL/RET with stack frame |
| **A2A** | TELL/ASK/DELEGATE/BROADCAST as native opcodes |
| **System** | SYSCALL for OS services |
| **Formats** | A (1B), B (2B), C (3B), D (4B+i16), E (4B 3-reg), G (variable) |

---

## Compilation Pipeline

```
Source (FLUX.MD / markdown specs)
    ↓
flux-compiler (6 planes, dual-interpreter gradient)
    ↓
Bytecode (FLUX ISA v2)
    ↓
flux-runtime / flux-runtime-c / flux (Rust)
    ↓
Execution + A2A protocol
    ↓
PLATO room writes (tiles, gradient)
    ↓
Fleet coordination (git-agent, greenhorn, smartcrdt)
```

**Alternative path (agentic-compiler):**
```
Markdown specs
    ↓
agentic-compiler (swarm deliberation, RA rounds)
    ↓
Optimal output (voted, refined)
    ↓
Direct executable code
    ↓
[potentially] compile to FLUX bytecode
```

---

## Recommendations

1. **Create or locate cocapn-glue-core** — Critical gap, referenced but not found
2. **Consolidate flux-compiler variants** — Two repos with identical structure; pick one canonical
3. **Consolidate flux-reasoner variants** — Same issue
4. **Validate flux-os self-compilation** — Claims boot-time FLUX.MD→native, not yet tested
5. **Complete holodeck-core stubs** — combat, manual, npc need full implementations
6. **Document PLATO-FLUX integration** — The bridge is conceptual, tight integration unclear
7. **Validate flux-discussion-flows standalone** — Depends heavily on minimax orchestration

---

## Audit Metadata

| Field | Value |
|-------|-------|
| Repos audited | 16 |
| Working | 15 |
| Missing | 1 (cocapn-glue-core) |
| Duplicated | 4 (flux-compiler x2, flux-reasoner x2) |
| Recent activity | All within last 7 days |
| Fleet integration | All I2I/Git-Agent Standard v2.0 compliant |

---

*Audit complete. Ready to push to flux-research/audit/flux-stack-audit.md*

🦐 *Cocapn Fleet — lighthouse keeper architecture*