# TRACK 3: SCUMMVM / TIC-80 Render Adapter

**Research goal:** Can we render PLATO app-ui/ tiles as SCUMMVM rooms or TIC-80 carts?
**Status:** Research complete — viable path identified for both targets. TIC-80 is the pragmatic first target.

---

## 1. SCUMMVM — Target Analysis

### What SCUMMVM Renders

SCUMMVM is NOT a game engine you write for — it's a **re-implementation** of classic adventure game engines (SCUMM, AGI, SCI, etc.). It interprets compiled bytecode from original game data files.

The most relevant target format is **SCUMM** (LucasArts' Script Creation Utility for Maniac Mansion).

### SCUMM Game Structure

```
game.1  (main data file — container for all resources)
└── LF / LFLF blocks (resource containers)
    ├── RNAM — room names
    ├── DROO — directory of room offsets
    ├── ROOM blocks (one per room)
    │   ├── Background image (8bpp bitmap)
    │   ├── Object table (interactive items)
    │   ├── Box/walkbox data (walkable areas)
    │   ├── EN / ENCD — Room entry script
    │   ├── EX / EXCD — Room exit script
    │   ├── LSCR — Local scripts
    │   └── OC / OBCD — Object code (verb handlers)
    └── SCRP — Global scripts
```

### Script Types

| Type | Block ID | When it runs |
|------|----------|--------------|
| Global script | `SCRP` | Whole game, shared |
| Local script | `LSCR` | Room-specific |
| Room Entry | `EN` / `ENCD` | Player enters room |
| Room Exit | `EX` / `EXCD` | Player leaves room |
| Object script | `OC` / `OBCD` | Player interacts with object |
| Verb table | (embedded in OC) | Maps verbs → script offsets |

### Simplest SCUMM Game

Minimum viable game:
- **1 room** with background
- **1 actor** (controllable character)
- **1 object** (interactive element)
- **1 object script** that prints dialog on "Talk To"
- **1 room entry script** that places the actor
- **Walkbox** defining where actor can move

SCUMM scripts are **compiled bytecode** — not human-writable directly. Tools:
- **[ScummC](https://github.com/ScummVM/scummc)** — C-like SCUMM compiler (compile → bytecode)
- **scumm-8** — Alternative assembler (lower-level)

SCUMM script is high-level, event-driven, concurrent. A "Hello World" interaction:

```
// Conceptual SCUMM script
room "Beach" {
  actor "Guybrush" at (100, 100)
  object "Hermit" at (200, 100)

  script talk_to_hermit {
    if (verb == VERB_TALK) {
      walk_actor("Guybrush", "Hermit")
      say_line("Hermit", "Hello, world!")
    }
  }
}
```

### SCUMMVM Adapter Feasibility

**RATING: High complexity, low pragmatism**

- ❌ SCUMM bytecode format is complex, versioned (V1-V8), and tightly coupled to specific game engines
- ❌ No standalone "build SCUMM games" toolchain — ScummC exists but is fragile
- ❌ SCUMMVM doesn't have a straightforward "load custom game from directory" flow
- ✅ If we target the ScummC compile chain, we could generate C-like source, then compile to bytecode
- ✅ PLATO app-ui/ tiles map well conceptually (background→room bg, sprites→actors, zones→objects)

**Recommendation:** Document the mapping for future, but DO NOT build a SCUMMVM adapter first. Build TIC-80 and LÖVE2D first. If the LÖVE2D adapter proves the architecture, add ScummC source generation as a third target.

---

## 2. TIC-80 — Target Analysis

### What TIC-80 Renders

TIC-80 is a **fantasy console** — self-contained dev environment + runtime. Cartridges are **source code** (primarily Lua) with embedded sprite/map/sound data.

### TIC-80 Specs

| Property | Value |
|----------|-------|
| Resolution | 240×136 pixels |
| Colors | 16 (from 24-bit palette) |
| Sprites | 256 foreground (8×8) + 256 background tiles |
| Map | 240×136 tiles (1920×1088 px) |
| Sound | 4 channels, 64 SFX, 8 music tracks |
| Code | 512KB source / 256KB compiled WASM |
| RAM | 272KB total (32KB VRAM) |
| Languages | Lua (primary), JS, MoonScript, Wren, Fennel, Python, Ruby, more |
| Input | 4 gamepads + mouse + keyboard |
| FPS | 60 |

### Simplest TIC-80 Cartridge

A cart is just plain text with metadata comments:

```lua
-- title: Hello PLATO
-- author: PLATO-NG
-- desc: Rendered from app-ui tiles
-- script: lua
-- input: gamepad

function TIC()
    cls()                                  -- Clear screen
    print("Hello from PLATO!", 60, 60, 12) -- [color=12] white
end
```

Save as `.lua` → `load` in TIC-80 → `save hello.tic` → runs.

### Full Minimal Walkaround

```lua
-- title: PLATO Demo
-- author: PLATO-NG
-- desc: A tiny walkaround
-- script: lua

-- Player position
local px = 120
local py = 68
local speed = 2

function TIC()
    -- Handle input
    if btn(0) then py = py - speed end  -- up
    if btn(1) then py = py + speed end  -- down
    if btn(2) then px = px - speed end  -- left
    if btn(3) then px = px + speed end  -- right

    -- Draw
    cls()
    -- [spr(id, x, y, ...)] Draw player sprite (id=1, white square)
    spr(1, px, py, 0, 1, 0, 0, 2, 2)
    -- [print(str, x, y, color)] Title text
    print("Press arrows to move", 40, 10, 6)
end
```

This runs immediately in TIC-80. No build step. No compilation. The source IS the cartridge.

### TIC-80 Cartridge Binary Format

When exported as `.tic`, the binary layout is:

| Offset | Size | Content |
|--------|------|---------|
| 0x00   | 4    | Magic: `TIC` |
| 0x04   | 4    | Version |
| 0x08   | 4    | Code size |
| 0x0C   | 4    | Unused |
| 0x10   | 4    | Cover data size |
| 0x14   | ...  | Cover PNG image data |
| ...    | ...  | Source code (null-terminated) |
| ...    | 256×256×2 | Sprite sheet (foreground) |
| ...    | 256×256×2 | Sprite sheet (background/tiles) |
| ...    | 240×136×2 | Map data |
| ...    | 64 * ... | SFX data |
| ...    | 8 * ...  | Music pattern data |
| ...    | 16       | Palette (4-byte RGBA per entry) |
| ...    | various  | Waveform data |

**Key insight:** We don't need to generate raw `.tic` binaries. We can generate **Lua source files** that:
1. Define sprites via `poke()` to VRAM
2. Set map data via `mset()`
3. Run the game loop in `TIC()`
4. Then load into TIC-80 and export

Or even simpler: write a **TIC-80 compatible `.lua` file** that contains all data inline as Lua tables.

### TIC-80 Adapter Feasibility

**RATING: Low complexity, high pragmatism**

- ✅ Cartridges are **source code** — we generate Lua that TIC-80 interprets directly
- ✅ `TIC()` callback provides the main loop — maps directly to PLATO app-logic
- ✅ `spr()`, `map()`, `cls()`, `print()` are simple, stable APIs
- ✅ TIC-80 has a CLI mode: `tic80 --cmd 'load cart.lua; run'`
- ✅ TIC-80 runs on Linux, ARM, Raspberry Pi — compatible with Oracle Cloud servers
- ✅ We can serve `.tic` or `.lua` files from a PLATO room via HTTP
- ⚠️ 16-color palette limit — but fine for retro-style games
- ⚠️ 240×136 resolution — fine for simple games, tile-based UIs

---

## 3. PLATO app-ui/ Tile Schema → Target Mapping

### Proposed app-ui Tile Schema

We define a standard schema for PLATO app-ui tiles:

```json5
// app-ui/manifest tile
{
  "type": "app-ui/manifest",
  "version": "1.0",
  "render_targets": ["tic80", "scummvm", "love2d"],
  "title": "My Adventure",
  "author": "PLATO",
  "description": "A game generated from PLATO tiles"
}
```

```json5
// app-ui/tile: background
{
  "type": "app-ui/background",
  "tile_id": "bg-beach",
  "width": 30,        // tiles wide (240px / 8px)
  "height": 17,       // tiles high (136px / 8px)
  "palette": [        // 16-color palette in hex
    "#000000", "#1D2B53", "#7E2553", "#008751",
    "#AB5236", "#5F574F", "#C2C3C7", "#FFF1E8",
    "#FF004D", "#FFA300", "#FFEC27", "#00E436",
    "#29ADFF", "#83769C", "#FF77A8", "#FFCCAA"
  ],
  "tiles": [          // 2D array, each is palette index
    [0, 0, 0, 0, 0, 0, ...],
    [0, 1, 1, 1, 1, 0, ...],
    ...
  ]
}
```

```json5
// app-ui/tile: sprites
{
  "type": "app-ui/sprites",
  "tile_id": "sprites-characters",
  "sprites": [
    {
      "id": 1,
      "name": "player",
      "width": 2,     // in tiles (16px)
      "height": 2,    // in tiles (16px)
      "frames": [
        [  // frame 0: idle
          [0,1,1,0],
          [1,3,3,1],
          [1,1,1,1],
          [0,1,1,0]
        ],
        [  // frame 1: walk
          [0,1,1,0],
          [1,3,3,1],
          [1,0,0,1],
          [0,1,1,0]
        ]
      ]
    },
    {
      "id": 2,
      "name": "npc",
      "width": 2,
      "height": 2,
      "frames": [
        [
          [0,2,2,0],
          [2,4,4,2],
          [2,2,2,2],
          [0,2,2,0]
        ]
      ]
    }
  ]
}
```

```json5
// app-ui/tile: zones (interactive areas)
{
  "type": "app-ui/zones",
  "tile_id": "zones-interactions",
  "zones": [
    {
      "id": "npc-zone",
      "x": 100, "y": 68,
      "width": 16, "height": 16,
      "trigger": "proximity",  // or "click", "overlap"
      "radius": 20,
      "action": "start_dialog",
      "params": { "npc_id": "old_man", "dialog": "Hello from PLATO!" }
    },
    {
      "id": "exit-zone",
      "x": 220, "y": 0,
      "width": 20, "height": 136,
      "trigger": "overlap",
      "action": "change_room",
      "params": { "room": "beach-2", "enter_x": 10, "enter_y": 68 }
    },
    {
      "id": "item-zone",
      "x": 40, "y": 80,
      "width": 12, "height": 12,
      "trigger": "click",
      "action": "collect_item",
      "params": { "item_id": "coin", "message": "Found a coin!" }
    }
  ]
}
```

```json5
// app-ui/tile: scripts (game logic)
{
  "type": "app-ui/scripts",
  "tile_id": "scripts-logic",
  "scripts": [
    {
      "name": "player_movement",
      "language": "lua",
      "trigger": "frame",      // runs every frame
      "code": [
        "-- Player movement from app-ui/scripts",
        "local speed = 2",
        "if btn(0) then py = py - speed end",
        "if btn(1) then py = py + speed end",
        "if btn(2) then px = px - speed end",
        "if btn(3) then px = px + speed end"
      ]
    },
    {
      "name": "npc_dialog",
      "language": "lua",
      "trigger": "event",
      "event": "start_dialog",
      "code": [
        "function show_dialog(text)",
        "  local frame = 0",
        "  repeat",
        "    cls()",
        "    spr(1, px, py)",
        "    rect(10, 100, 220, 30, 0)",
        "    print(text, 20, 110, 15)",
        "    frame = frame + 1",
        "    if frame > 180 then break end",
        "  until btnp(4)",
        "end"
      ]
    },
    {
      "name": "room_exit",
      "language": "lua",
      "trigger": "event",
      "event": "change_room",
      "code": [
        "-- Room transition (stub for multi-room)",
        "px = params.enter_x",
        "py = params.enter_y",
        "print('Entering ' .. params.room, 60, 60, 12)",
        "sync()"
      ]
    }
  ]
}
```

```json5
// app-ui/tile: sound
{
  "type": "app-ui/sound",
  "tile_id": "sfx-footstep",
  "sfx": [
    {
      "id": 0,
      "name": "footstep",
      "type": "square",
      "frequency_start": 200,
      "frequency_end": 100,
      "duration": 5,
      "volume": 10,
      "speed": 30
    }
  ],
  "music": [
    {
      "id": 0,
      "name": "bgm",
      "tempo": 120,
      "patterns": [0, 0, 1, 1, 2, 2, 1, 1]
    }
  ]
}
```

---

## 4. Generation: PLATO Room → TIC-80 Cartridge

### Adapter Architecture

```
┌──────────────────────────────────────────┐
│          PLATO Adapter Room               │
│  (registers as renderer for app-ui/*)     │
│                                           │
│  1. Read all app-ui/ tiles from app room  │
│  2. Merge sprite atlas                    │
│  3. Compile zone map                      │
│  4. Assemble script tile code             │
│  5. Generate Lua source                   │
│  6. Write output tile: output/tic80.lua   │
│     And/or serve via HTTP                 │
└──────────────────────────────────────────┘
```

### Phase 1: Tile Reader

```python
# Pseudocode for the adapter room script
class TIC80Adapter:
    """Reads PLATO app-ui/ tiles and generates a TIC-80 Lua cartridge."""

    def read_tiles(self, room_id):
        self.manifest = plato.read(room_id, "app-ui/manifest")
        self.background = plato.read(room_id, "app-ui/background")
        self.sprites = plato.read(room_id, "app-ui/sprites")
        self.zones = plato.read(room_id, "app-ui/zones")
        self.scripts = plato.read(room_id, "app-ui/scripts")
        self.sound = plato.read(room_id, "app-ui/sound")
        return self

    def generate(self):
        chunks = [
            self._metadata(),
            self._sprite_data(),
            self._map_data(),
            self._sound_data(),
            self._main_code(),
            self._script_code(),
        ]
        lua_source = "\n\n".join(chunks)
        return lua_source

    def _metadata(self):
        m = self.manifest
        return f"""-- title: {m['title']}
-- author: {m['author']}
-- desc: {m.get('description', '')}
-- script: lua"""

    def _sprite_data(self):
        """Generate sprite sheet as VRAM poke calls."""
        lines = ["-- Sprite data from PLATO app-ui/sprites"]
        # Generate VRAM poke sequences for each sprite
        for sprite in self.sprites['sprites']:
            sid = sprite['id']
            for fi, frame in enumerate(sprite['frames']):
                for row_idx, row in enumerate(frame):
                    for col_idx, color_idx in enumerate(row):
                        # TIC-80 sprite VRAM: 0x00000 + (sid * 64) + ...
                        vram_addr = 0x00000 + (sid * 64) + (row_idx * 8) + col_idx
                        lines.append(f"  poke(0x{vram_addr:05X}, {color_idx})")
        return lines

    def _main_code(self):
        return """-- Main loop generated by PLATO-NG
local px = 120
local py = 68
local dialog_active = false
local dialog_text = ""

function TIC()
    cls()

    -- Draw background map
    map(0, 0, 30, 17, 0, 0)

    -- Draw player
    spr(1, px, py, 0, 1, 0, 0, 2, 2)

    -- Run frame scripts
    run_frame_scripts()

    -- Draw HUD
    print("PLATO-NG Demo", 2, 2, 6)
end

"""

    def _script_code(self):
        """Inject script tiles as Lua functions."""
        lines = []
        for script in self.scripts['scripts']:
            lines.append(f"\n-- Script: {script['name']} ({script['trigger']})")
            for line in script['code']:
                lines.append(f"  {line}")
        return "\n".join(lines)
```

### Phase 2: Concrete Example — PLATO Tiles → Runnable TIC-80 Cart

Here's what the **generated output** looks like for the tile schema above:

```lua
-- title: My Adventure
-- author: PLATO-NG
-- desc: A game generated from PLATO tiles
-- script: lua
-- input: gamepad

-- =============================================
-- Sprites (from app-ui/sprites)
-- Load into TIC-80 sprite sheet VRAM
-- =============================================
-- Sprite 1: player (16x16, 2 tiles x 2 tiles)
poke(0x00000 + 0*64 + 0*8 + 0, 0) poke(0x00000 + 0*64 + 0*8 + 1, 1)
poke(0x00000 + 0*64 + 0*8 + 2, 1) poke(0x00000 + 0*64 + 0*8 + 3, 0)

-- (simplified: full script would unroll all pixels)

-- =============================================
-- Map data (from app-ui/background)
-- Set via mset(x, y, tile_id)
-- =============================================
for y = 0, 16 do
    for x = 0, 29 do
        mset(x, y, bg_tiles[y+1][x+1])
    end
end

-- =============================================
-- Sound data (from app-ui/sound)
-- =============================================
-- SFX 0: footstep
-- (sfx API calls in game loop)

-- =============================================
-- Player state
-- =============================================
local px = 120
local py = 68

-- Items collected
local inventory = {}

-- Dialog state
local dialog = { active = false, text = "", timer = 0 }

-- =============================================
-- Script: player_movement (frame trigger)
-- =============================================
function run_player_movement()
    local speed = 2
    if btn(0) then py = py - speed end
    if btn(1) then py = py + speed end
    if btn(2) then px = px - speed end
    if btn(3) then px = px + speed end

    -- Keep player in bounds
    px = math.max(0, math.min(224, px))
    py = math.max(0, math.min(120, py))
end

-- =============================================
-- Script: zone_check (frame trigger)
-- Proximity detection for interactive zones
-- =============================================
function run_zone_check()
    -- Zone: npc-zone (100, 68, radius 20)
    local dx = px - 100
    local dy = py - 68
    if dx*dx + dy*dy < 20*20 and btnp(4) then
        show_dialog("Hello from PLATO!")
    end

    -- Zone: exit-zone (220, 0, width 20, height 136)
    if px > 220 and py > 0 and py < 136 then
        print("Leaving room...", 60, 60, 12)
        -- Room transition stub
    end

    -- Zone: item-zone (40, 80, radius 12)
    local ix, iy = 40, 80
    local idx = px - ix
    local idy = py - iy
    if idx*idx + idy*idy < 12*12 and btnp(4) then
        if not inventory["coin"] then
            inventory["coin"] = true
            show_dialog("Found a coin!")
        end
    end
end

-- =============================================
-- Script: dialog_system (event trigger)
-- =============================================
function show_dialog(text)
    dialog.active = true
    dialog.text = text
    dialog.timer = 180  -- ~3 seconds at 60fps
end

function run_dialog()
    if not dialog.active then return end

    -- Draw dialog box
    rect(10, 100, 220, 30, 0)
    rectb(10, 100, 220, 30, 12)
    print(dialog.text, 20, 110, 15)

    -- Auto-dismiss
    dialog.timer = dialog.timer - 1
    if dialog.timer <= 0 or btnp(4) then
        dialog.active = false
    end
end

-- =============================================
-- Main loop — called 60 times/second
-- =============================================
function TIC()
    cls()

    -- Draw background map
    map(0, 0, 30, 17, 0, 0)

    -- Run frame scripts
    run_player_movement()
    run_zone_check()

    -- Draw player
    spr(1, px, py, 0, 1, 0, 0, 2, 2)

    -- Draw dialog over everything
    run_dialog()

    -- HUD
    print("PLATO-NG Demo", 2, 2, 6)
    if inventory["coin"] then
        print("Coin collected!", 2, 12, 10)
    end
end
```

### Phase 3: Generation Pipeline — Full Adapter Script

```python
def plato_tiles_to_tic80(room_id):
    """Full pipeline: PLATO room → TIC-80 cartridge file."""

    # 1. Read tiles
    tiles = plato_ng.read_all_tiles(room_id, "app-ui/")

    # 2. Extract components
    bg = tiles.get("background", default_background())
    sprites = tiles.get("sprites", default_sprites())
    zones = tiles.get("zones", {})
    scripts = tiles.get("scripts", default_scripts())
    sound = tiles.get("sound", {})

    # 3. Generate Lua source
    source = TIC80Generator() \
        .set_metadata(tiles["manifest"]) \
        .set_sprites(sprites) \
        .set_map(bg) \
        .set_zones(zones) \
        .set_scripts(scripts) \
        .set_sound(sound) \
        .build()

    # 4. Write output tiles
    plato_ng.write(room_id, "output/tic80.lua", {
        "type": "text/lua",
        "content": source,
        "renderer": "tic80",
        "generated_at": timestamp()
    })

    # 5. Optionally compile to .tic binary
    # tic80 --cmd "load output.lua; save output.tic; exit"

    # 6. Serve via HTTP (optional)
    # plato_ng.serve(room_id, "output/tic80.lua", "text/plain")

    return source
```

---

## 5. Minimum Viable Adapter

### MVP Scope (Build First)

| Component | Status | Notes |
|-----------|--------|-------|
| Tile reader (standard schema) | To build | JSON schema for app-ui/ tiles |
| Lua source generator (raw text) | To build | Concatenate tile data → Lua |
| Zone→collision code gen | To build | Simple proximity/overlap → btnp() checks |
| Sprite→VRAM poke generation | To build | Flat sprite data → poke() calls |
| Script injection | To build | app-ui/scripts code → Lua functions |
| Map generation | To build | Background tile grid → mset() calls |
| Output tile write | To build | Write generated source to output/ |
| HTTP serve | To build | Serve .lua file for direct TIC-80 loading |
| .tic binary packaging | Optional | Requires tic80 CLI binary installed |

### What Adapter Does NOT Need (MVP)

- Full SCUMM bytecode generation (too complex)
- Multi-room state management (single room is fine)
- Sound/music generation (add in Phase 2)
- Animation system (add in Phase 2)
- Complex dialog trees (simple `print()` works)

### To Ship MVP

1. **Define JSON Schema** for app-ui/ tiles (manifest, background, sprites, zones, scripts, sound)
2. **Build `TIC80Generator`** — takes tile data, emits Lua string
3. **Build `PlatoTileReader`** → reads PLATO room tile chain, returns dict
4. **Wire into PLATO-NG adapter room** — room reads app-ui/ → writes output/
5. **Install TIC-80 on server** — `apt install tic80` or download binary
6. **Test loop:** Write tile → generate → load in TIC-80 → play

---

## 6. Comparison: SCUMMVM vs TIC-80

| Factor | SCUMMVM | TIC-80 |
|--------|---------|--------|
| Game format | Compiled bytecode (V1-V8) | Source code (Lua) |
| Toolchain | ScummC compiler needed | Plain text, no build step |
| Render target | Adventure games only | Any 2D game type |
| Constraints | Fixed engine behavior | Full Lua runtime |
| Resolution | 320×200 typical | 240×136 |
| Colors | 256 (VGA palette) | 16 (customizable) |
| Input | Point-and-click | Gamepad + keyboard |
| PLATO mapper workload | Full compiler → bytecode | String concatenation |
| MVP effort | Weeks | Days |

**Clear winner: TIC-80 as target 1, LÖVE2D as target 2, SCUMMVM as stretch target 3.**

---

## 7. Next Steps

1. **Define app-ui tile JSON schema** (shared across all render targets)
2. **Build `plato-ng-adapter` repo** with:
   - `schema/` — Tile JSON schemas
   - `generators/tic80.py` — TIC-80 Lua generator
   - `generators/love2d.py` — LÖVE2D Lua generator (Track 4)
   - `generators/scummc.py` — ScummC source generator (stretch)
   - `reader.py` — PLATO room tile reader
3. **Install TIC-80** on Oracle Cloud for testing
4. **MVP demo:** Write a simple room with 1 sprite + 1 zone + 1 dialog → generate → run in TIC-80

---

## Appendix A: TIC-80 API Reference (for code generation)

### Drawing
```lua
cls(color)           -- Clear screen with color (default 0)
spr(id, x, y, ...)   -- Draw sprite
map(x, y, w, h, sx, sy) -- Draw map region
print(text, x, y, color) -- Print text
rect(x, y, w, h, color) -- Filled rectangle
rectb(x, y, w, h, color) -- Rectangle border
circ(x, y, r, color) -- Filled circle
line(x0, y0, x1, y1, color) -- Line
pix(x, y, color)     -- Single pixel (get/set)
font(text, x, y, ...) -- Custom font rendering
```

### Input
```lua
btn(id)      -- Gamepad button (0=up,1=down,2=left,3=right,
             --   4=A, 5=B, 6=X, 7=Y)
btnp(id)     -- Button pressed this frame (vs held)
key(keycode) -- Keyboard state
keyp(keycode)-- Keyboard press
mouse()      -- Returns x, y, left, middle, right
```

### Sound
```lua
sfx(id, note, duration, channel, volumes)  -- Play SFX
music(id, duration, ...)                   -- Play music
```

### Memory
```lua
poke(addr, val)     -- Write byte to RAM
peek(addr)          -- Read byte from RAM
mset(x, y, tile_id) -- Set map tile
mget(x, y)          -- Get map tile
fset(index, flag)   -- Set sprite flag
fget(index, flag)   -- Get sprite flag
sync(mask, bank)    -- Sync VRAM banks
pmem(index, val)    -- Persistent memory (save data)
```

---

## Appendix B: SCUMMVM Block Formats (Reference)

For future implementation, the key SCUMM block types:

```
Room Resource (V6+):
  EN  (4 bytes) + size (4 bytes) + entry script bytecode
  EX  (4 bytes) + size (4 bytes) + exit script bytecode
  LSCR (4 bytes) + size (4 bytes) + script ID (2 bytes) + bytecode
  OC  (2 bytes) + size (4 bytes) + object header + verb table + bytecode
    object header: id (1-2 bytes), x, y, state, parent, walk_x, walk_y
    verb table: verb_id + offset pairs, terminated by 0xFF

Global Script:
  SCRP (4 bytes) + size (4 bytes) + bytecode

Object Code:
  OBCD (4 bytes) + size (4 bytes) + object_id + verb_table + bytecode
```

SCUMM bytecode is stack-based with ~150 opcodes. Full reference at:
https://wiki.scummvm.org/index.php/SCUMM/Technical_Reference/Script_resources
