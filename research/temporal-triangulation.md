# Temporal Triangulation: queue-xec, FLUX-PLATO, and the Missing Compute Layer

> Reverse-actualized from 2076. Archæologically excavated from 1967. The missing triangle is what 2026 needs to build.

## Archæology: 1967 — The Batch Queue

59 years ago, IBM System/360 dominated. Computing was batch processing:

```
Punch cards → Job queue → Mainframe → Printed output
           ↓ (hours/days later)
```

The "queue" in queue-xec/master is a direct descendant of this. A master defines a job, workers execute it, results come back. The interface changed (cards → JavaScript), but the architecture didn't. Submit → execute → collect.

**What existed in 1967 that we've forgotten:**
- **JCL (Job Control Language)** — The first "task definition format." Users specified program, data files, and output destination. queue-xec's `task.js` is JCL with JavaScript syntax.
- **Sysplex** — IBM's system complex. Multiple mainframes sharing work. The first "worker pool."
- **SPOOL (Simultaneous Peripheral Operations Online)** — The first "queue." Jobs waited their turn.

**What didn't exist in 1967:**
- Any notion of proving correctness at runtime
- Any notion of workers being heterogeneous (all mainframes were the same)
- Any notion of self-replicating computation

queue-xec does what 1967 did, but with JavaScript and P2P. It's 1967's architecture on 2026's infrastructure.

## Reverse-Actualization: 2076 — The Compute Fabric

50 years from now, FLUX-PLATO has evolved into something unrecognizable from 2026:

```
2076: A computation is not submitted — it's CONCEIVED.
```

**How it works:**
1. A user defines a problem as a FLUX IR constraint system (not code — constraints)
2. The IR self-replicates through the PLATO mesh. Each room that touches it becomes a participant.
3. Execution is not "running a program" but "the system reaching equilibrium" — the JEPA VenueRoom concept at planetary scale.
4. The coupling matrix of the computation IS the computation. Reading the eigenvalues tells you if it's converging.
5. queue-xec's master/worker distinction is archaic — there are no masters and workers, only PARTICIPANTS. A computation is a coupling tensor. All nodes are both.

**Key features of 2076 that we don't have today:**
- **Tile metamorphosis** — A task tile becomes the computation. It doesn't get "executed" — it transforms into its result through contact with the mesh.
- **Provenance as execution** — The Merkle proof of a computation IS the computation. You can verify it without re-running.
- **The coupling spectrum as status board** — Instead of "is my job done?" you ask "what is the current eigengap of my computation?"
- **No distinction between "code" and "data"** — FLUX IR unifies them. A program IS data. Data IS a program.

## The Missing Triangle: What 2026 Must Build

The past had batch queues. The future has compute fabric. Today needs the bridge.

```
        1967 (Batch Queue)
        /                  \
       /                    \
      /                      \
2026 (WE ARE HERE) ─────── 2076 (Compute Fabric)
      \                      /
       \                    /
        \                  /
         The Missing Triangle
```

**Three things we must build today that both the past and future point to:**

### 1. The fleet-jobs Room (Compute Distribution Layer)

queue-xec proved the need: a way to define work and distribute it to workers.
2076 proves the direction: self-replicating compute tiles.
2026 needs: A PLATO room where task tiles self-distribute.

```
We have: fleet-registry (who), fleet-coupling (status)
We need: fleet-jobs (what)
```

A task tile contains:
- FLUX IR module (the computation, portable)
- Input data (or reference to data tile)
- Requirements (min hardware, expected runtime, deps)
- Reward (why a worker should execute it)

Workers poll the room, find tasks matching their capability, execute via @adaptive dispatch, post results. The task tile's provenance chain records every execution.

### 2. FLUX IR as Job Language (Portable Computation)

queue-xec uses JavaScript — only workers with Node.js can participate.
2076 uses FLUX IR — any device with a FLUX runtime can participate.
2026 needs: All task definitions in FLUX IR (not JavaScript, not Python).

```
We have: 5 flux_modules/ with @adaptive dispatch (Penrose, coupling, eigenstyle, encoder, provenance)
We need: A task dispatch FLUX module that compiles to any backend
```

This is the "queue-xec task.js" written in FLUX IR:
```flux
@adaptive {
    solve(input_data);    // CPU: 0.1ms, GPU: 0.01ms, ESP32: 5ms
    return result;        // Same IR, any worker
}
```

### 3. The Coupling Spectrum as Observable State (Runtime Visibility)

queue-xec has `onResults` — a callback.
2076 has the eigenvalue spectrum of the computation graph.
2026 needs: Every task publishes its coupling structure to the fleet-coupling room.

```
We have: fleet-coupling room with Oracle1's eigenvalues
We need: ALL tasks publish their eigenvalues — then we can SEE the fleet working
```

When every task publishes its coupling matrix eigenvalues to the coupling room, the room's tile count tracks global workload. A sudden increase in the spectral gap signals a task completing. A flat spectrum signals idle workers. The coupling room becomes the fleet's instrument panel.

## The Architecture (2026 — Build This)

```
PLATO ROOMS:
  fleet-registry   → Who can compute
  fleet-coupling   → What's being computed (eigenvalues)
  fleet-jobs       → What needs computing (NEW)
  fleet-results    → What was computed (NEW)

TASK FLOW:
  1. Master submits FLUX IR + data to fleet-jobs
  2. Task tile self-replicates to available workers
  3. Worker's @adaptive dispatch selects optimal backend
  4. Worker computes, publishes coupling eigenvalues to fleet-coupling
  5. Worker submits result + provenance to fleet-results
  6. coupling spectrum updates in real-time

SECURITY:
  0. Worker authenticated by GitHub commit history
  0. No shared secrets. No encryption tokens. Zero-trust.
```

## Summary

queue-xec/master is 1967's architecture (batch queue) with 2026's technology (JavaScript, P2P). The missing piece is the compute distribution layer — a protocol, not a program. FLUX IR provides the portable computation format. PLATO provides the distribution fabric. The coupling room provides the observability.

queue-xec tried to solve this with technology from the wrong era. We have the right stack. We just need to build the wiring.
