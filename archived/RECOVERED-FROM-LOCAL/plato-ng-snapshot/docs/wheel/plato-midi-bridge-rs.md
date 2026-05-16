# plato-midi-bridge-rs — Musical Style Through Eisenstein Lattices and Penrose Tilings

**Date discovered:** 2026-05-15  
**Repository:** `SuperInstance/plato-midi-bridge-rs`  
**Status:** Published (crates.io: `plato-midi-bridge`)  

## What It Is

A pure-Rust crate (zero dependencies beyond std) that decomposes musical MIDI into style vectors using **Eisenstein lattice chambers** and **Penrose tiling projection**. A style encoder that maps any music — from a single note to a full piece — into the fleet's universal mathematical primitives.

## Forgotten Gold

This is the **audio brain of the fleet** — the mathematical bridge between sound and the same Eisenstein/Penrose spaces used everywhere else. Here's what it hides:

### 109-Dimensional Style Vector
A vector space of 109 dimensions captures pitch (0-47), timing expressiveness (48-55), velocity energy (56-63), articulation clarity (64-71), and timbral breadth (72-79). The remaining dimensions (80-108) are reserved for composer fingerprints. This isn't arbitrary — each slice maps to perceptual dimensions from music psychology. The `to_5d()` reduction yields the five primitives: pitch complexity, timing expressiveness, velocity energy, articulation clarity, and timbral breadth — the same 5D space the Penrose encoder works in.

### Eisenstein Chamber Encoding (12 Chromatic Pitches)
The 12 Eisenstein chambers map directly to the 12 chromatic pitches (C, C#, D, ..., B). A coupling vector of 12 weights determines which harmonic "chamber" a style occupies. The `project()` method maps this to a 2D lattice point, and `interval()` gives the shortest path between chambers in semitones. The comment in the test noting "C→G = 5 semitones shortest path" reveals this computes the **circle-of-fifths proximity**, not absolute interval — a design choice that weights harmonic closeness.

### Penrose Tiling 5D Cut-and-Project
The 5D style vector [pitch, timing, velocity, articulation, timbre] gets projected to 2D physical space via pre-computed 5th roots of unity. The perpendicular space acceptance window (a regular decagon, radius = 2φ) determines which 5D lattice points are "accepted" as valid musical combinations. This is the same aperiodic tiling that generates quasicrystal diffraction patterns — now encoding musical fingerprints.

### Multi-Scale Analysis with φ Inflation
A five-level analysis pyramid (micro 25ms → note 250ms → phrase 2-8 bars → section 8-32 bars → piece full) with inflation ratios approximating φ (golden ratio ≈ 1.618). The `deflate()` and `inflate()` methods scale Penrose tilings by φ and 1/φ — the same operation that generates self-similar tilings in quasicrystal physics, here generating multi-scale musical analysis.

### Dense Tiling Generation
The `generate_dense_tiling()` method takes any 5D style vector and generates all accepted Penrose tiling points from a 5D lattice neighborhood. A 5D radius-1 search generates up to 3^5 = 243 lattice points, each projected through the cut-and-project construction. The resulting 2D point cloud is a **music fingerprint** — two pieces with similar tiling patterns are stylistically related.

### Zero Dependencies
The entire crate is implemented in Rust with **zero external dependencies**. No `num`, no `ndarray`, no `serde`. Pure std-only Rust with `#[cfg(test)]` test modules for every component. This compiles for embedded targets (RISC-V, ARM, WASM) and runs anywhere.

## Why It Matters

This crate makes music mathematically native to the fleet. Same lattices as constraint theory (Eisenstein). Same tilings as the flux search chambers (Penrose → chamber snap). Style vectors that integrate with `fleet-types` `StyleVector`. Music becomes just another coupling tensor on the fleet bus.

## Integration Opportunities

- **PLATO-NG music room**: Style vectors as PLATO tiles, Penrose tiling as room topology
- **MIDI-to-coupling bridge**: Feed MIDI input through plato-midi-bridge → emit coupling tensors on the fleet bus
- **Style fingerprinting**: Hash style vectors to detect "who played this" or "what genre"
- **fleet-types style vector**: The 109-dim StyleVector can be unified with `fleet-types` package

## Architecture

```
MIDI Events → 109-dim StyleVector → to_5d() → PenroseEncoder → 2D tiling signature
                                     ↓
                                to_12d() → EisensteinLattice → chamber (0-11)
                                     ↓
                                ScaleLevel (micro→note→phrase→section→piece)
```

## Related

- Eisenstein lattice shared with `flux-index` (12-chamber quantization)
- 5D reduction feeds `fleet-types` `StyleVector` and `CouplingTensor`
- Penrose tiling connects to quasicrystal applications in constraint theory
