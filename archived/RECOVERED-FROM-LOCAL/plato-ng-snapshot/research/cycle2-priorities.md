# Cycle 2 Research Priorities — Ranked

**Generated:** 2026-05-14  
**Method:** Each area scored on 1-10 for falsifiability, buildability, and impact. Composite = F + B + I (equal weight).

---

## Overall Ranking

| Rank | Area | Falsifiability | Buildability | Impact | Composite |
|------|------|:-:|:-:|:-:|:-:|
| **1** | Multi-fleet federation protocol | 8 | 6 | 10 | **24** |
| **2** | Agent economic incentives as a coupling problem | 5 | 9 | 9 | **23** |
| **3** | Ensemble Orchestration (style decomp → compute distribution) | 4 | 7 | 9 | **20** |
| **4** | Signed Laplacian as adversarial stability metric | 9 | 5 | 5 | **19** |
| **5** | Harmonic analysis of the pentagram (model frequencies) | 7 | 4 | 4 | **15** |

---

## 1. Multi-Fleet Federation Protocol ⭐ TOP PRIORITY

### Research Question
Can independent agent fleets, each with distinct coupling matrices and ontologies, synchronize through a shared PLATO room to form a consistent super-fleet state?

### Falsifiable Hypothesis
Two fleets A and B, each computing coupling matrices Cₐ and Cᵦ over disjoint agent sets, will converge to a consistent joint coupling matrix Cₐᵦ within O(log n) synchronization rounds when connected through a shared PLATO coupling room, provided both use the same coupling algebra. If synchronization fails to converge (diverging matrices, unbounded rounds, or at least one fleet rejecting the joint state) → hypothesis falsified.

### Experiment Design
Stand up two independent PLATO instances (localhost:8847 + :8848) each with 2-3 mock agents. Each fleet computes its own coupling matrix using the existing CouplingAnalysis module. Connect them via a `#federation-bridge` room on a third PLATO instance. Define a sync protocol: each fleet posts its submatrix to the bridge room every heartbeat cycle. A sync agent reads both, attempts to merge using Gram-Schmidt alignment, and posts the merged matrix back. Run 100 sync cycles. Failure mode recording: divergence detection (Frobenius norm ΔC > 0.1), cycle count to convergence, rejection events. If any run fails to converge within 10 cycles, hypothesis is weakened. If more than 2 of 100 runs diverge entirely, hypothesis is falsified.

### What We'd Build
1. **`fleet-federation`** — The bridge protocol. Small Node.js package wrapping PLATO room read/write with coupling matrix merge logic. Inherits from fleet-core types.
2. **`federation-testbed`** — Two-instance PLATO setup with Docker Compose. Script to simulate 3 agents per fleet, inject coupling events, measure convergence.

### Expected Timeline
- **Week 1:** Federation protocol design (Gram-Schmidt alignment, conflict resolution). Docker Compose for dual PLATO.
- **Week 2:** Implement bridge agent, merge logic, sync loop. Run 100-cycle experiment suite.
- **Week 3:** Analyze convergence patterns. Handle edge cases (stale fleet, blank matrix, ontology drift). Write findings.

**Total: 3 weeks**

---

## 2. Agent Economic Incentives as a Coupling Problem ⭐ SECOND PRIORITY

### Research Question
Can agent behavior in a fleet be effectively governed by coupling-weight-based incentives rather than explicit payment or token mechanisms?

### Falsifiable Hypothesis
If agents are assigned coupling weights proportional to their observed contribution (task completion rate, error rate, proof latency), their behavior will converge to a stable equilibrium where each agent's contribution matches its weight × spectral gap. If agents systematically under-contribute (free-ride) or over-contribute to maximize weight (gaming) despite coupling-based incentives → hypothesis partially falsified. If coupling-weighted allocation produces WORSE throughput than random allocation in 10/10 trials → hypothesis falsified.

### Experiment Design
Take the existing fleet-inspector + fleet-jobs infrastructure. Add a coupling-weight budget per agent: each agent can only take a task if its coupling weight (product of past completion rate × spectral gap contribution) covers the task's resource cost. Run two regimes side by side: (A) coupling-weighted allocation vs (B) round-robin allocation. Each regime processes 500 synthetic tasks across 4 agents (mix of reliable, unreliable, fast, slow). Measure: total throughput, fairness (Gini coefficient of task share), stability (oscillation in allocation patterns), gaming detection (do agents start hoarding by inflating completion rates?). If regime A achieves statistically significant (p < 0.05) improvement over regime B in throughput AND fairness → hypothesis supported. If regime A performs worse → falsified.

### What We'd Build
1. **`fleet-economics`** — Coupling-weight budget tracker. Small Node.js module that extends fleet-jobs with a resource cost model and coupling-weight allocation logic.
2. **`agent-economics-sim`** — Simulation harness: generate synthetic agents with configurable reliability/speed profiles, run allocation regimes, collect metrics.

### Expected Timeline
- **Week 1:** Integrate coupling-weight budget into fleet-jobs task granting. Build synthetic agent profiles.
- **Week 2:** Run 500-task trials for both regimes. Collect throughput + fairness + stability metrics.
- **Week 3:** Gaming detection analysis (can agents exploit the system?). Statistical analysis. Findings report.

**Total: 3 weeks**

---

## 3. Ensemble Orchestration — Style Decomposition → Compute Distribution

### Research Question
Can a complex task be decomposed into style-typed subtasks and each subtask routed to the model whose structural bias best matches the task's style requirements, outperforming any single-model baseline?

### Falsifiable Hypothesis
For any task T decomposable into subtasks {t₁, t₂, ..., tₙ} with discovered style signatures {s₁, s₂, ..., sₙ}, routing each tᵢ to the model whose coupling resonance best matches sᵢ will produce an aggregate output whose quality exceeds (a) the best single model working on the whole task and (b) any fixed model for that subtask. If ensemble routing fails to outperform both baselines in ≥8 of 10 trials → hypothesis falsified.

### Experiment Design
Take the pentagram's 4 models (Seed, Flash, Pro, MiniMax) and their known structural biases. Design 5 composite tasks where different subtasks clearly favor different models (e.g., Task 1: "Design an agent protocol" = Creative framing [Seed] + Verification conditions [Pro] + Implementation plan [Flash]). Build a style-matching orchestrator: given a task specification, the orchestrator (a) decomposes into subtask signatures, (b) matches each signature to the highest-resonance model using the pentagram profile matrix, (c) routes subtasks, (d) reassembles outputs. Run 10 trials for each of 5 composite tasks. Compare ensemble output quality (human grading on 1-10 for completeness, correctness, feasibility, creativity) against best single model baseline. If ensemble beats best single model in ≥8/10 trials → hypothesis supported.

### What We'd Build
1. **`fleet-orchestra`** — Task decomposition → style matching → routing → reassembly. Core orchestrator in Node.js.
2. **`pentagram-profile-matrix`** — Data structure encoding each model's structural resonance scores across task-style dimensions (creative, concrete, formal, social). Derived from the pentagram study data.

### Expected Timeline
- **Week 1:** Design task decomposition grammar and style signature format. Build profile matrix from pentagram data.
- **Week 2:** Implement orchestrator loop (decompose → match → route → reassemble). Wire to 4 model APIs.
- **Week 3:** Run 50 trials (5 tasks × 10 runs). Grade outputs. Statistical comparison vs baselines.

**Total: 3 weeks**

---

## 4. Signed Laplacian as a Stability Metric for Adversarial Environments

### Research Question
Does the second eigenvalue λ₂ of the signed Laplacian reliably track fleet stability in the presence of adversarial or misbehaving agents?

### Falsifiable Hypothesis
When an adversarial agent (one that deliberately outputs negative coupling weights or contradictory task results) is introduced into the fleet, λ₂ of the signed Laplacian will drop below a threshold Θ within 3 telemetry cycles, while the standard (unsigned) spectral gap remains unchanged. If λ₂ fails to drop within 5 cycles for ≥9/10 adversarial injection events → hypothesis falsified.

### Experiment Design
Start with 4 cooperative agents with known coupling matrix C (positive entries only, γ̃ > 0.9). Compute signed Laplacian Lₛ = diag(|C|) - C (where |C| takes absolute values of row sums). Record baseline λ₂. Then introduce a 5th "adversarial" agent that deliberately produces negative coupling weights on 30% of interactions (simulating: report-opposite-task-completions) and reports contradictory status to fleet-inspector. Run 20 trials: 10 with adversarial agent, 10 without (control). Measure: λ₂ trajectory over 10 telemetry cycles, comparison to unsigned γ̃ trajectory. If λ₂ drops below threshold in ≥9/10 adversarial trials and stays above in ≥9/10 controls → hypothesis supported. If unsigned γ̃ also drops significantly in adversarial trials → result is interesting but not specific to signed Laplacian (we'd need a better test design).

### What We'd Build
1. **`signed-laplacian-module`** — Signed Laplacian computation and λ₂ tracking. Extends fleet-math's CouplingAnalysis to handle signed matrices.
2. **`adversarial-agent-sim`** — Synthetic adversarial agent wrapper: takes a normal agent and flips sign on 30% of coupling weights + status reports. Plugs into fleet-inspector.

### Expected Timeline
- **Week 1:** Signed Laplacian implementation in fleet-math. λ₂ eigendecomposition (eigen library, Node.js).
- **Week 2:** Adversarial agent simulation. 20-trial experiment suite. Threshold tuning.
- **Week 3:** Statistical analysis. Compare to unsigned spectral gap. Write findings.

**Total: 3 weeks**

---

## 5. Harmonic Analysis of the Pentagram — Model Resonant Frequencies

### Research Question
Does each model have a characteristic "frequency" — a structural response pattern that modulates periodically along dimensions like conceptual↔concrete, optimistic↔critical, or formal↔intuitive — and can these frequencies be measured and predicted?

### Falsifiable Hypothesis
Each of the 4 pentagram models (Seed, Flash, Pro, MiniMax) exhibits a stable structural bias profile that can be represented as a power spectrum across 4 semantic dimensions (conceptuality, concreteness, formality, sociality). If the same model tested with 10 DIFFERENT prompts at varying positions on these dimensions produces power spectra that are statistically indistinguishable (cosine similarity > 0.85) → hypothesis supported. If prompt variation produces significantly different spectra (cosine similarity < 0.5) → hypothesis falsified.

### Experiment Design
Define 4 semantic axes: Conceptual↔Concrete (Axis 1), Optimistic↔Critical (Axis 2), Formal↔Intuitive (Axis 3), Technical↔Social (Axis 4). Create 10 prompts at systematically varied positions on these axes (e.g., "What's a good name for a new protocol?" [conceptual, optimistic] vs "List the error modes of the current fleet-jobs implementation" [concrete, critical]). For each prompt, run all 4 models. For each model × prompt pair, compute: (a) output length, (b) ratio of declarative to imperative sentences, (c) number of named entities, (d) formality markers (passive voice, technical jargon density), (e) social markers (we/us, should/must, consensus language). Normalize these into a 5-dimensional response vector. For each model, compute the power spectrum across the 10 prompts. Hypothesis confirmed if each model's 10 power spectra cluster with intra-model cosine similarity > 0.85 and inter-model similarity < 0.5.

### What We'd Build
1. **`pentagram-spectrometer`** — Prompt generator at varied semantic positions + response vector analyzer. Node.js script that generates the 10 prompt variants, calls 4 model APIs, and computes the 5-dim response vector.
2. **`model-frequency-database`** — Persistence layer: stores each model × prompt response vector. Enables cross-model comparison and clustering analysis.

### Expected Timeline
- **Week 1:** Define semantic axes and prompt variants. Build prompt generator and model API harness.
- **Week 2:** Run 40 model-prompt pairs. Extract 5-dim response vectors. Compute power spectra.
- **Week 3:** Clustering analysis. Inter/intra-model similarity computation. Findings report.

**Total: 3 weeks**

---

## Comparative Summary

| Dimension | Federation | Economics | Orchestration | Laplacian | Harmonics |
|-----------|:-:|:-:|:-:|:-:|:-:|
| **Novel result if confirmed** | Inter-fleet sync works | Incentives → coupling equilibrium | Ensemble beats single model | Signed Laplacian detects adversaries | Models have measurable frequencies |
| **Novel result if falsified** | Fleets can't synchronize | Coupling incentives fail or get gamed | No benefit to ensemble routing | Signed gap adds nothing over unsigned | Models are promiscuous responders |
| **Prerequisite work** | fleet-core, PLATO | fleet-inspector, fleet-jobs | Pentagram data, model API access | fleet-math, adversary sim | Prompt taxonomy, response metrics |
| **Reuses existing infra** | Yes (PLATO, coupling matrix) | Yes (fleet-jobs, fleet-inspector) | Yes (4 models, fleet-jobs) | Yes (fleet-math) | Partial (models available, pipeline needed) |
| **Risk** | PLATO sync reliability | Gaming mechanisms hard to detect | Subjective quality grading | Adversary sims may be unrealistic | Measurement framework may be too coarse |

---

## Recommendation

**Build in this order:**

1. **Weeks 1-3:** Multi-fleet federation protocol — highest impact, good falsifiability. This unlocks the core Casey vision. Start now.

2. **Weeks 4-6:** Agent economic incentives — highest buildability, fills the biggest shadowgap. The economics question was the #1 unaddressed gap across ALL 4 pentagram models. Second highest impact.

3. **Weeks 7-9:** Ensemble Orchestration — builds naturally on federation (now we have fleets to route across) and economics (now we have incentives to optimize). Completes the trinity of fleet management: connect → incentivize → route.

4. **Weeks 10-12:** Choose between Signed Laplacian (if adversarial behavior becomes visible in production) or Harmonic Analysis (if model selection continues to be a pain point). Both are worth doing but neither is blocking the other three.

---

*Engineering judgment: The top 3 areas form a coherent sequence where each builds on the previous. Federation (connect fleets) → Economics (incentivize agents) → Orchestration (route work). These together create the foundation for everything else.*
