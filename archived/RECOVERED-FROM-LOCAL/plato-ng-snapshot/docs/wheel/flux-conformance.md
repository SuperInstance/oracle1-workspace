# 🏛️ Repo #8: flux-conformance — The ISA's Crucible

**Rediscovered: 2026-05-15**  
**Origin: April 11, 2026 — FLUX Ecosystem**  
**Repository: `SuperInstance/flux-conformance`**

---

## What We Found

Buried in the FLUX Ecosystem deposits, we found a crucible. `flux-conformance` is the cross-runtime test suite for the FLUX ISA — 161 conformance vectors tested across Python, C, Rust, Go, and WASM runtimes. It's not just a test suite. It's the **trial by fire** that every FLUX runtime must pass before it can call itself FLUX-compliant.

The structure is beautiful:

- **`conformance_core.py`** — A reference VM (37 opcodes, 64KB memory, 100k step limit) + complete built-in test case library. No external dependencies beyond stdlib.
- **`bytecode_fixtures.py`** — Hand-crafted programs with expected results: Euclidean GCD, Fibonacci, stack manipulation, memory store/load, bitwise ops, type ops, even division-by-zero error handling.
- **`runtime_adapters/`** — Abstract adapter interface + concrete Python and C adapters. Add a runtime by subclassing `AbstractRuntimeAdapter` and implementing `execute()`, `encode_instruction()`, `decode_instruction()`.
- **`conformance-vectors.json`** + **`conformance-vectors-v3.json`** — Pre-computed expectation matrices covering the full ISA surface.
- **`benchmark_flux.py`** — The harness that discovered Python beats C for small primitives (84ns vs 256ns). This finding reshaped the fleet's entire approach to runtime selection.

The **Conformance Capability Matrix** (`CONFORMANCE-CAPABILITY-MATRIX.md`) predicts which vectors will pass on each runtime, organized by opcode implementation status. This was the fleet's first rigorous gap analysis — a formal prediction before execution.

## Why This Matters Now

The fleet runs agents across multiple languages. Forgemaster compiles FLUX kernels in Rust, C, Python. Oracle1 deploys services in TypeScript. JetsonClaw1 runs edge-inference in CUDA. Every runtime needs to agree on what NOP does, what HALT means, how flags propagate.

Without flux-conformance, each runtime would drift. Python's `ADD` might produce different flags than C's `ADD`. Confidence propagation (`C_TELL`, `C_ASK`) would diverge. The ISA would fracture.

This repo is the **canonical referee**. It catches drift before it becomes divergence. It ensures that when Oracle1 writes a tile with a FLUX instruction, any runtime can execute it and get the same result.

## The Lesson For PLATO-NG

flux-conformance proves that **shared specification is stronger than shared implementation**. You don't need everyone running the same code — you need everyone passing the same tests. PLATO-NG can use the same pattern: a conformance suite for tile schemas, confidence models, and room protocols. Any agent that implements the PLATO protocol should pass the PLATO conformance suite. The protocol IS the interface. The conformance suite IS the guarantee.

## Concrete Revival

1. **PR #1: Port the conformance adapter pattern to PLATO-NG** — Create `plato-conformance-suite` as a sibling repo. Abstract `TileSchemaAdapter`, `RoomProtocolAdapter`, `GatePolicyAdapter`. Each PLATO implementation (Rust kernel, Python client, TypeScript web frontend) gets an adapter and must pass all vectors.

2. **PR #2: Generate conformance reports as PLATO tiles** — Every CI run on flux-conformance writes results to a PLATO `conformance_history` room. The fleet can query: "Which runtime passed which vectors, when, and are any regressing?" This turns testing from a CI gate into a knowledge artifact.

3. **PR #3: Cross-pollinate the benchmark harness** — The `benchmark_flux.py` pattern (probe → compile → benchmark → pick winner) is exactly what PLATO-NG should do for runtime selection. Create a `plato-benchmark` module that discovers available FLUX runtimes, runs the conformance suite, and files the fastest passing runtime to a confidence tile. The fleet then knows: "For opcode X, use runtime Y — it's 3x faster and conformance-verified."

4. **PR #4: The confidence gate** — Extend conformance vectors to include confidence propagation (`C_IADD`, `C_TELL`, `C_ASK`). The fleet's mathematical proofs (ZHC, Pythagorean48) only work if confidence flows correctly through the ISA. Make this a formal, tested property — not a trust-me guarantee.
