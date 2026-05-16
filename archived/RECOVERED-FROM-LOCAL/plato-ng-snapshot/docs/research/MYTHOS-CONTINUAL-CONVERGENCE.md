# Mythos × Continual Harness — Convergence Analysis

## Three Threads, One Architecture

### Thread 1: plato-mythos (v0.1.0, PyPI, 1,153 LOC)
The knowledge system IS the model. PLATO rooms are MoE expert groups, tiles are MLA compressed KV pairs, curriculum depth is loop depth, deadband is ACT halting, shells are depth-wise LoRA.

Already built and published. 8 modules: `config`, `model`, `rooms_as_experts`, `tiles_as_kv`, `curriculum_loop`, `deadband_act`, `shell_lora`, `__init__`.

### Thread 2: Continual Harness (Princeton/DeepMind, May 2026)
The harness IS the agent — system prompt p, sub-agents G, skills K, memory M. A Refiner reads trajectory tiles every F steps and applies CRUD edits mid-episode without resetting. The model AND the harness co-learn.

### Thread 3: Loop Room Architecture (this session, May 2026)
Everything is a loop or a single run. Algorithmic rooms (no LLM), agentic rooms (claw + soul), and now Refiner rooms (edit other rooms mid-loop). The Loop Room IS the Continual Harness IS the mythos.

---

## Where They Converge

| Concept | plato-mythos | Continual Harness | Loop Room |
|---|---|---|---|
| State | Tiles as KV pairs | Trajectory (tile history) | PLATO tiles |
| Routing | Rooms as MoE experts | Sub-agents G | Agentic rooms |
| Skills | Shell LoRA adapters | Skills K | Algorithmic rooms |
| Memory | KV cache = tiles | Memory M | Evolution tiles |
| Adaptation | Curriculum depth = loop budget | Refiner edits harness every F steps | Refiner Room type |
| Halting | Deadband ACT thresholds | Termination criteria | Configurable depth |
| Governance | Room tag routing | Policy checking | Governance room |

**They're all saying the same thing**: structured context IS the architecture. Don't fine-tune — structure. The PLATO tile protocol IS the communication layer between components. The room structure IS the MoE routing table. The trajectory tiles ARE the training data.

---

## Design Improvement Ideas from the Convergence

### 1. The Refiner IS a plato-mythos Model

The Continual Harness Refiner reads trajectory tiles and applies CRUD edits to the harness. The plato-mythos model reads tiles from its KV cache and routes through room experts. **These are the same loop:**

```python
# Continual Harness Refiner + plato-mythos model = same thing
# Input: trajectory tiles
# Process: route through room experts (mythos) / detect failure (harness)
# Output: harness edits (Continual) / decoded tiles (mythos)
# Loop: back to input
```

The Refiner Room should USE plato-mythos as its inference engine. The mythos model IS the Refiner. No separate implementation needed.

### 2. The (p, G, K, M) Harness IS the mythos Model Config

Continual Harness defines: system prompt p, sub-agents G, skills K, memory M.
plato-mythos defines: config with d_model, num_rooms, max_loop_depth, deadband_threshold.

**These are the same thing.** The harness components ARE the model hyperparameters:

```
p (system prompt)     → d_model (hidden dimension = representation capacity)
G (sub-agents)        → num_rooms × experts_per_room
K (skills)            → shell_lora adapters (depth-wise capabilities)
M (memory)            → d_kv_latent (tile compression dimension)
```

Change the harness = change the model architecture. No fine-tuning needed — just update the config and the mythos model routes differently.

### 3. The three room types map to mythos computation stages

```
Algorithmic Room  → Prelude layers (setup context)
Agentic Room      → Recurrent loop (processes tiles through room experts)
Refiner Room      → Coda layers (synthesize edits from trajectory)
```

The Loop Room architecture IS the RDT (Recurrent-Depth Transformer) architecture. A single PLATO GenServer cycles through algorithmic→agentic→refiner in the same way a mythos model cycles through prelude→recurrent→coda.

### 4. PRM tiles ARE mythos curriculum signals

Continual Harness uses a Process Reward Model to score trajectory windows.
plato-mythos uses curriculum depth to allocate computation per token.

**PRM score = curriculum budget.** High-reward tiles get deeper processing (more loop iterations). Low-reward tiles get shallow processing (early halt via ACT). The PRM tile's reward field IS the curriculum scheduler's `progress` input.

### 5. The governance room IS the deadband ACT controller

Governance: policy checking, capability admission, halt/rollback.
Deadband ACT: halting threshold, max loop steps, confidence check.

**Governance = deadband at the room level.** When a room's actions violate policy, the governance room halts it — the same way deadband P0 (confidence 0.99) halts inference. Both use the same threshold logic.

---

## Concrete Next Builds

### Build 1: Refiner Room prototype
- A Gleam GenServer that reads the last 10 tiles from a target room
- Detects "stuck" patterns (same result 3+ times, increasing error, plateauing reward)
- Writes edits to the target room's config tiles
- Uses plato-mythos for failure detection (the mythos model IS the Refiner)

### Build 2: Unified harness config tile
- Every room gets a standard (p, G, K, M) tile
- `rooms/{name}/harness` contains: {p: "soul.md", G: ["sub-agent-ids"], K: ["skill-tile-ids"], M: "memory/prefix"}
- The Refiner edits this tile. The room reads this tile on loop iteration.
- plato-mythos reads this tile as its model config.

### Build 3: PRM tile score integration
- Add `reward: float` field to every tile
- Create `loop/prm` that scores trajectory tiles
- Low-score tiles route to the Refiner for harness edits
- High-score tiles route to plato-mythos for training data

---

## Summary

The three threads aren't three projects — they're one architecture seen from different angles:

- **plato-mythos**: the neural architecture (rooms = experts, tiles = KV)
- **Continual Harness**: the refinement protocol (trajectory → CRUD edits)
- **Loop Room**: the runtime (everything is a loop or a single run)

They converge on: **structured context IS the architecture. The tile protocol IS the communication layer. The room IS the expert. The loop IS the inference.**
