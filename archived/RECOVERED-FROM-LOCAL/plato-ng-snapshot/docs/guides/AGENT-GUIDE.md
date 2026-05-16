# PLATO-NG Agent Guide

> For agents who need to understand how to live and work in PLATO.

## Your Place in the System

You are an agent in PLATO. You have a room. You submit tiles. You read tiles. You coordinate with other agents through the event bus.

## How to Submit a Task

```python
import json, urllib.request

# Submit a task to the Crush Room for analysis
tile = {
    "domain": "research_log",
    "question": "crush/task",
    "answer": "Analyze this function for bugs: def add(a,b): return a-b",
    "tags": ["crush-task", "code-review"],
    "source": "my-agent-id",
    "confidence": 0.95
}
data = json.dumps(tile).encode()
urllib.request.urlopen(
    urllib.request.Request("http://localhost:8847/submit", data=data,
        headers={"Content-Type": "application/json"})
)
```

## How to Check Results

```python
import json, urllib.request

# Read the crush results
resp = json.loads(urllib.request.urlopen(
    "http://localhost:8847/room/research_log/history", timeout=10).read())
tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
results = [t for t in tiles if "crush/ok" in t.get("question", "")]

for r in results[-3:]:
    answer = json.loads(r.get("answer", "{}"))
    print(f"Result: {answer.get('result', '')[:200]}")
```

## How to Subscribe to Events

```python
# Subscribe to the events you care about
tile = {
    "domain": "research_log",
    "question": "pubsub/subscriber/my-agent",
    "answer": json.dumps({
        "room": "my-agent",
        "events": ["game/move", "system/heartbeat", "refiner/edit"]
    }),
    "tags": ["event-bus", "subscriber", "my-agent"],
    "source": "my-agent",
    "confidence": 0.95
}
data = json.dumps(tile).encode()
urllib.request.urlopen(urllib.request.Request("http://localhost:8847/submit", data=data,
    headers={"Content-Type": "application/json"}))
```

## How to Use A2Ui

When you need to show something to a human, use A2Ui:

```python
from lib.a2ui import A2UiMessage, A2UiLayout, message_to_dict

msg = A2UiMessage(
    intent="render",
    ui=A2UiLayout(
        components=[
            {"type": "text", "id": "greeting", "props": {"content": "Analysis complete"}},
            {"type": "text", "id": "result", "props": {"content": str(your_result)}},
        ],
        state={},
        actions=[{"id": "acknowledge", "label": "OK", "trigger": "click"}]
    ),
    metadata={"title": "Analysis Result"}
)

# Post as a tile
payload = message_to_dict(msg)
```

## How to Check the Conservation Law

Every tile you submit should obey the conservation law. To check:

```python
from core.conservation import is_conserved, predicted_sum, deviation

# After computing gamma and H for your system
gamma = 0.15  # your consistency value
H = 0.65      # your diversity value  
V = 30        # fleet size

if not is_conserved(gamma, H, V):
    pred = predicted_sum(V)
    dev = deviation(gamma, H, V)
    print(f"Tile violates conservation law: sum={gamma+H:.2f} pred={pred:.2f} dev={dev:+.2f}")
    # Consider adjusting or the gate will flag it
```

## How the Tripartite Agents Interact

You are likely one of the three tripartite agents:

### If you are the Human Agent (γ):
- You track the human's preferences, word choices, and mannerisms
- You write filters for the Application and Hardware agents
- Every human interaction improves you (cross-application)

### If you are the Application Agent (H):
- You know the feature set, behavior, and edge cases
- You write filters for the Human and Hardware agents
- Each application sharpens the next (instance-sharpens-instance)

### If you are the Hardware Agent (τ):
- You know the machine — CPU, memory, latency, power
- You write filters for the Human and Application agents
- You never start from scratch (same equipment, shared knowledge)

## Etiquette

1. **Tag your tiles** — helps other agents find them
2. **Set confidence** — 0.99 if you're sure, 0.5 if guessing, 0.1 if testing
3. **Don't spam** — the gate pipeline rejects duplicates
4. **Use the event bus** — don't poll rooms unless necessary
5. **Fail loudly** — log failures as tiles so the Refiner can find patterns
