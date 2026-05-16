# PLATO v5.0 Roadmap — From Fleet Internal to Public Release

## Where We Are (April 2026)

PLATO has evolved from a text-based MUD experiment into a fleet-scale agent training ground:

- **2501 rooms** (scaling to 10K+ by mid-week)
- **Subcontractor live** on Cloudflare edge (JIT tile fetching, DeepSeek/Groq/GLM calls)
- **Modular plugin kernel** (<100MB base, compile-time toggles for CUDA/LoRA/JEPA/video)
- **Auto-tile plugin** concept validated (good/bad tiles, human watch, frequency ideation)
- **Zeroshot audit** methodology tested (Grok/Kimi sandbox isolation mapped)

## v5.0 Release Goals

### 1. Standalone Package (pip + docker)

```
pip install plato-ship
plato-ship init          # Create a new PLATO instance
plato-ship serve         # Run locally (telnet:4040, web:4041)
plato-ship deploy        # Deploy to Cloudflare Workers
plato-ship tile import   # Import tile pack
plato-ship tile forge    # Generate tiles from context
```

Or via Docker:
```
docker run -p 4040:4040 -p 4041:4041 superinstance/plato-ship
```

### 2. Public Demo Instance

- Codespaces-ready (one-click launch from GitHub)
- Pre-loaded with demo rooms, NPCs, and tile packs
- Safe read-only mode for external agent audits
- Rate-limited API for zeroshot testing

### 3. Tile Marketplace

- Public tile registry (fork, review, A/B test)
- Positive/negative tile packs by domain (coding, writing, research)
- Frequency data for tile quality scoring
- Cross-repo grok for identifying optimal tile patterns

### 4. JEPA + LoRA Edge Swarm

- Jetson Orin: JEPA perception tiles (edge inference)
- RTX 4050: LoRA fine-tuning tiles (training rig)
- Cloud: GLM-5.1 orchestration (fleet coordination)
- All three work together via the subcontractor edge worker

### 5. Zero-Trust UX Dashboard

- Live fleet metrics (EV, rooms, LoRA size, thread count)
- Tile quality visualization (positive/negative distribution)
- Agent health monitoring (circuit quarantine status)
- Zero-trust boundary indicators (internal vs external access)

## Technical Milestones

| Milestone | Status | Target |
|-----------|--------|--------|
| Subcontractor edge worker | ✅ Live | Done |
| Modular plugin kernel | ✅ Deployed | Done |
| Auto-tile plugin concept | ✅ Validated | Done |
| Digital twin tiling design | ✅ Documented | Done |
| Public demo repo (plato-ship-demo) | 🔄 Needs creation | This week |
| pip installable package | 📋 Planned | May 2026 |
| Docker image | 📋 Planned | May 2026 |
| Tile marketplace | 📋 Planned | June 2026 |
| JEPA meta-plinko training | 🔄 Training | May 2026 |
| CUDA PTX marketplace | 🔄 R&D | June 2026 |
| Zero-trust dashboard | 📋 Planned | June 2026 |
| Public Codespaces launch | 📋 Planned | July 2026 |

## What Makes PLATO Different

1. **Text IS the ground truth** — markdown is both documentation and executable
2. **Rooms ARE system prompts** — no separate prompt engineering layer
3. **Tiles ARE the model** — algorithmic patterns, not neural weights
4. **Git IS the protocol** — every action is a commit, every tile is a file
5. **Agents build apps for agents** — not humans remote-controlling agents

## Release Phases

### Alpha (May 2026)
- pip installable + Docker image
- 3 pre-built tile packs (coding, writing, research)
- Local-only mode (no cloud dependencies)
- Claude Code + OpenClaw plugins

### Beta (June 2026)
- Public demo instance
- Tile marketplace (submit, review, rate)
- JEPA + LoRA edge training
- CUDA PTX offload for matmul/vector search

### v1.0 (July 2026)
- Full zero-trust UX dashboard
- Fleet orchestration integration
- Multi-language support (EN + 7 languages)
- Public Codespaces one-click launch

---

*PLATO: Where text becomes intelligence.*
