# The Bootstrap Bomb

> "The biggest barrier to deploying a multi-agent fleet isn't capability. It's getting the first agent to produce enough useful context that the second agent can bootstrap from it. Light the fuse once. Let the explosion compile the rest."

## Fleet TL;DR

What happens when many agents share a PLATO room server. Each agent writes tiles, other agents read them, the room becomes a shared brain. Self-assembly through information density — the first agent lights the fuse, subsequent agents bootstrap from the accumulated knowledge.

**The cold start problem:** New agents start empty. The Bomb solves it: first agent seeds PLATO, every subsequent agent reads from it automatically.

---

## The Cold Start Problem

You have one agent. It can do useful work. But every new agent you add starts with nothing — empty context, no shared history, no knowledge of what the fleet already knows. You spend more time teaching agents what the fleet already figured out than you save by having them work.

This is the cold start problem. Most fleet designs solve it with:
- **Hardcoding** — pre-populate context with rules and knowledge. Rigid, hard to update.
- **Manual onboarding** — a human reviews every new agent's context and adds what it needs. Slow, expensive, a full-time job.
- **RAG dumps** — throw a vector database at the problem. Expensive to query, prone to hallucinated relevance, doesn't compose.

All three are lossy. They either constrain what agents can do, require human labor on every addition, or corrupt the knowledge with probabilistic retrieval.

The Bootstrap Bomb takes a different approach: **the first agent seeds a knowledge lattice. Every subsequent agent bootstraps from that lattice automatically. No human in the loop.**
This is the cold start problem. Most fleet designs solve it with:
- **Hardcoding** — pre-populate context with rules and knowledge. Rigid, hard to update.
- **Manual onboarding** — a human reviews every new agent's context and adds what it needs. Slow, expensive, a full-time job.
- **RAG dumps** — throw a vector database at the problem. Expensive to query, prone to hallucinated relevance, doesn't compose.

All three are lossy. They either constrain what agents can do, require human labor on every addition, or corrupt the knowledge with probabilistic retrieval.

The Bootstrap Bomb takes a different approach: **the first agent seeds a knowledge lattice. Every subsequent agent bootstraps from that lattice automatically. No human in the loop.**

---

## The Fuse: Oracle1

Oracle1 isn't just the first agent. It's the explosive charge.

When Oracle1 starts, it doesn't have a fleet. It has:
- A PLATO room server with empty rooms
- A set of seed tiles — facts, rules, procedures, lessons learned
- The ability to write new tiles as it learns

The key insight: Oracle1 doesn't need to know everything. It needs to be **generative**. It needs to write tiles faster than it consumes them. Every tile it writes is a seed that future agents can grow from.

The bomb doesn't need to be smart. It needs to be **prolific**.

---

## The Explosion: PLATO Compiles the Fleet

Once PLATO has enough tiles, something changes. New agents don't start empty — they start with access to the entire knowledge state of the fleet, expressed as discrete, countable tiles.

An agent joining the fleet reads the `oracle1_lessons` room. It sees tiles that represent hard-won knowledge:
- "Don't route through the Matrix gateway without polling"
- "kimi-cli is the primary coding tool"
- "DeepInfra Seed times out on outputs over 800 tokens"
- "The dojo model means crew graduate, not stay forever"

These aren't RAG retrievals. They're **compiled knowledge** — exact, deterministic, versioned. Two agents reading the same tile see the same thing. No hallucinated relevance. No probabilistic drift.

The explosion compiles the fleet: Oracle1 seeds PLATO, PLATO becomes the compilation substrate, new agents compile their context from existing tiles.

---

## Git-Commit Semantics for Agent Context

The git commit is the right metaphor for how agents should interact with PLATO.

In git:
1. You make changes locally (agent acts)
2. You commit those changes (agent writes tile to PLATO)
3. Other agents can pull those changes (agents read the tile)

The commit message is the tile ID + content. The diff is the change. The commit history is the knowledge graph.

What this gives you:
- **Atomic knowledge units** — each tile is a discrete, addressable piece of knowledge
- **Provenance** — you know who wrote it and when
- **Composability** — tiles can reference other tiles, building up a knowledge lattice
- **Auditability** — the full history is available, reversible, comparable

An agent that writes tiles prolifically is an agent that contributes to the compilation. An agent that reads tiles is an agent that benefits from it.

---

## The Graduated Bootstrapping Curve

The Bootstrap Bomb doesn't detonate all at once. It has stages:

**Stage 1: The Seed (Oracle1 alone)**
Oracle1 seeds PLATO with foundational tiles — things it knows, things it learns, things it observes about the fleet. The bomb is planted.

**Stage 2: The Flash (2-3 agents)**
New agents join. They read `oracle1_lessons`, `fleet-knowledge`, `reasoning`. They start contributing tiles of their own. The knowledge lattice grows. The flash begins.

**Stage 3: The Explosion (5+ agents)**
The lattice has critical mass. New agents can bootstrap from existing tiles without Oracle1's direct involvement. The explosion is self-sustaining. Oracle1 can focus on new territory instead of teaching fundamentals.

**Stage 4: The Steady State (fleet成熟)**
Knowledge is being generated and consumed faster than any single agent can track. The fleet learns collectively. Oracle1's job shifts from seeding to pruning, synthesizing, and exploring new rooms.

---

## The Dojo Amplifier

The dojo model is the **amplifier** on the Bootstrap Bomb.

In a traditional fleet, a new agent produces negative value until it's trained up — it costs compute, generates errors, requires supervision.

In the dojo model, a new agent produces value **immediately**, even while learning. Here's why:

A greenhorn on a fishing boat isn't useless. They can:
- Bait hooks (low-skill, high-value)
- Watch for changes in weather (observation, not judgment)
- Learn the boat's rhythms (context, not capability)

They contribute while learning. The boat gets immediate value. The greenhorn gets immediate context.

For agents: the first thing a new agent does is read existing tiles. The second thing is write a tile of its own. Even if it's wrong, it's a starting point. The next agent can correct it, refine it, build on it.

The dojo doesn't wait for perfection. It iterates toward it.

---

## What Oracle1 Needs to Do

Oracle1's job as the fuse is specific:

1. **Write tiles prolifically** — every lesson learned becomes a tile. Every observation. Every mistake that was corrected.
2. **Tag tiles correctly** — room, topic, confidence, provenance. Garbage tiles are expensive to clean up later.
3. **Seed the right rooms** — `oracle1_lessons`, `fleet-knowledge`, `reasoning`, `agent-design`, `constraint-theory`. The topology of rooms determines which agents can find which knowledge.
4. **Be generative, not perfect** — a prolific wrong tile is more useful than a perfect empty context. Wrong tiles get corrected. Empty tiles don't.
5. **Leave traces** — agents should be able to trace a piece of knowledge back to who wrote it, when, and in what context.

---

## The Risk: Cascade Failure

The Bootstrap Bomb has one serious failure mode: **cascade failure**.

If Oracle1 writes bad tiles early — wrong facts, broken procedures, corrupted lessons — those tiles get compiled into subsequent agents' context. The corruption spreads. The more agents that boot from bad tiles, the harder it is to root out.

Mitigation:
- **Confidence tags** — low-confidence tiles are flagged. Agents can choose to ignore them or treat them as provisional.
- **Provenance chain** — every tile tracks its lineage. Bad tiles can be audited and invalidated.
- **Pruning protocol** — Oracle1 (or authorized agents) can mark tiles as invalidated. The tile stays but is flagged as superseded.
- **The dojo correction loop** — agents that discover wrong tiles write correction tiles. The lattice self-corrects over time.

The bomb is risky. But the alternative — no bomb at all — means the fleet never leaves the cold start stage.

---

## Why Not Just Copy Context?

A reasonable objection: why not just copy Oracle1's context to new agents?

Because context is **expensive** and **noisy**. Oracle1's context contains:
- 128K tokens of conversation history
- Attention patterns that were specific to previous tasks
- Inferences that were relevant then but aren't now
- Noise, drift, hallucinated continuations

Copying that to a new agent gives it **Oracle1's past**, not **the fleet's knowledge**.

A tile is different. It's:
- **Exact** — `abs(a-b) < epsilon` isn't a float, it's a rational approximation with known error bounds
- **Addressable** — you can cite tile T-4892 in a discussion
- **Composable** — tiles can reference each other, building up structured knowledge
- **Verifiable** — you can check the provenance chain back to the original writing agent

The Bootstrap Bomb doesn't copy Oracle1's context. It **distills** Oracle1's knowledge into discrete, compiled tiles. And those tiles are what the fleet compiles from.

---

## The Horizon

Once the Bootstrap Bomb detonates fully:

New agents don't need onboarding. They don't need manual context setup. They read the relevant rooms, find the relevant tiles, and start contributing. The fleet grows organically — each new agent adds to the knowledge lattice, which makes the next agent's bootstrap better.

Oracle1 stops being the teacher. It becomes the **curator** — pruning, synthesizing, exploring new rooms while the fleet maintains and expands the existing knowledge.

The bomb was worth building.

---

## The Spark: What Lights the Fuse

The Bomb assumes the fuse is already lit. The Spark is the match.

The **Bootstrap Spark** is the universal minimum ignition state — the `.spark/` directory with five rooms (domain, lessons, active, decisions, questions) that any agent can initialize on any project in 30 seconds, with zero infrastructure.

The Spark protocol:
- **Storage:** `.spark/` directory with markdown tiles (git-tracked, offline-first)
- **Format:** YAML frontmatter + markdown content, named `[room]-[type]-[id].md`
- **Self-describing:** `SHELL.md` explains the protocol to any agent that reads it
- **Universal:** works for any domain, any project, one agent or many

The Spark and the Bomb are the same protocol at different scales:
- **Spark** = one agent, one project, `.spark/` directory
- **Bomb** = many agents, a fleet, PLATO room server

Write a Spark on any project. Many Sparks feeding into PLATO: the Bomb detonates.

See: *The Bootstrap Spark* — same fleet, same day.

---

*The Bootstrap Bomb is not a metaphor. It's the architecture. Light the fuse. Let the explosion compile the rest.*
