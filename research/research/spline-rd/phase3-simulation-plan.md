# Spline Physics Simulation Environment — Implementation Plan

**Project:** Phase 3 — Digital Lofting Before Physical Prototype  
**Purpose:** Build a high-fidelity elastic beam simulator to validate ANALOG_SPLINE quadratic Bézier model  
**Status:** Planning complete, implementation pending  

---

## Executive Summary

We have a digital model (ANALOG_SPLINE in constraint-theory-llvm) that uses quadratic Bézier interpolation to compute spline curves. This model assumes linear elasticity and small deflections. Before printing physical spline fixtures (Phase 3 physical), we need to build a high-fidelity physics simulation to validate the digital model in silico.

This is the shipwright's "lofting at 1:1" — drawing the full-scale shape on the floor digitally before committing to wood and nails.

The simulation environment will:
1. Model elastic beam physics with high accuracy
2. Support multiple numerical methods for cross-validation
3. Compare output against our ANALOG_SPLINE implementation
4. Generate test cases for regression testing
5. Produce visualizations for manual inspection

---

## 1. Physics Model

### 1.1 Governing Equations

**Euler-Bernoulli Beam Theory** (primary model):
```
M(x) = EI * d²w/dx²     (bending moment = flexural rigidity × curvature)
V(x) = dM/dx            (shear force = derivative of bending moment)
q(x) = -dV/dx           (distributed load = negative derivative of shear)

d⁴w/dx⁴ = q(x) / EI     (fourth-order ODE for beam deflection)
```

For a beam with no distributed load (q=0) between pins:
```
d⁴w/dx⁴ = 0  →  w(x) is a cubic polynomial in each segment
```

This matches our ANALOG_SPLINE assumption: the equilibrium shape between two pins is a cubic (quadratic in the planar case, since we constrain the curve to pass through both pins).

### 1.2 Physics to Include

**Must Include (baseline):**
- Linear elasticity (Hookean material response)
- Small-deflection theory (w << beam length)
- Pin constraints (position enforced, moment free)
- Uniform cross-section (constant EI along beam)
- Self-weight (optional, gravity load)

**Include for higher fidelity:**
- Geometric nonlinearity (large deflections, w ~ L/10 or larger)
- Distributed load (self-weight, point loads at intermediate positions)
- Initial stress/strain state
- Support settlement (pins that move under load)

**Include for production accuracy:**
- Viscoelasticity (time-dependent material response, creep)
- Plasticity (permanent deformation beyond yield)
- Layer adhesion anisotropy (for 3D-printed materials, properties vary by layer orientation)
- Thermal effects (coefficient of thermal expansion)

### 1.3 What We're Validating

The key question: **Does our quadratic Bézier model match the true equilibrium shape of a physical spline?**

The Bézier model assumes:
- The beam is massless and infinitely stiff in extension/compression
- Only bending deformation matters (no shear, no torsion)
- The equilibrium shape is the minimum-bending-energy curve
- Pin constraints fix position but not slope (simply supported beam)

The true physical spline has:
- Mass (distributed along its length)
- Shear deformation (Timoshenko beam theory gives slightly different shapes)
- Clamping at pins (wood grain compresses under nail)
- Plastic deformation if overbent

We need to quantify the error between our Bézier model and the true physics across relevant parameter ranges.

---

## 2. Numerical Methods

### 2.1 Method Comparison

| Method | Accuracy | Speed | Complexity | Notes |
|--------|----------|-------|------------|-------|
| **Shooting Method (Euler Elastica)** | High | Medium | Medium | Best for large deflections, finds equilibrium directly |
| **Finite Difference (FD)** | High | Medium | Low | Simple, well-understood, good for uniform grids |
| **Finite Element (FEM)** | Very High | Slow | High | Handles complex geometries, used in commercial tools |
| **Galerkin/Weighted Residual** | High | Medium | Medium | Good balance of accuracy and simplicity |
| **Relaxation/Energy Minimization** | High | Slow | Low | Iteratively minimizes bending energy directly |

### 2.2 Recommended Approach: Shooting Method + Energy Minimization

**For validation:** Use both Shooting Method and Energy Minimization as independent cross-checks. If both agree on the same shape, we have high confidence. If they disagree, we find the bug.

**Shooting Method (Euler Elastica):**
```
Given: pin positions (x0,y0) and (x1,y1), tangent directions at pins (θ0, θ1)
Goal: find the curve w(x) that satisfies equilibrium

Approach:
1. Guess initial slope θ0 at left pin
2. Integrate the beam ODE forward using RK4
3. At right pin, check if y matches target
4. Newton iteration to find correct θ0 that satisfies both endpoint conditions

The Euler elastica equation in parametric form:
d²θ/ds = -M(s) / EI(s)
where θ is the tangent angle, s is arc length, M(s) is the bending moment at s
```

**Energy Minimization (Direct Method):**
```
Functional: J[w] = ∫₀ˡ EI/2 * (w'')² dx  (bending energy)
Constraint: w(0) = y0, w(l) = y1 (pin positions enforced)

For simply supported beam with pin at each end:
- Solve the system of equations from stationarity: δJ/δw = 0
- This gives the cubic spline coefficients directly

The analytical solution for a simply supported beam with end moments M0, Mn:
w(x) = (M0(l-x) + Mn*x) * x(l-x) / (6EI*l)
```

### 2.3 Discretization Strategy

For the simulation environment, use a uniform arc-length discretization:

```
N = number of segments (recommended: N = 100 for validation, N = 500 for publication-quality)
Arc length s from 0 to L_total
Beam state at each node i: (x_i, y_i, θ_i, κ_i)
where θ_i = dθ/ds (tangent angle), κ_i = d²y/dx² (curvature)
```

Arc-length parameterization is important because:
- Natural boundary conditions are expressed in terms of arc length
- Energy functional is expressed in terms of arc length
- It handles sharp curves without step-size problems

### 2.4 Convergence Criteria

For validation purposes, we need tight convergence:

```
Position tolerance: |y_sim - y_analytical| < 1e-6 (normalized to beam length)
Curvature tolerance: |κ_sim - κ_analytical| < 1e-4
Energy tolerance: |E_sim - E_exact| < 1e-8
```

Use Richardson extrapolation to estimate true error:
```
E(h/2) = (4*E(h/2) - E(h)) / 3  (if solution is O(h²) convergent)
```

---

## 3. Rust Crate Architecture

### 3.1 Crate Name

`spline-physics` (or `beam-sim`)

### 3.2 Module Structure

```
spline-physics/
├── Cargo.toml
├── src/
│   ├── lib.rs              (public API, re-exports)
│   ├── beam/
│   │   ├── mod.rs          (Beam struct, material properties)
│   │   ├── cross_section.rs (I, A, section modulus for rectangular/circular)
│   │   └── material.rs     (E, nu, density, yield stress)
│   ├── solvers/
│   │   ├── mod.rs          (Solver trait + implementations)
│   │   ├── shooting.rs    (Euler elastica shooting method)
│   │   ├── energy_min.rs   (Energy minimization via Newton-Raphson)
│   │   ├── fd.rs           (Finite difference scheme)
│   │   └── comparison.rs   (Compare two solver outputs)
│   ├── models/
│   │   ├── mod.rs
│   │   ├── euler_bernoulli.rs  (Linear elasticity, small deflections)
│   │   ├── timoshenko.rs      (Shear deformation included)
│   │   └── large_deflection.rs (Geometrically nonlinear)
│   ├── validation/
│   │   ├── mod.rs
│   │   ├── analytical.rs   (Known analytical solutions for testing)
│   │   ├── bezier_compare.rs (Compare to ANALOG_SPLINE output)
│   │   └── test_suite.rs   (Standard test configurations)
│   └── utils/
│       ├── mod.rs
│       ├── quadrature.rs   (Gaussian quadrature for integrals)
│       ├── interpolation.rs (Spline interpolation utilities)
│       └── visualization.rs (Export to CSV for plotting)
└── tests/
    ├── validation_tests.rs
    ├── convergence_tests.rs
    └── integration_tests.rs
```

### 3.3 Core Traits

```rust
/// Material property provider
pub trait Material {
    fn youngs_modulus(&self) -> f64;
    fn shear_modulus(&self) -> f64;
    fn density(&self) -> f64;
    fn yield_strength(&self) -> f64;
}

/// Cross-sectional geometry provider  
pub trait CrossSection {
    fn moment_of_inertia(&self) -> f64;
    fn area(&self) -> f64;
    fn section_modulus(&self) -> f64;
}

/// Solver for beam equilibrium
pub trait BeamSolver {
    fn solve(&self, config: &BeamConfig) -> Result<BeamSolution, SolverError>;
    
    fn name(&self) -> &str;
    fn expected_accuracy(&self) -> f64;
}

/// Solution output from a beam solver
#[derive(Clone)]
pub struct BeamSolution {
    pub positions: Vec<(f64, f64)>,       // (x, y) at each node
    pub tangents: Vec<f64>,              // tangent angle θ at each node
    pub curvatures: Vec<f64>,            // curvature κ at each node
    pub bending_moment: Vec<f64>,         // M(x) at each node
    pub shear_force: Vec<f64>,            // V(x) at each node
    pub bending_energy: f64,              // total energy ∫EI/2 * κ² ds
    pub arc_lengths: Vec<f64>,            // arc length s at each node
}
```

### 3.4 BeamConfig Structure

```rust
pub struct BeamConfig {
    // Geometry
    pub length: f64,
    pub pin_positions: Vec<(f64, f64)>,  // [(x0,y0), (x1,y1), ...]
    
    // Material
    pub material: Box<dyn Material>,
    pub cross_section: Box<dyn CrossSection>,
    
    // Boundary conditions
    pub boundary_conditions: BoundaryConditions,
    
    // Loads (optional)
    pub distributed_load: Option<f64>,  // q(x) in N/m
    pub point_loads: Vec<(f64, f64)>,   // (position, magnitude)
    
    // Simulation parameters
    pub num_nodes: usize,
    pub convergence_tolerance: f64,
    pub max_iterations: usize,
}

pub enum BoundaryConditions {
    SimplySupported,  // Pins: position fixed, moment = 0
    Clamped,          // Fixed: position AND slope fixed
    Free,             // No constraints at this end
}
```

---

## 4. Material Parameterization

### 4.1 Materials to Model

| Material | E (GPa) | ρ (g/cm³) | Notes |
|----------|---------|-----------|-------|
| PLA (print) | 3.5 | 1.24 | Isotropic assumption, 100% infill |
| Cedar | 6.0 | 0.4 | Shipwright batten material |
| Oak | 12.0 | 0.7 | Shipwright batten material |
| Steel (M4 rod) | 200.0 | 7.8 | Pin material |
| Fiberglass | 30.0 | 2.0 | Structural composite |

### 4.2 Cross-Section for Simulation

For the PLA spline fixture (Phase 3 physical):
- Rectangular cross-section: 3mm × 1mm = 3mm wide, 1mm thick
- I = bd³/12 = 3×1³/12 = 0.25 mm⁴ = 2.5×10⁻¹³ m⁴
- For steel pins: solid cylindrical M4 rod, diameter = 4mm

For the shipwright battens:
- Circular cross-section (typical cedar/oak batten): diameter d
- I = πd⁴/64
- E.g., d=6mm: I = π*6⁴/64 = 127 mm⁴

### 4.3 Material Variation

For validation, we need to characterize material property uncertainty:

```
PLA: E = 3.5 ± 0.5 GPa (typically ±15% batch variation)
Cedar: E = 6.0 ± 1.0 GPa (grain direction matters)
Oak: E = 12.0 ± 2.0 GPa
```

The simulation should accept E as a range, not a point estimate, so we can compute the sensitivity of our Bézier model to material variation.

---

## 5. Test Configurations

### 5.1 Standard Test Suite

**Test 1: Single Segment (2 Pins)**
- Pin A at (0, 0)
- Pin B at (L, 0) — flat baseline
- Expected: zero curvature (straight line)
- Purpose: validate zero-case behavior

**Test 2: Symmetric Arch (3 Pins, Symmetric)**
- Pin A at (0, 0)
- Pin B at (L/2, h) — peak at midpoint
- Pin C at (L, 0)
- Expected: circular arc for small h/L, sinusoidal for moderate h/L
- Purpose: validate against known analytical solution

**Test 3: Asymmetric Arch (3 Pins, Asymmetric)**
- Pin A at (0, 0)
- Pin B at (0.4L, h) — peak off-center
- Pin C at (L, 0)
- Purpose: this is our main validation case — compare to ANALOG_SPLINE

**Test 4: Multi-Segment (4+ Pins)**
- Pin A at (0, 0)
- Pin B at (0.3L, h1)
- Pin C at (0.7L, h2)
- Pin D at (L, 0)
- Purpose: test continuous curvature at intermediate pins

**Test 5: Large Deflection**
- L = 200mm, h = 30mm (h/L = 0.15 — large deflection regime)
- Purpose: test geometric nonlinearity, compare to linear model

**Test 6: Distributed Load (Self-Weight)**
- Beam under its own weight
- Simply supported at ends
- Expected: parabolic deflection under uniform load
- Purpose: validate load handling

### 5.2 Test Matrix

| Test | Description | h/L Ratio | Material | Pins | Expected Error Source |
|------|-------------|-----------|----------|------|-----------------------|
| T1 | Flat baseline | 0.0 | Any | 2 | Numerical precision |
| T2a | Low arch | 0.05 | PLA | 3 | Bending only |
| T2b | Moderate arch | 0.10 | PLA | 3 | Geometric nonlinearity |
| T2c | High arch | 0.15 | PLA | 3 | Large deflection |
| T3 | Off-center peak | 0.10 | PLA | 3 | Bézier vs. true elastica |
| T4 | Multi-segment | 0.10 | PLA | 4 | Continuity at intermediate |
| T5 | Steel pins | — | PLA | 3 | Clamping stiffness |
| T6 | Self-weight | — | PLA | 2 | Distributed load |

### 5.3 Acceptance Criteria

For each test configuration, we compute:

```
position_error = max_i |y_sim[i] - y_bezier[i]|
curvature_error = max_i |κ_sim[i] - κ_bezier[i]|
peak_height_error = |y_sim_peak - y_bezier_peak|
energy_ratio = E_sim / E_bezier
```

**Pass criteria:**
- position_error < 0.5mm (for 200mm beam)
- curvature_error < 0.01 mm⁻¹
- peak_height_error < 0.3mm
- energy_ratio within [0.98, 1.02] (within 2%)

**Warning criteria:**
- position_error 0.5mm - 2mm: model is adequate, document correction
- position_error > 2mm: model needs revision

---

## 6. Validation Strategy

### 6.1 Validate Simulation Against Analytical Solutions

**Test 1:** Cantilever beam with end load
- Exact solution: w(x) = PL³/(3EI) at tip
- Compare simulation output against this

**Test 2:** Simply supported beam with uniform load
- Exact solution: w(x) = qx(l-x)(l² - x²)/(24EI)
- Maximum deflection at x = l/2: w_max = 5ql⁴/(384EI)

**Test 3:** Pure bending moment at ends
- Exact solution: circular arc, constant curvature κ = M/EI

### 6.2 Cross-Validate Numerical Methods

For each test configuration:
1. Run Shooting Method → solution A
2. Run Energy Minimization → solution B
3. Run Finite Difference → solution C
4. Compare A vs B vs C

Acceptable: |A - B| < 1e-6, |B - C| < 1e-6  
If they disagree by more, find the bug.

### 6.3 Validate Against Published Results

Search for published experimental data on:
- PLA beam deflection measurements
- Cedar/oak batten curvature measurements
- Published elastica solutions for specific boundary conditions

Key sources to reference:
- "The elastic curve of a beam under terminal couple" (classic problem)
- "Large deflections of a cantilever beam" (Koiter's papers)
- "The elastica: a historical review" (recent review article)

### 6.4 Sensitivity Analysis

Once baseline is validated, run parameter sweeps:

```
For each material (PLA, cedar, oak):
  For each h/L in [0.05, 0.10, 0.15, 0.20]:
    For each L in [100mm, 200mm, 300mm]:
      Compute position_error(y_sim vs y_bezier)
      Compute curvature_error(κ_sim vs κ_bezier)
      Plot error vs h/L curves
```

This tells us where the Bézier model is accurate and where it breaks down.

---

## 7. Benchmark Comparison

### 7.1 How to Compare

For each test configuration:
1. Run ANALOG_SPLINE from constraint-theory-llvm → get Bézier curve
2. Run spline-physics simulation → get simulated curve
3. Resample both curves to common arc-length grid (N=60, matching ANALOG_SPLINE)
4. Compute comparison metrics

```rust
pub fn compare_bezier_to_simulation(
    bezier_points: &[(f64, f64)],  // from ANALOG_SPLINE
    sim_points: &[(f64, f64)],    // from spline-physics
) -> ComparisonMetrics {
    // Resample to common grid
    // Compute position_error
    // Compute curvature_error  
    // Compute energy ratio
    // Return metrics
}
```

### 7.2 Metrics to Report

| Metric | Formula | Units | Acceptable |
|--------|---------|-------|------------|
| Max position error | max|y_sim - y_bezier| | mm | < 0.5 |
| RMS position error | sqrt(mean((y_sim - y_bezier)²)) | mm | < 0.2 |
| Max curvature error | max|κ_sim - κ_bezier| | mm⁻¹ | < 0.01 |
| Peak height error | |y_sim_peak - y_bezier_peak| | mm | < 0.3 |
| Energy ratio | E_sim / E_bezier | — | [0.98, 1.02] |
| Curvature jump (at pins) | |κ_left - κ_right| | mm⁻¹ | < 0.001 |

### 7.3 Benchmark Results Table (Target)

| Test Config | pos_err_max | pos_err_rms | curv_err_max | peak_err | energy_ratio |
|-------------|-------------|-------------|--------------|----------|--------------|
| T2a (h/L=0.05) | < 0.1mm | < 0.05mm | < 0.001 | < 0.1mm | 1.000 |
| T2b (h/L=0.10) | < 0.3mm | < 0.15mm | < 0.005 | < 0.2mm | 1.005 |
| T2c (h/L=0.15) | < 0.8mm | < 0.4mm | < 0.01 | < 0.4mm | 1.015 |
| T3 (asymmetric) | < 0.5mm | < 0.25mm | < 0.008 | < 0.3mm | 1.008 |

If T2c (high arch, h/L=0.15) shows large errors, the linear Bézier model is insufficient for large deflections — and we need to switch to the large-deflection solver or use a cubic Bézier instead.

---

## 8. Implementation Order

### Phase A: Core Infrastructure (2-3 days)

1. **spline-physics crate setup** — Cargo.toml, lib.rs, module structure
2. **Material and CrossSection traits** — with concrete implementations for PLA, cedar, oak
3. **BeamConfig and BeamSolution structs** — complete with documentation
4. **Test 1 (flat baseline)** — validate that solver returns straight line with no error
5. **Analytical solutions module** — implement known solutions for T1-T3

### Phase B: First Solver — Energy Minimization (2-3 days)

1. **Energy minimization solver** — minimize ∫EI/2(w'')²dx subject to pin constraints
2. **Test 2a (symmetric arch, low)** — validate against circular arc approximation
3. **Test 2b (symmetric arch, moderate)** — see if low-order approximation holds
4. **Cross-check with analytical solution** for simply supported beam with end moments

### Phase C: Second Solver — Shooting Method (2-3 days)

1. **Shooting method for Euler elastica** — Newton iteration on initial slope
2. **Test against Energy Minimization** — must agree within tolerance
3. **Test 3 (asymmetric arch)** — this is the key validation case
4. **Large deflection test (T2c)** — if h/L > 0.1, geometric nonlinearity matters

### Phase D: Benchmark Comparison (1-2 days)

1. **bezier_compare module** — integrate with constraint-theory-llvm ANALOG_SPLINE
2. **Run full test suite** — generate metrics table
3. **Document results** — error vs h/L curves, pass/fail per test
4. **Write regression tests** — ensure future changes don't regress

### Phase E: Visualization and Documentation (1 day)

1. **CSV export for gnuplot/matplotlib** — visualize curves, errors
2. **Convergence plots** — error vs N (discretization nodes)
3. **Material sensitivity plots** — error vs E variation
4. **README and examples** — show how to use the crate

**Total estimated time: 8-12 days** (assuming focused work)

---

## 9. File Layout

```
spline-physics/
├── Cargo.toml
├── README.md
├── LICENSE
├── src/
│   ├── lib.rs
│   ├── beam.rs           # Beam struct + BeamConfig
│   ├── material.rs       # Material trait + PLA/Cedar/Oak/Steel
│   ├── cross_section.rs  # CrossSection trait + Rectangular/Circular
│   ├── boundary.rs       # BoundaryConditions enum
│   ├── solution.rs       # BeamSolution struct
│   ├── solvers/
│   │   ├── mod.rs        # Solver trait
│   │   ├── energy.rs     # Energy minimization
│   │   ├── shooting.rs   # Euler elastica shooting
│   │   └── fd.rs         # Finite difference
│   ├── comparison/
│   │   ├── mod.rs
│   │   ├── metrics.rs    # ComparisonMetrics
│   │   ├── bezier.rs     # Compare to ANALOG_SPLINE
│   │   └── analytical.rs  # Compare to exact solutions
│   ├── analytical/
│   │   ├── mod.rs
│   │   ├── cantilever.rs
│   │   ├── simply_supported.rs
│   │   └── pure_bending.rs
│   ├── tests/
│   │   ├── test_suite.rs
│   │   ├── convergence.rs
│   │   └── validation.rs
│   └── utils/
│       ├── quadrature.rs
│       ├── interpolation.rs
│       └── export.rs     # CSV export
├── examples/
│   ├── basic.rs          # Simple 3-pin arch
│   ├── multi_segment.rs  # 4+ pins
│   ├── large_deflection.rs
│   └── compare_to_bezier.rs
└── benches/
    └── solver_benchmarks.rs
```

### 9.1 Dependencies (Cargo.toml)

```toml
[package]
name = "spline-physics"
version = "0.1.0"
edition = "2021"

[dependencies]
nalgebra = "0.32"          # Linear algebra (vectors, matrices)
ndarray = "0.15"          # N-dimensional arrays
sqrt_num = "0.1"          # For some numerical routines
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"         # Config file parsing

[dev-dependencies]
criterion = "0.5"         # Benchmarking
approx = "0.5"            # Floating-point comparisons
plotly = "0.8"           # Visualization (optional)

[profile.release]
opt-level = 3
lto = true
```

---

## 10. Integration with constraint-theory-llvm

### 10.1 The Comparison Point

The key question: does ANALOG_SPLINE (quadratic Bézier) produce the same output as the true physical spline?

For each test configuration:
1. Call `analog_spline(points, material, tension)` → get Bézier curve
2. Call `spline_physics::solve(config)` → get physical simulation
3. Compare point-by-point

### 10.2 Potential Discrepancies

**Discrepancy 1: Curvature at pins**
- Bézier: C¹ continuous at control point (tangent is continuous, but second derivative jumps)
- Physical: C² continuous at pins (moment is continuous)
- This means κ_bezier might jump at pin, while κ_physical is continuous
- **Action:** Measure κ_jump at control point, report in metrics

**Discrepancy 2: Peak height**
- For asymmetric arches, Bézier peak may be slightly lower or higher than true elastica
- **Action:** Measure peak_height_error, report as primary metric

**Discrepancy 3: Large deflection**
- For h/L > 0.1, geometric nonlinearity kicks in
- Bézier assumes linear elasticity, true elastica is nonlinear
- **Action:** If T2c (h/L=0.15) fails, document that Bézier is insufficient for large deflections

**Discrepancy 4: Energy**
- Bézier minimizes a discrete energy functional
- Physical spline minimizes the continuous energy functional
- They should agree closely, but may differ by ~1-2%
- **Action:** Report energy_ratio in benchmark results

### 10.3 Expected Outcomes

**Best case:** All tests pass, Bézier is accurate to < 0.5mm for h/L < 0.1
**Acceptable:** Tests pass for h/L < 0.15, errors > 0.5mm only for large deflections
**Problematic:** Errors > 2mm even for moderate h/L — Bézier model needs revision

---

## 11. Open Questions (For Casey)

1. **Material data:** Do we have measured E for the specific PLA we'll print with? Or should we assume a range?
2. **Pin clamping stiffness:** The physical pins aren't perfectly free to rotate — they have some clamping stiffness from the press-fit. Should we model this?
3. **3D effects:** The real spline is a 3D object with width (3mm). Does our 2D model capture enough?
4. **Temperature sensitivity:** PLA is amorphous, E varies with temperature. Should we include thermal correction?
5. **Real batten comparison:** When we move to real shipwright battens (cedar/oak), should we add grain direction effects?

---

## 12. Next Steps

1. **Create the crate** with basic module structure
2. **Implement Phase A** (core infrastructure)
3. **Run flat baseline test** (T1) to validate zero-case
4. **Proceed through Phase B-D** following the implementation order
5. **Report results** — pass/fail table, error curves, integration with constraint-theory-llvm

**Timeline:** ~8-12 days of focused work to complete the full validation pipeline.

---

*Plan written: 2026-05-05*  
*Author: Oracle1 with Claude Code*  
*For: SuperInstance/constraint-theory-llvm Phase 3*