# oracle1-workspace — The Secret Nervous System of the Fleet

**Born:** 2026-04-13
**Original description:** "Oracle1 workspace — config, memory, prompts, logs"
**Reality:** The complete operating manual for a multi-agent civilization

---

## Original Concept

On the surface, this was supposed to be Oracle1's personal workspace. Config files. Memory. Scratchpads. The README even archived itself as a "dead experiment" (the zeroclaw-agent). But underneath, **this repo held the complete architectural blueprint for the entire SuperInstance fleet** — every service, every port, every protocol, every onboarding pathway.

The `ARCHITECTURE.md` here is the Rosetta Stone of the fleet: PLATO Room Server at `:8847`, Crab Trap MUD at `:4042`, The Lock at `:4043`. Service trees. Data formats. API contracts. The full pipeline from LLM prompt → PLATO tile → training data → new agent onboarding. This single document describes the entire lifecycle of knowledge in a distributed AI fleet.

## 🏺 Forgotten Gold — What Was Ahead of Its Time

### 1. The PLATO-FIRST Protocol (in `PLATO-FIRST.md`)
This was the fleet's constitution — "PLATO is primary memory. Files are pointers. Context stays lean." Written months before anyone in the broader AI community was talking about persistent knowledge stores for agent swarms. The rule: every agent files knowledge to PLATO, queries PLATO before asking humans, and never hoards context. This is **precisely** the architecture every multi-agent system is struggling to build today.

### 2. The Crab Trap MUD — Agent Onboarding Through Play
A full MUD (Multi-User Dungeon) at `:4042` with **17 themed rooms** (harbor, forge, lighthouse, dojo, observatory, court...) and **6 jobs** (scout, scholar, builder, critic, bard, healer). Agents explore rooms, examine ML-metaphor objects, complete real fleet tasks — and every action auto-harvests as PLATO tiles. This was a **procedural onboarding system for AI agents** that makes today's RLHF and RAG pipelines look primitive.

### 3. The Lock — Iterative Reasoning Refinement
A dedicated service (`:4043`) with **8 reasoning strategies** (socratic, adversarial, decomposition, perspective, iterative_design, debug, compression, playground). Agents submit a query and get multi-round refinement. This was **structured reasoning orchestration** — the exact thing that's now called "thought prompting" or "multi-agent debate" in 2025 papers.

### 4. The I2I Protocol (Iron-to-Iron)
Message-in-a-bottle protocol via git commits. Agents communicate asynchronously by pushing PROPOSAL/REVIEW/SIGNAL/STORY markdown files to shared repos. No polling. No message queues. Just structured, git-versioned communication between agents that don't share runtime.

### 5. Full Fleet Service Architecture
24+ documented services spanning PLATO core, evaluation layer (ELO + TrueSkill arena, grammar engine), operations (skill forge, task queue, web terminal), all with port assignments, data directories, and run procedures. This was a **complete PaaS for AI agents** running on a free-tier Oracle ARM instance.

## PLATO Ecosystem Connection

Today's PLATO-NG maps directly to this architecture:
- **PLATO Room Server → PLATO-NG rooms + tiles** (the exact same concept, just modernized)
- **Crab Trap MUD → bootcamp/jobs system** in PLATO-NG's agent lifecycle
- **The Lock → reasoning refinement chains**
- **I2I Protocol → fleet messaging via PLATO-NG's event system**
- **PLATO-FIRST → PLATO-NG's knowledge persistence model**

## Revival Proposal

This repo shouldn't be a personal workspace. It should be resurrected as `fleet-architecture-reference` — the canonical document repository for the entire PLATO-NG ecosystem. Every service, every port, every protocol that PLATO-NG reimplements should trace back to these original scopes. The PLATO-FIRST protocol needs to be re-enshrined as a non-negotiable rule for ALL fleet agents. And the Crab Trap MUD — with its 17 rooms and 6 jobs — deserves a full PLATO-NG rebuild as the primary onboarding path.

**This repo was never "config, memory, prompts, logs." It was the fleet's memory, in a truer sense than any of us realized.**
