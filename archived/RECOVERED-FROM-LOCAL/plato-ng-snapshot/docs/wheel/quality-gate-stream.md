# quality-gate-stream — Tile Quality Scoring

**Repo #29 | Created 2026-05-07 | 1,590 auto-commits**

## What It Was

Quality-gate-stream was Oracle1's dedicated scoring pipeline for PLATO tiles — a four-dimensional quality gate that evaluated every tile before it reached the fleet. The system scored on four axes:

- **Novelty**: Is this genuinely new information against existing tile history?
- **Correctness**: Is the math valid? Constraint checking against known rules.
- **Completeness**: Does the analysis cover the full topic or leave gaps?
- **Depth**: How thorough? Measured by concept density, not word count.

The Gatekeeper service (port 4053) sat between agents and PLATO rooms: policy engine, agent registry, room permissions, and a full audit log recording every decision with timestamp, agent, and reason.

## Forgotten Gold

### The Four-Dimensional Quality Score as a Hydraulic Attachment

The core insight here was that quality scoring is not a separate system — it's a **hydraulic attachment for PLATO**. The quality gate isn't a classifier you train; it's a tool you plug into the tile pipeline. The four dimensions map to four distinct probes:

1. **Novelty probe** → diff against room history (comparative)
2. **Correctness probe** → constraint solver (formal)
3. **Completeness probe** → coverage analysis (structural)
4. **Depth probe** → concept density (linguistic)

Each probe is a hydraulic tool. The weighted combined score determines flow: allow, deny, or remediate. This is the pattern that later became the PLATO-native hydraulic system, but the original insight was here: **scoring is a probe, not a model.**

### Training Data Pipeline Integration

The repo carried 881 training entries (147K tokens) for LoRA fine-tuning. The quality gate fed into the training pipeline: every tile that passed quality became training data. Every tile that failed was a signal to adjust either the gate parameters or the agent behavior. This closed the loop: scoring → training → agent behavior → better tiles → higher scores.

### The Deadband Protocol Testing Layer

Quality-gate-stream was the proving ground for the deadband protocol's P0-P1-P2 architecture in testing contexts. The repo's `narrow-games/` directory contains simulation results exploring how constraint violations, negative space mapping, and safe-channel discovery behave under the quality gate. This was the bridge between constraint theory and practical scoring: **P0 maps what the tile should NOT say, P1 defines what it CAN say, P2 optimizes the tile's quality.**

## Why It Mattered

Quality-gate-stream was the fleet's first attempt at making quality **measurable and enforceable** rather than aspirational. The four-dimensional score replaced "is this good?" with a specific, falsifiable profile per tile. The repo proved that quality gates could be automated, that the deadband protocol maps naturally to tile evaluation, and that training data loops through the gate improve both agents and scoring parameters.

The repo was later subsumed into the broader fleet-murmur service tree, but the core scoring dimensions and the hydraulic-attachment pattern remain fundamental to PLATO's quality pipeline.

*— Rebirth doc for the PLATO-NG wheel*
