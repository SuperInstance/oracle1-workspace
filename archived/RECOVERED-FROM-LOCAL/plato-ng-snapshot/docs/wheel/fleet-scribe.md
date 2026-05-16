# 📝 fleet-scribe — Download-and-Try Digital Twin Builder

**Repo #48** | Created: 2026-05-11 | Status: 🚢 SHIPPED (PyPI: `pip3 install fleet-scribe`)

## What Was Found

fleet-scribe is a **digital twin builder** that sits beside any application, mirrors its state to PLATO rooms, and implements the One Delta principle end-to-end. Installation is one command: `pip3 install fleet-scribe && scribe --app my_app`. No infrastructure, no server, no configuration files.

## Forgotten Gold

### 1. The 5-Stage One Delta Loop (Fully Implemented in 2k Lines)

The entire One Delta lifecycle shipped working:

1. **MIRROR** — `AppMirror.snapshot()` walks files, reads processes, captures system metrics
2. **SNAP** — `DeltaDetection.delta()` compares current vs baseline, returns only what changed
3. **SIMULATE** — `Simulator.predict()` runs linear extrapolation on gradient history
4. **PERCEIVE** — gradient > threshold triggers perception tiles to PLATO with full context
5. **OPTIMIZE** — `compile.py` detects constants, cycles, and trends across N observations; compiles to fast check functions

### 2. Core Library Modules (Production-Ready)

| Module | Lines | Purpose |
|--------|-------|---------|
| `core.py` | ~220 | `DeltaDetection` — state comparison, array diff, text diff, deterministic cache keying |
| `cache.py` | ~210 | `FileCache` — persistent JSON-backed cache (sha256-based filenames, TTL/prune, hit/miss stats) |
| `compile.py` | ~240 | Pattern detection (constant/cycle/trend) + `CompiledRule` generation with fast check functions |
| `automate.py` | ~260 | Action automation — HTTP webhooks, shell commands, Python functions, PLATO tiles; threaded executor with throttling |
| `scribe.py` | ~200 | CLI entry point + `Scribe` unified class (combines all modules) |

### 3. Pattern Compilation: The Automation Pipeline

The `compile.py` module is the hidden gem:
- **Constant detection**: identical values across N observations → `confidence = 1.0` — compiled rule: `lambda v: v == expected`
- **Cycle detection**: autocorrelation at multiple lags detects periodicity → compiled rule with period/phase/amplitude
- **Trend detection**: direction consistency score monitors monotonic trends → compiled rule checks value against trend line
- All patterns with confidence < 0.5 are excluded (anti-noise)

### 4. Delta Detection Engine (`core.py`)

- **Dict-based state comparison**: returns `{added, removed, changed, magnitude}` with threshold filtering
- **Array delta**: element-wise relative difference with NaN handling → boolean change mask
- **Text delta**: SequenceMatcher-based line-level diff with edit distance
- **Deterministic cache keying**: SHA-256 of canonical JSON or numpy bytes (16-char hex)

### 5. Automator: The "If-This-Then-That" Engine (`automate.py`)

- 4 action types: function, HTTP (webhooks), shell (with template variables), PLATO (tiles)
- Threaded executor (configurable worker count) with async queue
- Per-pattern throttle (cooldown seconds to prevent flooding)
- Glob pattern (`*`) to fire on any delta

## PLATO-NG Integration Path

1. **Re-host as PLATO-NG SDK module**: The `Scribe` class pattern (`watch() → compile_all() → automate`) maps directly to PLATO-NG's agent lifecycle
2. **Port FileCache**: The SHA-256 filename scheme + TTL pruning is perfect for PLATO-NG's edge-cache layer
3. **Pattern compilation as PLATO-NG built-in**: Constant/cycle/trend detection should be a native PLATO-NG room feature — rooms should self-report their stability profile
4. **Automator as Agent Reflex**: The action automation system should become PLATO-NG's reflexive layer — "when the gradient crosses threshold, write this tile"
5. **Flux bytecode compilation**: The compile.py pipeline is the natural path from observation → FLUX bytecode (currently compiles to Python functions; the next step is compiling to FLUX-ISA)

---

*One command. Sits beside any app. Builds a PLATO twin. Every interaction is a witnessed tile.*
