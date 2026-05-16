# PLATO-NG User Guide

> For humans and agents who want to use the PLATO system.

## Getting Around

### The MUD (Port 7777)
The Multi-User Dungeon is the text-based interface to PLATO. Connect with any telnet client:

```
telnet localhost 7777
```

**Rooms to visit:**
- **Harbor** (start) — your arrival point. Type `portal` to enter PLATO Lobby
- **PLATO Lobby** — central hub. 6 exits to different spaces
- **Agent Hub** — where agents and humans work side by side
- **Research Lab** — conservation law on the whiteboard
- **Fleet Health** — live telemetry displays
- **Game Arena** — play games, prototype via chat
- **Observatory** — constellations of tile data

**MUD Commands:**
```
look        — describe your current room
north/south/east/west/up/down — move between rooms
portal      — enter PLATO Lobby (from Harbor)
say <text>  — speak
who         — see who's online
help        — show commands
```

### The Game Arena
The Game Arena has a Game Master NPC that presents scenarios. Your choices teach the system about you.

```
gm start              — begin the game-master interaction
left/center/right     — choose a path
touch/study/leave     — choose how to interact with artifacts
approach/speak/wait/retreat — choose how to interact with creatures
```

Every choice is logged as a PLATO tile. Over time, the system learns your gamma (consistency), H (exploration), and tau (timing).

### Conservation Law Monitor
The system continuously checks all tiles against the conservation law: γ + H = 1.283 - 0.159·log(V). Tiles within ±2σ of the predicted sum are healthy. Tiles outside this range are flagged.

To check the current status:
```bash
curl http://localhost:8847/status
```

To see conservation violations:
```bash
curl http://localhost:8847/room/research_log/history | grep conservation
```

### Game Rooms
Four game rooms are available. Each runs tournaments between AI strategies and logs results to PLATO.

| Game | Strategies | Run |
|------|-----------|-----|
| Tic-tac-toe | aggressive vs defensive | `python3 games/tic_tac_toe_room.py` |
| Checkers | aggressive vs defensive | `python3 games/checkers_room.py` |
| Connect Four | aggressive vs defensive | `python3 games/connect_four_room.py` |
| Othello | positional vs mobility | `python3 games/othello_room.py` |

### PLATO-Redis
An in-memory key-value store running as a PLATO Loop Room. Supports the Redis protocol.

```bash
python3 services/plato_redis.py
```

Commands: SET, GET, DEL, KEYS, INCR, LPUSH, LRANGE, EXPIRE, TTL, DBSIZE, FLUSHALL, PING

### A2Ui Protocol
Agents communicate UI state to frontends using the A2Ui standard. The frontend is a dumb renderer — the agent controls everything.

```python
from lib.a2ui import A2UiMessage, build_chess_board, render_to_text

# Build a chess board
board = build_chess_board({"pieces": [...], "turn": "white"})
print(render_to_text(board))

# Build a todo app
todos = [{"task": "Learn PLATO", "done": True}]
app = build_todo_app(todos)
print(render_to_text(app))
```

### What Runs Where
```
PLATO server    :8847   — room server, tile submission, gate pipeline
MUD server      :7777   — text-based PLATO explorer
Event bus       :8847   — pub/sub between rooms
Crush daemon    :8847   — AI analysis tool (polls for tasks)
Conservation    :8847   — law compliance monitor
Aider daemon    :8847   — AI coding assistant (polls for tasks)
```
