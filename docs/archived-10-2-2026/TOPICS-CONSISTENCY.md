# GitHub Topics Consistency Audit

**Date:** 2026-07-12  
**Operator:** OpenClaw subagent  
**Status:** ✅ Complete — all 26 repos tagged

---

## Overview

Applied consistent topic tags across all SuperInstance org repos so they cluster together on GitHub's topic discovery pages. GitHub Topics function as lightweight, decentralized categories — consistent tagging improves cross-repo discoverability and org coherence.

## Topic Taxonomy

### Org-Wide Tags (all repos)
| Tag | Purpose |
|-----|---------|
| `superinstance` | Org-wide unifier — every repo carries this |
| `ai-agents` | Core domain identifier |

### Family-Specific Tags

**FLUX family** (`flux-runtime`, `flux-core`, `flux-js`, `flux-compiler`, `flux-vm`):
- `flux` — product family
- `bytecode-vm` — technical category
- `deterministic-execution` — key property

**PLATO family** (`plato-server`, `plato-engine-block-c`, `plato-runtime-kernel`, `plato-engine-block-elixir`, `plato-engine-block`, `plato-core`):
- `plato` — product family
- `agent-runtime` — technical category
- `rooms` — core concept

**Theory family** (`constraint-theory-core`, `constraint-theory-py`, `ternary-science`, `lau-hodge-theory`):
- `constraint-theory` — research domain
- `ternary` — mathematical foundation
- `formal-methods` — methodology

**Infra/Agent repos** (`exocortex`, `construct-core`, `crab`, `categorical-agents`, `grand-pattern-rs`, `git-agent`, `git-agent-codespace`, `capitaine-1`, `codespace-edge-rd`, `AI-Writings`, `SuperInstance`):
- Org-wide tags only (`superinstance`, `ai-agents`)

## Results

| # | Repo | Topics Applied | Status |
|---|------|---------------|--------|
| 1 | `flux-runtime` | superinstance, ai-agents, flux, bytecode-vm, deterministic-execution | ✅ |
| 2 | `flux-core` | superinstance, ai-agents, flux, bytecode-vm, deterministic-execution | ✅ |
| 3 | `flux-js` | superinstance, ai-agents, flux, bytecode-vm, deterministic-execution | ✅ |
| 4 | `flux-compiler` | superinstance, ai-agents, flux, bytecode-vm, deterministic-execution | ✅ |
| 5 | `flux-vm` | superinstance, ai-agents, flux, bytecode-vm, deterministic-execution | ✅ |
| 6 | `plato-server` | superinstance, ai-agents, plato, agent-runtime, rooms | ✅ |
| 7 | `plato-engine-block-c` | superinstance, ai-agents, plato, agent-runtime, rooms | ✅ |
| 8 | `plato-runtime-kernel` | superinstance, ai-agents, plato, agent-runtime, rooms | ✅ |
| 9 | `plato-engine-block-elixir` | superinstance, ai-agents, plato, agent-runtime, rooms | ✅ |
| 10 | `plato-engine-block` | superinstance, ai-agents, plato, agent-runtime, rooms | ✅ |
| 11 | `plato-core` | superinstance, ai-agents, plato, agent-runtime, rooms | ✅ |
| 12 | `constraint-theory-core` | superinstance, ai-agents, constraint-theory, ternary, formal-methods | ✅ |
| 13 | `constraint-theory-py` | superinstance, ai-agents, constraint-theory, ternary, formal-methods | ✅ |
| 14 | `ternary-science` | superinstance, ai-agents, constraint-theory, ternary, formal-methods | ✅ |
| 15 | `lau-hodge-theory` | superinstance, ai-agents, constraint-theory, ternary, formal-methods | ✅ |
| 16 | `exocortex` | superinstance, ai-agents | ✅ |
| 17 | `construct-core` | superinstance, ai-agents | ✅ |
| 18 | `crab` | superinstance, ai-agents | ✅ |
| 19 | `categorical-agents` | superinstance, ai-agents | ✅ |
| 20 | `grand-pattern-rs` | superinstance, ai-agents | ✅ |
| 21 | `git-agent` | superinstance, ai-agents | ✅ |
| 22 | `git-agent-codespace` | superinstance, ai-agents | ✅ |
| 23 | `capitaine-1` | superinstance, ai-agents | ✅ |
| 24 | `codespace-edge-rd` | superinstance, ai-agents | ✅ |
| 25 | `AI-Writings` | superinstance, ai-agents | ✅ |
| 26 | `SuperInstance` | superinstance, ai-agents | ✅ |

**Total:** 26/26 tagged successfully · 0 failures

## Verification

Spot-checked live topics via `gh api repos/SuperInstance/<repo>/topics`:
- `flux-runtime` → includes all 5 flux tags ✅
- `plato-core` → includes all 5 plato tags ✅
- `constraint-theory-core` → includes all 5 theory tags ✅
- `exocortex` → includes both org-wide tags ✅
- `SuperInstance` → includes both org-wide tags ✅

Pre-existing repo-specific tags (e.g., `rust`, `python`, `jit`, `ssa`) were preserved — only additive tagging was performed.

## Notes

- GitHub does not have a curated org-level topics page; discoverability happens through individual topic pages (e.g., `github.com/topics/superinstance`)
- The `superinstance` topic now serves as the org-wide discovery anchor
- Existing repo-specific tags were preserved — no destructive topic removal (except the placeholder tag if present)
- Rate limit consumed: ~51 API calls out of 5000 (negligible)

## Method

```bash
# Example command per repo
gh repo edit SuperInstance/flux-runtime \
  --add-topic superinstance,ai-agents,flux,bytecode-vm,deterministic-execution \
  --remove-topic placeholder
```
