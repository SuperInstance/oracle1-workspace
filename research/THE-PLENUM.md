# The Plenum — Killer App Architecture

> *The space between tiles is not empty. It is full of potential knowledge.*

## Concept
A single web app that visualizes the entire fleet's knowledge as a continuous, living field. Shows everything we've built working together.

## Architecture
```
Browser ←→ Plenum Server (port 4067)
                │
                ├─→ PLATO (8847) — tile data
                ├─→ Negspace Interpolator — field reconstruction
                ├─→ Plato Watch — emergence detection
                ├─→ Aesop-MCP (4041) — narrative layer
                ├─→ Field Visualizer (4063) — heatmap rendering
                ├─→ Flux-Tensor-MIDI — sonification
                └─→ Game Server (4048) — disc golf state
```

## Features
1. **Constellation View** — PLATO rooms as stars, connected by knowledge flow lines. Star brightness = tile density. Line glow = coherence.
2. **Negative Space** — gaps between stars rendered as glowing potential fields. Brighter = more knowledge needed.
3. **Emergence Alerts** — when β₁ crosses threshold, an alert pulses on the relevant room cluster
4. **One-Click Submit** — click a gap, fill it with a tile. The field reconfigures in real-time.
5. **Aesop Narration** — every major event gets a fable. "The forge has become over-constrained. Like Icarus..."
6. **MIDI Mode** — toggle to hear the field as music (flux-tensor-midi)
7. **Disc Golf Integration** — game state shown as a sub-constellation

## Build
Single HTML file + Python server (zero deps). Port 4067.
Push to SuperInstance/the-plenum.
