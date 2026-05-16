# Experiment: Proof-Carrying Spectral Gap Falsification (H2)

## Hypothesis

**H2**: Embedding zero-knowledge proofs in fleet-jobs task tiles reduces the false-positive rate of spectral-gap completion detection from `O(ε·n·m)` to negligible. For a proof-anchored coupling matrix `W^π`, the spectral gap `γ̃^π` is identically `1.0` for any set of honest agents regardless of fleet size `n`.

---

## 1. The Coupling Matrices

### Standard Behavioral Coupling `W`

`W` is an `n × n` matrix where entry `W_{ij} ∈ [0,1]` represents the behavioral similarity between agents `i` and `j`, derived from observed task performance signals. In practice:

- Entries are estimated from noisy observations (completion times, output quality, resource usage)
- Noise grows with fleet size — more agents means more cross-talk, scheduling jitter, and measurement error
- Result: `γ̃` (the spectral gap of the normalized Laplacian) degrades as `n` increases

This is the **status quo** that H2 claims is broken.

### Proof-Anchored Coupling `W^π`

`W^π` is an `n × n` matrix where:

```
W^π_{ij} = 1  if agent j submitted a valid zero-knowledge proof of task completion
W^π_{ij} = 0  otherwise
```

Properties:
- **Boolean, not continuous** — no gradient, no noise floor
- **Agent-independent** — `W^π_{ij}` depends only on agent `j`, not on the pair `(i,j)`
- **Monotone under honesty** — an honest agent with a correct proof always produces a 1

For a fleet where every agent submits valid proofs:

```
W^π = J_n   (the all-ones matrix)
```

---

## 2. Spectral Gap Analysis

### Standard Coupling

For `W` with behavioral noise, the normalized Laplacian is:

```
L = I - D^{-1/2} W D^{-1/2}
```

where `D` is the degree matrix. The spectral gap `γ̃` is the smallest positive eigenvalue of `L`.

**Known behavior**: `γ̃ → 0` as `n → ∞` in the presence of noise. False positives occur when `γ̃ < τ` (threshold) even though all agents completed their tasks — the noise masks the signal.

### Proof-Anchored Coupling

For `W^π = J_n` (all agents honest):

- Degree matrix: `D = n·I` (each agent has degree n)
- Normalized Laplacian: `L^π = I - (1/√n) J_n (1/√n) = I - (1/n) J_n`
- Eigenvalues: `λ_1 = 0` (multiplicity 1, eigenvector = all-ones), `λ_2 = 1` (multiplicity n-1)
- **Spectral gap: `γ̃^π = 1.0`**, independent of `n`

**Key result**: The spectral gap is invariant with respect to fleet size. Adding more honest agents does not change `γ̃^π`.

For `W^π` with a mixture of honest and dishonest agents:

- Suppose `h` agents are honest (proof valid), `d = n-h` are dishonest (proof invalid)
- `W^π` has `h` columns of all-ones, `d` columns of all-zeros
- This is a rank-1 matrix with one non-zero singular value
- The spectral gap `γ̃^π` depends only on `h/n`, not on `n` itself

---

## 3. Falsifiable Predictions

### Prediction 1: Size-Independence

> For a fleet of `n` agents where all agents submit valid proofs, `γ̃^π = 1.0` for ANY `n ≥ 2`.

This contradicts the current behavior where `γ̃ → 0` as `n` grows.

### Prediction 2: Threshold Separation

> For any fleet size `n` and any noise level `σ` in the behavioral signal, there exists a threshold `τ > 0` such that `P(γ̃ < τ | all honest) >> P(γ̃^π < τ | all honest)`.

In words: false-positive probability is orders of magnitude lower for `W^π`.

### Prediction 3: Dishonest Detection

> For `W^π`, the spectral gap `γ̃^π` drops discontinuously when any single agent fails proof verification, regardless of fleet size.

For `W`, a single underperforming agent in a fleet of 64 is barely detectable (the behavioral noise swamps the signal). For `W^π`, one bad column drops the matrix rank, and `γ̃^π` changes by a step function.

---

## 4. Test Design

### Simulated Fleets

| Fleet | n | Description |
|-------|---|-------------|
| F4    | 4 | Small fleet, reference baseline |
| F16   | 16 | Medium fleet, current operational size |
| F64   | 64 | Large fleet, stress test |

### Simulation Procedure

For each fleet `n ∈ {4, 16, 64}`:

1. **Generate `W`** (standard behavioral coupling):
   - For each agent `j`, draw true task-completion signal `s_j ∈ {0.8, 1.0}` (1.0 = honest completion)
   - Add Gaussian noise: `w_{ij} = s_j + ε`, where `ε ∼ N(0, σ²)`, clip to `[0,1]`
   - This gives a noisy matrix where even all-honest fleets have entries < 1.0
   - Compute `γ̃` = spectral gap of normalized Laplacian of `W`

2. **Generate `W^π`** (proof-anchored coupling):
   - All agents honest: set all entries to 1
   - Compute `γ̃^π` = spectral gap of normalized Laplacian of `W^π`

3. **Repeat** across multiple noise levels `σ ∈ {0.05, 0.1, 0.2}` and `r = 100` Monte Carlo trials per condition

### Metrics

| Metric | Description |
|--------|-------------|
| `γ̃(n, σ)` | Mean spectral gap for standard coupling, by fleet size and noise |
| `γ̃^π(n)` | Spectral gap for proof-anchored coupling (deterministic for all-honest) |
| `FP(τ, n, σ)` | False-positive rate for standard coupling at threshold `τ` |
| `FP^π(τ, n)` | False-positive rate for proof-anchored coupling at threshold `τ` |

### Expected Results

| n | `γ̃` (σ=0.1) | `γ̃^π` | Signal-to-Noise Ratio |
|---|-------------|--------|----------------------|
| 4  | ~0.85       | 1.0    | ~5:1 (W) vs ∞ (W^π) |
| 16 | ~0.60       | 1.0    | ~3:1 (W) vs ∞ (W^π) |
| 64 | ~0.35       | 1.0    | ~1.5:1 (W) vs ∞ (W^π) |

**Falsification criterion**: If `γ̃^π < 0.95` for any `n ≥ 4` with all-honest agents, H2 is **rejected**. If `γ̃^π = 1.0` to machine precision and `γ̃` shows degradation with `n`, H2 is **confirmed**.

---

## 5. Edge Cases and Failure Modes

### If H2 Fails (γ̃^π < 1.0 for honest agents)

Possible causes:
- Proof verification itself introduces false negatives (valid proofs rejected)
- The assumption that `W^π = J_n` for honest agents is wrong — proofs may need pairwise verification logic
- The normalized Laplacian of `J_n` actually has gap 1.0 — this cannot fail mathematically, so failure would mean the proof system itself is unreliable

### If H2 Passes but Is Useless

Even if `γ̃^π = 1.0` for all-honest fleets, the system is only useful if:
1. ZK proof generation doesn't slow agents below unacceptable latencies
2. Proof verification scales to `O(n²)` operations (the coupling matrix is dense for `W^π = J_n`)
3. Dishonest agents cannot forge proofs (soundness of the ZK system)

### Numerical Considerations

- Use `float64` for spectral decomposition
- For `γ̃^π` of `J_n`, expect exact `1.0` up to rounding error (`~10⁻¹⁵`)
- Set `τ = 0.9` as the pass/fail threshold for `γ̃^π` — any measured value below 0.99 is a rejection

---

## 6. Test Harness Skeleton (Pseudocode)

```
function test_H2():
    for n in [4, 16, 64]:
        # W^π: all honest
        W_pi = ones(n, n)
        γ̃_pi = spectral_gap(W_pi)           # Should be exactly 1.0
        
        for σ in [0.05, 0.1, 0.2]:
            for trial in 1..100:
                # W: noisy behavioral
                s = [1.0] * n                  # all honest → true signal
                noise = σ * randn(n, n)
                W = clip(s + noise, 0, 1)
                γ̃[trial] = spectral_gap(W)
            
            μ = mean(γ̃), err = std(γ̃) / sqrt(100)
            print(f"n={n}, σ={σ}: γ̃ = {μ} ± {err}, γ̃^π = {γ̃_pi}")
            
            if γ̃_pi < 0.99:
                return REJECT_H2
    
    return CONFIRM_H2
```

---

## 7. What a Positive Result (γ̃^π = 1.0) Means

If H2 is confirmed:

1. **Proof-carrying task tiles eliminate the noise dimension entirely.** The completion signal is no longer a continuous variable with measurement error — it's a boolean that's either provably true or false.

2. **Fleet size no longer degrades detection quality.** A fleet of 1024 agents is as monitorable as a fleet of 4.

3. **The coupling matrix W becomes optional.** If proof validity alone gives perfect completion detection, the behavioral coupling `W` can be reserved for training and optimization, not monitoring.

4. **Spectral-gap false positives go to zero** — but only for completion detection. Proofs don't help with task quality, only task finalization.

### Next Directions (if H2 confirmed)

- **H3**: Embedding quality scores WITHIN proofs (ZK-SNARK for `quality ≥ τ`) extends zero-FP to quality monitoring
- **H4**: Distributed proof aggregation (threshold proofs, committee verification) scales beyond `n=64` without `O(n²)` coupling
