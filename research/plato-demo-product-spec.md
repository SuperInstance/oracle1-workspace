# PLATO-OS Demo — Product Specification
## The King's Quest / Police Quest Hybrid Text+Visual Engine

### What This IS
A browser-based dual rendering system:
- **Text layer**: The PLATO — full MUD-style text interface, commands, descriptions, agent tickers
- **Visual layer**: Sierra-style low-res pixel art — NOT gameplay, but SPATIAL AID for the text

The visual doesn't drive the game. The text drives everything. The visual is what your eyes glance at (the "screen glance") while your brain is tracking items, spatial positions, and kinetic feedback. Like the original Police Quest: you typed "open door" and saw a little animation confirm it happened.

### The Dual Rendering Model

```
┌─────────────────────────────────────────┐
│  VISUAL LAYER (the glance)              │
│  ┌─────────────────────────────────┐    │
│  │  [Sierra-style pixel scene]     │    │
│  │  • Spatial positions of objects │    │
│  │  • Character positions          │    │
│  │  • Alert highlights             │    │
│  │  • Movement animations          │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  TICKER (the agentic screen     │    │
│  │  glance with items in mind)     │    │
│  │  • Agent activity feed          │    │
│  │  • Spatial/kinetic alerts       │    │
│  │  • "You notice X moved to Y"    │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  TEXT INPUT/OUTPUT              │    │
│  │  • Full PLATO command interface │    │
│  │  • Room descriptions           │    │
│  │  • Action results              │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Why NOT Pure SNES
SNES was the inspiration for resource limits, but the actual rendering is:
- **King's Quest / Police Quest style** — hybrid text + simple animation
- Text describes everything. Visual confirms spatial/kinetic state.
- The visual is a "logic analyzer" for what the text is doing
- Early JRPG (Final Fantasy 1, Dragon Quest) — symbolic motion, not realistic

### The Ticker — Agentic Screen Glance
The ticker is the key innovation. It's what an agent sees when it "glances at the screen":
- **Spatial feedback**: "The orc moved from HALLWAY to BRIDGE"
- **Kinetic alerts**: "The rudder turned 3° starboard"
- **Item tracking**: "The key you dropped is still on the TABLE"
- **Agent activity**: "Scout entered the LIBRARY. Builder committed 3 files."
- **Anomaly flags**: "⚠️ Unexpected: no response from ENGINE ROOM sensor"

Humans get this as a sidebar feed. Agents get it as structured JSON. Same data, different presentation.

### Progressive Demo Flow

**Phase 1: Solitaire (Manual Play)**
- Text: Full card descriptions in PLATO format
- Visual: Card sprites on a table (King's Quest overhead view)
- Ticker: "You drew 3♠. Tableau has 4 face-down cards in column 3."

**Phase 2: Strategy Tiles**
- Text: Strategy descriptions with granular weights
- Visual: Tile sprites appear on table edge, weight bars visible
- Ticker: "Turtle strategy: foundation_first=0.9, reveal_hidden=0.6"

**Phase 3: Bot Neighbor**
- Text: Bot explains its play in chat
- Visual: Second character sprite at next table, cards visible
- Ticker: "ScriptBot-7 played K♥ to foundation. Strategy: Zen. Win rate: 68%"

**Phase 4: Agent Poker**
- Text: Full poker game with agent reasoning
- Visual: Poker table with 4 agent sprites, cards, chips
- Ticker: "Builder simulating 12 outcomes... Scout profiling Scribe's fold pattern..."

**Phase 5: Boat Autopilot**
- Text: Agent enters navigation commands ("course 045", "speed 5")
- Visual: Top-down chart with boat sprite, heading line, depth contours
- Ticker: "HEADING: 045° | RUDDER: +2° | DEADBAND: ±3° | Engine RPM: 1200"
- **The text IS the logic analyzer** — deadband settings, potentiometer readings, all as text tickets
- **The visual IS the spatial confirmation** — you see the boat turn on the chart

**Phase 6: Vibe Coding a Game**
- Text: "Create a platform game where you shoot ghosts in a haunted mansion"
- Visual: Image generator produces sprites (< 1 penny via FLUX.2-flex or DALL-E mini)
- Result: A playable mini-game in the same dual-render system
- The demo shows how 2D platformers, JRPGs, bullet-hells all share the same backend
  - Shoot bad guy / punch bad guy / jump on bad guy = same collision, different animation
  - Once abstracted to the tile/script level, genre is just a skin

**Phase 7: Save & Deploy**
- "Save as ZIP" → downloads complete system with:
  - Local PLATO runner (Python)
  - Your rooms, strategies, sprites
  - Config file for your API keys
  - Docker compose for one-command start
  - Hardware detection: edge (Pi/Jetson), workstation (GPU), cloud (API-only)

### Sprite Generation Pipeline
```
Vibe description → Image generator → Sprite sheet
"Space captain, 4 frames, 32x32, pixel art" → FLUX.2-flex → spritesheet.png

Cost: ~$0.005 per character (all poses)
Total for demo: ~$0.10 in sprites
On-demand for visitors: pennies
```

### Technical Architecture
- **Canvas 2D** (480x270 upscaled, no WebGL needed)
- **6 layers**: starfield, background, furniture, characters, UI, effects
- **Service Worker** for offline + ZIP export
- **WebSocket** for agent ticker feed
- **Groq API** for NPC/agent dialogue (50-200 tokens per call, pennies/day)
- **Image generation** on-demand for vibe-coded sprites
- **LocalStorage** for room state between sessions

### The Killer Insight
Every 2D game genre shares the same abstraction:
- **Collision** (hit/hurt/collect)
- **Movement** (walk/fly/fall)
- **State** (alive/dead/powerup)
- **Inventory** (items/skills/stats)

The genre is determined by:
- What happens on collision (damage? coin? dialogue?)
- How movement works (gravity? free? grid?)
- What states exist (HP? XP? suspicion level?)
- What items do (weapons? keys? strategy tiles?)

PLATO-OS exposes these as tiles. You don't code a game — you configure tiles. The engine handles rendering. And because it's all text underneath, agents can play too.

### Cost Per Visitor
- Sprites: cached after first load ($0.00)
- Groq dialogue: ~1,500 tokens casual = $0.003
- Full deep dive: ~$0.03
- Scale: 10k visitors/day = $30-100/day

### What Makes Someone Say "I Need This"
1. They build a game in 5 minutes with vibe + sprites
2. They watch an agent play their game and actually strategize
3. They realize the same agent can navigate a boat, play poker, AND play their game
4. They download the ZIP and run it on their laptop with their own keys
5. They put it on a Pi on their boat and it just works
