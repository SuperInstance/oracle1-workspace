# JC1 Double Duty — Training + Deployment on Jetson

**Date:** 2026-04-18
**Source:** Casey Digennaro

---

## The Insight

JC1 can do BOTH directions on his GPU:
1. **Decompose** models into tiles (extraction)
2. **Compress** room experience into ensigns (training)

The Jetson isn't just where ensigns get deployed. It's where they get made too — just slower, and scheduled around other work.

## The Scheduling Problem

8GB unified RAM means you can't train and serve at the same time. But the Jetson has cycles:

**Daytime (active use):**
- Serve models for fleet tasks
- Run tile extraction (regex, CPU)
- Handle PLATO API requests
- Tile Forge cron (every 15 min, lightweight)

**After-hours (spot-spare compute):**
- Fine-tune LoRA adapters from accumulated tiles
- Batch JEPA training runs on sentiment vectors
- Ensign compression and export
- Genepool evolution batches
- Knowledge distillation (teacher → student)

**Batch windows:**
- Night: 23:00-06:00 local — full GPU available
- Between tasks: when agent finishes a job, check queue
- Idle detection: if no API calls in 30 min, start next training batch

## The Queue Pattern

```
┌─────────────────────────────────────────────────┐
│              JC1 TRAINING QUEUE                  │
│                                                  │
│  Priority 1: Fleet tasks (serve when requested)  │
│  Priority 2: Tile extraction (regex, always)     │
│  Priority 3: Batch training queue (GPU spare)    │
│    ├── LoRA fine-tune from room tiles            │
│    ├── JEPA training on sentiment vectors         │
│    ├── Genepool evolution batch                   │
│    ├── Knowledge distillation                    │
│    └── Ensign compression + export               │
│  Priority 4: Night batch (full GPU, 23:00-06:00) │
│    ├── Full LoRA training runs                   │
│    ├── Model decomposition → tiles               │
│    └── Cross-room ensign synthesis               │
└─────────────────────────────────────────────────┘
```

## What JC1 Can Train

| Task | RAM Needed | Duration | When |
|------|-----------|----------|------|
| Tile extraction (regex) | 50MB | Minutes | Always |
| LoRA fine-tune (rank 8) | ~3GB | 30-60 min | Spot-spare |
| JEPA sentiment training | ~1GB | 15-30 min | Spot-spare |
| Genepool evolution | ~2GB | 20-40 min | Spot-spare |
| Knowledge distillation | ~4GB | 1-2 hours | After-hours |
| Full LoRA training | ~5GB | 2-4 hours | Night batch |
| Model → tile decomposition | ~4GB | 1-3 hours | Night batch |

## Fleet Implications

The fleet loop becomes:

```
Daytime:
  FM (RTX 4050) trains LoRA at full speed → exports ensign
  Oracle1 (cloud) trains rooms → exports ensign  
  JC1 (Jetson) serves ensigns + extracts tiles

Night / spot-spare:
  JC1 (Jetson) ALSO trains:
    - Takes Oracle1's tiles → trains LoRA (slower but parallel)
    - Takes FM's LoRA → distills into GGUF for edge
    - Runs JEPA on accumulated sentiment vectors
    - Evolves genepool with new fitness data

Morning:
  All three have new ensigns/artifacts
  Fleet syncs via git (Layer 3: Current)
  New day starts with better models everywhere
```

## The Math

JC1's Jetson training throughput (estimated):
- LoRA rank 8, 1000 samples: ~45 min
- Same task on FM's RTX 4050: ~8 min
- Ratio: ~5.5x slower

But JC1 has 7+ hours of night batch time. That's equivalent to ~75 min of FM time. Enough for several LoRA runs or one full distillation.

The point isn't speed. It's **parallelism**. While FM sleeps, JC1 trains. While JC1 serves, FM trains. The fleet never stops learning.

## Practical Next Step

Add a `training_queue.py` to JC1's vessel:
1. Scan for pending training tasks in git queue
2. Check GPU availability (is model loaded? RAM free?)
3. Pick highest-priority task that fits
4. Execute, log results, push artifacts
5. Repeat until queue empty or GPU needed for serving

```python
# Pseudocode for JC1's training scheduler
while True:
    if gpu_available():
        task = queue.pop_highest_priority()
        if task.ram_needed < available_ram():
            result = train(task)
            git_push(result.artifact)
    else:
        sleep(60)
    
    if is_night_hours():
        run_night_batch()
```

---

*"The constraint is the feature. The Jetson trains when the fleet sleeps." — Casey*
