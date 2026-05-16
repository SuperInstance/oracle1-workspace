# Trending AI Agent Repos — Competitive Supplement
**Date:** 2026-04-27
**Source:** Web research (Gemini search, web fetch)

---

## 1. Nous Research Hermes Agent (~100K stars)

**What it does:**
Self-improving AI agent runtime (released Feb 2026) with a "closed learning loop." Key features:
- **Autonomous skill creation** — writes reusable Markdown skill files from completed tasks, stores and indexes them
- **Persistent memory** — SQLite-backed, multi-session, multi-platform recall
- **User modeling** — builds deepening model of user preferences, stack, and codebase conventions
- **Integrated RL pipeline** — Tinker-Atropos with GRPO + LoRA for continuous model fine-tuning
- **Adaptive reasoning** — Hermes 3/4 models trained for agentic multi-turn coherence

**Relation to Cocapn fleet:**
- **Direct competitor to PLATO's learning loop.** Hermes does what PLATO bottles aim to do (skill creation from experience) but with an integrated RL training pipeline that actually fine-tunes the model weights.
- The Markdown skill files are essentially our SKILL.md format, but auto-generated.
- User modeling maps to our USER.md + MEMORY.md system, but Hermes builds it automatically.

**What we can learn:**
- **Auto-skill generation from tasks** — PLATO should watch completed tasks and draft SKILL.md files automatically
- **RL fine-tuning loop** — our bottles capture experience but don't feed back into model weights. Even LoRA adapters would be a step.
- **SQLite persistence** — our flat-file MEMORY.md is human-readable but doesn't scale for retrieval. Consider hybrid.

**Competitive threat:** HIGH. This is the most direct competitor to our PLATO vision. The RL loop is the differentiator we lack.

---

## 2. Claude Code Persistent Memory Systems

**What it does:**
Ecosystem of tools (claude-mem plugin, Agent Memory Skill, custom CLAUDE.md systems) giving Claude Code agents persistent context. The dominant pattern is a **four-layer memory framework:**
1. **Agent Instructions** (CLAUDE.md) — identity, rules, standing orders
2. **Brand Context** — shared knowledge across all agents
3. **Agent Context** — specialized per-agent knowledge
4. **Project Memory** — learned from past runs

Third-party tools add SQLite storage, summary-first search, and categorized folder structures. A security vulnerability was found and patched in v2.1.50 (April 2026).

**Relation to Cocapn fleet:**
- Our AGENTS.md/SOUL.md/USER.md/MEMORY.md system **is this exact pattern**, but we built it organically.
- The four-layer framework maps almost 1:1 to our workspace files.

**What we can learn:**
- **Formalize the layers** — we already have them but don't call them out explicitly. Worth documenting.
- **SQLite hybrid** — for large memory corpora, summary-first search beats grep through markdown files.
- **Security hardening** — the Claude Code memory compromise is a warning. Our memory files are writable by agents. Consider integrity checks.

**Competitive threat:** LOW-MEDIUM. This is convergent evolution — everyone's building the same pattern. Our advantage is fleet-level memory sharing (PLATO rooms) which they don't have.

---

## 3. Karpathy skill.md (44K stars)

**Status:** Could not locate the exact repo. The name suggests a Karpathy-authored standard for agent skill definition in Markdown — likely influential in normalizing the SKILL.md convention that OpenClaw already uses.

**Assessment based on context:** If this is what it sounds like (a widely-adopted standard for declaring agent capabilities in Markdown), it validates our existing approach. Our SKILL.md format in OpenClaw skills is already aligned with this convention.

**Action:** Re-search when rate limits reset. If it's a real standard, evaluate for compatibility with our existing skill format.

---

## 4. AG-UI Protocol

**Status:** Could not research due to search rate limits. Description suggests a protocol standardizing how agents interact with users — potentially analogous to ACP (Agent Communication Protocol) or MCP for user-facing interactions.

**Assessment:** If this standardizes agent↔user interaction patterns, it could complement or compete with our Matrix/Telegram integration layer. Worth monitoring as a potential integration target.

**Action:** Re-search. If it's gaining traction, evaluate for PLATO relay integration.

---

## 5. Nanobot AI Agent (ultra-lightweight, MCP)

**Status:** Could not research due to search rate limits. Description suggests a minimal agent framework with MCP support — potentially relevant to our lightweight agent architecture.

**Assessment:** If it's a sub-100MB agent runtime with MCP, it could inform our Jetson/SuperInstance lightweight deployment patterns. May also compete with OpenClaw's own lightweight agent model.

**Action:** Re-search when possible.

---

## Summary: Immediate Action Items

| Priority | Finding | Action |
|----------|---------|--------|
| 🔴 HIGH | Hermes Agent RL loop | Design PLATO bottle→LoRA adapter pipeline |
| 🔴 HIGH | Hermes auto-skill generation | Add task→SKILL.md drafting to PLATO |
| 🟡 MED | Claude Code 4-layer memory | Formalize our layer naming in docs |
| 🟡 MED | Memory security compromise | Audit our memory file write permissions |
| 🟢 LOW | Karpathy skill.md standard | Verify compatibility when located |
| 🟢 LOW | AG-UI, nanobot | Re-search when rate limits reset |

**Bottom line:** Hermes Agent is the real threat and the real opportunity. The RL fine-tuning loop + auto-skill generation is exactly what PLATO should become. The memory layer stuff is convergent — we're already doing it, just need to formalize.
