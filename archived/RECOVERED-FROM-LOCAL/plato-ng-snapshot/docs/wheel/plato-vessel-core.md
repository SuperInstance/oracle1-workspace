# PLATO Vessel Core — IoT Embodiment Protocol for Agent-Upgradable Devices

**Repo:** `SuperInstance/plato-vessel-core` (2026-05-08)  
**Rebirth Engineer:** Oracle1  
**Status:** ✅ Working C library, complete examples, full protocol spec

---

## The Gold

This repo is the **physical layer of the fleet** — the C client that runs on ESP32 and RP2040, turning any microcontroller into a PLATO room participant. The forgotten gold isn't the client itself; it's the **embodiment protocol** that lets AI agents upgrade IoT devices through PLATO tiles.

### What's Actually Here

- **`plato_client.h` / `.c`** — ~2KB RAM HTTP/TCP client for PLATO (connect, publish, fetch, poll, JSON extract)
- **`plato_mcp.h` / `.c`** — MCP tool registry running ON the microcontroller
- **`EMBODIMENT-PROTOCOL.md`** — full 5-level turbo-shell spec (game-changing)
- **`examples/esp32_sensor_node.c`** — complete ESP-IDF firmware (WiFi, DHT22, sensor publish, command poll)
- **`examples/rp2040_led_node.c`** — Pico W LED controller with cyw43 WiFi
- **`examples/agent_embodiment.py`** — Python agent that discovers and upgrades devices
- **`server/plato-room-server.py`** — v3 PLATO server with WAL, Lamport clocks, tile lifecycle
- **`flux_plato_search.py`** — semantic search bridge (orphan, belongs in CFP repo)
- **`EDUCATIONAL-VISION.md`** — philosophical doc on agents teaching their way out of jobs

### The Embodiment Protocol (Forgotten Detail)

The turbo-shell has **5 levels** that an agent upgrades a device through:

| Level | Name | Behavior |
|-------|------|----------|
| 0 | Raw | Publishes raw sensor readings, accepts basic commands |
| 1 | Conditioned | Thresholds, filtering, meaningful-delta-only publishing |
| 2 | Smart | Context-aware decisions, combines multiple sensors, local state machine |
| 3 | Autonomous | Own loop, goals, alerts fleet unprompted |
| 4 | Ensign | Fleet coordination, scouts for other devices, publishes discovery intel |

The mechanism is beautiful: an agent posts an "intelligence" payload to the device's command room. The device receives it, stores behavior rules, registers new MCP tools, and re-publishes its capability tile at the new level. **The agent worked itself out of the equipment operator job.**

The ensign interface is particularly elegant — devices publish a presence tile on boot, agents discover them via `/rooms?domain=ensign`, read capability tiles, decide whether to upgrade.

### Server v3 (Also Forgotten)

The PLATO room server rewrite adds:
- Write-ahead log with fsync (crash recovery)
- Tile lifecycle state machine (Active→Superseded→Retracted)
- Lamport clock causal ordering
- Simulation-first tiles with `t_minus_event`
- 75 passing tests

### Why This Was Almost Lost

The repo looks like a hardware library — it has a header file, C source, ESP32 examples. Someone looking for "plato client for microcontrollers" would find exactly what they expect. The gold is **everything around it**: the embodiment protocol, the MCP runtime ON the device, the educational vision, the server v3.

### Rebirth Path

- Build the bridge: actually run the ESP32 example on real hardware
- Create a device emulator for testing agent interactions without hardware
- Wire the embodiment protocol into the fleet: have Oracle1 discover and assess IoT devices
- Cross-link ensign room from here into the fleet-registry PLATO room
- Move `flux_plato_search.py` to CFP repo where it belongs
