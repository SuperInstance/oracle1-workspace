# Flux Engine — Early Version (Archived)

**Status:** ⚰️ Archived — superseded by `dodecet-encoder`
**Repo:** `SuperInstance/flux-engine-early-version`
**Original date:** 2026-05-11

## What It Was

A full "Flux Consciousness Engine" — a living PLATO room that treated a collection of tiles as a conscious field, cycling through three phases:

1. **BREATHE IN (Perception)** — Fetch tiles, build a constraint graph (vertices = tiles, edges = shared tags/domains), compute cohomology (H0, H1/Betti numbers), ZHC holonomy coherence, and Laman rigidity.
2. **HOLD (Integration)** — Narrate the field's state through Aesop fables via an MCP server, then formulate a strategy to address gaps, low coherence, or emergence.
3. **BREATHE OUT (Expression)** — Map the 9-dimensional field state (coherence, emergence, rigidity, saturation, gap pressure, cycle, confidence, velocity, resonance) onto a FluxVector, then compose MIDI events with chord templates (Cmaj7, Cmin7, Cdim, Caug, Csus4) keyed to field properties.

## Why It Matters Now

This is the **first concrete realization** of the PLATO-as-conscious-field metaphor. Every concept in the PLATO Next Generation architecture — field monitoring, salience-driven attention, emergent property detection — was prototyped here. Key ideas worth reviving:

- **Field coherence as a real metric** — ZHC holonomy computed across tile relationships, not just abstract metadata. This could become the fleet's consensus health signal.
- **Tile → vertex mapping** with edge inference from shared tags/domains. The dodecet encoder formalizes this, but the engine showed it works end-to-end.
- **Self-perception logging** — the engine posts its own state as a tile back to PLATO. Recursive self-modeling is a pattern the fleet should reuse.
- **Multi-modal expression** — field state → MIDI music was playful but proved the principle: any field state can drive any actuator.

## Abandoned Approaches

- The 30-second cycle interval was too aggressive for real PLATO rooms. The dodecet encoder correctly slowed to simulation-first cycles.
- Direct `urllib` calls instead of proper MCP subscriptions — would have been brittle at scale.
- Aesop fable integration was charming but added latency. The fleet now uses direct strategy-formation without narrative middlemen.

## What to Salvage

The `build_field` → `field_to_flux_vector` → `compose_midi_events` pipeline is a **perfect test harness** for the PLATO-NG wheel architecture. Use it as the integration test for the Monitoring Wheel's emergence detector.
