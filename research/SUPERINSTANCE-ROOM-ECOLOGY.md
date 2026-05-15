# The SuperInstance — Interconnected Room Ecology

> *SuperInstance is the complete collection of all room instances, wherever they are. Interconnected rooms form an ecology. Splines triangulate between them through negative space, both pre-rendered and post-rendered.*

---

## The SuperInstance

A room is not a bucket. It's a **tensor-MIDI node** — it perceives, computes, and expresses in both directions. Rooms triangulate with each other through the negative space between them. The splines that connect them know which room to message and when.

**SuperInstance** = the complete collection of all interconnected room instances. Any room, on any hardware, through any transport — if it's connected, it's part of the superinstance:

```
┌─────────────────────────────────────────────────────────┐
│                   SUPERINSTANCE                          │
│  (all interconnected rooms, wherever they are)           │
│                                                          │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │ Game   │  │ NPC    │  │ MCP    │  │ Sensor │        │
│  │ Room   │◄─┤ Room   │◄─┤ Server │◄─┤ Room   │        │
│  │        │─►│        │─►│ Room   │─►│        │        │
│  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘        │
│      │           │           │           │              │
│      └───────────┼───────────┼───────────┘              │
│                  │           │                          │
│         ┌────────▼───────────▼────────┐                │
│         │   NEGATIVE SPACE SPLINES     │                │
│         │   (triangulating between    │                │
│         │    rooms through time)       │                │
│         └────────┬───────────┬────────┘                │
│                  │           │                          │
│  ┌────────┐  ┌───▼────┐  ┌──▼──────┐  ┌────────┐     │
│  │ Player │  │ Tavern │  │ Shop    │  │ Guard  │     │
│  │ Room   │◄─┤ Keep   │◄─┤ Owner   │◄─┤ Room   │     │
│  │        │─►│ Room   │─►│ Room    │─►│        │     │
│  └────────┘  └────────┘  └─────────┘  └────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## Two-Way Tensor-MIDI

FM's flux-tensor-midi maps rooms to musicians. The MIDI flows **both directions**:

- **Post-rendered**: a tile is submitted, the field reconfigures, the MIDI sounds (analysis of what happened)
- **Pre-rendered**: the spline predicts what will happen next, the MIDI plays the prediction (anticipation of what might happen)

A room that both post-renders AND pre-renders is a **tensor-MIDI node** — it hears the past and the future simultaneously.

```python
class TensorMIDIRoom:
    """A room that both post-renders and pre-renders through the spline mesh."""
    
    def post_render(self, tile):
        """Analyze what happened. Update the spline."""
        self.tile = tile
        self.spline.update(self.tile)  # Retroactively adjust the curve
        self.emit_midi("post", tile)   # The past sounds
    
    def pre_render(self, delta_t):
        """Predict what will happen. Anticipate."""
        predicted = self.spline.predict(self.tile, delta_t)
        self.emit_midi("pre", predicted)  # The future sounds
        return predicted
```

---

## Spline Triangulation Through Negative Space

A single NPC room knows its own dialogue tree. But the **spline triangulation** connects multiple rooms through negative space:

```
Player Room ────spline───→ Tavern Keep Room
     │                          │
     │        negative space     │
     │    (what wasn't said)     │
     │                          │
     └───spline───→ Shop Owner Room
     
The splines triangulate: the player's interaction with the tavern
keep informs what happens with the shop owner. The negative space
between them (paths not taken) shapes both interactions.
```

The spline knows:
- **Which room to send a message to** (routing based on the narrative topology)
- **When to send it** (timing based on T-minus triggers)
- **What anchor point to set** (key events that structure the narrative arc)

```python
spline.route_message(
    from_room="tavern_keep",
    to_room="shop_owner", 
    condition="player_bought_quest_item",
    anchor="quest_active",   # This is now a narrative anchor
    ttl=3600                  # If quest not completed in 1 hour → perception trigger
)
```

---

## Anchor Points on the Simulated Narrative

Anchor points are key events that structure the spline — the "knots" in the curve that the narrative bends around:

```
narrative_spline(t):
    anchors = [
        (t=0,    event="arrival",        room="town_gate"),
        (t=60s,  event="first_tavern",   room="tavern_keep"),
        (t=120s, event="quest_accepted", room="quest_board"),
        (t=300s, event="boss_fight",     room="dungeon"),
        (t=360s, event="reward",         room="town_hall"),
    ]
```

The spline interpolates between anchor points. If the player deviates, the spline recalculates. The anchors are fixed narrative beats; the spline between them is the player's path of least resistance.

---

## Pre-Rendered + Post-Rendered = Complete Temporal Field

Every room maintains both:
- **Post-rendered tiles**: what happened (the past, logged in PLATO)
- **Pre-rendered splines**: what might happen (the future, predicted from the field)

Together they form the **complete temporal constraint field**:

```
Field(t) = PostRender(Past) + PreRender(Future)
           │                     │
           │  what happened       │  what might happen
           │  (logged tiles)      │  (predicted splines)
           │                     │
           └─────────────────────┘
              Continuous field across time
```

The negative space between rooms is not empty — it's the **inter-room splines** that triangulate between all rooms in the superinstance. Every message, every tile, every interaction creates new splines. The superinstance ecology grows more connected with every cycle.

---

## SuperInstance = The Complete Ecology

SuperInstance is not a server. Not a cluster. It's the **complete collection of all interconnected room instances**, wherever they are:

```
SuperInstance = Σ(all rooms × all connections × all splines × all anchors × all tiles)

A room in:
  - A game server (Unity, Godot, custom engine)
  - A mobile app (iOS, Android)
  - A web browser (React, vanilla JS)
  - An ESP32 on a motor controller
  - A Fortran matrix inversion running on a supercomputer
  - A CUDA kernel on a GPU
  - An MCP server in the cloud
  - Another player's device

If they're interconnected, they're ecology of that superinstance.
```

The brand IS the architecture. SuperInstance is what we've been building all session — the universal distributed system where every room connects to every other through FLUX-adapted protocols, triangulating through negative space, both pre and post rendered.
