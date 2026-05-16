# Wheel: memory-crystal-early-version

**Repo #65** — Archived 2026-05-13 → Superseded by `SuperInstance/penrose-memory`

## What It Was

A complete Rust crate implementing **crystallized memory**: lossy, reconstructive persistence for AI agents. Content was compressed into `Tile` structs (constraints + summary + valence), stored as JSON on disk, and recalled through context-dependent reconstruction. Think of it as a filesystem-backed associative memory where every write is lossy from day one.

## Forgotten Gold 🔥

### 1. The Telephone Game + Crystallization Point Detection
This is the most valuable forgotten concept. `TelephoneChain` tracks successive rounds of encode→decode→re-encode and measures **fact survival rate** at each round. The `crystallization_point()` method identifies exactly *when* a memory stops degrading — the round where survival rate drops < 5% between iterations. This is a **runtime-detectable phase transition**: the memory has converged to its immutable core.

**plato-ng relevance**: This should be a first-class primitive. When an agent stores a memory, run it through 2-3 telephone rounds to find its crystallization point BEFORE committing. Don't just store raw embeddings — store the crystallized constraint set that survives compression.

### 2. Ebbinghaus Decay with Reconsolidation
The `DecaySchedule` implements the full Ebbinghaus forgetting curve (`retention = e^(-t/S)`) with:
- **Valence-weighted half-life**: High-valence memories decay slower (effective half-life *= 1 + 0.5*valence)
- **Access-count reinforcement**: Each retrieval extends effective half-life by ln(access_count) * 0.3
- **Reconsolidation**: Each recall resets the decay clock AND merges new context into the existing tile (neurobiological model — memories become labile when recalled, and re-storage strengthens them)

Penrose-memory absorbed the tile structure but **discarded the reconsolidation model**. plato-ng should bring this back.

### 3. Generation Tracking with Parent Pointers
Every tile tracks `generation: u32` and `parent_id: Option<TileId>`. This creates a DAG of memory evolution: you can trace any reconstructed memory back to its original source. Combined with the telephone game, this gives a **full provenance chain** for every memory.

### 4. Multi-Index BTreeMap Design
`CrystalIndex` maintains THREE parallel indices (by valence, by timestamp, by constraint keywords) — all kept in sync through insert/remove. The keyword index uses a `HashMap<String, HashSet<TileId>>` for O(1) lookups. This is a practical lesson in how to index crystallized memories efficiently.

### 5. Crystal Persistence as Design Pattern
The `Crystal` struct wraps an on-disk tiles directory with lazy loading. It only reads tiles on-demand but maintains a live in-memory index. This is the right architecture for agent memory that's larger than RAM.

## What Was Absorbed vs Discarded

| Absorbed into penrose-memory | Discarded |
|---|---|
| Tile structure (UUID, constraints, valence) | Ebbinghaus reconsolidation model |
| Constraint-based text encoding | Generation tracking with parent pointers |
| Telephone game concept | Crystallization point algorithm |
| | Disk-based persistence layer |
| | Multi-index BTreeMap design |

## Extraction Value for plato-ng

**High**: The telephone→crystallization pipeline is directly implementable. The Rust code compiles clean — just modernize the dependencies and rebase on plato-ng's memory types. The decay model with reconsolidation is the missing piece in fleet-memory's current architecture.
