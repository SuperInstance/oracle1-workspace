
# H-Delta: coupling-behavior mismatch detection

import numpy as np

def compute_delta(C, eff_actual):
    """Compare predicted diversity from coupling vs observed."""
    n = C.shape[0]
    eigvals = np.linalg.eigvalsh(C)[::-1]
    p = np.abs(eigvals) / (np.sum(np.abs(eigvals)) + 1e-15)
    p = p[p > 1e-10]
    H = float(-np.sum(p * np.log(p)) / np.log(n))
    
    eff_pred = round(np.exp(H * np.log(n)))
    delta = abs(eff_pred - eff_actual)
    threshold = 2 + 0.1 * np.log2(n)
    
    return {
        "H": H,
        "eff_predicted": eff_pred,
        "eff_actual": eff_actual,
        "delta": delta,
        "threshold": threshold,
        "flagged": delta > threshold,
        "severity": "CRITICAL" if delta > 3 * threshold else \
                    "HIGH" if delta > 2 * threshold else \
                    "WARNING" if delta > threshold else "OK"
    }

# Example: detect sybil
if __name__ == "__main__":
    V = 30
    X = np.random.randn(V, 109)
    C = X @ X.T / (np.linalg.norm(X, axis=1, keepdims=True)**2 + 1e-10)
    
    # Healthy: eff matches
    r1 = compute_delta(C, eff_actual=20)
    print(f"Healthy: {r1}")
    
    # Sybil: predicted eff is very low, actual is high
    X_s = np.vstack([X[0]] * 20 + [np.random.randn(10, 109)])
    C_s = X_s @ X_s.T / (np.linalg.norm(X_s, axis=1, keepdims=True)**2 + 1e-10)
    r2 = compute_delta(C_s, eff_actual=25)
    print(f"Sybil: {r2}")
