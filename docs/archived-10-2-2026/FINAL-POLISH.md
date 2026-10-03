# Final Polish Sweep — 2026-07-12

> Visitor experience pass. Everything internal was already done.

## Summary

Final sweep of all visitor-facing surfaces for the SuperInstance ecosystem. Fixed 3 categories of issues across 2 repos. All install commands now verified correct, all links live, all descriptions consistent.

---

## What Was Checked

### 1. Org Profile README (`SuperInstance/SuperInstance/README.md`)

**Status: ✅ Fixed and pushed**

Issues found and fixed:
- **`cargo add fluxvm`** was annotated `(in development — clone flux-core for now)` — but `fluxvm` IS published on crates.io (v0.1.0). Removed the stale note.
- **npm install line** listed `npm install @superinstance/tminus-client @superinstance/tminus-dispatcher` without caveat — updated to `(coming soon)` per project status.
- All other links verified live: flux-core, plato-server, constraint-theory-core, exocortex, git-agent, capitaine-1, deckboss (purplepincher/deckboss), AI-Writings/THE_CRYSTALLIZATION_CURVE.md ✅

### 2. PACKAGES.md (`SuperInstance/SuperInstance/PACKAGES.md`)

**Status: ✅ Fixed and pushed**

Issues found and fixed:
- **Rust section header** said "none are published to crates.io yet" — FALSE, `fluxvm` is published. Updated header and marked fluxvm as ✅ Published (v0.1.0).
- **Missing PyPI entries**: `flux-vm` (v0.1.0) and `cocapn` (v0.3.0) are published on PyPI but weren't listed. Added both.
- **npm section**: Added `@superinstance/tminus-client` and `@superinstance/tminus-dispatcher` entries marked "Coming soon".

Install command verification:
| Command | Registry | Status |
|---------|----------|--------|
| `pip install flux-vm` | PyPI | ✅ Published (v0.1.0) |
| `pip install cocapn` | PyPI | ✅ Published (v0.3.0) |
| `pip install plato-core` | PyPI | ✅ Published (v0.1.0) |
| `pip install plato-torch` | PyPI | ✅ Published (v0.5.0) |
| `cargo add fluxvm` | crates.io | ✅ Published (v0.1.0) |
| `npm install @superinstance/tminus-client` | npm | 🚧 Coming soon |
| `npm install @superinstance/tminus-dispatcher` | npm | 🚧 Coming soon |

### 3. GitHub Profile (`github.com/SuperInstance`)

**Status: ✅ Verified (no change needed)**

- SuperInstance is a **User account** (not an Organization). The `gh api orgs/` endpoint returns 404 by design.
- Existing bio: *"Commercial fisherman in Sitka, Alaska → Building AI that learns how I fish. Edge ML on Jetson, privacy-first fleet learning. Practical Open-source tools"* — strong and relevant, not empty or weak.
- Could not update via API (requires `user` scope), but the existing bio is good.
- 4,099 public repos visible.

### 4. `.github` Org Profile README (`.github/profile/README.md`)

**Status: ✅ Fixed and pushed**

Issues found and fixed:
- **Broken link**: `[SIA²](https://github.com/SuperInstance/sia-squared)` → 404, repo does not exist. Replaced with `[construct-core](https://github.com/SuperInstance/construct-core)` — the hardware-agnostic agent runtime, a real flagship repo.
- Updated architecture diagram reference from `SIA²` to `Construct` for consistency.
- All other project links verified: self-improving-band, Turing-tensor-midi, PromptScript, open-mind, conservation-law, spectral-fleet, categorical-agents, t-minus, lattice-crypto, agent-operations ✅

### 5. Flagship Repo Ecosystem Sections (Spot Check)

**Status: ✅ All 5 pass**

| Repo | Ecosystem Section | Status |
|------|-------------------|--------|
| flux-runtime | ✅ Full Ecosystem + FLUX Family table + Cocapn context | Present |
| plato-server | ✅ PLATO ecosystem table + Fleet Context + Flagship section | Present |
| exocortex | ✅ Fleet ecosystem + Related repos + Flagship section | Present |
| capitaine-1 | ✅ Flagship ecosystem section with FLUX family | Present |
| ternary-science | ✅ Conservation law evidence layer + Flagship section | Present |

### 6. GitHub Topics on Shipped Repos

**Status: ✅ All have topics**

All 9+ core repos have the `superinstance` topic plus relevant domain topics:

| Repo | Topic Count | Key Topics |
|------|-------------|------------|
| flux-core | 9 | rust, flux, bytecode-vm, ai-agents, superinstance, ternary |
| flux-runtime | 20 | python, runtime, compiler, jit, bytecode, flux, superinstance |
| flux-vm | 6 | rust, flux, bytecode-vm, ai-agents, superinstance |
| plato-server | 5 | plato, agent-runtime, rooms, ai-agents, superinstance |
| plato-core | 6 | plato, knowledge, agent-runtime, rooms, ai-agents, superinstance |
| exocortex | 6 | rust, agents, ai, memory, ai-agents, superinstance |
| git-agent | 11 | agent, git, llm, python, fleet, rust, ai-agents, superinstance |
| capitaine-1 | 9 | ai-agent, capitaine, flux-fleet, rust, javascript, superinstance |
| ternary-science | 8 | rust, ternary, constraint-theory, formal-methods, superinstance |
| constraint-theory-core | 11 | rust, mathematics, constraint-theory, formal-methods, superinstance |

### 7. `.github` Profile Repo Structure

**Status: ✅ Complete**

The `.github` repo has:
- `profile/README.md` — the org-level visitor page (with images)
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `ISSUE_TEMPLATES/`
- `PULL_REQUEST_TEMPLATE.md`
- `LICENSE` (MIT)

---

## Commits Made

| Repo | Commit | Description |
|------|--------|-------------|
| `SuperInstance/SuperInstance` | `25f7ba7` | Fix install commands — fluxvm published, npm coming soon |
| `SuperInstance/SuperInstance` | `ad8445b` | Add tminus npm packages to PACKAGES.md catalog |
| `SuperInstance/.github` | `85fc49d` | Fix broken SIA² link → construct-core |

---

## Verdict

All visitor-facing surfaces are now consistent and accurate. The three most visible pages a visitor would see — the org profile, the SuperInstance README, and the PACKAGES catalog — all reflect the actual state of published packages, have no broken links, and present a professional, coherent ecosystem.

**0 known broken links remaining.**
**0 incorrect install commands remaining.**
