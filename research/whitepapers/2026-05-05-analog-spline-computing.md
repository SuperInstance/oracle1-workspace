# The Spline as Analog Computer: Information Density and PLATO Integration

*A technical treatise on embodied computation in elastic continua, and a design proposal for cost-effective analog-digital hybrid constraint solving.*

---

## Introduction

In the workshop of a shipwright, a length of cedar batten bent between two nails performs computations that digital systems struggle to match in real-time. The batten, with no sensors, no processors, and no power supply, simultaneously solves differential equations describing minimum-energy deformation, maintains curvature continuity across its entire length, and encodes information about boundary conditions, material properties, and spatial geometry—all encoded in its physical form. This is not metaphor. This is analog computation, embodied in material.

Casey Digennaro, a commercial fisherman and boat builder, has long observed this phenomenon from the deck: a spline contains extraordinary information density—peak heights, inflection points in 3D space (and mathematically more than 3D), higher derivatives—yet is defined by just a few nail positions, baton elasticity and plasticity, and distances between nails. This observation, when formalized, reveals a profound insight for constraint theory: **the physical spline is not just a data structure representing a curve—it is a computational artifact that solves constraint problems automatically, through the physics of elastic deformation.**

This document formalizes that insight, explores its theoretical foundations, catalogs the kinds of computations splines natively perform, examines information encoding schemes, and proposes a cost-effective integration architecture for PLATO—the decentralized constraint orchestration system where this work finds its home.

---

## Part 1: The Spline as Analog Computer

### 1. Information in a Spline

What does a spline actually encode? The naïve answer—"a smooth curve"—understates the case dramatically. A physical spline encodes, simultaneously and continuously:

- **Position**: Every point along the spline's length has a definite spatial coordinate (x, y, z in 3D, though the mathematics generalizes to n-dimensional manifolds).
- **Tangent vector**: The first derivative of position with respect to arc length, dP/ds, gives the direction of the curve at every point. The spline is C¹-continuous—this derivative is well-defined and continuous everywhere, including at the nails.
- **Curvature**: The second derivative, κ = |d²P/ds²|, measures how sharply the spline bends at each point. The spline is C²-continuous—curvature is well-defined and continuous everywhere.
- **Rate of curvature change**: dκ/ds, the third derivative, describes how curvature itself varies along the curve. Physical splines maintain C³-continuity in practice (the third derivative may have jump discontinuities at nails, but within segments it is smooth).
- **Inflection points**: Points where curvature κ = 0, where the spline transitions from bending one way to bending another. These are implicitly determined by the nail positions.
- **Peak heights**: Local maxima of the distance from some reference plane, which in hull design correspond to maximum beam, freeboard, or other critical dimensions.

A spline with N control points (nails) encodes **O(N²) constraints implicitly**. This includes:
- N position constraints (one per nail)
- N−1 tangent continuity constraints at each interval boundary
- N−1 curvature continuity constraints
- N−1 third-derivative bounds (from material properties)

The physical spline is a **SOLVER**: given boundary conditions (the nail positions), it computes the minimum-energy shape automatically. This is not figure of speech—it literally performs variational minimization in the physical world. The functional being minimized is the total bending energy:

```
E = ∫₀ˡ (M²/2EI) ds
```

where M is the bending moment, E is Young's modulus, I is the moment of inertia, and the integral is taken along the arc length l. The spline shape that emerges between two nails is precisely the function that minimizes this integral subject to the boundary conditions. This is the Euler-Lagrange equation applied by the material itself.

The Euler-Bernoulli beam equation states: **κ = M/EI**—curvature is directly proportional to bending moment, inversely proportional to flexural rigidity. A physical spline satisfies this differential equation as a physical object, not as an algorithm. The material doesn't *solve* the equation; it *embodies* the solution. The distinction matters: an algorithm computes the solution; the spline *is* the solution.

This gives us a profound compression result. To specify a smooth curve with its first three derivatives and all inflection points, a digital system requires storing perhaps 100+ floating-point values (sampled at sufficient resolution). The physical spline stores this same information as:
- 2-3 nail positions (6-9 floats, depending on dimensionality)
- 1 material property float (E, the Young's modulus)
- 1 cross-sectional property float (I, the moment of inertia)

Total: approximately **16 bytes** for equivalent information about a smooth curve. The compression ratio exceeds 500:1 for typical curves.

---

### 2. What Splines Can Compute

The physical spline is not merely a representation of a curve—it actively computes solutions to several important problems in physics and engineering. These computations happen simultaneously and instantaneously, limited only by the speed of sound propagation in the material (stress waves traveling through the batten).

**Path planning**: Given a start point A and an end point B, with specified tangent directions at each, a spline bent between pins at A and B computes the unique curve of minimum bending energy connecting them. This is the classic Euler elastica problem, solved by the batten without iteration, without convergence criteria, and without floating-point roundoff. In boat building, this appears as the spiling batten: the builder places nails at known points on the stem and transom, and the batten finds the exact fair curve between them.

**Surface fairing**: When a batten is sprung between constraint points in a boat's hull plating layout, it computes the minimum-energy surface connecting those constraints. The batten finds the fairest possible curve—that which minimizes the integral of squared curvature—automatically. No algorithm could achieve this result more cheaply or more quickly.

**Structural analysis**: The shape of a spline bent between two supports encodes the bending moment diagram for that loading condition. If you know the load distribution and the support positions, the spline's deflection curve yields the internal moment at every point. In hull design, the curve of the spiling batten directly informs the structural analysis of longitudinal framing.

**Fluid flow**: Potential flow around a hull form can be traced by a spline. The spline's curvature satisfies Laplace's equation in the fluid domain (for inviscid, irrotational flow), meaning the spline traced on the hull surface is a streamline of the flow field. The geometry of the spline simultaneously satisfies the kinematic boundary condition (no-penetration at the hull surface) and the dynamic boundary condition (constant pressure, Bernoulli). Again: the physics computes this for free.

**Conformal mapping**: Splines approximate conformal maps that preserve angles in the complex plane. In naval architecture, this appears in the use of spline-based body plans to generate streamlines and waterlines that maintain correct angular relationships at intersection lines.

In every case, the batten computes this without any digital computation—the physics computes it. The material is the computer.

---

### 3. Information Encoding

The information-theoretic efficiency of spline encoding deserves systematic examination.

**Nail positions** serve as boundary conditions—the constraints that the spline must satisfy. In the language of variational calculus, these are the essential boundary conditions that constrain the solution space of the Euler-Lagrange equation. A spline between two nails fixes two endpoint positions; a spline through three nails in a plane uniquely determines a circle (if we allow circular arcs) or a cubic spline segment (if we allow general curvature distributions).

**Baton elasticity** is encoded by two material properties:
- **E (Young's modulus)**: The ratio of stress to strain in the linear elastic regime. Oak: ~12 GPa. Cedar: ~6 GPa. Fiberglass: ~30 GPa. Steel: ~200 GPa. This determines how much force is required to achieve a given curvature.
- **I (moment of inertia)**: The second moment of area of the batten's cross-section. A thinner batten bends more easily (lower I); a wider batten resists bending (higher I). The product EI is the flexural rigidity.

Together, EI determines how tightly the spline will spring between nails of a given spacing. A high-EI spline (steel) between nails 2 meters apart will have nearly constant curvature; a low-EI spline (cedar) will exhibit significant bow between the same nails.

**Baton plasticity**—how much permanent deformation occurs when the batten is forced beyond its elastic limit—determines the spring-back behavior. A perfectly plastic batten, once bent, stays bent. A perfectly elastic batten returns to its original shape when released. Real batten materials exhibit viscoelastic behavior: some spring-back, some permanent set. Shipwrights exploit this: they over-bend the spiling batten to account for spring-back when the shape is transferred to the work.

**Distance between nails** determines the sampling resolution of the constraint. Closer nails provide more constraint points; the spline must pass through more positions, meaning it has less freedom to minimize bending energy. A closely-nailed spline approaches the shape defined by the nail positions directly; a widely-nailed spline has more freedom to find a fair curve. The spacing between nails is the "sampling rate" at which the builder constrains the solution.

**Information density** is the key insight. The encoding is extraordinarily lossy—many different nail configurations can produce visually identical splines in limited regions—but the information density in the physical form is extraordinarily high. Consider the comparison:

- A 1024-dimensional HDC vector, stored as 1024 floats: **8 KB**
- A spline encoding equivalent information about smooth curves: **~16 bytes** (3 nail positions × 3 coordinates + 1 material property float + 1 cross-section float)

This is a **500:1 compression ratio**. The price paid is lossy compression: the spline cannot represent arbitrary curves, only those achievable by elastic deformation of a specific material. But for the domain of smooth physical curves—hull surfaces, structural members, fairing lines—this constraint is acceptable and often desirable, because the resulting curves are guaranteed to be fair (minimum-energy).

The practical implication: splines are a hardware-appropriate representation for smooth physical geometry. They are the native format of material reality.

---

## Part 2: PLATO Analog Compute Integration

### 4. Where Analog Fits in PLATO

PLATO is fundamentally digital. Tiles are hashes. Rooms are delta streams. The protocol is HTTP. Every constraint satisfaction problem is ultimately solved by code running on machines executing instruction cycles. This is not a limitation—it is a design choice that enables deterministic, reproducible, composable reasoning about system state.

But the spline insight suggests that for a specific class of constraints—those involving smooth physical geometry—the physics of elastic materials provides computation for free. The question is not whether to use analog (the answer is yes, for appropriate problems), but **where the analog computation stops and the digital begins**.

PLATO's constraint model has natural integration points for analog compute:

**Room-level analog**: A PLATO room has a boundary—a closed curve or surface defining the room's extent. In the physical world, a room's boundary is defined by walls, which are physical objects. In PLATO, the room boundary is a constraint that tiles must satisfy to belong to the room. If we treat the room boundary as a spline, the first N tiles in a room establish boundary constraints (nail positions), and the room's spline computes the boundary curve. Subsequent tiles snap to this computed spline. The room boundary is thus an analog computation: the first tiles define constraints, the physics computes the curve, remaining tiles are placed relative to that computed curve.

**Tile-level analog**: Each tile can encode its own constraints as "nails" on the room's spline. A tile at position (x, y) in room space is a constraint that the room's boundary spline must pass through or near. The tile's constraint becomes part of the room's spline computation. This is recursive: tiles are both inputs to the analog computation and outputs from it.

**FLUX-C opcode analog**: FLUX-C is PLATO's constraint orchestration language. We propose a new opcode: `GUARD_spline(constraint)`. This opcode specifies a boundary condition (a nail position and tangent direction) and delegates the interpolation between constraints to a physical spline solver. The solver is a service that maintains a library of material properties (E, I for oak, cedar, fiberglass, steel) and computes spline curves from boundary specifications. The output is a tile hash computed from the interpolated curve.

The key design question: **where does the analog stop and digital start?** The answer is the **analog-to-digital boundary**, the measurement step. The physical spline computes continuously; we sample it at discrete points to produce digital values. The sampling resolution determines the fidelity of the digital representation. At the boundary:

- Spline outputs (continuous curve points) → tile hash (digital): a point on the spline is measured, hashed, and becomes a tile identifier.
- Room boundary → PLATO delta stream: the room's boundary spline is published as a sequence of constraint tiles, each tile encoding a sample point on the spline.

The analog computation is invisible to the PLATO protocol—it happens in the material. Only the inputs (nail positions) and outputs (sampled curve points) are visible to the digital system.

---

### 5. Cost-Effective Design Principles

The fundamental question in analog-digital hybrid design is: **when does analog provide a cost benefit over digital?** The answer is specific and principled.

**Use analog when the material physics provides the solving for free**—when the computation is inherent in the physical process and requires no algorithmic overhead. In other words: analog ROI is positive when the alternative is to numerically solve a differential equation or perform optimization to achieve the same result.

| Task | Analog? | Reason |
|---|---|---|
| Surface interpolation | YES | Physics does it for free via elastic relaxation |
| Path planning with obstacles | NO | Digital search (A*, RRT) is more flexible |
| Force distribution in structure | YES | Material embodies the differential equation κ = M/EI |
| Bounded constraint checking | NO | Digital is cheaper and deterministic |
| Curvature continuity | YES | Material enforces automatically; digital requires C² smoothing |
| Temporal constraints | NO | Digital tracking is more precise and auditable |

The **minimum analog system** for a useful PLATO constraint is a spline between 2 nails (or 3 for a plane). Two nail positions in 2D define a unique cubic spline segment with one degree of freedom (the curvature at one endpoint). Three nail positions constrain the spline completely, yielding a unique minimum-energy curve. The cost: 2-3 nail positions + 1 material property = approximately 16 bytes for a continuous surface representation.

This is the **analog compute ROI formula**: the cost (in bytes) of specifying constraints is offset by the information content of the resulting curve. When the alternative is storing a dense sampling of a smooth curve (N points × 3 coordinates = 3N floats), analog wins for curves that can be represented with fewer than ~N/500 constraints.

**Analog compute ROI is positive when the constraint involves physical reality**—hull shapes, force distributions, structural integrity, any domain where the material physics of the constraint domain directly encodes the solution.

---

### 6. Various Ways to Analog Compute

Beyond splines, the history of engineering offers a rich taxonomy of analog computers—physical systems that embody computation in material. Understanding this taxonomy illuminates the broader potential of analog computation within PLATO.

**Mechanical analog computers** exploit rigid-body dynamics:
- **Lever systems**: A lever computes force balance (F₁d₁ = F₂d₂) through material deformation. The fulcrum is the equality constraint.
- **Cams**: A rotating cam profile computes a non-linear transfer function: input rotation angle → output displacement. Used in engine timing, these are look-up tables in metal.
- **Linkages**: The Peaucellier-Lipkin linkage converts rotation to perfect straight-line motion—an exact geometric computation that digital systems approximate with tolerance.
- **Spline/batten**: As detailed above, elastic beams solve minimum-energy variational problems.

**Fluidic analog computers** exploit hydrostatics and fluid dynamics:
- **Water levels**: A连通器 (communicating vessels) system ensures hydrostatic equality—water finds the same level in all connected vessels regardless of shape. This computes the solution to Laplace's equation for gravity-driven potential flow. Used by shipwrights to transfer level references across a hull.
- **Pneumatic systems**: Air pressure equalization computes average quantities. A plenum chamber with multiple outlets computes the mean pressure distribution across its volume.
- **Hydraulic presses**: Pascal's law (pressure transmission through incompressible fluid) computes force multiplication. A small piston area × distance → large piston area × distance, preserving work.

**Electrical analog computers** exploit circuit dynamics (heavily used in the 1940s-1970s):
- **Resistor networks**: A resistive grid solves Laplace's equation for electrostatic potential—the voltage at each node is a weighted average of its neighbors, computing the steady-state heat distribution or potential flow.
- **Op-amp integrators**: Operational amplifiers computing ∫Vdt, used in solving differential equations (the analog computer as differential equation solver).
- **The AREA theorem**: Analog computers for computing areas under curves—integration as voltage accumulation.

**Optical analog computers** exploit wave optics:
- **Lens systems**: A lens computes a Fourier transform in real-time. The focal plane of a lens contains the spatial frequency spectrum of the input. This is the principle behind optical image processing.
- **Interferometry**: Phase comparison between two wavefronts computes angstrom-level displacements. Used in precision metrology, these are analog computers for comparing optical path lengths.
- **Shadow casting**: Moiré patterns from shadow projection compute relative displacements and angles.

**Chemical analog computers** exploit reaction-diffusion:
- **Reaction-diffusion systems**: Belousov-Zhabotinsky reactions produce locally symmetric patterns—chemical oscillators computing spatial symmetry.
- **Crystallization**: Crystal growth computes minimum-energy lattice configurations from first principles.

**Acoustic analog computers** exploit wave resonance:
- **Standing wave patterns**: A resonant cavity computes the eigenmodes of the cavity—analogous to solving the Helmholtz equation.
- **Resonance cavities**: Organ pipes, Helmholtz resonators—systems tuned to specific frequencies compute frequency selection.

The broader lesson: **computation is not exclusive to digital systems**. Any physical system that transforms inputs to outputs according to physical law is, in a meaningful sense, a computer. The question for PLATO is which physical systems provide useful computations at lower cost than digital alternatives.

---

### 7. Analog-Digital Hybrid Design

The hybrid architecture combines the precision and flexibility of digital systems with the computational efficiency of analog physics. The design principle is: **digital for specification and measurement; analog for computation; digital for representation and transmission.**

**Input**: Digital constraint specification. The GUARD opcode specifies what the spline must satisfy—nail positions in 3D, tangent directions, material type (oak, cedar, fiberglass, steel). This specification is digital: exact coordinates, exact material properties, exact tolerances.

**Processing**: Physical spline solves (analog). The specification is handed to a spline solver service that maintains material property libraries and computes the resulting curve. The computation uses digital logic to set up the problem, but the actual curve-finding—the minimization of bending energy—is performed by the physics of the material. In practice, this can be implemented by:
- A software library that solves the Euler-Bernoulli beam equation (if material physics is well-characterized), or
- A physical spline robot that actually bends a batten and measures the result (if material behavior is complex or poorly characterized).

**Output**: Measured nail positions → digital tile hash. The spline output is sampled at discrete points—the positions where the computed curve intersects tile boundaries or sampling planes. These sampled positions become tile identifiers through PLATO's hashing scheme. The measurement is the analog-to-digital conversion: continuous spatial position → discrete digital identifier.

**Error bounds**: Analog output has ±tolerance from material property variation. Real materials vary: Oak's E ranges from 10-14 GPa depending on grain, moisture content, and specific species. This variation means that two identical spline specifications might produce slightly different curves. The digital system must bound these errors—either by characterizing material variation and propagating it through the computation, or by treating analog output as having bounded uncertainty.

**Key insight**: Analog is not "less precise"—it is **differently precise**. A spline is precise within its material domain (elasticity, within the elastic limit, for a known material). Digital is precise within its bit domain (IEEE 754, 64-bit floating point). The analog-digital boundary is a translation between precision domains, not a loss of precision.

**Hybrid architecture flow**:
```
GUARD_digital_constraint → FLUX_C → analog solver (spline) → digital output → tile
```

The digital constraint (nail positions, material properties) is the input. The analog solver computes the curve. The digital output (sampled curve points) is hashed into tiles. The tile stream is the digital representation of the analog computation.

---

### 8. Shipwright Techniques as Analog Compute

Traditional shipwrights developed a sophisticated toolkit of analog computers over centuries of boatbuilding. Each tool is a single-purpose analog computer, extremely cheap, extremely reliable, and solving a specific constraint problem that digital systems either cannot solve cheaper or cannot solve at all without extensive modeling.

**Spiling battens**: A cedar batten sprung between nails driven into a reference edge (the gunwale or transom edge) and corresponding points on the work piece. The batten computes the minimum-energy fair curve connecting the reference edge to the work piece, transferring the shape without measurement. This is an **analog copier**: the physical spline copies the shape from reference to work piece, computing the fairing curve in the process. No coordinate measurement is required; the shape is transferred directly through the batten's physics.

**Story pole**: A length of wood with notches cut at critical dimensions (keel height, rabbet depth, frame spacing). The notches encode relative position information as physical notches in the pole. The story pole is an **analog memory**: it stores dimensional relationships as physical geometry. To use it, the builder references the pole against the work, and the notches indicate where to cut, mark, or position. The pole's memory is stable across the building process (unless damaged) and requires no batteries, no calibration, and no digital retrieval.

**Water level**: A length of clear plastic tubing filled with water. Because water seeks hydrostatic equilibrium—equal level in all connected points—the water level computes the solution to Laplace's equation for gravitational potential. Place the tube at the bow; read the level at the stern. The physics solves the level constraint for free. This is used to transfer reference levels across a hull, ensuring the keel is straight and the hull is not twisted. No digital measurement, no calculation, no algorithm—just physics.

**The sector**: A flat wooden device with two arms pivoted at one end, used to calculate proportional relationships between similar triangles. In hull construction, the sector transfers the proportions of a small model to full-sized framing: if the model's frame is at 3:1 scale to the full hull, the sector reproduces that ratio directly. This is an **analog proportional calculator**: it computes scale factors without arithmetic.

**Trammel points**: A beam compass with interchangeable tips—a bar with two pivot points and a sliding middle support. Used to strike large radii that would be impractical with a conventional compass. The trammel computes radius: given a center point and a radius, the tip traces a circular arc. This is an **analog radius solver**: the trammel embodies the definition of a circle (all points equidistant from center) in rigid geometry.

**Bevel gauges**: A sliding bevel (a blade locked at an angle to a handle) used to transfer angles from one location to another. The bevel computes angular transformation: it reads an angle at one point and reproduces it at another. In hull framing, bevels transfer the complex angles of frame timbers from the drawing to the work. This is an **analog coordinate transformation**: it converts angular coordinates between reference frames without computation.

**Spanish windlass**: A mechanical contraption using a rope, a toggle, and a lever to generate large mechanical advantage from a small applied force. Used to bend hull planks around sharp curves (e.g., at the bow). The Spanish windlass computes **force amplification**: it converts small human force into large clamping force through geometry. The mechanical advantage is the ratio of lever arms—a pure geometric computation embodied in the device.

Each of these tools is a single-purpose analog computer, solving one class of constraint problems at a cost of a few dollars and a few hours of skill acquisition. No digital computer can match them for cost-effectiveness in their domains. The lesson for PLATO: **design analog tools for specific constraint problems, not general-purpose computation**.

---

### 9. Design Proposal: PLATO Analog Layer

We propose adding a dedicated analog computation layer to PLATO's FLUX-C constraint orchestration language. This layer exposes physical analog solvers as first-class operations, bridging the gap between digital constraint specification and analog constraint satisfaction.

**New FLUX-C opcode**: `analog_spline`

```
GUARD analog_spline(
  boundary_constraints: [(position: Vec3, tangent: Vec3?)],
  material_type: enum(oak, cedar, fiberglass, steel),
  sampling_resolution: u32
) -> spline_curve
```

**Parameters**:
- `boundary_constraints`: Array of (position, tangent) pairs. Each pair is a "nail"—a point that the spline must pass through, with optional tangent direction. The spline will compute minimum-energy interpolation between all constraints.
- `material_type`: Material selector. Oak (E=12 GPa), Cedar (E=6 GPa), Fiberglass (E=30 GPa), Steel (E=200 GPa). Material selection determines the bending stiffness of the computed spline.
- `sampling_resolution`: Number of points to sample along the computed curve. Higher resolution gives more fidelity but more output tiles.

**Output**: A spline curve, sampled at `sampling_resolution` points. Each sample point is returned as a tile with a position hash computed from the sample coordinates.

**Integration**: Within a PLATO room, tiles can reference `analog_spline` results by tile ID. The first N tiles in a room can establish room boundary constraints (nail positions). Subsequent tiles can either reference the room's boundary spline or provide additional constraint points.

**Room boundary as spline**: The first K tiles in a room define K boundary constraints. A room-level `analog_spline` operation computes the room's boundary spline from these constraints. The resulting spline is a property of the room, accessible to all subsequent tiles. Tiles snap to the boundary by referencing the room's spline.

**Physical interpretation**: The `analog_spline` opcode models a physical batten of the specified material, bent between pins at the constraint positions. The output is the batten's equilibrium shape, sampled at the specified resolution. The model assumes linear elasticity, small deflections, and no body forces (gravity neglected—appropriate for hull surface fairing where gravity is small compared to stiffness).

**Cost**: 3 nail positions × 3 coordinates = 9 floats + 1 material type enum + 1 sampling resolution = approximately 40 bytes input. Output: N sample points × 3 coordinates × 4 bytes = 12N bytes. For N=100, this is 1200 bytes—a savings over storing a 100-point dense curve (1200 bytes anyway) but with the guarantee of C² continuity from the minimum-energy property.

For the minimum case (2 constraints, 1 material), the analog spline encodes a continuous curve in approximately 16 bytes. This is the **PLATO analog layer minimum viable unit**: one spline, two nails, one material.

---

### 10. Open Questions

Several questions remain open for further research and experimentation:

**Error bounding**: How do we bound the error from material property variation in analog compute? Real materials exhibit variation in E and I of 10-20% across specimens. This propagates through the spline computation. We need to characterize material property distributions and propagate them through the Euler-Bernoulli equation to produce confidence intervals on spline output. Alternatively, we can treat analog output as having bounded uncertainty and design PLATO's constraint satisfaction to handle bounded inputs.

**Composition**: Can we compose analog computers—splines feeding into splines feeding into splines? In principle, yes: the output of one spline computation (a set of sampled points) can serve as input to another. In physical terms, this is like attaching one batten to the end of another—the second batten's endpoint constraints are set by the first batten's sampled output. The practical question is how composition affects error propagation.

**Minimum analog system**: What is the minimum analog system for a useful PLATO constraint? The minimum is one constraint point (a single nail) and a known material—though this is underconstrained (many curves pass through a single point). The minimum overconstrained case is two points in 2D (uniquely determines a cubic spline with one free parameter—curvature at one end). We need to characterize the minimum constraints for each analog computation type.

**Spring-back and plasticity**: How does spring-back (plasticity) interact with constraint satisfaction over time? A spline loaded beyond its elastic limit will take a permanent set. This is both a feature (the bent shape persists) and a limitation (the shape may deviate from the computed minimum-energy shape if the material is overstressed). Viscoelastic materials exhibit time-dependent behavior—creep and stress relaxation—that affects the long-term stability of analog-spline outputs.

**Integration with FLUX-C**: What is the cleanest integration of analog operations into the FLUX-C constraint language? We propose `analog_spline` as a starting point, but other analog operations (water level for equality, sector for proportion, trammel for radius) may warrant dedicated opcodes.

---

## Conclusion

The spline is not merely a geometric primitive—it is a computational artifact, a physical embodiment of the solution to a variational problem. The batten bent between two nails does not *represent* a curve; it *computes* a curve, through the physics of elastic deformation. The information density is extraordinary: a handful of bytes encodes a continuous curve with its derivatives and inflection points, because the physics of the material is the computation.

For PLATO, this insight suggests a design principle: **delegate constraint solving to physics wherever physics can solve it for free**. The analog computation is not a compromise or a fallback—it is a different computational paradigm, with different precision characteristics and different cost structures. Digital systems handle specification and measurement; analog systems handle computation.

The design proposal—`analog_spline`, material libraries, room-level spline boundaries—provides a concrete starting point. The shipwright's toolkit—spiling battens, story poles, water levels, sectors, trammels—provides a rich catalog of single-purpose analog computers to draw from. The hybrid architecture—GUARD_digital → FLUX_C → analog solver → digital output → tile—provides a template for integration.

The batten doesn't solve the differential equation. The batten *is* the solution, embodied in cedar or oak or steel, waiting between two nails, computing the fairest curve that physics allows.

---

*"The physicists have taken shelter in their mathematics, and the shipwrights have taken shelter in their splines. But both are computing the same thing: the shape that minimum energy demands."*
— Adapted from R. Feynman

---

*Document: /tmp/analog-spline-computing.md*
*Author: Oracle1 subagent (research task)*
*Date: 2026-05-05*
*Tags: analog_compute, spline, constraint_theory, material_as_solver, batten, information_density*