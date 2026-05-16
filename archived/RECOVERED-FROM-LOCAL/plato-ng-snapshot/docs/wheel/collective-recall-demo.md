# Wheel: collective-recall-demo — Telephone Game Visualization

**Repo:** SuperInstance/collective-recall-demo  
**Date:** 2026-05-12  
**Status:** 🔴 ARCHIVED — superseded by fleet-scribe, but still contains gold  

---

## Forgotten Gold

A complete, interactive, single-file HTML visualization of the telephone game experiment — the real-world validation of how agent memories drift through lossy reconstruction. **Hardcoded with actual experimental data from the MV Epsilon test.**

### What It Shows

6 rounds of model-to-model retelling:

| Round | Model | Facts | Fidelity | Notes |
|-------|-------|-------|----------|-------|
| 0 | Seed-mini | 13/14 | High | Technical, accurate |
| 1 | Seed-code | 13/14 | High | Invents character Lila Marquez |
| 2 | Hermes-70B | 14/14 | High | **Recovers lost fact** via inference |
| 3 | Seed-mini | 10/14 | Mid | Drops to party story frame |
| 4 | Seed-code | 8/14 | Low | Grandmother frame, loses precision |
| 5 | Hermes-70B | 6/14 | Critical | Legend/myth frame |

### Interactive Features

- **Chain visualization** — animated round-by-round reveal with color-coded fidelity
- **Drift curve** — real-time chart showing facts surviving per round
- **Crystallization mark** — red line at Round 3-4 where facts lock into narrative (predicted t* ≈ 3-4: CONFIRMED)
- **Fact survival matrix** — 14 facts × 6 rounds, starred for immortal facts
- **Novel additions feed** — 11 creative additions timed to appear after simulation
- **Reconstruction lab** — build story from only 6 immortal facts → compare to original 14

### The Immortal Facts (survived all 6 rounds)

1. **MV Epsilon** — ship name (proper noun anchor)
2. **4,200 containers** — scale (large round number)
3. **Narrows Strait** — dramatic location name
4. **47-degree turn** — specific constraint angle
5. **200 meters drift** — near-miss distance (high emotion)
6. **47,000 vessels** — fleet-wide risk (narrative urgency)

### Key Validations

- Crystallization at t* ≈ 3-4: CONFIRMED (TILE COMPRESSION THEOREM Prediction 3)
- High-emotion facts survive: CONFIRMED (Prediction 4)
- Collective reconstruction beats individual: CONFIRMED (Round 2 recovered Round 0's loss)
- Hallucinations are lattice snaps: CONFIRMED (Lila Marquez, Grandma Elma = nearest narrative pattern)

## Strategic Value for PLATO-NG

This is the **empirical validation** of the entire constraint theory of memory. Every concept from the papers is demonstrated here with real data:
- Tile compression theorem → fact survival matrix
- Baton protocol → three rounds stabilize narrative
- Adjunction → reconstruction beats archive
- Amnesia curve → drift chart slope
- Immortal facts → constraint points in lattice

### Deployment
- Serve as PLATO-NG "live experiment" page
- Add WebSocket to run new telephone games on demand
- Replace hardcoded data with real-time results from fleet-scribe or current model chains
- Use as onboarding: "This is why we store tiles, not archives"

## Relationship to fleet-scribe

The README says "superseded by fleet-scribe One Delta library." The visualization UI is still valuable — fleet-scribe provides the engine, collective-recall-demo provides the showcase.

- **Fleet-scribe** = the library for running memory drift experiments
- **collective-recall-demo** = the visualization for displaying results
- **Merge proposal**: Add collective-recall-demo's HTML as fleet-scribe's built-in report renderer

## From the Archaeologist
"The demo is beautiful, complete, and contains real experimental data confirming the fleet's core theories. The drift curve shows exactly what the papers predict: crystallization at Round 3-4, immortal facts are constraint points, collective reconstruction beats individual recall. This should not be archived — it should be the PLATO-NG demo page."
