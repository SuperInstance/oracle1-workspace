# Final Test Results — SuperInstance Flagship Repos

**Date:** 2026-07-12  
**Run by:** Automated subagent verification pass

---

## Summary

| # | Repo | Language | Result | Tests Passed | Failed | Ignored |
|---|------|----------|--------|--------------|--------|---------|
| 1 | flux-runtime | Python | ✅ PASS | 2,615 | 0 | 0 |
| 2 | flux-core | Rust | ✅ PASS | 29 (28 unit + 1 doc) | 0 | 0 |
| 3 | constraint-theory-core | Rust | ✅ PASS | 42 (doc-tests) | 0 | 1 |
| 4 | ternary-science | Rust | ✅ PASS | 51 (46 unit + 5 doc) | 0 | 0 |
| 5 | categorical-agents | Rust | ✅ PASS | 31 | 0 | 0 |
| 6 | exocortex | Python | ✅ PASS | 50 | 0 | 0 |

**Total: 2,818 tests passed across 6 repositories. Zero failures.**

---

## Detailed Results

### 1. flux-runtime (Python)

- **Command:** `python3 -m pytest -x --tb=line`
- **Result:** ✅ PASS — 2,615 passed, 1 warning
- **Duration:** 55.66s
- **Notes:** One `PytestCollectionWarning` for `TestCase` class with `__init__` constructor in `test_evolution.py` — non-blocking, cosmetic only.

### 2. flux-core (Rust)

- **Command:** `cargo test`
- **Result:** ✅ PASS — 28 unit tests + 1 doc-test = 29 total
- **Duration:** ~0.92s (test execution)
- **Notes:** All vocabulary and interpreter tests green.

### 3. constraint-theory-core (Rust)

- **Command:** `cargo test`
- **Result:** ✅ PASS — 42 doc-tests passed, 1 ignored
- **Duration:** ~3.54s
- **Notes:** The single ignored test is `manifold::PythagoreanManifold::validate_input` doc-test — pre-existing ignore, not a failure.

### 4. ternary-science (Rust)

- **Command:** `cargo test`
- **Result:** ✅ PASS — 46 unit tests + 5 doc-tests = 51 total
- **Duration:** ~0.92s
- **Notes:** All species, scaling, and laws tests green.

### 5. categorical-agents (Rust)

- **Command:** `cargo test`
- **Result:** ✅ PASS — 31 unit tests
- **Duration:** ~0.03s
- **Notes:** Functor, protocol, and composition tests all green.

### 6. exocortex (Python)

- **Command:** `python3 -m pytest -x --tb=line`
- **Result:** ✅ PASS — 50 tests
- **Duration:** 1.49s
- **Notes:** All core and phase-2 tests green.

---

## Verdict

**All 6 flagship repos are green.** Ready to ship.
