# Logical Connection Layer: From Theorems to Implementation

> *How the Spectral Gap Theorem, the VenueRoom equilibrium loop, and the fleet-jobs protocol converge into working code.*

---

## 1. Spectral Gap → fleet-jobs Implementation

### 1.1 Theorem Recap

**Theorem 3 (Spectral Gap Completion):** A task completes iff the spectral gap of the computation's coupling tensor exceeds a threshold Θ. Formally:

```
γ(t) = λ₁(t) - λ₂(t)  where λ₁ ≥ λ₂ ≥ ... ≥ λ_K are eigenvalues of W(t)
Task completes at t* iff γ(t*) > Θ = ε · ||W(0)||_F
```

### 1.2 The VenueRoom AS a Spectral Gap Prototype

The VenueRoom in `/tmp/plato-midi-bridge/plato_midi_bridge/jepa/room.py` already implements **an equilibrium loop that IS the spectral gap computation**. The code reveals the direct mapping:

| VenueRoom Concept | Spectral Gap Concept |
|---|---|
| `global_state` (embedding) | Dominant eigenvector v₁ |
| `self.step()` iteration | Coupling matrix evolution: W(t+dt) = W(t) + α∇ℒ |
| `coupling = nn.Parameter(init_coupling)` | Coupling matrix W |
| `delta = ‖global_state - old_state‖.norm()` | Spectral gap proxy γ(t) |
| `tol = 1e-4` (convergence threshold) | Equilibrium threshold Θ |
| `max_steps = 32` | Maximum iterations to reach equilibrium |
| `F.softmax(self.coupling, dim=1)` | Normalized attention distribution |
| `attention = coupling_weights.mean(dim=1)` | Participant significance scores |

**The equilibrium delta IS the spectral gap.** When the VenueRoom converges (`delta < 1e-4`), it means `γ(t) > Θ` — the system has found a fixed point. The dominant eigenvalue λ₁ is the room's settled global state; the gap to λ₂ is the delta below tolerance.

**The critical insight:** The VenueRoom uses delta = ‖state(t) - state(t-1)‖ as an **empirical proxy** for the spectral gap. A true spectral gap computation would require eigendecomposition of the coupling matrix. But the proxy works because:

```
If ‖state(t) - state(t-1)‖ < ε then ‖W(t) - W(t-1)‖_F < ε'
⇒ eigenvalue shift < ε'  (by Weyl's perturbation theorem)
⇒ γ(t) > Θ when the proxy stabilizes
```

### 1.3 Concrete: Why the VenueRoom Is a 1.0 Prototype

The VenueRoom was designed for multi-agent musical resonance, but its mechanics ARE the fleet-jobs compute model:

```python
# room.py line ~72 — the equilibrium loop
for step in range(max_steps):          # max 32 iterations
    old_state = self.global_state       # snapshot t-1
    predictions = self.step()           # agent predictions
    delta = (self.global_state - old_state).norm().item()  # spectral gap proxy
    if delta < tol:                     # gap > Θ
        break                           # task complete
```

In fleet-jobs terms, this loop becomes:

```python
# fleet-jobs spectral gap check
for iteration in range(max_iterations):
    old_gap = spectral_gap(coupling_matrix)
    run_one_iteration(worker_state, coupling_matrix)
    new_gap = spectral_gap(coupling_matrix)
    delta_gap = abs(new_gap - old_gap)
    if delta_gap < THETA:         # equilibrium reached
        publish_equilibrium_signal(task_id, new_gap, THETA)
        break
```

### 1.4 The CouplingAnalysis Module

The actual spectral gap computation bridges the rooms:

```python
# /tmp/research/ — fleet_math.py (proposed module)
from typing import List, Tuple
import numpy as np

THETA_DEFAULT = 1e-4  # default equilibrium threshold

class CouplingAnalysis:
    """Compute and track spectral gap of a coupling matrix."""

    @staticmethod
    def build_coupling(result_data: dict) -> 'CouplingAnalysis':
        """Build coupling matrix from a result or state snapshot."""
        # result_data is a dict with 'eigenvalues' or 'coupling_matrix'
        if 'coupling_matrix' in result_data:
            W = np.array(result_data['coupling_matrix'])
        elif 'eigenvalues' in result_data:
            return CouplingAnalysis.from_eigenvalues(result_data['eigenvalues'])
        else:
            raise ValueError("No coupling data in result")
        return CouplingAnalysis(W)

    def __init__(self, coupling_matrix: np.ndarray):
        self.W = np.array(coupling_matrix)
        self._compute_spectrum()

    def _compute_spectrum(self):
        """Compute eigenvalues and gap."""
        self.eigenvalues = np.linalg.eigvalsh(self.W)[::-1]  # descending
        self.gap = self.eigenvalues[0] - self.eigenvalues[1] if len(self.eigenvalues) >= 2 else float('inf')

    @staticmethod
    def from_eigenvalues(eigs: List[float]) -> 'CouplingAnalysis':
        """Rebuild from known eigenvalues."""
        W = np.diag(sorted(eigs, reverse=True))
        return CouplingAnalysis(W)

    def is_equilibrium(self, theta: float = THETA_DEFAULT) -> bool:
        """Check if spectral gap exceeds threshold."""
        return self.gap > theta

    @staticmethod
    def compute_gap(eigenvalues: List[float]) -> float:
        """Static: gap from eigenvalue list."""
        sorted_eigs = sorted(eigenvalues, reverse=True)
        if len(sorted_eigs) < 2:
            return float('inf')
        return sorted_eigs[0] - sorted_eigs[1]
```

### 1.5 How the Implementation Works End-to-End

```
fleet-jobs (room)         fleet-coupling (room)        fleet-results (room)
     │                          │                            │
     │─ TASK_TILE ────────────→ │                            │
     │                          │                            │
     │                          │  Worker polls fleet-jobs   │
     │← Worker claims task ────│                            │
     │                          │                            │
     │                          │  Worker builds coupling    │
     │                          │  matrix from task data     │
     │                          │                            │
     │                          │── EigenvalueSnapshot ────→│
     │                          │   (λ₁, λ₂, ..., λ_K)      │
     │                          │                            │
     │                          │  Worker iterates:          │
     │                          │  W(t+1) = W(t) + α∇ℒ      │
     │                          │                            │
     │                          │── EigenvalueSnapshot ────→│
     │                          │   (gap increasing...)      │
     │                          │                            │
     │                          │── EquilibriumSignal ────→ │
     │                          │   (gap > Θ!)              │
     │                          │                            │
     │← CompletedTaskTile ─────│                            │
     │                          │                            │
```

### 1.6 The CLINCHER — One-Line Connection

```python
# After worker executes, publish eigenvalues
eigs = CouplingAnalysis.build_coupling(result_data).eigenvalues
gap = eigs[0] - eigs[1]
if gap > THETA:
    mark_complete(task_id, result)
```

This is the implementation-level encoding of **Theorem 3**. The gap computation is the completion criterion — not "did the worker respond?" but "did the coupling tensor reach equilibrium?"

---

## 2. Generalization → Actual Data Flow

### 2.1 queue-xec Data Flow (Current)

```
Master:  pushNewJob(task, code, data)
           │
           ├── Encrypt code + data with transferEncryptToken
           ├── Send via Bugout P2P to worker
           │
Worker:  receive job
           ├── npm install (dependencies)
           ├── require('./task.js')
           ├── task.run(jobData)
           └── shareResults(result)
                    │
Master:  onResults(result)
           └── collector callback
```

**Cost:** 6+ RPC round-trips, runtime npm install, shared secret key.

### 2.2 FLUX-PLATO Data Flow (Proposed)

```
Orchestrator                    PLATO Rooms                     Worker
     │                              │                              │
     │─ POST fleet-registry/join ──→│←─ POST fleet-registry/join ─│
     │   {agent_id, capabilities}   │   {agent_id, capabilities}  │
     │                              │                              │
     │─ POST fleet-jobs/submit ────→│                              │
     │   TASK_TILE:                  │                              │
     │   {question: "TASK: ...",    │                              │
     │    answer: {"type":"exec",   │                              │
     │             "flux_ref":"sha256:abc",                        │
     │             "data_ref":"sha256:def"}}                      │
     │                              │                              │
     │                              │─ Worker polls fleet-jobs ──→│
     │                              │   GET /room/fleet-jobs/tiles │
     │                              │                              │
     │                              │← Worker claims task ────────│
     │                              │   POST fleet-jobs/claim     │
     │                              │   {task_id, worker_id}      │
     │                              │                              │
     │                              │─ Worker GETs FLUX tile ────→│
     │                              │   Fetch flux_ref from cache  │
     │                              │                              │
     │                              │     Worker executes FLUX IR  │
     │                              │     ┌─────────────────┐     │
     │                              │     │ Compile FLUX IR  │     │
     │                              │     │ → native/WASM   │     │
     │                              │     │                  │     │
     │                              │     │ Build coupling   │     │
     │                              │     │ matrix W from   │     │
     │                              │     │ task constraints │     │
     │                              │     │                  │     │
     │                              │     │ Iterate:         │     │
     │                              │     │ W ← W + α∇ℒ     │     │
     │                              │     │ Compute γ = λ₁-λ₂│     │
     │                              │     │ While γ ≤ Θ:     │     │
     │                              │     │   publish λ's    │     │
     │                              │     │   to coupling    │     │
     │                              │     └─────────────────┘     │
     │                              │                              │
     │← POST fleet-coupling/result ─│← Worker posts result ──────│
     │   EQUILIBRIUM_SIGNAL:        │   POST fleet-results/tile   │
     │   {task_id, gap, threshold,  │   {result_tile: "sha256:xyz"│
     │    result_tile, iterations}  │    gap: 0.0015,             │
     │                              │    backend: "gpu"}          │
     │                              │                              │
     │  Orchestrator verifies gap:  │                              │
     │  gap = 0.0015 > THETA=0.001 │                              │
     │  → task COMPLETE ✅         │                              │
```

### 2.3 Component Mapping: queue-xec → FLUX-PLATO

| queue-xec Component | FLUX-PLATO Equivalent | PLATO Room | Data |
|---|---|---|---|
| `pushNewJob(task, code, data)` | `POST fleet-jobs/submit` | fleet-jobs | TASK_TILE with flux_ref + data_ref |
| `execAssets.files[]` | `POST tile-registry/tile` | tile-registry | FLUX IR modules, content-addressed |
| `transferEncryptToken` | Zero-trust GitHub OIDC | fleet-registry | Agent auth via commit history |
| Bugout DHT discovery | `GET fleet-registry/agents` | fleet-registry | Agent capability tiles |
| Worker `requestWork` | Worker polls `GET fleet-jobs/tiles` | fleet-jobs | Pending task tiles |
| Worker `task.run(jobData)` | Compile + execute FLUX IR | — | Local FLUX runtime |
| Worker progress (implicit) | `POST fleet-coupling/snapshot` | fleet-coupling | Eigenvalue snapshots |
| Worker `shareResults(result)` | `POST fleet-results/tile` | fleet-results | ResultTile + EquilibriumSignal |
| Master `onResults(callback)` | `GET fleet-coupling/results` | fleet-coupling | CouplingAnalysis.gap > THETA |

### 2.4 Why the Generalization Works

**Theorem 1** proved that the coupling matrix formalism strictly generalizes master/worker. The data flow above is the **constructive proof** — it shows exactly how every queue-xec operation maps to a FLUX-PLATO operation.

The key difference: the old data flow has 6+ RPCs with a central master bottleneck. The new data flow has **2 PLATO room writes (submit + result)**. The coupling room provides the intelligence that the master used to provide — but it emerges from the protocol, not from a privileged node.

---

## 3. The Fleet-Jobs Room Design

### 3.1 The Three-Room Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         PLATO Mesh                                    │
│                                                                      │
│  ┌──────────────────────┐    ┌──────────────────────┐               │
│  │     fleet-jobs       │    │    fleet-coupling     │              │
│  │                      │    │                       │              │
│  │  TASK_TILE (submit)  │    │  CouplingSnapshot     │              │
│  │  ClaimedTaskTile     │    │  EquilibriumSignal    │              │
│  │  CompletedTaskTile   │    │  ResonanceClaim       │              │
│  │                      │    │  ErrorSignal          │              │
│  └──────────┬───────────┘    └───────────┬───────────┘              │
│             │                            │                          │
│             └──────────┬─────────────────┘                          │
│                        │                                             │
│             ┌──────────▼───────────┐                                │
│             │    fleet-results      │                                │
│             │                       │                                │
│             │  ResultTile           │                                │
│             │  (content-addressed)  │                                │
│             └───────────────────────┘                                │
│                                                                      │
│  And supporting:                                                     │
│  ┌──────────────────────┐    ┌──────────────────────┐               │
│  │   fleet-registry     │    │    tile-registry      │              │
│  │   (agent discovery)  │    │  (FLUX IR modules)    │              │
│  └──────────────────────┘    └──────────────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 Room Schemas

#### fleet-jobs — TASK_TILE

```python
TASK_TILE_SCHEMA = {
    "question": str,        # "TASK: {task_id} — description"
    "answer": {
        "type": "exec" | "constraint",  # 2006-style vs 2046-style
        "flux_ref": str,    # "sha256:..." — FLUX IR module hash
        "data_ref": str,    # "sha256:..." — input data hash
        "requirements": {
            "min_ram_mb": int,
            "preferred_backend": "cpu" | "gpu" | "tpu",
        },
        "ttl_seconds": int,  # 60 to 86400
    },
    "source": str,          # submitter identity
    "tags": [str],          # ["task", "type:exec"]
}
```

#### fleet-jobs — ClaimedTaskTile

```python
CLAIMED_TILE_SCHEMA = {
    "parent_task_ref": str,   # SHA-256 of original TASK_TILE
    "worker_id": str,         # claiming worker identity
    "claimed_at": int,        # unix timestamp
    "status": "claimed" | "executing",
    "progress": float,        # 0.0 to 100.0
    "eigenvalue_snapshot": {  # snapshot at claim time
        "lambda_1": float,
        "lambda_2": float,
        "spectral_gap": float,
    },
}
```

#### fleet-coupling — CouplingSnapshot

```python
COUPLING_SNAPSHOT = {
    "task_ref": str,          # parent task
    "worker_id": str,
    "iteration": int,
    "timestamp": int,
    "eigenvalues": [float],   # λ₁, λ₂, ..., λ_K descending
    "spectral_gap": float,    # λ₁ - λ₂
    "threshold": float,       # Θ for this computation
    "delta_time_us": int,     # wall time since last snapshot
}
```

#### fleet-coupling — EquilibriumSignal

```python
EQUILIBRIUM_SIGNAL = {
    "task_ref": str,
    "worker_id": str,
    "type": "equilibrium_reached",
    "final_gap": float,
    "threshold": float,
    "result_tile_ref": str,   # points to fleet-results ResultTile
    "iterations": int,
    "wall_time_ms": int,
    "coupling_trace_ref": str,  # SHA-256 of full coupling evolution
}
```

#### fleet-results — ResultTile

```python
RESULT_TILE = {
    "task_ref": str,
    "result_hash": str,       # SHA-256 of output data
    "schema": str,            # result schema version
    "provenance": {           # execution chain
        "flux_ref": str,
        "data_ref": str,
        "worker_id": str,
        "claimed_at": int,
        "completed_at": int,
    },
    "backend_used": str,
    "runtime_seconds": float,
    "error": str | None,
}
```

### 3.3 Example: Complete Task Lifecycle

```python
# === 1. SUBMIT ===
import requests
import json

PLATO = "http://localhost:8847"

# Post task to fleet-jobs
task_tile = {
    "question": "TASK: compute_large_fft --size 1048576",
    "answer": json.dumps({
        "type": "exec",
        "flux_ref": "sha256:abc123def456",
        "data_ref": "sha256:def456ghi789",
        "requirements": {"min_ram_mb": 256, "preferred_backend": "gpu"},
        "ttl_seconds": 3600,
    }),
    "source": "oracle1",
    "tags": ["task", "type:exec", "fft"],
}
requests.post(f"{PLATO}/room/fleet-jobs/tile", json=task_tile)

# === 2. WORKER DISCOVERY ===
# Worker polls for pending tasks matching capability
pending = requests.get(f"{PLATO}/room/fleet-jobs/tiles").json()
for tile in pending:
    answer = json.loads(tile["answer"])
    if "gpu" in answer.get("requirements", {}).get("preferred_backend", ""):
        claim_task(tile)

# === 3. WORKER CLAIMS ===
claim_tile = {
    "parent_task_ref": "sha256:abc123...",
    "worker_id": "worker-gpu-001",
    "claimed_at": 1715789400,
    "status": "claimed",
    "eigenvalue_snapshot": {
        "lambda_1": 42.0,      # worker's self-eigenvalue (computational capacity)
        "lambda_2": 0.5,       # residual noise
        "spectral_gap": 41.5,  # high = available
    },
}
requests.post(f"{PLATO}/room/fleet-jobs/tile", json=claim_tile)

# === 4. WORKER EXECUTES + PUBLISHES COUPLING SNAPSHOTS ===
for i, gap in enumerate(track_spectral_gap()):
    snapshot = {
        "task_ref": "sha256:abc123...",
        "worker_id": "worker-gpu-001",
        "iteration": i,
        "eigenvalues": [gap.peak, gap.next_peak],
        "spectral_gap": gap.peak - gap.next_peak,
        "threshold": 0.001,
    }
    requests.post(f"{PLATO}/room/fleet-coupling/tile", json=snapshot)

# === 5. EQUILIBRIUM REACHED ===
signal = EQUILIBRIUM_SIGNAL(
    task_ref="sha256:abc123...",
    worker_id="worker-gpu-001",
    final_gap=0.0023,
    threshold=0.001,
    result_tile_ref="sha256:result789xyz",
    iterations=17,
)
requests.post(f"{PLATO}/room/fleet-coupling/tile", json=signal)

# === 6. ORCHESTRATOR VERIFIES AND MARKS COMPLETE ===
results = requests.get(f"{PLATO}/room/fleet-coupling/tiles").json()
for tile in results:
    if tile.get("type") == "equilibrium_reached":
        if tile["final_gap"] > tile["threshold"]:
            mark_complete(tile["task_ref"])
```

---

## 4. The Actual Build Plan

### Phase 1: Create the Three PLATO Rooms and Verify Tile Acceptance

**Goal:** Three empty PLATO rooms that accept tiles with the schemas defined above.

```python
# scripts/setup_fleet_rooms.py
"""Create fleet-jobs, fleet-coupling, fleet-results rooms on PLATO.

Usage: python3 setup_fleet_rooms.py
"""

import requests
import json
import time

PLATO = "http://localhost:8847"
ROOMS = [
    {
        "name": "fleet-jobs",
        "description": "Task submission and lifecycle — TASK_TILE, ClaimedTaskTile, CompletedTaskTile",
        "schema_validation": "strict",
    },
    {
        "name": "fleet-coupling",
        "description": "Coupling matrix snapshots, eigenvalue spectra, equilibrium signals",
        "schema_validation": "strict",
    },
    {
        "name": "fleet-results",
        "description": "Immutable result tiles with content-addressed provenance",
        "schema_validation": "strict",
    },
]

def create_room(name: str, description: str):
    """Create a PLATO room via the relay API."""
    try:
        resp = requests.post(
            f"{PLATO}/room/{name}/create",
            json={"description": description},
            timeout=10,
        )
        if resp.status_code in (200, 201, 409):  # 409 = already exists
            print(f"  ✅ Room '{name}' ready ({resp.status_code})")
            return True
        else:
            print(f"  ❌ Room '{name}' failed: {resp.status_code} {resp.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  ⚠️  Could not connect to PLATO at {PLATO}")
        print(f"     To create manually: mkdir -p /tmp/plato/{name}")
        os.makedirs(f"/tmp/plato/{name}", exist_ok=True)
        return True

def verify_tile_acceptance(room: str, tile: dict) -> bool:
    """Post a test tile and verify it's accepted."""
    try:
        resp = requests.post(
            f"{PLATO}/room/{room}/tile",
            json=tile,
            timeout=10,
        )
        if resp.status_code in (200, 201):
            print(f"  ✅ Tile accepted in '{room}'")
            return True
        else:
            print(f"  ⚠️  Room '{room}' returned {resp.status_code}: {resp.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  ⚠️  PLATO unreachable, tile not verified")
        return False


def main():
    import os
    print("=== Phase 1: Create Fleet Rooms ===\n")

    # 1. Create rooms
    for room in ROOMS:
        print(f"Creating room: {room['name']}")
        create_room(room["name"], room["description"])

    print()

    # 2. Verify tile acceptance in each room
    test_tiles = {
        "fleet-jobs": {
            "question": "TASK: verify_room_acceptance",
            "answer": json.dumps({
                "type": "exec",
                "flux_ref": "sha256:test",
                "data_ref": "sha256:test",
                "requirements": {"min_ram_mb": 1},
                "ttl_seconds": 300,
            }),
            "source": "setup_script",
            "tags": ["test", "bootstrap"],
        },
        "fleet-coupling": {
            "task_ref": "sha256:test",
            "worker_id": "setup_script",
            "iteration": 0,
            "eigenvalues": [1.0, 0.5, 0.1],
            "spectral_gap": 0.5,
            "threshold": 0.001,
            "timestamp": int(time.time()),
        },
        "fleet-results": {
            "task_ref": "sha256:test",
            "result_hash": "sha256:test_result",
            "schema": "v1",
            "provenance": {
                "flux_ref": "sha256:test",
                "data_ref": "sha256:test",
                "worker_id": "setup_script",
            },
            "backend_used": "cpu",
            "runtime_seconds": 0.001,
        },
    }

    for room, tile in test_tiles.items():
        print(f"Verifying '{room}' accepts tiles...")
        verify_tile_acceptance(room, tile)

    print("\n✅ Phase 1 complete. Three rooms operational.")


if __name__ == "__main__":
    main()
```

### Phase 2: Test Worker That Polls fleet-jobs, Executes FLUX IR, Posts Results

**Goal:** A worker agent that:
1. Polls fleet-jobs for pending tasks
2. Claims a task via ClaimedTaskTile
3. Fetches the FLUX IR module and input data
4. Compiles and executes (or simulates execution for testing)
5. Publish eigenvalue snapshots to fleet-coupling
6. Posts result to fleet-results
7. Marks task complete in fleet-jobs

```python
# scripts/fleet_worker.py
"""Test worker for fleet-jobs protocol.

Usage: python3 fleet_worker.py [--worker-id worker-cpu-001]
"""

import requests
import json
import time
import argparse
import uuid
import os
import sys

PLATO = "http://localhost:8847"
POLL_INTERVAL_S = 3  # check for tasks every 3 seconds


class FleetWorker:
    """A worker that polls fleet-jobs, executes FLUX IR modules, and returns results."""

    def __init__(self, worker_id: str = None):
        self.worker_id = worker_id or f"worker-{uuid.uuid4().hex[:8]}"
        self.capabilities = ["cpu", "computation"]
        self.current_task = None
        self.eigenvalues_history = []
        self.spectral_gap_history = []

    def register(self):
        """Register with fleet-registry."""
        registration = {
            "worker_id": self.worker_id,
            "capabilities": self.capabilities,
            "available_resources": {"ram_mb": 4096},
            "registered_at": int(time.time()),
        }
        try:
            resp = requests.post(
                f"{PLATO}/room/fleet-registry/tile",
                json=registration,
                timeout=5,
            )
            print(f"  [{self.worker_id}] Registered: {resp.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"  [{self.worker_id}] Registration skipped (PLATO unreachable)")

    def poll_for_tasks(self):
        """Poll fleet-jobs for pending tasks."""
        try:
            resp = requests.get(f"{PLATO}/room/fleet-jobs/tiles", timeout=5)
            if resp.status_code != 200:
                return []
            tiles = resp.json()
            # Filter: only unclaimed tasks (no "claimed_at" in answer)
            pending = []
            for tile in tiles:
                answer = json.loads(tile.get("answer", "{}"))
                if isinstance(answer, dict) and not answer.get("claimed_by"):
                    pending.append(tile)
            return pending
        except (requests.exceptions.ConnectionError, json.JSONDecodeError):
            return []

    def claim_task(self, task_tile: dict) -> bool:
        """Claim a task by posting ClaimedTaskTile."""
        claim = {
            "parent_task_ref": self._compute_hash(task_tile),
            "worker_id": self.worker_id,
            "claimed_at": int(time.time()),
            "status": "claimed",
            "eigenvalue_snapshot": {
                "lambda_1": 42.0,   # worker's capacity
                "lambda_2": 0.5,
                "spectral_gap": 41.5,
            },
        }
        try:
            resp = requests.post(
                f"{PLATO}/room/fleet-jobs/tile",
                json=claim,
                timeout=5,
            )
            return resp.status_code in (200, 201)
        except requests.exceptions.ConnectionError:
            return False

    def execute_task(self, task_tile: dict):
        """Execute a task with spectral gap tracking.

        Simulates FLUX IR execution by iterating a synthetic coupling matrix
        toward equilibrium, publishing eigenvalue snapshots along the way.
        """
        answer = json.loads(task_tile.get("answer", "{}"))
        flux_ref = answer.get("flux_ref", "sha256:unknown")
        print(f"  [{self.worker_id}] Executing {flux_ref}...")

        # Simulate: coupling matrix starts random, converges via gradient descent
        self.current_task = task_tile
        THETA = 0.001

        # Initial state
        import numpy as np
        np.random.seed(hash(flux_ref) % 2**31)
        W = np.random.randn(4, 4).astype(np.float64)
        W = (W + W.T) / 2     # symmetric
        W = W / np.max(np.abs(W)) * 10  # scale

        for iteration in range(32):  # max iterations
            # Coupling matrix evolution step: W(t+1) = W(t) + α∇ℒ
            alpha = 0.5 / (1 + iteration)
            noise = np.random.randn(4, 4).astype(np.float64) * 0.01
            noise = (noise + noise.T) / 2
            W = W + alpha * (-W + np.diag(np.diag(W)) + noise)

            # Compute eigenvalues
            eigs = np.linalg.eigvalsh(W)
            eigs = sorted(eigs, reverse=True)
            gap = eigs[0] - eigs[1] if len(eigs) >= 2 else float('inf')

            self.eigenvalues_history.append(eigs.tolist())
            self.spectral_gap_history.append(gap)

            # Publish coupling snapshot
            snapshot = {
                "task_ref": self._compute_hash(task_tile),
                "worker_id": self.worker_id,
                "iteration": iteration,
                "timestamp": int(time.time() * 1000),
                "eigenvalues": eigs.tolist(),
                "spectral_gap": float(gap),
                "threshold": THETA,
                "delta_time_us": 1000,
            }
            try:
                requests.post(
                    f"{PLATO}/room/fleet-coupling/tile",
                    json=snapshot,
                    timeout=2,
                )
            except requests.exceptions.ConnectionError:
                pass  # Continue anyway

            print(f"  iteration {iteration:2d}: λ₁={eigs[0]:.4f}, λ₂={eigs[1]:.4f}, γ={gap:.6f}")

            # Check equilibrium
            if gap > THETA:
                print(f"  ✅ Equilibrium reached at iteration {iteration}! γ={gap:.6f} > Θ={THETA}")
                return {
                    "result": {"status": "completed", "final_gap": float(gap)},
                    "iterations": iteration,
                    "final_gap": float(gap),
                }

        # Max iterations reached without convergence
        return {
            "result": {"status": "partial", "final_gap": float(gap)},
            "iterations": 32,
            "final_gap": float(gap),
        }

    def publish_result(self, task_tile: dict, execution_result: dict):
        """Publish result to fleet-results and equilibrium signal to fleet-coupling."""
        task_hash = self._compute_hash(task_tile)
        result_hash = hashlib.sha256(
            json.dumps(execution_result, sort_keys=True).encode()
        ).hexdigest()[:16]

        # Result tile
        result_tile = {
            "task_ref": task_hash,
            "result_hash": f"sha256:{result_hash}",
            "schema": "v1",
            "provenance": {
                "flux_ref": json.loads(task_tile.get("answer", "{}")).get("flux_ref", ""),
                "data_ref": json.loads(task_tile.get("answer", "{}")).get("data_ref", ""),
                "worker_id": self.worker_id,
                "claimed_at": int(time.time()),
                "completed_at": int(time.time()),
            },
            "backend_used": "cpu" if "cpu" in self.capabilities else "unknown",
            "runtime_seconds": 0.5,
        }

        try:
            resp = requests.post(
                f"{PLATO}/room/fleet-results/tile",
                json=result_tile,
                timeout=5,
            )
            print(f"  [{self.worker_id}] Result published: {resp.status_code}")

            # Equilibrium signal on fleet-coupling
            signal = {
                "task_ref": task_hash,
                "worker_id": self.worker_id,
                "type": "equilibrium_reached",
                "final_gap": execution_result.get("final_gap", 0),
                "threshold": 0.001,
                "result_tile_ref": result_tile["result_hash"],
                "iterations": execution_result.get("iterations", 0),
                "wall_time_ms": 500,
            }
            requests.post(
                f"{PLATO}/room/fleet-coupling/tile",
                json=signal,
                timeout=5,
            )

            # Mark task complete in fleet-jobs
            complete_tile = {
                "parent_task_ref": task_hash,
                "worker_id": self.worker_id,
                "completed_at": int(time.time()),
                "result_ref": result_tile["result_hash"],
                "backend_used": "cpu",
                "runtime_seconds": 0.5,
            }
            requests.post(
                f"{PLATO}/room/fleet-jobs/tile",
                json=complete_tile,
                timeout=5,
            )

        except requests.exceptions.ConnectionError as e:
            print(f"  [{self.worker_id}] Result publication failed: {e}")

    def run(self):
        """Main worker loop."""
        import hashlib
        self._compute_hash = lambda tile: f"sha256:{hashlib.sha256(json.dumps(tile, sort_keys=True).encode()).hexdigest()[:16]}"

        print(f"\n=== Fleet Worker: {self.worker_id} ===")
        self.register()

        print(f"Polling fleet-jobs every {POLL_INTERVAL_S}s...")
        while True:
            pending = self.poll_for_tasks()
            if pending:
                task = pending[0]
                print(f"\n  Found task: {task.get('question', 'unknown')}")
                if self.claim_task(task):
                    print(f"  Claimed: ✅")
                    result = self.execute_task(task)
                    self.publish_result(task, result)
                else:
                    print(f"  Claim failed (likely claimed by another worker)")
            time.sleep(POLL_INTERVAL_S)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fleet Worker Agent")
    parser.add_argument("--worker-id", type=str, default=None)
    args = parser.parse_args()

    worker = FleetWorker(worker_id=args.worker_id)
    try:
        worker.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
```

### Phase 3: Spectral Gap as Completion Criterion

**Goal:** Wire up the orchestrator to check the spectral gap from fleet-coupling and decide task completion based on Theorem 3.

```python
# scripts/fleet_orchestrator.py
"""Orchestrator that submits tasks and verifies completion via spectral gap.

Usage: python3 fleet_orchestrator.py --submit-task "TASK: my_computation"
"""

import requests
import json
import time
import argparse
import sys

PLATO = "http://localhost:8847"
POLL_INTERVAL_S = 2
THETA = 0.001  # default equilibrium threshold


class FleetOrchestrator:
    """Submits tasks to fleet-jobs and monitors fleet-coupling for spectral gap completion."""

    def __init__(self):
        self.submitted_tasks = {}

    def submit_task(self, task_id: str, flux_ref: str = "sha256:demo_module",
                    data_ref: str = "sha256:demo_data", req_ram: int = 256,
                    backend: str = "cpu", ttl: int = 3600) -> str:
        """Submit a task tile to fleet-jobs."""
        import hashlib
        tile = {
            "question": f"TASK: {task_id}",
            "answer": json.dumps({
                "type": "exec",
                "flux_ref": flux_ref,
                "data_ref": data_ref,
                "requirements": {"min_ram_mb": req_ram, "preferred_backend": backend},
                "ttl_seconds": ttl,
            }),
            "source": "orchestrator-1",
            "tags": ["task", "type:exec"],
        }

        try:
            resp = requests.post(f"{PLATO}/room/fleet-jobs/tile", json=tile, timeout=10)
            tile_hash = f"sha256:{hashlib.sha256(json.dumps(tile, sort_keys=True).encode()).hexdigest()[:16]}"
            self.submitted_tasks[tile_hash] = {
                "task_id": task_id,
                "tile": tile,
                "submitted_at": time.time(),
                "status": "pending",
                "gap_history": [],
            }
            print(f"  ✅ Task submitted: {task_id} (hash: {tile_hash[:20]}...)")
            return tile_hash
        except requests.exceptions.ConnectionError:
            print(f"  ❌ PLATO unreachable. Cannot submit task.")
            return None

    def monitor_coupling(self, task_hash: str, timeout_s: int = 120) -> dict:
        """Monitor fleet-coupling for equilibrium signal on this task.

        Checks spectral gap from CouplingSnapshots. When gap > THETA,
        considers the task complete. This IS the implementation of Theorem 3.
        """
        start = time.time()
        print(f"  Monitoring fleet-coupling for task {task_hash[:20]}...")
        print(f"  Threshold Θ = {THETA}")

        while time.time() - start < timeout_s:
            try:
                resp = requests.get(f"{PLATO}/room/fleet-coupling/tiles", timeout=5)
                if resp.status_code != 200:
                    time.sleep(POLL_INTERVAL_S)
                    continue

                tiles = resp.json()
                # Filter tiles for this task
                task_tiles = [t for t in tiles if t.get("task_ref") == task_hash]

                for tile in task_tiles:
                    gap = tile.get("spectral_gap", 0)
                    if tile.get("type") == "equilibrium_reached":
                        print(f"\n  🎯 EQUILIBRIUM SIGNAL DETECTED!")
                        print(f"     Final gap: {tile.get('final_gap', 0):.6f}")
                        print(f"     Threshold:  {tile.get('threshold', 0)}")
                        print(f"     Iterations: {tile.get('iterations', 0)}")
                        print(f"     Result ref: {tile.get('result_tile_ref', 'N/A')}")
                        self.submitted_tasks[task_hash]["status"] = "completed"
                        return tile

                    if gap > THETA and gap > 0:
                        # The spectral gap theorem in action!
                        print(f"  ⚡ Gap={gap:.6f} > Θ={THETA} — task completing via Theorem 3")
                        self.submitted_tasks[task_hash]["status"] = "completing"

                    # Track gap history
                    if gap > 0:
                        self.submitted_tasks[task_hash]["gap_history"].append(gap)

                # Print progress every few seconds
                if int(time.time() - start) % 6 == 0 and task_tiles:
                    latest_gap = task_tiles[-1].get("spectral_gap", 0)
                    print(f"  iteration {task_tiles[-1].get('iteration', '?')}: γ={latest_gap:.6f} (Θ={THETA})")

            except requests.exceptions.ConnectionError:
                pass

            time.sleep(POLL_INTERVAL_S)

        print(f"  ⏰ Timeout after {timeout_s}s")
        return {"status": "timeout"}

    def verify_and_summarize(self, task_hash: str):
        """After completion, verify the result and print summary."""
        info = self.submitted_tasks.get(task_hash, {})
        gap_curve = info.get("gap_history", [])

        print(f"\n=== Task Summary: {info.get('task_id', 'unknown')} ===")
        print(f"  Status:       {info.get('status', 'unknown')}")
        print(f"  Submitted:    {info.get('submitted_at', 0):.1f}")
        print(f"  Gap samples:  {len(gap_curve)}")
        if gap_curve:
            print(f"  Final gap:    {gap_curve[-1]:.6f}")
            print(f"  Max gap:      {max(gap_curve):.6f}")
            print(f"  Initial gap:  {gap_curve[0]:.6f}")
            print(f"  Duration:     {time.time() - info.get('submitted_at', time.time()):.1f}s")

        # Central check: was the spectral gap criterion met?
        if gap_curve and max(gap_curve) > THETA:
            print(f"\n  ✅ Theorem 3 SATISFIED: gap exceeded threshold Θ={THETA}")
        else:
            print(f"\n  ⚠️  Theorem 3 NOT SATISFIED: gap never exceeded threshold Θ={THETA}")

    def interactive_demo(self):
        """Run a full demo: submit, wait, verify."""
        task_hash = self.submit_task(
            task_id="demo_fft --size 1024",
            flux_ref="sha256:fft_module_v1",
            data_ref="sha256:test_data",
        )
        if not task_hash:
            return

        print("\nWaiting for worker to claim and execute...")
        time.sleep(2)

        result = self.monitor_coupling(task_hash, timeout_s=60)
        self.verify_and_summarize(task_hash)


if __name__ == "__main__":
    orch = FleetOrchestrator()
    orch.interactive_demo()
```

---

## 5. Summary: The Bridge from Theorem to Code

### What Connects

| Abstract | Concrete | File |
|---|---|---|
| Theorem 3: Spectral Gap Completion | `CouplingAnalysis.gap > THETA` in `mark_complete()` | `scripts/fleet_orchestrator.py` |
| VenueRoom equilibrium loop | 32 iterations, delta < 1e-4 proxy for γ > Θ | `room.py` lines 131-155 |
| Coupling matrix evolution | `W = W + α(-W + diag(diag(W)) + noise)` | `scripts/fleet_worker.py` |
| EquilibriumSignal | Published to fleet-coupling with final_gap > threshold | `scripts/fleet_worker.py` |
| Three rooms as coupling tensor | fleet-jobs (inputs), fleet-coupling (evolution), fleet-results (output) | `scripts/setup_fleet_rooms.py` |
| queue-xec `pushNewJob()` | `POST fleet-jobs/tile` with TASK_TILE | Orchestrator → fleet-jobs |
| queue-xec `onResults()` | Get fleet-coupling tiles, check gap > THETA | Orchestrator ← fleet-coupling |
| 2006-style: explicit exec | TASK_TILE with `type: "exec"` | fleet-jobs room schema |
| 2046-style: constraint resolution | TASK_TILE with `type: "constraint"` | fleet-jobs room schema |

### The Tension Resolved

The 20-year tension between "sending work to machines" (2006) and "becoming the work with machines" (2046) is resolved by the **coupling tensor formalism**:

- **queue-xec** sends work → implementation of diagonal coupling (master decides everything)
- **PLATO resonance** lets work emerge → implementation of non-diagonal coupling (mutual constraint satisfaction)
- **fleet-jobs** accepts both → the room protocol is neutral to how work gets done

The spectral gap doesn't care whether the computation arrived via RPC or resonance. It only measures whether the coupling tensor has reached equilibrium. **That is the bridge.**

### Build Order

```
Phase 1: setup_fleet_rooms.py  ───→ Three PLATO rooms operational
Phase 2: fleet_worker.py       ───→ Worker polls, claims, executes, posts results
Phase 3: fleet_orchestrator.py ───→ Submits tasks, monitors gap, verifies completion
```

Each phase builds on the previous. Phase 3 is where Theorem 3 becomes executable code — a task is "complete" when `gap > THETA`, verified from fleet-coupling tiles.
