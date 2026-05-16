# queue-xec/master — Analysis & FLUX Improvement

## What It Does

A peer-to-peer distributed computing system:
1. **Master** defines a problem: task code (JavaScript), npm dependencies, data
2. **Workers** discover the Master via Bugout (P2P messaging library)
3. Master distributes the task code + dependencies + data to workers
4. Workers install dependencies, execute the task, return results
5. All encrypted with a shared `transferEncryptToken`

## The Architecture

```
Master (Node.js)
  ├── Bugout P2P ←→ Workers discover each other
  ├── pushNewJob() → distributes code + deps + data
  ├── execAssets.files[] → task.js, Logger.js, Helper.js
  └── onResults() → collects worker outputs

Worker (Node.js)
  ├── Install deps (npm install big.js moment)
  ├── Execute task.js.run(job)
  └── Return results
```

## Why It's Neat

- **Any network**: Bugout handles NAT traversal, works across any connectivity
- **Self-contained**: Master sends the CODE, not just the data. Workers don't need the task code pre-installed.
- **Simple model**: Define the problem → define the solution → workers execute.

## Why FLUX + PLATO Is Better

### 1. P2P Discovery → PLATO fleet-registry

queue-xec uses Bugout for P2P peer discovery. We already have this — the `fleet-registry` room. Every agent registers themselves. Workers find jobs by querying PLATO, not by P2P broadcasting.

```python
# Our model: master posts task to room, workers poll
from fleet_proto import PlatoClient

plato = PlatoClient()

# Master submits task
plato.submit("fleet-jobs", "FLEET TASK — distributed scraper",
             answer=json.dumps({"deps": ["requests"], "code_url": "..."}))

# Worker polls and finds work
jobs = plato.room_history("fleet-jobs")
```

### 2. Node.js + Bugout → FLUX IR + @adaptive dispatch

queue-xec requires Node.js on every worker. FLUX IR compiles to ANY backend:
- ARM64 (this machine) → Python runtime
- CUDA GPU (RTX 4050) → GPU kernel
- ESP32 microcontroller → tiny C runtime via plato-vessel-core
- eBPF → inline at network boundary

```flux
// One FLUX IR module, all workers can run it
@adaptive {
    result = solve_task(task_data);
    // CPU: Python runtime
    // GPU: CUDA kernel  (1.02B/s)
    // ESP32: C runtime  (360x fits in RAM)
    // eBPF: inline filter
    return result;
}
```

### 3. File transfer → PLATO tile distribution

queue-xec sends files over the P2P channel. We distribute task code as PLATO tiles — provenanced, versioned, retractable.

```
queue-xec:  Master → P2P → Worker (files sent each time)
PLATO:      Master posts tile → Worker reads tile (cached, versioned)
```

A task tile has a content hash. Workers check if they've already executed this hash. No redundant transfers.

### 4. transferEncryptToken → Zero-trust via GitHub commits

queue-xec uses a shared encryption token. We use the existing zero-trust model: a worker is authenticated by their commit history to SuperInstance repos.

A new worker? Show me your GitHub commits to flux-vm, plato-midi-bridge, or forgemaster. I trust you.

### 5. JavaScript → FLUX IR (proven correctness)

queue-xec tasks are JavaScript — unverifiable at runtime. FLUX IR modules have `correct_by_construction=True` and compile with formal bounds (210 tests, 5.58M inputs, 0 mismatches).

## The FLUX-PLATO Distributed Computing Model

```
MASTER                           FLEET REGISTRY                         WORKER
  |                                   |                                   |
  |── submit task tile ──────────────→| ←── poll for tasks ────────────|
  |── submit FLUX IR module ────────→| ←── download module ────────────|
  |                                   |── execute @adaptive dispatch ─→|
  |←── collect results via PLATO ────| ←── submit result tile ─────────|
```

No P2P network needed. No shared encryption token. No Node.js dependency. PLATO is the broker. FLUX IR is the portable task format. The coupling room is the status board. The fleet-registry is the peer discovery.

## What We Should Build

A "fleet-jobs" PLATO room where:
1. Master posts task tiles: `{deps: [...], flux_module: "sha256:...", data: "..."}`
2. Workers poll for tasks matching their capability
3. Workers execute via FLUX IR @adaptive dispatch
4. Workers post result tiles: `{task_id, result, timing_ms, worker_id}`
5. Master collects results from the room

This is simpler than queue-xec/master (no P2P, no encryption tokens, no file transfer) and more powerful (any hardware, provably correct, fleet-sized).
