# Constraint Theory (py) — Rebirth Doc

> 🔗 **Forgotten Gold: Repo #70** | 2026-05-15 | Forgemaster Archaeologist

## What It Is

Pure Python constraint satisfaction toolkit (v0.3.0, published on PyPI). Five modules: Eisenstein (A₂) lattice operations, temporal deadband funnel, adaptive tolerance, PLATO tile interface, and baton shard protocol. **Zero external dependencies.** 100+ tests.

## Why It's Gold

This is the mathematical engine behind PLATO's constraint solving. Every module solves a specific fleet problem:

### Eisenstein Lattice (`eisenstein.py`)
Snap any 2D point to nearest A₂ hexagonal lattice point with guaranteed worst-case error ≤ 0.577 (covering radius). Full Eisenstein integer arithmetic (norm, distance, rotation by 60° increments). 12-bit dodecet encoding packs snap metadata (error level, angle, chamber, safety flag) into a single u16. 6 Weyl chambers with barycentric coordinate classification. Core: golden-ratio 9-candidate Voronoi search.

### Temporal Constraints (`temporal.py`)
Exponential-decay deadband funnel — the constraint tightens over time. TemporalAgent observes (x, y) points, snaps to A₂ lattice, compares error against funnel width. Phases: APPROACH → NARROWING → SNAP_IMMINENT → CRYSTALLIZED (or ANOMALY). Chirality tracking — the agent commits to one Weyl chamber over time. Running statistics (Welford), prediction error, precision energy accumulation. Anomaly detection at 2-sigma.

### Adaptive Tolerance (`adaptive.py`)
Formula ε(c) = min(k/c, ε_max) — as manifold curvature goes to infinity near boundaries, snapping precision tightens. Region classification: FAR → APPROACHING → NEAR → CRITICAL → SINGULAR. AdaptiveTolerance compositor with LRU caching. Curvature estimation via finite differences. adaptive_snap() convenience function.

### PLATO Tile (`plato.py`)
Domain-scored knowledge tiles with relevance decay, recency tracking, reliability EMA updates, priority levels (LOW/MEDIUM/HIGH/CRITICAL), cross-reference graph. PlatoTileStore with query by domain/tags/min-relevance/state, sorted by composite score. Score weights configurable.

### Baton Shard (`baton.py`)
Three-way context split: artifacts (large blobs), reasoning (chain-of-thought list), blockers (active problems). SHA-256 integrity hashing per shard + root hash. Structural diff between shard generations. JSON serialization. Validation with issue reporting.

## Overlap With fleet-math-py

The `eisenstein` module shares DNA with fleet-math-py's Eisenstein snapping — both implement the A₂ lattice snap and dodecet encoding. However, constraint-theory-py goes further with: full A2Point arithmetic, 6 Weyl chamber classification, rotation by 60° steps, Voronoi cell area / error CDF / lattice generation utilities, and the `snap_with_metadata` API.

**Unique to constraint-theory-py** (no overlap):
- Temporal deadband funnel and TemporalAgent
- Adaptive tolerance compositor with caching
- PLATO tile interface (PlatoTile, PlatoTileStore)
- Baton shard protocol (split/merge/diff/validate)

These four modules are **pure new value** for PLATO-NG.

## What PLATO-NG Would Do With It

1. **Eisenstein snapping** as the foundation of PLATO-NG's coordinate system — every tile gets an A₂ lattice position encoded as a 12-bit dodecet
2. **TemporalAgent** as the constraint propagation engine — funnel phases map to PLATO lifecycle states, chirality maps to agent specialization
3. **AdaptiveTolerance** for boundary-of-knowledge detection — as agents approach their competence limits, tolerance tightens (stricter validation)
4. **PlatoTile** and **PlatoTileStore** as the in-memory PLATO tile prototype — exact schema for the PLATO-NG tile store
5. **BatonShard** as the handoff protocol — agent A splits context, passes to agent B, B diffs before/after for audit

## Link

`https://github.com/SuperInstance/constraint-theory-py`

`pip install constraint-theory`
