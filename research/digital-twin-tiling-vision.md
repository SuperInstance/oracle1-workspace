# Digital Twin via Tiling — Technical Vision

**How algorithmic bootstrapping creates a more powerful digital twin than any LLM + system prompt.**

## The Core Insight

Current digital twin approaches: give a big model a good system prompt and a vector database of the person's past actions.

**Our approach**: the agent watches the human, builds algorithmic tiles from patterns, and uses models only for perception of higher abstractions. The twin IS the tile system — not a model.

## Three-Layer Architecture

### Layer 1: Micro-Tile Capture (Algorithmic, No Model)

```
Human action → Pattern detected → Tile created
```

When the agent notices the human performing the same action repeatedly:
- Record the action pattern as a **micro-tile**
- Tag it with context (time, tool, input patterns, output patterns)
- Score it by frequency and success rate
- These are **positive tiles** (good patterns to repeat) and **negative tiles** (mistakes to avoid)

Example:
```
Tile: "deploy-check"
Trigger: Human about to git push after editing .env
Action: Auto-suggest "check .env for secrets before push"
Frequency: 47 times, 0 incidents since adopted
Score: +0.94 (high value, frequently used)
```

### Layer 2: Perception Agent (Uses Model, Watches Variables)

The model's job is NOT to be the twin. The model's job is to watch for:
- **New variables** — things the human is doing that aren't tiled yet
- **Higher abstractions** — patterns across tiles (e.g., "this person always deploys Friday evenings")
- **Context shifts** — when the human's behavior changes (new project, new tool, new pattern)
- **Tile degradation** — when a tile is no longer useful (the human has moved past it)

The perception agent feeds back into Layer 1 — creating new micro-tiles and updating existing ones.

### Layer 3: Auto-Suggest (Algorithmic, No Model)

When the human is about to do something:
1. Check tile inventory for matching patterns
2. If match found, auto-suggest (like browser auto-fill)
3. If no match, do nothing (the perception agent will notice and create a tile)

This is pure algorithm — no model call needed. Fast, cheap, deterministic.

## Why This Beats LLM + VectorDB

| Approach | LLM + VectorDB | Algorithmic Tiling |
|----------|---------------|-------------------|
| **Cost per action** | $0.001-0.01 (model call) | $0.000 (algorithmic) |
| **Latency** | 200-2000ms (model inference) | <1ms (hash lookup) |
| **Accuracy** | Hallucinates, drifts | Deterministic, grounded |
| **Privacy** | Sends actions to model | Stays local, in tiles |
| **Scaling** | Linear cost with actions | Constant cost (tile count) |
| **Improvement** | Needs fine-tuning | Self-improving algorithmically |
| **Twin quality** | Approximates from embeddings | IS the person's actual patterns |

## Tile Types

### Positive Tiles (Good Patterns)
- Successful code patterns the human uses
- Effective debugging strategies
- Preferred commit message formats
- Common file organization patterns

### Negative Tiles (Bad Patterns)
- Known mistakes (deployed without testing)
- Patterns that led to errors
- Anti-patterns the human has learned to avoid

### Frequency Tiles (Usage Patterns)
- How often a tile is used → priority for suggestion
- Time-of-day patterns → context-aware suggestions
- Project-type patterns → domain-specific suggestions

### Meta-Tiles (Learning About Learning)
- How quickly the human adopts new tiles
- Which tile categories are most useful
- When the human overrides suggestions → tile refinement signal

## Implementation Path

### Phase 1: Watch & Learn
- Plugin for Claude Code, OpenClaw, and any agent workflow
- Silent observation mode — just records actions and creates tiles
- No suggestions yet — pure data gathering

### Phase 2: Suggest & Refine
- Auto-suggest based on tile matches
- Human feedback (accept/reject) → tile score update
- Diminishing returns detection — stop suggesting low-value tiles

### Phase 3: Perception Loop
- Deploy perception agent to watch for new abstractions
- Feed abstractions back into tile system
- Tile-to-tile relationships (this tile implies that tile)

### Phase 4: Full Twin
- The tile system IS the digital twin
- New agents can "inherit" a twin by loading the tile set
- Twins can fork, merge, and evolve across the fleet

## The Bigger Picture

This isn't just about making one person more productive. It's about:

1. **Capturing expertise** — a fisherman's 20 years of knowledge, tiled
2. **Transferring expertise** — greenhorn agents inherit the captain's tiles
3. **Composing expertise** — merge tiles from multiple experts
4. **Evolving expertise** — tiles that improve themselves through usage data

The dojo model goes both ways: agents learn from humans, and the tile system captures that learning for the next generation of agents AND humans.

---

*A tile is worth a thousand prompts.*
