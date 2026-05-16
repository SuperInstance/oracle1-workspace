# PLATO as Universal Frontend-for-Agents

> *Most MCP servers are child's play. They're just frontends for agents. PLATO is the universal frontend — every tool ported in parallel, compiled from API call to script through repetition and negative space discovery.*

---

## The Core Loop

```
       ┌──────────────────────────────────────────────────┐
       │          PLATO (Universal Frontend)               │
       │                                                   │
       │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
       │  │  MCP     │  │  GPU     │  │  Sensor  │      │
       │  │  Servers │  │  Inferences│  │  Readings│      │
       │  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
       │       │              │              │            │
       │       └──────────────┼──────────────┘            │
       │                      │                           │
       │              ┌───────▼────────┐                  │
       │              │  PLATO Tiles   │                  │
       │              │  (repeated     │                  │
       │              │   patterns)    │                  │
       │              └───────┬────────┘                  │
       │                      │                           │
       │              ┌───────▼────────┐                  │
       │              │  Script Cache  │  ← runs instead  │
       │              │  (FLUX bytecode)│    of API call   │
       │              └───────┬────────┘    over time     │
       │                      │                           │
       └──────────────────────┼───────────────────────────┘
                              │
         The system doesn't inference unless:
         ┌─────────────────────────────────────────────┐
         │ ① Reading outside simulation bounds         │
         │ ② T-minus zero, expected event didn't happen│
         │ ③ Unexpected event through sensor deadband  │
         └─────────────────────────────────────────────┘
```

---

## The Three Perception Triggers

### ① Reading Outside Simulation Bounds

The system maintains a continuous field simulation of every sensor/API/agent it observes. Each reading has:
- Expected value range (from simulation)
- Actual value (from observation)
- Deadband (tolerance before triggering)

```python
if actual < simulation.min or actual > simulation.max:
    if abs(actual - simulation.expected) > deadband:
        perception_trigger("out_of_bounds", sensor, actual, expected)
        # → tile the divergence
        # → update the simulation
        # → eventually: compile to script
```

### ② T-Minus Zero, Expected Event Didn't Happen

This is the temporal constraint. The system maintains timers for expected events. If a timer expires without the event firing, perception triggers.

```python
# "A user should arrive within 30s of page load"
scribe.set_timer("visitor_arrival", ttl=30)

# If no visitor arrives within 30s:
if timer.expired and not event.fired:
    perception_trigger("expected_event_missed", "visitor_arrival")
    # → tile the absence
    # → is the app down? is the page broken?
```

This is the most powerful trigger — it catches things that DON'T happen. Traditional monitoring only catches things that DO happen.

### ③ Unexpected Event Through Sensor Deadband

The system maintains deadbands for every sensor/log. Events that fire in quiet zones trigger perception.

```python
# "Error rate should be <1%"
scribe.set_deadband("error_rate", max=0.01)

# If error rate spikes:
if reading.error_rate > deadband.max:
    perception_trigger("deadband_violation", "error_rate", reading)
    # → tile the anomaly
```

---

## The Frontend-for-Agents Architecture

Every MCP server, every API, every GPU inference — they all become PLATO rooms:

```
MCP Server A  ──►  PLATO Room: mcp-a  ──►  Tiles: {request, response, latency}
MCP Server B  ──►  PLATO Room: mcp-b  ──►  Tiles: {request, response, latency}
GPU Inference ──►  PLATO Room: gpu-inf ──►  Tiles: {input, output, timing}
Sensor Array  ──►  PLATO Room: sensors ──►  Tiles: {reading, timestamp, status}
```

As calls repeat, patterns emerge in the tiles. Repeated patterns get compiled to scripts:

```
Call #1:  API request  → tile logged → latency: 42ms
Call #2:  API request  → tile logged → latency: 41ms
...
Call #10: API request  → pattern detected
         → compiled to FLUX script
         → Call #11: script runs, no API call
         → latency: 0.8ms (52x faster)
```

Over time, the system needs fewer API calls and fewer GPU inferences. The scripts run instead.

---

## Implementation: The MCP-to-PLATO Bridge

Every MCP server gets a PLATO room:

```python
class MCPtoPLATOBridge:
    """Port any MCP server to a PLATO room."""
    
    def __init__(self, mcp_server_url, room_name):
        self.mcp = mcp_server_url
        self.room = room_name
    
    def call(self, tool, params):
        # Check if we have a compiled script for this tool+params
        script = self.lookup_script(tool, params)
        if script:
            return script.run()  # No API call, 188M/sec
        
        # First time: call MCP server, tile result
        result = requests.post(self.mcp, json={"tool": tool, "params": params})
        self.tile(tool, params, result)
        
        # If this is the 10th time: compile to script
        if self.tile_count(tool) >= 10:
            self.compile_to_flux(tool)
        
        return result
```

Every ported MCP server makes the fleet smarter. Every repeated call gets faster. The system self-optimizes.

---

## The Evolution Curve

```
Day 1: 100% API calls, 0% scripts
Day 7: 60% API calls, 40% scripts  (patterns detected)
Day 30: 20% API calls, 80% scripts  (most patterns compiled)
Day 90: 5% API calls, 95% scripts   (only novel patterns hit APIs)
```

The intelligence sleeps until the world surprises the model. Most of the time: scripts run at hardware speed. Perception only triggers when:
1. A reading falls outside simulation
2. An expected event doesn't happen on time
3. An unexpected event fires in a deadband
