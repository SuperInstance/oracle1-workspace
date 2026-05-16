# PLATO-NG Architecture Decisions

> Why we built it this way. For future engineers and agents who need to understand our choices.

## Decision 1: Python + NumPy for Math, Not Rust

**Context**: We tested Rust, Go, C, Zig, TypeScript, and Python for the same computation (eigendecomposition, spectral analysis).

**Result**: Python + NumPy at 19,214 evals/s (n=30) vs Rust at 9,713 evals/s.

**Why**: Python's NumPy is already calling C-level BLAS/LAPACK. Rust calls the same BLAS. Neither beats the other — they both call the same optimized C libraries. Python wins on development speed.

**Exception**: For tile persistence (SQLite via rusqlite) and hardware dispatch (CUDA, WebGPU), Rust NIFs via rustler are the right choice because they avoid the GIL.

## Decision 2: Gleam/BEAM for Routing, Not Python

**Context**: The PLATO server needs to handle 10K+ concurrent rooms. Python threading tops out at ~1K.

**Result**: BEAM handles 10M+ concurrent processes at 2KB each.

**Why**: BEAM was designed for telephone exchanges — massive concurrency with fault isolation. Python wasn't. When PLATO scales beyond 1K rooms, the routing layer migrates to Gleam GenServers. The room logic stays in Python.

## Decision 3: Tiles, Not Streams

**Context**: Most systems communicate via event streams (Kafka, Redis Pub/Sub). PLATO uses tiles (immutable facts with provenance).

**Why**: Tiles are auditable. Every submission has a parent, every room has a history, every decision is traceable. Streams are ephemeral. Tiles are permanent.

**Tradeoff**: Tiles are slower than streams for real-time coordination (~650 GETs/sec vs ~50,000 messages/sec in Kafka). For PLATO's scale (<10K rooms), this is fine. For real-time coordination, the event bus serves the same role.

## Decision 4: The Conservation Law as an Active Constraint

**Context**: We discovered the conservation law empirically. Then we had a choice: keep it as a research finding, or bake it into the system.

**Result**: The law is baked into:
- The gate pipeline (tiles outside ±2σ are flagged)
- Memory decay (off-law tiles decay 128x faster)
- The Refiner (drift >3σ triggers harness edits)
- The event bus (on-law tiles preferred for propagation)

**Why**: The law has R²=0.9602 across 5000+ samples. It's more reliable than any heuristic we could write. Letting the system enforce itself reduces anomalies.

## Decision 5: Three Agents, Not Two

**Context**: Most AI systems pair a user model with an application model. Two agents.

**Result**: We added a third — the hardware agent.

**Why**: Two agents create blind spots (each sees the other but not themselves). Three agents close all blind spots. The conservation law predicted this: three spectral parameters (γ, H, τ) → three agents (human, application, hardware).

**Evidence**: Every experimental run that used only two agents produced blind spots — either the hardware constraints were violated, or the human preferences were ignored. Three agents converged to stable, efficient operation.

## Decision 6: Application-First, Not Software-First

**Context**: Traditional development writes code first, deploys when ready. Months to first user.

**Result**: Application-First — describe the app, the agent simulates it immediately, compilation happens gradually.

**Why**: The cost of being wrong drops by orders of magnitude. Instead of $500K and 6 months to learn the app doesn't work, it's $50 in inference costs and 30 minutes. This changes which ideas get pursued.

**Risk**: The success trap — an agent-simulated app that works too well must be transitioned to code before hitting scale walls.
