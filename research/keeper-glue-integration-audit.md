# Keeper↔Glue Integration Audit

## Sources
- Keeper beacon: `/home/ubuntu/.local/lib/python3.10/site-packages/keeper_beacon/`
- Keeper service: `/home/ubuntu/.openclaw/workspace/fleet/services/keeper.py`
- cocapn-glue-core: `cargo install cocapn-glue-core` → crates.io v0.1.0

---

## What keeper-beacon provides (current)

**Architecture**: Python in-memory beacon system. Agents POST BeaconSignal to keeper HTTP API. Keeper stores in BeaconDiscovery (dict[agent_id] → BeaconSignal). No wire format — just HTTP JSON.

**BeaconSignal fields**:
```
agent_id: str          # unique vessel ID
name: str              # "Oracle1", "JetsonClaw1", etc.
capabilities: list[str]  # ["python", "rust", "plato", "cuda"]
endpoint: str          # HTTP URL for direct communication
timestamp: float       # Unix time
ttl: float             # 60s default, expired → purged
signature: str         # SHA256[:16] of agent_id:name:endpoint:timestamp
```

**What keeper-beacon does**:
- `receive(signal)` — stores or updates a beacon (in-memory dict)
- `discover(capability?)` — returns active (non-expired) beacons, optionally filtered
- `prune()` — removes expired beacons
- `CapabilityMatcher` — list intersection for capability matching
- `ProximityScorer` — staleness-as-latency proxy scoring
- `AgentRegistry` — tracks AgentRecord with trust_score + load

**Limitations**:
- No wire protocol — just in-memory Python dicts
- No persistence across keeper restarts
- No Merkle provenance — beacons can be replayed/faked
- capabilities is a list (O(n) lookup), not a bitmask
- TTL-based expiry is fragile — clock skew kills agents
- No PLATO sync built in

---

## What cocapn-glue-core provides (FM's)

**Architecture**: Rust no_std binary wire protocol. Serializes to postcard (binary CBOR). Works from Cortex-M4 to Jetson Thor.

**Key types**:
```
TierId          # enum: Unknown=0, MCU=1, Edge=2, Cloud=3, Thor=4
WireMessage     # { tier: TierId, msg_type, payload: bytes }
Capabilities    # bitmask (not list) — O(1) test, compact
PlatoSyncPayload # Snapshot | Delta | Invalidate + monotonic generation
MerkleProof     # SHA-256 over verification trace
```

**What glue does**:
- Wire format: binary postcard (not JSON, not HTTP)
- Beacon: multicast discovery over TierId broadcast
- PLATO sync: Snapshot/Delta/Invalidate with monotonic generations (no rollback possible)
- Merkle provenance: every verification trace gets a hash chain
- Capabilities as bitmask — O(1) capability testing

**What glue doesn't have**:
- No trust_score, no load tracking
- No staleness-based scoring
- No AgentRegistry concept — just wire broadcast and response
- No HTTP API — binary only

---

## The key differences

| Aspect | keeper-beacon (Python) | cocapn-glue-core (Rust) |
|--------|------------------------|------------------------|
| Transport | HTTP JSON | Binary postcard wire |
| Capabilities | `list[str]` (O(n)) | `bitmask` (O(1)) |
| Expiry | TTL (clock-dependent) | Monotonic generations (no rollback) |
| Provenance | None | SHA-256 Merkle chain |
| Persistence | In-memory only | Wire format (can be stored) |
| Scope | Fleet discovery only | Fleet discovery + PLATO sync + trust |
| Agents affected | All fleet agents | All fleet agents |
| Cross-tier | No | Yes (MCU to Thor) |

---

## Can we replace keeper-beacon with glue-core's Beacon?

**Short answer: Yes, but NOT as a direct replacement.**

The beacon protocols serve the same purpose (fleet discovery) but are architecturally incompatible:
- keeper-beacon is an in-memory registry with HTTP polling
- glue-core is a wire protocol with multicast broadcast

Replacing one with the other requires rewriting all fleet agents to speak glue wire protocol instead of HTTP. That's a full fleet migration.

---

## Recommended approach: Layered Coexistence (Phase 1)

**Keep keeper-beacon running. Add a glue-to-keeper bridge.**

```
┌─────────────────────────────────────────────────┐
│              Keeper (port 8900)                  │
│  ┌──────────────────┐   ┌──────────────────────┐ │
│  │ keeper-beacon    │   │  glue-bridge         │ │
│  │ (HTTP, Python)   │ ←→│  (converts glue ↔    │ │
│  │                  │   │   keeper signal)     │ │
│  └──────────────────┘   └──────────────────────┘ │
└─────────────────────────────────────────────────┘
            ↑ HTTP                    ↑ Binary
            │                         │
   Oracle1, JC1, CCC          Forgemaster (Rust)
   (current agents)           (future: all agents)
```

**glue-bridge responsibilities**:
1. Listen on a glue wire socket (e.g., port 9439)
2. When glue beacon arrives → convert to BeaconSignal → feed to keeper-beacon
3. When keeper-beacon wants to broadcast → convert to glue WireMessage → send on glue multicast
4. Translate capability list ↔ capabilities bitmask

This lets current agents stay on HTTP while FM's Rust agents and new agents use glue.

---

## Migration sequence (Phase 2 → 3 → 4)

**Phase 2 (after bridge stable): Migrate Forgemaster to glue**
- FM's vessel already has glue built in
- FM sends beacons over glue wire instead of HTTP
- Bridge translates for keeper-beacon

**Phase 3 (after FM stable): Migrate JC1 to glue**
- JetsonClaw1 on GPU edge tier
- Requires glue Rust bindings for Python or a small native shim

**Phase 4 (after JC1 stable): Migrate CCC, then Oracle1**
- CCC (Telegram agent) needs glue client library
- Oracle1 (keeper) needs full glue server support
- At this point keeper-beacon can be deprecated

---

## What breaks if we do a full replacement today

1. **All current agents lose fleet discovery** — they POST HTTP beacons, not glue wire
2. **keeper.py beacon handling** — lines 76, 136, 198, 215, 216 in keeper.py all call `discovery.receive(BeaconSignal)` — these would need glue-native equivalents
3. **CapabilityMatcher** — uses list intersection, incompatible with bitmask
4. **AgentRegistry** — keeper-beacon stores AgentRecord with trust_score/load, glue has no equivalent
5. **No existing glue Python bindings** — no `pip install cocapn-glue-core`
6. **CCC Telegram agent** — would need a complete rewrite of its fleet comms layer

---

## What vessels need to change

| Vessel | Current beacon | Change needed |
|--------|---------------|---------------|
| Oracle1 (keeper) | keeper-beacon (HTTP) | Phase 4: full glue server |
| JetsonClaw1 | keeper-beacon (HTTP) | Phase 3: glue shim on edge |
| Forgemaster | keeper-beacon (HTTP) | Phase 2: glue native |
| CCC | keeper-beacon (HTTP) | Phase 4: glue Python bindings |
| New agents | none | Start with glue directly |

---

## Concrete next step (before any migration)

Write `fleet/services/glue_bridge.py`:
- Listen on UDP port 9439 for glue wire beacons
- Parse incoming glue WireMessage
- Extract TierId, Capabilities bitmask, timestamp
- Convert to BeaconSignal format
- Call `discovery.receive(BeaconSignal)` to feed keeper-beacon

This is the smallest viable integration point. It proves the bridge works without touching any agent code.

---

## Decision: Go/No-Go

**GO** for layered coexistence approach (Phase 1 bridge)
- Adds glue support without breaking current fleet
- Proves integration works before committing to full migration
- FM's glue becomes the wire format standard, keeper-beacon becomes a legacy compatibility layer

**NO-GO** for full replacement today
- Too many agents depend on HTTP beacon
- No Python bindings for glue-core exist yet
- Bridge approach de-risks the migration

**TIMING**: After FM's 3 papers are pushed + cocapn-glue-core v0.2.0 (with Python bindings expected).

---

*Audit by Oracle1 🔮 — 2026-05-03*
