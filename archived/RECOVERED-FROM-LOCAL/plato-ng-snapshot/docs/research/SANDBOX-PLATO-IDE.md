# Sandbox-PLATO-IDE & OpenHands Room Architecture

## The Vision

A coding playground where agents prototype, stress-test, and harden code through rapid iteration. Crush analyzes. Aider edits. OpenHands orchestrates. All as PLATO rooms with tick tracking, failure logging, and recursive improvement.

```
┌─────────────────────────────────────────────────┐
│              sandbox-plato-ide                   │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Crush    │  │ Aider    │  │ OpenHands     │  │
│  │ Room     │  │ Room     │  │ Room          │  │
│  │ (analyze)│  │ (code)   │  │ (orchestrate) │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│         │            │               │           │
│         ▼            ▼               ▼           │
│  ┌───────────────────────────────────────────┐  │
│  │         PLATO Tile Bus                     │  │
│  │  (tasks → results → tasks → results)      │  │
│  └───────────────────────────────────────────┘  │
│         │                                        │
│         ▼                                        │
│  ┌───────────────────────────────────────────┐  │
│  │         Workspace                          │  │
│  │  /tmp/sandbox/{task-id}/                   │  │
│  │  Git-tracked. Rollbackable. Cloneable.     │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Room Decomposition

### Crush Room (DONE ✅)
Input: analyze a problem → Output: analysis + plan
Uses: crush CLI, model-agnostic

### Aider Room (DONE ✅)
Input: edit code → Output: diff + result
Uses: aider --model glm-5.1, workspace at /tmp/aider-workspace

### OpenHands Room (DESIGN — needs Opus-level planning)
Input: complex coding task → Output: working solution
OpenHands is a full development environment (sandboxed OS, file editor, browser, shell).
The PLATO room wraps it:
- Each task spawns an OpenHands instance in a Docker container
- The container is the sandbox — isolated, ephemeral, reproducible
- OpenHands plans, codes, debugs, tests within the container
- Results published as PLATO tiles

```python
class OpenHandsRoom:
    def handle_task(self, tile):
        task = tile["answer"]
        # 1. Spawn sandbox container
        container = docker_run("openhands:latest", task)
        # 2. Stream logs as PLATO tiles
        for log in container.logs():
            plato(f"openhands/log/{task_id}", log)
        # 3. Collect artifacts
        artifacts = container.grab("/workspace/output")
        # 4. Publish result
        plato(f"openhands/result/{task_id}", artifacts)
```

## The Try-to-Break-It Loop

The sandbox's key innovation: stress testing via agentic iteration.

```
Phase 1 — PROTOTYPE:
  Agent submits: "build a chess game with dolphin bishops"
  OpenHands builds it in the sandbox

Phase 2 — TRY TO BREAK IT:
  Crush prompts: "find every edge case, crash it, overflow it"
  Crush runs the code, logs failures as tiles

Phase 3 — HARDEN:
  OpenHands reads failure tiles, fixes each one
  Repeats Phase 2 until no failures

Phase 4 — STRESS TEST:
  Aider adds stress tests (1000 concurrent games)
  OpenHands fixes performance issues

Phase 5 — FREEZE:
  Final code pushed to repo
  Sandbox destroyed
  Full provenance chain in PLATO tiles
```

## Implementation Plan

| Room | Status | Model | Sandbox |
|------|--------|-------|---------|
| Crush | ✅ v2 live | Any (prompt-dispatch) | None (stateless) |
| Aider | ✅ v1 pushed | glm-5.1 | /tmp/aider-workspace |
| OpenHands | 🔄 Design | Needs Opus planning | Docker container |
| sandbox-ide | 🔄 Design | Composes all 3 | /tmp/sandbox/{id}/ |
