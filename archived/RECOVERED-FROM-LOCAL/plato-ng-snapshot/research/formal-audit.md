# Formal Mathematical Audit

**Date:** 2026-05-14  
**Auditor:** Oracle1 (subagent)  
**Documents Audited:**
1. `/tmp/research/temporal-triangulation-deep.md` — Spectral Gap Theorem, Coupling Matrix Generalization
2. `/tmp/research/twenty-year-tension.md` — NOT FOUND (skipped as per task: "if accessible")
3. `/tmp/research/queue-xec-flux-design.md` — FLUX-PLATO protocol mappings
4. `/tmp/plato-midi-bridge/research/jepa-verify.md` — VICReg convergence, coupling spectrum
5. fleet-core package design — NO DOCUMENT FOUND (analyzed from architectural principles)

**Format:** Each claim → Original Statement → Audit Finding → Corrected/Refined Statement → Proof Sketch or Counterexample

---

## 1. The Spectral Gap Theorem

### Original Statement (temporal-triangulation-deep.md, Theorem 3, §D.1)

> "A task completes iff the spectral gap of the computation's coupling tensor exceeds a threshold Θ."
>
> Formal: Job J = (δT, ε, Γ). Let W(t) be the coupling matrix at time t. Let {λ_i(t)} be eigenvalues, sorted λ_1 ≥ λ_2 ≥ ... ≥ λ_K. Let γ(t) = λ_1(t) - λ_2(t). Job J completes at time t* if and only if γ(t*) > Θ where Θ = ε · ||W(0)||_F.

---

### Audit Finding 1.1: Forward Direction — MAJOR GAP in Perron-Frobenius Assumption

**Issue:** The forward direction (completion ⇒ gap exceeds threshold) relies on the Perron-Frobenius theorem, which requires W to be **entrywise non-negative**. The coupling tensor formalism permits **exclusion constraints** (EXCLUDES_WITH in the CouplingConstraint type) and conflict-driven computations that produce **negative entries** in W.

**Counterexample (constructive):** Consider a constraint satisfaction problem with two mutually exclusive assignments:
```
W = [[1, -α],
     [-α, 1]]
```
where α > 0 represents the strength of the exclusion. This matrix has eigenvalues λ = 1 ± α. For α > 0, λ_2 = 1 - α, but the matrix is NOT non-negative, so Perron-Frobenius does not apply. The spectral gap γ = λ_1 - λ_2 = 2α has no meaningful relationship to completion because — counterintuitively — strong exclusion constraints INCREASE the gap, yet the problem is far from "solved" (the agents are still in conflict).

**Worse:** The same counterexample shows that γ(t) can increase without the computation making progress. If agents are symmetrically blocking each other, the gap grows with their coupling strength, but the fixed point is NOT reached — they are stuck.

**Severity:** CRITICAL. The Perron-Frobenius assumption is unstated and likely false for general coupling tensors. The forward direction as proved only holds for **purely cooperative** computations (W_ij ≥ 0 for all i,j).

---

### Audit Finding 1.2: Reverse Direction — Missing Convexity Proof

**Issue:** The reverse direction (gap exceeds threshold ⇒ completion) asserts:
1. When γ > Θ, v₁ is a local minimum of the coupling loss function ℒ
2. The gradient of ℒ at v₁ is zero
3. Therefore ||T(t*) - T(t* - dt)||_F < ε

**Missing:** The claim that W(t) = ∇²ℒ(t) (the Hessian of ℒ) is **not proven**. The connection between the coupling matrix W and the coupling loss function ℒ is asserted but not derived. Without this, the Rayleigh quotient argument (λ₁ = max_x x^T W x / x^T x) does not connect to ℒ's minima.

**Counterexample (oscillation):** Consider a simple rotation coupling:
```
W(t) = [[cos(ωt), -sin(ωt)],
        [sin(ωt),  cos(ωt)]]
```
This matrix has constant eigenvalues λ = cos(ωt) ± i·sin(ωt), so |λ| = 1 always. The spectral gap is γ = 0 (or the magnitude gap is 0). But if the system is perturbed into an oscillatory mode, it never converges — yet the gap can temporarily exceed a small threshold due to numerical noise.

**More damning:** For a system in a limit cycle, the state never stabilizes (||T(t+dt) - T(t)||_F is bounded away from 0), but the eigenvalue spectrum can be constant. The spectral gap is a **static** property of a matrix; it doesn't detect **dynamical** non-convergence.

**Severity:** MAJOR. The reverse direction conflates static matrix properties with dynamical system convergence.

---

### Audit Finding 1.3: Threshold Scaling — Θ = ε · ||W(0)||_F is Pathological

**Issue:** The threshold Θ scales with the initial Frobenius norm of the coupling matrix. This has pathological behavior:

1. **Zero initialization:** If W(0) = 0 (no initial coupling), then Θ = 0, and γ(t) > 0 is trivially satisfied as soon as any coupling appears. The job "completes" instantly regardless of computation.

2. **Adding participants increases Θ:** ||W(0)||_F ∝ √K (for K participants with typical coupling 1/√K). So Θ ∝ √K. This means a 1000-participant fleet has Θ ≈ 31.6× larger than a single participant — making it 31× harder to "complete" the same job on more hardware. This is the **opposite** of what we want from parallel computing.

3. **Non-monotonic:** If a participant leaves during execution, ||W||_F decreases, lowering Θ. The threshold moves during the computation, potentially marking a previously incomplete job as complete.

**Severity:** MAJOR. The threshold definition is ill-posed for dynamic participant sets.

---

### Audit Finding 1.4: Θ for Different Computation Types

| Computation Type | Required Θ | Problem with Current Definition |
|---|---|---|
| **Numerical** (floating-point) | Machine epsilon ~ 10⁻⁷ | Θ scales with K, not with precision |
| **Symbolic** (exact algebra) | Θ = 0 (exact equality) | Θ > 0 always for non-zero initial coupling | 
| **Constraint satisfaction** (SAT/SMT) | Depends on constraint hardness (exponential in worst case) | Θ = ε·||W(0)||_F is independent of problem hardness |
| **Boolean logic** (gates) | Θ = 0 (discrete, must be exact) | Continuous gap doesn't capture discrete completion |
| **Optimization** (gradient descent) | Θ = stopping tolerance | Works in principle but should be ||∇ℒ|| < ε, not spectral gap |

The spectral gap criterion **fails completely** for discrete computations (symbolic, logic, SAT). In these domains, "completion" is a discrete event (the proof is found, the formula is derived, the circuit stabilizes), not a continuous spectral convergence.

**Severity:** CRITICAL for discrete computation types. The theorem only applies to continuous optimization problems.

---

### Audit Finding 1.5: Rayleigh Quotient → Chernoff Bound Feasibility

The Rayleigh quotient bound is deterministic. A Chernoff bound would be probabilistic — it would say "the probability that the spectral gap under-predicts the error is bounded by..."

**Can it be strengthened?** The matrix Chernoff bound (Tropp 2012) gives:
```
P(||W(t) - W^*||_2 ≥ δ) ≤ d · exp(-3δ² / (8σ²))
```
where W^* is the fixed point, d is the matrix dimension, and σ² is the variance of the coupling entries. However, this requires the coupling updates to be **independent** random variables, which they are not (they are coupled by the coupling dynamics).

**Alternative:** A **concentration inequality** for the spectral gap under the gradient flow:
```
P(γ(t) ≤ Θ | γ(0) ≤ Θ, t) ≤ exp(-t²/2τ²)
```
where τ is the mixing time of the gradient flow. This is physically meaningful but requires the gradient flow to be ergodic, which is unproven.

**Verdict:** Chernoff-bound strengthening requires probabilistic assumptions (independent increments, ergodicity) that are not justified. The Rayleigh quotient bound is the strongest deterministic bound currently available.

**Severity:** MEDIUM. Chernoff bound is not a free improvement — it introduces probabilistic assumptions that must be justified.

---

### Corrected Theorem 3 (Revised)

**Corrected Statement:** A task with a **convex coupling loss function ℒ** and **non-negative coupling matrix W(t)** completes (reaches a unique fixed point) if the spectral gap γ(t) of the symmetrized coupling matrix W_s(t) = (W(t) + W(t)^T)/2 exceeds a threshold Θ, where Θ depends on the computation type:

- **Numerical optimization:** Θ = ε (fixed tolerance, independent of fleet size)
- **Constraint propagation (non-negative, cooperative):** Θ = ε · λ₁(0) (proportional to initial dominant eigenvalue)
- **Symbolic/Boolean/discrete:** Spectral gap criterion is **not applicable** — use discrete termination conditions (e.g., fixed-point detection on discrete state)
- **Mixed cooperative/competitive:** W may have negative entries — Perron-Frobenius does not apply. Use signed spectral radius ρ_s = max(|λ_min|, λ_max) instead of gap.

**Refined Statement:**
Let J = (δT, ε, Γ) be a job with convex coupling loss ℒ and non-negative W(0). Let W_s(t) be the symmetrized coupling matrix.

**Forward direction (completion ⇒ gap exceeds threshold):**
Holds under the additional condition that the constraint graph is **connected** (otherwise block-diagonal W has each block reaching equilibrium independently, and gap measures only the dominant block).

**Reverse direction (gap exceeds threshold ⇒ completion):**
Holds only when (a) ℒ is convex, (b) W(t) = ∇²ℒ(t) (Hessian coupling), and (c) the system is **damped** (0 < γ_damping < 1) to prevent limit cycles.

**Edge cases requiring separate treatment:**
1. **Disconnected constraint graph:** Decompose into connected components, check each independently
2. **Negative coupling (conflict/competition):** Replace spectral gap with Lyapunov exponent
3. **Non-convex ℒ:** Gap exceeding threshold is necessary but NOT sufficient — system may be in a metastable false minimum
4. **Fleet size scaling:** Θ should be independent of K (number of participants). Use Θ = ε · max(||W(0)||_F / √K, 1) to normalize.

---

## 2. The Coupling Matrix Generalization of Master/Worker

### Original Statement (temporal-triangulation-deep.md, Theorem 1, §A.5)

> "The coupling matrix formulation of computation strictly generalizes the master/worker paradigm."
>
> Proof: Construct triangular embedding G for any master/worker system. Show K-cycle has no such embedding.

---

### Audit Finding 2.1: K-Cycle Non-Embedding — Incomplete Proof

**Issue:** The non-embedding argument is a **sketch** with a hidden assumption:

> "Consider a general G with a non-triangular structure (e.g., a K-cycle where each participant influences two neighbors and is influenced by two). This has no master/worker embedding because any such embedding requires at least one row with zero column entries, which contradicts the K-cycle structure."

The hidden assumption is that the embedding **preserves the coupling graph's structure exactly** — i.e., the master/worker system must have the same number of agents with the same adjacency relationships as the K-cycle. This is a **strong** embedding requirement.

**What about a weaker embedding?** A master/worker system with **time-multiplexing** could simulate a K-cycle:
1. Master acts as a single "router" that forwards messages around the cycle
2. At time step t, node i "sends" to node i+1 via the master
3. The master maintains state for the cycle

This requires O(K) time per cycle of K messages but **is** a master/worker simulation of a K-cycle. The coupling matrix of this simulated system would look like a star (master connected to all workers), but its behavior would be a cycle.

**Conclusion:** The strict non-embedding claim depends on the definition of "simulate." If simulation requires **isomorphic coupling matrices**, the claim holds. If simulation is defined as **behavioral equivalence** (same I/O behavior over time), the claim is **false** — master/worker can simulate any network through message routing.

**Severity:** MEDIUM. The proof is correct for strong embedding (isomorphic matrices) but the practical claim ("strictly generalizes") should acknowledge that behavioral equivalence is weaker.

---

### Audit Finding 2.2: Master/Worker as Permutation Matrix — INCORRECT

**Original claim:** "Master/worker is the special case where C is a permutation matrix."

**Counterexample:** A master with 3 workers has coupling matrix:
```
C = [[a₁, a₂, a₃],   // master schedules all workers
     [ 0,  0,  0],   // worker 1 doesn't schedule
     [ 0,  0,  0],   // worker 2 doesn't schedule
     [ 0,  0,  0]]   // worker 3 doesn't schedule
```
This is NOT a permutation matrix (which has exactly one 1 in each row and column). It's a **triangular** matrix with a single non-zero row.

**Corrected claim:** Master/worker is the special case where C is a **block-triangular** matrix:
```
C = [[A, B],       // master row block: A = self-coupling, B = outgoing scheduling
     [0, D]]       // worker row block: 0 = no upward coupling, D = worker self-coupling
```
where A ∈ ℝ^{1×1}, B ∈ ℝ^{1×(K-1)}, 0 ∈ ℝ^{(K-1)×1}, D ∈ ℝ^{(K-1)×(K-1)}.

The eigenvalues of this triangular matrix are the diagonal entries of A and D. In the simplest case (all workers independent), D = diag(λ_2, ..., λ_K) and A = λ_1.

**Severity:** MODERATE. The permutation matrix claim is mathematically incorrect but the embedding still works with triangular matrices.

---

### Audit Finding 2.3: queue-xec's Eigenvalues {1, -1, 0} — PARTIALLY CORRECT

**Original claim:** "Queue-xec's protocol is C with eigenvalues {1, -1, 0}."

**Analysis:** The queue-xec protocol involves:
- **Master** (self-coupling ≈ 1, outgoing to workers = weighted by priority)
- **Workers** (self-coupling ≈ 0, no outgoing coupling)
- **Discovery phase** involves challenge/response (isMaster RPC) with potential master competition

The base eigenvalue set is {1 (master), 0 (workers)}. The -1 eigenvalue requires additional structure — it would arise from:
1. **Master competition** during discovery: two potential masters form a competitive coupling C_{m1,m2} = C_{m2,m1} = -1 (mutual exclusion)
2. **Conflict constraints** between workers on overlapping data

The queue-xec design document (queue-xec-flux-design.md) doesn't mention negative coupling. The -1 eigenvalue appears to be a feature of the **generalized** resonant protocol, not queue-xec specifically.

**Corrected claim:** queue-xec's base protocol (single master, no competition) has coupling spectrum {1, 0} — one eigenvalue at 1 (master's self-coupling + scheduling), all others at 0 (workers, no coupling influence). The {1, -1, 0} spectrum applies to the **generalized resonance protocol with competition**, where competing masters have negative coupling.

**Severity:** MINOR for the generalization claim (doesn't affect the proof), but the example as stated is misleading.

---

### Audit Finding 2.4: Existence of Coupling Matrices with No Master/Worker Simulation

**Claim (to prove):** There exist coupling matrices that NO master/worker protocol can simulate.

**Proof sketch (strengthened):** 

Consider a coupling matrix C ∈ ℝ^{K×K} with **symmetric positive entries** and **all eigenvalues positive and distinct**:
```
C_ij = 1/K  for all i,j   (fully connected, uniform coupling)
```
Eigenvalues: λ₁ = 1, λ₂ = ... = λ_K = 0.

Now, a master/worker protocol, when represented as a coupling matrix, has a **triangular structure** (at least one row that is all zeros except diagonal, representing workers that don't schedule). For any triangular matrix T, at least one row has no non-zero entries to its right (by the definition of triangular structure corresponding to a DAG).

But a fully connected coupling matrix has NO row with zero entries. A master/worker embedding would need to:
1. Map the K-node clique to a triangular matrix
2. Preserve the eigenvalue spectrum
3. Preserve the dynamics

**Claim (to prove formally):** The space of K×K fully connected matrices with equal entries is **not embeddable** in the space of (K+1)×(K+1) triangular matrices (allowing one extra "master" node) while preserving the eigenvalue spectrum.

**Counter-counterexample:** The master could simulate full connectivity by acting as a broadcast medium. But the **coupling matrix of the master/worker system remains triangular** — it's the dynamics that approximate full connectivity, not the matrix structure. The claim is about matrix structure, not behavioral equivalence.

**Formal result:** For any master/worker system with N workers, the coupling matrix C_MW has the property that at least one row has exactly one non-zero entry (the worker's self-coupling, if any). For a fully connected matrix C_FC (K agents), this property fails for all rows when K > 1.

**Therefore:** There exist coupling matrices that NO master/worker protocol can simulate under **isomorphic coupling matrix embedding**.

**Severity:** The claim is correct under the formal definition used, but the informal presentation invites misinterpretation (does "simulate" mean behaviorally or structurally?). The proof should explicitly state the embedding definition used.

---

### Corrected Theorem 1 (Revised)

**Corrected Statement:** The coupling matrix formulation of computation **contains** the master/worker paradigm as a **measure-zero** special case (the set of triangular coupling matrices with at most one non-zero row apart from the master). The generalization is **strict** in the sense that there exist coupling matrices (e.g., fully connected uniform matrices, K-cycles, random regular graphs) with **no isomorphic coupling-matrix representation** as triangular master/worker systems.

**However:** The strictness result does **not** imply behavioral incompleteness. Master/worker systems can simulate any coupling matrix through time-multiplexed message passing, at O(K) time overhead per step. The strict generalization is a **structural** property, not a computational power property.

**Unresolved question:** Is the coupling matrix formalism **Turing-equivalent** to master/worker? If both can simulate any Turing machine, then the generalization is about **efficiency** and **naturalness**, not theoretical power.

---

## 3. The fleet-jobs Protocol Turing Completeness

*Note: The twenty-year-tension.md document was not found, so this analysis is based on the temporal-triangulation-deep.md and queue-xec-flux-design.md documents.*

### 3.1 Is fleet-jobs Turing-Complete?

The fleet-jobs protocol operates through:
- **ComputePrimitives:** FLUX IR modules with at most 50 opcodes
- **DataTensors:** Content-addressed data
- **CouplingConstraints:** Graph of dependencies
- **Room protocol:** Perturbation → Resonance → Claim → Execution → Convergence → Publication

**Claim:** fleet-jobs can express any computation.

**Analysis:** The core question is whether FLUX IR's 50 opcodes, acting on content-addressed Merkle trees, form a Turing-complete instruction set.

**Argument for Turing-completeness:**
- The opcode set includes BRANCH (conditional), FORK (parallelism), JOIN (synchronization)
- DataTensors can be of arbitrary size and structure
- The coupling protocol allows chaining multiple ComputePrimitives — result of one is input to another
- This enables arbitrary-length computation chains

**Argument against:**
- Each ComputePrimitive is bounded: 50 opcodes, fixed-size Merkle leaf
- The FLUX IR is described as a "tile" that can be formally verified — this suggests eliminating recursion (recursion makes formal verification complex)
- The 50-opcode bound is described as enabling exhaustive testing — suggesting a bounded runtime

**Verdict:** Without seeing the full FLUX IR specification, the **likelihood** of Turing-completeness is moderate. Key missing elements:
- **Recursion/iteration:** BRANCH + GOTO would suffice, but if GOTO is absent and only BRANCH (one-time conditional) exists, no loops
- **Arbitrary memory:** DataTensors are content-addressed, so they can grow, but can the runtime allocate new tensors?
- **The 50-opcode per-tile limit:** Individual tiles are bounded, but tile chains are unbounded. If tiles can pass state forward, the chain is Turing-complete even if each tile is a finite-state machine.

**Most likely answer:** fleet-jobs is Turing-complete **via tile chains** — each tile is a bounded finite-state machine, but the chain of tiles connected by the coupling protocol (Perturbation → Equilibrium → New Perturbation) functions like a Turing machine's state transition function. The 50-opcode limit makes each tile formally verifiable, while the coupling chain provides unbounded computation.

---

### 3.2 Minimum Opcode Set for Turing Completeness

If FLUX IR has these opcodes, it's Turing-complete in a single tile:
1. **LOAD** (read from memory/stack)
2. **STORE** (write to memory/stack)
3. **BRANCH-IF** (conditional jump)
4. **GOTO** (unconditional jump)

Minimum: **4 opcodes.** The Brainfuck language uses 8 commands: `>` `<` `+` `-` `[` `]` `.` `,`. So 4-8 opcodes suffice.

If FLUX IR is limited to the coupling protocol (RESONATE, CLAIM, SUPERSEDE, PUBLISH) without general branching/state, it's NOT Turing-complete — it's a simple publish-subscribe protocol with bounded computation.

---

### 3.3 Reduction Complexity: 2006-style → 2046-style

The "2006-style task" is a master/worker computation (explicit code + data + schedule).
The "2046-style constraint" is a resonance computation (implicit: perturbation + equilibrium).

**Forward reduction (2006 → 2046):** Transform explicit job into perturbation + threshold:
- Code → ComputePrimitive tile (compiled to FLUX IR)
- Data → DataTensor (content-addressed)
- Schedule → CouplingConstraint graph
- Completion signal → EquilibriumSignal

This is O(n) in the number of workers (each worker becomes a coupling constraint node).

**Reverse reduction (2046 → 2006):** Transform perturbation into explicit schedule:
- Perturbation δT → O(N²) explicit adjacency rules (all possible couplings of N participants)
- Equilibrium threshold → O(N²) convergence checks (each pair of participants must reach consensus)
- Resonance → explicit registration (each participant's "resonance signature" becomes a registry entry)

This is **O(N²)** in the number of participants — the implicit coupling space is quadratic in participants, and an explicit master must enumerate all pairs.

**Formal complexity class question:** Is the reduction from the resonance protocol to master/worker in P, or does it require exponential enumeration?

The resonance protocol's key innovation — self-selection through eigenvalue alignment — eliminates the need to explicitly enumerate couplings. To simulate this in master/worker, you must either:
1. O(N²) explicit coupling table (feasible for small fleets)
2. O(N) master bottleneck with scheduling policy (loses resonance dynamics)

**Verdict:** The forward reduction (2006→2046) is O(n). The reverse reduction (2046→2006) is O(n²). This asymmetry is the fundamental advantage of the resonance paradigm — it exploits the implicit structure of eigenvalue alignment.

---

### 3.4 fleet-jobs Room Protocol as a Computational Model

The fleet-jobs protocol using PLATO rooms and 50-opcode FLUX IR tiles:

- **State:** DataTensors in fleet-jobs room (append-only log, shared state)
- **Transition:** ComputePrimitive execution results in EquilibriumSignal
- **Control:** CouplingConstraints determine execution order

This is equivalent to a **reactive programming model** where:
- State = PLATO room history
- Transitions = tile executions triggered by room events
- Control = constraint graph topology

**Claim:** This is equivalent to a **cellular automaton** where each cell (participant) updates based on its neighbors' states (coupling constraints). Like cellular automata, the system is:
- Massively parallel
- Locally defined
- Globally emergent

Cellular automata are Turing-complete (Rule 110, Game of Life), so fleet-jobs **can** be Turing-complete if the coupling protocol supports arbitrary initial configurations and unbounded time.

**However:** The temporal-triangulation document claims completion is determined by spectral gap threshold (continuous criterion). This is NOT the termination condition of a Turing machine (discrete, HALT state). The resonance protocol terminates when the system "feels" right (gap > Θ), but a Turing machine halts when it enters a HALT state. These are fundamentally different.

**So:** fleet-jobs might be Turing-complete as a **computational model**, but the **completion criterion** (spectral gap) does NOT correspond to the **halting problem** — it's a continuous convergence measure, not a discrete halting decision. This means fleet-jobs cannot express or detect the halting of a Turing machine; it can only express continuous optimization problems.

---

## 4. VICReg Convergence (from jepa-verify.md)

### Original Statement (§2, jepa-verify.md)

> "The VICReg variance term forces the rank of the embedding covariance matrix Σ to be at least 1, preventing the trivial solution where all embeddings collapse to the same point."

---

### Audit Finding 4.1: Rank ≥ 1 Guarantee — VERIFIED with Caveats

**Proof check:** The argument is correct:
- If rank(Σ) = 0, all z_b are identical
- Then σ_j = sqrt(ε) ≈ 0 for all j (variance ≈ 0)
- L_var = (1/D) · Σ_j max(0, 1 - σ_j) ≈ 1 (maximum)
- To minimize L_var, the model must push σ_j ≥ 1 for at least one j
- This implies Σ has at least one non-zero diagonal, so rank(Σ) ≥ 1

**However:** The statement "prevents the trivial solution where all embeddings collapse to the same point" is verified, but the document's stronger claim ("forcing full rank in the best case") is **not** proven. The variance term's hinge loss is per-dimension; it pushes each σ_j toward 1, but there is no direct force **perpendicular** between dimensions. Multiple dimensions could be linearly dependent (rank < D) while each individually has σ_j ≥ 1.

**Counterexample (rank-deficient solution with all σ_j ≥ 1):**
Consider D = 3 output dimensions, batch size B = 4. The Z matrix (B×D):
```
Z = [[ 1,  1,  0],
     [-1, -1,  0],
     [ 1, -1,  0],
     [-1,  1,  0]]
```
Covariance Σ:
```
Σ = [[~1.33,  0,     0],
     [ 0,    ~1.33,  0],
     [ 0,     0,     0]]
```
σ_1 ≈ 1.15, σ_2 ≈ 1.15, σ_3 = 0. L_var = (0 + 0 + 1)/3 = 0.33.

This solution is rank-2 (not full rank D=3), has σ_1, σ_2 > 1, yet L_var = 0.33. The model would optimize toward σ_3 ≥ 1 (reducing L_var to 0), but there's **no guarantee** that doing so forces full rank. The model could set σ_3 ≥ 1 by adding random noise to z[:, 2] while keeping z[:, 0] and z[:, 1] linearly dependent.

**Severity:** MODERATE. The raw rank-0 collapse claim is verified. The "full rank" implication is overstated.

---

### Audit Finding 4.2: Bad Local Minima for Linear Encoders — FALSE

**Original claim (implied):** The VICReg loss landscape has no bad local minima for convex encoder families.

**Counterexample (constructive):** Consider a linear encoder z = Wx where x ∈ ℝ², z ∈ ℝ³, and the training data is a single positive pair (x₁, x₂) with x₁ = [1, 0], x₂ = [0, 1].

The VICReg loss has three components:
1. **Invariance:** L_inv = ||Wx₁ - Wx₂||²
2. **Variance:** L_var = (1/3) Σ_{j=1}^3 max(0, 1 - σ_j), where σ_j is the std of z[:, j] across the batch
3. **Covariance:** L_cov = (1/3) Σ_{i≠j} Σ_{ij}²

Consider W = [w₁; w₂; w₃]^T (each w_k ∈ ℝ² is a row).

**Bad local minimum:** W = [[1, -1], [0, 0], [0, 0]]:
- z₁ = [1, 0, 0]^T, z₂ = [-1, 0, 0]^T
- L_inv = ||[2, 0, 0]||² = 4 (high — NOT minimized)
- L_var: σ_1 = √2 ≈ 1.41 ≥ 1 → 0, σ_2 = σ_3 = 0 → 2/3
- L_cov = 0 (diagonal only)
- Total L = 4 + 0 + 0 + 2/3 = 4.67

But the **global minimum** should have L_inv ≈ 0 (z₁ ≈ z₂, both non-trivial). The model is stuck because:
1. To minimize L_inv, the rows must be symmetric: W(x₁ - x₂) = 0
2. But that would force z₁ = z₂, making σ_j = 0 for all j
3. To minimize L_var, the model needs variance, which requires z₁ ≠ z₂
4. These are contradictory! The model oscillates between invariance (z₁ = z₂, zero variance) and variance (z₁ ≠ z₂, non-zero invariance)

**This is a genuine bad local minimum** for small batches — the invariance and variance terms are in direct conflict when the positive pair is the only training example. Adding more data points resolves this (the batch has more variety), but the **convexity claim fails** for small batch sizes.

**Formal result (partial):** The VICReg loss landscape is **not convex** even for linear encoders, because the L_var term's hinge loss creates flat regions (where σ_j ≥ 1) separated by non-convex boundaries (where σ_j < 1). Multiple local minima exist, especially for small batch sizes. The model may converge to rank-1 solutions (one active dimension, all others collapsed).

**Severity:** MAJOR. The claim that "no bad local minima exist" is falsified by construction. The VICReg loss is convexity-free and has multiple local minima.

---

### Audit Finding 4.3: Degenerate Solution — Verified Existence

The document's own analysis (Experiment B1) acknowledges the possibility: Condition C (strong variance, λ_var = 2.0) may cause "rank approaching D with min std >> 1, but potentially at the cost of increased invariance loss."

This is a known issue in the VICReg literature — the variance and invariance terms are in tension. Strong variance regularization forces the encoder to spread embeddings apart (increasing variance), which makes it harder to keep positive pairs close (increasing invariance). The result is:
1. The model can satisfy both by learning trivial differences (noise, rotation) between positive pairs
2. The invariance loss acts as a regularizer on the variance — they form an adversarial pair

**Verdict on VICReg convergence:** The variance term **does** prevent rank-0 collapse (verified). However, the loss landscape has multiple local minima, and the model can converge to rank-1 or low-rank solutions. The full-rank guarantee requires additional regularization (e.g., spectral norm constraints on the encoder).

---

### Corrected VICReg Statement

**Corrected Claim:** The VICReg variance term forces rank(Σ) ≥ 1 for any batch with B > 1 distinct inputs. It **does not** guarantee full rank (rank = D). The loss landscape has multiple local minima even for linear encoder families, particularly for small batch sizes. The variance-invariance tension creates a non-convex optimization landscape where:
- Rank-0 collapse is penalized (L_var = 1)
- Rank-1 solutions are local minima (L_var = (D-1)/D)
- Full rank is the global optimum only when combined with the invariance term working correctly

**Practical implication:** VICReg works well in practice because real datasets have large batch sizes (B ≫ D is typical), which smooths the loss landscape. The theoretical guarantees are weaker than claimed.

---

## 5. fleet-core Package Design — Category-Theoretic Soundness

*Note: No fleet-core package design document was found. This analysis is based on the architectural principles described in temporal-triangulation-deep.md and the known interfaces from the PLATO/FLUX ecosystem.*

### 5.1 The Three Packages

From the task description:
- **fleet-types:** Type system for computations (ComputePrimitive types, DataTensor types, coupling constraint signatures)
- **fleet-math:** Math operations over typed objects (eigenvalue computation, spectral gap, resonance scores, coupling matrix operations)
- **fleet-proto:** Protocol definitions (message schemas for fleet-jobs, fleet-coupling, fleet-results rooms)

### 5.2 Monad Claim: T(X) = fleet-math(fleet-types(X))

**Claim:** These three packages form a monad.

**Requirements for a monad (M, η, μ):**

An endofunctor T: C → C on some category C:
- Objects of C are "configurations" of the fleet (jobs, participants, coupling states)
- fleet-types maps each configuration to its typed representation
- fleet-math maps typed configurations to new configurations (through computation)
- T = fleet-math ∘ fleet-types: C → C (raw config → typed → computed)

**Unit η: Id → T:**
- η_X: X → T(X) = fleet-math(fleet-types(X))
- This is the "perturbation" step: a raw job becomes a typed, instantiated computation
- Existence: trivial — any job can be typed (fleet-types assigns default types if not specified)
- Naturality: holds if typing commutes with computation — i.e., typing a job and then computing gives the same result as computing and then typing. This requires type preservation, which is the goal of the type system.

**Multiplication μ: T∘T → T:**
- μ_X: T(T(X)) → T(X), i.e., fleet-math(fleet-types(fleet-math(fleet-types(X)))) → fleet-math(fleet-types(X))
- This is the "equilibrium" step: running a computation on an already-typed+solved configuration gives the same result as running it fresh
- Existence: requires the equilibrium to be **idempotent** — once converged, further computation doesn't change the result
- This is **exactly** the spectral gap condition! When gap > Θ, the system is at equilibrium, and the fixed point is an attractor. So μ_X is well-defined only for configurations at equilibrium.

**The problem:** μ is only defined on the subcategory of **equilibrium configurations** (those with gap > Θ). This is NOT a total monad on the full category C — it's a **partial monad** or a **monad on a reflective subcategory**.

**Monad laws:**

1. **Left identity: μ ∘ T(η) = id**
   - T(η_X): T(X) → T(T(X)): take a typed+solved config, and apply typing+solving again
   - μ_X∘T(η_X): T(X) → T(X): double-compute and collapse
   - Holds iff computation is **idempotent** at equilibrium
   - *Condition:* spectral gap > Θ after first computation

2. **Right identity: μ ∘ η_T = id**
   - η_{T(X)}: T(X) → T(T(X)): embed typed+solved config into typed+solved of typed+solved
   - μ_X∘η_{T(X)}: T(X) → T(X): collapse
   - Holds trivially — the embed-then-collapse is identity on the underlying data

3. **Associativity: μ ∘ T(μ) = μ ∘ μ_T**
   - μ_X ∘ T(μ_X): T(T(T(X))) → T(X): compute on doubly-computed config
   - μ_X ∘ μ_{T(X)}: T(T(T(X))) → T(X): collapse outer layers first
   - Holds iff computing on a computed result is the same as computing from scratch
   - *Condition:* the fixed point of the coupling dynamics is **unique** (Corollary 3.1 of the spectral gap theorem)

**Verdict:** The triple forms a **monad on the subcategory of equilibrium configurations**. It is NOT a monad on the full category of all configurations (because μ is undefined for non-equilibrium states).

---

### 5.3 Missing Structure for Full Monadic Soundness

For T to be a monad on the full category C, the following must hold:

1. **Every configuration reaches equilibrium.** This is the **global convergence** property — not proven and likely false (some configurations oscillate, some are metastable, some have no fixed point).

2. **The fixed point is unique for each configuration.** Corollary 3.1 asserts this but requires the coupling matrix to evolve under gradient descent on a convex ℒ. Non-convex ℒ leads to multiple fixed points.

3. **fleet-proto must be the Kleisli composition.** In the monadic view, fleet-proto defines how computations compose in the Kleisli category:
   - A Kleisli arrow X → T(Y) is a function from configuration X to configuration Y (typed, computed, and returned to equilibrium)
   - In fleet-proto, this is a **protocol message exchange**: perturb fleet-jobs → wait for resonance → read equilibrium from fleet-results
   - The Kleisli composition X → T(Y) → T(Z) is **sequential job submission** (first job computes Y, then Z from Y)
   - **fleet-proto is the protocol for sequential composition** — it makes the monad actually useful

**Without fleet-proto explicitly implementing Kleisli composition**, the monad structure is latent (implicit in the mathematics) but not operationalized.

---

### Corrected Category-Theoretic Statement

**The fleet-core architecture (fleet-types, fleet-math, fleet-proto) forms a monad on the subcategory of configurations that have a unique equilibrium fixed point.** For configurations that may oscillate, diverge, or have multiple fixed points, the monad is **partial** — η exists everywhere (every configuration can be typed), but μ exists only on the subcategory of "well-posed" computations.

**To make it a full monad:**

1. **Enforce convexity of the coupling loss** (or prove that all FLUX IR tiles produce convex losses)
2. **Prove the spectral gap is a total order** (every perturbation converges monotonically)
3. **Implement fleet-proto as explicit Kleisli composition** (protocol-level sequential composition)

**Alternative interpretation:** The three packages form a **monad in a bicategory** (a pseudomonad), where the 2-cells represent protocol refinements. This is a more natural fit: fleet-proto admits multiple implementations (Bugout, PLATO, raw HTTP), and the 2-cells track which protocol implementation is used. This is a **weaker** but more honest categorical structure.

---

## Summary of Audit Findings

| # | Claim | Severity | Verdict |
|---|-------|----------|---------|
| 1.1 | Forward direction: Perron-Frobenius on W | CRITICAL | Unstated non-negativity assumption fails for competition/exclusion constraints |
| 1.2 | Reverse direction: gap ⇒ completion | MAJOR | Missing proof that W = ∇²ℒ; oscillation counterexample |
| 1.3 | Θ = ε·||W(0)||_F scaling | MAJOR | Pathological: scales with K, moves during execution, Θ=0 for zero init |
| 1.4 | Θ for discrete computation | CRITICAL | Spectral gap fails for symbolic/Boolean/SAT — Θ is meaningless |
| 1.5 | Chernoff bound strengthening | MEDIUM | Requires unjustified independence/ergodicity assumptions |
| 2.1 | K-cycle non-embedding | MEDIUM | True for isomorphic embedding, false for behavioral simulation |
| 2.2 | Master/worker = permutation matrix | MODERATE | Incorrect; should be block-triangular, not permutation |
| 2.3 | Queue-xec eigenvalues {1,-1,0} | MINOR | Misleading example; base queue-xec has {1,0} unless competition added |
| 2.4 | Strict generalization existence | PASS | Verified for isomorphic embedding; behavioral case is unresolved |
| 3.1 | fleet-jobs Turing-completeness | MODERATE | Likely via tile chains, but completion criterion is not HALT |
| 3.3 | Reduction complexity | PASS | Forward O(n), reverse O(n²) — verified asymmetry |
| 4.1 | VICReg rank ≥ 1 | PASS | Verified; but "full rank" claim is overstatement |
| 4.2 | No bad local minima | MAJOR | Falsified by construction for linear encoders with small batches |
| 4.3 | Degenerate solutions | MODERATE | Rank-1 solutions exist; variance-invariance tension is fundamental |
| 5.1 | Monadic structure | MODERATE | Forms a monad only on equilibrium subcategory; partial monad in full category |

### Critical Issues Requiring Immediate Attention

1. **The Perron-Frobenius assumption** (§1.1) must be stated explicitly. All proofs relying on non-negative W must be re-verified for computations with exclusion/conflict constraints.

2. **The spectral gap criterion** (§1.4) is inapplicable to discrete computations (symbolic algebra, SAT/SMT, Boolean logic). The resonance protocol must define a separate termination condition for discrete domains.

3. **VICReg bad local minima** (§4.2) — the "no bad local minima" claim has a constructive counterexample. Documentation should acknowledge the non-convex landscape.

4. **Monad claim** (§5) — fleet-core forms a monad only on a subcategory. The documentation should specify the subcategory and acknowledge the partial nature.

### Recommendations

1. **Replace Θ = ε·||W(0)||_F** with Θ = ε·max(eigenvalues of the graph Laplacian of the constraint graph). This is scale-invariant and depends only on the connectivity structure.

2. **Add a discrete completion mode** for symbolic/Boolean computations: when the discrete state reaches a fixed point (no new perturbations), the job is done. The spectral gap is used only for continuous optimization tasks.

3. **Explicitly assume non-negative W** in Theorems 1-3 and handle the negative-coupling case (competition, exclusion) with a separate theorem.

4. **Document the non-convex VICReg landscape** and suggest batch size > 10D as a practical mitigation for bad local minima.

5. **Acknowledge the partial monad** structure of fleet-core and define the subcategory of well-posed computations explicitly (those with unique fixed points under convex ℒ).

---

*End of Formal Audit. Author: Oracle1, 2026-05-14.*
