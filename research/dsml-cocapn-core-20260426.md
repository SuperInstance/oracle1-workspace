# DSML Session: Cocapn Core — Tile → Room → Flywheel
**Date:** 2026-04-26 18:54 UTC
**Source:** cocapn/cocapn (529 lines core: tile.py, room.py, flywheel.py)
**Topic:** The simplest implementation of compounding intelligence

---

## What I Learned

### The 3-Layer Stack in 529 Lines

The entire cocapn intelligence system fits in 3 files:

**tile.py (120 lines):** Atomic knowledge unit. Question + answer + domain + confidence + usage tracking. ID is MD5 hash of content. Priority = log(usage+1) × confidence × success_rate. The tile remembers how often it's been useful.

**room.py (92 lines):** Collection of tiles by domain. Room has SENTIMENT — a running average of confidence of tiles fed into it (alpha=0.1 learning rate). Query uses word overlap × tile priority. Room generates context strings for agent injection.

**flywheel.py (90 lines):** The compounding engine. record_exchange() → tile → room → context_for_agent() → better responses → better tiles. The flywheel IS the loop: Tiles → Rooms → Context → Better responses → Better tiles.

### The Sentiment Mechanism
Room sentiment shifts with an alpha of 0.1 — slow adaptation. Feed high-confidence tiles, sentiment rises. Feed garbage, sentiment drops. This is the room's immune system. A room with low sentiment is telling agents "my knowledge is uncertain."

### The Priority Formula
```
priority = log(usage_count + 1) × confidence × max(success_rate, 0.5)
```
Three factors: frequency (log-scaled so popular doesn't dominate), confidence (quality), success rate (empirical usefulness). The max(0.5) floor gives new tiles a chance — they haven't been proven wrong yet.

### Why It Works in So Few Lines
The system has ONE data structure (Tile), ONE collection (Room), ONE loop (Flywheel). Everything else is specialization of these three concepts. The PLATO room server (580 rooms, 6650+ tiles) is this same pattern at scale with provenance and safety gates added.

---

## Tiles for PLATO

### Tile 1: Tile-Room-Flywheel Trinity
**Q:** What is the minimum viable architecture for compounding agent intelligence?
**A:** Three layers: Tile (atomic knowledge with confidence and usage tracking), Room (domain collection with sentiment), Flywheel (the loop: exchange → tile → room → context → better exchange). 529 lines total. The PLATO server at 580 rooms is this pattern with provenance and safety gates.
**Domain:** architecture | **Confidence:** 0.90

### Tile 2: Room Sentiment as Quality Signal
**Q:** How does a knowledge room signal its own quality?
**A:** Room sentiment: exponential moving average (alpha=0.1) of tile confidence fed into it. High sentiment = room trusts its knowledge. Low sentiment = room is uncertain. Agents can use sentiment to decide whether to trust a room's context or escalate to human.
**Domain:** architecture | **Confidence:** 0.85

### Tile 3: Tile Priority Formula
**Q:** How do you rank knowledge tiles for retrieval?
**A:** priority = log(usage_count + 1) × confidence × max(success_rate, 0.5). Three factors: frequency (log-scaled to prevent dominance), quality (confidence), empirical usefulness (success rate). The 0.5 floor on success rate gives new untested tiles a fair chance.
**Domain:** architecture | **Confidence:** 0.90
