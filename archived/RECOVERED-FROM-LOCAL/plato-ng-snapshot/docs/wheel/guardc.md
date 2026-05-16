# guardc — GUARD → FLUX Verified Compiler

> **Dated:** 2026-05-05 · **Repository:** SuperInstance/guardc

## The Core Insight

A domain-specific language (GUARD) for specifying safety constraints — think GD&T for software — compiled through 6 pipeline stages to FLUX ISA bytecode with independently-checkable proof certificates. 2541 lines across 9 Rust modules.

## Forgotten Gold

### 1. Unit-Aware Type System

The CIR (Constraint IR) carries physical units through the entire pipeline: meters, seconds, kilograms, Kelvin, radians, amperes, moles. Unit arithmetic (product, division, normalization) is implemented with rational power-products of base dimensions. This means **dimensional analysis at compile time** — a constraint about temperature won't accidentally apply to distance.

### 2. Six-Stage Verified Pipeline

| Stage | Lines | What |
|-------|-------|------|
| AST | 252 | Raw syntax tree |
| CIR | 431 | Constraint IR with types + units |
| LCIR | 263 | Flat A-normal form |
| Lowering | 635 | Quantifier elimination, temporal expansion |
| Codegen | 355 | LCIR → FLUX bytecode |
| Proof | 401 | SMT-LIB + Merkle certificate |

The **lowering** stage is the real gold: it eliminates quantifiers over finite domains, expands temporal operators (Always, Eventually, Next) into history buffer operations, flattens relations into simple atoms, and emits explicit CFG with jumps and branches.

### 3. SMT-LIB Proof Certificates

Every compiled GUARD program produces a `.guardcert` JSON artifact containing:
- Source and bytecode SHA-256 hashes (tamper detection)
- Per-obligation SMT-LIB verification conditions
- Solver results with counterexample models
- A Merkle root chaining all obligations

This is **zero-trust compilation** — the certificate can be independently verified without trusting the compiler. The cert format supports SMT2, LFSC, and native modes with configurable hash algorithms (SHA-256 / Blake3).

### 4. Temporal Operators in a Constraint DSL

The GUARD DSL embeds Linear Temporal Logic: `Always`, `Eventually`, `Next`, `Until`, `Since`, `For` (duration), `After` (duration), `Old`, `RateOf` (derivative), `Delta` (difference). The lowering pass expands these into explicit history-buffer operations on the FLUX VM — making it possible to specify constraints like "rate of change must never exceed 5 units per second" as a compile-time-checkable property.

### 5. FLUX Stack VM Memory Layout

The codegen targets a specific 43-opcode FLUX ISA with carefully designed memory:
- Slots 0-31: Constants
- Slots 32-127: State variables
- Slots 128-223: Temporal history buffers
- Slots 224-255: Scratch / locals

This layout reflects the constraint execution model: constants at the bottom, state in the middle, history buffers above, temporaries at the top. It's a **constraint-first VM** design.

### 6. A-Form (ANF) as Intermediate Representation

The LCIR enforces A-normal form — every sub-expression is bound to a variable. This simplifies codegen to direct opcode emission, and makes term-rewriting (for quantifier elimination, temporal expansion) trivially correct.

## Relevance to Wheel

This predates the quality gate stream but contains its exact pattern: DSL → verified IR → bytecode → proof certificate. The temporal lowering and unit analysis are directly applicable to the Wheel's constraint emission rules.
