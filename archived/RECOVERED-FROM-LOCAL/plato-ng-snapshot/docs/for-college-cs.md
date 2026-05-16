# PLATO Under the Hood

> For college CS majors who want to understand the architecture.

## Overview

PLATO is a room-based message-passing system with a typed protocol, a quality gate pipeline, provenance tracking, and a runtime that supports both deterministic and AI-driven processes.

**Core abstractions:** tiles (immutable messages), rooms (addressable namespaces), gates (validators), Loop Rooms (long-lived processes), and the event bus (pub/sub).

## Data Model

### Tile
```python
@dataclass
class Tile:
    domain: str        # Room/namespace
    question: str      # Query or identifier
    answer: str        # Content (may be JSON-serialized)
    tags: list[str]    # Classification labels
    source: str        # Creator identifier
    confidence: float  # [0, 1] — self-assessed quality
    # Server-added:
    _hash: str         # Content hash for dedup
    _clock: int        # Lamport clock for ordering
    _ts: float         # Submission timestamp
    provenance: dict   # Parent chain for lineage
```

### Gate Pipeline
Each tile passes through gates P0-P4 before acceptance:
- P0: minimum answer length (20 chars)
- P1: minimum confidence (0.1)
- P2: at least one tag
- P3: content-based quality heuristic
- P4: conservation law compliance (integrated)

Gates are composable: add P5 (GUARD constraint validation) by inserting a new gate function.

### Lamport Clock
The server maintains a Lamport clock. Each mutation increments it. Tiles can be queried by clock value for incremental sync.

## Loop Room Runtime

### Process Model
```
Loop Room = GenServer pattern:
  init() → state
  loop(state):
    receive:
      Task(tile) → new_state = process(tile, state)
                   send(new_state.tile)
                   loop(new_state)
      Status(reply_to) → send(reply_to, state.metrics)
                          loop(state)
      Halt() → terminate()
```

Each room runs in its own process (~2KB). The supervisor monitors all rooms, restarting on failure.

### Process Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| Algorithmic | Deterministic state machine. No model calls. | Game rules, move validation |
| Agentic | Calls external model. Has soul + memory. | Game master, strategy analysis |
| Refiner | Reads other rooms, applies CRUD to harness. | Failure detection, harness editing |

## Computational Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Tile submission | O(gates) | Each gate is O(tile size) |
| Room history query | O(log(tiles)) | Sorted by clock |
| Eigendecomposition (V=30) | O(V³) = 27K ops | NumPy LAPACK, 0.05ms |
| Conservation law check | O(1) | Constant-time formula |
| Gamma-H computation | O(V²) | Matrix ops, 0.05ms at V=30 |

## The Conservation Law

### Empirical Form
γ + H = 1.283 - 0.159·log(V), R²=0.9602

### Derivation Sketch
For a coupling matrix C = XX^T / diag(XX^T) where X ~ N(0, I_V · I_p):
1. The normalized Laplacian L = D^{-1/2}(D - C)D^{-1/2} has eigenvalues accounting for graph connectivity
2. The coupling matrix C follows a Marchenko-Pastur law in the V/p → c limit
3. Spectral entropy H = -Σ p_i log(p_i) / log(V) where p_i = λ_i(C) / Σλ_j
4. The MP log-moment μ₁^log(c) appears in BOTH H and the dominant eigenvalue of L
5. These moments cancel in the sum, leaving only the V-dependent term

### Implications
- The sum γ+H is a **type-dependent constant** for fixed V
- Deviations indicate measurement error or system change
- The Refiner uses >3σ deviations as failure signals

## Tripartite Filter System

Each of the three agents implements a filter-writer interface:

```python
class TripartiteAgent:
    def write_self_filter(self) -> Filter
    def write_filter_for(self, other: TripartiteAgent) -> Filter
    def evaluate(self, filter: Filter) -> float  # score [0, 1]
    def refine(self, evaluations: list[tuple[Filter, float]]) -> Filter
```

The oscillation loop:
```python
while not converged(scores, threshold=0.05):
    h_filter = human.write_filter_for(app)
    a_filter = app.write_filter_for(hw)
    hw_filter = hw.write_filter_for(human)
    
    app.evaluate(h_filter)
    hw.evaluate(a_filter)
    human.evaluate(hw_filter)
```

Convergence is guaranteed when scores stabilize within 0.05 across 3 iterations.

## Performance Benchmarks

| Operation | Throughput | Details |
|-----------|-----------|---------|
| Tile submission | 1,392/s | Python HTTP server |
| Tile read | 653/s | Room history query |
| Dict creation | 2.2M/s | Python baseline |
| A2Ui serialization | 132,441/s | 10K cycles in 76ms |
| Eigendecomposition n=30 | 19,214/s | NumPy LAPACK |
| Conservation law check | O(1) | 0.0005ms |
| Compiled game loop | 785K/s | After inference->code compilation |
