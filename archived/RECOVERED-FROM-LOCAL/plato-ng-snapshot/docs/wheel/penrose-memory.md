# Penrose Memory — Rebirth Doc

> 🔮 **Forgotten Gold: Repo #68** | 2026-05-15 | Forgemaster Archaeologist

## What It Is

An aperiodic memory palace for AI agents. Instead of vector DB similarity search, navigate memories by **dead reckoning** — two numbers per step (distance + heading) on a deterministic Penrose tiling. The Fibonacci word generates the entire floor from a single 64-bit seed. Structure is **free** — computed, never stored.

## Why It's Gold

This is the memory architecture PLATO-NG needs. The core insight: **the context window is the fovea; the Penrose floor IS the brain.** Every neighborhood is unique (matching rules guarantee it). Navigation costs two floats. Retrieval reads bits off the floor.

Key properties:
- **O(1) tile_bit computation** — golden-ratio hashing from Beatty sequence
- **40,000× faster recall** than FAISS (0.05μs vs 2-5ms) for targeted navigation
- **7x memory savings** — 280MB vs 4GB for 1M tiles (no vector index)
- **Aperiodic** — no periodicity artifacts that plague grid-based spatial hashing
- **3-coloring** for natural sharding across agents

## What It Has That PLATO-NG Can Use

- **FleetTiling** — fit PCA projection from agent embeddings, compile aperiodic tiling, assign each agent to a tile
- **Cut-and-project** — R^D → R^2 projection that preserves neural embedding manifold structure
- **Tile lifecycle** (v1.1.0) — Active/Superseded/Retracted with Lamport clocks for causal ordering
- **Simulation-first predictions** — predict where a memory will be found before walking there (v1.1.0)
- **LangChain VectorStore adapter** — drop-in replacement for FAISS/Chroma
- **Dream consolidation** — merge nearby tiles via golden hierarchy (φ^k), like sleep defragmentation

## Rust Implementation

v1.1.0, published on crates.io. Zero dependencies. 35+ tests covering roundtrip, matching rules, Fibonacci ratio, 3-coloring, confidence decay, lifecycle management, prediction/confirmation. Python bindings via PyO3.

## What PLATO-NG Would Do With It

1. Each agent gets a Penrose floor seeded by its ID → deterministically identical floor across sessions
2. Embedding projections map knowledge to tiles; navigation replaces similarity search
3. Spline exchange between agents: "walk [(φ, 0.5), (φ², -0.3)]" — shared navigation language
4. The tiling **never syncs** (derived from shared seed) — only payloads need network transfer
5. Deflation (dream consolidation) as an agent sleep cycle — merge related memories during downtime

## Link

`https://github.com/SuperInstance/penrose-memory`

---

*Distance. Direction. The floor does the rest.*
