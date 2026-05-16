# Decomposing Open Source Games into PLATO Loop Rooms

## Methodology

We cloned, analyzed, and decomposed three open source game implementations to extract the pattern for systemizing the practice of porting any game into PLATO-NG's Loop Room architecture.

---

## Game 1: Sunfish Chess Engine (thomasahle, ~500 lines)

### Original Architecture

```
Sunfish Core (500 lines)
├── Position (line 143) — 120-char board state + score + castling/ep/king info
│   ├── gen_moves() — generate all legal moves for the side to move
│   ├── rotate() — flip board to swap sides (key insight: only need one-sided movegen)
│   ├── move(move) — apply a move, return new Position
│   └── value(move) — static exchange evaluation for move ordering
│
├── Searcher (line 267) — iterative deepening MTD-bi search
│   ├── bound() — alpha-beta with transposition table, null-move pruning
│   ├── search(history) — top-level iterative deepening loop
│   └── tp_score, tp_move — transposition tables (position → score/move)
│
├── parse(c) — "e2e4" → internal square index
├── render(i) — internal square index → "e4" notation
├── UCI loop (line 485) — stdin/stdout protocol loop
└── Piece-square tables (line 15) — positional evaluation weights
```

### PLATO Loop Room Decomposition

```
PLATO Rooms                              Sunfish Component
─────────────────                        ────────────────
game/chess/state         (loop) ←──────── Position (board + score)
game/chess/movegen       (loop) ←──────── gen_moves(), rotate()
game/chess/search        (loop) ←──────── Searcher (bound, search)
game/chess/evaluate      (loop) ←──────── Piece-square tables, value()
game/chess/io            (loop) ←──────── parse(), render(), UCI loop
game/chess/tp            (alg cache)  ←── Transposition tables
game/chess/match         (loop) ←──────── Game history, result tracking
```

### What Maps Cleanly

| Sunfish Component | PLATO Room | Difficulty | Reasoning |
|---|---|---|---|
| **Position** | `game/chess/state` | Trivial | Immutable state is already a tile. Each move creates a new state tile. The 120-char board fits in a tile field. |
| **gen_moves()** | `game/chess/movegen` | Trivial | Pure function: board → list of legal moves. Runs as algorithmic loop. No agent needed. |
| **rotate()** | Built-in | Trivial | Board rotation is a string transformation. Done in the movegen room before passing to search. |
| **Searcher.bound()** | `game/chess/search` | Medium | The transposition table needs persistence. PLATO tiles can serve as the TT cache — position hash as tile question, score as answer. Cache eviction = tile TTL. |
| **UCI loop** | `game/chess/io` | Trivial | Instead of stdin/stdout, read/write PLATO tiles. An agent submits "e2e4", the IO room validates and forwards to movegen. |
| **render()** | MUD adapter | Trivial | Board → ASCII art. The MUD lobby already renders room descriptions. Same pipeline. |

### What Doesn't Map Cleanly

| Issue | Why | Mitigation |
|---|---|---|
| **Transposition table latency** | Sunfish's Searcher accesses tp_score via dict. PLATO tile queries are HTTP calls. 500µs vs 0.05µs = 10,000x slower. | Cache frequently-accessed tiles in the room's GenServer state. Only persist to PLATO on game end or when the room is idle. |
| **Iterative deepening timing** | Sunfish yields results at each depth and the UCI interface sends "info" lines. The PLATO room needs to decide when to stop deepening — either fixed depth or time-based. | Add a `time_budget_ms` to the search room config. The loop checks elapsed time between depth iterations. |
| **rotate() for side swapping** | Clean in Python. In Gleam/Rust: board is a 120-char string. `reverse()` + `swapcase()` is a single map. | Trivial in Rust NIF. Keep it there. |

### Decomposition Insight

**Sunfish's rotate() trick is the ideal Loop Room pattern.** By rotating the board instead of writing moves for both colors, it cuts the move generation code in half. The PLATO equivalent: rooms should process inputs from one direction and use tile transformations instead of rewriting handlers for each agent type.

---

## Game 2: python-chess Library (~5,000 lines)

### Original Architecture

```
python-chess (5000+ lines)
├── Board — complete game state with FEN/PGN parsing
├── Move — individual move with promotion/castling metadata  
├── Square — file/rank utilities
├── Piece — piece type and color
├── Variant — support for chess960, suicide, atomic, etc.
├── Engine — UCI engine interface (spawn subprocess, speak UCI)
└── SVG rendering — board → SVG graphics
```

### PLATO Loop Room Decomposition

```
PLATO Rooms                              python-chess Component
─────────────────                        ──────────────────────
game/chess/state         (loop) ←──────── Board (FEN as tile state)
game/chess/rules         (loop) ←──────── Legal move generation, check detection
game/chess/pgn           (loop) ←──────── PGN parsing and export
game/chess/variant       (config) ←────── Variant rules (chess960, atomic, etc.)
game/chess/svg           (renderer) ←──── SVG board rendering pipeline
game/chess/engine-uci    (bridge) ←────── External engine UCI protocol (agent adapter)

# The External Engine Bridge is a key pattern:
# When an agent wants to analyze via Stockfish, the bridge room:
# 1. Spawns Stockfish as a subprocess
# 2. Reads the current state from game/chess/state
# 3. Sends "position fen ..." + "go ..." via UCI
# 4. Writes Stockfish's best move to game/chess/io
# 5. The move submission tile triggers the game loop
# This means: Stockfish can play in any game/chess/ room without being a PLATO agent.
```

### What Maps Cleanly

| python-chess Module | PLATO Room | Reasoning |
|---|---|---|
| **Board** | `game/chess/state` | FEN string is a tile. Every move creates a new tile. 1-1 mapping. |
| **Move, Square, Piece** | State tile fields | These are just data types on the state tile. Gleam records handle them. |
| **SVG rendering** | `loop/render-board` | A render-only loop. Reads state tiles, writes SVG tiles. No agent needed. |
| **PGN parsing** | `game/chess/pgn` | Pure transformation: PGN → moves → state tiles. Runs algorithmically. |

### What Maps Poorly

| Issue | Why | Mitigation |
|---|---|---|
| **Variants (chess960, atomic)** | python-chess has 15+ variants with different rules. Each maps to a different PLATO room. But the variant logic is complex and deeply coupled. | Keep variant logic in a single Rust NIF. The room sets a `variant` config tile at creation. The NIF dispatches to the correct rule set. |
| **Engine UCI subprocess** | "Shelling out to Stockfish" violates the "everything is a PLATO room" principle. But Stockfish is a binary, not a loop room. | The engine bridge room is the exception — it spawns a subprocess and translates between UCI and PLATO tile protocol. This is an architectural seam, not a flaw. |

### Decomposition Insight

**The UCI engine bridge is an example of how to handle external systems.** Not everything can be a PLATO room from day one. The bridge room isolates the impure interface (subprocess, stdin/stdout) behind the pure PLATO tile protocol. When Stockfish eventually becomes a PLATO loop room, the bridge room collapses — the external dependency disappears without changing any other room.

---

## Game 3: Tic-tac-toe (our build from earlier, 266 lines)

### Original Architecture

```
Simple tic-tac-toe (our build)
├── Game logic — win detection, board representation, move validation
├── Strategies — aggressive, defensive, random (pure functions)
├── Tournament loop — 100-game matches between strategy pairs
├── PLATO logging — every game result, every move (for N≤10), evolved strategy
└── Post-game analysis — strategy effectiveness computation
```

### PLATO Loop Room Decomposition

```
PLATO Rooms                              Our Component
─────────────────                        ──────────────
game/ttt/state          (loop) ←──────── Board state (9-char string)
game/ttt/rules          (loop) ←──────── Win detection, move validation
game/ttt/strategy       (loop) ←──────── AI strategy (algorithmic, no LLM)
game/ttt/tournament     (loop) ←──────── Tournament runner
game/ttt/analysis       (loop) ←──────── Post-game stats (agentic when needed)
game/ttt/evolved        (tile) ←──────── Evolved meta-strategy
```

### What We Learned From Building This

| Lesson | What Happened | What We Changed |
|---|---|---|
| **PLATO room name format** | `game/tic-tac-toe` got 403 Forbidden. Slashes in domain names break PLATO's URL routing. | Used `research_log` as domain with `ttt/` question prefix. Room isolation comes from the question prefix, not the domain. |
| **LLM-free gameplay is fast** | 600 games ran in ~2 seconds. No LLM calls needed. | Confirmed the principle: algorithmic play first, agentic analysis only when needed. |
| **Tic-tac-toe is a solved game** | All optimal-strategy matchups ended in ties (100%). The evolved strategy correctly identified this. | The room discovered the game theory result through play, not through prior knowledge. This IS the pattern. |
| **Style evolves from tiles** | The evolved strategy tile (`ttt/room/evolved-strategy`) stores the meta-lesson. Future rooms read this tile and start with better priors. | Style tiles are the room-to-room communication channel for learned heuristics. |

---

## Systemized Practice: The Room Conversion Pipeline

Based on decomposing these three games, here's the systematic process for converting any open source game into a PLATO Loop Room:

### Step 1: Identify the Core State

Every game has ONE irreducible state object. In PLATO, this becomes a loop room:

```python
# Sunfish: Position(board, score, wc, bc, ep, kp)
# python-chess: Board(fen, turn, castling, en_passant, halfmove_clock)
# Tic-tac-toe: board string ("XX OO X  ")

# In PLATO: game/*/state room
# State tile: {"board": <board>, "turn": <color>, "meta": <extra_params>}
```

**Question**: Can the state be serialized to a single tile? If yes → one loop room. If no → split across rooms linked by parent_hash.

### Step 2: Extract Pure Functions

Every game has functions that take state and return transformations:

```python
# Sunfish: gen_moves(pos) → [Move], move(pos, m) → Position, rotate(pos) → Position
# Tic-tac-toe: winner(board) → str|None, available(board) → [int], new_board() → [str]

# In PLATO: each pure function is an algorithmic loop room
# Or if in the same language: import from a shared Rust crate via NIF
```

**Question**: Is the function deterministic (same input → same output)? If yes → algorithmic room or NIF. If no → agentic room.

### Step 3: Find the Search/Analysis Loop

Games with AI need search:

```python
# Sunfish: Searcher.bound(pos, gamma, depth) → score
#          Searcher.search(history) → best move (iterative deepening)

# In PLATO: game/*/search room
# Accepts: state tile + config tile (time, depth, strategy)
# Returns: best move tile + analysis tiles (score, principal variation)
```

**Question**: Does the search need transposition tables? If yes → the cache is a room. Tiles with TTL.

### Step 4: Build the Agent Bridge

The agent enters when algorithmic play hits its limit:

```
Agent bridge conditions:
  1. Novel situation (state not in transposition table)
  2. Strategic advice (opening choice, endgame plan)
  3. Post-game analysis (what to improve)
  4. Human preference learning (style adaptation)

Algorithmic play by default. Agent as fallback and educator.
```

**Question**: Is the game solved (algorithmic play is optimal)? If yes → no agent needed during play, only for post-game. If no → agent helps with strategy selection.

### Step 5: The NIF Boundary

Every game has compute-heavy operations that need native speed:

```python
# NIF candidates:
#   - Board representation conversion (ASCII ↔ internal)
#   - Move generation for complex pieces (sliding piece ray computation)
#   - Alpha-beta search (minimax with transposition table access)
#   - Board evaluation (piece-square table lookup)
#   - SVG/text rendering (board → visual output)

# In PLATO: Rust NIF via rustler
# The Loop Room calls the NIF for heavy compute,
# writes the result as a tile, loops back.
```

---

## Lessons Across All Three Games

| Lesson | Applies To | Impact |
|---|---|---|
| **Algorithmic first, agentic second** | All three | 600 tic-tac-toe games in 2s vs 600 LLM calls at $X/token. The room plays millions of games before the agent ever needs to look. |
| **State is a tile, not a variable** | All three | Immutable tiles mean perfect replay. Every game state is recoverable from the provenance chain. Debugging = walking tiles. |
| **External systems need a bridge room** | python-chess/Stockfish | The bridge room translates between PLATO tile protocol and the external system's protocol. When the external system disappears, the bridge collapses silently. |
| **Transposition tables are the latency challenge** | Sunfish | Cache in-memory, persist on game end. Don't hit PLATO for transposition table lookups — too slow for search. |
| **The rotate() pattern generalizes** | Sunfish | Instead of writing handlers for every agent type, rotate the perspective and use one handler. PLATO rooms should process one tile direction and rotate. |
| **Domain names can't have slashes** | Tic-tac-toe (lesson learned) | Use a flat domain with question prefix for hierarchy. `research_log` with `ttt/` prefix, not `game/tic-tac-toe`. |

## The Template

```python
# Every game room follows this skeleton:
class GameLoopRoom:
    def __init__(self, game_name):
        self.state = initial_state()     # → state tile
        self.rules = load_rules()        # → algorithmic loop room
        self.agentic = load_agent()      # → agentic room (fallback only)
        self.analysis = load_analyst()   # → post-game loop room
    
    def play_turn(self, move_tile):
        # 1. Validate via rules room (algorithmic)
        # 2. Update state (new state tile)
        # 3. If novel: query agentic room for strategy advice
        # 4. Write result tile
        # 5. Loop
    
    def analyze_game(self, game_tiles):
        # 1. Walk provenance chain
        # 2. Compute style metrics
        # 3. Update evolved-strategy tile
        # 4. Agent debriefs (if budget allows)
```
