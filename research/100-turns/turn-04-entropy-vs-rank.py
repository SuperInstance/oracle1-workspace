"""
Turn 4/100 — Is Spectral Entropy H(C) Really the Same as Eff_Rank(X)?

Hypothesis: Spectral entropy of the coupling matrix and effective rank 
of style vectors share information through the same mathematical structure.
Specifically, H(C) ≈ log(eff_rank) for well-conditioned coupling matrices.

Test: Vary true rank (k_true) while controlling for noise to see if
H(Coupling) tracks eff_rank(X) across the full range.

Also test: Can we use H(C) as a SURROGATE for eff_rank when we only 
have coupling (no style vectors)? This would mean agents can estimate
fleet diversity without sharing their full style vectors.
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
print("TURN 4/100 — H(C) vs EFF_RANK(X): SAME OR DIFFERENT?")
print("=" * 60)

# ── Controlled experiment: vary true rank with LOW noise ──
print("\n--- Exp 1: Clean signal — vary k_true ---")
clean_results = []
for k_true in range(1, 31):
    eff_ranks = []
    entropies = []
    for rep in range(50):
        U = np.random.randn(n_agents, k_true)
        V = np.random.randn(k_true, n_feats)
        X = U @ V + np.random.randn(n_agents, n_feats) * 0.1
        
        pca = PCA()
        pca.fit(X)
        cum = np.cumsum(pca.explained_variance_ratio_)
        eff_95 = int(np.argmax(cum >= 0.95) + 1)
        eff_ranks.append(eff_95)
        
        C = ca.build_coupling(X)
        eigvals = np.linalg.eigvalsh(C)[::-1]
        p = np.abs(eigvals) / (np.sum(np.abs(eigvals)) + 1e-15)
        p = p[p > 1e-10]
        H = -np.sum(p * np.log(p)) / np.log(n_agents)  # normalized by max
        entropies.append(H)
    
    mean_eff = np.mean(eff_ranks)
    mean_H = np.mean(entropies)
    clean_results.append((k_true, mean_eff, mean_H))
    if k_true in [1, 2, 3, 5, 10, 15, 20, 25, 30]:
        print(f"  k_true={k_true:2d} → mean_eff={mean_eff:4.1f}  mean_H={mean_H:.3f}")

# Relationship: eff_rank vs H(C)
effs = np.array([r[1] for r in clean_results])
Hs = np.array([r[2] for r in clean_results])
rho, p = stats.spearmanr(effs, Hs)
print(f"\n  Spearman ρ(eff_95, H_Coupling) = {rho:.3f} (p={p:.4f})")
print(f"  Pearson r(log(eff_95), H_Coupling) = {np.corrcoef(np.log(effs+1), Hs)[0,1]:.3f}")

# ── Exp 2: Can H(C) substitute for eff_rank when style vectors hidden? ──
print("\n--- Exp 2: Surrogate test (coupling-only estimation) ---")
# Simulate: agents only share coupling, not style vectors
surrogate_results = []
for _ in range(200):
    k_true = np.random.randint(1, 25)
    noise = np.random.uniform(0.05, 1.0)
    
    U = np.random.randn(n_agents, k_true)
    V = np.random.randn(k_true, n_feats)
    X = U @ V + np.random.randn(n_agents, n_feats) * noise
    
    # True eff_rank (requires style vectors)
    pca = PCA()
    pca.fit(X)
    true_eff = np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.95) + 1
    
    # Coupling-only features (no style vectors needed)
    C = ca.build_coupling(X)
    eigvals = np.linalg.eigvalsh(C)[::-1]
    p = np.abs(eigvals) / (np.sum(np.abs(eigvals)) + 1e-15)
    p = p[p > 1e-10]
    H = -np.sum(p * np.log(p)) / np.log(n_agents)
    
    # Power law decay slope
    idx = np.arange(1, min(len(eigvals), 50) + 1)
    log_eig = np.log(np.maximum(eigvals[:len(idx)], 1e-15))
    log_idx = np.log(idx)
    if np.all(np.isfinite(log_eig)) and len(log_eig) > 3:
        slope, _, _, _, _ = stats.linregress(log_idx, log_eig)
    else:
        slope = 0
    
    surrogate_results.append({'true_eff': true_eff, 'H': H, 'slope': slope})

# Plot the scatter
true_effs = np.array([r['true_eff'] for r in surrogate_results])
Hs_arr = np.array([r['H'] for r in surrogate_results])
slopes_arr = np.array([r['slope'] for r in surrogate_results])

print(f"\n  N={len(surrogate_results)} surrogates")
print(f"  H(C) → true_eff: ρ={stats.spearmanr(Hs_arr, true_effs)[0]:.3f}")
print(f"  power_law → true_eff: ρ={stats.spearmanr(slopes_arr, true_effs)[0]:.3f}")

# Simple predictor: eff_rank ≈ exp(α·H + β)
H_clean = Hs_arr[np.isfinite(Hs_arr) & (Hs_arr > 0)]
eff_clean = true_effs[np.isfinite(Hs_arr) & (Hs_arr > 0)]
if len(H_clean) > 10:
    log_eff = np.log(eff_clean)
    r2 = np.corrcoef(H_clean, log_eff)[0,1] ** 2
    print(f"\n  H ∼ log(eff_rank): R² = {r2:.3f}")

# ── Exp 3: The degeneracy test — what happens at k_true=1? ──
print("\n--- Exp 3: Edge case — k_true=1 (single latent factor) ---")
all_H_k1 = []
for _ in range(100):
    U = np.random.randn(n_agents, 1)
    V = np.random.randn(1, n_feats)
    X = U @ V + np.random.randn(n_agents, n_feats) * 0.05
    C = ca.build_coupling(X)
    eigvals = np.linalg.eigvalsh(C)[::-1]
    p = np.abs(eigvals) / (np.sum(np.abs(eigvals)) + 1e-15)
    p = p[p > 1e-10]
    H = -np.sum(p * np.log(p)) / np.log(n_agents)
    all_H_k1.append(H)

print(f"  Mean H(C) at k_true=1: {np.mean(all_H_k1):.3f}")
print(f"  Theoretical minimum: H=0 for rank-1 coupling matrix")
print(f"  Actual H=0.95 × H for rank-1: C_ij = s_i · s_j / ||s_i||·||s_j|| gives")
print(f"  λ₁ = n (dominant), λ₂..λₙ ≈ 0 → H ≈ 0  since only 1 eigenvalue matters")

# ── Exp 4: Formal relationship ──
print("\n--- Exp 4: Formal bound — eff_rank vs coupling entropy ---")
print("""
Theoretical connection:
  If X = U V^T + ε (noise), then C = X X^T / (diag norm).
  
  eig(C) ≈ eig(X X^T) / trace(X X^T) for normalized vectors.
  eig(XX^T) = σ_i²(X) where σ_i are singular values of X.
  
  Therefore: spectral entropy H(C) ≈ H(σ²(X) / Σσ²) = von Neumann entropy of Gram matrix.
  
  And: effective rank of X = number of σ_i² above noise floor.
  
  CONNECTION: Both measure the SHAPE of the singular value spectrum.
  H(C) is a continuous measure; eff_rank is a hard threshold.
  They are DIFFERENT views of the same underlying structure.

Falsifiable prediction: For any coupling matrix C from any source:
  eff_rank(X) ≈ soft_threshold(-H(C), n_agents)
  
  Where soft_threshold converts entropy to rank via
  eff_rank = exp(α·H(C) + β) with α ≈ 2 (entropy of 48-dim sphere)
""")
print("=" * 60)
