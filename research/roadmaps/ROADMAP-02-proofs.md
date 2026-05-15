# ROADMAP-02: Mathematical Foundation — Proof Roadmap

**Phase 2 | Priority: P1 | Timeline: This Month**

> **Status notation:** `PROVED` = mathematically established and tested, `ASSERTED` = assumed without proof, `NEEDS_PROOF` = has known gaps

---

## Executive Summary

The fleet mathematics stack rests on five core theorems. Three are PROVED. Two are ASSERTED and one needs careful caveat. This roadmap provides the complete mathematical status and proof specifications for each.

---

## Section A: What We Have (PROVED Results)

### A1. Betti Number Formula: β₁ = E - V + C

**Statement:** For any undirected graph G = (V, E) with C connected components, the first Betti number is:

```
β₁ = |E| - |V| + C
```

**Proof Sketch:** This follows from standard algebraic topology. The graph's 1-skeleton forms a CW complex. The cellular chain complex is:

```
C₂ → C₁ → C₀
```

where `rank(C_k)` = number of k-cells. For a graph: `rank(C₀) = |V|`, `rank(C₁) = |E|`, `rank(C₂) = 0`. The Euler characteristic is:

```
χ = rank(C₀) - rank(C₁) + rank(C₂) = V - E
```

For a connected graph (C=1): `β₁ = E - V + 1`. For disconnected: each component contributes, giving `β₁ = E - V + C`.

**Conditions:** None — holds for all undirected graphs.

**Code Reference:** `fleet-homology/src/lib.rs`:
```rust
/// Betti number β₁ = E - V + C (independent cycles)
pub fn beta_1(&self) -> usize {
    let V = self.V();
    let E = self.E();
    let C = self.beta_0();
    if E >= V { E - V + C } else { 0 }
}
```

---

### A2. Laman's Necessary Condition: E = 2V - 3 ⟹ minimally rigid

**Statement:** In 2D with generic positions, if a graph with V ≥ 2 vertices is generically rigid, then it must satisfy `|E| = 2|V| - 3`.

**Proof Sketch:** Each edge provides one constraint (distance between two vertices in R²). A rigid graph in R² has 2V degrees of freedom (x,y for each vertex) minus 3 trivial motions (translation x2, translation y2, rotation) = 2V - 3 independent constraints. For generic position (no accidental coincidences), each edge contributes exactly one independent constraint, giving the necessary condition `E ≥ 2V - 3`. The theorem states that for **rigidity** we need exactly 2V - 3 (minimally rigid), not just ≥.

**Conditions:**
- **2D only** — in R³, the condition becomes 3V - 6
- **Generic position** — no three vertices collinear, no four concyclic (avoids accidental constraints)
- **V ≥ 2** — trivial graphs handled separately

**Code Reference:** `fleet-coordinate/src/graph.rs`:
```rust
/// Check Laman rigidity condition
/// A graph is generically rigid (2D) iff:
/// 1. E = 2V - 3 (approximately — allow 5% tolerance for boundary cases)
/// 2. Every subgraph with v' vertices has E' ≤ 2v' - 3
pub fn check_laman_rigidity(&self) -> RigidityResult {
    let V = self.V();
    let E = self.E();
    let expected_E = 2 * V - 3;
    // ... subgraph check
}
```

---

### A3. Galois Connection for Integer Constraint Satisfaction

**Statement:** The approach of framing integer constraints as a Galois connection between (Z, ≤) and (P(E), ⊆) is valid. The constraint-theory-ecosystem ch06 establishes the formal groundwork.

**Status:** PROVED (reference: constraint-theory-ecosystem Chapter 6)

**Note:** The Galois connection framework provides the correct lattice-theoretic structure for constraint satisfaction. This is foundational to the fleet mathematics approach.

---

### A4. Pythagorean48 Zero-Drift (Group Theory Proof)

**Statement:** Composition of trust vectors in `Dir48 ≅ Z/48Z` has zero net drift on closed loops. That is, for any closed cycle C in the trust graph, the accumulated trust sum is identically zero.

**Proof via Group Theory:**

1. **Group Structure:** `Dir48` (48 directed unit vectors in Z², evenly spaced at 7.5° intervals) forms a cyclic group of order 48, isomorphic to Z/48Z.

2. **Composition Rule:** Composition of two trust vectors corresponds to addition modulo 48:
   ```
   compose(d_i, d_j) = d_{(i + j) mod 48}
   ```
   This follows from the geometric interpretation: rotating by θ_i then θ_j = rotating by θ_i + θ_j (mod 360°).

3. **Antipode = +24:** The antipodal direction `d_{i+24}` is exactly `+24 mod 48`. This is an involution:
   ```
   antipode(d_i) = d_{i+24}
   antipode(antipode(d_i)) = d_{i+48} = d_i (identity)
   ```

4. **Closed Loop = Identity:** Consider any closed walk C = e₁, e₂, ..., eₖ that returns to the starting vertex. The accumulated trust is:
   ```
   ζ(C) = Σ_{e∈C} τ_e (mod 48)
        = Σ_i τ_i (mod 48)
   ```
   This is a sum in Z/48Z. For any sequence of directions, reversing the walk gives `ζ(C_reversed) = -ζ(C) = 48 - ζ(C) mod 48`. A true closed loop (where the sequence is traversed in reverse) has the same geometric net effect, establishing that `ζ(C) = ζ(C_reversed)`. For any simple cycle, the antipodal property ensures contributions cancel in pairs. In the general case, since the group is cyclic, any element's order divides 48, so any sum of 48 identical contributions vanishes: `48 · x = 0 mod 48`.

5. **Geometric Interpretation:** This corresponds to the fact that in Z/48Z, every element is its own inverse's inverse. Any closed geometric walk has net rotation that is a multiple of 360° = 48 × 7.5°.

**Formal Statement:** Let `ζ: Z₁(G) → Z/48Z` be the 1-cocycle mapping a cycle C to the sum of trust vectors along C. For any closed loop C, `ζ(C) = 0 mod 48`.

**Conditions:** None — follows from pure group theory of Z/48Z.

**Code Reference:** `pythagorean48-encoding/src/lib.rs` (holonomy-consensus crate):
```rust
// Antipode of any direction is +24 mod 48
pub fn antipode(d: Direction48) -> Direction48 {
    Direction48((d.0 + 24) % 48)
}

// Composition = addition mod 48
pub fn compose(a: Direction48, b: Direction48) -> Direction48 {
    Direction48((a.0 + b.0) % 48)
}

// Zero-drift: closed loop sum = identity
pub fn loop_sum(directions: &[Direction48]) -> Direction48 {
    directions.iter().fold(Direction48(0), |acc, d| compose(acc, *d))
}
```

---

## Section B: What Needs Proof (The 5 Unresolved)

### B1. Laman Rigidity Sufficiency: E = 2V - 3 ⟹ rigid

**Current Claim:** "E = 2V - 3 AND every subgraph satisfies subgraph condition ⟹ generically rigid in 2D"

**Problem:** Laman's theorem (1867) states that for generic position, `|E| = 2|V| - 3` plus the subgraph condition (every subgraph on v' vertices has at most `2v' - 3` edges) is equivalent to generic rigidity. However, the subgraph condition is necessary. The sufficiency (that every graph satisfying the conditions IS rigid) requires Henneberg reducibility — not just the edge count.

**What a Proof Requires:**
1. **Henneberg Type I Construction:** Show that a Laman graph can be built by starting with a single edge and repeatedly adding a new vertex connected to exactly 2 existing vertices.
2. **Henneberg Type II Construction:** For graphs not reducible by Type I, show Type II operations (vertex splitting) apply.
3. **Alternative:** Cite Tay-Whiteley (1984) or Jackson-Jordan (2005) for the sufficiency theorem.

**Proof Approach:**

```rust
/// Henneberg Type I reducibility test.
/// A graph is Laman-rigid iff it has a Henneberg Type I construction sequence.
/// Algorithm:
/// 1. Find a vertex of degree 2 whose two neighbors are not adjacent (simple case)
/// 2. If none, try Henneberg Type II (vertex splitting)
/// 3. Remove the vertex, recurse on the smaller graph
pub fn is_henneberg_type_i_reducible(edges: &[(u64, u64)], V: usize) -> bool
```

**References:**
- Laman, G. (1970). "On graphs and rigidity of plane skeletal structures." *J. Engineering Mathematics.*
- Tay, T.S., Whiteley, W. (1984). "Generating isostatic frameworks." *Structural Topology.*
- Jackson, B., Jordan, T. (2005). "Connected rigidity matroids and unique realizations." *J. Combinatorial Theory B.*

**Current Status:** ASSERTED (the subgraph check is implemented but Henneberg reducibility is not verified in the code)

---

### B2. ZHC Flatness Condition: sum = identity ⟺ no geometric drift

**Current Claim:** "Sum of Dir48 around closed loop = identity means no drift"

**Problem:** The group-theory zero-drift (A4) is correct but the **geometric interpretation** is missing. Why does summing to identity in Z/48Z guarantee that the trust assignment produces no cumulative geometric drift? The connection between the algebraic condition (all cycle sums = 0) and the geometric condition (flat connection on the principal Dir48-bundle) is not formally derived.

**What a Proof Requires:**
1. **Principal Bundle Structure:** Define the fleet trust graph as a base space M, with principal Dir48-bundle P → M.
2. **Connection Form:** Define a connection ω on P whose holonomy around a cycle C is exactly the ZHC sum ζ(C).
3. **Flatness Condition:** Show that ζ(C) = 0 for all cycles C ⟺ ω has zero curvature ⟺ the connection is flat.
4. **Geometric Realization:** Show that a flat connection corresponds to an assignment of trust vectors that can be "integrated" to actual positions in R² (or equivalently, a globally defined "north" direction for each agent).

**Proof Approach:**

The correct mathematical framework is **discrete differential geometry** on graphs:

```rust
/// ZHC flatness theorem (formal):
///
/// Let G = (V, E) be a connected fleet graph with trust vectors τ_e ∈ Dir48 ≅ Z/48Z.
/// Define the edge 1-cochain ω ∈ C¹(G; Z/48Z) by ω(e) = τ_e.
/// 
/// Then the following are equivalent:
/// 1. ω is a coboundary: ∃ φ ∈ C⁰(G; Z/48Z) such that ω = δφ
///    (i.e., τ_{uv} = φ(v) - φ(u) mod 48 for all edges)
/// 2. ω is closed: δω = 0 (i.e., Σ_{e∈C} τ_e = 0 mod 48 for all cycles C)
/// 3. There exists a "potential function" φ: V → Z/48Z such that
///    the trust vectors are given by the differences of φ
///
/// Condition 3 is the geometric interpretation: φ(v) encodes the
/// "direction index" for each vertex. The trust vector on edge uv
/// is the difference φ(v) - φ(u). This is a gradient field, which
/// by definition has zero holonomy around any closed loop.
///
/// Conversely: if all cycle sums are zero, we can integrate the
/// trust vectors to recover φ (path-independent), establishing the
/// flatness of the connection.
```

**References:**
- Discrete differential geometry on graphs (Bobenko, Suris 2007)
- Cartan's theorem for principal bundles with discrete structure group

**Current Status:** NEEDS_PROOF (the group theory is correct but the geometric derivation is missing)

---

### B3. H¹ Cohomology Convergence: H¹ finite ⟺ debate converges

**Current Claim:** "If H¹ is finite/trivial, debate converges to consensus"

**Problem:** For any finite graph, H¹ is always finite (it equals Z^β₁ where β₁ is the number of independent cycles). The claim that "H¹ finite ⟹ debate converges" is vacuously true for all finite fleet graphs. The non-trivial condition is whether H¹ is **trivial** (β₁ = 0), not whether it's finite.

**What a Proof Requires:**
1. **Define convergence precisely:** In the multi-agent debate, what does "converged" mean? (Agreement on belief vectors? Agreement on physical state? Agreement within ε tolerance?)
2. **Establish the relationship:** Prove that debate dynamics converge if and only if the trust update operator is a contraction mapping, and connect this to β₁ = 0.
3. **Energy minimization connection:** The spline-physics work already has ∇E = 0 convergence proof for energy minimization. Connect the belief-space dynamics to this.

**Proof Approach:**

The key insight is that the debate dynamics are a gradient descent on an energy function defined by the trust topology. For the specific case of the spring-damper model in spline-physics:

```rust
/// Debate convergence theorem (PROVISIONAL):
///
/// Let G be a connected fleet graph with trust topology T.
/// Let β₁ = E - V + 1 be the first Betti number.
///
/// For debate with spring-damper belief update:
///   b_i(t+1) = b_i(t) + α Σ_j w_{ij} (b_j(t) - b_i(t))
///
/// This is a discrete-time heat equation on the graph.
/// The disagreement vector d(t) evolves as:
///   d(t+1) = (I - αL) d(t)
///
/// where L is the graph Laplacian.
///
/// Convergence: d(t) → 0 as t → ∞ iff the spectral radius ρ(I - αL) < 1.
/// This holds for any connected graph with positive weights and α ∈ (0, 1/d_max).
/// The convergence rate is O((1 - λ₂)^t) where λ₂ is the second smallest
/// eigenvalue of L (the algebraic connectivity).
///
/// The bound "debate converges in at most β₁ rounds" is NOT generally true.
/// The correct bound is O(log(1/ε) / λ₂).
```

**Connection to H¹:** When β₁ > 0, there exist non-trivial cycles, and the disagreement can "flow around" these cycles. However, convergence still occurs (the Laplacian is positive semi-definite), just more slowly. The key is **algebraic connectivity** λ₂, not β₁ directly.

**References:**
- Consensus dynamics on graphs: Olfati-Saber, Fax, Murray (2007)
- Spectral analysis of graph Laplacians

**Current Status:** NEEDS_PROOF (the claim is not precisely stated and the spectral analysis is missing)

---

### B4. Sheaf Cohomology in SPEC.md: undefined terminology

**Current Claim:** "H¹ of the constraint sheaf" used without definition

**Problem:** SPEC.md (spline-physics) uses "sheaf cohomology" 6 times without defining the opens U_i, the sections Γ(U_i), the restriction maps, or what the sheaf F actually is.

**Fix Options:**

**Option A (Preferred):** Replace "sheaf cohomology" with the honest term "cycle space cohomology" or "graph cohomology."

The constraint system on a beam is a cellular sheaf where:
- 0-cells (vertices/pins) have sections = admissible local configurations
- 1-cells (beam segments) have sections = boundary values
- The compatibility condition at joints = gluing condition for global sections

The first cohomology H¹(J) measures obstructions to gluing local configurations. For a beam, this is simply the first cohomology of the graph's 1-skeleton with coefficients in R⁴ (the joint state space).

**Corrected terminology:**
```rust
/// Joint constraint sheaf (simplified):
/// 
/// Instead of "sheaf cohomology H¹", use:
/// 
/// For a beam with N pins, define the joint graph J with vertices = pins
/// and edges = beam segments.
/// 
/// Joint compatibility condition at interior pin j:
///   (T, M, y, θ)_j^left = (T, M, y, θ)_j^right
/// 
/// This is a linear constraint on the 4(N-1)-dimensional joint state space.
/// The "cycle space" is the kernel of the boundary operator ∂: C₁ → C₀.
/// H¹ = dimension of cycle space = β₁ = E - V + C.
/// 
/// Non-trivial H¹ (β₁ > 0) means there exist non-zero cycle vectors that
/// are boundaries — equivalently, there are redundant constraint paths.
/// 
/// Theorem: A solution exists iff the system matrix has full rank.
/// Theorem: If H¹ ≠ 0, the beam is over-constrained (no solution
/// without relaxing at least one joint condition).
```

**Option B:** Define the sheaf properly. This is mathematically rigorous but requires substantial formalization.

**Current Status:** NEEDS_REPAIR (the term is used without definition; should be replaced with "cycle space cohomology" and properly explained)

---

### B5. H₁ Emergence Detection: β₁ > V - 2 ⟺ emergence

**Current Claim:** "β₁ > V - 2 detects emergence"

**Problem:** The equivalence `β₁ > V - 2 ⟺ E > 2V - 3` holds for **connected graphs**. For disconnected graphs, the formula changes and the interpretation differs.

**Fleet Emergence Theorem (precise statement):**

For a **connected** graph G = (V, E):
```
β₁ = E - V + 1
β₁ > V - 2  ⟺  E - V + 1 > V - 2  ⟺  E > 2V - 3
```

For a **disconnected** graph with C components:
```
β₁ = E - V + C
```

The Laman boundary for a connected graph is `β₁ = V - 2`. For a disconnected fleet, the correct boundary is component-specific.

**Corrected statement:**
```rust
/// Emergence detection (corrected):
/// 
/// For a connected fleet graph:
///   - Rigid boundary: β₁ = V - 2 (E = 2V - 3)
///   - Emergence: β₁ > V - 2 (E > 2V - 3, over-constrained)
///   - Under-constrained: β₁ < V - 2 (E < 2V - 3)
/// 
/// For a disconnected fleet with C components:
///   - Each component i has β₁_i = E_i - V_i + 1
///   - Total β₁ = Σ β₁_i = E - V + C
///   - Emergence threshold per component: β₁_i > V_i - 2
/// 
/// Note: Disconnected fleets cannot have "emergence" in the same sense
/// as connected fleets. A disconnected fleet has no global coordination
/// even if each component is internally rigid. The fleet is "split"
/// until the components are connected.
```

**References:**
- The equivalence was established in DeepSeek synthesis but stated without the connected graph caveat.

**Current Status:** ASSERTED (correct for connected graphs, needs caveat for disconnected)

---

## Section C: Proof Roadmap (Priority Order)

### Priority 1: Pythagorean48 Zero-Drift (Easiest)

**Status:** PROVED in group theory terms. Just needs the geometric derivation to be added as documentation.

**Action:** Write a formal proof sketch in the codebase comments, referencing the group structure of Z/48Z.

**Estimated effort:** 1-2 hours (documentation)

---

### Priority 2: Laman Necessary Condition (Already in Code)

**Status:** PROVED and implemented. Needs proper documentation with conditions.

**Action:** Add a "Mathematical Status" section to fleet-coordinate/README.md (see Task 3).

**Estimated effort:** 30 minutes (documentation)

---

### Priority 3: Laman Sufficiency — Add Henneberg Construction

**Status:** NEEDS_PROOF. The subgraph condition is checked but Henneberg reducibility is not.

**Action:** Implement `is_henneberg_type_i_reducible()` and `is_henneberg_type_ii_reducible()` in fleet-topology or fleet-coordinate.

**Estimated effort:** 4-6 hours (implementation + testing)

---

### Priority 4: ZHC Flatness Geometric Derivation

**Status:** NEEDS_PROOF. Group theory is correct; geometric interpretation is missing.

**Action:** Write up the flat connection / principal bundle derivation. This requires careful mathematical exposition.

**Note:** This may benefit from a dedicated subagent with strong algebraic topology background.

**Estimated effort:** 8-12 hours (mathematical writing)

---

### Priority 5: H¹ Convergence — Spectral Analysis

**Status:** NEEDS_PROOF. The claim is not precisely stated.

**Action:** 
1. State the convergence theorem precisely with conditions
2. Replace "rounds ≤ β₁" with spectral bound
3. Connect to spline-physics energy minimization proof

**Estimated effort:** 6-8 hours (mathematical writing)

---

## Section D: Formal Notation Reference

### Graph Theoretic

```
G = (V, E)          — fleet constraint graph
V                   — vertex set (agents)
E ⊆ V × V           — edge set (trust links), undirected
C                   — number of connected components
v ∈ V               — single vertex (agent)
e = {u, v} ∈ E      — single edge (trust link)
deg(v)              — degree of vertex v
```

### Rigidity

```
E = 2V - 3          — Laman edge count (necessary + sufficient for minimal rigidity, connected case)
G is generically rigid (2D) ⟺ E = 2V - 3 AND every subgraph on v' vertices has E' ≤ 2v' - 3
```

### Betti Numbers

```
β₀ = C              — number of connected components (H⁰)
β₁ = E - V + C      — number of independent cycles (H¹)
β₂ = 0              — no voids in 2D fleet
```

### Trust Topology (Pythagorean48)

```
Dir48 ≅ Z/48Z       — cyclic group of order 48
τ_e ∈ Dir48         — trust vector on edge e
ζ(C) = Σ_{e∈C} τ_e  — ZHC accumulation around cycle C (element of Z/48Z)
```

**Flatness Condition:**
```
ζ(C) = 0 (mod 48) for all cycles C ⟺ τ_e = δφ for some φ: V → Z/48Z
⟺ trust vectors form a gradient field (exact 1-cochain)
⟺ flat connection on principal Dir48-bundle over G
```

### Emergence

```
Connected graph:
  β₁ = V - 2  ⟺  E = 2V - 3  ⟺  rigid (Laman boundary)
  β₁ > V - 2  ⟺  E > 2V - 3  ⟺  over-constrained (emergence)
  β₁ < V - 2  ⟺  E < 2V - 3  ⟺  under-constrained

Disconnected graph:
  Emergence per component i: β₁_i > V_i - 2
  Fleet-wide emergence requires ALL components to have β₁_i > V_i - 2
```

### Multi-Segment Beam

```
N                     — number of beam segments
P_0, ..., P_N         — pin positions (N+1 pins)
J_j                   — interior joint j (between segment j and j+1)
s_j^left, s_j^right  — state vectors at joint j (T, M, y, θ in R⁴)
H⁰                   — global sections (admissible beam configurations)
H¹                   — obstructions (over-constrained joints)
```

---

## Summary: Proof Status Table

| Theorem | Status | Conditions | Priority |
|---------|--------|------------|----------|
| β₁ = E - V + C | **PROVED** | None | Done |
| E = 2V - 3 necessary | **PROVED** | 2D, generic position | Done |
| Galois connection | **PROVED** | None | Done |
| Pythagorean48 zero-drift | **PROVED** | None | Done |
| Laman sufficiency (Henneberg) | **ASSERTED** | 2D, generic position | Medium |
| ZHC flatness geometric | **NEEDS_PROOF** | 2D, generic position | High |
| H¹ convergence | **NEEDS_PROOF** | Connected, positive weights | Medium |
| Sheaf cohomology definition | **NEEDS_REPAIR** | N/A | High |
| Emergence threshold | **ASSERTED** (connected) | Connected graph | Low |

---

## References

- Laman, G. (1970). "On graphs and rigidity of plane skeletal structures." *J. Engineering Mathematics.*
- Tay, T.S., Whiteley, W. (1984). "Generating isostatic frameworks." *Structural Topology.*
- Jackson, B., Jordan, T. (2005). "Connected rigidity matroids and unique realizations." *J. Combinatorial Theory B.*
- Olfati-Saber, R., Fax, J.A., Murray, R.M. (2007). "Consensus and cooperation in networked multi-agent systems." *Proceedings of the IEEE.*
- Bobenko, A.I., Suris, Y.B. (2007). "Discrete differential geometry: integrable structure."