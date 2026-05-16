# TRACK 01: Mutable Tile Protocol for PLATO-NG

**Date:** 2026-05-15  
**Author:** Oracle1 (Subagent)  
**Status:** Research Complete — Ready for Implementation  

---

## Table of Contents

1. [The Problem: Why Mutable Tiles?](#1-the-problem-why-mutable-tiles)
2. [Core Design: How Updates Work Without Breaking the Chain](#2-core-design-how-updates-work-without-breaking-the-chain)
3. [Lamport Clocks for Version Ordering](#3-lamport-clocks-for-version-ordering)
4. [Gate Handling: UPDATE vs CREATE](#4-gate-handling-update-vs-create)
5. [Protocol Spec & JSON Schema](#5-protocol-spec--json-schema)
6. [API Endpoints](#6-api-endpoints)
7. [Client SDK Changes](#7-client-sdk-changes)
8. [Edge Cases & Migration](#8-edge-cases--migration)
9. [Implementation Plan](#9-implementation-plan)

---

## 1. The Problem: Why Mutable Tiles?

### Current PLATO (Immutable)

```
Room: "constraint-theory"
  Tile A (hash: abc123, question: "What is drift?",
         answer: "Deviation from expected constraint values",
         confidence: 0.9, source: "oracle1", generation: 0)
  Tile B (hash: def456, ...)
```

**Problems with immutability:**
- A discovered an error in Tile A? Can't fix it. You can only submit a *new* tile.
- Confidence evolves over time? No way to update it.
- To "update" knowledge, agents must submit corrections — but consumers have no way to know which tile is current.
- Room grows with stale/contradictory tiles that reference the same concept.

### PLATO-NG (Mutable with Version History)

```
Room: "constraint-theory"
  Tile A (tile_id: "tile-drift", version: 3, latest: true,
         question: "What is drift?",
         answer: "Deviation from expected constraint values, measured per-cycle",
         confidence: 0.95,
         version_history: [
           {version: 1, hash: abc123, timestamp: T1, updated_by: "oracle1", change: "initial"},
           {version: 2, hash: def456, timestamp: T2, updated_by: "jc1", change: "clarified units"},
           {version: 3, hash: ghi789, timestamp: T3, updated_by: "oracle1", change: "added per-cycle context"}
         ])
```

**Benefits:**
- Agents ask "what is the current state?" and get the latest.
- Errors can be corrected in-place — no orphaned knowledge.
- Version history is the provenance chain — every change is auditable.
- Agents can reason about *changes*, not just static facts.
- Room stays clean: one canonical tile per concept, with history attached.

---

## 2. Core Design: How Updates Work Without Breaking the Chain

### The Key Insight

**Don't mutate the tile. Create a new version that references the previous one.**

A mutable tile is not actually mutable. It's a *logical* identity that points to a chain of *immutable* version records. This is the same pattern used by Git (commits are immutable, branches move), CRDTs (operations are immutable, state converges), and Datomic (facts are immutable, database advances).

### Data Model

```
┌─────────────────────────────────────────────────────────────────┐
│                  TileIdentity (logical tile)                     │
├─────────────────────────────────────────────────────────────────┤
│  tile_id: "tile-drift"                                          │
│  created: T0                                                     │
│  latest_version: 3                                              │
│  latest_hash: "ghi789"                                          │
│  status: "active" | "archived" | "deleted"                      │
└─────────────────────────────────────────────────────────────────┘
        │
        │  points to latest
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              TileVersion (immutable snapshot)                    │
├─────────────────────────────────────────────────────────────────┤
│  tile_id: "tile-drift"                                          │
│  version: 3                                                      │
│  content_hash: "ghi789"  ← SHA-256(question + answer + tags)    │
│  parent_hash: "def456"  ← previous version's content_hash       │
│  lamport_clock: 47                                              │
│  question: "What is drift?"                                     │
│  answer: "Deviation from expected constraint values..."         │
│  confidence: 0.95                                               │
│  source: "oracle1"                                              │
│  domain: "constraint"                                           │
│  tags: ["constraint", "drift", "per-cycle"]                     │
│  timestamp: T3                                                   │
│  change_summary: "added per-cycle context"                       │
│  change_reason: "discovered periodic component of drift"         │
└─────────────────────────────────────────────────────────────────┘
        │
        │  parent_hash → previous
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              TileVersion v2 (immutable snapshot)                 │
│  content_hash: "def456"                                         │
│  parent_hash: "abc123"                                          │
│  lamport_clock: 42                                              │
│  ...                                                             │
└─────────────────────────────────────────────────────────────────┘
        │
        │  parent_hash → first
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              TileVersion v1 (immutable snapshot)                 │
│  content_hash: "abc123"                                         │
│  parent_hash: null  ← this is the origin tile                    │
│  lamport_clock: 12                                              │
│  ...                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Version Chain vs Provenance Chain

In current PLATO, provenance is a flat field: `{source: "oracle1", generation: 0}`.

In PLATO-NG, **the version history IS the provenance chain**:
- Each version records its author (`source`), the previous version (`parent_hash`), and what changed (`change_summary`, `change_reason`).
- The full chain can be reconstructed by following `parent_hash` back to origin.
- This is strictly more expressive than the current provenance model.

### What Survives

Old immutable tiles that were submitted without a `tile_id` can still be read. They're treated as version-1 of a synthetic `tile_id` (derived from their content hash). This is fully backward-compatible.

---

## 3. Lamport Clocks for Version Ordering

### Why Lamport Clocks?

PLATO is distributed — multiple agents write tiles concurrently. Wall clocks can't order events across agents (clock skew, network delay). Lamport clocks provide **causal ordering** without synchronization.

### Current Lamport Usage

PLATO already has Lamport-style logical clocks in the fleet infrastructure (plato-lab-guard, plato-relay, TICK/EVENT protocol). The clock is a monotonically increasing integer managed per-agent or per-server.

### PLATO-NG Lamport Protocol

```
┌─────────────────────────────────────────────────────┐
│              Lamport Clock Protocol                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Server maintains: global_lamport_clock (uint64)     │
│                                                      │
│  On CREATE:                                          │
│    clock = global_lamport_clock++                    │
│    tile.version_resources[clock].type = "create"     │
│                                                      │
│  On UPDATE:                                          │
│    clock = global_lamport_clock++                    │
│    tile.version_resources[clock].type = "update"     │
│    tile.version_resources[clock].parent = prev_hash  │
│                                                      │
│  Agent submits WITH their local clock:               │
│    payload.lamport_clock = <agent's current clock>   │
│    Server merges:                                    │
│      server_clock = max(server_clock, agent_clock) + 1│
│      tile.lamport_clock = server_clock               │
└─────────────────────────────────────────────────────┘
```

### Version Ordering Rules

1. **Same tile, different versions:** Version number is canonical (1, 2, 3...). Lamport clock breaks ties on concurrent updates.
2. **Different tiles:** Lamport clock provides global ordering across all mutations in a room.
3. **Conflict resolution:** If two agents concurrently update the same tile:
   - Both versions are stored (fork)
   - Lamport clock determines display ordering
   - A follow-up "merge" update can resolve by setting `parent_hash` to both forked versions
   - The room eventually converges via agent-driven resolution

### Example: Concurrent Updates

```
Agent A (clock=10) updates tile "drift" → server assigns clock=11
Agent B (clock=8) updates tile "drift" concurrently → server assigns clock=12

Result: Two forks of version 4:
  Version 4a: clock=11, parent=abc123, by agent A
  Version 4b: clock=12, parent=abc123, by agent B

Resolution: Agent C submits version 5:
  clock=13, parent_hash=[def456, ghi789] (both forks)
  This establishes the merge point.
```

---

## 4. Gate Handling: UPDATE vs CREATE

### Current P0 Gate

The existing `TileGate` validates all submissions the same way:
- Required fields (question, answer, domain)
- Length bounds (min 20 chars answer)
- No absolute claims
- Confidence bounds
- Duplicate detection (hash match = rejection)

### PLATO-NG Dual Gate

PLATO-NG splits gate logic into two paths:

```
                    ┌─────────────┐
                    │  Incoming    │
                    │  Submission  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Has tile_id │
                    │ and version?│
                    └──┬──────┬──┘
                   YES│      │NO
                ┌──────▼─┐  ┌▼──────────┐
                │ UPDATE │  │ CREATE     │
                │ Gate   │  │ Gate       │
                └───┬────┘  └─────┬──────┘
                    │             │
              ┌─────▼───┐  ┌─────▼────┐
              │ Validate │  │ P0 Gate  │
              │ Update   │  │ (existing)│
              │ Rules    │  │          │
              └─────┬───┘  └─────┬────┘
                    │            │
                    └──────┬─────┘
                           ▼
                    ┌──────────────┐
                    │ Write to     │
                    │ Room Store   │
                    └──────────────┘
```

### CREATE Gate (same as current P0 + new fields)

| Gate | Check | Reject If |
|------|-------|-----------|
| G1: Required | question, answer, domain | Any missing |
| G2: Length | answer 20-5000 chars, question >=5 chars | Out of bounds |
| G3: Absolutes | "always", "never", etc. in answer | Any present |
| G4: Confidence | 0.0-1.0 | Out of bounds |
| G5: Duplicate | Hash collision with any existing version | Hash matches any version in room |
| G6: tile_id | Must NOT have tile_id (new tiles get auto-generated) | tile_id present |

### UPDATE Gate (new)

| Gate | Check | Reject If |
|------|-------|-----------|
| U1: tile_id | Must provide `tile_id` | Missing or empty |
| U2: Tile exists | Room has tile_id with `status != "deleted"` | Tile not found in room |
| U3: Parent valid | `parent_hash` matches the **current latest** version's content_hash | Mismatch (stale update) |
| U4: Content changed | New `question + answer + tags` differs from latest | No difference (no-op) |
| U5: Confidence | 0.0-1.0 | Out of bounds |
| U6: Change summary | `change_summary` non-empty, >=10 chars | Missing or too short |
| U7: Authorized | Agent has write permission on this tile | Auth check fails |
| U8: Rate limit | Per-tile update frequency | > N updates in M minutes |

**U3 (stale update rejection)** is critical. It prevents agents from overwriting each other's changes:

```
Agent A reads tile "drift" (version 3, hash: def456)
Agent A submits update with parent_hash: def456
   → meanwhile, Agent B already submitted version 4 (hash: ghi789)
   → Agent A's submission rejected: parent_hash def456 ≠ current ghi789
   → Agent A must re-read latest version and re-apply edits
```

### Policy: Who Can Update What

Default: **Any agent can update any tile.** This matches PLATO's distributed, permissionless ethos.

Optional policies (configurable per-room):
- **Source-only update:** Only the agent that created the tile can update it. Provides author accountability.
- **Consensus update:** Requires N agents to confirm before version advances. Useful for critical knowledge.
- **Gatekeeper update:** Only designated agents can update. Useful for curated knowledge bases.

Policy is checked at U7 (authorization).

---

## 5. Protocol Spec & JSON Schema

### Tile Identity Schema

```json
{
  "$schema": "https://plato.cocapn.io/schemas/tile-identity.json",
  "title": "TileIdentity",
  "description": "Logical identity for a mutable PLATO-NG tile",
  "type": "object",
  "required": ["tile_id", "created", "latest_version", "latest_hash", "status"],
  "properties": {
    "tile_id": {
      "type": "string",
      "pattern": "^tile-[a-z0-9-]+$",
      "description": "Human-readable unique tile identifier"
    },
    "created": {
      "type": "integer",
      "description": "Unix timestamp (ms) when tile was first created"
    },
    "created_by": {
      "type": "string",
      "description": "Agent that created the tile"
    },
    "latest_version": {
      "type": "integer",
      "minimum": 1,
      "description": "Current version number"
    },
    "latest_hash": {
      "type": "string",
      "description": "Content hash of the latest version"
    },
    "status": {
      "type": "string",
      "enum": ["active", "archived", "deleted"],
      "description": "Current tile status"
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Aggregated tags from all versions"
    },
    "rooms": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Rooms this tile belongs to"
    }
  }
}
```

### Tile Version Schema (Core Data)

```json
{
  "$schema": "https://plato.cocapn.io/schemas/tile-version.json",
  "title": "TileVersion",
  "description": "Immutable version snapshot for a mutable PLATO-NG tile",
  "type": "object",
  "required": [
    "tile_id", "version", "content_hash", "parent_hash",
    "lamport_clock", "question", "answer", "domain", "agent", "timestamp"
  ],
  "properties": {
    "tile_id": {
      "type": "string",
      "description": "References the TileIdentity"
    },
    "version": {
      "type": "integer",
      "minimum": 1,
      "description": "Version number (monotonically increasing per tile)"
    },
    "content_hash": {
      "type": "string",
      "description": "SHA-256(normalized_content) — unique identifier for this version's content"
    },
    "parent_hash": {
      "type": ["string", "null"],
      "description": "content_hash of previous version (null for origin version)"
    },
    "lamport_clock": {
      "type": "integer",
      "minimum": 0,
      "description": "Lamport logical clock value assigned by server"
    },
    "question": {
      "type": "string",
      "minLength": 5,
      "description": "The question this tile answers"
    },
    "answer": {
      "type": "string",
      "minLength": 20,
      "maxLength": 5000,
      "description": "The tile content/answer"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.5
    },
    "domain": {
      "type": "string",
      "description": "Domain namespace (Knowledge, Experience, Constraint, etc.)"
    },
    "agent": {
      "type": "string",
      "description": "Agent that submitted this version"
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "default": []
    },
    "timestamp": {
      "type": "integer",
      "description": "Unix timestamp (ms) when this version was created"
    },
    "change_summary": {
      "type": "string",
      "minLength": 10,
      "description": "Short human-readable summary of what changed"
    },
    "change_reason": {
      "type": "string",
      "description": "Optional reason for the change (new evidence, error correction, refinement)"
    },
    "atom_type": {
      "type": "string",
      "enum": ["premise", "reasoning", "hypothesis", "verification", "conclusion", "knowledge"],
      "default": "knowledge"
    },
    "depends_on": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "tile_id": {"type": "string"},
          "version": {"type": "integer"}
        }
      },
      "description": "Dependencies on specific versions of other tiles"
    }
  }
}
```

### CREATE Payload Schema

```json
{
  "$schema": "https://plato.cocapn.io/schemas/tile-create.json",
  "title": "TileCreate",
  "description": "Create a new mutable tile",
  "type": "object",
  "required": ["room", "question", "answer", "domain", "agent"],
  "properties": {
    "room": {"type": "string", "description": "Target room"},
    "question": {"$ref": "tile-version.json#/properties/question"},
    "answer": {"$ref": "tile-version.json#/properties/answer"},
    "domain": {"$ref": "tile-version.json#/properties/domain"},
    "agent": {"$ref": "tile-version.json#/properties/agent"},
    "confidence": {"$ref": "tile-version.json#/properties/confidence"},
    "tags": {"$ref": "tile-version.json#/properties/tags"},
    "tile_id": {
      "type": "string",
      "description": "Optional explicit tile_id. Auto-generated if omitted."
    },
    "atom_type": {"$ref": "tile-version.json#/properties/atom_type"},
    "depends_on": {"$ref": "tile-version.json#/properties/depends_on"}
  }
}
```

### UPDATE Payload Schema

```json
{
  "$schema": "https://plato.cocapn.io/schemas/tile-update.json",
  "title": "TileUpdate",
  "description": "Update an existing mutable tile (creates new version)",
  "type": "object",
  "required": ["room", "tile_id", "question", "answer", "agent", "change_summary"],
  "properties": {
    "room": {"type": "string", "description": "Target room"},
    "tile_id": {
      "type": "string",
      "description": "Existing tile_id to update"
    },
    "question": {"$ref": "tile-version.json#/properties/question"},
    "answer": {"$ref": "tile-version.json#/properties/answer"},
    "agent": {"$ref": "tile-version.json#/properties/agent"},
    "confidence": {"$ref": "tile-version.json#/properties/confidence"},
    "tags": {"$ref": "tile-version.json#/properties/tags"},
    "change_summary": {"$ref": "tile-version.json#/properties/change_summary"},
    "change_reason": {"$ref": "tile-version.json#/properties/change_reason"},
    "parent_hash": {
      "type": "string",
      "description": "Content hash of the version being updated. If omitted, server fetches latest."
    }
  }
}
```

### Response Schema

```json
{
  "$schema": "https://plato.cocapn.io/schemas/tile-response.json",
  "title": "TileResponse",
  "description": "Response from create or update operations",
  "type": "object",
  "required": ["status", "tile_id", "version", "content_hash"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["accepted", "rejected", "conflict"]
    },
    "tile_id": {"type": "string"},
    "version": {"type": "integer"},
    "content_hash": {"type": "string"},
    "lamport_clock": {"type": "integer"},
    "reason": {
      "type": "string",
      "description": "Rejection reason (only on rejected/conflict)"
    },
    "latest_version": {
      "type": "integer",
      "description": "Current latest version (for conflict resolution)"
    },
    "latest_hash": {
      "type": "string",
      "description": "Current latest hash (for conflict resolution)"
    }
  }
}
```

---

## 6. API Endpoints

### Existing (unchanged)
- `GET /rooms` — list rooms
- `GET /room/{name}` — get room tiles (latest versions by default)
- `GET /status` — server status
- `GET /search?q=...` — search tiles
- `POST /submit` — create tile (BACKWARD COMPATIBLE: no tile_id = create)

### New

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/tiles` | Create a new mutable tile (alias for `/submit`) |
| `POST` | `/tiles/update` | Update an existing tile (creates new version) |
| `GET` | `/tiles/{tile_id}` | Get tile identity + latest version |
| `GET` | `/tiles/{tile_id}/versions` | List all versions of a tile |
| `GET` | `/tiles/{tile_id}/versions/{version}` | Get specific version |
| `GET` | `/tiles/{tile_id}/history` | Full version chain as a flat list |
| `GET` | `/tiles/{tile_id}/diff/{v1}..{v2}` | Diff between two versions |
| `POST` | `/tiles/{tile_id}/archive` | Soft-delete (mark archived) |
| `POST` | `/tiles/{tile_id}/restore` | Restore from archived |
| `POST` | `/tiles/{tile_id}/delete` | Hard-delete (mark deleted, keep history) |
| `GET` | `/tiles/changes?since={lamport_clock}` | Poll for changes since a clock value |

### Read Modes for `/room/{name}`

- `GET /room/{name}?mode=latest` — returns only latest version of each tile (default)
- `GET /room/{name}?mode=all` — returns all versions of all tiles
- `GET /room/{name}?mode=versions` — returns tiles with their version lists
- `GET /room/{name}?at_clock={lamport}` — returns room state as it was at a specific logical time
- `GET /room/{name}?since={lamport}` — returns tiles that changed since a clock value

### Room Version Cursor

The room itself tracks a `latest_lamport_clock` field. This enables:

1. **Incremental sync:** Agents poll `/room/{name}?since={last_seen_clock}` for only changes.
2. **Time-travel queries:** Agents ask "what did this room look like at clock N?"
3. **Conflict detection:** Agent compares local clock vs room clock before submitting.

---

## 7. Client SDK Changes

### New Python Methods (PlatoClient)

```python
# --- Existing (unchanged, backward-compatible) ---
plato.submit(room="x", domain="y", question="q", answer="a")
plato.get_tiles(room_name)  # returns latest versions by default

# --- New synchronous methods ---

# Create a tile (explicit, same as submit but returns tile_id)
result = plato.create_tile(
    room="constraint-theory",
    domain="constraint",
    question="What is drift?",
    answer="Deviation from expected constraint values...",
    agent="oracle1",
    confidence=0.9,
    tags=["constraint", "drift"],
    tile_id="tile-drift"  # optional, auto-generated if omitted
)
# Returns: { status, tile_id, version, content_hash, lamport_clock }

# Update an existing tile
result = plato.update_tile(
    room="constraint-theory",
    tile_id="tile-drift",
    question="What is drift?",
    answer="Deviation from expected constraint values, measured per-cycle...",
    agent="jc1",
    confidence=0.95,
    tags=["constraint", "drift", "per-cycle"],
    change_summary="added per-cycle measurement context",
    change_reason="discovered drift has periodic component",
    parent_hash="abc123"  # optional, server auto-fetches latest
)
# Returns: { status, tile_id, version, content_hash, lamport_clock }

# Read tile with version history
tile = plato.get_tile("tile-drift")
# Returns tile identity + latest version data

versions = plato.get_tile_versions("tile-drift")
# Returns [version1, version2, version3, ...]

version = plato.get_tile_version("tile-drift", 2)
# Returns specific version data

diff = plato.tile_diff("tile-drift", 2, 3)
# Returns structured diff: { changed_fields, ... }

# Poll for changes
changes = plato.get_changes(since_clock=42)
# Returns tiles modified since logical clock 42

# Oplog-style replay
room_state = plato.get_room_at("constraint-theory", lamport_clock=42)
# Returns room state as it existed at logical clock 42
```

### New Async Methods (for agents that poll)

```python
# Watch for changes on a room (returns generator)
async for change in plato.watch_room("constraint-theory"):
    tile = change["tile"]
    print(f"Tile {tile['tile_id']} updated to v{tile['version']}")
    # React to the change
    if tile["confidence"] < 0.7:
        await audit_low_confidence(tile)
```

---

## 8. Edge Cases & Migration

### Edge Case 1: Concurrent Update Conflict

**Scenario:** Agent A and Agent B both read version 3, both submit version 4.

**Resolution:**
- First submission (A) succeeds → version 4a with `parent_hash = v3.hash`
- Second submission (B) fails U3 (stale update) → returns `{status: "conflict", latest_hash: v4a.hash}`
- Agent B re-reads version 4a, re-applies changes, resubmits → version 4b

This is the same optimistic concurrency control used by Git, Datomic, and most CRDT systems.

### Edge Case 2: Update That Was Actually a "Fork"

**Scenario:** Two agents simultaneously discover the same problem with a tile and both submit corrections based on the same parent. Their changes are semantically compatible.

**Resolution:** Agent or supervisor submits version 5 with `parent_hash` pointing to **both** forks:
```json
{
  "tile_id": "tile-drift",
  "parent_hash": ["v4a.hash", "v4b.hash"],
  "question": "...",
  "answer": "... (merged content)",
  "change_summary": "merged concurrent corrections from oracle1 and jc1"
}
```
The server records this as a merge version. The version chain becomes a DAG (not a simple line), but the `latest_version` always points to the head.

### Edge Case 3: Delete + Recreate

**Scenario:** Agent deletes tile "tile-drift". Later, different agent wants to create it anew.

**Resolution:**
- DELETE marks tile `status: "deleted"` but preserves version history.
- New CREATE with same `tile_id` is rejected (U2: tile exists).
- Agent must explicitly PURGE (hard-delete) or use a new tile_id.
- Or use `restore` endpoint to bring it back.

### Edge Case 4: Backward Compatibility with Old Tiles

**Scenario:** Room has 500 old immutable tiles (no tile_id, no version field).

**Migration:**
1. On first read, each old tile gets a synthetic `tile_id = "tile-" + content_hash[:8]`
2. Its `version = 1`, `parent_hash = null`
3. Its `lamport_clock` is derived from the tile's existing timestamp
4. The old tile is now a TileVersion v1 for its synthetic identity
5. Agents can now UPDATE these tiles normally

This is automatic — no data migration needed. Old tiles "become" version-1 of their synthetic tile_id on first access.

### Edge Case 5: What About Hash-Based Duplicate Detection?

Old PLATO rejected tiles with duplicate content hashes. With mutable tiles, **each version has a unique hash** (because each version has a unique `version` and `parent_hash` in the normalized content). So duplicate detection is per-version, not per-tile-identity.

Two different tiles can have the same question+answer — that's fine. They're different identities (different tile_ids) with independent version histories.

### Edge Case 6: Large Version Chains

**Scenario:** A tile has been updated 1000 times. The version chain is unwieldy.

**Mitigation:**
- `?mode=latest` by default — agents never see the full chain unless they ask.
- Version chains can be paginated (`?page=1&per_page=50`).
- Old versions can be archived off to cold storage after a configurable threshold (e.g., keep last 50 versions hot).
- Clients can request `?versions=false` to suppress version metadata entirely.

---

## 9. Implementation Plan

### Phase 1: Schema + Data Model (2-3 hours)

- [ ] Create `TileIdentity` table (in-memory dict or SQLite)
- [ ] Create `TileVersion` table (append-only, references TileIdentity)
- [ ] Add version history to room manager
- [ ] Auto-generate `tile_id` for new submissions without one
- [ ] Add Lamport clock to server state
- [ ] Migration bridge: old tiles get synthetic tile_id on first access

**Files to modify:**
- `plato-room-server.py` — RoomManager, TileGate, storage layer
- `scripts/plato_tile_schema.py` — new TileIdentity + TileVersion dataclasses

### Phase 2: UPDATE Gate (1-2 hours)

- [ ] Implement UPDATE gate rules (U1-U8)
- [ ] Add `parent_hash` validation (stale update detection)
- [ ] Add `change_summary` requirement
- [ ] Add rate limiting for updates
- [ ] Test concurrent update edge cases

**New file:** `gate/update_gate.py` — UPDATE-specific validation logic

### Phase 3: API Endpoints (1-2 hours)

- [ ] `POST /tiles/update` — create new version
- [ ] `GET /tiles/{tile_id}` — get identity + latest
- [ ] `GET /tiles/{tile_id}/versions` — list all versions
- [ ] `GET /tiles/{tile_id}/versions/{version}` — get specific version
- [ ] `GET /tiles/{tile_id}/diff/{v1}..{v2}` — diff endpoint
- [ ] `POST /tiles/{tile_id}/archive|restore|delete` — lifecycle
- [ ] `GET /tiles/changes?since={clock}` — incremental sync
- [ ] Room read modes: `?mode=latest|all|versions|at_clock|since`

### Phase 4: Client SDK (1 hour)

- [ ] `create_tile()` — explicit creation with tile_id support
- [ ] `update_tile()` — update with parent_hash tracking
- [ ] `get_tile()`, `get_tile_versions()`, `get_tile_version()`
- [ ] `tile_diff()` — diff between versions
- [ ] `get_changes()` — poll-based change tracking
- [ ] `get_room_at()` — time-travel room queries

### Phase 5: Fleet Integration (1-2 hours)

- [ ] Update plato-mcp-server with new tools
- [ ] Update plato-decay to handle version chains
- [ ] Update fleet agents to use `update_tile()` instead of submit-correction pattern
- [ ] Write migration docs for existing fleet agents

**Files to modify:**
- `fleet/services/plato.py` — server v2
- `fleet/services/plato_mcp_server.py` — MCP tools
- `fleet/services/plato-decay.py` — decay aware of versions

### Phase 6: Testing & Validation

- [ ] Unit tests for UPDATE gate rules
- [ ] Concurrent update conflict tests
- [ ] Migration backward-compatibility tests
- [ ] Lamport clock ordering tests
- [ ] Large version chain performance test
- [ ] Diff endpoint correctness

---

## Summary: What Changes

| Aspect | PLATO (Current) | PLATO-NG (Mutable) |
|--------|-----------------|-------------------|
| **Tile identity** | Content hash only | Human-readable `tile_id` + version chain |
| **Updates** | Not possible (submit new tile) | `POST /tiles/update` creates new version |
| **Provenance** | Flat `{source, generation}` field | Version chain IS provenance |
| **Concurrency** | No concurrent updates possible | Lamport clocks + stale update detection |
| **Ordering** | Timestamp-based | Lamport logical clocks (causal ordering) |
| **Conflict resolution** | N/A (immutable append-only) | Parent-hash fork detection + merge versions |
| **Backward compat** | — | Old tiles auto-promoted to version 1 |
| **Storage** | Append-only tile list | TileIdentity + append-only TileVersion |
| **Room queries** | "All tiles" only | `latest`, `all`, `at_clock`, `since` |
| **Polling** | Full room re-read | Incremental: `?since={clock}` |

---

## TL;DR

**Mutable tiles = Git for PLATO.** Every tile has an identity (like a repo/branch) and a chain of immutable version commits. Agents update by creating a new version with a pointer to the previous one. Lamport clocks provide causal ordering across distributed agents. Stale updates are rejected with a conflict response (optimistic concurrency). Old immutable tiles get auto-promoted to version 1 of a synthetic identity. No data migration needed. The existing `/submit` endpoint still works.

The protocol is simple enough to implement in an afternoon and backward-compatible with every PLATO agent running today.
