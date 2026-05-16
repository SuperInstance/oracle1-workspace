# Flux Reasoner Engine

**A Python package for running dual-interpreter reasoning with PLATO gradient arbitration**

*Package: `flux-reasoner` · Published to PyPI · Cocapn Fleet Architecture*

---

## Overview

`flux-reasoner` is a Python package that implements the dual-interpreter architecture described in `dual-interpreter-architecture.md`. It runs two LLM interpreters in parallel — one creative (Seed-2.0-mini via DeepInfra), one logical (DeepSeek-v4-flash) — and uses PLATO to compute the gradient between them.

```
Input ──►┌─────────────────────────────────────────────┐
         │         FLUX REASONER ENGINE               │
         │                                             │
         │  ┌─────────────────┐  ┌─────────────────┐  │
         │  │ CREATIVE (DMN)  │  │ LOGICAL (ECN)   │  │
         │  │ Seed-2.0-mini   │  │ DeepSeek-v4-flash│  │
         │  │ @ temp 0.85     │  │ @ temp 0.1       │  │
         │  └────────┬────────┘  └────────┬────────┘  │
         │           │                    │          │
         │           ▼                    ▼          │
         │  ┌─────────────────────────────────────┐  │
         │  │           PLATO (rPFC Bridge)        │  │
         │  │   gradient = novelty − penalty       │  │
         │  │   broadcasts: adopt / modify / reject │  │
         │  └─────────────────────────────────────┘  │
         │                    │                      │
         └────────────────────┼──────────────────────┘
                              ▼
                         Final Output
```

---

## Installation

```bash
pip install flux-reasoner
```

**Requirements:**
- Python 3.10+
- `httpx` for async HTTP calls
- `pydantic` for structured outputs
- `asyncio` for parallel execution

**Environment variables:**
```bash
export DEEPINFRA_API_KEY="your-deepinfra-key"      # for Seed-2.0-mini
export DEEPSEEK_API_KEY="your-deepseek-key"        # for v4-flash
export PLATO_API_URL="http://localhost:8847"        # PLATO gateway (default)
```

---

## Quick Start

```python
import asyncio
from flux_reasoner import ReasonerEngine, ProblemInput

async def main():
    engine = ReasonerEngine()
    
    result = await engine.reason(
        problem=ProblemInput(
            question="Should I expand the fishing fleet by 2 boats this season?",
            context={"cash_reserve": 150000, "fuel_costs": "volatile", "crew_availability": "limited"}
        )
    )
    
    print(f"Decision: {result.winner}")
    print(f"Gradient: {result.gradient:.3f}")
    print(f"Status:   {result.status}")  # adopted / modified / rejected

asyncio.run(main())
```

---

## Core API

### `ReasonerEngine`

The main class. Manages both interpreter processes and PLATO integration.

```python
from flux_reasoner import ReasonerEngine

engine = ReasonerEngine(
    deepinfra_api_key: str,           # DeepInfra key for Seed
    deepseek_api_key: str,            # DeepSeek key for v4-flash
    deepinfra_base_url: str = "https://api.deepinfra.com/v1/openai",
    deepseek_base_url: str = "https://api.deepseek.com",
    plato_url: str = "http://localhost:8847",
    novelty_threshold: float = 0.4,   # min novelty to pass
    penalty_threshold: float = 0.7,   # max penalty before reject
    max_candidates: int = 5,          # N options from creative interpreter
    temperature_creative: float = 0.85,
    temperature_logical: float = 0.1,
)
```

### `engine.reason()`

Main entry point. Runs both interpreters in parallel and returns the gradient-ranked result.

```python
from flux_reasoner import ReasonerEngine, ProblemInput

result = await engine.reason(
    problem: ProblemInput,
    constraints: list[str] | None = None,  # optional hard constraints
    verbose: bool = False,                  # print intermediate steps
) -> ReasoningResult
```

### `ProblemInput`

```python
@dataclass
class ProblemInput:
    question: str                    # the core question or decision
    context: dict[str, Any]          # key-value context
    n_options: int = 5               # how many creative options to generate
```

### `ReasoningResult`

```python
@dataclass
class ReasoningResult:
    winner: str                      # the winning option text
    gradient: float                  # novelty − penalty
    status: Literal["adopted", "modified", "rejected"]
    creative_outputs: list[CandidateOption]   # all N creative options
    logical_evaluations: list[Evaluation]      # scores per option
    reasoning_trace: str             # full PLATO trace for audit
    timestamp: datetime
```

### `CandidateOption`

```python
@dataclass
class CandidateOption:
    id: int
    text: str
    novelty_score: float  # ∈ [0, 1]
    raw_output: str       # unmodified Seed output
```

### `Evaluation`

```python
@dataclass
class Evaluation:
    option_id: int
    penalty_score: float   # ∈ [0, 1], 0 = clean
    passes_constraints: bool
    best_path: bool        # is this the logical interpreter's pick?
    failures: list[str]    # specific constraint violations
```

---

## Detailed API Examples

### Example 1: Basic Decision Making

```python
import asyncio
from flux_reasoner import ReasonerEngine, ProblemInput

async def decide():
    engine = ReasonerEngine()  # uses env vars
    
    result = await engine.reason(
        problem=ProblemInput(
            question="Which port should we dock at for the winter maintenance?",
            context={
                "fuel_price_anchorage": 3.20,
                "fuel_price_kodiak": 2.85,
                "drydock_capacity_anchorage": "3 boats",
                "drydock_capacity_kodiak": "full",
                "crew_flight_cost_anchorage": 450,
                "crew_flight_cost_kodiak": 1200,
            }
        )
    )
    
    print(f"Winner: {result.winner}")
    print(f"Gradient: {result.gradient:.3f}  ({result.status})")
    print(f"Reasoning: {result.reasoning_trace}")

asyncio.run(decide())
```

### Example 2: With Hard Constraints

```python
result = await engine.reason(
    problem=ProblemInput(
        question="How should we allocate the fleet for the fall season?",
        context={"fleet_size": 8, "market_prices": {"salmon": 4.20, "cod": 2.10}},
    ),
    constraints=[
        "never send more than 4 boats to the same zone",
        "maintain at least 2 boats in reserve",
        "respect crew hour limits (max 60h/week)",
    ],
)
```

### Example 3: Iterative Refinement (Modify Loop)

```python
result = await engine.reason(problem=ProblemInput(question="...", context={}))

if result.status == "modified":
    # Feed PLATO's feedback back into the creative interpreter
    revised = await engine.reason(
        problem=ProblemInput(question="...", context={}),
        feedback=result.reasoning_trace,  # PLATO's feedback to creative interpreter
        iteration=2,
    )
    print(f"Revised winner: {revised.winner}")
```

### Example 4: Full Candidate Exploration

```python
result = await engine.reason(problem=ProblemInput(question="...", context={}))

# Inspect all candidates and their scores
for candidate in result.creative_outputs:
    eval_result = next(
        e for e in result.logical_evaluations if e.option_id == candidate.id
    )
    print(f"  Option {candidate.id}: novelty={candidate.novelty_score:.2f}, "
          f"penalty={eval_result.penalty_score:.2f}, "
          f"gradient={candidate.novelty_score - eval_result.penalty_score:.2f}")
```

---

## Architecture: How It Works

### Step 1 — Parallel Invocation

Both interpreters receive the same `ProblemInput` simultaneously. They do NOT see each other's outputs.

```python
# Pseudo-code for the parallel run
async def _run_parallel(self, problem: ProblemInput):
    creative_task = self._creative_interpreter(problem)   # Seed-2.0-mini
    logical_task  = self._logical_interpreter(problem)   # DeepSeek-v4-flash
    
    results = await asyncio.gather(creative_task, logical_task)
    return results[0], results[1]
```

### Step 2 — Novelty Scoring (Creative)

The creative interpreter returns N text options. Novelty is computed by:

1. Passing each option through a lightweight embedding model
2. Computing pairwise cosine distance between all options
3. Options that are far from the cluster centroid get higher novelty

```python
def compute_novelty(options: list[str]) -> list[float]:
    embeddings = embed_batch(options)  # e5-small or similar
    centroid = mean(embeddings)
    scores = [cosine_distance(e, centroid) for e in embeddings]
    return normalize(scores)  # scale to [0, 1]
```

### Step 3 — Penalty Scoring (Logical)

The logical interpreter receives the problem + all N options and evaluates each against constraints.

```python
def compute_penalty(evaluations: list[Evaluation]) -> list[float]:
    # penalty = 0 means no constraint violations
    # penalty = 1 means hard violation
    return [e.penalty_score for e in evaluations]
```

### Step 4 — Gradient Computation (PLATO)

```python
def compute_gradient(
    novelty_scores: list[float],
    penalty_scores: list[float]
) -> list[float]:
    return [n - p for n, p in zip(novelty_scores, penalty_scores)]

def decide_status(gradient: float) -> str:
    if gradient > 0.4:  return "adopted"
    elif gradient >= -0.2: return "modified"
    else: return "rejected"
```

### Step 5 — PLATO Write

The final result (winner + reasoning trace) is written to a PLATO room:

```python
plato_payload = {
    "room": f"flux_reasoner_{problem.question[:40]}",
    "winner": winner_text,
    "gradient": final_gradient,
    "status": status,
    "candidates": [...],    # all options with scores
    "trace": reasoning_trace,
}
await self._plato.write(plato_payload)
```

---

## Package Structure

```
flux_reasoner/
├── __init__.py           # exports: ReasonerEngine, ProblemInput, ReasoningResult
├── engine.py             # ReasonerEngine class
├── interpreters/
│   ├── __init__.py
│   ├── creative.py       # Seed-2.0-mini interpreter (DeepInfra)
│   └── logical.py        # DeepSeek-v4-flash interpreter
├── plato/
│   ├── __init__.py
│   ├── bridge.py         # PLATO gradient computation + write
│   └── scoring.py        # novelty + penalty scoring
├── schemas.py            # Pydantic dataclasses
└── utils.py              # embedding helpers, normalization
```

---

## Usage with OpenManus

```python
from flux_reasoner import ReasonerEngine, ProblemInput

async def flux_task(task_description: str, context: dict):
    engine = ReasonerEngine()
    result = await engine.reason(
        problem=ProblemInput(question=task_description, context=context),
        verbose=True,
    )
    return {
        "answer": result.winner,
        "confidence": abs(result.gradient),
        "trace": result.reasoning_trace,
    }
```

---

## Configuration Reference

| Parameter                | Default                              | Description                          |
|--------------------------|--------------------------------------|--------------------------------------|
| `deepinfra_api_key`      | env `DEEPINFRA_API_KEY`              | DeepInfra API key (Seed models)      |
| `deepseek_api_key`       | env `DEEPSEEK_API_KEY`               | DeepSeek API key (v4-flash)          |
| `plato_url`              | `http://localhost:8847`              | PLATO gateway URL                    |
| `novelty_threshold`      | `0.4`                                | Min novelty score to be considered   |
| `penalty_threshold`      | `0.7`                                | Max penalty before auto-reject       |
| `max_candidates`         | `5`                                  | N options from creative interpreter  |
| `temperature_creative`   | `0.85`                               | Temperature for Seed-2.0-mini        |
| `temperature_logical`    | `0.1`                                | Temperature for DeepSeek-v4-flash    |
| `model_creative`         | `ByteDance/Seed-2.0-mini`            | Creative model ID (DeepInfra)        |
| `model_logical`          | `deepseek-ai/DeepSeek-V3`            | Logical model (SiliconFlow or direct)|

---

## Publishing to PyPI

```bash
# Build
cd flux-reasoner
python3 -m build

# Publish
twine upload dist/* --config-file ~/.pypirc
```

PyPI account: `cocapn` (token in `~/.pypirc`)

---

## Related Documents

| Document                         | Package              | Focus                              |
|----------------------------------|----------------------|------------------------------------|
| `dual-interpreter-architecture.md` | —                  | Core architecture principles       |
| `flux-compiler.md`               | `flux-compiler`        | Abstraction planes + dual-interpreter |
| `seed-creative-swarm.md`         | `seed-creative-swarm`  | Ensemble of N Seed processes        |
| `killer-app-collection.md`       | —                    | Killer apps built on dual-interpreter |