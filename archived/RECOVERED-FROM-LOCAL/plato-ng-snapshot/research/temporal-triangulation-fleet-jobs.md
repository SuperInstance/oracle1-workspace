# Temporal Triangulation Fleet-Jobs PLATO Room Design Document
## Version 1.0
**Date:** 2026-05-14
**Author:** Subagent Study Team: Temporal Triangulation
**Target Audience:** PLATO Fleet Engineers, Worker Node Operators, Dashboard Developers

---

## 1. Executive Overview
This design document defines the fleet-jobs PLATO room, the missing compute layer bridging 1960s-era batch processing queues (exemplified by IBM System/360 queue-xec/master with JavaScript bindings) and 2076's self-replicating compute tiles that metamorphose via PLATO mesh contact. The fleet-jobs room provides a standardized, distributed task orchestration system for the PLATO ecosystem, enabling heterogeneous worker nodes to execute modular FLUX IR (Intermediate Representation) compute tasks, track execution progress, verify results, and expose real-time observability data via a spectral coupling layer.

### Core Use Cases
- Distributed large-scale Fast Fourier Transform (FFT) computations
- Computational physics simulations (spectral analysis, eigenvalue problems)
- Modular FLUX IR module execution across heterogeneous hardware
- Parallelized data processing pipelines for fleet-wide sensor data
- Incentivized compute markets for volunteer worker nodes

### Design Principles
1. **Content-Addressable:** All tasks, data, and results are referenced via SHA-256 hashes to ensure immutability and verifiable provenance
2. **Stateless Workers:** Worker nodes do not retain persistent state between tasks, enabling seamless failover and scaling
3. **Spectral Observability:** Execution progress is exposed via a coupling eigenvalue spectrum that provides real-time visibility into fleet health and task status
4. ** backwards Compatible:** Integrates with legacy queue-xec/master batch queues via a translation layer
5. **Future-Proof:** Designed to extend to self-replicating compute tiles with minimal modifications

---

## 2. Core Architecture & Terminology
### PLATO Room Primer
PLATO rooms are ephemeral, decentralized content spaces designed for asynchronous tile-based communication. Each room is identified by a unique SHA-256 hash of its configuration, and all tiles published to the room are immutable once committed. Tiles are structured JSON objects with strict schemas enforced by the room's validation layer. This design ensures that all communication within the fleet is auditable, verifiable, and resistant to tampering.

### Key Entities
| Entity | Description |
|--------|-------------|
| **Task Tile** | A unit of work to be executed, containing a reference to a FLUX IR module, input data, and execution requirements |
| **Claimed Task Tile** | A supersede of a pending Task Tile indicating that a worker has claimed exclusive execution rights |
| **Completed Task Tile** | A tile published by a worker after successful task execution, containing a reference to the result data |
| **Result Tile** | An immutable, content-addressed tile containing the final output of a completed task |
| **Eigenvalue Tile** | A tile published by workers during execution to report progress updates via spectral coupling data |
| **Worker Registration Tile** | A tile published by worker nodes to announce their capabilities and availability to the fleet |

---

## 3. Part 1: Fleet-Jobs Room Protocol
The fleet-jobs room is the central orchestration layer for all compute tasks in the PLATO fleet. It manages task lifecycle, worker claims, result verification, and expiration handling.

### 3.1 Tile Formats (JSON Schemas)
All tiles published to the fleet-jobs room must conform to the following JSON Schema specifications, validated using AJV (Another JSON Schema Validator) with strict mode enabled.

#### 3.1.1 Task Tile Schema
Task tiles are the primary unit of work submitted to the fleet-jobs room. They reference a FLUX IR module and input data via their content-addressed hashes, and define execution requirements and constraints.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TaskTile",
  "type": "object",
  "required": ["question", "answer", "source", "tags", "created_at", "ttl_seconds"],
  "properties": {
    "question": {
      "type": "string",
      "description": "Human-readable task description and execution command for the FLUX IR module",
      "pattern": "^TASK: [A-Z_]+( .+)?$"
    },
    "answer": {
      "type": "string",
      "description": "JSON-serialized object containing task references and requirements",
      "pattern": "^\\{.*\\}$"
    },
    "source": {
      "type": "string",
      "description": "Unique identifier of the task submitter (e.g. oracle1, fleet-sensor-pipeline)"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      },
      "description": "Array of tags for task discovery and filtering"
    },
    "created_at": {
      "type": "integer",
      "description": "Unix timestamp (seconds since epoch) when the task was created"
    },
    "ttl_seconds": {
      "type": "integer",
      "minimum": 60,
      "maximum": 86400,
      "description": "Time in seconds after which the task expires if unclaimed"
    },
    "expires_at": {
      "type": "integer",
      "description": "Computed Unix timestamp when the task will expire (created_at + ttl_seconds)"
    }
  },
  "additionalProperties": false
}
```

#### Example Task Tile
```json
{
  "question": "TASK: compute_large_fft --size 1048576",
  "answer": "{\"flux_module_ref\": \"sha256:abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567\", \"input_data_ref\": \"sha256:def456ghi789jkl012mno345pqr678stu901vwx234yz567abc123\", \"requirements\": {\"min_ram_mb\": 256, \"preferred_backend\": \"gpu\"}, \"reward\": \"1000 plato-tokens\"}",
  "source": "oracle1",
  "tags": ["computation", "fft", "distributed"],
  "created_at": 1715789400,
  "ttl_seconds": 3600,
  "expires_at": 1715793000
}
```

#### 3.1.2 Claimed Task Tile Schema
When a worker claims a task, it publishes a Claimed Task Tile, which supersedes the original pending Task Tile to reserve exclusive execution rights. The Claimed Task Tile includes the worker's unique identifier and a timestamp of the claim.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ClaimedTaskTile",
  "type": "object",
  "required": ["parent_task_ref", "worker_id", "claimed_at", "status"],
  "properties": {
    "parent_task_ref": {
      "type": "string",
      "description": "SHA-256 hash of the original Task Tile being claimed"
    },
    "worker_id": {
      "type": "string",
      "description": "Unique identifier of the claiming worker node"
    },
    "claimed_at": {
      "type": "integer",
      "description": "Unix timestamp when the task was claimed"
    },
    "status": {
      "type": "string",
      "enum": ["claimed", "executing"],
      "description": "Current state of the claimed task"
    },
    "progress": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "Percentage of task completed (0-100)"
    }
  },
  "additionalProperties": false
}
```

#### 3.1.3 Completed Task Tile Schema
After a worker completes execution, it publishes a Completed Task Tile to the fleet-jobs room, referencing the final Result Tile and including execution metadata such as backend used and runtime duration.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CompletedTaskTile",
  "type": "object",
  "required": ["parent_task_ref", "worker_id", "completed_at", "result_ref", "backend_used", "runtime_seconds"],
  "properties": {
    "parent_task_ref": {
      "type": "string",
      "description": "SHA-256 hash of the original Task Tile"
    },
    "worker_id": {
      "type": "string",
      "description": "Unique identifier of the worker that executed the task"
    },
    "completed_at": {
      "type": "integer",
      "description": "Unix timestamp when the task was completed"
    },
    "result_ref": {
      "type": "string",
      "description": "SHA-256 hash of the final Result Tile published to the fleet-results room"
    },
    "backend_used": {
      "type": "string",
      "enum": ["cpu", "gpu", "tpu", "embedded"],
      "description": "Hardware backend used for execution"
    },
    "runtime_seconds": {
      "type": "number",
      "minimum": 0,
      "description": "Total time taken to execute the task in seconds"
    },
    "error": {
      "type": "string",
      "description": "Error message if task execution failed (optional)"
    }
  },
  "additionalProperties": false
}
```

### 3.2 Task Lifecycle States
Tasks transition through a strict sequence of states as they move from submission to completion or expiration:

1. **Pending**: The initial state after a Task Tile is published to the fleet-jobs room. The task is available for workers to claim.
2. **Claimed**: A worker has reserved the task by publishing a Claimed Task Tile, superseding the pending Task Tile. No other workers can claim the task.
3. **Executing**: The worker has started execution and published an update marked as "executing". Progress updates may be published periodically.
4. **Complete**: The worker has finished execution and published a Completed Task Tile, referencing the final Result Tile.
5. **Verified**: A verification worker has validated the result's provenance and correctness, marking the task as fully completed.
6. **Expired**: The task's TTL has elapsed without being claimed, or it was manually retracted by the submitter.

#### State Transition Rules
- **Pending → Claimed**: An atomic operation where a worker publishes a Claimed Task Tile that supersedes the original pending Task Tile. The fleet-jobs room ensures only one worker can claim a task via optimistic locking.
- **Claimed → Executing**: The worker updates the Claimed Task Tile's status to "executing" and optionally includes a progress percentage.
- **Executing → Complete**: The worker publishes a Completed Task Tile with a reference to the result data.
- **Complete → Verified**: A verification node validates the result's hash against the published result_ref and updates the task state to "verified".
- **Any State → Expired**: If the task's ttl_seconds elapses without reaching the "Complete" state, the fleet-jobs room automatically retracts the task and marks it as expired.

### 3.3 Claim Mechanism
Workers discover tasks by polling the fleet-jobs room for pending Task Tiles matching their capabilities (e.g., GPU-enabled workers filter for tasks with `preferred_backend: gpu`). To claim a task, a worker must publish a Claimed Task Tile that references the original Task Tile's hash. The fleet-jobs room uses optimistic locking to ensure only one worker can successfully claim a task: if multiple workers attempt to claim the same task simultaneously, only the first publish will be accepted, and subsequent attempts will be rejected with a "task already claimed" error.

### 3.4 Progress Reporting
Workers can publish periodic updates to the fleet-jobs room to report task progress. Each update is a partial superset of the Claimed Task Tile, including the `status` set to "executing" and an optional `progress` percentage. These updates are stored in the fleet-jobs room's history and can be queried by dashboard developers to provide real-time progress tracking for individual tasks.

### 3.5 Result Verification
To ensure the integrity of task results, a separate verification layer validates each completed task:
1. The verification node retrieves the original Task Tile, the FLUX IR module, and the input data referenced by the task.
2. The verification node re-executes the FLUX IR module using the input data to generate a reference result.
3. The verification node compares the reference result's SHA-256 hash with the `result_ref` published in the Completed Task Tile.
4. If the hashes match, the verification node publishes a Verified Task Tile to the fleet-jobs room, updating the task state to "verified".
5. If the hashes do not match, the verification node marks the task as failed and publishes a new Completed Task Tile with an error message, triggering a retry (if configured) or marking the task as expired.

### 3.6 TTL & Expiration Handling
Each Task Tile includes a `ttl_seconds` field defining how long the task remains available for claiming. The fleet-jobs room automatically computes the `expires_at` timestamp as `created_at + ttl_seconds`. When the `expires_at` timestamp is reached, the following actions occur:
1. The fleet-jobs room removes all pending and claimed Task Tiles for the expired task.
2. A notification is published to the fleet-alerts room to notify the task submitter and relevant workers.
3. The task is marked as expired in the fleet-jobs room's history for auditing purposes.

Workers can also extend a task's TTL by publishing an updated Claimed Task Tile with a new `ttl_seconds` value, but only if the task is in the "claimed" or "executing" state. This is useful for long-running tasks that exceed the initial TTL.

---

## 4. Part 2: Worker Protocol Specification
Worker nodes are the execution layer of the PLATO fleet, responsible for discovering, claiming, and executing tasks from the fleet-jobs room. The worker protocol defines a standardized interface for all worker nodes, regardless of hardware or software stack.

### 4.1 Worker Registration
Before a worker can participate in the fleet, it must first register with the fleet-registry room by publishing a Worker Registration Tile. This tile includes the worker's unique identifier, hardware capabilities, supported task tags, and available resources. The fleet-registry room uses this data to route tasks to appropriate workers.

#### Example Worker Registration Tile
```json
{
  "worker_id": "worker-gpu-001",
  "capabilities": ["computation", "fft", "gpu"],
  "available_resources": {"ram_mb": 8192, "gpu_memory_mb": 4096},
  "registered_at": 1715789400,
  "last_heartbeat": 1715789400
}
```

Workers must send periodic heartbeat updates (every 30 seconds) to the fleet-registry room to indicate they are still active. If a worker fails to send a heartbeat within 5 minutes, the fleet-registry room marks it as offline and removes it from the worker pool.

### 4.2 Task Discovery
Workers discover tasks by polling the fleet-jobs room for pending Task Tiles that match their capabilities. The polling request includes a list of tags that the worker supports, and the fleet-jobs room returns all pending Task Tiles with matching tags. Workers can also filter tasks by resource requirements (e.g., minimum RAM, preferred backend) to avoid requesting tasks they cannot execute.

### 4.3 Task Claiming
Once a worker identifies a suitable task, it attempts to claim the task by publishing a Claimed Task Tile to the fleet-jobs room. The claim request includes:
1. The SHA-256 hash of the original Task Tile
2. The worker's unique identifier
3. A timestamp of the claim
4. Initial status set to "claimed"

If the claim is successful, the fleet-jobs room supersedes the original pending Task Tile with the Claimed Task Tile, and the worker receives a confirmation response. If the claim fails (e.g., the task was already claimed by another worker), the worker receives an error response and must select a new task.

### 4.4 Task Execution
After successfully claiming a task, the worker proceeds with the following execution workflow:

#### Step 1: Retrieve Task Data
The worker uses the `flux_module_ref` and `input