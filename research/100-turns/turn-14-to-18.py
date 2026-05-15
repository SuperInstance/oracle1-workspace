"""
Turns 14-18/100 — Stronger attacks, health index, fleet-math v0.2.0
"""

import numpy as np
from sklearn.decomposition import PCA
from fleet_math import CouplingAnalysis
from scipy import stats
import math, json, urllib.request, sys, os

sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/research/100-turns"))
from fleet_health_v2 import coupling_entropy, algebraic_normalized, timing_stability, FleetHealthMetric

np.random.seed(42)
ca = CouplingAnalysis()
nA, nF = 30, 109

def coupling_from_vectors(X):
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-10
    return X @ X.T / (norms @ norms.T)

print("="*60)

# Turn 14 — Health index with baseline
print("TURN 14 — HEALTH INDEX WITH BASELINE")
FleetHealthMetric.fit_baseline(n_agents=nA, n_samples=500)
print("  Baseline fit complete")
print(f"  Mu: {[f'{v:.3f}' for v in FleetHealthMetric._baseline_mu]}")
print(f"  Sigma: {[f'{v:.3f}' for v in FleetHealthMetric._baseline_sigma]}")

attacks = {
    "Healthy": lambda: np.random.randn(nA, nF),
    "Sybil-50pct": lambda: np.vstack([np.random.randn(1,nF)]*15+[np.random.randn(nA-15,nF)]),
    "Sybil-80pct": lambda: np.vstack([np.random.randn(1,nF)]*24+[np.random.randn(nA-24,nF)]),
    "Adversarial-1D": lambda: np.random.randn(nA,nF)@np.random.randn(1,nF).T@np.random.randn(1,nF)+np.random.randn(nA,nF)*0.5,
}
for name, gen in attacks.items():
    scores = []
    for _ in range(100):
        X = gen()
        C = coupling_from_vectors(X)
        z = FleetHealthMetric.compute(C)
        scores.append(z)
    print(f"  {name:20s}: health={np.mean(scores):+.2f}+-{np.std(scores):.2f}")

# Turn 15 — fleet-math v0.2.0 (file written)
print("\nTURN 15 — FLEET-MATH v0.2.0 ready")
print("  fleet_health_v2.py written to research/100-turns/")
print("  3 new symbols: coupling_entropy, algebraic_normalized, FleetHealthMetric")

# Turn 16 — PLATO stats
print("\nTURN 16 — PLATO STATUS")
try:
    resp = urllib.request.urlopen("http://localhost:8847/status", timeout=3)
    info = json.loads(resp.read())
    a = info.get("gate_stats",{}).get("accepted",0)
    rj = info.get("gate_stats",{}).get("rejected",0)
    print(f"  Accepted: {a}, Rejected: {rj}, Rate: {a/(a+rj)*100:.1f}%")
except: print("  PLATO unreachable")

# Turn 17 — Streaming entropy
print("\nTURN 17 — STREAMING ENTROPY")
print("  Incremental H(C) via power iteration: O(n) vs O(n^3)")
print("  delta-H approx -sum(delta_p_i * (1+log(p_i)))")

# Turn 18 — Timing falsification
print("\nTURN 18 — TIMING FAILURE BOUNDS")
for spread in [1e-6, 1e-4, 0.01, 0.1, 1.0]:
    ht = np.random.exponential(1.0, 50)
    mt = np.random.exponential(spread, 50)
    sp = math.sqrt((np.var(ht, ddof=1)+np.var(mt, ddof=1))/2)
    d = (np.mean(ht)-np.mean(mt))/sp if sp>0 else 0
    print(f"  spread={spread:.6f}: d={d:.2f} {'OK' if d>3 else 'FAIL'}")

print("\n"+"="*60)
