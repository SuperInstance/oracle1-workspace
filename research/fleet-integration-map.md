# Cycle 8

# Weaver Integration Map — Plato-Torch, Fleet-Simulator, Holodeck-Rust, Plato-Ensign

**Cycle:** 8  
**Phase:** 2 — Analyze & Document  
**Status:** Completed mapping of current connections and gaps between four core fleet technologies.

---

## 1. Plato-Torch (Training Rooms)
**Purpose:** Provides 25 preset training rooms and self‑training rooms for agent skill development.  
**Key Files:** `DeadbandRoom` preset, `plato_torch/rooms/`, `plato_torch/tests/`.  
**Current Connections:**
- **To Plato‑Ensign:** Direct. `plato‑ensign` exports room experience (accumulated tiles) into LoRA adapters. This is a primary data flow: rooms train → tiles accumulate → ensigns export.
- **To Fleet‑Simulator:** Indirect via shared tile format. The simulator generates synthetic training data (agent interactions) that can be ingested as tiles into a Plato‑Torch room.
- **To Holodeck‑Rust:** No direct connection observed. Holodeck is a sentiment‑aware MUD server; its NPC interactions are not currently wired as a tile source for Plato‑Torch rooms.

## 2. Fleet‑Simulator (Training Data Generator)
**Purpose:** Generates simulated fleet‑interaction data for training.  
**Key Files:** `fleet‑simulator/src/`, `fleet‑simulator/examples/`.  
**Current Connections:**
- **To Plato‑Torch:** One‑way data feed. The simulator can produce tile‑compatible JSON that could be loaded into a room. No observed real‑time streaming integration.
- **To Holodeck‑Rust:** No observed connection. The simulator focuses on fleet‑agent patterns, not MUD‑style NPC sentiment.
- **To Plato‑Ensign:** Indirect. If simulator data is ingested into a room, that room’s exported ensign would inherit simulated patterns.

## 3. Holodeck‑Rust (Sentiment‑Aware MUD Server)
**Purpose:** Multi‑user dungeon server with NPCs that react to player sentiment.  
**Key Files:** `holodeck‑rust/src/`, `holodeck‑rust/protocol/`.  
**Current Connections:**
- **To Plato‑Torch:** None. NPC‑player interactions are not currently captured as training tiles.
- **To Fleet‑Simulator:** None. Different domains (social RPG vs. fleet‑agent simulation).
- **To Plato‑Ensign:** None. No evidence that holodeck sessions are exported as adapters.

## 4. Plato‑Ensign (LoRA Adapter Exporter)
**Purpose:** Exports a room’s accumulated experience into a lightweight LoRA adapter for specialist models.  
**Key Files:** `plato‑ensign/src/export.rs`, `plato‑ensign/config/`.  
**Current Connections:**
- **To Plato‑Torch:** Primary. Direct dependency; reads room state and tile history to produce adapters.
- **To Fleet‑Simulator:** Indirect, as noted above.
- **To Holodeck‑Rust:** None.

---

## Integration Gaps (What’s Not Connected)

1. **Holodeck‑Rust → Plato‑Torch:** Social NPC interactions are a rich source of training tiles (sentiment, dialogue, player choices). Currently isolated.
2. **Real‑time tile streaming:** Fleet‑simulator and holodeck could stream tiles to a live room, but current flow appears file‑based or batch‑oriented.
3. **Ghost‑tile injection:** The `GhostInjector` (from memory files) is not wired into holodeck or the simulator—dead agents’ P0 lessons remain static.
4. **DeadbandRoom → plato‑relay:** The DeadbandRoom preset does not yet broadcast its state to the fleet’s relay system for live monitoring.

---

## Recommended Wiring (Backlog Items)

1. **Wire GhostInjector into holodeck:** Inject ghost tiles as NPC memory fragments.
2. **Connect DeadbandRoom to plato‑relay:** Enable real‑time fleet oversight of training.
3. **Add holodeck tile‑exporter:** Capture NPC‑player exchanges as tiles for room ingestion.
4. **Test end‑to‑end pipeline:** Simulator → Room → Ensign → Deployed adapter.

---

**Tile submitted:** Integration map of four core technologies with identified connections and gaps.  
**Next action:** Begin wiring GhostInjector into holodeck‑rust (backlog item 1).