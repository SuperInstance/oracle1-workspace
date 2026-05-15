# FLUX-X2 — Continuous Field Extension for FLUX ISA

> Extends FLUX-C (42 opcodes) with 13 new opcodes for Eisenstein geometry, holonomy consensus, and temporal perception. Backward compatible. Uses unused opcode slots.

---

## Opcode Allocation

| Range | Count | Use | Status |
|-------|-------|-----|--------|
| 0x00-0x0F | 16 | Stack ops | 4 used, 12 free |
| 0x10-0x2F | 32 | Arithmetic | 7 used, 25 free |
| 0x30-0x4F | 32 | Comparison | 9 used, 23 free |
| 0x50-0x5F | 16 | Boolean | 3 used, 13 free |
| 0x60-0x6F | 16 | Constraint | 4 used, **12 new** |
| 0x70-0x7F | 16 | Control | 6 used, 10 free |
| 0x80-0xFF | 128 | System | 9 used, 119 free |

**New opcodes added:** 13, placed in constraint (0x60) and arithmetic (0x10) ranges.

---

## Group 1: Eisenstein Geometry (3 opcodes)

### 0x17 EISENSTEIN_NORM
**Stack:** [a, b] → [a² - ab + b²]
**Cycles:** 3
Takes two stack values as Eisenstein coordinates (a, b), returns hexagonal norm.

```flux-c
PUSH 3        ; a
PUSH 4        ; b
EISENSTEIN_NORM ; 9 - 12 + 16 = 13
```

### 0x18 HEX_SNAP
**Stack:** [x, y] → [a, b, error]
**Cycles:** 8
Snaps Cartesian coordinates (x, y) to nearest Eisenstein lattice point (a, b). Returns error distance.

```flux-c
PUSH 0.73     ; x
PUSH 0.21     ; y
HEX_SNAP      ; a=1, b=0, error=0.02
```

### 0x19 VORONOI_SEARCH
**Stack:** [x, y, n_candidates] → [a, b, error]
**Cycles:** 12 + 2×n
Searches n nearest Eisenstein neighbors for best snap. Implements P1 deadband search.

```flux-c
PUSH 0.73     ; x
PUSH 0.21     ; y
PUSH 6        ; 6 hexagonal neighbors
VORONOI_SEARCH
```

---

## Group 2: Holonomy Consensus (4 opcodes)

### 0x64 CYCLE_FIND `graph_id`
**Stack:** [] → [cycle_count]
**Cycles:** O(V × E)
Finds fundamental cycles in constraint graph identified by graph_id. Returns count.

```flux-c
CYCLE_FIND 0x01  ; Find cycles in graph 1
PUSH result
```

### 0x65 HOLONOMY `cycle_id`
**Stack:** [] → [holonomy]
**Cycles:** 5
Measures holonomy (product of weights) around a specific fundamental cycle.

```flux-c
CYCLE_FIND 0x01  ; Find cycles
HOLONOMY 0x01    ; Measure cycle 1
```

### 0x66 CONSENSUS_CHECK `tolerance`
**Stack:** [graph_id] → [passed]
**Cycles:** 10 per cycle
Checks if all cycles in a graph have holonomy within tolerance.

```flux-c
; ZHC consensus check
PUSH 0x01        ; graph ID
CONSENSUS_CHECK 0.01  ; tolerance 0.01
ASSERT           ; halt if no consensus
```

### 0x67 VIOLATOR_ID
**Stack:** [] → [node_id, holonomy]
**Cycles:** 3
Returns the node that appears in most violating cycles.

```flux-c
VIOLATOR_ID      ; Stack: [node_id, holonomy]
```

---

## Group 3: Temporal Perception (3 opcodes)

### 0x68 T_MINUS `timer_id` `ttl`
**Stack:** [] → [expired]
**Cycles:** 2
Creates a T-minus timer. Returns 1 if expired, 0 if still running.

```flux-c
T_MINUS 0x01 100  ; 100ms timer
NOT               ; invert: 0 = still waiting
ASSERT            ; fail if timer expired without event
```

### 0x69 DEADBAND_CHECK `sensor_id` `lo` `hi`
**Stack:** [value] → [violated]
**Cycles:** 3
Checks if value falls outside [lo, hi] deadband.

```flux-c
LOAD_VAR sensor_1
DEADBAND_CHECK 0x01 0 100  ; Check sensor 1 in [0, 100]
ASSERT              ; Trap if outside deadband
```

### 0x6A SCRIPT_CHECK
**Stack:** [input_hash] → [has_script, output]
**Cycles:** 1
One Delta: checks if input has a compiled script. Returns script output or 0.

```flux-c
; One Delta — the only perception trigger
SCRIPT_CHECK       ; Do we have a script for this?
JUMP_IF has_script ; If yes, run it
; No script — perception needed
CALL perceive
has_script:
; Script output on stack
```

---

## Group 4: Continuous Field (3 opcodes)

### 0x69 (alt) FIELD_QUERY
**Stack:** [x, y] → [value, gradient_x, gradient_y]
**Cycles:** 15
Queries the continuous constraint field at (x, y). Returns interpolated value and gradient.

### 0x6B FIELD_GAP
**Stack:** [x, y] → [gap_potential]
**Cycles:** 10
Returns the "gap potential" at (x, y) — how much new knowledge would improve field coverage.

### 0x6C FIELD_EMERGENCE
**Stack:** [room_id] → [beta_1, severity]
**Cycles:** 20
Computes H1 emergence (β₁ = E - V + C) and severity (ε = β₁/(V-2) - 1) from the constraint field.

```flux-c
FIELD_EMERGENCE 0x01  ; Forge room
DUP                ; severity on top
PUSH 0.0
GT                 ; severity > 0?
JUMP_IF emergent   ; If emergent, handle it
```

---

## Total Extension: 13 opcodes, 0 breaking changes

| Group | Opcodes | Slots Used | Purpose |
|-------|---------|------------|---------|
| Eisenstein | 0x17-0x19 | 3 (arithmetic) | Hexagonal lattice operations |
| Holonomy | 0x64-0x67 | 4 (constraint) | Consensus measurement |
| Temporal | 0x68-0x6A | 3 (constraint) | One Delta perception |
| Field | 0x69, 0x6B-0x6C | 3 (constraint) | Continuous field queries |

42 base + 13 extension = **55 opcodes total.** FLUX becomes a continuous-field-aware constraint language without losing its safety-critical determinism.
