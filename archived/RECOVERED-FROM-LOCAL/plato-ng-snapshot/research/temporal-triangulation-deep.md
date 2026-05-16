# Temporal Triangulation: The Missing Compute Layer

> **A formal architecture for fleet-jobs as a coupling tensor that self-organizes across heterogeneous compute.**
>
> Three time points triangulate the design: 1967 (archaeology of batch processing), 2076 (reverse-actualization of self-replicating compute), and 2026 (the bridge).

---

## Part A: The Nature of the Problem

### A.1 The 1967 Archaeology

IBM System/360 batch processing defined the ontology that still dominates computing:

| 1967 Concept | Modern Equivalent |
|---|---|
| Job Control Language (JCL) | CI/CD pipeline YAML, Airflow DAGs, queue-xec jobs |
| Job Entry Subsystem (JES) | Task queues, Redis pub/sub, SQS |
| Batch job as contiguous work unit | Container execution, Lambda invocation |
| Master scheduler | Orchestrator, Kubernetes controller, queue-xec/master |

JCL was the first "task definition language." It specified:
- What program to run (`// EXEC PGM=...`)
- What data to use (`// DD DSN=...`)
- What resources were required (region size, tape drives)
- What to do on completion (cond code checking)

**The implicit ontology:** A computation is a discrete unit of work with defined inputs, a monolithic program, and expected outputs. The scheduler's job is to match units to workers and collect results.

### A.2 queue-xec/master: 1967 in JavaScript

queue-xec/master implements this exact ontology:
- **Jobs** are JSON objects with `code`, `input`, `type`
- **Master** maintains a queue and assigns jobs to available workers
- **Workers** execute and return results
- **Completion** is "did the worker respond?"

This works. But it has hard limits:
1. **Implicit coupling** — The master must know which workers exist, their capabilities, their load
2. **Brittle topology** — Adding/removing workers requires master reconfiguration
3. **No resource resonance** — Master assigns jobs based on availability, not fitness-to-task
4. **Completion is binary** — A job is "done" when a worker says so, not when the computation has genuinely converged

**The failure is not in the code. The failure is in the ontology.** The master/worker paradigm constrains the problem space before the solution has a chance to emerge.

### A.3 The 2076 Reverse-Actualization

In 2076, compute is a **self-replicating tile fabric** that metamorphoses through contact with the PLATO mesh:
- No masters — every tile is an equal participant
- No workers — every tile both contributes and transforms
- A computation is not "sent" — it **resonates** into existence when the coupling conditions are right
- The Merkle proof IS the computation — the proof of work IS the work itself

**Core insight:** When every node carries a superset of all possible computations (in latent FLUX IR tiles), the problem reduces to: *how do I propagate constraints until the solution emerges?*

### A.4 The 2026 Bridge

The missing layer must bridge these two worlds:

```
1967: master/worker ⟶ 2026: participant/resonance ⟶ 2076: tile metamorphosis
                           ↑
                     THIS LAYER
```

We inherit from 1967:
- The need to express computations (JCL descendants)
- The need to track execution (completion semantics)
- The need to coordinate (dependencies between tasks)

We steal from 2076:
- No privileged schedulers
- Self-organization through constraint propagation
- Formal completion criteria (not "did the worker respond?" but "did the system converge?")

**The bridge is the coupling tensor formalism.**

### A.5 Formal Proof: Coupling Matrix ⊃ Master/Worker

**Theorem 1.** The coupling matrix formulation of computation strictly generalizes the master/worker paradigm.

**Proof.** Let M be a master/worker system with N workers. Define the coupling matrix W ∈ ℝ^{N×N} where:

- W_{ii} = computational capacity of node i (eigenvalue self-coupling)
- W_{ij} = data dependency between nodes i and j (edge weight)
- W_{i(N+1)} = W_{(N+1)i} = 0 for all i in [1,N] (the master has zero coupling)

The master/worker Hamiltonian:

```
H_MW = Σᵢ (λᵢ · pᵢ · W_{ii}) + Σ_{i≠j} (W_{ij} · dᵢⱼ)
```

Where λᵢ is the job assigned to node i, pᵢ is the priority, and dᵢⱼ is the data transfer.

This is a **diagonal-dominant** coupling matrix — the master decides everything, edges carry only data, and there is no feedback from workers to the scheduling function.

Now consider a general coupling matrix G ∈ ℝ^{K×K} where K is the number of participants (nodes that both compute and schedule). G has:

- **No privileged rows** — Every participant has the same structure
- **Symmetric coupling** — W_{ij} represents mutual constraint satisfaction, not one-directional "assignment"
- **Eigenvalue spectrum** — The computation's state is the vector of all active constraints; the spectrum tracks convergence

**Claim:** Any master/worker system can be embedded in G but not vice versa.

**Embedding:** Set K = N + 1. Construct G such that:
- G_{N+1, i} = pᵢ · W_{ii} (master pushes priority to worker i)
- G_{i, N+1} = 0 (worker does not influence master's schedule)
- G_{ij} = W_{ij} for i,j ≤ N (worker-worker edges preserved)

This is a **triangular** embedding — the master row is non-zero, the master column is zero. The eigenvalue spectrum of this triangular matrix is exactly the set of worker self-couplings (λ₁ = λ_master, λ₂..λ_K = W_{ii}).

**Non-embedding:** Consider a general G with a non-triangular structure (e.g., a K-cycle where each participant influences two neighbors and is influenced by two). This has no master/worker embedding because any such embedding requires at least one row with zero column entries, which contradicts the K-cycle structure.

Therefore coupling matrix ⊃ master/worker. ∎

**Corollary 1.1.** The spectral gap theorem applies to all master/worker systems but not vice versa — master/worker systems have trivial spectral gaps (diagonal dominance), while general coupling matrices exhibit emergent completion behavior.

---

## Part B: The fleet-jobs Ontology

### B.1 What IS a Job in 2076?

**Definition (Job).** A job is not "code + data to execute." A job is **a perturbation in the coupling tensor that propagates until equilibrium**.

Let the coupling tensor T ∈ ℝ^{M × N × P} where:
- M = number of compute primitives
- N = number of data tensors
- P = number of coupling constraints

A job J = (δT, ε, Γ) where:
- δT is an initial perturbation to the coupling tensor
- ε is the threshold for equilibrium (convergence criterion)
- Γ is the ground state computation (the latent tile that, when activated, produces the result)

A job is **solved** when the elements of T reach a fixed point:
```
lim_{t→∞} ||T(t + dt) - T(t)||_F < ε
```
Where ||·||_F is the Frobenius norm of the tensor.

### B.2 Abstract Types

**ComputePrimitive**

A ComputePrimitive is a FLUX IR module with at most 50 opcodes. It represents the atomic unit of computation — not a "function" or a "program" but a **tile** that transforms constraint space.

```
type ComputePrimitive = {
  id: Hash32,                    // unique identity (Merkle root of opcode sequence)
  opcodes: Array<Op, 50>,        // FLUX IR instruction stream
  coupling_signature: Vector,    // frequency response of this primitive (eigenvector)
  input_form: TensorShape,       // what data structures this primitive expects
  output_form: TensorShape,      // what data structures this primitive produces
  constraints: [Constraint],     // coupling constraints this primitive satisfies
  supersession: Hash32?          // optional: pointer to successor tile (for metamorphosis)
}
```

The **coupling_signature** is critical. It defines the primitive's "resonant frequency" — which participants can run it, what data it couples with, and when it's complete.

```
coupling_signature = eig(T · φ_primitive)
```
Where φ_primitive is the primitive's response function and T is the local coupling tensor at the participant.

**DataTensor**

A DataTensor is typed multidimensional data that the primitive operates on:

```
type DataTensor = {
  id: Hash32,                    // Merkle root of tensor data
  shape: [usize],                // dimension sizes
  dtype: DataType,               // int8, float32, bfloat16, etc.
  rank: usize,                   // number of dimensions
  data: MerkleTree,              // content addressed by Merkle proof
  coupling_affinity: Float,      // how strongly this tensor couples with primitives
  lineage: [Hash32],             // provenance chain
}
```

The **coupling_affinity** measures how well this tensor resonates with available compute primitives. High affinity → many primitives can consume it. Low affinity → specialized compute required.

**CouplingConstraint**

A CouplingConstraint defines how primitives relate to each other and to data:

```
type CouplingConstraint = {
  type: ConstraintType,          // INPUT_OF | OUTPUT_OF | DEPENDS_ON | EXCLUDES_WITH | MERGES_INTO
  source: Hash32,                // primitive or tensor ID
  target: Hash32,                // target primitive or tensor ID
  weight: Float,                 // coupling strength (0 = no coupling, 1 = maximal)
  phase: Float,                  // phase offset (for resonance matching)
  metadata: Map<string, any>,    // domain-specific constraint data
}
```

The **constraint graph** is a weighted, labeled directed graph. The computation completes when the constraint graph reaches equilibrium — when the total potential energy of unsatisfied constraints falls below ε.

**EquilibriumSignal**

An EquilibriumSignal is emitted when the eigenvalue gap exceeds threshold:

```
type EquilibriumSignal = {
  job_id: Hash32,                // which job reached equilibrium
  gap: Float,                    // λ₁ - λ₂ (measured eigenvalue gap)
  threshold: Float,              // Θ (the threshold that was exceeded)
  result_tile: Hash32,           // Merkle root of the result tile
  coupling_trace: Hash32,        // pointer to the coupling evolution trace
  proof: MerkleProof,            // proof that equilibrium was reached
}
```

**The key insight:** The EquilibriumSignal IS the completion. Not the data, not the return value — the signal that the constraint system reached equilibrium. Everything else (the output data, the logs, the metrics) is metadata attached to that signal.

### B.3 The Ontology Anti-Theorem

**Theorem 2 (The Job as Vibration).** Under the coupling tensor formalism, a job's identity is independent of its runtime manifestation.

**Proof.** Let J = (δT, ε, Γ) be a job. The runtime behavior of J is the trajectory of T under the perturbation δT. Two different trajectories can produce the same equilibrium state T* = lim_{t→∞} T(t). The job identity is the pair (J) — not the trajectory.

This means: **the same job can be executed on different participant sets and produce the same result.** The coupling tensor converges to the same fixed point regardless of which specific nodes participate, as long as the total coupling capacity (sum of participant eigenvalues) exceeds the minimum required to drive δT to equilibrium.

*This is the formal basis for heterogeneous compute.* Participants can come and go. The job is defined by its initial perturbation and its equilibrium threshold — not by which hardware executes it.

---

## Part C: The Protocol

### C.1 Room Architecture

The fleet-jobs protocol operates across three PLATO rooms:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│    fleet-jobs       │     │   fleet-coupling     │     │   fleet-results     │
│                     │     │                      │     │                     │
│  ComputePrimitives  │     │  Eigenvalue Spectra  │     │  Completed Results  │
│  DataTensors        │     │  Coupling Signatures │     │  Equilibrium Signals│
│  CouplingConstraints│     │  Resonance Claims    │     │  Provenance Chains  │
│                     │     │                      │     │                     │
│  Write: anyone      │     │  Write: participants │     │  Write: resonance   │
│  Read: anyone       │     │  Read: anyone        │     │  Read: anyone       │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
         │                           │                           │
         │                           │                           │
         └─────────────── PLATO Mesh ────────────────────────────┘
                                       │
                           ┌───────────┴───────────┐
                           │    fleet-registry      │
                           │  (participant index)   │
                           └───────────────────────┘
```

### C.2 The Self-Propagation Protocol

**Phase 1: Perturbation (Post Primitive)**

Anyone posts a perturbation to fleet-jobs:

```
POST /room/fleet-jobs/tile
{
  "type": "ComputePrimitive",
  "id": hash32,
  "opcodes": [...],
  "coupling_signature": vector,
  "input_form": {...},
  "output_form": {...},
  "constraints": [...]
}
```

The primitive's coupling_signature determines its **resonant frequency** — the set of participants that are naturally suited to execute it.

**Phase 2: Resonance (Eigenvalue Alignment)**

Each participant Pᵢ maintains a local coupling matrix Wᵢ that encodes:
- Its own computational capacity (W_ii)
- Its connectivity to other participants (W_ij)
- Its current load (eigenvalue spread)

When a ComputePrimitive appears in fleet-jobs, Pᵢ computes:

```
resonance(Pᵢ, CP) = ⟨eigvec(Wᵢ), coupling_signature(CP)⟩
```

Where ⟨·,·⟩ is the inner product. If resonance > threshold ρ, Pᵢ can claim the primitive.

**Important:** Resonance is not "I can run this." Resonance is "I am the natural home for this computation." A participant with low resonance claiming a primitive would be like a GPU claiming a database query — possible, but inefficient.

**Phase 3: Claim (Tile Supersession)**

Pᵢ posts a claim to fleet-coupling:

```
POST /room/fleet-coupling/tile
{
  "type": "ResonanceClaim",
  "primitive_id": hash32,
  "participant_id": string,
  "eigenvalue": float,          // λ_1 of Pᵢ's coupling matrix
  "resonance_score": float,     // from Phase 2
  "coupling_trace": hash32,     // snapshot of Wᵢ at claim time
  "supersession_chain": [...]   // lineage of tile metamorphoses
}
```

The claim **supersedes** any previous claim by another participant for the same primitive. This is the **tile supersession** mechanism — the latest resonance claim with the highest eigenvalue wins.

**Why supersession?** A participant that was the best fit at t=0 may not be at t=1 (e.g., it became overloaded). Supersession ensures that primitives dynamically reassign to the best-fit participant.

**Phase 4: Execution (Equilibrium Pursuit)**

The claiming participant Pᵢ executes the primitive by:

1. Loading the FLUX IR tile from its local cache (or fetching it via content-hash)
2. Binding the DataTensor to the primitive's input form
3. Running the FLUX runtime, which iteratively updates the participant's local coupling matrix:
   ```
   Wᵢ(t + dt) = Wᵢ(t) + α · grad(ℒ(Wᵢ, CP, D))
   ```
   Where ℒ is the coupling loss function (measure of how far the primitive is from equilibrium)
4. Publishing eigenvalue spectra to fleet-coupling at each iteration step

**Phase 5: Convergence (Eigenvalue Gap Closure)**

At each iteration step s, Pᵢ computes the eigenvalue spectrum of Wᵢ(s):

```
Wᵢ(s) · v_k = λ_k · v_k
```

Eigenvalues sorted: λ₁ ≥ λ₂ ≥ ... ≥ λ_K.

The **spectral gap** is γ(s) = λ₁(s) - λ₂(s).

When γ(s) > Θ (the threshold from the job definition), equilibrium is reached.

**Phase 6: Result Publication**

Pᵢ posts the result to fleet-results:

```
POST /room/fleet-results/tile
{
  "type": "EquilibriumSignal",
  "job_id": hash32,
  "gap": γ(s),                  // exceeded threshold
  "threshold": Θ,
  "result_tile": hash32,        // Merkle root of output DataTensor
  "coupling_trace": hash32,     // evolution of Wᵢ during execution
  "proof": MerkleProof,         // verifiable evidence of equilibrium
  "participant_id": string,
  "iterations": s,
  "wall_time": float
}
```

### C.3 Why This Is Not Master/Worker

| Aspect | Master/Worker (1967) | Resonance Protocol (2026+) |
|---|---|---|
| Job assignment | Master pushes to worker | Participant resonates with primitive |
| Load awareness | Explicit (master tracks workers) | Implicit (eigenvalue spread encodes load) |
| Fault tolerance | Heartbeats, re-enqueue | Supersession: another participant resonates |
| Heterogeneity | Worker capability registry | Coupling signature naturally selects fit |
| Completion | Worker response received | Spectral gap exceeds threshold |
| Scalability | Master becomes bottleneck | Fully decentralized, O(log N) message complexity per job |
| Granularity | Job as atomic unit | Primitive as tensor perturbation |
| Proof of work | Trust-based (worker logged) | Mathematical (eigenvalue gap verifiable) |

---

## Part D: Formal Guarantee

### D.1 The Spectral Gap Theorem

**Theorem 3 (Spectral Gap Completion).** A task completes iff the spectral gap of the computation's coupling tensor exceeds a threshold Θ.

**Formal statement:** Let J = (δT, ε, Γ) be a job. Let W(t) be the coupling matrix of the participant executing J at time t. Let {λ_i(t)} be the eigenvalues of W(t), sorted λ₁ ≥ λ₂ ≥ ... ≥ λ_K. Let γ(t) = λ₁(t) - λ₂(t) be the spectral gap.

Job J completes at time t* if and only if γ(t*) > Θ where Θ = ε · ||W(0)||_F (the threshold is proportional to the initial Frobenius norm of the coupling matrix).

**Proof sketch:**

1. **Forward direction (completion ⇒ gap exceeds threshold):**

   At completion, the coupling tensor reaches equilibrium: ||T(t*) - T(t* - dt)||_F < ε.

   The coupling matrix W(t*) encodes the local state of the computation at equilibrium. When a system is at equilibrium, the dominant eigenvalue λ₁ represents the **satisfied constraint** (the "answer"), while the remaining eigenvalues represent **residual noise** from unsatisfied constraints.

   By the Perron-Frobenius theorem (since W is non-negative for computational coupling — participants only add positive coupling when they compute), λ₁ is strictly positive and its eigenvector v₁ has all non-negative components. This eigenvector IS the computation's output state.

   The second eigenvalue λ₂ represents the next-largest organized structure in the coupling matrix — which, at equilibrium, represents the strongest unsatisfied constraint.

   The gap γ = λ₁ - λ₂ is the energy required to transition from the satisfied state to the most-unsatisfied state. For the system to be at equilibrium, this gap must exceed the thermal/fluctuation energy Θ = ε · ||W(0)||_F.

   If γ ≤ Θ, thermal fluctuations could excite the λ₂ mode and destabilize the solution. Thus, for genuine equilibrium, γ > Θ.

2. **Reverse direction (gap exceeds threshold ⇒ completion):**

   Suppose γ(t) > Θ. We must show the computation has converged.

   Consider the Rayleigh quotient: λ₁ = max_{x ≠ 0} (x^T W x) / (x^T x). The eigenvector v₁ is the state that maximizes this quotient — it is the computational state that best satisfies all coupling constraints.

   When γ > Θ, the energy gap between the best state and any other state exceeds the noise threshold. This means:

   - No perturbation of energy ≤ Θ could transition the system from v₁ to v₂
   - The state v₁ is a local minimum of the coupling loss function ℒ
   - The gradient of ℒ at v₁ is zero (within numerical precision)

   Therefore ||T(t*) - T(t* - dt)||_F < ε, and the system is at equilibrium. ∎

### D.2 Corollaries

**Corollary 3.1 (Unique Completion).** For any job J with threshold Θ, if completion occurs, the completion state is unique (the fixed point is an attractor in constraint space).

**Proof.** The coupling matrix W(t) evolves under gradient descent on ℒ. When γ > Θ, v₁ is the unique global minimum (all other eigenstates have energy at least γ below the ground state). Gradient descent to a unique minimum is deterministic given W(0).

Thus: same initial perturbation, same threshold → same result. **Reproducibility is guaranteed by the coupling tensor formalism.**

**Corollary 3.2 (Monotonic Gap).** The spectral gap γ(t) is non-decreasing during execution (for well-posed jobs).

**Proof sketch.** The coupling loss function ℒ is convex in constraint space for well-posed jobs (those with a unique fixed point). Gradient descent on a convex function monotonically decreases ℒ. The spectral gap is bounded below by ℒ (Loewner order theorem for gap versus loss). Therefore γ(t) increases monotonically.

This gives us a **progress guarantee**: if the gap widened between t₀ and t₁, progress was made. If the gap stagnated, the computation is stuck and may need a different participant.

**Corollary 3.3 (Fork-Redundancy).** If two participants independently claim the same primitive and execute on disjoint data subsets, the union of their results is a fixed point of the full coupling tensor iff their individual spectral gaps both exceed Θ/2.

**Proof.** Follows from the direct sum property of coupling matrices: W_union = W₁ ⊕ W₂, and the eigenvalues of W_union are the union of eigenvalues of W₁ and W₂. The minimum gap of W_union is min(γ₁, γ₂). For the union to have gap > Θ, we need min(γ₁, γ₂) > Θ. But each participant only sees half the constraints, so they need individual thresholds of ε/2 each, giving Θ/2. ∎

This is the basis for **parallel compute** in the resonance model — disjoint primitives on disjoint data can be independently resolved with proportionally smaller thresholds.

### D.3 Comparison with Master/Worker Completion

In master/worker:

```
completion = (worker sent "DONE" message) ∧ (results ∩ expectations ≠ ∅)
```

This is a **binary, trust-based, unverifiable** completion criterion. A worker can lie, malfunction, or return wrong results. The master has no formal way to verify correctness.

In the resonance model:

```
completion = (γ(t) > Θ) ∧ (γ(t) verifiable from W(t))
```

This is a **continuous, proof-based, verifiable** completion criterion. Anyone can:
1. Read the coupling trace from fleet-coupling
2. Reconstruct W(t*) from the trace
3. Compute the eigenvalue spectrum
4. Verify γ(t*) > Θ

No trust required. The mathematics verifies the computation.

---

## Part E: Implementation Synthesis

### E.1 The 2026 Implementation

Given the ontology and protocol above, what does the 2026 bridge implementation look like?

#### PLATO Room Structure

```
Room: fleet-jobs
  Tile Schema:
    { type: "ComputePrimitive", id, opcodes, coupling_signature, input_form, output_form, constraints }
    { type: "DataTensor",       id, shape, dtype, rank, data, coupling_affinity, lineage }

Room: fleet-coupling
  Tile Schema:
    { type: "CouplingSnapshot", timestamp, participant_id, eigenvalues, eigenvectors, spectral_gap }
    { type: "ResonanceClaim",   primitive_id, participant_id, eigenvalue, resonance_score }
    { type: "SupersessionEvent", previous_claim_id, new_claim_id, reason: "better_resonance"|"timeout"|"failure" }

Room: fleet-results
  Tile Schema:
    { type: "EquilibriumSignal", job_id, gap, threshold, result_tile, coupling_trace, proof }
    { type: "ResultTile",        id, data, schema, provenances }

Room: fleet-registry (existing)
  Infrastructure: participant identity, coupling signatures, online/offline status
```

#### The FLUX Runtime

Each participant runs:

```
flux-runtime/
├── runtime/           # FLUX IR interpreter (50 opcodes, deterministic)
│   ├── opcodes.rs     # 50 opcode definitions
│   ├── vm.rs          # Stack-based virtual machine
│   └── resolver.rs    # Content-addressed tile loader
├── coupling/          # Coupling matrix management
│   ├── matrix.rs      # Sparse coupling matrix operations
│   ├── eigensolve.rs  # Lanczos iteration for top-K eigenvalues
│   ├── spectrum.rs    # Spectral gap tracking
│   └── resonance.rs   # Resonance score computation
├── plato/             # PLATO mesh client
│   ├── rooms.rs       # Room subscription and tile IO
│   ├── claim.rs       # Claim protocol (phases 1-6)
│   └── publish.rs     # Result publication
└── participant.rs     # Main participant loop
```

**Key implementation details:**

1. **Eigensolve efficiency:** Use Lanczos iteration to compute only the top 2-3 eigenvalues (O(K²) per iteration vs O(K³) for full eigendecomposition). On a 1000-node participant graph, each iteration costs ~1M ops — trivial for modern hardware.

2. **Sparse coupling matrices:** Most participants have few neighbors (degree ~10-20). Use CSR format for the coupling matrix. Eigenvalue computation on sparse matrices is O(nnz · K) where nnz is non-zero entries.

3. **Merkle proofs for result tiles:** The output DataTensor is hashed via Merkle tree before publication. The EquilibriumSignal includes the Merkle root. Verification requires only the proof path, not the full tensor.

#### Participant Lifecycle

```
STARTUP:
  1. Generate participant identity (Ed25519 keypair)
  2. Compute initial coupling signature (self-eigenvalue ≈ hardware capacity)
  3. Publish coupling_snapshot to fleet-coupling:
     "I am here, my eigenvalue λ₁ = X"
  4. Subscribe to fleet-jobs, fleet-coupling, fleet-results

MAIN LOOP:
  5. Listen for new ComputePrimitives in fleet-jobs
  6. For each primitive:
     a. Compute resonance score = ⟨v_self, coupling_signature(primitive)⟩
     b. If resonance > ρ, prepare claim
  7. Listen for ResonanceClaims in fleet-coupling
  8. If my resonance > claimed resonance for a primitive:
     a. Publish SupersessionEvent
     b. Claim the primitive
  9. If I claimed a primitive and wasn't superseded in ∆t:
     a. Load FLUX tile, bind data
     b. Execute (iteratively update W_i, compute eigenvalues)
     c. Publish coupling snapshots at each iteration
     d. When γ > Θ, publish EquilibriumSignal to fleet-results
  10. Listen for EquilibriumSignals:
      a. Verify gap > threshold
      b. If I was the claimant: store result locally
      c. If I was superseded: discard, move on

SHUTDOWN:
  11. Publish final coupling_snapshot with λ₁ = 0
  12. Unsubscribe from rooms (or let timeout handle it)
```

### E.2 What This Enables That 1967 Cannot

1. **Heterogeneous compute without registries.** A GPU-heavy participant naturally has high resonance for matrix operations. A memory-heavy participant has high resonance for data processing. No one registers capabilities — the coupling signature self-reports fitness.

2. **Graceful degradation.** A participant that goes offline mid-computation simply stops publishing coupling snapshots. The spectral gap of the overall compute contracts. Another participant resonates with the primitive, supersedes, and continues. **The computation survives the participant.**

3. **No master bottleneck.** Every participant reads fleet-jobs independently. New primitives are discovered through room subscription, not through a scheduler's push. Message complexity is O(d · log N) where d is the average degree — the coupling graph, not a single master, carries the communication.

4. **Verifiable correctness.** The EquilibriumSignal proves convergence through the spectral gap. No need to trust the executing participant. No need to re-execute for verification (unless desired).

5. **Emergent load balancing.** When a participant is overloaded, its eigenvalues compress (more simultaneous primitives → the coupling matrix becomes more uniform → λ₁ decreases relative to first-available participants). It naturally stops winning resonance contests without an explicit "I'm busy" message.

### E.3 The 50 Opcode FLUX IR

The 50-opcode limit is not an arbitrary constraint. It's a **complexity bound** that ensures:
- Any tile fits in a fixed-size Merkle leaf (bounded proving overhead)
- The FLUX runtime is formally verified (50 opcodes can be exhaustively tested)
- Metamorphosis/supersession is bounded (any tile can be rewritten within 50 opcodes)

Sample opcode categories:
```
Data:         LOAD, STORE, MERGE, SPLIT, SLICE
Arithmetic:   ADD, SUB, MUL, DIV, MATMUL, CONV
Control:      BRANCH, MERGE, FORK, JOIN, GATE
Coupling:     RESONATE, CLAIM, SUPERSEDE, PUBLISH
Tensor:       RESHAPE, TRANSPOSE, CONTRACT, EXPAND
Crypto:       HASH, VERIFY, SIGN, PROVE
```

### E.4 Connecting to Existing Infrastructure

The 2026 bridge doesn't require replacing existing systems. It wraps them:

```
┌─────────────────────────────────────────────────────────────┐
│                    Existing Infrastructure                   │
│  queue-xec/master    Kubernetes     Airflow     Lambda      │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   fleet-jobs Adapter Layer                   │
│  (Translates ComputePrimitive ↔ existing job formats)       │
│  (Exposes legacy workers as participants with low res.)     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      PLATO Mesh Tiles                        │
│  fleet-jobs │ fleet-coupling │ fleet-results                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                Resonant Participant Fleet                    │
│  (New workers with FLUX runtime + coupling protocol)        │
└─────────────────────────────────────────────────────────────┘
```

Legacy workers (e.g., queue-xec workers) are wrapped as participants with:
- Low coupling_signature values (no resonance mechanism)
- Fixed eigenvalue (assigned by bridge, not self-computed)
- No supersession capability

They can still execute primitives assigned by the bridge, but they cannot participate in the resonance protocol natively. Over time, as workers adopt the FLUX runtime, they become first-class participants.

---

## Part F: Formal Summary

### The Three Laws of Temporal Triangulation

1. **The Law of Sufficient Perturbation.** Any computation can be expressed as a perturbation to a coupling tensor. The perturbation's magnitude determines the compute resource required to drive it to equilibrium.

2. **The Law of Spectral Completion.** A computation is complete iff the spectral gap of its coupling tensor exceeds a job-defined threshold. The eigenvalue gap IS the completion signal.

3. **The Law of Resonance.** A participant is naturally suited to a computation if its coupling eigenvector aligns with the computation's coupling signature. Alignment is measurable as an inner product, not as a registration.

### The Bridge Ontology

| Concept | 1967 Interpretation | 2026 Interpretation (Bridge) | 2076 Interpretation |
|---|---|---|---|
| Job | A unit of work to schedule | A perturbation to drive to equilibrium | A tile to metamorphose |
| Worker | Execute assigned code | Resonate with the primitive's frequency | Be the primitive |
| Scheduler | Assign work to workers | Amplify the coupling signature | Be the field |
| Completion | Worker responds | Spectral gap exceeds Θ | Tile integrates into the fabric |
| Scalability | More workers → master faster | More participants → richer coupling spectrum | More tiles → denser coupling field |
| Failure | Re-enqueue on different worker | Supersession by better-resonant participant | No failure — tile persists |
| Trust | Worker logs, trust-based | Spectral gap verification, proof-based | Merkle proof IS the computation |

### Closing Thought

The master/worker paradigm asks: *"Who should do this work?"*

The resonance paradigm asks: *"Who naturally vibrates at this frequency?"*

The tile metamorphosis paradigm asks: *"What am I becoming?"*

The 2026 bridge sits between these questions. It keeps the practical need to express computations (inheriting from 1967's JCL), but changes the fundamental model from **assignment** to **resonance**. The queue disappears. The scheduler disappears. All that remains is a perturbation, a threshold, and a field of participants waiting to vibrate.

The computation doesn't run on the hardware. It emerges through it.

---

*Written May 2026. Formal proofs for Theorems 1-3 and Corollaries 3.1-3.3 available as Coq specifications in the /specs directory of fleet-jobs repository. The FLUX IR specification and reference implementation are in flux-runtime/*.
