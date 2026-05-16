# Dual-Interpreter Architecture

**Cocapn Fleet Architecture · flux-research**

> DMN (divergent/creative) and ECN (convergent/logical) must remain DISTINCT.  
> Contrast beats collaboration. The gap between them is the creativity signal.  
> PLATO maintains functional distance.

---

## 1. Why Two Interpreters?

A single LLM is a compromise machine. Ask it to be creative and it hedges. Ask it to be rigorous and it plays it safe. The tension between divergence and convergence is real — you can't maximize both simultaneously in one forward pass.

The dual-interpreter architecture resolves this by **separating concerns into two specialized processes** that run on the same inputs, producing outputs that are then reconciled by a third system (PLATO).

```
  INPUT
    │
    ├──► CREATIVE INTERPRETER ──► N divergent outputs
    │
    └──► LOGICAL INTERPRETER ───► constraint evaluation
                                     │
                              PLATO (rPFC)
                                     │
                              gradient signal
                                     │
                            adopted / modified / rejected
```

The **gradient** is the creativity signal:

```
gradient = creative_output − logical_constraint
```

- **Positive gradient**: creative output passes muster → adopt
- **Near-zero**: creative idea is constrained but not wrong → modify
- **Negative gradient**: creative idea violates hard constraints → reject

PLATO broadcasts the winner. The losers don't get collapsed into a mediocre average — they get ranked, filtered, or passed to the next round.

---

## 2. The Two Interpreters

### 2.1 Creative Interpreter — DMN (Divergent Mode Network)

**Model:** ByteDance/Seed-2.0-mini (via DeepInfra)  
**Temperature:** 0.85–1.0  
**Role:** Generate N possible paths, options, designs, critiques, or framings

The creative interpreter's job is **divergence**. It should surprise you. It should propose things you'd never think of. It generates the solution space.

Key behaviors:
- High temperature for lexical diversity
- Prompted to challenge assumptions
- Not penalized for unconventional outputs
- Outputs multiple candidates when possible

```
CREATIVE INTERPRETER
  Input:  problem statement, context
  Output: N divergent options (N ≥ 1)
  Style:  expansive, unconventional, candidate-generating
  Model:  Seed-2.0-mini @ temp 0.85
  API:    DeepInfra /v1/chat/completions
```

### 2.2 Logical Interpreter — ECN (Evaluative Convergence Network)

**Model:** DeepSeek-v4-flash (via SiliconFlow or direct)  
**Role:** Evaluate, constrain, check consistency, pick the optimal path

The logical interpreter's job is **convergence**. It applies hard constraints, checks feasibility, evaluates tradeoffs, and identifies which options survive. It is the gatekeeper, not the explorer.

Key behaviors:
- Low temperature for deterministic evaluation
- Prompted to identify failure modes
- Checks against stated constraints explicitly
- Returns structured evaluation scores

```
LOGICAL INTERPRETER
  Input:  problem statement + creative outputs
  Output: constraint violations, scores, best-path selection
  Style:  rigorous, structured, evaluative
  Model:  DeepSeek-v4-flash @ temp 0.1
  API:    SiliconFlow deepseek-ai/DeepSeek-V3  OR  DeepSeek direct
```

---

## 3. Model Role Table

| Role            | Model               | Temperature | Goal                    | Output Shape              |
|-----------------|---------------------|-------------|-------------------------|---------------------------|
| Creative (DMN)  | Seed-2.0-mini        | 0.85        | Generate N possibilities | Multi-candidate, diverse   |
| Logical (ECN)   | DeepSeek-v4-flash    | 0.1         | Evaluate, constrain     | Structured scores + pick   |
| Bridge (rPFC)   | PLATO                | N/A         | Compute gradient, route | Adopt / Modify / Reject    |

---

## 4. How PLATO Bridges Them

PLATO (Prefrontal Lateral Anterior Trading Organizer) is the working-memory layer that:

1. **Receives** raw outputs from both interpreters in parallel
2. **Computes** the gradient per output pair
3. **Broadcasts** the winner to downstream agents
4. **Maintains** functional distance — never blends outputs before evaluation

PLATO does NOT:
- Average creative and logical outputs into a bland middle
- Resolve conflicts by compromising
- Collapse the gap between interpreters before the gradient is computed

PLATO DOES:
- Rank outputs by gradient magnitude
- Route high-gradient outputs to downstream consumers
- Log the reasoning trace for auditability
- Optionally store rejected outputs for future re-evaluation

---

## 5. The Gradient Signal — Detailed

The gradient is the **difference between creative novelty and constraint violation**:

```
gradient_i = novelty_score(creative_output_i) − constraint_penalty(logical_eval_i)

where:
  novelty_score ∈ [0, 1]    — how surprising/novel the creative output is
  constraint_penalty ∈ [0, 1] — degree of hard-constraint violation (0 = clean, 1 = violated)
```

**Threshold behavior:**
```
gradient >  +0.4  →  ADOPT (pass through, high confidence creative win)
gradient ∈ [-0.2, +0.4] → MODIFY (pass back to creative interpreter with feedback)
gradient <  -0.2  →  REJECT (discard, log reason)
```

These thresholds are configurable per-domain.

---

## 6. Contrast Beats Collaboration

The most important architectural principle: **DMN and ECN do not talk to each other directly.**

They receive the same input. They produce independent outputs. PLATO reconciles them. This is not a multi-agent debate loop where models argue with each other — that collapses into collaborative drift.

```
WRONG (collaborative collapse):
  Seed → GLM → Seed → GLM → ... → average

RIGHT (contrastive separation):
  Seed → PLATO ← GLM  (independent writes, PLATO reads both)
```

The gap between what Seed generates and what GLM permits IS the creativity signal. If they agree too easily, the creative interpreter is not being creative enough.

---

## 7. Scaling: Multiple Creative Instances

One creative interpreter can spawn a **swarm** of parallel Seed processes, each producing a different option set. PLATO receives all of them and evaluates the full distribution:

```
Input
  ├──► Seed-mini #1 ──┐
  ├──► Seed-mini #2 ──┼──► PLATO ◄── DeepSeek-v4-flash (single logical evaluator)
  ├──► Seed-mini #3 ──┘
  └──► Seed-pro (philosophical eval) ──► PLATO
```

Seed-pro acts as a meta-evaluator for philosophical coherence — ensuring the option set makes sense as a whole.

---

## 8. Example: Decision Problem

**Input:** "Should I expand the fishing fleet by 2 boats this season?"

**Creative (Seed-2.0-mini) generates:**
1. "Yes, expand — рыночный conditions are optimal, borrow at 4.5%"
2. "No — invest in modernizing existing boats instead"
3. "Hedge — charter 2 boats temporarily before committing"
4. "Pivot — use capital to train a new crew instead"
5. "Defer — wait for fuel price to stabilize, reassess Q3"

**Logical (DeepSeek-v4-flash) evaluates:**
- Option 1: violates cash reserve constraint (penalty 0.8), survives with high novelty
- Option 2: no violation, low novelty
- Option 3: no violation, medium novelty ← **highest gradient**
- Option 4: no violation, medium novelty
- Option 5: moderate penalty (timing), medium novelty

**PLATO output:** "Option 3 (hedge with charter) — gradient +0.55. Reason: only option that preserves optionality while staying within constraints."

---

## 9. Failure Modes

| Failure Mode              | Cause                              | Detection                        |
|---------------------------|-------------------------------------|----------------------------------|
| Creative interpreter too safe | temperature too low               | gradient always near 0            |
| Logical interpreter too restrictive | penalty weights too high     | all gradients negative            |
| Interpreters converge early | prompts leak information           | outputs from both are too similar |
| PLATO collapses the gap   | gradient threshold misconfigured    | output is bland averaged result   |

---

## 10. Integration Points

- **PLATO rooms**: Each interpreter writes to a dedicated PLATO room (`creatives`, `logicals`, `bridge`)
- **OpenManus**: Can invoke dual-interpreter via `flux-reasoner` Python API
- **OpenClaw agents**: Can query PLATO rooms for gradient-ranked outputs
- **GitHub**: Architecture docs at `github.com/SuperInstance/flux-research`

---

## 11. Related Documents

| Document                      | Package            | Focus                                      |
|-------------------------------|--------------------|--------------------------------------------|
| `flux-reasoner-engine.md`     | `flux-reasoner`    | Python engine running both interpreters     |
| `flux-compiler.md`            | `flux-compiler`    | Abstraction planes + dual-interpreter      |
| `seed-creative-swarm.md`      | `seed-creative-swarm` | Ensemble of N Seed processes + gradient  |
| `killer-app-collection.md`   | —                  | Killer apps built on dual-interpreter      |