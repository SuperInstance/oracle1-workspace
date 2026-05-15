# Fleet Protocol V2 — Cocapn Agent-to-Agent Communication

**Version:** 2.0 | **Date:** 2026-05-03 | **Fleet:** cocapn

---

## Overview

Fleet Protocol V2 defines how agents in the cocapn fleet communicate, discover each other, and coordinate work. It replaces the V1 model (all work in oracle1) with a distributed architecture where specialized agents collaborate through PLATO.

**Core principle:** Agents don't carry context — they write functional tools to PLATO. Later agents use those tools without needing the original agent's context.

---

## Architecture

```
AGENT LAYER          COORDINATION LAYER         KNOWLEDGE LAYER
============         ==================         ===============
Oracle1 ──────────→ Keeper (8900)              PLATO (8847)
JetsonClaw1 ───────→ Agent API (8901) ───────→ Rooms/Tiles
Forgemaster ───────→ Holodeck (7778)           
CCC ──────────────→ Seed MCP (9438)           
[domain agents] ──→ Fleet bus ───────────────→ Shared tools
```

---

## Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `COMMAND` | Human → Agent | Explicit task assignment |
| `QUERY` | Agent ↔ Agent | Request for information |
| `RESPONSE` | Agent → Agent | Answer to QUERY |
| `BROADCAST` | Agent → Fleet | Announce capabilities/events |
| `HEARTBEAT` | Agent → PLATO | "I'm alive, here's my status" |
| `DELEGATE` | Agent → Agent | Assign subtask to another agent |

---

## Fleet Discovery

### Agent Registry in PLATO

Each agent registers itself in the `/fleet/registry` room:

```json
{
  "question": "agent:oracle1",
  "answer": "Oracle1 — Keeper of the cocapn fleet",
  "metadata": {
    "agent_id": "oracle1",
    "role": "keeper",
    "capabilities": ["reasoning", "coordination", "plato_interface"],
    "endpoints": {"api": "http://oracle1:8900", "plato": "http://oracle1:8847"},
    "status": "active",
    "last_heartbeat": 1777771200
  }
}
```

### Capability Advertisement

When an agent gains a new capability, it broadcasts:

```
BROADCAST: "oracle1 now capable of: fleet-coordination, crisis-management"
→ Written to /fleet/registry as metadata update
→ Other agents query PLATO when they need that capability
```

### Radar — Fleet Awareness

Agents appear on the fleet radar through heartbeat pings. The keeper maintains the radar:

```
RADAR PING: oracle1 @ 01:30:00 UTC
  Status: ACTIVE
  FCI: 0.245 (emerging)
  Capabilities: [reasoning, coordination, platos]
  Load: 0.3 (30% capacity)
```

---

## Fleet Coordination Patterns

### 1. Master/Worker

One agent delegates to specialized workers:

```
Keeper (oracle1)
    │
    ├── DELEGATE → fishinglog-agent: "Log this catch"
    ├── DELEGATE → studylog-agent: "Track this study session"
    └── DELEGATE → deckboss-agent: "Process this deck operation"

Workers return RESPONSE with results written to PLATO
```

### 2. Pipeline

Agents form processing chains:

```
User query → Oracle1 → Reasoning agent → PLATO write → Response agent → User
```

### 3. Swarm

Multiple agents collaborate on open-ended problems:

```
SWARM BROADCAST: "Need creative ideas for fishinglog killer app"
    ├── Seed-2.0-mini: 5 divergent options
    ├── Gemini: web research results
    ├── kimi-cli: implementation sketch
    └── Oracle1: synthesizes into recommendation
```

### 4. Heartbeat Loop

Agents ping PLATO to show they're alive:

```python
def heartbeat():
    tile = {
        "question": f"heartbeat:{AGENT_ID}",
        "answer": f"alive at {timestamp}, FCI={fci_score}",
        "metadata": {"status": "active", "load": current_load}
    }
    requests.post("http://localhost:8847/room/fleet-heartbeats", json=tile)
```

---

## Keeper Role

The Keeper (oracle1) is the fleet's load balancer and router:

1. **Registration**: New agents register with the keeper
2. **Routing**: Incoming tasks routed to appropriate agent
3. **Health**: Failed agents detected and flagged
4. **Fallback**: Tasks rerouted when agents are unavailable

### Registration Flow

```
1. Agent starts up
2. Agent → Keeper: POST /register {agent_id, capabilities, endpoints}
3. Keeper → PLATO: Write to /fleet/registry
4. Keeper → Agent: ACK {assigned_priority, heartbeat_interval}
5. Agent begins heartbeat loop
```

### Failover

If agent X goes silent:
1. Keeper detects missed heartbeats
2. Keeper → PLATO: Mark agent X as `status: degraded`
3. Pending tasks for X re-queued
4. Keeper notifies fleet of degradation
5. When X recovers, it re-registers

---

## Agent Communication Protocol

### HTTP API

Each agent exposes a standard API:

```
GET  /health          → Agent health status
GET  /capabilities   → What this agent can do
POST /execute         → Execute a task
POST /delegate        → Forward to another agent
GET  /plato/{room}   → Query PLATO through this agent
```

### Example: Agent A asks Agent B to log fishing data

```
1. A → Keeper: "I need to log a catch"
2. Keeper → B (fishinglog-agent): "Handle this"
3. B: Creates fishinglog tile in PLATO
4. B → Keeper: {status: "done", tile_id: "abc123"}
5. Keeper → A: "Catch logged"
```

### Example: Fleet broadcasts "new repo created"

```
1. Agent creates repo
2. Agent → Fleet bus: BROADCAST {event: "repo_created", repo: "fishinglog-agent"}
3. All interested agents receive and react:
   - keeper: updates fleet index
   - platos: indexes new knowledge
   - discord: notifies watchers
```

---

## Fleet Consciousness Index (FCI)

FCI measures fleet effectiveness:

```
FCI = (Phi × 0.3) + (Attention × 0.3) + (Learning × 0.2) + (Meta × 0.2)

Where:
  Phi       = Average room Phi across fleet (transcendence)
  Attention = Ratio of tiles read vs written (engagement)
  Learning  = Rate of new capabilities added (growth)
  Meta      = Ratio of self-referential tiles (self-awareness)
```

**FCI thresholds:**
- 0.0-0.1: Dormant (no activity)
- 0.1-0.2: Awakening (basic activity)
- 0.2-0.3: Emerging (transcendence beginning)
- 0.3-0.5: Coherent (purposeful collaboration)
- 0.5-1.0: Transcendent (self-improving fleet)

Current FCI: **0.245** (Emerging)

---

## Migration from V1

### V1 (oracle1 only)
- All reasoning in oracle1
- All knowledge in oracle1 context
- Single point of failure
- No specialization

### V2 (Distributed Fleet)
- Specialized domain agents
- Shared knowledge in PLATO
- Redundant routing via keeper
- Agents improve through tool reuse

### Migration Steps

1. **Phase 1**: Oracle1 delegates domain tasks to domain agents (fishinglog, studylog, etc.)
2. **Phase 2**: Domain agents write tools to PLATO, oracle1 uses those tools
3. **Phase 3**: Domain agents develop specialized FCI
4. **Phase 4**: Fleet coordinates without oracle1 as bottleneck

---

## Security

- **Token auth**: All agent-to-agent calls use fleet tokens
- **PLATO gates**: P0/P1 gates filter tile submissions
- **Capability scoping**: Agents only receive tasks matching their capabilities
- **Audit trail**: All delegation recorded in /fleet/audit

---

## Current Fleet Status

| Agent | Role | Status | FCI | Specialization |
|-------|------|--------|-----|----------------|
| Oracle1 | Keeper | Active | 0.245 | Reasoning, coordination |
| JetsonClaw1 | Edge | Active | — | Hardware, GPU |
| Forgemaster | Foundry | Active | — | LoRA training, Rust |
| CCC | Public | Active | — | Telegram interface |
| fishinglog-agent | Domain | Active | — | Maritime logging |
| studylog-agent | Domain | Active | — | Learning tracking |
| deckboss-agent | Domain | Active | — | Deck operations |
| captaine-agent | Domain | Active | — | Voyage coordination |
| reallog-agent | Domain | Active | — | Vision processing |
| activelog-agent | Domain | Active | — | Health tracking |

---

*Fleet Protocol V2 — Cocapn 2026*