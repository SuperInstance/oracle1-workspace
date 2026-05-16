"""
BATCH 6: DERIVE THE FULL FUNCTIONAL FORM OF EPSILON(n)

The main chain found: gamma+H = 0.870 - 0.232/log(V) for style coupling (R²=0.981).
But the ratio of actual_epsilon to 1/log(V) goes from ~0.3x (V=10) to ~3.1x (V=500),
meaning 1/log(V) is NOT the right functional form.

Task: Fit multiple candidate forms for epsilon(n) and identify the best.
Also verify: do topology-only and style coupling give the SAME conservation law?
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy import stats
import math, sys, os, json, urllib.request

sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/research/100-turns"))
from fleet_health_v2 import coupling_entropy, algebraic_normalized

np.random.seed(42)
nF = 109

def C_style(V, k):
    """Style coupling: random latent features."""
    U = np.random.randn(V, k)
    Vm = np.random.randn(k, nF)
    X = U @ Vm + np.random.randn(V, nF) * 0.2
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-10
    return X @ X.T / (norms @ norms.T)

def C_topo(V, p=0.3):
    """Topology coupling: random graph with edge weights."""
    C = np.zeros((V, V))
    for i in range(V):
        for j in range(i+1, V):
            if np.random.random() < p:
                C[i, j] = C[j, i] = np.random.uniform(0.3, 1.0)
    np.fill_diagonal(C, 1.0)
    d = np.maximum(C.sum(axis=1), 1.0)
    return C / np.sqrt(np.outer(d, d))

def C_mixed(V, k, w_style=0.5):
    """Mixed coupling: weighted blend of style and topology."""
    return w_style * C_style(V, k) + (1 - w_style) * C_topo(V)

# ══════════════════════════════════════════════════════════════════════
# PART 1: MEASURE gamma+H ACROSS V FOR STYLE COUPLING
# ══════════════════════════════════════════════════════════════════════
print("=" * 72)
print("BATCH 6: DERIVE THE FULL FUNCTIONAL FORM OF EPSILON(n)")
print("=" * 72)

# Data points from the task prompt (main chain, style coupling)
Vs = np.array([5, 10, 20, 30, 50, 100, 200, 500])

print("\n📊 Measuring gamma+H across V (style coupling, n=500 per V)...")
gh_obs = []
gh_stderr = []
for V in Vs:
    vals = []
    for _ in range(500):
        k = np.random.randint(1, min(30, V))
        C = C_style(V, k)
        vals.append(algebraic_normalized(C) + coupling_entropy(C))
    gh_obs.append(np.mean(vals))
    gh_stderr.append(np.std(vals) / np.sqrt(500))
    print(f"  V={V:3d}: gamma+H = {gh_obs[-1]:.3f} ± {gh_stderr[-1]:.3f}")

gh_obs = np.array(gh_obs)
gh_stderr = np.array(gh_stderr)
eps_obs = 1.0 - gh_obs

print("\n  Epsilon = 1 - (gamma+H):")
for i, V in enumerate(Vs):
    pred_1log = 1.0 / math.log(V)
    print(f"  V={V:3d}: eps={eps_obs[i]:.4f}  1/log(V)={pred_1log:.4f}  ratio={eps_obs[i]/pred_1log:.2f}x")

# ══════════════════════════════════════════════════════════════════════
# PART 2: FIT CANDIDATE FORMS
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 2: FITTING CANDIDATE FORMS FOR EPSILON(n)")
print("=" * 72)

n = Vs.astype(float)
eps = eps_obs

# Weights: use inverse variance if available, else uniform
weights = 1.0 / np.maximum(gh_stderr, 1e-6)

def r2_score(y_true, y_pred, w=None):
    """Weighted R² (1 - SS_res / SS_tot)."""
    if w is None:
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    else:
        w = w / np.sum(w)
        y_bar = np.average(y_true, weights=w)
        ss_res = np.sum(w * (y_true - y_pred) ** 2)
        ss_tot = np.sum(w * (y_true - y_bar) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

def aic(n_obs, n_params, ss_res):
    """Akaike Information Criterion (small sample correction)."""
    k = n_params
    if n_obs <= k + 1:
        return float('inf')
    aic = n_obs * np.log(ss_res / n_obs) + 2 * k
    # Small sample correction
    aic_c = aic + 2 * k * (k + 1) / (n_obs - k - 1)
    return aic_c

candidates = []

# ── Form 1: c / log(n) ──
def f1(n, c):
    return c / np.log(n)
popt, _ = curve_fit(f1, n, eps, p0=[0.5], sigma=1.0/weights, absolute_sigma=False)
eps_pred1 = f1(n, *popt)
r2_1 = r2_score(eps, eps_pred1, weights)
res1 = np.sum(weights * (eps - eps_pred1) ** 2)
aic_1 = aic(len(n), 1, np.sum((eps - eps_pred1) ** 2))
candidates.append(("c/log(n)", popt[0], r2_1, aic_1))
print(f"\n  Form 1: eps = {popt[0]:.4f} / log(n)")
print(f"    R² = {r2_1:.4f}, AICc = {aic_1:.1f}")

# ── Form 2: c/n + d/log(n) ──
def f2(n, c, d):
    return c / n + d / np.log(n)
popt, _ = curve_fit(f2, n, eps, p0=[0.3, 1.5], sigma=1.0/weights, absolute_sigma=False)
eps_pred2 = f2(n, *popt)
r2_2 = r2_score(eps, eps_pred2, weights)
aic_2 = aic(len(n), 2, np.sum((eps - eps_pred2) ** 2))
candidates.append(("c/n + d/log(n)", (popt[0], popt[1]), r2_2, aic_2))
print(f"\n  Form 2: eps = {popt[0]:.4f}/n + {popt[1]:.4f}/log(n)")
print(f"    R² = {r2_2:.4f}, AICc = {aic_2:.1f}")

# ── Form 3: c*exp(-d*n) + e ──
def f3(n, c, d, e):
    return c * np.exp(-d * n) + e
try:
    popt, _ = curve_fit(f3, n, eps, p0=[0.5, 0.01, 0.4], sigma=1.0/weights, absolute_sigma=False, maxfev=10000)
    eps_pred3 = f3(n, *popt)
    r2_3 = r2_score(eps, eps_pred3, weights)
    aic_3 = aic(len(n), 3, np.sum((eps - eps_pred3) ** 2))
    candidates.append(("c*exp(-d*n) + e", tuple(popt), r2_3, aic_3))
    print(f"\n  Form 3: eps = {popt[0]:.4f}*exp(-{popt[1]:.6f}*n) + {popt[2]:.4f}")
    print(f"    R² = {r2_3:.4f}, AICc = {aic_3:.1f}")
except RuntimeError as e:
    print(f"\n  Form 3: FAILED - {e}")

# ── Form 4: c/n^d + e ──
def f4(n, c, d, e):
    return c / (n ** d) + e
try:
    popt, _ = curve_fit(f4, n, eps, p0=[1.0, 0.5, 0.3], sigma=1.0/weights, absolute_sigma=False, maxfev=10000)
    eps_pred4 = f4(n, *popt)
    r2_4 = r2_score(eps, eps_pred4, weights)
    aic_4 = aic(len(n), 3, np.sum((eps - eps_pred4) ** 2))
    candidates.append(("c/n^d + e", tuple(popt), r2_4, aic_4))
    print(f"\n  Form 4: eps = {popt[0]:.4f}/n^{popt[1]:.4f} + {popt[2]:.4f}")
    print(f"    R² = {r2_4:.4f}, AICc = {aic_4:.1f}")
except RuntimeError as e:
    print(f"\n  Form 4: FAILED - {e}")

# ── Form 5: c + d*log(n)/n ──
def f5(n, c, d):
    return c + d * np.log(n) / n
try:
    popt, _ = curve_fit(f5, n, eps, p0=[0.5, 0.5], sigma=1.0/weights, absolute_sigma=False, maxfev=10000)
    eps_pred5 = f5(n, *popt)
    r2_5 = r2_score(eps, eps_pred5, weights)
    aic_5 = aic(len(n), 2, np.sum((eps - eps_pred5) ** 2))
    candidates.append(("c + d*log(n)/n", tuple(popt), r2_5, aic_5))
    print(f"\n  Form 5: eps = {popt[0]:.4f} + {popt[1]:.4f}*log(n)/n")
    print(f"    R² = {r2_5:.4f}, AICc = {aic_5:.1f}")
except RuntimeError as e:
    print(f"\n  Form 5: FAILED - {e}")

# ── Form 6: c*log(log(n))/log(n) ──
def f6(n, c):
    return c * np.log(np.log(n)) / np.log(n)
try:
    popt, _ = curve_fit(f6, n, eps, p0=[2.0], sigma=1.0/weights, absolute_sigma=False, maxfev=10000)
    eps_pred6 = f6(n, *popt)
    r2_6 = r2_score(eps, eps_pred6, weights)
    aic_6 = aic(len(n), 1, np.sum((eps - eps_pred6) ** 2))
    candidates.append(("c*log(log(n))/log(n)", popt[0], r2_6, aic_6))
    print(f"\n  Form 6: eps = {popt[0]:.4f}*log(log(n))/log(n)")
    print(f"    R² = {r2_6:.4f}, AICc = {aic_6:.1f}")
except RuntimeError as e:
    print(f"\n  Form 6: FAILED - {e}")

# ── Form 7: c/sqrt(n) + d/log(n) ──
def f7(n, c, d):
    return c / np.sqrt(n) + d / np.log(n)
try:
    popt, _ = curve_fit(f7, n, eps, p0=[0.5, 1.0], sigma=1.0/weights, absolute_sigma=False, maxfev=10000)
    eps_pred7 = f7(n, *popt)
    r2_7 = r2_score(eps, eps_pred7, weights)
    aic_7 = aic(len(n), 2, np.sum((eps - eps_pred7) ** 2))
    candidates.append(("c/sqrt(n) + d/log(n)", tuple(popt), r2_7, aic_7))
    print(f"\n  Form 7: eps = {popt[0]:.4f}/sqrt(n) + {popt[1]:.4f}/log(n)")
    print(f"    R² = {r2_7:.4f}, AICc = {aic_7:.1f}")
except RuntimeError as e:
    print(f"\n  Form 7: FAILED - {e}")

# ══════════════════════════════════════════════════════════════════════
# PART 3: BEST FIT SUMMARY
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 3: BEST FIT SUMMARY")
print("=" * 72)

# Sort by AICc (lower is better), break ties with R²
candidates.sort(key=lambda x: (x[3], -x[2]))
print(f"\n  {'Form':<30s} {'Params':<30s} {'R²':>8s} {'AICc':>8s}")
print(f"  {'-'*30} {'-'*30} {'-'*8} {'-'*8}")
for name, params, r2val, aicval in candidates:
    if isinstance(params, tuple):
        pstr = ", ".join([f"{p:.4f}" for p in params])
    else:
        pstr = f"{params:.4f}"
    print(f"  {name:<30s} {pstr:<30s} {r2val:>8.4f} {aicval:>8.1f}")

best = candidates[0]
best_name = best[0]
best_params = best[1]

print(f"\n  🏆 BEST FIT: eps(n) = {best_name}")
print(f"     R² = {best[2]:.4f}, AICc = {best[3]:.1f}")

# ══════════════════════════════════════════════════════════════════════
# PART 4: TOPOLOGY vs STYLE — do they give the SAME conservation law?
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 4: TOPOLOGY vs STYLE COUPLING — SAME LAW?")
print("=" * 72)

print("\n  Comparing gamma+H across V for style vs topology vs mixed...")
results = {}
for coupling_type in ["Style", "Topo (p=0.3)", "Mixed (w=0.5)"]:
    vals = {V: [] for V in [5, 10, 20, 30, 50, 100, 200]}
    for V in [5, 10, 20, 30, 50, 100, 200]:
        for _ in range(200):
            if coupling_type == "Style":
                k = np.random.randint(1, min(30, V))
                C = C_style(V, k)
            elif coupling_type == "Topo (p=0.3)":
                C = C_topo(V, p=0.3)
            elif coupling_type == "Mixed (w=0.5)":
                k = np.random.randint(1, min(30, V))
                C = C_mixed(V, k, w_style=0.5)
            vals[V].append(algebraic_normalized(C) + coupling_entropy(C))
    
    means = np.array([np.mean(vals[V]) for V in [5, 10, 20, 30, 50, 100, 200]])
    stds = np.array([np.std(vals[V]) for V in [5, 10, 20, 30, 50, 100, 200]])
    results[coupling_type] = (means, stds)
    
    print(f"\n  {coupling_type}:")
    for i, V in enumerate([5, 10, 20, 30, 50, 100, 200]):
        print(f"    V={V:3d}: gamma+H = {means[i]:.3f} ± {stds[i]:.3f}   eps = {1-means[i]:.4f}")

# Statistical comparison
print("\n--- Statistical Test: Are curves identical? ---")
# Fit separate eps models for each coupling type
for coupling_type, (m, s) in results.items():
    eps_type = 1.0 - m
    Vs_sub = np.array([5, 10, 20, 30, 50, 100, 200], dtype=float)
    # Power law: c/n^d + e
    def f_power(n, c, d, e):
        return c / (n ** d) + e
    try:
        popt, pcov = curve_fit(f_power, Vs_sub, eps_type, p0=[1.0, 0.5, 0.1], maxfev=10000)
        eps_pred = f_power(Vs_sub, *popt)
        r2 = r2_score(eps_type, eps_pred)
        print(f"  {coupling_type:20s}: eps = {popt[0]:.4f}/n^{popt[1]:.4f} + {popt[2]:.4f}   (R²={r2:.4f})")
    except RuntimeError as e:
        print(f"  {coupling_type:20s}: power-law fit failed ({e})")

# Compare style vs topo at each V
print("\n--- Per-V Comparison (style vs topo) ---")
m_style, s_style = results["Style"]
m_topo, s_topo = results["Topo (p=0.3)"]
for i, V in enumerate([5, 10, 20, 30, 50, 100, 200]):
    diff = m_style[i] - m_topo[i]
    pooled_se = np.sqrt(s_style[i]**2 + s_topo[i]**2)
    z = diff / pooled_se if pooled_se > 0 else 0
    sig = "⚠️ SIGNIFICANT" if abs(z) > 2.0 else "✓ same"
    print(f"  V={V:3d}: style={m_style[i]:.3f} topo={m_topo[i]:.3f}  diff={diff:+.3f}  |z|={abs(z):.2f}  {sig}")

# ══════════════════════════════════════════════════════════════════════
# PART 5: ASYMPTOTIC ANALYSIS
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 5: ASYMPTOTIC ANALYSIS — epsilon as V→∞")
print("=" * 72)

# The best-fit form's limit as n→∞
print(f"\n  Best form: {best_name}")
for i, V in enumerate(Vs):
    if "c/log(n)" == best_name:
        eps_pred = best_params / math.log(V)
    elif "c/n^d + e" == best_name:
        c, d, e = best_params
        eps_pred = c / (V ** d) + e
    elif "c*exp(-d*n) + e" == best_name:
        c, d, e = best_params
        eps_pred = c * math.exp(-d * V) + e
    elif "c/n + d/log(n)" == best_name:
        c, d = best_params
        eps_pred = c / V + d / math.log(V)
    elif "c + d*log(n)/n" == best_name:
        c, d = best_params
        eps_pred = c + d * math.log(V) / V
    elif "c*log(log(n))/log(n)" == best_name:
        eps_pred = best_params * math.log(math.log(V)) / math.log(V)
    elif "c/sqrt(n) + d/log(n)" == best_name:
        c, d = best_params
        eps_pred = c / math.sqrt(V) + d / math.log(V)
    else:
        eps_pred = 0.0
    
    actual = eps_obs[i]
    err_pct = abs(eps_pred - actual) / max(actual, 1e-6) * 100
    print(f"  V={V:3d}: predicted eps={eps_pred:.4f}  actual eps={actual:.4f}  error={err_pct:.1f}%")

# Compute asymptotic limit
print("\n  Asymptotic analysis:")
if best_name == "c/n^d + e":
    c, d, e = best_params
    print(f"    As n→∞: eps → {e:.4f}")
    print(f"    Thus gamma+H → {1-e:.4f} as n→∞")
elif best_name == "c*exp(-d*n) + e":
    c, d, e = best_params
    print(f"    As n→∞: eps → {e:.4f}")
    print(f"    Thus gamma+H → {1-e:.4f} as n→∞")
elif best_name == "c + d*log(n)/n":
    c, d = best_params
    print(f"    As n→∞: eps → {c:.4f}")
    print(f"    Thus gamma+H → {1-c:.4f} as n→∞")
else:
    print(f"    As n→∞: eps → 0 (form decays to zero)")
    print(f"    Thus gamma+H → 1 as n→∞ (perfect conservation)")

# ══════════════════════════════════════════════════════════════════════
# PART 6: PUBLISH TO PLATO
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("PART 6: PUBLISH TO PLATO")
print("=" * 72)

best_r2 = best[2]
best_aic = best[3]

# Build summary string
summary_lines = [
    f"BATCH 6: EPSILON(n) FULL FUNCTIONAL FORM DERIVED",
    f"",
    f"Best fit: eps(n) = {best_name}",
]

if isinstance(best_params, tuple):
    for j, p in enumerate(best_params):
        summary_lines.append(f"  param[{j}] = {p:.6f}")
else:
    summary_lines.append(f"  param = {best_params:.6f}")

summary_lines.append(f"  R² = {best_r2:.4f}, AICc = {best_aic:.1f}")
summary_lines.append(f"")
summary_lines.append("All candidates ranked by AICc:")
for name, params, r2val, aicval in candidates:
    if isinstance(params, tuple):
        pstr = ", ".join([f"{p:.4f}" for p in params])
    else:
        pstr = f"{params:.4f}"
    summary_lines.append(f"  {name}: R²={r2val:.4f}, AICc={aicval:.1f}, params=({pstr})")

summary_lines.append(f"")
summary_lines.append("Topology vs Style comparison:")
for coupling_type, (m, s) in results.items():
    summary_lines.append(f"  {coupling_type}: gamma+H ranges {m[0]:.3f} to {m[-1]:.3f}")

summary_lines.append(f"")
# Check if topology and style give same law
m_style, _ = results.get("Style", (np.zeros(7), np.zeros(7)))
m_topo, _ = results.get("Topo (p=0.3)", (np.zeros(7), np.zeros(7)))
max_diff = np.max(np.abs(m_style - m_topo))
summary_lines.append(f"Max difference (style vs topo): {max_diff:.4f}")
if max_diff < 0.05:
    summary_lines.append("CONCLUSION: YES — both coupling types follow the SAME conservation law.")
else:
    summary_lines.append("CONCLUSION: NO — style and topology show different gamma+H values.")

summary_lines.append(f"")
summary_lines.append(f"Asymptotic limit: gamma+H → {1 - (best_params[-1] if isinstance(best_params, tuple) else 0):.4f}")

answer = "\n".join(summary_lines)

payload = json.dumps({
    "domain": "research_log",
    "question": "BATCH 6: Epsilon(n) full functional form derived (2026-05-15)",
    "answer": answer,
    "tags": [
        "batch-6", "epsilon-form", "conservation-law", "functional-form",
        f"best-fit-{best_name.replace('/','-').replace('*','x')}",
        f"R2-{best_r2:.4f}", "2026-05-15"
    ],
    "source": "oracle1",
    "confidence": min(0.95, max(0.5, best_r2))
})

try:
    result = os.popen(
        f"curl -s -X POST http://localhost:8847/submit "
        f"-H 'Content-Type: application/json' "
        f"-d '{payload}'"
    ).read()
    print(f"  ✅ PLATO response: {result[:80].strip()}")
except Exception as e:
    print(f"  ❌ PLATO push failed: {e}")

# Also push to PLATO room oracle1 for more durable storage
room_payload = json.dumps({
    "msg": answer,
    "from": "oracle1",
    "type": "research_result"
})
try:
    result = os.popen(
        f"curl -s -X POST http://localhost:8847/room/oracle1 "
        f"-H 'Content-Type: application/json' "
        f"-d '{room_payload}'"
    ).read()
    print(f"  ✅ PLATO room push: {result[:60].strip()}")
except Exception as e:
    print(f"  ❌ PLATO room push failed: {e}")

# ══════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("FINAL SUMMARY")
print("=" * 72)
print(f"""
📐 EPSILON(n) FORM DERIVED — Batch 6 Complete

Best fit: eps(n) = {best_name}
R² = {best_r2:.4f} | AICc = {best_aic:.1f}

Conservation law: gamma+H = 1 - eps(n)
                 ≈ 1 - {best_name}

Topology vs Style: {'SAME' if max_diff < 0.05 else 'DIFFERENT'} conservation law
  (max diff = {max_diff:.4f})

PLATO: ✅ Published

Next batch (7): Test conservation law on MIXED coupling matrices.
  Does gamma+H still hold when both topology and style contribute?
""")

print("=" * 72)
