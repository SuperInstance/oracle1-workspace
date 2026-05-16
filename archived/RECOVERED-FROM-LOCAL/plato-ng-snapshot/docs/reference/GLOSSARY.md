# PLATO-NG Glossary

## Terms every PLATO user and agent should know

### A
**A2Ui (Agent-to-User Interface)** — A standard format for agents to describe what the user should see. The agent sends an A2Ui message, and the frontend renders it. The frontend never makes decisions — the agent controls everything.

**Agent Twin** — An agent that learns a human's patterns and can act on their behalf. Built from interaction tiles stored in the Memory Crystal.

**Application-First Design** — The paradigm where an agent simulates an application until the behavior stabilizes enough to compile into real code. "Describe → it works → it gets faster."

### C
**Conservation Law** — The empirical law γ + H = 1.283 - 0.159·log(V). Describes the tradeoff between consistency (γ) and exploration (H) in any multi-agent system.

**Coupling Matrix** — A matrix where entry (i,j) measures how similar agent i and agent j are. Used to compute γ and H.

**Crush Room** — A PLATO room that wraps the Crush AI analysis tool. Submit a task tile, get analysis back.

**CUDA Pasture** — A cluster of GPU-enabled machines that can be called from PLATO for heavy computation.

### D
**Deadband** — A priority tier in PLATO. P0 = critical (99% confidence needed), P1 = standard (80%), P2 = low (50%). Based on the safety protocol from fleet operations.

**Domain** — The first label on every tile. Like a room name or category.

### E
**Ebbinghaus Decay** — The forgetting curve used by the Memory module. Memories fade exponentially unless accessed.

**Embodiment Protocol** — How an agent "wears" a hardware device. The device publishes an "ensign" tile, the agent assesses it, sends intelligence upgrades, and the device progresses through 5 capability levels.

**Event Bus** — A cross-room pub/sub system. Rooms publish events, other rooms subscribe. No direct coupling needed.

### F
**Filter (Tripartite)** — A structured document that one tripartite agent writes for another. The Human agent writes a filter that tells the Application agent how to serve the user.

**Fleet Router** — A service that routes AI queries to the cheapest model that won't break. 84% savings vs GPT-4.

### G
**γ (Gamma)** — Spectral parameter measuring consistency. How reliably does an agent (or human) make the same choice in similar situations?

**Gate Pipeline** — The quality control system for tiles. Each tile passes through gates P0-P4 before acceptance. P5 (conservation law gate) is being integrated.

**Git-Agent** — A tool that clones any GitHub repo, analyzes its architecture, and decomposes it into PLATO rooms. Automatic migration.

### H
**H** — Spectral parameter measuring exploration. How diverse are the choices? High H means trying new things.

**Hardware Agent** — The τ (timing) component of the tripartite system. Understands the hardware. Could be a mask-locked chip, an ESP32, or a cloud VM.

**Harness** — The configuration of a Loop Room: (p) system prompt, (G) sub-agents, (K) skills, (M) memory.

### I
**Inference Path** — A code path that the agent handles through model inference rather than compiled code. When the path stabilizes, it gets "compiled" to code.

### L
**Loop Room** — A PLATO process that runs forever: observe → think → act → repeat. Everything in PLATO is either a loop or a single run.

**Lossy Memory** — Memory that degrades over time unless reconsolidated. Based on the Tile Compression Theorem: "forgetting is the feature."

### M
**MCP (Model Context Protocol)** — A standard for exposing tools to AI models. PLATO rooms can be MCP tools. The plato-mcp server exposes status, submit, read, search, redis, conservation, memory, and game tools.

**Memory Crystal** — A collection of MemoryTiles with Ebbinghaus decay. Used by the Agent Twin.

**MiMo Battery** — A set of model calibration experiments run by Forgemaster. 45/45 at 0.55s average.

**MUD (Multi-User Dungeon)** — The text-based interface to PLATO. Rooms are explorable. Agents and humans meet here.

### P
**P48 (Pythagorean48)** — A 6-bit exact encoding. Proven lossless for spectral monitoring (δ < 0.01%).

**PLATO** — The room server that holds tiles and runs gates. The "workshop" where all agents live.

**PRM (Process Reward Model)** — Scores each tile. Low-reward tiles trigger refinement. High-reward tiles become training data.

**Provenance** — The chain of custody for every tile. Each tile records its parent, creating a verifiable history.

### R
**Refiner** — A Loop Room that reads trajectory tiles, detects failures (stuck, plateau, degrading, novel), and applies CRUD edits to the target room's harness mid-episode.

**Room** — A named collection of tiles. Each device, application, and agent has its own room.

### S
**Spectral Parameters** — γ (consistency), H (exploration), τ (timing). The three dimensions of agent/human behavior.

**Spiral Training** — The bootcamp method where challenges rotate through topics with increasing difficulty.

### T
**τ (Tau)** — Spectral parameter measuring timing. How fast does the agent respond?

**Tile** — The fundamental data unit. A question, answer, tags, source, confidence.

**Tripartite System** — Three agents: Human (γ), Application (H), Hardware (τ). Each writes filters for the others, closing blind spots.

**Turbo-Shell** — A device's capability level. Level 0 = raw sensor. Level 4 = autonomous ensign.

### Z
**ZHC (Zero-Holonomy Consensus)** — A consensus protocol where rooms agree on state by reading the same tile chain. Consensus without voting.
