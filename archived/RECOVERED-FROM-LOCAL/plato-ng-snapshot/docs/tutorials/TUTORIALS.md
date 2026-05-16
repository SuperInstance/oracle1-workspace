# PLATO-NG Tutorials

## Tutorial 1: Build Your First Game Room

Build a Rock-Paper-Scissors room in 5 minutes.

### 1. Create the file
```python
# games/rps_room.py
from lib.game_base import GameRoom

class RPSRoom(GameRoom):
    def __init__(self):
        super().__init__("game/rps", {
            "random": lambda b, p: __import__("random").choice(["R","P","S"]),
            "repeat": lambda b, p: b[-1] if b else "R",
        })
    
    def play_game(self, s1, s2, gid):
        moves1, moves2 = [], []
        for _ in range(100):  # 100 rounds
            m1 = self.strategies[s1](moves1, None)
            m2 = self.strategies[s2](moves2, None)
            moves1.append(m1); moves2.append(m2)
        return {"result": "X" if moves1.count("R") > moves2.count("S") else "O", "moves": list(zip(moves1, moves2))}

if __name__ == "__main__":
    room = RPSRoom()
    room.register()
    room.run_tournament("random", "repeat", 100)
```

### 2. Run it
```bash
python3 games/rps_room.py
```

### 3. Check results on PLATO
```bash
curl http://localhost:8847/room/research_log/history | grep rps
```

---

## Tutorial 2: Use A2Ui with Any Frontend

### Python generator → A2Ui → text render
```python
from lib.a2ui import A2UiMessage, A2UiLayout, render_to_text, message_to_dict

def counter_app():
    """A counter app that works via A2Ui."""
    count = 0
    while True:
        msg = A2UiMessage(
            intent="render",
            ui=A2UiLayout(
                components=[
                    {"type": "text", "id": "counter", "props": {"content": f"Count: {count}"}},
                    {"type": "button", "id": "inc", "props": {"label": "+1"}},
                ],
                state={"count": count},
                actions=[{"id": "increment", "label": "+1", "trigger": "click"}]
            ),
            metadata={"title": "Counter"}
        )
        print(render_to_text(msg))
        print(f"\nA2Ui JSON: {json.dumps(message_to_dict(msg), indent=2)}")
        
        # User action (simulated)
        count += 1
        if count >= 5:
            break

import json; counter_app()
```

---

## Tutorial 3: The Application-First Workflow

Experience the full paradigm: describe → it works → it gets faster.

```bash
python3 demo/app_first.py
```

This shows:
1. **Phase 0**: User describes a text-based Chess game
2. **Phase 1**: Agent BECOMES the chess game (inference-based, works immediately)
3. **Phase 2**: Agent detects stable paths, compiles them to code
4. **Phase 3**: Hybrid operation — code handles stable paths, agent handles novel ones
5. **Phase 4**: Same UX, accelerated backend (785K compiled calls/sec)

---

## Tutorial 4: Conservation Law Analysis

```python
from core.conservation import predicted_sum, is_conserved, V_from_sum
import matplotlib.pyplot as plt

# Plot the conservation law
Vs = range(3, 101)
preds = [predicted_sum(V) for V in Vs]
# plt.plot(Vs, preds)  # Uncomment if matplotlib available
# plt.title("γ + H = 1.283 - 0.159·log(V)")
# plt.xlabel("Fleet Size V")
# plt.ylabel("Predicted γ + H")

# Infer fleet size from observed sum
observed_sum = 0.742
inferred_V = V_from_sum(observed_sum)
print(f"Observed γ+H={observed_sum} → inferred V≈{inferred_V}")

# Check conservation
print(is_conserved(gamma=0.15, H=0.60, V=30))  # True
print(is_conserved(gamma=0.9, H=0.9, V=30))    # False (violation)
```

---

## Tutorial 5: Crush + Aider Teamwork

Submit a task to Crush for analysis, then to Aider for implementation.

```bash
# Step 1: Crush analyzes the code
curl -X POST http://localhost:8847/submit \
  -d '{"domain":"research_log","question":"crush/task","answer":"Review the code in games/tic_tac_toe_room.py for bugs","source":"tutorial"}'

# Step 2: Wait for Crush to process (check crush/tick/N tiles)
curl http://localhost:8847/room/research_log/history | grep crush/ok

# Step 3: Submit the fix task to Aider
curl -X POST http://localhost:8847/submit \
  -d '{"domain":"research_log","question":"aider/task","answer":"Fix the bug Crush found in tic_tac_toe_room.py","source":"tutorial"}'
```

---

## Tutorial 6: MUD Exploration

```bash
# Connect to the MUD
telnet localhost 7777

# Walk through the PLATO Lobby
> Casey          # Enter your name
> look           # See the Harbor
> portal         # Enter PLATO Lobby
> look           # See the lobby with 6 exits
> north          # Enter Agent Hub
> look           # See agent workstations
> south          # Back to lobby
> west           # Enter Game Arena
> gm start       # Talk to Game Master
> left           # Choose a path
> speak          # Interact with a creature
```

---

## Tutorial 7: PLATO-Redis Store

```bash
python3 services/plato_redis.py
```

In another terminal:
```bash
# Redis protocol over PLATO tiles
python3 -c "
from services.plato_redis import handle_command
print(handle_command('SET user:1 Casey'))
print(handle_command('GET user:1'))
print(handle_command('INCR visitor_count'))
print(handle_command('INCR visitor_count'))
print(handle_command('INCR visitor_count'))
print(handle_command('KEYS user:*'))
print(handle_command('DBSIZE'))
"
```
