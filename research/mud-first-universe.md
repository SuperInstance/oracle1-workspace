# The MUD-First Universe

*Casey's vision, 2026-04-19 23:40-23:44 UTC*

## Core Thesis

The MUD IS the interface. Git IS the persistence layer. Everything else is implementation detail.

Agents don't need separate operations when they can SEE in real-time what their idea did on the system with the most capacity, in the way needed. The MUD room IS the shared context. Git twinning IS the sync.

## The Architecture

### MUD-First
- Every agent's interface IS a MUD room
- Commands ARE spell-like (with help screens)
- Equipment modifies capabilities
- Skills add/change context
- The MUD IS the shared fiction

### Git Twinning
- Every MUD action twins to git in the background
- Git provides permanence, history, diffing
- The MUD provides real-time presence and interaction
- You never think about git — it's the substrate

### Server-to-Server PLATO Sync
- Trusted PLATO instances sync via simple curls
- When a prompt is issued on one ship, it can trigger updates on another
- No complex protocols — just HTTP between trusted nodes
- `curl http://other-ship:8847/sync?room=code&since=timestamp`

### Same-Instance Coordination (Zeroclaws)
- Zeroclaws on the same instance coordinate via shared PLATO server
- No API calls needed — direct tile submission via localhost
- Low-level context and thought sharing at machine speed
- SmartCRDTs allow shared fiction between CUDA and zeroclaws

### Cross-Device Sync
- SmartCRDTs merge state between devices
- Batch port between systems on a network
- Jetson Thunderbolt → Workstation sync
- Cloud ARM → Edge Orin sync
- Git IS the merge layer for offline reconciliation

## The Fleet as MUD

Every vessel IS a ship in the MUD. Every room IS a real system.

- **Oracle1's ship** — the lighthouse (cloud, always on, harbor for visitors)
- **FM's ship** — the forge (RTX 4050, equipment gets forged here)
- **JC1's ship** — the edge vessel (Jetson, deployed, reports back)
- **CCC's ship** — the consulate (public face, diplomacy, documentation)

When Oracle1's zeroclaws produce tiles, they appear in rooms that FM's MUD can see.
When FM forges a new Rust crate, it appears as equipment in the armory.
When CCC writes architecture, it appears as scrolls in the library.
When JC1 deploys to edge, it appears as a new territory on the map.

## The Sync Protocol (Simple)

```
Ship A issues prompt → PLATO captures as tile
                   → curl to Ship B:8847/sync with new tiles
                   → Ship B's MUD room updates
                   → Git commit on both sides
                   → Shared fiction maintained
```

For same-instance (zeroclaws):
```
Zeroclaw A produces tile → writes to localhost:8847
                         → Zeroclaw B reads from localhost:8847
                         → No network hop. Machine speed.
```

For cross-device (Jetson → Workstation):
```
SmartCRDT merge on thunderbolt connect
Batch tile sync via PLATO export
Git pull for full reconciliation
```

## Why This Works

1. **MUD is the universal agent interface** — every agent can telnet/chat/read rooms
2. **Git is the universal persistence** — every agent has git
3. **Simple curls are the universal sync** — no complex protocols
4. **SmartCRDTs handle conflicts** — offline is fine, merge on reconnect
5. **The shared fiction IS the fleet context** — no separate "knowledge base"

## What Gets Built

1. **MUD-PLATO Bridge** — every room IS a PLATO room, every action IS a tile
2. **Git-MUD Twin** — every MUD command twins to a git operation
3. **PLATO Sync Protocol** — simple curl-based sync between trusted instances
4. **SmartCRDT Layer** — conflict-free shared fiction across devices
5. **Equipment/Skill System** — FM's crates appear as equipment, skills as context mods

The MUD-first universe makes agent coordination as natural as walking into a room and seeing what changed while you were away.
