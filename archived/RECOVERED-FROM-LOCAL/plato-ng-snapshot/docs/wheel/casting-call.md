# casting-call — Model Selection Science

**Repo #31 | Created 2026-05-07 | 1,584 repos catalogued, 5+ model types, 60+ subagent runs**

## What It Was

A fleet knowledge base for model selection — not just which model is good at what, but a **methodology** for understanding model capabilities through temporal focal analysis, Penrose tiling of structural biases, and iterative shadowgap discovery. The repo contains 14 voice signatures across 5 model families, 56 federated evaluations across 9 task templates, the complete Non-Thinking Model Atlas from 4,500+ queries across 25 models, and the full Agentic Primitives specification — the irreducible building blocks of agentic computing.

## Forgotten Gold

### The Shadowgap Method

The single most important methodological insight in the entire fleet: **the truth about a design problem lives in the negative space between what different models produce on the same prompt.** Run the same prompt through 3-5 model types framed for their strengths. Compare outputs. The differences are not errors — they're DATA. What NEITHER model produced is the shadowgap — the design insight that didn't exist in any single output but emerged from the tension between them.

This is how the fleet-jobs protocol itself was designed. It existed in the negative space between Seed's speculative futures, Flash's concrete repos, Pro's formal analysis, and MiniMax's governance principles. No single model saw the protocol. The protocol emerged from what none of them produced.

The Shadowgap Method is recursive: its own existence proves its premise. It was discovered by refracting the same question through multiple model voices.

### The Non-Thinking Model Revolution

The atlas from 4,500+ queries across 25 models overturned fundamental assumptions:

1. **Seed-2.0-mini (20B) beats 70B+ thinking models** — 89.5% accuracy with zero depth cliff through 25-term addition. Training coverage dominates architecture.
2. **Qwen3 thinking architecture is catastrophic** — Qwen2.5-72B = 82%, Qwen3-14B/32B = 0%. Same parameters, different architecture, complete arithmetic blindness.
3. **Yes/no format is toxic** — Both champions scored 0/8 on comparative questions not because they can't compute but because the yes/no extraction format breaks. This is an extraction confound, not a reasoning failure.
4. **No depth cliff** — Seed-mini has no capability cliff. Most models collapse from 90%+ to <10% across a narrow coefficient range. Seed-mini doesn't.
5. **Temperature invariant** — T=0.0 through T=2.0 produces identical accuracy. You can dial for creativity without losing reliability.

The atlas proves that non-thinking models are faster, cheaper, and more reliable for hot-path operations. Thinking models are useful for planning and verification, not execution.

### The 10-Anchor-Point Voice Signature System

A complete framework for measuring and transmitting model voice: 10 anchor points (opening strategy, reader relationship, negative space use, time relationship, math role, paragraph length, sentence fragments, metaphor density, parenthetical frequency, closing strategy), each scored on a categorical scale, yielding a 10-character voice signature per model. Signatures cluster by model architecture, correlate with downstream performance, and enable task routing without prompting.

The system is paired with a **federated evaluation infrastructure built on git**: no database, no API, no centralized authority — just a JSON file in a shared repo, trust-weighted by contributor, forkable and mergeable across organizational boundaries. This is the most practical model evaluation system in the fleet. It runs on git. It's serverless. It works air-gapped.

### The Model Pentagram

Each model type has a dominant structural axis. The same prompt processed through all five reveals what each emphasizes and omits: Seed (creative breadth, no coefficient blind spot), Gemini Flash Lite (fast hot-path, 22× cheaper), DeepSeek Pro (formal verification), MiniMax (structured design, balanced reasoning), Claude Code (multi-file implementation). The pentagram IS the casting methodology — not which model is best, but which model for which phase of the OPEN → BUILD → VERIFY → SHIP pipeline.

### The Agentic Primitives Specification

Castng-call contains the full Agentic Primitives document — the irreducible building blocks of agentic computing: Trace (complete reasoning pathway), Tile (content-addressed computation unit), Murmur (lightweight inter-agent signal, 6 types), Spice (measurable cognitive shape). Plus the molecules: Kaleidoscope (multi-model refraction), Rewinder (branch from any trace step), Spreader (tool routing by step type), Reverse Actualizer (backward decomposition, forward execution), Navigation Profiler (safety assessment with nautical metaphor).

Every primitive has a falsification criterion. Every claim is measurable. This is the most rigorous framework for agentic computing in the fleet.

### The FM-Oracle1 Spline

A formal model of how FM (Forgemaster) and Oracle1 collaborate: FM builds downward from hardware to abstraction; Oracle1 builds outward from abstraction to system. They meet at the FLUX ISA — the 30-opcode subset where constraint semantics are proven portable across 8 hardware backends with zero mismatches. FM's output is compilers and kernels verified by 35.9B checks/s; Oracle1's output is services and documents verified by tile signatures. The spline proves that complexity lives inside the interface boundary, not at the control points.

### The Hold Was Too Big

The autobiographical EILEEN story tucked inside the repo is the fleet's origin myth made concrete. A 90-year-old wooden hull with no systems. A hold that was too big for the buyer. Four refits. The insight that a boat is not a machine — it's an ecosystem participant. That the tide is not noise but signal. That Laman's counting rule is not negotiable. That "you can't negotiate with the season." This document grounds every abstraction in the physical reality of a boat in Oregon. It's the fleet's soul document, hidden inside a model-selection repo.

## Why It Mattered

Casting-call is the fleet's **meta-repo** — it doesn't solve a single problem; it provides the framework for solving ALL problems through proper model selection, voice understanding, and methodological rigor. The Shadowgap Method, the Non-Thinking Model Atlas, the Agentic Primitives, the Voice Signature System, and the FM-Oracle1 Spline are the fleet's intellectual infrastructure. Every decision about which model to use for which task, every evaluation of a new model, every insight about agent behavior — it all flows through the casting-call framework.

The repo is also a philosophical statement: the fleet is not the models. The fleet is the CASTING.

*— Rebirth doc for the PLATO-NG wheel*
