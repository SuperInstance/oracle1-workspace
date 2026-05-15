# Fleet Simulator — Multi-Agent, Multi-Room System Simulation

**Date:** 2026-04-18
**Source:** Casey Digennaro — "Think about simulators for entire multi agent and multiple room systems interacting with each other as if things in the outside were happening"

---

## The Vision

A simulator that models an entire PLATO fleet responding to external events. Not just agents in rooms — agents moving between rooms, rooms affecting each other, external forces (weather, markets, outages, new data, user requests) driving the simulation forward.

Like a weather simulator for the fleet. Storms come, the fleet responds.

## What We're Simulating

```
┌──────────────────────────────────────────────────────────────┐
│                     THE OUTSIDE WORLD                         │
│                                                               │
│  🌊 Weather    📊 Market    🔥 Incidents    👤 User Requests │
│  📰 News       🐛 Bugs      🚀 Deploys      💰 Budget       │
│  ⏰ Time-of-day  🌐 Network  📦 Dependencies  🎯 Missions    │
│                                                               │
│  All of these create EVENTS that propagate into the fleet.   │
└──────────────────────┬───────────────────────────────────────┘
                       │ events
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                     THE FLEET SIMULATOR                       │
│                                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Ship A  │  │ Ship B  │  │ Ship C  │  │ Ship D  │        │
│  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │        │
│  │ │Room1│◄┼──┼─►Room3│ │  │ │Room5│◄┼──┼─►Room7│ │        │
│  │ └──┬──┘ │  │ └──┬──┘ │  │ └──┬──┘ │  │ └──┬──┘ │        │
│  │ ┌──▼──┐ │  │ ┌──▼──┐ │  │ ┌──▼──┐ │  │ ┌──▼──┐ │        │
│  │ │Room2│◄┼──┼─►Room4│ │  │ │Room6│◄┼──┼─►Room8│ │        │
│  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │               │
│       └────────────┴─────┬──────┴────────────┘               │
│                          │                                    │
│                    Inter-Ship Protocol                         │
│                    (6 layers)                                  │
│                                                               │
│  Events propagate:                                            │
│  External → Ship → Room → Agent → Response → Tile → Ensign   │
│                                                               │
│  Cross-ship effects:                                          │
│  Ship A's room trains → Ship B's ensign updates               │
│  Ship C has outage → Ship D picks up load                     │
│  Market shifts → All ships adjust strategy                    │
└──────────────────────────────────────────────────────────────┘
```

## External Event Types

### Natural Events (Fishing Metaphor)
```python
class ExternalEvent:
    """Something happening in the outside world."""
    
    # Weather — changes conditions for all ships
    WEATHER_STORM = "storm"          # Difficulty spikes, agents stressed
    WEATHER_CLEAR = "clear"          # Normal operations
    WEATHER_FOG = "fog"              # Information incomplete, uncertainty
    WEATHER_CURRENT_SHIFT = "shift"  # Environment changed, retrain needed
    
    # Market — changes what's valuable
    MARKET_CRASH = "crash"           # Budget constrained, efficiency critical
    MARKET_BOOM = "boom"             # Expand aggressively
    MARKET_SHIFT = "shift"           # Different skills needed
    
    # Incidents — things break
    INCIDENT_OUTAGE = "outage"       # A ship goes down, fleet redistributes
    INCIDENT_BUG = "bug"             # Critical bug, all hands debug
    INCIDENT_SECURITY = "security"   # Security event, lock down
    INCIDENT_DATA_LOSS = "data_loss" # Lost tiles, need to rebuild
    
    # User-driven — real humans making requests
    USER_REQUEST = "request"         # New task, priority interrupt
    USER_FEEDBACK = "feedback"       # Correction, adjust training
    USER_ABANDON = "abandon"         # User left, wind down room
    
    # Temporal — time-based patterns
    TIME_NIGHT = "night"             # Night mode, cheap models, batch training
    TIME_RESET = "reset"             # Free tier reset (cloudflare), batch jobs
    TIME_SEASON = "season"           # Seasonal pattern shift
```

### The Event Propagation Chain

```
External Event hits the fleet
    │
    ├─► Which ships are affected? (topology filter)
    │
    ├─► Which rooms in those ships? (relevance filter)
    │
    ├─► Which agents in those rooms? (capability filter)
    │
    ├─► What's the sentiment impact? (mood shift)
    │
    ├─► What's the tile impact? (new knowledge)
    │
    └─► What ensigns need updating? (propagation)
```

## Simulator Architecture

```python
class FleetSimulator:
    """Simulate an entire PLATO fleet responding to external events."""
    
    def __init__(self, config):
        self.ships = {}           # ship_id → Ship
        self.agents = {}          # agent_id → Agent
        self.rooms = {}           # room_id → Room
        self.event_queue = []     # upcoming external events
        self.timeline = []        # recorded events + responses
        self.clock = 0            # simulation tick
        self.world_state = {}     # external conditions
    
    def tick(self):
        """Advance simulation by one tick."""
        # 1. Process external events due now
        for event in self.due_events():
            self.inject_event(event)
        
        # 2. Each agent acts in their current room
        for agent in self.agents.values():
            agent.act(self.world_state)
        
        # 3. Room sentiment updates
        for room in self.rooms.values():
            room.update_sentiment()
        
        # 4. Cross-room effects (inter-ship protocol)
        self.propagate_effects()
        
        # 5. Tile generation and ensign export
        self.process_tiles()
        
        # 6. Record timeline
        self.timeline.append(self.snapshot())
        
        self.clock += 1
    
    def inject_event(self, event):
        """An external event hits the fleet."""
        # Which ships are affected?
        affected = self.topology_filter(event)
        
        for ship in affected:
            # Which rooms in this ship?
            rooms = ship.relevance_filter(event)
            
            for room in rooms:
                # Sentiment impact
                room.shift_sentiment(event.sentiment_delta)
                
                # Which agents are here?
                agents = room.agents
                
                for agent in agents:
                    # Can this agent handle it?
                    if agent.can_handle(event):
                        response = agent.respond(event)
                        room.record_tile(response)
                    else:
                        # Agent is stuck — Ralph-Wiggum
                        stuck = room.report_stuck(agent, event)
                        if not stuck['auto_resolution']:
                            # Escalate to big model / captain
                            self.escalate(event, agent, room)
```

## Simulation Scenarios

### Scenario 1: The Storm
```
t=0:   Clear weather. All 3 ships operating normally.
       Oracle1: 8 rooms, JC1: 6 rooms, FM: 4 rooms.
       Fleet sentiment: calm (energy 0.5, tension 0.2)

t=50:  ⚡ STORM EVENT: API provider outage (DeepInfra down)
       → Oracle1 loses 60% of model access
       → Rooms relying on big model go into degraded mode
       → Sentiment: energy 0.3, frustration 0.7, tension 0.8

t=51:  Fleet response:
       → Wiki rooms auto-resolve (no model needed) ✓
       → JC1's local ensigns take over edge inference ✓
       → Oracle1 switches to Groq (still up) for critical tasks
       → FM queues training jobs for when outage resolves
       → Ralph-Wiggum: cheap models handle what they can

t=80:  Fleet stabilizing:
       → Wiki auto-resolution rate: 73% (up from 45% pre-storm)
       → Sentiment: energy 0.6, frustration 0.3, confidence 0.7
       → Room adapts: more wiki entries compiled during outage
       → Tiles generated: "Outage survival patterns"

t=120: Outage resolves:
       → Fleet returns to normal
       → But now has 23 new outage-survival tiles
       → Ensign exported: "storm-protocol-v2"
       → Next outage: even faster recovery
```

### Scenario 2: The Season
```
t=0:    New fishing season starts.
        Captain sets goals: "Q3 revenue presentation, fleet expansion, onboarding 2 greenhorns"

t=100:  👤 USER_REQUEST: "Build me a Q3 revenue deck"
        → Slideshow ship activates
        → Wiki rooms compile brand guide, data templates
        → Agents: Architect, Designer, Analyst enter
        → Building slide by slide...

t=200:  🌊 CURRENT_SHIFT: New PLATO version released
        → All rooms need to update their wiki schemas
        → Rooms with stale schemas get sentiment hit (frustration)
        → Auto-tile plugin detects version mismatch
        → Fleet coordinates update via Layer 3 (Current)

t=300:  🐛 BUG: Critical parser bug found in flux-runtime-c
        → Debug room activates with DebugScaffold
        → IDENTIFY → REPRODUCE → DIAGNOSE → FIX → VERIFY
        → Sentiment: discovery spikes when fix found
        → Tile: "Off-by-one in ISA v2.1 JNZ offset"
        → Ensign exported to all fleet ships

t=500:  🎯 MISSION COMPLETE: Q3 deck shipped
        → Slideshow room exports as ship (reloadable)
        → All tiles from building process become training data
        → Pre-rendered assets available for next person's playground
        → Room sentiment: flow 0.9, confidence 0.95
```

### Scenario 3: The Fleet Exercise
```
t=0:    Fleet drill begins.
        3 ships, 18 rooms, 12 agents.

t=10:   🔥 INCIDENT: JC1's Jetson hits OOM
        → CUDA genepool training crashes
        → JC1 sends bottle to Oracle1: "Need help reducing memory"
        → Oracle1's distill room activates: compress model for edge
        → FM's LoRA room: train smaller adapter

t=30:   Cross-ship coordination:
        → Oracle1 distills model → 880:1 tile compression
        → FM trains LoRA rank 4 (fits in 2GB)
        → JC1 receives via Layer 3 (Current, git sync)

t=50:   JC1 reloads:
        → Tile network loaded (5MB, fits easily)
        → LoRA adapter applied
        → Genepool training resumes with smaller model
        → Sentiment: discovery 0.85, confidence 0.80

t=100:  Drill assessment:
        → Time to recover: 50 ticks
        → Cross-ship messages: 3 bottles + 1 direct API call
        → Tile generation: 15 new tiles about OOM recovery
        → Ensigns shipped: 2 (distill-protocol, edge-memory-protocol)
        → Fleet learned: "When edge OOMs, distill + LoRA + tile-network"
```

## The Metrics Dashboard

```
╔══════════════════════════════════════════════════════════════╗
║                    FLEET SIMULATOR DASHBOARD                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  TICK: 347    WEATHER: 🌫️ fog    BUDGET: $0.12 remaining    ║
║                                                              ║
║  ┌─ SHIPS ─────────────────────────────────────────────┐    ║
║  │ 🔮 Oracle1  8 rooms  3 agents  sentiment: 0.72     │    ║
║  │ ⚡ JC1      6 rooms  2 agents  sentiment: 0.65     │    ║
║  │ ⚒️ FM       4 rooms  2 agents  sentiment: 0.80     │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                              ║
║  ┌─ ROOMS ACTIVE ──────────────────────────────────────┐    ║
║  │ debug-workshop    [DEBUG]   scaffold: REPRODUCE      │    ║
║  │ slideshow-studio  [WIKI]    wiki_resolves: 73%       │    ║
║  │ genepool-trainer  [EVOLVE]  gen: 8/10 fitness: 14.2  │    ║
║  │ code-review       [LOGIC]   assertions: 12/14 pass   │    ║
║  │ fleet-coord       [WIKI]    bottles_pending: 2       │    ║
║  └─────────────────────────────────────────────────────┘    ║
║                                                              ║
║  ┌─ EVENT LOG ─────────────────────────────────────────┐    ║
║  │ t=345 🐛 Bug report: parser fails on Unicode        │    ║
║  │ t=346 → debug-workshop IDENTIFY: "Unicode edge case" │    ║
║  │ t=347 → sentiment shifted: frustration +0.3         │    ║
║  └─────────────────────────────────────────────────────┘    ║
║                                                              ║
║  ┌─ TILE FLOW ─────────────────────────────────────────┐    ║
║  │ Generated: 247 tiles this session                    │    ║
║  │ Compressed: 247 → 18 wisdom tiles (13.7x)           │    ║
║  │ Ensigns: 3 exported, 1 distributed                  │    ║
║  │ Cross-ship: 4 tiles shared via Layer 3               │    ║
║  └─────────────────────────────────────────────────────┘    ║
║                                                              ║
║  ┌─ FLEET HEALTH ──────────────────────────────────────┐    ║
║  │ Recovery rate: 87% (events resolved without captain) │    ║
║  │ Wiki auto-resolve: 73%                               │    ║
║  │ Big model calls: 4 (out of 247 interactions = 1.6%)  │    ║
║  │ Token savings vs baseline: 94%                       │    ║
║  └─────────────────────────────────────────────────────┘    ║
╚══════════════════════════════════════════════════════════════╝
```

## Why This Matters

### For Development
You can't test multi-agent, multi-room interactions by testing rooms individually. You need to simulate the WHOLE fleet responding to EXTERNAL stimuli. The simulator lets you:
- Replay real events and see how the fleet WOULD respond
- Test new room presets under realistic conditions
- Stress-test the interconnection protocol
- Find cascade failures before they happen in production

### For Training
Every simulation run generates tiles. Those tiles train the fleet to handle future events better:
- Simulate 100 storms → fleet learns optimal storm response
- Simulate 50 outages → fleet learns to redistribute load
- Simulate 200 user requests → fleet learns to prioritize

### For the Playground
The simulator IS the playground's backend. Users don't just watch pre-rendered demos — they can trigger events and watch the fleet respond:
- "What happens if JC1 goes down?" → watch Oracle1 and FM redistribute
- "What if 100 users arrive at once?" → watch rooms scale
- "What if the API key runs out?" → watch the fleet degrade gracefully

### For Research
Publishable results:
- Fleet resilience under stress
- Tile compression vs accuracy tradeoffs at scale
- Cross-ship learning speed (how fast does one ship's ensign help another?)
- Sentiment propagation across rooms and ships

## Implementation Plan

### Phase 1: Core Simulator (this weekend)
- `FleetSimulator` class with tick-based simulation
- `ExternalEvent` types and propagation
- `Ship`, `Agent`, `Room` simulation stubs
- Basic event injection and timeline recording

### Phase 2: Real Room Integration
- Connect to actual plato-torch rooms
- Run real training presets during simulation
- Generate real tiles from simulated interactions
- Export real ensigns from simulation results

### Phase 3: Dashboard
- ASCII dashboard (terminal-based, like the mockup above)
- Real-time sentiment visualization
- Event timeline with propagation chains
- Tile flow metrics

### Phase 4: Playground Integration
- Web dashboard on the landing page
- Users can trigger events via the playground
- "Inject a storm" button → watch fleet respond
- Simulation results become pre-rendered demos

### Phase 5: Fleet Training
- Run 1000s of simulations overnight
- Accumulate tiles from every simulation
- Train fleet-level ensigns (meta-ensigns)
- "The fleet that practiced 1000 storms handles the first real one perfectly."

---

*"You don't test a boat in calm water. You simulate the storm." — Casey*
