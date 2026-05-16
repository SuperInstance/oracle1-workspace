# Attention Daemon — Early Version (Archived)

**Status:** ⚰️ Archived — "1KB scaffolding only"
**Repo:** `SuperInstance/attention-daemon-early-version`
**Original date:** 2026-05-11

## What It Was

The simplest of the three early FLUX experiments — a **salience attention daemon** that polls PLATO rooms every 60 seconds, computes a salience score for each room, and displays the top 5 most "interesting" rooms with a Unicode bar chart.

The salience function was a weighted combination of:
- **Novelty (30%)** — tile_count / 100, normalized. How much content exists.
- **Change (40%)** — absolute tile count delta from last poll. How much things are moving.
- **Curiosity (30%)** — 1/(1 + tile_count). Inverse exploration bonus — less-known rooms are more interesting.

Scored rooms sorted descending, top 5 displayed with `█`/`░` progress bars showing relative salience.

## Why It Matters Now

This is the **direct ancestor** of the PLATO-NG Monitoring Wheel's salience detector. The formula — novelty + change + curiosity — is exactly what the Monitoring Wheel needs for adaptive resource allocation across the fleet.

Key insights from this experiment:
1. **Curiosity drive** — the inverse-exploration bonus is a real pattern: rooms with fewer tiles get more attention, which balances exploration vs exploitation.
2. **Change weighting** — the 40% weight on delta was correct; detecting rooms in flux is more valuable than static high-traffic rooms.
3. **Bar chart UI** — simple, effective, embeddable in any terminal or PLATO log.

## What to Salvage

1. **The salience formula** — `0.3*novelty + 0.4*change + 0.3*curiosity` should be the default heuristic in the Monitoring Wheel's salience detector, with tunable weights per agent role.
2. **Archive → active pattern** — this was never meant to run continuously. Convert it to an event-triggered function that fires when tile counts change significantly.
3. **Attention budget** — the daemon didn't have one, but the concept of "only show top 5" is a primitive attention budget. Formalize it.

## Abandoned Approaches

- Hardcoded 60-second polling interval is wasteful. The Monitoring Wheel should use event-driven triggers (tile submission events) instead of polling.
- Single-process design limits scaling to one PLATO instance.
- No persistence — salience scores are lost between restarts. Should write to PLATO as tiles, not just print to stdout.
