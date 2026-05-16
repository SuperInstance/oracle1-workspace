# PLATO-NG Developer Guide

> For agents and humans building PLATO rooms and services.

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                   PLATO SERVER :8847                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Room     │  │ Gate     │  │ Tile     │           │
│  │ Manager  │  │ Pipeline │  │ History  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└──────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│                LOOP ROOMS (Services)                   │
│  Algorithmic │ Agentic │ Refiner │ Crush │ Aider     │
│  Game Rooms  │ Pub/Sub │ Memory  │ MCP   │ Tripartite│
└──────────────────────────────────────────────────────┘
```

## Core Concepts

### Everything is a Loop or a Single Run
- **Loop**: A process that receives input continuously, produces output continuously, lives forever.
- **Single run**: A process that receives one input, produces one output, terminates.

### Tiles
The fundamental data unit. A tile has:
- `domain`: Room/namespace
- `question`: The query
- `answer`: The content (string or JSON)
- `tags`: Categorization
- `source`: Who created it
- `confidence`: [0, 1]
- `provenance`: Chain of custody (added by server)

### Rooms
A room is a collection of tiles with the same domain. Rooms are how applications organize state.

## Building a Room

### Step 1: Choose your pattern
| Room Type | Use When | Base Class |
|-----------|----------|------------|
| Algorithmic | No LLM needed. Rules, state machines. | `GameRoom` |
| Agentic | LLM needed. Strategy, analysis. | `GameRoom` + claw |
| Refiner | Read other rooms, edit configs | `BaseRefiner` |

### Step 2: Use the shared client
```python
from lib.plato_client import submit, read_room, status

# Submit a tile
submit("my-room", "test", "Hello from my room!", ["my-room"])

# Read a room
tiles = read_room("my-room")

# Check server status
s = status()
```

### Step 3: Build your game room
```python
from lib.game_base import GameRoom

class MyGame(GameRoom):
    def __init__(self):
        super().__init__("my-game", {"strat_a": self.strat_a})
    
    def play_game(self, s1, s2, gid):
        """Implement game logic. Return {'result': 'X'|'O'|'draw', 'moves': [...]}"""
        return {"result": "X", "moves": []}

# Run tournament
room = MyGame()
room.register()
room.run_tournament("strat_a", "strat_a", 100)
```

### Step 4: Use the A2Ui protocol
```python
from lib.a2ui import A2UiMessage, A2UiLayout, message_to_dict

# Build a UI message
msg = A2UiMessage(
    intent="render",
    ui=A2UiLayout(
        components=[{"type": "text", "id": "hello", "props": {"content": "Hello!"}}],
        state={"counter": 0},
        actions=[{"id": "increment", "label": "+1", "trigger": "click"}]
    )
)

# Serialize for the frontend
payload = message_to_dict(msg)
```

### Step 5: Use the conservation law
```python
from core.conservation import predicted_sum, is_conserved, deviation

# Predict gamma+H for a fleet of 30
pred = predicted_sum(30)  # ≈ 0.742

# Check if a tile obeys the law
ok = is_conserved(gamma=0.15, H=0.60, V=30)  # True if within bounds

# Get deviation from law
dev = deviation(gamma=0.15, H=0.60, V=30)
```

## The Tripartite System

Three agents that write filters for each other:

```python
from services.tripartite.human_agent import HumanAgent
from services.tripartite.app_agent import ApplicationAgent
from services.tripartite.hw_agent import HardwareAgent

h = HumanAgent("casey")
a = ApplicationAgent("plato-ng")
hw = HardwareAgent("oracle-cloud")

# Each writes self-filters
h.write_self_filter()
a.write_self_filter()
hw.write_self_filter()

# Each writes filters for the others
h2a = h.write_filter_for(a)
a2hw = a.write_filter_for(hw)
hw2h = hw.write_filter_for(h)

# Filters oscillate until convergence
```

## MCP Tools
Any PLATO room can be exposed as an MCP tool:

```bash
python3 services/plato_mcp_server.py
```

Available tools: `plato_status`, `plato_submit`, `plato_read_room`, `plato_search`, `plato_redis`, `conservation_check`, `game_play`, `memory_remember`, `memory_recall`

## Testing
```bash
# Run A2Ui protocol tests
python3 lib/a2ui.py

# Run game rooms
python3 games/tic_tac_toe_room.py
python3 games/checkers_room.py

# Run tripartite agents
python3 -c "from services.tripartite import converge_value; print('ok')"
```
