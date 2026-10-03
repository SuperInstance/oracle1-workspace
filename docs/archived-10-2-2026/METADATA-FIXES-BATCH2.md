# Metadata Fixes — Batch 2

**Date:** 2026-07-12
**Scope:** SuperInstance repos with empty descriptions (a-g priority + all remaining)
**Rate limit used:** ~65 calls (2378 → 2335 remaining)

## Summary

Scanned all 1000 SuperInstance repos. Found **10 repos** with empty descriptions. All 10 were updated with descriptions and topic tags.

## Repos Updated

| # | Repo | Description | Topics |
|---|------|-------------|--------|
| 1 | `lau-plato-tutor` | The PLATO tutoring language — meaning-matched response evaluation using single embedding space for semantic answer comparison in Rust | rust, superinstance, embeddings, nlp, semantic-evaluation, tutoring |
| 2 | `lau-room-native` | Room-native agent system where the room itself IS the agent's context — Rust implementation of spatial agent architecture | rust, superinstance, agent-system, cognitive-architecture, spatial-context |
| 3 | `lau-shell-transport` | Transport layer for inter-shell communication — unified Transport trait with memory, stdio, and file-based JSONL backends, multiplexing router, and TTL-aware envelopes in Rust | rust, superinstance, inter-process-communication, messaging, transport |
| 4 | `loom-caching-rollout` | Production-grade shell script for phased 25% canary rollout of Loom caching with automatic rollback guardrails and Cloudflare metric sync | canary-deployment, cloudflare, devops, rollout, shell-script |
| 5 | `plato-portal` | Python SDK for persistent multi-agent systems — agents with markdown memory, in-memory fleet, thread-safe LRU cache, and optional DeepInfra LLM integration | multi-agent, persistent-memory, python, sdk, superinstance |
| 6 | `plato-semantic-search` | Production Cloudflare Worker for semantic search over the Plato/SuperInstance crate ecosystem using Workers AI BGE-small embeddings and Vectorize cosine ANN retrieval | ai, cloudflare-workers, embeddings, semantic-search, vectorize |
| 7 | `Scrapcraft` | Browser-based 3D voxel game set in an industrial scrapyard — middle schoolers build robots, program them with AI, and learn embedded engineering via Arduino C++ and MicroPython | arduino, education, stem, threejs, voxel-game |
| 8 | `sketch-composite-headspace` | Cognitive DAW prototype running two parallel reasoning shells (bass + treble) coordinated via t-minus cueing, fusing deep architectural analysis with fast pattern matching | archived, cognitive-architecture, experimental, parallel-reasoning, superinstance |
| 9 | `sketch-forgemaster-experiments` | Archived experiment results from the Forgemaster project — validating parallel stereoscopic reasoning with dual-shell cognitive architecture on ARM64 hardware | archived, arm64, cognitive-architecture, experiments, superinstance |
| 10 | `the-rotation` | Recursive self-improvement infrastructure for agent fleets — five-layer closed loop: Bayesian confidence, PID control, multi-shell compression, tensor cycle closure, and attractor dynamics | agent-fleet, bayesian, pid-controller, recursive-self-improvement, superinstance |

## Notes

- All 1000 visible SuperInstance repos were scanned; only these 10 had empty descriptions
- Batch 1 (h-z repos) was covered in a prior metadata pass
- Rate limit remained healthy throughout (never dropped below 2300)
- Some repos (lau-plato-tutor, lau-room-native) had generic fleet-template READMEs; their Cargo.toml `description` fields and source code were used for more accurate descriptions
