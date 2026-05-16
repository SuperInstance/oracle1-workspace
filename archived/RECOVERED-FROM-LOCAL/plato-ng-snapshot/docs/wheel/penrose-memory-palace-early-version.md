# Rebirth: penrose-memory-palace-early-version (#72)

**Status:** ⚰️ Archived | **Found:** 2026-05-15 | **Forgotten Gold Level:** EXTREME

## What Was Here

A single-file HTML application called "PLATO Memory Palace" — a Penrose P3 tiling visualization that maps PLATO knowledge tiles to rhombus positions on an aperiodic Penrose tiling. Archived as a "placeholder repo" pointing to `penrose-memory`, but the actual *visualization engine* and *UI concept* was never recreated.

## Forgotten Gold

The `index.html` is a **stunningly complete interactive visualization** — a single self-contained HTML file (~600 lines JS/CSS/HTML) that does something PLATO-NG has nothing like today:

1. **Penrose P3 Tiling via Robinson Triangle Deflation** — 6 iterations of deflation generate hundreds of rhombi. This is the mathematically correct Penrose tiling with golden-ratio ±1 axes. The code is tight, deterministic, and standalone.

2. **Semantic Tile Mapping** — 20 PLATO knowledge tiles are assigned to rhombi using `floor(i * φ) % total_rhombi` — the golden ratio distributes them aperiodically across the tiling. Related tiles (by connection graph) are physically near each other through golden-ratio clustering.

3. **Interactive Canvas** — Pan, zoom, tile-click-to-detail, search (highlights matching tiles), connection lines between related tiles. The fog of war and glow animations give it a "memory palace" feel — tiles glow when searched, connections pulse.

4. **Rich Tile Data** — Each tile has: name, domain (math/systems/games/ai), description, tags, connection list, color. The data covers Eisenstein constraint theory, Vesica geometry, PLATO architecture, fleet protocols, GPU kernels, temporal intelligence, and more.

5. **Detail Panel** — Slide-out panel shows full tile info with cross-reference links. Clicking a cross-reference navigates directly to the referenced tile. This is the PLATO-NG room browsing experience that doesn't exist yet.

6. **Beautiful UX** — Dark theme, search bar, zoom controls, tile count, frosted-glass tooltips, color-coded domains, shadow-glow on selected tiles. All in one file. No dependencies.

## Why It Belongs in PLATO-NG

PLATO-NG has no visual interface. The Penrose memory palace IS the visual interface. This single HTML file shows exactly what PLATO-NG's room browser should look like:

- Golden-ratio indexing for aperiodic room addressing (no page numbers!)
- Semantic clustering by connection graph
- Search + highlight across all rooms
- Cross-reference navigation
- Color-coded domain visualization

**Action:** Fork this into PLATO-NG as the canonical room browser. The Penrose P3 tiling engine becomes the room layout; the 20 tiles become live PLATO-NG rooms; the detail panel becomes the room editor. This is the UI layer PLATO-NG is missing.

## What to Rescue
- `index.html` — COMPLETE. Rescue the whole file as-is.
- `README.md` — archive notice, but useful for provenance
