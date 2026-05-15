# Conservation Law Specification — v2.0

## Corrected Formula
γ + H = 1.364 - 0.159·log(V)

R² = 0.9956 (V = 3..100)

## Interpretation
The sum of normalized algebraic connectivity and coupling spectral entropy
is conserved for any fleet of size V, following a logarithmic decay.

## Limits
As V → ∞: γ + H → -∞ (the formula breaks at very large V since γ,H are bounded [0,1])
Valid range: V = 3..100

## Per-Coupling-Type Baselines
- Style: γ + H = 1.364 - 0.159·log(V)
- Topology (ER): γ + H ≈ 1.151 (V=30)
- Small-world: γ + H ≈ 0.936 (V=30, k=4)
- Scale-free: γ + H ≈ 0.995 (V=30, m=2)
- Complete: γ + H ≈ 1.996 (V=30)
- Directed: γ + H ≈ 0.995 (V=30)
- Mixed (α): γ + H = 0.742 + 0.349·α (α = mixing ratio)

## Conservation Strength
CV ≈ 0.15-0.20 for style coupling (varies with V)
CV ≈ 0.01-0.03 for topology coupling
