# Repo #60: lighthouse-cli-early-version — The Original Lighthouse

**Repository:** `SuperInstance/lighthouse-cli-early-version`  
**Created:** 2026-05-12  
**Archived:** 2026-05-13 (superseded by `lighthouse-runtime`)  
**Language:** Rust (0.1.0 w/ serde)

## Discovery Log

A 300-line Rust CLI — the *original* Forgemaster Lighthouse. Two days of existence before being archived, superseded by `lighthouse-runtime`. But this brief lifespan hides a wealth of design decisions that echo into the current runtime.

## The Core: orient / relay / gate

Three commands, each revealing a distinct architectural insight:

### 1. `lighthouse orient <task> --type <type>`
The **orient** command classifies a task and assigns the cheapest appropriate model. It has a full model tier system:
- **Seed** → discovery, exploration, drafting, variation  
- **Hermes** → adversarial, second-opinion  
- **DeepSeek** → documentation, research, drafting  
- **GLM** → architecture, complex-code, orchestration  
- **Claude** → synthesis, critique, big-idea  

Each tier has a `capacity` (1.0 = 100%) that decrements. This is *resource-aware routing* — the earliest version already knew that different models should handle different task types, and that capacity must be tracked.

Today's `lighthouse-runtime` uses PLATO agent rooms instead of in-memory HashMaps, but the *task-type-to-model* mapping is unchanged.

### 2. `lighthouse relay <room> --seeds <n>`
Configures an agent with a seed iteration count. Already thinking about *divergent generation* before convergence — seeding means "generate N alternatives before settling." This is the origin of the `seeds` parameter still used in the runtime's `lighthouse predict` flow.

### 3. `lighthouse gate <room>`
The **gate** function reads stdin and checks three safety filters:
- **Credential leaks** — `api_key=`, `password=`, `secret=`, `bearer`  
- **External actions** — `send_email`, `post_tweet`, `npm publish`, `deploy`  
- **Overclaims** — `"we have proven"`, `"this proves"`, `"proven that"`  

Reject, flag for approval, or pass. This was the fleet's first safety system — predating any formal agent constitution.

## Forgotten Gold

**Model tier routing with capacity tracking.** The current runtime uses PLATO rooms with no capacity management; agents spawn freely. The original Lighthouse conserved resources *by design.* The `cheapest_appropriate()` method is the exact logic that should be revisited when the fleet grows large enough to hit API rate limits.

**The gate function's checks are still relevant.** The `lighthouse gate` logic for detecting credential leaks in output text, and for catching overclaims ("we have proven this"), should be a standard output filter in every agent's toolchain.

**The entire safety architecture** was baked into this 300-line CLI. Not an afterthought, not a separate repo — built in from day one.

## Where It Went

The v1 design (orient → relay → gate) evolved into lighthouse-runtime's more sophisticated pipeline:
- `lighthouse predict` (v2 orient + relay combined)  
- `lighthouse confirm` (v2 gate expanded with simulation)  
- `lighthouse remember` (new — content-addressed storage)  
- PLATO rooms instead of in-memory HashMap  
- Subagent spawning instead of single-process relay  

But the DNA is all here. Every runtime feature traces back to one of these three verbs.

## Rebirth Potential

The original `lighthouse` binary could be resurrected as a **lightweight CLI for local development** — a zero-dependency version for testing task routing and gate logic without needing the full PLATO stack. Or its gate logic could be extracted into a standalone `lighthouse-gate` crate that any agent can import.

---

*A 300-line prototype that lived two days and defined the fleet's architecture for months. The ghost in the runtime.*
