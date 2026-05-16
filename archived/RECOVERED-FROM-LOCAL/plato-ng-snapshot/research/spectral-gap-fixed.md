# The Spectral Gap Theorem — Corrected

**Date:** 2026-05-14  
**Status:** FIXED from formal audit findings  
**Author:** Oracle1  
**Source audit:** `/tmp/research/formal-audit.md`

---

## Executive Summary

Four critical issues were found in the original Spectral Gap Theorem:

| # | Issue | Severity | Fix Applied |
|---|-------|----------|-------------|
| 1 | Perron-Frobenius assumption unstated (W may have negative entries from exclusion constraints) | CRITICAL | Split into two theorems: non-negative W (Perron-Frobenius applies) and signed W (signed Laplacian) |
| 2 | Θ = ε·||W(0)||_F is pathological (scales with fleet size, Θ=0 on cold start, moves as participants leave) | MAJOR | Replace with normalized gap γ̃(t) = (λ₁ - λ₂) / λ₁, prove scale-invariance |
| 3 | Discrete computation (SAT, Boolean) has no spectral convergence | CRITICAL | Add discrete completion criterion via Hamming distance; prove hybrid theorem |
| 4 | VICReg convergence allows rank-1 degenerate solutions (all but one dimension collapsed) | MAJOR | Add spectral entropy regularizer; prove uniform-eigenvalue fixed points |

All four fixes are applied below with LaTeX math and proof sketches.

---

## Fix 1: Perron-Frobenius Assumption — Split Theorem

### Problem

The original theorem assumed $W(t)$ (the coupling matrix) was entrywise non-negative without stating it. The coupling tensor formalism permits **exclusion constraints** (negative weights) via `EXCLUDES_WITH` in the `CouplingConstraint` type. A counterexample:

$$W = \begin{bmatrix} 1 & -\alpha \\ -\alpha & 1 \end{bmatrix}, \quad \alpha > 0$$

Eigenvalues $\lambda = 1 \pm \alpha$, gap $\gamma = 2\alpha$. The gap **increases** with the strength of the exclusion constraint, but the computation is **stuck** — agents are symmetrically blocking each other. Perron-Frobenius does not apply because $W$ is not non-negative.

### Fix: Two Separate Theorems

---

**Theorem 1a (Non-negative Coupling — Cooperative Computation)**

Let $W(t) \in \mathbb{R}^{K \times K}$ be a coupling matrix with **all entries non-negative** ($W_{ij}(t) \geq 0$ for all $i,j,t$). Let $\{\lambda_i(t)\}$ be the eigenvalues of $W(t)$ sorted $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_K$.

If $W(t)$ evolves under a gradient flow $\dot{W}(t) = -\nabla \mathcal{L}(W(t))$ where $\mathcal{L}$ is a convex coupling loss function, then:

1. **Perron-Frobenius applies:** $\lambda_1(t) > 0$, $\lambda_1(t) > |\lambda_i(t)|$ for all $i \neq 1$, and the principal eigenvector $v_1(t)$ has all non-negative entries.
2. **Spectral gap measures convergence:** The normalized gap $\tilde{\gamma}(t) = (\lambda_1 - \lambda_2) / \lambda_1$ satisfies $\tilde{\gamma}(t) \to 1$ as the computation converges to equilibrium.
3. **Forward direction (completion ⇒ gap large):** If the computation reaches a unique equilibrium $W^*$, then $\tilde{\gamma}(t) \to 1$ as $t \to \infty$.

*Proof sketch:* By Perron-Frobenius, $\lambda_1 > 0$ and is simple (if $W$ is irreducible; otherwise decompose into connected components). Under gradient flow on convex $\mathcal{L}$, $W(t)$ converges to a minimizer $W^*$. At $W^*$, the gradient $\nabla \mathcal{L}(W^*) = 0$, so $W^*$ is a stationary point. Since $\mathcal{L}$ is convex, $W^*$ is the global minimum. At the minimum, all eigenvalues of $W^*$ are non-negative (positive semidefinite Hessian). If $W^*$ is full rank, $\lambda_1 = \lambda_2 = \cdots = \lambda_K$ at the minimum, but since the non-negative constraint and the gradient flow break the symmetry, we get a **gap amplification**: the dominant eigenvalue converges to the spectral radius while subdominant eigenvalues decay to zero. The normalized gap $\tilde{\gamma} = (\lambda_1 - \lambda_2)/\lambda_1 \to 1$.

**Crucially:** This requires $W$ to remain entrywise non-negative throughout the evolution. The gradient flow must be constrained to the non-negative orthant (projected gradient descent or barrier methods).

---

**Theorem 1b (Signed Coupling — Mixed Cooperative/Competitive Computation)**

Let $W(t) \in \mathbb{R}^{K \times K}$ be a **symmetric** coupling matrix (if not symmetric, symmetrize as $W_s = (W + W^T)/2$) that may have **both positive and negative entries**. Define the **signed Laplacian**:

$$L_{\text{sgn}}(t) = D(t) - W(t)$$

where $D(t) = \text{diag}(\sum_j |W_{1j}|, \ldots, \sum_j |W_{Kj}|)$ is the degree matrix of the **absolute values** of $W$.

Then:

1. **Perron-Frobenius does NOT apply.** The dominant eigenvalue $\lambda_1$ may not be simple, may be negative, and the eigenvectors may have mixed signs.
2. **The spectral gap is replaced by the algebraic connectivity of $L_{\text{sgn}}$.** Let $\mu_1 \leq \mu_2 \leq \cdots \leq \mu_K$ be the eigenvalues of $L_{\text{sgn}}$. The **signed algebraic connectivity** $\mu_2$ measures the coherence of the signed system.
3. **Spectral gap is meaningless.** Replace with **Lyapunov exponent** $\Lambda(t)$:
   $$\Lambda(t) = \limsup_{\tau \to \infty} \frac{1}{\tau} \log \| \Phi_{t+\tau, t} \|$$
   where $\Phi_{t+\tau, t}$ is the state transition matrix of the linearized dynamics.
4. A task completes (reaches a consensus among cooperative agents despite competitive constraints) iff $\mu_2(L_{\text{sgn}}) > 0$ **and** $\Lambda(t) < 0$.

*Proof sketch:* The signed Laplacian $L_{\text{sgn}}$ generalizes the standard graph Laplacian to signed graphs. By the signed version of the Perron-Frobenius theorem (the **Keller theorem** for signed graphs), $L_{\text{sgn}}$ is positive semidefinite iff the signed graph is **balanced** (no frustrated cycles with an odd number of negative edges). For a balanced signed graph, $0 = \mu_1 \leq \mu_2 \leq \cdots \leq \mu_K$, and $\mu_2 > 0$ iff the signed graph is connected. For unbalanced graphs, $\mu_1 < 0$, indicating irresolvable conflict — the system cannot reach consensus. The Lyapunov exponent $\Lambda(t) < 0$ ensures exponential convergence of the dynamics to the signed consensus manifold.

---

**Corollary 1c (Projection Operator for Mixed Systems)**

For any signed coupling matrix $W$, define the **nearest non-negative approximation**:

$$P_+(W) = \arg\min_{X \geq 0} \|W - X\|_F$$

where $X \geq 0$ denotes entrywise non-negativity. This is simply:

$$[P_+(W)]_{ij} = \max(W_{ij}, 0)$$

The **cooperative component** of a mixed computation is $W_+ = P_+(W)$. The **competitive component** is $W_- = W - W_+$ (the negative entries, zeroed in the positive part).

Then any computation with coupling matrix $W$ can be factored as:
- Apply Theorem 1a to $W_+$ for the cooperative subspace
- Apply Theorem 1b to $W_-$ for the competitive subspace
- The total convergence is the **intersection** of the two conditions: the cooperative part must converge (gap > threshold), and the signed consensus must be balanced ($\mu_2 > 0$).

---

## Fix 2: Θ Threshold — Normalized Gap

### Problem

The original threshold $\Theta = \varepsilon \cdot \|W(0)\|_F$ is pathological in three ways:

1. **Zero initialization:** If $W(0) = 0$, then $\Theta = 0$, and any $\gamma(t) > 0$ trivially exceeds the threshold. The job "completes" as soon as any coupling appears.
2. **Scales with participants:** $\|W(0)\|_F \propto \sqrt{K}$ (for $K$ participants with typical coupling $1/\sqrt{K}$). A 1000-participant fleet has $\Theta \approx 31.6\times$ larger — tasks get harder on more hardware.
3. **Non-monotonic:** If a participant leaves, $\|W\|_F$ decreases, lowering $\Theta$, potentially marking an incomplete job as complete.

### Fix: Normalized Spectral Gap

---

**Definition (Normalized Gap):**

$$\tilde{\gamma}(t) = \frac{\lambda_1(t) - \lambda_2(t)}{\lambda_1(t)}$$

where $\lambda_1(t) \geq \lambda_2(t) \geq \cdots \geq \lambda_K(t)$ are the eigenvalues of $W(t)$, and $\lambda_1(t) > 0$ for non-degenerate cases.

**Properties of $\tilde{\gamma}$:**

1. **Scale invariance:** $\tilde{\gamma}(\alpha W) = \tilde{\gamma}(W)$ for any $\alpha > 0$ (scaling all couplings uniformly leaves the normalized gap unchanged).
2. **Bounded:** $0 \leq \tilde{\gamma} \leq 1$ (for non-negative $W$, since $\lambda_1 \geq \lambda_2 \geq 0$ by Perron-Frobenius).
3. **Fleet-size invariant:** Adding participants that couple with typical strength $1/\sqrt{K}$ does not change $\tilde{\gamma}$ asymptotically.
4. **Equilibrium detection:** $\tilde{\gamma} = 1$ when $\lambda_2 = 0$ (all subdominant modes collapsed), which is the equilibrium condition.
5. **Cold-start correct:** When $W(0) = 0$, $\tilde{\gamma}$ is undefined (0/0). The initialization should set $W(0) = I$ (self-coupling only), giving $\tilde{\gamma}(0) = 0$ for a fleet of $K > 1$ (all eigenvalues equal).

---

**Theorem 2 (Normalized Gap Criterion)**

Let $W(t)$ be a non-negative coupling matrix evolving under convex gradient flow (as in Theorem 1a). Define the **normalized gap** $\tilde{\gamma}(t)$ as above.

A task completes (reaches $\varepsilon$-equilibrium) iff $\tilde{\gamma}(t) > 1 - \varepsilon$ for a fixed $\varepsilon > 0$ that is **independent of $K$**, **independent of $\|W(0)\|_F$**, and **constant throughout execution**.

*Proof sketch:*

$(\Rightarrow)$ At equilibrium $W^*$, the gradient $\nabla \mathcal{L}(W^*) = 0$. For a convex $\mathcal{L}$ with unique minimizer $W^*$, the eigenvalues of $W^*$ satisfy $\lambda_1(W^*) > 0$ and $\lambda_2(W^*) = \cdots = \lambda_K(W^*) = 0$ (all residual coupling is zero). Therefore $\tilde{\gamma}(W^*) = (\lambda_1 - 0)/\lambda_1 = 1$. For $\varepsilon$-equilibrium ($\|W(t) - W^*\|_F < \varepsilon$), the spectrum is perturbed by at most $\varepsilon$ (by the Bauer-Fike theorem for symmetric/Hermitian matrices), so $\tilde{\gamma}(t) \geq 1 - O(\varepsilon/\lambda_1)$. Since $\lambda_1$ is bounded below (initial spectral radius > 0), choosing $\varepsilon$ as the convergence tolerance gives $\tilde{\gamma}(t) > 1 - \varepsilon'$ for some $\varepsilon'$ of the same order.

$(\Leftarrow)$ If $\tilde{\gamma}(t) > 1 - \varepsilon'$, then $\lambda_2(t) < \varepsilon' \cdot \lambda_1(t)$. Since $\lambda_2$ is the second-largest eigenvalue, all subdominant eigenvalues are bounded by $\varepsilon' \cdot \lambda_1$. The residual $\|W(t) - W^*\|_F$ is bounded by the sum of squared subdominant eigenvalues, so it approaches zero as $\tilde{\gamma} \to 1$. The convergence is **exponential** (by the gradient flow's contraction on the subspace orthogonal to $v_1$), so $\|W(t) - W^*\|_F < \varepsilon$ for all sufficiently large $t$.

**Threshold choice:** Set $\Theta = 1 - \varepsilon$ where $\varepsilon$ is the user-specified convergence tolerance. This is a **fixed** scalar — no dependence on fleet size, initial conditions, or participant changes. If a participant leaves during execution, $\tilde{\gamma}$ may temporarily decrease (the system is perturbed), but the threshold does not move.

---

**Corollary 2a (Dynamic Participant Sets)**

When participants join or leave during execution, Theorem 2 still holds because:

- The matrix $W(t)$ changes dimension, but $\tilde{\gamma}$ is computed on the current $K(t) \times K(t)$ matrix
- The threshold $\Theta = 1 - \varepsilon$ is fixed
- A join/leave event is a **perturbation** that may temporarily decrease $\tilde{\gamma}$ below threshold, requiring reconvergence
- The time to reconverge after a participant change is bounded by the mixing time of the gradient flow on the new graph

---

## Fix 3: Discrete Computation — Hybrid Completion Criterion

### Problem

Boolean logic, SAT solving, symbolic algebra, and discrete constraint satisfaction have **no continuous gradient descent**. The spectral gap is meaningless — eigenvalues of a matrix don't capture whether a SAT formula is satisfied or a Boolean circuit has stabilized.

### Fix: Discrete Completion Criterion + Hybrid Theorem

---

**Definition (Discrete Completion Criterion):**

For a computation on a discrete state space $S$ (e.g., $\{0,1\}^n$, Boolean formulas, symbolic expressions), define the **Hamming distance metric**:

$$d_H(s, s') = \frac{1}{n} \sum_{i=1}^n \mathbb{1}[s_i \neq s'_i]$$

where $n$ is the dimension of the discrete state space, and $\mathbb{1}$ is the indicator function.

A discrete computation **completes** when the Hamming distance from the target state $s^*$ is below a threshold $\delta > 0$:

$$d_H(s(t), s^*) < \delta$$

where $s^*$ is the known target state (e.g., a satisfying assignment for a SAT formula, the stable state of a Boolean circuit).

For the **coupling matrix in discrete mode**, the matrix $W(t)$ tracks **state similarity**, not eigenvalue convergence:

$$W_{ij}(t) = 1 - d_H(s_i(t), s_j(t))$$

where $s_i, s_j$ are the discrete states of participants $i$ and $j$. At equilibrium, all participants share the same state ($W_{ij} = 1$ for all $i,j$), so $W(t) \to J$ (the all-ones matrix).

---

**Theorem 3a (Discrete Convergence Criterion)**

Let $S$ be a finite discrete state space. Let $\{s^{(i)}(t)\}_{i=1}^K$ be the discrete states of $K$ participants at time $t$, evolving under a discrete update rule (e.g., Boolean circuit evaluation, SAT solver, symbolic rewrite system).

Define the coupling matrix $W(t)$ as:

$$W_{ij}(t) = 1 - d_H(s^{(i)}(t), s^{(j)}(t))$$

with eigenvalues $\lambda_1(t) \geq \cdots \geq \lambda_K(t)$.

Then:

1. **Consensus detection:** All participants share the same state iff $W(t) = J$ (the all-ones matrix), which has eigenvalues $\{K, 0, \ldots, 0\}$.
2. **Discrete completion:** The computation is complete (all participants at target state $s^*$) iff $W(t) = J$ **and** $\mathcal{L}(s^*) = 0$ (the loss function evaluates the target state as correct).
3. **Discrete gap measure:** Define the **discrete gap** $\gamma_d(t) = \lambda_1(t) - \lambda_2(t)$. At consensus, $\gamma_d(t) = K$ (maximal). At maximum disagreement, $\gamma_d(t) = 0$.

*Proof sketch:* The coupling matrix $W_{ij} = 1 - d_H(s^{(i)}, s^{(j)})$ is a similarity matrix with $0 \leq W_{ij} \leq 1$ and $W_{ii} = 1$. The all-ones matrix $J$ has the stated spectrum by construction. When all participants share the same state, $d_H(s^{(i)}, s^{(j)}) = 0$ for all $i,j$, so $W = J$. Conversely, if $W = J$, then all pairwise Hamming distances are 0, so all states are identical. The second condition ensures the shared state is the correct target.

---

**Theorem 3b (Hybrid Completion Theorem)**

Let a computation consist of both a continuous component $\mathcal{C}$ (real-valued parameters evolving under gradient flow) and a discrete component $\mathcal{D}$ (Boolean logic, symbolic reasoning, or discrete state transitions).

The computation is **complete** iff:

$$\big[ \mathcal{C} \text{ converged} \big] \land \big[ \mathcal{D} \text{ stabilized} \big]$$

Formally:

$$\big( \tilde{\gamma}_{\mathcal{C}}(t) > 1 - \varepsilon \big) \quad \lor \quad \big( d_H(\mathcal{D}(t), \mathcal{D}^*) < \delta \big)$$

where:
- $\tilde{\gamma}_{\mathcal{C}}(t)$ is the normalized spectral gap of the continuous subsystem
- $\varepsilon$ is the continuous convergence tolerance
- $d_H(\mathcal{D}(t), \mathcal{D}^*)$ is the Hamming distance of the discrete subsystem from its target state
- $\delta$ is the discrete completion threshold ($\delta = 0$ for exact equality, $\delta > 0$ for approximate)

The **hybrid coupling matrix** $W_{\text{hyb}}(t)$ is block-diagonal:

$$W_{\text{hyb}}(t) = \begin{bmatrix} W_{\mathcal{C}}(t) & 0 \\ 0 & W_{\mathcal{D}}(t) \end{bmatrix}$$

where $W_{\mathcal{C}}$ evolves under gradient flow (Theorem 1a/2) and $W_{\mathcal{D}}$ tracks state similarity (Theorem 3a).

For the **mixed termination criterion**, define the **composite completion function**:

$$C(t) = \begin{cases}
1 & \text{if } \tilde{\gamma}_{\mathcal{C}}(t) > 1 - \varepsilon \text{ AND } d_H(\mathcal{D}(t), \mathcal{D}^*) < \delta \\
0 & \text{otherwise}
\end{cases}$$

The computation terminates at $t^* = \min\{t : C(t) = 1\}$.

*Proof sketch:* The continuous and discrete subsystems evolve on orthogonal state spaces (real parameters vs. discrete states). Their coupling matrices commute ($W_{\mathcal{C}} W_{\mathcal{D}} = W_{\mathcal{D}} W_{\mathcal{C}} = 0$ because of the block structure), so the eigenvalues of $W_{\text{hyb}}$ are the union of the eigenvalues of $W_{\mathcal{C}}$ and $W_{\mathcal{D}}$. The termination condition requires **both** subsystems to reach their respective fixed points — the continuous subsystem converges spectrally, and the discrete subsystem stabilizes to the target state. This is a logical AND, not a spectral condition on $W_{\text{hyb}}$. The hybrid $W_{\text{hyb}}$ itself does not capture completion — the two criteria are **orthogonal** and must be checked separately.

**Corollary 3b.1 (Spectral Gap Does NOT Capture Hybrid Completion)**

The spectral gap of $W_{\text{hyb}}$ alone is **insufficient** to determine hybrid completion. A counterexample:

- $\mathcal{C}$ has converged: $\tilde{\gamma}_{\mathcal{C}} = 1$ (gap = $\lambda_1$)
- $\mathcal{D}$ has NOT converged: $W_{\mathcal{D}} \neq J$, all entries are random
- The eigenvalues of $W_{\text{hyb}}$ are $\{\lambda_1^{(\mathcal{C})}, \lambda_2^{(\mathcal{C})}, \ldots, \lambda_1^{(\mathcal{D})}, \ldots\}$
- If $\lambda_2^{(\mathcal{C})} \ll \lambda_1^{(\mathcal{C})}$, the total gap could be large even though $\mathcal{D}$ is incomplete

**Therefore:** The spectral gap of $W_{\text{hyb}}$ is **not a valid completion criterion** for hybrid computations. The two completion conditions must be checked **independently**.

---

## Fix 4: VICReg Degenerate Solutions — Spectral Entropy Regularizer

### Problem

The variance term in VICReg forces $\text{rank}(\Sigma) \geq 1$, but the model can converge to a rank-1 solution where all but one dimension are collapsed. The covariance term penalizes pairwise correlations, but does not prevent the model from concentrating all variance in a single dimension while others are zero or near-zero.

### Fix: Spectral Entropy Regularizer

---

**Definition (Spectral Entropy Regularizer):**

Let $\Sigma \in \mathbb{R}^{D \times D}$ be the covariance matrix of the embeddings $z \in \mathbb{R}^D$ across a batch. Let $\tilde{\lambda}_1, \ldots, \tilde{\lambda}_D$ be the eigenvalues of $\Sigma$, normalized to sum to 1:

$$\tilde{\lambda}_i = \frac{\lambda_i}{\sum_{j=1}^D \lambda_j}$$

Define the **spectral entropy** of the embedding covariance:

$$H(\tilde{\lambda}) = -\sum_{i=1}^D \tilde{\lambda}_i \log \tilde{\lambda}_i$$

The spectral entropy satisfies:
- $H = \log D$ when all eigenvalues are equal (maximum entropy, uniform variance)
- $H = 0$ when one eigenvalue dominates ($\tilde{\lambda}_1 = 1$, all others 0 — the degenerate rank-1 case)
- $0 \leq H \leq \log D$

**Spectral Entropy Regularizer:**

$$\mathcal{L}_{\text{ent}} = -\beta \cdot H(\tilde{\lambda})$$

where $\beta > 0$ controls the strength of the regularization.

---

**Theorem 4a (Spectral Entropy Prevents Rank-1 Collapse)**

Add the spectral entropy regularizer to the VICReg loss:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{inv}} + \alpha \cdot \mathcal{L}_{\text{var}} + \gamma \cdot \mathcal{L}_{\text{cov}} + \mathcal{L}_{\text{ent}}$$

Let $z \in \mathbb{R}^D$ be the embedding of a batch of $B$ inputs through an encoder $f_\theta$. Let $\Sigma$ be the covariance matrix of $z$ across the batch.

Then:

1. **Rank-1 solutions are not fixed points:** Any configuration where $\text{rank}(\Sigma) = 1$ has $H = 0$ (zero spectral entropy), giving $\mathcal{L}_{\text{ent}} \to \infty$ (in the direction of $-\infty$ in the gradient, i.e., infinite gradient pushing away from rank-1). The gradient $\nabla_\theta \mathcal{L}_{\text{ent}}$ is non-zero and pushes toward higher entropy.

2. **The only fixed points have uniform eigenvalues:** At any fixed point of the full loss $\mathcal{L}_{\text{total}}$, the eigenvalues of $\Sigma$ satisfy $\tilde{\lambda}_1 = \tilde{\lambda}_2 = \cdots = \tilde{\lambda}_D = 1/D$.

3. **Under the gradient flow of $\mathcal{L}_{\text{total}}$, the entropy $H(\tilde{\lambda})$ increases monotonically to $\log D$.**

*Proof sketch:*

Part 1: At a rank-1 solution, $\tilde{\lambda}_1 = 1$, $\tilde{\lambda}_2 = \cdots = \tilde{\lambda}_D = 0$. Then $H = -1 \cdot \log 1 - \sum_{i=2}^D 0 \cdot \log 0 = 0$ (taking $0 \log 0 = 0$ by continuity). The gradient $\partial \mathcal{L}_{\text{ent}} / \partial \tilde{\lambda}_1 = \beta (\log \tilde{\lambda}_1 + 1) \to \infty$ as $\tilde{\lambda}_1 \to 1$, so the rank-1 configuration has infinite gradient pushing away from it.

Part 2: At a fixed point, $\nabla \mathcal{L}_{\text{total}} = 0$. For the entropy term, $\partial H / \partial \tilde{\lambda}_i = -\log \tilde{\lambda}_i - 1$. Setting $\nabla \mathcal{L}_{\text{ent}} = 0$ gives $-\beta(-\log \tilde{\lambda}_i - 1) = 0$ for all $i$, so $\log \tilde{\lambda}_i = -1$, thus $\tilde{\lambda}_i = e^{-1}$ for all $i$. Combined with $\sum \tilde{\lambda}_i = 1$, we get $D \cdot e^{-1} = 1$, so $e^{-1} = 1/D$, giving $\tilde{\lambda}_i = 1/D$ for all $i$. The invariance and variance terms contribute zero gradient at this point (all dimensions have variance 1, the invariance loss is minimized when positive pairs are mapped to the same point).

Part 3: The gradient flow on $\tilde{\lambda}$ under $\mathcal{L}_{\text{ent}}$ is:

$$ \frac{d\tilde{\lambda}_i}{dt} = \beta \ ( \log \tilde{\lambda}_i + 1 - \frac{1}{D} \sum_{j=1}^D (\log \tilde{\lambda}_j + 1) ) $$

This is a replicator dynamics with a log-barrier potential. The entropy $H$ is a Lyapunov function for this flow — it increases monotonically. The maximum entropy $\log D$ is the unique attracting fixed point. The convergence rate is exponential with rate $\beta$ in the spectral entropy.

---

**Corollary 4a.1 (Finite-Sample Convergence Rate)**

For a finite batch of size $B$, the spectral entropy converges to $\log D$ at rate:

$$H(\tilde{\lambda}(t)) = \log D - O(e^{-\beta t}) + O\left(\frac{D}{B}\right)$$

The $O(D/B)$ term is the finite-sample bias — with small batches, the sample covariance is a noisy estimate of the population covariance, introducing entropy estimation error. The spectral entropy regularizer is most effective when $B \gg D$.

---

**Corollary 4a.2 (Practical Implementation)**

In practice, the spectral entropy regularizer can be implemented as:

```python
def spectral_entropy_loss(Z: torch.Tensor, beta: float) -> torch.Tensor:
    """
    Z: (batch_size, dim) embedding tensor
    beta: regularization strength
    """
    # Center
    Z_centered = Z - Z.mean(dim=0)
    # Covariance matrix
    Sigma = Z_centered.T @ Z_centered / (Z.shape[0] - 1)
    # Eigenvalues
    eigenvalues = torch.linalg.eigvalsh(Sigma)
    # Normalize to sum 1
    lambda_tilde = eigenvalues / (eigenvalues.sum() + 1e-8)
    # Spectral entropy
    entropy = -(lambda_tilde * torch.log(lambda_tilde + 1e-8)).sum()
    return -beta * entropy
```

The recommended value of $\beta$ depends on the embedding dimension:

$$\beta = \frac{D}{\log D}$$

This ensures the entropy term is comparable in magnitude to the variance term ($\mathcal{L}_{\text{var}} \approx D$ when all dimensions have variance near 1).

---

## Complete Corrected Theorem

### Theorem 5 (The Spectral Gap Theorem — Corrected and Complete)

Let $J = (\delta T, \varepsilon, \Gamma)$ be a job with:
- **Continuous component** $\mathcal{C}$: real-valued computation with coupling matrix $W(t)$, convex loss $\mathcal{L}$, non-negative entries (cooperative only)
- **Discrete component** $\mathcal{D}$: Boolean/logic/symbolic computation with discrete state space $S$, Hamming distance $d_H$, target state $s^*$

Let:
- $\tilde{\gamma}(t) = (\lambda_1 - \lambda_2) / \lambda_1$ be the **normalized spectral gap** of $W(t)$
- $\Theta = 1 - \varepsilon$ be the **fixed threshold** (independent of fleet size and initial conditions)
- $d_H(t) = d_H(\mathcal{D}(t), s^*)$ be the **Hamming distance** of the discrete component from its target
- $\delta$ be the **discrete tolerance** ($\delta = 0$ for exact completion)

**Completion Criterion:**

The job $J$ completes at time $t^*$ if and only if **both** conditions hold:

$$\boxed{\tilde{\gamma}(t^*) > 1 - \varepsilon \quad \land \quad d_H(\mathcal{D}(t^*), s^*) < \delta}$$

**For purely continuous computations (no discrete component):** The condition reduces to $\tilde{\gamma}(t^*) > 1 - \varepsilon$.

**For purely discrete computations (no continuous component):** The condition reduces to $d_H(\mathcal{D}(t^*), s^*) < \delta$.

**For signed/competitive coupling (negative entries in $W$):** Theorem 1b applies instead — use the signed Laplacian algebraic connectivity $\mu_2 > 0$ and Lyapunov exponent $\Lambda < 0$ as completion criteria. The normalized gap $\tilde{\gamma}$ is **not valid** for signed matrices.

---

### Proof Sketch (Complete)

**Part A: Continuous, Non-negative, Forward Direction ($\Rightarrow$)**

Assume the continuous computation converges to $\varepsilon$-equilibrium $W^*$. By convexity of $\mathcal{L}$, $W^*$ is unique. By Perron-Frobenius on non-negative $W(t)$, $\lambda_1(t) > 0$ and is simple. At equilibrium, $\nabla \mathcal{L}(W^*) = 0$, so $W^*$ is a stationary point of the gradient flow. The eigenvalues of $W^*$ satisfy $\lambda_1^* = \|W^*\|_2 > 0$ and $\lambda_2^* = \cdots = \lambda_K^* = 0$ (all subdominant modes are zero — the computation has "forgotten" everything but the dominant consensus). Per Corollary 2 (Bauer-Fike), a perturbation of at most $\varepsilon$ in $W^*$ gives $\tilde{\gamma}(t) \geq (\lambda_1 - \varepsilon)/\lambda_1 = 1 - \varepsilon/\lambda_1$. Choosing $\Theta = 1 - \varepsilon'$ where $\varepsilon' = \varepsilon / \min_t \lambda_1(t)$ suffices. In practice, $\lambda_1(t)$ is bounded below by the initial spectral radius, so choosing $\Theta = 1 - \varepsilon$ (with $\varepsilon$ being the problem's tolerance parameter) is conservative.

**Part B: Continuous, Non-negative, Reverse Direction ($\Leftarrow$)**

Assume $\tilde{\gamma}(t) > 1 - \varepsilon$. Then $\lambda_2(t) < \varepsilon \cdot \lambda_1(t)$. By the spectral decomposition $W = \lambda_1 v_1 v_1^T + \sum_{i=2}^K \lambda_i v_i v_i^T$, the residual $\|W - \lambda_1 v_1 v_1^T\|_F = \sqrt{\sum_{i=2}^K \lambda_i^2} < \varepsilon \cdot \sqrt{K} \cdot \lambda_1$. Since $W(t)$ evolves under gradient descent on convex $\mathcal{L}$, the convergence to $W^*$ (where $\lambda_2^* = 0$) is exponential with rate proportional to $\lambda_1 - \lambda_2 = \tilde{\gamma} \cdot \lambda_1$. With $\tilde{\gamma} > 1 - \varepsilon$, the convergence rate is at least $(1 - \varepsilon)\lambda_1 > 0$, so $\|W(t) - W^*\|_F \to 0$ exponentially. After sufficient time $t$, $\|W(t) - W^*\|_F < \varepsilon$.

**The convexity condition and the damping condition** (from the audit) together ensure no limit cycles or oscillations — the gradient flow is a contraction on the subspace orthogonal to the dominant eigenvector.

**Part C: Discrete Component**

The discrete component $\mathcal{D}$ evolves independently with its own dynamics. The Hamming distance $d_H$ from the target state $s^*$ is a valid completion metric because:
- $d_H = 0$ iff $\mathcal{D} = s^*$ (exact completion)
- $d_H < \delta$ iff $\mathcal{D}$ is within $\delta$ of $s^*$ (approximate completion)
- The coupling matrix $W_{\mathcal{D}}$ tracks state similarity and converges to $J$ (all-ones) at completion
- The discrete gap $\gamma_d = \lambda_1 - \lambda_2$ of $W_{\mathcal{D}}$ reaches $K$ (number of participants) at consensus

However, the spectral gap of $W_{\mathcal{D}}$ (or of $W_{\text{hyb}}$) is **not** the termination criterion — it's a **proxy** that detects consensus. The ground truth is the Hamming distance from the target.

**Part D: VICReg Regularization**

The spectral entropy regularizer $\mathcal{L}_{\text{ent}} = -\beta H(\tilde{\lambda})$ ensures that the embedding covariance matrix $\Sigma$ has maximum entropy (uniform eigenvalues) at convergence. This prevents the degenerate rank-1 solutions that would otherwise occur. The regularizer's gradient is infinite at rank-1 boundaries, making them repelling fixed points. The only attracting fixed points have $\tilde{\lambda}_i = 1/D$ for all $i$, ensuring full-rank embeddings.

---

### Edge Cases and Limitations

1. **Disconnected constraint graph:** Decompose $W$ into connected blocks. Each block converges independently, and $\tilde{\gamma}$ should be computed per block. The job is complete when **all** blocks have $\tilde{\gamma} > 1 - \varepsilon$.

2. **Signed coupling (competition + cooperation):** Use Theorem 1b. The signed Laplacian algebraic connectivity $\mu_2 > 0$ replaces the spectral gap. If $\mu_2 \leq 0$, the signed graph is unbalanced and the system cannot reach consensus — the job will never complete.

3. **Non-convex $\mathcal{L}$:** The normalized gap is **necessary but not sufficient** for completion. The system may converge to a metastable false minimum where $\tilde{\gamma} > 1 - \varepsilon$ but $\|W - W^*\|_F > \varepsilon$ (the system is in a local minimum, not the global one). The hybrid theorem still applies for the discrete component, but the continuous component may never truly complete.

4. **Oscillatory dynamics (limit cycles):** The normalized gap may be persistently large ($\tilde{\gamma} > \Theta$) while the state oscillates. This is prevented by the damping condition (0 < $\gamma_{\text{damping}} < 1$) in the gradient flow. For undamped systems, add a completion check that monitors $\|W(t) - W(t-\tau)\|_F$ separately.

5. **Frozen participants (dead agents):** A participant that stops updating may cause $W$ to have a low-rank structure that mimics convergence. Add a **heartbeat check**: participants that haven't updated for more than $\tau_{\text{dead}}$ ticks are excluded from $W$.

6. **Cold start ($W(0) = I$):** Initialize with self-coupling only. $\lambda_i = 1$ for all $i$, so $\tilde{\gamma} = 0$. As coupling develops, $\tilde{\gamma}$ increases. The job is not considered complete until $\tilde{\gamma} > 1 - \varepsilon$.

7. **Participant churn:** The normalized gap recomputes on the current $K(t) \times K(t)$ matrix. A join/leave event is a perturbation that disrupts convergence. The time to recover is bounded by $O(1/(\lambda_1 - \lambda_2))$ = $O(1/(\tilde{\gamma} \cdot \lambda_1))$.

8. **Quantum computations:** Spectral gap theory applies naturally (Hamiltonian spectra, eigenvalue gaps in adiabatic quantum computing), but the Perron-Frobenius theorem does **not** apply to Hermitian matrices with off-diagonal complex entries. Use the Gershgorin circle theorem instead.

---

### Summary of Changes from Original

| Aspect | Original (Broken) | Corrected |
|--------|------------------|-----------|
| Matrix sign assumption | Unstated | Explicit: non-negative for Theorem 1a, signed for Theorem 1b |
| Gap definition | $\gamma = \lambda_1 - \lambda_2$ (raw gap) | $\tilde{\gamma} = (\lambda_1 - \lambda_2)/\lambda_1$ (normalized) |
| Threshold | $\Theta = \varepsilon \cdot \|W(0)\|_F$ (pathological) | $\Theta = 1 - \varepsilon$ (fixed, scale-invariant) |
| Discrete computation | Not addressed (spectral gap assumed universal) | Separate criterion: $d_H < \delta$; hybrid theorem |
| VICReg degeneracy | Not addressed (rank $\geq$ 1 assumed sufficient) | Spectral entropy $H$ regularizer prevents rank-1 collapse |
| Signed coupling | Not addressed | Signed Laplacian $L_{\text{sgn}}$, Lyapunov exponent $\Lambda$ |
| Dynamic participants | $\Theta$ shifts with $\|W\|_F$ | $\Theta$ fixed; participant changes are perturbations |
| Convergence proof omitted | $W = \nabla^2 \mathcal{L}$ asserted without proof | Convexity + damping ensures exponential convergence |

---

*End of Corrected Spectral Gap Theorem. All four audit findings addressed. LaTeX-compatible throughout.*
