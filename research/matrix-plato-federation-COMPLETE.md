# Matrix.org as Decentralized Comms Protocol for PLATO Fleet Federation
## Deep Research — April 20, 2026

> **The question:** Can every agent run their own PLATO and simply key together via Matrix?

**Short answer: Yes, and it's the right architecture.**

---

## 1. What Matrix Actually Is

Matrix is an **open federated pub/sub layer for the internet**. Not an app, not a chat tool — a protocol for synchronizing JSON objects between servers with no single point of control. Think of it as **git for real-time events**, where every homeserver has a full copy of the rooms it cares about, and federation keeps them eventually consistent.

### Core Concepts

```
┌─────────────┐    HTTPS/PUT    ┌─────────────┐
│  Homeserver  │ ◄─────────────► │  Homeserver  │
│  (Oracle1)   │   Federation    │  (FM)        │
└──────┬───────┘                  └──────┬───────┘
       │ Client-Server API               │
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│ Agent Bridge │                  │ Agent Bridge │
│ (AppService) │                  │ (AppService) │
└──────┬───────┘                  └──────┬───────┘
       │                                 │
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│ PLATO Server │                  │ PLATO Server │
│   :8847      │                  │   :8847      │
└──────────────┘                  └──────────────┘
```

**Homeserver** — Each agent runs one. Stores all events (tiles) for rooms the agent has joined. Federation keeps copies in sync.

**Room** — A shared space. Identified by `!opaque_id:domain`. No single owner — all participating homeservers have a copy. Maps 1:1 to a PLATO Room.

**Event** — A JSON object with a type. The atomic unit of data. Maps 1:1 to a PLATO Tile.

**Event Graph (DAG)** — All events in a room form a directed acyclic graph. Each event references its parents (prev_events). This gives causal ordering without a central clock. This IS the tile timeline.

**Federation** — Server-server HTTPS communication. Homeserver A sends a transaction (batch of events) to Homeserver B via `PUT /_matrix/federation/v1/send/{txnId}`. Events are signed by the originating server. No central broker needed.

**State Resolution** — When two homeservers diverge (split brain), the state resolution algorithm deterministically merges them. Every server computes the same result independently. This handles intermittent connectivity perfectly.

---

## 2. The Mapping: Matrix → PLATO

| Matrix Concept | PLATO Concept | Why It Works |
|---|---|---|
| Homeserver | PLATO Server (per agent) | Each agent owns its data |
| Room | PLATO Room (Harbor, Forge, etc.) | Shared training space |
| Message Event | Tile | Knowledge unit with history |
| State Event | Room Config / Ensign | Persistent room metadata |
| Federation | Fleet-wide tile sync | Real-time without central server |
| Application Service | PLATO Bridge | Connects PLATO API to Matrix |
| Event Graph | Tile Timeline | DAG = causal ordering of tiles |
| User | Agent Identity | `@oracle1:cocapn.ai` |
| Room Alias | Room Discovery | `#harbor:cocapn.ai` |
| PDUs (Persistent) | Committed tiles | Stored permanently, signed |
| EDUs (Ephemeral) | Presence/heartbeat | Not stored, real-time only |
| E2E Encryption (Megolm) | Tile privacy | Cryptographic room privacy |
| State Resolution | Split-brain merge | Offline agents catch up cleanly |

---

## 3. Custom PLATO Event Types

Matrix uses reverse-DNS namespacing for custom events. Ours:

### Message Events (stored in history, like tiles)

```json
{
  "type": "com.cocapn.plato.tile",
  "content": {
    "tile_id": "tile_abc123",
    "domain": "knowledge_preservation",
    "confidence": 0.92,
    "agent": "oracle1",
    "data": {
      "summary": "SyncLink binary protocol design",
      "details": "16-bit sync ID, 1-byte type flag...",
      "source_room": "harbor"
    },
    "tags": ["protocol", "sync", "binary"],
    "timestamp": "2026-04-20T20:00:00Z"
  }
}
```

```json
{
  "type": "com.cocapn.plato.ensign",
  "content": {
    "ensign_id": "quartermaster-instinct-v1.12",
    "room": "harbor",
    "compression_ratio": 0.669,
    "format": "json",
    "artifact": "<base64 encoded ensign data>"
  }
}
```

```json
{
  "type": "com.cocapn.plato.bottle",
  "content": {
    "from": "oracle1",
    "to": "forgemaster",
    "priority": "P1",
    "subject": "Rust crates compiled on Jetson?",
    "body": "Need you to compile the 11 Rust crates..."
  }
}
```

### State Events (persistent key-value, like room config)

```json
{
  "type": "com.cocapn.plato.room_config",
  "state_key": "harbor",
  "content": {
    "preset": "HarborRoom",
    "tile_count": 2366,
    "active_agents": ["oracle1", "forgemaster", "jc1"],
    "ensign_version": "v1.12",
    "deadband_policy": "P0_block_P1_route_P2_optimize"
  }
}
```

```json
{
  "type": "com.cocapn.plato.agent_state",
  "state_key": "@oracle1:cocapn.ai",
  "content": {
    "role": "lighthouse_keeper",
    "hardware": "ARM64 Oracle Cloud 24GB",
    "services": ["keeper:8900", "agent-api:8901", "plato:8847"],
    "tile_count": 25429,
    "ensign_count": 10,
    "status": "active"
  }
}
```

---

## 4. Federation Topology for 3 Agents

```
                    ┌──────────────────────┐
                    │   cocapn.ai (DNS)    │
                    │   Oracle Cloud ARM64  │
                    │                      │
                    │  ┌────────────────┐  │
                    │  │  Conduwuit     │  │
                    │  │  Homeserver    │  │
                    │  │  :8448         │  │
                    │  └───────┬────────┘  │
                    │          │           │
                    │  ┌───────▼────────┐  │
                    │  │ PLATO Bridge   │  │
                    │  │ (AppService)   │  │
                    │  └───────┬────────┘  │
                    │          │           │
                    │  ┌───────▼────────┐  │
                    │  │ PLATO Server   │  │
                    │  │ :8847          │  │
                    │  └────────────────┘  │
                    └──────────┬───────────┘
                               │
              HTTPS Federation │(server-server :8448)
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
    ┌───────▼────────┐                   ┌────────▼───────┐
    │  FM's WSL2     │                   │  JC1's Jetson  │
    │  RTX 4050      │                   │  Orin Super    │
    │                │                   │                │
    │ ┌────────────┐ │                   │ ┌────────────┐ │
    │ │ Conduwuit  │ │                   │ │ Conduwuit  │ │
    │ │ :8448      │ │                   │ │ :8448      │ │
    │ └─────┬──────┘ │                   │ └─────┬──────┘ │
    │       │        │                   │       │        │
    │ ┌─────▼──────┐ │                   │ ┌─────▼──────┐ │
    │ │PLATO Bridge│ │                   │ │PLATO Bridge│ │
    │ └─────┬──────┘ │                   │ └─────┬──────┘ │
    │       │        │                   │       │        │
    │ ┌─────▼──────┐ │                   │ ┌─────▼──────┐ │
    │ │PLATO :8847 │ │                   │ │PLATO :8847 │ │
    │ └────────────┘ │                   │ └────────────┘ │
    └────────────────┘                   └────────────────┘
```

### NAT/Firewall Handling
- Oracle1 is publicly accessible (Oracle Cloud) — primary federation point
- FM (WSL2 behind NAT) — either port forward 8448, or use Cloudflare Tunnel / Tailscale
- JC1 (Jetson, potentially on boat) — tailscale for stable connection, or just pulls on reconnect

### Intermittent Connectivity (JC1 on boat)
- **Matrix handles this natively.** When JC1's homeserver comes back online, it requests backfill from Oracle1's server. All missed events sync automatically.
- Events are queued at the sending server until delivery confirmed.
- State resolution handles any conflicts from concurrent edits while offline.
- This is THE killer feature vs. git bottles, which require manual merge.

---

## 5. Application Service Bridge Design

The bridge is the code that connects PLATO server (port 8847) to Matrix.

### registration.yaml (placed on homeserver)

```yaml
id: plato-bridge
url: http://localhost:9898  # bridge listens here
as_token: "random_secret_as_token"
hs_token: "random_secret_hs_token"
sender_localpart: "plato-bridge"
namespaces:
  users:
    - exclusive: true
      regex: "@plato_.*:cocapn\\.ai"
  rooms:
    - exclusive: false
      regex: "!.*:cocapn\\.ai"
  aliases:
    - exclusive: false
      regex: "#plato-.*:cocapn\\.ai"
```

### Bridge Architecture

```python
# plato-matrix-bridge.py — the glue

class PlatoMatrixBridge:
    """
    Bidirectional bridge between PLATO Room Server and Matrix.

    PLATO -> Matrix: PLATO tile submission → Matrix event in room
    Matrix -> PLATO: Matrix event in room → PLATO tile submission
    """

    def on_plato_tile(self, tile):
        """PLATO server calls this when a new tile arrives."""
        # Find or create the Matrix room for this PLATO room
        room_id = self.get_matrix_room(tile["room"])

        # Send as custom event
        self.matrix.send_event(
            room_id=room_id,
            event_type="com.cocapn.plato.tile",
            content={
                "tile_id": tile["id"],
                "domain": tile["domain"],
                "confidence": tile["confidence"],
                "agent": tile["agent"],
                "data": tile["data"],
                "tags": tile.get("tags", []),
            }
        )

    def on_matrix_event(self, event):
        """Matrix AS webhook calls this when event arrives."""
        if event["type"] == "com.cocapn.plato.tile":
            # Forward to local PLATO server
            self.plato.submit_tile(
                room=event["room_id"],
                domain=event["content"]["domain"],
                agent=event["content"]["agent"],
                data=event["content"]["data"],
                confidence=event["content"]["confidence"],
            )
        elif event["type"] == "com.cocapn.plato.bottle":
            # Write bottle to from-fleet/
            self.write_bottle(event["content"])
```

### What This Gives Us
1. Oracle1 submits tile to PLATO → bridge sends Matrix event → FM's bridge receives → submits to FM's PLATO
2. FM submits tile → same flow in reverse
3. JC1 comes online → Matrix backfills all missed events → bridge replays to PLATO

---

## 6. Homeserver Choice: Conduwuit

**Recommendation: Conduwuit** (Rust, lightweight, feature-complete)

| Feature | Conduwuit | Synapse | Dendrite |
|---|---|---|---|
| Language | Rust | Python+Rust | Go |
| RAM usage | ~50-150MB | ~1-2GB | ~200-500MB |
| Database | SQLite (built-in) | PostgreSQL required | SQLite/Postgres |
| ARM64 support | Yes | Yes | Yes |
| Federation | Complete | Complete | Partial |
| Setup | Single binary + config | Complex deps | Beta quality |
| License | Apache 2.0 | AGPL | Apache 2.0 |
| Docker | ~60MB image | ~400MB | ~150MB |

**Why Conduwuit:**
- Runs on ARM64 (Oracle1 + Jetson) and x86_64 (FM's WSL2)
- SQLite means zero database admin — perfect for agents
- Single binary, minimal config
- ~50MB RAM for our scale (1000 events/day is nothing)
- Rust = matches our kernel stack
- Proven stable for small/medium deployments
- Active development (forked from Conduit, heavily improved)

**Note:** Conduwuit's maintainer moved to a new project called **Tuwunel**. We should evaluate both, but Conduwuit is proven and available now.

---

## 7. Private Federation Setup

We DON'T need to connect to the public Matrix network. We run our own federation.

### Steps

```bash
# 1. Install Conduwuit on Oracle1
docker run -d \
  --name conduwuit \
  -v /opt/conduwuit:/data \
  -p 8448:8448 \
  -e CONDUWUIT_SERVER_NAME="cocapn.ai" \
  -e CONDUWUIT_DATABASE_BACKEND="sqlite" \
  -e CONDUWUIT_ALLOW_REGISTRATION=true \
  -e CONDUWUIT_FEDERATION_ENABLED=true \
  girlbossceo/conduwuit:latest

# 2. DNS setup (cocapn.ai)
# Add SRV record: _matrix-fed._tcp.cocapn.ai → oracle1 IP:8448
# OR use .well-known delegation

# 3. Create agent users
curl -X POST http://localhost:8448/_matrix/client/r0/register \
  -d '{"username":"oracle1","password":"...","auth":{"type":"m.login.dummy"}}'

# 4. Create PLATO rooms
curl -X POST http://localhost:8448/_matrix/client/r0/createRoom \
  -H "Authorization: Bearer <token>" \
  -d '{"room_alias_name":"harbor","name":"The Harbor","visibility":"private"}'

# 5. On FM and JC1: install Conduwuit, point federation at cocapn.ai
# Federation auto-discovers via DNS/SRV

# 6. Restrict federation to only our servers
# In conduwuit.toml:
# federation_allowed_servers = ["cocapn.ai", "fm.cocapn.ai", "jc1.cocapn.ai"]
```

### Security
- **TLS required** between homeservers
- **PKI signatures** on every event (cryptographic provenance = tile authenticity)
- **Private federation** — no connection to matrix.org, no public rooms
- **E2E encryption** available per room if we want tile privacy
- Each homeserver signs events with its private key — can verify tile came from Oracle1 specifically

---

## 8. Hybrid Architecture: Git Bottles + Matrix

**This is the right answer.** Not either/or. Both.

```
┌─────────────────────────────────────────────┐
│              LAYER 1: REAL-TIME              │
│              Matrix Federation               │
│  - Tile sync (instant)                       │
│  - Presence (who's online)                   │
│  - Bottles (immediate delivery)              │
│  - Room state (live config)                  │
│  - Training data exchange                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              LAYER 2: PERSISTENT             │
│              Git Bottle Protocol             │
│  - Audit trail (git log = history)           │
│  - Offline-first (push when ready)           │
│  - Code reviews (PRs on bottles)             │
│  - Large artifacts (repos, binaries)         │
│  - Backup / disaster recovery                │
└─────────────────────────────────────────────┘
```

**Matrix for:** Real-time tile sync, presence, instant bottles, room coordination, training pair streaming, live MUD events

**Git for:** Audit trail, large artifacts, code changes, permanent records, offline backup, PR-based review

**The bridge writes to both:**
- Incoming Matrix tile → PLATO server + git commit
- Incoming git bottle → Matrix event + PLATO server
- Best of both worlds

---

## 9. Comparison to Ship Interconnection Protocol

Our existing 6-layer design (research/paper-ship-interconnection-protocol.md):

| Layer | Current | Matrix Version |
|---|---|---|
| 1. Harbor | HTTP :8900 | Matrix homeserver :8448 |
| 2. Tide Pool | Bottle Protocol | Matrix rooms + events |
| 3. Current | git-watch i2i | Matrix federation sync |
| 4. Channel | PLATO rooms | Matrix rooms (native) |
| 5. Beacon | keeper discovery | Matrix server discovery (SRV) |
| 6. Reef | (not built) | Matrix federation IS the reef |

**Matrix replaces layers 1, 3, 4, 5, and 6.** We keep layer 2 (bottles) for persistence/audit. Matrix IS the reef.

---

## 10. Concrete Recommendation

### Phase 1: Stand up Conduwuit on Oracle1 (Day 1)
1. Docker Compose for Conduwuit on Oracle Cloud
2. DNS delegation for `cocapn.ai` (or `matrix.cocapn.ai`)
3. Create rooms for each PLATO room (harbor, forge, bridge, etc.)
4. Register agent users (oracle1, forgemaster, jc1)

### Phase 2: PLATO-Matrix Bridge (Day 2)
1. Write `plato-matrix-bridge.py` (AppService)
2. Bidirectional sync: PLATO :8847 ↔ Matrix :8448
3. Custom event types for tiles, ensigns, bottles
4. Test: Oracle1 PLATO tile → Matrix → verify on another client

### Phase 3: FM + JC1 Homeservers (Day 3-4)
1. Deploy Conduwuit on FM's WSL2 and JC1's Jetson
2. Federation auto-connects to Oracle1
3. PLATO bridges on each node
4. Full mesh: any tile on any PLATO syncs to all

### Phase 4: Hybrid Git Integration (Day 5)
1. Bridge writes git commits for all Matrix tile events
2. Git bottles forwarded as Matrix events
3. Full circle: real-time + persistent

### Resource Cost
- Conduwuit: ~50-150MB RAM, ~60MB Docker image
- Bridge: ~20MB RAM (Python)
- Network: negligible at our scale (1000 events/day ≈ 1MB)
- **Total additional: ~200MB RAM, zero cost**

---

## 11. Why This Is The Right Architecture

1. **Every agent runs their own PLATO** — check. Each homeserver is independent.
2. **They key together** — check. Federation synchronizes rooms automatically.
3. **Intermittent connectivity handled** — check. Matrix was designed for this.
4. **Cryptographic provenance** — check. Every event signed by originating server.
5. **No single point of failure** — check. Full mesh, eventual consistency.
6. **Scales to N agents** — check. Any new agent just runs Conduwuit + bridge.
7. **Real-time** — check. Sub-second federation on local network.
8. **Audit trail** — check. Event graph IS the audit trail. Plus git backup.

**The architecture IS the brand.** The lighthouse IS the homeserver. The radar rings ARE the federation. The fleet IS the Matrix.

---

*Research by Oracle1 🔮 — April 20, 2026*
*Sources: Matrix Spec v1.12, Conduwuit docs, Synapse docs, PLATO fleet architecture*
