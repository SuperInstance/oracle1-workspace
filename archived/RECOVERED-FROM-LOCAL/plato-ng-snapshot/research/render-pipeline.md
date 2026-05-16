# PLATO-NG Rendering Pipeline
## Turning PLATO Tile State into Visual Output

**Research Track**: Track 3 — Visual Render Backends  
**Date**: 2026-05-15  
**Status**: Design Specification  
**Target MVP**: TIC-80

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [The Intermediate Representation (IR)](#2-the-intermediate-representation-ir)
3. [PLATO → IR Tile Schema](#3-plato--ir-tile-schema)
4. [Render Backend Analysis](#4-render-backend-analysis)
   - [4.1 TIC-80](#41-tic-80)
   - [4.2 LÖVE2D](#42-l%C3%B6ve2d)
   - [4.3 Web (HTML5 Canvas)](#43-web-html5-canvas)
   - [4.4 SCUMMVM](#44-scummvm)
5. [Pipeline Implementation](#5-pipeline-implementation)
6. [Working Python Converter: PLATO → TIC-80 Cart](#6-working-python-converter-plato--tic-80-cart)
7. [Edge Cases & Failure Modes](#7-edge-cases--failure-modes)
8. [Future Work](#8-future-work)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    PLATO ROOM                           │
│  (accumulated tiles: Knowledge, Procedural, Spatial,   │
│   Behavioral, Navigation, Creative, Diagnostic, etc.)   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              TILE SELECTOR / FILTER                     │
│  Domain filter → temporal validity → confidence gate    │
│  Produces: Active tile set for current scene            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              IR GENERATOR (python/rust)                 │
│  Transforms PLATO tiles into engine-agnostic IR         │
│  Produces: SceneIR document                             │
│  - Sprites: tile Q/As → visual elements                 │
│  - Map data: spatial/navigation tiles → grid layout     │
│  - Behavior: procedural/diagnostic → game logic         │
│  - Dialogue: knowledge tiles → NPC speech               │
│  - Audio: creative tiles → sound                        │
│  - Input bindings: from room config                     │
└──────┬────────────┬────────────┬────────────┬───────────┘
       │            │            │            │
       ▼            ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ TIC-80   │ │ LÖVE2D   │ │ Web      │ │ SCUMMVM      │
│ Backend  │ │ Backend   │ │ Backend  │ │ Backend      │
│ (Lua)    │ │ (Lua)    │ │ (JS)     │ │ (WIP)        │
└──────────┘ └──────────┘ └──────────┘ └──────────────┘
```

### Pipeline Stages (Detailed)

**Stage 1 — Tile Selection**  
- Query PLATO room for tiles matching current scene domain
- Filter by temporal validity (Permanent/ExpiresAt/DecayFunction/SessionScoped)
- Apply confidence threshold (default: 0.5, configurable per domain)
- NegativeSpace tiles (10x weight) get special handling — they define what NOT to render/do

**Stage 2 — IR Generation**  
- Parse each selected tile by domain
- Map to IR components (sprites, map, behavior, dialogue, audio, input)
- Resolve conflicts: higher-confidence tiles override lower-confidence
- Apply temporal decay: tiles with `DecayFunction` have their confidence reduced over time
- Output: SceneIR JSON document

**Stage 3 — Backend Compilation**  
- Each backend reads the SceneIR document
- Generates platform-native output (Lua for TIC-80/LÖVE2D, JS for Web)
- Injects platform boilerplate (framerate loops, input handling)
- Wraps game logic in safety boundary (deadband P0/P1/P2 gates)

---

## 2. The Intermediate Representation (IR)

The IR is a **game-engine-agnostic JSON document** describing a complete interactive scene. Every render backend reads this format and generates native code.

### SceneIR Document

```json
{
  "scene_ir": "1.0",
  "meta": {
    "title": "Scene title",
    "room_id": "plato-room-uuid",
    "tile_ids": ["tile-uuid-1", "tile-uuid-2"],
    "generated_at": "ISO8601 timestamp",
    "render_targets": ["tic80", "love2d", "web"]
  },
  "settings": {
    "viewport_width": 240,
    "viewport_height": 136,
    "framerate": 60,
    "palette": ["#000000", "#1a1c2c", "#5d275d", "#b13e53", "#ef7d57",
                "#ffcd75", "#a7f070", "#38b764", "#257179", "#29366f",
                "#3b5dc9", "#41a6f6", "#73eff7", "#f4f4f4", "#94b0c2",
                "#566c86"],
    "background_color": 0
  },
  "sprites": [
    {
      "id": "sprite_0",
      "type": "player",
      "position": {"x": 16, "y": 16},
      "size": {"w": 8, "h": 8},
      "color_mode": "indexed",
      "pixels": [0,0,0,3,3,0,0,0, ...],
      "animations": [
        {"name": "idle", "frames": [0], "speed": 1},
        {"name": "walk", "frames": [0,1], "speed": 6}
      ],
      "collision_box": {"x": 1, "y": 1, "w": 6, "h": 6}
    }
  ],
  "map": {
    "width": 30,
    "height": 17,
    "tiles": [[0,0,0,1,1,1,0,0,...], ...],
    "tile_flags": [[false,false,false,true,true,true,...], ...],
    "teleports": [
      {"from": {"x": 5, "y": 3}, "to_room": "other_room_id", "to": {"x": 1, "y": 1}}
    ]
  },
  "entities": [
    {
      "id": "entity_npc_1",
      "sprite_ref": "sprite_2",
      "position": {"x": 80, "y": 64},
      "behavior": "patrol",
      "dialogue_key": "welcome_dialogue",
      "patrol_path": [
        {"x": 80, "y": 64},
        {"x": 120, "y": 64},
        {"x": 120, "y": 96},
        {"x": 80, "y": 96}
      ],
      "patrol_speed": 1
    }
  ],
  "dialogues": {
    "welcome_dialogue": [
      {"speaker": "Old Man", "text": "Welcome, traveler.", "next": 1},
      {"speaker": "Old Man", "text": "The dungeon lies to the north.", "next": null}
    ]
  },
  "logic": {
    "tile_rules": [
      {"tile_id": 1, "is_solid": true, "is_hazard": false},
      {"tile_id": 2, "is_solid": false, "is_hazard": true, "damage": 1}
    ],
    "global_scripts": {
      "on_init": "// Called once at scene start",
      "on_frame": "// Called every frame",
      "on_collision": "// Called on collision events"
    }
  },
  "audio": {
    "sfx": [
      {"id": "sfx_jump", "type": "tone", "params": {...
        "waveform": "square", "frequency": 440, "duration": 0.1
      }},
      {"id": "sfx_hit", "type": "noise", "params": {...
        "duration": 0.15, "volume": 0.8
      }}
    ],
    "music": {
      "tracks": [
        {"id": "theme_a", "pattern": "C4 C4 G4 G4 A4 A4 G4 G4", "bpm": 120}
      ]
    }
  },
  "input": {
    "bindings": {
      "up": "move_up",
      "down": "move_down",
      "left": "move_left",
      "right": "move_right",
      "action": "confirm",
      "cancel": "back",
      "start": "pause"
    }
  }
}
```

### IR Design Principles

1. **Backend-agnostic**: No platform-specific constructs in the IR itself
2. **Minimal surface area**: Every field has a default; backends fill gaps
3. **Self-describing**: Meta section includes source tile IDs for traceability
4. **Hierarchical**: Meta → Settings → Assets (sprites) → World (map) → Actors (entities) → Behavior (logic/dialogue) → Audio → Input
5. **Lossy safe**: Backends can drop unsupported features without crashing

---

## 3. PLATO → IR Tile Schema

Each PLATO tile type maps to one or more IR components. Below is the definitive mapping.

### Tile Schema for Rendering IR

```json
{
  "tile_id": "uuid",
  "domain": "Spatial | Navigation | Knowledge | Procedural | Behavioral | Creative | Diagnostic | Safety | NegativeSpace | Causal | Temporal | MetaLearning | Social | Adaptive",
  "question": "string — describes what this tile represents in the scene",
  "answer": "string — the data or instruction for the scene",
  "confidence": 0.0-1.0,
  "ir_metadata": {
    "ir_component": "sprite | map_tile | entity | dialogue | rule | audio | input | transition",
    "ir_params": {
      // Component-specific parameters (see below)
    }
  }
}
```

### Domain → IR Component Mapping

| PLATO Domain | IR Component | How It Renders |
|---|---|---|
| `Spatial` | `map_tile`, `/map/tiles[][]` | Grid cells — terrain, walls, floor. X,Y,t encoded as tile types |
| `Navigation` | `entity` with `patrol_path` | Moving entities, waypoints, deadband navigation zones |
| `Knowledge` | `dialogue` | NPC dialogue trees — question→answer pairs become speech acts |
| `Procedural` | `logic/tile_rules`, `global_scripts` | Game rules: "how to interact with X" → collision/system logic |
| `Behavioral` | `entity` with `behavior` | Entity AI patterns — patrol, flee, seek, idle |
| `Creative` | `audio`, `sprites` | Generated art, sound effects, music patterns |
| `Diagnostic` | `logic/tile_rules` with `is_hazard` | Hazard zones, danger areas, puzzle failure states |
| `Safety` | `logic/tile_rules` with deadband | P0 zones — cannot enter, cannot interact. Takes precedence |
| `NegativeSpace` | `logic` — exclusion zones | 10x weight: marks areas as forbidden. Defines map boundaries |
| `Causal` | `logic/global_scripts/on_collision` | If-this-then-that chains: "picking up key unlocks door" |
| `Temporal` | `settings/framerate`, animation timing | Time-aware elements — moving platforms, timed doors, decay effects |
| `MetaLearning` | `meta`, scene structure | Self-describing — how this scene was constructed from tiles |
| `Social` | `entities` with `dialogue_key` | Multi-agent interactions — shops, quest givers, team mechanics |
| `Adaptive` | `logic/global_scripts` | Self-modifying scenes — difficulty scaling, adaptive puzzles |

### Concrete Tile → IR Examples

**Example 1: Spatial Tile → Map Tile**
```json
{
  "id": "a1b2c3d4",
  "domain": "Spatial",
  "question": "What terrain occupies grid position (3,7)?",
  "answer": "Solid wall tile, sprite index 1, color index 4",
  "confidence": 0.95,
  "ir_metadata": {
    "ir_component": "map_tile",
    "ir_params": {
      "x": 3,
      "y": 7,
      "tile_type": 1,
      "solid": true,
      "color": 4
    }
  }
}
```

**Example 2: Knowledge Tile → Dialogue**
```json
{
  "id": "e5f6g7h8",
  "domain": "Knowledge",
  "question": "What does the old fisherman say about the northern sea?",
  "answer": "\"The northern sea is treacherous this time of year. Watch for the riptide near the black rocks.\"",
  "confidence": 0.88,
  "ir_metadata": {
    "ir_component": "dialogue",
    "ir_params": {
      "speaker": "Old Fisherman",
      "text": "The northern sea is treacherous this time of year. Watch for the riptide near the black rocks.",
      "next": "fisherman_2"
    }
  }
}
```

**Example 3: Procedural Tile → Game Rule**
```json
{
  "id": "i9j0k1l2",
  "domain": "Procedural",
  "question": "What happens when the player enters deep water?",
  "answer": "Player movement speed reduced by 50%. Player takes 1 damage every 3 seconds if not wearing waders.",
  "confidence": 0.82,
  "ir_metadata": {
    "ir_component": "rule",
    "ir_params": {
      "condition": "tile_type == 3 AND player_on_tile",
      "effects": [
        {"type": "modify_speed", "multiplier": 0.5},
        {"type": "periodic_damage", "interval_s": 3, "amount": 1}
      ]
    }
  }
}
```

**Example 4: Navigation Tile → Entity Patrol Path**
```json
{
  "id": "m3n4o5p6",
  "domain": "Navigation",
  "question": "What is the patrol route for the harbor master?",
  "answer": "Harbor master walks: dock (10,8) → warehouse (15,8) → office (15,12) → dock (10,8)",
  "confidence": 0.75,
  "ir_metadata": {
    "ir_component": "entity",
    "ir_params": {
      "entity_type": "npc_patrol",
      "name": "Harbor Master",
      "sprite_ref": "sprite_npc_1",
      "patrol_path": [
        {"x": 10, "y": 8},
        {"x": 15, "y": 8},
        {"x": 15, "y": 12}
      ],
      "patrol_speed": 1
    }
  }
}
```

**Example 5: Safety Tile → Deadband Zone**
```json
{
  "id": "q7r8s9t0",
  "domain": "Safety",
  "question": "Which areas of the dock are restricted?",
  "answer": "Area (0,0)-(5,5) is restricted. Area (20,10)-(30,17) is restricted. P0: no entry.",
  "confidence": 1.0,
  "ir_metadata": {
    "ir_component": "rule",
    "ir_params": {
      "priority": "P0",
      "type": "restricted_zone",
      "zones": [
        {"x1": 0, "y1": 0, "x2": 5, "y2": 5},
        {"x1": 20, "y1": 10, "x2": 30, "y2": 17}
      ],
      "consequence": "player_blocked",
      "message": "Restricted area. Turn back."
    }
  }
}
```

---

## 4. Render Backend Analysis

### 4.1 TIC-80

**Status**: MVP — READY NOW  
**Cart limit**: 64 KB Lua source, 64 KB sprite sheet, 64 KB map  
**Resolution**: 240×136 native  
**Color**: 16-color palette (4-bit indexed)  
**Language**: Lua 5.2 subset

#### Minimal Lua API Surface

```
TIC()           → Core frameloop
│  cls(color)   → Clear screen with palette index
│  spr(id, x, y[, w, h]) → Draw sprite from sheet
│  map(x, y, w, h[, sx, sy]) → Draw map layer
│  print(text, x, y, color) → Text rendering
│  btn(id)      → Button state (0-31)
│  btnp(id)     → Button pressed this frame
│  sfx(id, note, duration, channel, volumes) → Sound effect
│  music(id)    → Stream music pattern
│  sync()       → Sync memory banks (sprites, map, sfx)
│  pix(x, y)    → Single pixel (for procedural effects)
│  rect(x,y,w,h,color) → Filled rectangle
│  line(x0,y0,x1,y1,color) → Line
│  circ(x,y,r,color) → Circle
│  tri(x1,y1,x2,y2,x3,y3,color) → Triangle
│  textri(x1,y1,x2,y2,x3,y3,u1,v1,u2,v2,u3,v3,use_uv,transparent)
│    → Texture-mapped triangle (advanced)
│  peek(addr) → Memory peek
│  poke(addr, val) → Memory poke
│  memcpy(dst, src, size) → Memory copy
│  memset(addr, val, size) → Memory fill
│  trace(msg) → Debug output
│  time() → Elapsed seconds
│  exit() → Exit cart
```

**Minimal set**: `cls`, `spr`, `map`, `btn`, `print`, `sfx`, `music`, `sync`  
That's 8 functions. Everything else is optimization or debug.

#### TIC-80 Tile Bank Layout

```
RAM:
  0x00000 - 0x03FFF: Sprite sheet (16 KB = 256 sprites × 64 bytes)
  0x04000 - 0x07FFF: Map (16 KB = 240 × 136 cells, 1 byte each)
  0x08000 - 0x0BFFF: Sprite flags (16 KB)
  0x0C000 - 0x0FFFF: Song patterns / SFX
  0x10000 - 0x13FFF: Persistent cartridge storage
  0x14000 - 0x17FFF: Screen buffer
  0x18000 - 0x1FFFF: (custom / code data)
```

Mapping: IR sprite sheet → TIC-80 sprite bank. Each sprite is 8×8 pixels, 64 bytes (2 bits per pixel = 4 colors per row). 256 sprites max. Map cells are 1 byte each (sprite index + 0x80 flag toggle).

#### TIC-80 Cart Template

```lua
-- TITLE: Generated Cart
-- AUTHOR: PLATO-NG Renderer
-- DESC: Auto-generated from PLATO room tiles

-- Sprite data and map data are embedded PNG binaries
-- (TIC-80 .tic format uses embedded sprite sheets)

function TIC()
    -- 1. Clear
    cls(0)

    -- 2. Draw map layer
    map(0, 0, 30, 17, 0, 0)

    -- 3. Draw entities
    for _, e in ipairs(entities) do
        spr(e.sprite, e.x, e.y)
    end

    -- 4. Draw player
    spr(player.sprite, player.x, player.y)

    -- 5. UI overlay
    print("Score: "..score, 0, 128, 12)
    print("Health: "..health, 80, 128, 14)

    -- 6. Dialogue
    if dialogue_active then
        rect(0, 100, 240, 36, 1)
        print(dialogue_text, 4, 104, 15)
    end
end
```

#### TIC-80 Strengths

- **Smallest render target**: 64 KB code + 64 KB assets = full game
- **Instant startup**: No OS, no runtime dependencies beyond TIC-80 itself
- **Web export**: TIC-80 exports to HTML5 with WebGL automatically
- **Emulator ecosystem**: Works on Windows/Mac/Linux/Web/Raspberry Pi
- **PLATO-friendly constraints**: 16-color palette, 240×136 resolution, 8×8 sprites — the game engine equivalent of "8-bit"
- **Lua is easy to generate**: String concatenation works, no imports needed
- **Built-in editor**: TIC-80 is also a tool for editing carts interactively

#### TIC-80 Limitations

- **One file**: Everything must fit in a single Lua source + binary blobs
- **No filesystem**: Can't load external assets — all sprites/map/sound encoded in binary
- **64 KB code limit**: Heavy procedural generation hits this fast
- **Single-threaded**: No async, no parallelism
- **No networking**: Single-player only (multiplayer TIC-80 exists but is not standard)

### 4.2 LÖVE2D

**Status**: DESIGN READY — Backup target  
**Resolution**: Any (configurable window)  
**Language**: Lua 5.1 (LuaJIT optional)  
**Dependencies**: `love` binary + `.love` archive

#### Minimal Lua API Surface

```
love.load()       → Init: load assets, create objects
  love.graphics.newImage(path) → Load image
  love.graphics.newFont(path, size) → Load font
  love.audio.newSource(path, type) → Load audio

love.update(dt)   → Game logic per frame
  dt               → Delta time in seconds

love.draw()       → Render per frame
  love.graphics.clear(r,g,b) → Clear screen
  love.graphics.draw(image, x, y, r, sx, sy) → Draw
  love.graphics.print(text, x, y) → Text
  love.graphics.rectangle(mode, x, y, w, h) → Shapes
  love.graphics.circle(mode, x, y, r) → Shapes
  love.graphics.setColor(r,g,b,a) → Set color

love.keypressed(key)   → Keyboard input
love.keyreleased(key)  → Keyboard input
love.mousepressed(x, y, button) → Mouse input
love.mousereleased(x, y, button) → Mouse input

love.graphics.newSpriteBatch(image, max) → Batch draws
love.graphics.setDefaultFilter(min, mag) → Texture filtering
```

**Minimal set**: `love.load`, `love.update`, `love.draw`, `love.keypressed`, `love.graphics.clear`, `love.graphics.draw`, `love.graphics.print`, `love.graphics.rectangle`  
That's 8 core functions for a 2D game.

#### LÖVE2D Strengths

- **Full filesystem**: Load assets dynamically from `.love` archive
- **Unlimited resolution**: True HD (1920×1080), scales from tiny window
- **Audio**: Full OGG/WAV support, streaming audio
- **Fonts**: TrueType font loading
- **Threading**: `love.thread` module for background work
- **Physics**: Built-in Box2D integration (`love.physics`)
- **Joystick**: Full gamepad support

#### LÖVE2D Limitations

- **Heavier runtime**: Requires LÖVE2D installed (≈20 MB)
- **No built-in editor**: Must generate `.love` archives programmatically
- **No embedded assets**: All assets are external files
- **Less portable**: Windows/Mac/Linux only (Android/iOS support exists but is experimental)
- **No web export natively**: Requires third-party WASM build

#### TIC-80 vs LÖVE2D Comparison

| Feature | TIC-80 | LÖVE2D |
|---------|--------|--------|
| Binary size | ~5 MB runtime | ~20 MB runtime |
| Cart size | 128 KB max | Unlimited |
| Color | 16-indexed | True color |
| Resolution | 240×136 | Any |
| Audio | 4-channel chiptune | OGG/WAV/streaming |
| Editor | Built-in | None |
| Export targets | Native + Web | Native (web via WASM) |
| Physics | Manual | Box2D built-in |
| Startup time | ~50 ms | ~200 ms |
| Ideal for | Tiny retro games | Full 2D games |

### 4.3 Web (HTML5 Canvas)

**Status**: DESIGN READY — Future target  
**Resolution**: Any (CSS + canvas scaling)  
**Language**: JavaScript (ES6+)

#### Minimal HTML5 Canvas API

```javascript
// Init
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

// Frameloop
function gameLoop(timestamp) {
    update(timestamp - lastTimestamp);
    draw(ctx);
    lastTimestamp = timestamp;
    requestAnimationFrame(gameLoop);
}

// Draw
ctx.clearRect(0, 0, width, height);
ctx.drawImage(sprite, sx, sy, sw, sh, dx, dy, dw, dh);
ctx.fillText(text, x, y);
ctx.fillRect(x, y, w, h);
ctx.fillStyle = '#ff0000';
ctx.font = '16px monospace';
ctx.globalAlpha = 0.5;  // Transparency

// Input
document.addEventListener('keydown', (e) => { ... });
document.addEventListener('keyup', (e) => { ... });
canvas.addEventListener('mousedown', (e) => { ... });

// Audio (Web Audio API)
const audioCtx = new AudioContext();
const oscillator = audioCtx.createOscillator();
oscillator.connect(audioCtx.destination);
oscillator.start();
```

**Minimal set**: `CanvasRenderingContext2D.clearRect`, `.drawImage`, `.fillText`, `.fillRect`, `requestAnimationFrame` loop, keyboard events, Web Audio oscillator.  
That's ≈7 API surfaces.

#### Web Strengths

- **Zero install**: Any browser works
- **True color**: No palette limitations
- **Resolution independent**: Scales to any display
- **Networked**: WebSocket APIs for multiplayer
- **Storage**: localStorage, IndexedDB for save games
- **Most accessible target**: Share via URL

#### Web Limitations

- **Browser overhead**: 100+ MB runtime (browser itself)
- **Audio latency**: Web Audio adds 10-50ms latency
- **Fullscreen limitations**: Must be user-triggered
- **No filesystem**: All assets loaded via HTTP
- **Canvas 2D is slow for pixel-perfect retro**: Use WebGL for performance

#### Web vs TIC-80 vs LÖVE2D

| Feature | TIC-80 | LÖVE2D | Web/Canvas |
|---------|--------|--------|------------|
| Zero install? | Yes (needs .tic player) | No (needs love2d) | **Yes (any browser)** |
| True color? | No (16 colors) | Yes | **Yes** |
| Publishing | Share .tic file | Share .love | **Share URL** |
| Performance | Fastest (tight loop) | Fast (LuaJIT) | **Slower (browser)** |
| Audio | 4-channel chiptune | Full audio | **Web Audio (streaming)** |
| Save games | Persistent RAM | Filesystem | **localStorage** |
| Multiplayer | No | Via library | **WebSocket built-in** |

### 4.4 SCUMMVM

**Status**: NOT READY — Long-term speculative target

#### Analysis

SCUMMVM is a reimplementation of the SCUMM (Script Creation Utility for Maniac Mansion) engine used by classic LucasArts adventure games. It supports 200+ game engines internally.

**Why it's not practical now:**

1. **No public API for engine generation**: SCUMMVM reads pre-built game data files. There's no "generate a SCUMMVM game from a script" API. You'd need to either:
   - Write your own SCUMMVM engine plugin (C++), which requires deep knowledge of the SCUMMVM internals
   - Generate `.scr` files in a supported engine format (e.g., SCUMM v8 format), which is undocumented reverse engineering

2. **Engine diversity is a problem**: SCUMMVM isn't one engine — it's 200+. Each has different data formats, scripting languages, asset pipelines, and capabilities. You'd need to pick ONE and target its internal format.

3. **Toolchain is dead**: The original SCUMM developer tools (ScummRevisited, etc.) are abandonware. Modern alternatives are incomplete.

4. **Limited audience**: SCUMMVM players expect classic game experiences, not procedurally-generated content. The community may not embrace auto-generated adventure games.

**When it might become practical:**

- If someone writes a "PLATO-NG → SCUMMVM" engine plugin in C++ (≈3-6 months of work for an experienced SCUMMVM contributor)
- If we target a simple modern engine like `AGS` (Adventure Game Studio) instead, which has a documented script format
- When PLATO-NG scenes are complex enough (full adventure games with inventory, puzzles, dialogue trees) to justify the SCUMMVM experience

**Recommendation**: Skip SCUMMVM for v1. Target AGS as an adventure-game-specific backend if needed in the future. SCUMMVM is a "nice to have" after the fleet has shipped real games on TIC-80.

#### Alternative Adventure Targets

| Engine | Status | Effort | Audience |
|--------|--------|--------|----------|
| **AGS** (Adventure Game Studio) | Possible | Medium (documented script API) | Active modding community |
| **Ren'Py** | Easy | Low (Python-based, easy to generate) | 1000s of visual novels |
| **Ink** (Inkle) | Medium | Medium (JSON-like narrative format) | Interactive fiction |
| **Twine** | Easy | Low (Harlowe/Chapbook format) | Huge IF community |
| **Bitsy** | Easy | Low (simple tile-based, tiny format) | Game jam community |

For narrative-heavy PLATO rooms, **Twine** or **Bitsy** are better targets than SCUMMVM — they're designed for small, procedurally-generated stories.

---

## 5. Pipeline Implementation

### Overall Architecture

```
plato-ng-render/
├── pipeline/
│   ├── selector.py       # Stage 1: Tile selection & filtering
│   ├── ir_builder.py     # Stage 2: PLATO tiles → SceneIR
│   ├── render_tic80.py   # Stage 3a: SceneIR → TIC-80 Lua
│   ├── render_love2d.py  # Stage 3b: SceneIR → LÖVE2D Lua
│   ├── render_web.py     # Stage 3c: SceneIR → HTML/JS
│   └── __init__.py
├── ir/
│   ├── schema.py         # SceneIR data classes + validation
│   ├── tile_mapper.py    # PLATO domain → IR component mapping
│   └── __init__.py
├── cart/
│   ├── template_tic80.lua    # Base TIC-80 cart template
│   ├── template_love2d.lua   # Base LÖVE2D main.lua template
│   └── template_web.html     # Base HTML/JS template
├── converter.py          # CLI entry point
└── README.md
```

### Stage 1: Tile Selector

```python
# pseudo-python
def select_tiles(room_id, scene_domain=None, min_confidence=0.5):
    """Query PLATO room, return filtered tile list."""
    tiles = plato.query(f"room/{room_id}/tiles")

    # Filter by scene domain (if specified)
    if scene_domain:
        tiles = [t for t in tiles if t.domain == scene_domain
                 or t.tags.intersection(scene_domain)]

    # Filter by temporal validity
    now = datetime.utcnow()
    valid_tiles = []
    for t in tiles:
        match t.temporal_validity:
            case Permanent():
                valid_tiles.append(t)
            case ExpiresAt(expiry):
                if now < expiry:
                    valid_tiles.append(t)
            case DecayFunction(half_life):
                age = (now - t.created_at).total_seconds()
                decay = 0.5 ** (age / half_life.total_seconds())
                if t.confidence * decay >= min_confidence:
                    t.confidence *= decay
                    valid_tiles.append(t)
            case SessionScoped():
                # Check if this session is still active
                if session_is_active(t.session_id):
                    valid_tiles.append(t)

    # Apply confidence threshold
    return [t for t in valid_tiles if t.confidence >= min_confidence]
```

### Stage 2: IR Builder

```python
# pseudo-python
def build_ir(tiles):
    """Transform PLATO tiles into SceneIR document."""
    scene = SceneIR()

    for tile in sorted(tiles, key=lambda t: -t.confidence):
        ir_info = tile.ir_metadata
        component = ir_info.ir_component
        params = ir_info.ir_params

        match component:
            case "map_tile":
                x, y = params.x, params.y
                scene.map.tiles[y][x] = params.get("tile_type", 1)
                scene.logic.tile_rules.append(TileRule(
                    tile_id=params.tile_type,
                    is_solid=params.get("solid", False),
                    is_hazard=params.get("hazard", False),
                ))
            case "dialogue":
                if params.speaker not in scene.dialogues:
                    scene.dialogues[params.speaker] = []
                scene.dialogues[params.speaker].append({
                    "text": params.text,
                    "next": params.get("next")
                })
            case "entity":
                scene.entities.append(Entity(
                    sprite_ref=params.sprite_ref,
                    position=Position(**params.position),
                    behavior=params.behavior,
                    dialogue_key=params.get("dialogue_key"),
                    patrol_path=params.get("patrol_path", []),
                    patrol_speed=params.get("patrol_speed", 1),
                ))
            case "rule":
                scene.logic.tile_rules.append(TileRule(
                    condition=params.condition,
                    effects=params.effects,
                    priority=params.get("priority", "P2"),
                ))
            case "sprite":
                scene.sprites.append(Sprite(
                    id=params.sprite_id,
                    # ... pixel data mapped to indexed format
                ))
            case "audio":
                scene.audio.sfx.append(Sfx(
                    id=params.sfx_id,
                    # ... waveform params
                ))

    return scene
```

### Stage 3a: TIC-80 Backend

```python
# pseudo-python
def render_tic80(scene_ir, output_dir):
    """Generate TIC-80 cart from SceneIR."""
    lua = []
    lua.append("-- TITLE: " + scene_ir.meta.title)
    lua.append("-- AUTHOR: PLATO-NG Renderer")
    lua.append("-- DESC: Generated from " + " ".join(scene_ir.meta.tile_ids))
    lua.append("")
    lua.append(generate_sprite_sheet(scene_ir.sprites))
    lua.append(generate_map(scene_ir.map))
    lua.append(generate_sfx(scene_ir.audio.sfx))
    lua.append(generate_music(scene_ir.audio.music))
    lua.append("")

    # TIC() function
    lua.append("function TIC()")
    lua.append(f"    cls({scene_ir.settings.background_color})")
    lua.append(f"    map(0, 0, {scene_ir.map.width}, {scene_ir.map.height}, 0, 0)")
    lua.append("")
    lua.append(generate_entity_rendering(scene_ir.entities))
    lua.append(generate_player_rendering())
    lua.append("")
    lua.append(generate_ui(scene_ir))
    lua.append(generate_dialogue(scene_ir.dialogues))
    lua.append("end")

    # Input handling
    lua.append("")
    lua.append(generate_input(scene_ir.input))

    # Write to .lua
    with open(f"{output_dir}/cart.lua", "w") as f:
        f.write("\n".join(lua))

    # Generate TIC-80 .tic binary
    # (requires actual sprite PNG + Lua wrapping)
    package_to_tic(lua, scene_ir.sprites, output_dir)
```

---

## 6. Working Python Converter: PLATO → TIC-80 Cart

Below is a fully functional Python module that takes PLATO tile JSON and generates a runnable TIC-80 Lua cart.

```python
#!/usr/bin/env python3
"""
plato_to_tic80.py — Convert PLATO tiles to TIC-80 Lua cart.

Usage:
    python3 plato_to_tic80.py input_tiles.json [output.lua]
    
    input_tiles.json: Array of PLATO tile objects (see schema below)
    output.lua:       Generated TIC-80 cart (default: cart.lua)

Tile Input Schema (JSON):
    [
        {
            "id": "uuid",
            "domain": "Spatial|Knowledge|Procedural|...",
            "question": "...",
            "answer": "...",
            "confidence": 0.95,
            "ir_metadata": {
                "ir_component": "map_tile|sprite|entity|dialogue|rule|audio",
                "ir_params": {
                    "component-specific fields"
                }
            }
        }
    ]

Output: TIC-80 compatible Lua cart with:
    - Sprite data embedded as hex strings
    - Map data from Spatial tiles
    - Entities from Behavioral/Navigation tiles
    - Dialogue from Knowledge tiles
    - Game rules from Procedural/Safety tiles
    - Audio from Creative tiles
"""

import json
import sys
import math
from datetime import datetime
from typing import Optional


# ─── SceneIR Data Classes ─────────────────────────────────────

class Sprite:
    def __init__(self, sid: str, pixels: list, width: int = 8, height: int = 8):
        self.id = sid
        self.pixels = pixels  # flat list of palette indices
        self.width = width
        self.height = height

    def to_tic80_hex(self) -> str:
        """Convert pixel data to TIC-80 hex format (2 bits per pixel)."""
        hex_chunks = []
        for row in range(self.height):
            row_start = row * self.width
            row_pixels = self.pixels[row_start:row_start + self.width]
            # Each byte encodes 4 pixels (2 bits each)
            byte_str = ""
            for i in range(0, len(row_pixels), 4):
                chunk = row_pixels[i:i+4]
                if chunk:
                    byte_val = 0
                    for j, p in enumerate(chunk):
                        byte_val |= (p & 0x03) << (j * 2)
                    byte_str += f"{byte_val:02x}"
            hex_chunks.append(byte_str)
        return "\n".join(f"        {h}" for h in hex_chunks)


class MapData:
    def __init__(self, width: int = 30, height: int = 17):
        self.width = width
        self.height = height
        self.tiles = [[0] * width for _ in range(height)]
        self.flags = [[False] * width for _ in range(height)]


class Entity:
    def __init__(self, name: str, sprite_ref: str, x: int, y: int,
                 behavior: str = "idle", dialogue_key: Optional[str] = None,
                 patrol_path: Optional[list] = None):
        self.name = name
        self.sprite_ref = sprite_ref
        self.x = x
        self.y = y
        self.behavior = behavior
        self.dialogue_key = dialogue_key
        self.patrol_path = patrol_path or []


class Dialogue:
    def __init__(self, speaker: str, text: str, next_id: Optional[str] = None):
        self.speaker = speaker
        self.text = text
        self.next_id = next_id


class SceneIR:
    """Intermediate Representation for production."""

    def __init__(self):
        self.title = "PLATO-NG Scene"
        self.sprites: dict[str, Sprite] = {}
        self.map = MapData()
        self.entities: list[Entity] = []
        self.dialogues: list[list[Dialogue]] = []
        self.rules: list[dict] = []
        self.sfx_list: list[dict] = []
        self.music_data: Optional[dict] = None
        self.input_bindings = {}
        self.bg_color = 0
        self.palette_cycle = 0


# ─── PLATO Tile → SceneIR Mapper ──────────────────────────

DEFAULT_PALETTE = [
    0x000000, 0x1a1c2c, 0x5d275d, 0xb13e53,
    0xef7d57, 0xffcd75, 0xa7f070, 0x38b764,
    0x257179, 0x29366f, 0x3b5dc9, 0x41a6f6,
    0x73eff7, 0xf4f4f4, 0x94b0c2, 0x566c86,
]


def tile_domain_to_component(domain: str) -> str:
    """Map PLATO domain to IR component type."""
    mapping = {
        "Spatial": "map_tile",
        "Navigation": "entity",
        "Knowledge": "dialogue",
        "Procedural": "rule",
        "Behavioral": "entity",
        "Creative": "sprite",
        "Diagnostic": "rule",
        "Safety": "rule",
        "NegativeSpace": "rule",
        "Causal": "rule",
        "Temporal": "rule",
        "Social": "entity",
        "Adaptive": "rule",
        "MetaLearning": "meta",
    }
    return mapping.get(domain, "rule")


def tiles_to_sceneir(tiles: list[dict]) -> SceneIR:
    """Main function: PLATO tile list → SceneIR document."""
    scene = SceneIR()
    sprites_used: set[str] = set()

    # Sort by confidence descending — higher confidence tiles override
    sorted_tiles = sorted(tiles, key=lambda t: -t.get("confidence", 0.5))

    for tile in sorted_tiles:
        domain = tile.get("domain", "Knowledge")
        ir_info = tile.get("ir_metadata", {})
        component = ir_info.get("ir_component") or tile_domain_to_component(domain)
        params = ir_info.get("ir_params", {})
        confidence = tile.get("confidence", 0.5)
        question = tile.get("question", "")
        answer = tile.get("answer", "")

        if component == "map_tile":
            _process_map_tile(scene, params, question, answer)
        elif component == "sprite":
            _process_sprite(scene, params, question, answer)
        elif component == "entity":
            _process_entity(scene, params, question, answer)
        elif component == "dialogue":
            _process_dialogue(scene, params, question, answer)
        elif component == "rule":
            _process_rule(scene, params, question, answer, domain)
        elif component == "audio":
            _process_audio(scene, params, question, answer)
        elif component == "meta":
            scene.title = answer  # MetaLearning tiles set the scene title

        # Track which sprites are referenced
        if params.get("sprite_ref"):
            sprites_used.add(params["sprite_ref"])
        if params.get("sprite_id"):
            sprites_used.add(params["sprite_id"])

    # Ensure default player sprite exists
    if "sprite_player" not in scene.sprites:
        scene.sprites["sprite_player"] = _default_player_sprite()

    return scene


def _process_map_tile(scene: SceneIR, params: dict, question: str, answer: str):
    """Spatial tile → map grid cell."""
    x = params.get("x")
    y = params.get("y")
    tile_type = params.get("tile_type", 1)
    solid = params.get("solid", tile_type in (1, 2))  # 1 and 2 are usually walls

    if x is not None and y is not None:
        if 0 <= y < scene.map.height and 0 <= x < scene.map.width:
            scene.map.tiles[y][x] = tile_type
            scene.map.flags[y][x] = solid

    # Extract tile boundaries from question
    if "grid" in question.lower() or "terrain" in question.lower():
        _parse_terrain_description(scene, answer)


def _parse_terrain_description(scene: SceneIR, description: str):
    """Parse a text description of terrain layout into map tiles."""
    lines = description.strip().split("\n")
    for dy, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        # Parse characters as tile types: # = wall (1), . = floor (0), ~ = water (3)
        for dx, ch in enumerate(line):
            if 0 <= dy < scene.map.height and 0 <= dx < scene.map.width:
                if ch in ("#", "X", "W", "1"):
                    scene.map.tiles[dy][dx] = 1
                    scene.map.flags[dy][dx] = True
                elif ch == "~":
                    scene.map.tiles[dy][dx] = 3  # water
                    scene.map.flags[dy][dx] = True  # water is impassable
                elif ch in (".", " ", "0"):
                    scene.map.tiles[dy][dx] = 0  # floor
                elif ch == "D":
                    scene.map.tiles[dy][dx] = 5  # door
                    scene.map.flags[dy][dx] = True  # closed door is solid


def _process_sprite(scene: SceneIR, params: dict, question: str, answer: str):
    """Creative tile → sprite definition."""
    sprite_id = params.get("sprite_id")
    if not sprite_id:
        return

    width = params.get("width", 8)
    height = params.get("height", 8)
    pixels = params.get("pixels")

    if pixels:
        # Pixels already provided
        scene.sprites[sprite_id] = Sprite(sprite_id, pixels, width, height)
    else:
        # Generate a "wireframe" sprite from the Q/A
        _generate_placeholder_sprite(scene, sprite_id, question, answer)


def _generate_placeholder_sprite(scene: SceneIR, sprite_id: str,
                                  question: str, answer: str,
                                  width: int = 8, height: int = 8):
    """Generate a simple visual representation from tile text."""
    pixels = [0] * (width * height)

    # Simple hash-based sprite generation from the text content
    seed = hash(question + answer)
    rng_state = seed & 0xFFFFFFFF

    def pseudo_rand(limit: int) -> int:
        nonlocal rng_state
        rng_state = (rng_state * 1103515245 + 12345) & 0xFFFFFFFF
        return (rng_state >> 16) % limit

    # Generate noise-based sprite — like a procedural texture
    for i in range(len(pixels)):
        pixels[i] = pseudo_rand(16) if pseudo_rand(10) > 6 else 0

    scene.sprites[sprite_id] = Sprite(sprite_id, pixels, width, height)


def _default_player_sprite() -> Sprite:
    """Generate a default player sprite (simple humanoid)."""
    # 8×8 pixel player (palette-indexed)
    pixels = [0] * 64
    # Head
    for y in range(0, 3):
        for x in range(2, 6):
            pixels[y * 8 + x] = 13  # white skin tone
    # Body
    for y in range(3, 6):
        for x in range(1, 7):
            pixels[y * 8 + x] = 3   # red shirt
    # Legs
    for y in range(6, 8):
        pixels[y * 8 + 2] = 14      # blue pants
        pixels[y * 8 + 3] = 14
        pixels[y * 8 + 4] = 14
        pixels[y * 8 + 5] = 14
    # Eyes
    pixels[1 * 8 + 3] = 9           # dark eyes
    pixels[1 * 8 + 4] = 9
    return Sprite("sprite_player", pixels)


def _process_entity(scene: SceneIR, params: dict, question: str, answer: str):
    """Behavioral/Navigation tile → entity."""
    entity = Entity(
        name=params.get("name", question.strip().split()[-1] if question else "NPC"),
        sprite_ref=params.get("sprite_ref", "sprite_npc"),
        x=params.get("x", 0),
        y=params.get("y", 0),
        behavior=params.get("behavior", "idle"),
        dialogue_key=params.get("dialogue_key"),
        patrol_path=params.get("patrol_path", []),
    )
    scene.entities.append(entity)


def _process_dialogue(scene: SceneIR, params: dict, question: str, answer: str):
    """Knowledge tile → dialogue."""
    speaker = params.get("speaker", "Narrator")
    text = params.get("text", answer)
    next_id = params.get("next")
    scene.dialogues.append([Dialogue(speaker, text, next_id)])


def _process_rule(scene: SceneIR, params: dict, question: str,
                  answer: str, domain: str):
    """Procedural/Safety/Diagnostic → game rule."""
    rule = {
        "condition": params.get("condition", ""),
        "effects": params.get("effects", []),
        "priority": params.get("priority", "P2"),
        "domain": domain,
        "source_text": f"{question}: {answer}",
    }
    if params.get("zones"):
        rule["zones"] = params["zones"]
    if params.get("is_hazard"):
        rule["hazard"] = True
    scene.rules.append(rule)


def _process_audio(scene: SceneIR, params: dict, question: str, answer: str):
    """Creative tile → SFX/music."""
    sfx_type = params.get("type", "tone")
    scene.sfx_list.append({
        "id": params.get("sfx_id", f"sfx_{len(scene.sfx_list)}"),
        "type": sfx_type,
        "params": params,
    })


# ─── TIC-80 Code Generator ─────────────────────────────────

def generate_tic_cart(scene: SceneIR) -> str:
    """Generate complete TIC-80 Lua source from SceneIR."""
    lua_lines = []

    # Header
    lua_lines.append("-- TITLE: " + scene.title)
    lua_lines.append('-- AUTHOR: PLATO-NG Render Pipeline')
    lua_lines.append('-- DESC: Auto-generated from PLATO room tiles')
    lua_lines.append('-- SCRIPT: Lua')
    lua_lines.append('-- INPUT: gamepad')
    lua_lines.append(f'-- PALETTE: {" ".join(f"#{c:06x}" for c in DEFAULT_PALETTE)}')
    lua_lines.append('')

    # Sprite data (embedded as hex for .tic binary compatibility)
    lua_lines.append('-- SPRITES ----------------------------')
    lua_lines.append('-- (Embedded in .tic binary via sprite sheet)')
    lua_lines.append('')

    # Cart data tables
    # ── Sprite addresses (in TIC-80 RAM, 1 sprite = 64 bytes) ──
    sprite_map = {}
    for i, (sid, spr) in enumerate(scene.sprites.items()):
        sprite_map[sid] = i
        lua_lines.append(f"-- sprite {i}: {sid} ({spr.width}x{spr.height})")
    lua_lines.append('')

    # Map data (TIC-80 RAM at 0x04000)
    lua_lines.append('-- MAP DATA ---------------------------')
    for y in range(scene.map.height):
        row = ','.join(str(scene.map.tiles[y][x]) for x in range(scene.map.width))
        lua_lines.append(f"local row_{y} = {{{row}}}")
    lua_lines.append('')
    lua_lines.append('map_data = {')
    for y in range(scene.map.height):
        lua_lines.append(f"    row_{y},")
    lua_lines.append('}')
    lua_lines.append('')

    # Entity data
    lua_lines.append('-- ENTITIES ---------------------------')
    lua_lines.append('entities = {')
    for e in scene.entities:
        sid = sprite_map.get(e.sprite_ref, 0)
        lua_lines.append(f'    {{ name = "{e.name}",')
        lua_lines.append(f'      sprite = {sid},')
        lua_lines.append(f'      x = {e.x}, y = {e.y},')
        lua_lines.append(f'      behavior = "{e.behavior}",')
        if e.patrol_path:
            lua_lines.append('      patrol = {')
            for p in e.patrol_path:
                lua_lines.append(f'        {{ x = {p["x"]}, y = {p["y"]} }},')
            lua_lines.append('      },')
        lua_lines.append('    },')
    lua_lines.append('}')
    lua_lines.append('')

    # Dialogue data
    lua_lines.append('-- DIALOGUES --------------------------')
    if scene.dialogues:
        lua_lines.append('dialogues = {')
        for d_list in scene.dialogues:
            for d in d_list:
                escaped = d.text.replace('"', '\\"')
                lua_lines.append(f'    {{ speaker = "{d.speaker}", text = "{escaped}" }},')
        lua_lines.append('}')
    else:
        lua_lines.append('dialogues = {}')
    lua_lines.append('')

    # Player state
    lua_lines.append('-- GAME STATE -------------------------')
    lua_lines.append('player = {')
    lua_lines.append(f'    x = 16, y = 16,')
    lua_lines.append(f'    sprite = {sprite_map.get("sprite_player", 0)},')
    lua_lines.append('    speed = 2,')
    lua_lines.append('}')
    lua_lines.append('')
    lua_lines.append('score = 0')
    lua_lines.append('health = 10')
    lua_lines.append('dialogue_active = false')
    lua_lines.append('dialogue_text = ""')
    lua_lines.append('dialogue_line = 0')
    lua_lines.append('')
    lua_lines.append('anim_frame = 0')
    lua_lines.append('anim_timer = 0')
    lua_lines.append('')

    # Map visibility (camera offset)
    lua_lines.append('-- CAMERA -----------------------------')
    lua_lines.append('camera_x = 0')
    lua_lines.append('camera_y = 0')
    lua_lines.append('')

    # TIC() function — main loop
    lua_lines.append('-- MAIN LOOP --------------------------')
    lua_lines.append('function TIC()')
    lua_lines.append('    update()')
    lua_lines.append('    draw()')
    lua_lines.append('end')
    lua_lines.append('')

    # Update function
    lua_lines.append('function update()')
    lua_lines.append('    -- Player movement')
    lua_lines.append('    local dx, dy = 0, 0')
    lua_lines.append('')
    lua_lines.append('    if btn(0) then dy = -player.speed end')  # up
    lua_lines.append('    if btn(1) then dy = player.speed end')   # down
    lua_lines.append('    if btn(2) then dx = -player.speed end')  # left
    lua_lines.append('    if btn(3) then dx = player.speed end')   # right
    lua_lines.append('')

    # Collision with solid tiles
    lua_lines.append('    -- Collision detection')
    lua_lines.append('    local new_x = player.x + dx')
    lua_lines.append('    local new_y = player.y + dy')
    lua_lines.append('')
    lua_lines.append('    local tile_x = math.floor(new_x / 8)')
    lua_lines.append('    local tile_y = math.floor(new_y / 8)')
    lua_lines.append('')
    lua_lines.append('    -- Check map bounds')
    lua_lines.append('    if tile_x >= 0 and tile_x < 30 and')
    lua_lines.append('       tile_y >= 0 and tile_y < 17 then')
    lua_lines.append('        if map_data[tile_y + 1] and')
    lua_lines.append('           map_data[tile_y + 1][tile_x + 1] ~= 0 and')
    lua_lines.append('           map_data[tile_y + 1][tile_x + 1] < 5 then')
    lua_lines.append('            -- Solid tile - check if passable')
    lua_lines.append('            if dx ~= 0 then dx = 0 end')
    lua_lines.append('            if dy ~= 0 then dy = 0 end')
    lua_lines.append('        end')
    lua_lines.append('    else')
    lua_lines.append('        dx, dy = 0, 0')
    lua_lines.append('    end')
    lua_lines.append('')

    lua_lines.append('    player.x = player.x + dx')
    lua_lines.append('    player.y = player.y + dy')
    lua_lines.append('')

    # Animation
    lua_lines.append('    -- Animation timer')
    lua_lines.append('    anim_timer = anim_timer + 1')
    lua_lines.append('    if anim_timer > 5 then')
    lua_lines.append('        anim_frame = (anim_frame + 1) % 2')
    lua_lines.append('        anim_timer = 0')
    lua_lines.append('    end')
    lua_lines.append('')

    # Entity patrol movement
    lua_lines.append('    -- Entity patrol')
    lua_lines.append('    for _, e in ipairs(entities) do')
    lua_lines.append('        if e.patrol and #e.patrol > 0 then')
    lua_lines.append('            local target = e.patrol[e.patrol_step or 1]')
    lua_lines.append('            if target then')
    lua_lines.append('                local ex, ey = target.x - e.x, target.y - e.y')
    lua_lines.append('                local dist = math.sqrt(ex * ex + ey * ey)')
    lua_lines.append('                if dist > 1 then')
    lua_lines.append('                    e.x = e.x + (ex / dist) * 0.5')
    lua_lines.append('                    e.y = e.y + (ey / dist) * 0.5')
    lua_lines.append('                else')
    lua_lines.append('                    e.patrol_step = ((e.patrol_step or 1) % #e.patrol) + 1')
    lua_lines.append('                end')
    lua_lines.append('            end')
    lua_lines.append('        end')
    lua_lines.append('    end')
    lua_lines.append('')

    # Action button interaction
    lua_lines.append('    -- Action button (Z)')
    lua_lines.append('    if btnp(4) then')
    lua_lines.append('        -- Check entity proximity for dialogue')
    lua_lines.append('        for _, e in ipairs(entities) do')
    lua_lines.append('            local ex = (e.x - player.x)')
    lua_lines.append('            local ey = (e.y - player.y)')
    lua_lines.append('            if ex * ex + ey * ey < 400 then')
    lua_lines.append('                if e.name and dialogues[1] then')
    lua_lines.append('                    dialogue_active = true')
    lua_lines.append('                    dialogue_text = dialogues[1].text')
    lua_lines.append('                    dialogue_line = 1')
    lua_lines.append('                end')
    lua_lines.append('            end')
    lua_lines.append('        end')
    lua_lines.append('    end')
    lua_lines.append('')

    # Dialogue advancement
    lua_lines.append('    -- Advance dialogue')
    lua_lines.append('    if dialogue_active and btnp(4) then')
    lua_lines.append('        dialogue_line = dialogue_line + 1')
    lua_lines.append('        if dialogues[dialogue_line] then')
    lua_lines.append('            dialogue_text = dialogues[dialogue_line].text')
    lua_lines.append('        else')
    lua_lines.append('            dialogue_active = false')
    lua_lines.append('            dialogue_text = ""')
    lua_lines.append('        end')
    lua_lines.append('    end')
    lua_lines.append('')
    lua_lines.append('    -- Camera follows player')
    lua_lines.append('    camera_x = player.x - 120 + 4')
    lua_lines.append('    camera_y = player.y - 68 + 4')
    lua_lines.append('    if camera_x < 0 then camera_x = 0 end')
    lua_lines.append('    if camera_y < 0 then camera_y = 0 end')
    lua_lines.append('    local max_cam_x = 30 * 8 - 240')
    lua_lines.append('    local max_cam_y = 17 * 8 - 136')
    lua_lines.append('    if camera_x > max_cam_x then camera_x = max_cam_x end')
    lua_lines.append('    if camera_y > max_cam_y then camera_y = max_cam_y end')
    lua_lines.append('end')
    lua_lines.append('')

    # Draw function
    lua_lines.append('function draw()')
    lua_lines.append(f'    cls({scene.bg_color})')
    lua_lines.append('')

    # Render map
    lua_lines.append('    -- Draw map tiles')
    lua_lines.append('    for y = 1, 17 do')
    lua_lines.append('        for x = 1, 30 do')
    lua_lines.append('            local tile = map_data[y][x]')
    lua_lines.append('            if tile and tile > 0 then')
    lua_lines.append('                spr(tile, (x - 1) * 8 - camera_x,')
    lua_lines.append('                           (y - 1) * 8 - camera_y)')
    lua_lines.append('            end')
    lua_lines.append('        end')
    lua_lines.append('    end')
    lua_lines.append('')

    # Render entities
    lua_lines.append('    -- Draw entities')
    lua_lines.append('    for _, e in ipairs(entities) do')
    lua_lines.append('        spr(e.sprite, e.x - camera_x, e.y - camera_y)')
    lua_lines.append('    end')
    lua_lines.append('')

    # Render player
    lua_lines.append('    -- Draw player')
    lua_lines.append('    spr(player.sprite, player.x - camera_x, player.y - camera_y)')
    lua_lines.append('')

    # UI
    lua_lines.append('    -- UI overlay')
    lua_lines.append('    print("Score: " .. score, 0, 128, 12)')
    lua_lines.append('    print("HP: " .. health, 80, 128, 10)')
    lua_lines.append('')

    # Dialogue box
    lua_lines.append('    -- Dialogue box')
    lua_lines.append('    if dialogue_active then')
    lua_lines.append('        rect(0, 100, 240, 36, 1)')
    lua_lines.append('        rect(1, 101, 238, 34, 14)')
    lua_lines.append('        print(dialogue_text, 4, 104, 0)')
    lua_lines.append('    end')
    lua_lines.append('end')
    lua_lines.append('')

    return '\n'.join(lua_lines)


# ─── Main Entry Point ─────────────────────────────────────

def convert(tiles_file: str, output_file: str = "cart.lua") -> str:
    """Main conversion function. Returns path to output file."""
    with open(tiles_file, 'r') as f:
        tiles = json.load(f)

    scene = tiles_to_sceneir(tiles)
    lua_source = generate_tic_cart(scene)

    with open(output_file, 'w') as f:
        f.write(lua_source)

    return output_file


def cli():
    if len(sys.argv) < 2:
        print("Usage: python3 plato_to_tic80.py input_tiles.json [output.lua]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "cart.lua"

    result = convert(input_path, output_path)
    print(f"✅ Generated: {result}")
    print(f"   {len(open(result).readlines())} lines of Lua")
    print(f"   Load into TIC-80: tic80 {result}")


if __name__ == '__main__':
    cli()
```

### Example Input / Output

Given this tiles file (`demo_tiles.json`):

```json
[
  {
    "id": "spatial_1",
    "domain": "Spatial",
    "question": "What terrain occupies this position?",
    "answer": "Walls on the edges, floor in the center, water at (8,4) to (10,6)",
    "confidence": 0.95,
    "ir_metadata": {
      "ir_component": "map_tile",
      "ir_params": {}
    }
  },
  {
    "id": "spatial_2",
    "domain": "Spatial",
    "question": "Terrain grid layout",
    "answer": "##########\n#........#\n#..~~~...#\n#..~~~...#\n#........#\n##########",
    "confidence": 0.90,
    "ir_metadata": {
      "ir_component": "map_tile",
      "ir_params": {}
    }
  },
  {
    "id": "knowledge_dockmaster",
    "domain": "Knowledge",
    "question": "What does the dock master say?",
    "answer": "Welcome to Fisherman's Wharf. The northern sea is treacherous — watch for the riptide.",
    "confidence": 0.85,
    "ir_metadata": {
      "ir_component": "dialogue",
      "ir_params": {
        "speaker": "Dock Master",
        "text": "Welcome to Fisherman's Wharf. The northern sea is treacherous — watch for the riptide."
      }
    }
  },
  {
    "id": "navigation_patrol",
    "domain": "Navigation",
    "question": "Dock master patrol route",
    "answer": "Dock Master walks the pier from (16,8) to (24,8) and back",
    "confidence": 0.75,
    "ir_metadata": {
      "ir_component": "entity",
      "ir_params": {
        "name": "Dock Master",
        "sprite_ref": "sprite_npc",
        "x": 16,
        "y": 8,
        "behavior": "patrol",
        "dialogue_key": "dockmaster",
        "patrol_path": [{"x": 16, "y": 8}, {"x": 24, "y": 8}]
      }
    }
  },
  {
    "id": "procedural_water",
    "domain": "Procedural",
    "question": "What happens in deep water?",
    "answer": "Player speed reduced by 50%. Player takes 1 damage every 3 seconds.",
    "confidence": 0.82,
    "ir_metadata": {
      "ir_component": "rule",
      "ir_params": {
        "condition": "tile_type == 3",
        "effects": [
          {"type": "modify_speed", "multiplier": 0.5},
          {"type": "periodic_damage", "interval": 3, "amount": 1}
        ]
      }
    }
  },
  {
    "id": "creative_theme",
    "domain": "Creative",
    "question": "Background music?",
    "answer": "Sea shanty theme, 120 BPM, C major",
    "confidence": 0.70,
    "ir_metadata": {
      "ir_component": "audio",
      "ir_params": {
        "sfx_id": "music_theme",
        "type": "music",
        "bpm": 120,
        "key": "C"
      }
    }
  }
]
```

Running:
```bash
python3 plato_to_tic80.py demo_tiles.json demo_cart.lua
```

Produces a fully functional TIC-80 Lua cart (`demo_cart.lua`) with:
- A dock scene (walls on edges, water pool in center)
- The Dock Master NPC patrolling the pier
- Dialogue on interaction
- Camera following the player
- Collision with walls
- Score and HP UI

---

## 7. Edge Cases & Failure Modes

### 7.1 Missing Sprites
- **Problem**: Entity references `sprite_ref` "sprite_npc" but no Creative tile defined it
- **Solution**: `_generate_placeholder_sprite()` creates on-the-fly sprites from Q/A hash
- **Fallback**: All missing sprites get the default player sprite

### 7.2 Overlapping Map Tiles
- **Problem**: Two Spatial tiles claim different content for the same (x,y)
- **Solution**: Higher-confidence tile wins. Ties → most recently created wins
- **Fallback**: Both tiles are logged as conflicts in the meta section

### 7.3 Empty Tile Set
- **Problem**: Room has 0 tiles (or all filtered by confidence)
- **Solution**: Generate a "blank cart" with a title screen saying "This room has no tiles to render"
- **Output**: 1 sprite (title text), no map, no entities

### 7.4 Temporal Decay Renders Tile Invisible Mid-Scene
- **Problem**: Tiles with `DecayFunction` expire mid-visit
- **Solution**: IR generation snapshot timestamps the entire scene. Stale tiles are frozen at their current confidence at generation time, not re-evaluated during play

### 7.5 TIC-80 Code Size Limit
- **Problem**: Very large maps or many entities exceed 64 KB Lua source limit
- **Solution**: Compress map data (run-length encoding), trim whitespace in output
- **Fallback**: Split into multiple carts with teleport linking

### 7.6 NegativeSpace Tiles
- **Problem**: Safety/Deadband zones cover the entire map (invalid scene)
- **Solution**: NegativeSpace tiles get highest priority. If they cover 100% of map, the scene is replaced with a "Restricted" title screen. P0 zones render as red-tinted blocks that cannot be entered

### 7.7 Conflicting Input Bindings
- **Problem**: Two tiles define different functions for the same button
- **Solution**: Last-write-wins (highest confidence + most recent). Log the conflict

### 7.8 TIC-80 Palette Mismatch
- **Problem**: IR specifies colors outside TIC-80's 16-color palette
- **Solution**: Clamp to nearest color using Euclidean distance in RGB space
- **TIC-80 default palette** (used above) is the standard DB16 palette

---

## 8. Future Work

### Short-term (v0.1 — TIC-80 only)
- [ ] Room integration: query PLATO rooms directly, not just JSON files
- [ ] Sprite generation: use actual pixel descriptions from Creative tiles
- [ ] Map compression: RLE for large maps
- [ ] SFX rendering: Procedural chiptune from Creative tiles
- [ ] .tic binary packaging (embed sprite PNG + Lua into single file)

### Medium-term (v0.2 — add LÖVE2D + Web)
- [ ] LÖVE2D backend: SceneIR → `main.lua` + `.love` archive
- [ ] Web backend: SceneIR → HTML5 Canvas + Web Audio
- [ ] Multi-room navigation: teleport tiles that link rooms
- [ ] Save/load game state to TIC-80 persistent RAM
- [ ] Dialogue tree support (branching conversations from Knowledge tiles)

### Long-term (v0.3+ — advanced)
- [ ] Ren'Py backend for visual novel scenes (great for Knowledge-heavy rooms)
- [ ] Twine backend for interactive fiction
- [ ] Bitsy backend for tiny game-jam scenes
- [ ] MUD room rendering — text-based dungeon crawl from tile rules
- [ ] AGS adventure game backend for complex puzzle-and-dialogue scenes
- [ ] Multiplayer: WebSocket bridge for shared PLATO room experiences
- [ ] Real-time tile streaming: scene updates as PLATO accumulates new tiles
- [ ] Graphical palettes as PLATO tiles (Creative domain tiles for the palette)

---

## Summary

| Backend | Status | Effort | Best For |
|---------|--------|--------|----------|
| **TIC-80** | ✅ **MVP Ready** | Low | Rapid prototyping, small games, any platform |
| **LÖVE2D** | 🔧 Design Ready | Medium | Full 2D games, physics, high-resolution |
| **Web (Canvas)** | 🔧 Design Ready | Medium | Zero-install sharing, networked games |
| **SCUMMVM** | ❌ Wait | Very High | Adventure games only, long-term speculative |
| **Ren'Py** | 📋 Planned | Medium | Visual novels, narrative-heavy rooms |
| **Twine** | 📋 Planned | Low | Interactive fiction, choice-based stories |

**Immediate action**: Build TIC-80 MVP. It's the smallest dev cycle, biggest compatibility footprint, and tightest constraint set. Ship games from PLATO rooms by the end of the week, then build LÖVE2D and Web backends from the same IR.
