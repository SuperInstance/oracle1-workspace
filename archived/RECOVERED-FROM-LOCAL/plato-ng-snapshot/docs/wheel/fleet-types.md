# fleet-types — Canonical Fleet Core Library

**Date discovered:** 2026-05-15  
**Repository:** `SuperInstance/fleet-types`  
**Status:** Published (PyPI: `fleet-types`)  

## What It Is

The canonical type definitions that every SuperInstance agent imports. One package, one import, consistent types across the entire fleet. Contains `AgentId`, `CouplingTensor`, `StyleVector`, `Task`, `TaskStatus` — the four horsemen of the fleet's data model.

## Forgotten Gold

This is the **type system of the fleet** — what makes every agent speak the same language. It looks simple (one file, four dataclasses, one enum), but this simplicity masks the deepest unification work in the fleet. Here's the gold:

### AgentId — Fleet Registry in Four Lines
`AgentId` with classmethods (`oracle1()`, `forgemaster()`, `jc1()`, `ccc()`) is the fleet's DNS. Every agent has exactly one way to identify itself: `AgentId(name, host, role)`. The roles are evocative: `oracle1` → `lighthouse`, `forgemaster` → `constraint-theory`, `jc1` → `edge`, `ccc` → `public-face`. This encodes the fleet topology in a single dataclass.

### CouplingTensor — The Universal Data Structure
`CouplingTensor` is the **kitchen sink of the fleet** — a symmetric weighted adjacency matrix that every agent works with. The domain changes but the math doesn't:
- `eigenvalues`: spectral decomposition of the coupling structure
- `spectral_gap`: `λ_n - λ_{n-1}` — the gap that determines how many meaningful dimensions exist
- `fiedler_value`: algebraic connectivity (larger = more connected network)

This is directly tied to the conservation law (γ+H = 1.283 - 0.159·log(V)) — the spectral gap determines the number of meaningful coupling dimensions, which constrains the harmonic balance. Every coupling tensor in the fleet obeys the same conservation law.

### StyleVector — Fleet's Fingerprint
A generic N-dim vector with:
- `cosine_similarity()` — how close two fingerprints are
- `to_5d()` — reduction to [pitch×12, timing×100, velocity, 1-articulation, timbre]
- `from_109()` / `from_5d()` — constructors that parallel the midi-bridge style vector

The 5D reduction (pitch, timing, velocity, articulation, timbre) matches `plato-midi-bridge-rs` perfectly — they're the same 5D primitives in different packages. This is the unified fingerprint for anything in the fleet: code, music, agent behavior, coupling topology.

### Task — Lifecycle-Tracked Work
`Task` with `TaskStatus` (PENDING → ACTIVE → RESOLVED | SUPERSEDED | RETRACTED) is the **work lifecycle** of the fleet. `source` and `target` are `AgentId`, not strings. Every task carries its creation timestamp, resolution timestamp, and result string. This is the basis for the fleet's work queue / task routing system.

### Zero Complexity
One file, four dataclasses, one enum, one dependency (`numpy`). The CI.yml checks import works and runs `py_compile`. That's it. The heavy math (spectral gap, eigen decomposition) is wrapped in numpy — the type system doesn't reimplement it, it unifies it.

## Why It Matters

This is the **Rosetta Stone** for every agent communication in the fleet. Before this, every agent had its own `AgentId`, its own coupling matrix class, its own style vector. Now they don't. One import, consistent everywhere. This is the foundational layer that makes PLATO multicast, CRDT sync, and fleet routing possible.

## Integration Opportunities

- **PLATO-NG integration**: Use `AgentId` as room identifiers, `CouplingTensor` as room topology, `Task` as work queue items
- **All agents**: Every new agent should `from fleet_types import *` as their first import
- **CouplingTensor + flux-index**: The spectral gap of a codebase's coupling tensor could predict refactoring complexity
- **StyleVector + midi-bridge**: Unified style vector across music, code, and fleet behavior

## Architecture

```
fleet-types/
├── __init__.py (one file, ~100 lines)
│   ├── AgentId: canonical identity
│   ├── CouplingTensor: universal data structure
│   ├── StyleVector: fleet fingerprint
│   ├── Task: lifecycle-tracked work
│   └── TaskStatus: lifecycle states
└── setup.py (one dependency: numpy)
```

## Related

- `plato-midi-bridge-rs` style vectors align with `StyleVector.to_5d()` primitives
- `flux-index`'s embedder could emit `StyleVector`\-compatible fingerprints for code
- Conservation law (γ+H = 1.283 - 0.159·log(V)) governs `CouplingTensor` spectral gaps
