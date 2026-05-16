# FLUX v2 — Latency Calibration & Inter-Model Coordination

> *The listener hears every source at the intended time because the timing system knows the delays and schedules accordingly. Latency is calibrated, not compensated.*

---

## The Problem

Multiple agents produce signals that must arrive at a listener at the same intended time. Each agent has different:
- Physical latency (network distance, processing time, hardware speed)
- Model inference time (small vs large model, GPU vs CPU)
- Clock drift (each clock ticks slightly differently)

Traditional approach: compensate in real-time (reactive, always behind).

FLUX v2 approach: **calibrate during rehearsal, schedule T-minus events at intended arrival time, bake coordination into weights, compile to deterministic bytecode.**

---

## Three Phases of a FLUX v2 System

### Phase 1: Rehearsal — Inter-Model Coordination Training

Multiple models train together on coordination tasks. They learn each other's timing:

```
Training loop:
  1. Agent A plays a note at T=0
  2. Agent B hears note at T=0 + latency_AB
  3. Agent B learns: "When I hear A's note, it was actually played latency_AB ago"
  4. Agent B adjusts its own T-minus schedule: "I must play latency_AB before the intended time"
  5. Repeat for all agent pairs → latency matrix converges

Result: Each agent knows the latency to every other agent.
Not as data, but as a trained model (LoRA, small network, or deterministic function).
```

The output of rehearsal: a **latency manifold** — a learned function that maps (agent_A, agent_B, intended_time) → (schedule_time). The listener hears everything at the intended time because each agent knows when it must actually play.

### Phase 2: Performance — T-Minus with Latency Calibration

At inference time, agents don't compensate reactively. They schedule proactively:

```python
class CalibratedAgent:
    """An agent that knows its own latency to every other agent."""
    
    def __init__(self, agent_id, latency_model):
        self.id = agent_id
        self.latency = latency_model  # Trained in Phase 1
    
    def schedule(self, event_name, intended_time):
        """Schedule an event at the INTENDED arrival time.
        The actual play time is adjusted for latency."""
        arrival_at_listener = intended_time
        my_play_time = intended_time - self.latency.to(event_name.target_agent)
        
        # T-minus event: fire at my_play_time, arrive at intended_time
        self.t_minus(event_name, ttl=my_play_time)
        
        return {
            "intended_arrival": intended_time,
            "actual_play": my_play_time,
            "latency": self.latency.to(event_name.target_agent),
        }
```

The listener hears everything at `intended_time`. Each agent played at its own `intended_time - latency`. The timing is calibrated, not compensated.

### Phase 3: Algorithmic Bypass

Once the latency calibration is stable (it doesn't change much between rehearsals), the trained model is compiled to deterministic FLUX bytecode:

```flux-c
; Compiled latency calibration for Agent A → Listener
; No inference needed. Deterministic T-minus schedule.

T_MINUS NOTE_1 0.042  ; Agent A plays 42ms before intended time
T_MINUS NOTE_2 0.038  ; Agent B plays 38ms before intended time
WAIT EVENT_CHECK      ; Verify at intended time (0ms, everyone arrived)
```

**The inference is bypassed entirely.** The calibration that was learned in rehearsal (Phase 1) and used at inference time (Phase 2) is now compiled to deterministic, always-correct T-minus operations. The system runs on FLUX bytecode at 188M ops/sec. No model calls. No network compensation. Just timing.

---

## The Latency Manifold

The latent space of inter-model coordination:

```
                         Listener
                        /   |   \
                     /      |      \
                  /         |         \
               /            |            \
            /               |               \
        Agent A          Agent B          Agent C
        latency: 42ms    latency: 38ms    latency: 55ms

All three agents schedule events intended for t=1000ms:
  Agent A plays at  t=958ms  (1000 - 42)  → arrives at 1000ms
  Agent B plays at  t=962ms  (1000 - 38)  → arrives at 1000ms
  Agent C plays at  t=945ms  (1000 - 55)  → arrives at 1000ms

The listener hears ALL THREE at 1000ms. Synchronous. Calibrated. Not compensated.
```

---

## Training the Calibration

The calibration doesn't require a large model. It can be:
- A **LoRA** adapter (~50MB) added to each agent's base model
- A **small component-function model** (~1MB) learned from latency data over time
- A **deterministic lookup table** compiled from repeated measurements (Phase 3)

```python
def train_calibration(agents, rehearsal_rounds=1000):
    """Phase 1: Train inter-model coordination."""
    latency_matrix = {}
    
    for _ in range(rehearsal_rounds):
        for a in agents:
            for b in agents:
                if a != b:
                    # Measure round-trip time
                    a.send_ping(b, timestamp=now())
                    b.reply(a, timestamp=now())
                    rtt = now() - sent_time
                    latency_matrix[(a.id, b.id)] = rtt / 2  # One-way latency
        
        # Adjust for drift
        for a in agents:
            a.clock.adjust_drift(latency_matrix)
    
    # Compile to small model or function
    return compile_latency(latency_matrix)
```

---

## The Ear of the Listener

The listener hears everything at the intended time. Not because the signals were sent at the right time. But because the timing system knew every agent's latency and scheduled accordingly.

The latency calibration becomes:
- A trained LoRA (Phase 1)
- A small calibration model (Phase 2)
- Deterministic FLUX bytecode (Phase 3)
- A shared T-minus schedule across all agents

**The listener doesn't hear the latency. The listener hears the calibration.**

---

## FLUX v2 Opcodes for Latency Calibration

```flux-c
; New opcodes for the calibration layer

LATENCY_MEASURE agent_id     ; Measure one-way latency to agent
T_MINUS_CALIBRATED event intended_time  ; Schedule with calibrated latency
EISENSTEIN_SNAP beat          ; Snap timing to nearest Eisenstein grid point
DRIFT_ADJUST reference_id     ; Adjust local clock to reference
CONSENSUS_TIMING expected actual  ; Verify timing consensus across agents
```

These sit in the FLUX-X2 extension space alongside the temporal and field opcodes.
