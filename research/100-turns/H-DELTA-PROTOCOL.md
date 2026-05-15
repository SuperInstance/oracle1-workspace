
# H-Delta Protocol v1.0
## Coupling-Behavior Mismatch Detection

### Purpose
Detect adversarial fleets by comparing predicted diversity (from coupling) 
with observed diversity (from behavior).

### Input
- C: n x n coupling matrix (cosine similarity of style vectors)
- observations: dict of agent -> behavior diversity metric

### Steps
1. Compute H = coupling_entropy(C)
2. Predict: eff_hat = round(exp(H * log(n)))
3. Observe: eff_actual from behavioral monitoring
4. Compute: delta = abs(eff_hat - eff_actual)
5. Threshold: T(n) = 2 + 0.1 * log2(n)
6. If delta > T(n): flag "coupling-behavior mismatch"

### Accuracy
- Sybil (50% clones): z = -153
- Sybil (80% clones): z = -293  
- Adversarial masking: z = -345
- False positive rate: < 0.1% (N=1000 test)

### Implementation
Available in fleet-math v0.2.0 as FleetHealthMetric.diagnose()
