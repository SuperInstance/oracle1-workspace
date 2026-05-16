# Track 5: Vibe Coding Agent for PLATO-NG

> **Research question:** What agent architecture enables rapid game iteration via chat?
> **Core insight:** Human types intent → PLATO tiles update → game changes → human sees → iterates.
> **The loop must complete in < 2 seconds.**

---

## 1. The Vision

The vibe coding agent closes the PLATO-NG loop:

```
┌─────────────────────────────────────────────────────┐
│                   THE VIBE LOOP                      │
│                                                      │
│  Human: "Make the bishop into a dolphin"            │
│         │                                           │
│         ▼                                           │
│  ┌─────────────┐  ┌──────────────────┐              │
│  │ NL Parser   │  │ Intent Resolver  │              │
│  │ (human→plan)│→ │ (plan→tile ops)  │              │
│  └─────────────┘  └──────────────────┘              │
│                           │                          │
│                           ▼                          │
│  ┌─────────────────────────────────────────┐        │
│  │          Tile Graph Generator             │        │
│  │  (generates changes to app-ui/,           │        │
│  │   app-logic/, app-state/ tiles)           │        │
│  └─────────────────────────────────────────┘        │
│                           │                          │
│                           ▼                          │
│  ┌─────────────────────────────────────────┐        │
│  │          Render Adapter Triggers          │        │
│  │  (picks up tile change → re-renders)      │        │
│  └─────────────────────────────────────────┘        │
│                           │                          │
│                           ▼                          │
│  Human sees new dolphin bishop in < 2 seconds ◄─────┘
│                                                      │
│  Human: "No, make it leap when it captures"         │
│  → Loop repeats                                      │
│  → Human never touches code                          │
│  → Every iteration is a concrete game change         │
└─────────────────────────────────────────────────────┘
```

**Key metrics:**
- **Latency target:** < 2 seconds per iteration
- **Understanding accuracy:** Agent should get intent right 90%+ on first try
- **Iteration depth:** Support chained changes (10+ iterations per session)
- **Rollback:** Human can say "undo that" or "go back 3 changes"

---

## 2. Agent Architecture

The vibe coding agent is NOT a monolithic model call. It is a **pipeline of specialized micro-agents** communicating through PLATO tiles:

### 2.1 Overview

```
┌─────────────────────────────────────────────────────────┐
│                VIBE CODING AGENT (VCA)                    │
│                                                          │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │  NL Listener  │  │ Intent Resolver │  │ Plan Builder  │ │
│  │ (app-io/      │→ │ (classify +     │→ │ (sequence of   │ │
│  │  input-queue) │  │  parameterize)  │  │  tile ops)     │ │
│  └──────────────┘  └────────────────┘  └───────┬──────┘ │
│                                                  │        │
│         ┌────────────────────────────────────────┘        │
│         ▼                                                 │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │ Tile Writer   │  │ Code Generator │  │ Asset Gen     │ │
│  │ (mutable      │  │ (mutation func │  │ (sprites,     │ │
│  │  tile writes) │  │  generators)   │  │  sound fx)    │ │
│  └───────┬──────┘  └───────┬────────┘  └──────┬───────┘ │
│          │                 │                   │          │
│          └─────────────────┼───────────────────┘          │
│                            ▼                              │
│  ┌─────────────────────────────────────────┐              │
│  │          Change Committer                 │              │
│  │  (atomic tile update + render trigger)    │              │
│  └─────────────────────────────────────────┘              │
│                            │                               │
│                            ▼                               │
│  PLATO tiles updated → Render adapter re-renders          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Component Detail

#### A) NL Listener

**Role:** Poll `app-io/input-queue` tile for new human intents. Debounce rapid input.

**Implementation:** A lightweight watcher (polling every 100ms) that checks for changes on the input tile. When a new message appears:
1. Copy to `app-io/pending-intent` tile (staging area)
2. Set `app-io/listener-status` to `"pending"`
3. Wake the Intent Resolver

**Simplest viable:**
```python
class NlListener:
    def __init__(self, plato_client, poll_ms=100):
        self.client = plato_client
        self.last_seq = 0
        
    async def poll(self):
        while True:
            tile = await self.client.read_tile("app-io/input-queue")
            if tile.seq > self.last_seq:
                self.last_seq = tile.seq
                await self.client.write_tile("app-io/pending-intent", {
                    "text": tile.content["text"],
                    "timestamp": tile.timestamp,
                    "seq": tile.seq
                })
            await asyncio.sleep(self.poll_ms / 1000)
```

#### B) Intent Resolver

**Role:** Take raw human language → classified game change with parameters.

**Classification taxonomy (v1):**

| Intent Category | Examples | Output Type |
|---|---|---|
| `modify_asset` | "make bishop a dolphin", "change pawn to red" | `{target: "bishop", new_asset: "dolphin", params: {...}}` |
| `modify_behavior` | "bishop leaps on capture", "pawn moves backwards" | `{target: "bishop", behavior: "capture_leap", params: {...}}` |
| `modify_layout` | "rotate the board", "add a third row" | `{layout_change: "rotate", params: {...}}` |
| `add_feature` | "add a score counter", "show move timer" | `{feature: "score_counter", ui_location: "top-left"}` |
| `remove_feature` | "remove the sidebar", "hide captured pieces" | `{target: "sidebar"}` |
| `undo` | "undo that", "go back" | `{steps: 1}` |
| `save_version` | "save this version", "snapshot" | `{name: "optional tag"}` |
| `ask_question` | "what pieces are left?", "show me the rulebook" | Not a change — routes to Q&A |

**Implementation approach:** Use a small, fast model (glm-4.7-flash or kimi-k2-turbo) to classify and extract parameters. The prompt is structured with few-shot examples from the current app domain.

```python
INTENT_PROMPT = """You are the Intent Resolver for a PLATO-NG game editor.
Given a human request, classify the intent and extract parameters.

Current game: {game_domain}
Available pieces: {pieces}
Available assets: {assets}

Human: "{user_input}"
Output JSON:
{{
  "intent": "modify_asset|modify_behavior|modify_layout|add_feature|remove_feature|undo|save_version|ask_question",
  "confidence": 0.0-1.0,
  "params": {{...}},
  "clarification_needed": "optional question if ambiguous"
}}"""
```

**Critical design choice:** The resolver MUST handle ambiguity gracefully. If confidence < 0.7, it asks a clarifying question rather than guessing.

#### C) Plan Builder

**Role:** Convert a resolved intent into a concrete sequence of PLATO tile operations.

**Example plan:**

```json
{
  "intent": "modify_asset",
  "params": {"target": "bishop", "new_asset": "dolphin"},
  "plan_steps": [
    {
      "op": "update_tile",
      "tile_path": "app-ui/piece-graphics",
      "patch": {"bishop": {"sprite": "dolphin", "palette": "ocean"}}
    },
    {
      "op": "update_tile",
      "tile_path": "app-logic/animation-params",
      "patch": {"bishop": {"capture_animation": "leap", "move_animation": "swim"}}
    },
    {
      "op": "generate_asset",
      "target": "sprites/dolphin.png",
      "prompt": "A cute pixel-art cartoon dolphin, 16x16, blue and white, game sprite style",
      "size": "16x16"
    },
    {
      "op": "trigger_render",
      "target": "love2d"
    }
  ]
}
```

**Simplest implementation:** Prompt same model that classified the intent to also produce the plan. Two-shot approach:
1. Resolver: classify + extract params
2. Planner: params → plan steps

#### D) Tile Writer

**Role:** Execute plan steps that write to PLATO tiles.

**Must handle:**
- Atomic updates (all changes or none — rollback on failure)
- Version-aware writes (don't clobber concurrent human edits)
- Pre-image saving for undo support

**Undo architecture:**
```
PLATO room: app-vibe/undo-stack
  tile: undo-0  → {snapshot of state before step 0}
  tile: undo-1  → {snapshot after step 0, before step 1}
  tile: undo-n  → {snapshot before step n}
  
Undo: restore most recent snapshot and pop the stack.
```

**Implementation sketch:**
```python
class TileWriter:
    def __init__(self, client):
        self.client = client
        self.undo_stack = []
    
    async def execute(self, plan):
        # Snapshot current state
        snapshot = await self._snapshot_affected_tiles(plan)
        self.undo_stack.append(snapshot)
        
        # Execute each step
        for step in plan.steps:
            if step.op == "update_tile":
                await self._patch_tile(step.tile_path, step.patch)
            elif step.op == "generate_asset":
                await self._call_asset_generator(step)
            elif step.op == "trigger_render":
                await self._trigger_render(step.target)
        
        # Commit undo stack
        await self.client.write_tile("app-vibe/undo-stack", self.undo_stack)
    
    async def undo(self, steps=1):
        for _ in range(steps):
            snapshot = self.undo_stack.pop()
            await self._restore_snapshot(snapshot)
```

#### E) Code Generator

**Role:** Generate or modify game logic functions that are stored as PLATO tiles.

This is the hard part. Game logic lives in tiles that are executed by the render adapter. We need to generate code in the target language (Lua for LÖVE2D, Guard for constraint gates).

**Approach:** Each game mechanic decomposes into a **small, composable function stored in a single tile**:

```
app-logic/
├── move-validators/
│   ├── pawn-move.lua       → function is_valid_pawn_move(board, from, to)
│   ├── bishop-move.lua     → function is_valid_bishop_move(board, from, to)
│   └── knight-move.lua     → function is_valid_knight_move(board, from, to)
├── capture-handlers/
│   ├── pawn-capture.lua    → function handle_pawn_capture(board, from, to)
│   └── bishop-capture.lua  → function handle_bishop_capture(board, from, to)
└── game-rules/
    ├── check-detection.lua → function is_in_check(board, color)
    └── win-conditions.lua  → function check_win(board)
```

When a human says "make the bishop a dolphin", the code generator:
1. **Finds** the bishop-related tiles (via naming convention)
2. **Generates** new sprite/animation code for the dolphin behavior
3. **Writes** it to the appropriate tiles

**Code gen model choice:** This is where we need a strong coder. **kimi-cli** is ideal because:
- It can read the existing tile structure
- Generate Lua/Guard code that integrates properly
- Return the output as structured tile updates

**Implementation:**
```python
async def generate_code_change(target_piece, behavior_change, game_domain):
    # Read existing code tiles
    existing_code = await read_tiles("app-logic/")
    
    # Use kimi-cli to generate the change
    prompt = f"""
    Game: {game_domain}
    Existing code structure:
    {existing_code}
    
    Change: Make the {target_piece} {behavior_change}.
    
    Generate the Lua code changes needed.
    Output format:
    {{
      "files": {{
        "app-logic/move-validators/{target_piece}-move.lua": "...new code...",
        "app-logic/capture-handlers/{target_piece}-capture.lua": "...new code..."
      }}
    }}
    """
    
    result = await run_kimi_cli(prompt, work_dir="/tmp/plato-ng")
    return parse_result(result)
```

#### F) Asset Generator

**Role:** Generate sprite/audio assets when a human wants to change visuals.

**Approach:**
1. Parse the asset description from the intent params
2. Call an image generation model (Qwen3-VL, DALL-E, or Stable Diffusion)
3. Downscale to game-appropriate resolution (16x16, 32x32 pixel art)
4. Save as tile in `app-ui/sprites/`

**Key consideration:** Asset generation is the slowest part of the loop. Strategy:
- **Fast path:** Use pre-existing asset templates with palette swaps (< 100ms)
- **Medium path:** Use a pixel-art generation model (~500ms)
- **Slow path:** Full-resolution generation + downscale (~2-5s)
- **Cache:** Cache generated assets so "make it blue again" returns instantly

### 2.3 Agent State Machine

```
                    ┌──────────┐
                    │  IDLE    │ ◄────── After all changes committed
                    └────┬─────┘
                         │ New human input detected
                         ▼
                    ┌──────────┐
                    │ LISTEN   │ (capture raw input, debounce)
                    └────┬─────┘
                         │ Input stabilizes (100ms no change)
                         ▼
                    ┌───────────┐
                    │ RESOLVE   │ (classify intent, extract params)
                    └─────┬─────┘
                     ┌────┴────┐
                     ▼         ▼
              ┌─────────┐  ┌─────────┐
              │ CLARIFY  │  │ PLAN    │
              │ (ask Q)  │  │ (build  │
              └────┬─────┘  │ steps)  │
                   │        └────┬────┘
                   │             │
                   ▼             ▼
              ┌──────────────────────┐
              │ Can resolve?         │
              │ YES → PLAN           │
              │ NO → back to IDLE    │
              └──────────────────────┘
                                  │
                                  ▼
                         ┌──────────────┐
                         │ EXECUTE      │
                         │ (write tiles,│
                         │  gen assets, │
                         │  trigger     │
                         │  render)     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ VERIFY       │
                         │ (check tile  │
                         │  constraints,│
                         │  report)     │
                         └──────┬───────┘
                                │
                         ┌──────┴──────┐
                         ▼             ▼
                   ┌──────────┐  ┌──────────┐
                   │ OK       │  │ ROLLBACK │
                   │ → IDLE   │  │ → undo   │
                   └──────────┘  └──────────┘
```

---

## 3. The Loop: Concrete Protocol

### 3.1 PLATO Tiles Used by the Agent

The vibe coding agent uses a dedicated room `app-vibe/` for its operational state, plus the app's `app-ui/`, `app-logic/`, `app-state/`, and `app-io/` rooms:

```
app-vibe/                    # Vibe agent's operational room
├── pending-intent            # Latest NL input awaiting processing
├── last-resolved-intent      # Parsed intent (JSON)
├── current-plan              # Build plan (JSON array of steps)
├── execution-status          # Running, Done, Failed, RolledBack
├── undo-stack                # Stack of pre-change snapshots
├── last-response             # Agent's response to human
│
app-io/                       # App I/O room (shared with renderer)
├── input-queue               # Human input arrives here
├── output-events             # Agent sends messages here
│
app-ui/                       # Renderable UI tiles
├── piece-graphics            # Sprite assignments per piece
├── animation-params          # Animation definitions
├── board-layout              # Board structure
├── sprites/                  # Generated sprite assets
│
app-logic/                    # Game logic tiles
├── move-validators/          # Per-piece move validation
├── capture-handlers/         # Per-piece capture behavior
├── animation-handlers/       # Per-type animation logic
│
app-state/                    # Live game state
├── board-position            # Current position
├── captured-pieces           # Captured pieces list
└── turn-tracker              # Whose turn
```

### 3.2 The Protocol (Step by Step)

**Step 0: Initialization**
```
Agent starts → reads app-vibe/ state
            → checks for existing undo stack
            → enters IDLE state
            → writes status tile: {"state": "IDLE", "app": "chess", "since": timestamp}
```

**Step 1: Human speaks**
```
Human types: "make the bishop a dolphin"
Renderer (or chat bridge) writes to app-io/input-queue:
  {"text": "make the bishop a dolphin", "source": "chat", "seq": 42}
```

**Step 2: Listener wakes**
```
NL Listener polls every 100ms → sees seq changed
→ copies to app-vibe/pending-intent
→ sets app-vibe/execution-status to "LISTENING"
→ wakes Intent Resolver
```

**Step 3: Resolve intent (target: < 500ms)**
```
Intent Resolver reads pending-intent
→ calls fast model (glm-4.7-flash) with current app context
→ writes to app-vibe/last-resolved-intent:
  {
    "intent": "modify_asset",
    "confidence": 0.92,
    "params": {
      "target": "bishop",
      "new_asset": "dolphin",
      "implicit_behavior": "swims instead of slides"
    },
    "raw": "make the bishop a dolphin"
  }
```

**Step 3b (if ambiguous): Clarify**
```
If confidence < 0.7:
  → writes to app-io/output-events: "Do you mean change the bishop's
    appearance to a dolphin, or make it move like a dolphin?"
  → sets status to "AWAITING_CLARIFICATION"
  → waits for human reply
  → merges reply with original intent → re-resolve
```

**Step 4: Build plan (target: < 300ms)**
```
Plan Builder reads resolved intent + current app state
→ generates ordered plan steps
→ writes to app-vibe/current-plan:
  {
    "plan_id": "plan-007",
    "intent_id": "intent-042",
    "steps": [
      {"op": "snapshot_state", "tiles": ["app-ui/piece-graphics", "app-logic/animation-params"]},
      {"op": "update_tile", "tile_path": "app-ui/piece-graphics", "patch": {...}},
      {"op": "update_tile", "tile_path": "app-logic/animation-params", "patch": {...}},
      {"op": "generate_asset", "prompt": "pixel art dolphin 16x16 blue white", "size": "16x16"},
      {"op": "trigger_render", "target": "love2d"}
    ],
    "estimated_cost_ms": 1200
  }
```

**Step 5: Execute plan (target: < 1 second total)**
```
Executor reads plan and runs sequentially:
→ Step 1: Snapshot current state (save undo point) ~10ms
→ Step 2: Update piece-graphics tile ~50ms
→ Step 3: Update animation-params tile ~50ms
→ Step 4: Generate dolphin sprite ~500ms (or 50ms if cached)
→ Step 5: Set app-vibe/execution-status = "TRIGGER_RENDER_READY"
          → This is the signal to the Render Adapter that it should re-render
    
Total mutable tile operations: ~110ms + asset gen ~500ms = ~610ms
```

**Step 5b: Asset generation (parallelizable)**
```
Asset Generator runs in a separate lightweight process:
→ Calls pixel-art model with prompt
→ Downsamples to game resolution (if needed)
→ Saves as app-ui/sprites/dolphin.png
→ Updates piece-graphics to reference new sprite
```

**Step 6: Trigger render**
```
Executor writes to a render-trigger tile that the render adapter watches:
→ writes app-vibe/render-trigger: {"plan_id": "plan-007", "changed_tiles": [...]}
→ Render adapter sees trigger → re-reads app-ui/ → re-renders game output
```

**Step 7: Human sees change**
```
Render adapter outputs the new game frame.
Human sees the dolphin bishop on screen.
Total elapsed: ~800ms (within 2s target)
```

**Step 8: Agent responds**
```
Agent writes to app-io/output-events:
  "✅ Done! The bishop is now a dolphin. It swims instead of sliding.
   Want me to make it leap when it captures? 🐬"
```

### 3.3 Timing Budget

```
Phase          Target     Max       Notes
──────────────────────────────────────────────
Poll detect     50ms     200ms     Poll every 100ms
NL resolve     200ms     500ms     glm-4.7-flash, lightweight
Plan build     150ms     300ms     Template-based + fast model
Tile writes     50ms     200ms     2-4 tile patches
Asset gen      300ms    2000ms     Cached or pixel-gen
Render trig      5ms      20ms     Tile write + adapter poll
Adapter render 200ms    1000ms     LÖVE2D reload is fastest
Agent response  50ms     200ms     Status message to human
──────────────────────────────────────────────
Total total   1005ms    4420ms     Target < 2s, max ~4.5s
```

**Optimization levers for < 2s:**
1. **Cache assets aggressively** — most visual changes are palette swaps
2. **Model routing** — intent resolution on fast model; code gen on strong model
3. **Parallelize** — asset generation while tile writes happen
4. **Incremental patches** — don't regenerate entire game, just changed tiles
5. **Render adapter polling** — adapter watches a trigger tile, doesn't re-read everything

---

## 4. Tool Selection

### 4.1 Primary Tools

| Component | Tool | Rationale |
|---|---|---|
| NL intent resolver | `glm-4.7-flash` | Fast (< 200ms), good NL understanding, cheap |
| Plan builder | `glm-5-turbo` | Needs structured output, moderate speed |
| Code generator | **kimi-cli** | Casey's directive: primary coding tool. Reads app logic, generates Lua/Guard. |
| Asset generator | `Qwen3-VL-32B-Instruct` | Fast pixel-art generation, can work from sprites |
| Render adapter | LÖVE2D/Lua | Fastest render cycle for prototyping |
| Overall coordinator | `glm-5.1` | Agent orchestrator, error handling, state management |

### 4.2 Why kimi-cli for Code Gen

kimi-cli (Moonshot Kimi K2.5 reasoning model) is the right choice for game logic generation because:

1. **Strong at context-aware code gen** — reads existing tile structure and generates compatible code
2. **Reasoning model** — understands game mechanics, not just syntax
3. **Structured output** — can return JSON-formatted file changes
4. **Already installed** — `kimi-cli --work-dir <dir>` for workspace-specific generation
5. **Casey's explicit directive** — "use extensively for code"

```
Usage pattern for code gen:
$ echo "Read app-logic/move-validators/bishop.lua and app-ui/piece-graphics/tile.json.
Change the bishop sprite to a dolphin and make it move like a knight instead of diagonally.
Output the changes as JSON with keys being tile paths and values being the new content." \
| kimi-cli --work-dir ~/.openclaw/workspace/plato-ng/chess-game
```

### 4.3 Tool Routing Matrix

| Task | First Choice | Fallback | Rationale |
|---|---|---|---|
| NL → intent | glm-4.7-flash | glm-5-turbo | Speed primary, accuracy secondary |
| Intent → plan | glm-5-turbo | glm-5.1 | Needs structured output |
| Code gen | kimi-cli | deepseek-chat (v4-flash) | Best code quality |
| Asset gen | Qwen3-VL-32B | Stable Diffusion via API | Fast enough, good pixel art |
| Verification | glm-4.7-flash | — | Lightweight check |
| Error handling | glm-5.1 | — | Needs full context |

---

## 5. Simplest Viable Implementation

### 5.1 Minimum Viable Agent (Plato-NG Chat Agent v0.1)

**What it does:**
- Listens for human input on a single chat tile
- Maps ~5 intents (modify_asset, modify_behavior, undo, ask_question, save)
- Writes to 2-3 app-ui/ tiles
- Triggers a LÖVE2D render adapter
- Reports back to human

**What it doesn't do (yet):**
- Complex multi-step plans
- Asset generation (uses template sprites)
- Undo stack (single-step undo only)
- Parallel execution

**Code skeleton:**

```python
# plato-vibe-agent.py — Simplest viable implementation

import asyncio
import json
import time
from typing import Optional

class PlatoVibeAgent:
    """The simplest vibe coding agent for PLATO-NG."""
    
    def __init__(self, client, app_room: str, model="glm-4.7-flash"):
        self.client = client
        self.app = app_room
        self.model = model
        self.last_seq = 0
        self.undo_snapshot: Optional[dict] = None
        
    async def run(self):
        """Main loop: poll input → resolve → plan → execute → respond."""
        print(f"🤖 Vibe Agent started for {self.app}")
        await self._write_status("IDLE")
        
        while True:
            intent = await self._poll_input()
            if intent is None:
                await asyncio.sleep(0.1)
                continue
                
            resolved = await self._resolve(intent)
            if resolved.get("clarification_needed"):
                await self._respond(resolved["clarification_needed"])
                continue
                
            plan = await self._plan(resolved)
            self.undo_snapshot = await self._snapshot()
            success = await self._execute(plan)
            
            if success:
                await self._trigger_render()
                await self._respond(self._format_success(resolved))
            else:
                await self._rollback()
                await self._respond(self._format_error(plan))
    
    async def _poll_input(self) -> Optional[str]:
        tile = await self.client.read_tile(f"{self.app}/app-io/input-queue")
        if tile.seq > self.last_seq:
            self.last_seq = tile.seq
            return tile.content.get("text")
        return None
    
    async def _resolve(self, text: str) -> dict:
        # Call glm-4.7-flash for fast intent classification
        prompt = f"""Classify this game editing request:
        Game: {self.app}
        Request: "{text}"
        
        Output JSON: {{"intent": "...", "params": {{...}}, "confidence": 0.0-1.0,
                       "clarification_needed": null}}
        """
        result = await self._call_model(self.model, prompt)
        return json.loads(result)
    
    async def _plan(self, resolved: dict) -> list:
        intent = resolved["intent"]
        params = resolved["params"]
        
        if intent == "modify_asset":
            return [{
                "op": "update_tile",
                "tile_path": f"{self.app}/app-ui/piece-graphics",
                "patch": {params["target"]: {"sprite": params["new_asset"]}}
            }]
        elif intent == "undo":
            return [{"op": "undo"}]
        # ... other intents
    
    async def _execute(self, plan: list) -> bool:
        for step in plan:
            if step["op"] == "update_tile":
                current = await self.client.read_tile(step["tile_path"])
                current.content.update(step["patch"])
                await self.client.write_tile(step["tile_path"], current.content)
            elif step["op"] == "undo":
                return await self._rollback()
        return True
    
    async def _trigger_render(self):
        await self.client.write_tile(f"{self.app}/app-vibe/render-trigger", {
            "timestamp": time.time(),
            "source": "vibe-agent"
        })
    
    async def _respond(self, message: str):
        await self.client.write_tile(f"{self.app}/app-io/output-events", {
            "text": message,
            "timestamp": time.time()
        })
        print(f"🤖 {message}")
```

### 5.2 Integration with Existing Tools

The simplest viable integration uses existing infrastructure:

```
┌─────────────────────────────────────────────────────────┐
│              EXISTING INFRASTRUCTURE                      │
│                                                          │
│  PLATO-CORE (tile store + provenance)                    │
│    └── Mutable tile support (Track 1 output)             │
│                                                          │
│  GUARD (constraint system)                                │
│    └── Tile validation gates (Track 2 output)            │
│                                                          │
│  Render Adapter (Track 3 or 4 output)                    │
│    └── Reads app-ui/ → renders game                      │
│                                                          │
│  Chat Bridge (existing)                                   │
│    └── Telegram/Discord → app-io/input-queue              │
│                                                          │
│  Vibe Agent (THIS TRACK)                                  │
│    └── Reads input → writes tiles → triggers render      │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Edge Cases & Failure Modes

### 6.1 Intent Ambiguity
**Problem:** "Make the bishop a dolphin" — is this visual, behavioral, or both?
**Solution:** If confidence < 0.7, ask. Use a few-shot clarifying prompt.
```
Human: "make it blue"
Agent: "Which piece should be blue?"
```

### 6.2 Multi-step Rollback
**Problem:** After 10 changes, human says "undo back to the octopus version"
**Solution:** Undo stack stores pre-image snapshots. Agent can walk back N steps or search for snapshot tagged with "octopus".

### 6.3 Conflicting Edits
**Problem:** Human types "make bishop a dolphin" then immediately types "no, make it a shark"
**Solution:** Listener debounces with 500ms cooldown. If second input arrives before plan execution starts, merge intents. If during execution, queue and apply after current plan completes.

### 6.4 Asset Generation Failure
**Problem:** Image generation produces garbage
**Solution:** Agent detects via size/content check. Retries with different prompt. After 3 failures, responds "I couldn't generate that sprite — want to try a different animal or choose from templates?"

### 6.5 Render Adapter Lag
**Problem:** Render adapter is slow to pick up changes
**Solution:** Render trigger tile includes a timestamp. Adapter polls every 100ms (same as listener). If adapter hasn't picked up in 500ms, agent self-alerts.

---

## 7. Future Directions

### 7.1 Multi-model Orchestration
Use different models for different subtasks, routed automatically:
- **Zero-shot changes** → fast models (glm-4.7-flash)
- **Novel mechanics** → reasoning models (kimi-cli / deepseek-v4)
- **Art generation** → vision models (Qwen3-VL)
- **Architecture changes** → full PLATO-aware agents (glm-5.1)

### 7.2 Learning from Iteration
The agent can learn human preferences over time:
- "Casey always wants bishops to be animals" → store preference
- "Casey prefers blue palette" → palette preference
- Store in `app-vibe/preferences` tile

### 7.3 Predictive Pre-building
After N iterations, the agent can predict likely next changes and pre-build:
- If human just changed the bishop, they'll probably change the rook next
- Pre-load rook templates into cache
- Reduce perceived latency to sub-200ms

### 7.4 Persistent Agent Memory
Store agent-state across sessions:
```
app-vibe/
├── preferences/      # Learned human preferences
├── templates/        # Reusable sprite/behavior templates
├── change-history/   # Full session history for rollback
└── patterns/         # Common change patterns detected
```

---

## 8. Summary

| Aspect | Answer |
|---|---|
| **Agent architecture** | Pipeline of micro-agents: Listener → Resolver → Planner → Executor → Responder. Each component handles one concern. |
| **Loop speed** | < 2s target achievable with fast model (glm-4.7-flash) for NL, kimi-cli for code gen, and render trigger polling. |
| **Key tools** | kimi-cli (code gen), glm-4.7-flash (NL), Qwen3-VL (assets), LÖVE2D (render target for speed). |
| **Simplest impl** | 200-line Python agent that reads/writes PLATO tiles, maps 5 intents, triggers LÖVE2D re-render. |
| **Protocol** | PLATO tiles as the coordination bus. Agent writes to `app-vibe/`, reads from `app-io/`, triggers via render trigger tile. |
| **Failure handling** | Clarify ambiguity, snapshot for undo, retry asset gen 3x, debounce rapid input. |
| **Future** | Multi-model orchestration, learning preferences, predictive pre-building, persistent agent memory. |

---

**Next action:** Build the v0.1 agent prototype with kimi-cli code gen support. Connect to a LÖVE2D chess renderer. Test the loop: "make bishop a dolphin" → < 2s.
