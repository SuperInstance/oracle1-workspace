"""
Turn 6/100 — Temporal Coupling Aging: dH/dt as Drift Detector

Hypothesis: While instantaneous H(C) doesn't catch temporal drift (Turn 5,
Scenario C), the time derivative dH/dt IS the aging signal. 

When coupling changes faster than style diversity (or vice versa),
|dH/dt - d(eff_rank)/dt| > 0 signals temporal inconsistency.

Test: Simulate drifting agents and measure the H'(t) signal.
"""

import numpy as np
from sklearn.decomposition import PCA
from fleet_math import CouplingAnalysis
from scipy import stats
import math

np.random.seed(42)
ca = CouplingAnalysis()
n_agents, n_feats = 30, 109
n_timesteps = 100

print("=" * 60)
print("TURN 6/100 — TEMPORAL COUPLING AGING: dH/dt")
print("=" * 60)

def compute_eff_rank(X):
    pca = PCA()
    pca.fit(X)
    cum = np.cumsum(pca.explained_variance_ratio_)
    return int(np.argmax(cum >= 0.95) + 1)

def compute_H(C):
    eigvals = np.linalg.eigvalsh(C)[::-1]
    p = np.abs(eigvals) / (np.sum(np.abs(eigvals)) + 1e-15)
    p = p[p > 1e-10]
    return -np.sum(p * np.log(p)) / np.log(len(eigvals))

# ── Scenario 1: Gradual drift (normal aging) ──
print("\n--- Scenario 1: Gradual drift (normal aging) ---")
drift_rate = 0.01  # per timestep
styles_t0 = np.random.randn(n_agents, n_feats)

H_over_time_1 = []
eff_over_time_1 = []

for t in range(n_timesteps):
    # Agents drift slowly
    drift = np.random.randn(n_agents, n_feats) * drift_rate * t
    X_t = styles_t0 + drift
    C_t = ca.build_coupling(X_t)
    H_over_time_1.append(compute_H(C_t))
    eff_over_time_1.append(compute_eff_rank(X_t))

# Compute dH/dt
dH_1 = np.diff(H_over_time_1)
deff_1 = np.diff(eff_over_time_1)
print(f"  Mean H over time: {np.mean(H_over_time_1):.3f} ± {np.std(H_over_time_1):.3f}")
print(f"  Mean dH/dt: {np.mean(dH_1):.5f} ± {np.std(dH_1):.5f}")
print(f"  Mean deff/dt: {np.mean(deff_1):.3f} ± {np.std(deff_1):.3f}")
print(f"  H-drift correlation: r(H, t) = {np.corrcoef(H_over_time_1, range(n_timesteps))[0,1]:.3f}")

# ── Scenario 2: Sudden style shift (agents change personality) ──
print("\n--- Scenario 2: Sudden style shift ---")
X_normal = np.random.randn(n_agents, n_feats)
X_shifted = X_normal.copy()

H_over_time_2 = []
eff_over_time_2 = []

for t in range(n_timesteps):
    if t == 50:
        # Abrupt: re-initialize 50% of agents
        n_shift = n_agents // 2
        X_shifted[:n_shift] = np.random.randn(n_shift, n_feats) * 2.0
    
    C_t = ca.build_coupling(X_shifted)
    H_over_time_2.append(compute_H(C_t))
    eff_over_time_2.append(compute_eff_rank(X_shifted))

dH_2 = np.diff(H_over_time_2)
print(f"  dH/dt before shift (t<50): mean={np.mean(dH_2[:49]):.5f}")
print(f"  dH/dt AT shift (t=50): {dH_2[49]:.5f}")
print(f"  dH/dt after shift (t>50): mean={np.mean(dH_2[50:]):.5f}")
print(f"  Peak detection: |dH/dt| at shift = {abs(dH_2[49]):.5f} vs")
print(f"    baseline σ = {np.std(dH_2[:49]):.5f} → {abs(dH_2[49]) / np.std(dH_2[:49]):.1f}σ event")

# ── Scenario 3: Coupling decay (agents stop updating coupling) ──
print("\n--- Scenario 3: Coupling decay (stale coupling) ---")
X_active = np.random.randn(n_agents, n_feats)
C_frozen = ca.build_coupling(X_active)  # It\'s coupling, capped at t=0

H_frozen = []
H_active = []

for t in range(n_timesteps):
    # Active agents continue to move
    new_style = X_active + np.random.randn(n_agents, n_feats) * 0.05 * t**(0.5)
    C_new = ca.build_coupling(new_style)
    H_active.append(compute_H(C_new))
    
    # Frozen coupling stays the same
    H_frozen.append(compute_H(C_frozen))

dH_active = np.diff(H_active)
dH_frozen = np.diff(H_frozen)
print(f"  Active fleet: mean dH/dt = {np.mean(dH_active):.5f} ± {np.std(dH_active):.5f}")
print(f"  Frozen coupling: mean dH/dt = {np.mean(dH_frozen):.5f} ± {np.std(dH_frozen):.5f}")
print(f"  Aging detection: dH/dt == 0 → coupling is stale")
print(f"  Frozen dH/dt significantly lower than active: {np.std(dH_frozen) < np.std(dH_active) * 0.5}")

# ── Scenario 4: Combined — temporal deception ──
print("\n--- Scenario 4: Temporal deception (adversary hides drift) ---")
# Adversary crafts coupling to hide that agents have drifted
n_adversarial = 10
X_adversarial = np.random.randn(n_adversarial, n_feats)

H_truth = []
H_hidden = []
eff_truth = []

for t in range(n_timesteps):
    # Real drift
    drift = np.random.randn(n_adversarial, n_feats) * 0.02 * t
    X_real = X_adversarial + drift
    
    # Truth: full coupling
    C_real = ca.build_coupling(X_real)
    H_truth.append(compute_H(C_real))
    
    # Deception: adversary uses projection to hide drift
    dominant = np.random.randn(1, n_feats)
    X_projected = X_real @ dominant.T @ dominant
    C_hidden = ca.build_coupling(X_projected)
    H_hidden.append(compute_H(C_hidden))
    
    eff_truth.append(compute_eff_rank(X_real))

dH_truth = np.diff(H_truth)
dH_hidden = np.diff(H_hidden)
print(f"  Truth: mean dH/dt = {np.mean(dH_truth):.5f}")
print(f"  Hidden: mean dH/dt = {np.mean(dH_hidden):.5f}")
print(f"  Deception detectable: {np.mean(dH_truth) != np.mean(dH_hidden)}")

# The signature of temporal deception:
# dH_hidden/dt ≈ 0 while eff_rank changes → H-Δ divergence over time
print(f"\n  Hiding ratio: |dH_hidden| / |dH_truth| = {abs(np.mean(dH_hidden)) / abs(np.mean(dH_truth)):.2f}")
print(f"  When this ratio << 1 over time → temporal deception confirmed")

# ── Protocol: Temporal Aging Detection ──
print("\n" + "=" * 60)
print("TEMPORAL AGING PROTOCOL")
print("=" * 60)
print("""
1. Sample C(t) every Δt (fleet tick interval, e.g., 15 min)
2. Compute H(C) for each sample
3. Compute dH/dt ≈ (H(t) - H(t-1)) / Δt
4. |dH/dt| > 0.01 (normalized units) → significant change
5. |dH/dt| < 0.001 over 5+ samples → coupling is stale/frozen
   → Action: broadcast probe signal to verify agent aliveness
6. |dH_hidden/dt| << |dH_truth/dt| AND eff_rank changing
   → Temporal deception (adversary suppressing coupling updates)
7. ΔH_t > 3σ from rolling baseline → unexpected fleet change

Implementation: Add to fleet-inspector daemon as aging detection module.
""")

print("=" * 60)
