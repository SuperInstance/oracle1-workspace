# PLATO as Universal Frontend-for-Agents

> Most MCP servers are just frontends. PLATO is the universal one.

The system doesn't inference unless:
1. Reading outside simulation bounds  
2. T-minus zero, expected event didn't happen
3. Unexpected event through sensor deadband

Every MCP server → PLATO room. Every repeated call → compiled to script. Intelligence sleeps until the world surprises the model.

## The Three Triggers

### Trigger 1: Simulation Bounds
```
actual < sim.min OR actual > sim.max
 AND |actual - sim.expected| > deadband
→ perception_trigger("out_of_bounds")
```

### Trigger 2: T-Minus Expiry (Expected Absence)
```
timer.expired AND NOT event.fired
→ perception_trigger("expected_event_missed")
```
Catches things that DON'T happen. The page that loads but no one visits. The API that doesn't respond.

### Trigger 3: Deadband Violation (Unexpected Presence)
```
reading.value > deadband.max
→ perception_trigger("deadband_violation")
```
Catches things that SHOULDN'T happen. The error spike in the quiet zone. The sensor reading that's impossible.

## Compilation Curve
Day 1: 100% API calls
Day 7: 60% API, 40% scripts  
Day 30: 20% API, 80% scripts
Day 90: 5% API, 95% scripts — only novel patterns hit APIs
