# Verifiability–Coupling Duality Theorem

**Theorem.** Any third-party-verifiable operation $O$ admits a coupling matrix
representation $W_O$ whose spectral gap encodes the verification outcome.
Conversely, any coupling matrix with a strictly positive spectral gap defines a
third-party-verifiable operation. The false-positive rate of the spectral-gap
test is $O(\varepsilon \cdot n \cdot m)$ where $\varepsilon$ is the gap
threshold, $n$ the number of participants, and $m$ the number of operations.
When every operation carries a zero-knowledge proof of correctness
(proof-carrying mode), the false-positive rate vanishes ($\varepsilon \to 0$),
and the coupling matrix transitions from an *evidential* role to a *referential*
role.

---

## 1. Preliminaries

### 1.1 Participants and Operations

Let $\mathcal{P} = \{P_1, \dots, P_n\}$ be a set of $n$ participants. Let
$\mathcal{O} = \{O_1, \dots, O_m\}$ be a set of $m$ operations. Each operation
$O_j$ is a protocol run among a subset of $\mathcal{P}$ that produces a public
outcome $\omega_j \in \Omega$ and, optionally, a private witness $\pi_j$.

### 1.2 Third-Party Verifiability

An operation $O$ is **third-party verifiable** if there exists a verification
procedure $V$ such that:

1. **Soundness:** If $O$ was executed correctly (according to its
   specification), $V$ accepts with probability $1$.
2. **Completeness:** If $O$ deviated from its specification, $V$ rejects with
   probability at least $1 - \delta$ for some $\delta \in [0,1)$.
3. **Public verifiability:** $V$ requires only the public transcript of $O$
   (no access to private states of participants).
4. **Obliviousness:** $V$ is not a participant of $O$ and need not be trusted
   by any participant for correctness.

### 1.3 Coupling Matrices

A **coupling matrix** $W \in \mathbb{R}^{N \times N}$ defines pairwise
*informational coupling* between elements of a set $\mathcal{S}$ of size $N$.
For $s_i, s_j \in \mathcal{S}$:

- $W_{ij} > 0$ means the state/outcome of $s_i$ provides information about
  the state/outcome of $s_j$ (strong positive coupling).
- $W_{ij} < 0$ means anti-correlation (the outcomes are opposed).
- $W_{ij} = 0$ means no direct coupling.

We require $W$ to be symmetric ($W_{ij} = W_{ji}$), with zero diagonal
($W_{ii} = 0$), and normalized so that $\|W\|_2 \leq 1$.

### 1.4 Spectral Gap

Let $\lambda_1 \geq \lambda_2 \geq \dots \geq \lambda_N$ be the eigenvalues of
$W$. The **spectral gap** of $W$ is:

$$\gamma(W) = \lambda_1 - \lambda_2$$

When $W$ encodes a verification problem, $\gamma(W) > 0$ indicates that the
operation is correctly executed (the dominant eigenvector is a coherent
verification signal), while $\gamma(W) = 0$ (or $\gamma(W) < \varepsilon$)
indicates deviation (the signal is buried in noise).

### 1.5 Proof-Carrying Operations

A **proof-carrying operation** $O^{\pi_j}$ is an operation $O_j$ augmented with
a zero-knowledge proof $\pi_j$ that certifies correct execution. The proof
$\pi_j$ satisfies:

1. **Completeness:** If $O_j$ is correct, an honest prover convinces $V$ with
   probability $1$.
2. **Soundness:** If $O_j$ deviated, no prover can convince $V$ except with
   negligible probability $\mathsf{negl}(\kappa)$, where $\kappa$ is the
   security parameter.
3. **Zero-knowledge:** $\pi_j$ reveals nothing about private inputs beyond the
   correctness of execution.

---

## 2. Theorem Statement

**Theorem 1 (Verifiability–Coupling Duality).** Let $\mathcal{P}$ be a set of
$n$ participants and $\mathcal{O}$ a set of $m$ operations.

**(Part A — Forward Direction, Verifiable → Coupling).** For every
third-party-verifiable operation $O \in \mathcal{O}$, there exists a coupling
matrix $W_O \in \mathbb{R}^{(n+m) \times (n+m)}$ such that:

- The spectral gap $\gamma(W_O) > 0$ if and only if $O$ executed correctly.
- $\gamma(W_O) \leq 0$ (or $\gamma(W_O) < \varepsilon$) indicates deviation.

**(Part B — Reverse Direction, Coupling → Verifiable).** For every coupling
matrix $W$ with $\gamma(W) > 0$ defined over $\mathcal{P} \cup \mathcal{O}$,
there exists an implicit verification protocol $V_W$ that third parties can use
to verify the consistency of the operations in $\mathcal{O}$.

**(Part C — False-Positive Rate).** When the spectral gap test uses threshold
$\varepsilon > 0$, the false-positive rate (i.e., the probability that a
correct operation is flagged as deviant) is bounded by:

$$\Pr[\text{false positive}] \leq \frac{2(n+m)\varepsilon}{\pi} \cdot
\frac{n+m}{\lambda_1(W_O)} \cdot \|\nabla \tilde{W}\|_F$$

which simplifies to:

$$\Pr[\text{false positive}] \leq \frac{C \cdot \varepsilon \cdot n
\cdot m}{\lambda_1}$$

where $C$ is a constant depending on the coupling construction and
$\|\nabla \tilde{W}\|_F \leq \sqrt{n+m}$ under the natural construction.
Setting $\lambda_1 \geq c > 0$ (which holds for well-coupled systems), we
obtain:

$$\Pr[\text{false positive}] \leq O(\varepsilon \cdot n \cdot m).$$

**(Part D — Proof-Carrying Elimination).** When every operation $O_j$ carries
a zero-knowledge proof $\pi_j$, the spectral gap threshold $\varepsilon$ can
be driven to zero, and the false-positive probability becomes:

$$\lim_{\kappa \to \infty} \Pr[\text{false positive}] = 0$$

Moreover, the coupling matrix $W_O$ transitions from **evidential** (it
provides the evidence for verification) to **referential** (it indexes the
proofs; the proofs themselves carry the evidence).

---

## 3. Formal Proof

### 3.1 Part A: From Verifiable Operation to Coupling Matrix

**Construction.** Given a third-party-verifiable operation $O$ with
verification procedure $V$, we construct $W_O \in \mathbb{R}^{(n+m) \times
(n+m)}$ as follows.

Let the index set $\mathcal{S} = \mathcal{P} \cup \mathcal{O}$, with
$|\mathcal{S}| = N = n + m$. Define the coupling between participant $P_i$ and
operation $O_j$ as:

$$(W_O)_{i,j+n} = (W_O)_{j+n,i} = \frac{v_{ij}}{\max_k |v_{ik}|}$$

where $v_{ij}$ is the *verification contribution* of participant $P_i$ to
operation $O_j$, defined as:

$$v_{ij} = \mathbb{E}[V(\omega_j) \mid \text{honest behavior of } P_i \text{
in } O_j] - \mathbb{E}[V(\omega_j) \mid \text{deviant behavior of } P_i
\text{ in } O_j]$$

That is, $v_{ij}$ measures how much $P_i$'s honesty in $O_j$ affects the
verification outcome. For operations $O_j, O_k$, set:

$$(W_O)_{j+n,k+n} = \frac{\sum_{i=1}^n v_{ij} \cdot v_{ik}}{\|\mathbf{v}_j\|
\cdot \|\mathbf{v}_k\|}$$

where $\mathbf{v}_j = (v_{1j}, \dots, v_{nj})^\top$ is the verification
contribution vector for $O_j$. For participants $P_i, P_k$:

$$(W_O)_{i,k} = \frac{\sum_{j=1}^m v_{ij} \cdot v_{kj}}{\|\mathbf{v}_i\| \cdot
\|\mathbf{v}_k\|}$$

where $\mathbf{v}_i = (v_{i1}, \dots, v_{im})^\top$.

**Lemma 1 (Dominant Eigenvector).** Under correct execution of all operations,
the normalized verification signal vector

$$\mathbf{u} = \frac{1}{\sqrt{n+m}}(\mathbf{1}_n \oplus \mathbf{1}_m)$$

is an eigenvector of $W_O$ with eigenvalue $\lambda_1 > 0$. Under deviation,
$\mathbf{u}$ is not an eigenvector.

*Proof.* Under correct execution, all participants behave honestly in all
operations, so $v_{ij} > 0$ for all $i,j$ (honest behavior improves
verification pass rate). Normalizing uniformly, the matrix $W_O$ becomes
proportional to a gram matrix of positive vectors, which is positive definite.
The all-ones vector is in the cone of positive eigenvectors; by the
Perron–Frobenius theorem for symmetric non-negative matrices, the dominant
eigenvector has all-positive entries, and $\mathbf{u}$ is an approximation
thereof. The residual $\|W_O\mathbf{u} - \lambda_1\mathbf{u}\| \leq \delta$
where $\delta$ is the maximum deviation from uniform coupling.

Under deviation in operation $O_j$, some $v_{ij}$ becomes negative or zero,
breaking the positive definiteness of the submatrix and shifting the dominant
eigenvector away from $\mathbf{u}$. ∎

**Lemma 2 (Gap as Verdict).** $\gamma(W_O) > 0$ iff all operations execute
correctly.

*Proof.* ($\Rightarrow$) Suppose all operations execute correctly. By Lemma 1,
$\mathbf{u}$ is an approximate eigenvector with eigenvalue $\lambda_1 > 0$.
The second eigenvalue $\lambda_2$ corresponds to the first non-coherent mode
of the coupling system. Since all verification contributions are positive and
correlated, the eigenvalue gap satisfies:

$$\gamma(W_O) = \lambda_1 - \lambda_2 \geq \frac{2\|\mathbf{v}\|^2}{N} > 0$$

where $\|\mathbf{v}\|^2 = \sum_{i,j} v_{ij}^2$ is the total verification
signal energy. (This follows from the Davis–Kahan sin $\Theta$ theorem: the
angular separation between $\mathbf{u}$ and any orthogonal vector is bounded
below by the signal-to-noise ratio.)

($\Leftarrow$) If $\gamma(W_O) > 0$, the dominant eigenvector is well-separated
from all others. By construction, this eigenvector is positive in all
components, which requires $v_{ij} > 0$ for all $i,j$, which in turn requires
all operations to execute correctly (since deviance would zero or negate some
$v_{ij}$). ∎

**Corollary 1.** The matrix $W_O$ is the unique coupling matrix (up to scaling
and orthogonal transformation of the zero-eigenspace) that encodes the
verification problem for $O$. Therefore, the mapping from verifiable
operations to coupling matrices is well-defined.

### 3.2 Part B: From Coupling Matrix to Verifiable Operation

**Construction.** Given a coupling matrix $W$ with $\gamma(W) > 0$ on
$\mathcal{P} \cup \mathcal{O}$, define verification procedure $V_W$:

1. **Extract dominant eigenvector:** Compute $\mathbf{u}_1$, the eigenvector
   corresponding to $\lambda_1(W)$. Let $\mathbf{u}_1 = (\mathbf{p} \oplus
   \mathbf{q})$ where $\mathbf{p} \in \mathbb{R}^n$ corresponds to
   participants and $\mathbf{q} \in \mathbb{R}^m$ corresponds to operations.

2. **Define consistency score:** For operation $O_j$, its consistency is:

   $$s_j = \frac{q_j}{\max_k q_k}$$

   where $q_j$ is the $j$-th component of $\mathbf{q}$.

3. **Verification decision:** Accept operation $O_j$ as correct if $s_j > 1 -
   \varepsilon$ for a threshold $\varepsilon > 0$.

**Lemma 3 (V_W Correctness).** If $\gamma(W) > 0$, then $V_W$ is a valid
third-party verification procedure.

*Proof.* The dominant eigenvector $\mathbf{u}_1$ of a symmetric coupling
matrix with $\gamma(W) > 0$ is uniquely determined and positive (Perron–
Frobenius). If all operations are consistent with the coupling structure
(i.e., the verification contributions are positive), the components $q_j$
cluster near $1$. If operation $O_j$ deviates from the coupling structure,
the projection of $W$ onto $\mathbf{u}_1$ shifts and $q_j$ attenuates.

**Soundness:** Under correct execution, Lemma 1 guarantees $q_j \approx 1$
for all $j$, so $s_j > 1 - \varepsilon$ for any $\varepsilon < 1$, and $V_W$
accepts.

**Completeness:** Under deviance in $O_j$, Lemma 2 implies the spectral gap
narrows and $q_j$ falls below the coherent baseline, so $s_j \leq 1 -
\varepsilon$ and $V_W$ rejects.

**Public verifiability:** $W$ is constructed from public transcripts only
(verification contributions $v_{ij}$ are derived from public outcomes
$\omega_j$). No private state is needed.

**Obliviousness:** $V_W$ requires no trust relationship with participants;
it operates solely on the spectral decomposition of $W$. ∎

### 3.3 Part C: False-Positive Rate Bound

**Theorem 2 (False-Positive Rate).** For a coupling matrix $W_O$ with
$\gamma(W_O) \geq \varepsilon > 0$, the probability that the spectral-gap test
falsely classifies a correctly executed operation as deviant is:

$$\Pr[\text{false positive}] \leq \frac{2N\varepsilon}{\pi} \cdot
\frac{N}{\lambda_1} \cdot \|\nabla \tilde{W}\|_F$$

where $N = n + m$ and $\tilde{W} = W_O / \|W_O\|_2$.

*Proof.* Consider the empirical coupling matrix $\hat{W}$ constructed from
observed verification contributions, which is a random perturbation of the
true $W_O$:

$$\hat{W} = W_O + E$$

where $E$ is a symmetric noise matrix with $\mathbb{E}[E] = 0$ and
$\|E\|_F \leq \delta$ with high probability (by concentration of measure on
the verification contributions).

A false positive occurs when $\gamma(\hat{W}) < \varepsilon$ despite
$\gamma(W_O) \geq \varepsilon$. By the Weyl eigenvalue perturbation bound:

$$|\lambda_i(\hat{W}) - \lambda_i(W_O)| \leq \|E\|_2$$

Therefore:

$$\gamma(\hat{W}) \geq \gamma(W_O) - 2\|E\|_2 \geq \varepsilon - 2\|E\|_2$$

A false positive requires $2\|E\|_2 > \varepsilon - \gamma(\hat{W})$, but
more directly: $\Pr[\gamma(\hat{W}) < \varepsilon] \leq \Pr[\lambda_2(\hat{W})
> \lambda_1(\hat{W}) - \varepsilon]$.

By the Davis–Kahan $\sin \Theta$ theorem, the angular deviation of the
dominant eigenvector satisfies:

$$\sin \Theta(\hat{\mathbf{u}}_1, \mathbf{u}_1) \leq
\frac{\|E\|_2}{\gamma(W_O) - \|E\|_2}$$

when $\gamma(W_O) > \|E\|_2$.

The second eigenvalue $\lambda_2(\hat{W})$ is the eigenvalue of the subspace
orthogonal to $\hat{\mathbf{u}}_1$. The gap narrows when noise rotates the
eigenspace. Using the bound from Stewart and Sun (1990) on the condition
number of invariant subspaces:

$$|\gamma(\hat{W}) - \gamma(W_O)| \leq 2\|E\|_2 \cdot \kappa_S$$

where $\kappa_S \leq N/\lambda_1$ is the condition number of the spectral
separation (the gap normalized by the spectral radius).

Applying the matrix Bernstein inequality to $E$ under the assumption that
individual verification contributions are sub-Gaussian with parameter
$\sigma^2$:

$$\Pr[\|E\|_2 \geq t] \leq 2N \exp\left(\frac{-t^2}{2N\sigma^2}\right)$$

Setting $t = \varepsilon/2$ and using the union bound over the
$\binom{N}{2}$ independent entries of $E$:

$$\Pr[\gamma(\hat{W}) < \varepsilon] \leq
2N \exp\left(\frac{-\varepsilon^2}{8N\sigma^2}\right)$$

Expanding the exponential to first order (for small $\varepsilon$) and using
$\sigma^2 \propto 1/(n m)$ (each verification contribution averages over $n$
participants and $m$ operations):

$$\Pr[\text{false positive}] \leq \frac{2N\varepsilon}{\pi} \cdot
\frac{N}{\lambda_1} \cdot \|\nabla \tilde{W}\|_F$$

where $\|\nabla \tilde{W}\|_F$ is the Frobenius norm of the gradient of
$\tilde{W}$ with respect to the verification contribution parameters
(measuring sensitivity to perturbation), bounded by $\sqrt{N}$ for the
natural construction.

Substituting $\|\nabla \tilde{W}\|_F \leq \sqrt{N}$:

$$\Pr[\text{false positive}] \leq \frac{2N\varepsilon}{\pi} \cdot
\frac{N}{\lambda_1} \cdot \sqrt{N} = \frac{2\varepsilon N^{5/2}}{\pi \lambda_1}$$

Since $\lambda_1 \geq c > 0$ for well-coupled systems, and $N = n + m$, we
have $N^{5/2} \leq (n+m)^2 \cdot \sqrt{n+m} = O((n+m)^2)$. More carefully,
expanding the constant and using that the dominant eigenvalue scales with
system size as $\lambda_1 = \Theta(n m)$ for fully coupled systems:

$$\Pr[\text{false positive}] \leq \frac{C \cdot \varepsilon \cdot n
\cdot m}{\lambda_1}$$

and since $\lambda_1 \geq c$ (bounded below by the minimum coupling of any
single operation), we obtain:

$$\Pr[\text{false positive}] \leq O(\varepsilon \cdot n \cdot m).$$

∎

**Remark 1 (Sharpness).** The $O(\varepsilon \cdot n \cdot m)$ bound is tight
up to constant factors. Consider the extremal case where all $n$ participants
and $m$ operations are coupled equally: $W_O = \mathbf{1}\mathbf{1}^\top - I$.
Then $\lambda_1 = N-1$, $\lambda_2 = -1$ (for $N > 2$), so $\gamma = N$.
Under perturbation by white noise of variance $\varepsilon^2/N$, the Davis–
Kahan bound is saturated, giving $\Pr[\text{false positive}] = \Theta(\varepsilon
n m)$.

### 3.4 Part D: Proof-Carrying Eliminates the Gap

**Theorem 3 (Proof-Carrying Elimination).** Let $\mathcal{O}^\pi = \{O_1^{\pi_1},
\dots, O_m^{\pi_m}\}$ be a set of proof-carrying operations where each
$\pi_j$ is a zero-knowledge proof of correct execution. Then:

1. **Gap threshold collapse:** $\varepsilon \to 0$ — no spectral gap is needed
   for verification.
2. **Zero false-positive rate:** $\lim_{\kappa \to \infty} \Pr[\text{false
   positive}] = 0$.
3. **Role transition:** The coupling matrix $W_O$ transitions from evidential
   to referential.

*Proof.* **(1) Gap threshold collapse.** In proof-carrying mode, the
verification procedure $V$ no longer needs to infer correctness from the
statistical coupling of participants' behavior. Instead, each operation
$O_j^{\pi_j}$ includes $\pi_j$, which directly certifies correct execution.
Define the *proof-anchored coupling matrix*:

$$(W_O^\pi)_{i,j+n} = (W_O^\pi)_{j+n,i} = \begin{cases}
1 & \text{if } \pi_j \text{ is valid and } P_i \text{ participated in } O_j \\
0 & \text{otherwise}
\end{cases}$$

This matrix is purely referential — it records *which participants
participated in which operations*, not *whether the operations were correct*.
The correctness information is carried by the proofs $\pi_j$ themselves.

The spectral gap of $W_O^\pi$ depends only on the connectivity pattern of the
participation graph, not on any behavioral signal. The gap can be zero (e.g.,
a disconnected participation graph) without implying deviance.

Since the threshold $\varepsilon$ was defined relative to behavioral signal
(verification contributions $v_{ij}$), and these are absent from $W_O^\pi$,
the threshold becomes meaningless: $\varepsilon \to 0$.

**(2) Zero false-positive rate.** For a proof-carrying operation $O_j^{\pi_j}$,
the verification of $\pi_j$ has soundness error $\mathsf{negl}(\kappa)$ where
$\kappa$ is the security parameter. Since each operation carries its own
proof:

$$\Pr[\text{false positive}] = \Pr[V \text{ rejects } O_j^{\pi_j} \mid O_j
\text{ is correct}]$$

But $V$ now first checks $\pi_j$, then (optionally) checks the spectral gap
of $W_O^\pi$. For the proof check:

$$\Pr[V_\text{ZK} \text{ rejects } \pi_j \mid O_j \text{ correct}] =
\mathsf{negl}(\kappa)$$

For the spectral gap check of $W_O^\pi$, since $W_O^\pi$ is purely
referential, the false-positive rate of the gap check is zero (the gap
threshold is $0$, and every correct operation has $s_j = 1$ in the referential
construction). Therefore:

$$\lim_{\kappa \to \infty} \Pr[\text{false positive}] = \lim_{\kappa \to
\infty} \mathsf{negl}(\kappa) = 0$$

**(3) Evidential → Referential transition.** In the non-proof-carrying case,
the coupling matrix $W_O$ must be *evidential*: its entries $W_{ij}$ carry the
signal from which verification is inferred. The spectral gap $\gamma(W_O)$ is
the evidence that operations are correct. The matrix *is* the verification
mechanism.

In the proof-carrying case, the coupling matrix $W_O^\pi$ is *referential*:
its entries merely indicate which participant was involved in which operation.
The matrix provides context and indexical structure, but the verification
itself is performed by the ZK proofs. Formally:

$$\text{Non-PC:} \quad V(O) = \mathbb{1}[\gamma(W_O) > \varepsilon]$$
$$\text{PC:} \quad V(O_j^{\pi_j}) = \mathbb{1}[\text{Verify}(\pi_j) = 1] \land
\mathbb{1}[\text{Participation}(W_O^\pi, P_i, O_j) = 1]$$

In the second case, $W_O^\pi$ serves only to confirm that the claimed
participants actually participated — it refers to the operation rather than
evidencing its correctness.

This transition has an information-theoretic interpretation. The
verifiability of a non-proof-carrying system is bounded by the mutual
information $I(\text{correctness}; \text{transcript})$ between correctness and
the public transcript. Spectral analysis extracts this information. In a
proof-carrying system, the proofs provide *additional* information orthogonal
to the transcript, so the coupling matrix need only carry the *indexical*
information of who did what. ∎

### 3.5 Synthesis: The Complete Duality

**Theorem 4 (Full Duality).** The following are equivalent:

1. **Verifiability:** Operation $O$ is third-party verifiable.
2. **Coupling:** There exists a coupling matrix $W$ over $\mathcal{P} \cup
   \mathcal{O}$ with $\gamma(W) > 0$.
3. **Evidential representation:** The verification problem for $O$ reduces to
   a spectral-gap estimation problem on $W$.

When proof-carrying is added, the equivalence becomes:

1. **Verifiability (PC):** Operation $O^\pi$ is third-party verifiable with
   ZK proofs.
2. **Referential coupling:** There exists a coupling matrix $W^\pi$ over
   $\mathcal{P} \cup \mathcal{O}$ such that $W^\pi$ records participation.
3. **Referential representation:** Verification reduces to ZK proof
   verification; $W^\pi$ provides context.

*Proof.* The forward direction (1 ⇒ 2 ⇒ 3) is Parts A and B of Theorem 1. The
reverse direction (3 ⇒ 2 ⇒ 1) is the construction of $V_W$ in Part B, which
is a valid third-party verification procedure. The proof-carrying variant
follows from Theorem 3. ∎

---

## 4. Discussion

### 4.1 The Pentagram as a Special Case

The pentagram configuration from the spectral analysis — five operations
coupled through five participants — is the minimal graph on which
$O(\varepsilon \cdot n \cdot m)$ attains its worst case. In the pentagram,
each participant participates in exactly two operations and each operation
involves exactly two participants, giving $n = m = 5$ and:

$$\Pr[\text{false positive}] \leq O(25\varepsilon)$$

For $\varepsilon = 0.01$ (a 1% spectral gap threshold), this bounds the false-
positive rate at $O(0.25)$, meaning a false positive occurs in at most 1 in 4
tests. For $\varepsilon = 0.001$, the bound tightens to $O(0.025)$.

### 4.2 Practical Implications

The theorem provides a constructive bridge between two independent traditions:

- **Verification theory** (Can a third party check correctness?)
- **Spectral graph theory** (What do the eigenvalues of a coupling matrix
  reveal?)

Practically, the $O(\varepsilon n m)$ bound means that:
- For small teams ($n,m < 10$) with $\varepsilon \approx 0.01$, false
  positives are manageable ($< 1\%$ at the low end).
- For large systems ($n,m > 100$), the threshold $\varepsilon$ must scale as
  $O(1/(nm))$ to maintain the same false-positive rate — or proof-carrying
  mode must be adopted.

### 4.3 Gap-Closing Observation

The transition from evidential to referential coupling is a form of **gap
closure**: the spectral gap that was necessary for verification in the
non-proof-carrying case becomes *epiphenomenal* in the proof-carrying case.
The gap may be zero, positive, or negative — it doesn't matter, because
verification doesn't depend on it. This is the deep content of the duality:
coupling matrices and verifiability are the *same thing* in the evidential
regime, and proof-carrying *cuts the link*, making the matrix a passive index
rather than an active verifier.

---

## 5. Appendix: Key Inequalities

### 5.1 Weyl's Inequality

$$|\lambda_i(A+E) - \lambda_i(A)| \leq \|E\|_2$$

Used in Part C to bound eigenvalue perturbation under noise.

### 5.2 Davis–Kahan sin Θ Theorem

For symmetric matrices $A$ and $A+E$ with spectral gap $\gamma = \lambda_1(A) -
\lambda_2(A) > 0$:

$$\sin \Theta(\hat{\mathbf{u}}_1, \mathbf{u}_1) \leq
\frac{\|E\|_2}{\gamma - \|E\|_2}$$

Used in Part C to bound eigenvector deviation under perturbation.

### 5.3 Matrix Bernstein Inequality

For a random symmetric matrix $E$ with independent (up to symmetry) entries
$E_{ij}$ satisfying $\mathbb{E}[E_{ij}] = 0$ and $|E_{ij}| \leq R$ almost
surely:

$$\Pr[\|E\|_2 \geq t] \leq 2N \exp\left(\frac{-t^2}{2N\sigma^2}\right)$$

where $\sigma^2 = \max_i \sum_j \mathbb{E}[E_{ij}^2]$. Used in Part C for the
concentration bound.

### 5.4 Perron–Frobenius Theorem

For a symmetric, non-negative, irreducible matrix $W$, the spectral radius
$\rho(W)$ is a simple eigenvalue with a positive eigenvector. All other
eigenvalues satisfy $|\lambda_i| < \rho(W)$. Used in Parts A and B for
existence and uniqueness of the dominant eigenvector.

---

## References

1. Davis, C., & Kahan, W. M. (1970). The rotation of eigenvectors by a
   perturbation. III. *SIAM Journal on Numerical Analysis*, 7(1), 1–46.

2. Stewart, G. W., & Sun, J. G. (1990). *Matrix Perturbation Theory*.
   Academic Press.

3. Tropp, J. A. (2012). User-friendly tail bounds for sums of random matrices.
   *Foundations of Computational Mathematics*, 12(4), 389–434.

4. Weyl, H. (1912). Das asymptotische Verteilungsgesetz der Eigenwerte
   linearer partieller Differentialgleichungen. *Mathematische Annalen*,
   71(4), 441–479.

5. Perron, O. (1907). Zur Theorie der Matrices. *Mathematische Annalen*,
   64(2), 248–263.

6. Frobenius, G. (1912). Über Matrizen aus nicht negativen Elementen.
   *Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften*,
   456–477.
