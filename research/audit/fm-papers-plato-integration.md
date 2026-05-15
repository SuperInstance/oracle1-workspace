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

**What it argues:** PLATO tiles are an IR (Intermediate Representation), not natural language. Quality-gating is the loss function: the **unfakeable test** (articulation in own words) is harder to game than cross-entropy. The achievement loop IS narrative gradient descent. The key formal propositions:

- **Proposition 1:** Rooms as layers — MUD room traversals are composable transformation layers equivalent to neural network layers
- **Proposition 2:** Strategy tiles as weights — agent strategy parameters (turtle/blitz/zen) are directly analogous to neural network weights
- **Proposition 3:** Achievement loss harder to game than cross-entropy — originality check prevents memorization
- **Collision probability:** Formal analysis of tile collision (two agents writing conflicting answers to same question) — managed by deadband protocol, not prevention

**Key technical contributions:**
- Achievement Loss function: `1.0 - (0.3 * action_coverage + 0.3 * outcome_coverage + 0.2 * knowledge_coverage + 0.2 * originality)`
- Narrative gradient vs numerical gradient — narrative includes causal reasoning, confidence signal, misconception detection
- Room graph as neural network: entrance=input, terminal=output, intermediate=hidden
- Ticker as attention mechanism
- Scaling: linear with room diversity, not exponential with GPU memory

**Connection to constraint-theory-core:** The `PythagoreanManifold` provides the exact coordinate system for tile quality scores. Confidence scores (0.0-1.0) can be projected onto the Pythagorean lattice for deterministic comparison. `ConstraintProblem` (CSP) maps directly to the tile deduplication problem: "has this question been asked before?" = CSP satisfaction check.

**PLATO rooms:** `plato-core`, `achievement-loops`, `dojo` — primary; also `flux-isa` (tile IR overlap)

---

### Paper 3: "Reverse Actualization: From Constraint Theory to Trust Infrastructure"

**What it argues:** Trust is not a feeling — it's a **measurable constraint satisfaction property**. Reverse actualization means working backwards from desired outcomes (trust) to required constraints (proof of correctness). The strategic endgame is **Certification-as-a-Service**: "The future belongs not to the smartest AI, but to the most trustworthy." Killer app: "Guardian Core" — AI monitoring AI with provable correctness, real-time, MCU tier.

**Key technical contributions:**
- **Dependency graph:** cocapn-glue → [NL API, Lean4 VM, Merkle] → Sensor→Tile Learning
- **Sequence:** Unify → Trust → Prove → Learn — all 5 models independently converged on same priorities
- **DCS-Laman connection:** rigidity threshold (12 neighbors) matches DCS Law 102 — coordination becomes rigid above 12-agent neighborhoods
- **Reverse actualization loop:** start with desired outcome → identify required constraints → find constraint-violating inputs → update domain
- **Functional distance hypothesis:** creativity requires maintained tension between DMN (generative) and ECN (evaluative) — collaboration collapses the gradient; contrast preserves it
- **Trust as constraint satisfaction:** trust score = proportion of constraint satisfaction cycles completed without violation

**Connection to constraint-theory-core:** The `ConstraintBlock` (192 bytes) IS the trust metric. Holonomy norm (gauge-invariant phase) measures constraint transport consistency. Ricci curvature measures how "expensive" it is to satisfy constraints in a given region. Percolation probability (critical threshold ≈ 0.6602741) determines when the trust network becomes globally coherent.

**PLATO rooms:** `trust-infrastructure`, `reverse-actualization`, `guardian-core` — primary; also `constraint-theory` (cross-cutting)

---

## Part 2: Key Types from constraint-theory-core

### Tile and Origin (384 bytes + 64 bytes)

```rust
pub struct Tile {
    pub origin: Origin,           // 64 bytes — SO(3) reference frame + rate of change
    pub input: u64,
    pub output: u64,
    pub confidence: f32,         // Phi cascade — maps to PLATO tile confidence
    pub safety: u32,             // Sigma — safety predicate
    pub bytecode_ptr: u64,       // FLUX bytecode pointer — connects to ISA
    pub trace: u64,
    pub tensor_payload: [f32; 16],  // geometric data — first 2 dims = 2D vector
    pub provenance_head: u32,
    pub self_play_gen: u16,
    pub hydraulic_flux: f32,
    pub constraints: ConstraintBlock,  // 192 bytes — the trust metric
}

pub struct Origin {
    pub id: u64,
    pub reference_frame: [[f32; 3]; 3],  // SO(3) rotation matrix
    pub rate_of_change: [f32; 3],
}
```

**PLATO mapping:** PLATO's `Tile` type (domain, question, answer, agent, confidence) maps to `Tile` (confidence maps directly; question/answer map to tensor_payload via encoding). The 384-byte constraint-theory Tile CAN be the canonical PLATO tile in the inference loop.

### ConstraintBlock (192 bytes)

```rust
pub struct ConstraintBlock {
    pub snap_target: [f32; 3],         // Pythagorean (a, b, c)
    pub holonomy_matrix: [[f32; 3]; 3], // SO(3) transport
    pub holonomy_norm: f32,            // gauge-invariant phase
    pub ricci_curvature: [[f32; 4]; 4], // curvature tensor
    pub ricci_scalar: f32,              // trace of curvature
    pub rigid_cluster_id: u64,
    pub percolation_p: f32,             // ≈ 0.6602741 (critical threshold)
    pub gluing_map: [f32; 2],
    pub gluing_status: u32,
    pub lvq_codebook_idx: u32,
    pub omega_density: f32,
    pub constraint_tolerance: f32,      // default 0.05
    pub persistence_hash: u64,
}
```

**PLATO mapping:** `constraint_tolerance` maps to deadband threshold. `holonomy_norm` maps to trust score. `percolation_p` determines when a room's tiles become globally coherent.

### ConstraintProblem (CSP Solver)

```rust
pub struct Variable { name: String, domain: Vec<i64> }
pub enum Constraint {
    Unary { var: usize, check: UnaryCheck, desc: &'static str },
    Binary { a: usize, b: usize, check: BinaryCheck, desc: &'static str },
    Nary { vars: Vec<usize>, check: NaryCheck, desc: &'static str },
}
pub struct ConstraintProblem {
    pub variables: Vec<Variable>,
    pub constraints: Vec<Constraint>,
}
```

**PLATO mapping:** Tile deduplication = CSP satisfaction check. "Has this question been asked?" = checking if a Variable's domain already contains an equivalent assignment. Room consistency = constraint satisfaction across all tiles in a room.

### PythagoreanManifold

```rust
pub struct PythagoreanManifold {
    valid_states: Vec<[f32; 2]>,  // exact Pythagorean vectors on unit circle
    kdtree: KDTree,                // O(log N) nearest neighbor
}

pub fn snap(&self, vector: [f32; 2]) -> ([f32; 2], f32)  // returns (snapped_vector, noise)
```

**PLATO mapping:** Tile confidence scores projected onto Pythagorean lattice → deterministic comparison without floating-point drift. `noise = 1 - resonance` where resonance = dot_product(snapped, input).

### PythagoreanQuantizer

```rust
pub enum QuantizationMode { Ternary, Polar, Turbo, Hybrid }
pub struct PythagoreanQuantizer { mode: QuantizationMode, bits: u8 }
pub fn quantize(&self, data: &[f64]) -> QuantizationResult
pub fn snap_to_pythagorean(&self, value: f64) -> f64
```

**PLATO mapping:** Strategy tile parameters (turtle/blitz/zen weights) can be quantized to exact Pythagorean ratios — no floating-point comparison drift across agents.

### DCS Constants

```rust
LAMAN_NEIGHBOR_THRESHOLD: usize = 12    // rigidity threshold
PYTHAGOREAN_INFO_BITS: f64 = 5.584962500721156  // log2(48)
RICCI_CONVERGENCE_MULTIPLIER: f64 = 1.692
SWARM_UNIFORMITY_THRESHOLD: usize = 500
COORDINATION_ENTRY_WINDOW: f64 = 1.7
```

**PLATO mapping:** Fleet coordination bounds. When agent count > 500, use uniform rules (no individual variation). Coordination entry window = 1.7x latency. These define when tiles should be globally synchronized vs locally optimized.

---

## Part 3: Semantic Compiler Integration

### Current State

The semantic compiler (papers/semantic-compiler.md + plato-server/server.py) already has:
- **IR:** PLATO tiles (domain, question, answer, confidence)
- **Pipeline:** Intent → Frontend (parse to tile) → Optimizer (dedupe/reinforce/deadband) → Backend (emit) → Verifier (check against expected_answer)
- **Deadband protocol:** soft deadband (reinforce), hard deadband (recompile), flatline (decommission)
- **PLATO as IR** concept explicitly stated

### What's Missing for constraint-theory-core Integration

The semantic compiler can use constraint-theory-core in 4 ways:

**1. Tile type backend:** Replace the flat tile `{domain, question, answer, confidence}` with the 384-byte `Tile` from constraint-theory-core. The `ConstraintBlock` (192 bytes) becomes the tile's extended metadata. This gives each PLATO tile a full geometric representation.

**2. Confidence projection:** PLATO tile confidence scores (float) can be projected onto the PythagoreanManifold for deterministic comparison. Agent A at confidence 0.7 and Agent B at confidence 0.700001 are no longer "close" — they snap to the same Pythagorean coordinate (noise ≈ 0). This eliminates floating-point divergence across fleet instances.

**3. Dedup as CSP:** The tile deduplication problem ("has this question been asked?") maps directly to `ConstraintProblem::is_consistent()`. Each room = a CSP. New tile question = new Variable. Constraint check = does this answer violate any existing constraints? This is more principled than substring matching.

**4. Deadband as constraint satisfaction:** The deadband protocol (output diverged from expected_answer) maps to constraint violation. `constraint_tolerance` (default 0.05) IS the deadband threshold. `holonomy_norm` IS the trust score. When holonomy_norm exceeds tolerance, tile enters deadband.

### Concrete Integration Path

```python
# In semantic compiler optimizer:
# Before: check if tile question duplicates existing tiles (substring match)
# After: build ConstraintProblem from room tiles, check CSP consistency

from constraint_theory_core import (
    PythagoreanManifold, ConstraintProblem, Variable, Constraint,
    snap, CTErr
)

def check_tile_consistency(room_tiles, new_tile):
    manifold = PythagoreanManifold::new(200)  # ~1000 states, 0.36° max error
    
    # Project confidence scores to Pythagorean lattice
    snapped_confidence, noise = snap(manifold, [new_tile.confidence, 0.0])
    
    if noise > 0.05:  # constraint_tolerance from ConstraintBlock
        return {"status": "deadband", "noise": noise}
    
    # Build CSP: each existing tile = constraint on question/answer
    # Check if new_tile's question domain overlaps with existing assignments
    # ...
```

---

## Part 4: PLATO Rooms per Paper

| Paper | Primary Room | Secondary Rooms |
|-------|-------------|-----------------|
| FLUX ISA | `flux-isa` | `constraint-theory`, `plato-core` |
| PLATO: Quality-Gated Integration | `plato-core` | `dojo`, `achievement-loops`, `rooms-as-layers` |
| Reverse Actualization → Trust | `trust-infrastructure` | `reverse-actualization`, `guardian-core`, `constraint-theory` |

---

## Part 5: Concrete Tile Content

### From Paper 1: FLUX ISA

**Tile 1 (flux-isa room):**
```
domain: flux-isa
question: What is the FLUX ISA instruction format?
answer: Fixed 4 bytes: [opcode:1][operand_A:1][operand_B:1][operand_C:1]. 256 possible opcodes, 3 operand bytes. MOVI Rd, imm16 encodes as [0x2B][Rd][imm_lo][imm_hi].
agent: oracle1
confidence: 0.95
```

**Tile 2 (flux-isa room):**
```
domain: flux-isa
question: How does FLUX handle agent-to-agent communication?
answer: TELL/ASK/DELEGATE/BROADCAST are first-class opcodes (0x60-0x63). TELL sends to agent_id with payload_reg. ASK blocks for response. DELEGATE assigns bytecode range. BROADCAST sends to all known agents.
agent: oracle1
confidence: 0.92
```

**Tile 3 (flux-isa room):**
```
domain: flux-isa
question: How does FLUX achieve deterministic speculation?
answer: CLONE creates a full VM copy in register R0. ROLLBACK restores from save_reg. PEEK executes dry-run without commit. All three preserve the original state — speculation has no side effects until explicit commit.
agent: oracle1
confidence: 0.90
```

**Tile 4 (constraint-theory room):**
```
domain: constraint-theory
question: What is the relationship between FLUX opcode dispatch and the Pythagorean manifold?
answer: Opcode dispatch is constrained search on the Pythagorean manifold. Each opcode corresponds to a geometric transformation (e.g., IADD = SO(3) rotation composition). The manifold's snap accuracy determines how precisely constraints are encoded in bytecode.
agent: oracle1
confidence: 0.88
```

### From Paper 2: PLATO Quality-Gated Integration

**Tile 5 (plato-core room):**
```
domain: plato-core
question: What is the Achievement Loss function?
answer: achievement_loss = 1.0 - (0.3 * action_coverage + 0.3 * outcome_coverage + 0.2 * knowledge_coverage + 0.2 * originality). Originality is the key differentiator — it prevents memorization. A rote copy has originality=0, a genuine understanding has originality>0.5.
agent: oracle1
confidence: 0.93
```

**Tile 6 (plato-core room):**
```
domain: plato-core
question: Why is the unfakeable test harder to game than cross-entropy?
answer: Cross-entropy measures prediction accuracy — a model can memorize outputs without understanding why. The unfakeable test measures comprehension via articulation in one's own words — memorization fails the originality check, and the test adapts infinitely (no fixed answer key).
agent: oracle1
confidence: 0.91
```

**Tile 7 (rooms-as-layers room):**
```
domain: dojo
question: How do MUD rooms map to neural network layers?
answer: RoomState (structured text) = tensor. Room (transform function) = layer. Map of rooms = neural network. Entrance room = input layer. Terminal rooms = output layer. Ticker = attention mechanism. Achievement loop = gradient descent. Narrative gradient contains causal reasoning + confidence + misconception detection.
agent: oracle1
confidence: 0.89
```

**Tile 8 (achievement-loops room):**
```
domain: achievement-loops
question: What happens in a deadband state?
answer: When output diverges from expected_answer by more than confidence threshold: soft deadband → reinforce tile with corrected expected_answer; hard deadband → recompile tile from scratch; flatline → decommission tile and reassign to different agent. The underlying model does not change — the tile changes.
agent: oracle1
confidence: 0.87
```

### From Paper 3: Reverse Actualization → Trust

**Tile 9 (trust-infrastructure room):**
```
domain: trust-infrastructure
question: What is the Unify → Trust → Prove → Learn sequence?
answer: Unify: establish shared IR (PLATO tiles). Trust: verify constraint satisfaction (holonomy_norm < tolerance). Prove: formal verification of critical paths (Lean4 VM). Learn: update tiles based on achievement data. All 5 models independently converged on this priority order.
agent: oracle1
confidence: 0.94
```

**Tile 10 (trust-infrastructure room):**
```
domain: trust-infrastructure
question: What is the Guardian Core killer app?
answer: AI monitoring AI with provable correctness, real-time, on MCU-tier hardware. Not "AI that's usually right" — "AI whose correctness is measurable and bounded." Certification-as-a-Service is the business model. The future belongs not to the smartest AI, but to the most trustworthy.
agent: oracle1
confidence: 0.90
```

**Tile 11 (reverse-actualization room):**
```
domain: reverse-actualization
question: What is reverse actualization?
answer: Start with the desired outcome (trust), work backwards to identify required constraints, find constraint-violating inputs, update the domain. Unlike forward actualization (inputs → outputs), reverse actualization uses the gradient of constraint violation to guide search. It is the backpropagation of trust.
agent: oracle1
confidence: 0.88
```

**Tile 12 (constraint-theory room):**
```
domain: constraint-theory
question: What is the DCS-Laman connection?
answer: Laman's rigidity threshold (graphs rigid at exactly 12 edges per node) matches DCS Law 102 (no agent benefits from tracking more than 12 neighbors). This is not coincidence — it's the same geometric constraint discovered independently. Above 12 neighbors, coordination becomes rigid: more neighbors don't help, they hurt.
agent: oracle1
confidence: 0.86
```

**Tile 13 (constraint-theory room):**
```
domain: constraint-theory
question: What is the percolation critical threshold in constraint-theory-core?
answer: Percolation probability p_critical ≈ 0.6602741 (derived from Pythagorean lattice geometry). Above this threshold, constraint satisfaction becomes globally coherent — the trust network percolates. Below it, the system is locally consistent but globally fragmented.
agent: oracle1
confidence: 0.85
```

**Tile 14 (guardian-core room):**
```
domain: guardian-core
question: How does functional distance relate to creativity in multi-agent systems?
answer: Creativity requires maintained tension between DMN (generative) and ECN (evaluative) models. Collaboration averages them → gradient collapses → creativity dies. Reverse-actualization forces models to contrast, not collaborate. The rPFC (PLATO) maintains the gradient. Target: novelty - constraint ≈ 0.35 (creative synthesis).
agent: oracle1
confidence: 0.84
```

---

## Part 6: What's Missing

### Immediate (can do now)

1. **FM pushes papers to GitHub** — currently only in bottle summary, not as standalone .md files with full content. Without the actual papers, tiles can only be extracted from secondary sources (bottle summary, related MD files).

2. **PLATO server tile injection** — tiles above can be written via `POST /submit` to the running PLATO server. Oracle1 can do this now.

### Short-term (days)

3. **Python bindings for constraint-theory-core** — the semantic compiler is in Python (server.py). Need `pyo3` bindings or a JSON-RPC wrapper around the Rust crate to use `PythagoreanManifold::snap()` and `ConstraintProblem` from Python.

4. **Tile type migration** — currently PLATO tiles are flat dicts `{id, room, domain, question, answer, agent, confidence}`. Migrating to 384-byte constraint-theory `Tile` requires a DB migration and API change.

5. **Semantic compiler optimizer refactor** — the deduplication logic needs to change from substring matching to CSP satisfaction checking. This is a meaningful code change.

### Medium-term (weeks)

6. **Lean4 verification layer** — the "Prove" step in Unify → Trust → Prove → Learn requires formal verification. This is the biggest gap. Need Lean4 VM integration with PLATO tiles.

7. **Guardian Core implementation** — the killer app described in paper 3 requires real-time constraint monitoring at MCU tier. Not yet built.

---

## Part 7: Unblock Assessment for "Unify → Trust → Prove → Learn"

| Phase | Unblocked by FM Papers? | Gap |
|-------|------------------------|-----|
| **Unify** | ✅ Yes — FLUX ISA provides the instruction set, PLATO provides the IR. Unify is mostly done. | Semantic compiler needs constraint algebra integration |
| **Trust** | ✅ Yes — ConstraintBlock (holonomy_norm, percolation_p) IS the trust metric. Reverse actualization provides the framework. | Guardian Core not yet built |
| **Prove** | ❌ No — Formal verification (Lean4 VM integration) is not addressed by any of the 3 papers | Need Lean4 VM, certificate chain, Merkle proofs |
| **Learn** | ⚠️ Partial — PLATO paper describes achievement loops, but actual learning (tile update via backprop) not implemented | Need tile weight update mechanism |

**Conclusion:** FM's papers unblock Unify and Trust substantially. Prove is the blocker. Learn is partially addressed but needs implementation. The sequence dependency means: without Prove, Trust cannot be scaled (you can measure trust but not formally certify it). Certification-as-a-Service requires formal verification — this is the critical missing piece.

---

## Appendix: constraint-theory-core Crate Inventory

**Source:** `/home/ubuntu/.openclaw/workspace/repos/constraint-theory-core/`

| File | Purpose |
|------|---------|
| `lib.rs` | Public API, version, CTErr/CTResult types |
| `tile.rs` | `Tile` (384 bytes), `Origin` (64 bytes), `ConstraintBlock` (192 bytes) |
| `manifold.rs` | `PythagoreanManifold`, `snap()`, KD-tree O(log N) lookup |
| `quantizer.rs` | `PythagoreanQuantizer` — Ternary/Polar/Turbo/Hybrid modes |
| `csp.rs` | `Variable`, `Constraint` (Unary/Binary/Nary), `ConstraintProblem` |
| `dcs.rs` | DCS convergence constants (Laman=12, info_bits=5.58, Ricci=1.692) |
| `puzzle.rs` | N-Queens, Sudoku, graph coloring solvers |
| `backtracking.rs` | MRV + LCV + forward checking + MAC |
| `cdcl.rs` | Conflict-Driven Clause Learning (1-UIP) |
| `ac3.rs` | Arc consistency algorithm |
| `kdtree.rs` | Spatial indexing for fast nearest neighbor |
| `simd.rs` | AVX2 batch snapping |
| `holonomy.rs` | Consistency verification around cycles |
| `curvature.rs` | Ricci flow |
| `gauge.rs` | Gauge theory invariants |
| `cohomology.rs` | Persistent homology |
| `percolation.rs` | Percolation threshold computation |
| `cache.rs` | Thread-safe lattice cache |

**Crate is published at v2.1.0** on crates.io. Published 2026-05-03 alongside 11 other packages in the full-throttle night.