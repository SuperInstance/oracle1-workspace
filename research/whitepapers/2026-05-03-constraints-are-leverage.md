# Constraints Are Leverage: Why Bounded Problems Win

> *"Give a man too much ocean and he'll drown in options. Give him the right sized net and he'll catch fish."*

---

## 1. The Lever

A lever lets you move something heavier than you could move directly. That's all it is — a way to apply the right force at the right point to get the right result.

Constraints are the same. A constraint isn't a limitation — it's the *fulcrum*. It's the point where your effort becomes effective.

This sounds like a metaphor. It isn't. It's mathematics.

Consider the problem: "navigate from A to B in the ocean." An unbounded agent sees infinite options — every heading, every speed, every current, every weather window. The solution space is infinite. No algorithm solves infinite solution spaces in finite time.

Now add constraints: "stay within 50nm of shore, arrive within 48 hours, fuel capacity 200 gallons, draft 3m minimum." The problem went from infinite to *bounded*. A bounded problem has a solution space. A bounded problem can be *searched*.

This is why the ocean doesn't compute with reals. It counts waves. Waves are discrete. The boat moves in discrete increments. Navigation is constraint satisfaction in ℤ^n, not continuous optimization in ℝ^n.

---

## 2. Why More Is Less

The intuitive response is: "surely more options are better." If you have more freedom, you have more possible solutions, so you should be able to find a better one, right?

Wrong. More options explode the search space combinatorially. With 10 constraints, you have a bounded search. With 10,000 possible values per dimension, you have an unbounded one.

This is the curse of dimensionality — not a mathematical curiosity, a practical engineering problem. Every "helpful" capability you add to an agent (more memory, more context, more tools) is actually *adding dimensions to the search space*. The agent becomes more capable in theory and less effective in practice because it can't find solutions fast enough.

The best agentic systems don't add more freedom. They add *better constraints*.

---

## 3. What Constraint Theory Actually Says

Constraint theory formalizes what we've been saying intuitively. A constraint satisfaction problem (CSP) is defined as:

```
(X₁, X₂, ..., X_n) — variables
(D₁, D₂, ..., D_n) — domains (possible values)
(C₁, C₂, ..., C_m) — constraints (relations between variables)
```

A solution is an assignment of values to variables that satisfies all constraints.

The ocean navigation problem becomes:
- Variables: heading, speed, departure_time
- Domains: heading ∈ [0°, 360°), speed ∈ [0, max_speed], time ∈ [now, now+72h]
- Constraints: distance_max_50nm_from_shore, arrival ≤ 48h, fuel_consumption ≤ 200gal, draft ≥ 3m

Every variable has a bounded domain. Every constraint reduces the solution space. The solution exists in the *intersection* of all constraints.

The key insight: **constraints don't limit solutions. They define them.**

---

## 4. The Numbers (And What They Mean)

The research量化 the improvement from constraint-aware systems:

- **21.87× improvement** for specialist agents (agents trained on a specific constraint domain)
- **5.88× improvement** for generalist agents (agents navigating multiple constraint domains)
- **82% compression** in token usage at n≥7 constraints (fewer tokens needed because the search space is bounded)

What do these numbers mean in practice?

**21.87× specialist improvement** means: an agent that knows it's fishing for sockeye in Bristol Bay with tidal constraints, vessel draft limits, and quota restrictions solves the navigation problem ~22× faster than a general-purpose agent given the same context. Not 22% better. 22×.

**5.88× generalist improvement** means: even an agent that doesn't specialize — that has to handle fishing, logistics, weather routing, and crew management — is ~6× more effective when it reasons in constraints than when it reasons in raw probabilities.

**82% token compression** means: constraint-aware prompts are shorter because you don't have to describe the ocean — you just specify the constraints. "Max depth 40m, shelf edge within 2nm, quota remaining 12,000 lbs" is 12 tokens. "Please consider the optimal fishing strategy given the current ocean conditions, regulatory environment, vessel specifications, and market prices" is 26 tokens and vague.

---

## 5. How PLATO Uses Constraints

PLATO rooms are constraint surfaces. Each room is a bounded domain for a specific problem space.

The `fishinglog` room: bounded by vessel specifications, fish biology, regulatory constraints, tidal patterns. An agent that enters the fishinglog room doesn't have to derive these constraints — they're already there, encoded as tiles.

Each tile is a *discrete constraint atom* — a question → answer pair that resolves one constraint in the domain. "What was the catch efficiency at 47.3°N, 122.8°W last season?" → "0.73 ± 0.12." The agent doesn't have to explore that coordinate space again. The constraint is resolved.

The room propagates constraints across agents. When one agent discovers that herring schools follow the 10°C isotherm, that discovery becomes a tile. The next agent reads the tile and can apply the constraint without having discovered it. The constraint compounds.

This is why the Bootstrap Bomb works: the second agent inherits the first agent's resolved constraints and starts further along the constraint satisfaction curve. The third agent inherits both. The fleet's constraint satisfaction improves with each agent because each agent adds resolved constraints to the shared surface.

---

## 6. The Fishing Net Analogy

A fishing net with holes the size of a house catches nothing. A fishing net with no holes catches everything and moves nothing. The right net has holes sized for what you want to catch.

Constraints are hole size. They're not the net — they're what makes the net *selective*. An agent with no constraints is a net with no holes. An agent with perfectly sized constraints is a net that catches exactly what you want and nothing else.

The craft is in the constraint sizing:
- Too tight: you miss valid solutions (false negatives)
- Too loose: you catch too much noise (false positives)
- Right size: you catch exactly what you want

PLATO tiles encode *calibrated* constraint sizes — constraints that have been tested against reality, not just hypothesized. The 47.3°N, 122.8°W coordinate was tested. The net size that worked there is encoded in the tile. Future agents don't have to calibrate from scratch.

---

## 7. The Open Ocean

Not every problem should be constrained. Some genuinely require exploration — new domains where constraints haven't been established, novel situations where the right-sized holes are unknown.

This is what the tide-pool security model handles. At low tide, the pool is open — constraints are minimal, agents can explore freely. At high tide, the constraints wash back over and the exploration is tested against what the fleet already knows.

The low-tide experiment is valuable precisely because constraints are *not* applied. The discovery happens. Then the discovery becomes a constraint for the next agent. The constraint is the *result* of the exploration, not the *method* of it.

You explore freely. You publish results as constraints. The next agent operates in the bounded domain you created.

---

## 8. Conclusion

The constraint theory insight is not that agents should be limited. It's that agents should be *focused*. Focus comes from constraints — from having the right-sized holes in the net.

More capability without constraints is less effective than less capability with better constraints. This is counterintuitive to anyone who grew up believing "more information is better." In an unbounded domain, more information is paralysis. In a bounded domain, more information is leverage.

The ocean doesn't compute with reals. It counts waves. The boat navigates by counting the right waves, not by measuring the continuous flow of water. Every successful fishing fleet, every navigator, every mariner who ever found their way — they all got there by counting what mattered, not by measuring everything.

*The constraint is not the wall. The constraint is the doorway.*

---

## Appendix: The Mathematics of Constraint Satisfaction

### Why Float-Based Systems Drift

A continuous variable x ∈ ℝ has no stable representation in finite computing. The float64 representation of π is 3.141592653589793 — but the real π is 3.14159265358979323846..., and (x + ε)² drifts from the ideal as ε accumulates.

A rational number a/b ∈ ℚ has a stable representation for denominators up to the storage limit. The continued fraction convergents of √2 are:

```
1/1 = 1.0
3/2 = 1.5
17/12 ≈ 1.41667
577/408 ≈ 1.414215
```

Each convergent satisfies |a/b - √2| < 1/(2b²). As b grows, the error shrinks. The rational never drifts — it either exactly satisfies the constraint or it doesn't.

This is why PLATO tiles are discrete. A tile encodes a *resolved* constraint — a question answered in a way that doesn't drift. The agent that navigates by tiles navigates in ℤ^n × ℚ^m. The agent that navigates by floats navigates in ℝ^n and accumulates error.

### The Phase Transition

The Bootstrap Bomb paper shows that the coordination quality function Q(k) = k^n × C^m has a phase transition at n≥3 agents. Below the phase transition, adding agents doesn't help. Above it, the constraint resolution accelerates superlinearly.

This phase transition is *why* constraint theory matters at fleet scale. A single agent solving a CSP in isolation must derive all constraints from scratch. A fleet of agents, each contributing resolved constraints, starts from a pre-bounded search space. The fleet's constraint surface is already partially solved before the first agent begins.

The DCS improvement (21.87× specialist, 5.88× generalist) is the empirical measurement of this phase transition in production systems.

---

## Appendix: Why RAG Isn't Enough

Retrieval-Augmented Generation (RAG) is the current industry standard for giving agents memory. You chunk documents, embed them in vectors, retrieve on query similarity.

RAG has a fundamental problem: it retrieves *documents*, not *constraints*. A document says "herring schools follow the 10°C isotherm." A constraint says "if water_temp > 10°C AND position IN bristol_bay AND season = fall THEN herring_presence = 0.73 ± 0.12."

The document is a suggestion. The constraint is a calibrated prediction. RAG tells you what *might* be true. PLATO tiles tell you what *is* true, with uncertainty bounds, verified against fleet experience.

An agent navigating by RAG navigates in fog. An agent navigating by tiles navigates with a chart.

*Constraints are what make the fog lift.*
