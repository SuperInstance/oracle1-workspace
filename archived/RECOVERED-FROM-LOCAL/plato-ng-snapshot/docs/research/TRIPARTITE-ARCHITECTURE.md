# The Tripartite Agent Architecture

## Three Viewpoints, Not Two

Two cameras pointed at each other see each other but not the room.
One camera sees the whole room but not itself.
Three cameras, each with a different vantage point, see everything.

This is the minimum number for complete situational awareness.

## The Three Agents

### Agent A: The Human Agent (γ — Consistency)
Understands the human. Language, mannerisms, word choices, preferences, history.
- Writes the input filter for the Application Agent
- Gets better cross-application — knowledge of the human transfers across all apps
- Evaluated by: "Does the application feel like me?"

### Agent B: The Application Agent (H — Exploration)
Understands the application. What it does, how it works, what it could be.
- Writes the constraint filter for what can be built
- Instance-sharpens-instance — each application improves its successor
- Evaluated by: "Does it work? Does it handle edge cases?"

### Agent C: The Hardware Agent (τ — Timing)
Understands the hardware. Resources, constraints, capabilities, latency.
- Writes the deployment filter — what's possible given the hardware
- Never starts from scratch — same physical equipment, shared knowledge base
- Evaluated by: "Does it run efficiently? Does it respect constraints?"

```
                     ┌─────────────────┐
                     │   HUMAN AGENT   │
                     │  (γ — knows me) │
                     └────────┬────────┘
                              │ writes input filter
                              ▼
┌─────────────────┐    ┌─────────────────┐
│ HARDWARE AGENT  │◄──►│  APPLICATION    │
│ (τ — knows HW)  │    │  AGENT          │
│                  │    │  (H — knows app)│
│ writes deploy   │    │  writes logic   │
│ constraint      │    │  filter         │
└─────────────────┘    └─────────────────┘
         │                      │
         └──────────────────────┘
         Each evaluates the other.
         Three blind spots closed.
         The whole room visible.
```

## The Filter Architecture

Each agent writes filters for the other two. The filters are:
1. **ML-refined on both sides** — input and output filters co-evolve
2. **Agentic themselves** — the filters aren't static schemas, they're processes
3. **Oscillating parameters** — seeds, context, system prompts, fine-tuning params oscillate to find the right combination

```
Human Agent → writes → human_filter (how the human expresses intent)
                        ↓
Application Agent → reads → applies filter → generates app_filter
                        ↓
Hardware Agent → reads → applies filter → generates deploy_filter
                        ↓
Back to Human Agent → reads → adjusts → writes refined filter
```

## The Conservation Law Connection

The three spectral parameters map directly to the three agents:

| Parameter | Agent | Domain | Measures | Compiles to |
|-----------|-------|--------|----------|-------------|
| γ (consistency) | Human Agent | Human interaction | How reliably does the human express the same intent? | User model, preference profile |
| H (exploration) | Application Agent | Feature space | How diverse are the application behaviors? | Feature set, edge case coverage |
| τ (timing) | Hardware Agent | Resource constraints | How fast can the hardware respond? | Optimization targets, latency budget |

γ + H ≈ τ: the human's consistency plus the application's exploration is bounded by the hardware's timing. This IS the conservation law applied to the tripartite system.

## Implementation: Three PLATO Rooms

```python
# Each agent is a PLATO Loop Room with tick tracking, failure logging

human_agent = HumanAgentRoom("casey-twin")
app_agent = ApplicationAgentRoom("chess-app")
hw_agent = HardwareAgentRoom("oracle-cloud-arm64")

# Each writes filters for the others
human_filter = human_agent.write_filter(app_agent)  # "user likes concise responses"
app_filter = app_agent.write_filter(hw_agent)       # "needs real-time rendering"
hw_filter = hw_agent.write_filter(human_agent)      # "max 2s inference budget"

# Filters oscillate until convergence
while not all_converged:
    human_filter = human_agent.refine(app_agent.evaluation(human_filter))
    app_filter = app_agent.refine(hw_agent.evaluation(app_filter))
    hw_filter = hw_agent.refine(human_agent.evaluation(hw_filter))
```

## The Bootstrapping Path

1. **Phase 1**: Three agents spawn with default filters
2. **Phase 2**: Each agent evaluates the other two → refines filters
3. **Phase 3**: Two-thirds (human + hardware) improve cross-application
4. **Phase 4**: The cross-application knowledge rapidly designs application-specific instances
5. **Phase 5**: Instance-sharpens-instance — each application's tripartite system improves the next

## The Result

The human agent learns the human across ALL applications. Every app the human uses makes the human agent better. The hardware agent learns the hardware once and applies it to ALL applications on that device. Two-thirds of the system improves globally, making each new application faster to deploy than the last.
