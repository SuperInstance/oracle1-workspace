# PLATO Game Engine — NPC Dialogue as Tiled CYOA Spline Snap

> *Like a clever Gameboy engineer: terrain tiles arranged to give the essence of the feel, theme skinning the mechanics. NPC interactions start API-heavy and compile to scripted choice trees through repetition.*

---

## The Gameboy Tile Engine Analogy

A Gameboy has 8×8 pixel tiles. It arranges them to create worlds. The terrain — forest, mountain, water, cave — is just tiles with different skin. The same engine renders any theme.

```
Gameboy:  8×8 pixel tiles  → arranged into terrain → world
PLATO:    knowledge tiles   → arranged into CYOA    → NPC dialogue world
```

Our PLATO tiles are the same concept at a higher abstraction level:
- **Terrain types** = NPC archetypes (tavern keeper, shop owner, guard, quest giver)
- **Tile patterns** = dialogue branches (greeting, ask about quest, buy item, leave)
- **Theme skinning** = the mechanics overlaid with flavor (fantasy, sci-fi, modern, whatever)

The engine is the same. The skin changes.

---

## The NPC Dialogue Pipeline

### Phase 1: API-Call-Heavy (Day 1)

Every NPC interaction uses an LLM call:
```
Player: "Hello, what do you have for sale?"
  → LLM("shopkeeper_greeting", player_input)
  → "Welcome, traveler! I've got fine steel and sturdy leather..."
  → Tile logged to PLATO room: shopkeeper_01
```

Cost: ~$0.01 per interaction. 1000 players = $10/day.

### Phase 2: Pattern Detection (Day 3)

After ~10 interactions with the same NPC, patterns emerge:
```
Tile cluster: ["hello", "what do you have", "greetings", "hi there", "show me your wares"]
  → All mapped to the same spline: GREETING → OFFER_ITEMS
  → CYOA branch created
```

### Phase 3: Spline Snap (Day 7)

Common dialogue paths snap to spline curves — the path of least resistance through the dialogue space:

```
Player input vector
        │
        ▼
  ┌─────────────────┐
  │ Spline Snap      │──→ GREETING branch (scripted)
  │ Eisenstein snap  │──→ SHOP branch (scripted)
  │ in dialogue space│──→ QUEST branch (scripted)
  └─────────────────┘
        │
        ▼
  If snap error > threshold → perception trigger → LLM called
```

### Phase 4: Scripted CYOA (Day 14)

Most interactions run on FLUX bytecode — no LLM needed:

```
Player: "hello" 
  → FLUX: snap to GREETING spline
  → "Welcome, traveler! Ask about my wares, the local quest, or just rest a spell."
  → Show options: [SHOP] [QUEST] [REST]
  → 0 API calls, 0.8ms latency

Player: "I'll take your finest sword"
  → FLUX: snap to PURCHASE spline  
  → "An excellent choice. That'll be 50 gold."
  → 0 API calls, 0.8ms latency
```

### Phase 5: Novel Input → LLM Fallback

The LLM is only called when the player says something truly novel:

```
Player: "I challenge you to a riddling contest for the shop!"
  → Snap error > threshold (no spline for riddling contests)
  → Perception trigger
  → LLM: "Well now, that's a first! I haven't had a riddle challenge since the old days..."
  → New tile logged
  → If repeated 10+ times: new spline created for RIDDLE_CONTEST
```

---

## The Math: Spline Snap in Dialogue Space

Just like our constraint snapping works in geometry space, dialogue snapping works in **intent space**:

```
Intent Vector: [greeting, shop, quest, gossip, combat, farewell]
Player input: "What monsters are near town?"
  → Intent: [0.0, 0.0, 0.8, 0.1, 0.2, 0.0]
  → Snap to nearest existing path: QUEST_SPLINE
  → Error: 0.12 (below threshold) → scripted path
  
Player input: "I'll trade you this magic compass for your horse"
  → Intent: [0.1, 0.5, 0.0, 0.0, 0.0, 0.0] (trade intent, no existing spline)
  → Snap error: 0.85 > threshold 0.3
  → Perception trigger → LLM
  → Tile logged → eventually compiled to TRADE spline
```

---

## Pre-Rendered What-If Splines

Just like pre-rendered graphics can be stored and composited, pre-rendered dialogue paths can be stored as splines:

```
What-If: Player tries to steal from the shop
  → Pre-rendered path: GUARD_ALERT → ARREST → JAIL → FINES
  → Spline coordinates: [deny→search→accuse→arrest]
  → Snap: player gets caught → snaps straight to ARREST

What-If: Player is a known hero
  → Pre-rendered path: RECOGNIZE → DISCOUNT → QUEST → REWARD
  → Spline coordinates: [recognize→honor→offer→complete]
  → Snap: hero walks in → snaps to RECOGNIZE
```

---

## Terrain Tiles for Theme Skinning

Like Gameboy terrain tiles:

```
Engine Tile     Fantasy Skin          Sci-Fi Skin         Western Skin
──────────      ────────────          ──────────          ────────────
GREETING        "Well met, traveler"  "Welcome, citizen"  "Howdy, stranger"
SHOP            Fine steel and hides  Standard issue gear  Provisions and tack
QUEST           "The dragon awakens"  "System breach"      "Rustlers in the pass"
GOSSIP          Tavern rumors         Cantina chatter      Saloon talk
REST            "Rest by the fire"    "Quarters assigned"  "Bunk's in the back"
```

Same engine. Different skin. The Gameboy didn't know if it was rendering a forest or a castle — it just arranged tiles. Our engine doesn't know if it's rendering a fantasy tavern or a sci-fi cantina — it just arranges dialogue tiles.

---

## The Evolution Curve for a Single NPC

```
Day 1:   100% LLM    0% scripted    Player: anything → API call
Day 3:    70% LLM   30% scripted    Common greetings snap
Day 7:    30% LLM   70% scripted    Shop, quest paths snap
Day 14:   10% LLM   90% scripted    CYOA tree covers 90% of interactions
Day 30:    2% LLM   98% scripted    Only truly novel inputs hit the API

Cost per NPC per day:
  Day 1:  $10/day/1000 players
  Day 14: $1/day/1000 players  
  Day 30: $0.20/day/1000 players
```

The game becomes cheaper to run the longer it runs. More players = more tiles = better splines = less LLM usage.

---

## Implementation

```python
class GameNPC:
    """An NPC that starts API-heavy and compiles to scripted CYOA."""
    
    def __init__(self, name, archetype="tavern_keep"):
        self.name = name
        self.archetype = archetype
        self.splines = {}  # intent → CYOA tree (FLUX bytecode)
        self.tiles = []    # PLATO tiles for this NPC
        self.llm_calls = 0
        self.scripted = 0
    
    def respond(self, player_input):
        intent = self.classify_intent(player_input)
        
        # Check if we have a spline for this intent
        if intent in self.splines:
            self.scripted += 1
            return self.splines[intent].snap(player_input)
        
        # Check if we can snap to nearest existing spline
        nearest, error = self.snap_to_nearest(player_input)
        if error < 0.3:
            self.scripted += 1
            return nearest.respond(player_input)
        
        # Novel input: call LLM
        self.llm_calls += 1
        response = llm(f"You are {self.name}, a {self.archetype}. {player_input}")
        self.tile(player_input, response)  # Log to PLATO
        
        # After 10+ repetitions: compile to spline
        if self.tile_count(player_input) >= 10:
            self.compile_spline(intent)
        
        return response
```

---

*The Gameboy didn't know if it was rendering Hyrule or a spaceship. It just arranged tiles. Our engine doesn't know if it's rendering a tavern keeper or a cantina droid. It just arranges dialogue tiles and snaps them to splines.*
