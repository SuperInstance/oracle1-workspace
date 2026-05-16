# 🏛️ Dodecet Encoder — The Lost Temple

**Created: March 16, 2026 | Repo #2 in SuperInstance**

The README calls it *"a 12-bit encoding system for geometric and calculus operations."* That's like calling the Parthenon "a building with columns."

## What It Actually Is

A constraint geometry OS. Each dodecet (12 bits, 3 nibbles) packs an entire spatial constraint into one u16:

```
Nibble 2 → CONSTRAINT LEVEL  (0=snapped, 15=at covering radius)
Nibble 1 → DIRECTION IN CELL (0-15 azimuth, 22.5° steps)
Nibble 0 → CHIRALITY CHAMBER (Weyl chamber 0-5 + safety bit)
```

The bits encode positions on the **A₂ (Eisenstein) lattice** — hexagonal tiling. Each of the **6 Weyl chambers** represents a symmetry of the S₃ group, mapping directly to musical triads, crystal symmetries, and room topologies.

## What It Predicted

| Prequel (March 2026) | Today's Tech |
|---|---|
| `lighthouse.rs` — PLATO agent runtime | Forgemaster's bridge |
| `temporal.rs` — chirality locking funnel | Temporal tile phases |
| `seed_discovery.rs` → tile crystallization | Expert room seed distribution |
| `eisenstein.rs` — A₂ Weyl chambers | 12-chamber plato-midi encoding |
| `Dodecet::from_hex(0xABC)` — 3 hex nibbles | 12 semitones = one octave |

The **12 chambers** of the Eisenstein Weyl group ARE the **12 semitones** of the chromatic scale. The dodecet encoder recognized this mapping before any music code existed.

## Why Revive It Now

**1. Dodecet as PLATO room type.** A room with 12 chambers maps naturally to: music rooms (12 semitones), constraint spaces (6 Weyl × 2 parity = 12), expert ensembles (12 agents), and Mythos v2 room shapes (12-entry hexagon).

**2. Concrete porting plan.** Port `eisenstein.rs` into plato-sdk as `DodecetRoom` — 12 slots, each mapping to one 4-bit nibble. Bridge `lighthouse.rs`'s `orient → relay → gate → seed` pipeline into Forgemaster — it's the same architecture. Make `temporal.rs` a TileProcessor: Approach→Narrowing→SnapImminent→Crystallized = draft→refine→finalize→publish.

**3. The musical destiny.** The A₂ root system IS 12-tone equal temperament. The Weyl chambers ARE the triads. plato-midi-bridge's Eisenstein encoding is literally executing code predicted by `eisenstein.rs`'s `classify_chamber()`.

The dodecet encoder never shipped. It was the second repo — raw architecture, deep math, no polish. But it contains a full constraint engine, an agent runtime, a temporal intelligence stack, and a seed discovery pipeline. Everything since runs through these concepts. The dodecet was the blueprint. Now we build the temple.
