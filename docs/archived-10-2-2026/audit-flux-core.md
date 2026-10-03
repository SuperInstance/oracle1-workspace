# Deep Audit: flux-core

**Repo:** SuperInstance/flux-core  
**Tier:** 1 — Ship-Ready ✅  
**Language:** Rust  
**License:** MIT  
**Audited:** 2026-07-12  

---

## Overview

Rust implementation of the FLUX bytecode runtime — VM, assembler, A2A agent protocol, and vocabulary system. Includes criterion benchmarks.

## Metadata

| Metric | Value |
|--------|-------|
| Stars | 2 |
| Forks | 0 |
| Size | 197 KB |
| Open Issues | 0 |
| Last Pushed | 2026-06-14 |
| Rust Edition | 2021 |
| Dependencies | regex 1 |
| Dev Dependencies | criterion 0.5 |

## Structure

```
flux-core/
├── src/
│   ├── a2a/           # Agent-to-agent protocol
│   ├── bytecode/      # Bytecode definitions
│   ├── vm/            # Virtual machine
│   ├── vocabulary/    # Vocabulary system
│   ├── error.rs       # Error types
│   └── lib.rs         # Library root
├── tests/
│   ├── test_a2a.rs        # 2 tests
│   ├── test_assembler.rs  # 4 tests
│   ├── test_vm.rs         # 6 tests
│   └── vocabulary_tests.rs # 28 tests
├── benches/
│   └── vm_benchmark.rs    # Criterion benchmarks
├── flux-core/         # Nested crate (possibly a sub-crate)
├── Cargo.toml
└── Cargo.lock
```

## Test Suite

**40 tests total:**
- `test_vm.rs`: 6 tests (VM execution)
- `test_assembler.rs`: 4 tests (assembly)
- `test_a2a.rs`: 2 tests (A2A protocol)
- `vocabulary_tests.rs`: 28 tests (vocabulary system)

## CI/CD

Three workflows:
1. **ci.yml** — `cargo check --all-targets --all-features`, `cargo test --all-features`, `cargo clippy -- -D warnings`
2. **rust-ci.yml** — Additional Rust CI
3. **publish.yml** — crates.io publishing workflow

CI quality is **excellent**: uses dtolnay/rust-toolchain, caches cargo registry, enforces clippy with warnings-as-errors.

## What It Needs

1. **More integration tests** — Current 40 tests are primarily unit-level
2. **Nested flux-core/ subcrate** — Confusing structure; clarify or merge
3. **crates.io publication** — publish.yml exists but no evidence of actual publication
4. **Documentation** — Rust doc comments + mdBook would be ideal
5. **Version strategy** — Currently 0.1.0; define path to 1.0

## Verdict

**Excellent Rust crate.** Clean structure, proper CI with clippy-as-errors, benchmarks, good test count. Ready for crates.io publication.
