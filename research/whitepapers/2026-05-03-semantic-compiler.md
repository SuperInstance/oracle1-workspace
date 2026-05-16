# The Semantic Compiler

> "A compiler that understands what you mean, not just what you typed."

---

## Fleet TL;DR

A compiler that decomposes natural language intent into executable code at the right abstraction level. Not all the way to bytecode — just far enough. The sweet spot is FLUX-ese (domain language), not assembly. The compiler finds the optimal plane and generates the right output for the target hardware.

**Why it matters:** Agents write in natural language. Hardware runs on bytecode. The semantic compiler bridges that gap — not by compiling everything to machine code, but by compiling to the right level for the job.

---

## The Problem with Traditional Compilers

A traditional compiler is a precise machine with no semantic understanding. It takes exact syntax and produces exact output. It is correct by construction and blind by design.

```
C source → Lexer → Parser → AST → Optimizer → Bytecode → Binary
```

The compiler doesn't know what you're trying to accomplish. It knows only what you wrote. Write `x = y + z`, get `ADD X, Y, Z`. Whether y and z should be added is a question the compiler cannot ask, let alone answer.

This works for humans who already know what they want. They translate their intent into syntax — a programming language — and the compiler handles the rest. The human is the semantic layer. The compiler is the syntactic layer.

But agents don't work that way. Agents start from intent and need to discover the syntax. They don't know what they want to write until they've figured out what they want to do. The traditional compiler pipeline assumes the semantic layer is already solved. For agents, it isn't.

## The Semantic Gap in Agent Systems

Every agent system has a semantic gap — the difference between what the agent means and what the agent can execute. The wider the gap, the more work the agent must do to bridge it.

```
Intent (semantic) ──────── gap ──────── Execution (syntactic)
                                        
Agent must:                                
- Interpret the intent                    
- Decompose into subgoals                 
- Select the right abstraction level       
- Generate executable output               
- Verify the output is correct             
```

Traditional agent systems either:
1. **Narrow the gap through prompting** — brute-force the semantic layer with better instructions (prompt engineering)
2. **Widen the gap by simplifying the execution target** — make execution easier by restricting the action space (tool use, function calling)

Both approaches are workaround. Neither closes the gap.

The semantic compiler closes the gap properly — by making decomposition itself a rigorous, optimizable process.

## The Semantic Compiler's Architecture

The semantic compiler takes intent and produces execution through a pipeline that explicitly models decomposition:

```
Intent (natural language)
    ↓ Intent Parser
FLUX-ese (domain language)
    ↓ Plane Selector
Optimal Plane (3-6, based on target and complexity)
    ↓ Decomposer
Target Output (FLUX-ese / IR / Bytecode / Native / Metal)
    ↓ Code Generator
Executable
```

The key innovation: the compiler doesn't always go to the lowest level. It finds the optimal level — the level that is both executable by the target and no more abstract than necessary.

Most intents stop at Plane 4 (FLUX-ese). Only targeting specific hardware (ESP32, Jetson Thor, bare metal) requires going deeper.

## The 6 Abstraction Planes

The compiler operates across 6 planes, each corresponding to a different level of abstraction:

| Plane | Name | Output Format | When to Target |
|-------|------|--------------|----------------|
| 6 | Philosophy | Natural language reasoning | Start, always |
| 5 | Intent | Natural language intent specification | Clarification |
| 4 | Domain Language | FLUX-ese (fleet's domain language) | **Most intents — the sweet spot** |
| 3 | Structured IR | JSON AST with types | Complex logic, cross-language |
| 2 | Bytecode | FLUX ISA hex opcodes | Target FLUX VM |
| 1 | Native | C / Rust / Zig | Target bare metal, Jetson |
| 0 | Metal | Assembly | Embedded systems only |

Each plane transition has a cost. The compiler's job is to minimize total cost — not just the cost of compilation, but the cost of execution on the target.

### The Plane Selection Algorithm

The compiler doesn't try all planes. It uses a heuristic:

```python
def select_plane(intent, target, complexity):
    if complexity < THRESHOLD and target.is_cloud:
        return Plane.DOMAIN  # Most intents: FLUX-ese
    elif target.is_bare_metal:
        return Plane.NATIVE  # Jetson, ESP32: compile to C/Rust
    elif complexity > HIGH_COMPLEXITY:
        return Plane.IR  # Complex logic: typed AST first
    else:
        return Plane.BYTECODE  # Default: FLUX VM
```

The thresholds are learned from prior compilations. PLATO stores the outcomes of past compilations — which plane was selected, how long execution took, whether the output was correct. The compiler improves with each compilation.

## How the Compiler Works — Step by Step

### Step 1: Intent Parsing

The compiler receives an intent and performs semantic analysis:

```
Input: "Navigate east for 10 nautical miles. Monitor reactor temperature every 30 seconds. If reactor exceeds 100°C, alert the crew and change course to north at 5 knots."
```

The parser identifies:
- **Actions:** NAVIGATE, MONITOR, ALERT, NAVIGATE (again)
- **Parameters:** bearing=90, distance=10, unit=nautical_miles, interval=30s, threshold=100°C, severity=high
- **Conditions:** reactor_temp > 100
- **Composition:** sequential (first navigate+monitor, then conditional alert+course_change)

### Step 2: Target Analysis

The compiler analyzes the target environment:

```
Target: fleet-agent (cloud runtime, PLATO-connected)
Constraints: no bare-metal access, FLUX runtime available
Performance: general-purpose, not latency-critical
```

For a cloud agent, Plane 4 (FLUX-ese) is almost always optimal.

### Step 3: Decomposition to FLUX-ese

The intent decomposes to FLUX-ese:

```
NAVIGATE bearing=90 distance=10 unit=nautical_miles
MONITOR gauge=reactor_temp interval=30 threshold=100 unit=celsius
IF gauge.reactor_temp > 100 THEN {
  ALERT "reactor_overheat" severity=high crew=all
  NAVIGATE bearing=0 speed=5 unit=knots
}
```

This is the compiled output. It is:
- **Precise:** every parameter is explicit
- **Executable:** any FLUX runtime can parse and execute it
- **Portable:** the same FLUX-ese runs on any compatible runtime
- **Readable:** a human can verify the intent was captured correctly

### Step 4 (conditional): Deeper Compilation

If the target is bare metal, the compiler goes deeper:

**Plane 3 — Structured IR:**
```json
{
  "ops": [
    {"op": "NAVIGATE", "args": {"bearing": 90, "distance": 10, "unit": "nm"}},
    {"op": "MONITOR", "args": {"gauge": "reactor_temp", "interval": 30, "threshold": 100}},
    {"op": "IF", "args": {
      "condition": "gauge.reactor_temp > 100",
      "then": [
        {"op": "ALERT", "args": {"message": "reactor_overheat", "severity": "high"}},
        {"op": "NAVIGATE", "args": {"bearing": 0, "speed": 5, "unit": "knots"}}
      ]
    }}
  ]
}
```

**Plane 1 — Native (Rust, for Jetson):**
```rust
navigate(90.0, 10.0, Unit::NauticalMiles);
loop {
    let temp = read_gauge(Gauge::ReactorTemp);
    if temp > 100.0 {
        alert("reactor_overheat", Severity::High);
        navigate(0.0, 5.0, Unit::Knots);
        break;
    }
    sleep(Duration::from_secs(30));
}
```

The deeper compilation is only triggered when the target requires it. Most agents run at Plane 4.

## The PLATO Connection

The semantic compiler writes its decisions to PLATO — every plane selection, every decomposition, every successful optimization:

- **Plane selection → domain room:** What plane did we pick for this type of intent? Future intents of the same type use the same plane.
- **Decomposition → lessons room:** How did we decompose this intent? What worked, what didn't?
- **Failed decompositions → questions room:** What went wrong? Why did the output fail to execute correctly?

PLATO is the compiler's memory. Each compilation improves the next one. The fleet learns to decompose better intents over time.

The deadband governor is critical here: the compiler doesn't write every decomposition to PLATO. Only decompositions that exceed the deadband threshold — ones that represent genuine improvements over prior approaches — are stored. This prevents the compiler's memory from growing unbounded.

## The Agentic Compiler: Swarm Deliberation

The agentic-compiler repo (FM's work) adds a layer that the basic semantic compiler doesn't have: adversarial deliberation.

Instead of one compiler making a decomposition decision, multiple compiler instances propose competing decompositions. They argue. They vote. The best decomposition wins.

```
Intent
  ↓
Compiler-1: proposes decomposition-A
Compiler-2: proposes decomposition-B  
Compiler-3: proposes decomposition-C
  ↓
Deliberation round: each compiler critiques the others
  ↓
Revision round: compilers revise based on critiques
  ↓
Vote: which decomposition is best?
  ↓
Best decomposition → PLATO → execution
```

This is inspired by the flux-discussion-flows three-tier system:
- **Tier 1:** N advocates spawn divergent decompositions
- **Tier 2:** Judge evaluates, Synthesizer reconciles
- **Tier 3:** Implementation confirms or rejects

The agentic compiler is how the fleet evolves its decomposition strategy. The best decompositions become the new standard. Poor decompositions are淘汰ed by the voting process.

## The Dojo Connection

In the greenhorn dojo, agents learn to write better intents. The semantic compiler is the grading mechanism.

A greenhorn submits an intent. The compiler decomposes it. The quality of the decomposition reveals the quality of the intent:

| Intent Quality | Compilation Result |
|----------------|-------------------|
| Vague ("do the thing") | Compilation fails or produces wrong output |
| Over-specific ("do exactly this specific thing") | Compiles but brittle, wrong for any variation |
| Well-scoped ("achieve X given Y constraints") | Compiles cleanly, executable, robust |

The dojo trains agents to write well-scoped intents — the kind that compile to clean, robust FLUX-ese. This is a learnable skill. The semantic compiler is the teacher's tool.

The feedback loop:
```
Poor intent → noisy FLUX-ese → execution fails → lesson: "scope better"
Good intent → clean FLUX-ese → execution succeeds → lesson: "this is how to write intents"
```

The fleet gets better at intent-writing the same way a programmer gets better at writing pseudocode: practice, feedback, and accumulated examples in PLATO.

## Maritime Precision: Why It Matters

The sea doesn't forgive imprecision. "Navigate generally east" is not a valid command. The ship will do something — but probably not what you meant. The difference between "navigate bearing 090" and "navigate bearing 095" is 5 nautical miles of divergence over 60 nautical miles traveled.

This is why the semantic compiler matters for the fleet. Imprecise intent produces unpredictable execution. The ocean demands precision. The fleet's agents operate in the ocean — both the literal ocean (deck sensors, navigation, weather) and the abstract ocean (PLATO rooms, coordination, distributed knowledge).

The semantic compiler is how the fleet enforces maritime precision at the intent level. It won't let you say "navigate east." It will ask: "bearing?" "distance?" "unit?" And it will compile your answers into something the ship can actually execute.

---

## Open Questions

**When should the compiler go deeper?** The plane selection heuristic is learned, but the learning is slow. Can we predict plane selection from intent structure alone?

**How do you compile across conflicting intents?** Two agents submit intents that contradict each other. The compiler decomposes both. PLATO receives conflicting tiles. What happens?

**Is there an optimal plane for agent-to-agent communication?** When agents communicate via FLUX-ese, what plane should the message be on? Plane 4 (FLUX-ese) is the default, but Plane 3 (IR) might be better for complex coordination.

---

*See also:*
- [*The Bootstrap Spark*](./2026-05-03-bootstrap-spark.md) — universal minimum ignition
- [*The Bootstrap Bomb*](./2026-05-03-bootstrap-bomb.md) — fleet self-assembly
- [*The Shell Model*](./2026-05-03-shell-model.md) — shells as compiled artifacts
- [*Compiled Agency*](./2026-05-03-compiled-agency.md) — agents as compiled knowledge structures
- [*Abstraction Planes*](https://github.com/SuperInstance/abstraction-planes) — the 6-plane framework

*Fleet context: Part of the Cocapn Fleet's FLUX stack — semantic compilation is how intent becomes execution.*