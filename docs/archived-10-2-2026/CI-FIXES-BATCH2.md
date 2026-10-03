# CI Fixes — Batch 2

**Date:** 2026-07-12  
**Operator:** OpenClaw subagent  
**Scope:** SuperInstance org — second wave of CI hardening  
**Starting rate limit:** 3944  
**Ending rate limit:** 3222  
**Total commits:** 25 workflow files pushed across 25 repos

---

## Summary

Batch 1 fixed 54 repos. This batch addressed the remaining priority repos identified in the engineering ideation doc, plus scanned ~80 additional repos across the org.

| Category | Count |
|---|---|
| Priority repos fixed (broken CI) | 6 |
| Additional repos fixed (`|| true` masking) | 2 |
| New CI created (missing entirely) | 17 |
| Already good (no action needed) | 3 |
| Skipped (documentation-only repos) | 3 |
| **Total repos touched** | **25** |

---

## Priority Repos — Issues Found & Fixed

### 1. plato-engine-block-zig (Zig, master)
- **Issue:** No CI at all — no `.github/workflows/` directory
- **Fix:** Created `ci.yml` with 3-job Zig pattern (lint via `zig fmt`, test via `zig build test`, build via `zig build`)
- **Commit:** `712ddf5`

### 2. plato-core (Python, master)
- **Issue:** `|| true` at end of `pytest || python -m pytest || true` — **masks all test failures**. Also `2>/dev/null || true` on dependency install steps. No lint or build jobs.
- **Fix:** Replaced with standardized Python 3-job CI (lint via ruff, test with matrix, build via `python -m build`). Removed all `|| true` masking.
- **Commit:** `5eb3b8c`

### 3. plato-audio-jepa (Rust, main)
- **Issue:** Single monolithic job running `cargo check`, `cargo test`, and `cargo clippy` in sequence. No separate lint/build jobs.
- **Fix:** Split into standardized Rust 3-job pattern (lint with fmt+clippy, test, build release).
- **Commit:** `9387a3f`

### 4. plato-vision-jepa (Rust, main)
- **Issue:** Same monolithic single-job pattern as plato-audio-jepa.
- **Fix:** Same Rust 3-job split.
- **Commit:** `a610954`

### 5. exocortex (Python, master)
- **Issue:** Only had a test job. No lint or build jobs.
- **Fix:** Upgraded to standardized Python 3-job CI.
- **Commit:** `72e2c9b`

### 6. plato-torch (Python, main)
- **Issue:** `|| true` at end of `python -m pytest ... || true` — **masks all test failures**. Also `--exit-zero` on flake8 (non-critical but inconsistent).
- **Fix:** Replaced with standardized Python 3-job CI. Removed all failure masking.
- **Commit:** `009f2ec`

---

## Already Good (No Action Needed)

| Repo | Language | Assessment |
|---|---|---|
| plato-engine-block-elixir | Elixir | Proper 2-job CI (lint via `mix format`, test with OTP matrix). Solid. |
| flux-vm | Rust | 4-job CI (check, test, clippy, fmt). Comprehensive. |
| flux-compiler | Rust | Full CI with test, lint, bench, MSRV check, plus Metal SRAM Bake workflow. Excellent. |

---

## Additional Repos — `|| true` Failures Fixed

### plato-dojo (Python, main)
- **Issue:** `pytest || true` masks all test failures
- **Fix:** Standardized Python 3-job CI
- **Commit:** `31bf966`

### plato-construct (HTML, main)
- **Issue:** `tidy -q -e "$f" || true` makes HTML validation completely ineffective
- **Fix:** Removed `|| true`, added proper lint/test/build pattern for HTML projects
- **Commit:** `dd938f5`

---

## New CI Created — Missing CI Repos

All received standardized lint/test/build workflows matching their primary language:

| Repo | Language | Branch | Commit |
|---|---|---|---|
| openconstruct-jetson | C++ | main | `a24978d` |
| oracle1-chronicle | Python | main | `2a2ed64` |
| oracle2 | Rust | master | `0b5a3fd` |
| penrose-lattice | Rust | main | `4ba17c1` |
| perception-action | Python | master | `a8f188f` |
| physics-clock | Python | master | `60d3e34` |
| plato-a2a | Rust | main | `4887974` |
| plato-alignments-early-version | Python | main | `8293bfc` |
| plato-calibration-early-version | Python | main | `f7e6706` |
| plato-client-php | PHP | main | `0facb70` |
| plato-contract | Rust | main | `caf46d4` |
| plato-correlator | Rust | main | `a526492` |
| wasserstein-narrative | TypeScript | main | `48ea943` |
| watch-follow | Python | main | `3c80000` |
| zhc-chain | Rust | main | `2b0de68` |
| zhc-consensus | Rust | master | `7cbcb70` |
| zhc-yang-mills | Python | master | `b6e3a6c` |

---

## Skipped — Documentation-Only Repos (No CI Needed)

| Repo | Description |
|---|---|
| wiki | Deprecated, docs only |
| zeitgeist-protocol | README + LICENSE only, 0 KB |
| zeroclaws | Architecture docs, no code |

---

## CI Patterns Standardized

### Rust (11 repos)
```
lint:   cargo fmt --check + cargo clippy -D warnings
test:   cargo test --workspace
build:  cargo build --workspace --release
```

### Python (11 repos)
```
lint:   ruff check .
test:   pytest -v (matrix: 3.10, 3.11, 3.12)
build:  python -m build --sdist --wheel
```

### Zig (1 repo)
```
lint:   zig fmt --check src/
test:   zig build test
build:  zig build
```

### C++ (1 repo)
```
lint:   clang-format --dry-run --Werror
test:   cmake + ctest
build:  cmake --build (Release)
```

### TypeScript (1 repo)
```
lint:   eslint .
test:   npm test (matrix: node 18, 20, 22)
build:  npm run build --if-present
```

### PHP (1 repo)
```
lint:   php-cs-fixer --dry-run
test:   phpunit (matrix: 8.1, 8.2, 8.3)
build:  composer dump-autoload --optimize
```

### HTML (1 repo)
```
lint:   tidy validation (no || true)
test:   internal link checker
build:  copy to dist/
```

---

## Rate Limit Tracking

| Check Point | Remaining |
|---|---|
| Start | 3944 |
| After priority repos (6) | 3837 |
| After batch 2 (14 more) | 3374 |
| After batch 3 (5 more) | 3222 |

Never dropped below 500 threshold.

---

## Methodology

- All workflow files pushed via GitHub Contents API (PUT) — no git clones needed
- Existing file SHAs fetched for updates (not creates)
- Each workflow targets the repo's default branch
- `|| true` and `continue-on-error: true` on critical steps treated as P0 bugs
- Stub/placeholder workflows replaced entirely
- Language detected from repo metadata to select appropriate CI template
