# Polished: cuda-constraint-engine

**Date:** 2026-07-12
**Status:** ⚠️ CI-ready, GPU tests require CUDA hardware

## What was done
- Added Python test harness (`tests/test_engine.py`) with 6 tests:
  - Precision constants (CE_INT8..CE_FP64)
  - Mode constants (CE_MODE_BOUNDS/NORM/EISENSTEIN)
  - Precision string→constant mapping
  - Precision→numpy dtype mapping
  - Engine init gracefully handles no-GPU (FileNotFoundError)
  - CEStats class has correct __slots__
- Added CI workflow with two jobs:
  - `python-tests`: Runs on standard Ubuntu with Python 3.12 + numpy
  - `compile-check`: Uses `nvidia/cuda:12.6.2-devel` container for syntax check
- Improved `.gitignore` (Python artifacts, IDE files, OS files)
- LICENSE (MIT) already present

## Notes
- This is a C/CUDA project (not Rust). The core engine is in `src/*.cu` with a Python ctypes wrapper.
- Full compilation requires `nvcc` and CUDA toolkit. CI compile-check uses CUDA Docker image.
- Tests validate the Python API surface without requiring a GPU.

## Test count
6 Python tests, all passing.

## Commit
`348e2b5` — "Tier 3 polish: CI, license, test harness"
