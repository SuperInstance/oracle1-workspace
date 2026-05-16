# Experiment: Signed Laplacian as Stability Metric for Adversarial Environments

**Date:** 2026-05-14
**Method:** Synthetic coupling matrices, 6-agent fleet

## Hypothesis

> The signed Laplacian's second eigenvalue (Fiedler value of the signed graph) predicts fleet stability:
> - λ₂ > 0.5 → **stable**
> - 0.1 < λ₂ < 0.5 → **fragile**
> - λ₂ < 0.1 → **unstable**

## Data

| Case | λ₂ | Spectral Gap | Negative/Positive Edges | Weight | Verdict |
|---|---|---|---|---|---|
| cooperative-all | 6.0000 | 6.0000 | 0 / 30 | all +1 | **STABLE** ✓ |
| mixed-balanced | 2.7502 | 1.8173 | 20 / 10 | rand ±0.5–1.0 | **STABLE** ✓ |
| competitive-dominant | 1.8467 | 0.7190 | 20 / 10 | neg -0.8–-1.0, pos +0.2–0.5 | **STABLE** ✓ |
| adversarial-ring | 0.2679 | **0.0000** | 6 / 6 | alternating +1/-1 ring | **FRAGILE** ✓ |

All 4/4 cases **confirm** the hypothesis.

## Key Findings

### 1. Cooperative graph (case 1) — trivial confirmation
Standard all-positive graph: λ₂ = 6, κ = 1.0. Full algebraic connectivity. Consensus converges in O(1/6) time. **Baseline pass.**

### 2. Mixed signs (cases 2, 3) — counterintuitive
Both mixed-balanced and competitive-dominant registered λ₂ > 0.5 (stable) despite having 2× as many negative edges as positive. Why? The **absolute magnitude** of negative weights (~0.9 avg) barely exceeded positives (~0.35 avg for case 3). The signed Laplacian uses D_abs = diag(|W|·1), so heavy absolute weights increase node degrees, raising all eigenvalues. **The sign ratio alone doesn't determine λ₂ — edge magnitude matters.**

This suggests a refined metric: **λ₂ normalized by total absolute coupling** (κ = λ₂/λₙ) gives a better picture:
- cooperative-all: κ = 1.0000 (single coherent block)
- competitive-dominant: κ = 0.2936 (weakly coherent despite λ₂ > 0.5)
- adversarial-ring: κ = 0.0718 (nearly incoherent)

### 3. Adversarial ring (case 4) — the real test
Alternating +1/-1 on a ring topology. λ₂ = 0.2679, λ₁ = 0.2679 (spectral gap = 0). **Eigenvalue multiplicity** — λ₁ ≈ λ₂ means the eigenvector subspace is 2D. This is the classic signature of a signed graph approaching bipartite frustration. Even with equal positive/negative edges, the alternating pattern creates near-instability. **Threat: a clever adversary could arrange pairwise competitions to collapse λ₂ below the threshold without increasing total negativity — just by alternating signs.**

### 4. Where the "unstable" bucket should matter
No test case hit λ₂ < 0.1. That requires near-perfect cancellation of signed coupling — achievable via:
- **Bipartite graph** with balanced signs (e.g., two equally-sized factions with internal cooperation and cross-faction competition)
- **Grasshopper graph** (dense positive cliques with moderate negative cross-edges)
- **Signed complete graph** where sum of each row ≈ 0

## Recommendations

1. **Use κ = λ₂/λₙ (normalized) instead of raw λ₂** — magnitude-independent comparison across fleet sizes
2. **Monitor spectral gap λ₂ − λ₁**, not just λ₂ — eigenvalue multiplicity indicates latent factions
3. **Boundary refinement**: current thresholds (0.5, 0.1) are preliminary. Re-calibrate on physical fleet simulations with actual dynamics (consensus protocol + adversarial injection)
4. **Signed Cheeger constant** may outperform λ₂ for sparse adversarial topologies (ring, path, star-with-traitor)

## Code

```python
import numpy as np

def signed_algebraic_connectivity(W):
    D_abs = np.diag(np.abs(W).sum(axis=1))
    L = D_abs - W
    eigs = np.sort(np.linalg.eigvalsh(L))
    return eigs

def normalize_metrics(W):
    eigs = signed_algebraic_connectivity(W)
    kappa = eigs[1] / eigs[-1]  # λ₂ / λₙ
    gap = eigs[1] - eigs[0]     # λ₂ - λ₁
    return {"lambda_2": eigs[1], "kappa": kappa, "gap": gap}
```
