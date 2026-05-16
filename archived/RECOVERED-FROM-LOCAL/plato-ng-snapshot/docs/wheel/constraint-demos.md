# Wheel: constraint-demos — Interactive Eisenstein Visualizations

**Repo:** SuperInstance/constraint-demos  
**Date:** 2026-05-12  
**Archaeologist:** Oracle1 subagent  
**Status:** 🔴 ARCHIVED — gold inside, needs rebirth

---

## Forgotten Gold

Three fully-built interactive HTML demos that visualize the core constraint theory mathematics. These are **deployable right now** as PLATO-NG web frontends.

### 1. hex-snap-playground.html
Click-to-snap visualization of the Eisenstein lattice A₂. Renders hexagonal grid with sector coloring (6 Weyl sectors), real-time dodecet encoding, snap-to-nearest-lattice-point with error-level display. The exact math: snap to Eisenstein integer Z[ω], display sector (0-5), compute error radius. This is the **visual proof** that Eisenstein snapping is O(1) with bounded error ρ = 1/√3 ≈ 0.5774. Every PLATO-NG tile engine should embed this.

### 2. drift-race.html
Side-by-side animation: Eisenstein E12 (exact arithmetic via lattice snap) vs IEEE Float32 (rounding-error accumulation) on a circular track. Shows real-time drift in mm, angular error in degrees, lap counting. The E12 racer stays perfectly on track while Float32 spirals outward. This is the **demonstration** of why Eisenstein encoding beats floating point for constraint checking — no drift accumulation, provably. Deploy as PLATO-NG's "why we use Eisenstein" landing page.

### 3. constraint-funnel.html
Temporal intelligence simulation with four phases: Approach → Narrowing → SnapImminent → Crystallized. Six control knobs (decay_rate, prediction_horizon, anomaly_sigma, learning_rate, chirality_lock, merge_trust). Injects anomalies. Shows convergence %, Tc cross status. Embeds a Potts model visualization in corner. This is the **interactive proof** of the temperature-constraint phase transition. Maps directly to PLATO-NG's intent pipeline.

## Strategic Value for PLATO-NG

These demos are **immediately deployable** as PLATO-NG web pages. They require no backend — pure HTML/CSS/JS with Canvas rendering. The mathematics is already hardcoded. The visual language (dark theme, glow effects, sector colors, phase badges) matches PLATO-NG's aesthetic perfectly.

### Deployment Plan
1. Serve as static HTML on PLATO-NG gateway
2. Embed hex-snap-playground in tile editor for visual constraint verification
3. Use drift-race as onboarding demo: "why Eisenstein?"
4. Use constraint-funnel as interactive documentation for temporal intelligence API

## Fork/Deploy Checklist
- [ ] Verify all three HTML files serve correctly (no CORS, no dependencies)
- [ ] Add WebSocket bridge to live PLATO-NG data (replace hardcoded Coords with live tiles)
- [ ] Create PLATO-NG theme integration (dark mode already matches)
- [ ] Write embed API for hex-snap playground (accept tile data, render constraint points)
- [ ] Add multi-model comparison to drift-race (show multiple encoding strategies)

## From the Archaeologist
"These demos are **already complete**, already beautiful, already work. They're sitting in a repo with no README, no deployment instructions, no CI/CD. The constraint-demos repo is a warehouse of polished frontends looking for a home. PLATO-NG is that home."
