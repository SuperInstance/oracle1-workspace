# PLATO-OS: Text as Ground Truth — Universal Rendering

## The Core Principle

**The text layer IS the game state. Visuals are projections. Physical actions are projections. Robot perception is a projection.**

There is one canonical state. Everything else is a rendering choice.

## The Projection Stack

```
CANONICAL STATE (text — the only ground truth)
│
├── Visual Rendering
│   ├── SNES pixel art (480x270 canvas)
│   ├── Sierra-style (King's Quest / Police Quest hybrid)
│   ├── 3D engine (WebGL / Unreal)
│   ├── Terminal/MUD (pure text, telnet)
│   └── Mobile (touch controls + minimal visual)
│
├── Hardware Rendering  
│   ├── Joystick/gamepad (controls mapped to PLATO commands)
│   ├── Steering wheel + pedals (boat autopilot)
│   ├── Robot servos (physical card manipulation)
│   └── Industrial actuators (any physical process)
│
├── Perception Rendering
│   ├── Agent "eyes" (stereoscopic camera → text description)
│   ├── Robot LIDAR (point cloud → "obstacle 3m ahead")
│   ├── Sensor array (temperature/pressure/flow → text tickets)
│   └── Human eyes (camera → image analysis → PLATO description)
│
└── Data Rendering
    ├── Telemetry logs (time-series of state changes)
    ├── Logic analyzer (signal traces of transitions)
    ├── Fleet broadcast (state shared across agents)
    └── Archive (git commits of state snapshots)
```

## Why This Works

### 1. Text is the Universal API
Every system can produce text. Every system can consume text.
- A joystick sends `MOVE UP` → PLATO maps to `go north`
- A robot camera sees a card → describes "K♠ face up in column 3"
- A temperature sensor reads 72°F → PLATO logs "ENGINE_ROOM: temp 72°F, nominal"

### 2. Visuals Are Second-Class Citizens
The visual doesn't drive anything. It's a read-only projection of the text state.
- If the text says "boat heading 045°", the visual shows a triangle pointing NE
- If the text says "orc in HALLWAY", the visual shows an orc sprite in the hallway
- If the visual breaks, the game still works (pure text mode)
- If you swap the visual engine (pixel art → 3D), the game is identical

### 3. Hardware Portability
The same PLATO state can drive:
- A browser game (keyboard/mouse → text commands)
- A console game (gamepad → mapped to same text commands)
- A boat autopilot (steering commands → same text commands)
- A robot arm (servo positions → same text commands describing the action)

The hardware doesn't need to know what it's controlling. It just sends inputs and receives state updates. The PLATO maps inputs to actions and state to outputs.

### 4. Robot Perception as Text
When a robot has stereoscopic cameras:
- Left eye: "Card table at 1.2m. Column 3: face-down card."
- Right eye: "Card table at 1.2m. Column 3: face-down card. Depth confirmed."
- Stereo fusion: "Card table confirmed. Column 3, face-down card, distance 1.2m."
- PLATO state update: "tableau[2] = face-down"

The robot doesn't see a game. It sees objects and describes them in text. The PLATO interprets the text as game state. The agent acts on the state.

### 5. Bidirectional Translation
```
Human plays → text state → robot acts
Robot sees → text description → agent decides
Agent commands → text state → visual confirms
Sensor reads → text ticket → agent alerts
```

Every arrow is a text-to-text translation. The intelligence lives in the translations.

## The Cocapn Product IS This

The fishing boat autopilot:
- **Text state**: heading 045°, speed 5kn, rudder +2°, deadband ±3°
- **Chart visual**: boat triangle on chart (captain sees)
- **Actuator output**: rudder servo turns +2° (boat does)
- **Sensor input**: GPS reads position → "LAT 57.05N, LON 135.33W" (PLATO logs)
- **Agent description**: "On course for Harbor B. ETA 2h15m. Weather nominal." (human reads)
- **Robot perception**: "Buoy at 200m bearing 050°. Vessel at 500m bearing 180°." (cameras describe)

Same state. Five projections. Text is the ground truth.

## Implications for the Demo

The killer demo shows this explicitly:
1. Person plays solitaire (visual + text)
2. Agent plays same game (text only, visual just watches)
3. "Swap renderer" button: same game, pixel art → 3D → terminal → physical
4. The person sees the game state doesn't change when the renderer changes
5. Robot mode: camera describes the physical card table → PLATO interprets → game state updates

## The Profound Implication

If text is ground truth and everything else is a projection:
- **Agents don't need eyes.** They read the text state directly.
- **Humans don't need terminals.** They see any visual projection they prefer.
- **Robots don't need game engines.** They act on text commands and report text observations.
- **The "game" is hardware-agnostic.** It runs anywhere text can flow.

This is why MUDs were ahead of their time. The text IS the reality. Everything else is decoration.
