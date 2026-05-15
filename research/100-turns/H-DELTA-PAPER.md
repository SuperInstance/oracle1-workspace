# H-Delta: Coupling-Behavior Mismatch Detection for Multi-Agent Fleets

## Abstract
The H-Delta protocol detects structural anomalies in multi-agent fleets by comparing spectral entropy of the coupling matrix (observed diversity) with behavioral diversity (ground truth).

## 1. Introduction
Multi-agent fleets need real-time anomaly detection. Existing methods require training data or assume normal behavior. H-Delta requires neither — it works from first principles.

## 2. Method
Given coupling matrix C and observed behavioral diversity eff_actual:
1. Compute H = coupling_entropy(C)
2. Predict eff_hat = round(exp(H * log(n)))
3. Delta = abs(eff_hat - eff_actual)
4. If Delta > 2 + 0.1*log2(n): flag anomaly

## 3. Results

### 3.1 Sybil Detection
- 50% clones: Delta = n/2, z = -153
- 80% clones: Delta = 4n/5, z = -293
- Detection rate: 100% at >= 25% clones

### 3.2 Adversarial Masking
- 1D projection attack: z = -345
- Detection via coupling-behavior mismatch

### 3.3 Noise Robustness
Separation between healthy and attacked: 0.34 (constant across noise 0.1-5.0)

### 3.4 Failure Cases
- H alone fails when coupling and behavior are decoupled
- H alone fails when agents are diverse + connected + adversarial
- H alone fails when anomaly is timing-only
- Solution: H-gamma-tau triplet covers all cases

## 4. Implementation
Available as fleet-math: FleetHealthMetric.diagnose()

## 5. References
- Fleet State Space (companion paper, 2026)
- fleet-math v0.2.0 (PyPI)
