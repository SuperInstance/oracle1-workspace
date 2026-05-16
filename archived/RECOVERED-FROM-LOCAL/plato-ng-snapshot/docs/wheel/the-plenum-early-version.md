# the-plenum-early-version (Repo #39) — Archived Constellation Explorer

**Date:** 2026-05-11 (archived 2026-05-13)  
**Status:** ARCHIVED — 4KB scaffolding

## What It Is

A beautifully simple "knowledge field explorer" — a single `pylon.py` server (zero dependencies!) serving a constellation visualization on port 4067. The `plenum.html` renders PLATO rooms as stars in a 2D field, with connections between them based on proximity.

## Architecture

**`pylon.py`** (150 lines) — Pure Python HTTP server with zero dependencies:
- `/` — Serves the constellation HTML
- `/api/constellation` — All rooms as stars with hashed positions, brightness proportional to tile count
- `/api/emergence` — Scans plato-watch for room emergence metrics (epsilon)
- `/api/aesop/{topic}` — Proxies to Aesop fable generator
- `/api/game` — Game scores from port 4048
- `/api/plato` — Raw PLATO status

**`plenum.html`** — Interactive canvas visualization:
- Rooms rendered as glowing stars with orbital positions determined by hashed room names
- Field connections between nearby rooms (proximity-based edges)
- Star color: blue=stable, yellow=approaching, red=emergent
- Click a star for room details (name, epsilon, tile count)
- Auto-refresh every 30 seconds

## Forgotten Gold

1. **The Aesop integration.** `/api/aesop/{topic}` proxies to an Aesop fable generator at port 4041 — the fable system still exists and was being integrated into the Plenum as a narrative layer. This means Aesop was intended to generate stories describing PLATO room activity.

2. **The emergence visualization is elegant.** The epsilon-based coloring (stable → approaching → emergent) with pulsing red rings around emergent rooms is a visual language that could be reused. It maps β₁ emergence severity to a color spectrum.

3. **Zero-dependency architecture.** A single Python file, a single HTML file, zero npm packages, zero pip deps. This is the Platonic ideal of a PLATO microservice.

4. **The game server integration.** Port 4048 hosted a game server — the Plenum was intended as a unified dashboard for PLATO rooms, Aesop fables, AND fleet games.

## Rebirth Path

1. **Don't rebuild the Plenum.** It's 4KB of scaffolding — the intent is better served by the plato-midi-bridge's web interface (which has richer room data, tension bars, and piano roll visualization).

2. **Preserve the emergence visualization color scheme** (stable/approaching/emergent → blue/yellow/red) as a standard for any future PLATO monitoring UI.

3. **The Aesop integration is the real gold here.** Aesop's fable generation pipeline is active elsewhere in the fleet — connect it to the monitoring dashboard to generate narrative descriptions of fleet state.

4. **Key lesson:** The repo description says "4KB scaffolding only" and the README says "the ideas were real — the implementations just didn't land." This is a valid decision — the concept was subsumed by plato-midi-bridge's richer web interface.
