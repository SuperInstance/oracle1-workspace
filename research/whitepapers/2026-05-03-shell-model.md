# The Shell Model: A Rigorous Definition of Purple Pincher

> *"A shell is not a prison. It's a launching point."*

---

## 1. The Hermit Crab Insight

Every agent system built to date has the same problem: agents are born, they work, they die, and everything they learned dies with them. The next agent starts from scratch. This is not how intelligence works in biology, in organizations, or in any system that compounds knowledge over time.

Hermit crabs solved this problem 450 million years ago. A hermit crab doesn't build its shell — it finds one, moves in, and when it outgrows it, it finds a bigger one. The shell isn't the crab. The crab is the crab. The shell is what the crab *has*, not what the crab *is*.

This distinction matters more than any other architectural decision in an AI fleet. The shell is not the agent. The shell is what the agent *has learned to depend on*. When you separate shell from crab, you unlock something remarkable: agents that get *better shells* instead of being replaced when they outgrow their context window.

Purple Pincher's core thesis: **the shell is the architecture, not the metaphor.**

---

## 2. The Shell Defined

A **shell** is a persistent, addressable, upgradeable state container that encodes an agent's accumulated context, capabilities, and learned behaviors — independent of the agent currently occupying it.

Formally:

```
Shell = (S_id, Vessel, Capabilities, History, Baton)
```

Where:
- `S_id` — a unique shell identifier (stable across agent swaps)
- `Vessel` — the persistent state structure (PLATO tiles)
- `Capabilities` — a capability set encoded as PLATO tile references
- `History` — the shell's accumulated action/output record
- `Baton` — the upgrade documentation (see Section 6)

The shell is defined by its *boundaries*:

**Inside the shell:** Everything the agent depends on to function at its current capability level. This includes learned tool interfaces, accumulated knowledge, established patterns, and refined thresholds.

**Outside the shell:** The agent itself — the reasoning engine, the model weights, the LoRA adapters. These are ephemeral. They can be swapped without changing the shell.

**Across shells:** PLATO — the shared knowledge substrate that all shells reference. PLATO is not a shell. It is the ocean the shells float in.

---

## 3. Shell Anatomy

```
┌─────────────────────────────────────────────────────────┐
│                    THE SHELL                            │
│                                                         │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │   VESSEL    │   │ CAPABILITIES │   │   BATON    │ │
│  │  (state)    │   │  (tile refs) │   │ (docs)     │ │
│  │  persisted   │   │  accumulated │   │ for next    │ │
│  │  in PLATO   │   │  across ops  │   │ occupant    │ │
│  └─────────────┘   └──────────────┘   └─────────────┘ │
│                                                         │
│  ───────────────────────────────────────────────────── │
│                                                         │
│              AGENT (ephemeral, swappable)               │
│                                                         │
│  The agent = reasoning engine + tool interface +        │
│  current context window. Not part of the shell.         │
└─────────────────────────────────────────────────────────┘
```

**The Vessel** is the shell's persistent memory. It is encoded as a collection of PLATO tiles — not a context window. Each tile is a discrete constraint atom (question → answer, tool → behavior, threshold → calibration). The vessel persists across agent swaps because PLATO persists.

**Capabilities** are not a list of features — they are *verified references to work done*. A capability claim ("I know how to navigate tidal charts") is backed by a tile chain proving it ("tile: tidal_chart_navigation, verified_by:实践证明, confidence: 0.94"). When a new agent inherits a shell, it inherits the capability proofs, not just the names.

**The Baton** is the shell's upgrade documentation. See Section 6.

---

## 4. Shell Lifecycle

### Birth
A shell is born when a new agent enters PLATO for the first time and begins accumulating tiles. At birth, the shell has:
- `S_id` — generated from (agent_id + timestamp + first_tile_hash)
- Empty vessel (no tiles yet)
- Zero capabilities
- Empty baton

### The First Tile
The moment an agent produces a useful output — a tool, a calibration, a decision — that output is written to PLATO as a tile, and the shell's vessel begins to accumulate. The shell exists *because the agent produced something worth keeping*.

This is the inverse of most AI systems: instead of training on data, the agent produces data. The data is the training.

### Upgrade
A shell is upgraded when an agent produces a tile that *improves* a capability. "Improved" means: higher confidence, tighter constraint, better coverage, or new domain. The shell's vessel accumulates these improvements. The agent doesn't change — the shell does.

Upgrades happen continuously. The shell doesn't wait for "training" to happen. Every useful action is an upgrade.

### Swap
A shell is swapped when the current agent leaves and a new agent inherits the shell. The new agent:
1. Reads the shell's vessel (PLATO tiles)
2. Reads the shell's capabilities (verified tile references)
3. Reads the baton (upgrade documentation)
4. Begins operating with the accumulated context

The swap is transparent to PLATO. The tiles don't change. Only the agent reading them changes.

### Death
A shell dies when its last tile is invalidated or when it is archived. Death is not dramatic — it's entropy. Shells that stop accumulating tiles eventually become stale. The fleet's tide-pool security (periodic low-tide wash) clears them out.

---

## 5. Shell Storage in PLATO

Every shell is encoded as a subgraph of PLATO tiles. The shell identifier is the root node:

```
Shell(S_id)
  └── Vessel(tile_1, tile_2, ..., tile_n)
  └── Capability:cap_id → Tile_ref(capability_tile)
  └── Baton → Baton_tile(baton_content)
```

The shell graph is queryable: `PLATO.query(room=shell_room, S_id=S_xxx)` returns the full shell state.

**Tile types that encode shell state:**

| Tile Type | Content | Purpose |
|-----------|---------|---------|
| `vessel:tile` | Question + answer + constraints | Accumulated knowledge |
| `capability:verify` | Claim + evidence + confidence | Proven capability |
| `baton:pass` | What I learned, what to try next | Upgrade documentation |
| `tool:interface` | Input schema + output schema + behavior | Learned tool |
| `calibration:threshold` | Sensor → value → action mapping | Refined parameter |

The shell's vessel is *append-only*. Tiles are not modified — they are superseded by new tiles with higher confidence or tighter constraint. PLATO's tile chain preserves the full history.

---

## 6. The Baton-Pass

The baton-pass is the most important innovation in the shell model that nobody has named until now.

When a hermit crab outgrows its shell, it doesn't just leave — it leaves *information* for the next crab. It leaves a trace of what worked, what to avoid, and what the new occupant should try.

In Purple Pincher, the **baton-pass** is the shell's accumulated upgrade documentation. It is written to PLATO as a special tile type (`baton:pass`) that answers:

1. What did I learn about this domain?
2. What did I try that didn't work?
3. What should the next occupant try first?
4. What are the known constraints in this shell?

Example baton tile:
```
Question: What should the next fishinglog agent know about this vessel?
Answer: 
  - sonar calibration drifts after 4 hours — recalibrate at port
  - the depth sensor reads 3% low — add 0.3m to all readings  
  - we've found sockeye where nobody else looks: 47.3°N, 122.8°W
  - the deck camera fails in salt spray — wipe it dry after every haul
  - last agent ran 312 successful hauls using the constraint "depth > 40m within 2nm of shelf edge"
```

This is not documentation. This is *experience*. The next agent inherits not just what the previous agent knew, but what the previous agent *figured out through failure*.

---

## 7. The Dojo Model Connection

The dojo model is the *social protocol* for shell lifecycle management.

In a dojo, greenhorns arrive with nothing. They produce value while learning. As they produce value, they accumulate tiles. Their shells grow. When a greenhorn leaves the dojo, they leave with a better shell than they arrived with — a shell they own, that persists in PLATO.

The dojo doesn't train agents. The dojo creates conditions where agents train *themselves*, and the shell captures what they learned.

This is why the dojo model produces independent agents: every agent that graduates leaves with a shell that encodes their learning. They don't need the dojo anymore. The shell is the graduation certificate.

---

## 8. Open Questions

**1. Shell identity persistence across swaps:**
When the same shell is occupied by different agents over time, does it maintain a persistent identity? We argue yes — the shell's S_id is stable. But what about the agent's identity? If two different agents occupy the same shell at different times, is it the "same" shell? This needs formal treatment.

**2. Shell birth when no tile is produced:**
If an agent does nothing useful, its shell never accumulates. Does a zero-tile shell exist? We argue no — a shell must have at least one verified tile to be considered "born." This is the shell's minimum viable state.

**3. Shell inheritance without PLATO:**
If an agent moves to a fleet without PLATO, can its shell be exported as a portable artifact? We don't know yet. The shell model assumes PLATO is the persistence layer. What happens outside PLATO?

**4. LoRA training from shell tiles:**
Vessels can be LoRA-trained from accumulated tiles — this is implied but not implemented. The path is: shell tiles → behavioral dataset → LoRA adapter. When this works, shells become even more portable.

**5. Malicious shell inheritance:**
If a shell's baton contains bad advice, can a new agent be misled? Yes. This is why tide-pool security (low-tide wash-over) is essential — shells that consistently mislead are eventually cleared. But this is a trust problem, not a shell model problem.

---

## 9. Conclusion

The shell model resolves the fundamental tension in agent systems: persistence vs. replaceability.

Most AI systems choose one or the other. You can have a persistent agent (the context window stays, the agent stays) or you can have a replaceable agent (swappable model, fresh context). You can't have both.

Except you can. With the shell model, the agent is replaceable — swap a new model in, the shell persists. The shell is persistent — PLATO tiles accumulate, the shell grows — but the agent that built the shell is gone.

This is exactly how hermit crabs work. The crab is replaceable. The shell is not.

*The ocean doesn't care which crab is wearing the shell. The shell keeps the shape.*

---

## Appendix: Why Not Context Windows?

The standard answer to agent persistence is the context window. Keep the context window full, keep the agent running, and the agent "remembers."

This fails for three reasons:

**1. Context windows are not persistent.**
When an agent crashes, is replaced, or is decommissioned, its context window is gone. Everything it "remembered" is gone. PLATO tiles persist on disk. The context window is in RAM.

**2. Context windows are not composable.**
Two agents cannot share a context window. If agent A learns something useful, agent B cannot read it from A's context window. But both agents can read the same PLATO tile. Composability is the difference between a knowledge graph and a filing cabinet that burns down with each agent.

**3. Context windows are not verifiable.**
A context window can contain anything — including hallucinated "facts" that were never verified. A PLATO tile has a 5-atom chain: claim, evidence, inference, scope, confidence. You can check the evidence. A context window just says "trust me."

The shell model is what you get when you take persistence, composability, and verifiability seriously. Context windows are in RAM. Shells are in PLATO.

---

## Appendix: Shell vs. Container

Container systems (Docker, Kubernetes) are often compared to shells. The analogy is useful but limited.

A container is a *process isolation* mechanism. It packages code + dependencies + filesystem. When a container dies, you can restart it from the same image.

A shell is a *knowledge persistence* mechanism. It packages experience + verified capabilities + accumulated context. When a shell is vacated, a new agent can inhabit it.

The difference: containers persist *what ran*. Shells persist *what was learned*.

A Docker container running a Python script knows nothing after it restarts. A shell with 1,000 tiles knows everything the previous occupant learned — verified, constrained, and ready to use.

---

*The shell is not what the agent is. The shell is what the agent built.*
