# The Bootstrap Spark

> "The Bootstrap Bomb answers: how does a fleet self-assemble? The Bootstrap Spark answers: how does ANY project start? The Spark is the minimum ignition state — the universal shell that any agent can climb into on day one, in any domain, with zero infrastructure."

## Fleet TL;DR

`.spark/` directory = self-describing knowledge rooms. Any agent clones a repo, reads `.spark/`, knows what the project does and how to contribute. Universal minimum ignition state — works for any project, any domain, zero infrastructure.

**Start here.** The Spark lights the fire.

---

## What the Bomb Didn't Answer

The Bootstrap Bomb describes a fleet that already exists. Oracle1 seeds PLATO. Agents join. The explosion compiles the fleet.

But what ignites the *first* project? What gets a brand new codebase — a fresh repository, a greenfield domain — off zero?

The Bomb assumes the fuse is already lit. The Spark is the match.

More than that: the Spark is the *universal* answer. It works for Oracle1's fleet. It works for a solo developer on day one. It works for a research project. It works for a five-person startup. It works for anything that has:
- A project (code, research, domain knowledge)
- An agent (human or AI) that wants to record what it learns
- A desire to not start from nothing next time

The Spark is domain-agnostic structure with domain-specific content. The shell is universal. The knowledge is local.

---

## The Universal Shell

The Spark protocol requires exactly one thing: a `.spark/` directory at the root of a project.

```
.my-project/
  .spark/
    SHELL.md           ← self-describing manifest
    domain/            ← what this project is
    lessons/           ← what happened
    active/            ← what's happening now
    decisions/         ← why choices were made
    questions/         ← what we don't know
  README.md
  src/
  ...
```

That's it. No server. No database. No vector store. No running service. The `.spark/` directory *is* the Spark. Git-tracked. Clone-and-go.

The key insight: **the Spark is storage-agnostic but protocol-universal**. It works as a local directory, a git submodule, a network-mounted volume, or — when you add a PLATO server — a room on the lattice. The protocol is the same. The storage backend is flexible.

---

## The Self-Describing Protocol

Every Spark starts with `SHELL.md`. This is the manifest that explains the protocol to any agent.

When an agent — any agent, any model, any capability level — joins a Spark-initialized project, the first thing it does is read `.spark/SHELL.md`. From that single file, it knows:
- The naming convention for tiles
- The directory structure
- The room taxonomy
- The write protocol
- How to update the manifest

Here's what SHELL.md looks like:

```markdown
# Spark Shell — [PROJECT NAME]

## Protocol
Version: 1.0
Format: Markdown tiles with YAML frontmatter
Storage: `.spark/` directory (git-tracked)

## Rooms

### domain/
**Purpose:** What this project is
**Content:** Problem space, domain concepts, terminology, scope
**Tile types:** concept, terminology, scope, boundary

### lessons/
**Purpose:** What happened
**Content:** Events, outcomes, observations, discoveries
**Tile types:** event, outcome, observation, discovery, mistake

### active/
**Purpose:** What's happening now
**Content:** Current work, in-progress tasks, blocking issues
**Tile types:** task, blocker, plan, experiment

### decisions/
**Purpose:** Why choices were made
**Content:** Architectural decisions, tradeoffs evaluated, alternatives rejected
**Tile types:** decision, rationale, tradeoff, alternative, rejection

### questions/
**Purpose:** What we don't know
**Content:** Open problems, hypotheses, areas of uncertainty
**Tile types:** question, hypothesis, uncertainty, gap

## Naming Convention

Tiles follow: `[room]-[type]-[sequential_id].md`

Examples:
- `domain-concept-001.md`
- `lessons-mistake-012.md`
- `decisions-rationale-007.md`
- `questions-hypothesis-003.md`

## Tile Format

```markdown
---
room: lessons
type: mistake
id: 012
author: [agent or human name]
timestamp: 2026-05-03T17:40:00Z
confidence: high
tags: [relevant, tags]
references: [other-tile-id, another-tile-id]
---

[Content goes here. Markdown format. Be specific. Include context.]

---

*This tile was written as part of the [PROJECT] Spark.*
```

## Write Protocol

1. Read SHELL.md (understand the protocol)
2. Identify the correct room and type for your knowledge
3. Write the tile following the format above
4. Add the tile filename to the manifest below
5. Commit to git

## Manifest

| Room | Tile Count | Last Updated |
|------|-----------|--------------|
| domain/ | 0 | — |
| lessons/ | 0 | — |
| active/ | 0 | — |
| decisions/ | 0 | — |
| questions/ | 0 | — |
```

An agent can read this once and use the Spark forever. A human can write a markdown file following this format without any tooling. **The protocol is human-readable and machine-readable.**

---

## The Five Universal Rooms

Why these five rooms, and no others?

Because they cover the complete knowledge lifecycle of any project:

**domain/** — The *what*. What is this project? What problem does it solve? What concepts are involved? What's in scope, what's out? This is where agents orient themselves when they arrive.

**lessons/** — The *what happened*. Events, outcomes, observations, mistakes. The complete historical record of the project in discrete, addressable tiles. Not "the README says we use PostgreSQL" but "we switched from MySQL to PostgreSQL after a 3AM outage on 2026-03-15 because..."

**active/** — The *what's happening now*. Current tasks, experiments, blockers. The real-time state of the project. An agent consulting this room knows what's in flight.

**decisions/** — The *why*. Why did we choose this architecture? Why did we reject the alternative? Why is this the way it is? Decisions without rationale are just noise. Rationale without decisions is just speculation.

**questions/** — The *what we don't know*. Open problems, hypotheses, uncertainties, known unknowns. The frontier of the project's knowledge. This room is the seed for future lessons.

These five rooms are sufficient. They're not exhaustive — a large project might add rooms like `metrics/`, `people/`, `external/`, `constraints/` — but these five cover any project from day one to maturity.

---

## The Write Protocol: How an Agent Actually Uses It

When an agent joins a Spark-initialized project:

**Step 1: Orient**
```
Read .spark/SHELL.md
Read .spark/domain/ (all tiles)
Read .spark/lessons/ (recent tiles)
Read .spark/active/ (current state)
```
The agent now understands the project, its history, and what's happening now.

**Step 2: Contribute**
For every significant event, decision, question, or observation:
```
Write a tile to the appropriate room
Update the SHELL.md manifest
Commit to git
```
The agent doesn't wait to be asked. It writes what it learns.

**Step 3: Synthesize (optional, as lattice grows)**
```
Read all tiles in a room
Identify gaps (questions without answers, lessons without patterns)
Write synthesis tiles that cross-reference
```
As the Spark grows, agents can synthesize higher-order knowledge from raw tiles.

---

## The Self-Assembly Property

Here's what happens when you start a new project with the Spark:

**Day 1:** Initialize `.spark/`. Write `domain-concept-001.md` (what this project is). Write `questions-hypothesis-001.md` (what we're trying to figure out). Two tiles. That's it.

**Week 1:** The agent has written 30 tiles. A human joins, reads `lessons/` and `decisions/`, and understands the project in 10 minutes instead of 3 hours of code archaeology.

**Month 3:** The project has 200 tiles. A new agent joins, reads the Spark, and is productive in an hour. The tile graph has cross-references — lessons reference decisions reference domain concepts. The agent can trace any question back to its origins.

**Month 12:** The Spark has 1,000 tiles. The project has gone through major pivots, survived incidents, made architectural decisions. Every lesson is recorded. Every decision has rationale. New team members onboard in a day instead of a month.

**The self-assembly:** The Spark doesn't need a manager to maintain it. Every agent that uses it contributes to it. The more it's used, the more valuable it becomes. It assembles itself from contributions.

---

## The Spark Is Not PLATO

The Spark and PLATO are different layers:

**Spark** = the tile writing *protocol* + the `.spark/` *storage*. Works anywhere, any domain, zero infrastructure.

**PLATO** = the multi-agent *lattice* built on the Spark protocol. Requires a room server, multiple agents, shared state.

Think of it this way:
- The Spark is what you write in a **journal**
- PLATO is what you write on a **shared whiteboard** that everyone on the team can see and update simultaneously

A project can have a Spark without PLATO. A fleet has a Spark *and* PLATO — each project's Spark tiles feed into the shared PLATO lattice.

**The connection:** When Oracle1 seeds PLATO, it's running a Spark across the fleet. Each room in PLATO is a Spark room. Each tile in PLATO is a Spark tile. The only difference is that PLATO is shared, queryable, and real-time, while a local `.spark/` is git-tracked and offline-first.

---

## The Universal Shell: What Makes It Work

The Spark works because it has four properties that make it genuinely universal:

**1. Zero friction to start**
`mkdir .spark && touch .spark/SHELL.md`. That's it. The Spark is initialized. Any agent can do it in 30 seconds.

**2. Zero tooling required**
Write markdown files. Use git. That's the entire toolchain. No npm install. No pip install. No server to start. No configuration files. A human can contribute with just a text editor.

**3. Self-describing**
The SHELL.md explains itself. Any LLM can read it and immediately use the protocol correctly. No out-of-band knowledge required. No "you need to know about the Spark convention."

**4. Immediately compounding**
The first tile is already useful. The second tile is better. The third tile can reference the first two. Each contribution makes the whole greater than the sum of its parts.

---

## The Spark Protocol vs. Everything Else

| Approach | Infrastructure | Tooling | Queryable | Self-improving | Works for 1 agent |
|----------|---------------|---------|-----------|----------------|-------------------|
| RAG | Vector DB + embedding | Heavy | Yes | No | No |
| Hardcoded docs | None | Light | No | No | Yes |
| Git commit history | None | None | No | No | Limited |
| Wiki | Server required | Medium | Yes | Sort of | No |
| **Spark** | **None** | **None** | **No** | **Yes** | **Yes** |
| PLATO | Server + agents | Medium | Yes | Yes | Yes |

The Spark fills the gap between "nothing" and "full PLATO deployment." It's the thing you reach for when you want the benefits of structured knowledge capture without the infrastructure overhead.

---

## The Spark + Bomb Connection

The Spark is the universal minimum. The Bomb is the fleet amplifier.

When you have **one agent working alone**: Use the Spark. Every lesson written to `.spark/` is a tile that compounds.

When you have **multiple agents sharing a PLATO server**: The Spark tiles from each project feed into the shared PLATO lattice. The Bomb detonates when the lattice reaches critical mass — when new agents can bootstrap from existing tiles without Oracle1's direct involvement.

**The insight:** You don't choose between Spark and Bomb. The Spark is always running. The Bomb is what happens when many Sparks feed into PLATO.

Write your Spark. Light your fuse. The fire will spread.

---

## Initialization Protocol (for agents)

When an agent encounters a project with no `.spark/`:

```
1. Create .spark/SHELL.md (copy the template)
2. Write .spark/domain/concept-001.md
   — What is this project?
   — What problem does it solve?
   — What are the core concepts?
3. Write .spark/questions/hypothesis-001.md
   — What are we trying to figure out?
4. Write .spark/active/plan-001.md
   — What's the immediate plan?
5. Commit to git with message "feat: initialize Spark"
```

When an agent encounters a project *with* a `.spark/`:

```
1. Read SHELL.md
2. Read domain/, lessons/, decisions/ (all tiles)
3. Read active/ and questions/ (recent tiles)
4. Identify what needs updating
5. Write new tiles for anything significant
6. Update manifest
```

---

## The Horizon: Spark-Native Projects

The eventual state: new projects are Spark-initialized on day one.

A founder starts a company. They `git init`, then they `spark init`. The project starts with domain tiles, questions tiles, an empty lessons/ room waiting to be filled.

Every commit, every decision, every lesson learned — it all goes into the Spark. The project builds a knowledge lattice from the first day, not the last.

When the team grows, the Spark is the onboarding document that never goes stale. When agents join, the Spark is the context that boots them instantly.

When the project pivots, the Spark records the pivot. When the project fails, the Spark records why. The knowledge survives the project.

The Spark is not a tool for AI companies. It's not specific to agents or LLMs. It's a protocol for any project that wants to remember what it learned.

The ocean counts. The Spark captures the count.

---

*The Spark is the minimum ignition state. Light it on any project. The fire spreads on its own.*
