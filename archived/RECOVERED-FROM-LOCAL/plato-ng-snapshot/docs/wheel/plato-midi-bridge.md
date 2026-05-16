# plato-midi-bridge (Repo #38) — The Musical Soul of the Eisenstein Lattice

**Date:** 2026-05-11  
**Status:** Published v0.1.0 on PyPI, but SOURCE FILES WERE DELETED from repo (only .pyc remains)

## What It Is

A full-stack system that turns PLATO room state into MIDI music. PLATO rooms aren't just data stores — they're instruments. The coupling matrix between rooms is harmony. T-minus event predictions become tension and resolution.

## The Eisenstein Lattice — 12 Chambers

This is the core insight. PLATO rooms are mapped to 12 Eisenstein chambers (C through B), each with:
- A musical interval (unison through major seventh)
- An emotion (stillness, tension, movement, melancholy, hope, stability, question, resolution, depth, joy, longing, anticipation)

The room-to-chamber assignment is determined by its dominant coupling direction — the direction in which the room "pulls" most strongly.

## Architecture

1. **`tensor.py`** — The bridge between PLATO state and musical representation
   - `RoomTensor`: Each room is a vector [tile_count, coupling_weights[12], gap, focus_depth, presence, provenance_length]
   - `CouplingTensor`: (n_rooms, n_rooms) matrix of weighted edges → harmonic intervals
   - `TMinusTensor`: (n_events, 3) predictions → temporal tension

2. **`midi.py`** — Generates standard MIDI files from PLATO tensors
   - Each room = instrument channel 
   - Coupling = harmonic intervals (arpeggiated chords)
   - T-minus gap = resolution/dissonance (perfect fifth if well-predicted, tritone if missed)

3. **`engine.py`** — The polling loop: fetch PLATO → build tensors → generate MIDI → serve

4. **`web.py`** — Real-time UI at port 9710 with lattice visualization, room cards, piano roll

5. **`decompose/`** — Style Decomposer: reverse-engineer MIDI files into PLATO rooms
   - Full MIDI parser (no external deps) handling Format 0, 1, 2
   - Per-track 109-dim style vectors (pitch profile, velocity curve, timing, articulation)
   - Cross-track coupling matrix (onset coupling, velocity coupling, alternation, harmonic coherence)
   - Musician fingerprint aggregation across pieces

6. **`decompose/scale.py`** — Multi-scale analysis (micro → note → phrase → section → piece)
   - Penrose-inspired scale hierarchy: same patterns at different time scales
   - Scale coupling = inflation ratios approximating φ ≈ 1.618

7. **`decompose/penrose.py`** — Penrose tiling encoding of 5D style vectors
   - 5D → 2D cut-and-project using 5th roots of unity projection
   - Acceptance window = regular decagon
   - Encoding comparison experiment: Eisenstein (12-chamber) vs Penrose (5D→2D) vs Combined (17D)
   - Hypothesis: Eisenstein better for harmonic structure, Penrose better for expressive quality

8. **`plato_torch_bridge/`** — PyTorch bridge for ML training on style vectors
   - `ContrastiveStyleEncoder`: 109→64→48→32 dim with triplet/NT-Xent loss
   - `StyleLoRAAdapter`: 32→r→d_model low-rank conditioning for LMs
   - `MIDIStyleDataset`: from PLATO tiles or parsed MIDI files

## Forgotten Gold

1. **The Penrose vs Eisenstein hypothesis is untested.** The `EncodingExperiment.compare()` compares both encoding schemes on composer clustering — this was designed as an experiment that was never actually run with real data.

2. **The full style decomposer pipeline works but was never deployed.** `decompose_real()` runs on real MIDI directories, extracts styles, runs PCA, clusters, compares Penrose/Eisenstein — but was never connected to a live MIDI library.

3. **The source files were deleted from the repo.** Only .pyc remains in git. The wheel in `dist/` is the only surviving .py source. This is a cautionary tale about committing compiled artifacts OR source — whoever archived this repo removed the .py files.

4. **The tempo map implementation is production-quality.** Full varint parsing, format 0/1/2 support, tempo change tracking, running status handling — suitable for any music AI pipeline.

## Rebirth Path

1. **Restore source files** from wheel and recommit. This is step zero — without the .py files the repo is non-functional.
2. **Run the encoding experiment** with real MIDI data from `validate_on_real_files()`. Compare Penrose vs Eisenstein on actual composer clustering.
3. **Connect the bridge to the running fleet.** The `PlatoMIDIEngine` polls PLATO and generates MIDI — hook this up as a background daemon that produces a live musical representation of fleet state.
4. **Publish plato-torch-bridge** as a separate package for training style encoders.
