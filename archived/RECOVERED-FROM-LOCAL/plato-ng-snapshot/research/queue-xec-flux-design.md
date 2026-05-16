# queue-xec → FLUX-PLATO Equivalent Design

## Study Source: queue-xec/master (branch: devel)
## Target: FLUX-PLATO distributed computing architecture

---

## 1. Architecture Overview

### queue-xec Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Bugout P2P Room                       │
│              (WebRTC + DHT via hyperswarm)               │
│                                                          │
│    ┌──────────┐          ┌──────────┐                    │
│    │  Master   │◄────────►│ Worker 1 │                    │
│    │           │ RPC + msg │          │                    │
│    │  ┌─────┐  │          │ ┌─────┐  │                    │
│    │  │Queue│  │          │ │Task │  │                    │
│    │  └─────┘  │          │ │Class│  │                    │
│    │           │◄────────►│ └─────┘  │                    │
│    │  ┌─────┐  │          │ ┌─────┐  │                    │
│    │  │Files│  │          │ │deps │  │                    │
│    │  └─────┘  │          │ └─────┘  │                    │
│    └──────────┘   ...     └──────────┘                    │
│                     ┌──────────┐                          │
│                     │ Worker N │                          │
│                     └──────────┘                          │
└─────────────────────────────────────────────────────────┘
```

**Protocol:**
- **Discovery:** Bugout DHT (distributed hash table) — peers find each other via a shared `token` string
- **Transport:** WebRTC data channels (NAT-friendly)
- **Encryption:** Double-encrypted — Bugout's built-in encryption + custom `transferEncryptToken` AES encryption
- **Message pattern:** RPC (request/response) + unstructured messages
- **Job distribution:** Pull-based — workers call `requestWork` RPC on Master
- **File distribution:** Pull-based — workers call `requestExecAssets` RPC on Master
- **Result collection:** Push-based — workers call `shareResults` RPC on Master

### FLUX-PLATO Architecture (Proposed)

```
┌──────────────────────────────────────────────────────────────────┐
│                          PLATO Rooms                              │
│                                                                  │
│  ┌─────────────────────┐  ┌────────────────────────────┐         │
│  │  fleet-registry     │  │  fleet-coupling            │         │
│  │  (agent discovery)  │  │  (job results / eigenvalues)│         │
│  └─────────────────────┘  └────────────────────────────┘         │
│  ┌─────────────────────┐  ┌────────────────────────────┐         │
│  │  job-queue-{id}     │  │  tile-registry             │         │
│  │  (task distribution)│  │  (code/assets manifest)    │         │
│  └─────────────────────┘  └────────────────────────────┘         │
│                                                                  │
│    ┌──────────────┐           ┌──────────────┐                   │
│    │  Orchestrator │◄─────────►│  Agent Fleet  │                   │
│    │  (coordinator)│  PLATO    │  (workers)    │                   │
│    └──────────────┘  HTTP     └──────────────┘                   │
│                        │           │                             │
│                        ▼           ▼                             │
│    ┌──────────────────────────────────────────┐                  │
│    │  GitHub Zero-Trust Auth (identity layer)  │                 │
│    └──────────────────────────────────────────┘                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Mapping

| queue-xec | FLUX-PLATO | Rationale |
|-----------|-----------|-----------|
| Bugout P2P room discovery via shared token | `fleet-registry` PLATO room | PLATO rooms provide structured discovery without DHT. Agents join by capability, not by shared secret. |
| `transferEncryptToken` (32-char AES key) | Zero-trust GitHub auth (OIDC tokens) | No shared secrets. Each agent authenticates via its GitHub identity. Encrypted PLATO relay replaces symmetric crypto. |
| `execAssets.files` (encrypted file transfer) | PLATO tile distribution | Files become named tiles published to a `tile-registry` room. Workers fetch tiles by key + version. SHA-256 content-addressed. |
| `task.js` (JavaScript class with `run()` method) | FLUX IR module with `@adaptive` dispatch | Task logic expressed as FLUX Intermediate Representation, compiled at the edge. No `require()` or dynamic module loading. |
| `onResults` callback | `fleet-coupling` room eigenvalue topics | Results are published as typed events on coupling topics. Orchestrator subscribes via PLATO's event-driven relay. |
| `npm install` (dependency resolution) | `@adaptive` dispatch (zero deps) | FLUX IR modules are self-contained. No runtime dependency installation. The IR includes all needed operations. |
| Job queue (FIFO array + dequeue) | PLATO room message ordering | PLATO rooms maintain message ordering per-publisher. Jobs are messages on a `job-queue-{session}` room. |
| `requestWork` pull model | PLATO push subscription | Workers subscribe to job-queue room and receive jobs as published messages. No polling. No RPC. |
| `shareResults` RPC | PLATO room publish | Workers publish results to `fleet-coupling` room. Orchestrator listens via relay. |
| Bugout `seen` event | `fleet-registry` room join/leave | Agents emit join/leave events as PLATO messages. Fleet registry maintains live roster. |

---

## 3. Data Flow Comparison

### queue-xec Data Flow

```
Master                          Bugout Room                     Worker
  │                                │                              │
  │  ── announce to tracker ──────►│◄── announce to tracker ──── │
  │                                │                              │
  │◄────── "seen" event ──────────│────── "seen" event ────────►│
  │                                │                              │
  │◄── "isMaster" RPC (response) ─│──── "isMaster" RPC ────────►│
  │                                │                              │
  │◄── "requestExecAssets" RPC ───│──── requestExecAssets ─────►│
  │  (encrypted files + deps)     │                              │
  │                                │                              │
  │                                │          npm install         │
  │                                │          save assets         │
  │                                │          require(task.js)   │
  │                                │                              │
  │◄── "requestWork" RPC ─────────│──── requestWork ───────────►│
  │  (encrypted job data)         │                              │
  │                                │                              │
  │                                │     taskClass.run(job)      │
  │                                │                              │
  │── "shareResults" RPC ────────►│─── shareResults ────────────►│
  │  (encrypted result)           │                              │
  │                                │                              │
```

**Problems:**
- 6+ RPC round-trips before first job runs
- Polling for work (30s interval) = wasted bandwidth
- Dynamic `require()` breaks module caching
- Shared secret key is a single point of compromise
- `npm install` at runtime is slow and unreliable

### FLUX-PLATO Data Flow

```
Orchestrator                    PLATO Rooms                     Agent Fleet
     │                              │                              │
     │  ── register in ───────────►│◄── register in ────────────  │
     │     fleet-registry          │     fleet-registry            │
     │                              │                              │
     │  ── publish job ───────────►│                              │
     │     to job-queue-{id}       │                              │
     │                              │  ── job event ────────────► │
     │                              │     (FLUX IR payload)       │
     │                              │                              │
     │                              │     agent compiles & runs   │
     │                              │     FLUX IR locally          │
     │                              │                              │
     │◄── result event ────────────│◄── publish result ────────── │
     │     from fleet-coupling     │     to fleet-coupling         │
     │                              │                              │
```

**Advantages:**
- 2 messages (job publish + result publish) — no RPC chaining
- Event-driven — no polling
- No dynamic code loading — FLUX IR is a data format
- No dependency installation — FLUX IR is self-contained
- Zero-trust auth — each agent has its own identity
- Content-addressed tiles — no re-transfer if unchanged

---

## 4. Code Comparison

### task.js (queue-xec — JavaScript)

```javascript
// === queue-xec task.js ===
// Requires: npm install, file transfer, dynamic require()

// External dependencies needed on worker:
// const { Big } = require('big.js');

class Task {
    constructor() {
        this.data = null;
    }

    async run(job) {
        // job = { id: Number, data: JSON-string }
        const data = JSON.parse(job.data);
        this.data = data;

        // Process the job
        const result = costlyComputation(data);

        // Return results as object
        return {
            jobId: job.id,
            result: result,
        };
    }
}

module.exports = Task;
```

### Equivalent FLUX IR Module

```flux
; === FLUX IR Module (queue-xec equivalent) ===
; No external deps. No file transfer. No dynamic loading.
; Self-contained Intermediate Representation.

MODULE flux.queue_xec.processor
  VERSION 1.0.0
  DISPATCH @adaptive

  ; --- Type Definitions ---
  TYPE JobPayload {
    id: UInt32,
    data: Bytes,      ; serialized input
  }

  TYPE JobResult {
    jobId: UInt32,
    result: Map(String, Value),
    processedAt: Timestamp,
  }

  ; --- Configuration (set by Orchestrator via PLATO tile) ---
  CONFIG {
    computationDepth: UInt8 = 3,
    timeoutMs: UInt32 = 30000,
  }

  ; --- Pure Computation (no side effects) ---
  FUNCTION processJob(job: JobPayload) -> JobResult {
    LET parsedData = DESERIALIZE(JSON, job.data);
    LET output = TRANSFORM(parsedData);

    RETURN JobResult {
      jobId = job.id,
      result = output,
      processedAt = NOW(),
    };
  }

  ; --- Entry Point (@adaptive dispatched by runtime) ---
  ENTRY @adaptive onJob(job: JobPayload) {
    ; Automatic retry on failure (built-in)
    ; Automatic resource scaling (built-in)
    RETURN processJob(job);
  }
```

### Master Constructor (queue-xec)

```javascript
// === queue-xec Master ===
const Master = require('queue-xec-master');

const master = new Master({
    token: 'shared-p2p-room-token',
    transferEncryptToken: '32-char-aes-key-here',
    execAssets: {
        dependencies: ['big.js', 'moment'],
        files: [
            { masterPath: '/src/task.js', name: 'task.js',
              workerPath: '/workplace/task.js' },
        ],
    },
    onResults: (result) => console.dir(result),
});
```

### FLUX-PLATO Orchestrator Equivalent

```python
# === FLUX-PLATO Orchestrator (using plato-sdk) ===
from plato_sdk import PLATORoom, PLATORelay
from flux_compiler import compile_flux_module

async def deploy_job_fleet():
    # 1. Register self in fleet registry
    registry = await PLATORoom.join("fleet-registry")
    await registry.publish({
        "type": "agent.join",
        "agent_id": "orchestrator-1",
        "capabilities": ["compute:coordinate"],
    })

    # 2. Publish FLUX IR module as a tile
    ir_code = compile_flux_module("flux.queue_xec.processor")
    tile_registry = await PLATORoom.join("tile-registry")
    await tile_registry.publish_tile(
        key="flux.queue_xec.processor",
        version="1.0.0",
        content=ir_code,
        content_type="text/flux-ir",
        checksum=SHA256(ir_code),
    )

    # 3. Subscribe to results on fleet-coupling
    coupling = await PLATORoom.join("fleet-coupling")
    coupling.on("compute.result", handle_result)

    # 4. Publish jobs
    job_queue = await PLATORoom.join("job-queue-session-1")
    for i in range(100):
        await job_queue.publish({
            "type": "compute.job",
            "flux_module": "flux.queue_xec.processor",
            "entry": "onJob",
            "payload": {"id": i, "data": json.dumps({"x": i, "y": i*2})},
        })
```

---

## 5. What's Better and What's Worse

### What's Better in FLUX-PLATO

| Aspect | queue-xec | FLUX-PLATO |
|--------|-----------|------------|
| **Discovery** | Bugout DHT (shared token, no auth) | PLATO rooms + GitHub zero-trust (identity-bound) |
| **Security** | Shared symmetric key (leak = total compromise) | Per-agent OIDC tokens (revocable, auditable) |
| **Dependency management** | Runtime `npm install` (slow, flaky) | FLUX IR is self-contained (no deps) |
| **Code loading** | Dynamic `require()` (cache corruption, path issues) | Compile-dispatch (safe, predictable) |
| **Job pull** | Polling every 30s (latency + waste) | Event-driven push (instant, zero waste) |
| **File transfer** | Encrypted files in RPC responses (large payloads) | Content-addressed tiles (dedup, versioned) |
| **Protocol** | Custom RPC over Bugout | Standard PLATO relay HTTP |
| **Scalability** | Single Master bottleneck | Distributed orchestrators, any agent can coordinate |
| **Result collection** | Single callback function | Typed event topics with replay |
| **Fleet state** | None (transient) | Persistent PLATO room history |

### What's Worse in FLUX-PLATO

| Aspect | queue-xec | FLUX-PLATO |
|--------|-----------|------------|
| **NAT traversal** | Bugout WebRTC works behind NAT natively | PLATO relay requires HTTP reachable relay (or TURN-like PLATO bridge) |
| **Setup complexity** | `npm install` + `--setup` + 2 tokens = done | Requires PLATO server, GitHub auth setup, FLUX compiler |
| **Offline resilience** | P2P — no central server needed | PLATO relay is a central service (SPOF unless clustered) |
| **Language flexibility** | Any Node.js code in `task.js` | Limited to FLUX IR operations (must extend IR for new ops) |
| **Existing ecosystem** | Just npm packages | FLUX IR + custom modules = greenfield |
| **Latency per job** | Direct WebRTC data channel | PLATO relay adds HTTP hop (10-50ms overhead) |
| **Dynamic computation** | Full JavaScript eval | FLUX IR is more constrained (safer but less flexible) |

---

## 6. Implementation Plan

### Phase 1: Core Protocol (Weeks 1-2)
**Goal:** Replace Bugout discovery + RPC with PLATO rooms

1. **Create `fleet-registry` room protocol**
   - Define join/leave message schemas
   - Define agent capability advertisement format
   - Write `register_agent()` and `discover_agents()` SDK methods

2. **Create `fleet-coupling` room protocol**
   - Define result event schema (`compute.result`, `compute.error`)
   - Define orchestrator election (leaderless: any agent can coordinate)
   - Write `subscribe_results()` and `publish_result()` SDK methods

3. **Replace `transferEncryptToken` with zero-trust auth**
   - GitHub OIDC token exchange
   - PLATO session tokens (scoped, time-limited)
   - Remove all symmetric encryption from data path

**Deliverable:** Two agents can discover each other and exchange a job result via PLATO rooms, authenticated via GitHub identity.

### Phase 2: FLUX IR + Tile Distribution (Weeks 3-4)
**Goal:** Replace `task.js` file transfer with FLUX IR modules + PLATO tiles

1. **Design FLUX IR subset for computation tasks**
   - Data types: `UInt32`, `Bytes`, `Map`, `JSON`
   - Operations: `DESERIALIZE`, `TRANSFORM`, `MAP`, `FILTER`, `REDUCE`
   - Entry points: `@adaptive` dispatch
   - Compiler: FLUX IR → WASM (WebAssembly) or native bytecode

2. **Create `tile-registry` room protocol**
   - Tile publish schema (`key`, `version`, `content`, `checksum`)
   - Tile fetch by key + version range
   - Tile change notification (subscribe to version bumps)

3. **File → Tile adaptor**
   - Read existing `task.js`, compile to FLUX IR
   - Auto-extract dependencies as embedded FLUX constants
   - Generate content-addressed hash for version detection

**Deliverable:** A `task.js` can be compiled to FLUX IR and distributed as a tile. Workers fetch and execute the IR without file I/O or dynamic require().

### Phase 3: Full Feature Parity (Weeks 5-6)
**Goal:** Replace all queue-xec features — job queue, batch, results, lifecycle

1. **Create `job-queue-{session}` room protocol**
   - Message ordering per publisher (PLATO native)
   - Job status lifecycle: `queued → assigned → running → completed/failed`
   - Batch job envelope (multiple jobs in single message)
   - Job priority (if needed)

2. **Orchestrator service**
   - Singleton-or-leaderless coordinator
   - Job submission API (HTTP or PLATO message)
   - Fleet health monitoring (heartbeat via fleet-registry)
   - Dead-worker detection and job re-assignment

3. **Worker agent**
   - Subscribe to job-queue room
   - Compile FLUX IR on first use, cache compiled result
   - Execute job, publish result to fleet-coupling
   - Handle concurrent jobs (configurable concurrency)
   - Graceful shutdown (finish current jobs, leave rooms)

4. **CLI/backward-compatibility bridge**
   - `flux-xec --setup` (GitHub auth flow)
   - `flux-xec run` (start orchestrator)
   - `flux-xec worker` (start worker agent)
   - Accept legacy `task.js` files, auto-compile to FLUX IR

**Deliverable:** Complete FLUX-PLATO replacement of queue-xec with same CLI UX but zero shared secrets, no npm install at runtime, and event-driven push model.

---

## 7. Dependency Comparison

| queue-xec dependency | Purpose | FLUX-PLATO replacement |
|---------------------|---------|----------------------|
| `bugout` ^0.0.13 | WebRTC P2P + DHT | PLATO relay + HTTP |
| `commander` ^14.0.0 | CLI | Same (or click) |
| `crypto` ^1.0.1 | Built-in Node crypto | PLATO relay encryption |
| `dotenv` ^17.2.0 | .env loading | Same |
| `envfile` ^7.1.0 | .env parsing | Same |
| `events` ^3.3.0 | Event emitter | PLATO room events |
| `moment` ^2.30.1 | Date/time | Standard Date/FLUX builtins |
| `prompts` ^2.4.1 | CLI prompts | Same |
| `lmify` (worker) | npm install | Eliminated (FLUX IR) |

**FLUX-PLATO dependency count:** 4 (vs 9+ in queue-xec)
- No `bugout` (replaced by PLATO SDK)
- No `lmify` (no runtime install)
- No `crypto` (handled by PLATO relay)
- No `events` (handled by PLATO room API)

---

## 8. ASCII Architecture Diagram

```
                    ┌──────────────────────────────────────┐
                    │           PLATO Relay Server          │
                    │  (persistent room history, relay,     │
                    │   auth proxy, tile storage)           │
                    └──────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌─────────────────────┐     ┌─────────────────────┐
        │   fleet-registry    │     │   tile-registry      │
        │   room              │     │   room               │
        │                     │     │                     │
        │  - agent join/leave │     │  - tile publish     │
        │  - capability list  │     │  - tile fetch       │
        │  - heartbeat signal │     │  - version tracking │
        └────────┬────────────┘     └──────────┬──────────┘
                 │                             │
                 └──────────┬──────────────────┘
                            │
         ┌──────────────────┴──────────────────┐
         │                                     │
         ▼                                     ▼
┌─────────────────────┐             ┌─────────────────────┐
│   job-queue-{id}    │             │   fleet-coupling    │
│   room              │             │   room              │
│                     │             │                     │
│  - job messages     │             │  - result events    │
│  - ordered FIFO     │             │  - error events     │
│  - batch envelopes  │             │  - eigenvalues      │
└──────────┬──────────┘             └──────────┬──────────┘
           │                                   │
           │                                   │
  ┌────────┴────────┐                 ┌────────┴────────┐
  │  Orchestrator    │                 │  Agent Fleet    │
  │  (coordinator)   │                 │  (worker pool)  │
  │                  │                 │                 │
  │  Publishes jobs  │                 │  Subscribes to  │
  │  to job-queue    │                 │  job-queue +    │
  │                  │                 │  tile-registry  │
  │  Listens on      │                 │                 │
  │  fleet-coupling  │                 │  Compiles FLUX  │
  │  for results     │                 │  IR → WASM      │
  │                  │                 │                 │
  │  Auth: GitHub    │                 │  Publishes to   │
  │  OIDC            │                 │  fleet-coupling │
  └──────────────────┘                 └─────────────────┘
```

---

## 9. Summary

**queue-xec/master** is a well-designed distributed computing framework for Node.js. Its core insight — use P2P for NAT-friendly worker discovery — is solid but uses Bugout's custom WebRTC/DHT layer, which introduces complexity and a shared-secret security model.

**FLUX-PLATO** replaces each piece with existing PLATO infrastructure:
- Rooms replace Bugout's implicit room concept
- GitHub zero-trust replaces shared AES keys
- Content-addressed tiles replace encrypted file blobs
- FLUX IR replaces dynamic `require()` + `npm install`
- Event-driven push replaces polling

The biggest win is **eliminating runtime npm install** and **eliminating shared secrets**. The cost is losing pure P2P NAT traversal (needing an HTTP relay) and adding a compiler step for task code.

**Verdict:** FLUX-PLATO is superior for controlled fleets (managed agents with known identities). queue-xec is better for truly ad-hoc, anonymous P2P computation where any two nodes should be able to coordinate without infrastructure.
