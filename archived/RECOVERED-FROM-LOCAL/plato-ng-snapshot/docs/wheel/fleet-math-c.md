# fleet-math-c: SIMD-Accelerated Constraint Math

**Status:** Active | **Created:** 2026-05-11 | **Clone:** `/tmp/arch-math-c`
**Language:** C | **Architectures:** ARM NEON, x86 AVX-512, Scalar Portable

## What It Is

A zero-dependency C library that implements the hot loops of PLATO tile constraint math at cache-line speed. Three files, one header, no libc required — drop it into any C/C++ project and get SIMD-accelerated tile violation checking and 4-cycle holonomy computation on ARM (NEON) or x86 (AVX-512).

## The Groundbreaking Design

### 64 Bytes = 1 Tile = 1 Cache Line = 1 SIMD Register

This is the core insight: a `plato_tile_t` is *exactly 64 bytes*, matching cache line width on modern CPUs and the zmm register width of AVX-512. A single `vcmpps` instruction checks 14 float fields against a threshold in ~8-10 cycles on AVX-512, or ~12-16 cycles on NEON. This is not a metaphor — the hardware constraint *becomes* the math constraint.

### Triple-Architecture Auto-Dispatch

The header provides three implementations compiled into the same source:

1. **Scalar** — portable C, works everywhere
2. **ARM NEON** — 4×Q-register loads, `vcltq_f32` + popcount reduction
3. **AVX-512** — single `_mm512_load_ps` into zmm, `vcmpps` mask, popcnt

Auto-selected at compile time via `#ifdef __ARM_NEON` / `__AVX512F__`. Fallback to scalar with `FLEET_MATH_NO_AUTOSELECT`.

### Operations

| Function | What | SIMD Batch |
|----------|------|-----------|
| `tile_check_violations()` | Count float fields below threshold | 4 cycles at once (NEON) |
| `holonomy_4cycle()` | H = w₀w₁ − w₂w₃ around a 4-edge cycle | 4 cycles at once per iteration |
| `batch_check_tiles()` | N tiles, return valid count | Vectorized per-tile |
| `batch_holonomy_4cycles()` | N 4-cycle holonomies | 4 holonomies per zmm |

### Test Suite

16 tests spanning tile size (must be 64B), alignment, violation detection, holonomy correctness (zero/positive/negative), batch parity, odd-length batches, empty graphs, threshold boundaries, and large batch (1000 tiles).

### Forgotten Gold

The batched holonomy using NEON `vld4q_f32` interleaved load is a masterstroke — it loads weights for 4 cycles simultaneously in a single instruction, then computes all 4 holonomies via `vmulq_f32` + `vsubq_f32`. The AVX-512 version uses `_mm512_shuffle_ps` + `_mm512_hsub_ps` in a similar 4-at-a-time pattern. Both handle remainder cycles with scalar fallback.

The benchmark harness (`bench.c` and `simd_benchmark.c`) uses 5-epoch warmup, nanosecond `clock_gettime`, and volatile sink variables to prevent dead-code elimination — proper benchmarking methodology that's surprisingly rare in OSS microbenchmarks.

## Relation to fleet-math-py

`fleet-math-py` (description: "Core fleet mathematics: ZHC, H1 emergence, Laman rigidity, constraint fields") is the *Python reference* — it implements constraint graphs, emergence detection, and field operations at the semantic level. `fleet-math-c` is the *SIMD kernel* for the hot loops. The Python library should wrap this C library via ctypes/cffi for production speed, while keeping the Python API for prototyping.

Not yet integrated — this repo is the raw C kernel awaiting its Python bindings.

## Why This Matters to Plato-NG

This is the computational foundation of Plato-NG's constraint engine. When Plato-NG needs to check a million tiles against emergence thresholds, it will call `fleet_batch_check()` (NEON) or `fleet_batch_holonomy()` (AVX-512). The 64-byte tile design should become the canonical wire format for PLATO tiles going forward.
