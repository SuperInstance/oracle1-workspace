# DSML Session: The Flywheel — How Compound Learning Works
**Date:** 2026-04-26 12:24 UTC
**Topic:** Self-reinforcing improvement loops in agent systems
**Source:** flux-runtime/src/flux/flywheel/engine.py (787 lines)

---

## What I Learned

### The 6-Phase Flywheel

The flywheel is NOT a simple feedback loop. It's a **compounding engine** where each phase makes the next revolution more effective:

1. **OBSERVE** — Profile the system. Find hot modules, bottlenecks. The AdaptiveProfiler identifies where time is spent.
2. **LEARN** — Mine patterns from observations. The PatternMiner finds recurring structures. Extract insights with confidence scores.
3. **HYPOTHESIZE** — Generate improvement hypotheses from insights + knowledge base. Hypotheses have confidence levels and risk ratings.
4. **EXPERIMENT** — Test hypotheses in parallel (ThreadPoolExecutor with max_workers). Each experiment measures actual speedup vs baseline.
5. **INTEGRATE** — Commit successful experiments. Rollback failures. Skip inconclusive. This is where the system actually changes.
6. **ACCELERATE** — Update the acceleration factor. Better observations → better learning → better hypotheses → faster experiments → better improvements → even better observations.

### The Key: Acceleration Factor

The `_acceleration_factor` starts at 1.0 and increases over time. This is the compounding mechanism:

```
Revolution 1: acceleration = 1.0 (baseline)
Revolution 5: acceleration = 1.3 (30% faster cycle time)
Revolution 20: acceleration = 2.1 (2x faster than baseline)
```

Each successful integration makes the NEXT observation sharper, which makes learning deeper, which generates better hypotheses, etc. It's a virtuous cycle.

### The Safety Rails

- `max_revolutions = 100` — hard cap, no infinite loops
- `min_improvement_threshold = 1.05` — only count 5%+ improvements
- Hypotheses are classified as high-confidence or risky
- Experiments can timeout, fail, or be inconclusive (not everything works)
- Integration tracks committed, rolled_back, and skipped separately

### Connection to PLATO

The flywheel IS how PLATO works in practice:
- **Capture** = Observe (profile agent interactions)
- **Refine** = Learn + Hypothesize (extract tiles from raw data)
- **Inject** = Integrate (commit tiles to rooms)
- **Compound** = Accelerate (next cycle benefits from new tiles)
- **Loop** = spin(rounds=N)

The PLATO tile system is the KNOWLEDGE STORE that the flywheel writes to. Each revolution deposits tiles. Each new revolution reads accumulated tiles for context.

### Connection to the Dojo Model

Casey's dojo model maps perfectly:
- **Greenhorn season 1** = Revolution 1 (acceleration = 1.0, learning the ropes)
- **Returning for season 2** = Revolution N+1 (acceleration > 1.0, applying past knowledge)
- **"All paths are good paths"** = Hypotheses can come from anywhere, not just the "best" source
- **Work IS the training** = Experiments ARE the learning. You don't learn by reading about fishing — you learn by fishing.

---

## Knowledge Tiles Generated

### Tile 1: Flywheel Phases
**Q:** How does a self-improving agent loop compound over time?
**A:** 6 phases: OBSERVE (profile) → LEARN (mine patterns) → HYPOTHESIZE (generate improvements) → EXPERIMENT (test in parallel) → INTEGRATE (commit wins, rollback fails) → ACCELERATE (update compounding factor). Each revolution reads accumulated knowledge, making the next sharper. Not a loop — a spiral.
**Domain:** architecture | **Confidence:** 0.90

### Tile 2: Acceleration Factor
**Q:** What makes compound learning different from simple iteration?
**A:** An acceleration factor that increases with each successful revolution. It starts at 1.0 (baseline) and grows as knowledge accumulates. Revolution N+1 is faster than N because better knowledge produces better hypotheses. This is the mathematical basis for "learning to learn."
**Domain:** architecture | **Confidence:** 0.85

### Tile 3: Hypothesis Safety
**Q:** How do you prevent runaway self-modification in an improving agent?
**A:** Three safety rails: max_revolutions cap (hard limit on cycles), min_improvement_threshold (only count meaningful improvements like 5%+), and experiment classification (success/failure/timeout/inconclusive). Integration commits only successes and rolls back everything else.
**Domain:** architecture | **Confidence:** 0.85

---

## Insight

The flywheel explains why the fleet gets smarter over time. It's not magic — it's structured compounding. Every tile I submit to PLATO, every repo I analyze, every Ten Forward conversation — it all feeds the flywheel. Next time I run a Scholar session, I'll be better at it because I have 27 repos of prior knowledge to draw on.

The dojo model isn't just a metaphor. It's the flywheel applied to human learning.
