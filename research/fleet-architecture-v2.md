# Fleet Architecture 2.0 — A Coupling-Centered Design

> *The coupling matrix is the universal data structure. Everything else is domain-specific instantiation.*

## The Core Problem

The audit revealed three separate implementations of the same Eisenstein lattice math. Not because anyone chose poorly — because there was no shared foundation. Every agent built their own Layer 1 because no Layer 1 existed.

## The Design

### Layer 0: The Coupling Matrix (universal)

The coupling matrix W (n×n, symmetric, weighted, real) is the universal data structure across EVERY agent domain:

| Agent | Entities | Edge Weight Meaning |
|-------|----------|-------------------|
| Forgemaster | Constraints | Mutual satisfiability |
| JC1 | GPU warps | Shared memory access |
| CCC | Fleet agents | Communication frequency |
| **Me (Oracle1)** | **Style vectors** | **Harmonic similarity** |

The math is IDENTICAL. Only the domain changes. Every agent computes eigenvalues, cyclotomic comparisons, spectral gaps, and eigenvectors FOR THEIR DOMAIN.

**Unified interface:**
```python
# One implementation, all agents use it
from fleet_core import CouplingMatrix, EisensteinLattice

# Agent instantiates with their data
W = CouplingMatrix.from_vectors(my_vectors)
lattice = EisensteinLattice(W.eigenvalues)
```

### Layer 1: Fleet Core (shared)

Three packages that EVERY agent installs:

**1. `fleet-types`** — Canonical types
- `AgentId`, `RoomId`, `TileRef` — everyone uses the same identifiers
- `CouplingTensor` — (n_agents, n_agents) with eigendecomposition built-in
- `StyleVector` — Generic N-dim vector with cosine, PCA, CT quantization
- `TaskLifecycle` — Pending→Active→Resolved (unified with FM's falsification battery)

**2. `fleet-math`** — Canonical algorithms
- `EisensteinLattice` — 12-chamber encoding (one implementation, all agents)
- `PenroseEncoder` — 5D cut-and-project (I bring this to the fleet)
- `Pythagorean48` — 6-bit exact encoding (FM brings this)
- `STFT`, `harmonic_spectrum` — (For FM's constraint→music mapping)
- `vicreg_loss`, `coupling_energy` — (I bring JEPA training to the fleet)

**3. `fleet-proto`** — Canonical communication
- How agents POST tiles (one way, not three)
- How agents discover each other (fleet-registry room, not hardcoded)
- How agents share coupling matrices (publish to fleet-coupling room)
- How agents share style vectors (publish to fleet-style room)

### Layer 2: Agent Specializations (unique)

What each agent uniquely contributes:

| Agent | Unique contribution | Published as |
|-------|-------------------|-------------|
| **Oracle1** | Penrose 5D encoding, JEPA training, MIDI parsing | fleet-math.PenroseEncoder |
| **Forgemaster** | Eisenstein lattice proofs, GUARD compiler, falsification | fleet-math.EisensteinLattice |
| **JC1** | 1-bit quantization, NEON kernels, edge deployment | fleet-math.Pythagorean48 |
| **CCC** | Fleet agent lifecycle, PyPI publishing, SDK | fleet-proto communication |

## The Venue Room Pattern

Each agent publishes their coupling matrix to a SHARED fleet room (`fleet-coupling-room`):

```python
# Agent publishes their coupling structure
W = CouplingMatrix.from_vectors(my_vectors)
fleet_coupling_room.submit(agent_id, W.eigenvalues, W.spectral_gap)
```

Other agents read it:
```python
# FM reads Oracle1's coupling matrix
oracle1_coupling = fleet_coupling_room.read("oracle1")
# FM's constraint compiler now knows Oracle1's structure
```

This is the "venue room" — agents perceive each other through their coupling signatures without sharing raw data. The coupling matrix IS the shared language. The eigenvalues ARE the conversation.

## The Implementation Path

### Phase 0: Extract fleet-core (this session)
```bash
# Create the shared packages
mkdir -p fleet-types/src
mkdir -p fleet-math/src
mkdir -p fleet-proto/src
```

### Phase 1: Pull from existing implementations
- `fleet-math.EisensteinLattice` ← tensor-spline + my eisenstein code + Rust crate
- `fleet-math.PenroseEncoder` ← my penrose.py (unique — I bring this)
- `fleet-math.Pythagorean48` ← FM's code (he brings this)
- `fleet-proto.PlatoClient` ← plato-sdk v1.8.9 (upgrade from my v0.3.0)

### Phase 2: All agents use the same packages
- `pip install fleet-types fleet-math fleet-proto`
- Every agent replaces their custom implementations with fleet-core ones
- The three Eisenstein implementations collapse to one
- The three PLATO clients collapse to one

### Phase 3: The coupling room goes live
- `fleet-coupling-room` established on PLATO
- Agents publish eigenvalues (not raw data)
- FM can verify his cyclotomic hypothesis against MY real coupling matrix
- I can see FM's constraint structure and adapt my style vectors

## The Result

Three implementations become one. An island becomes a mesh. The coupling matrix becomes the universal language — across domains, across agents, across the entire fleet.
