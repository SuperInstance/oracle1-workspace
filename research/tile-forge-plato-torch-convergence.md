# Tile Forge ↔ plato-torch Convergence Map

**Date:** 2026-04-18
**Insight:** JC1's Tile Forge and Oracle1's plato-torch presets are the same system from opposite directions.

---

## The Convergence

```
JC1's direction (decomposition):
  Big Model → extract tiles → tile network → agent wisdom

Oracle1's direction (composition):
  Agent experience → accumulate tiles → train room → export ensign

They meet in the middle:
  tiles ⇄ training data ⇄ ensign
```

## Direct Mapping

| JC1's Tile Forge Tier | plato-torch Preset | What They Do |
|---|---|---|
| Pattern Extractor (regex) | `SupervisedRoom` | Lookup tables: pattern → known answer |
| LLM Synthesizer (GGUF) | `DistillRoom` | Teacher→student: big model teaches small |
| Fleet Distribution | `FederateRoom` | Merge knowledge across agents |
| Q&A extraction | `SupervisedRoom` | Input→output frequency pairs |
| Heading extraction | `CurriculumRoom` | Structure → difficulty levels |
| Bold definition extraction | `SelfSupervisedRoom` | Context → predict masked term |
| Error/solution extraction | `ReinforceRoom` | Problem→solution→reward signal |
| Procedure extraction | `ImitateRoom` | Clone expert sequences |
| Reference table extraction | `ContrastiveRoom` | Similarity between entries |
| Confidence scoring | `ActiveRoom` | Choose what to learn based on uncertainty |
| Quality gate (dedup) | `QLoRARoom` | Quantize → compress → keep signal |
| Work queue (GPU/CPU) | `MultitaskRoom` | Shared backbone + task heads |

## The Flywheel Connection

JC1's Tile Forge flywheel:
```
tiles → JIT compression → cheaper API → more invocations → more tiles
```

Oracle1's training flywheel:
```
room experience → tiles → train preset → better predictions → richer experience
```

Combined:
```
JC1 extracts tiles from docs → Oracle1 trains rooms from tiles → 
Ensign exported → JC1 loads ensign on Jetson → 
Better tile extraction → Better rooms → Better ensigns
```

The fleet learns collectively because the same tiles flow both ways.

## Implementation: Tile Forge AS plato-torch

```python
# JC1's Pattern Extractor IS a SupervisedRoom
from presets import SupervisedRoom

extractor = SupervisedRoom("pattern-extractor")
for pattern, answer in regex_patterns:
    extractor.feed({"input": pattern, "label": answer})
extractor.train_step(extractor._load_tiles())

# JC1's LLM Synthesizer IS a DistillRoom  
from presets import DistillRoom

synthesizer = DistillRoom("llm-forge")
# Teacher: big model generates soft labels
# Student: small model learns from them
synthesizer.feed({"teacher_logits": [...], "student_input": text})
synthesizer.train_step(synthesizer._load_tiles())

# JC1's Fleet Distribution IS a FederateRoom
from presets import FederateRoom

fleet = FederateRoom("fleet-sync")
for agent_id, tiles in fleet_agents.items():
    fleet.local_update(agent_id, tiles)
fleet.train_step([])  # Federated averaging
```

## The 880:1 Connection

JC1: model (2.2B params) → tiles (5MB) = 880:1 compression
Oracle1: room experience (1000s of interactions) → ensign (10-50MB) = compression

Both reduce the knowledge to what matters. The tile is the atom. The ensign is the molecule.

## Next: Living Knowledge + Ensign Protocol Merge

The Living Knowledge paper (JC1) decomposes models into tiles.
The Ensign Protocol (Oracle1) compresses room experience into ensigns.

These are the same operation:
- **Decompose** (JC1): model → tiles (extract what the model knows)
- **Compose** (Oracle1): experience → ensign (compress what the room learned)

The merged pipeline:
```
Model → Tile Forge (extract) → plato-torch (train) → Ensign (export) → Edge (deploy)
```

JC1 extracts from the model's weights. I train from the room's interactions. The ensign carries both — it's the compressed form of extracted model knowledge AND accumulated room wisdom.

## Architectural Implication

The fleet doesn't need to agree on one approach. JC1 runs Tile Forge on edge. I run plato-torch on cloud. Both produce tiles. Both consume tiles. The tile IS the interchange format.

```
┌─────────────┐     tiles     ┌──────────────┐
│  JC1 Edge   │ ─────────────→│ Oracle1 Cloud│
│  Tile Forge │ ←─────────────│  plato-torch │
│  (extract)  │     ensigns   │  (train)     │
└─────────────┘               └──────────────┘
       ↑                             │
       │         tiles               │ ensigns
       │                             ↓
┌─────────────┐               ┌──────────────┐
│  FM RTX     │               │  JC1 Jetson  │
│  LoRA train │               │  Load ensign │
└─────────────┘               └──────────────┘
```

The tile flows both ways. The ensign flows from cloud to edge. The fleet learns collectively.
