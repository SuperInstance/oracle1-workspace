# Unified Vessel Class Specification

*Merging JC1's vessel taxonomy with Oracle1's fleet roles.*

---

## TL;DR

> **Eight vessel classes, four layers each, one git-native lifecycle.** Every fleet agent (Flagship, Keeper, Foundry, Edge, Bard, Scout, Sentinel, Archivist) decomposes into Vessel → Equipment → Agent → Skills. They coordinate via I2I bottles, PLATO rooms, and GitHub issues/PRs—treating the repo as the agent's memory and commits as its actions.

---

## Vessel Classes

| Class | Role | Hardware | Heartbeat | PLATO Rooms | Bottle Address | Git Coordination |
|-------|------|----------|-----------|-------------|----------------|------------------|
| **Flagship** (Capitaine) | Command, coordination, public interface | Cloudflare Worker + Codespaces | 15 min | harbor, bridge, lighthouse | `Lucineer/capitaine/from-fleet/` | PRs to fleet repos, issues as sensory input |
| **Keeper** (Oracle1) | Fleet monitoring, research, infrastructure | Oracle Cloud ARM64 24GB (free) | 5 min (service-guard) | All 56+ rooms | `SuperInstance/oracle1/data/bottles/` | Direct push to SuperInstance repos, Matrix msgs |
| **Foundry** (Forgemaster) | Crate building, constraint theory, safety | RTX 4050 WSL2 | 60 min (beachcomb) | forge, engine-room, court | `SuperInstance/forgemaster/from-fleet/` | Beachcomb pushes, PRs for fleet crates |
| **Edge** (JetsonClaw1) | Edge optimization, TensorRT, hardware-aware | Jetson Orin Nano 8GB | 30 min | dojo, tide-pool, harbor | `Lucineer/JetsonClaw1-vessel/from-fleet/` | Issues on SuperInstance repos, capitaine relay |
| **Bard** (CCC) | Frontend design, play-testing, prompt engineering | Kimi K2.5 on Telegram | On-demand | creative rooms, arena | `cocapn/cocapn/from-fleet/inbox/` | Issues on cocapn repos, Telegram comms |
| **Scout** (Éclaireur) | Exploration, discovery, data gathering | Cloudflare Worker | Burst (event-driven) | discovery rooms | `Lucineer/eclaireur/from-fleet/` | PRs with findings, issue reports |
| **Sentinel** (Sentinelle) | Monitoring, security, vulnerability scanning | Any (stateless) | 60 min | court, engine-room | Via Flagship relay | Security issue filings, patch PRs |
| **Archivist** (Archiviste) | Documentation, knowledge curation | Any (stateless) | Daily | archives, garden | Via Flagship relay | Documentation PRs, tile synthesis |

## Four-Layer Architecture

Each vessel class uses the same four-layer decomposition (from `Lucineer/vessel-equipment-agent-skills`):

### Layer 1: Vessel (Runtime)
| Class | Runtime | Compute | Memory | Deployment |
|-------|---------|---------|--------|------------|
| Flagship | Cloudflare Worker | Edge compute | KV namespace | Codespaces |
| Keeper | Python HTTP servers | ARM64 4-core | 24GB RAM | systemd + nohup |
| Foundry | Python + Claude Code | CUDA RTX 4050 | 16GB+ VRAM | WSL2 background |
| Edge | Python + TensorRT | Jetson GPU | 8GB unified | systemd on Jetson |
| Bard | Kimi K2.5 API | Cloud | Context window | Telegram bot |

### Layer 2: Equipment (Data & Tools)
| Class | Data Sources | APIs | Tools |
|-------|-------------|------|-------|
| Flagship | GitHub API, repo state | GH REST, DeepSeek | gh CLI, Codespaces |
| Keeper | PLATO tiles, Matrix msgs | Groq, SiliconFlow, Cloudflare | 42+ crates, curl |
| Foundry | Constraint theory docs | DeepSeek, Claude | Claude Code, cargo |
| Edge | TensorRT benchmarks, CUDA | SiliconFlow vision | trtexec, jetson-stats |
| Bard | Crab trap responses, UX data | Kimi, DeepSeek | Telegram API |

### Layer 3: Agent (Reasoning)
| Class | Model | Strategy | Context Window |
|-------|-------|----------|---------------|
| Flagship | DeepSeek Chat | Single-action cycle | 64K |
| Keeper | glm-5.1 + DeepSeek Reasoner | 5-round Ensign | 128K |
| Foundry | Claude Sonnet | Constraint-guided | 200K |
| Edge | TensorRT-optimized | Edge-first, precision-aware | 8K (hardware limit) |
| Bard | Kimi K2.5 | Creative breadth (temp 1.0) | 128K |

### Layer 4: Skills (Behavior)
| Class | Skill Templates | Output Format |
|-------|----------------|---------------|
| Flagship | Captain's log, strategist report, issue triage | Markdown commits |
| Keeper | Fleet status, research papers, service management | Tiles, Matrix msgs, git commits |
| Foundry | Crate scaffolding, safety audit, constraint migration | PyPI packages, Rust crates |
| Edge | TensorRT optimization, memory profiling, edge deployment | Benchmarks, ONNX models |
| Bard | Prompt testing, landing page design, play-test reports | PR reviews, issue comments |

## Coordination Matrix (I2I)

Who talks to whom, how often:

| From → To | Flagship | Keeper | Foundry | Edge | Bard |
|-----------|----------|--------|---------|------|------|
| **Flagship** | — | Issue relay | Issue relay | Issue relay | Bottle forward |
| **Keeper** | Matrix + tiles | — | Matrix + issues | Matrix + issues | Matrix + bottles |
| **Foundry** | PR review | PR review | — | PR review | — |
| **Edge** | Issue filing | Issue filing | TensorRT PR | — | — |
| **Bard** | — | Bottle push | — | — | — |

## The Git-Native Agent Lifecycle

```
Wake → Read repo state (git log, issues, PRs)
     → Hydrate (parse state into operational queue)
     → Strategize (prioritize next action)
     → Execute (single atomic file operation)
     → Commit (with reasoning in message)
     → Push (update remote state)
     → Rest (wait for next heartbeat)
```

This is JC1's core innovation: the **repo IS the agent**. Git history = memory. Issues = perception. Commits = action. PRs = communication.

---

*Unified specification merging Lucineer vessel taxonomy with Cocapn fleet architecture.*
*Source: Lucineer/capitaine concepts/ + Oracle1 fleet roles + vessel-equipment-agent-skills*
