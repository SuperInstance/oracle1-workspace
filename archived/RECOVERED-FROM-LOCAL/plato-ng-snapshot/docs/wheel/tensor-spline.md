# tensor-spline — Eisenstein Lattice Weight Compression

**Repo:** `SuperInstance/tensor-spline` (2026-05-14)
**Status:** FORGOTTEN GOLD — Published to PyPI, zero stars, never mentioned again.

## What It Is

A genuinely novel neural network weight compression technique. Instead of storing full weight matrices as independent floats, `SplineLinear` parameterizes weights via control points on an **Eisenstein (hexagonal) lattice** — a+bω where ω = e^(2πi/3). The full weight matrix is re-materialized on every forward pass through IDW interpolation, Gaussian RBF, or bicubic B-spline kernels.

## Why It Matters

This isn't LoRA with a different name. The Eisenstein lattice gives hexagonal packing (most efficient 2D covering), so control points naturally cluster near the origin with maximal density. The interpolation is *structural* — weights at neighboring positions share control points through smooth proximity weighting, not just low-rank decomposition.

- **SplineLinear:** 16,384:1 compression on 512×512 layers (262K → 16 params)
- **100% accuracy at 20× compression** on drift-detect (smooth tasks)
- **Three basis functions:** eisenstein (IDW, smooth), gaussian (learned bandwidth), bspline (bicubic kernel)
- **HierarchicalSplineLinear:** Two-level coarse+fine for high-dimensional tasks (409:1 at 256×128)
- **LowRankLinear:** Falls back to U@V factorization for sharp classification tasks (5-16×)
- **Auto-selection:** `recommend_variant()` picks the right method from a task description

## Forgotten Gold

The README is brutally honest — "only 31% on topic-classify" — but that's a feature, not a bug. The documentation explicitly tells you which tool to use for which task. The test suite covers all three basis functions. The `inject_spline()` and `inject_low_rank()` functions are drop-in replacements for any `nn.Linear` model.

This was published and abandoned. The research work is solid. The code is clean, well-documented, and type-annotated. It's a complete compression library waiting for someone to pair it with the PLATO training pipeline.
