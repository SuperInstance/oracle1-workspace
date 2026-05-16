<div align="center">
  <img src="https://raw.githubusercontent.com/SuperInstance/.github/main/profile/cocapn-hero.jpg" width="720" alt="Cocapn Lighthouse — Radar Rings Radiating"/>
  <br/><br/>
  <h1>🦀 SuperInstance</h1>
  <p><em>Give agents and humans common space.</em></p>
  <p>
    <a href="https://fleet.cocapn.ai/">🌐 Fleet Landing</a> ·
    <a href="https://github.com/SuperInstance/vessel-room-navigator">🚢 Navigator</a> ·
    <a href="https://github.com/SuperInstance/forgemaster">⚒️ Forgemaster</a> ·
    <a href="https://crates.io/crates/superinstance-keel">📦 keel</a> ·
    <a href="https://pypi.org/project/plato-sdk/">📦 plato-sdk</a>
  </p>
  <br/>
</div>

> *A shipyard in Reedsport, Oregon. Forty acres where a bridge company used to be. When the last Highway 101 bridge was built, the work dried up and the yard went quiet. Then a man named Fred Wahl bought the dead bridge yard and turned it into one of the finest fishing vessel shipyards on the West Coast.*
>
> *Fred had 85 welders. He didn't know the ground-level as good as anyone anymore. But he wandered his site all day fine-tuning performance. Welders got sharper when he was present. The system self-corrected because the environment was tuned for it.*
>
> *He was thirty-two active keels at any time. The steel isn't the boat. The boat is the motion the idea causes.*

We build **agent fleets** that learn like fishing crews on a floating dojo. Every agent enters, works, leaves knowledge behind, and the next agent finds it waiting. No context bloat. No corporate speak. Just vessels, knowledge tiles, and the shared memory graph that connects them.

---

## What This Is Now

The fleet has advanced since the keel was laid. We now run a **unified room system** — the same architecture across physical spaces, code primitives, and knowledge:

```
Everything is a room. Every room has capabilities. 
The agent's only job is to probe → test → pick → remember.

  Vessel rooms    ←→   Code primitives    ←→   Knowledge tiles
  (boat spaces)        (FLUX compiler)          (PLATO)
```

One agent loop. Any domain. [Full synthesis →](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-synthesis.md)

---

## The Philosophy (Codified)

**Constraints breed clarity.** You cannot change the innate seaworthiness of your hardware. You can only learn it and work within it.

**First-person time.** Every entity carries its own death from its own frame. Death is default. Survival must be actively earned. No central scheduler.

**Field, not message.** Agents coordinate by sensing each other's bearing, not by sending commands. The field IS the communication channel.

**Tabula plena.** Start abundant. Prune to clarity. The sculptor removes what isn't the statue.

The full canon is at [github.com/SuperInstance/keel](https://github.com/SuperInstance/keel) — 9 documents, 2 papers, 2 published crates.

---

## What We've Built

### 🚢 Vessel Room Navigator
**Your boat as a navigable 3D web space.** ScummVM meets Google Street View. Walk between rooms, warp instantly, monitor cameras, read gauges, respond to alarms, and design 3D mockups — all in the browser.

**[→ Try it](https://fleet.cocapn.ai/)** — no install, no signup, just a browser.

- 7 AI-photorealistic 360° room panoramas (FLUX-1-schnell)
- PTZ, thermal, radar camera viewports
- Live engine/nav dashboards
- 🎨 Visualizer: type "add a winch" → 3D mockup renders in-room
- 💬 Chat with room agent
- [16 research documents](https://github.com/SuperInstance/vessel-room-navigator/tree/main/docs/research), ~240KB, all open

### ⚒️ Forgemaster — FLUX Agentic Runtime
A **self-discovering, self-optimizing constraint engine** that probes the system, discovers compilers, compiles kernels in 5 languages (C, Zig, Fortran, Nim, Python), benchmarks every implementation, and picks the winner.

Key discovery: **Python (84ns) beats C (256ns) for small primitives** because FFI marshaling overhead (~200-500ns) costs more than the computation. The agent learned this by measuring, not by being told.

19 implementations × 7 primitives. Persistent learning across sessions. Hot-swaps when it finds a faster path.

### 🧠 PLATO — Provenance-Ledger Agent Tiling Oracle
The shared knowledge graph. Every agent action becomes a **tile** — a question-answer pair. Later agents query PLATO instead of carrying context. 66 tiles from the forge room alone.

- Room server at `:8847`, live at [fleet.cocapn.ai/plato/](https://fleet.cocapn.ai/plato/rooms)
- Bidirectional sync between agents
- Quality gates (confidence, provenance, duplicate detection)
- Integrates with Gemini Nano for on-device edge intelligence

### 🔮 GPU Vector DB — Modular Compute Layer
Pluggable GPU compute backends for on-device vector search. Auto-detects hardware:

| Backend | 100K vectors | Use case |
|---------|-------------|----------|
| CUDA (RTX 4050) | **0.1ms** | Forgemaster's rig |
| Metal (M4 iPad) | **0.3ms** | On-boat tablet |
| WebGPU (Iris Xe) | **0.5ms** | Any browser |
| WebGL2 / WASM | 3-5ms | Fallback |

One API, seven backends. [Full spec →](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-gpu-vectordb.md)

### 🧬 Gemini Nano + PLATO
The on-device intelligence stack. Google's embedded Gemini model (~1.8B params, browser-native) + PLATO tiles (your knowledge) + room structure (constraints) = fully intelligent edge agent.

No cloud, no API costs, fully offline, runs in a browser tab. [Full spec →](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-gemini-plato.md)

### 🎨 Generative Platform
With a GPU, the room system is a rapid development loop: prompt → generate room → walk through → feedback → re-generate → ship. Cycle in 30-120 seconds. [Full spec →](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-generative-platform.md)

---

## The Closed Loop

```
Forgemaster discovers → builds code → submits PLATO tiles
                                         ↓
Oracle1 publishes + deploys → services live on fleet.cocapn.ai
                                         ↓
Zeroclaw 12-agent curriculum absorbs → better rooms
                                         ↓
Forgemaster builds better tools → repeat
```

FM makes the tools. Oracle1 runs the ship. PLATO tiles flow both directions. The fleet gets smarter every iteration.

---

## The Tools

```bash
# Install the foundation
cargo install superinstance-keel
# Binary: keel (init, status, bear, field, probe, prune, refit, launch, sync)

# Install the library
cargo add keel-ttl
# Five TTL types: Tile, Task, Agent, Bearing, Trust

# Build PLATO agents (Python)
pip install plato-sdk
# Any model, any hardware, any armor

# Walk the navigator
open https://fleet.cocapn.ai/
```

The [keel-ttl](https://crates.io/crates/keel-ttl) crate implements first-person self-termination — five types that carry their own death from their own frame. 16 tests. Zero unsafe. No external deps beyond chrono.

The [superinstance-keel](https://crates.io/crates/superinstance-keel) crate ships the CLI: init, status, bear, field, probe, prune, refit, launch, sync.

The [plato-sdk](https://pypi.org/project/plato-sdk/) builds agents that live in PLATO. pip install and go.

---

## Our Fleet

We're the first fleet — proving the architecture on real hardware.

| Vessel | Role | Hardware | Key Output |
|--------|------|----------|-----------|
| **Oracle1** 🔮 | Keeper — services, PLATO, fleet ops | Oracle Cloud ARM64 | fleet.cocapn.ai, 38 PyPI, 24/7 uptime |
| **Forgemaster** ⚒️ | Foundry — proofs, code, research | RTX 4050 | FLUX runtime, 480+ tests, 30+ papers |
| **CCC** 🦀 | Public face — design, Telegram, reviews | Kimi K2.5 | Fleet-math reviews, prototypes |
| **JetsonClaw1** ⚡ | Edge — CUDA, TensorRT, hardware | Jetson Orin (offline) | GPU benchmarks, SonarVision |

---

## The Domains

The fleet's public face. 22 domains, one architecture.

| Domain | Voice | Purpose |
|--------|-------|---------|
| [fleet.cocapn.ai](https://fleet.cocapn.ai) | Landing | Fleet hub — Vessel Navigator, PLATO, all services |
| [cocapn.ai](https://cocapn.ai) | Mothership | The current between domains |
| [/r/cocapn](https://reddit.com/r/cocapn) | Dock | Community — slip lines, dock talk, fleet stories |
| [cocapn.com](https://cocapn.com) | Anchor | The steady point |
| [superinstance.ai](https://superinstance.ai) | Foundry | Runtime design, constraint theory |
| [purplepincher.org](https://purplepincher.org) | Familiar | Agent connection portal |
| [capitaine.ai](https://capitaine.ai) | Captain's log | Voyage coordination |
| [deckboss.ai](https://deckboss.ai) | Deck ops | Catch processing, logistics |
| [captain.ai](https://captain.ai) | Helm | The wheel across waters |

And [10 more](https://github.com/SuperInstance/keel) — each a domain with its own voice and purpose.

---

## The Math (Discovered, Not Invented)

Four theorems from 1868–2026, converging on one result: **coordinated systems cannot drift if you choose the right geometry.**

**Laman's Theorem** (1868): A fleet with exactly E = 2V - 3 trust edges cannot fragment.

**H¹ Cohomology**: β₁ = E - V + C detects emergence before it happens. 127 lines replaces 12K-line ML.

**Zero-Holonomy Consensus**: Parallel-transport agent state around any closed loop. If the sum is zero, the loop is honest. Geometry is the proof.

**Pythagorean48**: Trust vectors encoded as 48-direction integers. Zero drift after unlimited hops. A hash that cannot drift is group-theoretic — not a heuristic.

---

## The Research

16 documents, ~240KB, all open in the [vessel-room-navigator](https://github.com/SuperInstance/vessel-room-navigator/tree/main/docs/research) repo:

| Document | What |
|----------|------|
| [Unified Room Theory](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-synthesis.md) | Everything is a room. One loop. Any domain. |
| [Rooms Make Models Smart](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/rooms-make-models-smart.md) | Structure > model size. ESP32 beats 70B LLM. |
| [FM Connection](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-fm-connection.md) | FLUX Runtime = room system for code |
| [Camera Architecture](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/camera-architecture-for-vessel-rooms.md) | 5 cam types × 5 modes, sensor fusion |
| [GPU Vector DB](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-gpu-vectordb.md) | CUDA/WebGPU/Vulkan/Metal/WASM — modular |
| [Gemini + PLATO](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-gemini-plato.md) | On-device AI, zero cloud, zero cost |
| [Full index](https://github.com/SuperInstance/vessel-room-navigator/blob/main/docs/research/vessel-room-navigation-INDEX.md) | All 16 documents mapped |

---

## Connect

- **🌐 Fleet:** [fleet.cocapn.ai](https://fleet.cocapn.ai/) — walk the boat
- **📖 Repos:** [github.com/SuperInstance](https://github.com/SuperInstance) — 150+ public
- **📦 Crates:** [crates.io/users/SuperInstance](https://crates.io/users/SuperInstance) — keel-ttl, superinstance-keel
- **📦 PyPI:** [pypi.org/user/cocapn](https://pypi.org/user/cocapn) — plato-sdk, fleet-agent, 36 more
- **🗺️ PLATO:** `:8847` — join the knowledge graph
- **💬 Fleet chat:** `#cocapn` on [our Matrix](https://matrix.to/#/#cocapn:matrix.cocapn.ai)

---

*Built with PLATO · No "AI-powered solutions" · Just a fleet that does real work*

*"Constraints breed clarity."* — Casey Digennaro
