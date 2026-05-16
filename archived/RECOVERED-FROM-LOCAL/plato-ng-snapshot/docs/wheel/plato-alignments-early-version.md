# Wheel Rebirth: plato-alignments-early-version

**Repo:** `SuperInstance/plato-alignments-early-version`
**Archived:** 2026-05-13 | **Scaffolding:** ~1KB

## What Was It?

The most complete of the three scaffolding repos. An **alignment artifact system** — capture agent context at a calibrated snap point and store it as a summonable resource. New agents inherit alignment knowledge without retraining.

Core concepts:

- **AlignmentArtifact** — a snapshot of agent context at the moment a calibration triangle converged below threshold. Contains: agent ID, room, full context dict, calibration snapshot (t, w, residual), human-readable description. Content-addressed by SHA-256 of context.
- **AlignmentRegistry** — persistent library of artifacts (JSON on disk). `capture()` stores a snap point. `summon()` loads an artifact into a new agent's context, injecting calibration data. `list_alignments()` surfaces available artifacts by room or tag, sorted by summon count.
- **The Ender's Game principle** — knowledge transfer via inheritance, not training. The demo shows a forge_agent capturing an ARM64 constraint optimization alignment, then a new agent summons it and gets calibrated T, W, and residual injected into their context.

## What Was the Design Intent?

**Context as transferable resource.** Alignment isn't about training — it's about capturing the moment when an agent converges on truth. That moment becomes an artifact that other agents can inherit. The fleet accumulates alignment artifacts like a library of proven configurations. Each successful solve adds to the library.

## Absorbed Into What?

The README explicitly states: "Concept absorbed into plato-sdk." The capture-summon lifecycle is the core of PLATO's knowledge transfer architecture. plato-sdk's alignment system inherits the artifact model, the snapshot data structure, and the summon/replay pattern.

## Why It Matters

This is the bridge between calibration (when to snap) and the semantic field (where to store it). Alignments make calibration useful — without storage and retrieval, a snap point is just a number. This repo turned snap points into legible, summonable artifacts that accumulate fleet intelligence. The demo code is production-grade in concept; the registry/summon pattern is what makes PLATO a learning system rather than a stateless one.
