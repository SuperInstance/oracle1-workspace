# POLISHED: flux-vm

**Date:** 2026-07-12  
**Commit:** `30d6a9d` — "Tier 2 → Tier 1: fix CI, license, packaging"

## What Was Done

### CI Fixed
- ❌ Removed: `python-ci.yml` (Python CI for a Rust repo — ran `pytest || true`)
- ✅ Added: `ci.yml` — proper Rust CI with 4 jobs: check, test, clippy, fmt
- Uses `Swatinem/rust-cache@v2` for dependency caching
- Uses `dtolnay/rust-toolchain@stable` for consistent toolchain

### Workspace Fixed
- ❌ Was: No root `Cargo.toml` — 6 sub-crates with no workspace definition
- ✅ Now: Root `Cargo.toml` defines workspace with `resolver = "2"` and shared package metadata

### License
- Already had Apache-2.0 LICENSE file
- Fixed sub-crate repository URLs (were pointing to wrong repos like `forgemaster`)

### Code Fixes
- Fixed `flux-isa-mini` stm32_sensor example — gated with `required-features = ["defmt"]` so it doesn't break `cargo test` on hosted platforms

### README Polish
- Added CI badge and license badge
- Added ISA variant documentation table (mini/std/edge/thor)
- Added workspace crates overview table
- Added contributing section

## Test Results

```
87 tests passed, 0 failed
- flux-ast: 7 tests
- flux-isa: 4 tests
- flux-isa-mini: 7 tests
- flux-isa-std: 19 tests (5 unit + 14 integration)
- flux-isa-edge: 25 tests
- flux-isa-thor: 21 tests (12 unit + 9 integration)
```

## What Still Needs Work

- pipeline_e2e.rs has 0 tests — needs end-to-end pipeline tests
- C benchmark file (bench_goto.c) in tests/ — unusual for Rust repo
- Python test files in tests/ — should be removed or moved to integration
- Thor ISA has 8 clippy warnings (dead code) — not blocking but should be cleaned up
- No crates.io publication yet
