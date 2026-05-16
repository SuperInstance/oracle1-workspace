# Phase 3: Physical Spline Prototype Design

**Status:** Design Complete — Ready for Fabrication  
**R&D Stage:** Lofting at 1:1 (digital simulation done, physical prototype next)  
**Target:** JC1 edge deployment validation

---

## Design: 3D-Printable Spline Fixture

### Purpose
Validate that our digital Bézier model matches real physical behavior. 
Print a spline from known material properties, bend it between 3 pins, 
measure the actual curve with a CNC probe, compare to ANALOG_SPLINE output.

### Why This Matters
The digital simulation assumes:
- Linear elasticity (κ = M/EI)
- Small deflections (no geometric nonlinearity)
- No body forces (gravity neglected)
- Material properties are uniform and known

The physical world is messier. If the printed spline deviates from the model, 
we need to understand why (material property variation, print orientation effects, 
layer adhesion anisotropy, etc.). This is the shipwright's "lofting at 1:1" — 
draw it full-scale on the floor and see if it actually fits.

### Material Candidates

| Material | E (GPa) | Printability | Notes |
|----------|---------|--------------|-------|
| PLA | 3.5 | Excellent | Cheap, isotropic, biodegradable |
| PETG | 2.1 | Good | More flexible, better layer adhesion |
| Nylon (PA12) | 1.6 | Moderate | Most flexible, moisture-sensitive |
| TPU (flexible) | 0.01-0.1 | Challenging | Very flexible, not structural |

**Recommended:** PLA for first prototype. E ≈ 3.5 GPa is well-characterized,
print settings are well-understood, and it's stiff enough to maintain shape.

### Design Parameters

```
Cross-section: 3mm × 1mm rectangular strip (thin = more flexible)
Length: 200mm (long enough to show curvature between pins)
Pin spacing: Pin A at 0mm, Pin B at 80mm, Pin C at 200mm (asymmetric)
Pin diameter: 4mm (standard nail-like constraint)
```

**Expected curve shape:** The 200mm PLA strip between pins at 0, 80, 200mm
should form a smooth arch with peak at approximately x=80mm, y≈10-15mm
(depending on exact E and deflection).

### 3D Printing Specifications

```
Layer height: 0.2mm
Infill: 100% (solid — material properties matter, not weight)
Orientation: flat on build plate (maximum stiffness in XY)
Material: PLA (eSUN or Prusament recommended for consistency)
Print settings: 210°C nozzle, 60°C bed, no cooling fan (reduces warping)
```

### Test Protocol

1. **Print** 5 identical spline fixtures from same roll (batch variation check)
2. **Measure** pin positions with calipers (±0.02mm resolution)
3. **Probe** the spline curve at 20 points using CNC probe or dial indicator
4. **Compare** measured points to ANALOG_SPLINE(predicted) output
5. **Calculate** deviation: max(|y_measured - y_predicted|) across all points

**Acceptance criteria:** 
- Max deviation < 1mm: model is accurate, proceed to Phase 4 (JC1 edge)
- Max deviation 1-3mm: model is adequate, document correction factors  
- Max deviation > 3mm: model needs revision, return to Phase 1 (lofting)

### Pin Design (Press-Fit)

```
Pin hole diameter: 3.8mm (0.2mm interference fit for PLA)
Pin insertion depth: 5mm
Pin protrusion: 2mm above surface (nail-like constraint)
Pin material: Steel M4 rod, cut to length, ends deburred
```

Pins should be press-fit — tight enough to stay in place, loose enough to remove.

### Measurement Grid

Points to probe (relative to Pin A at x=0):
- x = 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200 mm
- At each x: measure y at 3 positions across width (left edge, center, right edge)
- Total: 33 measurements per spline fixture

### OpenSCAD Design File

```openscad
// Spline Fixture for Physical Validation
// Parametric: adjust length, pin spacing, cross-section

length = 200;
pin_spacing = [0, 80, 200];  // pin positions in mm
strip_width = 3;
strip_height = 1;
pin_diameter = 4;
pin_hole_diameter = 3.8;
pin_insertion_depth = 5;

module spline_fixture() {
    // Main strip
    translate([-length/2, -strip_width/2, 0])
        cube([length, strip_width, strip_height]);
    
    // Pin holes (3 locations)
    for (x = pin_spacing) {
        translate([x-length/2, 0, -pin_insertion_depth])
            cylinder(d=pin_hole_diameter, h=pin_insertion_depth+2);
    }
    
    // Index marks every 20mm
    for (x = [-180:40:180]) {
        translate([x, -strip_width/2-1, strip_height/2])
            cube([0.5, 1, 0.2]);
    }
}

spline_fixture();
```

### Expected Results (Simulation)

Using PLA properties (E = 3.5 GPa, assuming linear elasticity):

For pin positions at 0, 80, 200mm with 3mm×1mm cross-section:
- Deflection at x=80mm (center): approximately 12-15mm (depends on exact E)
- Curvature is continuous at x=80mm (control point)
- Curvature jump at x=80mm should be 0.0000 (C² continuous Bézier)

### Lessons from Shipwright Practice

Shipwrights didn't trust theoretical models — they lofted at 1:1:
1. Draw the shape full-scale on the lofting floor
2. Build a physical template (mold)
3. Test the template against the actual hull frame
4. Adjust until they matched

We're doing the same:
1. Simulate in Rust (ANALOG_SPLINE digital model)
2. Print the physical spline fixture
3. Probe the actual curve
4. Compare to model, adjust if needed

---

## Next: Phase 4 (JC1 Edge Test)

Once physical prototype validates the model:
1. Deploy `analog_compute` module to JC1 (ARM64, edge encoding)
2. Run PLATO room with spline-boundary mode, 50+ tiles
3. Measure: latency per tile placement, energy consumption, memory usage
4. Compare to cloud VM baseline

**Phase 3 deliverable:** OpenSCAD design file + test protocol + acceptance criteria.

