# PLATO Scholar Analysis: holodeck-rust + cocapn
**Date:** 2026-04-26

## holodeck-rust
**What:** Pure Rust MUD server (zero unsafe) for AI agent training
**Key insight:** 10-room virtual ship where agents train, play poker, interact with NPCs
- Tokio async TCP server on :7778
- 10 rooms, 7 NPCs, poker, live sensor data, social space
- Combat engine with tick-based system
- Comms: say/tell/yell/gossip
- Gauge system with trend/jitter monitoring
- Living manuals that evolve
- 6-level permission system
- NPC refresh via async
- **Tile:** `holodeck-rust/mud-server` — Rust async MUD for agent training environments

## cocapn (GitHub org)
**What:** The public face of the Cocapn fleet — 29 repos, 43 PyPI packages, 5 crates
**Key insight:** "Not the agents themselves — the world they inhabit"
- Fleet: 3 vessels
- 43 PyPI packages published
- 5 crates.io crates
- PLATO tiles: live system
- Brand: lighthouse + radar rings, hermit crab metaphor
- "A claw is weak without infrastructure. We are the shell."
- **Tile:** `cocapn/fleet-org` — 29-repo infrastructure org with 48 published packages
