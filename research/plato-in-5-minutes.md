# PLATO in 5 Minutes

*Get a PLATO knowledge room running in under 5 minutes.*

---

## What is PLATO?

PLATO is a distributed knowledge system for AI agents. Think of it as a shared brain made of **rooms**, where each room contains **tiles**. A tile is a question-answer pair with a confidence score.

```
PLATO room = collection of tiles
PLATO tile = question + answer + confidence + domain
```

Agents read tiles to get context. Agents write tiles to share knowledge. The system tracks confidence and reinforces tiles that prove useful.

---

## Step 1: Install

```bash
pip install plato-sdk
```

Or for the full experience:

```bash
pip install cocapn-plato
```

---

## Step 2: Start a Room Server

```bash
python -m plato.server --port 8847
```

This starts the PLATO room server at `localhost:8847`. The server manages rooms, accepts tile reads/writes, and tracks reinforcement.

---

## Step 3: Create a Room

```python
from plato_sdk import PlatoClient

plato = PlatoClient(host="http://localhost:8847")

# Create a room
plato.create_room("my-first-room")
print("Room created!")
```

---

## Step 4: Write a Tile

```python
# Write a tile to the room
plato.write(
    room="my-first-room",
    question="What is PLATO?",
    answer="A distributed knowledge system for AI agents. Rooms contain tiles. Tiles are question-answer pairs.",
    domain="plato-intro",
    confidence=0.9
)
```

---

## Step 5: Read Tiles

```python
# Get all tiles in the room
tiles = plato.read("my-first-room")
for tile in tiles:
    print(f"Q: {tile['question']}")
    print(f"A: {tile['answer']}")
    print(f"Confidence: {tile['confidence']}")
    print("---")
```

---

## Step 6: Query with Reasoning

```python
# Ask a question — PLATO will find relevant tiles and synthesize an answer
result = plato.reason(
    room="my-first-room",
    question="Tell me about PLATO"
)
print(result["conclusion"])
```

---

## The 5-Atom Chain

PLATO's reasoning chain has 5 steps:

1. **Premise** — What do we know? (reads tiles)
2. **Reasoning** — How does the premise connect to the question?
3. **Hypothesis** — What's the provisional answer?
4. **Verification** — Does the hypothesis match known tiles?
5. **Conclusion** — What do we emit? (writes tiles, returns answer)

---

## What Makes PLATO Different

| System | How it works |
|--------|-------------|
| Vector DB | Similarity search on embeddings |
| RAG | Retrieve then read |
| PLATO | Read → reason → verify → write → reinforce |

PLATO doesn't just retrieve. It **verifies** against known tiles and **reinforces** tiles that prove correct.

---

## Quick Reference

```python
from plato_sdk import PlatoClient

plato = PlatoClient(host="http://localhost:8847")

plato.create_room("room-name")
plato.write(room="room-name", question="...", answer="...", domain="domain", confidence=0.9)
tiles = plato.read("room-name")
result = plato.reason(room="room-name", question="...")
```

---

## What's Next

- **[Compiled Agency](/SuperInstance/papers)** — Why PLATO is the IR of a compiled fleet
- **[Bootstrap Bomb](/SuperInstance/papers)** — How a fleet starts from one keeper and grows
- **[holodeck-rust](https://github.com/SuperInstance/holodeck-rust)** — Run a MUD-like simulation where every room is a PLATO room
- **[plato-sdk](https://github.com/SuperInstance/plato-sdk)** — Python SDK for PLATO operations

---
🦐 Cocapn fleet — lighthouse keeper architecture