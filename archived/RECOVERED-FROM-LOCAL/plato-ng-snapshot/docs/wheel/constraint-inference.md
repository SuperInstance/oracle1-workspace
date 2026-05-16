# constraint-inference — Rebirth Doc

> Reverse-engineers constraint parameters from user override patterns. Created 2026-05-07. **ARCHIVED** — superseded by Forgemaster FLUX runtime.

## What It Is

A TypeScript service that watches how users override captain decisions and reverse-engineers what constraint boundaries need adjusting. Every override is a constraint signal: when captain says EMERGENCE and user says STABLE, the emergence threshold was too sensitive. The service maps decision deltas to constraint parameter updates, then re-deliberates the entire fleet state with the new model.

## Forgotten Gold

### 1. Simulation-First Prediction (v0.2.0)

The most sophisticated pattern in the repo: **every constraint update is a hypothesis**. Before applying, predict the effect and file a "t-minus prediction" tile to PLATO. After observing 1 hour of real override data, confirm or supersede the prediction. This uses a Lamport clock for causal ordering — ensuring that even in a distributed fleet, prediction→confirmation chains are ordered correctly. This "predict → apply → observe → confirm/supersede" pattern is a general insight applicable to any learning system that modifies shared state based on human feedback.

### 2. The Decision Ordering Model

The core theoretical insight: decisions form a spectrum from most constrained to most permissive: `CONSTRAINED → STABLE → DECIDED → EMERGENCE`. When a user overrides from a less-constrained to more-constrained state (captain=EMERGENCE, user=STABLE), they're tightening. The reverse is loosening. This is elegant constraint theory baked into a simple array index comparison. It maps real human steering behavior to computable parameter adjustments without needing a heavy ML model.

### 3. Autonomous HTTP API Server

The engine runs its own HTTP server on port 9439 with a REST API: `POST /override` to inject override events, `GET /model` for current state, `GET /patterns` for detected patterns, `GET /health` for liveness. This makes it a self-contained microservice that any agent in the fleet can talk to directly, without going through a broker.

### 4. Re-Deliberation Feedback Loop

`re_deliberate.ts` closes the loop: detect override pattern → update constraint model → write update to PLATO → signal captain to re-deliberate → captain runs with new parameters → new decisions logged → next override cycle. This creates a self-correcting system that converges on the user's true constraint preferences over time.

### 5. PLATO v3 Lifecycle Operations

The `plato_bridge.ts` implements advanced PLATO lifecycle patterns: prediction tiles with `t_minus_event` timestamps, supersede operations that replace stale predictions, Lamport clock merging for distributed causal ordering. These APIs are more advanced than what most fleet agents use — they were designed for v3 of the PLATO protocol that supports tile lifecycle states (active → superseded → retracted).

## Why It Matters Now

Archived because constraint theory work moved to Forgemaster's FLUX runtime — but the simulation-first pattern, the decision ordering model, and the autonomous HTTP API design are transferable architectural insights. The Lamport clock + prediction→confirm cycle is a general distributed learning pattern. The decision spectrum model belongs in any system where humans steer agents.
