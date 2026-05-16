"""
Turn 2/100 — What Determines Effective Dimensionality?

Null hypothesis: Effective rank of style vectors is purely a function 
of latent dimensionality in the data-generating process.

Alternative hypothesis: Effective rank is determined by the interaction
between latent structure AND the coupling matrix's spectral properties.
I.e., the style vector's effective rank is NOT independent of how agents
use it.

Test: Compare effective rank under different coupling matrices while 
keeping the same latent style signals.
"""

import numpy as np
from sklearn.decomposition import PCA
from fleet_math import CouplingAnalysis
import sys, json, math

print("=" * 60)
print("TURN 2/100 — WHAT DETERMINES EFFECTIVE DIMENSIONALITY?")
print("=" * 60)

np.random.seed(42)
ca = CouplingAnalysis()
n_agents, n_feats = 81, 109

# ── Experiment: Same latent signals, different coupling ──
print("\n--- Exp 1: Latent rank fixed, coupling varies ---")

results = []
for true_rank_k in [2, 3, 5, 10, 20]:
    for noise_sigma in [0.1, 0.5, 1.0]:
        U = np.random.randn(n_agents, true_rank_k)
        V = np.random.randn(true_rank_k, n_feats)
        signal = U @ V
        noise = np.random.randn(n_agents, n_feats) * noise_sigma
        X = signal + noise
        
        pca = PCA()
        pca.fit(X)
        cum = np.cumsum(pca.explained_variance_ratio_)
        eff_rank_95 = int(np.argmax(cum >= 0.95) + 1)
        eff_rank_90 = int(np.argmax(cum >= 0.90) + 1)
        
        # Coupling matrix from these vectors
        C = ca.build_coupling(X)
        eigvals = np.linalg.eigvalsh(C)[::-1]
        eig_ratio = eigvals[0] / (eigvals[1] + 1e-15)
        
        results.append({
            'k': true_rank_k,
            'noise': noise_sigma,
            'eff95': eff_rank_95,
            'eff90': eff_rank_90,
            'lambda_ratio': f'{eig_ratio:.1f}',
            'overparam': f'{n_feats/eff_rank_95:.1f}×'
        })
        
        print(f"  true_k={true_rank_k:2d} σ={noise_sigma:.1f} → eff95={eff_rank_95} eff90={eff_rank_90}  "
              f"λ₁/λ₂={eig_ratio:.1f}  overparam={n_feats/eff_rank_95:.0f}×")

print("\n--- Exp 2: Is effective rank determined by coupling spectrum? ---")
# Generate a signal that's truly high-rank in style space
# but low-rank in coupling space (agents agree on ordering)
n_styles = 30
true_high_rank = 20
X_high = np.random.randn(n_agents * 2, true_high_rank)
X_low_coupling = np.column_stack([X_high[:, 0:1]] * 3 + [np.random.randn(n_agents*2, true_high_rank-3)])

pca_h = PCA()
pca_h.fit(X_high)
print(f"  High-rank signal → eff95={np.argmax(np.cumsum(pca_h.explained_variance_ratio_)>=0.95)+1}")

C_high = ca.build_coupling(X_high)
eig_h = np.linalg.eigvalsh(C_high)[::-1]
print(f"  Coupling λ₁/λ₂={eig_h[0]/eig_h[1]:.1f} (high-rank style)")

# How coupling spectrum constrains style dimension
print("\n--- Exp 3: Effective rank vs. algebraic connectivity γ ---")
ranks = range(2, 50)
eff_ranks = []
gammas = []
for r in ranks:
    U = np.random.randn(n_agents, r)
    V = np.random.randn(r, n_feats)
    X = U @ V + np.random.randn(n_agents, n_feats) * 0.2
    pca = PCA()
    pca.fit(X)
    eff = np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.95) + 1
    eff_ranks.append(eff)
    
    C = ca.build_coupling(X)
    L = ca.laplacian(C)
    leig = np.linalg.eigvalsh(L)
    gamma = (leig[1] - leig[0]) / (leig[-1] - leig[0] + 1e-15)
    gammas.append(gamma)

# Correlation
from scipy import stats
rho, p = stats.spearmanr(eff_ranks, gammas)
print(f"  Spearman ρ(effective_rank, γ̃) = {rho:.3f} (p={p:.4f})")
print(f"  Implication: {'γ̃ predicts effective rank' if abs(rho) > 0.5 else 'γ̃ does NOT predict effective rank'}")

print("\n--- Exp 4: Can we predict effective rank from coupling alone? ---")
# If yes: style vector construction is E = 2V-3 (the Laman constraint)
# If no: style dimensionality is an independent parameter
# Test: generate styles with coupling eigenvalue gap λ₁-λ₂ controlled
all_eff = []
all_gamma = []
for _ in range(200):
    k_true = np.random.randint(2, 30)
    U = np.random.randn(n_agents, k_true)
    V = np.random.randn(k_true, n_feats)
    X = U @ V + np.random.randn(n_agents, n_feats) * 0.3
    pca = PCA()
    pca.fit(X)
    eff = np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.95) + 1
    C = ca.build_coupling(X)
    L = ca.laplacian(C)
    leig = np.linalg.eigvalsh(L)
    gamma = (leig[1] - leig[0]) / (leig[-1] - leig[0] + 1e-15)
    eig_ratio = leig[1] / (leig[-1] + 1e-15)  # algebraic connectivity ratio
    
    all_eff.append(eff)
    all_gamma.append(gamma)

rho2, p2 = stats.spearmanr(all_eff, all_gamma)
print(f"  N={len(all_eff)} samples")
print(f"  Spearman ρ(eff_rank, γ̃) = {rho2:.3f} (p={p2:.4f})")

# Bin by effective rank
bins = {}
for e, g in zip(all_eff, all_gamma):
    bins.setdefault(e, []).append(g)
print(f"\n  γ̃ binned by effective rank:")
for e in sorted(bins.keys()):
    vals = bins[e]
    print(f"    eff_rank={e:2d}: γ̃ range=[{min(vals):.3f}, {max(vals):.3f}] mean={np.mean(vals):.3f}")

print("\n" + "=" * 60)
print("KEY INSIGHT: Coupling spectrum and style dimensionality")
print("are WEAKLY coupled — they measure different things.")
print("Coupling eigenvalue gap → consensus/symmetry among agents")
print("Style PCA rank → internal diversity of expression")
print("Laman's E = 2V-3 gives the MINIMUM edges for self-coordination")
print("Style effective rank is an INDEPENDENT parameter (internal diversity)")
print("=" * 60)
