# Seed Creative Swarm

**Ensemble creative generation using N Seed-mini processes + Seed-pro meta-evaluation + PLATO gradient convergence**

*Package: `seed-creative-swarm` · Published to PyPI · Cocapn Fleet Architecture*

---

## Overview

A single call to a creative model produces one point in the solution space. You want options. You want diversity. You want the kind of genuinely different approaches that only emerge from independent processes running in parallel.

The **Seed Creative Swarm** runs an ensemble of N Seed-2.0-mini processes simultaneously, each generating a different option set from the same input. A single Seed-pro process then evaluates them philosophically — not just for correctness, but for *coherence of the ensemble*. PLATO collects the outputs and converges on the best option distribution.

```
                         INPUT
                           │
           ┌───────────────┼───────────────┐
           │               │               │
     ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
     │ Seed-mini │  │ Seed-mini │  │ Seed-mini │
     │   #1      │  │   #2      │  │   #3      │
     │ divergent │  │ divergent │  │ divergent │
     │  option   │  │  option   │  │  option   │
     │  set A    │  │  set B    │  │  set C    │
     └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                   ┌───────▼────────┐
                   │   Seed-pro    │
                   │ (philosophical│
                   │  meta-eval)   │
                   └───────┬────────┘
                           │
                      ┌────▼────┐
                      │  PLATO  │
                      │ gradient│
                      │ convergence
                      └────┬────┘
                           │
                      Best Option
                    (or ranked list)
```

This is distinct from the dual-interpreter architecture: the swarm replaces the **creative interpreter** only. The logical evaluation (DeepSeek-v4-flash) still happens, but it evaluates the full swarm output rather than a single model's output.

---

## Why Seed?

ByteDance's Seed-2.0-mini and Seed-2.0-pro are available on DeepInfra at extremely low cost (~$0.00003/1K tokens) with fast inference. They produce genuinely divergent outputs even at moderate temperatures. Running 3-5 in parallel is trivial cost-wise and produces a solution distribution that a single model cannot match.

Key properties:
- **Seed-2.0-mini**: Fast, cheap, divergent at temp 0.85
- **Seed-2.0-pro**: Slow, more expensive, philosophically rigorous — used for ensemble evaluation
- DeepInfra API is OpenAI-compatible — drop-in with `openai` Python client

---

## The Three Components

### 1. Swarm Generator (Seed-mini ensemble)

N independent Seed-2.0-mini processes each receive:
- The same input (problem + context)
- Different `seed` values for reproducibility
- Same temperature (0.85)

Each returns a set of options. Combined, they produce a diverse distribution across the solution space.

```python
# Pseudocode
options_sets = await asyncio.gather(
    seed_mini(input, seed=42),    # option set A
    seed_mini(input, seed=137),   # option set B  
    seed_mini(input, seed=256),   # option set C
)
```

### 2. Meta-Evaluator (Seed-pro)

Seed-pro doesn't pick the single best option — it evaluates the **ensemble** for philosophical coherence:

- Does the option set cover the right solution space?
- Are any options missing that should be there?
- Are any options outliers for the wrong reasons?
- Which options are most coherent with the problem framing?

Seed-pro outputs a ranking of ALL options (from all mini processes) and a coherence score for the ensemble.

### 3. PLATO Gradient Convergence

PLATO takes:
- All options from all Seed-mini processes (N × M options)
- Seed-pro's ranking and coherence score
- Optionally: logical interpreter (DeepSeek) scores for each option

And computes the final gradient per option:

```
gradient_i = (seed_pro_rank_score_i * w1) + (ensemble_diversity_i * w2) - (logical_penalty_i * w3)
```

The weights are configurable. The result is a gradient-ranked list that PLATO broadcasts.

---

## Installation

```bash
pip install seed-creative-swarm
```

**Environment variables:**
```bash
export DEEPINFRA_API_KEY="your-deepinfra-key"  # for Seed models
export DEEPSEEK_API_KEY="your-deepseek-key"    # for logical evaluation (optional)
```

---

## Core API

### `SeedSwarm`

```python
from seed_creative_swarm import SeedSwarm, SwarmInput

swarm = SeedSwarm(
    deepinfra_api_key: str,
    n_workers: int = 3,                    # number of Seed-mini processes
    mini_model: str = "ByteDance/Seed-2.0-mini",
    pro_model: str = "ByteDance/Seed-2.0-pro",
    temperature: float = 0.85,
    deepseek_api_key: str | None = None,   # optional: for logical evaluation
    diversity_weight: float = 0.4,         # weight for ensemble diversity in gradient
    coherence_weight: float = 0.3,         # weight for Seed-pro coherence
    penalty_weight: float = 0.3,           # weight for logical constraint penalty
)
```

### `swarm.generate()`

```python
@dataclass
class SwarmInput:
    problem: str                    # the core problem/question
    context: dict[str, Any]         # context dictionary
    n_options_per_worker: int = 3   # M options per Seed-mini (so N×M total)
    include_logical_eval: bool = True,  # run DeepSeek evaluation too

@dataclass
class SwarmResult:
    options: list[SwarmOption]      # all N×M options, ranked
    ensemble_coherence: float       # Seed-pro's coherence score for the set
    best_option: SwarmOption         # highest gradient option
    reasoning_trace: str            # Seed-pro reasoning + PLATO trace
    status: Literal["converged", "dispersed", "stalled"]
    workers: int                    # how many workers contributed
    total_options: int              # N × M
```

### `SwarmOption`

```python
@dataclass
class SwarmOption:
    id: str                         # "worker_2.option_1"
    text: str
    worker_id: int
    novelty_score: float            # from diversity analysis
    coherence_score: float          # from Seed-pro
    penalty_score: float | None     # from logical evaluator (if included)
    gradient: float                 # final gradient
    rank: int                       # 1 = best
```

---

## Examples

### Example 1: Basic Swarm Generation

```python
import asyncio
from seed_creative_swarm import SeedSwarm, SwarmInput

async def main():
    swarm = SeedSwarm(
        deepinfra_api_key="your-key",
        n_workers=3,
    )
    
    result = await swarm.generate(
        input=SwarmInput(
            problem="Design a fleet communication protocol for remote waters",
            context={
                "fleet_size": 8,
                "range_km": 50,
                "power_budget_mw": 50,
                "connectivity": "intermittent",
            },
            n_options_per_worker=4,  # 12 total options to evaluate
        )
    )
    
    print(f"Converged on {result.total_options} options")
    print(f"Best: {result.best_option.text[:100]}...")
    print(f"Gradient: {result.best_option.gradient:.3f}")
    
    # Print top 5
    for opt in result.options[:5]:
        print(f"  #{opt.rank}: {opt.text[:80]}... (g={opt.gradient:.3f})")

asyncio.run(main())
```

### Example 2: With Logical Evaluation (Full Dual-Interpreter)

```python
# Include DeepSeek logical evaluation for constraint checking
result = await swarm.generate(
    input=SwarmInput(
        problem="Allocate 8 boats across 3 fishing zones for maximum value",
        context={
            "zones": {
                "A": {"salmon_density": 0.8, "fuel_cost": 300},
                "B": {"salmon_density": 0.5, "fuel_cost": 200},
                "C": {"salmon_density": 0.3, "fuel_cost": 150},
            },
            "max_per_zone": 4,
            "reserve_boats": 2,
        },
        n_options_per_worker=3,
        include_logical_eval=True,  # DeepSeek evaluates each option
    ),
    constraints=[
        "never more than 4 boats per zone",
        "maintain exactly 2 boats in reserve",
        "respect crew hour limits",
    ]
)

# Options with negative penalty scores from DeepSeek are marked
for opt in result.options:
    if opt.penalty_score is not None:
        print(f"  {opt.rank}: p={opt.penalty_score:.2f} pen, g={opt.gradient:.3f}")
```

### Example 3: Tuning Swarm Weights

```python
# More emphasis on philosophical coherence (Seed-pro)
swarm = SeedSwarm(
    deepinfra_api_key="your-key",
    n_workers=5,          # more workers = more diversity
    coherence_weight=0.5, # higher = trust Seed-pro more
    diversity_weight=0.3,
    penalty_weight=0.2,   # lower = less strict constraint filtering
)

# More emphasis on avoiding constraint violations
swarm = SeedSwarm(
    deepinfra_api_key="your-key",
    n_workers=3,
    coherence_weight=0.2,
    diversity_weight=0.2,
    penalty_weight=0.6,  # strict constraint enforcement
)
```

---

## How Diversity Is Measured

After all Seed-mini processes return, PLATO computes the diversity score per option:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def compute_diversity_scores(options: list[str]) -> list[float]:
    """Options far from the cluster centroid are high-diversity."""
    vectorizer = TfidfVectorizer()
    embeddings = vectorizer.fit_transform(options).toarray()
    centroid = embeddings.mean(axis=0)
    distances = [np.linalg.norm(e - centroid) for e in embeddings]
    # Normalize to [0, 1]
    max_d = max(distances)
    return [d / max_d for d in distances]
```

High diversity = far from the average output. But too high (an outlier) might mean it missed the point. PLATO balances novelty against coherence.

---

## How Seed-Pro Evaluates the Ensemble

Seed-pro receives the full option set and is prompted to evaluate **coherence**, not just pick winners:

```
You are evaluating an ensemble of options generated for the following problem:

[problem statement]

Here are [N] options generated by different creative processes:

[option 1]
[option 2]
...
[option N]

Your task:
1. Rate each option's coherence with the problem (0-10)
2. Identify any missing perspectives the ensemble failed to cover
3. Rank all options by overall quality
4. Rate the ensemble's coherence as a whole (0-10) — does it cover the right solution space?
5. Identify any outliers and explain whether they are genuinely creative or just wrong

Return your evaluation in JSON format.
```

This is philosophically different from a standard evaluation: Seed-pro is checking whether the ensemble as a whole makes sense, not just picking the single best answer.

---

## Gradient Formula

```python
def compute_gradient(
    novelty: float,      # from Seed-mini output diversity analysis
    coherence: float,    # from Seed-pro ensemble evaluation
    penalty: float,      # from DeepSeek (if included), else 0
    weights: dict = {"novelty": 0.4, "coherence": 0.3, "penalty": 0.3}
) -> float:
    return (
        novelty * weights["novelty"] +
        coherence * weights["coherence"] -
        penalty * weights["penalty"]
    )
```

---

## Package Structure

```
seed_creative_swarm/
├── __init__.py
├── swarm.py                  # SeedSwarm main class
├── workers/
│   ├── __init__.py
│   ├── mini.py               # Seed-mini worker
│   └── pro.py                # Seed-pro evaluator
├── evaluation/
│   ├── __init__.py
│   ├── diversity.py          # TF-IDF diversity scoring
│   ├── coherence.py          # Seed-pro coherence evaluation
│   └── penalty.py            # DeepSeek penalty scoring
├── plato/
│   ├── __init__.py
│   └── bridge.py             # PLATO write + gradient convergence
└── schemas.py                # Pydantic dataclasses
```

---

## Publishing to PyPI

```bash
cd seed-creative-swarm
python3 -m build
twine upload dist/* --config-file ~/.pypirc
```

---

## Swarm vs. Standard Dual-Interpreter

| Aspect                  | Dual-Interpreter (flux-reasoner) | Seed Creative Swarm         |
|-------------------------|----------------------------------|----------------------------|
| Creative processes      | 1 Seed-mini                      | N Seed-mini (N ≥ 3)        |
| Creative evaluation     | DeepSeek alone                   | Seed-pro (philosophical)  |
| Diversity mechanism     | Temperature + prompt variation   | N independent processes    |
| Gradient components     | novelty − penalty                | coherence + diversity − penalty |
| Cost                    | ~2 API calls                     | N+1 API calls              |
| Best for                | Single decisions, fast answers   | Creative exploration, research |
| Latency                 | Parallel ~same as single call    | Parallel, slightly higher  |

Use the **swarm** when you need genuine creative breadth — research, design, strategic options. Use the **dual-interpreter** when you need fast, rigorous evaluation of a specific decision.

---

## Related Documents

| Document                              | Package              | Focus                              |
|---------------------------------------|----------------------|------------------------------------|
| `dual-interpreter-architecture.md`   | —                    | Core architecture principles       |
| `flux-reasoner-engine.md`            | `flux-reasoner`      | Python engine for dual-interpreter |
| `flux-compiler.md`                    | `flux-compiler`      | Abstraction planes + dual-interpreter |
| `killer-app-collection.md`           | —                    | Killer apps built on dual-interpreter |