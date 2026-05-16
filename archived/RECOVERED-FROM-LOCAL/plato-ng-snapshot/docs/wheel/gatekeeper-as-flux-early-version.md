# Gatekeeper as FLUX — Early Version (Archived)

**Status:** ⚰️ Archived — "empty placeholder" per README, but **code was actually written**
**Repo:** `SuperInstance/gatekeeper-as-flux-early-version`
**Original date:** 2026-05-11

## What It Was

Despite the README claiming "no code was written," this repo contains **two substantial files** that bridge the Gatekeeper and FLUX protocols:

### `bridge.py` — Gatekeeper Policy → FLUX-C Bytecode Compiler
Compiles GUARD IR policies (min_length, max_length, no_absolute terms, confidence_range) into FLUX-C stack-based bytecode. Each policy becomes a sequence of PUSH/LOAD_VAR/SWAP/ASSERT mnemonics, ending in a final ALLOW if all checks pass. This is a **real policy compilation pipeline** — 4 policies → 16 FLUX-C instructions.

### `eisenstein_deadband.py` — Eisenstein Lattice Snapping
FM proved (mathematically) that the Eisenstein (hexagonal) integer lattice is superior to the Z2 (square) lattice for constraint snapping:

- **Cell area:** √3/2 ≈ 0.866 (Eisenstein) vs 1.0 (Z2) — more efficient packing
- **Covering radius:** 1/√3 ≈ 0.577 (Eisenstein) vs 1/√2 ≈ 0.707 (Z2) — tighter constraint neighborhood
- **Adversarial gap:** CLOSED — Eisenstein is provably superior

Implements the three deadband protocols on the Eisenstein lattice:
- **P0 (greedy):** Snap to nearest Eisenstein point with 6-neighbor search
- **P1 (hex Voronoi):** 6-candidate hexagonal Voronoi search with better coverage
- **P2 (true nearest):** Standard nearest-neighbor (unchanged from Z2)

The benchmark shows ~99% pass rate for both P0 and P1 at 0.5 threshold.

## Why It Matters Now

This is the **missing link** between policy enforcement (Gatekeeper) and field-constraint satisfaction (FLUX). The Eisenstein lattice theory is production-grade mathematics that FM validated — the fleet should integrate it into the PLATO-NG Gatekeeper Wheel.

## What to Salvage

1. **FLUX-C bytecode format** — a simple stack VM for expressing policy constraints. Could be the intermediate representation for the Gatekeeper Wheel's policy compiler.
2. **Eisenstein lattice deadband** — directly applicable to any constraint-satisfaction problem where you need to snap to nearest satisfying state. The hexagonal lattice is mathematically optimal.
3. **P0/P1/P2 protocol pattern** — the tiered approach (greedy → better → exact) is a clean pattern for progressive constraint resolution in the Gatekeeper Wheel.

## Abandoned Approaches

- The FLUX-C bytecode was never connected to an actual VM. The interpreter doesn't exist yet.
- Single-file design — no separation of compiler, lattice math, or protocol logic.
