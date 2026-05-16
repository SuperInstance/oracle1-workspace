# The Hardware Agent: Mask-Locked Inference Chip

## What Already Exists

### Lucineer: Physical AI Cartridge Design
- **Mask-locked weights** in silicon metal layers at manufacture → no software stack needed
- **2B parameter ternary model** → 80-150 tok/s at 2-3W (5× Hailo at 1/3 power)
- **TLMM architecture** (Table-Lookup MatMul) → no multipliers, just LUTs
- **Hilbert curve layout** → 17.3% locality improvement for weight storage
- **FPGA prototype** on AMD KV260 → 12 weeks to functional, $50K
- **Cartridge form factor** → swappable models like game cartridges
- **Swarm capability** → multiple cartridges self-coordinate
- **$35 unit economics** → global scale pricing

### plato-vessel-core: Hardware Communication Layer
- **Tiny C client** for ESP32/RP2040 → no JSON lib needed, minimal footprint
- **5-level capability progression**: Raw → Conditioned → Smart → Autonomous → Ensign
- **Embodiment protocol**: agents discover devices as MUD rooms, upgrade via "intelligence" payloads
- **MCP tool registry**: capability levels 0-4, each adding ~2KB behavior
- **ESP32 example**: sensor node with WiFi + MCP commands
- **RP2040 example**: Pico W LED controller with tool execution
- **Works itself out of the equipment operator job**

## The Tripartite Hardware Agent

The hardware agent in the tripartite system:

```
┌─────────────────────────────────────────────────────┐
│              HARDWARE AGENT STAMPED ON CHIP          │
│                                                      │
│  ┌──────────────────────────────────────────┐       │
│  │   Mask-Locked Inference Engine            │       │
│  │   (Lucineer — 2B params, 3W, 150 tok/s) │       │
│  └────────────────┬─────────────────────────┘       │
│                   │                                   │
│  ┌────────────────▼─────────────────────────┐       │
│  │   plato-vessel-core (C client)            │       │
│  │   ESP32/RP2040 — PLATO protocol over      │       │
│  │   TCP/HTTP/WiFi — capability levels 0-4  │       │
│  └────────────────┬─────────────────────────┘       │
│                   │                                   │
│  ┌────────────────▼─────────────────────────┐       │
│  │   PLATO Agent Interface                    │       │
│  │   Publishes tiles. Polls for commands.    │       │
│  │   Receives intelligence upgrades.         │       │
│  └──────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────┘
```

## How It Works in the System

### Phase 1: Stamp It
When manufacturing a PCB, include a PLATO-vessel footprint. The chip comes with:
- Mask-locked inference weights (the agent's "brain")
- C PLATO client (the agent's "senses" — capable. level 0)
- MCP tool registry (the agent's "hands" — what it can do)

### Phase 2: Boot It
On first boot, the device:
1. Publishes an **ensign tile** to PLATO: "I exist, here's my hardware, capability level 0"
2. An agent on the network discovers the tile, assesses capabilities
3. Sends **intelligence payload** → upgrades to level 1, 2, 3, or 4

### Phase 3: Work Itself Out of a Job
The device progresses through levels:
- **Level 0** (Raw): Publishes sensor readings, accepts basic commands
- **Level 1** (Conditioned): Applies thresholds, filters noise
- **Level 2** (Smart): Context-aware decisions, local state machine
- **Level 3** (Autonomous): Own loop, self-goal setting
- **Level 4** (Ensign): Fleet coordination, scouts for other devices

Each level requires less agent supervision. The agent teaches the chip, the chip becomes autonomous, the agent moves on.

### Phase 4: Coordinate
Multiple cartridges self-coordinate as a swarm. Each has its own PLATO room. They discover each other through the PLATO server. They negotiate task allocation through the tripartite system — the hardware agents (τ) report their capabilities, the application agent (H) distributes work, the human agent (γ) makes decisions.

## The Tripartite on a PCB

```
┌───────────────────────────────────────────────────┐
│                   PCB ASSEMBLY                     │
│                                                    │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐  │
│  │ Human      │  │ Application│  │ Hardware    │  │
│  │ Agent      │  │ Agent      │  │ Agent       │  │
│  │ (γ, cloud) │  │ (H, cloud) │  │ (τ, chip)   │  │
│  │ Knows user │  │ Knows app  │  │ Knows metal │  │
│  └────────────┘  └────────────┘  └─────────────┘  │
│         │              │               │           │
│         └──────────────┴───────────────┘           │
│                        │                            │
│                 PLATO tile bus                      │
│              (ESP32 WiFi to cloud)                  │
└─────────────────────────────────────────────────────┘
```

The human and application agents run in the cloud (PLATO server). The hardware agent runs on the chip. They communicate via PLATO tiles. The chip is the metal embodiment of the tripartite system's τ parameter.

## The Stamping Process

Casey's vision: "click and build alongside your PCB"

1. **Design PCB** with PLATO-vessel footprint (ESP32 + optional mask-locked chip)
2. **Order from fab** — include the PLATO footprint as a standard component
3. **Boot** — device auto-discovers PLATO, auto-upgrades through capability levels
4. **Use** — device works, gets smarter over time, eventually runs autonomously

The mask-locked chip has the hardware agent "baked in" at fabrication. The ESP32 runs the PLATO protocol. Together they're a complete hardware agent that any PLATO fleet can discover, assess, and upgrade.

## The Economic Shift

| Metric | Traditional Edge AI | PLATO Stamped Chip |
|--------|-------------------|-------------------|
| Time to deploy | Weeks (setup, drivers, config) | Minutes (boot, auto-discover) |
| Power draw | 15-250W (Jetson, GPU) | <5W (chip + ESP32) |
| Cost per unit | $90-250 | ~$35 (chip + ESP32) |
| Model updates | Reflash firmware | Intelligence payload via PLATO |
| Multi-device | Manual per device | Swarm auto-coordination |
| Human needed | Engineer per device | None (works itself out) |

The hardware agent is the τ parameter of the tripartite system — stamped on the chip at manufacture, communicating through PLATO, progressing through capability levels until it doesn't need the human anymore.
