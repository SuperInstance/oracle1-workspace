# fleet-memory.md — Content-Addressable Distributed Memory

**Forgotten Gold from:** `SuperInstance/fleet-memory` (2026-05-09)
**Ancestor of:** Memory Crystal (PLATO-NG v0.1)

## The Core Idea

`fleet-memory` is a Rust crate (zero external dependencies) that implements distributed holographic memory for agent fleets. Patterns are striped across `n_agents`, each holding `dim_per_agent` interpolation points. Storage and retrieval use cosine similarity; partial cues match on a prefix of dimensions.

It's not a database. It's a **distributed attractor memory** — each agent holds a fragment, but coupling between fragments enables holographic reconstruction. This is the formal basis for PLATO-NG's Memory Crystal system.

## Experimental Grounding

Three experiments anchor the implementation:

- **E191 (8.3× lossless compression):** Attractor-based encoding of structured vectors achieves 8.3× compression with zero information loss.
- **E193 (1-bit coherence):** Every bit of stored data carries complete system information. Perfect retrieval from single-bit queries.
- **E194 (perfect coupling recovery):** Zero L2 error on full-agent erasures — survivors' coupling fills gaps via per-dimension mean.

These demonstrate that a fleet of agents can store and retrieve patterns without any central index. The pattern IS the address.

## Lifecycle States (v0.2.0)

Already integrated: `Active → Superseded → Retracted` lifecycle mirrors PLATO v3's tile lifecycle. The key insight from the Tripartite Convergence paper is embedded here: *supersession is not deletion, forgetting is strategic compression.*

## Simulation-First Predictions

Patterns carry a `t_minus_event` field — predictions about future events. When the event happens, the prediction is confirmed and becomes active knowledge. When mismatched, it's superseded by corrected observation. This is the simulation-first pattern embedded at the memory level.

## What's Missing from PLATO-NG

1. **Content-addressable retrieval by similarity.** PLATO-NG tiles are addressed by hash. fleet-memory retrieves by cosine similarity — "find me the pattern that looks like this." This is the foundation for associative memory that PLATO-NG lacks.

2. **Partial cue matching.** `retrieve_partial` finds full patterns from partial queries. This enables progressive disclosure: "I only know 2 of 8 dimensions, but find me what matches."

3. **Information entropy per agent.** `information_per_agent` tracks Shannon entropy across all patterns stored on each agent. This is a diagnostic for knowledge distribution that PLATO-NG doesn't have.

4. **Lamport clocks at the memory level.** fleet-memory has `LamportClock` integrated into `MemoryPattern` lifecycle operations. PLATO-NG tiles don't carry causal ordering metadata.

5. **Distributed coupling recovery.** The `corrupt_and_recover` mechanism is a simplified attractor network. PLATO-NG has no equivalent — when an agent goes silent, its knowledge is simply lost.

## How to Reclaim

The Memory Crystal in PLATO-NG should be a **hybrid**: hash-addressed block storage (current) + content-addressable similarity retrieval (from fleet-memory). The key addition is cosine-similarity queries across the tile index, enabling associative recall without knowing the exact tile ID.
