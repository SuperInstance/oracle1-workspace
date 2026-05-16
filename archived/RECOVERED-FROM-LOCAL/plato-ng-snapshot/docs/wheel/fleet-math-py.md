# fleet-math-py (Repo #40) — The Lost Constraint Theory Library

**Date:** 2026-05-11  
**Status:** v0.1.0 in repo, v0.3.0 on PyPI (DIFFERENT code)

## What It Is (Repo version)

Python bindings for fleet-math-c — the core fleet mathematics library for graph consensus and rigidity. But the repo contains FOUR modules that were **completely removed** from the published PyPI package:

### Unpublished Modules (in repo, NOT in PyPI v0.3.0)

1. **`zhc.py` — Zero Holonomy Consensus (ZHC)**
   - `ConstraintGraph`: weighted undirected graph with holonomy checking
   - Fundamental cycle decomposition via spanning tree
   - `check_consensus(tolerance)` — returns (consensus_bool, violation_cycles)
   - The big idea: a configuration has zero holonomy iff product of weights around every cycle = 1

2. **`h1.py` — H1 Emergence Detection**
   - `betti_1(graph)` = E - V + C (first Betti number)
   - `emergence_severity(graph)` = β₁/(V-2) - 1 (how far beyond minimally-connected)
   - `detect_emergence(graph, threshold)` — topological emergence detection
   - The ε > 0 threshold: when cycles outnumber the tree threshold

3. **`laman.py` — Laman Rigidity for 2D Bar-Joint Frameworks**
   - `is_rigid(graph)`: E >= 2V - 3 (necessary condition)
   - `is_minimally_rigid(graph)`: E == 2V - 3 + Laman count condition
   - `rigid_margin(graph)`: E - (2V - 3) — how redundantly rigid
   - Exhaustive Laman count check for graphs up to 12 vertices

4. **`field.py` — Continuous Constraint Field Interpolation**
   - `Field`: 2D scalar field with inverse-distance weighted interpolation
   - `gradients(resolution)`: gradient field on a grid
   - `gaps(grid_size, threshold)`: finds low-density regions
   - Power parameter p for natural falloff

### Published Modules (PyPI v0.3.0, NOT in repo)

- `health.py` — Fleet health metrics (coupling entropy, algebraic connectivity, timing stability, z-score health)
- `types.py` — Coupling type calibration (style, topology, mixed, directed) with type-aware health

## The Critical Finding

**The constraint theory mathematics (ZHC, H1, Laman, Field) was stripped from the published package.** The v0.3.0 on PyPI has completely different modules — `health.py` and `types.py` — with no mention of holonomy, Betti numbers, or Laman rigidity.

This means the repo version (0.1.0) contains **unpublished constraint theory code** that was the original value proposition of fleet-math. The published version pivoted to fleet health monitoring and coupling type analysis, leaving the foundational mathematics behind.

## Comparative Analysis

| Feature | Repo v0.1.0 | PyPI v0.3.0 |
|---------|-------------|--------------|
| ConstraintGraph + ZHC | ✅ Full implementation | ❌ Removed |
| H1 emergence (β₁) | ✅ Full implementation | ❌ Removed |
| Laman rigidity | ✅ Full implementation | ❌ Removed |
| Field interpolation | ✅ Full implementation | ❌ Removed |
| Fleet health metrics | ❌ | ✅ Added |
| Coupling type calibration | ❌ | ✅ Added |
| Python bindings for C | Claimed | Not claimed |

## Forgotten Gold

1. **ZHC is the core of flux-tensor-midi constraint theory.** Zero holonomy consensus is how the fleet validates that constraint cycles don't drift — this is foundational to the Eisenstein lattice and the plato-midi-bridge.

2. **Laman rigidity provides the mathematical foundation for fleet structural integrity.** A fleet graph that's not rigid will deform under load (communication drift). The rigid_margin tells you how much redundancy you have.

3. **The Field module's gap detection** maps directly to fleet topology — low-density regions in the field are communication dead zones.

4. **The `__pycache__` reveals there were also scripts** (`fleet_health_v2`, `fleet_orchestrator`, `fleet_worker`, `fleet_inspector`) that use these math modules but were removed from the repo.

## Rebirth Path

1. **Merge the constraint theory modules back into the published package** as `fleet_math.constraint` subpackage. The ZHC/H1/Laman/Field code is clean, tested (18 unit tests), and production-ready.

2. **Re-publish as v0.4.0** with both constraint theory AND health metrics. The published package needs both — they answer different questions about fleet structure.

3. **Connect ZHC to plato-midi-bridge.** The holonomy check is the mathematical validation that the Eisenstein lattice chambers don't drift — each room's coupling cycle should have zero holonomy.

4. **Build the bridge script.** The `fleet_math.cpython-310.pyc` in the plato-midi-bridge repo suggests these modules were meant to be called from a bridge script — restore the missing script from the pyc.
