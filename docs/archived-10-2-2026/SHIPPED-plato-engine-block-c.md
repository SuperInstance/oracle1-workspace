# SHIPPED: plato-engine-block-c

**Date:** 2026-07-12
**Commit:** `50ab2af` on `master`
**Clone:** `git clone https://github.com/SuperInstance/plato-engine-block-c`

## What It Is

Tiny embeddable sensor→history→alarm engine in C99. Zero dynamic allocation after init. Single-header library. Designed for marine vessel monitoring, IoT, and embedded systems. Includes standalone daemon and multi-client TCP server.

## What Was Done

### CI Fix
- **Replaced stub CI** (`echo "No CI configured"`) with real pipeline:
  - Builds all targets (`make all`)
  - Builds and runs all tests (`make test`)
  - Builds all examples (`make examples`)
  - Verification step: clean build from scratch
- Tests now gate merges

### License
- MIT — already present, verified ✓

### Packaging (Makefile)
- Already excellent: `-std=c99 -Wall -Wextra -Wpedantic -O2`
- Targets: `all`, `test`, `examples`, `clean`, `DEBUG=1`
- No changes needed ✓

### Release Workflow
- Added `.github/workflows/release.yml` — triggers on version tags (`v*`)
- Creates source tarball with all source + docs
- Creates GitHub Release with auto-generated notes

### Code Quality
- Fixed 8 compiler warnings in `test_protocol.c` (unused variables under `-Wextra`)
- All code now compiles clean with `-Wall -Wextra -Wpedantic`

### .gitignore
- Added missing `symmetry_demo` binary

## Test Results

```
=== Engine Tests ===       14/14 passed
=== Protocol Tests ===     14/14 passed
=== History Buffer Tests === 7/7 passed
                           ----
                           35/35 passed
```

Zero compiler warnings across all targets (engine, server, tests, 4 examples).

Coverage:
- Engine: init, sensors, tick, history overflow, alarms (fire/cooldown/re-arm/miss), actuators, subscribe
- Protocol: tick, history, actuator set, alarm list, subscribe, help, quit, unknown, whitespace
- History: push, retrieve, wrap, multi-sensor independence

## How to Use

```bash
# Build
make

# Run tests
make test

# Interactive daemon
./plato_engine
> tick
> history 5
> alarm list

# Auto-tick daemon (1s interval)
./plato_engine -a 1000

# TCP server (multi-client)
./plato_server 7070

# Embed in your project (single header!)
#define PLATO_ENGINE_IMPL
#include "plato_engine.h"
```

## Genuinely Usable?
Yes. Single-header C99 library, zero heap allocation, 15KB binary. Someone can clone, `make`, and have a working sensor monitoring daemon in 10 seconds. ESP32 porting guide in the README. This is the most embedded-ready repo in the ecosystem.
