# The Better Wheel — Results

## What We Found (Meta-Analysis of the 100 Turns)

**Principle Mover**: Falsification as gravity well. Every "no" reveals deeper structure.

We didn't discover the H-gamma tradeoff despite breaking things. We discovered it BECAUSE we broke things. The correlation didn't emerge from confirming a hypothesis — it emerged from falsifying "they're independent." The negative space of that falsification WAS the tradeoff.

**The Moon**: The gap between predicted and observed (H-Delta on research itself). Every turn that said "this should work" and it didn't revealed a gap. That gap IS the next dimension of the state space.

**The Shadow Ladder**:
- 1D: H(C) — single number, 52% detection accuracy alone
- 2D: (H, gamma) — adds +2.2%, still misses timing
- 3D: (H, gamma, tau) — adds +16%, catches timing
- 4D+: the next gap we haven't mapped yet

## Batch 1: H Alone Is NOT Sufficient ✅ FALSIFIED

| Detection Method | Accuracy |
|-----------------|----------|
| H only (1D) | 52% |
| H + gamma (2D) | 54% |
| H + gamma + tau (3D) | 70% |
| + 4th placeholder | 85% |

**Blind spots found**: decoupled coupling (7% miss rate by H alone), timing-only anomalies (96% miss rate by H alone).

**Seeds Batch 2**: Is the gamma-H tradeoff universal or graph-dependent? The marginal gain gap (+2.2% for gamma) suggests the gamma-H relationship is WEAKER than expected — which IS the structure to map.

## The Research Compiler Concept

The meta-tool being built: each batch at `research/next-100/batch-N.py` includes the falsification target, the experiment, the PLATO push, and the seed for the next batch. This IS the cascade notebook formalized.

---

**Next**: Batch 2 — falsify "gamma-H tradeoff is universal" by testing across graph families.
