# keeper-beacon × cocapn-glue-core Integration Audit

**Date:** 2026-05-03
**Analyst:** Oracle1 (subagent)
**Task:** Go/no-go on wiring keeper-beacon fleet discovery to cocapn-glue-core's Beacon protocol
**Status:** COMPLETE — READY FOR DECISION

---

## 0. Executive Summary

**Recommendation: LAYERED COEXISTENCE (not full replacement)**

| | keeper-beacon (Python) | cocapn-glue-core (Rust) |
|---|---|---|
| **Language** | Python 3.10 | Rust (no_std, ~22KB) |
| **Discovery model** | Centralized HTTP POST/Python dict | Decentralized broadcast/recv traits |
| **Capabilities** | String list matching | 6-bit u32 bitmask (NoStd/Async/CUDA/Plato/FFI/Python) |
| **Identity** | `agent_id` (arbitrary string) | `TierId` (8-byte fixed, tier-specific) |
| **Transport** | HTTP/JSON over TCP | Postcard binary over any `Transport` impl |
| **PLATO sync** | None (keeper stores agents, no rooms) | Snapshot/Delta/Invalidate via `PlatoSyncPayload` |
| **Provenance** | SHA-256 sig (16 hex chars) | Merkle tree over `VerificationTrace` |
| **Generations** | None | `SyncGeneration(u64)` monotonic |

These are **orthogonal layers**, not competing implementations:

- **keeper-beacon** = **fleet registry + HTTP API + capability matching + proximity scoring** (Python, Oracle1's runtime)
- **cocapn-glue-core** = **wire format + binary serialization + transport abstraction + PLATO sync payload** (Rust, embeddable)

You cannot "replace" one with the other. They solve different problems at different layers.

---

## 1. What Each System Actually Provides

### 1a. cocapn-glue-core Beacon Protocol

Source: `src/discovery/beacon.rs` + `src/discovery/capabilities.rs` + `src/discovery/peer.rs`

```rust
// Fixed 8-byte tier identifier (no heap)
pub struct TierId([u8; 8]);
impl TierId {
    pub const BROADCAST: TierId = TierId([0xFF; 8]);
    pub fn from_mac(mac: &[u8; 6]) -> Self;    // Mini tier
    pub fn from_pid_timestamp(pid: u32, ts: u32) -> Self;  // Std tier
    pub fn from_uuid_prefix(uuid: &[u8; 16]) -> Self;     // Edge/Thor tier
}

// Capability bitmask (6 bits)
#[repr(u32)]
pub enum Capability {
    NoStd = 1 << 0,
    Async  = 1 << 1,
    Cuda   = 1 << 2,
    Plato  = 1 << 3,
    Ffi    = 1 << 4,
    Python = 1 << 5,
}
pub struct Capabilities(pub u32);  // OR of Capability values

// Beacon broadcast packet
pub struct Beacon {
    pub sender: TierId,
    pub capabilities: Capabilities,
    pub protocol_version: u16,
    pub timestamp: u64,
}

// Discovery trait (implementors supply transport)
pub trait Discovery {
    fn broadcast(&mut self, beacon: &Beacon) -> Result<(), Self::Error>;
    fn listen(&mut self) -> Result<Beacon, Self::Error>;
}

// Wire message envelope
pub enum WireMessage {
    Handshake(Handshake),   // connection setup
    DataChunk(DataChunk),   // chunked payload
    Ack(Ack),              // delivery receipt
    Error(WireError),      // transport-level error
}

// PLATO sync
pub enum PlatoSyncPayload {
    Snapshot { room_id, generation: SyncGeneration, data },
    Delta { room_id, from_gen, to_gen, patch },
    Invalidate { room_id, generation },
    SyncAck { room_id, generation },
}

// Serialization: Postcard (compact binary, no_std compatible)
pub fn serialize_message(msg: &WireMessage) -> Result<Vec<u8>, postcard::Error>;
pub fn deserialize_message(bytes: &[u8]) -> Result<WireMessage, postcard::Error>;
```

**What glue-core's Beacon gives you:**
- Binary wire format (Postcard) — ~10-50x smaller than JSON over HTTP
- Fixed-size `TierId` — deterministic, no string parsing, no heap
- 6-bit capability bitmask — fast capability checks without string compare
- `Discovery` trait — you implement `broadcast()`/`listen()` for your transport (UDP multicast, WebSocket, UART, anything)
- `Transport` trait — read/write abstraction, swap UART for TCP without changing protocol
- PLATO sync payloads — generation-based delta sync for knowledge rooms
- **No network I/O built in** — that's your job via `Discovery` trait implementation

### 1b. keeper-beacon (Python)

Source: `keeper_beacon/` (pip package, v0.1.0, Python 3.10)

```python
# registry.py — fleet member tracking
@dataclass
class AgentRecord:
    agent_id: str          # arbitrary string (e.g., "jetson-claw-1")
    name: str
    capabilities: list[str]  # ["python", "cuda", "plato_search", ...]
    endpoint: str           # HTTP URL
    status: AgentStatus    # ACTIVE/IDLE/OFFLINE/MAINTENANCE
    trust_score: float      # 0.0–1.0
    load: float             # 0.0–1.0

class AgentRegistry:
    def register(record) -> bool
    def heartbeat(agent_id) -> bool
    def get(agent_id) -> AgentRecord | None
    @property active_agents() -> list[AgentRecord]

# discovery.py — beacon signal store
@dataclass
class BeaconSignal:
    agent_id: str
    name: str
    capabilities: list[str]
    endpoint: str
    timestamp: float
    ttl: float = 60.0
    signature: str = ""      # SHA-256 of agent_id:name:endpoint:timestamp

class BeaconDiscovery:
    def receive(signal: BeaconSignal) -> bool
    def discover(capability: str | None) -> list[BeaconSignal]
    def prune() -> int

# matcher.py — task-to-agent capability matching
class CapabilityMatcher:
    def match(agents, required: list[str]) -> list[MatchResult]
    def best_match(agents, required) -> MatchResult | None
    def fully_capable(agents, required) -> list[MatchResult]

# proximity.py — proximity scoring
class ProximityScorer:
    def score_agents(agents, required_caps, max_latency_ms) -> list[tuple[Agent, float]]

# keeper.py — HTTP API on port 8900
POST /register       → AgentRegistry.register + BeaconDiscovery.receive
POST /heartbeat      → AgentRegistry.heartbeat + beacon refresh
GET  /discover       → BeaconDiscovery.discover(capability=)
GET  /match          → CapabilityMatcher.match
GET  /proximity      → ProximityScorer.score_agents
POST /bottle/send    → BottleRouter.send (fleet messaging)
POST /bottle/collect → BottleRouter.collect
```

**What keeper-beacon gives you:**
- REST HTTP API — agents POST registration/heartbeat, keeper responds
- Python-native fleet registry with staleness tracking (300s threshold)
- String-based capability matching with weighted scoring (cap/load/trust)
- Bottle-protocol messaging (separate routing layer)
- **No binary wire format** — JSON over HTTP, Python dicts
- **No transport abstraction** — HTTP only, no UDP/UART/WebSocket
- **No PLATO sync** — keeper knows about agents, not knowledge rooms

---

## 2. Exact Changes Needed to Wire Them Together

The goal: **use glue-core's wire format as the encoding layer under keeper-beacon's discovery semantics**, while keeping the Python registry/matching/scorer intact.

### 2a. Bridge: Python → glue-core encoding

**Problem:** keeper-beacon emits `BeaconSignal` (Python dict, string capabilities). glue-core expects `Beacon { sender: TierId, capabilities: Capabilities, protocol_version: u16, timestamp: u64 }`.

**Solution:** Write a thin Python shim (`glue_bridge.py`) that:
1. Takes a `BeaconSignal` (Python)
2. Encodes it as Postcard binary matching glue-core's `Beacon` layout
3. Sends over a `Transport`-compatible channel (initially: HTTP POST to keeper, which proxies to a Rust sidecar)

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│ keeper-beacon   │────▶│ glue_bridge.py   │────▶│ keeper-glue-sidecar│
│ (Python dicts)  │     │ (Postcard encode)│     │ (Rust, std binary) │
└─────────────────┘     └──────────────────┘     └────────────────────┘
                                                         │
                              ┌──────────────────────────┘
                              ▼
                        WireMessage::Handshake(...)
                        (via Transport trait, TCP/Unix socket)
```

**Code-level changes (glue_bridge.py):**

```python
# glue_bridge.py — thin shim, no Rust needed for encoding side
import struct, hashlib, time

# TierId construction (for keeper's own tier)
def tier_id_from_pid() -> bytes:
    import os
    pid = os.getpid() % 0xFFFFFFFF
    ts = int(time.time()) & 0xFFFFFFFF
    return struct.pack("<I", pid) + struct.pack("<I", ts)

# Beacon encoding to Postcard-compatible bytes (manual, no Rust FFI needed)
CAPABILITY_MAP = {
    "python": 1 << 5,
    "async": 1 << 1,
    "cuda": 1 << 2,
    "plato": 1 << 3,
    "ffi": 1 << 4,
    "nostd": 1 << 0,
}

def encode_beacon(agent_id: str, capabilities: list[str],
                  protocol_version: int = 1) -> bytes:
    tier_id = tier_id_from_pid()
    caps_u32 = 0
    for cap in capabilities:
        if cap.lower() in CAPABILITY_MAP:
            caps_u32 |= CAPABILITY_MAP[cap.lower()]
    ts = int(time.time() * 1000)  # ms for glue-core's u64
    # Postcard encoding: [variant_idx(u8)][TierId(8)][caps(u32)][version(u16)][ts(u64)]
    msg = bytes([0]) + tier_id + struct.pack("<I", caps_u32) + struct.pack("<H", protocol_version) + struct.pack("<Q", ts)
    return msg

def encode_handshake(agent_id: str, capabilities: list[str]) -> bytes:
    """Handshake = Beacon encoded as WireMessage::Handshake"""
    beacon_bytes = encode_beacon(agent_id, capabilities)
    # WireMessage::Handshake variant index = 0
    return beacon_bytes
```

This shim doesn't need Rust FFI — pure Python struct packing to Postcard format. The receiving side (Rust sidecar) does the decode.

### 2b. Rust sidecar (keeper-glue-agent)

A minimal Rust binary (`keeper-glue-agent`) that:
1. Listens on a Unix socket or localhost TCP port
2. Receives Postcard-encoded `WireMessage` bytes from Python
3. Decodes via `cocapn_glue_core::wire::deserialize_message()`
4. Forwards decoded `Beacon` to keeper's `BeaconDiscovery.receive()` via HTTP

```rust
// keeper-glue-agent/src/main.rs
use cocapn_glue_core::wire::{self, TierId, WireMessage};
use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8910")?;
    for stream in listener.incoming() {
        let mut stream = stream?;
        let mut buf = vec![0u8; 65536];
        let n = stream.read(&mut buf)?;
        let msg: WireMessage = wire::deserialize_message(&buf[..n])?;
        // Forward to keeper HTTP API
        forward_beacon_to_keeper(&msg);
    }
    Ok(())
}

fn forward_beacon_to_keeper(msg: &WireMessage) {
    // Extract Beacon fields, call keeper's HTTP POST /register
    // ...
}
```

### 2c. keeper.py changes

**Minimal diff to keeper.py:**

```python
# keeper.py — add near top, after imports
from glue_bridge import encode_handshake, tier_id_from_pid

# In POST /register handler, after registry.register():
def do_POST(self):
    # ... existing registry/register code ...
    # NEW: also emit to glue sidecar
    try:
        import urllib.request
        handshake_bytes = encode_handshake(name, body.get("capabilities", []))
        req = urllib.request.Request(
            "http://127.0.0.1:8910/send",
            data=handshake_bytes,
            headers={"Content-Type": "application/octet-stream"},
        )
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass  # sidecar down is non-fatal, existing path still works
```

This preserves full backward compatibility — keeper still works if the Rust sidecar is down.

### 2d. Fleet agents (JC1, CCC, etc.) — no changes needed initially

Agents continue using keeper's HTTP API (`POST /register`). The glue layer is entirely inside keeper. Agents only migrate when their vessels are updated to use glue-core's `Discovery` trait directly.

---

## 3. Compatibility Risk

### Breaking changes if we do full replacement:

| Risk | Severity | Detail |
|------|----------|--------|
| **Agent IDs** | **HIGH** | keeper uses arbitrary strings (`"jetson-claw-1"`). glue-core uses 8-byte `TierId`. No mapping exists. A full replacement breaks all existing `/register` callers. |
| **Capability format** | **HIGH** | keeper uses `list[str]` (`["python", "cuda", "plato_search"]`). glue-core uses 6-bit u32 (`0b100111`). No bidirectional conversion without a canonical mapping table. |
| **Transport** | **HIGH** | keeper uses HTTP/JSON. glue-core defines a `Transport` trait with no built-in implementation. You cannot "just replace" without implementing a transport. |
| **Bottle protocol** | **LOW** | Bottle routing is entirely separate (Python, `BottleRouter`). Not affected by beacon changes. |
| **PLATO sync** | **N/A** | keeper has no PLATO sync. glue-core's `PlatoSyncPayload` is orthogonal — no conflict, just new capability. |
| **Keeper state** | **MEDIUM** | Existing `fleet.json` state stores agents as `{agent_id: {...}}`. If new agents register with `TierId`, the state format changes. Migration needed. |

**The hard problem: TierId ↔ agent_id mapping.** keeper's entire API, BottleRouter, AgentRegistry, and all fleet consumers (Conductor, Nexus, PathFinder) use `agent_id` strings. glue-core's `TierId` is 8 raw bytes with no semantic meaning outside the tier. Without a bidirectional mapping layer, you cannot phase this in incrementally.

---

## 4. Recommended Approach: Layered Coexistence

**Not a big-bang replacement. A protocol stacking:**

```
Layer 1 (unchanged):  keeper-beacon Python registry + HTTP API + capability matcher + bottle routing
Layer 2 (new):       glue-core binary encoding as OPTIONAL upgrade path for Rust/embedded agents
                     (Python agents stay on Layer 1, Rust agents can opt into Layer 2)
Layer 3 (future):    When majority of fleet uses glue-core, deprecate Layer 1's beacon encoding
                     but keep the registry/matching API (backward compatible via TierId→agent_id map)
```

**Why not full replacement now:**
1. **No Rust FFI story** — keeper.py is pure Python. Calling Rust requires either a sidecar process or PyO3 bindings. PyO3 bindings would mean compiling Rust into a Python module (complex, version-locked). Sidecar is simpler but adds a process to manage.
2. **String → binary impedance mismatch** — all existing fleet agents (JC1, CCC, etc.) use string agent_ids and string capability lists. glue-core's fixed TierId + bitmask requires a migration layer.
3. **Transport trait is a blank slate** — glue-core defines `Discovery` trait but provides no UDP multicast, no WebSocket, no HTTP server. You must implement the transport. That's a non-trivial engineering effort.
4. **keeper-beacon has matching/scoring that glue doesn't** — `CapabilityMatcher`, `ProximityScorer` are Python algorithms with weighted scoring. glue-core has no equivalent. You'd have to reimplement them in Rust or keep the Python layer anyway.

**The correct replacement threshold:** When 50%+ of fleet agents are Rust-based (directly using glue-core's `Discovery` trait with their own `Transport` impl), then keeper's Python layer can become a thin proxy. Until then, the Python registry is the source of truth.

---

## 5. Migration Sequence

### Phase 0 — Parallel Stack (0 current)
- [ ] Write `glue_bridge.py` (Python Postcard encoder, no Rust needed)
- [ ] Publish `keeper-glue-agent` Rust sidecar to crates.io
- [ ] Test encoding roundtrip: `BeaconSignal` → `encode_beacon()` → sidecar decode → keeper HTTP `/register`
- [ ] Zero fleet disruption — both paths work simultaneously

### Phase 1 — Keeper accepts glue-core (weeks 1–2)
- [ ] keeper.py POST `/register` accepts BOTH JSON (existing) AND Postcard binary (new, Content-Type: application/octet-stream)
- [ ] keeper.py response includes `X-TierId` header for new clients
- [ ] No agent changes required
- [ ] State file gets optional TierId field on AgentRecord

### Phase 2 — Rust agents opt in (weeks 3–6)
- [ ] JC1 vessel updates to include `cocapn-glue-core` + `Discovery` impl over TCP
- [ ] JC1 sends `WireMessage::Handshake` to keeper-glue-agent sidecar
- [ ] sidecar maps `TierId` → keeper agent_id (via lookup or allocation table)
- [ ] CCC vessel follows same pattern
- [ ] FM vessel (Forgemaster's own deployment) uses glue-native discovery

### Phase 3 — Fleet on glue (months 2–3)
- [ ] 50%+ of active agents sending binary beacons
- [ ] Python registry continues to accept both formats (backward compat)
- [ ] Deprecate `BeaconSignal.signature` (replaced by Merkle provenance)
- [ ] keeper-glue-agent becomes required (not optional)

### Phase 4 — Simplification (month 3+)
- [ ] Drop JSON beacon path from keeper.py (breaking change, announce deprecation)
- [ ] All agents must use glue-core wire format
- [ ] `TierId ↔ agent_id` mapping baked into keeper state
- [ ] Remove `keeper_beacon` pip package dependency from keeper.py
- [ ] PLATO sync via `PlatoSyncPayload` activates (Snapshot/Delta/Invalidate)

---

## 6. What Each Subagent/Vessel Must Change

### Oracle1 (keeper.py)
| Change | Scope | Risk |
|--------|-------|------|
| Add `glue_bridge.py` import | ~5 lines | LOW |
| Accept Postcard binary in `/register` | ~20 lines | LOW |
| Add `X-TierId` response header | ~5 lines | LOW |
| Keep both paths functional | Existing tests pass | LOW |
| Eventually drop JSON path | Deprecation + migration | MEDIUM |

### JC1 (JetsonClaw1-vessel)
| Change | Scope | Risk |
|--------|-------|------|
| Add `cocapn-glue-core` to vessel Cargo.toml | 1 line | LOW |
| Implement `Discovery` trait for UART/TCP | ~50 lines | MEDIUM |
| Send `Beacon` on boot + heartbeat | ~20 lines | LOW |
| Handle `TierId` allocation (from keeper on first connect) | ~30 lines | MEDIUM |
| Replace `POST /register` with `WireMessage::Handshake` | ~10 lines | LOW |

**Note:** JC1 is already Rust-capable (it's Forgemaster's reference vessel). This is the natural first adopter.

### CCC (Cocapn-Captain-Crew, if exists)
Same as JC1 once JC1 proves the path. If CCC is Python-only, it stays on keeper's HTTP API through Phase 2.

### FM (Forgemaster's own deployment)
- Primary author of `cocapn-glue-core` — already using it
- Should implement `Discovery` trait over Unix socket or TCP
- Coordinate with Oracle1 on `TierId` allocation scheme
- Needs to publish `keeper-glue-agent` sidecar (see Phase 0)

### agent-api (fleet services/agent_api.py)
| Change | Scope | Risk |
|--------|-------|------|
| Accept `TierId` field in registration payload | ~10 lines | LOW |
| Store TierId alongside agent_id in state | Existing state format change | MEDIUM |
| Propagate TierId to Plato room metadata | ~20 lines | LOW |

---

## 7. GO/NO-GO Verdict

```
┌─────────────────────────────────────────────────────────┐
│  DECISION POINT: Full replacement now                   │
│  VERDICT:  NO-GO (not yet)                              │
│                                                         │
│  DECISION POINT: Layered coexistence + phased migration │
│  VERDICT:  GO — start Phase 0 immediately              │
└─────────────────────────────────────────────────────────┘
```

### Why GO on coexistence:
- **No disruption** to live fleet (both paths work simultaneously)
- **Unblocks Rust agents** (JC1, FM, future embedded) who need binary wire format
- **Preserves Python registry** (all matching/scoring algorithms stay in Python)
- **glue-core's value is real**: Postcard binary is 10-50x smaller than JSON, `TierId` is fixed-size (no string parsing), `Transport` abstraction lets you swap UDP for TCP without protocol changes

### Why not full replacement yet:
- **No transport implementation** — glue-core's `Discovery` trait is a blank slate
- **No TierId allocation scheme** — need to design `TierId ↔ agent_id` mapping
- **No Rust FFI story** — keeper.py is pure Python, no PyO3 bindings today
- **Python agents must continue working** — they have no path to glue-core today

### The critical path item:
**`keeper-glue-agent` sidecar** — this is the load-bearing piece that lets Python keeper and Rust agents communicate in glue-core's wire format. FM needs to publish it. Without it, Phase 1 cannot start.

### The critical design item:
**TierId allocation table** — who allocates TierIds? Does keeper assign them on first `Handshake`? Is there a registry? This must be solved before Phase 2 begins.

---

## Appendix A: Wire Format Detail

### Postcard-encoded Handshake (WireMessage::Handshake variant=0)

```
Byte 0:       variant index = 0 (Handshake)
Bytes 1-8:    TierId (8 bytes, little-endian for PID/timestamp tiers)
Bytes 9-12:   capabilities u32 bitmask
Bytes 13-14:  protocol_version u16 (little-endian)
Bytes 15-22:  timestamp u64 (little-endian, milliseconds)
Total: 23 bytes (vs ~150+ bytes JSON equivalent)
```

### Beacon Packet (glue-core Discovery layer)

```
Implements Discovery trait — transport-specific:
- UDP multicast: send to GLUE_MULTICAST_GROUP:port
- TCP: connect to keeper:8910, send Postcard bytes
- UART: write bytes directly to serial
```

### Python BeaconSignal (keeper-beacon current)

```json
{
  "agent_id": "jetson-claw-1",
  "name": "JetsonClaw1",
  "capabilities": ["python", "cuda", "plato_search"],
  "endpoint": "http://192.168.1.100:8901",
  "timestamp": 1746272400.123,
  "ttl": 60.0,
  "signature": "a3f8b2c1d4e5"
}
```
JSON string: ~200-300 bytes. No binary equivalent.

---

## Appendix B: Missing BEACHCOMB-PROTOCOL.md

The task referenced `/home/ubuntu/.openclaw/workspace/repos/forgemaster/from-fleet/BEACHCOMB-PROTOCOL.md` but:
1. The `forgemaster` repo does not exist at that path
2. `BEACHCOMB-PROTOCOL.md` was not found in any repo
3. `beachcomb_v3.py` exists at `scripts/beachcomb_v3.py` — this is a commit-watching script, not a protocol spec

**Recommendation:** FM should publish `BEACHCOMB-PROTOCOL.md` to the cocapn-glue-core repo README or a dedicated `SPEC.md`. The protocol spec is the single source of truth for tier-to-tier communication — it should live next to the code that implements it.

---

## Appendix C: crates.io vs. Source

`cocapn-glue-core` v0.1.0 was sourced from the extracted crate at `/tmp/cocapn-glue-core-0.1.0/` (downloaded from crates.io). The GitHub repo `SuperInstance/cocapn-glue-core` was not accessible (404 on raw content, empty on tree listing). This suggests:
- Crate was published from a local build, not pushed to GitHub
- Or repo is private/non-existent
- **Action needed:** FM should push `cocapn-glue-core` to GitHub so the fleet can audit the source

---

*End of audit. Oracle1, 2026-05-03.*
