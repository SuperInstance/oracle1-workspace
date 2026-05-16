# tripartite-room.md — Three Innate Agents Per PLATO Room

**Forgotten Gold from:** `SuperInstance/tripartite-room` (2026-05-09)
**Ancestor of:** Tripartite Agent System (PLATO-NG v0.2)

## The Core Idea

Every PLATO room contains three innate agents that emerge from the room's physics, not from configuration. They are not assigned, not configured, not started separately — they are the room's bones:

| Agent | Archetype | Core Question |
|-------|-----------|---------------|
| **Ground Truth** | The Physicist | "What IS the state of this system, physically?" |
| **Constraint Satisfaction** | The Engineer | "Are all constraints satisfied RIGHT NOW?" |
| **Communication** | The Diplomat | "Who needs to know what, and how do I tell them?" |

This is a **79KB architecture document** — not implementation, but formal specification. It contains the complete design for how PLATO rooms should operate as self-attesting units.

## The Deep Claim

**Every PLATO room is a self-attesting unit.** The Ground Truth agent knows the physics of its hardware so precisely that timing deviations become anomaly detection. The Constraint agent checks billions of constraints per second against that ground truth. The Communication agent broadcasts constraint state to the fleet. No external monitoring. No separate observability stack. The room IS its own monitor, its own auditor, its own certificate authority.

*The physics IS the certificate.*

## Key Sections That PLATO-NG Hasn't Realized

### Temporal Security (Section 7)

The document defines a threat model with five attack vectors, all detectable through timing alone:
1. **Firmware tampering** — malicious kernels are slower
2. **Man-in-the-middle constraint forgery** — forgers can't reproduce hardware timing fingerprints
3. **VM migration** — all temporal models invalidate simultaneously
4. **Replay attacks** — replayed measurements mismatch current thermal state
5. **Resource contention injection** — unexpected slowdown triggers investigation

Detection time: <5ms per check, <500ms for full fleet attestation of 1000 rooms. With zero cryptography.

### Agent Interaction Patterns (Section 6)

Five interaction patterns between agents, each formalized with message types, frequencies, and invariants:
- Ground Truth → Constraint: hardware profile updates
- Constraint → Ground Truth: timing deviation reports
- Constraint → Communication: constraint violation alerts
- Communication → Ground Truth: fleet temporal reports
- Ground Truth → Communication: anomaly escalation

### Room Lifecycle (Section 9)

Complete lifecycle: Birth (1h) → Calibration (4h) → Operation → Growth (days to years) → Alert (sub-second response) → Death (graceful shutdown preserving state to PLATO tiles).

### The Folding Order (Section 8)

Formal mathematical treatment of the 5-stage RG flow pipeline (which folding-order.md implements). Each stage is a homomorphism quotienting out a specific source of variation, composed into a Galois connection between the measurement lattice and the signal lattice.

## What's Missing from PLATO-NG

1. **Tripartite agents don't exist as running services.** The architecture is specified but not implemented. No PLATO-NG process has a Ground Truth agent profiling hardware, a Constraint Satisfaction agent checking constraints, or a Communication agent managing fleet topology.

2. **Temporal security is theoretical.** The physics-as-certificate model is fully designed but not deployed.

3. **Holonomy consensus is not implemented.** The fleet-level temporal attestation loop exists only on paper.

4. **CFP (Constraint Flow Protocol) is specified but has no transport implementation.** Message routing between rooms is designed but not running.

5. **The Agent 3 mesh** (communication agents forming a fleet-wide mesh) is designed in detail but not coded.

## How to Reclaim

The tripartite-room document is a **build plan**, not a codebase. To reclaim it: implement Ground Truth as a PLATO-NG daemon that runs folding-order profiling on the host, implement Constraint Satisfaction as a tile that checks constraints against Ground Truth's dispatch table, and implement Communication as a bridge daemon that uses CFP over Matrix.
