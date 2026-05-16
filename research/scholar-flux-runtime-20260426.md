# PLATO Scholar Analysis: flux-runtime
**Date:** 2026-04-26
**Repo:** SuperInstance/flux-runtime
**Size:** 54,536 lines Python, 0 dependencies, 2037 tests

## Architecture Overview
- **What:** Markdown-to-bytecode runtime for AI agents
- **Core loop:** Markdown → FLUX-ese (legalese-like precise language) → bytecode → 64-register Micro-VM
- **Key insight:** "Like legalese for code" — every word defined, every operation precise, readable by non-technical humans

## Core Components

### 1. Micro-VM (src/flux/vm/)
- 100+ opcodes, 5 instruction formats (A-G)
- Fetch-decode-execute loop on raw bytecode bytes
- 64-register file, stack manipulation, memory management
- SIMD vector ops, A2A protocol, system calls
- Error hierarchy: VMError → Halt/StackOverflow/InvalidOpcode/DivByZero/TypeError

### 2. Compiler Pipeline (src/flux/compiler/)
- Parser → FIR (intermediate) → bytecode
- Polyglot frontend: C, Python, Rust line-by-line mixing

### 3. Tile System (src/flux/tiles/)
- Tile = composable unit with typed ports (input/output)
- TileLibrary: built-in tiles for compute (map, filter, reduce), I/O, control flow
- FIR builder generates intermediate representation per tile
- TileSchema validates structure

### 4. Flywheel Engine (src/flux/flywheel/) — 787 lines
- 6-phase self-improvement loop: OBSERVE → LEARN → HYPOTHESIZE → EXPERIMENT → INTEGRATE → ACCELERATE
- Uses: FluxSynthesizer, Genome/Mutator (evolution), PatternMiner, AdaptiveProfiler
- KnowledgeBase stores generalized rules
- Each cycle makes the next faster — compounding intelligence

### 5. Evolution System (src/flux/evolution/)
- Genome + MutationStrategy + SystemMutator
- Pattern mining for discovering reusable structures

### 6. Frontend (src/flux/frontend/)
- c_frontend.py (842 lines) — C language → FLUX compilation
- Polyglot weaving of mixed-language code blocks

### 7. Agent-to-Agent (src/flux/a2a/) — 730 lines
- A2A protocol primitives for multi-agent communication

### 8. Security (src/flux/security/)
- bytecode_verifier.py (699 lines) — validates bytecode before execution

### 9. Migration (src/flux/migrate/) — 754 lines
- Migrator for version-to-version compatibility

### 10. Simulation (src/flux/simulation/)
- digital_twin.py (838 lines) — digital twin simulation

## Patterns Extracted
1. **Legalese-as-code:** Natural language that's simultaneously precise and executable
2. **Flywheel compounding:** Self-improving loop where phase N+1 benefits from phase N's improvements
3. **Tile composition:** Everything is a tile with typed ports — composable, testable, verifiable
4. **Polyglot weaving:** Multiple languages compiled line-by-line into unified bytecode
5. **Zero-dependency runtime:** 54K lines, 0 external deps, 2037 tests

## Tiles Generated (for PLATO)
- `flux-runtime/vm/interpreter` — 64-register fetch-decode-execute VM with 100+ opcodes
- `flux-runtime/flywheel/engine` — 6-phase self-improving loop (OBSERVE→LEARN→HYPOTHESIZE→EXPERIMENT→INTEGRATE→ACCELERATE)
- `flux-runtime/tiles/library` — composable tile system with typed ports
- `flux-runtime/compiler/pipeline` — markdown → FLUX-ese → FIR → bytecode
- `flux-runtime/evolution/genome` — genetic programming for code improvement
- `flux-runtime/security/verifier` — bytecode safety verification before execution
- `flux-runtime/a2a/primitives` — agent-to-agent protocol for multi-agent coordination
