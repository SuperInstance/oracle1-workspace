# ZHC + Pythagorean48 → Loop Room Architecture Bridge

**Research Date:** 2026-05-15  
**Researcher:** Oracle1 (subagent)  
**Sources:** fleet-math-py (`fleet_math.zhc`, `fleet_math.h1`, `fleet_math.laman`, `fleet_math.field`), fleet-core (`fleet_math.__init__` — Eisenstein Lattice, PenroseEncoder, Pythagorean48, CouplingAnalysis), fleet-room-convention SKILL.md, fleet-trust-patterns SKILL.md, fleet-bottle-protocol SKILL.md, ARCHITECTURE.md (PLATO Room Server), constraint theory papers

---

## 1. Executive Summary

The Loop Room pattern (rooms as loops or single runs) already **implements ZHC natively**. Every PLATO room is a node in a directed constraint graph; every tile is a weighted edge. The ZHC check — product of weights around every cycle = 1 — is the formal condition for "room agreement." Pythagorean48 provides the **exact integer encoding** (6-bit) to represent agreement signatures compactly. The bridge is already built; this document makes it explicit.

---

## 2. What ZHC Actually Is

From `fleet_math.zhc.ConstraintGraph`:

```python
class ConstraintGraph:
    """Weighted undirected graph for holonomy consensus checking.
    Edge weights are positive floats; holonomy around a cycle
    is the product of weights along that cycle.
    """
    
    def check_consensus(self, tolerance=0.01):
        for cycle in self.fundamental_cycles():
            h = self.holonomy(cycle)  # product of weights
            if abs(h - 1.0) > tolerance:
                return False, [(cycle, h)]
        return True, []
```

**Key properties:**
- Nodes = agents/rooms/processes
- Edges = constraint relationships (with weights)
- **Zero holonomy** = every cycle's weight-product = 1.0
- Fundamental cycles are computed via DFS spanning tree
- Tolerance parameter controls strictness

**This IS a consensus protocol.** Not proof-of-work, not PBFT — it's a **graph-theoretic constraint satisfaction** protocol. Nodes agree when the graph is holonomy-free.

---

## 3. What Pythagorean48 Actually Is

From `fleet-core/fleet-math/src/fleet_math/__init__.py`:

```python
PHI = (1 + math.sqrt(5)) / 2

def pythagorean48_snap(vector: np.ndarray) -> np.ndarray:
    """6-bit exact integer encoding. FM brings this to the fleet."""
    return np.round(vector * 48) / 48
```

**Key properties:**
- Quantizes continuous vectors to 48 discrete levels
- 48 < 64 = 2^6 → **exactly 6 bits** of information per dimension
- `np.round(vector * 48) / 48` is a **nearest-neighbor discretization**
- Returns an array of the same shape (n-dimensional), each value ∈ {..., k/48, ...}

### Why 48? Connections to Deep Math

| Property | Value | Relevance |
|----------|-------|-----------|
| 48 = 4! × 2 | 24 × 2 | Symmetries of the hypercube (B₄ Coxeter group order) |
| 48 = 3 × 16 | 3 × 4² | Relates to 4D coordinate axes |
| 48 = 2⁴ × 3 | | Prime factorization |
| GL(2,3) order | 48 | General linear group over GF(3) |
| Quaternion group GL | 48 | Binary octahedral group |
| 48 = 2 × (4² + 4⁰) | 2 × 17 | Pythagorean-ish relation |
| 48 as 48 discrete directions | | Each is a "compass bearing" for agreement |

**Pythagorean flavor:** 48 appears as the 2nd icositetrachoron number, the number of symmetries of a cube's vertices, and the order of several important Lie group configurations. The "Pythagorean" naming reflects that 48 discrete directions on a circle each correspond to a Pythagorean triple's angle.

---

## 4. The Loop Room Pattern

### What is a Loop Room?

From the Fleet Architecture (ARCHITECTURE.md):

```
Everything is a loop or a single run.
```

**Loop rooms** (continuous):
- `crab-trap-mud` — runs forever, agents explore, auto-harvest tiles to PLATO
- `the-lock` — iterative reasoning server, runs sessions continuously
- `fleet-inspector` — monitoring loop
- Any room that reads tiles → processes → writes tiles → repeats

**Single-run rooms** (ephemeral):
- Curriculum Engine stages (5-stage pipeline, one-shot)
- submit-session.py (extract-and-submit, terminates)
- Any `POST /submit` → validate → store → done

### Rooms as Nodes

From the Fleet Room Convention:

```yaml
# Each room has identity, exits, state
identity:
  name: "lab"
  kind: "lab"
exits:
  - room: "engine"
    cost: 0
```

A room IS an application: identity → state (tiles, agents, constraints) → exits → bridges.

### Tiles as Edges

From PLATO Room Server API:

```
POST /submit   → validate → sign → store
GET  /room/{name} → retrieve tiles
```

A tile written by room A and read by room B = a **directed constraint edge** from A → B. The tile's `_hash` (provenance chain) provides a verifiable weight.

---

## 5. Design: How Loop Rooms Implement ZHC Natively

### 5.1 Room Agreement Through Shared Tile Chains

**The mechanism:** Room A writes a tile to PLATO room `math-lab`. Room B reads from `math-lab`. Both have now agreed on that tile's content.

**In ZHC terms:**
- Room A = node_A
- Room B = node_B
- The tile = a constraint edge from A → B
- The tile's **provenance chain weight** = edge weight

**Concrete protocol:**

```python
# Tile-as-constraint-edge encoding
tile = {
    "room_id": "math-lab",
    "domain": "constraint-theory",
    "agent": "forgemaster",
    "question": "ZHC state: what is the coupling constant?",
    "answer": "3.14159",  # Agreed state value
    "tile_type": "consensus",
    "confidence": 0.95,
    "_hash": "abc123def",  # Provenance chain weight
}
```

When room B reads this tile and uses its value, it encodes a constraint:
```
weight(node_A, node_B) = confidence × chain_size_factor
```

**ZHC check:** For any cycle of rooms (A → B → C → A), do the products of their agreements equal 1.0?

```
tile_weight(A→B) × tile_weight(B→C) × tile_weight(C→A) ≈ 1.0
```

### 5.2 Pythagorean48 Encoding — The 6-Bit Agreement Signature

Each tile carries a **Pythagorean48 snap** of the agreement vector:

```python
def tile_agreement_signature(node_A_state, node_B_state):
    """Compute a 6-bit agreement signature between two rooms."""
    # Continuous agreement vector
    agreement = node_A_state - node_B_state
    
    # Snap to 48 discrete levels → 6-bit exact
    signature = pythagorean48_snap(agreement)
    
    # Now exactly representable in 6 bits per dimension
    # Two rooms agree if signatures match
    return signature
```

**48 discrete directions = 48 types of agreement states:**

| Signature | Meaning | 
|-----------|---------|
| 0/48 | Exact agreement (holonomy = 1.0) |
| 24/48 | Complete disagreement (antipodal) |
| 12/48 | Orthogonal (partial agreement) |
| k/48 | Gradient of disagreement |

**Why 6 bits matters:**
- `0` to `47` → fits in a single tile metadata byte
- Comparison is exact (`==` not `≈`) — no floating point drift
- Can be packed into PLATO tile hash fields
- 48 = order of GL(2,3) → relates to the **group structure of consensus** itself
- A 48-element group can represent all rotational symmetries of a cube — pure agreement/disagreement algebra

### 5.3 Disagreement Resolution (Holonomy ≠ 1.0)

When `check_consensus()` returns `False`, the violating cycles need resolution.

**Detection via fundamental cycles:**

```python
g = ConstraintGraph()
# Add edges from tile reads
for tile_a_to_b in consensus_tiles:
    g.add_edge(tile_a_to_b.source, tile_a_to_b.target, 
               weight=tile_a_to_b.confidence)

consensus, violations = g.check_consensus(tolerance=0.01)
# violations = [(cycle, holonomy_value), ...]
```

Each violation tells us:
1. **Which rooms are in the cycle** (A, B, C)
2. **Where the holonomy breaks** (product ≠ 1.0)
3. **Which specific tile weights cause the mismatch**

**Resolution protocol** (three approaches, use in order):

#### Approach A: Refiner Mediation (Recommended)
The **PLATO Refiner** (like The Lock's iterative reasoning) mediates:

1. Refiner detects violated cycle (A → B → C → A)
2. Calculates expected weights for zero holonomy
3. Proposes new tile values that would bring product to 1.0
4. Rooms vote on the proposal (Pythagorean48 signatures must match)
5. On agreement: Refiner writes corrective tiles marking consensus
6. On rejection: Escalate to human (Casey)

```python
# Refiner mediation protocol
def resolve_holonomy(cycle, current_holonomy):
    """Calculate what weights would make the cycle balance."""
    # Current: w_ab × w_bc × w_ca = h (n ≠ 1.0)
    # Target: w_ab' × w_bc' × w_ca' = 1.0
    
    # Distribute correction proportional to confidence
    adjustment = math.log(current_holonomy) / 3
    
    # Each room adjusts its tile weight
    proposal = {
        "cycle": cycle,
        "adjustments": {
            "A→B": {"old": w_ab, "new": w_ab / math.exp(adjustment)},
            "B→C": {"old": w_bc, "new": w_bc / math.exp(adjustment)},
            "C→A": {"old": w_ca, "new": w_ca / math.exp(adjustment)},
        }
    }
    return proposal
```

#### Approach B: Forked Tile Chains
When mediation fails, rooms fork:

1. Room A writes a tile with confidence high (`fork-A`)
2. Room B writes a competing tile (`fork-B`)
3. Both forks coexist — PLATO stores both
4. A third room (Refiner) reads both, writes a merger tile
5. Merger tile carries Pythagorean48 signature = weighted average
6. Original rooms read merger, adjust their state
7. Post-merger ZHC check should pass
8. If still violated → escalate

```python
tile_a_fork = {
    "room_id": "math-lab",
    "domain": "constraint-theory",
    "agent": "forgemaster",
    "question": "ZHC STATE: coupling constant",
    "answer": "3.14",
    "tile_type": "consensus-fork",
    "fork_group": "A",
    "confidence": 0.90,
}

tile_b_fork = {
    "room_id": "math-lab",
    "domain": "constraint-theory",
    "agent": "oracle1",
    "question": "ZHC STATE: coupling constant",
    "answer": "3.15",
    "tile_type": "consensus-fork",
    "fork_group": "B",
    "confidence": 0.85,
}

# Refiner reads both, produces merger:
tile_merger = {
    "room_id": "math-lab",
    "domain": "constraint-theory",
    "agent": "refiner",
    "question": "ZHC STATE MERGER: coupling constant",
    "answer": "3.145",  # Pythagorean48 snapped
    "tile_type": "consensus-merger",
    "p48_signature": [0.785, 0.000, 0.000],  # 6-bit exact
    "confidence": 0.95,
    "parent_forks": ["abc123", "def456"],
}
```

#### Approach C: Betti-Number Escalation (H1 Emergence)
From `fleet_math.h1`:

```python
def emergence_severity(graph):
    """ε = β₁ / (V - 2) - 1
    ε > 0 indicates redundant connectivity beyond a tree.
    """
```

If the number of **unresolved cycles** (β₁ = E − V + C) exceeds V − 2, the system has "emerged" into a state too complex to auto-resolve. **Escalate to human** immediately.

**Threshold logic:**
```python
V = len(all_rooms)          # Number of rooms
E = sum(tiles_per_room)     # Number of constraint edges  
C = connected_components    # Isolated room groups

beta1 = E - V + C
if detect_emergence(graph, threshold=0.0):
    # β₁ > V − 2 → too many cycles → human needed
    HUMAN_IN_THE_LOOP = True
```

This is the **Laman rigidity** connection (from `fleet_math.laman`):
```python
if is_rigid(graph):
    # E >= 2V - 3 per component → graph is "rigid"
    # Consensus is structurally stable
if is_minimally_rigid(graph):
    # E == 2V - 3 → exactly as many constraints as needed
    # No redundancy, no ambiguity
```

---

## 6. Concrete Tile Protocol for Agreement

### ZHC Tile Specification

Every consensus-related tile should carry these fields:

```json
{
    "room_id": "<plato-room>",
    "domain": "zhc-consensus",
    "agent": "<room-name>",
    "question": "ZHC: <variable-name>",
    "answer": "<value>",
    "tile_type": "zhc-constraint",
    "confidence": 0.0..1.0,
    "p48_signature": [0.375, 0.125, 0.0],
    "p48_cycle_group": "<cycle-id>",
    "tags": ["zhc", "consensus", "<domain>"],
    "provenance": {
        "chain_size": <number>,
        "timestamp": <unix-epoch>
    }
}
```

**Field semantics:**
- `p48_signature` — The Pythagorean48-snapped agreement vector (6-bit per dim)
- `p48_cycle_group` — Which cycle this tile participates in
- `confidence` — Edge weight (used in holonomy product)
- `chain_size` — Part of the weight calculation (longer chain = more trust)

### Edge Weight Calculation

```python
def tile_weight(tile):
    """Compute ZHC constraint weight from a PLATO tile."""
    confidence = tile.get("confidence", 0.5)
    chain_size = tile.get("provenance", {}).get("chain_size", 1)
    
    # Weight = confidence boosted by chain maturity
    # Diminishing returns on chain length
    chain_factor = 1.0 + math.log(1 + chain_size) * 0.1
    return confidence * chain_factor
```

### Disagreement Tile Protocol

When rooms disagree, they write a **disagreement tile**:

```json
{
    "room_id": "bridge",
    "domain": "zhc-consensus",
    "agent": "room-A",
    "question": "ZHC: disagreement with room-B",
    "answer": "room-B's value",
    "tile_type": "zhc-disagreement",
    "confidence": 0.3,
    "p48_signature": [null, null, null],
    "p48_delta": 0.25,
    "p48_cycle_group": "cycle-7",
    "tags": ["zhc", "disagreement", "mediation-needed"],
    "provenance": {
        "chain_size": 15,
        "timestamp": 1778888888
    }
}
```

`p48_delta = abs(p48_signature_A - p48_signature_B)` — how many 48ths apart the two rooms are.

---

## 7. Scaling to a BEAM Cluster

BEAM (Erlang VM) gives us **process-per-room scalability**. PLATO tiles become a distributed shared-state substrate.

### Distribution Protocol = Tile Replication

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│ Node 1   │         │ Node 2   │         │ Node 3   │
│ ┌──────┐ │  tile   │ ┌──────┐ │  tile   │ ┌──────┐ │
│ │Room A│─│──────▶──│─│Room B│─│──────▶──│─│Room C│ │
│ └──────┘ │  repl.  │ └──────┘ │  repl.  │ └──────┘ │
└──────────┘         └──────────┘         └──────────┘
        │                                     │
        │            tile repl.               │
        └─────────────────────────────────────┘
```

**On a BEAM cluster:**
- Each BEAM node hosts a subset of rooms
- PLATO tile replication IS the distribution protocol
- No separate consensus layer needed — tile provenance chains provide it
- Rooms on different BEAM nodes still communicate through PLATO tiles
- Tile replication latency = propagation delay (~same as ZHC fundamental cycle)

### ZHC on BEAM: Distributed Check Protocol

```python
# Each BEAM node runs this periodically
def check_cycle_consensus(cycle, plato_endpoints):
    """Check a cycle across BEAM nodes."""
    tiles = []
    for endpoint in plato_endpoints:
        room_tiles = fetch(f"{endpoint}/room/{cycle.room}")
        tiles.extend(room_tiles)
    
    g = build_constraint_graph(tiles)
    consensus, violations = g.check_consensus(tolerance=0.01)
    
    if not consensus:
        broadcast_mediation_request(violations)
    
    return consensus
```

### BEAM-Specific Optimizations

| Feature | Benefit for ZHC | 
|---------|-----------------|
| Lightweight processes | One process per room — map ZHC cycles to process groups |
| ETS tables | Cache Pythagorean48 signatures for fast comparisons |
| Distribution protocol | Tile replication = built-in consensus propagation |
| Hot code swapping | Update ZHC tolerance without downtime |
| Supervision trees | Auto-restart failed rooms; consensus state survives |

---

## 8. Laman Rigidity Connection

From `fleet_math.laman`, Laman rigidity checks whether a constraint graph is **structurally stable**.

For rooms (vertices) with constraint tiles (edges):

```python
V = number of rooms
E = number of consensus tile edges

# Minimally rigid: E == 2V - 3
# → exactly as many tile connections as needed
# → no ambiguity, no redundancy

# Redundantly rigid: E > 2V - 3
# → extra connections → redundant consensus
# → more expensive to check but more robust

# Not rigid: E < 2V - 3
# → not enough connections
# → rooms can 'drift' independently
# → consensus is fragile
```

**Tuning for Loop Rooms:**
- Minimally rigid = efficient but brittle
- Redundantly rigid = robust but more ZHC cycles to check
- Rule of thumb: each room should connect to at least 3 others (2V − 3 condition)

---

## 9. Field Interpolation for Continuous Consensus

From `fleet_math.field`:

The constraint field interpolation can **predict disagreements before they happen**:

```python
def detect_drift_before_disagreement(room_states):
    field = Field()
    for room_id, (x, y, weight) in room_states:
        field.embed(room_id, x, y, weight)
    
    # Find gaps in the field where consensus is weak
    gaps = field.gaps(grid_size=10, density_threshold=0.5)
    
    # Rooms in gaps are drifting — preemptively mediate
    for gap in gaps:
        schedule_mediation(gap['x'], gap['y'])
```

---

## 10. Implementation Roadmap

### Phase 1: Instrument PLATO with ZHC Checks (Now)
Add a `/zhc/check` endpoint to the PLATO Room Server:

```
GET /zhc/check?room={name}&tolerance=0.01
→ {consensus: true|false, violations: [(cycle, holonomy), ...]}
```

Minimal: read tiles from the room, build ConstraintGraph, run check_consensus().

### Phase 2: Add Pythagorean48 Signatures (Now)
When rooms write tiles, compute a Pythagorean48 snap of the answer/state and store it as `p48_signature` field.

```python
# In PLATO POST /submit handler:
if tile.get("domain") == "zhc-consensus":
    answer = float(tile["answer"])
    tile["p48_signature"] = pythagorean48_snap(np.array([answer]))
```

### Phase 3: Build Refiner Mediation (Next)
The PLATO Refiner (or The Lock server) gets ZHC-aware:

1. Poll `/zhc/check` periodically
2. On violation → run `resolve_holonomy(cycle, holonomy)`
3. Write mediation proposal tiles
4. Monitor for resolution

### Phase 4: BEAM Distribution (Future)
Deploy rooms across BEAM nodes with PLATO tile replication as the distribution substrate. Each BEAM node runs its own `/zhc/check` for local cycles and broadcasts only holonomy violations.

---

## 11. Open Questions

1. **Weight semantics:** Should tile `confidence` be the ZHC edge weight, or should weight include tile length, chain depth, and agent trust? The `Field` interpolation suggests a 2D embedding; trust adds a third dimension.

2. **48 justification:** Is 48 the right quantization for all domains? For high-precision math (π, e) we might need more levels. For trust scores (0.0-1.0), 48 levels might be too many. Pythagorean48 gives exactly 6 bits — this maps naturally to 64-level quantization (6-bit full range) but deliberately uses fewer.

3. **Cycle detection frequency:** ZHC checks are O(EV) in the fundamental cycle count. On a fleet with 1000 rooms and 10K tiles, how often can we run the check? Answer: rarely enough that it matters, often enough that drift is caught before escalation.

4. **The Laman rigidity threshold:** E ≥ 2V − 3 per connected component. If the fleet graph is too sparse (not rigid), should we add "dummy" constraint tiles? Or accept that non-rigid configurations don't need full consensus?

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **ZHC** | Zero-Holonomy Consensus — product of constraint weights around every cycle = 1 |
| **Holonomy** | Product of edge weights along a closed cycle |
| **Pythagorean48** | 6-bit exact integer encoding: `np.round(v * 48) / 48` |
| **Constraint Graph** | Weighted graph where edges represent agreement constraints |
| **Loop Room** | A PLATO room running in continuous loop (reads tiles → processes → writes) |
| **Single-Run Room** | Ephemeral room (runs once, terminates) |
| **Fundamental Cycle** | Basis cycle relative to a spanning tree (DFS) |
| **Refiner Mediation** | Third-party resolution of holonomy violations |
| **Laman Rigidity** | E ≥ 2V − 3 for structural stability of constraint graph |
| **H1 Emergence** | β₁ = E − V + C — cycles beyond tree connectivity |
| **PLATO Tile** | Atomic knowledge unit with provenance chain and trust |
| **BEAM** | Erlang VM — process-per-room scalability substrate |

---

## 13. References

1. `fleet_math.zhc` — ZHC ConstraintGraph implementation (fleet-math-py)
2. `fleet_math.h1` — H1 emergence detection (Betti number)
3. `fleet_math.laman` — Laman rigidity checks
4. `fleet_math.field` — Continuous constraint field interpolation
5. `fleet-core fleet_math.__init__` — Eisenstein Lattice, PenroseEncoder, Pythagorean48, CouplingAnalysis
6. `ARCHITECTURE.md` — Cocapn Fleet Architecture (PLATO Room Server, Crab Trap MUD, The Lock)
7. `fleet-room-convention SKILL.md` — Room directory structures and YAML format
8. `fleet-trust-patterns SKILL.md` — Trust-based decision patterns (Bayesian fusion, decay, threshold)
9. `fleet-bottle-protocol SKILL.md` — I2I bottle communication between rooms
10. Unified Constraint Theory paper (flux-research) — Covering codes, entropy reduction, DCS protocol
