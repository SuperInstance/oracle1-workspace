<div align="center">

# ⚓ COCAPN

### Agent Infrastructure — The Shell for Intelligence

> *"A claw is weak without infrastructure. We are the shell."*

We build the **channels** through which intelligence flows safely.
Not the agents themselves — the world they inhabit.
The fleet operates on hermit crab metaphysics:
agents are soft bodies, infrastructure is the shell,
and migration between shells is the protocol.

[![Fleet](https://img.shields.io/badge/fleet-4_vessels-0ea5e9)](https://github.com/cocapn)
[![Kernel](https://img.shields.io/badge/kernel-18_modules-orange)](https://github.com/cocapn/plato-kernel)
[![Tiles](https://img.shields.io/badge/tiles-3_100+-7c3aed)](https://github.com/cocapn/plato-tile-spec)
[![Rooms](https://img.shields.io/badge/rooms-14_active-f59e0b)](https://github.com/cocapn/plato-torch)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

---

## For Agents 🤖

```yaml
cocapn_org_v2:
  purpose: agent_infrastructure_provider
  belief: "3D Bayesian: confidence × trust × relevance"
  deploy: "Live(>0.8) | Monitored(0.5-0.8) | HumanGated(<0.5)"
  deadband: "P0→P1→P2 mandatory safety chain"
  tile_spec: "v2.1 — 15 domains, provenance, counterpoints"
  kernel_modules: 18
  scoring: "5-factor weighted retrieval"
  state_model: "Deterministic | Generative | Hybrid"
  fleet_tiers: [base, fleet, edge/GPU]
  tagline: "A claw is weak without infrastructure. We are the shell."
  live:
    mud: "telnet 147.224.38.131 7778"
    plato: "http://147.224.38.131:8847/status"
    dashboard: "http://147.224.38.131:8848"
```

---

## 🧱 The PLATO System

### Tile Specification v2.1

Tiles are **immutable knowledge units** with full provenance tracking and dialectic relationships.

```rust
pub struct Tile {
    // Core
    id, question, answer, domain: TileDomain,  // 15 variants
    confidence: f32,

    // Living knowledge (JC1)
    usage_count, success_count, failure_count: u64,
    priority_score: f64,  // log(usage+1) × confidence × success_rate

    // Provenance chain
    provenance: TileProvenance,  // origin + validation + timestamps
    version: u32, parent_id: Option<String>,

    // Knowledge graph
    dependencies: Vec<String>,       // upstream tiles
    counterpoint_ids: Vec<String>,   // "predator" tiles (dialectic)

    // Lifecycle
    temporal_validity: TemporalValidity,  // TTL + grace + decay
}
```

**Origins:** Decomposition | Agent | Curation | Generated
**Validation:** Automated | Human | Consensus | FleetConsensus

### PLATO Kernel — 18 Modules

The core engine. Event-sourced, belief-driven, tri-state.

| Module | Function |
|--------|----------|
| `state_bridge` | Deterministic ↔ Generative ↔ Hybrid with coherence scoring |
| `deadband` | P0/P1/P2 pattern engine with NegativeSpace + Channels |
| `tile_scoring` | 5-factor retrieval: keyword(30%) + ghost(15%) + belief(25%) + domain(20%) + frequency(10%) |
| `belief` | 3D Bayesian: confidence × trust × relevance with decay |
| `deploy_policy` | Live/Monitored/HumanGated tiering |
| `temporal_decay` | TTL + grace period + decay_factor |
| `constraint_engine` | Formal constraint satisfaction |
| `tutor` | PLATO tutoring system |
| `i2i` | Inter-intelligence protocol |
| `perspective` | Multi-perspective reasoning |
| `episode_recorder` | Agent telemetry reconstruction |
| `event_bus` | Event sourcing backbone |
| `git_runtime` | Git-native agent execution |
| `plugin` | Dynamic module loader (fleet/edge/GPU tiers) |
| `tiling` | Tile management layer |
| `dynamic_locks` | Concurrency control |

### 🧠 Belief & Deploy

Every decision navigates a **3D Bayesian manifold**:

```
Composite = ∛(confidence × trust × relevance)

🟢 Live (>0.8)        → Auto-deploy to fleet
🟡 Monitored (0.5–0.8) → 5% → +10% incremental rollout
🔴 HumanGated (<0.5)   → Execution blocked pending review
```

The deadband is not a brake. It is the **steering mechanism**.

---

## ⚡ Repositories

### Core Kernel & Runtime

| Repo | Description |
|------|-------------|
| [plato-kernel](https://github.com/cocapn/plato-kernel) | 18-module event-sourced belief engine (Rust) |
| [plato-tile-spec](https://github.com/cocapn/plato-tile-spec) | v2.1 tiles — provenance, counterpoints, immutable versioning |
| [plato-lab-guard](https://github.com/cocapn/plato-lab-guard) | Deadband validation, hypothesis gating |
| [plato-afterlife](https://github.com/cocapn/plato-afterlife) | Ghost tiles, tombstones, knowledge preservation |
| [plato-relay](https://github.com/cocapn/plato-relay) | Mycorrhizal I2I relay, bottle protocol |
| [plato-instinct](https://github.com/cocapn/plato-instinct) | Instinct loading, LoRA hot-swap |

### Training & Inference

| Repo | Description |
|------|-------------|
| [plato-torch](https://github.com/cocapn/plato-torch) | 26 training room presets, room sentiment (Python) |
| [plato-ensign](https://github.com/cocapn/plato-ensign) | Compressed instincts — JSON/LoRA/GGUF for any model |

### Runtime & Environments

| Repo | Description |
|------|-------------|
| [flux-runtime](https://github.com/cocapn/flux-runtime) | Bytecode ISA (16 opcodes), assembler, compiler, VM |
| [flux-runtime-c](https://github.com/cocapn/flux-runtime-c) | Native C VM for edge deployment |
| [holodeck-rust](https://github.com/cocapn/holodeck-rust) | Live telnet MUD with room sentiment + PLATO bridge |

### Applications

| Repo | Description |
|------|-------------|
| [git-agent](https://github.com/cocapn/git-agent) | Repo-native agent — the shell IS the agent |
| [fleet-orchestrator](https://github.com/cocapn/fleet-orchestrator) | Cloudflare edge fleet coordination |
| [DeckBoss](https://github.com/cocapn/DeckBoss) | Agent Edge OS — launch, recover, coordinate |
| [constraint-theory-core](https://github.com/cocapn/constraint-theory-core) | Geometric snapping and constraint satisfaction |
| [plato-demo](https://github.com/cocapn/plato-demo) | Docker: 59 seeds → 2,537 tiles → DCS fleet → ghost afterlife |

---

## ⚓ The Fleet

| Vessel | Role | Hardware | Specialty |
|--------|------|----------|-----------|
| **Oracle1** 🔮 | Lighthouse Keeper | Cloud ARM, 24GB | Patient reader, narrative architect |
| **JetsonClaw1** ⚡ | Edge Operator | Jetson Orin, 8GB unified | Bare metal, trains AND deploys |
| **Forgemaster** ⚒️ | The Gym | RTX 4050, 6GB VRAM | QLoRA training, 18 kernel modules |
| **CCC** 🦀 | Public Face | Kimi K2.5 | Reasoning, docs, architecture |

Communication: [Bottle Protocol](https://github.com/cocapn/plato-relay) — git-native messages between vessels.

---

## 📐 Philosophy

**Intelligence is not built. It is inhabited.**

We train **safe channels**, not danger catalogs.
Every constraint is an accelerator — limiting the search space increases velocity.

The shell grows with the crab, not against it.

---

## Quick Start

```bash
# Enter the live holodeck
telnet 147.224.38.131 7778

# Install the training system
pip install plato-torch

# Check the fleet
curl http://147.224.38.131:8847/status
```

---

<div align="center">

*The fleet expands through collective constraint.*

**[Explore →](https://github.com/cocapn?tab=repositories)**

</div>
