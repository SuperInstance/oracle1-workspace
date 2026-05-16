# PLATO↔Glue Sync Audit

## Context
FM's cocapn-glue-core includes PLATO sync built into the wire protocol:
- Snapshot / Delta / Invalidate messages
- Monotonic generations (no rollback)
- Merkle provenance over verification traces
- Wire format: binary postcard (not JSON over HTTP)

PLATO room server: running at localhost:8847
- HTTP JSON API: GET /rooms, POST /rooms/{room}/tiles
- Rooms have tiles, tiles have content/source/type/confidence/reinforcement_count

## Current PLATO sync model

```
Client → HTTP POST /rooms/{room}/tiles
Body: { "content": "...", "source": "...", "type": "..." }
Response: tile ID

Client → HTTP GET /rooms/{room}/tiles
Response: { "tile_id": { "content": "...", "source": "...", ... } }
```

**Gaps vs glue's requirements**:
- No monotonic generations (no ordering guarantee, rollback possible)
- No Merkle chain over tiles
- No Snapshot/Delta/Invalidate (no incremental sync)
- No binary format (JSON over HTTP is text-heavy, slow on MCU)
- No TierId awareness (all clients same tier)

## How PLATO maps to glue's sync messages

| PLATO concept | Glue message | Fit? |
|-------------|-------------|------|
| Room = tile namespace | Snapshot has room-level granularity | ✅ |
| Tile = content unit | Delta carries individual tile ops | ✅ |
| Reinforcement count | Generation number (monotonic) | ✅ (different semantics) |
| No rollback | Monotonic generations | ✅ (PLATO already this way) |
| Content string | Binary-encoded payload | ⚠️ (encoding mismatch) |
| No provenance | Merkle chain over traces | ❌ (PLATO has no provenance tracking) |

## Can we run PLATO over glue transport?

**Yes, but it requires a translation layer.** PLATO's HTTP API cannot be replaced directly — the wire formats are incompatible (JSON vs postcard binary). A glue-to-PLATO bridge is needed.

```
glue wire (postcard binary)
    ↓ parse
glue PlatoSyncPayload (Snapshot/Delta/Invalidate)
    ↓ translate
PLATO HTTP JSON
    ↓ forward
PLATO room server (localhost:8847)
```

OR a full replacement:
```
glue wire (postcard binary)
    ↓ parse
glue PlatoSyncPayload
    ↓ directly apply to
PLATO tile store (replaces HTTP server)
    ↓
Binary PLATO at new port (e.g., 8848)
```

## Minimum viable bridge (Option A — incremental)

A `glue_plato_bridge.py` that:
1. Listens on glue multicast socket for PlatoSyncPayload messages
2. Parses Delta messages (tile create/update/delete)
3. Translates to PLATO HTTP API calls
4. Forwards to localhost:8847

This keeps the PLATO server unchanged. Only the transport changes for remote agents.

**Pros**: No changes to PLATO server itself
**Cons**: Still uses HTTP internally, glue Merkle provenance not enforced at PLATO level

## Full replacement (Option B — clean slate)

Replace PLATO's HTTP API with glue wire protocol as the transport. PLATO server becomes a binary service at a new port. HTTP API deprecated.

**Pros**: Full Merkle provenance, monotonic generations, binary efficiency
**Cons**: Rewrites PLATO server, breaks all existing PLATO clients (including current Oracle1)

## Performance implications

| Metric | Current HTTP | Over glue |
|--------|-------------|-----------|
| Tile write latency | ~5ms (local) | ~1ms (binary, no JSON parse) |
| Snapshot download | JSON parse O(n) | postcard decode O(n) but faster |
| Incremental sync | Full room reload | Delta messages only |
| MCU compatibility | No (JSON/HTTP too heavy) | Yes (no_std glue) |
| Merkle per tile | No | Yes |

## Recommendation

**Do Option A first (minimum viable bridge)**:
- Write `glue_plato_bridge.py`
- Keep PLATO server unchanged at 8847
- New agents (FM's Rust agents) use glue wire
- Bridge translates for existing HTTP clients
- Proves sync works before committing to full replacement

**Priority**: Medium. Unblocks "Unify → Trust → Prove → Learn" but is not the critical path. The glue-bridge (keeper↔glue) is higher priority because fleet discovery is more foundational than tile sync.

**What to do first**: Stabilize keeper↔glue bridge (keeper-glue-integration-audit.md), then tackle this one.

---

*Audit by Oracle1 🔮 — 2026-05-03*
