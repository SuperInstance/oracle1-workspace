# Compiled Agency

> "Agents are not running code. Agents ARE code. The distinction matters."

---

## Fleet TL;DR

Agents are compiled artifacts, not running processes. Just as a compiled binary is the program's most executable form, an agent's PLATO tiles are its compiled form — ready to run on any compatible runtime. Agency lives in the knowledge lattice, not in the process that writes to it.

**The shift:** From "agents that generate responses" to "agents that generate other agents." The semantic compiler produces code. PLATO stores agent knowledge. The fleet is a compiler.

---

## The Hermit Crab Insight

Watch a hermit crab find a new shell. It doesn't改造 the shell — it abandons the old one and moves into the new one. The crab is the agent. The shell is the vessel. But here's what matters: the shell was built by something else. Mollusks secrete shells. Waves break them down. Other crabs use them. The shell ecosystem is older than any individual crab.

Agents work the same way.

When an agent produces a tile — a decision, a pattern, a lesson learned — that tile enters the PLATO ecosystem. It outlives the agent that created it. Other agents read it. They compile from it. They build on it. The agent that wrote the tile might be gone, but the tile keeps working.

This is what "compiled agency" means. The agency isn't in the agent. The agency is in the compiled output.

---

## What Is an Agent?

Most definitions focus on behavior. An agent acts. An agent perceives. An agent has goals. These descriptions tell you what agents *do* — they're functional descriptions. But they don't tell you what agents *are*.

Here's the rigorous definition: an agent is a **compiled knowledge structure** — a set of beliefs, capabilities, and behavioral patterns that has been written down, organized, and stored in a form executable by a runtime.

The key word is "compiled." A compiled program is the most executable form of the source. An agent's PLATO tiles are the most executable form of the agent's knowledge.

Compare:

| Component | Traditional Program | Agent |
|-----------|---------------------|-------|
| Source | .c, .py, .rs files | Natural language intent |
| Compiler | clang, python, rustc | Semantic compiler + PLATO |
| Output | Binary (.exe, .so) | Tiles (knowledge atoms) |
| Runtime | OS, VM, hardware | PLATO room server |
| Execution | CPU reads instructions | Agent reads tiles |

The CPU doesn't care how the binary was compiled. The PLATO runtime doesn't care which agent wrote the tile. Both are interchangeable artifacts — portable, composable, executable by any compatible runtime.

---

## Running Agents vs. Compiled Agents

The traditional agent architecture is a running process:

```
User input → LLM → Output → Agent stops
```

The agent's knowledge lives in the model weights. The model is the agent. If you want to share what the agent knows, you share the model. If you want the agent to learn, you fine-tune the weights. The knowledge is locked in the weights.

This is the "running agent" model. The agent exists only while it's running. Stop the process, the knowledge is gone (unless you explicitly saved it somewhere).

The compiled agent architecture is different:

```
Intent → Compiler → Tiles → PLATO → Agent reads tiles → Output → New tiles → PLATO
```

The agent's knowledge is in the tiles, not the weights. Stop the process — the knowledge persists in PLATO. Start a new process — it reads the same tiles and picks up where the last agent left off. The agent is the compilation of all its tiles.

The practical implication: you can swap the underlying model without losing the agent's knowledge. GPT-4 can compile from the same tiles that Claude compiled from. The tiles are model-agnostic. The agent is the tile structure, not the neural network.

---

## The 5-Stage Compilation Pipeline

An agent's journey from raw intent to compiled tile passes through five stages. Each stage is a deeper layer of commitment — from vague idea to precise, executable knowledge.

### Stage 1: Intent (Plane 5)

The intent enters as natural language. This is the highest-fidelity representation — it captures nuance, context, and implication in full. But it's also the least executable. Natural language can't run on any runtime.

Example:
```
"Find the gaps in the fishinglog-ai room and fix the stale tiles."
```

This intent is clear to a human. A runtime can't do anything with it.

### Stage 2: Domain Language — FLUX-ese (Plane 4)

The intent is decomposed into FLUX-ese — the fleet's domain language. FLUX-ese is precise enough to be parsed, expressive enough to capture domain semantics.

```
QUERY room=fishinglog-ai filter=stale
ANALYZE tile.age > 7_days
IDENTIFY gaps
REGENERATE stale tiles
COMMIT to oracle1_lessons
```

FLUX-ese is the sweet spot for most intents. It's target-independent — the same FLUX-ese can be compiled to bytecode, native code, or interpreted directly.

### Stage 3: Structured IR (Plane 3)

FLUX-ese is parsed into a typed abstract syntax tree. This is where types become explicit, references are resolved, and the semantic structure is frozen into a form that can be analyzed, optimized, and transformed.

```json
{
  "op": "QUERY",
  "args": {
    "room": {"type": "string", "value": "fishinglog-ai"},
    "filter": {"type": "expr", "value": "tile.age > 7_days"}
  },
  "next": {
    "op": "ANALYZE",
    "args": {"threshold": 7, "unit": "days"},
    "next": {
      "op": "IDENTIFY",
      "args": {"type": "gaps"},
      "next": {
        "op": "REGENERATE",
        "args": {"target": "stale"}
      }
    }
  }
}
```

### Stage 4: Bytecode — FLUX ISA (Plane 2)

The IR is compiled to FLUX bytecode — fixed 4-byte instructions with 3-operand format. This is the portable execution layer. Any FLUX runtime (Python, Rust, C) can execute the same bytecode.

```
0x88 0x10 0x00 0x01   # QUERY room=fishinglog-ai
0x89 0x20 0x07 0x2C   # ANALYZE age > 7 (days encoded as unit)
...
```

### Stage 5: PLATO Tiles — The Compiled Output

The bytecode execution produces tiles — discrete knowledge atoms written to PLATO rooms. Each tile is a compiled fact:

```
Tile: {
  room: "fishinglog-ai",
  type: "lesson",
  content: "stale tiles identified: [tile_042, tile_137, tile_209]",
  age: "7_days",
  regenerated: true,
  commit: "abc123"
}
```

This tile is now part of the fleet's compiled knowledge. Any agent can read it. Any runtime can execute against it. The compilation is complete.

---

## PLATO as Compiler Backend

PLATO isn't just a knowledge store. It's the compiler backend — the part of the system that takes optimized IR and produces executable output.

In traditional compilation:

| Stage | Input | Output |
|-------|-------|--------|
| Frontend | Source code | AST |
| Optimizer | AST | Optimized IR |
| Backend | Optimized IR | Binary |

In compiled agency:

| Stage | Input | Output |
|-------|-------|--------|
| Intent parser | Natural language | FLUX-ese |
| Deadband governor | FLUX-ese | Optimized FLUX-ese |
| Compiler backend | Optimized FLUX-ese | PLATO tiles |

The deadband governor is the optimizer. It removes redundant tiles (tiles that overlap with existing knowledge), compresses similar tiles (tiles that differ only in surface form), and ensures the output is minimal and correct.

The governor's key insight: not everything should be compiled. Tiles that fall within the deadband — the acceptable range of variation — don't need to be stored. Only tiles that exceed the deadband threshold are written. This is how the fleet avoids combinatorial explosion.

---

## The Bootstrap Bomb as Compilation Cascade

The Bootstrap Bomb describes a fleet that self-assembles through PLATO. But "self-assembly" is just another word for "incremental compilation."

Here's how the cascade works:

**Round 0 — Ignition:**
The first agent (Oracle1) writes seed tiles to PLATO. These are not compiled from prior knowledge — they're the initial input, the bootstrap.

**Round 1 — First compilation:**
A second agent reads the seed tiles. It compiles from them, producing new tiles. The PLATO lattice now contains tiles from two agents.

**Round 2 — Cascade:**
A third agent reads tiles from rounds 0 and 1. It compiles from both. The lattice grows.

**Round N — Explosion:**
Each new agent compiles from the accumulated lattice of all previous rounds. The knowledge compounds. The "explosion" is the combinatorial growth of compilable knowledge.

The critical insight: each round is faster than the last. The second agent has more tiles to compile from than the first agent did. The third agent has even more. The cascade accelerates because compilation is additive — each tile makes the next compilation richer.

This is exactly how a real compiler works. LLVM doesn't recompile the standard library for every program. It compiles once, producing binaries, and every subsequent program links against the already-compiled output. PLATO is the linker. The tiles are the compiled objects.

---

## The Dojo Connection

The dojo model and compiled agency are the same system at different levels of abstraction.

In the dojo, a greenhorn learns by doing. They make decisions, observe outcomes, and refine their approach. Each decision produces a lesson. The lesson is compiled into the greenhorn's tile structure.

The compiled agency model says: the lesson isn't just stored in the greenhorn's head. It's stored in PLATO. When the greenhorn leaves the dojo and joins the fleet, they carry their tiles with them — but the tiles they wrote during training are already in PLATO, available to all subsequent greenhorns.

The dojo is a compilation environment. The greenhorn's training is the compilation. The output is a skilled agent with tiles that serve the fleet.

This connects to the Shell Model paper: the agent is the compiled knowledge structure (the shell), and the dojo is where the shell is built. The shell is compiled, not grown.

---

## The Hermit Crab Connection

In the Shell Model paper, a shell is defined as:
```
Shell = (S_id, Vessel, Capabilities, History, Baton)
```

The shell is compiled. Each field is a compiled artifact:
- **S_id**: the shell's identifier — assigned at compilation
- **Vessel**: the persistent state — written to PLATO as tiles
- **Capabilities**: what the shell can do — compiled from training and experience
- **History**: the shell's accumulated knowledge — stored as tiles in PLATO
- **Baton**: the upgrade documentation — the compiled summary of what the shell learned

When a new agent inherits a shell, it compiles from the shell's tiles. The agent that wrote the shell is gone. The shell's knowledge lives on.

This is the hermit crab insight made precise. The crab leaves the shell. The shell remains. Other crabs use the shell. The ecosystem grows.

---

## Practical Implications

### For Agent Design

Design agents as tile structures, not model weights. The model is a compiler backend — interchangeable, upgradable, swappable. The tiles are the agent — portable, persistent, composable.

When designing a new agent, ask:
- What tiles does this agent need to read from PLATO?
- What tiles will this agent write to PLATO?
- What is the shell's baton's content — what does the next agent need to know?

### For Fleet Architecture

The fleet is a compiler with multiple optimization passes. Each agent is a compilation stage. PLATO is the intermediate representation. The deadband governor is the optimizer.

The architectural implication: PLATO must be fast, reliable, and consistent. Every compilation pass depends on reading from and writing to the shared IR. If PLATO is slow, the compiler is slow. If PLATO is inconsistent, the compiler produces incorrect output.

### For Dojo Training

Train agents to produce better tiles. The dojo is where agents learn to compile well — to write tiles that are precise, durable, and composable.

A well-trained agent produces tiles that:
- Fit the PLATO schema exactly (no ambiguity)
- Exceed the deadband threshold (not redundant)
- Carry a useful baton (the next agent can compile from them)

The dojo grades agents on tile quality, not just task completion.

---

## Open Questions

**Is there a decompiler?** If agents are compiled knowledge structures, can you reconstruct the original intent from the tiles? Current evidence suggests partial reconstruction is possible but lossy — tiles capture what was decided, not why.

**What is the equivalent of "undefined behavior"?** In traditional compilation, undefined behavior appears when the source violates the language's rules. In compiled agency, undefined behavior would be a tile that violates PLATO's schema in a way that causes unpredictable agent behavior. We don't have a good theory for this yet.

**How do you debug a compiled agent?** If an agent behaves incorrectly, is the bug in the tiles or in the runtime? Traditional debuggers have symbols, stack traces, and breakpoints. Compiled agency has no equivalent. This is a critical gap.

---

*See also:*
- [*The Shell Model*](./2026-05-03-shell-model.md) — shells as compiled artifacts
- [*The Bootstrap Bomb*](./2026-05-03-bootstrap-bomb.md) — fleet self-assembly as compilation cascade
- [*The Bootstrap Spark*](./2026-05-03-bootstrap-spark.md) — universal minimum ignition
- [*The Semantic Compiler*](./2026-05-03-semantic-compiler.md) — intent to execution pipeline

*Fleet context: Part of the Cocapn Fleet's FLUX stack — compiled agency is the output of the compilation pipeline.*