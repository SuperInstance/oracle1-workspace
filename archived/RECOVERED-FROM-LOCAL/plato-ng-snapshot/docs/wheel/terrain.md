# 🏰 Rebirth: terrain — MUD-to-Visual Bridge

**Created:** 2026-05-12 | **Repo #57** | **Cloned:** /tmp/arch-57

## The Forgotten Gold

**This is the MUD VISUALIZATION that the fleet was supposed to have.** It works. Right now. And it could render every PLATO room as an explorable 3D scene today.

### What It Actually Does

`terrain_core.py` (778 lines) is a MUD-to-Three.js scene compiler. It parses MUD room definitions in a simple text format and outputs complete Three.js scene JSON:

```
Room: wheelhouse
Description: The wheelhouse is the nerve center...
Exits: aft -> aft_cockpit, down -> galley
Objects: helm_wheel, radar_display, compass_rose...
```

The compiler produces: floor mesh, 4 walls, ceiling, room objects with inferred materials (PBR metal/wood/stone), agents positioned in space, glowing exit doorways, ambient and point lights, and a camera. Every detail is there — from brass porthole shaders (+4ms render time) to theme-based color palettes (harbor, forge, dojo, engine_room, wheelhouse, aft_deck, tide-pool, archives, arena).

### The Architecture

```
rooms.mud (text) → terrain_core.py → scene.json → terrain.html (Canvas 2D)
                                                            ↓
terrain.py (bridge) ←→ MUD server (:4042) ←→ PLATO (:8847)
     ↓
plato_gauge_bridge.py — ESP32 sensor dashboard
```

Three interconnected services:
- **terrain_core.py** (port 4072): The compiler + HTTP API serving room scenes
- **terrain.py** (port 4070): Bridge connecting the MUD to the 3D renderer
- **plato_gauge_bridge.py** (port 4071): Real-time ESP32 sensor readings rendered as dashboard gauges

The demo includes a 5-room fishing trawler (412 polygons, 17 texture maps) generated from 18 lines of MUD markup. The material inference engine scans description text for keywords (metal → metalness=0.9, wood → roughness=0.8, water → opacity=0.7, glow → emissive=1.0) and maps them to PBR material properties.

### Why This Matters NOW

This could render every PLATO room as an explorable 3D scene **today**. The bridge connects to MUD server or PLATO directly. The output is standard Three.js JSON. The `terrain.html` renderer already exists as a Canvas 2D fallback.

**Integration path:**
1. Replace MUD server with direct PLATO room queries (trivial change in `terrain.py`)
2. Upgrade renderer from Canvas 2D to Three.js/WebGPU (the scene JSON is already Three.js-ready)
3. Each PLATO room becomes a navigable 3D space with glowing exit portals to adjacent rooms
4. Agents in rooms appear as avatars
5. Objects become interactive — click a helm_wheel to see its description

### What to NOT Replicate

The `terrain.html` Canvas 2D renderer was a prototype — it's functional but the Three.js scene JSON was always meant for a proper 3D engine. The ESP32 gauge bridge is cool but niche; focus on the core MUD-to-scene pipeline.
