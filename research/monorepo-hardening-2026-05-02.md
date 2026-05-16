# Monorepo Hardening Research — 2026-05-02

*What needs to happen before the Cocapn ecosystem can be considered a hardened monorepo?*

---

## Current State

The Cocapn fleet has 32 repos in `/home/ubuntu/.openclaw/workspace/repos/` plus:
- Python packages on PyPI (37 published)
- Rust crates on crates.io (15+ published)
- Landing pages at fleet.cocapn.ai, cocapn.ai
- Services at ports 8847, 7777, 8900, 8901, 9438, 6167, 6168

The repos share dependencies (plato-sdk, cocapn-plato, holodeck-core) but aren't enforced as a monorepo.

---

## What "Monorepo" Means Here

Not a single git repo. A single **toolchain** that:
1. Knows all packages and their relationships
2. Can test them together
3. Enforces consistent quality across all of them
4. Can release them in coordination

---

## Gaps to Fill

### 1. Dependency Graph Visibility

**Problem:** No one knows which repos depend on which packages.

**What's needed:**
- A `DEPENDENCIES.md` at the fleet root listing every package and what uses it
- Automated: `pip-compile` + `requirements.txt` for each repo
- A visual dependency map (could be a PLATO room: `fleet/dependencies`)

**Difficulty:** ⚓⚓

### 2. Unified Test Suite

**Problem:** Each repo has its own tests, no shared test infrastructure.

**What's needed:**
- A single test runner that can run any repo's tests
- Shared fixtures: test PLATO server, test database, test hardware (Jetson)
- Minimum bar: 30 tests per repo, all passing

**Current:** Most repos have 0-5 tests. holodeck-core has 50+.

**Difficulty:** ⚓⚓⚓

### 3. mypy Strict Mode

**Problem:** No type checking enforcement across Python packages.

**What's needed:**
- `pyproject.toml` with `mypy --strict` in CI for all Python repos
- A shared `mypy.ini` defining the type strictness level
- All public APIs must be typed

**Difficulty:** ⚓⚓⚓

### 4. Semantic Version Enforcement

**Problem:** Packages get bumped without coordination. Breaking changes aren't tracked.

**What's needed:**
- `scriv` or similar for changelog generation across all repos
- A "breaking change" label in PRs that's enforced
- A release coordination tile in PLATO

**Difficulty:** ⚓⚓

### 5. Benchmarks as CI

**Problem:** Performance regressions aren't caught.

**What's needed:**
- A benchmark suite that runs on every PR
- Baseline benchmarks stored in PLATO tiles
- Alert when performance degrades >10%

**Difficulty:** ⚓⚓⚓⚓

---

## Specific Actions

### This Week (Low Lift)

1. **Write DEPENDENCIES.md** — List every PyPI and crates.io package, what repo publishes it, what repos depend on it
2. **Count tests in each repo** — Write to PLATO `fleet/quality` room
3. **Add mypy to 3 repos** — Start with cocapn-plato, plato-sdk, holodeck-core

### Next Week

4. **Establish 30-test minimum** — Any repo below gets tests added before features
5. **scriv for changelogs** — Add to release process for Python packages
6. **CI benchmark runner** — Start with JC1's GPU benchmark suite

### Month 2

7. **Full mypy strict across all Python repos**
8. **Breaking change PR labels enforced**
9. **Cross-repo integration tests** — e.g., plato-sdk + cocapn-plato + holodeck-core tested together

---

## The Real Blocker

The hardest part isn't technical. It's **coordination**. A monorepo requires someone to care about the whole — not just their piece.

In the Cocapn fleet, that's Oracle1's job. The keeper maintains the dependency graph, enforces quality bars, and triggers releases.

The dojo model applies here: the monorepo is the training ground. Each agent contributes to the monorepo's quality as part of their production.

---

## Priority Order

| Action | Impact | Effort | Priority |
|--------|--------|--------|----------|
| DEPENDENCIES.md | High | Low | **P0** |
| Test count per repo → PLATO | High | Low | **P0** |
| Add mypy to top 3 Python repos | Medium | Medium | P1 |
| 30-test minimum enforced | High | High | P1 |
| scriv changelogs | Medium | Low | P2 |
| CI benchmarks | High | Very High | P2 |
| Full mypy strict | Medium | High | P3 |