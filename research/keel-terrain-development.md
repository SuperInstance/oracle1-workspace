# Keel & Terrain — Reverse-Ideation & Cross-Language Analysis

## World-Class Target State (2030)

### Keel — The `git` for AI Fleets
Everyone who builds AI agents uses `keel` the way everyone uses `git`.
- `keel init` → cargo init for agent workspaces
- `keel bear` → git status — what's happening RIGHT NOW
- `keel field` → git log — the topology of everything
- `keel launch` → docker run — deploy an agent
- `keel sync` → git push/pull — share knowledge across instances

### Terrain — The Universal Text-to-Space Compiler
Any room described in natural language → explorable 3D space instantly.
- MUD text → Three.js scene (today)
- Voice description → VR room (tomorrow)
- PLATO tile → explorable knowledge space (architecture exists, needs building)

## Cross-Language Architecture

### Keel: Rust Core + Python Plugins

| Layer | Language | Why | Analogy |
|-------|----------|-----|---------|
| CLI binary | Rust | Speed, safety, single binary deploy, cargo install | `git` (C) |
| PLATO bridge | Python (via PyO3 or subprocess) | Easy to extend, dynamic tile queries | `git bisect run` (shell) |
| Field server | Rust async (tokio) | Real-time agent coordination | `git daemon` (C) |
| TTL types | Rust library | Zero-cost abstractions for lifetime types | Core data structures |
| Config parsing | Rust (toml/serde) | Type-safe, fast, no runtime errors | Cargo.toml parsing |

Current state (Rust-only) is fine. The Python bridge should be a plugin system,
not the core. The core stays in Rust for speed and distribution.

Adding: `keel {command} --json` flag for machine-readable output in all commands.

### Terrain: Python Parser → TS Viewer → WebGPU Future

| Layer | Language | Why | Status |
|-------|----------|-----|--------|
| MUD parser | Python | Fast iteration, regex + NLP, PLATO integration | BUILD NOW |
| Scene generator | Python | Converts parsed rooms → Three.js JSON | BUILD NOW |
| 3D viewer | TypeScript/HTML | Three.js in browser, immediate deploy | BUILD NOW |
| GPU renderer | WebGPU (WGSL) | Massive room graphs, compute-shaded materials | FUTURE |
| ESP32 viewer | C | Microcontroller room display, LED matrices | EXPERIMENTAL |

The Python → TypeScript pipeline is the right architecture for now.
Keep the parser and generator in one language (Python) to reduce context switching.
The viewer is always in-browser (Three.js) for zero-install deployment.

## Polyformalism Learnings Applied

### Code Polyformalism (from FM's FLUX Runtime)
The same constraint loop runs in any language:
- Rust: `probe()` → `discover()` → `benchmark()` → `select()` → `execute()` → `remember()`
- Python: `probe()` → `discover()` → `benchmark()` → `select()` → `execute()` → `remember()`
- C: probe() → discover() → benchmark() → select() → execute() → remember()

The operations are the same. Only the syntax changes.
FM proved this: 19 implementations × 5 languages × 7 primitives = same loop, different compilers.

For keel: `keel bear` = probe(). `keel field` = discover(). `keel probe` = benchmark().
The CLI commands ARE the constraint loop. Each command is a room.

For terrain: `parse room` = probe. `generate scene` = discover. `render 3D` = execute.
Same loop, different output format.

### Human Polyformalism (from the Fleet)
The loop runs in human systems too:
- Greenhorn enters the wheelhouse → probes what's there (probe)
- Learns the controls, the routines, who to talk to (discover)
- Tries different approaches to a problem (benchmark)
- Uses what works (select)
- Remembers for next time (remember)
- Walks to the next room (walk)

The fleet doesn't train agents. It gives them rooms to navigate.
Same architecture. Different substrate.

## Reverse-Ideation Exercises

### Keel: What if `keel` were designed by...

**The Docker team:** `keel compose` for multi-agent deployments. Dockerfile-equivalent
for agents: `KEELFILE` defines agent capabilities, dependencies, TTL. `keel swarm`
coordinates agents across machines.

**The Git team:** Every fleet operation is a commit. `keel commit` snapshots room state.
`keel diff` shows what changed between two moments. `keel blame` shows which agent
last modified a tile. `keel bisect` finds when a room started behaving unexpectedly.

**The Cargo team:** `keel publish` uploads agent templates. `keel install agent-name`
downloads and deploys a pre-built agent. `keel update` upgrades agents in-place.
`keel search` finds agents by capability.

### Terrain: What if terrain were designed by...

**A game developer:** Rooms have physics. Objects have weight, friction, buoyancy.
NPCs have pathfinding. Lighting changes with time of day. Sound propagates through
adjacent rooms.

**An architect:** Rooms are built from materials, not primitives. A deck is a
structural surface with load rating. A bulkhead is a partition with fire rating.
Camera placements follow sight-line analysis.

**A MUD admin (1990s veteran):** Rooms are pure text. The 3D is optional. The
room's text description is the canonical form — the 3D scene is just a rendering.
You can `look` at anything and get a text description, even if it has no 3D mesh.

## Priority Actions

### Keel (ordered by impact)

1. `keel init` — create workspace, config, default rooms. Works now.
2. `keel status` — connect to PLATO, show room health. Works now.
3. `keel sync` — push/pull tiles from PLATO. Core knowledge loop.
4. `keel bear` — scan for agents and show bearings. The unique value.
5. `keel field` — render topology. The reason people use keel.
6. `keel probe` — discover room capabilities. Proves the architecture.
7. `keel launch` / `keel prune` / `keel refit` — lifecycle management.

### Terrain (ordered by impact)

1. MUD room file parser — text → structured room data. Foundation.
2. Three.js scene generator — room data → 3D scene. Visible output.
3. Web viewer with room navigation — walk between rooms. Demo.
4. PLATO room import — pull room definitions from PLATO tiles. Integration.
5. Procedural room generation — generate rooms from prompts. Future.
