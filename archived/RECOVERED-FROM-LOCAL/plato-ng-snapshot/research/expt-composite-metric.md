# Experiment: Composite Metric H Validation

## Formula Tested

```
H = gamma_tilde × (|active| / n)

where:
  gamma_tilde = (λ_max - λ_2nd_max) / λ_max
  λ from eigendecomposition of W (weighted adjacency + self-loops)
  |active| = count of non-stale agents
  n = total fleet size
```

## Test Cases

### Case 1: All Online — ✅ PASS
- Matrix: `ones(4,4) + 0.5×I` (fully connected, strong self-loops)
- Active: 4/4
- **H = 0.889** (expected > 0.8)
- High spectral gap + full active ratio → healthy fleet

### Case 2: Half Online — ⚠️ DEGENERATE FALSE NEGATIVE
- Matrix: `diag([1, 1, 0.3, 0.3])` (no cross-coupling)
- Active: 2/4
- **H = 0.000** (expected 0.25–0.5)
- **Cause:** Diagonal matrix produces two equal eigenvalues (1.0, 1.0). The spectral gap gamma = (1−1)/1 = 0, collapsing H to zero.
- **Diagnosis:** This is partly a test-construction artifact — a real fleet would have nonzero cross-coupling between active agents.
- **With realistic coupling:** `W = [[1,0.5,0,0],[0.5,1,0,0],[0,0,0.3,0.1],[0,0,0.1,0.3]]` → H = **0.333** (within expected range).
- **Real concern:** A fleet where active agents form two fully disconnected subgraphs would also get gamma=0. This is a genuine blind spot.

### Case 3: 3 of 4 Stale — ✅ PASS
- Matrix: `0.1 × diag([1,0.3,0.3,0.3]) + 0.9 × ones(4,4)` (one healthy agent, three weak but coupled)
- Active: 1/4
- **H = 0.244** (expected < 0.3)
- Low active ratio dominates, keeping H below threshold

## Results Summary

| Case | H | Expected | Status |
|------|---|----------|--------|
| All online | 0.889 | > 0.8 | ✅ PASS |
| Half online (diagonal) | 0.000 | 0.25–0.5 | ⚠️ FAIL (artifact) |
| Half online (coupled) | 0.333 | 0.25–0.5 | ✅ PASS (realistic) |
| 3 of 4 stale | 0.244 | < 0.3 | ✅ PASS |

## Key Finding: The Spectral Gap Degeneracy Problem

The composite metric H works correctly **when the interaction graph has a clear dominant eigenvalue mode**. However, gamma (spectral gap) collapses to zero when the two largest eigenvalues are equal, which happens naturally for:

1. **Disconnected components of equal size** — two independent active clusters of similar size
2. **Diagonal matrices** — no cross-coupling (the test artifact case)
3. **Perfect symmetry** — e.g., a fleet split into two identical subgraphs

### Mitigation Options

1. **Degree-normalized γ**: Replace `γ = (λ₁−λ₂)/λ₁` with `γ = (λ₁−λ₂)/(λ₁−λₙ)` to normalize by the full spectral range.
2. **Active-ratio fallback**: When `γ < ε`, fall back to `H = |active|/n` (pure coverage ratio).
3. **Clustering-aware variant**: Use algebraic connectivity (Fiedler eigenvalue) instead of top-two gap for disconnected cases.

## Conclusion

The composite metric `H = γ × (|active|/n)` is **conditionally validated**. It cleanly distinguishes healthy fleets from degraded ones when the interaction graph has a clear dominant eigenvalue. The degeneracy edge case (gamma=0 from equal eigenvalues) is the main vulnerability — but it primarily manifests when active agents are fully disconnected, which is at least partially detectable.

**Recommendation:** Use H as the primary metric but add a Fiedler-value floor check or active-ratio fallback to handle the degenerate case.

## Raw Output

```
  All online: H=0.889 (expected: >0.8)
  Half online: H=0.000 (expected: 0.25-0.5)
  3 of 4 stale: H=0.244 (expected: <0.3)

Half-online eigenvalues (sorted): [0.3 0.3 1.  1. ]
Cause: gamma collapse from repeated eigenvalues
With realistic coupling: gamma=0.667, H=0.333
```

*Generated 2026-05-14 17:55 UTC — subagent expt-composite-metric*
