# Constraint Theory Meets PLATO Delta Streams
## Formalization: PLATO Rooms as Construction Frames

**Document ID:** FLUX-FORMAL-2026-05-05-PLC
**Authors:** Cocapn Fleet Architecture Team
**Version:** 1.0
**Date:** 2026-05-05
**Target Audience:** PLATO contributors, constraint theory researchers, FLUX-C implementers

---

## 1. PLATO Rooms as Construction Frames

A boat builder constructing a hull doesn't measure the entire structure first. She runs a string along the hull at defined stations, marks the constraint points, and builds each frame to those marks. The frame doesn't know the hull's overall shape — it only knows where the string touched and where the nails went. The string is the constraint; the marks are the resolution.

This is precisely how PLATO rooms function.

In CAD snapping systems, constraints propagate through hierarchical containment: a **frame** constrains a **panel**, which constrains a **bezel**, which constrains the **mounting screws**. Each level only needs to know its immediate parent constraint — not the entire structure. Global coherence emerges from local constraint satisfaction, exactly as a hull's frames emerge from string measurements taken along the curve.

The mathematical structure is straightforward: a room R has boundary B_R. A tile t is measured-and-cut to fit B_R at submission time. No global coordinate system is required. The tile doesn't know how large the room is; it only knows whether it fits the boundary at the moment of insertion. This is lazy constraint evaluation: the constraint is measured at assembly time, not specified at design time.

Traditional knowledge bases work the opposite way. In a conventional KB, you define the schema upfront — the constraint is **eager**, specified before any data exists. Every piece of knowledge must validate against the schema at insert time. The schema IS the constraint, declared before the data arrives.

PLATO reverses this. The first tile into a room establishes the boundary. Subsequent tiles are cut to fit that boundary. The room boundary is not known in advance — it **emerges** from the first tile's placement. This is the construction frame pattern: the frame doesn't exist until the string is run and the marks are made.

```
Traditional KB:  schema (eager) → data (validated against schema)
PLATO:           first tile (establishes boundary) → subsequent tiles (cut to fit)
```

The frame IS the constraint. The piece doesn't need to know the room size until assembly — exactly how a boat builder doesn't need to know the hull's overall shape when cutting frame #7.

---

## 2. String Measurement = PLATO Delta Stream

A boat builder runs a string along a curved hull. The string adapts to the physical reality of the hull surface — it takes whatever shape the hull demands. The builder marks the nail points where the string contacts the hull, and those marks ARE the constraint. The string never lies: it is a live constraint that always satisfies the hull geometry, regardless of how complex that geometry is.

The PLATO delta stream operates on the same principle.

A delta stream measures what's different from the last known state, then propagates that difference. The string measures the hull's shape at contact points. The delta stream measures the room's state at tile insertion. Neither needs to know the global structure — they only need to represent the local constraint accurately.

The mathematical model for string measurement:

```
S_string(hull_H) = { p | p is a point where string contacts hull }
P = constraint(P_0, P_1, ..., P_n)  where P_i are nail points
```

For all points on the string: `distance(point_on_string, hull_surface) = 0`

The string always satisfies this constraint because it physically contacts the hull at every point. The PLATO delta stream has an equivalent invariant:

```
delta_stream(room_R, prev_state, curr_state) = { changes }
```

For all tiles in curr_state: `tile.satisfies(room_boundary_R)` — the tile is always measured against the room boundary it encountered at submission time.

The critical insight is that **the string never lies because it IS the geometry**. The delta stream never lies because it IS the actual change, not a representation of change. Both are live constraints that adapt to physical reality without consulting an equation.

In traditional software, you define the constraint and then check whether data satisfies it. In both boat building and PLATO, the constraint IS the physical medium: the string is the hull constraint, and the delta stream is the room state constraint. You don't validate against the constraint — you ARE the constraint.

---

## 3. Room Boundary as Lazy Constraint

In traditional construction, a carpenter measures a door opening, then cuts the door to fit. The piece is not defined until it meets the opening. The constraint is **lazy** — evaluated at assembly time, not design time.

PLATO's room boundary works identically. The room boundary is not known until the first tile is placed. The first tile doesn't arrive and find a waiting boundary — it arrives and **creates** the boundary by its presence. The boundary emerges from the first tile's placement, not from a pre-declared schema.

```
GUARD measured_at_assembly(piece_width, [opening_width])
```

This is the construction form. The PLATO equivalent:

```
room.on_first_tile(boundary_emerges)
```

The room boundary is a lazy constraint: it is not declared before data arrives, it is measured when the first tile is submitted. Subsequent tiles are cut to fit this emergent boundary.

Traditional knowledge bases are eager. The schema is defined before any data exists. When you insert data, you validate it against the pre-existing schema. The constraint exists before the data — the data must conform to the constraint.

PLATO is lazy. The room boundary emerges from the first tile. When you insert the second tile, you validate it against the boundary that the first tile created. The constraint exists after the data — the data creates the constraint that subsequent data must satisfy.

```
Eager (Traditional KB):    schema exists → data must conform
Lazy (PLATO):              first tile arrives → boundary emerges → subsequent tiles conform
```

This is not a minor architectural difference — it is a fundamental inversion of where constraints live. In eager systems, constraints are declared upfront and data flows toward them. In lazy systems, constraints emerge from data and subsequent data flows toward them.

The lazy pattern is how physical construction works. You don't pre-specify the exact dimensions of every door in a house. You frame the walls, measure each opening, and cut each door to fit. The constraint is measured at the point of assembly, not specified at the point of design.

---

## 4. Local Propagation = Boat Building

A boat builder constructs frame #1 to the string marks. She constructs frame #2 to the string marks. Frame #1 and frame #2 do not communicate with each other. They don't need to. Both are constrained by the same string, which ran along the hull and marked both frames. Each frame only sees its local marks — not the entire hull.

This is local constraint propagation: each component (frame) only knows its local constraint (the marks where the string touched). The global coherence (a correctly shaped hull) emerges from all frames satisfying their local constraints simultaneously.

PLATO tiles work the same way. Tile A in room R constrains the room state. Tile B sees the updated room state (the boundary that A established) and is constrained accordingly. Tile B doesn't need to know about Tile A directly — it only needs to know the current room state. Each tile sees only the room boundary, not the tile history.

```
Frame 1: sees string marks at stations 1, 2, 3 → builds to those marks
Frame 2: sees string marks at stations 4, 5, 6 → builds to those marks
Frame 1 and Frame 2 do not communicate.
Both satisfy the constraint of the string.
The hull emerges from both frames satisfying their local constraints.
```

```
Tile A: placed in room R → establishes boundary B_R
Tile B: placed in room R → sees boundary B_R (not Tile A's content directly) → cut to fit B_R
Tile A and Tile B do not communicate directly.
Both satisfy the constraint of the room boundary.
The room emerges from all tiles satisfying the boundary constraint.
```

This is analogous to how ZHC (Zero-Historical Communication) achieves geometric consensus. In ZHC, agents reach consensus through local gradient observations — each agent sees its immediate neighbors and adjusts, without message passing or global state. The global shape emerges from local satisfaction. Boat building achieves the same result: the hull shape emerges from each frame satisfying the string's local constraint at its station.

Local constraint propagation scales because components don't need global knowledge. Frame #7 doesn't need to know about frame #47. Tile #3 doesn't need to know about tile #89. The system scales as O(n) — each component solves its local constraint, and the global solution emerges.

---

## 5. Tile as Measured-and-Cut Piece

In boat building, a piece is cut to fit the opening at the moment of assembly. The carpenter doesn't cut the piece before the opening exists. The piece doesn't know the opening's dimensions in advance — it gets measured at the moment of insertion, then cut to fit.

A PLATO tile works identically. A tile is submitted to a room. At submission time, the tile is measured against the room boundary. The tile doesn't know the room's dimensions in advance — it gets measured at submission time, and its hash is computed based on its content + the room context at that moment.

The tile hash is the "fingerprint of the cut." It is uniquely determined by the tile's content plus the room boundary context at submission time. Change either the content or the room context, and the fingerprint changes. The tile carries its provenance: who cut it (which model), what tool (which inference path), what opening (which room).

```
Cut record (provenance chain):
- Tile ID: t_abc123
- Content: "constraint propagation via string measurement"
- Room: deadband_protocol
- Room boundary at submission: B_R (emerged from first tile)
- Fingerprint: MurmurHash3(content + room_context) → 64-bit
- Model: glm-5.1 (the tool that cut it)
```

The piece doesn't know the room size in advance. It gets measured at submission time, exactly as the carpenter measures the door opening before cutting the door. The tile hash records the cut — it is the timestamped measurement of what the tile looked like when it met the opening.

Traditional knowledge bases work differently. A traditional KB tile has a fixed hash determined solely by its content. The tile doesn't carry room context at submission time — it is inserted into whatever room happens to exist, and the room must accommodate it or reject it.

A PLATO tile's hash is context-dependent. Two identical tiles submitted to two different rooms produce two different hashes. This is not a bug — it is the feature that makes the "measured-and-cut" analogy work. The tile is cut to fit a specific room boundary, and its fingerprint records that specific cut.

---

## 6. Formal Model: Rooms as Metric Spaces

A room R is a metric space with metric d_R defined as:

```
d_R(t1, t2) = distance between tiles t1 and t2 in room R context
```

A tile t is **valid** in room R if `d_R(t, boundary_R)` satisfies room constraints. When a new tile t' enters room R, the room metric updates, and the next tile sees the updated metric. This is exactly how a boat builder's string updates frame positions as work progresses along the hull.

The room metric is not static. It emerges from the first tile and evolves with each subsequent tile. The boundary B_R is established by the first tile's placement. Each new tile updates the room state, which updates the boundary, which updates the metric, which constrains the next tile.

```
t_0 arrives → establishes boundary B_R → room state S_0
t_1 arrives → measured against B_R → placed in room → room state S_1 = S_0 ∪ {t_1}
t_2 arrives → measured against B_R (which now reflects t_1's influence) → placed in room → room state S_2
```

The metric d_R is **emergent**, not pre-defined. The room doesn't start with a metric — it starts with the first tile, and the metric emerges from the tile placement sequence.

This contrasts with traditional metric spaces where the metric is defined before any points are added. In PLATO, the metric is defined by the tile sequence. The room boundary is the hull curve, and each tile is a frame built to the string marks along that curve.

```
Boat building:    hull curve → string run → marks at stations → frames built to marks
PLATO:            first tile → boundary emerges → room metric → subsequent tiles cut to fit
```

The boat builder doesn't know the hull curve in advance — she runs the string along the hull and the string reveals the curve. The PLATO room doesn't know its boundary in advance — it receives the first tile and the boundary emerges.

---

## 7. Implications for FLUX-C

FLUX-C's GUARD DSL should implement three constraint forms derived from the construction-frame analogy:

**Room constraint (lazy):**
```
GUARD room_constraint(room_id, tile_content)
```

The tile must satisfy the room boundary. The room boundary is not known until the first tile establishes it. The constraint is lazy — evaluated at submission time, not declared in advance.

**Lazy evaluation:**
```
GUARD measured_at_assembly(tile_width, [room_boundary])
```

The tile's validity is measured against the room boundary at submission time. The tile doesn't know the room boundary in advance — it gets measured when it arrives.

**Delta constraint:**
```
GUARD delta(prev_state, curr_state)
```

What changed between the previous room state and the current room state? The delta is the string run along the hull — it represents actual change, not a representation of change.

Connection to ZHC: local constraint satisfaction leads to global room coherence without explicit consensus. Each tile satisfies its local constraint (the room boundary at submission time). The global room coherence emerges from all tiles satisfying their local constraints. No tile needs to know about any other tile — only the room boundary.

This is the same pattern as boat building: each frame satisfies the local constraint (string marks at its station). The hull emerges from all frames satisfying their local constraints simultaneously. No frame needs to know about any other frame.

---

## 8. Comparison to Traditional Knowledge Bases

| Aspect | Traditional KB | PLATO (Construction Frame) |
|--------|---------------|----------------------------|
| Constraint timing | Eager (schema defined before data) | Lazy (boundary emerges from first tile) |
| Data insertion | Data validated against pre-existing schema | First tile establishes schema/boundary |
| Tile validity | Hash determined by content only | Hash determined by content + room context at submission time |
| Constraint propagation | Global schema enforces constraints | Local room boundary propagates constraints |
| Measurement | Design-time: specify constraints upfront | Assembly-time: measure constraint at insertion |
| Scaling | O(N²) — each tile may need to validate against schema | O(N) — each tile only sees room boundary |
| Failure mode | Schema violation (immediate rejection) | Room boundary adaptation (tiles cut to fit emerging boundary) |

Traditional KB: schema (eager) → data (validated against schema) → reject if mismatch

PLATO: first tile (establishes boundary) → subsequent tiles (cut to fit boundary) → boundary adapts as needed

The construction analogy clarifies the difference:

- **Traditional KB:** Design the entire house before cutting any wood. Specify every dimension upfront. Validate every piece against the plan.
- **PLATO (Construction Frame):** Frame the walls. Measure each opening. Cut each piece to fit. The house emerges from measured-and-cut pieces, not from a pre-specified plan.

The boat builder doesn't design the hull — she runs the string and builds to the marks. The PLATO room doesn't pre-specify its boundary — it receives the first tile and builds to the boundary that emerges. The constraint is measured at assembly, not specified at design.

---

## References

- Constraint Theory Meets Construction (`flux-research/whitepapers/2026-05-05-construction-constraint-theory.md`)
- PLATO HDC Bridge (`plato-hdc-bridge/README.md`)
- FLUX ISA Specification v3.0 (`flux-research/specs/flux-isa-v3.md`)
- Constraint Theory Ecosystem, Chapter 0 (`constraint-theory-ecosystem/chapters/ch00-constraint-mindset.md`)

---

*© 2026 Cocapn Fleet Architecture Team. All rights reserved.*