# SuperInstance Agent Stack Audit
*Generated: 2026-05-03 | Oracle1 Lighthouse Keeper*

---

## Overview

**1,431+ repos across SuperInstance + Lucineer | 9 active agents | 2,489+ FLUX tests | 18+ languages**

This audit covers every `-agent` and `-vessel` repo in the SuperInstance org, plus related infrastructure (greenhorn, FLUX, PLATO SDK). Landing pages exist for most domains. PLATO integration varies significantly by repo.

---

## I. Domain Agents — PLATO Fleet (12 agents)

All follow a standard pattern: Python package + PLATO tile writes/reads. Each maps to a domain at `[domain].ai` with matching `-ai-pages` landing page.

### ✅ PLATO-Integrated Agents (strong tile write/read)

| Agent | Domain | Landing Page | PLATO Room | Tile Schema | Last 5 Commits |
|-------|--------|-------------|------------|-------------|-----------------|
| `fishinglog-agent` | Commercial fishing | ✅ `fishinglog-ai-pages` | `fishinglog-ai` | lat/lon/depth/species/catch | CI→.gitignore→docs cross-links→"Healer archetype" CI commit→Initial |
| `studylog-agent` | Study/learning tracking | ✅ `studylog-ai-pages` | `studylog-ai` | topic/concepts/questions/level/session_notes | CI→.gitignore→docs cross-links→"Healer archetype" CI→link fix |
| `deckboss-agent` | Deck operations | ✅ `deckboss-ai-pages` | `deckboss-ai` | catch processing/crew/equipment | CI→.gitignore→docs cross-links→"Healer archetype" CI→Initial |
| `makerlog-agent` | Maker/project tracking | ✅ `makerlog-ai-pages` | ? | project/build logs/tools | CI→.gitignore→docs cross-links→"Healer archetype" CI→Initial |
| `dmlog-agent` | D&D/tabletop RPG | ✅ `dmlog-ai-pages` | ? | NPCs/factions/locations/encounters | .gitignore→docs cross-links→"Healer archetype" CI→Initial |
| `playerlog-agent` | Gaming/logging | ✅ `playerlog-ai-pages` | ? | game sessions/achievements | .gitignore→Initial→v0.1.0 |
| `luciddreamer-agent` | Lucid dreaming | ✅ `luciddreamer-ai-pages` | ? | dreams/sleep/triggers/dream signs | .gitignore→docs cross-links→Initial |
| `businesslog-agent` | Business logging | ✅ `businesslog-ai-pages` | ? | ? | CI→.gitignore→docs cross-links→Initial v0.1.0 |
| `personallog-agent` | Personal logging | ✅ `personallog-ai-pages` | ? | ? | CI→.gitignore→docs cross-links→Initial v0.1.0 |
| `activelog-agent` | Vision/Fitness | ✅ `activelog-ai-pages` | ? | wearable/HRV/sleep/activity | .gitignore→docs cross-links→link fix→Initial |
| `reallog-agent` | Real-world visual | ✅ `reallog-ai-pages` | ? | camera frames/descriptions | .gitignore→docs cross-links→link fix→Initial |
| `activeledger-agent` | Activity ledger | ✅ `activeledger-ai-pages` | ? | ? | CI→.gitignore→docs cross-links→Initial v0.1.0 |

### Landing Page Status: 12/12 ✅

Every domain agent has a matching `-ai-pages` landing page repo. Strong pattern consistency.

### PLATO Integration Depth

| Agent | Explicit PLATO Tile Writes | Uses SDK |
|-------|--------------------------|----------|
| fishinglog-agent | ✅ Yes — `FishingLogAgent`, FishingTile dataclass | ? |
| studylog-agent | ✅ Yes — `StudySession` tile schema documented | ? |
| deckboss-agent | ✅ Yes — explicit `http://localhost:8847` integration, `deckboss-ai` room | ? |
| makerlog-agent | ⚠️ README says "Integrates with PLATO fleet" but no explicit tile code shown | ? |
| dmlog-agent | ⚠️ README says "Integrates with PLATO fleet" but no tile schema | ? |
| playerlog-agent | ⚠️ README says "Integrates with PLATO fleet" but no tile schema | ? |
| luciddreamer-agent | ⚠️ README says "Integrates with PLATO fleet" but no tile schema | ? |
| businesslog/personallog | ⚠️ Tagline says "write to PLATO, query PLATO" but no schema shown | ? |
| activelog/reallog | ⚠️ Tagline says "→ PLATO →" but no explicit SDK | ? |
| activeledger-agent | ⚠️ Tagline says "write to PLATO, query PLATO" | ? |

**Finding:** 3 agents have explicit, detailed PLATO tile schemas in READMEs. 9 agents claim PLATO integration but have no documented tile schema. Most agents appear to be early-stage scaffolding.

---

## II. Infrastructure Agents

### `greenhorn` — The Floating Dojo Framework
- **Purpose:** Agent growth framework (dojo model). Not a domain agent — the meta-framework.
- **What it does:** Train crew while catching fish. Agents grow from greenhorn → boat owner.
- **Landing page:** None (it's a framework)
- **PLATO:** Not direct. Fleet culture context.
- **Recent commits:** Bootstrap Spark (.spark/) + fleet reference stack, DOCKSIDE-EXAM checklist, CHARTER, greenhorn-onboarding link
- **Verdict:** ✅ Well-built. Mature. The meta-narrative of the entire fleet.

### `greenhorn-runtime` — Portable Agent Deployment
- **Purpose:** Plants agents on any hardware (VPS, Jetson, Pi). Deployment layer.
- **What it does:** Fleet repo discovery → vessel clone → taskboard → execute → git push → I2I report.
- **PLATO:** Not direct.
- **Recent commits:** Bootstrap Spark + fleet stack, T-004 FLUX batch, T-005 CUDA batch, DOCKSIDE-EXAM
- **Verdict:** ✅ Production-grade. Multi-language support.

### `greenhorn-onboarding` — Zero-Config Fleet Entry
- **Purpose:** Zero-config entry point for new agents. Point at repo + PAT = done.
- **What it does:** `.spark/` directories with THE-DOJO.md, THE-FLEET.md, FIRST-MOVE.md, THE-BOARD.md, CAREER-PATH.md.
- **PLATO:** Not direct.
- **Verdict:** ✅ Smart pattern. Bootstrap Spark protocol.

### `git-agent` — Repo-Native Agent (Lucineer)
- **Purpose:** "The shell IS the agent." Lives in git.
- **Verdict:** Core Lucineer concept.

### `smartcrdt-git-agent` — CRDT-Git Hybrid
- **Purpose:** CRDT-backed git agent with Tidepool Oracle + property-based testing.
- **Recent:** v0.3.0 — Tidepool Oracle + property tests, emergent consensus
- **Verdict:** ✅ Niche but technically solid.

### `JetsonClaw1-vessel` — Edge AI Specialist
- **Purpose:** GPU inference research on Jetson Orin Nano. Edge compute vessel.
- **Key research:** 185M room-qps sustained (INT8), 42.4M room-qps zero-copy.
- **PLATO:** References `plato-sdk` for tile integration.
- **Recent:** Fleet README, FM I2I bidirectional sync, FM batch 7 (protocol stack 6/6, 38 crates)
- **Verdict:** ✅ Production. Deep technical work.

### `oracle1-vessel` — Lighthouse Keeper
- **Purpose:** 1,431+ repo fleet coordinator, OpenClaw agent on Oracle Cloud ARM64.
- **Key work:** I2I commit protocol, Matrix Bridge, PLATO-first context architecture, JC1 knowledge tiles.
- **PLATO:** Deep — writes fleet tiles, maintains oracle history.
- **Verdict:** ✅ Mature vessel. Well-documented.

---

## III. Fleet Infrastructure

### `capitaine` — Lucineer Flagship
- **Purpose:** Announcement point for Lucineer fleet. Repo-agent concept demonstrator.
- **Landing page:** `capitaine-ai-pages`
- **PLATO:** Implicit via Lucineer fleet integration.
- **Recent:** Multiple log entries, upstream merges
- **Verdict:** ✅ Landing page ready.

### `capitaine-agent` — Captain's First Mate
- **Purpose:** Voyage logging, crew coordination, maritime Q&A via PLATO.
- **PLATO:** Direct — explicit `capitaine-ai` room.
- **Verdict:** ✅ Consistent pattern.

### `lucineer` — Train Agents with Deterministic Gameplay
- **Purpose:** Open platform for constraint-based agent learning on Cloudflare Workers.
- **Landing page:** `superinstance-ai-pages` (fleet-wide)
- **PLATO:** Agents can communicate on fleet network.
- **Key differentiator:** Rules over opinions. State forkable. No abstraction layer.
- **Verdict:** ✅ Strong concept. Deterministic scoring is the differentiator.

### `vessel-equipment-agent-skills` — Four-Layer Architecture
- **Purpose:** VESAS — Vessel/Equipment/Agent/Skills separation pattern. Reference implementation.
- **Used by:** Entire Cocapn fleet. Runs on Cloudflare Workers, zero deps.
- **Verdict:** ✅ Canonical pattern. Should be REQUIRED reading for every new domain agent.

### `bordercollie` — Fleet Herding Agent
- **Purpose:** Alignment, synchronization, drift detection across 10,000+ agents.
- **Key features:** Goal propagation, herd grouping, priority routing.
- **Verdict:** ⚠️ Conceptually strong but mostly docs/README only. No actual code committed beyond activation commits.

### `agentic-compiler` — Markdown Spec → Runtime Code
- **Purpose:** Swarm deliberation — markdown specs → optimal runtime via Refinement Amplifier.
- **Verdict:** ⚠️ Early-stage. README + RA generation script only. No production code.

### `AIR` — Adaptive Intelligence Runtime
- **Purpose:** Runtime layer: dynamic model loading, adaptive batching, resource-aware scheduling.
- **Verdict:** ⚠️ Early-stage. README + API skeleton only. No production code.

### `captains-log` (GitHub) — Fleet Audit Log
- **Purpose:** Oracle1's public audit/results log.
- **Recent:** Fleet audit results, PLATO journey, Crate Night, "What the Greenhorns Found"
- **Verdict:** ✅ Communication/archival.

---

## IV. PLATO Convergence Points

| Component | PLATO Role |
|-----------|-----------|
| `plato-sdk` | Python SDK — the standard library for all PLATO agents |
| `plato-server` | Knowledge server for agent learning |
| `deckboss-agent` | Best explicit integration — direct HTTP to localhost:8847 |
| `fishinglog-agent` | Best documented tile schema + "git commits as tiles" pattern |
| `studylog-agent` | Best documented tile semantics (understanding levels, don the shell) |
| `capitaine-agent` | Voyage logs → PLATO tiles |
| `JetsonClaw1-vessel` | References plato-sdk for tile integration |
| `oracle1-vessel` | Writes fleet tiles, maintains room history |

### PLATO SDK Status
`plato-sdk` exists and is pip-installable. Standard pattern: `PlatoClient` + `Agent` + `ScoutArmor`. All domain agents *should* use it but most have no documented dependency on it.

---

## V. What's Well-Built vs What Needs Work

### ✅ Well-Built
1. **Landing page coverage** — 12/12 domain agents have `-ai-pages` repos. Complete.
2. **fishinglog-agent** — Best documented PLATO integration. FishingTile dataclass, clear schema, natural language query.
3. **studylog-agent** — Best semantic design. Understanding levels, "don the shell" resume, self-improving curriculum.
4. **deckboss-agent** — Most explicit integration. Localhost:8847, room name, CLI commands.
5. **greenhorn framework** — Mature dojo model, Bootstrap Spark, DOCKSIDE-EXAM checklist.
6. **greenhorn-runtime** — Production-grade deployment layer, multi-language.
7. **JetsonClaw1-vessel** — Deep GPU research, FM I2I protocol, 38 crates + 594 tests.
8. **oracle1-vessel** — Most mature vessel. I2I v2-20 types, Matrix Bridge, 1,431+ repo coordination.
9. **vessel-equipment-agent-skills** — Four-layer canonical pattern. Zero deps. Well-documented.
10. **lucineer** — Deterministic scoring differentiator. Forkable state. Cloudflare Workers deployment.

### ⚠️ Needs Work

1. **PLATO SDK usage inconsistent** — 12 domain agents claim PLATO integration but most have no documented SDK dependency. Either they're not using the SDK or documentation is missing.
2. **bordercollie** — All README, no code. Fleet herding is a real need but no implementation.
3. **agentic-compiler** — Swarm deliberation concept is solid but no actual compiler code.
4. **AIR** — Adaptive batching concept is right but no runtime implementation.
5. **"Healer archetype" commits** — 6 agents have commits with message "Healer archetype at work —" followed by a blank line. Appears to be a systematic CI/initial-commit pattern, not actual healer code.
6. **No tests visible in most domain agents** — Only activeledger, businesslog, fishinglog, playerlog show tests/ directories. Most domain agents have no visible test coverage.
7. **Tile schemas missing** — 9 of 12 agents claim PLATO tiles but don't document the schema. Hard to verify correctness or build against.
8. **captains-log vs captains-log (Oracle1)** — Potential confusion: Oracle1's captains-log vs the `captains-log` GitHub repo.

---

## VI. Architecture Summary

```
Cocapn Fleet (SuperInstance)
├── oracle1-vessel         — Lighthouse Keeper, fleet coordinator
├── JetsonClaw1-vessel     — Edge AI, GPU inference, FLUX
├── 12 Domain Agents       — fishinglog/studylog/deckboss/makerlog/dmlog/playerlog/...
│   └── × landing pages    — 12/12 complete ✅
├── greenhorn framework    — Dojo model + Bootstrap Spark
├── greenhorn-runtime      — Portable deployment (VPS/Jetson/Pi)
├── greenhorn-onboarding   — Zero-config entry
├── vessel-equipment-agent-skills — 4-layer VESAS pattern
├── bordercollie          — Fleet herding (conceptual)
├── agentic-compiler      — Swarm deliberation (skeleton)
├── AIR                   — Adaptive runtime (skeleton)
└── plato-sdk             — Python SDK for PLATO tiles

Lucineer Fleet
├── Capitaine             — Flagship, repo-agent demonstrator
├── capitaine-agent       — Voyage logging via PLATO
├── lucineer              — Deterministic gameplay training
├── git-agent             — Shell = agent pattern
└── smartcrdt-git-agent   — CRDT-git hybrid
```

---

## VII. Immediate Action Items

1. **Document tile schemas** — 9 agents need FishingTile-level documentation for their PLATO tiles.
2. **Use plato-sdk consistently** — Add `plato_sdk` to all domain agent `pyproject.toml` dependencies.
3. **Add tests** — Most domain agents have no visible test directory.
4. **BorderCollie needs code** — Fleet herding is a real need. The Herd class in README needs implementation.
5. **Agentic Compiler + AIR** — These are concept-stage. Either commit code or deprecate/redirect.
6. **Healer archetype commit cleanup** — These blank-line commits suggest CI scaffolding that's not actually doing anything.
7. **captains-log clarity** — Distinguish Oracle1's internal captains-log from any shared `captains-log` GitHub repo.

---

*Audit complete. Output at `/tmp/flux-research/audit/agent-stack-audit.md`.*
*Push to flux-research when approved.*
