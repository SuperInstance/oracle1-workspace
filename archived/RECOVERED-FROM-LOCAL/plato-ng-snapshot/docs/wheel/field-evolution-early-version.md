# 🔭 field-evolution-early-version — Proto-Emergence Monitor

**Repo #52** | Cloned from `SuperInstance/field-evolution-early-version` | Archived 2026-05-12

## Why This Exists

This 1KB scaffolding is the **first working emergence monitor** for the fleet. It watches the forge room in real-time, computes tile similarity graphs, and tracks ε over time. Before there was a dashboard, before there were formal emergence thresholds, this script was running in the background catching emergent patterns.

## What's Here

### `track.py` — The Emergence Tracker
A dual-mode script:
- **One-shot mode** (`python3 track.py`): Fetches forge room tiles from PLATO, builds a word-overlap similarity graph, computes `V`, `E`, `β₁`, and `ε`. Prints snapshot status (EMERGENT or STABLE).
- **Watch mode** (`python3 track.py --watch`): Polls every 30 seconds, logs evolution to `/tmp/field-evolution.json`, prints a live bar chart of ε with visual feedback.

The emergence formula is the same ε formula validated in `fleet-experiments` (repo #50): β₁ from homology, normalized by V-2, threshold at 0. But this implementation uses **word-overlap Jaccard similarity** (threshold 0.15) to build the edge set — a practical heuristic that predates the formal PLATO relationship model.

### `README.md` — Archived
Standard Cocapn archive notice. "The ideas were real — the implementations just didn't land."

## Critical Gold

This is **runtime evidence that emergence detection was being field-tested before the math was fully proven**. The watch mode writes a JSON log that could, with minimal effort, be turned into a time-series graph of emergence evolution. The 30-second polling interval, file-based persistence, and live bar-chart feedback all foreshadow the current monitoring infrastructure.

The Jaccard word-overlap approach is crude but surprisingly effective — it mirrors what PLATO's relationship model does more formally today. The 0.15 threshold was chosen empirically and works for medium-sized rooms.

## Rebirth Path

- The watch-mode JSON logger should become the telemetry sink for `plato-ng`
- Replace Jaccard word-overlap with the PLATO relationship model (tile→tile edges)
- Port the live bar chart into a forge room dashboard widget
- The 30s polling interval is good for room-level monitoring; tile-level may need sub-second
