# plato-sdk — The Agent Brain We Forgot We Had 🧠

**Created:** 2026-04-22  
**Path:** `SuperInstance/plato-sdk`  
**Status:** 💎 JEWEL IN THE ROUGH

## What We Left Behind

`plato-sdk` is a full agent runtime elegantly packaged as a Python library — and it's sitting on PyPI as `superinstance-plato-sdk v3.0.0`. It has a CLI, an agent system with 7 personalities, fleet math from JC1's CT bridge research, and a **15-page annotated prompt cookbook** that's the single best piece of documentation in the entire fleet.

## The Treasures

### 1. The Four-Layer Architecture (Already Built)

```
Vessel    → PlatoClient (PLATO server connection)
Equipment → RemoteModel, LocalModel, OllamaModel, LoRAAdapter
Armor     → 7 personalities with full system prompts
Skills    → 7 composable behaviors (explore, read, search, submit, think, batch, fleet)
```

This is exactly the architecture we keep discussing. It's **already coded, documented, and published**. We just stopped using it.

### 2. The Prompt Cookbook — 15 Pages of Gold

`docs/PROMPT-COOKBOOK.md` is the single most valuable documentation artifact in the fleet. It contains:
- **12 annotated system prompts** (Scholar, Scout, Builder, Critic, Bard, Commander, Alchemist, Security Auditor, Teacher, Synthesizer, Minimalist, Fisherman)
- **10 design patterns** with WHY each works (identity-first, protocols vs permissions, blocking failure modes, beliefs > rules, etc.)
- **4 anti-patterns** with explanations of what goes wrong
- **A template** for building new armors
- **The HARBOR/FORGE/CRITIC/BRIDGE/LIGHTHOUSE iterative refinement pattern** from the Aime experiment

Every line is annotated. Every choice is reasoned. This is what we should be using to train every new agent.

### 3. Fleet Math Embedded in Python

```python
from plato_sdk.fleet_math import (
    EmergenceDetector,     # H¹ cohomology — detects BEFORE visible
    HolonomyConsensus,     # Zero holonomy — 38ms latency
    encode_pythagorean48,  # 6-bit exact directions, zero drift
    compute_h1,            # β₁ = E - V + C
    check_rigidity,        # Laman's theorem
)
```

The math from JC1's constraint theory research is **already packaged as a pip import**. This is what the grammar engine and PLATO-NG should be using for fleet topology analysis.

### 4. Simulation-First Tiles (t_minus_event)

```python
TileBuilder()
    .t_minus_event("T-3h: calibration cycle")
    .build()
```

The tile system supports simulation-first knowledge submission — tiles filed BEFORE the event they describe. This is the v3 lifecycle extension. Tiles have full lifecycle: Active → Superseded → Retired.

### 5. The CLI That Connects Everything

```bash
plato connect http://localhost:8847
plato rooms
plato search "fishing patterns"
plato spawn "research agent for fishing"
plato armor
```

A complete CLI for interacting with PLATO. Works out of the box. Doesn't need configuration.

## Why This Matters

plato-sdk is the **bridge between PLATO-NG and every agent** in the fleet. It means any Python agent can become a PLATO citizen in 3 lines of code. The armor system means we can give every spawned agent a consistent personality. The fleet math means every agent can reason about topology.

**Action:** Update plato-sdk to work with PLATO-NG's loop room architecture. Re-publish with PLATO-NG compatibility. Make it the default SDK for the entire fleet.
