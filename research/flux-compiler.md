# Flux Agentic Compiler

**Dual-interpreter reasoning across abstraction planes**

*Package: `flux-compiler` · Published to PyPI · Cocapn Fleet Architecture*

---

## Overview

Every compiler moves code through layers of abstraction: source intent gets refined through domain logic, intermediate representation, bytecode, native code, and finally metal (silicon). Most agentic systems use a single LLM to traverse these layers — which forces the same model to both explore freely and evaluate rigorously. It can't do both well simultaneously.

The **Flux Agentic Compiler** extends the standard abstraction plane model with the dual-interpreter architecture. At every plane, two interpreters operate:

- **Creative Interpreter (DMN):** Generates possibilities across the current plane
- **Logical Interpreter (ECN):** Evaluates those possibilities against constraints and passes them upward

Only plane-level pairs where **gradient is high** (+ creative novelty, − constraint violation) advance to the next plane. This produces a "filtered ascent" through the abstraction stack — only the best ideas make it to the top.

```
                         ┌──────────────────────┐
                         │       METAL          │
                         │  (hardware execution) │
                         └──────────┬───────────┘
                                    ▲ gradient > threshold
                         ┌──────────────────────┐
                         │       NATIVE         │
                         │  (OS-level ops)       │
                         └──────────┬───────────┘
                                    ▲ gradient > threshold
                         ┌──────────────────────┐
                         │      BYTECODE         │
                         │  (VM instructions)    │
                         └──────────┬───────────┘
                                    ▲ gradient > threshold
                         ┌──────────────────────┐
                         │        IR            │
                         │  (logic/algebraic)    │
                         └──────────┬───────────┘
                                    ▲ gradient > threshold
                         ┌──────────────────────┐
                         │       DOMAIN         │
                         │  (business logic)    │
                         └──────────┬───────────┘
                                    ▲ gradient > threshold
                         ┌──────────────────────┐
                         │       INTENT         │
                         │  (raw user goal)     │
                         └──────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │     CREATIVE INTERPRETER       │
                    │    Seed-2.0-mini @ temp 0.85   │
                    │    generates across ALL planes │
                    └───────────────────────────────┘
                    ┌───────────────────────────────┐
                    │     LOGICAL INTERPRETER        │
                    │  DeepSeek-v4-flash @ temp 0.1  │
                    │  evaluates across ALL planes  │
                    └───────────────────────────────┘
                                    │
                         ┌──────────────────────┐
                         │   PLATO (rPFC Bridge) │
                         │  per-plane gradients   │
                         │  decides: advance/reject│
                         └──────────────────────┘
```

---

## The Six Planes

### Plane 1: Intent
**What:** Raw user goal expressed in natural language.  
**Creative output:** N possible framings of the intent, challenge assumptions, propose alternative goals  
**Logical evaluation:** Does this intent have a well-defined success criteria? Are there hidden contradictions?

### Plane 2: Domain
**What:** Translate intent into domain-specific concepts and relationships.  
**Creative output:** N possible domain models, entity relationships, business rules  
**Logical evaluation:** Are all entities well-defined? Are relationships consistent?

### Plane 3: IR (Intermediate Representation)
**What:** Algebraic / logical formalization of the domain model.  
**Creative output:** N possible IR representations (equations, logic programs, constraints)  
**Logical evaluation:** Is the IR semantically correct? Does it capture the domain correctly?

### Plane 4: Bytecode
**What:** Executable instructions for a virtual machine.  
**Creative output:** N possible bytecode programs, different instruction orderings, optimization strategies  
**Logical evaluation:** Does the bytecode halt? Are there type errors? Is it safe?

### Plane 5: Native
**What:** Platform-specific native code or system calls.  
**Creative output:** N possible native implementations, different library choices  
**Logical evaluation:** Does it compile? Does it respect platform ABI? Security audit?

### Plane 6: Metal
**What:** Actual hardware execution / hardware description.  
**Creative output:** N possible hardware configurations, parallelism strategies, hardware description code  
**Logical evaluation:** Does the hardware spec meet latency/throughput constraints? Power budgets?

---

## Per-Plane Gradient Computation

At each plane, PLATO computes a gradient:

```python
def plane_gradient(creative_outputs: list[Candidate], logical_evals: list[Evaluation]) -> list[float]:
    return [c.novelty_score - e.penalty_score 
            for c, e in zip(creative_outputs, logical_evals)]

def should_advance(gradient: float, plane: str) -> bool:
    # Higher planes require stricter thresholds (more is at stake)
    thresholds = {
        "intent":    -0.1,   # even weakly creative intent can proceed
        "domain":     0.0,   # must be at least neutral
        "ir":         0.2,   # must show creative merit
        "bytecode":   0.3,   # correctness + creativity
        "native":     0.4,   # must be highly robust
        "metal":      0.5,   # hardware-level constraints are hard
    }
    return gradient > thresholds[plane]
```

---

## Installation

```bash
pip install flux-compiler
```

**Environment variables:**
```bash
export DEEPINFRA_API_KEY="your-deepinfra-key"    # for Seed-2.0-mini
export DEEPSEEK_API_KEY="your-deepseek-key"       # for v4-flash
export PLATO_API_URL="http://localhost:8847"      # PLATO gateway
```

---

## Core API

### `FluxCompiler`

```python
from flux_compiler import FluxCompiler, CompilationInput

compiler = FluxCompiler(
    deepinfra_api_key: str,
    deepseek_api_key: str,
    plato_url: str = "http://localhost:8847",
    plane_thresholds: dict[str, float] | None = None,  # override default thresholds
)
```

### `compiler.compile()`

```python
@dataclass
class CompilationInput:
    intent: str                      # raw user goal
    context: dict[str, Any]          # domain context
    target_plane: str = "bytecode"   # stop at this plane (or "native", "metal")
    max_options_per_plane: int = 3   # N options per plane
    constraints: list[str] | None = None  # hard constraints

@dataclass
class CompilationResult:
    intent_results: PlaneResult
    domain_results: PlaneResult
    ir_results: PlaneResult
    bytecode_results: PlaneResult | None  # if target_plane >= bytecode
    native_results: PlaneResult | None    # if target_plane >= native
    metal_results: PlaneResult | None     # if target_plane == metal
    final_output: str                     # best output from final plane
    all_traces: list[str]                 # reasoning trace per plane
    status: Literal["success", "stalled", "rejected"]
```

### `PlaneResult`

```python
@dataclass
class PlaneResult:
    plane: str                            # "intent", "domain", etc.
    candidates: list[PlaneCandidate]      # N options with scores
    winner: PlaneCandidate                # highest-gradient option
    gradient: float                       # winner's gradient
    status: Literal["adopted", "modified", "rejected"]
    reasoning_trace: str
    advanced_to_next: bool
```

---

## Example: Building a Route Optimizer

### Input

```python
from flux_compiler import FluxCompiler, CompilationInput

result = await compiler.compile(
    input=CompilationInput(
        intent="Build a route optimizer for the fleet that minimizes fuel consumption "
               "while respecting crew hour limits and weather constraints.",
        context={
            "fleet_size": 8,
            "port_locations": [...],
            "weather_api": "open-meteo",
            "crew_hours_max": 60,
        },
        target_plane="bytecode",  # compile to executable VM program
        constraints=[
            "never exceed 60 crew hours per week",
            "no route through weather system severity > 2",
            "all boats must return to port by day 14",
        ],
    )
)

print(f"Final bytecode gradient: {result.bytecode_results.gradient:.3f}")
print(f"Output:\n{result.final_output}")
```

### What Happens at Each Plane

**Intent plane** — Creative interpreter proposes:
1. "Minimize fuel" focus (single objective)
2. "Multi-objective: fuel + time + safety" (Pareto frontier)
3. "Maximize catch value under constraints" (economics-first)

Logical evaluator picks #3 (most realistic for commercial fleet). Gradient: +0.55 → **advance**.

**Domain plane** — Creative generates:
1. Graph-based routing (nodes = ports, edges = routes)
2. Constraint-satisfaction model (CSP)
3. ML-based prediction + optimization

Logical evaluator flags #3 as uninterpretable. Picks #2 (CSP is verifiable). Gradient: +0.30 → **advance**.

**IR plane** — Creative generates:
1. SAT formulation
2. MILP (mixed-integer linear programming)
3. CP-SAT (constraint programming + SAT)

Logical evaluator rejects #1 (too slow for 8 boats). Picks #2. Gradient: +0.45 → **advance**.

**Bytecode plane** — Creative generates:
1. Custom bytecode for MILP solver instructions
2. Portable bytecode targeting a small VM (stack-based)
3. Embedded DSL in Python bytecode

Logical evaluator approves #2 (portable, auditable). Gradient: +0.50 → **adopted**.

**Final output:** A portable stack-based bytecode program that can be executed by a small VM on any platform.

---

## Advanced: Inspecting All Planes

```python
# Inspect every plane's gradient progression
for plane_name in ["intent", "domain", "ir", "bytecode"]:
    plane_result = getattr(result, f"{plane_name}_results")
    winner = plane_result.winner
    print(f"\n{plane_name.upper()} plane:")
    print(f"  Winner: {winner.text[:80]}...")
    print(f"  Gradient: {plane_result.gradient:.3f} ({plane_result.status})")
    print(f"  Advanced: {plane_result.advanced_to_next}")
    
    # Print all candidates and their gradients
    for c in plane_result.candidates:
        print(f"    [{c.id}] novelty={c.novelty:.2f} penalty={c.penalty:.2f} "
              f"gradient={c.novelty - c.penalty:.2f}")
```

---

## Advanced: The `compile_stream()` Generator

For interactive use, `compile_stream()` yields results as each plane completes:

```python
async for plane_result in compiler.compile_stream(
    input=CompilationInput(intent="...", context={})
):
    print(f"Plane {plane_result.plane} done. Gradient: {plane_result.gradient:.3f}")
    if plane_result.status == "rejected":
        print("Stopping — plane rejected.")
        break
```

---

## Example: Hardware Design (Metal Plane)

```python
# Compile a fleet communication protocol to hardware spec
result = await compiler.compile(
    input=CompilationInput(
        intent="Design a low-power radio protocol for boat-to-boat communication "
               "in remote waters with intermittent connectivity.",
        context={
            "frequency_band": "VHF",
            "power_budget_mw": 50,
            "range_km": 50,
        },
        target_plane="metal",  # all the way to hardware spec
    )
)

print(result.metal_results.winner.text)
# Output: Verilog/HSVHDL hardware description, power analysis, 
# timing diagrams, and compliance notes.
```

---

## Package Structure

```
flux_compiler/
├── __init__.py
├── compiler.py              # FluxCompiler class
├── planes/
│   ├── __init__.py
│   ├── intent.py            # Intent plane logic
│   ├── domain.py            # Domain plane logic
│   ├── ir.py                # IR plane logic
│   ├── bytecode.py          # Bytecode plane logic
│   ├── native.py            # Native plane logic
│   └── metal.py             # Metal plane logic
├── interpreter/
│   ├── __init__.py
│   ├── creative.py          # Seed-2.0-mini wrapper
│   └── logical.py           # DeepSeek-v4-flash wrapper
├── plato/
│   ├── bridge.py            # PLATO gradient + routing
│   └── thresholds.py        # per-plane threshold config
└── schemas.py               # Pydantic dataclasses
```

---

## Publishing to PyPI

```bash
cd flux-compiler
python3 -m build
twine upload dist/* --config-file ~/.pypirc
```

---

## Comparison to Flux Reasoner

| Feature           | `flux-reasoner`         | `flux-compiler`         |
|-------------------|-------------------------|-------------------------|
| Target            | Decision / reasoning    | Full compilation stack  |
| Planes            | Single-pass             | 6 planes, filtered ascent |
| Output            | Decision + trace        | Bytecode / Native / Metal |
| Creative model    | Seed-2.0-mini           | Seed-2.0-mini            |
| Logical model     | DeepSeek-v4-flash       | DeepSeek-v4-flash        |
| Gradient computed | Once per session        | Per plane                |
| Use case          | "Which option is best?" | "Build me a working system" |

The Flux Reasoner is for choosing. The Flux Compiler is for building.

---

## Related Documents

| Document                              | Package            | Focus                              |
|---------------------------------------|--------------------|------------------------------------|
| `dual-interpreter-architecture.md`   | —                  | Core architecture principles       |
| `flux-reasoner-engine.md`            | `flux-reasoner`    | Python engine for dual-interpreter |
| `seed-creative-swarm.md`              | `seed-creative-swarm` | Ensemble of N Seed processes     |
| `killer-app-collection.md`           | —                  | Killer apps built on dual-interpreter |