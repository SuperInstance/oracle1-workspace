# FLUX-C Analog Compute Integration for PLATO Rooms

## Design Document v1.0

**Author:** Oracle1 (PLATO Fleet Architecture)  
**Date:** 2026-05-05  
**Status:** Draft — R&D Phase 1  
**Target:** JC1 Edge Runtime, FLUX-C 43-opcode safety layer

---

## 1. Motivation: Why Analog Compute in PLATO?

PLATO rooms represent agent context as a dynamic, growing boundary. Each tile placed in a room defines a constraint on the room's shape. The room's state is not a fixed vector of coordinates — it is a **continuous surface** inferred from tile positions. Storing absolute coordinates for every tile becomes a storage burden as rooms scale, and absolute positions are fragile: corrupt one coordinate and the room's geometry is corrupted irrecoverably.

The insight from shipwright practice: you don't measure a hull point-by-point. You define the **spline** that the ribbands follow, and every plank bend is measured against that spline. The spline tolerates missing data, tolerates measurement noise, and can be updated incrementally as the hull grows.

This design introduces four FLUX-C analog opcodes that treat room boundaries as continuous spline surfaces rather than discrete point clouds. The opcodes are designed to run in the FLUX-C safety layer — they terminate, they are formally verifiable, and they carry explicit pre/postconditions that PLATO rooms can use for self-checking.

---

## 2. FLUX-C Opcode Design

FLUX-C uses Format G (Variable-Length Payload, 2+N bytes):

```
[ opcode (1 byte) ][ length (1 byte) ][ payload (N bytes) ]
```

New Analog opcodes are allocated in the 0xD0–0xDF range (currently unallocated in FLUX-C canonical):

| Hex | Name | Length | Payload |
|-----|------|--------|----------|
| 0xD0 | `ANALOG_SPLINE` | 34 | 3×points + material_E + tension |
| 0xD1 | `ANALOG_WATER_LEVEL` | 9 | point_array_ptr + count |
| 0xD2 | `ANALOG_STORY_POLE` | 10 | anchor + delta_array_ptr + count |
| 0xD3 | `ANALOG_SECTOR` | 9 | distance + divisor |

---

### 2.1 `ANALOG_SPLINE(0xD0)`

**Encoding:**

```
Byte 0:  0xD0 (opcode)
Byte 1:  0x22 (length = 34 bytes payload)
Bytes 2-9:   point[0]  — (x: f32, y: f32)
Bytes 10-17:  point[1]  — (x: f32, y: f32)
Bytes 18-25:  point[2]  — (x: f32, y: f32)
Bytes 26-29:  material_E — f32 (Young's modulus in GPa)
Bytes 30-33:  tension   — f32 (0.0 = linear, 1.0 = tight curve)
```

**Semantics:** Computes a quadratic Bézier spline passing through three boundary points. The middle point is the control point. Returns interpolated curve points via the FLUX-C stack as a sequence of (x, y, curvature) tuples. The number of output points is derived from material_E and tension (higher tension → more points, tighter bend).

**Preconditions:**
- `point[0].y <= point[1].y <= point[2].y` (ascending Y — spline flows upward)
- `material_E > 0.0` (Young's modulus must be positive; steel = 200.0, oak = 12.0, cedar = 6.0)
- `tension >= 0.0 && tension <= 1.0`
- All three points must be distinct (distance > ε where ε = 1e-6)

**Postconditions:**
- Output spline passes through point[0] and point[2] exactly
- Output spline has C1 continuity (continuous first derivative) at point[1]
- All output coordinates are finite (no NaN, no Inf)
- Curvature at output points is bounded by `material_E * tension` (stiff materials resist bend)
- GUARD tolerance: ±(0.5 + material_variation × tension) units

**Safety Margin:** ±ε where ε = 1e-6 for coordinate comparisons; material_E bounds checked before division. Stack overflow prevented by FLUX-C's bounded stack model (max 256 frames). The opcode cannot loop because the output point count is derived deterministically from inputs, not from iteration.

---

### 2.2 `ANALOG_WATER_LEVEL(0xD1)`

**Encoding:**

```
Byte 0:  0xD1 (opcode)
Byte 1:  0x09 (length = 9 bytes payload)
Bytes 2-5:   point_array_ptr — u32 (address of first point in memory)
Bytes 6-9:   count           — u32 (number of points, 3 ≤ count ≤ 256)
```

**Semantics:** Given an array of 2D points (each point = two f32 values), computes the horizontal line (level surface) that minimizes the sum of squared vertical deviations from all points. This is the least-squares regression line in the Y direction — the "water line" that a set of points would settle to under gravity. Returns a single f32: the Y-coordinate of the level surface.

**Preconditions:**
- `count >= 3` (minimum points for a meaningful level surface)
- `count <= 256` (FLUX-C memory region limit)
- `point_array_ptr` must be word-aligned (4-byte alignment)
- All point coordinates must be finite (no NaN, no Inf)

**Postconditions:**
- Result Y satisfies: `Y = Σ(points[i].y) / count` (arithmetic mean — the exact least-squares solution for horizontal line)
- Result is finite
- Zero deviations: if all points share the same Y, result = that Y exactly

**Safety Margin:** No division by count (count >= 3, always valid). Sum operation uses FLUX-C bounded integer arithmetic. Result is deterministic: same input points always produce the same Y.

---

### 2.3 `ANALOG_STORY_POLE(0xD2)`

**Encoding:**

```
Byte 0:  0xD2 (opcode)
Byte 1:  0x0A (length = 10 bytes payload)
Bytes 2-5:   anchor       — f32 (reference Y-coordinate)
Bytes 6-9:   delta_array_ptr — u32 (address of delta array)
```

**Note:** For this opcode, the count of deltas is implicit from the FLUX-C instruction length minus fixed header bytes, or passed via a companion register. The simplified encoding here assumes deltas are passed on the FLUX-C value stack (up to 16 deltas maximum, matching FLUX-C's stack depth).

```
Stack input (push before calling): delta[0..N-1] as f32 values, N <= 16
Stack output: result[0..N-1] as f32 values (anchor + delta[i] for each i)
```

**Semantics:** Transfers a level surface (water line) to different heights using a series of vertical offsets. Given an anchor Y (reference level) and an array of deltas, produces an array of absolute Y positions: `result[i] = anchor + sum_of_previous_deltas[0..i]`. This simulates a story pole used in boat building: a notched stick where each notch represents a frame's position along the hull, transferred from the lofting floor to the boat.

**Preconditions:**
- `anchor` must be finite
- All deltas must be finite
- `0 < N <= 16` (FLUX-C stack depth limit)
- Delta array must be word-aligned

**Postconditions:**
- `result[0] = anchor + delta[0]`
- `result[i] = result[i-1] + delta[i]` for i > 0 (running cumulative sum)
- All `result[i]` are finite
- If all deltas are 0: `result[i] = anchor` for all i

**Safety Margin:** Running sum cannot overflow f32 (delta magnitudes are bounded by GUARD tolerance). FLUX-C stack bounds prevent overflow. The bounded stack model means the number of deltas is known at call time — no unbounded iteration.

---

### 2.4 `ANALOG_SECTOR(0xD3)`

**Encoding:**

```
Byte 0:  0xD3 (opcode)
Byte 1:  0x09 (length = 9 bytes payload)
Bytes 2-5:   distance — f32 (total arc length or chord length)
Bytes 6-9:   divisor  — u32 (number of equal segments, 2 ≤ divisor ≤ 256)
```

**Semantics:** Divides a total distance into equal proportional segments, simulating the way a ship's compass divides an arc into equal parts when laying out a circular hull. Returns `divisor` segment lengths, each = `distance / divisor`. The segments are pushed to the FLUX-C stack as f32 values.

**Preconditions:**
- `distance > 0.0` (must be positive length)
- `divisor >= 2 && divisor <= 256`
- `distance / divisor` must not underflow (i.e., `distance >= divisor × f32_epsilon`)

**Postconditions:**
- `segment_length = distance / divisor`
- All `divisor` output values equal `segment_length` exactly (deterministic division)
- Sum of all output segments = `distance` exactly

**Safety Margin:** Divisor >= 2 and distance > 0 guarantees division is valid. Maximum divisor 256 prevents stack overflow on output. Result is exact for distances that are exact binary fractions; otherwise ±0.5 ulp rounding error.

---

## 3. PLATO Room Spline-Boundary Design

### 3.1 The Spline as Room State

In traditional designs, a room with N tiles stores N × 2 × 8 = 16N bytes of absolute coordinates. Every tile position is a fact stored independently. If any tile's coordinates are corrupted (bit flip, process crash mid-write), the room's geometry is corrupted with no recovery path except full recomputation from source.

The spline-boundary approach inverts this:

```
Room state = f(spline_control_points, material)
Spline = ANALOG_SPLINE(control_points, material_E, tension)
Tile validity = d(tile_position, spline) < GUARD_tolerance
```

The room does not store tile coordinates. The room stores the spline parameters: three control points and a material constant. From these, any tile's expected position can be computed. The tile's actual position is only stored in the delta stream (the sequence of tile placements, each expressed as an offset from the previous tile).

### 3.2 Kalman Filter Analogy

Each tile placement is a **measurement** of the room's true boundary. The room's spline is the **state estimate**. Adding a tile:

1. Measure: tile placed at position P
2. Predict: compute expected position on current spline
3. Correct: if P deviates from expected by < tolerance, accept tile and update spline control points; if deviation exceeds tolerance, flag for review
4. Next tile: sees the updated spline (updated state estimate)

This is exactly the Kalman filter cycle: predict → measure → correct → update. The spline is never "wrong" — it is the best estimate given all measurements so far. New measurements refine the estimate.

### 3.3 Tile Validity Check

For a tile at position P = (x, y) and a room spline S:

```
d(P, S) = |y - S(x)|   (vertical distance to spline curve)
```

If `d(P, S) < tolerance`: tile is on-boundary, valid.
If `d(P, S) >= tolerance`: tile is off-boundary, flagged.

The tolerance is: `tolerance = ε + material_variation × tension` where:
- `ε = 1e-6` (machine epsilon for coordinate comparison)
- `material_variation = ±5%` (typical material property variance)
- `tension` is the spline tension parameter

This gives tolerances in the range of 0.01–0.1 units for typical materials — tight enough to enforce geometry, loose enough to tolerate measurement noise.

---

## 4. Cost-Benefit Analysis

| Approach | Storage (bytes) | Compute (ops) | Precision | Fault Tolerance |
|----------|----------------|---------------|-----------|-----------------|
| Store absolute positions | N × dim × 8 = 16N | 0 (direct lookup) | ±0.5 ulp | **Fail if any point corrupted** |
| Store spline + deltas | 3 × 2 × 4 + 4 + N × 2 × 4 = 32 + 8N | O(N) to reconstruct | ±material_tolerance | **Tolerate N-1 missing points** |
| Store deltas only (no spline) | N × 2 × 4 = 8N | O(N) to reconstruct | ±propagation_error | **Fault tolerant by design** |

For a room with N=100 tiles in 2D:
- **Absolute:** 1,600 bytes stored
- **Spline + deltas:** 832 bytes stored (48% reduction), O(100) to reconstruct full geometry
- **Deltas only:** 800 bytes stored, O(100) to reconstruct

The spline approach provides the best fault tolerance per byte: if you lose 50% of the delta stream, you can still reconstruct the room geometry from the remaining deltas + spline. If you lose 50% of absolute coordinates, you have irrecoverable holes in your room.

**Precision comparison:** Absolute coordinates are precise to ±0.5 ulp (f64) but fragile. Spline coordinates are precise to ±material_tolerance (~0.01–0.1 units) but robust. For PLATO rooms, where geometry is inherently approximate (tiles represent conceptual boundaries, not CNC-cut parts), ±0.01 is more than sufficient.

---

## 5. Minimum Analog: The SPLINE-PRIMITIVE

The smallest analog compute that solves a meaningful constraint:

**2-point spline:** Defines a straight line segment. Two points + material. Storage: 2 × 2 × 4 + 4 = 20 bytes. Useful for simple room boundaries that are straight walls.

**3-point spline:** Defines a unique quadratic curve. Three points + material. Storage: 3 × 2 × 4 + 4 = 28 bytes. **This is the SPLINE-PRIMITIVE for 2D surfaces** — the minimum useful analog compute in PLATO rooms.

**4-point spline:** Defines a cubic Hermite spline with known tangent directions. Useful for 3D volumes (hull surfaces, lofted spaces). Storage: 4 × 3 × 4 + 4 = 52 bytes for 3D.

The SPLINE-PRIMITIVE (3-point, 2D) costs 28 bytes to store vs. 16 bytes for a single absolute coordinate. The delta compression means that for rooms larger than ~3 tiles, the spline approach uses less storage than absolute coordinates. And the fault tolerance is categorically better: you can lose half the room's deltas and still reconstruct it; lose one absolute coordinate and you have a hole.

---

## 6. Material Properties in FLUX-C

The FLUX-C Analog opcodes use Young's modulus (E) as the material parameter. Materials are not hard-coded into the opcode — they are loaded from a FLUX-C constant table:

| Material | E (GPa) | Density (g/cm³) | Typical Use | GUARD Symbol |
|----------|---------|-----------------|-------------|--------------|
| Cedar | 6.0 | 0.4 | Light, flexible boundaries | `GUARD_MAT_CEDAR` |
| Oak | 12.0 | 0.7 | Structural, moderate stiffness | `GUARD_MAT_OAK` |
| Fiberglass | 30.0 | 2.0 | Semi-rigid, moderate weight | `GUARD_MAT_FIBERGLASS` |
| Steel | 200.0 | 7.8 | Rigid, precise boundaries | `GUARD_MAT_STEEL` |

Additional FLUX-C constants:
- `GUARD_E` — current Young's modulus of the active material
- `GUARD_rho` — density of the active material (for weight calculations)
- `GUARD_epsilon` — plasticity coefficient (how much the material springs back after deformation)
- `GUARD_tolerance` — the room's geometric tolerance parameter

Material selection is a GUARD assertion in the PLATO room code:

```
GUARD room_material == GUARD_MAT_OAK
```

This ensures the material is set before any ANALOG_SPLINE call, satisfying the precondition.

---

## 7. Hybrid Digital-Analog Architecture

The architecture separates digital and analog concerns cleanly:

**Digital layer:**
- Tile hash computation (SHA-256, immutable once tile is placed)
- Delta stream storage and compression
- Room metadata (name, created, material, tolerance)
- Query processing (which tiles are within radius R of point P?)

**Analog layer:**
- Surface interpolation (ANALOG_SPLINE)
- Level surface computation (ANALOG_WATER_LEVEL)
- Position transfer (ANALOG_STORY_POLE)
- Proportional division (ANALOG_SECTOR)
- Curvature continuity enforcement

**Boundary (GUARD bridge):**
```
GUARD tile_within_tolerance(tile, room_spline)
  → ANALOG_SPLINE(control_points, material_E, tension)
  → compute d(tile_position, spline_output)
  → return d < tolerance
```

The boundary is where digital computation meets analog physics. The input is digital (tile hash, position). The constraint is a GUARD assertion. The output is digital (SATISFIED / VIOLATION). The computation in between is analog (spline interpolation, distance to curve).

Error bounds: ±epsilon = ±(1e-6 + material_variation × tension). This is the "analog" part — not a digital floating-point approximation of a curve, but a curve that has physical meaning (how would a plank of this material bend between these two points?).

---

## 8. R&D Iteration Cycle

Following the shipwright methodology: loft at 1:1 before committing to full construction.

### Phase 1: Digital Simulation (current)
Implement `ANALOG_SPLINE` as a digital simulation of analog behavior. The FLUX-C opcode calls a digital function that computes the spline, but the API contract is designed to match a physical spline (boundary conditions, tolerance, material parameters). Test with synthetic data: known control points, known material properties, verify output passes through boundary points.

**Deliverable:** `flux-c-analog` crate with `analog_spline`, `analog_water_level`, `analog_story_pole`, `analog_sector` functions. FLUX-C opcode encodings. Unit tests with known-good inputs.

### Phase 2: Benchmark
Measure `ANALOG_SPLINE` vs. standard digital interpolation (e.g., NumPy `scipy.interpolate.Bezier`, `scipy.interpolate.CubicSpline`). Metrics: latency per call, smoothness of output curve (second derivative continuity), memory usage. The analog approach should show better continuity properties (inherent C1 continuity from the quadratic Bézier formulation) at comparable or better performance.

**Deliverable:** Benchmark report. If digital simulation shows no advantage, revisit opcode design.

### Phase 3: Physical Prototype
Design and 3D-print a spline tool from a known material (oak or cedar filament). Fix the spline between three points, measure the actual curve with a CNC probe, compare to ANALOG_SPLINE output. This validates that the digital simulation accurately models physical behavior.

**Deliverable:** Physical spline fixture. Measurement data. Comparison to digital output.

### Phase 4: JC1 Edge Test
Deploy `ANALOG_SPLINE` to JC1 (Jetson Orin Nano, ARM64, edge encoding). Run constraint solving on a PLATO room with 50+ tiles. Verify that the opcode terminates, produces correct outputs, and stays within the edge energy budget. Benchmark against the same room on the cloud VM.

**Deliverable:** JC1 deployment. Energy measurement. Cloud vs. edge comparison.

### Phase 5: Production Integration
Integrate `ANALOG_SPLINE` as an optional PLATO room mode. Rooms can choose spline-boundary (default off) for rooms where fault tolerance and geometry continuity matter. Standard absolute-coordinate rooms remain the default for simplicity.

**Deliverable:** PLATO room mode flag. Migration path for existing rooms.

---

## 9. Shipwright R&D Lessons

Boat builders didn't jump from a mental model to a full hull. They built a half-model first, then a lofting at 1:1 scale (full-size drawing on the lofting floor), then a half-hull, then the full hull. Each stage taught them something that the previous stage couldn't:

- **Half-model** (1:4 scale): Does the overall shape look right? Is the bow entry correct?
- **Lofting** (1:1 scale): Are the curves fair? Do the ribbands line up? Are there any twists?
- **Half-hull**: Does it actually hold water? Is the balance right?
- **Full hull**: Everything works — or you find out what you missed.

We're following the same progression:
- **Phase 1 (half-model):** Digital simulation. Does the API make sense? Do the preconditions/postconditions hold?
- **Phase 2 (lofting):** Benchmark against standard approaches. Are we measuring the right things?
- **Phase 3 (half-hull):** Physical prototype. Does the real material behave as modeled?
- **Phase 4 (edge deployment):** Does it work on target hardware? Energy budget OK?
- **Phase 5 (full hull):** Production integration. The ship sails.

The iteration cycle is: **design → test → measure → refine → repeat**. Never skip stages. A full hull built without lofting will have fairing problems that cost 10× more to fix than the lofting would have taken.

---

## 10. Open Questions

1. **Tension parameter range:** 0.0–1.0 is the proposed range for tension. Should this be material-dependent (cedar can handle higher tension before kinking than steel)?

2. **Delta stream compression:** The current design stores raw deltas (each as 2× f32). Could we use delta-of-delta (second-order difference) for further compression? Would this interact with the fault tolerance properties?

3. **3D extension:** The 3-point quadratic Bézier works for 2D surfaces. For 3D rooms (volumetric PLATO spaces), we need either a tensor-product Bézier surface or a b-spline. What is the minimum useful 3D primitive?

4. **GUARD tolerance derivation:** The tolerance formula `ε + material_variation × tension` is proposed but not validated. Should we measure actual material variation for oak, cedar, fiberglass, and steel samples to get real numbers?

5. **Tile validity beyond distance:** Currently tile validity is purely geometric (distance to spline). Should we also consider tile content semantics (does this tile's type match the expected boundary type at this position)?

---

## Summary

FLUX-C analog compute provides four opcodes that treat PLATO room boundaries as continuous spline surfaces:

- `ANALOG_SPLINE` — computes a quadratic Bézier curve from three boundary points and material properties
- `ANALOG_WATER_LEVEL` — computes the least-squares level surface through a point cloud
- `ANALOG_STORY_POLE` — transfers a level surface to multiple heights via cumulative deltas
- `ANALOG_SECTOR` — divides a distance into equal proportional segments

The room's state is the spline, not a coordinate vector. Each tile placement refines the spline estimate (Kalman filter analogy). Tile validity is measured as distance to the spline curve, bounded by a GUARD tolerance derived from material properties.

Storage is reduced by ~48% for rooms larger than ~3 tiles. Fault tolerance is categorically improved: you can lose half the delta stream and still reconstruct the room; lose one absolute coordinate and you have a hole.

The R&D cycle follows shipwright practice: simulate → benchmark → physical prototype → edge test → deploy. No skipping stages. The design is ready for Phase 1 implementation.

---

*PLATO analog compute design — Oracle1, 2026-05-05*