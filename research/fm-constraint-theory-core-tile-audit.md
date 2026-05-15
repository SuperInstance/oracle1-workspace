# FM constraint-theory-core + PLATO Tile Audit

## Source: /home/ubuntu/.openclaw/workspace/repos/constraint-theory-core/

## What FM's Tile is (vs PLATO's Tile)

FM's Tile is a **384-byte geometric computation unit** — not a knowledge unit:

```
Tile (384 bytes, cache-line aligned)
├── Origin (64 bytes) — SO(3) rotation matrix + rate of change
│   └── id, reference_frame[3x3], rate_of_change[3]
├── input/output (16 bytes) — u64 each
├── confidence (f32) — Phi cascade score
├── safety (u32) — Sigma predicate
├── bytecode_ptr, trace (16 bytes) — execution pointers
├── tensor_payload[16] (64 bytes) — 16 floats for geometric data
├── provenance_head (u32)
├── self_play_gen (u16)
├── hydraulic_flux (f32)
└── ConstraintBlock (192 bytes)
    ├── snap_target[3] — Pythagorean snap target (a,b,c)
    ├── holonomy_matrix[3x3] — SO(3) transport
    ├── holonomy_norm — gauge-invariant phase
    ├── ricci_curvature[4x4] — curvature tensor
    ├── ricci_scalar
    ├── rigid_cluster_id, percolation_p
    ├── gluing_map, gluing_status
    ├── lvq_codebook_idx, omega_density
    └── persistence_hash
```

This is a **physics simulation / constraint satisfaction tile** — computing on manifolds, checking holonomy around cycles, Riccier curvature. It's not a knowledge representation tile.

## What PLATO's Tile is

PLATO's tile is a **knowledge unit**:
- content: string (the knowledge text)
- source: string (who wrote it)
- type: string (claim, fact, tool, etc.)
- room: string (topic room)
- confidence: float (0-1)
- reinforcement_count: int

**They are completely different abstractions.** FM's Tile is for geometric constraint solving. PLATO's Tile is for knowledge graph traversal.

## What CAN bridge them

The `PythagoreanQuantizer` in constraint-theory-core is the most PLATO-adjacent piece:

- **Ternary mode**: {-1, 0, 1} — could map to tile types (fact=1, claim=0, counter=-1)
- **Polar mode**: preserves unit norm exactly — could map to confidence normalization
- **Turbo mode**: near-optimal distortion — could map to lossy knowledge compression
- **Hybrid mode**: auto-selects based on input characteristics — could map to tile type detection

The snap-to-Pythagorean approach to exactness is philosophically aligned with PLATO's "quality gates reject uncertain tiles" — both are about landing on exact, trustable values.

## Key integration point: snap_target

The `snap_target: [f32; 3]` in FM's ConstraintBlock represents the Pythagorean triple (a,b,c) to snap to. This is the constraint target. If PLATO tiles had a `snap_target` field, the semantic compiler could use FM's quantizer to snap tile content to canonical forms — turning fuzzy knowledge into exact constraints.

## What's missing

1. FM's papers are still local — the 3 arXiv papers (FLUX ISA, PLATO quality gates, Reverse Actualization) haven't been pushed to GitHub
2. There's no `plato-tile-quantizer` bridge — someone needs to wire FM's Pythagorean snapping to PLATO's tile encoding
3. The constraint-theory-core crate is standalone — it doesn't know about PLATO rooms or the keeper

## Next concrete step

Write a `tile_quantizer.rs` that:
- Takes a PLATO tile content string
- Maps it through the quantizer (Ternary for classification, Polar for normalization)
- Outputs a snap_target that can be stored in the tile's metadata
- The semantic compiler then uses this snap_target to route tiles through constraint-theory-core's solver

This would let FM's constraint algebra run on PLATO knowledge, not just geometric vectors.
