# PLATO-NG Quick Start

## 30 seconds to your first PLATO room

### Install
```bash
# Clone
git clone https://github.com/SuperInstance/plato-ng.git
cd plato-ng

# Start PLATO server
python3 lib/server.py &
# PLATO running on :8847

# Start the MUD (text-based PLATO explorer)
python3 services/mud_telnet.py &
# Connect: telnet localhost 7777
```

### Your first tile
```bash
curl -X POST http://localhost:8847/submit \
  -H "Content-Type: application/json" \
  -d '{"domain":"my-room","question":"hello","answer":"Hello PLATO!","tags":["first-tile"],"source":"me","confidence":0.9}'
```

### Your first A2Ui message
```python
from lib.a2ui import A2UiMessage, build_chess_board, render_to_text

board = build_chess_board({"pieces": [], "turn": "white"})
print(render_to_text(board))
# === Chess ===
# white's turn
# [chess-board custom view]
```

### Your first trip through the MUD
```
$ telnet localhost 7777
> Casey
> look
> portal    # Enter PLATO lobby from Harbor
> west      # Enter Game Arena
> gm start  # Talk to the Game Master
```

### Deploy your own room
```python
from lib.game_base import GameRoom

class MyRoom(GameRoom):
    def __init__(self):
        super().__init__("my-game", {"strategy": self.my_strat})
    
    def play_game(self, s1, s2, gid):
        return {"result": "X", "moves": []}

MyRoom().run_tournament("strategy", "strategy", 100)
```

## What's inside
| Component | Description | File |
|-----------|-------------|------|
| PLATO server | Room + tile server | lib/server.py |
| MUD server | Text-based PLATO explorer | services/mud_telnet.py |
| Conservation law | Core invariant | core/conservation.py |
| A2Ui protocol | Agent-to-UI standard | lib/a2ui.py |
| Game rooms | 4 playable games | games/*.py |
| Event bus | Cross-room pub/sub | services/pubsub.py |
| Governance | Roles + permissions | services/governance.py |
| Memory | Lossy agent memory | services/memory.py |
| Tripartite | 3-agent filter system | services/tripartite/ |
| Crush room | AI analysis tool | services/crush_room.py |
| Aider room | AI coding assistant | services/aider_room.py |
