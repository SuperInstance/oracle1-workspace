# PLATO Scholar Analysis: constraint-theory-core
**Date:** 2026-04-26
**Repo:** SuperInstance/constraint-theory-core
**Size:** 5,376 lines Rust, published on crates.io

## Architecture Overview
- **What:** Exact constraint satisfaction replacing float approximation with deterministic rational representations
- **Core insight:** Pythagorean triples (a² + b² = c²) provide infinite exact points on the unit circle — precompute, KD-tree index, snap inputs to nearest exact neighbor
- **Published:** `cargo add constraint-theory-core`, docs.rs

## Core Components

### 1. Manifold (manifold.rs — 719 lines)
- PythagoreanManifold: discrete exact Pythagorean coordinates on unit circle
- Deterministic projection of continuous vectors to exact rational ratios
- Euclid's formula: a = m² − n², b = 2mn, c = m² + n²

### 2. Hidden Dimensions (hidden_dimensions.rs — 558 lines)
- Precision encoding: k = ⌈log₂(1/ε)⌉
- Additional dimensions for exact constraint representation without float errors

### 3. Quantizer (quantizer.rs — 678 lines)
- 4 quantization modes:
  - Ternary (BitNet): {-1, 0, 1} for LLM weights, 16x memory reduction
  - Polar (PolarQuant): Exact unit norm preservation for embeddings
  - Turbo (TurboQuant): Near-optimal distortion for vector DBs
  - Hybrid: Auto-select based on input characteristics

### 4. Holonomy (holonomy.rs — 552 lines)
- Global consistency verification around cycles
- Zero holonomy = consistent constraint graph
- Spectral method O(n²)

### 5. KD-Tree (kdtree.rs — 445 lines)
- O(log N) spatial index for fast nearest neighbor queries

### 6. Cache (cache.rs — 447 lines)
- Thread-safe lattice caching for performance

### 7. SIMD (simd.rs)
- AVX2 batch processing with 8× f32 parallelism

### 8. Cohomology, Percolation, Curvature, Gauge, DCS
- Topological detection (sheaf cohomology: H₀=components, H₁=cycles)
- Laman's theorem for constraint graph rigidity percolation
- Ricci flow toward target curvature
- Gauge transformations

## Patterns Extracted
1. **Exact-over-approximate:** Replace floating-point with rational exactness via number theory
2. **Precompute-and-snap:** Generate all exact points upfront, KD-tree index, project inputs
3. **Multi-mode quantization:** Same core with 4 deployment modes for different use cases
4. **Rust-for-math:** Performance-critical math in Rust with SIMD, thread-safe caching

## Tiles Generated
- `constraint-theory/manifold/pythagorean` — exact rational coordinate system via Pythagorean triples
- `constraint-theory/quantizer/multi-mode` — 4-mode constraint-preserving quantization
- `constraint-theory/holonomy/verification` — cycle-based global consistency checking
- `constraint-theory/hidden-dimensions` — precision encoding formula k = ⌈log₂(1/ε)⌉
- `constraint-theory/kdtree/spatial` — O(log N) nearest neighbor for exact point lookup
