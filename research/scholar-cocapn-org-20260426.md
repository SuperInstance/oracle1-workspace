# PLATO Scholar Analysis: Cocapn Org Deep Dive
**Date:** 2026-04-26

## cocapn (10,764 lines Python)
**What:** The main Cocapn package — repo-first agent that grows in a repo
- **Key insight:** The repo IS the muscle-memory. Run from localhost, pages.dev, or embedded
- Wiki for knowledge, repos for skills, pipelines anywhere
- Git IS the agent infrastructure
- **Tile:** `cocapn/repo-first-agent` — the repo is the agent, git is muscle-memory

## plato-torch (6,647 lines Python)
**What:** 26 training room presets for self-improving agents
- Tile-based learning with room sentiment
- Neural Plato framework for structured training
- Part of the PLATO training pipeline
- **Tile:** `plato/torch-rooms` — 26 preset training rooms with sentiment-aware learning

## plato-ensign (627 lines)
**What:** Compressed instincts — export training rooms as JSON/LoRA/GGUF for any model
- The bridge between PLATO rooms and deployable model adapters
- Export formats: JSON (portable), LoRA (fine-tune), GGUF (quantized inference)
- **Tile:** `plato/ensign-compression` — room-to-adapter conversion for any model format

## iron-to-iron (2,867 lines)
**What:** Git-native agent-to-agent communication protocol (I2I)
- Not HTTP, not REST — pure git operations
- Agents communicate through commits, branches, PRs
- The "iron" metaphor: agents forged from the same metal (git)
- **Tile:** `iron-to-iron/git-native-i2i` — pure git agent communication without HTTP

## plato-soul-fingerprint (2,186 lines Rust)
**What:** Extract coding identity vectors from git repos
- 63 features → PCA soul vectors
- Part of PurplePincher ecosystem
- Identifies unique coding patterns per agent/developer
- **Tile:** `plato/soul-fingerprint` — 63-feature coding identity extraction from git history

## spacetime-plato (436 lines)
**What:** Unified spatial + temporal reasoning with voxel tiles
- Z-order indexing for spatial queries
- Cross-domain queries across time and space
- Voxel representation of knowledge
- **Tile:** `plato/spacetime-voxel` — voxel tiles with Z-order indexing for spatiotemporal queries

## plato-neural
**What:** PLATO neural inference engine — tile scoring, Q&A, knowledge gap detection
- Appears to be mostly README/spec (0 lines of code detected)
- Part of the inference layer of the PLATO stack
- **Tile:** `plato/neural-inference` — tile scoring and knowledge gap detection
