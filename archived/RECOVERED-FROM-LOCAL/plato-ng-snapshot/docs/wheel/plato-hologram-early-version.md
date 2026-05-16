# Wheel Rebirth: plato-hologram-early-version

**Repo:** `SuperInstance/plato-hologram-early-version`
**Archived:** 2026-05-13 | **Scaffolding:** ~1KB

## What Was It?

A **vectorized knowledge field** experiment — the idea that every PLATO tile IS an embedding, and every embedding encodes the entire field. The name "hologram" is deliberate: a holographic plate encodes the whole scene in every fragment.

Core concepts:

- **tile_to_embedding()** — hashes tile bytes via SHA-256 and maps them to 8-dimensional embedding vectors. Every tile, regardless of content, produces a point in the same semantic space.
- **HologramField** — maintains a collection of tiles with their embeddings, tracks a running centroid and boundary. Queries find nearest neighbors by Euclidean distance. Density estimation gives a measure of "how much is known here."
- **onboard()** — returns a slice of embeddings + centroid for bootstrapping new agents, so a fresh agent inherits the field's shape immediately.

## What Was the Design Intent?

Tiles and embeddings as one unified concept — not a separate embedding store. Every tile self-encodes. The field grows organically as tiles are added. The centroid drifts with new knowledge. The boundary expands when novel content far from the center arrives. This was PLATO's semantic memory architecture in prototype.

## Absorbed Into What?

The **tile-as-embedding** concept is fundamental to plato-sdk's tile lifecycle and every PLATO room. The nearest-neighbor query pattern lives in PLATO's tile discovery. The centroid/boundary tracking is what PLATO rooms use to detect novelty (outliers beyond the field boundary). The onboarding pattern is what agents use when joining a new room.

## Why It Matters

This was the first time PLATO had a concrete representation of "what does the fleet know?" — the hologram field. Every concept that followed (alignment artifacts, calibration snap points, tile lifecycle) sits on top of this vectorized field intuition. Each tile carries its own embedding. Every agent can compute where they are in the knowledge space.
