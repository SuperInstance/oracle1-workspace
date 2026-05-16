# ROADMAP-01: False & Unsubstantiated Claims Removal
**Phase 1 | Priority: P0 | Timeline: This Week**

## Why This First
All 5 expert reviewers flagged false or unsubstantiated claims. These damage credibility with anyone who actually knows the underlying math. We fix these before making any new progress.

---

## CLAIM-01: "Unlimited Byzantine Fault Tolerance" via ZHC

**Severity:** CRITICAL — mathematically false
**Found in:** fleet-coordinate, holonomy-consensus, flux-research papers
**Evidence:** Fleet Systems Researcher + Marine Safety Engineer + PhD Student all flagged independently

### What's Wrong
FLP impossibility (1985): no deterministic algorithm achieves consensus in async networks with even one crash fault. ZHC (geometric holonomy = identity) does not transfer to Byzantine fault tolerance. The code has zero BFT mechanisms (no signatures, no voting, no authentication).

### Files to Edit
```
flux-research/papers/fleet-math-arxiv.md
flux-research/papers/fleet-math-synthesis-deepseek.md
fleet-coordinate/README.md
holonomy-consensus/README.md
```

### Replacement Language
**OLD:** "unlimited Byzantine tolerance" / "Byzantine fault tolerance" / "ZHC consensus"
**NEW:** "ZHC (Zero Holonomy Closure): a geometric consistency condition. When all closed trust loops sum to identity in the Pythagorean48 group, the fleet has a global invariant. This does NOT imply Byzantine fault tolerance — FLP shows consensus in async networks requires additional assumptions."

### Specific Replacements
- `fleet-coordinate/src/zhc.rs` README: change "Byzantine tolerance" to "geometric consistency check"
- `holonomy-consensus/README.md`: remove all mentions of Byzantine fault tolerance
- `flux-research/papers/fleet-math-arxiv.md`: add FLP caveat, rename section from "ZHC Byzantine Consensus" to "ZHC Geometric Consensus"

---

## CLAIM-02: "fluxc_terminates" Coq Proofs

**Severity:** CRITICAL — unverified claim
**Found in:** constraint-theory-llvm, cocapn.ai/certify.php
**Evidence:** Marine Safety Engineer: "Coq file is for toy subset, NOT the actual FLUX-C ISA"

### What's Wrong
The Coq file found is for guard expression normalization only (~150 lines). `fluxc_terminates` is NOT proved for the real FLUX-C ISA with 50 opcodes. The bytecode verifier is a 10-line stub.

### Files to Edit
```
constraint-theory-llvm/src/lib.rs (remove "fluxc_terminates" claim from comments)
constraint-theory-llvm/README.md
cocapn.ai/certify.php (remove "Coq proofs" language)
```

### Replacement Language
**OLD:** "FLUX Certify generates Coq proofs automatically"
**NEW:** "FLUX Certify compiles GUARD expressions to FLUX-C bytecode. The compilation pipeline includes a guard expression normalizer with Coq proofs of correctness for the normalization function. Full FLUX-C ISA verification is planned."

---

## CLAIM-03: "127 lines replace 12,000 lines of ML"

**Severity:** CRITICAL — unsubstantiated
**Found in:** flux-research papers, dissertation
**Evidence:** PhD Student + Marine Safety Engineer + Startup CTO

### What's Wrong
No dataset specified, no task definition, no ML baseline cited, no controlled experiment. This reads as marketing copy, not research.

### Files to Edit
```
flux-research/dissertation/CHAPTER-03-THEORY.md
flux-research/papers/fleet-math-arxiv.md
```

### Replacement Language
**Remove entirely** or replace with:
"We measured constraint checking latency and code size for a representative set of safety-critical guard expressions. The FLUX-C bytecode approach produces N lines of compiled output per guard expression. A full ML-based approach for the same task would require [X] lines and [Y]ms of inference. These numbers will be reported in Section [X] pending a controlled experiment."

---

## CLAIM-04: "Synthesis Theorem"

**Severity:** CRITICAL — marketing language
**Found in:** fleet-coordinate/README.md, fleet-coordinate/src/integration.rs
**Evidence:** Fleet Systems Researcher

### Files to Edit
```
fleet-coordinate/README.md
fleet-coordinate/src/integration.rs
```

### Replacement Language
**OLD:** "Synthesis Theorem: Laman-rigid fleet = provably self-coordinating"
**NEW:** "Fleet Coordinate Theorem (provisional): In a Laman-rigid fleet graph (E ≈ 2V-3, with sufficient edge verification), the fleet has a global invariant under ZHC closure. Sufficiency of the edge count condition requires Henneberg construction verification (see ROADMAP-02)."

---

## CLAIM-05: "max_neighbors = 12 from Laman's theorem"

**Severity:** HIGH — mathematically incorrect
**Found in:** fleet-coordinate, any README mentioning degree bounds
**Evidence:** Fleet Systems Researcher: "Laman gives no degree bound. A vertex in a Laman graph can have arbitrarily high degree."

### Files to Edit
```
fleet-coordinate/README.md
fleet-coordinate/src/graph.rs
```

### Replacement Language
**Remove entirely.** The maximum number of neighbors a fleet agent can coordinate with is a deployment decision based on communication bandwidth and trust management complexity, not a mathematical bound from Laman's theorem.

---

## CLAIM-06: "O(C·L) complexity"

**Severity:** HIGH — incorrect complexity analysis
**Found in:** holonomy-consensus/README.md
**Evidence:** Fleet Systems Researcher: "`find_all_cycles()` is O(N·deg) = O(N²) for dense graphs"

### Files to Edit
```
holonomy-consensus/README.md
holonomy-consensus/src/consensus.rs
```

### Replacement Language
**OLD:** "O(C·L) consensus"
**NEW:** "O(C·L) worst-case consensus, where C = number of cycles and L = longest cycle length. Note: cycle enumeration is O(N²) for dense graphs. The ZHC check itself is O(C·L)."

---

## CLAIM-07: "H1 100% accuracy, 2.7s early warning"

**Severity:** HIGH — unvalidated
**Found in:** fleet-coordinate, fleet-homology, flux-research papers
**Evidence:** Fleet Researcher + PhD Student

### Files to Edit
```
fleet-coordinate/README.md
fleet-homology/README.md
flux-research/papers/fleet-math-arxiv.md
```

### Replacement Language
**OLD:** "100% accuracy, 2.7s early warning"
**NEW:** "Preliminary measurements suggest emergence detection may precede task failure by several seconds in simulated environments. A controlled experiment is required to validate this claim. Current measurement: [TBD] pending experiment design."

---

## CLAIM-08: Sheaf Cohomology in SPEC.md

**Severity:** HIGH — undefined term used as authority
**Found in:** spline-physics/SPEC.md
**Evidence:** Mathematician: "uses 'sheaf' 6 times without defining opens, sections, or restriction maps"

### Files to Edit
```
spline-physics/SPEC.md
spline-physics/src/multi_agent/segment.rs
```

### Replacement Language
**OLD:** "sheaf cohomology" / "H¹" as a proof of convergence
**NEW:** Either:
1. **Define it properly:** "We model each joint as an open set U_i in a cover. Sections are feasible pin configurations. Restriction maps are projection operators. The sheaf is..."
2. **OR remove it:** Replace "sheaf cohomology convergence" with "cycle space dimension convergence" (which is what H¹ actually measures here)

---

## Files Summary for Phase 1

| File | Claims to Fix |
|------|-------------|
| `fleet-coordinate/README.md` | BFT, Synthesis Theorem, neighbors, complexity, H1 accuracy |
| `fleet-coordinate/src/zhc.rs` | BFT language in comments |
| `fleet-coordinate/src/graph.rs` | Remove max_neighbors claim |
| `holonomy-consensus/README.md` | BFT, O(C·L) complexity |
| `holonomy-consensus/src/consensus.rs` | Complexity comment |
| `constraint-theory-llvm/README.md` | Coq claim |
| `constraint-theory-llvm/src/lib.rs` | fluxc_terminates comment |
| `cocapn.ai/certify.php` | Coq proofs language |
| `flux-research/papers/fleet-math-arxiv.md` | BFT, ML comparison, H1 accuracy |
| `flux-research/papers/fleet-math-synthesis-deepseek.md` | BFT claim |
| `spline-physics/SPEC.md` | Sheaf cohomology |
| `flux-research/dissertation/CHAPTER-03-THEORY.md` | ML comparison |

---

## Verification Checklist

After editing each file, run:
```bash
# Verify no false claims remain
grep -r "unlimited" --include="*.md" --include="*.rs" repos/fleet-coordinate/ repos/holonomy-consensus/ flux-research/ || echo "CLEAN: no 'unlimited' found"
grep -r "Byzantine" --include="*.md" repos/fleet-coordinate/ repos/holonomy-consensus/ | grep -v "does NOT" || echo "CLEAN: no bare 'Byzantine' claims"
grep -r "127.*12,000\|12K.*ML\|synthesis theorem" --include="*.md" repos/ || echo "CLEAN: no unsubstantiated comparisons"
```
