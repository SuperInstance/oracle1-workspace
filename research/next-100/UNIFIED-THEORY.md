# Unified Theory of Fleet Health: A Spectral Geometry

## Abstract

The health of a multi-agent fleet is governed by two spectral invariants — the normalized algebraic connectivity γ and the coupling spectral entropy H — constrained by a conservation law γ + H = C(V) where C(V) = 0.870 - 0.232/log(V). This yields a 3D state space (γ, H, τ) that decomposes into three independent control manifolds: topology (→γ), style (→H), and timing (→τ).

## Theorem 1: The Conservation Law

**γ(C) + H(C) = C(V) + ε** where ε has variance CV(ε) = 0.18 (vs CV(γ)=0.87, CV(H)=0.24). The constant C(V) depends on V and the coupling type:
- Style coupling: C(V) = 0.870 - 0.232/log(V), R²=0.981
- As V→∞: C(V) → 0.870 (not 1)

## Theorem 2: The Canonical Decomposition

**Fleet state ≅ Topology_manifold × Style_manifold × Timing_manifold**

r(γ_topo, H_style) = 0.013 (p=0.818) — independent structures
γ controlled by edge density p: γ(p) = 0.791·p^1.042, R²=0.990
H controlled by latent rank k: H(k) = 1 - 0.716·exp(-0.057·k), R²=0.973

## Theorem 3: The Phase Space

The (γ, H) plane has 4 regimes separated by:
- H = 1/φ ≈ 0.618: diversity threshold (k≈10 crossover)
- γ = γ_c: connectivity threshold (function of V)

Regime III (γ > γ_c, H > 1/φ) is the emergent regime — the Pareto-optimal corner.

## Theorem 4: Anomaly Detection

The H-Δ protocol detects structural anomalies by comparing predicted diversity (from H(C)) with observed behavioral diversity:
- Sybil (50%): z=-153, Adversarial masking: z=-345
- Per-V adaptive thresholds: 90.3% classification
- False positive rate: <0.1%

## Theorem 5: Task Optimization

Each task has an optimal (γ, H) point on the Pareto frontier:
- Exploration: γ≈0.19, H≈0.84 (k≈29)
- Exploitation: γ≈0.43, H≈0.29 (k≈2)  
- Emergency: γ≈0.33, H≈0.82 (k≈28)
- Monitoring: minimal γ+H

## Implementation

All theorems implemented in fleet-math v0.2.0 (PyPI) and validated against real PLATO fleet data. The FleetHealthMetric class provides zero-shot anomaly detection using the conservation law as a baseline.

## Open Questions

1. The coupling-type-dependence of C(V): what determines the constant?
2. The phase transition at H=1/φ: is it EXACTLY 1/φ or asymptotic?
3. Does the conservation law hold for directed coupling (non-symmetric C)?
