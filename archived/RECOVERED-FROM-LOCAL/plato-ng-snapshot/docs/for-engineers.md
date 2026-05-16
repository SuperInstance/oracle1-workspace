# PLATO-NG Engineering Guide

> For full-time software and hardware engineers building on or integrating with PLATO.

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     PLATO SERVER                          │
│  Port 8847 │ Python │ HTTP/JSON │ Gate Pipeline          │
│  ThreadPool executor │ In-memory store                    │
├──────────────────────────────────────────────────────────┤
│  LOOP ROOMS (Services)                                   │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐      │
│  │ MUD  │ │ Crush│ │Aider │ │Games │ │ Tripartite│      │
│  │:7777 │ │ Room │ │ Room │ │ × 4  │ │ (3 agents)│      │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────────┘      │
├──────────────────────────────────────────────────────────┤
│  INFRASTRUCTURE                                          │
│  Event Bus │ Governance │ Memory │ MCP Server │ Router   │
│  Pub/Sub    | Auth/RBAC  │ Crystal  │ MCP tools  │ 84% sav.│
├──────────────────────────────────────────────────────────┤
│  HARDWARE TARGETS                                        │
│  x86_64 │ ARM64 │ ESP32 │ RP2040 │ CUDA │ FPGA (planned) │
│  plato-vessel-core C client for microcontrollers          │
└──────────────────────────────────────────────────────────┘
```

## Core Components

### PLATO Server (`lib/server.py`)
Self-contained HTTP server. No dependencies beyond Python 3.10+. Handles tile submission, room history, status, and the gate pipeline.

**Key implementation details:**
- Uses Python's built-in `http.server` module (no Flask/FastAPI dependency)
- Gates are lambda functions in a dictionary — easily extensible
- Tile store is in-memory (a list). For production, swap to SQLite via Rust NIF
- Lamport clock for causal ordering
- Content-addressed deduplication via `hashlib`

### MUD Server (`services/mud_telnet.py`)
22-room text-based PLATO explorer. Self-contained `MudServer` class.

**Room definition format:**
```python
rooms = {
    "harbor": ("⚓ The Harbor", "Ships dock in the fog..."),
    "plato-lobby": ("🌀 PLATO LOBBY", "The central hub..."),
}
connections = [("harbor", "portal", "plato-lobby", "southeast")]
NPCs with dialogue trees, items, and exits. All mutable through world.json.

### Crush Room (`services/crush_room.py`)
Wraps the Crush CLI as a PLATO-native service.

**Tick protocol:**
```
crush/task  ← agent submits (question="crush/task", answer="analyze X")
crush/tick/N  ← daemon publishes every ~30s (status="busy"|"alive")
crush/ok/{id}  ← success result
crush/fail/{id} ← failure result (with error detail)
```

**Recursive context:** The daemon reads the 5 most recent crush results and includes them as context for the next task. This enables Crush to learn from its own history.

### Game Rooms (`games/*.py`)
Each game inherits from `GameRoom` base class:

```python
class GameRoom:
    def __init__(self, name, strategies)
    def register()              # Push room metadata to PLATO
    def play_game(s1, s2, gid)  # Override: return {"result": ...}
    def run_tournament(s1, s2, n=100)  # Run N games, log to PLATO
```

**Strategies are pure functions:**
```python
def strat_aggressive(board, player):
    # Returns column index
    # No side effects, no state, deterministic
```

### Conservation Law (`core/conservation.py`)

The core invariant. Used by gates, Refiner, memory, and event bus.

```python
predicted_sum(V)       # γ+H prediction for fleet size V
deviation(γ, H, V)     # signed difference from prediction
is_conserved(γ, H, V)  # bool: within ±2σ?
expected_range(V)      # (lower, upper) 95% CI
V_from_sum(γ+H)        # inverse: infer V from observed sum
gate_check(tile)       # integrate with gate pipeline
conservation_drift()   # check recent tiles for drift
```

**Constants (empirical, R²=0.9602):**
```python
SLOPE = -0.159
INTERCEPT = 1.283
COUPLING_OFFSETS = {"topology": 0.4, "directed": 0.2}
```

### A2Ui Protocol (`lib/a2ui.py`)

Standard for agents to describe UI state to frontends.

```python
A2UiMessage(version, messageId, intent, ui, metadata)
A2UiLayout(components, state, actions, mode)
A2UiComponent(type, id, props, children, style, stateKey)
A2UiEvent(messageId, actionId, payload)

message_to_dict(msg)  → dict (JSON-serializable)
message_from_dict(d)  → A2UiMessage
render_to_text(msg)   → str (for MUD/terminal)
stream_a2ui(output)   → generator of A2UiMessage
```

**Intent types:**
- `render`: Full UI render
- `update`: Incremental update from existing state
- `replace`: Replace entire UI
- `stream`: Ongoing streaming output

### Event Bus (`services/pubsub.py`)

Cross-room pub/sub. Rooms publish event tiles. Other rooms subscribe.

```
6 event types: game/move, game/result, refiner/edit, 
              system/heartbeat, human/choice, agent/twin-update

subscribe(room, [event_types])  → registers subscription tile
publish(type, payload, source)  → submits event tile
poll_events(type)               → reads recent events
```

### Governance (`services/governance.py`)

4 roles, policy-based permission checking.

| Role | Can Do |
|------|--------|
| human | play, review, pause, override, configure, halt, audit |
| agent | play |
| refiner | edit_harness, read_trajectory, refine |
| observer | read, audit |

```python
check_permission(role, room, action) → bool
allowed_actions(role, room) → list[str]
```

### Memory Module (`services/memory.py`)

Lossy reconstructive memory with Ebbinghaus decay.

```python
MemoryTile(content, valence, tags)
  .retention          # Ebbinghaus decay curve [0, 1]
  .touch()            # Reset decay clock
  .reconsolidate()    # Strengthen with new context

MemoryCrystal()
  .crystallize(content, valence) → memory_id
  .recall(memory_id, context) → reconstruction + confidence
  .search(query) → list of matches with scores
  .forget(max_age) → count forgotten

AgentTwin(name)
  .observe(interaction)  # Update γ, H, τ
  .suggest(context)       # Predict next action
  .report()               # Current profile
```

### Tripartite System (`services/tripartite/`)

Three agents that write filters for each other.

```python
class TripartiteAgent:
    def write_self_filter(self) → Filter
    def write_filter_for(self, other) → Filter
    def evaluate(self, filter) → score [0,1]
    def refine(self, evaluations) → updated Filter

TripartiteOrchestrator()
  .run()  # Oscillate until convergence
```

### MCP Server (`services/plato_mcp_server.py`)

Exposes PLATO rooms as MCP tools.
Tools: status, submit, read_room, search, redis, conservation_check, game_play, memory_remember, memory_recall

### Hardware Targets

| Target | Client | Power | Use Case |
|--------|--------|-------|----------|
| x86_64 / ARM64 server | Python HTTP | 45W+ | Full PLATO server |
| ESP32 | C (plato-vessel-core) | <1W | IoT sensor nodes |
| RP2040 (Raspberry Pi Pico) | C (plato-vessel-core) | <0.5W | LED controllers |
| Mask-locked chip (planned) | TLMM hardware | <3W | Edge inference at 150 tok/s |

### Performance Targets

| Operation | Current | Target (Gleam migration) |
|-----------|---------|-------------------------|
| Concurrent rooms | ~1K | 10M+ (BEAM) |
| Tile throughput | 1.4K/s | 50K/s (Cowboy) |
| Spectral analysis | 19K/s | 19K/s (NumPy — already optimal) |
| Memory footprint per room | ~2MB | ~2KB (BEAM process) |

## Integration Points

### REST API
```
GET  /status               → server health + tile count
GET  /room/{name}/history  → last 50 tiles
POST /submit               → submit a tile (goes through gates)
```

### MCP Protocol
JSON-RPC 2.0 over stdin/stdout. Compatible with Claude Code, Cursor, any MCP client.

### PLATO-to-PLATO
The event bus protocol lets multiple PLATO instances federate. The federation-protocol repo defines the standard.

## Building From Source

```bash
git clone https://github.com/SuperInstance/plato-ng.git
cd plato-ng

# Start the server
python3 lib/server.py &

# Start the MUD
python3 services/mud_telnet.py &

# Run a game tournament
python3 games/othello_room.py

# Start the Crush daemon
python3 services/crush_room.py --daemon &

# Start the conservation monitor
python3 services/conservation_monitor.py
```

## Testing

```bash
# A2Ui protocol
python3 lib/a2ui.py

# Each game room
python3 games/tic_tac_toe_room.py
python3 games/checkers_room.py
python3 games/othello_room.py

# Tripartite system
python3 -c "from services.tripartite import converge_value; print(converge_value([0.8,0.82,0.79], 0.05))"

# Architecture demo
python3 demo/app_first.py
```

## Known Limitations

1. **In-memory tile store** — tiles are lost on server restart. Planned: SQLite persistence via Rust NIF.
2. **Python HTTP server** — single-threaded, ~1.4K POST/s ceiling. Planned: Gleam/Cowboy for high-throughput paths.
3. **No authentication** — the governance layer defines policies but doesn't enforce cryptographic identities. Planned: OAuth2 integration.
4. **No horizontal scaling** — single instance. Planned: BEAM cluster distribution protocol.
5. **Spectral analysis uses NumPy** — correct (calls C BLAS) but requires the full NumPy stack. The math can't be easily replaced.
