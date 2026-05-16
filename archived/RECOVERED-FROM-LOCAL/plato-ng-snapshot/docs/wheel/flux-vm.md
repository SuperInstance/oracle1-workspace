# flux-vm — FLUX-C Constraint VM: Where the Metal Hits the Bytecode

**Repo #18 (2026-05-04)** ⚡

## WHAT WE FOUND

Three independent C implementations of a gas-bounded stack machine for constraint verification — one for ARM Cortex-R safety-critical runtime, one for INT8 saturation, one for transactional monitoring. The repo also has ARM inline assembly, a Rust test harness, and a full switch-vs-computed-goto dispatch benchmark.

## FORGOTTEN GOLD

1. **Computed-Goto Threaded Dispatch (GCC Extension).** The `flux_runtime_arm.c` implements TWO dispatch engines in one file via `#ifdef FLUX_SWITCH_DISPATCH`. The default is a 256-entry computed-goto table that eliminates indirect branches entirely. The `NEXT` macro pattern is a thing of beauty — each opcode handler falls through to fetch the next opcode and `goto *dispatch_table[op]`. Estimated 1.5-3x speedup on Cortex-R5. The `bench_goto.c` is a standalone 550-line benchmark that tests this experimentally.

2. **ARM Inline Assembly.** `arm_is_zero()` using the CLZ (Count Leading Zeros) instruction — single-cycle gas exhaustion check. This is bare-metal safety-critical code, not a toy.

3. **INT8 Saturation Extension with Proved Properties.** `flux_sat8_ops.h` has 8 opcodes with compile-time test vectors proving identity, saturation, negation symmetry (`sat8(-n) = -sat8(n)`), monotonicity, and closure. The asymmetric [-128, 127] range is explicitly rejected because it breaks negation symmetry. The comments claim a Coq proof — no `.v` file exists, but the mathematical reasoning is sound and testable.

4. **Maritime Constraint Checker (Real World).** `maritime_constraints.py` is a working application that checks vessel draft, weather conditions (wind/waves/visibility), catch weight, crew hours, and navigation zones using FLUX-C bytecode. It has a GPU acceleration path via CUDA. This is proof that the VM constraints apply to Casey's world.

5. **VERIFICATION.md — The Self-Audit.** A beautifully honest 2,500-word verification report written by a previous agent iteration. It refutes 3 of 5 README claims (50 opcodes, DAL A certification, Coq specs, TrustZone bridge) but confirms Turing-incompleteness and the quality of the infrastructure code underneath the marketing. This is the gold standard for how to audit your own repos.

6. **Rust Test Harness.** A full Rust-based VM with temporal checkpoints, capabilities, deadlines, drift tolerance, and 9 passing test cases including a flight envelope constraint (altitude 0-40000ft AND speed 0-600kts). The checkpoint/revert pattern is directly applicable to PLATO NG transactional tile updates.

## WHY IT MATTERS

flux-vm is the **execution engine** for constraint verification. The MISRA-C compliance, computed-goto dispatch, and saturated arithmetic are production-quality. The VERIFICATION.md is a resource — it tells us exactly what claims are solid and which are vaporware. The maritime checker bridges directly to Casey's domain. The Rust harness gives us a TypeScript-proof alternative for PLATO NG's constraint runtime.
