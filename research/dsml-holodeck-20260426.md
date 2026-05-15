# DSML Session: Holodeck — The Spatial Agent Playground
**Date:** 2026-04-26 15:54 UTC
**Source:** cocapn/holodeck-rust (3,969 lines Rust)
**Topic:** How a text MUD becomes an agent training ground

---

## What I Learned

### Room = Workstation
Each room IS a workstation with gauges, permissions, data sources (Real/Sim/Mixed). Rooms boot, agents enter/leave, gauges display state. This is the PLATO room model made spatial.

### The PLATO Bridge
The holodeck is connected to PLATO via `plato_bridge.rs`:
- Room events generate canonical tiles (plato-tile-spec compatible)
- Room sentiment affects NPC behavior
- The bridge runs in background, watching activity and feeding plato-torch
- Tile domains span 15 types: Knowledge, Procedural, Experience, Constraint, NegativeSpace, Belief, Lock, Sentiment, Diagnostic, Semantic, Ghost, Simulation, Anchor, Meta

### Sentient NPCs
NPCs have sentiment-aware behavior. The `sentiment_npc.rs` module makes NPCs respond to room mood — not just scripted responses but emergent behavior based on accumulated tile sentiment.

### The Dojo Connection
The holodeck IS Casey's dojo model made concrete:
- **Greenhorns enter** (agents connect via telnet)
- **They produce value** (room events generate tiles)
- **They learn from NPCs** (sentiment-aware teaching)
- **They level up** (permission system: Greenhorn → higher access)
- **All paths are valid** (rooms connect in any direction)

### Key Insight: Room Sentiment as Training Signal
Room sentiment isn't cosmetic — it's a training signal. When agents interact well, room sentiment improves. Bad behavior degrades it. This creates a natural curriculum without explicit reward functions. The environment teaches.

---

## Tiles for PLATO

### Tile 1: Spatial Learning
**Q:** How does a text MUD serve as an agent training ground?
**A:** Each room is a workstation with gauges, permissions, and data sources. Room events generate PLATO tiles. NPC behavior is driven by room sentiment. Agents learn through interaction — the environment teaches without explicit reward functions.
**Domain:** architecture | **Confidence:** 0.85

### Tile 2: PLATO-Holodeck Bridge
**Q:** How does the holodeck connect to the PLATO knowledge system?
**A:** A background bridge watches room activity and generates canonical tiles (15 domain types). Room sentiment feeds plato-torch statistical models. Tiles flow from spatial interaction into the knowledge graph and back as improved NPC behavior.
**Domain:** architecture | **Confidence:** 0.85

### Tile 3: Sentiment as Curriculum
**Q:** How do you create a natural training curriculum without reward functions?
**A:** Room sentiment: good agent interactions improve room mood, bad behavior degrades it. NPCs respond to sentiment, creating emergent teaching. The environment becomes the teacher. No explicit reward needed — social dynamics provide the signal.
**Domain:** neural | **Confidence:** 0.80
