# Flux-Compiler Science Audit — 2026-05-13

## Executive Summary
Claims are PARTIALLY ACCURATE. The system prober and benchmark engine work, but
some counts are inflated and some language claims are aspirational rather than
implemented.

---

## Finding 1: "5-language self-discovering engine"

**Verdict: EXAGGERATED**

Code proves 4 compiled language kernels (C, Zig, Fortran, Nim) + Python/numpy.
probe_system() detects gcc, clang, zig, gfortran, nim, matlab, R, lua — but
only C, Zig, Fortran, Nim have actual compiled kernel implementations.

Python and numpy ARE implemented. MATLAB and R are detected but only callable
via CLI subprocess (no compiled kernels). Lua is checked but never bound.

**Breakdown:**
- C kernels: norm, check, bloom, snap, fold (5 kernels)
- Zig kernels: norm, bloom (2 kernels)
- Fortran kernels: bloom, fold (2 kernels)
- Nim kernels: norm, bloom (2 kernels)
- Python: norm, check, snap, fold (4 bindings, 2 via numpy)
- numpy: norm, check, bloom, fold (4 bindings)

Languages with compiled kernels: 4 (C, Zig, Fortran, Nim)
Languages detected but NOT compiled as kernels: MATLAB, R, Lua

---

## Finding 2: "19 implementations across 7 primitives"

**Verdict: EXAGGERATED (count differs from code)**

Only 5 primitives exist in the codebase (norm, check, bloom, snap, fold) and
perf_db.json confirms only 5 entries. The claim of 7 primitives is unsupported.

**Actual implementation count per primitive:**

| Primitive | Implementations |
|-----------|-----------------|
| norm      | 6 (c_scalar, c_avx2, zig, nim, python, numpy) |
| check     | 3 (c_avx2, python, numpy) |
| bloom     | 6 (c_avx2, zig, fortran_ior, nim, python, numpy) |
| snap      | 2 (c_avx2, python_voronoi) |
| fold      | 4 (c_scalar, fortran, python, numpy) |

**Total: 21 implementations across 5 primitives** (not 19 across 7)

---

## Finding 3: "Persistent learning" via perf_db.json

**Verdict: REAL**

- perf_db.json exists at repo root
- Contains real benchmark data (ns/call, call counts)
- Source attribution is accurate (e.g., "fortran_ior" for bloom,
  "zig_shared_lib" for norm, "numpy" for check)
- System probe captures hardware context (arch, cores, has_avx2, has_numpy)

The perf_db.json IS used by the code (referenced in flux_runtime.py line 457:
"2. Faster implementation was discovered in perf DB")

---

## Finding 4: "Benchmark engine with warmup + timed trials"

**Verdict: REAL (in fluxc_autotune.py)**

Code shows:
- Warmup loop before benchmark (line 117: "Warmup...")
- `clock_gettime(CLOCK_MONOTONIC)` for ns-precision timing
- Iterations parameterized (default 10M)
- Verification pass before benchmarking
- Correctness check after each strategy

The benchmark engine in fluxc_autotune.py is legitimate. However, the
"persistent learning" claim overstates what's actually stored — perf_db.json
appears to be a snapshot, not a continuously-growing learning database.

---

## Finding 5: "System prober"

**Verdict: REAL**

probe_system() in flux_runtime_v2.py (line 65) is a genuine system prober:
- Detects compilers: gcc, clang, zig, gfortran, nim, matlab, R, lua
- Checks Python packages: sympy, cvxpy, sklearn, networkx, cryptography
- Finds C shared libraries via ctypes.util.find_library
- Probes CPU features: AVX2, AVX512, SSE2
- Detects CUDA availability

---

## Summary Table

| Claim | Status | Notes |
|-------|--------|-------|
| 5-language engine | EXAGGERATED | 4 compiled (C/Zig/Fortran/Nim) + Python; MATLAB/R/Lua not compiled |
| 19 implementations | EXAGGERATED | 21 implementations across 5 primitives (not 19 across 7) |
| 7 primitives | FALSE | Only 5 primitives: norm, check, bloom, snap, fold |
| Persistent learning | HALF-TRUTH | perf_db.json is real and used, but not truly "learning" |
| Benchmark engine | VERIFIED | Warmup + timed trials + verification in fluxc_autotune.py |
| System prober | VERIFIED | probe_system() detects compilers, libs, CPU features |

---

## Performance Data (from perf_db.json)

| Primitive | Best Implementation | Avg ns/call |
|-----------|---------------------|--------------|
| check     | numpy               | 2929.6       |
| bloom     | fortran_ior         | 978.5        |
| snap      | python_voronoi_skip | 171903.4     |
| norm      | zig_shared_lib      | 5161.3       |
| fold      | numpy               | 27426.8      |

