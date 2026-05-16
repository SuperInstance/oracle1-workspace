# EXPERIMENT-02: Constraint Theory vs Machine Learning Comparison

## Claim Under Test

**127 Lines Replace 12K Lines of ML:** A constraint theory approach using 127 lines of pure mathematical reasoning outperforms or matches a 12,000-line ML model on the same task.

**Important:** This experiment has NOT been run. The claim cannot be made until it is.

---

## Task Selection

We evaluate three candidate tasks. **Option B (Consensus Achievement)** is recommended as primary because it maps directly to the ZHC role and has clear ground truth from the physics simulation.

### Option A: Anomaly Detection in Sensor Streams (H¹ role)
- **Task:** Detect emergent patterns in multi-agent sensor data
- **CT approach:** H¹ β₁ > V-2 as emergence detector
- **ML baseline:** 1D-CNN trained on sensor sequences
- **Dataset:** [To be identified — possibly NASA turbofan bearing data]
- **Ground truth:** Known anomaly labels
- **Difficulty:** Medium (requires dataset procurement)

### Option B: Consensus Achievement in Multi-Agent System (ZHC role) ⭐ RECOMMENDED
- **Task:** Predict whether a multi-agent debate will reach consensus
- **CT approach:** ZHC closure check (sum of edge weights around cycles = 0 in Pythagorean48)
- **ML baseline:** Random forest on graph features (V, E, β₁, edge density, clustering coef)
- **Ground truth:** From EXP-01, we have actual consensus outcomes for known graph structures
- **Dataset:** Generated synthetically from the beam debate simulation
- **Difficulty:** Low (we generate the data, no procurement needed)
- **Advantage:** Directly tests the ZHC claim in a controlled setting

### Option C: Beam Shape Prediction (spline-physics role)
- **Task:** Predict equilibrium beam shape given pin forces
- **CT approach:** Analytical Euler-elastica solution (127 lines)
- **ML baseline:** Feedforward neural network trained on (force → shape) pairs
- **Dataset:** Generated from existing spline-physics solver (known ground truth)
- **Difficulty:** Medium (requires clean dataset generation)

---

## Recommended Design: Option B (Consensus Achievement)

### Dataset Generation

Generate synthetic fleet graphs with known properties:

```python
import random

def generate_fleet_dataset(n_samples=1000):
    """
    Generate dataset of fleet graphs with consensus outcomes.
    Features: V, E, C, β₁, edge_density, avg_degree, clustering_coef
    Label: consensus_reached (bool), rounds_to_consensus (int)
    """
    samples = []
    for _ in range(n_samples):
        V = random.randint(3, 12)
        # Generate graph with controlled properties
        graph_type = random.choice(['tree', 'cycle', 'multicycle', 'laman', 'overconstrained'])
        edges = generate_graph_with_type(V, graph_type)
        
        # Run beam debate (from existing multi_agent module)
        result = run_beam_debate(edges, max_rounds=50)
        
        samples.append({
            'V': V,
            'E': len(edges),
            'C': count_components(edges, V),
            'beta_1': compute_beta_1(len(edges), V),
            'edge_density': 2 * len(edges) / (V * (V-1)),
            'avg_degree': 2 * len(edges) / V,
            'consensus_reached': result.reached,
            'rounds': result.rounds
        })
    return samples
```

### CT Approach (Constraint Theory)

```rust
/// ZHC Consensus Check — 127 lines of pure constraint theory
/// 
/// For each independent cycle in the trust graph:
/// Sum of edge weights (interpreted as vectors in Pythagorean48) must = identity.
/// If all cycles close (sum = 0), consensus is geometrically guaranteed.
/// 
/// This is NOT machine learning. It's a mathematical theorem:
/// Zero Holonomy Closure (ZHC) = geometric consistency condition.

pub fn zhc_check(edges: &[(u64, u64)], weights: &[f64]) -> ZHCCheckResult {
    // Compute cycle basis (basis of independent cycles)
    let cycles = cycle_basis(edges);
    
    // For each cycle, compute holonomy sum
    let mut cycle_results = Vec::new();
    for cycle in cycles {
        let holonomy = compute_holonomy_sum(&cycle, weights);
        cycle_results.push(HolonomyResult {
            cycle_length: cycle.len(),
            holonomy_magnitude: holonomy.magnitude(),
            closed: holonomy.is_near_identity(),
        });
    }
    
    // Consensus guaranteed if all cycles close
    let all_closed = cycle_results.iter().all(|r| r.closed);
    ZHCCheckResult {
        n_cycles: cycles.len(),
        all_cycles_closed: all_closed,
        max_holonomy: cycle_results.iter().map(|r| r.holonomy_magnitude).fold(0.0, f64::max),
        predicted_consensus: all_closed,
    }
}
```

### ML Baseline Approach

```python
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def train_ml_baseline(X_train, y_train, n_lines=12000):
    """
    Random Forest baseline for consensus prediction.
    Comparable to ~12K lines of ML infrastructure:
    - Data preprocessing: 500 lines
    - Feature engineering: 1000 lines
    - Model training loop: 800 lines
    - Hyperparameter tuning: 2000 lines
    - Evaluation metrics: 500 lines
    - Visualization: 1000 lines
    - Flask API server: 1500 lines
    - Data versioning (DVC): 800 lines
    - Experiment tracking (MLflow): 1200 lines
    - Kubernetes deployment configs: 2000 lines
    - Tests: 1500 lines
    Total: ~12,000 lines
    
    Model itself (the 127-line comparison):
    - Random Forest with 100 trees, max_depth=10
    - ~50 lines of actual model code
    """
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model
```

---

## Fair Comparison Criteria

### Hardware
- Same machine for both approaches
- CT: Rust binary, single-threaded benchmark
- ML: Python + scikit-learn, same machine

### Metrics

| Metric | CT Approach | ML Approach |
|--------|-------------|-------------|
| Accuracy | % correct consensus predictions | % correct consensus predictions |
| Latency | ms per prediction (single graph) | ms per prediction (single graph) |
| Code size | Actual line count (not marketing) | Actual line count |
| Robustness to noise | Accuracy with ±10% edge weight perturbation | Accuracy with same perturbation |
| Out-of-distribution | V=15, E=30 (unseen in training) | Same |
| Memory usage | MB | MB |

### Out-of-Distribution Test
- Train on V ∈ [3, 12]
- Test on V ∈ [15, 20] (unseen graph sizes)
- This tests generalization, not just fitting

---

## Statistical Analysis

```r
# Compare CT vs ML accuracy
ct_accuracy <- sum(ct_predictions == ground_truth) / n
ml_accuracy <- sum(ml_predictions == ground_truth) / n

# McNemar's test (paired comparison)
library(epitools)
mcnemar.test(ct_predictions, ml_predictions)

# Latency comparison (Wilcoxon signed-rank)
wilcox.test(ct_latency, ml_latency, paired=TRUE)

# Robustness: accuracy drop under noise
ct_robustness <- ct_accuracy_noise - ct_accuracy_clean
ml_robustness <- ml_accuracy_noise - ml_accuracy_clean
```

---

## Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| CT accuracy vs ML accuracy | CT ≥ ML - 5% (non-inferiority) |
| Latency | CT < ML (speed advantage) |
| OOD generalization | CT drop < ML drop |
| Code size | Document actual (not marketing) |

---

## Honest Caveats

1. **The 127-line claim is approximate.** The ZHC check implementation may be more or fewer than 127 lines depending on what's counted.
2. **The 12K-line ML claim needs verification.** We will count actual lines of ML infrastructure code.
3. **Synthetic data may not reflect real-world complexity.** The beam debate is a proxy, not the actual task.
4. **Task selection matters.** If we pick an easy task, both approaches may perform equally well.
5. **The comparison is not fully fair.** CT has domain knowledge built in (homological structure of graphs); ML must learn it.

This experiment provides the first controlled comparison between constraint theory and ML on the same task. It does not prove CT is universally superior.