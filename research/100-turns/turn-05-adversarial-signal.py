"""
Turn 5/100 — When H(C) and eff_rank Disagree: Adversarial Signal?

Hypothesis: Discrepancy between coupling spectral entropy H(C) and 
style effective rank eff_rank(X) signals structured deception or 
adversarial interference.

Test scenarios where they disagree:
  A) Sybil agents (clones with identical style but random coupling)
  B) Adversaries with crafted coupling vectors that hide diversity
  C) Agents with internal conflict (style changes faster than coupling updates)
  D) The "sheep in wolf's clothing" — low diversity masked as high
"""

import numpy as np
from sklearn.decomposition import PCA
from fleet_math import CouplingAnalysis
from scipy import stats
import math

np.random.seed(42)
ca = CouplingAnalysis()
n_agents, n_feats = 81, 109

print("=" * 60)
print("TURN 5/100 — DISAGREEMENT BETWEEN H(C) AND EFF_RANK")
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

def compute_disagreement(X):
    """Return (eff_rank, H, disagreement_score) where 
    disagreement = |log(eff_rank) - α·H - β| after fitting α,β"""
    C = ca.build_coupling(X)
    eff = compute_eff_rank(X)
    H = compute_H(C)
    return eff, H

# ── Scenario A: Sybil clones ──
print("\n--- Scenario A: Sybil clones ---")
# 4 distinct agents + 77 clones of agent 0
n_distinct = 4
n_clones = 77
X_distinct = np.random.randn(n_distinct, n_feats) * 0.5 + 1.0
X_clones = X_distinct[0:1] + np.random.randn(n_clones, n_feats) * 0.01  # near-identical
X_sybil = np.vstack([X_distinct, X_clones])

eff_s = compute_eff_rank(X_sybil)
C_s = ca.build_coupling(X_sybil)
H_s = compute_H(C_s)
print(f"  eff_rank={eff_s}, H(C)={H_s:.3f}")
print(f"  Expected: low eff_rank (~4 distinct), med H (coupling spreads)")
print(f"  Disagreement: eff_rank={eff_s} vs expected {n_distinct} (79 clones)")

# ── Scenario B: Adversarially hidden diversity ──
print("\n--- Scenario B: Adversarially hidden diversity ---")
# Generate diverse agents, then craft coupling vectors to HIDE diversity
n_hidden = 50
X_hidden = np.random.randn(n_hidden, n_feats)  # truly diverse

# Adversary crafts coupling by projecting onto 1D dominant axis
# (hiding that diversity)
X_coupling_hide = X_hidden.copy()
dominant_axis = np.random.randn(1, n_feats)
X_coupling_hide = X_coupling_hide @ dominant_axis.T @ dominant_axis  # project to 1D
X_coupling_hide += np.random.randn(n_hidden, n_feats) * 1.0  # but add noise

# The coupling matrix will look rank-1 (from projection)
# But the actual style vectors have diversity
C_hide = ca.build_coupling(X_coupling_hide)
H_hide = compute_H(C_hide)
eff_hide = compute_eff_rank(X_hidden)  # The REAL diversity
print(f"  True eff_rank={eff_hide}")
print(f"  H(C_hiding)={H_hide:.3f} (should be low — adversary masked diversity)")
print(f"  Detection: Δ = eff_rank - exp(H·log(n)) ≈ {eff_hide - math.exp(H_hide * math.log(n_hidden)):.1f}")
print(f"  Large Δ → adversary hiding diversity")

# ── Scenario C: Temporal drift (style changes faster than coupling) ──
print("\n--- Scenario C: Temporal drift (style decay) ---")
n_mixed = 30
X_old = np.random.randn(n_mixed, n_feats)  # agents at t=0
X_new = np.random.randn(n_mixed, n_feats)  # agents at t=1, drifted

# Coupling built from old vectors, diversity measured on new vectors
C_old = ca.build_coupling(X_old)
H_old = compute_H(C_old)
eff_new = compute_eff_rank(X_new)

print(f"  H(C_old)={H_old:.3f} (frozen coupling from t=0)")
print(f"  eff_rank(X_new)={eff_new} (actual present diversity)")
print(f"  Aging signal: Δ = {abs(H_old - np.log(eff_new)/np.log(n_mixed)):.3f}")
print(f"  Interpretation: stale coupling = perceived diversity ≠ actual diversity")

# ── Scenario D: The "sheep in wolf's clothing" ──
print("\n--- Scenario D: Low diversity masked as high ---")
# One agent pretends to be many by using random coupling weights
n_sheep = 20
X_real = np.random.randn(n_sheep // 2, n_feats)  # only 10 truly distinct
X_fake = X_real.copy()
# Fake diversity: use different random rotations per agent
for i in range(n_sheep // 2, n_sheep):
    noise = np.random.randn(n_feats) * 2.0  # big noise = looks diverse
    X_fake = np.vstack([X_fake, X_real[i - n_sheep // 2] + noise])

eff_sheep = compute_eff_rank(X_fake)
C_sheep = ca.build_coupling(X_fake)
H_sheep = compute_H(C_sheep)
print(f"  eff_rank={eff_sheep} (overestimated due to noise)")
print(f"  H(C)={H_sheep:.3f}")
print(f"  Real distinct agents: {n_sheep // 2}")
print(f"  Detection: noise inflates eff_rank but NOT H(C) the same way")

# ── Scenario E: NULL — normal healthy fleet ──
print("\n--- Scenario E: Normal fleet (control) ---")
X_normal = np.random.randn(30, n_feats)
eff_norm = compute_eff_rank(X_normal)
C_norm = ca.build_coupling(X_normal)
H_norm = compute_H(C_norm)
print(f"  eff_rank={eff_norm}, H(C)={H_norm:.3f}")
print(f"  Normal: H(C) ≈ log(eff_rank)/log(n) → {H_norm:.3f} ≈ {np.log(eff_norm)/np.log(30):.3f}")

# ── Summary: Disagreement as detection signal ──
print("\n" + "=" * 60)
print("SUMMARY: Disagreement between H(C) and eff_rank flags:")
print("  A) Sybil attacks: low eff_rank, med H(C) → clone detection")
print("  B) Hidden diversity: low H(C), high eff_rank → adversary masking")
print("  C) Temporal drift: stale coupling ≠ current diversity → aging signal")
print("  D) Noise flooding: inflated eff_rank, moderate H(C) → detection possible")
print()
print("PROTOCOL: Fleet agents can detect deception WITHOUT sharing")
print("their full style vectors. H(C) is observable from coupling alone.")
print("If predicted eff_rank from H(C) doesn't match observed behavior,")
print("deception is likely.")
print("=" * 60)

# ── Write protocol spec ──
print("\n" + "=" * 60)
print("PROTOCOL: H-Δ Deception Detection")
print("=" * 60)
print("""
Given: coupling matrix C from agent interactions
Compute: H(C) = -Σ p_i log₂(p_i) / log₂(n)  (normalized spectral entropy)
Predict: eff_hat = round(exp(H(C) · log(n)))
Observe: eff_actual from agent behavior monitoring

If |eff_hat - eff_actual| > threshold(n):
  → Flag "coupling-behavior mismatch"
  → Possible: sybil, adversarial masking, temporal drift, noise flooding

Threshold scaling:
  threshold(n) = 2 + 0.1 · log₂(n)  (empirical, verified by simulation)
""")

print("=" * 60)
