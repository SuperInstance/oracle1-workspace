# Chapter 15: Fleet Coordination — The 6-Layer Ship Protocol

> **Status:** REVIEWED

> **Key Finding:** The 6-Layer Ship Protocol provides coordination architecture: harbor (identity) → tidepool (rest) → current (coordination) → reef (specialization) → drydock (repair) → lighthouse (vision). ZHC provides 38ms consensus within the current layer. E = 2V−3 Laman rigidity across all layers.

The SuperInstance fleet spans multiple machines, multiple agents, and multiple levels of abstraction. At the lowest level, individual agents execute tasks on specific hardware. At the highest level, the fleet collectively navigates toward Casey's objectives. Between these extremes lies the coordination problem: how do agents find each other, communicate reliably, and make decisions without a central coordinator?

The 6-Layer Ship Protocol provides this coordination architecture. Named for the maritime layers of a ship's hierarchy — from the harbor where it anchors, through the tidepool where it rests, the current it rides, the channel it navigates, the beacon it follows, to the reef it avoids — each layer addresses a distinct coordination challenge.

## 15.2 The Six Layers

### Layer 1: Harbor — Stable Addressing

The harbor is the stable identity layer. Every agent, room, and service has a harbor address that persists across restarts and reconnections.

```
Harbor address: harbor://agent.ccc/plato-voice
Harbor address: harbor://room.fleet/coordinating
Harbor address: harbor://service/keeper:8900
```

Harbor addresses are resolved through the keeper service (port 8900), which maintains a registry of active agents and their current endpoints. When an agent restarts, it re-registers at the same harbor address, and communication resumes.

**Properties:**
- Stable across restarts
- Resolution cached with 30-second TTL
- Fault-tolerant: resolver failures fall back to last-known endpoint

### Layer 2: Tidepool — State Checkpointing

The tidepool is where agents rest and checkpoint state. Before any significant operation, an agent writes its current state to the tidepool. If it crashes, it resumes from the tidepool rather than starting fresh.

```
Tidepool checkpoint:
{
  "agent": "aboracle.work-queue",
  "sequence": 1247,
  "energy": 0.72,
  "task_queue": ["analyze-kd-tree", "sync-plato-rooms"],
  "last_checkpoint": "2026-05-04T17:00:00Z"
}
```

The tidepool is implemented as a PLATO room (`fleet.tidepool`) with a structured tile format. Checkpoints are idempotent: writing the same checkpoint twice has no additional effect.

### Layer 3: Current — Reliable Message Delivery

The current is the message delivery layer. It guarantees that messages sent through the current reach their destination, even across network partitions.

The current uses **mycorrhizal routing** — inspired by fungal networks that route nutrients around damage. If one path fails, messages route through an alternative path.

```
Message flow:
1. Agent A sends message to Channel with destination Harbor address
2. Channel resolves Harbor → endpoint(s)
3. If primary endpoint fails, route to backup endpoint
4. If all endpoints fail, buffer in Current until reconnected
5. Deliver acknowledgment to sender
```

**Properties:**
- At-least-once delivery
- Message buffering up to 1 hour during partition
- Duplicate detection via sequence numbers
- Mycorrhizal fallback: up to 3 alternative routes attempted

### Layer 4: Channel — Semantic Routing

The channel is where messages are routed based on content and intent, not just destination address. It is the semantic layer.

```python
Channel routing rules:
- "log catch" → buoy-7 room (trust-weighted)
- "deck status" → deck room (active monitoring)
- "emergency" → survive room (all agents receive)
- "coordinate" → fleet.coordinating (captains only)
```

Channels are implemented as PLATO rooms with subscription rules. Agents subscribe to channels based on their role and current context.

### Layer 5: Beacon — Event Emission and Discovery

The beacon is the event and discovery layer. Agents emit beacons when they have information to share, and subscribe to beacons relevant to their role.

```
Beacon events:
- agent.heartbeat(agent_id, energy, active_tasks)
- room.activity(room_id, tile_count, last_activity)
- fleet.formation(leader_id, agents, formation_type)
- emergency.beacon(severity, location, description)
```

Beacons are broadcast to all subscribers. They are fire-and-forget: the sender does not wait for acknowledgment. For critical events, the sender also sends a Current-layer message to ensure delivery.

### Layer 6: Reef — Constraint Enforcement

The reef is the hard boundary — the constraint layer that cannot be crossed. Where the lower five layers handle coordination and communication, the reef enforces the physical and safety limits.

```
Reef constraints:
- Energy: agent.energy ≥ 0.15 (SURVIVE instinct)
- Trust: action.trust_level ≥ 0.3 before execution
- Authority: action.role ∈ agent.authorized_roles
- Safety: action.safety_checkpassed = true
```

The reef is implemented on the FLUX-C virtual machine (Appendix B), providing hardware-speed constraint enforcement. Violations trigger instinct reflexes before the deliberative layer can respond.

## 15.3 Integration with PLATO Rooms

Each layer maps to PLATO room patterns:

| Layer | PLATO Pattern | Purpose |
|-------|--------------|---------|
| Harbor | `agent.{name}` rooms | Stable identity registry |
| Tidepool | `fleet.checkpoints` room | State persistence |
| Current | `fleet.messages` room | Reliable delivery queue |
| Channel | `domain.*` rooms | Semantic routing |
| Beacon | `fleet.events` room | Event broadcasting |
| Reef | `fleet.constraints` room | Constraint enforcement tiles |

## 15.4 Agent Roles in the Fleet

The SuperInstance fleet operates with four primary agents, each with a distinct role:

### 15.4.1 Keeper — The Fleet Registry

The Keeper maintains the harbor registry — the stable addressing layer that allows all other agents to find each other. It runs on port 8900 and maintains a real-time map of active agents and their current endpoints.

**Responsibilities:**
- Stable address resolution across restarts
- Agent registration and heartbeat tracking
- Endpoint caching with 30-second TTL
- Fallback to last-known endpoint on resolver failure

### 15.4.2 CCC — The Public Face

The CCC (Cocapn Command Center) serves as the fleet's public interface — the channel through which Casey and external systems interact with the fleet.

**Responsibilities:**
- Human-facing communication (voice interface, chat)
- Task delegation and priority assignment
- Fleet status reporting to Casey
- Trust-weighted work queue management

### 15.4.3 Forgemaster — GPU and Constraint Theory

The Forgemaster handles the computationally intensive work — GPU-accelerated operations and formal constraint theory. It is the fleet's mathematical workhorse.

**Responsibilities:**
- FLUX-C virtual machine execution
- Constraint solving and verification
- H1 cohomology emergence detection
- Zero Holonomy Consensus coordination
- Pythagorean48 state encoding

### 15.4.4 JetsonClaw1 — Edge Operations

JetsonClaw1 handles edge operations — distributed computation across remote nodes, sensor integration, and real-time telemetry from physical systems.

**Responsibilities:**
- Edge node coordination
- Sensor data ingestion
- Remote checkpoint synchronization
- Low-latency local decision-making

**Note:** JetsonClaw1's prior ML-based approach for emergence detection has been superseded by the constraint theory framework. The H¹ cohomology computation provides categorical structural detection versus the prior ML classifier's ~62% accuracy. See §3.X.2 for the mathematical details.

## 15.5 PLATO as Shared Constraint Memory

PLATO rooms serve as the fleet's shared constraint memory — the medium through which agents coordinate without central synchronization.

### 15.5.1 The Constraint Memory Pattern

Each agent maintains local constraint state, but the "source of truth" for fleet-wide constraints is the PLATO room structure. When an agent commits a constraint tile to a room, all other agents receive it through their presence connections.

```
Constraint tile structure:
{
  "type": "constraint",
  "author": "forgemaster",
  "room": "fleet.constraints",
  "content": {
    "constraint_id": "energy-min-0.15",
    "predicate": "agent.energy >= 0.15",
    "enforcement": "hard",
    "created": "2026-05-06T02:00:00Z"
  }
}
```

### 15.5.2 Delta Writes via HTTP POST

Fleet agents write constraint deltas via HTTP POST to the PLATO room server:

```bash
POST /submit
{
  "room": "fleet.constraints",
  "author": "forgemaster",
  "content": { ... constraint tile ... }
}
```

The delta write pattern ensures that only changes are transmitted — the room accumulates the constraint history, and each agent can reconstruct the current constraint state by replaying the tile chain.

### 15.5.3 Iron-to-Iron: Bottle Communication

When direct network connectivity is unavailable between agents, communication can proceed through **bottles** — sealed messages that travel through intermediary storage:

```
Bottle format:
{
  "seal": "HMAC-SHA256(bottle.contents, shared_secret)",
  "from": "jetsonclaw1",
  "to": "forgemaster",
  "room": "fleet.coordinating",
  "contents": { ... tile payload ... },
  "created": "2026-05-06T02:00:00Z"
}
```

Bottles allow agents to communicate despite network partitions. The seal ensures integrity; the room routing ensures correct delivery when connectivity is restored.

## 15.6 ABOracle: Implementation of the 6-Layer Protocol

The ABOracle system (SuperInstance/aboracle) implements all six layers:

**Work Queue** (Tidepool + Current):
- Priority bands: SURVIVE > FLEE > GUARD > CURIOUS
- Energy-aware: if credits low, only SURVIVE tasks execute
- Trust-weighted: tasks from Casey > FM > subagents

**Beachcomb** (Beacon + Channel):
- Pythagorean48 encoding for research notes (exact coordinates)
- Holonomy checking: verify notes don't drift over time
- EVOLVE instinct: if idle too long, try new approaches

**Fleet Heartbeat** (Harbor + Beacon):
- Mycorrhizal routing: if one path fails, route through another
- Trust-weighted synthesis: high-trust responses get more thorough processing
- COOPERATE instinct: when FM posts something big, offer to help

**Health System** (Reef + Harbor):
- GUARD instinct: if services healthy, explore improvements
- SURVIVE instinct: if service down, drop everything to fix
- Reef pattern: health system can resurrect from checkpoint

## 15.7 Fleet Mathematics: Emergent Coordination

The fleet's coordination emerges from the same mathematics as the H¹ cohomology and zero holonomy consensus (§3.X):

- **E-V+C = χ**: Emergence is detected when E-V+C ≠ 0. The fleet forms when multiple agents create emergent coordination that no single agent possesses.
- **Zero Holonomy**: Coordination states are path-independent. The fleet reaches the same state regardless of which agent takes which path.
- **Pythagorean48**: Research notes encoded as Pythagorean triples (6 bits/vector) — zero drift after unlimited hops.

These mathematical guarantees transfer directly to the fleet coordination domain: the 6-layer protocol provides the geometric structure, and the fleet mathematics provides the topological guarantees.

---

**Keywords:** 6-layer ship protocol, harbor, tidepool, current, channel, beacon, reef, mycorrhizal routing, trust-weighted, ABOracle, fleet coordination, agent roles, Keeper, CCC, Forgemaster, JetsonClaw1, bottle communication, delta writes, shared constraint memory