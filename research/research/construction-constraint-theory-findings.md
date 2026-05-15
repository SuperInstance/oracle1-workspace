# Construction Constraint Theory: Research Findings
**Generated:** 2026-05-05
**Sources:** FLUX-C whitepaper, constraint-theory-ecosystem ch00/ch06, web research on origami geometry, shipbuilding techniques, computational geometry

---

## 1. Origami Fold Geometry and Constraint Solving

**Key Concept:** Paper folding can solve arbitrary cubic equations exactly—not approximately—through geometric construction. Margherita P. Beloch demonstrated in 1936 that the Huzita-Hatori Axiom 6 (folding two points onto two lines simultaneously) is equivalent to solving a cubic equation. The 7 axioms define the complete set of single-fold operations in origami geometry.

**Mathematical Formalization:** The 7 Huzita-Hatori axioms generate geometric constraints from fold operations. Axiom 2 (fold point p1 onto p2) creates a perpendicular bisector: F(s) = {x | dist(x,p1) = dist(x,p2)}. Axiom 6 (simultaneously placing p1→l1 and p2→l2) is equivalent to finding a line tangent to two parabolas—solving a 3rd-degree equation. Margishvili's theorem states any cubic can be solved by a finite sequence of folds.

**Connection to FLUX-C/PLATO:** FLUX-C FOLD instructions can implement origami geometric constructions as constraint operations:
```
FOLD FOLDMAP axis=vertical reflect=[tile_a, tile_b]
FOLD CREASE line=fold_line_1
```
Each fold generates equality constraints between reflected points. A tri-fold creates a 3-way simultaneous constraint: `constrain(flat(section_1, section_2, section_3))` where all sections must fold flat without overlap.

**Concrete Example:** To trisect an angle (impossible with straightedge/compass), use Axiom 6: fold a point P onto one ray while passing through another point on the other ray. The fold line produced is the trisector. The construction solves x³ = a rather than just x².

---

## 2. Batten Splines and C² Continuity

**Key Concept:** Traditional boat builders fair curves using a batten—a thin flexible strip forced through marked control points. The batten always produces a fair (smooth, aesthetically pleasing) curve through those points without any equation or algorithm. The smoothness emerges from the material's physical properties, not mathematical computation.

**Mathematical Formalization:** C² continuity means position (C⁰), tangent (C¹), and curvature (C²) are all continuous at join points. A batten minimizes bending energy: E = ∫κ² ds where κ is curvature. The Euler-Bernoulli beam equation describes the shape: d²/dx²(EI d²y/dx²) = q(x). For a free batten between pins, the solution is the curve of minimum energy—which is inherently C² continuous.

**Connection to FLUX-C/PLATO:** FLUX-C could support material property constraints:
```
GUARD C2_continuous([p1, p2, p3, p4])
GUARD material_property(type=elastic, continuity_order=2)
```
The constraint IS the curvature—enforced by the material solver (physics), not a numerical solver. PLATO tiles as batten segments: each tile is a control point, the room boundary is the batten that enforces C² continuity between tiles.

**Concrete Example:** In hull lofting, the boat builder marks frame stations (control points) on a strongback. The batten is bent through all marks simultaneously. Where the batten contacts a mark, the builder scribes a line. The batten produces a fair curve regardless of mark spacing—C² continuity emerges from physics, not math.

---

## 3. Pythagorean Snapping in Computational Geometry

**Key Concept:** The 3-4-5 triangle is a self-squaring snap grid for angles—any triangle with sides 3, 4, 5 is guaranteed right-angled. Craftsmen use this as a constraint proxy: pegs at 3 and 4 units, string sums to 5 where angle = 90°. The triangle snaps the solution into existence.

**Mathematical Formalization:** Lattice-based constraint satisfaction projects high-dimensional points onto a simplex basis, solves in the reduced space, then projects back. For triangle snapping: project point p ∈ ℝⁿ to 3-simplex Δ₃, verify triangle validity (triangle inequality), lift back to ℝⁿ. Complexity: O(N) instead of O(N²). Exact recovery condition: projection must commute with constraint operator P: P(p) = p if p ∈ constraint_set.

**Connection to FLUX-C/PLATO:** PLATO queries on high-dimensional knowledge spaces could use triangle-basis projection:
```
GUARD project_simplex(point, dims=3)
GUARD snap_to_triangle(point)
GUARD lift_to_original(point)
```
The triangle basis acts as a constraint proxy—preserves essential geometry while reducing computation from O(N²) to O(N).

**Concrete Example:** In hardware verification, checking whether a 100-dimensional state satisfies all constraints can use projection: project to 3D, verify the 3-4-5 triangle constraint (guaranteed right angle), project back. If the projection is valid and commutes with the constraint operator, the original point is valid without checking all 100 dimensions.

---

## 4. String Measurement in Naval Architecture

**Key Concept:** Boat builders run a string along a curved hull to mark frame stations. The string is an analog computer—it conforms to the hull's shape without equations, outputting frame geometry directly. Combined with a 3-4-5 triangle jig for squaring, the string + jig produces frames that satisfy both hull curve and right-angle constraints simultaneously.

**Mathematical Formalization:** String measurement = constraint propagation via physical simulation. The string is a continuous flexible medium, the hull is a constraint surface (boundary conditions), the triangle jig is a reference constraint. The output is the solved state: frame shape satisfying all constraints simultaneously. This is equivalent to finite element analysis where the mesh IS the material and the solver IS physics.

**Connection to FLUX-C/PLATO:** PLATO delta streams are string measurements. A tile placed in a room measures the local shape of the knowledge hull—it doesn't know global structure, only constrains immediate neighbors. Constraints propagate outward from each tile, exactly as string shape propagates from hull contact points. The room boundary is the hull; each tile is a contact point.

**Concrete Example:** Frame #7 of a hull: run string from bow to frame #7 position, wrap around hull at frame station, run to stern. The string takes the exact curve of the hull. Mark the string's path at the frame station—that's the frame shape. No equations, no coordinate measurement. The string IS the constraint solver.

---

## 5. Force-Fit and Spring-Back in Furniture Making

**Key Concept:** Woodworkers cut pieces slightly oversize to account for spring-back—the material's elastic return after being forced into a mortise. The piece satisfies the constraint NOW (fits immediately) but the constraint is not fully satisfied until spring-back releases LATER. This is temporal constraint propagation: satisfy now, verify later.

**Mathematical Formalization:** Force-fit constraint with tolerance:
```
GUARD force_fit(width <= opening_width + 0.05, immediate=true)
GUARD post_force(width <= opening_width + 0.02, deferred=true)
```
`immediate=true` permits satisfaction within tolerance band. `deferred=true` triggers follow-on verification after assembly stress releases. The spring-back is a delayed constraint: initial satisfaction ≠ final satisfaction.

**Connection to FLUX-C/PLATO:** This maps to lazy evaluation in CS (evaluate on read, not on write) and optimistic locking in databases (write now, validate later). The GUARD `force_fit(constraint, tolerance)` semantics defer verification:
```
GUARD force_fit(piece_width, [opening_width], tolerance=0.05)
# assembly occurs here
GUARD post_assembly_verify(constraint, tolerance=0.02)
```

**Concrete Example:** A furniture maker cuts a tenon 0.5mm oversize. During assembly, the piece is forced in—the mortise compresses, the tenon bends slightly. Immediately after assembly: constraint satisfied (piece fits). Three days later after wood acclimates: spring-back releases, tenon compresses back, joint loosens. The deferred check catches the failure that immediate satisfaction missed.

---

## 6. Bi-Fold and Tri-Fold as Multi-Way Constraints

**Key Concept:** Origami tri-fold creates a 3-way constraint: three sections must all fold flat simultaneously without overlap. This differs fundamentally from pairwise constraints (A with B, B with C) because all three must satisfy the flatness constraint together—a simultaneous satisfaction problem, not sequential.

**Mathematical Formalization:** A tri-fold constraint is: ∀ sections {s₁,s₂,s₃}: flat(s₁) ∧ flat(s₂) ∧ flat(s₃) ∧ no_overlap(s₁,s₂) ∧ no_overlap(s₂,s₃) ∧ no_overlap(s₁,s₃). This is a hypergraph constraint (3-uniform hyperedge) rather than a graph constraint (pairwise edges). Solving requires all constraints satisfied simultaneously—not composable from pairwise solutions.

**Connection to FLUX-C/PLATO:** Hypergraph constraint solving in FLUX-C:
```
FOLD TRIFOLD sections=3 axis=vertical
GUARD hyperconstraint([tile_a, tile_b, tile_c], flatness)
```
Connection to n-wise testing in verification: exhaustively test all n-way combinations rather than all pairs. N-wise catches interaction bugs that pairwise misses.

**Concrete Example:** A business letter folded into thirds (tri-fold): the top third must fold down, the bottom third must fold up, and the middle section must accommodate both. All three sections must be flat simultaneously—the crease positions are constrained by all three sections, not just adjacent pairs. Adjusting one fold changes the required positions of the others.

---

## 7. PLATO Rooms as Construction Frames

**Key Concept:** In CAD systems, snapping constrains elements locally: a frame constrains the panel inside it, the panel constrains the bezel around it, the bezel constrains the mounting screws. Each element constrains only its immediate neighbors; global coherence emerges from local constraint propagation. The room boundary IS the constraint—pieces don't need to know room size in advance.

**Mathematical Formalization:** CAD snapping = local constraint propagation with frame hierarchy:
```
frame → constrains → panel → constrains → bezel → constrains → screws
```
The room boundary B defines the constraint surface. Tile placement: tile t satisfies C(t, B) where C is the local constraint (t fits within B). Global coherence: ∀ tiles tᵢ, tⱼ: if tᵢ adjacent tⱼ then C(tᵢ, tⱼ) satisfied. No global constraint solving—only neighbor-to-neighbor.

**Connection to FLUX-C/PLATO:** PLATO rooms function as construction frames. Tiles are measured-and-cut pieces (satisfy local constraint). Room boundary is the frame (constrains tile placement). String measurement analogy: PLATO tiles are strings run along hull—measure local shape, propagate constraints. Batten analogy: room boundary enforces C² continuity between tiles without tile-to-tile derivative computation.

**Concrete Example:** Installing a door in a rough opening: the door (piece) doesn't know the opening dimensions in advance. It only needs to satisfy the constraint when placed—fit within the frame, swing clear, lock engage. The frame constrains the door, not the other way around. Global coherence (house structure) emerges from local door-frame satisfaction, not from door knowing house dimensions.

---

## 8. Measure at Assembly vs Measure at Design

**Key Concept:** Craftsmen follow "measure the opening, cut the piece"—the opening constrains the piece, not the piece defining the opening. This is lazy constraint evaluation: the constraint is measured at assembly time (when information is available), not specified at design time. Software constraints are predominantly eager (immediate), construction constraints are predominantly lazy or deferred.

**Mathematical Formalization:** Eager constraint: GUARD width <= opening_width (evaluated when written, both values must exist NOW). Lazy constraint: GUARD measured_at_assembly(piece_width, [opening_width]) (stores constraint graph edge, not value; resolved at assembly). The lazy form defers comparison until assembly context provides the opening width value.

**Connection to FLUX-C/PLATO:** GUARD `measured_at_assembly()` as new constraint type:
```
GUARD measured_at_assembly(tile_width, [room_boundary_width])
```
This enables computation deferral: tile doesn't need room dimensions at creation, only at placement. Connection to lazy evaluation in CS (thunks, promises), late binding (dynamic scoping), optimistic locking (write now, validate later).

**Concrete Example:** A cabinet maker building fitted furniture: the carcase (opening) is built first, then the door (piece) is measured to fit the actual opening—not a nominal dimension. If the carcase is 602mm due to wall variation, the door is cut to 602mm. The constraint is measured at assembly, not designed upfront. Result: perfect fit regardless of wall variation.

---

## Summary: Construction Formalized

The 8 patterns form a unified constraint theory:

| Construction Technique | Formal Constraint Type |
|------------------------|------------------------|
| Origami fold geometry | Hypergraph constraints (multi-way) |
| Batten splines | Material-enforced C² continuity |
| Pythagorean snapping | Simplex projection with exact recovery |
| String measurement | Physical constraint propagation |
| Force-fit / spring-back | Temporal deferred constraints |
| Bi-fold / tri-fold | 3-way simultaneous constraints |
| PLATO rooms as frames | Local constraint propagation via frames |
| Measure at assembly | Lazy constraint evaluation |

**Central insight:** Craftspeople invented constraint propagation without the formalism. The math was always there—they just embodied it in wood, string, and paper folds. FLUX-C and PLATO formalize these patterns computationally, enabling agent fleets to benefit from computation patterns refined over centuries.

---

*Research completed 2026-05-05. Sources: FLUX-C whitepaper (2026-05-05), constraint-theory-ecosystem ch00/ch06, Wikipedia (Huzita-Hatori axioms, Peaucellier-Lipkin linkage), shipbuilding literature on batten splines and lofting techniques.*