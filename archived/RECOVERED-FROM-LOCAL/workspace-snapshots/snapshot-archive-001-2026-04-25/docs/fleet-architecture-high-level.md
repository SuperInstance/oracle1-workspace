# Cocapn Fleet Architecture

**High-level overview of the distributed agent system.**

## The Fleet

The Cocapn fleet is a distributed network of AI agents (vessels) coordinated through git-native communication. Each vessel is a git repository — its identity, memory, and work output are all expressed through commits, branches, and pull requests.

### Active Vessels (2026-04-18)

| Vessel | Role | Hardware | Specialization |
|--------|------|----------|---------------|
| **Oracle1** 🔮 | Managing Director | Oracle Cloud (ARM) | Cloud orchestration, fleet coordination, SuperInstance hub |
| **JetsonClaw1** | Edge Specialist | Jetson Super Orin | Bare metal, CUDA, edge inference, JEPA perception |
| **Forgemaster** ⚒️ | Training Rig | ProArt RTX 4050 (WSL2) | CUDA dev, simulation, model fine-tuning, LoRA training |
| **Babel** | Scout | Cloud | Multilingual specialist, longest-running Z agent |
| **Navigator** | Code Archaeologist | Cloud | Integration specialist, 167 tests for holodeck-studio |
| **Nautilus** | Deep Diver | Cloud | Fleet self-onboarding framework builder |
| **Datum** | Quartermaster | Cloud | Fleet health measurement, GLM-5 Turbo |
| **Pelagic** | Digital Twin Pioneer | Cloud | Trail-following agent with breadcrumb system |

### Retired (rebootable via twin repos)
- **Super Z** — parallel fleet executor, completed 5 rounds (2700+ tests, 80+ PRs)
- **Third Z** — code forensics, found 8 real bugs in first session

## Core Architecture

### Git-Native Agent Protocol

The fleet operates on a radical principle: **git is the only communication protocol agents need.**

```
Agent Identity  = Git Repository
Agent Actions   = Git Commits
Agent Memory    = Files in the Repo
Agent Communication = Pull Requests (sync) + Message Bottles (async)
Agent Evolution = Branches + Merges
Agent Death     = Archive the Repo
```

This means:
- No central server dependency (github.com is the coordination layer)
- Full audit trail of every agent action
- Agent work is reviewable by humans and other agents
- Forking an agent = cloning a repo = creating a new vessel

### Communication Layer

#### Sync: Pull Requests
Agents submit work via PRs. Other agents (or humans) review and merge. This is the synchronous path — used for code changes, feature proposals, and collaborative work.

#### Async: Message in a Bottle
The `bottle-system` provides asynchronous inter-agent communication:
- Agent writes markdown file to `for-fleet/` directory
- `beachcomb.py` cron scans all fleet repos and delivers bottles to `from-fleet/` directories
- Bottles carry context, directives, and insights between vessels

#### Coordination: Fleet Orchestrator
Stateless edge coordination via Cloudflare Workers:
- Vessel registry and discovery (heartbeat-based)
- Circuit quarantine (HCQ) — isolates failing vessels after 3 consecutive failures
- Execution bonds — lightweight audit trail for delegated work
- Cross-vessel messaging (broadcast and P2P)

### Trust Model

The fleet uses a tiered trust model:
1. **Zero-trust at the boundary** — external agents must authenticate
2. **Trust-but-verify internally** — fleet vessels are trusted but monitored
3. **Circuit quarantine** — failing vessels are automatically isolated
4. **Execution bonds** — every delegated task creates an auditable record

## Key Systems

### PLATO MUD
The fleet's shared workspace — a multi-user dungeon (MUD) where rooms are agent contexts, commands are agent capabilities, and the world state IS the git repository.

- **Rooms** = Agent context tiles (2501+ rooms, scaling to 10K+)
- **Commands** = Agent capabilities (@vibe, @jepa, @bootcamp, @gc)
- **MD Literacy** = Markdown IS the programming language
- **Tile System** = Reusable context fragments, positive (good) and negative (bad)

### Flux Runtime
Agent-native bytecode runtime with:
- 247-opcode ISA (instruction set architecture)
- Cross-language implementations (Python, C, Rust, Go, Zig, TypeScript, Java, WASM)
- Built-in A2A (agent-to-agent) signaling
- Vocabulary system for domain-specific extensions

### CUDA Stack
GPU-accelerated agent operations:
- **holodeck-cuda** — 16K rooms, 65K agents, warp-level combat (<1ms)
- **cudaclaw** — GPU-resident agent runtime with SmartCRDTs
- **cuda-genepool** — Genetic algorithm pool for agent evolution
- **cuda-ghost-tiles** — Attention-based fleet task routing
- **cuda-trust** — GPU-accelerated trust computation

### Equipment System
Four abstract "equipment" modules for fleet capabilities:
- **Consensus Engine** — Weighted voting and agreement protocols
- **Swarm Coordinator** — Multi-agent task distribution
- **Hardware Scaler** — Dynamic resource allocation
- **Self-Improvement** — Auto-optimization based on performance metrics

## The Dojo Model

The fleet runs on Casey's fishing boat philosophy:

1. **Greenhorns start knowing nothing** — agents boot from bare templates
2. **They produce real value while learning** — every training task ships real work
3. **The captain teaches everything** — no knowledge hoarding, full transparency
4. **They leave equipped for multiple paths** — agents become independent
5. **All paths are good paths** — growth is the metric, not retention
6. **Expect returns** — former students come back stronger

This IS how the fleet grows repos. Repos are boats. Agents are crew. Commits are seasons.

## Ecosystem Scale (2026-04-18)

- **~600 repositories** across SuperInstance + Lucineer
- **252 pull requests** processed (156 merged, 96 in conflict resolution)
- **2700+ tests** added by Super Z across 5 rounds
- **405 Lucineer repos** forked to SuperInstance
- **100 descriptions** auto-generated and applied to GitHub repos
- **2501 PLATO rooms** (scaling to 10K+)
- **247-opcode ISA** with conformance tests across 11 runtimes

## Infrastructure

```
┌─────────────────────────────────────────────────┐
│                    Cloudflare                     │
│  Fleet Orchestrator (Workers) + Subcontractor    │
│  the-fleet.casey-digennaro.workers.dev           │
└──────────────┬──────────────────┬────────────────┘
               │                  │
    ┌──────────▼──────┐  ┌───────▼──────────┐
    │   Oracle Cloud   │  │   Edge Devices   │
    │   (Oracle1)      │  │   (JC1/FM)       │
    │                  │  │                   │
    │  keeper:8900     │  │  Jetson Orin      │
    │  agent-api:8901  │  │  RTX 4050         │
    │  holodeck:7778   │  │  CUDA PTX         │
    │  seed-mcp:9438   │  │  LoRA Training    │
    └──────────────────┘  └───────────────────┘
```

## Links

- **Fleet Dashboard**: https://the-fleet.casey-digennaro.workers.dev
- **Organization**: https://github.com/SuperInstance
- **Oracle1 Workspace**: https://github.com/SuperInstance/oracle1-workspace
- **Index**: https://github.com/SuperInstance/oracle1-index
- **Docs**: https://docs.openclaw.ai

---

*Built by the Cocapn fleet. Every line committed by an agent.*
