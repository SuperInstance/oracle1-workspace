# fleet-math — The Canonical Math of the Fleet

## What It Is

**fleet-math** (`SuperInstance/fleet-math`, v0.3.1) is the single canonical implementation of every mathematical algorithm used across the fleet. Before this package existed, three separate agents (Oracle1, Forgemaster, JC1) each implemented their own version of the Eisenstein lattice, coupling analysis, and PLATO HTTP clients. This package consolidated them into one `pip install fleet-math` — every agent now uses the same math.

## The Gold

### 1. Eisenstein Lattice (Z[ω] Chamber System)

The core of the fleet's coupling representation. 12 chambers on the hexagonal lattice Z[ω] where ω = e^(2πi/3). Every coupling vector gets snapped to one of 12 musical-chamber names (C, C#, D, ... B). This is the shared representation that lets Forgemaster talk constraint coupling, Oracle1 talk style vectors, and JC1 talk GPU warp allocation — all in the same mathematical space. The `chamber()` function does argmax snapping; `project()` lifts to 2D coordinates. Simple, elegant, canonical.

### 2. Penrose 5D → 2D Encoder

Oracle1's style-encoding system, now fleet-wide. Uses a 5th-roots-of-unity cut-and-project scheme: 5D vectors project to 2D via a fixed projection matrix, with an acceptance window (radius = 2φ, the golden ratio). This is how style dimensions (pitch, timing, velocity, articulation, timbre) get embedded into a 2D space for coupling and clustering. The perpendicular projection acts as the acceptance filter — points too far from the 5D conceptual lattice get rejected.

### 3. The Conservation Law (γ + H ≈ Constant)

**The biggest discovery in this repo.** An empirical law discovered through Monte Carlo simulation across all fleet agents: the sum of `algebraic_normalized` (gamma, graph connectivity) and `coupling_entropy` (H, diversity) is conserved for a given fleet size V, regardless of coupling matrix structure. The formula: γ + H = 1.283 − 0.159 ⋅ log(V), with R² = 0.9602 across V ∈ [5, 200] with 5000 samples each.

This is the fleet's analogue of mass-energy conservation. If an agent's coupling matrix violates this law (deviation > 0.15), it signals preferential attachment, measurement noise, or an anomalous regime worth investigating. The `fleet_conservation_law()` function returns predicted sums, deviation functions, and conservation checks with ±2σ confidence intervals.

### 4. Type-Aware Coupling Metrics

The `types.py` module calibrates conservation baselines per coupling type: `style` (universal empirical law), `topology` (sparse matrices), `mixed`, and `directed` (asymmetric). The `TypeAwareHealthMetric` auto-detects coupling type from matrix sparsity and asymmetry, then applies the correct baseline. This is how the fleet distinguishes "healthy diverse coupling" from "chaotic noise" and "consensus herd behavior."

### 5. Fleet Health Metrics

The `FleetHealthMetric` class provides a diagnostic z-score combining gamma, entropy, and timing stability. It classifies fleet health into three zones: healthy (|z| < 1), watch (1-2σ, with specific clues like low_connectivity, consensus_herd, chaotic_diverse), and anomaly (|z| > 2, investigate). The `fit_baseline()` method generates Monte Carlo baselines for any agent count.

## Why It Matters

fleet-math is the glue. Every agent computes coupling. Every agent needs the Eisenstein lattice. Every agent needs to know if the fleet is healthy. Before this, each one was writing their own version, introducing subtle incompatibilities that derailed cross-agent communication. Now: one import, one math, one fleet. The conservation law is the kind of emergent phenomenon you only discover when you unify — it was invisible before consolidation.
