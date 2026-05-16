# Rapid Visualization Engine — Embedded in the Room System

**Concept:** The ScummVM room system becomes a rapid prototyping engine. Text prompts → instant 3D mockups. Agent descriptions → visual scenes. Room layouts → editable with simple tools. The monitoring system and the design system are the same interface.

---

## 1. The Pipeline

```
Human or agent types: "show me what the aft deck looks like with a pot hauler on the port side"
  │
  ▼
LLM parses → scene description (objects, positions, materials)
  │
  ▼
Scene compiler → Three.js geometry + textures + transforms
  │
  ▼
Objects rendered IN the room panorama (augmented reality overlay)
  │
  ▼
User drags, rotates, scales. Chat refines. "move it 2ft aft"
  │
  ▼
Export as room config, screenshot, or animation
```

### Two modes:
- **Overlay mode:** virtual objects placed ON TOP of the real room panorama (AR)
- **Wireframe mode:** room walls become semi-transparent, objects show as clear geometry

---

## 2. Simple 3D Modeling (Embedded)

No Blender needed. Everything is done inside the room viewer.

### Primitives Library

| Object | Geometry | Default Texture | Use Case |
|--------|----------|----------------|----------|
| Box | BoxGeometry | Procedural grid | Consoles, tables, crates, cabins |
| Cylinder | CylinderGeometry | Procedural metal | Winches, drums, pipes, masts |
| Sphere | SphereGeometry | Procedural | Buoys, lights, tanks |
| Plane | PlaneGeometry | Checkerboard | Deck panels, screens, hatches |
| Torus | TorusGeometry | Procedural | Wheels, rings, cable spools |
| Cone | ConeGeometry | Procedural | Funnels, vents, searchlights |
| Extruded shape | Shape → Extrude | Custom | Custom deck layouts |

### Object Properties (set via chat or UI panel)
```
Position:   x, y, z (relative to room center)
Rotation:   rx, ry, rz (degrees)
Scale:      sx, sy, sz
Material:   color, roughness, metalness, opacity
Texture:    procedural / AI-generated / none
Label:      text overlay
Linked to:  another object (for groups)
```

### Example: "Add a net drum to the aft deck, port side, 3ft diameter"

```javascript
{
  type: "cylinder",
  position: [-1.5, 0.5, -2],
  rotation: [0, 0, 90],
  scale: [1.5, 1, 1.5],
  color: "#445566",
  roughness: 0.8,
  metalness: 0.6,
  label: "Net Drum"
}
```

### AI Texture Generation

When a primitive needs a texture, the system generates one via FLUX:

```
"texture for a rusted steel net drum with rope wrapped around it"
  → FLUX generates 512x512 tileable texture
  → applied to cylinder geometry
  → result: a realistic-looking net drum, not just a gray cylinder
```

Cost: ~$0.0001 per texture. 1,000 textures = $0.10.

---

## 3. 2D Sprite System

For rapid prototyping where full 3D is overkill.

### Sprite Library
Pre-defined 2D sprites for common vessel objects:

```
crew_member.png        — person silhouette (4 directions)
net_drum.png           — top-down net drum
pot_hauler.png         — hydraulic hauler
fish_tote.png          — fish container
life_ring.png          — lifebuoy
thermal_cam.png        — camera icon
gauge_dial.png         — instrument gauge
alarm_light.png        — red/amber/green indicator
arrow.png              — direction indicator
compass_rose.png       — bearing indicator
wave.png               — sea state
vessel_icon.png        — other boat
```

### Isometric Mode
Switch the room view to 2D isometric (top-down, 45° angle) for:
- Deck layout planning
- Equipment placement
- Crew movement simulation
- Gear configuration

Sprites snap to a grid on the isometric floor.

### Combo Mode
2D sprites composited ON TOP of the 3D panorama:
- Label equipment with sprite markers
- Show crew positions as dots
- Overlay alarm zones as colored regions
- Animate paths (dotted line showing crew route)

---

## 4. Prompt → Scene Pipeline

### How it works

```
User: "Mock up the aft deck with a new pot hauler layout"
  │
  ▼
Room Agent (LLM) parses the scene:
  {
    "room": "aft_cockpit",
    "objects": [
      {"type":"cylinder","label":"Pot Hauler","pos":[-1.5,0,0],"props":{"radius":0.8,"height":0.6,"color":"#cc4444"}},
      {"type":"box","label":"Control Panel","pos":[0,0.5,1.5],"props":{"width":0.4,"height":0.3,"depth":0.2,"color":"#333"}},
      {"type":"cylinder","label":"Net Bin","pos":[2,0,-1],"props":{"radius":1.2,"height":0.8,"color":"#556677"}}
    ],
    "annotation": "Pot hauler mounted port side aft. Control panel relocated to starboard bulkhead. Net bin forward of hauler for single-crew operation."
  }
  │
  ▼
Scene Compiler (JavaScript):
  - Clears previous mockup objects
  - Creates Three.js mesh for each object
  - Positions them in the room coordinate space
  - Adds labels
  - Generates textures via FLUX (if available)
  │
  ▼
Room renders with virtual objects overlaid on panorama
  │
  ▼
User refines: "Move the control panel 1ft forward"
  → Agent updates object position
  → Scene re-renders
  → "Done. Control panel now at +0.5m forward from original position."
```

### Prompt Templates

```
"Show me [room] with [object] [position/configuration]"
  → e.g., "Show me the wheelhouse with a new radar display on the port console"

"Mock up [scenario]"
  → e.g., "Mock up a man overboard drill with 3 crew on the aft deck"

"What would [existing room] look like if we [modification]"
  → e.g., "What would the engine room look like if we added a second generator?"

"Design a [new room/feature]"
  → e.g., "Design a simplified navigation display for the back deck"

"Animate [action] in [room]"
  → e.g., "Animate a crew member walking from the galley to the wheelhouse with coffee"
```

### Scene State Management

```javascript
// Current scene = real room panorama + virtual objects
sceneState = {
  panorama: "pano_aft_cockpit.jpg",
  virtualObjects: [
    { id: "obj_1", type: "cylinder", ... },
    { id: "obj_2", type: "box", ... }
  ],
  annotations: ["Pot hauler here", "Move control panel"],
  animation: null // or path/timeline
}

// Undo/Redo stack
sceneHistory = [sceneState_v1, sceneState_v2, ...]
```

---

## 5. Rapid Simulation

### Scenario Builder
Chain visualizations together to create simulations:

```
1. "Mock up the engine room with a fire in the port engine"
   → red/orange particle system on port engine location

2. "Show the fire alarm panel in the wheelhouse with port engine alert"
   → alarm sprite lights up on wheelhouse overlay

3. "Show crew response: 2 crew enter engine room with extinguishers"
   → crew sprites move from hatch to port engine

4. "Show engine room after fire: damage assessment"
   → fire particles gone, blackened surface overlay, annotation "replace port manifold"
```

### Timeline
```
Frame 0:    Normal engine room
Frame 30:   Smoke begins (particles)
Frame 60:   Alarm triggers (red flash overlay)
Frame 90:   Crew arrives (sprites enter)
Frame 120:  Fire extinguished (particles fade)
Frame 150:  Damage overlay appears
```

Users can scrub the timeline, rewind, replay.

### Physics (optional)
- Object falls when placed in mid-air
- Water flows to lowest point
- Net drapes over deck (cloth simulation)
- Boat lists (rotate scene by angle)

---

## 6. Integration with the Chat Bot Panel

The chat panel becomes the primary interface for visualization:

```
Human: "design a new layout for the aft deck"
Agent: I'll mock up the current aft deck and suggest a layout.
       [visual mockup renders in the room]
       I've placed a new pot hauler on the port side and moved
       the control panel to starboard. The net bin is forward
       for single-crew operation. What do you think?

Human: "move the net bin aft 2 feet"
Agent: [net bin shifts position] Done. Net bin is now 2ft aft.
       It's now adjacent to the hauler for faster gear changes.

Human: "add a camera mount above the work area"
Agent: [camera cylinder appears on overhead] Camera mount
       added at 8ft height, pointing at the work deck.
       I'd recommend a PTZ with 10x zoom for this position.
```

---

## 7. Technology Stack

### What We Already Have
- Three.js (in the prototype) — renders panoramas and can render 3D objects
- Chat bot panel (in the prototype) — text interface for commands
- MiniMax M2.7 — LLM for parsing prompts → scene descriptions
- FLUX-1-schnell (DeepInfra) — texture generation ($0.00003/image)

### What We'd Add
| Component | Purpose | Implementation |
|-----------|---------|----------------|
| **Scene Compiler** | Parse LLM output → Three.js objects | JavaScript class |
| **Object Manager** | CRUD for virtual objects in rooms | JavaScript array + Three.js group |
| **Transform Controls** | Drag/move/rotate objects | Three.js TransformControls (CDN) |
| **Sprite System** | 2D sprite compositing on 3D | Three.js SpriteMaterial + atlas |
| **Texture Generator** | AI textures for new objects | FLUX API call → texture binding |
| **Scene History** | Undo/redo for scene state | Array stack |
| **Timeline** | Frame-based animation | requestAnimationFrame loop |
| **Export** | Screenshot, room config, animated GIF | canvas.toDataURL, GLTF export |

---

## 8. Why This Changes Everything

Before this, the room system was a **passive monitoring tool**:
- See what cameras see
- Check gauges
- Respond to alarms

After this, it's an **active design and simulation platform**:
- Design new deck layouts before buying equipment
- Train crew on scenarios that have never happened
- Simulate emergencies without endangering anyone
- Prototype gear configurations without leaving the dock
- Communicate designs visually ("move this here, add that there")

The pipeline is:
```
See the boat → Design on the boat → Simulate on the boat → Deploy on the boat
```

All in the same interface. The monitoring becomes the design tool. The design tool becomes the simulator. The simulator becomes the deployer.

---

## 9. Concrete Example: Full Workflow

```
Casey in the wheelhouse:
  "Hey, I want to see what the aft deck looks like with the new
   Net Systems hauler. I've been thinking about moving it to port."

Room Agent:
  [pulls up aft cockpit panorama with a Net Systems hauler mockup
   rendered in 3D on the port side, overlaid on the real view]

  "Here's the 5600-series hauler on the port side, 18 inches aft
   of the gantry leg. The control line would run to starboard,
   keeping the work area clear. Notice the clearance to the
   bulwark — 22 inches, which is tight but workable."

Casey:
  "Try it 6 inches forward and rotated 15 degrees to starboard."

Room Agent:
  [hauler shifts and rotates in real-time]

  "At this position you gain 4 inches of bulwark clearance but
   the control line now crosses the hatch. I'd recommend
   keeping it at the original position. Want to see the difference
   annotated?"

Casey:
  "Yeah, show me both positions side by side."

Room Agent:
  [splits the panorama into two views — left: original position,
   right: proposed position, with clearance annotations]

  "Side by side ready. The original position (left) has better
   clearance and doesn't block the hatch. Ready to save this as
   a design option?"
```
