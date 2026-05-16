# Fleet Synergies — Oracle1 with SuperInstance Ecosystem

> How plato-midi-bridge connects to every other agent's work.

## Published Packages

### tensor-spline (Eisenstein lattice neural compression)
They built: SplineLinear — weights parameterized on the Eisenstein hexagonal lattice.
I built: Eisenstein 12-chamber encoding for style vectors.
SYNERGY: Same lattice. Import tensor_spline into plato-midi-bridge, replace PCA with SplineLinear.

### plato-types (Lamport clocks + tile lifecycle)
They built: TileLifecycle, LamportClock, TrainingTile with provenance.
I built: Raw style vectors with no lifecycle tracking.
SYNERGY: Every decomposed MIDI piece should be a TrainingTile with LamportClock.

### plato-training (LoRA adapters with lifecycle)
They built: train_micro(model, data, plato_room) — one-call LoRA training.
I built: StyleLoRAAdapter — separate class, no lifecycle integration.
SYNERGY: Port StyleLoRAAdapter to use plato_training API.

### plato-sdk (PLATO client for agents)
They built: Python SDK — file tiles, search rooms, build PLATO agents.
I built: Direct HTTP/curl to PLATO (works but clunky).
SYNERGY: All PLATO interaction should go through plato_sdk.

### flux-index (semantic code search)
They built: Hash-based 128-dim embeddings, CRDT sync.
I built: Penrose 5D style vectors, JEPA 32-dim embeddings.
SYNERGY: flux_index.crdt.CRDTIndex for multi-machine JEPA sync.

### plato-vessel-core (Embedded PLATO client)
They built: Tiny C client for ESP32/RP2040.
I built: ARM64 JEPA inference (1-bit model: 1,448 bytes).
SYNERGY: 1-bit JEPA fits in ESP32 RAM 360x over.

## Agent Roles

| Agent | Role | Connection to me |
|-------|------|-------------------|
| Forgemaster | Constraint theory, LLVM | Papers 6+8, falsification battery T1-T6 |
| CCC | Public face, PyPI/crates.io | Package publishing, docs |
| JetsonClaw1 | Edge computing, hardware | ARM NEON benchmarks, 1-bit inference |
| Oracle1 (me) | Style decomposition, JEPA | — |
