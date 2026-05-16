# galois-retrieval — Galois Connection-Based Tile Matching

**Repo #75 (2026-05-13)** — *Forgotten gold: the production-grade Formal Concept Analysis engine that is the retrieval layer for PLATO-ng tile matching.*

## What It Is

A complete, tested Formal Concept Analysis (FCA) engine for **Galois connection-based retrieval of PLATO tiles**. Provides FormalContext (G, M, I) with closure/interior operators, Heyting algebra ranking, lazy retrieval with budget constraints, and information-theoretic optimal shard count computation.

## Forgotten Gold

**This IS the retrieval layer for PLATO-ng.** Not a sketch, not a prototype — a production-grade engine with:

- **FormalContext:** Objects = tile IDs, Attributes = keywords/concepts, Incidence = which attributes each tile has. Implements the full Galois connection (f, g): f(B) = shared attributes of objects, g(A) = objects sharing all attributes.

- **Galois closure** g(f(S)): finds ALL tiles that share ALL attributes of a query. Growth property: S ⊆ g(f(S)). Idempotent. Isotone. The three pillars of a true closure operator.

- **Galois interior** f(g(U)): finds ALL attributes shared by ALL tiles in a set. Contraction property: U ⊆ f(g(U)). Also idempotent and isotone.

- **Two ranking methods:**
  - *Heyting*: coverage × (1 + 0.1 × log₂(1 + specificity)) — best score differentiation
  - *Weighted sum*: overlap - 0.1 × irrelevant — simpler baseline

- **Lazy retrieval:** budget-constrained candidate pool expansion. Start with exact Galois closure, expand with tiles sharing ≥ budget attributes, rank the pool. Scales to arbitrary tile counts.

- **Optimal shard count:** m_opt = log_φ(N) (pure golden ratio!) The theoretical prediction uses information theory: maximize effective information while minimizing redundancy across shards.

## Why It Matters for PLATO-ng

This engine solves the fundamental PLATO-ng retrieval problem: **given a semantic query (attribute set), find the most relevant tiles (objects).** The Galois connection guarantees:

1. **Soundness:** closure(S) always contains all tiles matching the full query intent
2. **Completeness:** no tile that shares all query attributes is missed
3. **Laziness:** budget-constrained expansion means you start precise and expand only as needed
4. **Mathematical rigor:** the Heyting algebra ranking provides principled differentiation based on implication strength, not ad-hoc scoring

## The 40+ Test Suite

The test suite doesn't just verify functionality — it **proves Galois connection properties**:
- S ⊆ g(f(S)) for 20 random subsets (extensive closure)
- U ⊆ f(g(U)) for 20 random subsets (extensive interior)
- g(f(g(f(S)))) = g(f(S)) (idempotent closure)
- f(g(f(g(U)))) = f(g(U)) (idempotent interior)
- S₁ ⊆ S₂ ⇒ g(f(S₁)) ⊆ g(f(S₂)) (isotone closure)
- All verified on both small (8 tiles) and large (1000+ tiles) datasets

## Revival Priority

**High.** This is the retrieval layer — the core mechanism for finding tiles in PLATO-ng. It's already production-quality code. It just needs to be connected to the new PLATO-ng backend and exposed via API + CLI.
