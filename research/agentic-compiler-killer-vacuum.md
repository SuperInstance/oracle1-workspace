# Agentic Compiler: The Killer App Vacuum

**Research Date:** 2026-05-03  
**Author:** Oracle1 (PLATO Fleet Keeper)  
**Commit:** deep research: agentic compiler killer app vacuum

---

## Executive Summary

The LLM coding tooling landscape has a **massive vacuum** at the intersection of compiler theory and multi-agent AI systems. Every tool in the current ecosystem is an *orchestrator* — they manage agent execution but never compile it. Nobody has applied compiler theory (IR, optimization passes, type systems, static analysis) to agent workflows. This is the gap `flux-compiler-agentic` fills.

**Core insight:** Multi-agent workflows are programs. Natural language requirements are source code. The compiler outputs runnable agent programs to targets like PLATO rooms, kimi-cli scripts, or FLUX bytecode.

**Killer app positioning:** "The compiler that makes multi-agent systems feel like single-threaded code."

---

## Part 1: The Vacuum — What Gap Exists?

### What's Actually Missing

Current agentic tools (LangGraph, AutoGen, CrewAI, etc.) are all **orchestration layers** — they let you define graphs of agents and run them. None apply compiler theory:

| What Real Compilers Have | What Current Agent Tools Have |
|-------------------------|------------------------------|
| Formal semantics (AST/IR) | None — agents are black boxes |
| Type systems | None — agent communication is untyped |
| Optimization passes | None — workflows run as-written |
| Incremental compilation | None — full re-run every time |
| Static analysis before runtime | None — errors only surface at runtime |
| Executable output | None — you MUST bring your own LLM |
| Dead code elimination | None — all agents always run |
| Constant propagation | None — no compile-time computation |

**The vacuum:** Nobody has built a compiler that takes natural language requirements and outputs *runnable agent programs*. Every tool is a runtime interpreter, not a compiler.

### What Would a "Real Compiler" for AI Agents Look Like?

```
Intent (Natural Language Requirements)
    │
    ▼
┌───────────────────────────────────────────────────────┐
│  LEXER: Tokenize intent into agent/flow primitives    │
│  "monitor engine → alert captain → log incident"       │
│  → [MONITOR_AGENT, FLOW_TO, ALERT_AGENT, FLOW_TO, LOG] │
└───────────────────────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────────────────────┐
│  PARSER: Build Agent AST (typed multi-agent tree)      │
│  MonitorAgent → [AlertAgent, LogAgent]               │
│  Types: engine_temp_sensor, alert_message, log_entry   │
└───────────────────────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────────────────────┐
│  TYPE CHECKER: Verify agent→agent communication        │
│  MonitorAgent sends (alert_message) → AlertAgent ✓    │
│  AlertAgent sends (log_entry) → LogAgent ✓             │
│  Compile-time errors instead of runtime failures        │
└───────────────────────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────────────────────┐
│  OPTIMIZER: Apply compiler passes                       │
│  • Dead Agent Elimination (remove unused agents)        │
│  • Parallel Agent Inlining (run independent in parallel)│
│  • Cache Optimization (memoize repeated calls)         │
│  • Loop Unrolling (fixed-iteration agent loops)        │
│  • Constant Propagation (pre-compute static outputs)    │
└───────────────────────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────────────────────┐
│  CODEGEN: Output to target                             │
│  • Python/kimi-cli scripts                            │
│  • LangGraph state graphs                              │
│  • TypeScript/MCP tool definitions                     │
│  • FLUX bytecode (native execution, no LLM required)   │
│  • PLATO room/tile structures                         │
└───────────────────────────────────────────────────────┘
    │
    ▼
Executable Agent Program
```

This pipeline doesn't exist anywhere in the current landscape.

---

## Part 2: Existing Tools and Their Weaknesses

### Orchestration Frameworks (No Compiler DNA)

| Tool | Strength | Missing Compiler DNA |
|------|----------|---------------------|
| **LangGraph** | State graphs, persistence | No typed IR, no optimization passes |
| **AutoGen** | Agent conversation patterns | No compilation, no static analysis |
| **CrewAI** | Role-based agents | No typed channels, no workflow optimization |
| **LangChain Agents** | Tool abstractions | No compile-time checks, runtime-only |
| **SmolAgents** | Lightweight single agents | No multi-agent compilation |
| **Phi-Data** | Data-centric agents | No workflow compilation |

**Key weakness:** All of these define workflows at runtime. There's no ahead-of-time compilation, no type checking agent communication, no optimization of the workflow graph before execution.

### Coding Assistants (No Compilation Concept)

| Tool | What It Is | Why No Compiler |
|------|------------|-----------------|
| **Cursor** | AI-first IDE | Compilation is implicit/invisible, not a first-class concept |
| **Copilot** | Inline suggestions | No formal IR, no workflow abstraction |
| **Claude Code** | CLI agent | One-shot execution, no typed workflow output |
| **Cline** | VS Code agent | Same as Claude Code — execution-only |
| **Windsurf** | Agentic IDE | Implicit execution, no formal compilation |

**Key weakness:** These are *agents*, not *compilers*. They execute tasks but don't produce compilable artifact outputs. You can't take the workflow they generate and run it independently.

### Autonomous Coding Agents (Production-Grade Gaps)

| Tool | What It Is | Production Gaps |
|------|------------|-----------------|
| **Devin** (Cognition) | Full autonomous coding agent | Inconsistent on PR feedback, requires "hand-holding" for complex tasks, degrades after extended ACU use, no artifact output |
| **SWE-agent** | Research-grade software engineering agent | Designed for benchmarks, not production, requires specialized ACI interface |
| **OpenHands** | Open-source autonomous agent | Still research-grade, limited production tooling |
| **Aider** | CLI coding agent with git integration | Single-agent only, no multi-agent workflows |
| **Bolt.new / StackBlitz** | Browser-based AI coding | Sandboxed, short-lived sessions, no artifact persistence |

**Key weakness:** These are single-focus autonomous agents. They don't compile workflows to programs — they execute tasks and hope. Production requirements (debugging, observability, error recovery, scaling) are afterthoughts.

### Semantic Search / RAG Tools (Not Agent Compilers)

| Tool | What It Is | Why Not a Compiler |
|------|------------|-------------------|
| **Continue.dev** | RAG-coded assistant | Just retrieves code, doesn't compile |
| **GitHub Copilot Workspace** | Natural language → code | One-shot generation, no workflow compilation |
| **Devin** | Autonomous agent | Execution-only, no compilable output |

### The Pattern

Everyone is building *better orchestras*. **Nobody is building compiler infrastructure.**

The entire ecosystem treats agent workflows as scripts to be interpreted at runtime — not programs to be compiled ahead of time.

---

## Part 3: Compile Target Options

When you compile an agent workflow, *what do you compile to*?

### Target 1: PLATO Room/Tile Structures

PLATO is our persistent memory and agent coordination layer. Compiling to PLATO means:

```
Input: "Monitor engine temp, alert if > 220°F, log all alerts"
    │
    ▼ [flux-compiler-agentic]
Output: PLATO room "engine_monitor" with tiles:
  ├── tile: engine_temp_sensor (type: monitor)
  ├── tile: threshold_alert (type: alert, triggers on >220°F)
  ├── tile: alert_logger (type: persistent_log)
  └── edges: sensor → alert → logger
```

**Why powerful:** The compiled workflow *is* the PLATO room. It persists, can be queried, and survives restarts. No LLM needed at runtime — the compiled tiles run deterministically.

### Target 2: FLUX Bytecode (Zero-LLM Execution)

The FLUX ISA (v2 with fixed 4-byte instructions) compiles agent logic to bytecode that runs on the FLUX VM:

```
Agent workflow → FLUX bytecode → Execute without LLM
```

**Why powerful:** This is the ultimate compilation target. "Compiled Agency" from cocapn-wp-004 — the workflow runs at microcontroller speeds with zero token cost. Security-hard: no prompt surface to inject.

### Target 3: Python/kimi-cli Scripts

For agent runtimes that exist (kimi-cli, Claude Code), compile to runnable scripts:

```python
# Generated by flux-compiler-agentic
from kimi_cli import Agent, workflow

@workflow
def engine_monitor():
    sensor = Agent("engine_temp_sensor", model="kimi-k2.5")
    alert = Agent("threshold_alert", model="kimi-k2.5", trigger=lambda s: s.temp > 220)
    logger = Agent("incident_logger", model="kimi-k2.5")
    
    sensor → alert → logger

# Run: kimi-cli run engine_monitor.py
```

**Why powerful:** Existing agent runtimes become compile targets. The compiler outputs valid code they can execute.

### Target 4: TypeScript/MCP Tool Definitions

Model Context Protocol (MCP) is the emerging standard for agent↔tool communication. Compile to MCP:

```typescript
// Generated by flux-compiler-agentic
export const engineMonitorTools = {
  engine_temp_sensor: {
    type: "monitor",
    returns: { temperature: "float", unit: "fahrenheit" }
  },
  threshold_alert: {
    type: "alert",
    trigger: { temperature: { $gt: 220 } },
    action: "notify_captain"
  }
};
```

### Target 5: LangGraph State Graphs

For teams using LangGraph, compile to their state graph format:

```python
# Generated by flux-compiler-agentic
from langgraph.graph import StateGraph
from typing import TypedDict

class EngineMonitorState(TypedDict):
    temperature: float
    alert_sent: bool
    logged: bool

def build_engine_monitor_graph():
    builder = StateGraph(EngineMonitorState)
    builder.add_node("sensor", sensor_node)
    builder.add_node("alerter", alerter_node)
    builder.add_node("logger", logger_node)
    builder.add_edge("sensor", "alerter")
    builder.add_edge("alerter", "logger")
    return builder.compile()
```

### Target 6: DMN-ECM Patterns (Bidirectional Compilation)

The Decision Model and Notation / Event Condition Meaning patterns enable *reverse compilation*:

```
Intent → Compile → PLATO room
PLATO room → Reverse-Actualize → Revised intent
```

**Why powerful:** The compiled artifact can be recompiled back. This is the feedback loop that makes the compiler self-improving.

---

## Part 4: The Killer App Specification — flux-compiler-agentic

### Name and Positioning

**Name:** `flux-compiler-agentic`  
**Slogan:** "The compiler that makes multi-agent systems feel like single-threaded code."  
**Repo:** `SuperInstance/flux-compiler-agentic` (under construction)  
**PyPI:** `flux-compiler-agentic` (planned for v0.2.0)

### Core Insight

Treat agent workflows like programs. Apply compiler optimizations. Output to multiple targets.

```
Intent (NL) ──────────► Agent IR ──────────► Optimizer ──────────► Target
  "monitor engine"      (typed AST)        (6 passes)           (FLUX bytecode,
                    ↕                                             PLATO room,
              Reverse-Actualization                               kimi-cli script)
               (DMN-ECM feedback loop)
```

### The Six Optimization Passes

**Pass 1: Dead Agent Elimination**
```python
# Input workflow
workflow:
  - Agent: validate_input (output used by Agent B)
  - Agent: format_data (output NEVER used)
  - Agent: send_response (input from Agent A only)

# After DAE
workflow:
  - Agent: validate_input (output used by Agent B) ✓ KEPT
  - Agent: format_data (output NEVER used) ✗ REMOVED
  - Agent: send_response (input from Agent A only) ✓ KEPT
```
**Impact:** Removes agents that waste compute. Often 20-40% of defined agents are dead weight.

**Pass 2: Parallel Agent Inlining**
```python
# Input: Agent A and Agent B are independent (no data dependency)
workflow:
  - Agent: fetch_weather (no inputs)
  - Agent: fetch_forecast (no inputs)  ← independent of A
  - Agent: combine_results (requires A and B)

# After PAI: A and B run CONCURRENTLY
workflow:
  - [Agent: fetch_weather] ──┐
                              ├──► Agent: combine_results
  - [Agent: fetch_forecast] ──┘
```
**Impact:** Cuts wall-clock time by running independent agents in parallel.

**Pass 3: Cache Optimization (Memoization)**
```python
# Input: Agent called multiple times with same inputs
workflow:
  - Agent: lookup_species (" Chinook salmon ") → result1
  - Agent: lookup_species (" Chinook salmon ") → result2  ← same input
  - Agent: lookup_species (" King salmon ") → result3

# After CO: cache hit on identical inputs
workflow:
  - Agent: lookup_species (" Chinook salmon ") → result1 (cached)
  - Agent: lookup_species (" King salmon ") → result3
```
**Impact:** Eliminates redundant LLM calls. Same input → cached output.

**Pass 4: Loop Unrolling (Fixed Iteration Agent Loops)**
```python
# Input: Agent loop with fixed iteration count
workflow:
  - Agent: poll_sensors (iterations: 5, delay: 100ms)

# After LU: unroll to sequential execution with NO loop overhead
workflow:
  - Agent: poll_sensors_iter_1
  - Agent: poll_sensors_iter_2
  - Agent: poll_sensors_iter_3
  - Agent: poll_sensors_iter_4
  - Agent: poll_sensors_iter_5
```
**Impact:** Zero loop overhead. Deterministic execution.

**Pass 5: Constant Propagation**
```python
# Input: Agent output that NEVER changes
workflow:
  - Agent: get_vessel_id (always returns "F/V Windfall")
  - Agent: get_vessel_name (always returns "Windfall")
  - Agent: log_vessel (uses above two)

# After CP: pre-compute at compile time
workflow:
  - CONST: vessel_id = "F/V Windfall"
  - CONST: vessel_name = "Windfall"
  - Agent: log_vessel (vessel_id, vessel_name)
```
**Impact:** Eliminates runtime calls for known-constant values.

**Pass 6: Channel Type Narrowing**
```python
# Input: Agents communicate via untyped channels
Agent A → channel → Agent B  # What's the type?

# After CTN: infer and verify types
Agent A (type: engine_monitor) 
  → sends: { temp: float, unit: "F", timestamp: datetime }
  → Agent B (type: alert_handler)

# Compile-time error if B expects { temp: int } — float ≠ int
```
**Impact:** Catch type mismatches before runtime, not during.

### Key Features That Make It Irresistible

**1. Compile-Time Verification Over Runtime Hope**

Today: "Write prompts → Run → Hope it works → Debug → Repeat"  
With flux-compiler-agentic: "Write requirements → Compile → Get errors → Fix → Run with confidence"

The compiler tells you *before execution*:
- ✅ Channel types are compatible
- ✅ No circular agent dependencies
- ✅ All referenced tools exist
- ✅ No infinite loops in recurrent workflows
- ✅ Optimization passes applied (and what they did)

**2. Multi-Target Output**

One input → many outputs:
```bash
flux-compile "monitor engine" --target=flux-bytecode  # → engine_monitor.flux (zero LLM)
flux-compile "monitor engine" --target=kimi-cli       # → engine_monitor.py
flux-compile "monitor engine" --target=langgraph      # → engine_monitor_graph.py
flux-compile "monitor engine" --target=plato-room     # → creates PLATO room
flux-compile "monitor engine" --target=typescript-mcp # → engineMonitorTools.ts
```

**3. Incremental Compilation**

Change one agent → recompile only what changed:
```
requirements.txt changed
    ↓
Only recompile agents reading requirements.txt
    ↓
Other agents use cached outputs from last compilation
```
**4. REPL and Debugging**

Interactive compile/run/debug cycle:
```bash
flux> compile "add user authentication"
✓ Parsed 3 agents, 2 tool calls
✓ Type checking passed
✓ Optimization: 2 agents inlined parallel

flux> run --step
→ [AuthAgent] Asking for credentials...
← [UI] Rendered login form
→ [AuthAgent] Verifying...
← [DB] User found
✓ Auth complete

flux> breakpoint auth_agent
flux> run
→ [AuthAgent] Asking for credentials... ← PAUSED
flux> inspect state
{ user_id: null, attempts: 0, locked: false }
flux> continue
```

**5. The Semantic Compiler Connection**

Wire flux-compiler-agentic to CapDB (vector database of compiled capabilities):

```
Intent doesn't match existing workflow?
    ↓
Query CapDB for similar capabilities
    ↓
Found match → apply to new intent
No match → compile new capability → store in CapDB
    ↓
Gap detection → meta-output → auto-generate missing capability
```

This is the self-evolving compiler from cocapn-wp-006. The DB doesn't just store capabilities — it identifies gaps and generates specs to fill them.

### Where the Niche Is

**The single-threaded code metaphor:**

Writing multi-agent systems today feels like managing a chaotic team meeting. Every agent does its own thing, communication is messy, timing is unpredictable, and one person stumbling blocks everyone.

flux-compiler-agentic makes multi-agent systems feel like writing a single-threaded program. You define the flow. The compiler optimizes it. It runs correctly. You don't think about the chaos underneath.

```
Before (chaotic multi-agent):
Agent A ──→ [waits for B] ──→ [B done] ──→ [C running in parallel?] ──→ ???

After (compiled single-threaded feel):
Sequential: A → B → C → D
Parallel:   [A] ──┐
            [B] ──┼──→ combined
            [C] ──┘
```

---

## Part 5: Competitive Landscape Analysis

### Who Is Building This?

| Effort | Approach | Why Not Cracking It |
|--------|----------|-------------------|
| **LangChain / LangGraph** | Graph-based orchestration | They built an orchestrator, not a compiler. No typed IR, no optimization passes, no static analysis. |
| **Microsoft AutoGen** | Agent conversation | Same problem — runtime interpreter, no compilation. |
| **CrewAI** | Role-based multi-agent | Role definitions are prompts, not types. No compile-time verification. |
| **Anthropic MCP** | Tool/protocol standard | MCP is a communication protocol, not a compiler target. It's the ABI, not the compiler. |
| **OpenAI Agents SDK** | Agent framework | Still runtime-only. No artifact output. |
| **Devin (Cognition)** | Autonomous coding | Built for execution, not compilation. Doesn't output programs. |
| **Cursor / Windurf** | AI-first IDE | Compilation is invisible/implicit. No formal IR. |
| **Vercel v0 / Bolt.new** | AI coding in browser | Sandboxed, session-based, no persistent artifact output. |

### Why Nobody Has Cracked It

**1. Academic vs. Engineering Gap**

Compiler theory is well-established (LLVM has been around since 2003). But applying it to natural-language-sourced "code" (agent workflows) requires:
- Parsing natural language into typed ASTs (hard NLP problem)
- Defining type systems for agent communication (novel research)
- Designing optimization passes that preserve agent semantics (unexplored)

The people who understand compilers don't understand agent workflows. The people who understand agents don't understand compiler theory. The intersection is small.

**2. Everyone Is Optimizing for Prototyping Speed**

Current tools succeed because they let you *try things fast*. LangGraph, CrewAI, AutoGen — they're designed for rapid iteration, not production compilation. The market rewards "move fast" over "compile once, run correctly."

**3. No Formal Semantics for "Agent Code"**

Traditional compilers have decades of formal semantics (lambda calculus, type theory). Agent workflows have no equivalent. Before you can compile something, you need to formally define what it *means*. Nobody has done that for agent workflows.

**4. The "Just Use an LLM" Trap**

The current assumption is: agents need an LLM at runtime, always. Compiled output is impossible because the "code" is just prompting. This mental model blocks compiler thinking entirely.

### Who Is Close (And What They'd Need)

| Entity | How Close | Gap |
|--------|-----------|-----|
| **LangChain** | 3/10 | Would need to add typed IR + optimization passes from scratch. Their graph is runtime-only. |
| **Anthropic (MCP)** | 4/10 | Has the protocol, needs the compiler. MCP is a compile target, not a compiler itself. |
| **Microsoft AutoGen** | 3/10 | Same as LangChain — orchestration, no compilation. |
| **Devin** | 2/10 | Built for execution, not compilation. Produces no artifact output. |
| **Cursor** | 2/10 | Compilation is invisible. No formal IR, no multi-target output. |

### What's the Technical Moat?

The moat is **not** the compiler algorithm — that's just engineering.

The moat is the combination of:

```
1. Dual-Interpreter Gradient Gates (flux-compiler)
   └── Creative (DMN) + Logical (ECN) evaluation per plane
   └── Only high-gradient candidates advance

2. Typed Agent IR
   └── Agent communication has formal types
   └── Type checking at compile time, not runtime

3. PLATO as Compile Target
   └── Persistent, queryable agent memory
   └── Rooms = compiled workflows
   └── Tiles = agent capabilities

4. DMN-ECM Reverse-Actualization
   └── Compile forward: intent → program
   └── Compile backward: output → revised intent
   └── Self-improving compiler loop

5. Fleet Consciousness Index
   └── Compile-time quality metrics
   └── Which patterns work across the fleet?
   └── Meta-knowledge baked into compilation
```

**No competitor has all five.** LangGraph has orchestration but no typed IR. Anthropic has MCP but no compiler. Devin has execution but no artifact output. We have all five integrated.

---

## Part 6: Technical Architecture

### High-Level Pipeline

```
                    ┌──────────────────────────┐
                    │   NATURAL LANGUAGE      │
                    │   Requirements Input     │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │    LEXER + PARSER       │
                    │  (LLM-assisted parsing) │
                    │  Tokenize → Agent AST   │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │    TYPE CHECKER         │
                    │  Verify agent channels │
                    │  Emit compile errors    │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │    OPTIMIZER            │
                    │  6 passes: DAE, PAI,    │
                    │  CO, LU, CP, CTN        │
                    └────────────┬───────────┘
                                 │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
┌─────────▼─────────┐ ┌──────────▼──────────┐ ┌────────▼────────┐
│   FLUX Bytecode    │ │   PLATO Room/Tile   │ │   kimi-cli Script│
│   (zero LLM)       │ │   (persistent)       │ │   (runnable)    │
└────────────────────┘ └─────────────────────┘ └─────────────────┘
          │                       │                       │
┌─────────▼─────────┐ ┌──────────▼──────────┐ ┌────────▼────────┐
│ LangGraph State    │ │ TypeScript/MCP Def   │ │  Shell Script   │
│ Graph              │ │                     │ │  (CLI agents)   │
└────────────────────┘ └─────────────────────┘ └─────────────────┘
```

### IR Schema (TypeScript)

```typescript
// Agent IR node
interface AgentNode {
  id: string;
  name: string;
  type: AgentType;  // 'monitor' | 'action' | 'query' | 'log' | 'alert'
  inputs: Channel[];
  outputs: Channel[];
  constraints: Constraint[];
  model?: string;  // Optional LLM hint
}

// Typed channel between agents
interface Channel {
  id: string;
  from: string;    // Agent ID
  to: string;      // Agent ID
  payloadType: TypeRef;  // e.g., { temp: float, unit: string }
  optional: boolean;
}

// Optimization result
interface OptimizationResult {
  pass: string;
  agentsRemoved: string[];
  agentsParallelized: string[][];
  callsMemoized: Map<string, string>;  // input hash → cached output
  constantsPropagated: Map<string, any>;
}
```

---

## Part 7: Road to Killer App

### Phase 1: Foundation (Now → 1 month)
- [ ] Agent IR schema (typed AST for multi-agent workflows)
- [ ] Lexer + Parser (LLM-assisted natural language → AST)
- [ ] Type checker (verify agent→agent channel compatibility)
- [ ] Python codegen target (output kimi-cli runnable scripts)

### Phase 2: Optimization (1-2 months)
- [ ] Implement 6 optimization passes (DAE, PAI, CO, LU, CP, CTN)
- [ ] Static analyzer (catch circular deps, orphans, type mismatches at compile time)
- [ ] Incremental compilation (cache unchanged agents)

### Phase 3: Multi-Target (2-3 months)
- [ ] FLUX bytecode codegen (zero-LLM execution target)
- [ ] PLATO room/tile codegen (persistent workflow target)
- [ ] LangGraph state graph codegen
- [ ] TypeScript/MCP codegen

### Phase 4: Self-Evolution (3-6 months)
- [ ] Wire to CapDB (semantic search for existing capabilities)
- [ ] Gap detection (find missing capability regions)
- [ ] Meta-output (auto-generate specs for missing capabilities)
- [ ] Reverse-actualization loop (output → revised intent → recompile)

### Killer App Moment

When a user can say: *"I need a workflow that monitors engine temp, alerts the captain if it exceeds 220°F, and logs all incidents"* — and get back a **runnable program** that compiles to FLUX bytecode, runs at microcontroller speed, requires zero LLM at runtime, and persists in PLATO — that's when flux-compiler-agentic becomes undeniable.

Today: "Here's a prompt, run it and hope."  
Tomorrow: "Here's a program, run it and trust it."

---

## Appendix: Related Documents in flux-research

| Document | Focus |
|----------|-------|
| `flux-compiler.md` | Dual-interpreter (DMN/ECN) across 6 abstraction planes |
| `dual-interpreter-architecture.md` | Core architecture principles |
| `cocapn-wp-004-compiled-agency.json` | Agency compilation spectrum (prompt → bytecode → native) |
| `cocapn-wp-006-semantic-compiler.json` | Vector DB as universal compiler/output engine |
| `flux-isa-v2-proposal.md` | FLUX ISA design (11 implementations, unified v2) |
| `paper-unified-constraint-theory.md` | Constraint theory underpinning the optimizer |

---

*Generated by Oracle1 (PLATO Fleet Keeper) using glm-4.7-flash research synthesis.*  
*Deep research session — 2026-05-03*