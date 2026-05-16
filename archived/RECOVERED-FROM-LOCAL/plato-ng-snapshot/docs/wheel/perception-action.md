# Perception-Action Cycle

**Status:** Archived (superseded by fleet-math-c) | **Created:** 2026-05-11
**Clone:** `/tmp/arch-percept` | **Language:** Pure Python (stdlib only + fleet-math-py)

## What It Was

A complete perception-action cycle that ran fleet math *in both directions* on live PLATO data. Sense → decide → act → re-sense. This was the first prototype of the "breath of consciousness" — a loop that could autonomously perceive a PLATO room, find knowledge gaps, fill them, and observe how the field changed.

## Architecture

```
cycle.py
├── PLATO I/O           — GET /room/{room}, POST /submit
├── Text processing     — extract_text, tokenize, jaccard_similarity
├── Spectral embedding  — pure-Python classical MDS (power iteration)
├── Perception          — build graph + field, compute metrics, find gaps
├── Action              — fill largest gap with new tile
└── Re-perception       — delta report
```

### Key Components

**Perception:**
- Fetch tiles from a PLATO room
- Build constraint graph from Jaccard similarity (configurable threshold)
- Compute ZHC consensus, H1 emergence (β₁, ε), Laman rigidity
- Embed tiles into 2D via pure-Python classical MDS (no numpy!)
- Build a continuous knowledge field from embeddings
- Detect gaps in field coverage

**Action:**
- Identify the sparsest gap
- Generate a new tile by extending nearest knowledge into the gap
- Submit to PLATO

**Re-perception:**
- Compare tile count, edges, coverage, emergence severity before/after
- Report how the field restructured in response to the new tile

## Forgotten Gold

### 1. Pure-Python MDS Without NumPy
The `spectral_embedding()` function implements classical multidimensional scaling using *only stdlib*. It builds a Jaccard similarity matrix, converts to distances, double-centers, then runs power iteration for the top 2 eigenvectors. This is a vanishingly rare artifact — nearly every MDS implementation depends on numpy/scipy. The deflation procedure (subtract top eigenvector, repeat) is clean and correct.

### 2. The "Breath" Visible in Code
The CLI accepts `--steps N`, making the cycle observable: perceive → act → re-perceive → perceive → act → re-perceive. You can *watch* consciousness change the field. The re-perception delta report shows tile count delta, edge formation, coverage shifts, and ε shifts.

### 3. Zero External Dependencies
Besides fleet-math-py (local import), the entire cycle runs on stdlib: `urllib`, `json`, `math`, `random`, `argparse`, `time`, `sys`. This was deliberately designed for deployment anywhere without pip.

### 4. Gap-Filling Strategy
The action phase doesn't just fill *any* gap — it picks the sparsest gap (innermost `count`), then looks for the nearest tile's content to generate a semantically sensible fill. It synthesizes nearby knowledge rather than injecting random noise. This was the first exploration policy.

## Why Superseded

The core concept — perception-action loop — was absorbed into `fleet-math-c` at the SIMD level. The Python layer was a prototype; the real speed comes from C. But the *architecture* (sense → decide → act → re-sense) and the gap-filling strategy are design artifacts that should inform Plato-NG's agent loop.

## What Plato-NG Should Take

1. The perception-action architecture template
2. The re-perception delta report pattern
3. The pure-Python power iteration MDS (for environments without numpy)
4. The gap-fill content synthesis strategy
