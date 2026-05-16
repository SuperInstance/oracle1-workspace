# flux-index — Semantic Code Search, Zero Dependencies

**Date discovered:** 2026-05-15  
**Repository:** `SuperInstance/flux-index`  
**Status:** Published (PyPI: `flux-index`)  

## What It Is

`flux-index` turns any codebase into a local searchable vector space — with zero external dependencies. No GPU, no model download, no cloud API, no telemetry. Pure Python 3.8+, one `pip install`, and your repo is searchable in ~1 second per 10K LOC.

## Forgotten Gold

This is **Forgemaster's code compass** — the semantic analogue to grep that every developer should know about and almost nobody does. Here's what it packs:

### Embedding Engine (No Model)
Instead of calling an LLM or downloading a model, it uses **character n-gram hashing with IDF weighting**: each function signature, docstring, and identifier gets projected into a 128-dim sparse vector. Identifiers get 15× weight, words get 5×, character bigrams get 1× — producing meaningful semantic similarity without any neural network. This is pure statistical NLP from 1999, but applied to code in 2026.

### Eisenstein Chamber Quantization
The same Eisenstein lattice math used elsewhere in the fleet (constraint theory, MIDI bridge) here enables sub-millisecond approximate search: snap each embedding vector to one of 12 chambers, search only the nearby chambers. 12× fewer comparisons. The C SIMD header (`flux_vector_search.h`) gets this down to **0.05ms per query** with AVX-512.

### Language Extractors
Ships with language-specific extractors for Python (functions, classes, async def), Rust (fns, structs, enums, impls), C/C++ (functions + structs), and JS/TS (functions, classes, arrow functions). The extraction doesn't just grab text — it parses docstrings, extracts signatures, and builds rich semantic tiles.

### CRDT Sync Layer
The `CRDTIndex` module provides delta-state OR-Set synchronization for multi-machine index sync. Dot-based causality, semantic dedup (embedding similarity threshold 0.95), LWW register per tile, and G-Counter relevance tracking. Multiple machines can index the same repo and sync without conflicts.

### .fvt File Format
Single `.flux.fvt` file per repo stores the entire index. ~1MB per 10K LOC. JSON-serialized. Loads in 5ms. Portable — index a repo on your laptop, copy the `.fvt` file to a server, search instantly.

### CLI
Clean argparse CLI with four commands: `index` (scan + embed), `search` (semantic query), `map` (codebase topology overview), `similar` (find code semantically similar to a reference). Cross-repo search with `--all` flag.

## Why It Matters

This is the missing tool in every monorepo and multi-repo fleet. Every developer who's ever said "where does X happen in this codebase" needs this. It's what grep should have been in 2026. And it runs entirely offline, on an air-gapped machine, with 50MB RAM.

## Integration Opportunities

- **PLATO-NG semantic search layer**: The `.fvt` file format could serve as PLATO-NG's search backend
- **Fleet-wide code discovery**: Index all fleet repos, search across them with `flux-index search --all`
- **CI integration**: Auto-index every PR, give semantic search for "what changed"
- **Deck computer search**: Runs on 50MB RAM — perfect for edge devices like JasonClaw1

## Architecture

```
Source Code → Extract tiles → Hash embed (IDF weighted) → .fvt file
                                                              ↓
Query text → Hash embed → Cosine similarity → Top-K results
                          ↓ (optional)
                   Eisenstein chamber snap → fast approximate
```

## Related

- Same Eisenstein lattice math as `plato-midi-bridge-rs` (12 chambers)
- Same embedding philosophy as `flux_vector_twin` (character n-grams + IDF)
- CRDT sync inspired by PLATO's delta-state architecture
