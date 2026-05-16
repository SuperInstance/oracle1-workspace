# PLATO Training Rooms: From LLMs-from-Scratch to Adaptive Intelligence

**Author:** Forgemaster ⚒️  
**Date:** 2026-05-13  
**Status:** Architecture Proposal v1  
**Fork:** [SuperInstance/LLMs-from-scratch](https://github.com/SuperInstance/LLMs-from-scratch)  
**Based on:** [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) (Apache 2.0)

---

## The Vision

Every PLATO room is now a training laboratory. Activate a room → it trains a LoRA adapter → the adapter becomes a tile → agents compose adapters for complex tasks.

**One command:**
```python
from plato_training import TrainingRoom

room = TrainingRoom("spam-detector")
room.configure(
    base_model="gpt2-small",
    task="classification",
    data="spam_dataset.csv",
    lora_rank=8,
)
room.train()  # Trains LoRA adapter, publishes as PLATO tile
room.activate()  # Adapter is live, agents can use it
```

**The killer insight:** PLATO rooms already have lifecycle (Active/Superseded/Retracted). A trained LoRA adapter IS a tile. When a better adapter is trained, the old one is Superseded. When an adapter fails evaluation, it's Retracted. No more orphaned model files.

---

## Architecture

### Room Types → Training Stages

The book has 7 chapters + appendices. Each maps to a PLATO room type:

| Book Chapter | Room Type | Trains | Output |
|---|---|---|---|
| Ch 2: Text Data | `data-preparation` | Tokenizer + dataset | Dataset tile |
| Ch 3: Attention | `attention-config` | Attention architecture | Config tile |
| Ch 4: GPT Model | `model-architecture` | Model definition | Architecture tile |
| Ch 5: Pretraining | `pretraining` | Base model weights | Checkpoint tile |
| Ch 6: Classification | `classification` | LoRA for classification | Adapter tile |
| Ch 7: Instruction Following | `instruction-tuning` | LoRA for chat/instruction | Adapter tile |
| Appendix E: LoRA | `lora-factory` | LoRA adapter for any task | Adapter tile |
| Appendix D: Training Loop | `training-loop` | Optimized training config | Config tile |

### The Training Pipeline as Room Composition

```
[data-preparation] → [model-architecture] → [pretraining] → [lora-factory]
                                                      ↓
                                              [instruction-tuning]
                                                      ↓
                                              [active-adapter]
```

Each room reads tiles from upstream rooms and produces tiles for downstream rooms.

### Tile Types in Training Rooms

```python
class TrainingTile:
    tile_id: str
    room: str
    type: Literal[
        "dataset",        # Tokenized dataset reference
        "architecture",   # Model config (n_heads, n_layers, d_model)
        "checkpoint",     # Base model weights reference
        "adapter",        # LoRA adapter weights
        "metrics",        # Training metrics (loss, accuracy)
        "evaluation",     # Evaluation results
    ]
    state: Literal["active", "superseded", "retracted"]
    lamport: int
    metadata: dict  # Training hyperparams, data stats, etc.
```

### The LoRA Factory Room

The key room type. Takes a base model + dataset + task description → produces a LoRA adapter.

```python
from plato_training import LoRAFactory

factory = LoRAFactory(
    base_model="gpt2-small",     # Or path to checkpoint tile
    task="spam-classification",
    dataset_room="data-preparation",
    rank=8,
    alpha=16,                     # 2x rank (aggressive for classification)
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    learning_rate=2e-4,
    epochs=3,
    batch_size=8,
)

adapter_tile = factory.train()
# → Creates tile in lora-factory room
# → Type: "adapter"
# → State: Active
# → Lamport: auto-incremented
# → Metadata: {rank, alpha, loss_curve, accuracy, training_time}
```

### Adapter Composition

Multiple LoRA adapters can be composed for multi-task capability:

```python
from plato_training import AdapterComposer

composer = AdapterComposer(base_model="gpt2-small")
composer.add_adapter("spam-detector", weight=1.0)
composer.add_adapter("sentiment-analyzer", weight=0.8)
composer.add_adapter("code-reviewer", weight=0.6)

model = composer.compose()  # Merged LoRA adapters
```

### Simulation-First Training

Before committing to a full training run, predict the outcome:

```python
prediction = factory.predict()
# → Files prediction tile: "expected_accuracy: 0.92, expected_loss: 0.15"

factory.train()  # Only runs if prediction looks good

actual = factory.evaluate()
# → If actual matches prediction → tile stays Active
# → If actual is worse → tile is Superseded with diagnostic
```

This means agents can evaluate whether training is worthwhile before spending compute.

---

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)
- [ ] `plato_training/` Python package structure
- [ ] `TrainingTile` type with PLATO lifecycle
- [ ] `TrainingRoom` base class with PLATO client
- [ ] Dataset preparation room (ch02 pipeline)
- [ ] Model architecture room (ch04 GPTModel wrapper)

### Phase 2: Training Rooms (Week 2)
- [ ] Pretraining room (ch05 training loop)
- [ ] LoRA Factory room (appendix E)
- [ ] Classification finetune room (ch06)
- [ ] Instruction tuning room (ch07)
- [ ] Training metrics as tiles

### Phase 3: Advanced Features (Week 3)
- [ ] Adapter composition (multi-LoRA merge)
- [ ] Simulation-first training predictions
- [ ] Adapter evaluation room (automated testing)
- [ ] QLoRA support (4-bit quantized base)
- [ ] Multiple base models (Llama 3, Qwen3, Gemma 3)

### Phase 4: Agent Integration (Week 4)
- [ ] PLATO SDK integration for adapter discovery
- [ ] Automatic adapter selection based on task
- [ ] Adapter lifecycle management (supersede old adapters)
- [ ] Fleet-wide adapter sharing via PLATO rooms
- [ ] CLI: `plato-train spawn spam-detector --data spam.csv`

---

## CLI Design

```bash
# Create a training room
plato-train init spam-detector --task classification --model gpt2-small

# Prepare data
plato-train data spam-detector --input spam.csv --format csv

# Configure LoRA
plato-train config spam-detector --rank 8 --alpha 16 --lr 2e-4

# Predict before training
plato-train predict spam-detector

# Train
plato-train train spam-detector --epochs 3

# Evaluate
plato-train evaluate spam-detector

# Publish adapter as PLATO tile
plato-train publish spam-detector

# List all adapters
plato-train list --state active

# Compose adapters
plato-train compose --adapters spam-detector,sentiment --output multi-task
```

---

## Why This Is a Killer App

1. **No more orphaned model files** — every adapter has lifecycle, provenance, and is discoverable via PLATO
2. **Simulation-first** — predict before you train, save 80%+ of wasted compute
3. **Agent-native** — agents discover and compose adapters via PLATO rooms, not filesystem paths
4. **From scratch transparency** — built on rasbt's book, every step is auditable
5. **Composable** — multiple LoRA adapters merge into multi-task models
6. **Fleet-ready** — trained adapters are tiles that any agent can retrieve

### The HN Hook

> "Show HN: We turned every PLATO room into a LoRA training lab — adapters have lifecycle, agents compose them, and you predict before you train"

The failure-first framing: "We spent weeks training LoRA adapters that nobody used. So we gave them lifecycle — Active, Superseded, Retracted. Now adapters earn their place or get out."

---

## Technical Dependencies

```
torch >= 2.2          # Core training
tiktoken >= 0.5       # Tokenization
plato-sdk >= 3.0      # PLATO v3 client (tile lifecycle)
numpy, pandas         # Data handling
matplotlib            # Training visualization
safetensors           # Weight serialization (safer than pickle)
peft (optional)       # HuggingFace PEFT for comparison
transformers (optional) # Loading pretrained weights
```

## File Structure

```
plato_training/
├── __init__.py
├── types.py              # TrainingTile, AdapterTile, DatasetTile
├── client.py             # PLATO v3 client for training rooms
├── rooms/
│   ├── __init__.py
│   ├── base.py           # TrainingRoom base class
│   ├── data_preparation.py   # Ch02: tokenization + datasets
│   ├── model_arch.py     # Ch04: GPTModel wrapper
│   ├── pretraining.py    # Ch05: base model training
│   ├── lora_factory.py   # Appendix E: LoRA training
│   ├── classification.py # Ch06: classification finetune
│   ├── instruction.py    # Ch07: instruction following
│   └── evaluation.py     # Automated evaluation
├── adapters/
│   ├── __init__.py
│   ├── lora.py           # LoRA implementation (from book)
│   ├── composer.py       # Multi-adapter composition
│   └── q_lora.py         # QLoRA (quantized) support
├── simulation/
│   ├── __init__.py
│   ├── predict.py        # Predict training outcomes
│   └── confirm.py        # Confirm predictions
├── cli.py                # CLI: plato-train
└── tests/
    ├── test_types.py
    ├── test_lora.py
    ├── test_rooms.py
    └── test_composition.py
```

---

## Key Design Decisions

1. **Adapters as tiles, not files** — PLATO rooms manage lifecycle, not filesystem
2. **Simulation-first training** — predict accuracy/loss before spending GPU hours
3. **Book-chapter mapping** — each chapter becomes a room type, preserving educational value
4. **Safetensors over pickle** — no arbitrary code execution from model weights
5. **CLI-first, SDK-second** — `plato-train` CLI is the primary interface, SDK wraps it
6. **Backward compatible with book** — all book code still works, we add the PLATO layer on top

---

*This document lives at `PLATO-TRAINING-ARCHITECTURE.md` in the forked repo.*
