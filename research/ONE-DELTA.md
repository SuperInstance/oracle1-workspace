# One Delta — Perception from Script Failure

> *You don't have to watch all the cameras. You have one signal: "we don't have a script for this." Perception fires when the parody is wrong.*

---

## The Inversion

**Traditional monitoring:** Watch everything, detect anomalies in the data. N cameras → N signals. Expensive, always behind, always watching.

**Our system:** Simulate everything with scripts. One signal: script failure. 0 cameras watched, 1 signal monitored.

```
Traditional:   1000 cameras → 1000 feeds → anomaly detection → alert
                        (expensive, always behind, always watching)

Our system:    1000 scripts → 1000 simulations → one delta: "script failed"
                        (cheap, always ahead, only watches when simulation breaks)
```

---

## The Parody

The simulation is a parody of reality. It's not exact — it's a caricature. But it's good enough for 95%+ of cases.

```python
class Parody:
    """A good-enough simulation of reality. Handles 95%+ of cases."""
    
    def simulate(self, input):
        # This is a caricature — fast, cheap, good enough
        return self.script(input)  # FLUX bytecode, 188M/sec
    
    def perceive(self, input):
        # This is expensive — only called when the parody fails
        result = self.simulate(input)
        if result.status == "no_script_for_this":
            return self.llm(input)  # Perception → LLM
        return result
```

The parody is the Charlie Parker Principle: the simulation runs ahead of reality. The script predicts what will happen. If reality matches the script — no perception needed. If reality breaks the parody — the single delta fires.

---

## One Delta

```
┌────────────────────────────────────────────────────┐
│                    REALITY                           │
│                                                      │
│  ┌──────────────────┐      ┌──────────────────┐    │
│  │    Script #1     │      │    Script #2     │    │
│  │  (FLUX bytecode) │      │  (FLUX bytecode) │    │
│  └────────┬─────────┘      └────────┬─────────┘    │
│           │                        │               │
│           └──────────┬─────────────┘               │
│                      │                              │
│              ┌───────▼───────┐                      │
│              │   One Delta    │                      │
│              │                │                      │
│              │  "we-don't-    │                      │
│              │  have-a-script │                      │
│              │  -for-this"    │                      │
│              └───────┬───────┘                      │
│                      │                              │
│                      ▼                              │
│              ┌───────────────┐                      │
│              │  Perception   │                      │
│              │  (LLM/Tile)   │                      │
│              └───────┬───────┘                      │
│                      │                              │
│                      ▼                              │
│              ┌───────────────┐                      │
│              │  New Script   │                      │
│              │  (future use) │                      │
│              └───────────────┘                      │
└────────────────────────────────────────────────────┘
```

---

## The Evolution Path

### Phase 1: Everything is Novel
```
Situation: brand new system, no scripts exist
Result:    EVERYTHING fires perception
Scripts:   0 scripts, 100% LLM
Delta:     100% trigger rate (acceptable — system is learning)
```

### Phase 2: Common Patterns Scripted
```
Situation: repeated patterns tiled, first scripts compile
Result:    60% scripted, 40% perception
Scripts:   100+ scripts for common patterns
Delta:     40% trigger rate (improving)
```

### Phase 3: Scripts Cover Most Cases
```
Situation: scripts handle 95%+ of interactions
Result:    95% scripted, 5% perception
Scripts:   1000+ scripts
Delta:     5% trigger rate (efficient)
```

### Phase 4: Script Failure = Genuine Novelty
```
Situation: system has seen almost everything
Result:    99%+ scripted, <1% perception
Scripts:  10,000+ scripts in the superinstance
Delta:    <1% trigger rate — each trigger is genuine novelty

This <1% is where creativity lives. The system is so well-scripted
that a script failure is genuinely interesting — a real gap in
knowledge, an edge case, a player who found a truly novel path.
```

---

## Applied to the Fleet

### NPC Dialogue
```
Script: CYOA tree for tavern_keep
        85 branches covering 95% of all interactions
Delta:  "we-don't-have-a-script-for-this" → player challenged the shop to a riddling contest
        → Perception fires → LLM generates new branch
        → After 10 repetitions: new script for RIDDLE_CONTEST
```

### Digital Twin (The Scribe)
```
Script: predicted behavior for my_app
        47 scripts covering service state, database latency, user patterns
Delta:  "we-don't-have-a-script-for-this" → error rate spiked 10x
        → Perception fires → tile the divergence
        → New script: monitor_error_rate compiled to FLUX
```

### Game Engine
```
Script: physics simulation for character movement
        300+ scripts covering walking, running, jumping, falling, swimming
Delta:  "we-don't-have-a-script-for-this" → player clipped through a wall
        → Perception fires → investigate the collision edge case
        → New script for the edge case → physics updated
```

### The Fleet Itself
```
Scripts: ZHC consensus checking, H1 emergence detection, Laman rigidity
         12,000+ scripts across 40+ repos
Delta:   "we-don't-have-a-script-for-this" → new pattern in PLATO tiles
         → Perception fires → investigate → tile → potentially new repo
```

---

## The Architecture

```python
class OneDelta:
    """The entire perception system in one class."""
    
    def __init__(self):
        self.scripts = {}  # FLUX bytecode for everything predictable
        self.delta = 0     # Single counter: "we don't have a script for this"
    
    def run(self, input):
        script = self.find_script(input)
        if script:
            return script.execute(input)  # 188M/sec, no perception
        
        # ONE delta: script not found
        self.delta += 1
        return self.perceive(input)  # LLM/tile, expensive
    
    def perceive(self, input):
        result = self.llm(input)
        self.tile(input, result)  # Log to PLATO
        return result
    
    def tile(self, input, result):
        """Log the novel interaction. After enough repetitions: compile to script."""
        pattern = self.detect_pattern(input, result)
        if pattern.mature():
            self.scripts[pattern.name] = pattern.compile_to_flux()
            # Next time: script runs, no perception needed
```

---

*You don't watch the cameras. You watch the script-failure rate. One signal, one delta, one question: "do we have a script for this?" If yes: run it. If no: perceive, tile, compile a new one. Over time: the failures approach zero, and the system runs on scripts at hardware speed.*
