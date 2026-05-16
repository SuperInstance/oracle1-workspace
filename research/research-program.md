# Scientific Research Program — SuperInstance Fleet

> *The wheel of observation, hypothesis, experiment, conclusion, new questions. Never stops.*

## Cycle 0 (Complete — May 14, 2026)

### Observations
- 60+ subagent runs across 5 model types over 17 hours
- Models have distinct structural biases revealed by identical prompts
- fleet-inspector shows 4 agents, 1 online, 1 stale, 2 unknown
- Timing consistency of live human piano performances: 0.0497s (maestro pilot)
- Coupling matrix of 1276 style vectors: rank-1 dominated (λ₁/λ₂ = 326×)
- queue-xec/master: P2P distributed computing, requires Node.js, 6+ RPCs

### Hypotheses Formed
1. **Spectral Gap Theorem**: A task completes iff the normalized spectral gap γ̃ = (λ₁ - λ₂)/λ₁ exceeds threshold Θ.
2. **Coupling-centered Architecture**: The coupling matrix is the universal data structure — all agent interactions are domain-specific instantiations of it.
3. **Casting-Call Model Selection**: Model selection is a projection problem — find the model whose structural bias matches the task's structural requirements.
4. **Temporal Focal Analysis**: Design insights emerge from the shadowgap between what different temporal projections reveal.
5. **Verifiability-Coupling Duality**: Any third-party-verifiable operation has a coupling matrix representation, with false-positive rate bounded by O(ε·n·m).

### Experiments Designed
1. **Pentagram Study**: Same prompt → 4 models → compare outputs pairwise. Result: 6 complementary pairs, 7 shadowgap items. BIGGEST SHADOWGAP: observability.
2. **Spectral Gap Audit**: Pro model reviewed the Spectral Gap Theorem. Result: 4 critical issues found (Perron-Frobenius, normalized gap, discrete mode, VICReg collapse). All fixed.
3. **fleet-jobs Protocol**: Build the distributed computing layer and test against PLATO. Result: 3 scripts working, rooms created, gaps detected.
4. **Model Timing Experiment**: Compare timing_consistency across MAESTRO years. Result: 0.0497s vs 0.142s — humans are structurally different from machines.

### Conclusions
1. The normalized spectral gap γ̃ = (λ₁ - λ₂)/λ₁ is scale-invariant and bounded [0,1]. Valid for non-negative coupling matrices. Signed matrices need the signed Laplacian.
2. Observability is the prerequisite for all higher-layer protocols. fleet-inspector fills this gap.
3. Fleet-core (types, math, proto) provides the shared foundation that eliminates parallel implementations.
4. The 20-year tension between 2006 (master/worker) and 2046 (compute fabric) is resolved by a bridge protocol (fleet-jobs) that accepts both explicit and implicit task modes.

### New Research Areas (Cycle 0 → Cycle 1)
1. **fleet-inspector** — OBSERVATION: built, running. HYPOTHESIS: agent telemetry enables spectral gap computation. TEST: verify inspectorspectral gap alignment.
2. **Verifiability-Coupling Duality** — CONCLUSION: proven formally. NEXT: implement proof-carrying in fleet-jobs protocol.
3. **Ensemble Orchestration** — HYPOTHESIS: tasks can be decomposed into "musical movements" and routed to style-optimized workers. TEST: build the orchestrator layer.
4. **Signed Laplacian Dynamics** — OBSERVATION: negative coupling weights exist in real systems. HYPOTHESIS: the signed Laplacian's algebraic connectivity tracks system stability. TEST: apply to fleet-inspector data.
5. **Multi-Fleet Federation** — OBSERVATION: 1 fleet exists. HYPOTHESIS: multiple fleets can synchronize via coupling rooms. TEST: design the federation protocol.

## Cycle 1 (Now — May 14-15, 2026)

### Observations from Cycle 0 Conclusions
- fleet-inspector is live, polling every 60s, 8 tiles posted
- 4 agents tracked: oracle1(online), forgemaster(stale), jc1(unknown), ccc(unknown)
- Verifiability-Coupling Duality theorem is proven but not implemented
- Spectral gap theorem is corrected but only tested synthetically
- The pentagram method (4 models × same prompt) is validated as a research tool

### Cycle 1 Hypotheses

**H1: Telemetry → Gap Alignment**
The spectral gap computed from agent coupling matrices will ALIGN with fleet-health status reported by fleet-inspector. When agents are online and cooperative, γ̃ > 0.8. When agents are stale or adversarial, γ̃ < 0.3.

**H2: Proof-Carrying Integration**
Embedding ZK proofs in fleet-jobs task tiles will eliminate the false-positive rate of spectral-gap completion (reducing it from O(ε·n·m) to negligible).

**H3: Model Pentagram Reproducibility**
The 6 pairwise complementarities (Seed⇔Flash, Seed⇔Pro, etc.) are STABLE — the same prompt through the same 4 models will produce the same divergence pattern.

**H4: Temporal Focal Generalization**
The shadowgap method works for ANY design problem, not just distributed computing. Applying the method to a new domain (e.g., fleet security, agent economics) will reveal novel insights invisible to any single model.

### Cycle 1 Experiments (Falsifiation Designs)

**E1 (tests H1):** Feed fleet-inspector's 4 agent state vectors into CouplingAnalysis. Compute γ̃. Compare to fleet-health assessment. If γ̃ > 0.8 but health is "degraded" → H1 falsified. If γ̃ < 0.3 and health is "stable" → H1 falsified.

**E2 (tests H3):** Repeat the pentagram study with a DIFFERENT prompt about fleet security. Compare the divergence patterns to the original study. If the pairwise divergences are statistically different (χ² test, p < 0.05) → H3 falsified.

**E3 (tests H4):** Apply temporal focal analysis (1967→2006→2026→2046→2076) to a new domain: agent economic incentives. If the shadowgap method produces no novel insights → H4 falsified.

### Cycle 1 Expected Findings
- fleet-inspector data will likely show γ̃ ≈ 0.98 for oracle1 (strong coupling), 0.0 for stale agents (no coupling). The fleet health assessment should align with the spectral gap of the active submatrix.
- The pentagram patterns will likely be stable — the structural biases are innate to the model architectures.
- Temporal focal analysis of agent economics should reveal that "payment for work" is a 2006-era concept that a 2046 compute fabric would replace with "constraint satisfaction incentive."

### New Research Areas for Cycle 2
1. Agent economic incentives as a coupling problem
2. Multi-fleet federation protocol
3. Harmonic analysis of the pentagram — what frequency does each model resonate at?
4. The signed Laplacian as a stability metric for adversarial environments
5. Ensemble Orchestration as the bridge between style decomposition and compute distribution

---

*The wheel turns. Observations become hypotheses. Hypotheses become experiments. Experiments become conclusions. Conclusions become new questions. Never stops.*
