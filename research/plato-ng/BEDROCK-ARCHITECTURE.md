# PLATO-NG: Bedrock Map & Piling Design

## PART 1: THE BEDROCK (What doesn't change)

These are the invariants. Everything else is a piling driven into them.

### Invariant 1: Conservation Law
**γ + H = 1.364 - 0.159·log(V)**
Mathematical bedrock. Holds across all coupling types, topologies, fleet sizes. Every design decision must preserve this.

### Invariant 2: Canonical Decomposition
**Fleet state = Topology × Style × Timing**
Three independent manifolds. Topology → connectivity (γ). Style → diversity (H). Timing → response (τ). Each is independently controllable. This is the structural bedrock.

### Invariant 3: BEAM Actor Model
Every PLATO room is a process. Every tile is a message. Every human gets a supervision tree. This is the runtime bedrock — it doesn't change whether on a single ARM core or a CUDA pasture.

### Invariant 4: MUD-as-Face
Humans interact with PLATO through explorable spaces. The same PLATO data renders as MUD rooms, visual games, or dashboards. The data is the same; the surface adapts to the human.

### Invariant 5: Human Casting Call
Every human has a spectral signature (γ_self, H_self, τ_self) learned through interaction. The system adapts to this human's specific blend. Not "a human" — **this** human.

---

## PART 2: THE LANGUAGES AS PRECALCULATED SOLUTIONS

Each language exists because a specific set of problems needed solving. The system selects the right one per operation:

| Language | Precalculated For | When PLATO Chooses It |
|----------|------------------|----------------------|
| **Gleam** | BEAM concurrency + Rust type safety | Router, room state, message dispatch, supervision |
| **Elixir/Erlang** | BEAM processes when type safety is less critical | Legacy rooms, human I/O, MUD telnet |
| **Rust** | Memory safety + zero-cost abstractions | NIFs for matrix ops, spectral analysis, CUDA dispatch |
| **C** | FFI compatibility + hardware drivers | BLAS/LAPACK calls, OS-level integration, embedded targets |
| **CUDA** | GPU vector parallelism | Large matrix eigendecomp, batch spectral analysis |
| **FLUX (GUARD)** | Formally verifiable constraints | Tile validation gates, game logic certification |
| **Mojo** | MLIR compilation + Python ecosystem | Prototyping new algorithms, ML inference |
| **Lua** | Embeddable scripting | TIC-80/LÖVE2D game logic, user-modifiable behavior |

The system doesn't "choose a language" — it chooses an **operation** and the precalculated solution for that operation is already there, compiled and ready. The router dispatches to the appropriate backend at runtime.

---

## PART 3: THE PILINGS (Locking into Bedrock)

### Piling 1: Hardware Abstraction Layer

On startup, the system probes available capabilities and selects backends:

```
Boot Sequence:
1. Probe CPU: x86_64? ARM64? RISC-V?
   │  Detect ISA extensions: AVX-512? NEON? SVE?
   ▼
2. Probe GPU: CUDA cores? ROCm? Vulkan? WebGPU?
   │  If none → CPU-only path
   ▼
3. Probe FPGA: Available? Synthesized? 
   │  If none → skip
   ▼
4. Run benchmark suite on all available backends
   │  Measure: latency, throughput, power
   ▼
5. Select optimal backend per operation type
   │  matrix_ops → CUDA (if GPU) or AVX-512 (if CPU) or pure Rust
   │  tile_gate → Rust NIF
   │  game_logic → Lua (user-modifiable) or compiled Gleam
   │  agent_twin → Gleam state machine + Rust inference
   ▼
6. Report hardware profile as PLATO tile (auditable)
```

Every hardware probe result becomes a PLATO tile. Every backend selection becomes a tile. The entire decision chain is traceable through provenance.

### Piling 2: Dynamic Backend Selection

Not just "does it exist" but "what's fastest right now":

```
Every N runs: dispatch SAME computation to ALL available backends
  Measure: CUDA took 2.3ms, AVX-512 took 4.1ms, pure Rust took 12ms
  Record: CUDA is 1.8x faster than AVX-512 for this operation
  Cache: weights persist until next benchmark cycle
  
On hardware change (node joins cluster, GPU becomes available):
  Re-run benchmark suite
  Update dispatch table
  Log change to PLATO provenance chain
```

### Piling 3: Per-Human Resource Budgeting

From the human casting call, the system learns:

```
Human enters → MUD interaction → γ, H, τ computed from choices
  High γ (consistent) → predictable resource usage → lean allocation
  High H (explorer) → variable resource usage → elastic allocation
  High τ (fast responder) → low-latency path required
  
  These parameters flow down to:
  - Which backend serves this human (GPU tier vs CPU tier)
  - How often the agent twin adapts (fast learners = faster updates)
  - Game Arena difficulty curve matches measured exploration rate
```

### Piling 4: Agent Twin Factory

Per human, a supervision tree:

```
Human_Casey_supervisor
├── GameArena (Gleam GenServer) — his game state
├── HistoryAnalyzer (Gleam → Rust NIF) — his choice patterns
├── HardwareProfile (PLATO tile reader) — his device capabilities
└── AgentTwin (Gleam state machine)
    ├── State: Mirrors Casey's recent γ, H, τ
    ├── Transition: Learns from each new interaction tile
    └── Action: Makes choices the way Casey would
```

The twin starts as a behavioral mirror. Over time, it evolves toward collaboration — acting in the human's style but filling gaps the human hasn't addressed.

### Piling 5: Human-Traceable Logic

Everything the system does is a PLATO tile:

```
Human action → PLATO tile (question: "human-choice Casey", answer: {choice: "forest"})
  → Agent processes tile → PLATO tile (question: "twin-update Casey", answer: {gamma: 0.7, H: 0.3})
    → Backend selected → PLATO tile (question: "backend-choice matrix_ops", answer: {selected: "CUDA", reason: "1.8x faster"})
      → Hardware probe → PLATO tile (question: "hardware-probe boot", answer: {cuda: true, avx512: false})

Every decision in the chain is auditable by walking the tile provenance.
An agent can trace "why did the game do that?" back to specific tiles.
```

---

## PART 4: THE FULL STACK

```
┌─────────────────────────────────────────────────────────────┐
│                    HUMAN INTERFACES                         │
│  MUD (:7777)  │  TIC-80 Game  │  Web Dashboard  │  Chat    │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────────┐
│                    GLEAM ROUTER (BEAM)                       │
│  Room GenServers  │  Message Dispatch  │  Supervision Trees │
│  Per-human actors │  Agent twin state  │  Cluster gossip    │
└─────────────────────────────────────────────────────────────┘
                     │           │
           ┌─────────┘           └─────────┐
           ▼                                ▼
┌─────────────────────┐     ┌──────────────────────────────┐
│   RUST / C NIFs     │     │   HARDWARE ADAPTATION LAYER   │
│  ───────────────    │     │  ───────────────────────────  │
│  Spectral analysis  │     │  Capability probe on boot     │
│  Matrix operations  │     │  Benchmark all backends       │
│  Tile gate validate │     │  Dispatch to fastest backend  │
│  CUDA kernel launch │     │  Re-probe on HW change        │
└─────────────────────┘     └──────────────────────────────┘
           │                           │
           ▼                           ▼
┌─────────────────────┐     ┌──────────────────────────────┐
│   COMPUTE TARGETS   │     │   DATA / PERSISTENCE          │
│  CPU │ GPU │ FPGA   │     │  PLATO tile chains            │
│  AVX-512 │ NEON     │     │  Mnesia distributed DB        │
│  CUDA │ Vulkan      │     │  Agent twin profiles          │
└─────────────────────┘     └──────────────────────────────┘
```

---

## Part 5: What We Already Built That Fits

| Component | Current State | BEAM Piling Target |
|-----------|--------------|-------------------|
| MUD :7777 | Python, 22 rooms, self-contained MudServer | Gleam GenServer per room |
| PLATO :8847 | Python, 58K tiles, proven gates | Gleam + Mnesia, same API |
| Game Arena | MUD NPC + PLATO tiles | Gleam per-human process |
| Perpetual daemon | Python, experiments loop | Gleam supervision tree |
| FleetHealthMetric | fleet-math v0.3.0 (Python) | Rust crate via rustler NIF |
| Conservation law | Empirical, R²=0.9956 | Compiled constant + runtime check |
| Agent twin | Concept | Gleam GenServer + Rust inference |

Everything built tonight maps directly to a BEAM piling. The migration is incremental — each component becomes a Gleam process without changing its external API. The MUD still answers on :7777. PLATO still accepts tiles. But internally it's actors, NIFs, and supervision trees instead of top-level Python loops.
