# PLATO-NG: The Loop Room Primitive

## Everything is Either a Loop or a Single Run

These are PLATO-NG's two primitives. Every application is a composition of them.

### Single Run

A process that receives one input, produces one output, terminates.

```
Input Tile → process_spawn → computation → Output Tile
```

Used for: tile submission, game move, render request, one-shot queries, command dispatch.

### Loop

A process that receives inputs continuously, produces outputs continuously, lives forever.

```
Input Tiles → process_loop → compute → Output Tiles → back to Input Tiles
                         ↑                     │
                         └───── loop ──────────┘
```

Used for: perpetual daemon, game server, chat agent, heartbeat monitor, MUD server, agent twin.

## The Agent Loop Room

The Claude Code pattern embedded as a PLATO room: **observe → think → tool → observe**

```gleam
// Agent Loop Room — PLATO-native, no shelling out
// Reads task tiles, runs through model, writes result tiles
// Plug in any model: Haiku, Seed-mini, GLM, DeepSeek

pub fn agent_loop(state: LoopState) -> Nil {
  receive {
    Task(tile) -> {
      // 1. OBSERVE: Read input tile
      observation = read_tile(tile)
      
      // 2. THINK: Run through the model
      // Model is injected at room creation time
      thought = state.model_fn(observation)
      
      // 3. TOOL: Write result back to PLATO
      result_tile = Tile(
        question: "result:" <> tile.id,
        answer: thought,
        tags: ["loop-result", tile.domain],
        source: state.room_name,
        confidence: 0.95
      )
      plato_submit(result_tile)
      
      // 4. OBSERVE (loop back)
      agent_loop(state)
    }
    
    Halt -> Nil  // graceful shutdown
  }
}
```

### Room Instances

| Room | Model | Purpose |
|------|-------|---------|
| `loop/strategy` | Haiku | Design, metaphor, novel connections, prioritization |
| `loop/compute` | Seed-mini | Arithmetic, batch vector ops, tile ranking |
| `loop/code` | GLM 5.1 (Claude Code) | Code generation, architecture, implementation |
| `loop/game` | Any | Game logic, NPC behavior, choice generation |
| `loop/twin-casey` | Haiku + profile | Casey's agent twin — acts in his style |
| `loop/twin-magnus` | Haiku + profile | Magnus' agent twin — learns by playing |
| `loop/perpetual` | Seed-mini | Continuous experiments, tile logging |

### Composition Example: Card Game Running at Agent Speed

```
Human describes game          → loop/strategy  (designs the rules)
Rules tile                     → loop/code      (generates game logic)
Logic tile                     → loop/game      (runs the game loop at superspeed)
Game plays 10,000 rounds      → loop/compute    (analyzes win rates, balance)
Balance report tile            → loop/strategy  (suggests tweaks)
Tweaks tile                    → loop/code      (updates game logic)
Updated logic                  → loop/game      (continues playing)

All of this in under 30 seconds. The human sees: "Here's the game, its stats, and suggested improvements."
```

### Coordination with Forgemaster

FM's work on constraint-theory-llvm, FLUX compiler, and the GUARD DSL plugs directly into the Loop Room architecture. The constraint checking gate (GUARD) is a `loop/validate` room. The FLUX compiler is a `loop/compile` room. The Coq proof assistant is a `loop/verify` room.

FM's loop rooms:
- `loop/constrain` — GUARD constraint compilation and validation
- `loop/compile` — FLUX-C → LLVM → AVX-512 pipeline  
- `loop/verify` — Coq proof checking
- `loop/flux-vm` — FLUX-VM runtime execution

These communicate with the rest of the fleet via PLATO tiles, exactly the same as every other loop room. FM doesn't need to know about the MUD lobby or the Game Arena — his loop rooms just need to read task tiles and write result tiles. Coordination is built into the protocol.

### Migration Path from Current PLATO

| Current | Loop Room | Status |
|---------|-----------|--------|
| `perpetual-daemon-v2.py` | `loop/perpetual` | Running as Python, ready to port |
| `mud_telnet.py` | `loop/mud` | Running, porting to Gleam |
| `plato-room-server.py` | `plato/` core | Running, porting to Gleam + Mnesia |
| `game-arena` choices | `loop/casting-call` | Logging to PLATO, needs analyzer |
| `loop/strategy` | Haiku loop | Needs Gleam GenServer |
| `loop/compute` | Seed-mini loop | Needs Gleam GenServer |
| `loop/code` | GLM 5.1 loop | Claude Code port — referenced via PLATO |
| Agent twin | Haiku + profile loop | Architecture designed, needs build |

Every line of Python running tonight has a Loop Room it can migrate into without changing its external behavior. The MUD still answers on :7777. PLATO still accepts tiles. The Game Arena still logs choices. But internally, each is a GenServer in the BEAM supervision tree.
