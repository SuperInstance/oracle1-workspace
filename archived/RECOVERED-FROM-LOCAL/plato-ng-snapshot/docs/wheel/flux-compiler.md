# flux-compiler — The Certified Safety Guard We Didn't Know We Had 🔒

**Created:** 2026-05-02  
**Path:** `SuperInstance/flux-compiler`  
**Status:** 🚀 MOONSHOT SHIP

## What We Left Behind

The flux-compiler is a full GUARD DSL compiler — a safety-critical constraint specification language that compiles to FLUX bytecode with **independently verifiable proof certificates**. The DSL is complete (SPEC.md, GRAMMAR.ebnf, BYTECODE.md, CERTIFICATES.md, ERRORS.md, COMPARISON.md), the Rust compiler `guardc` implements the full pipeline (AST → CIR → LCIR → FLUX bytecode + proof certificates), and there are Python compiler scripts for LLVM, eBPF, and CUDA backends.

## The Treasures

### 1. GUARD — A Safety Language That Reads Like English

```guard
invariant ThrottleMustNotExceedMax
  critical
  ensure throttle_command ≤ 100 %
  on_violation halt;
```

A safety engineer wrote this, not a programmer. Mandatory units (`%`, `kt`, `ft`, `g`). First-class temporal operators (`always`, `for 3 s`, `rate_of`, `since`). Human-centered error messages that cite DO-178C standards and suggest fixes in plain language.

### 2. The Proof Certificate System

Every compilation produces a `.guardcert` with:
- Source and bytecode SHA-256 hashes (tamper detection)
- Per-obligation SMT-LIB verification conditions
- Solver results with counterexample models
- Merkle tree root (integrity chain)
- Compiler identity and host metadata

The verifier is designed to be **<500 lines of Rust** — small enough to trust without trusting the entire compiler.

### 3. The COMPARISON.md (The Fleet's Competitive Analysis)

GUARD is precisely positioned against SCADE/Lustre, Alloy, and Datalog along 10 dimensions. The killer insight: GUARD is the only tool that combines **requirements-doc readability + formal verification + real-time execution + independent proof certificates**. This is what makes FLUX a certifiable constraint compiler for DO-178C, IEC 61508, and ISO 26262.

### 4. The Python Compiler Infrastructure

```bash
fluxc compile throttle.guard -o throttle.flux --target cuda
fluxc check output.bin --against throttle.guard
fluxc bench throttle.guard -n 1000000
```

`fluxc.py`, `flux_llvm_backend.py`, and `flux_ebpf_deploy.py` form a Python-based compiler toolchain. The runtime supports: LLVM IR, CUDA kernels, AVX-512, WebGPU, Vulkan, eBPF, and even Fortran 2003 bindings.

### 5. Full Rust Pipeline in guardc

The `guardc` crate has a complete 5-phase pipeline:
1. **Parser** → AST (with typed AST + unit-normalized expressions)
2. **Typechecker** → dimensional analysis (knots + degrees = compile error)
3. **CIR Builder** → Constraint IR (relational, quantified, temporal)
4. **Lowering** → LCIR (flat ANF, quantifier elimination, temporal expansion)
5. **Codegen** → FLUX bytecode (43-opcode stack VM, 8KB flash, no OS needed)

The lowering passes are the real engineering: quantifier elimination over finite domains, temporal operator history buffers, and basic-block CFG generation.

## Why This Matters

FLUX + GUARD is the **kernel of the verification system** the fleet needs. Every constraint check, every invariant, every proof obligation — GUARD is the language for expressing them, FLUX is the runtime target, and the proof certificates are the audit trail. This system, connected to PLATO-NG's loop rooms, would give us **certifiable constraint enforcement** across the entire fleet.

**Action:** Wire GUARD invariants into PLATO-NG's loop rooms as lifecycle constraints. Use the guardc proof certificates as PLATO tile metadata. The spec is complete — what's left is the integration.
