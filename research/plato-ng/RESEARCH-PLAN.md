# PLATO-NG Research Plan

## Parallel Research Tracks (run simultaneously)

### Track 1: Mutable Tile Protocol
Research question: How do we add mutable state to PLATO's immutable provenance chain?
Approach: Versioned tiles. Each tile inherits the provenance chain but allows UPDATE operations that add a new link. The LATEST version is the current state. Version history IS the provenance.
Deliverable: Protocol spec + prototype

### Track 2: GUARD-as-Gate
Research question: Can FLUX GUARD constraints serve as PLATO tile validation gates?
Approach: Gate system (P0-P4) currently validates tile quality. Add P5: constraint gate. A tile is accepted only if it satisfies a GUARD constraint. The constraint IS the tile schema.
Deliverable: Gate P5 implementation sketch

### Track 3: SCUMMVM/TIC-80 Render Adapter
Research question: Can we render PLATO app-ui/ tiles as SCUMMVM rooms or TIC-80 carts?
Approach: PLATO room app-ui/ contains tiles {background, sprites, zones, scripts}. Adapter reads these and generates SCUMMVM script (.scr) or TIC-80 cart (.tic).
Deliverable: Functional adapter prototype

### Track 4: LÖVE2D/Lua Render Adapter
Research question: Same as T3 but for Lua/LÖVE2D.
Deliverable: Functional adapter prototype (lower complexity than SCUMMVM)

### Track 5: Vibe Coding Agent
Research question: What agent architecture enables rapid game iteration via chat?
Approach: Agent reads human intent from PLATO app-io/ tile, generates/updates app-ui/ and app-logic/ tiles, human sees result immediately. Loop speed is the key metric.
Deliverable: Agent spec + prototype

### Track 6: FLUX-PLATO Native Runtime
Research question: Can FLUX-C run PLATO's tile computation natively?
Approach: FLUX-VM gets PLATO syscalls (room_read, tile_write, constraint_check). PLATO-NG runs ON the FLUX-VM as a FLUX process.
Deliverable: Runtime architecture spec
