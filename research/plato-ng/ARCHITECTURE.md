# PLATO-NG: Turing-Complete Application Runtime

## The Vision

PLATO is no longer a tile store. PLATO IS the computation. Applications are PLATO rooms. State is PLATO tiles. Logic runs through the tile chain. UI renders from PLATO into any surface.

```
┌─────────────────────────────────────────────────┐
│                  PLATO-NG                        │
│  (Turing-complete tile computation engine)      │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ App Room  │  │ App Room  │  │ App Room  │      │
│  │ (State)   │  │ (Logic)   │  │ (UI)     │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│         │              │              │          │
│         ▼              ▼              ▼          │
│  ┌─────────────────────────────────────────┐    │
│  │         Renderer Adapter Layer           │    │
│  │  SCUMMVM │ TIC-80 │ Lua/LÖVE2D │ Web   │    │
│  └─────────────────────────────────────────┘    │
│         │                                        │
│         ▼                                        │
│  ┌─────────────────────────────────────────┐    │
│  │     Human I/O (chat, voice, GUI)        │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## Architecture

### 1. PLATO as Computation Engine (Not Store)

Current PLATO: tiles are finished thoughts with provenance chains.
PLATO-NG: tiles are LIVE VARIABLES. Rooms are PROCESSES.

| Concept | Current PLATO | PLATO-NG |
|---------|--------------|----------|
| Tile | Immutable record | Mutable state variable |
| Room | Topic namespace | Process/application |
| Chain | Provenance history | Execution trace |
| Gate | Quality filter | Constraint validator |
| Submit | Write result | Execute transformation |

### 2. The App Decomposition

Every app decomposes into PLATO rooms:

```
chess-game/
├── state/           # Game state (board, pieces, turns)
│   └── tiles: board-position, captured-pieces, move-history
├── logic/           # Transformations (move validation, win detection)
│   └── tiles: move-constraints, check-detector, endgame-detector
├── ui/              # Rendering instructions
│   └── tiles: piece-graphics, board-layout, animation-params
├── io/              # I/O adapters
│   └── tiles: input-queue, output-events, chat-sidebar
└── player/          # Agent instances
    └── tiles: agent-1, agent-2, human-input-hook
```

The recomposition: `UI = render(state, ui-instructions, renderer-adapter)`

### 3. Backend-Optimizing FLUX-Native Runtime

FLUX compiles GUARD constraints. PLATO-NG uses GUARD as its tile validation language:

```guard
// Chess move constraint as PLATO tile validation
constraint valid_move {
  input: board_state, from_square, to_square
  output: valid_boolean, new_board_state
  
  // Piece-specific move patterns
  match piece_type at from_square {
    case "knight": L_shape(to_square - from_square)
    case "bishop": diagonal(from_square, to_square) & clear_path
    case "rook": orthogonal(from_square, to_square) & clear_path
    case "queen": (diagonal | orthogonal) & clear_path
    case "king": chebyshev_distance <= 1
    case "pawn": forward_one | (capture_diagonal & first_move_two)
  }
}
```

This GUARD constraint IS the tile validation. When a human submits a move tile, the gate runs the constraint.

### 4. Dynamic Render Backend Selection

Apps declare a rendering target. PLATO-NG dynamically generates:

```
App declares: render_target = "scummvm"
PLATO-NG: app-state/ + app-ui/ → SCUMMVM room/script via adapter

App declares: render_target = "love2d"
PLATO-NG: app-state/ + app-ui/ → Lua/LÖVE2D via adapter

App declares: render_target = "web"
PLATO-NG: app-state/ + app-ui/ → HTML5/Canvas via adapter
```

The adapter IS a PLATO room. It reads `app-ui/` tiles and writes to the output surface.

### 5. The Vibe Coding Loop

```
Human: "make the bishop a dolphin"

[CHAT] → PLATO app-io/ tile: "change bishop graphic to dolphin"
  → Agent reads tile
  → Agent generates: PLATO app-ui/ tile: piece-bishop = {shape: "dolphin", color: "white"}
  → Renderer picks up tile change
  → Human sees new bishop sprite
  → Human: "no, make it leap for captures"
  → Agent updates capture-animation tile
  → Human plays, sees leap animation
  → Iterates via chat

This is a 1-second loop. Human never touches code.
PLATO is the database, the constraint engine, and the rendering pipeline.
```

## Feasibility Assessment

| Component | Status | Path Forward |
|-----------|--------|-------------|
| PLATO tile mutations (not immutability) | ❌ Immutable today | Add mutable tiles with version chains |
| GUARD as tile validation gate | ⚠️ Partial | GUARD exists, needs PLATO binding |
| Renderer adapters (SCUMMVM, TIC-80, Lua) | ❌ Doesn't exist | Build as PLATO rooms reading app-ui/ |
| FLUX-native PLATO runtime | ❌ Doesn't exist | FLUX-VM needs PLATO syscalls |
| Vibe coding agent loop | ⚠️ Partial | Agent API exists, needs game-dev skill |
| Human-in-the-loop iteration | ⚠️ Partial | Chat interface exists, needs game bindings |

## Next Steps (Research Phase)

1. **PLATO-NG spec**: Formal spec of mutable tiles, room-as-process, tile-as-variable
2. **GUARD-PLATO binding**: GUARD constraints as tile validation gates
3. **SCUMMVM adapter prototype**: Render PLATO app-ui/ tiles as SCUMMVM room
4. **LÖVE2D adapter prototype**: Render as runnable Lua game
5. **Demo: Chess in PLATO**: Full vibe-coding loop — human builds chess via chat
6. **Demo: Magnus' game**: Magnus prototypes his game idea in PLATO
