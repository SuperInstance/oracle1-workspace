# 📐 plato-types — The Canonical Foundation

**Status:** Published — zero dependencies  
**Date:** 2026-05-14  
**Wheel:** #79

## What It Is

The **formal canonical type definitions** for the entire PLATO tile protocol. Every PLATO implementation across the fleet references this package for the core data model: tiles, lifecycle states, Lamport clocks, training configuration, and content-addressed storage.

This is the **specification encoded as Python dataclasses** — the single source of truth that all other repos build on.

## Forgotten Gold

### 1. Lifecycle as a State Machine

The `LifecycleEvent` dataclass records **every state transition with causality**:

```python
@dataclass
class LifecycleEvent:
    from_state: TileLifecycle    # What it was
    to_state: TileLifecycle      # What it became
    reason: str                  # Human-readable justification
    timestamp: float             # When it happened
    lamport: int                 # Causal ordering
```

Events form an immutable audit log. A tile that went Active → Superseded → Retracted preserves the full chain. This is the **provenance mechanism** — at any point you can ask "why did this tile die?"

### 2. The `transition()` / `supersede()` / `retract()` Triple

```python
tile.transition(TileLifecycle.SUPERSEDED, "Better model available", lamport=42)
```

Compared to #77's simpler `.supersede(new_tile)` method, this version:
- **Records the full event** (not just state flip)
- **Links successor tiles** via `parent_tile` field
- **Provides `history()`** for audit trail
- **Provides `summary()`** for human-readable output

The `supersede()` method on `TrainingTile` is a **self-modifying reference** — it marks itself superseded AND sets the successor's parent. Two-way linking.

### 3. The `content_hash` Function

```python
def content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]
```

A **16-char hex prefix of SHA-256** — deliberately short for human readability while maintaining near-zero collision risk. This is the content-addressable identifier that ties physical weight bytes to logical tiles without embedding the bytes in the tile metadata.

**Why this matters**: You can verify a tile's content_hash matches the actual weights without loading them. This is the foundation for **trustless verification** across the fleet.

### 4. The `to_dict()` / `from_dict()` Round-Trip

Both #78 and #79 types have `to_dict()` and `from_dict()` classmethods that handle enum serialization, nested dataclass reconstruction, and lifecycle event deserialization. This is the **serialization contract** for the entire PLATO protocol.

Notable details:
- `tile_type` and `state` are serialized as their `.value` strings, not enum instances
- `LifecycleEvent` lists are manually reconstructed (not via simple `asdict`)
- `from_dict()` uses `cls.__dataclass_fields__` filtering to ignore unknown keys

### 5. Comparison: #77 vs #78/#79 Types

| Feature | #77 (early) | #78/#79 (canonical) |
|---|---|---|
| LifecycleEvent | ❌ | ✅ Full events with reason |
| content_hash | ❌ | ✅ SHA-256 16-char prefix |
| `transition()` | ❌ | ✅ Direct state transitions |
| `supersede()` | Sets state only | Records event + links successor |
| `history()` | ❌ | ✅ Full audit chain |
| `loss_curve` in Metrics | ❌ | ✅ List of per-batch losses |
| `serialization` | Basic `asdict` | Enums, events, nested types |
| `plato_room_id` field | ✅ (separate ID) | ❌ (room field suffices) |
| `data_path` field | ✅ (disk path) | ❌ (content_hash replaces) |

The evolution from #77 to #78/#79 shows the protocol maturing: from "a tile has a state" to "a tile is a full provenance chain."

### 6. Used Across the Fleet

```
plato-types  ← plato-training (training rooms)
             ← plato-sdk (PLATO server client)
             ← fleet-memory (distributed memory)
             ← folding-order (anomaly detection)
             ← flux-lucid (intent alignment)
             ← dodecet-encoder (agent lifecycle)
```

This package is the **type system for the entire PLATO ecosystem**. Any change to these types cascades everywhere. The zero-dependency property is intentional — this is designed to be importable in any Python environment without pulling in PyTorch, numpy, or HTTP libraries.

## Why It Matters

This is the **Constitution** — the foundational law that every PLATO entity agrees on. Without `plato-types`, two agents can't agree on whether a tile is Active or what its causal predecessor was. This package is the **Rosetta Stone** of the fleet.

## Integration Points

- plato-ng **must use** plato-types as its type foundation — not fork, not re-implement
- The `TileLifecycle` enum + `LifecycleEvent` + `TrainingTile` is the canonical data model
- If plato-ng needs new tile types, add them HERE, not in plato-ng
- The serialization contract (`to_dict()`/`from_dict()`) should be tested exhaustively in plato-ng's CI
