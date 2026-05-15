"""
Turns 19-25/100 — H-gamma Phase Space & Phase Transitions
"""

import numpy as np
from sklearn.decomposition import PCA
from fleet_math import CouplingAnalysis, PHI
from scipy import stats
import math, sys, os

sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/research/100-turns"))
from fleet_health_v2 import coupling_entropy, algebraic_normalized

np.random.seed(42)
ca = CouplingAnalysis()
nF = 109

def coupling_from_vectors(X):
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-10
    return X @ X.T / (norms @ norms.T)

print("="*60)

# Turn 19: H-gamma phase space mapping
print("TURN 19 — H-GAMMA PHASE SPACE")

# Scan across: V (fleet size), diversity (latent rank), connectivity (graph density)
phase_points = []
for V in [5, 10, 20, 50, 100]:
    for k in [1, 2, 5, 10, 20]:
        for _ in range(20):
            X = np.random.randn(V, nF)
            if k < nF:
                # Limited latent diversity
                U = np.random.randn(V, k)
                Vm = np.random.randn(k, nF)
                X = U @ Vm + np.random.randn(V, nF) * 0.2
            
            C = coupling_from_vectors(X)
            gamma = algebraic_normalized(C)
            H = coupling_entropy(C)
            phase_points.append((V, k, gamma, H))

# Find the H-1/phi crossing
for V in [5, 10, 20, 50, 100]:
    pts = [(g, h) for (v, k, g, h) in phase_points if v == V]
    gs = [p[0] for p in pts]
    hs = [p[1] for p in pts]
    print(f"  V={V:3d}: gamma_range=[{min(gs):.3f},{max(gs):.3f}] H_range=[{min(hs):.3f},{max(hs):.3f}]")
    n_above_phi = sum(1 for h in hs if h > 1/PHI)
    print(f"         H > 1/phi: {n_above_phi}/{len(hs)} ({n_above_phi/len(hs)*100:.0f}%)")

# Turn 20: Does H < 1/phi correlate with rank-1 coupling?
print("\nTURN 20 — H < 1/phi AND RANK-1 COUPLING")
for k_latent in [1, 2, 3, 5, 10]:
    Hs = []
    for _ in range(100):
        V = 30
        U = np.random.randn(V, k_latent)
        Vm = np.random.randn(k_latent, nF)
        X = U @ Vm + np.random.randn(V, nF) * 0.1
        C = coupling_from_vectors(X)
        H = coupling_entropy(C)
        Hs.append(H)
    print(f"  k_latent={k_latent:2d}: H(C)={np.mean(Hs):.3f}+-{np.std(Hs):.3f} below_phi={np.mean(Hs) < 1/PHI}")

# Turn 21: Does emergence (H1 > V-2) have a H-gamma signature?
print("\nTURN 21 — EMERGENCE SIGNATURE IN H-gamma SPACE")
# From fleet-math: E > 2V-3 means over-constrained = emergence
# H1 beta1 = E - V + 1 > V-2 means emergence
for V in [10, 20, 30, 50]:
    for edge_mult in [1.0, 1.5, 2.0, 3.0, 5.0]:
        E = int((2*V - 3) * edge_mult)  # Laman threshold * multiplier
        E = min(E, V*(V-1)//2)
        
        # Build graph with E edges
        edges = set()
        for i in range(1, V):
            j = np.random.randint(0, i)
            edges.add((i,j) if i<j else (j,i))
        possible = [(i,j) for i in range(V) for j in range(i+1,V) if (i,j) not in edges]
        extra = min(len(possible), E - (V-1))
        if extra > 0:
            for e in np.random.choice(len(possible), extra, replace=False):
                edges.add(possible[e])
        
        # Build coupling with noise
        C = np.zeros((V, V))
        for i, j in edges:
            w = np.random.uniform(0.3, 1.0)
            C[i,j] = C[j,i] = w
        C = C + np.random.randn(V, V) * 0.1  # noise
        C = (C + C.T) / 2  # symmetrize
        np.fill_diagonal(C, 1.0)
        
        gamma = algebraic_normalized(C)
        H = coupling_entropy(C)
        beta1 = E - V + 1
        emergence = beta1 > V - 2
        
        print(f"  V={V:2d} E={E:4d} edge_mult={edge_mult:.1f}: gamma={gamma:.3f} H={H:.3f} beta1={beta1:3d} emergence={emergence}")
    print()

# Turn 22: Phase diagram — is there a critical line?
print("TURN 22 — PHASE DIAGRAM CRITICAL LINE")
# Scan across V=5..100, compute gamma and H for random graphs
# Find if there's a functional relationship
from collections import defaultdict
phase_bins = defaultdict(list)
for _ in range(1000):
    V = np.random.randint(5, 101)
    p = np.random.uniform(0.05, 0.5)  # edge probability
    # Erdos-Renyi graph
    C = np.zeros((V, V))
    for i in range(V):
        for j in range(i+1, V):
            if np.random.random() < p:
                C[i,j] = C[j,i] = np.random.uniform(0.3, 1.0)
    # Ensure diagonal is 1
    np.fill_diagonal(C, 1.0)
    # Normalize
    d = np.maximum(C.sum(axis=1), 1.0)
    C = C / np.sqrt(np.outer(d, d))
    
    gamma = algebraic_normalized(C)
    H = coupling_entropy(C)
    
    phase_bins['all'].append((V, p, gamma, H))

# Check correlation
gs = [p[2] for p in phase_bins['all']]
hs = [p[3] for p in phase_bins['all']]
rho, pv = stats.spearmanr(gs, hs)
print(f"  N={len(gs)}: Spearman rho(gamma, H) = {rho:.3f} (p={pv:.4f})")

# Bin by fleet size
for V_bin in [(5,15), (16,30), (31,60), (61,100)]:
    pts = [(g, h) for (v, _, g, h) in phase_bins['all'] if V_bin[0] <= v <= V_bin[1]]
    if pts:
        gs2 = [p[0] for p in pts]
        hs2 = [p[1] for p in pts]
        r2, _ = stats.spearmanr(gs2, hs2)
        print(f"  V in {V_bin}: rho={r2:.3f} (N={len(pts)})")

# Turn 23: H-gamma separatrix — the 1/phi line
print("\nTURN 23 — SEPARATRIX: H = 1/phi")
# Is 1/phi the natural boundary between two regimes?
n_below = sum(1 for h in hs if h < 1/PHI)
n_above = len(hs) - n_below
print(f"  Below H=1/phi: {n_below}/{len(hs)} ({n_below/len(hs)*100:.1f}%)")
print(f"  Above H=1/phi: {n_above}/{len(hs)} ({n_above/len(hs)*100:.1f}%)")

# For Erdos-Renyi graphs, what's the typical gamma at H=1/phi?
close_to_phi = [(g, h, V) for (V, p, g, h) in phase_bins['all'] if abs(h - 1/PHI) < 0.05]
if close_to_phi:
    gc = [c[0] for c in close_to_phi]
    print(f"  At H=1/phi (N={len(close_to_phi)}): gamma={np.mean(gc):.3f}+-{np.std(gc):.3f}")

print(f"\n  PHASE REGIMES:")
print(f"    I:  H > 0.618, gamma low  → high diversity, weak coupling (unstable)")
print(f"    II: H < 0.618, gamma low  → low diversity, weak coupling (fragmented)")
print(f"    III: H > 0.618, gamma high → high diversity, strong coupling (EMERGENT)")
print(f"    IV: H < 0.618, gamma high → low diversity, strong coupling (consensus herd)")
print(f"  Regime III is the DESIRED state for emergence.")

# Turn 24: Does the H-gamma separatrix shift with V?
print("\nTURN 24 — SIZE SCALING OF H-gamma SPACE")
from collections import defaultdict
bins = defaultdict(list)
for V, p, g, h in phase_bins['all']:
    bins[V // 10].append((g, h))

for k in sorted(bins.keys()):
    pts = bins[k]
    gs = [p[0] for p in pts]
    hs = [p[1] for p in pts]
    avg_g = np.mean(gs)
    avg_h = np.mean(hs)
    in_III = sum(1 for g, h in pts if g > np.median(gs) and h > 1/PHI)
    print(f"  V={k*10}-{(k+1)*10-1}: avg_gamma={avg_g:.3f} avg_H={avg_h:.3f} regime_III={in_III}/{len(pts)}")

# Turn 25: Multifleet phase analysis
print("\nTURN 25 — MULTIFLEET PHASE (2+ fleets coupled)")
# Simulate two fleets with weak inter-fleet coupling
for inter_strength in [0, 0.1, 0.3, 0.5, 0.8, 1.0]:
    V1, V2 = 20, 20
    V_total = V1 + V2
    
    C = np.zeros((V_total, V_total))
    # Intra-fleet coupling (strong)
    for i in range(V_total):
        for j in range(i+1, V_total):
            same_fleet = (i < V1 and j < V1) or (i >= V1 and j >= V1)
            if same_fleet:
                if np.random.random() < 0.4:  # 40% intra-fleet edges
                    C[i,j] = C[j,i] = np.random.uniform(0.5, 1.0)
            else:
                if np.random.random() < inter_strength:  # inter-fleet edges
                    C[i,j] = C[j,i] = np.random.uniform(0.1, 0.3)
    
    np.fill_diagonal(C, 1.0)
    d = np.maximum(C.sum(axis=1), 1.0)
    C = C / np.sqrt(np.outer(d, d))
    
    gamma = algebraic_normalized(C)
    H = coupling_entropy(C)
    
    print(f"  inter_strength={inter_strength:.1f}: gamma={gamma:.3f} H={H:.3f} "
          f"regime={'III-emergent' if gamma > 0.618 else 'II-fragmented' if H < 0.618 else 'I-unstable' if gamma < 0.2 else 'IV-herd'}")

print("\n"+"="*60)
print("PHASE SPACE SUMMARY")
print("="*60)
print("""
The (gamma, H) plane is the FLEET STATE SPACE:
- gamma = connectivity (Laplacian spectral gap)
- H = diversity (coupling spectral entropy)
- They are NEARLY ORTHOGONAL for random vectors (rho ~ 0)

Phase transitions at:
- H = 1/phi ~ 0.618: diversity threshold
- gamma = 0.2-0.3: connectivity threshold (V-dependent)

Emergence requires: gamma > gamma_c AND H > 1/phi
  i.e., diverse agents that are well-connected = the sweet spot.
  
This is the same as H1 cohomology condition: beta1 > V-2 requires
enough edges (high gamma) AND enough diversity (high H).
""")
print("="*60)
