# 🗺️ LLMs-from-scratch-early-version — The Genesis

**Status:** Archived blueprint  
**Date:** 2026-05-13  
**Wheel:** #77

## What It Is

A fork of [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) (Sebastian Raschka's canonical LLM book) that Forgemaster used as the proving ground for the **PLATO Training Rooms** concept. The original book code is untouched — the PLATO additions live in `PLATO-TRAINING-ARCHITECTURE.md` and the `plato_training/` package.

This is where the entire training pipeline was **born**. Every concept in #78 and #79 traces back to the architecture document in this repo.

## Forgotten Gold

### 1. The Original Blueprint — `PLATO-TRAINING-ARCHITECTURE.md`

This single document is the **genesis of the PLATO training vision**:

> "Every PLATO room is now a training laboratory. Activate a room → it trains a LoRA adapter → the adapter becomes a tile → agents compose adapters for complex tasks."

It defines:
- **Chapter→Room mapping**: Each chapter of Raschka's book maps to a PLATO room type (Ch2→data-preparation, Ch3→attention-config, Ch4→model-architecture, Ch5→pretraining, Ch6→classification, Ch7→instruction-tuning, Appendix E→lora-factory)
- **Room composition as pipeline**: `[data-preparation] → [model-architecture] → [pretraining] → [lora-factory]`
- **Tile types for training**: dataset, architecture, checkpoint, adapter, metrics, evaluation
- **Simulation-first prediction**: Predict training outcomes before spending GPU hours
- **Adapter composition**: Multi-LoRA merge for multi-task capability
- **CLI design**: `plato-train` commands that still don't exist

### 2. Early LoRAFActory Implementation `rooms/lora_factory.py`

The original `LoRAFactory` class had features the evolved version lost:
- `predict()` method returning a prediction tile with heuristic accuracy estimates
- `configure()` with both model and config in a single call
- Full `_evaluate_loss()` with training loop

### 3. Original `plato_training/__init__.py` Exposes a Clean API

```python
from .rooms.lora_factory import LoRAFactory
```

This is the interface plato-ng should expose. Clean, minimal, one import for training.

## Why It Matters

This repo is the **prototype** that proved the concept worked. The architecture doc contains design decisions that the evolved repos silently assumed:
- **Adapters as tiles, not files** — the killer insight
- **Simulation-first** — predict before train
- **Book-chapter mapping** — each chapter is a room type
- **Safetensors over pickle** — security-first weight serialization
- **CLI-first, SDK-second** — `plato-train` is the UX

The `HN Hook` section in the doc is still golden copy for communication.

## Integration Points

- #78 `plato-training` **implemented** everything this doc envisioned
- #79 `plato-types` **formalized** the types this doc sketched
- The architecture doc should be archived in plato-ng as historical design rationale
- The `plato-train init` CLI design in this doc should inform plato-ng's CLI

## Rediscovered Value

The chapter-to-room mapping is the most undervalued insight here. Each Raschka chapter teaches a skill that maps to a PLATO room. This means **any ML book can be turned into PLATO rooms** — the mapping IS the learning architecture. The `LLMs-from-scratch` fork is the template for turning any educational resource into a z/OS-like training pipeline.
