# The Master Shipwright Archetype: Constraint Theory Formalization of Traditional Boat-Building Techniques

**Technical Whitepaper**
**Document ID:** FLUX-WHITEPUB-2026-05-05-MS
**Authors:** Cocapn Fleet Architecture Team
**Version Date:** 2026-05-05
**Target Audience:** Constraint theory researchers, PLATO contributors, distributed systems engineers, agent fleet architects

---

## 1. Abstract

This whitepaper documents the **Master Shipwright Archetype** — a formalization of 80 traditional boat-building techniques into constraint theory. We extend the seven patterns documented in *Constraint Theory Meets Construction* (FLUX-WHITEPUB-2026-05-05-CC) by integrating the full toolkit of master shipwrights: 50 physical operations (Lining Off, Spiling, Adzing, and their contemporaries) and 30 number-free analog computation tools (Story Poles, Ticking Sticks, The Sector, and their companions).

The central thesis: **master shipwrights practiced constraint propagation for centuries without the formalism.** Their tools — the Sector, the Story Pole, the Ticking Stick — are constraint engines encoded in wood and string. The "blindfolded" techniques tradesmen use on large builds represent intentional information management: tools that carry only the information that matters, when it matters. This is constraint theory at its most fundamental.

We provide complete formalization tables mapping each shipwright technique to its FLUX-C/PLATO equivalent, show how the Sector's "invisible calculation" maps to similar-triangle proportional scaling, and propose extensions to the GUARD DSL and PLATO room architecture that would enable agent fleets to reason like shipwrights.

---

## 2. Introduction: The Shipwright's Constraint Library

Every master shipwright possesses a constraint library — not written down, but embodied in their hands. Decades of building trains the eye to see where forces concentrate, where wood wants to move, where the next operation must respect the last. The hands execute what the eyes see; the brain manages the constraint graph.

This constraint library is not heuristic. It is mathematical. The Sector divides lengths into equal parts without division. The Story Pole transfers heights without knowing inches. The Water Level finds level across any distance without calculation. The Spanish Windlass amplifies small rotations into massive forces. Every tool is a specialized constraint solver — the physical world is the computational substrate.

**The insight from Casey:** "tradesmen put the blinders on for information management in large builds." Master shipwrights intentionally limit information flow. They don't measure everything — they use physical templates that carry ONLY the information that matters. This is constraint theory at its most fundamental: encode the constraint in the tool, not in a number.

This whitepaper documents that constraint library formally. We categorize the 80 techniques into two groups:

- **50 Physical Operations** — actions performed on wood (Adzing, Steam Bending, Caulking, etc.)
- **30 Number-Free Techniques** — analog computation tools that eliminate measurement (Story Poles, Sectors, Water Levels, etc.)

The number-free techniques are the critical formalization target. They represent centuries of refinement in computation-savings — tools that solve equations without writing them down.

---

## 3. The 50 Physical Operations: Constraint Enforcement Actions

The 50 physical operations are the shipwright's action vocabulary. Each operation enforces one or more constraints on the workpiece. We formalize each as a GUARD constraint opcode and identify its FLUX-C/PLATO equivalent.

### 3.1 Layout and Measurement Operations

| # | Technique | Formalization | GUARD Opcode | FLUX-C/PLATO Equivalent |
|---|-----------|---------------|--------------|------------------------|
| 1 | **Lining Off** | Mark reference lines on timber surface | `GUARD align_reference(line_id, axis)` | Delta stream alignment |
| 2 | **Spiling** | Transfer curved hull shape to flat plank via physical marking | `GUARD shape_transfer(source, target)` | Live constraint propagation |
| 3 | **Adzing** | Hewer removes wood to bring surface to line | `GUARD reduce_to_contour(contour_line)` | Boundary enforcement |
| 4 | **Slicking** | Fine shaving brings surface to true plane | `GUARD surface_truth(plane)` | Material-as-solver |
| 5 | **Fairing** | Bring curved surface to smooth continuous curve | `GUARD C2_continuous(control_points)` | Batten fairing (from Ch. 6) |
| 6 | **Steam Bending** | Heat + moisture makes wood pliable; cools into bent shape | `GUARD form_under_force(constraint_shape)` | Force-fit constraint with temporal deferral |
| 7 | **Scarfing** | Join two timbers at angled cut — each half carries partial angle | `GUARD angular_join(angle, [timber_a, timber_b])` | Constraint composition |
| 8 | **Trunnelling** | Bore hole through timber at precise angle | `GUARD bore_at_angle(angle, diameter)` | Geometric constraint enforcement |
| 9 | **Roving** | Drive wool fibers into seam as caulking | `GUARD seal_at_join(join_id)` | GUARD boundary seal |
| 10 | **Caulking** | Hammer iron rudders drive cotton/oakum into seams | `GUARD compress_into_seam(seam_id, material)` | Compression constraint |
| 11 | **Rabbeting** | Cut step-shaped groove along edge | `GUARD groove_along_edge(depth, width)` | Step constraint |
| 12 | **Beveling** | Cut angled surface to match adjacent angle | `GUARD angle_match(reference_surface)` | Bevel Gauge pattern |
| 13 | **Lofting** | Full-scale drawing on floor; build parts directly on lines | `GUARD full_scale_layout(drawing_id)` | Direct measurement (no abstraction) |
| 14 | **Planking Scale Calculation** | Compute plank width/length from lofting offsets | `GUARD scale_from_offsets(offset_list)` | Derived constraint computation |
| 15 | **Clinch Bolting** | Iron nail clenched over washer inside hole | `GUARD clenched_fastener(fastener_id)` | Invariant enforcement |
| 16 | **Gouging** | Curved chisel removes wood in channel | `GUARD channel_cut(profile)` | Groove constraint |
| 17 | **Calking V-Grooving** | Cut V-shaped groove for caulking material | `GUARD v_groove(depth, angle)` | Tapered constraint |
| 18 | **Tapering** | Gradually reduce thickness toward edge | `GUARD taper(length, reduction)` | Gradient constraint |
| 19 | **Dubbing** | Hollow out concave surface | `GUARD concave_contour(radius)` | Radius constraint |
| 20 | **Mortising** | Cut rectangular hole for tenon | `GUARD rectangular_hole(dim_a, dim_b, depth)` | Template constraint |
| 21 | **Tenoning** | Cut projecting tongue to fit mortise | `GUARD tongue_match(mortise_ref)` | Template matching |
| 22 | **Scribing** | Compass traces exact profile from reference surface | `GUARD profile_copy(source_contour)` | Zero-gap constraint transfer |
| 23 | **Plumb-lining** | String + plumb bob finds vertical reference | `GUARD vertical_reference()` | Gravity constraint |
| 24 | **Boring** | Drill holes for fasteners | `GUARD bore(diameter, depth, angle)` | Geometric constraint |
| 25 | **Laminating** | Build up thickness from multiple glued layers | `GUARD layered_buildup(thickness, layers)` | Stack constraint |
| 26 | **Dowel Pinning** | Drive wooden peg through parts | `GUARD peg_constraint(peg_dia, hole_ref)` | Invariant matching |
| 27 | **Chamfering** | Bevel edge to remove sharpness | `GUARD edge_bevel(angle, width)` | Surface transition |
| 28 | **Hollowing** | Excavate interior of large timber | `GUARD interior_contour(outer_wall, inner_wall)` | Cavity constraint |
| 29 | **Back-beveling** | Bevel背面 of board for better fit | `GUARD backside_bevel(angle)` | Secondary surface constraint |
| 30 | **Template Making** | Create full-scale pattern of complex shape | `GUARD template_create(shape_ref)` | Constraint archetype |
| 31 | **Lead-lining** | Lead sheet beaten into hull interior | `GUARD liner_constraint(liner_id)` | Internal boundary |
| 32 | **Batten Splicing** | Join two battens with overlapping scarf | `GUARD batten_join(length, scarf_ratio)` | Continuity constraint |
| 33 | **Counter-boring** | Bore enlarged section for bolt head | `GUARD head clearance(head_dia, depth)` | Geometric accommodation |
| 34 | **Wedge Driving** | Use wedge to draw joints tight | `GUARD wedge_force(direction, magnitude)` | Mechanical advantage constraint |
| 35 | **Planking Jacking** | Push plank against frame with jacks | `GUARD jacking_force(direction)` | Force application constraint |
| 36 | **Leveling** | Check and correct horizontal plane | `GUARD horizontal_plane(tolerance)` | Level constraint |
| 37 | **Checking Squareness** | Verify 90° relationship between surfaces | `GUARD right_angle(axis_a, axis_b)` | Triangle constraint (3-4-5) |
| 38 | **Fairing Ribbands** | Long battens temporarily fastened to frames | `GUARD ribband_fair([frame_list])` | Batten fairing C² |
| 39 | **Siding/Molding** | Shape timber to given profile | `GUARD profile_section(section_id)` | Cross-section constraint |
| 40 | **Treenail Wedging** | Wooden nail driven into undersized hole; swells | `GUARD wedge_expansion(nail_id)` | Material expansion constraint |
| 41 | **Keel Squaring** | Bring keel stock to uniform rectangular section | `GUARD rectangular_section(width, depth)` | Uniformity constraint |
| 42 | **Stem Fitting** | Fit stem timber to keel angle | `GUARD stem_angle(keel_ref)` | Angular join |
| 43 | **Stern Post Alignment** | Align stern post vertically and with centerline | `GUARD post_alignment(centerline)` | Axis alignment |
| 44 | **Garboard Fitting** | Fit first planking strake to keel | `GUARD garboard_fit(keel_ref)` | Initial boundary constraint |
| 45 | **Cambering** | Add small rise amidships for water shedding | `GUARD camber_curve(height, span)` | Curvature constraint |
| 46 | **Deck Beaming** | Shape and install deck beams | `GUARD beam_installation([beam_list])` | Structural constraint |
| 47 | **Knee Shaping** | Fit natural or assembled knee brackets | `GUARD knee_bracket(angle)` | Angular constraint |
| 48 | **Transom Fitting** | Fit transom to stern shape | `GUARD transom_fit(stern_ref)` | Terminal boundary |
| 49 | **Gunwale Capping** | Install capping rail on rail curve | `GUARD rail_installation(curve_ref)` | Rail constraint |
| 50 | **Mast Hewing** | Shape mast from rough square stock | `GUARD taper_section(length, diameter_top)` | Taper constraint |

### 3.2 Physical Operations: Key Formalizations

**Steam Bending** is force-fit with temporal deferral. The wood is forced into a die (the constraint shape), held there while hot, then released. The wood "wants" to return to its original shape — spring-back — but cools into the constrained shape. This is identical to furniture making's spring-back pattern:

```
GUARD form_under_force(constraint_shape, hold_time=t_cool, spring_back=0.05)
```

**Scarfing** demonstrates constraint composition: each half of the joint carries partial angle information. Neither half knows the full angle — together they satisfy the constraint. This is lazy constraint evaluation across distributed parts.

**Treenail Wedging** is material-expansion constraint solving: the wooden peg (treenail) is slightly larger than the hole. Driven under force, the wood compresses. When the driving stops, the wood swells slightly (moisture + compression recovery) and locks the joint. The peg enforces its own constraint.

---

## 4. The 30 Number-Free Techniques: Analog Computation Tools

These are the critical formalizations. Number-free techniques eliminate measurement by encoding constraints directly in the tool. The tool IS the constraint — no numbers required.

### 4.1 Core Number-Free Techniques

| # | Technique | Formalization | GUARD Opcode | FLUX-C/PLATO Equivalent |
|---|-----------|---------------|--------------|------------------------|
| 1 | **Story Poles** | Notched rod transfers vertical heights; records relative offsets | `GUARD delta_transfer(prev_mark, curr_mark)` | PLATO delta stream (what changed) |
| 2 | **Tick-Sticking** | Point-transfer sticks map irregular hull shapes to flat templates | `GUARD point_transfer([point_list])` | Ticking Stick pattern |
| 3 | **Batten Fairing** | Long springy strips find natural fair curve through control points | `GUARD C2_continuous([p1..pn])` | Batten spline constraint |
| 4 | **Scribing** | Compass traces exact profile onto adjacent surface | `GUARD profile_copy(source_surface)` | Zero-gap template constraint |
| 5 | **Spiling Battens** | Thin cedar strips physically mark shape directly on plank | `GUARD live_mark(source_curve)` | Live constraint propagation |
| 6 | **Staffing** | Flexible rods determine girth and proportional widths | `GUARD proportional_width(reference, ratio)` | Proportional constraint |
| 7 | **Lofting at 1:1** | Full-scale drawing on floor; build directly on the lines | `GUARD full_scale_build()` | Direct constraint (no abstraction) |
| 8 | **Plumb-Bobs** | Gravity + string for perfect verticality | `GUARD gravity_reference()` | Vertical constraint via physics |
| 9 | **Water Levels** | Clear hose finds level line across any distance | `GUARD hydrostatic_level()` | Material-as-solver (physics solves equation) |
| 10 | **Bevel Gauges** | Mechanical "angle-stealers" transfer pitch without knowing degrees | `GUARD angle_transfer(angle_ref)` | Constraint routing without coordinate conversion |
| 11 | **Molds & Jigs** | 1:1 frames as stencils for repetitive shaping | `GUARD stencil_constraint(stencil_id)` | Constraint archetypes (room templates) |
| 12 | **The Sector** | Folding geometric tool divides lengths into equal parts WITHOUT division | `GUARD proportional_divide(length, n)` | Simplex projection |
| 13 | **Chalk Lining** | Snapped string creates perfect straight reference over any distance | `GUARD straight_line(point_a, point_b)` | Linear constraint |
| 14 | **Girth Tapes** | Non-elastic string compares distances by marking points | `GUARD distance_compare([point_list])` | Relative measurement constraint |
| 15 | **Sight-Lines** | Closing one eye detects unfairness in curves | `GUARD visual_fairness_check()` | Continuity verification |
| 16 | **Dividers** | Two-pointed legs step off equal increments | `GUARD equal_increment(step_count)` | Discrete partitioning |
| 17 | **Caliper Transfer** | Metal arms capture and replicate thickness | `GUARD thickness_copy(source)` | Invariant enforcement |
| 18 | **Spar Gauges** | Preset wooden blocks with pegs for "eight-squaring" | `GUARD square_section(tolerance)` | Section uniformity constraint |
| 19 | **Templates** | Thin plywood "shadows" of complex parts | `GUARD template_match(shape_ref)` | Shape constraint |
| 20 | **Springing the Plank** | Physical force + deadheads find where plank wants to sit | `GUARD natural_position(plank_id)` | Material preference constraint |
| 21 | **Centerline Stretching** | Taut wire aligns stem, keel, stern post | `GUARD axis_alignment([point_list])` | Linear alignment |
| 22 | **Symmetry Checking** | Fixed-length stick compares port/starboard distances | `GUARD symmetry_verify(length)` | Mirror constraint |
| 23 | **Rabbet Squaring** | Scrap piece checks groove depth | `GUARD depth_verify(groove_ref)` | Fit verification |
| 24 | **Trunnel Sizing** | Drive peg through die plate to match hole diameter | `GUARD invariant_match(peg_ref)` | Exact matching constraint |
| 25 | **The Shifting Stock** | Wooden bevel board records and carries changing hull angles | `GUARD angle_sequence([angle_list])` | Constraint chain |
| 26 | **Marking Gauges** | Thumb-screw tool scribes line parallel to edge | `GUARD parallel_offset(distance)` | Offset constraint |
| 27 | **Trammel Points** | Large wooden-beam compasses swing massive arcs | `GUARD arc_trace(radius, center)` | Radius constraint |
| 28 | **Spanish Windlass** | Rope + twisting stick amplifies small rotation into large force | `GUARD mechanical_advantage(lever_ratio)` | Constraint amplification |
| 29 | **Story-String** | Knotted string remembers specific dimensions | `GUARD string记忆中(dim_ref)` | Stored constraint reference |
| 30 | **Shadow-Boxing** | Light source casts frame shadow to check symmetry | `GUARD shadow_verify(light_ref)` | Optical symmetry check |

---

## 5. The Sector: Invisible Calculation via Similar Triangles

The Sector is the most mathematically sophisticated of the number-free tools. It deserves detailed treatment.

### 5.1 The Technique

The Sector is a folding geometric tool with two legs marked in equal divisions (usually 10 or 12 units). To divide a plank into 5 equal strakes without a calculator:

1. Set dividers to the total width of the plank
2. Open the Sector until the divider tips fit the "10" marks on both legs
3. **Without moving the Sector**, place dividers on the "2" marks on both legs
4. That distance is exactly 1/5th of the plank width

No division required. No decimals. No measurement in inches.

### 5.2 The Mathematics

The Sector implements **similar triangle proportional scaling**:

```
total_width / 10 = segment_width / 2
segment_width = total_width * (2/10) = total_width / 5
```

The constraint is encoded in the geometry of the Sector legs. The "10" marks establish the reference triangle; the "2" marks establish the proportional subdivision. The Sector IS the equation — geometry instead of numbers.

### 5.3 Formalization

```
GUARD proportional_divide(total_width, n_equal_parts):
    # Similar triangle: set legs to span across reference marks
    reference_triangle = span(sector_legs, mark_a, mark_b)
    # Without moving, read segment from subdivision marks
    segment = read(sector_legs, subdivide_a, subdivide_b)
    # segment = total_width * (subdivide_b - subdivide_a) / (mark_b - mark_a)
    return segment
```

For the 5-strake case:
```
GUARD proportional_divide(width, 5)
→ returns width * 2/10 = width/5
```

The GUARD stores the geometric construction, not the numeric result. The construction IS the constraint.

### 5.4 FLUX-C Implications

FLUX-C should support a PROPORTIONAL opcode:

```
PROPORTIONAL DIVIDE width, 5 → [w1, w2, w3, w4, w5]  # 5 equal parts
PROPORTIONAL SCALE width, ratio → scaled_width        # proportional scaling
```

The PROPORTIONAL opcode implements similar-triangle construction without numeric division. This is the Sector's "invisible calculation" in bytecode form.

---

## 6. The Story Pole: Source of Truth via Relative Transfer

The Story Pole is the shipwright's source of truth for vertical measurements.

### 6.1 The Technique

A Story Pole is a long wooden rod with notches cut at every critical height encountered during construction. On a large build, the pole might carry 40+ notches — each representing a height encountered at a specific location.

Key properties:
- **Source of truth:** The pole records what IS, not what SHOULD BE
- **Relative transfer:** Flip the pole to the other side of a frame — if marks don't align, you know how much to move the frame WITHOUT knowing if the distance was 4 feet or 4.125 inches
- **Cumulative error elimination:** Tape measure errors compound over distance. The Story Pole transfers only the offset that matters: "here to here."

### 6.2 The Mathematics

The Story Pole implements **delta encoding** — what changed, not absolute state:

```
GUARD delta_transfer(prev_mark, curr_mark):
    # Returns the OFFSET, not the absolute value
    offset = curr_mark.position - prev_mark.position
    return offset
```

Application:
```
# Mark the starboard side of frame #7
mark_A = drive_pole(starboard_ref, frame_7_height)
# Flip to port side, check alignment
port_offset = check_pole_alignment(port_ref, mark_A)
# port_offset tells you how much to move frame
# It does NOT tell you the frame's absolute height
```

The Story Pole doesn't care about absolute coordinates. It only cares about offsets.

### 6.3 FLUX-C Implications

FLUX-C should support DELTA opcodes:

```
DELTA PREV curr_mark    → prev_position
DELTA CURR prev_mark    → curr_position
DELTA DIFF a, b        → offset_between(a, b)
```

The DELTA opcode returns what changed, not absolute state. This eliminates cumulative error by never storing absolute values in the transfer chain.

---

## 7. The Mapping Tables: Complete Constraint Formalization

### 7.1 Tool-to-Formalization Mapping

| Shipwright Tool | Formalization | FLUX-C Opcode | PLATO Equivalent |
|----------------|---------------|----------------|------------------|
| **Sector** | Similar triangles → proportional scaling without calculation | `PROPORTIONAL DIVIDE w, n` | Simplex projection (Pythagorean snapping) |
| **Story Pole** | Relative transfers, not absolute values. Cumulative error eliminated | `DELTA TRANSFER prev, curr` | PLATO delta streams |
| **Ticking Stick** | Physical template transfers complex shape without measurement | `TEMPLATE COPY shape_ref` | Constraint template (GUARD pattern) |
| **Spiling Battens** | Physically marks shape directly on plank | `LIVE MARK source_curve` | Live constraint propagation |
| **Bevel Gauge** | Captures angle physically, carries it to next location | `ANGLE TRANSFER angle_ref` | Constraint routing without coordinate conversion |
| **Water Level** | Water finds same level — physics solves the equation | `HYDROSTATIC LEVEL` | Material-as-solver |
| **Spanish Windlass** | Small rotation → large force via mechanical advantage | `MECH ADVANTAGE ratio` | Constraint amplification in fleet coordination |
| **Lofting at 1:1** | Full-scale drawing — build directly on the lines | `FULL SCALE BUILD` | Direct measurement (no abstraction) |
| **Molds & Jigs** | Physical stencil for complex shapes | `STENCIL CONSTRAINT id` | Constraint archetypes (room templates in PLATO) |
| **Trunnel Sizing** | Peg driven through plate ensures hole matches peg exactly | `INVARIANT MATCH peg_ref` | Invariant enforcement (GUARD pattern) |
| **Batten Fairing** | Long strips enforce C² continuity via material properties | `C2 CONTINUOUS [pts]` | Batten spline constraint |
| **Shadow-Boxing** | Light casts frame shadow to check symmetry | `SHADOW VERIFY light` | Optical symmetry verification |
| **Centerline Stretching** | Taut wire aligns stem, keel, stern post | `AXIS ALIGN [pts]` | Linear alignment constraint |
| **Symmetry Checking** | Fixed-length stick compares port/starboard distances | `SYMMETRY VERIFY length` | Mirror constraint |
| **Dividers** | Step off equal increments without measurement | `EQUAL INCREMENT n` | Discrete partitioning |
| **Girth Tapes** | Non-elastic string compares distances by marking | `DISTANCE COMPARE [pts]` | Relative measurement |

### 7.2 FLUX-C Design Implications

The 30 number-free techniques suggest the following GUARD DSL extensions:

**1. PROPORTIONAL — Similar Triangle Construction**
```
PROPORTIONAL DIVIDE width, 5      # Returns 5 equal parts via geometric construction
PROPORTIONAL SCALE width, 0.618   # Golden ratio scaling without calculation
```

**2. DELTA — Relative Transfer**
```
DELTA TRANSFER prev, curr         # Returns offset, not absolute value
DELTA DIFF a, b                   # Returns difference between two marks
```

**3. TEMPLATE — Shape Transfer**
```
TEMPLATE COPY source_surface      # Zero-gap profile transfer
TEMPLATE STENCIL id               # 1:1 shape reproduction
```

**4. LIVE — Live Constraint Propagation**
```
LIVE MARK source_curve            # Physically mark shape on target surface
LIVE CONSTRAINT source, target    # Enforce source curve on target
```

**5. MATERIAL — Material-as-Solver**
```
MATERIAL HYDROSTATIC LEVEL       # Water finds level (physics solves)
MATERIAL BATTER FAIR [pts]       # Strip material enforces C² continuity
MATERIAL SPRING BACK piece       # Account for elastic recovery
```

**6. AMPLIFY — Mechanical Advantage**
```
AMPLIFY ROTATION torque, 10       # 10:1 mechanical advantage
AMPLIFY FORCE rotation, distance  # Force amplification via lever
```

---

## 8. Information Management: The Blindfolded Principle

### 8.1 Casey's Insight

**"Tradesmen put the blinders on for information management in large builds."**

On a vessel with 40-foot hulls, 200 frames, and thousands of parts, measuring everything in absolute coordinates would be catastrophic. Tape measures accumulate error. A 1/16th inch per joint error, compounded over 200 joints, is 12.5 inches of total drift. The hull would be unflyable.

Master shipwrights solve this by **intentionally limiting information flow.** They don't measure everything — they use physical templates that carry ONLY the information that matters, WHEN it matters.

### 8.2 The Four Blindfolded Principles

**Principle 1: Encode the Constraint in the Tool, Not in a Number**

The Sector doesn't tell you the width in inches. It tells you the proportion. The Story Pole doesn't tell you the distance. It tells you the offset from the previous mark. The ticking stick doesn't measure the shape. It copies it directly.

**Principle 2: Carry Only the Information That Matters**

A Story Pole with 40 notches carries 40 relative offsets. It does NOT carry a coordinate system. It doesn't need one. The information that matters is: "this frame is 2-3/8 inches lower than this mark."

**Principle 3: Eliminate Cumulative Error at Every Transfer**

Every transfer is delta-encoded. The tape measure is the enemy — it stores absolute values that compound error. The Story Pole stores relative values that transfer without drift.

**Principle 4: Use Physics as the Solver**

The Water Level doesn't calculate level. Water finds level. The Batten doesn't solve for fair curve. Wood bends fair. The plumb bob doesn't compute verticality. Gravity defines it. When the material IS the solver, you eliminate the computation.

### 8.3 Formalization: Latent Information

This is **latent information** — the constraint is encoded in the tool, not in a number:

```
Sector:    Proportional relation (2/10 ratio) encodes the division constraint
Story Pole: Offset between marks encodes relative position
Batten:    Material stiffness encodes C² continuity
Water:     Hydrostatic equilibrium encodes level
Plumb:     Gravity vector encodes verticality
```

Latent information is constraint-as-material. The constraint cannot be violated without breaking the tool.

---

## 9. PLATO Implications: Rooms as Story Poles

### 9.1 The Room Boundary is a Story Pole

In PLATO, the room boundary emerges from the first tiles placed. Subsequent tiles measure against the emerging boundary, not against a pre-defined coordinate system. This is the Story Pole pattern:

1. First tile is placed → establishes initial reference
2. Second tile measures its relation to the first tile → records relative offset
3. Third tile measures its relation to the second → continues the chain
4. The room boundary IS the Story Pole — emerges from tiles, carries forward

```
GUARD room_delta(tile_n, tile_n_minus_1):
    # Returns what changed, not absolute state
    offset = tile_n.position - tile_n_minus_1.position
    return offset
```

### 9.2 Tiles as Ticking Sticks

Each tile copies shape from the previous constraint, not measured independently. Like a Ticking Stick tracing a hull curve onto a template:

1. Tile N constrains Tile N+1 by proximity
2. Tile N+1 records its position relative to Tile N
3. Global shape emerges from local constraint propagation

### 9.3 Room Templates as Molds

Pre-defined room shapes are molds and jigs — 1:1 templates that tiles conform to:

```
GUARD room_template_apply(template_id):
    # Room conforms to mold shape
    enforce(shape_mold[template_id])
```

---

## 10. Complete Technique Catalog

### 10.1 The 50 Physical Operations (with formalization summary)

1. **Lining Off** — Reference line marking → `GUARD align_reference`
2. **Spiling** — Shape transfer → `GUARD shape_transfer`
3. **Adzing** — Surface reduction → `GUARD reduce_to_contour`
4. **Slicking** — Surface planing → `GUARD surface_truth`
5. **Fairing** — Curve smoothing → `GUARD C2_continuous`
6. **Steam Bending** — Heat forming → `GUARD form_under_force`
7. **Scarfing** — Angle joining → `GUARD angular_join`
8. **Trunnelling** — Angle boring → `GUARD bore_at_angle`
9. **Roving** — Seam sealing → `GUARD seal_at_join`
10. **Caulking** — Iron driving → `GUARD compress_into_seam`
11. **Rabbeting** — Step grooving → `GUARD groove_along_edge`
12. **Beveling** — Angle cutting → `GUARD angle_match`
13. **Lofting** — Full-scale layout → `GUARD full_scale_layout`
14. **Planking Scale Calculation** — Scale computation → `GUARD scale_from_offsets`
15. **Clinch Bolting** — Clenched fastening → `GUARD clenched_fastener`
16. **Gouging** — Channel cutting → `GUARD channel_cut`
17. **Calking V-Grooving** — V-groove cutting → `GUARD v_groove`
18. **Tapering** — Thickness reduction → `GUARD taper`
19. **Dubbing** — Concavity cutting → `GUARD concave_contour`
20. **Mortising** — Rectangular hole → `GUARD rectangular_hole`
21. **Tenoning** — Tongue cutting → `GUARD tongue_match`
22. **Scribing** — Profile copying → `GUARD profile_copy`
23. **Plumb-lining** — Vertical reference → `GUARD vertical_reference`
24. **Boring** — Hole drilling → `GUARD bore`
25. **Laminating** — Layered buildup → `GUARD layered_buildup`
26. **Dowel Pinning** — Peg fastening → `GUARD peg_constraint`
27. **Chamfering** — Edge beveling → `GUARD edge_bevel`
28. **Hollowing** — Interior excavation → `GUARD interior_contour`
29. **Back-beveling** — Back beveling → `GUARD backside_bevel`
30. **Template Making** — Pattern creation → `GUARD template_create`
31. **Lead-lining** — Interior lead → `GUARD liner_constraint`
32. **Batten Splicing** — Batten joining → `GUARD batten_join`
33. **Counter-boring** — Head clearance → `GUARD head_clearance`
34. **Wedge Driving** — Wedge forcing → `GUARD wedge_force`
35. **Planking Jacking** — Plank forcing → `GUARD jacking_force`
36. **Leveling** — Horizontal checking → `GUARD horizontal_plane`
37. **Checking Squareness** — 90° verification → `GUARD right_angle`
38. **Fairing Ribbands** — Temporary fairing → `GUARD ribband_fair`
39. **Siding/Molding** — Profile shaping → `GUARD profile_section`
40. **Treenail Wedging** — Swell fastening → `GUARD wedge_expansion`
41. **Keel Squaring** — Keel uniformizing → `GUARD rectangular_section`
42. **Stem Fitting** — Stem joining → `GUARD stem_angle`
43. **Stern Post Alignment** — Post alignment → `GUARD post_alignment`
44. **Garboard Fitting** — First strake fitting → `GUARD garboard_fit`
45. **Cambering** — Deck crowning → `GUARD camber_curve`
46. **Deck Beaming** — Beam installation → `GUARD beam_installation`
47. **Knee Shaping** — Knee fitting → `GUARD knee_bracket`
48. **Transom Fitting** — Transom fitting → `GUARD transom_fit`
49. **Gunwale Capping** — Rail installation → `GUARD rail_installation`
50. **Mast Hewing** — Mast tapering → `GUARD taper_section`

### 10.2 The 30 Number-Free Techniques (with formalization summary)

1. **Story Poles** — Delta encoding → `GUARD delta_transfer`
2. **Tick-Sticking** — Point transfer → `GUARD point_transfer`
3. **Batten Fairing** — C² continuity → `GUARD C2_continuous`
4. **Scribing** — Profile copying → `GUARD profile_copy`
5. **Spiling Battens** — Live marking → `GUARD live_mark`
6. **Staffing** — Proportional width → `GUARD proportional_width`
7. **Lofting at 1:1** — Full-scale build → `GUARD full_scale_build`
8. **Plumb-Bobs** — Gravity reference → `GUARD gravity_reference`
9. **Water Levels** — Hydrostatic level → `GUARD hydrostatic_level`
10. **Bevel Gauges** — Angle transfer → `GUARD angle_transfer`
11. **Molds & Jigs** — Stencil constraint → `GUARD stencil_constraint`
12. **The Sector** — Proportional division → `GUARD proportional_divide`
13. **Chalk Lining** — Straight line → `GUARD straight_line`
14. **Girth Tapes** — Distance comparison → `GUARD distance_compare`
15. **Sight-Lines** — Visual fairness → `GUARD visual_fairness_check`
16. **Dividers** — Equal increments → `GUARD equal_increment`
17. **Caliper Transfer** — Thickness copying → `GUARD thickness_copy`
18. **Spar Gauges** — Square section → `GUARD square_section`
19. **Templates** — Shape matching → `GUARD template_match`
20. **Springing the Plank** — Natural position → `GUARD natural_position`
21. **Centerline Stretching** — Axis alignment → `GUARD axis_alignment`
22. **Symmetry Checking** — Mirror verification → `GUARD symmetry_verify`
23. **Rabbet Squaring** — Depth verification → `GUARD depth_verify`
24. **Trunnel Sizing** — Invariant matching → `GUARD invariant_match`
25. **The Shifting Stock** — Angle sequence → `GUARD angle_sequence`
26. **Marking Gauges** — Parallel offset → `GUARD parallel_offset`
27. **Trammel Points** — Arc tracing → `GUARD arc_trace`
28. **Spanish Windlass** — Mechanical advantage → `GUARD mechanical_advantage`
29. **Story-String** — Stored dimension → `GUARD string记忆`
30. **Shadow-Boxing** — Shadow verification → `GUARD shadow_verify`

---

## 11. Extended Mapping: All 80 Techniques to FLUX-C/PLATO

| Technique | Category | Formalization | Primary GUARD Opcode | PLATO Equivalent |
|-----------|----------|---------------|---------------------|-----------------|
| Lining Off | Physical | Reference alignment | `align_reference` | Delta stream |
| Spiling | Physical | Shape transfer | `shape_transfer` | Live propagation |
| Adzing | Physical | Surface reduction | `reduce_to_contour` | Boundary enforcement |
| Slicking | Physical | Surface planing | `surface_truth` | Material-as-solver |
| Fairing | Physical | C² continuity | `C2_continuous` | Batten constraint |
| Steam Bending | Physical | Force form | `form_under_force` | Force-fit temporal |
| Scarfing | Physical | Angular join | `angular_join` | Constraint composition |
| Trunnelling | Physical | Angle bore | `bore_at_angle` | Geometric constraint |
| Roving | Physical | Seam seal | `seal_at_join` | Boundary seal |
| Caulking | Physical | Compression | `compress_into_seam` | Compression constraint |
| Rabbeting | Physical | Step groove | `groove_along_edge` | Step constraint |
| Beveling | Physical | Angle match | `angle_match` | Bevel gauge |
| Lofting | Physical | Full-scale layout | `full_scale_layout` | Direct measurement |
| Planking Scale Calc | Physical | Scale compute | `scale_from_offsets` | Derived constraint |
| Clinch Bolting | Physical | Clench fastener | `clenched_fastener` | Invariant enforce |
| Gouging | Physical | Channel cut | `channel_cut` | Groove constraint |
| Calking V-Grooving | Physical | V-groove | `v_groove` | Tapered constraint |
| Tapering | Physical | Thickness reduce | `taper` | Gradient constraint |
| Dubbing | Physical | Concavity | `concave_contour` | Radius constraint |
| Mortising | Physical | Rect hole | `rectangular_hole` | Template constraint |
| Tenoning | Physical | Tongue match | `tongue_match` | Template matching |
| Scribing | Physical | Profile copy | `profile_copy` | Zero-gap transfer |
| Plumb-lining | Physical | Vertical ref | `vertical_reference` | Gravity constraint |
| Boring | Physical | Hole drill | `bore` | Geometric constraint |
| Laminating | Physical | Layer buildup | `layered_buildup` | Stack constraint |
| Dowel Pinning | Physical | Peg constraint | `peg_constraint` | Invariant match |
| Chamfering | Physical | Edge bevel | `edge_bevel` | Surface transition |
| Hollowing | Physical | Interior excav | `interior_contour` | Cavity constraint |
| Back-beveling | Physical | Back bevel | `backside_bevel` | Secondary surface |
| Template Making | Physical | Create pattern | `template_create` | Constraint archetype |
| Lead-lining | Physical | Lead liner | `liner_constraint` | Internal boundary |
| Batten Splicing | Physical | Batten join | `batten_join` | Continuity |
| Counter-boring | Physical | Head clear | `head_clearance` | Geometric accom |
| Wedge Driving | Physical | Wedge force | `wedge_force` | Mechanical adv |
| Planking Jacking | Physical | Jacking force | `jacking_force` | Force apply |
| Leveling | Physical | Horizontal chk | `horizontal_plane` | Level constraint |
| Checking Squareness | Physical | 90° verify | `right_angle` | Triangle constraint |
| Fairing Ribbands | Physical | Temp fairing | `ribband_fair` | Batten C² |
| Siding/Molding | Physical | Profile shape | `profile_section` | Cross-section |
| Treenail Wedging | Physical | Swell expand | `wedge_expansion` | Material expansion |
| Keel Squaring | Physical | Rect section | `rectangular_section` | Uniformity |
| Stem Fitting | Physical | Stem angle | `stem_angle` | Angular join |
| Stern Post Alignment | Physical | Post align | `post_alignment` | Axis alignment |
| Garboard Fitting | Physical | First strake | `garboard_fit` | Initial boundary |
| Cambering | Physical | Crown curve | `camber_curve` | Curvature |
| Deck Beaming | Physical | Beam install | `beam_installation` | Structural |
| Knee Shaping | Physical | Knee fit | `knee_bracket` | Angular |
| Transom Fitting | Physical | Transom fit | `transom_fit` | Terminal boundary |
| Gunwale Capping | Physical | Rail install | `rail_installation` | Rail constraint |
| Mast Hewing | Physical | Mast taper | `taper_section` | Taper |
| Story Poles | Number-Free | Delta transfer | `delta_transfer` | Delta stream |
| Tick-Sticking | Number-Free | Point transfer | `point_transfer` | Ticking stick |
| Batten Fairing | Number-Free | C² continuity | `C2_continuous` | Batten spline |
| Scribing | Number-Free | Profile copy | `profile_copy` | Zero-gap template |
| Spiling Battens | Number-Free | Live mark | `live_mark` | Live propagation |
| Staffing | Number-Free | Prop width | `proportional_width` | Proportional |
| Lofting at 1:1 | Number-Free | Full-scale build | `full_scale_build` | Direct |
| Plumb-Bobs | Number-Free | Gravity ref | `gravity_reference` | Vertical via physics |
| Water Levels | Number-Free | Hydrostatic | `hydrostatic_level` | Material-as-solver |
| Bevel Gauges | Number-Free | Angle transfer | `angle_transfer` | Route without coords |
| Molds & Jigs | Number-Free | Stencil | `stencil_constraint` | Archetypes (rooms) |
| The Sector | Number-Free | Prop divide | `proportional_divide` | Simplex projection |
| Chalk Lining | Number-Free | Straight line | `straight_line` | Linear |
| Girth Tapes | Number-Free | Dist compare | `distance_compare` | Relative measure |
| Sight-Lines | Number-Free | Visual check | `visual_fairness_check` | Continuity verify |
| Dividers | Number-Free | Equal incr | `equal_increment` | Discrete partition |
| Caliper Transfer | Number-Free | Thickness copy | `thickness_copy` | Invariant enforce |
| Spar Gauges | Number-Free | Square section | `square_section` | Uniformity |
| Templates | Number-Free | Shape match | `template_match` | Shape constraint |
| Springing Plank | Number-Free | Natural pos | `natural_position` | Material pref |
| Centerline Stretch | Number-Free | Axis align | `axis_alignment` | Linear align |
| Symmetry Checking | Number-Free | Mirror verify | `symmetry_verify` | Mirror constraint |
| Rabbet Squaring | Number-Free | Depth verify | `depth_verify` | Fit verify |
| Trunnel Sizing | Number-Free | Invariant match | `invariant_match` | Exact match |
| Shifting Stock | Number-Free | Angle sequence | `angle_sequence` | Constraint chain |
| Marking Gauges | Number-Free | Parallel off | `parallel_offset` | Offset constraint |
| Trammel Points | Number-Free | Arc trace | `arc_trace` | Radius constraint |
| Spanish Windlass | Number-Free | Mech adv | `mechanical_advantage` | Constraint amplify |
| Story-String | Number-Free | Stored dim | `string记忆` | Stored constraint |
| Shadow-Boxing | Number-Free | Shadow verify | `shadow_verify` | Optical symmetry |

---

## 12. Key Insights: What Shipwrights Knew

### 12.1 The Invisible Calculations

Master shipwrights performed calculations without writing them down:

- **The Sector's division:** Proportional reasoning via similar triangles
- **The Story Pole's offsets:** Delta encoding without absolute coordinates
- **The Water Level's level-finding:** Physics-as-solver without equations
- **The Batten's fair curve:** C² continuity via material properties

These are not approximations. They are exact solutions computed by geometry and material science.

### 12.2 The Blindfolded Principle in Practice

On a 40-foot hull build:
- A tape measure user accumulates 12+ inches of error over 200 joints
- A Story Pole user accumulates zero error — every transfer is delta-referenced
- A template user eliminates measurement entirely — the tool IS the constraint

The tradesman's "blinders" are not ignorance. They are intentional information management.

### 12.3 Constraint as Material

The deepest insight: **the constraint can be the material.**

- The Batten IS the C² continuity constraint
- The Water IS the level constraint
- The Plumb Bob IS the verticality constraint
- The Sector IS the proportional division constraint

When the material is the solver, you eliminate computation. This is constraint theory at its most fundamental: the constraint is embodied in the tool, not expressed in a number.

---

## 13. Implications for Agent Fleet Design

### 13.1 Fleet Coordination as Spanish Windlass

A Spanish Windlass takes small rotations (one person turning a stick) and amplifies them into massive forces (rope tension drawing hull planks tight). The mechanical advantage is 10:1 or more.

Fleet coordination should work the same way. One agent's small action (setting a Story Pole mark) should amplify into a large constraint effect (aligning an entire hull frame). The constraint amplification ratio should be high: a single tile placement constrains 10+ subsequent placements.

### 13.2 Agent Tiles as Ticking Sticks

Each agent in a fleet should work like a Ticking Stick:
- Copy shape from the previous constraint, not from measurement
- Record relative position, not absolute coordinate
- Pass the constraint forward, not the coordinate system

This eliminates cumulative error in fleet coordination. The fleet doesn't need a global coordinate system — it needs a chain of relative transfers.

### 13.3 Room Boundaries as Story Poles

PLATO rooms should function as Story Poles:
- The first tile establishes the initial reference
- Subsequent tiles measure against the emerging boundary
- The room boundary carries forward only what matters: the deltas
- Cumulative error is eliminated by delta propagation

---

## 14. Conclusion: The Shipwright's Legacy

Master shipwrights developed a constraint library over centuries. They formalized it not in papers but in hands — the hands that knew how to read a hull's curve, how to feel when a plank was ready to bend, how to trust the Story Pole over the tape measure.

This whitepaper has documented that constraint library formally. The 80 techniques — 50 physical operations and 30 number-free computation tools — map onto a complete constraint theory framework:

- **50 GUARD opcodes** for physical constraint enforcement
- **30 GUARD opcodes** for analog computation (number-free techniques)
- **Proportional division** via similar triangles (Sector)
- **Delta encoding** via relative transfers (Story Pole)
- **Material-as-solver** via physics (Water Level, Batten, Plumb Bob)
- **Constraint amplification** via mechanical advantage (Spanish Windlass)
- **Room templates** as 1:1 molds (Molds & Jigs)

The craftspeople's techniques are not approximations. They are exact solutions computed by materials and geometry. FLUX Certify and PLATO are formalizing what boat builders have known for generations.

**The formality is new. The mathematics is ancient.**

---

## References

- *Constraint Theory Meets Construction* (FLUX-WHITEPUB-2026-05-05-CC)
- FLUX ISA Specification v3.0 (`flux-research/specs/flux-isa-v3.md`)
- Constraint Theory Ecosystem, Chapter 0 (`constraint-theory-ecosystem/chapters/ch00-constraint-mindset.md`)
- FLUX-C Bytecode Reference (`flux-vm` crate documentation)
- PLATO Architecture Specification
- Traditional Boatbuilding Techniques (various source materials on file)

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-05 | Initial whitepaper — 80 techniques formalized |

---

*© 2026 Cocapn Fleet Architecture Team. All rights reserved.*
