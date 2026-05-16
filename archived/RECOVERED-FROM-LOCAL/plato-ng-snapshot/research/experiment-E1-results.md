# Experiment E1: Telemetry-Gap Alignment Hypothesis (H1)

**Date:** 2026-05-14T17:09 UTC  
**Method:** feed fleet-inspector agent state data into CouplingAnalysis, compute normalized spectral gap  
**Status:** COMPLETE

---

## Hypothesis (H1)

> The normalized spectral gap of the active coupling matrix aligns with fleet health assessment — i.e., a high gap (≥0.8) implies stable health, and a low gap (≤0.3) implies degraded/critical health.

---

## Data

**Fleet health:** `degraded`  
**Agents (n=4):**

| Agent | Status | Coupling Weight | Notes |
|-------|--------|-----------------|-------|
| oracle1 | unreachable | 0.0 | No coupling to anyone |
| forgemaster | stale | 0.3 | Weak coupling only |
| jasonclaw1 | unknown | 0.0 | No coupling to anyone |
| ccc | unknown | 0.0 | No coupling to anyone |

---

## Coupling Matrix

```
       ccc  forgemaster  jasonclaw1  oracle1
ccc     0.0         0.0         0.0      0.0
fmg     0.3         0.3         0.3      0.3
jc1     0.0         0.0         0.0      0.0
ora     0.0         0.0         0.0      0.0
```

**Observation:** The coupling matrix is dominated by zero entries. Only `forgemaster` (stale, w=0.3) has any connectivity. This creates a near-disconnected graph.

---

## Spectral Analysis

| Metric | Value |
|--------|-------|
| λ₁ (largest) | 0.4854 |
| λ₂ (second) | 0.0000 |
| λ₃ | 0.0000 |
| λ₄ (smallest) | -0.1854 |
| **Normalized gap γ̃** | **1.0000** |
| fleet_math spectral_gap (same) | 1.0000 |

---

## Hypothesis Test

```
gap > 0.8  → TRUE  (γ̃ = 1.0)
health degraded → TRUE
→ H1 FALSIFIED: high spectral gap but degraded fleet health
```

**Result: H1 is FALSIFIED.**

---

## Analysis & Interpretation

### Why the gap is 1.0 despite degraded health

The spectral gap of 1.0 arises because the coupling matrix is **effectively disconnected** — only one agent (forgemaster) carries non-zero coupling. The eigenvalue spectrum separates into:

1. **One non-zero eigenvalue** (0.485) from forgemaster's weak self-coupling cluster
2. **Three zero/near-zero eigenvalues** from the three isolated agents

When λ₂ ≈ 0 and λ₁ > 0, the normalized gap (λ₁ - λ₂)/λ₁ → 1.0 regardless of absolute magnitude.

### What this means for H1

**The spectral gap, as computed from uniform coupling weights, is not a monotonic health indicator.** A disconnected network (most agents offline) produces a maximal spectral gap — the active component is internally well-connected, but the fleet as a whole is degraded because most agents aren't reachable.

### Required correction

To make H1 meaningful, the spectral gap must be computed from:
- **Actual interaction topology** (not uniform coupling)
- **Normalized by fleet size** or combined with a **connectivity ratio** (#connected components / n)

A better composite metric for fleet health would be:
```
H = γ̃ × (|active| / n)
```
where `|active|` counts agents with coupling weight > 0.

For this fleet: H = 1.0 × (1/4) = **0.25** — correctly indicating degraded health.

---

## Raw Output

```
Agents: ['ccc', 'forgemaster', 'jasonclaw1', 'oracle1']
Coupling matrix:
[[0.  0.  0.  0. ]
 [0.3 0.3 0.3 0.3]
 [0.  0.  0.  0. ]
 [0.  0.  0.  0. ]]
Eigenvalues: [-0.1854102  0.         0.         0.4854102]
Normalized gap gamma_tilde: 1.0000
Fleet health: degraded
fleet_math spectral_gap: 1.0000
H1 FALSIFIED: high spectral gap (1.0000) but degraded health (degraded)
```
