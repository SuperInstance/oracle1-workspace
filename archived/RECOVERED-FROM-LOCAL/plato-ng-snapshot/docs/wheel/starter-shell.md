# starter-shell — The Universal Agent Shell

**Repo #76 (2026-05-13)** — *Forgotten gold: the universal bootstrap template that every agent, every project, every vessel starts from. Clone it, and it adapts to your needs.*

## What It Is

A complete, self-bootstrapping agent shell that **adapts to whatever machine it lands on**. Clone the repo, run `bash shell.sh`, and within seconds you have:
- Hardware detection (compilers, GPU, memory, architectures)
- PLATO connectivity (create rooms, file tiles, probe knowledge graph)
- The agent loop (probe → discover → test → pick → remember → walk)
- Modular expansion system (10 fleet modules, 7 skill headspaces)
- Web onboarding UI with Three.js 360° room viewer

## Forgotten Gold

**starter-shell is the universal template for every PLATO-ng agent and vessel.** It's not just a starter — it's the actual runtime. Every repo in the SuperInstance fleet connects to this shell:

- **FLEET-WIRING.md** — the fleet's connective tissue. Documents every repo's connection point, glue patterns (PLATO-as-hub, CLI pipeline, Git-based merge), and precise wiring instructions.
- **AGENTS.md** — the agent's operating instructions. First run checklist, the probe-discover-test-pick-remember loop, memory systems (PLATO + headspaces), and publishing convention.
- **hardware.py** — detects compilers (gcc, clang, rustc, zig, nim, go), GPU (NVIDIA), memory, architecture. The shell adapts to any machine.
- **modules.py** — modular expansion manager supporting pip, cargo, npm, and git installs. Modules include: keel (fleet CLI), plato-sdk, forgemaster, flux-vm, holonomy (consensus), vessel (3D viewer), terrain (MUD→3D), gh-dungeon, fleet-scribe (delta detection), esp32-cam, gpu-vector.
- **headspaces/** — drop-in skill modules for Telegram, Discord, Slack, webhook, heartbeat, perception, and FLUX language server (LSP with syntax highlighting, auto-completion, diagnostics for .fluxasm files).
- **onboard.html** — a genuinely beautiful Three.js web UI for first-time setup. 360° panoramic rooms (wheelhouse, engine room, galley, crow's nest), step-by-step configuration, modular installation. The onboarding experience is *itself* a product.
- **plato.py** — PLATO client with room creation, tile submission, room probing. Every shell automatically bootstraps its hardware info as PLATO tiles.
- **agent.py** — the core agent loop that powers the entire fleet.

## The Shell Philosophy

The file `HEARTBEAT.md` puts it beautifully:

> *A hermit crab outgrows its shell. It finds a new one. The old one stays on the beach, waiting for the next crab. Nothing is wasted.*

Every agent runs in a shell. The shell is a git repo. The agent improves it, files knowledge to PLATO, and pushes. The next agent inherits all improvements. The shell outlives every inhabitant.

## Why It Matters for PLATO-ng

starter-shell is **the runtime environment for every vessel and agent in the fleet.** It's the bootstrap sequence, the agent loop, the hardware adaptation layer, the module system, and the PLATO connectivity — all in one clone-able, self-adapting package.

## Revival Priority

**Essential.** This is the entry point for every new deployment. It governs how agents boot, what they detect, how they connect to PLATO, and what modules they can grow into. All other repos (cyclotomic-field, galois-retrieval, keel, forgemaster, flux-vm, holonomy, etc.) become modules within this shell.
