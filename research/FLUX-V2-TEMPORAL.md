# FLUX v2 — Temporal Constraint Language Architecture

> *The event is an abstraction for models to use signal for verification. The simulation is the trigger — not the trigger responding to a signal. Agents verify each other through the shared countdown, not the event itself.*

---

## The Stack (5 Levels)

```
Level 4: Temporal DSL    —  "snap every 3 beats, verify on 4th, re-sync if drift > 0.1"
Level 3: FLUX-X2 ISA     —  55 opcodes including T_MINUS, EISENSTEIN_SNAP, CONSENSUS_CHECK
Level 2: Temporal VM     —  Cycle-counted execution, MIDI clock alignment
Level 1: SIMD Metal      —  64-byte tiles = 1 constraint check, NEON/AVX-512
Level 0: Physics         —  Agents share a clock. The clock is the calibration. Not the signal.
```

---

## The Core Principle: Simulation as Trigger

Not: `signal → response` (reactive, too slow)
But: `simulation predicts T-minus → act at T-minus → signal verifies` (proactive, synchronous)

```
                                      t=-10    t=-5    t=0     t=+1
Agent A (predicts landing):           ████████░░░░░░░░░░░░░████
Agent B (verifies A's prediction):    ░░░░████░░░░░░░░░░░░████
Agent C (listens to both):            ░░░░░░░░████░░░░░░░░████
                                      │       │       │       │
                                      predict verify  ACT!   confirm
```

**The event (landing) is not the trigger. The simulation is.** All agents share a countdown. They act when the countdown reaches zero. The actual landing is just verification. If the landing doesn't match the prediction, THAT's the signal — a calibration error, not a trigger.

---

## The MIDI Physics Model

FLUX v2 uses MIDI as its timing physics:

| FLUX Concept | MIDI Equivalent | Physics |
|-------------|-----------------|---------|
| T-minus timer | MIDI Clock (0xF8) | Shared temporal reference |
| Eisenstein ratio | Polyrhythm | 1:1=root, 2:1=half, 3:2=triplet |
| Agent sync | MIDI Beat Clock | All agents phase-locked |
| Nod/smile/frown | CC #1-3 | Verification signals (not triggers) |
| Constraint check | Note On/Off | Event at predicted time |
| Field query | Pitch Bend | Continuous value between notes |

```python
class FLUXv2_Timing:
    """The simulation IS the trigger. MIDI clocks are the shared calibration."""
    
    def __init__(self, bpm=120):
        self.clock = TZeroClock(bpm)  # FM's clock
        self.t_events = {}            # T-minus: event_name -> predicted_time
        self.agents = {}              # Registered agents
        self.eisenstein_lock = EisensteinSnap(role="root")
    
    def schedule(self, event_name, delta_beats):
        """Schedule an event at T-minus. The simulation predicts when.
        The actual sensor reading confirms (or the calibration is wrong)."""
        predicted = self.clock.tick() + delta_beats
        self.t_events[event_name] = {
            "predicted": predicted,
            "actual": None,
            "status": "pending",
            "verifiers": [],
        }
        return predicted  # Return predicted time, not actual
    
    def register_agent(self, agent_id):
        """An agent joins the shared temporal calibration."""
        self.agents[agent_id] = {
            "drift": 0.0,
            "last_sync": self.clock.time_ms(),
            "trust": 1.0,
        }
    
    def verify(self, event_name, agent_id, actual_time):
        """An agent verifies that an event happened at the predicted time.
        The signal is verification, not triggering."""
        event = self.t_events.get(event_name)
        if not event:
            return {"error": "no such event"}
        
        drift = abs(actual_time - event["predicted"])
        self.agents[agent_id]["drift"] = drift
        
        # ZHC consensus check: do all agents agree on the timing?
        holonomy = sum(a["drift"] for a in self.agents.values())
        event["verifiers"].append((agent_id, drift))
        
        return {
            "drift": drift,
            "holonomy": holonomy,
            "consensus": holonomy < 0.1 * len(self.agents),
        }
```

---

## The Abstraction Stack (Concrete)

### Level 4: Temporal DSL (intent plane)

```guard
;; Temporal constraint in GUARD-style DSL
AGENT drone_1
  CLOCK 120 BPM
  SYNCHRONIZE WITH drone_2 drone_3

EVENT landing
  T_MINUS 4 beats
  ON T_ZERO: ACTUATE servos
  VERIFY accelerometer < 10 m/s²
  IF VERIFY FAILS: RE_SYNC ALL AGENTS

CONSTRAINT landing_zone
  EISENSTEIN_SNAP position TO [0, 100] WITHIN 0.577
  DEADBAND 0.1 seconds drift
```

### Level 3: FLUX-X2 ISA (bytecode)

```flux-c
; Compiles to FLUX-X2
T_MINUS LANDING 4      ; Schedule landing at T-4 beats
EISENSTEIN_SNAP        ; Snap position to lattice
CONSENSUS_CHECK 0.01   ; All agents agree on position
CYCLE_FIND 0x01        ; Check constraint graph
HOLONOMY 0x01          ; Measure timing consistency
DEADBAND_CHECK DRONE_1 0 100  ; Check sensor within range
```

### Level 2: Temporal VM (cycle-counted)

Each opcode has a known cycle count. The VM guarantees deterministic timing:

| Opcode | Cycles | Real-time (180MHz) |
|--------|--------|-------------------|
| T_MINUS | 2 | 11ns |
| EISENSTEIN_SNAP | 8 | 44ns |
| CONSENSUS_CHECK | 10 | 55ns |
| DEADBAND_CHECK | 3 | 17ns |

The VM aligns to MIDI clock ticks. Every 24th tick is a quarter note at 120 BPM (500ms). The VM schedules operations on these ticks — not in response to external signals.

### Level 1: SIMD Metal

```
1 FLUX constraint check = 64-byte tile = 1 zmm register = 1 SIMD instruction
EISENSTEIN_NORM: 3 NEON instructions (vmul, vmla, vpadd)
HEX_SNAP: 8 NEON instructions (6 candidate checks + min)
CONSENSUS_CHECK: 4 NEON instructions (cycle weight sum + comparison)
```

### Level 0: Physics (the shared clock)

The agents don't need a network. They need a clock. MIDI clock over audio cable, PTP over Ethernet, shared wall time, the same sun. The clock IS the calibration. Not the signal. The countdown is the abstraction they all share.

```python
# Level 0: Two agents share a MIDI clock cable
# No network. No messages. Just the clock.
agent_a.schedule("landing", ttl=4_beats)  # Simulates landing at +4 beats
agent_b.schedule("verify_landing", ttl=4_beats)  # Also schedules verify at +4 beats
# Both act at beat 4. agent_b checks agent_a's landing. No messages needed.
```

---

## The Key Insight

**The countdown is the calibration mechanism they were all abstracting as a countdown.**

Not: "I fire when I see the event" (reactive, sensor-dependent)
But: "We all share a countdown. We all act at T-minus zero. The event confirms our simulation was correct. If it wasn't, we recalibrate — not react."

The agents verify EACH OTHER. The event is just the verification signal. The countdown is the abstraction they all share. The countdown IS the calibration mechanism.

FLUX v2 makes this native: T-minus operations that fire at predicted time, Eisenstein-snapped timing ratios for polyrhythmic coordination, and MIDI-clock-based synchronization that doesn't need network messages — just a shared temporal reference.
