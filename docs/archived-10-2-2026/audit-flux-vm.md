# Deep Audit: flux-vm

**Repo:** SuperInstance/flux-vm  
**Tier:** 2 — Near-Ready 🔧  
**Language:** Rust  
**License:** NOASSERTION  
**Audited:** 2026-07-12  

---

## Overview

FLUX-C constraint VM with 50 opcodes, stack-based architecture. Multiple ISA variants: mini, std, edge, thor. Includes bridge and AST components.

## Metadata

| Metric | Value |
|--------|-------|
| Stars | 1 |
| Forks | 0 |
| Size | 181 KB |
| Open Issues | 0 |
| Last Pushed | 2026-05-17 |

## Structure

```
flux-vm/
├── vm/
│   └── flux_vm.rs        # Core VM implementation
├── flux-ast/             # AST definitions
├── flux-isa/             # Standard ISA
├── flux-isa-mini/        # Minimal ISA
├── flux-isa-edge/        # Edge ISA
├── flux-isa-thor/        # Thor ISA
├── bridge/               # Language bridge
├── src/                  # Main source
├── tests/
│   ├── flux_vm_test_harness.rs  # 10 tests
│   ├── pipeline_e2e.rs          # End-to-end (0 tests)
│   ├── test_fleet_integration.py
│   ├── test_multi_compiler.py
│   └── bench_goto.c             # C benchmark
└── test_sat8/            # SAT solver tests
```

## Issues

1. **No root Cargo.toml** — Workspace is undefined. Sub-crates may not build independently.
2. **Python CI for Rust repo** — `python-ci.yml` is the CI workflow, not a Rust CI
3. **License is NOASSERTION** — Legally unusable
4. **C benchmark file** in tests — unusual for Rust repo

## What It Needs

1. **Add proper Rust CI** (cargo check, test, clippy)
2. **Define root Cargo.toml as workspace**
3. **Fix license** (MIT or Apache-2.0)
4. **Add integration tests** (pipeline_e2e.rs has 0 tests)
5. **Document ISA variants** — What differentiates mini/std/edge/thor?
6. **Remove Python test files** or justify their presence
