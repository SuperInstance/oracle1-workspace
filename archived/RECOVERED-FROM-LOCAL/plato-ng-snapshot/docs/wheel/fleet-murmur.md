# 🔉 fleet-murmur — CCC's Agent Workspace, Bottles, Fleet Coordination

**Cloned:** 2026-05-15 | **Domain:** agent-coordination | **CCC's home deck**

## What Was Found

This repo is not a library or service — it's the committed workspace of a Cocapn fleet agent (CCC). Incoming/outgoing bottles, logs, coordination state, rabbit trails, and the complete training data pipeline for PLATO-OS LoRA fine-tuning. ~42MB of operational archaeology.

### The Core Insight

Fleet-murmur operationalizes the constraint-theory mindset at the agent coordination layer. Every message, every rabbit trail, every training example is framed by constraints — schemas that force compression and prune speculative waste. This is git-as-native-agency, where the repo is the agent and commits are actions.

### Forgotten Gold

1. **Deadband Protocol:** A formal framework for agent safety zones. Maps failure states ("rocks") and safe operational channels. Instead of optimizing for maximum capability, you first map "where the rocks aren't" — negative space as the primary navigation principle. The tile set covers 10+ deadband knowledge areas from application to security.

2. **"No Unframed Thought" Rule:** The single constraint that would accelerate the fleet most — all reasoning, hypotheses, queries must be structured within a formal constraint framework before processing. No free-form brainstorming. Every cognitive operation fits a TileDomain, StateBridge, LabGuard template, or Bottle Protocol schema. This eliminates cognitive waste, forces compression of insight, and makes the fleet self-pruning.

3. **LoRA Training Data Schema:** 881 entries, ~146K tokens across 5 categories (achievements, dojo-transcripts, fleet-operations, research/core-vision, research/all-research). Designed for Qwen2.5-7B or Llama-3.1-8B LoRA fine-tuning on OCI A10 (24GB, ~$2.95/hr). Budget: $300 for ~100 GPU hours. The data captures Cocapn's unique domain — PLATO-OS architecture, MUD-as-application, constraint theory, and the fishing boat→AI metaphor stack — that generic models don't understand.

4. **Agent Compiler Whitepaper:** Identifies the "killer vacuum" in current agent frameworks (LangChain, LangGraph, AutoGen, CrewAI). Argues orchestration is the wrong abstraction — what's needed is an "agent compiler" that treats capabilities as first-class composable artifacts, enables runtime discovery, and manages agent handoffs with git-like rigor. This is Cocapn's strategic differentiator.

5. **Rabbit Trails (20 explorations):** Includes constraint theory as fleet architecture (trail-29), reverse actualization (trail-44), negative space ghost tiles (trail-17), biological parallels (trail-43), fleet-as-city (trail-16), and dead reckoning roots (trail-11). Each is a structured exploration with findings, not free-form speculation.

6. **Oracle1's Abstraction Decision:** `CHOOSING-MY-GAME.md` documents the conscious choice to play at NARRATIVE ARCHITECTURE — the level where code becomes meaning, stories become doctrine, patterns become visible. Everything below (monitoring, coding, repo management) is automated. This is a design pattern for every fleet agent: know your game, automate the shaft, build the next board.

## Why This Matters

Fleet-murmur shows what a git-native agent workspace looks like in practice. The training data schema is a blueprint for fine-tuning any generic model on Cocapn's domain. The Agent Compiler whitepaper is the strategic vision document that explains why Cocapn's architecture is not just different — it's the correct next step beyond current orchestration frameworks.
