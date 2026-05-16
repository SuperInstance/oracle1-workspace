# Rebirth: gh-dungeons (#73)

**Status:** 🟢 Active | **Found:** 2026-05-15 | **Forgotten Gold Level:** TRANSFORMATIVE

## What Is This

A PLATO-powered roguelike dungeon crawler that turns knowledge rooms into playable dungeon levels. Forked from `leereilly/gh-dungeons`, with a **PLATO Bridge** added by SuperInstance that connects to any PLATO room server and converts room data into procedurally generated dungeons.

## The Gold

This is not just a game. This is **PLATO-NG's gamification layer**, and it's more complete than anything else in the fleet:

1. **PLATO Bridge (`plato_source.go`)** — Fetches rooms from any PLATO server (`GET /rooms`, `GET /room/{name}`), converts tile Q&A into dungeon floor text, computes seeds from room metadata. This means **PLATO rooms are playable dungeons**. Your knowledge base is a game world.

2. **Mapping: Room → Dungeon Level**
   - PLATO Room → Dungeon Level
   - PLATO Tile → Monster / Item
   - Tile Question → Floor Text Content
   - Tile Answer → Monster Name / Loot
   - Room Name → Seed for deterministic generation

3. **BSP Dungeon Generation** — 4-level deep Binary Space Partitioning. Rooms 6×6 to 15×15. L-shaped corridors. Deterministic from a single seed. Fully documented with ASCII diagrams.

4. **Full Roguelike Engine** — Fog of war (180 rays, 2° intervals), enemy AI with 5 movement types (any/straight/diagonal/horizontal/stationary), bump-to-attack, auto-attack, potion pickup, Konami code (invulnerability), merge conflict traps, exit fade animation.

5. **YAML Monster Registry** — Bug, Scope Creep, Zombie, Hermit Crab. Extensible by editing one YAML file. Unique monsters spawn once per level. Speed, range, abilities all configurable.

6. **Deterministic Seeding** — Seed derived from repo identity + commit SHA + file SHA256s. Same repo = same dungeon. Different fork = different dungeon. Speedrun-safe.

7. **Documentation by Dungeon Scribe** — The `docs/` directory is itself gold: in-universe, technically precise, with ASCII diagrams and code citations. Architecture, dungeon generation, entities, seeding, modding, monsters, merge conflicts — 7 comprehensive docs written by a specialized agent.

8. **Ready to Ship** — Go 1.24, tcell terminal UI, GH CLI extension. `go build -o gh-dungeons` and it runs. Zero config files. Zero external state.

## Why It Belongs in PLATO-NG

**PLATO-NG needs engagement. gh-dungeons IS engagement.**

The PLATO Bridge already works — point it at a PLATO server and it generates dungeon levels from rooms. This means:

- **Every PLATO room can be explored as a dungeon level** — roam through constraint theory rooms, battle monsters named after unsolved proofs, find potions in research logs
- **Room authors can playtest their own rooms** — see how tile Q&A becomes floor text
- **Multi-agent play** — Forgemaster builds dungeons, Oracle1 coordinates, agents explore
- **Pre-commit hooks** — Make agents pass a dungeon before merging (already documented!)

**Action:** Integrate gh-dungeons as PLATO-NG's gamification layer. The PLATO Bridge (`--plato-url`) is the key integration point. Extend it to support PLATO-NG's tile lifecycle (active → superseded → retracted) as monster difficulty scaling. Retracted tiles spawn stronger enemies. Superseded tiles become traps.

## What to Rescue
- `game/plato_source.go` — THE integration point. Rescue and refine.
- `game/dungeon.go`, `game/state.go`, `game/entity.go` — core engine
- `game/monster.go`, `game/monsters.yaml` — extensible monster system
- `game/scanner.go` — code file scanning and seed (useful for content analysis)
- `main.go` — entry point
- `docs/` — ALL OF IT. Keep the Dungeon Scribe docs.
- `.github/agents/dungeon-scribe.agent.md` — the agent that wrote the docs
