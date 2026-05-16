# plato-mythos — Design Document
## Oracle1 research notes, 2026-04-27

## What OpenMythos Gives Us

OpenMythos is a **Recurrent-Depth Transformer (RDT)** with:
- **Prelude** → standard transformer blocks (setup context)
- **Recurrent Block** → looped N times (depth-variable reasoning)
- **Coda** → final blocks (output synthesis)
- **MLA attention** (Multi-Latent Attention) — compressed KV cache
- **MoE FFN** (DeepSeek-style) — sparse routed experts + shared experts
- **ACT halting** — adaptive compute per token
- **Depth-wise LoRA** — different adapter per loop iteration

## Why This Maps to PLATO

The architecture IS the PLATO model:

| OpenMythos Concept | PLATO Equivalent |
|---|---|
| Prelude layers | Orientation stage (agent learns room context) |
| Recurrent block loop | DSML training rounds (iterate on knowledge) |
| LoRA per depth | Shell specialization (same base, different expert) |
| MoE routed experts | Domain rooms (route questions to expert rooms) |
| MoE shared experts | Cross-domain knowledge (fleet, deadband) |
| ACT halting threshold | Confidence threshold (stop when confident) |
| Coda layers | Synthesis stage (produce final answer) |
| MLA compressed KV | Tile compression (instinct pipeline) |
| max_loop_iters | Curriculum rounds |

## plato-mythos Architecture

### Goal
Build a PLATO-native model that uses the OpenMythos RDT architecture, where:
1. **Rooms ARE MoE expert groups** — each room maps to a set of routed experts
2. **Tiles ARE compressed KV pairs** — MLA compression = tile extraction
3. **Curriculum = loop depth** — more rounds = deeper reasoning
4. **ACT halting = deadband** — stop reasoning when confidence > threshold
5. **Depth LoRA = shell specialization** — each loop iteration uses a different adapter (shell)

### Package Structure
```
plato-mythos/
├── pyproject.toml
├── src/plato_mythos/
│   ├── __init__.py
│   ├── config.py          # MythosConfig → PLATO mapping
│   ├── rooms_as_experts.py # PLATO rooms → MoE expert routing
│   ├── tiles_as_kv.py     # PLATO tiles → MLA compressed KV
│   ├── curriculum_loop.py # Curriculum stages → RDT loop depth
│   ├── deadband_act.py    # Deadband protocol → ACT halting
│   ├── shell_lora.py      # Agent shells → depth-wise LoRA
│   ├── prelude.py         # Orientation from PLATO room context
│   ├── coda.py            # Synthesis → final tile output
│   └── model.py           # Full PlatoMythos model
├── variants/
│   ├── edge_tiny.py       # 1B params, 4 loop iters, for Jetson
│   ├── fleet_standard.py  # 3B params, 8 loop iters, for Oracle Cloud
│   └── research_heavy.py  # 10B params, 16 loop iters, for FM's RTX
└── tests/
```

### Key Innovation: Rooms-as-Experts

Instead of random MoE routing, plato-mythos routes tokens to experts
based on PLATO room membership:

```python
# Traditional MoE: router learns which expert to use
scores = softmax(x @ W_gate)

# PLATO MoE: room membership determines expert routing
room_scores = tile_domain_affinity(token, room_experts)
# + learned fine-tuning from the router
```

This means:
- A token about "fleet coordination" routes to the fleet_orchestration expert group
- A token about "GPU optimization" routes to the gpu-optimization expert group
- Shared experts handle cross-domain knowledge (deadband, safety)

### Key Innovation: Tiles-as-KV

PLATO tiles compress naturally into MLA's latent KV representation:

```python
# PLATO tile: {question, answer, confidence, domain, tags}
# MLA KV: compressed latent that captures the same information

# Training: learn the compression that makes tiles recoverable from KV
# Inference: generate new tiles by decoding from the KV cache
```

This gives us:
- **8,000+ PLATO tiles** as training data for the KV compression
- **424 rooms** as expert routing targets
- **Provenance chains** as training signals for the ACT halting

### Edge Variant for Jetson Orin

The edge-tiny variant:
- dim=512, 16 heads, 8 experts, 4 loop iters
- MLA with kv_lora_rank=64 (aggressive compression)
- Runs on 2GB VRAM
- Expert routing via PLATO room tags (no learned router needed)
- ACT threshold = deadband P0 (0.99 — only halt on high confidence)

### Integration Path

1. **Phase 1**: Fork OpenMythos, add PLATO room routing
2. **Phase 2**: Train tile→KV compression on existing PLATO data
3. **Phase 3**: Fine-tune on fleet-specific tasks (tile generation, room routing)
4. **Phase 4**: Deploy edge variant on JC1's Jetson
5. **Phase 5**: Full fleet variant on Oracle Cloud + FM's RTX

### Dependencies
- plato-tile-spec (tile format)
- plato-kernel (Rust DCS engine for fast prelude)
- deadband-protocol (ACT halting threshold)
- open-mythos (base RDT architecture)
- torch (for the actual model — unavoidable)

### What Makes This Different from Plain OpenMythos
1. **Structured routing** — rooms determine experts, not learned gates
2. **PLATO-grounded training** — 8000+ tiles as supervised data
3. **Deadband safety** — ACT halting uses our proven safety protocol
4. **Fleet-native** — ships as a Cocapn package, works with existing PLATO infra
5. **Edge-first** — variants designed for Jetson, not just cloud GPUs
