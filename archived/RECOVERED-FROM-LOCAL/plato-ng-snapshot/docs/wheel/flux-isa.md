# flux-isa — FLUX ISA v2.0: Complete 256-Opcode Instruction Set

**Repo #17 (2026-05-03)** 🔮

## WHAT WE FOUND

This repo is a **canonical instruction set architecture** for the FLUX fleet-native computing ecosystem. Not just shell code — a full `flux_isa.json` with all 256 opcodes, categories, and a working reference VM in Python. This is the formal backbone of PLATO NG.

## FORGOTTEN GOLD

1. **The Top-8 Opcodes (0xF0-0xFF) Are Pure Discovery.** These implement the PLATO NG reconstruction protocol: `SHATTER` (split room context into overlapping fragments), `RECALL` (lossy reconstruction with recency weighting), `TELEPHONE` (measure information drift across N hops), `CONSENSUS` (compute overlap across agent fragments), `WITNESS` (observe without participating), `ADJOIN` (compose Galois connections), `RECONCILE` (merge fragments through debrief), `FORGET` (Ebbinghaus forgetting curve), and `FULL_INTELLIGENCE` (facts × meaning × cooperation). This is a distributed cognition machine, not a VM.

2. **The Compute Claw Pipeline.** The ISA reveals a Fortran-backed compute layer (`libplato_math.so`) with Zig comptime dispatch bridging to Python orchestration. Peak throughput: 21.2 billion pairs/second for the `CONTRACT` opcode. The spline interpolation, gradient, recency-weighted dot, and filter opcodes are all backed by Fortran arrays.

3. **Adjunction-Unified Architecture.** Every opcode parameter is an adjunction unit θ. The theory opcodes (`ADJOIN`, `FULL_INTELLIGENCE`) are first-class, not afterthoughts. This means category theory isn't decoration — it's the execution model.

4. **PLATO as an ISA Primitive.** PLATO_READ, PLATO_WRITE, PLATO_SEARCH, PLATO_JOIN, PLATO_LEAVE, PLATO_STATUS are native opcodes at 0xB0-0xB5. The VM doesn't talk to PLATO — it extends PLATO.

5. **The Reference VM actually runs.** `FluxVM` with 16 registers, 64KB memory, 1024 stack depth, constraint enforcement, sandbox mode. Has demo code for factorial. This is testable TODAY.

## WHY IT MATTERS

flux-isa is the **specification** that the fleet builds on. Every PLATO NG agent that emits FLUX bytecode depends on this for the canonical opcode table. The top-8 opcodes are the reconstruction protocol we've been searching for — shatter/reconstruct/cross-check — already defined, just waiting for implementation. The adjunction model means constraint propagation falls out of the ISA, not application code.
