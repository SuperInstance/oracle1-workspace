"""
Turn 3/100 — Which Coupling Features Predict Style Dimensionality?

Hypothesis: While γ̃ (algebraic connectivity) does not correlate with 
effective rank, other spectral features of the coupling matrix DO predict it:
  - Participation ratio (PR = (Σλᵢ)² / Σλᵢ²) — how many eigenvalues matter
  - Spectral entropy H(λ) = -Σ pᵢ log pᵢ where pᵢ = λᵢ/Σλ
  - Spectral gap Δ = λ₁ - λ₂
  - Frobenius norm ||C||_F
  - Eigenvalue decay rate (power law exponent)

If none predict it, then style diversity is TRULY independent of coupling,
which means: ZHC and H1 operate on orthogonal dimensions of fleet state.
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
print("TURN 3/100 — WHICH COUPLING FEATURES PREDICT STYLE DIM?")
print("=" * 60)

def compute_spectral_features(C):
    """Extract all coupling/Laplacian spectral features."""
    eigvals = np.linalg.eigvalsh(C)[::-1]
    n = len(eigvals)
    
    trace = np.sum(eigvals)
    frob = np.linalg.norm(C)
    
    # Participation ratio (effective number of components)
    if trace > 0:
        pr = trace**2 / np.sum(eigvals**2)
    else:
        pr = 0
    
    # Spectral entropy
    p = np.abs(eigvals) / (np.sum(np.abs(eigvals)) + 1e-15)
    p = p[p > 0]
    H = -np.sum(p * np.log2(p)) / np.log2(n) if len(p) > 0 else 0  # normalized
    
    # Eigenvalue decay — power law fit
    idx = np.arange(1, min(n, 50) + 1)
    log_idx = np.log(idx)
    log_eig = np.log(np.maximum(eigvals[:len(idx)], 1e-15))
    if np.all(np.isfinite(log_eig)) and len(log_eig) > 3:
        slope, _, _, _, _ = stats.linregress(log_idx, log_eig)
    else:
        slope = 0
    
    # Laplacian features
    L = ca.laplacian(C)
    leig = np.linalg.eigvalsh(L)
    gamma_hat = (leig[1] - leig[0]) / (leig[-1] - leig[0] + 1e-15)
    
    # Ratio metrics
    lambda_ratio = eigvals[0] / (eigvals[1] + 1e-15)
    top_k_sum = np.sum(eigvals[:3])
    
    # Spectral gap (raw)
    gap = eigvals[0] - eigvals[1]
    
    return {
        'pr': pr,
        'H': H,
        'lambda_ratio': lambda_ratio,
        'gap': gap,
        'power_law': slope,
        'gamma_hat': gamma_hat,
        'frob': frob,
        'trace': trace,
        'top3_ratio': top_k_sum / (trace + 1e-15),
    }

# ── Generate 500 samples of varying true rank and noise ──
print("\n--- Generating 500 samples... ---")
samples = []
for _ in range(500):
    k_true = np.random.randint(1, 31)
    noise_sigma = np.random.uniform(0.05, 1.5)
    
    U = np.random.randn(n_agents, k_true)
    V = np.random.randn(k_true, n_feats)
    X = U @ V + np.random.randn(n_agents, n_feats) * noise_sigma
    
    # Compute effective rank
    pca = PCA()
    pca.fit(X)
    cum = np.cumsum(pca.explained_variance_ratio_)
    eff_95 = int(np.argmax(cum >= 0.95) + 1)
    eff_99 = int(np.argmax(cum >= 0.99) + 1)
    
    # Spectral features on coupling
    C = ca.build_coupling(X)
    feat = compute_spectral_features(C)
    feat['eff_95'] = eff_95
    feat['eff_99'] = eff_99
    feat['k_true'] = k_true
    feat['noise'] = noise_sigma
    samples.append(feat)

# ── Compute correlations ──
print("\n--- Correlation with effective rank (eff_95) ---")
features = ['pr', 'H', 'lambda_ratio', 'gap', 'power_law', 'gamma_hat', 'frob', 'trace', 'top3_ratio']
corrs = []
for feat_name in features:
    vals = np.array([s[feat_name] for s in samples])
    effs = np.array([s['eff_95'] for s in samples])
    
    # Check for non-constant data
    if np.std(vals) > 1e-10 and np.std(effs) > 1e-10:
        rho, p = stats.spearmanr(vals, effs)
        corrs.append((feat_name, rho, p))
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"  {feat_name:15s}: ρ={rho:+.3f} (p={p:.4f}) {sig}")
    else:
        print(f"  {feat_name:15s}: constant data, skipping")

# ── Can we build a predictor? ──
print("\n--- Multivariate prediction (linear regression) ---")
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

X_feat = np.column_stack([np.array([s[f] for s in samples]) for f in features])
y = np.array([s['eff_95'] for s in samples])

# Remove NaN/inf
mask = np.all(np.isfinite(X_feat), axis=1) & np.isfinite(y)
X_clean = X_feat[mask]
y_clean = y[mask]
print(f"  Clean samples: {np.sum(mask)}/{len(samples)}")

lr = LinearRegression()
scores = cross_val_score(lr, X_clean, y_clean, cv=5, scoring='r2')
print(f"  R² (5-fold CV): {np.mean(scores):.3f} ± {np.std(scores):.3f}")

# What if we include k_true and noise as predictors?
X_full = np.column_stack([X_feat, 
    np.array([s['k_true'] for s in samples]),
    np.array([s['noise'] for s in samples])])
Xf_clean = X_full[mask]
lr2 = LinearRegression()
scores2 = cross_val_score(lr2, Xf_clean, y_clean, cv=5, scoring='r2')
print(f"  R² WITH k_true + noise: {np.mean(scores2):.3f} ± {np.std(scores2):.3f}")
lr2.fit(Xf_clean, y_clean)
print(f"  Feature coefficients:")
names = features + ['k_true', 'noise']
for n, c in sorted(zip(names, lr2.coef_), key=lambda x: -abs(x[1])):
    print(f"    {n:15s}: {c:+.3f}")

print("\n" + "=" * 60)
print("KEY QUESTION: If coupling features don't predict eff_rank,")
print("then coupling (consensus) and style (diversity) are ORTHOGONAL.")
print("This means the fleet state space factorizes:")
print("  State = C_spectrum × Style_diversity × Active_agents")
print("=" * 60)
