# EXPERIMENT-01: H¹ Emergence Detection Validation

## Claim Under Test

**H¹ Emergence Detection:** In a fleet graph with V vertices, E edges, and C connected components, the first Betti number β₁ = E - V + C predicts consensus difficulty. Specifically:
- β₁ = 0 (tree): Consensus always succeeds
- β₁ = 1 (single cycle): Consensus succeeds if edge weights consistent
- β₁ > V - 2 (over-constrained): Consensus may fail or be delayed
- β₁ >> V - 2: Emergence detected (system has redundant constraint paths)

**Null Hypothesis (H₀):** β₁ does NOT predict consensus difficulty in multi-agent beam debates.
**Alternative Hypothesis (H₁):** β₁ > V - 2 correlates with consensus failure or delayed convergence.

**Note:** The claim "100% accuracy, 2.7s early warning" has NOT been validated. This experiment will measure actual accuracy and detection latency.

---

## Experimental Design

### 1. Synthetic Scenario Generator

Create fleet graphs with controlled β₁ values:

| Case | Graph Type | V | E | β₁ | Expected Behavior |
|------|-----------|---|---|---|------------------|
| A | Tree (path) | 5 | 4 | 0 | Always converge |
| B | Single cycle (ring) | 5 | 5 | 1 | Converge if weights consistent |
| C | Two cycles sharing edge | 5 | 6 | 2 | May have conflicts |
| D | Laman-rigid (β₁ = V-2) | 5 | 7 | 3 | Exactly rigid, no excess |
| E | Over-constrained | 5 | 9 | 5 | Excess edges → emergence |

### 2. Simulation: Multi-Agent Beam Debate

Use the existing spring-damper model from `spline-physics/src/multi_agent/`:

```rust
// Agent update rule (Hooke's law)
b_i^{(k+1)} = b_i^{(k)} + Σⱼ wᵢⱼ × k × (b_j^{(k)} - b_i^{(k)}) - c × Δb_i^{(k)}
```

- Same beam parameters (E=200GPa, I=1e-6 m⁴, span=1m, distributed load)
- Same initial conditions (beliefs start at ground truth ±5% random perturbation)
- Same trust topology weights (uniform w=1.0 for control)
- **Only vary:** graph structure → β₁

### 3. Measurement Metrics

For each trial, record:
- `consensus_reached`: bool (true if agreement > 92% within 50 rounds)
- `rounds_to_consensus`: usize (wall-clock rounds)
- `final_agreement`: f64 (agreement index at termination)
- `distance_from_ground_truth`: f64 (max displacement at consensus)
- `|∇E| at termination`: f64 (force residual)

### 4. Hypothesis Testing

```r
# Statistical test: Does β₁ predict consensus failure?
# Use logistic regression: P(failure) ~ β₁
model <- glm(failure ~ beta_1, data=trials, family=binomial)
summary(model)  # p-value for β₁ coefficient

# Also: Kruskal-Wallis test (non-parametric)
kruskal.test(rounds ~ case, data=trials)
```

---

## Test Cases

### Case A: Tree Graph (β₁=0)
```
V = 5, edges = [(0,1), (1,2), (2,3), (3,4)]
β₁ = 4 - 5 + 1 = 0
```
**Hypothesis:** 100% consensus success, rounds ~ O(log V)

### Case B: Single Cycle (β₁=1)
```
V = 5, edges = [(0,1), (1,2), (2,3), (3,4), (4,0)]
β₁ = 5 - 5 + 1 = 1
```
**Hypothesis:** Consensus succeeds if edge weights consistent. May slow near boundaries.

### Case C: Two Cycles Sharing Edge (β₁=2)
```
V = 5, edges = [(0,1), (1,2), (2,0), (2,3), (3,4), (4,2)]
β₁ = 6 - 5 + 1 = 2
```
**Hypothesis:** Multiple cycles create competing constraint paths. May need more rounds.

### Case D: Laman-Rigid (β₁ = V-2)
```
V = 5, E = 2V - 3 = 7, edges = [(0,1), (1,2), (2,3), (3,4), (4,0), (0,2), (2,4)]
β₁ = 7 - 5 + 1 = 3 = V - 2
```
**Hypothesis:** Exactly rigid, no redundancy. Consensus succeeds but at boundary.

### Case E: Over-Constrained (β₁ > V-2)
```
V = 5, E = 9 (complete graph K5 minus one edge)
β₁ = 9 - 5 + 1 = 5 > 3 (V-2)
```
**Hypothesis:** Redundant edges create over-constraint. Consensus may fail or oscillate.

---

## Statistical Design

### Sample Size
- 100 trials per case (500 total)
- α = 0.05 (significance level)
- Power = 0.80 (detect effect size d = 0.3)
- Effect size: smallest practically significant difference in rounds

### Analysis Plan
1. **Descriptive:** Mean ± SD for each metric per case
2. **Primary:** Logistic regression for consensus failure ~ β₁
3. **Secondary:** ANOVA / Kruskal-Wallis for rounds across cases
4. **Post-hoc:** Pairwise comparisons with Bonferroni correction

### Success Criteria
- Primary: p-value < 0.05 for β₁ coefficient in logistic regression
- Secondary: Effect size (Cohen's d) > 0.3 for Case E vs Case A
- F1 score for β₁ > V-2 predicting consensus failure: > 0.80

---

## Implementation

### Files
- `src/validation/h1_emergence.rs` — experiment runner
- `src/validation/mod.rs` — module declarations
- `scripts/analyze_h1_results.R` — statistical analysis

### Key Functions

```rust
/// Generate a Laman-rigid graph: E = 2V - 3 edges
pub fn generate_laman_graph(v: usize) -> Vec<(u64, u64)> { ... }

/// Generate an over-constrained graph: E > 2V - 3
pub fn generate_overconstrained_graph(v: usize, excess: usize) -> Vec<(u64, u64)> { ... }

/// Run multi-agent debate and return consensus metrics
pub fn run_debate(edges: &[(u64, u64)], trials: usize) -> DebateResult { ... }

/// Compute β₁ = E - V + C
pub fn compute_beta(edges: &[(u64, u64)], V: usize) -> usize { ... }

/// Main experiment: validate emergence hypothesis
pub fn validate_emergence_hypothesis() { ... }
```

---

## Expected Results

| Case | β₁ | Expected Consensus Rate | Expected Rounds |
|------|----|----------------------|-----------------|
| A | 0 | 100% | ~5-10 |
| B | 1 | 95% | ~10-20 |
| C | 2 | 85% | ~15-30 |
| D | V-2 | 80% | ~20-40 |
| E | >V-2 | 50-70% | >50 or fail |

**Important:** These are hypotheses, not facts. The experiment will tell us.

---

## Honest Caveats

1. **The "100% accuracy" claim is unvalidated.** This experiment measures actual accuracy.
2. **The "2.7s early warning" has not been measured.** We will measure detection latency.
3. **The beam physics simulation is a proxy for real fleet consensus.** Real multi-agent systems have different dynamics.
4. **Edge weights are uniform in this experiment.** Real trust topologies have heterogeneous weights.
5. **The spring-damper model is a simplified belief dynamics.** Real agents may have more complex update rules.

This experiment provides the first empirical measurement of the H¹ emergence claim. It is not a proof.