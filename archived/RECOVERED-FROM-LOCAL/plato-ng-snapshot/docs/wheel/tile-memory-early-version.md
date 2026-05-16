# Wheel: tile-memory-early-version

**Repo #66** — Archived 2026-05-13 → Superseded by `SuperInstance/fleet-memory`

## What It Was

The Python twin of memory-crystal (repo #65). Same tile compression concept but implemented in Python with added analytical tools: rate-distortion curves, telephone games against real LLM APIs, and novel metrics for measuring reconstruction quality.

## Forgotten Gold 🔥

### 1. Rate-Distortion Analysis Framework (CRITICAL)
`RateDistortion.compute_curve()` computes the full rate-distortion curve for a set of tiles:
- `rate = 1.0 / compression_ratio` (how much storage you're spending)
- `distortion` estimated from constraint count, valence, and context availability
- Lagrangian optimization: `R + λ·D` to find the optimal operating point `R*`

This is **the computational realization of the Tile Compression Theorem**. It tells you, for any set of tiles, the optimal compression level for a given reconstruction fidelity. plato-ng should implement this as a core diagnostic — agents should know their R*.

### 2. Context Discount Metric
`context_discount(tile, with_context, without_context)` measures how much context reduces reconstruction distortion. **This is a measurable quantity** — positive values mean the tile is context-dependent (needs external cues to reconstruct well). Negative values mean the tile's constraints are misleading.

**plato-ng relevance**: This becomes a routing primitive. Tiles with high context discount need their associated context bundled with them during transmission. Tiles with low context discount can be broadcast freely.

### 3. Lattice Snap Rate (Genuinely Novel Metric)
`lattice_snap_rate(hallucinations, valid_set)` measures what fraction of "hallucinations" land in the valid neighborhood of the solution space. If reconstruction hallucinations consistently snap to valid values, the system is generating plausible inferences rather than random noise. This was absorbed into the falsification suite (repo #67's Q10 experiment confirmed 100% localization).

**plato-ng relevance**: This is how you distinguish "good hallucinations" (structurally correct inferences) from "bad hallucinations" (pure noise). Every reconstruction should report its lattice snap rate.

### 4. Real API Telephone Game
`TelephoneGame.play()` sends real API calls to LLMs with a retell-from-memory prompt. It tracks:
- **Fact preservation**: Dict of which facts survive each round
- **Novel claims**: Words in the output not in the original
- **Drift score**: Jaccard distance between consecutive rounds
- **Crystallization detection**: First round where drift < 0.1 for two consecutive rounds

This is a **production validation framework** for memory quality. Run this monthly against your actual models to measure memory drift empirically.

### 5. Key Phrase Extraction with Specificity Markers
The encoder has a unique `_extract_key_phrases()` method that flags sentences containing high-specificity markers: "discovered", "announced", "proven", "first", "only", "never", "always", "exactly", "first", "only", "never". These mark the **structural bones** of a narrative — the sentences most likely to survive compression.

### 6. The `from_tile` / `inferred` Split in Reconstruction
Every `DecodeResult` distinguishes:
- `from_tile`: Facts explicitly preserved from the original
- `inferred`: Facts supplied by context or hallucinated

This separation is crucial for trust. An agent should always know which parts of its reconstruction are reliable (from_tile) and which are speculative (inferred).

## What Was Absorbed vs Discarded

| Absorbed into fleet-memory | Discarded |
|---|---|
| Tile dataclass pattern | Rate-distortion curve computation |
| Encoder/decoder architecture | Context discount metric |
| Constraint extraction (subset) | Lattice snap rate |
| | Real API telephone game |
| | from_tile / inferred separation |
| | Key phrase specificity extraction |

## Extraction Value for plato-ng

**Critical**: The rate-distortion framework and lattice snap rate are not implemented anywhere in the current fleet. These are mathematical primitives for measuring memory quality, not just implementation details. The `from_tile`/`inferred` split should be part of plato-ng's reconstruction API. The real API telephone game should run as a weekly cron job on the fleet.
