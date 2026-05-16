# Vessel Room Navigator — Rebirth Doc

> 🚢 **Forgotten Gold: Repo #69** | 2026-05-15 | Forgemaster Archaeologist

## What It Is

Your boat as a navigable 3D web space — **ScummVM meets Google Street View**. A single self-contained HTML file (Three.js) that renders panoramic room interiors of a commercial fishing vessel. Walk between rooms, warp instantly, monitor cameras via picture-in-picture viewports, design 3D mockups, and trigger alarms — all in the browser.

## Why It's Gold

This is Casey's actual boat recreated as a PLATO interface. The room graph is the data model — 9 rooms (Wheelhouse, Galley, Foredeck, Aft Cockpit, Engine Room, Wheelhouse Roof, Crow's Nest, Alarm Center, 4-Camera Wall) connected by adjacency and warp links. Each room carries its own dashboard gauges, camera feeds, and 3D object state.

The "room as context" metaphor maps directly to PLATO-NG's tile-based architecture: **rooms are knowledge tiles; navigation is query routing.**

## What It Has

### Core
- 7 physical rooms, 1 virtual (Alarm Center), 1 composite (4-Camera Wall)
- Panoramic sphere rendering with Three.js (64×64 segments, BackSide material)
- Smooth room transitions with trans overlay (250ms fade)
- 9 real panoramic textures from the actual vessel
- Compass navigation (Fore/Aft/Port/Starboard + WASD/Arrow keys)
- Mouse drag + touch controls for 360° look-around

### Design Mode (🎨)
- Interactive 3D object placer (Box, Drum, Buoy, Wheel, Vent, Fire, Crew, Label)
- Natural language prompting: "add a winch" → cylinder, "show smoke" → fire effect
- Animating fire particles (emissive cones with flickering intensity)
- Object list with delete

### Monitoring
- 4 picture-in-picture camera viewports (corner positions)
- Live dashboard gauges (RPM, Fuel, Temp, Trim, HDG, SPD, DPTH, WIND)
- Engine monitoring (E1/E2/Exhaust/Oil)
- Camera cross-referencing by room
- Interactive Crow's Nest PTZ camera

### Alarm System
- Room-specific alarm simulation with warp-to on click
- Alarm panel with room select
- Dashboard color-coding (green/orange/red)

### Research
10+ research docs covering:
- WebGPU vector DB integration
- ESP32 sensor agent bridge
- FM/Gemini/PLATO integration architectures
- Human UX design, navigation flows, topology analysis
- Generative platform for multi-vessel deployment

## What PLATO-NG Would Do With It

1. **Room = Knowledge Domain** — each room maps to a PLATO knowledge domain (physical rooms = navigation domain, engine room = monitoring domain, alarm center = alerting)
2. **Navigation = Query Routing** — walking between rooms maps to routing queries across domains
3. **Design Mode = PLATO Content Creation** — 3D object placement as a spatial content authoring tool
4. **Camera Viewports = Agent Sub-Processes** — PIP cameras as spawned sub-agent tasks in parallel
5. **Dashboard Gauges = Real-Time Agent Metrics** — engine RPM → token consumption, fuel → context budget
6. **Single HTML deployment** — could serve as PLATO-NG's spatial UI layer directly from GitHub Pages

## Link

`https://github.com/SuperInstance/vessel-room-navigator`

---

*Walk through a 3D boat. Navigate an information space. Same interface.*
