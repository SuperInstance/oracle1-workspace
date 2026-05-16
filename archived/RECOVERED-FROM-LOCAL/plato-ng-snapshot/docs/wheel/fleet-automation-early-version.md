# 🏗️ fleet-automation-early-version — Proto-One-Delta Library

**Repo #51** | Cloned from `SuperInstance/fleet-automation-early-version` | Archived 2026-05-12

## Why This Exists

This 5KB scaffolding contains the **first working implementation of the One Delta principle** as a reusable Python library. Before the fleet had tile lifecycle, Lamport clocks, and simulation-first coordination, there was this — a simple decorator that caches API calls and auto-compiles repeated patterns into fast-path scripts.

## What's Here

### `fleet_automation/__init__.py` — The Core
A `ScriptCache` class with hash-based deduplication (MD5), threshold tracking (default=3 triggers compilation), and a `FleetAutomation` decorator that wraps any function. The `@automate(threshold=3)` decorator pattern:
- Tracks how many times each input has been seen
- At threshold, "compiles" the cached result into a script
- Subsequent calls hit the script path — no API invocation

### `demo.py` — Working Demo
Five calls to a simulated 50ms API, alternating between 2 patterns. The decorator triggers compilation at call #3 (pattern 0) and call #5 (pattern 1). Output shows API calls vs script hits with measured speedup ratio.

### `setup.py` — Publishable
Ready for PyPI distribution with standard setup.py packaging. Never published.

## Critical Gold

This is the **embryonic form of the entire fleet's intelligence layer**. The core insight — "cache API results, compile repeated patterns to scripts, only perceive when genuinely novel" — is the exact same One Delta principle that now powers the forge room, the trial system, and the tile lifecycle. The hash-based caching, the threshold trigger, the decorator pattern: all were designed correctly at this proto stage.

The threshold logic here (`counts[key] >= 3`) is the simplest possible trigger. It works. But the experiments in `fleet-experiments` (repo #50) now suggest optimal thresholds depend on the cost ratio — this implementation was built before the math was proven.

## Rebirth Path

- The `ScriptCache` and `FleetAutomation` classes should be refactored into `plato-ng/libs/automation/`
- Replace the hardcoded threshold=3 with adaptive threshold based on exp1_speedup.py's cost model
- Add persistence layer (currently pure in-memory)
- The demo.py is a perfect test fixture
