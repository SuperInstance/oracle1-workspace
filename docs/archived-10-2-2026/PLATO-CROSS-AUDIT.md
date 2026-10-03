# PLATO Cross-Implementation Audit

**Date:** 2026-07-12  
**Auditor:** OpenClaw Automated Audit  
**Spec:** PLATO Wire Protocol v0.1 (`SuperInstance/AI-Writings/PLATO_WIRE_PROTOCOL.md`)

---

## Executive Summary

A comprehensive audit of six repos identified as "PLATO" implementations reveals **critical incompatibilities** with the wire protocol specification and with each other. **Zero implementations** are spec-compliant. Three repos are not PLATO engine blocks at all.

### Headline Findings

1. **No implementation produces JSON responses.** The spec mandates `{"type":"...", "data":{...}}` JSON for all responses. Every implementation uses ad-hoc plain text formats.
2. **No implementation sends the required welcome JSON.** The spec requires `{"type":"welcome","room_id":"...","tick_hz":...,"sensors":[...]}` on connect.
3. **Three of six repos are unrelated projects** sharing the PLATO name but implementing entirely different concepts.
4. **Command sets are inconsistent** across implementations — no two share the same command surface.
5. **The `actuator <name> <value>` command is missing** from all implementations — they use bare `<name> <value>` instead.

### Repositories Audited

| Repo | Language | Actually a PLATO Engine? | Spec Compliance |
|------|----------|-------------------------|-----------------|
| `plato-engine-block-c` | C | ✅ Yes (flagship) | ❌ 0/10 spec checks |
| `plato-engine-block` | Rust | ✅ Yes (reference) | ❌ 0/10 spec checks |
| `plato-engine-block-elixir` | Elixir | ✅ Yes | ❌ 0/10 spec checks |
| `plato-engine-block-zig` | Zig | ✅ Yes | ❌ 0/10 spec checks |
| `plato-runtime-kernel` | Rust | ❌ No — spatial spreadsheet engine | N/A |
| `plato-core` | Python | ❌ No — ML training tile registry | N/A |
| `plato-server` | Python | ❌ No — HTTP knowledge system | N/A |

---

## 1. PLATO Wire Protocol Spec Requirements

The spec (`PLATO_WIRE_PROTOCOL.md v0.1`) defines:

### 1.1 Response Format
All room→agent responses must be **single-line JSON objects** with a `type` field:
```json
{"type":"tick","t":1749234437.0,"seq":42,"data":{"coolant_temp_c":96.3}}
```

### 1.2 Command Surface
| Command | Response `type` | Required |
|---------|----------------|----------|
| `tick` | `tick` | ✅ |
| `history [N]` | `history` | ✅ |
| `actuator <name> <value>` | `ack` | ✅ |
| `alarm list` | `alarm_list` | ✅ |
| `alarm set <id> <condition> <cooldown>` | `ack` | ✅ |
| `subscribe` | `subscribed` | ✅ |
| `unsubscribe` | `unsubscribed` | ✅ |
| `help` | `help` | ✅ |
| `quit` | `bye` | ✅ |

### 1.3 Session Lifecycle
- Server sends `welcome` JSON on connect (with `room_id`, `tick_hz`, `sensors[]`)
- Default port: **1234**
- All text is UTF-8, lines end with `\n`

### 1.4 Spontaneous Messages
- **Alarm notifications** to subscribed clients: `{"type":"alarm","id":"...",...}`
- **Tick streams** to subscribed clients

---

## 2. Implementation-by-Implementation Analysis

### 2.1 C Implementation (`plato-engine-block-c`) — Flagship

**Files examined:** `include/plato_engine.h`, `src/main.c`, `src/server.c`, `src/sensors_dummy.c`

#### Tick Loop
- ✅ Reads all sensors via callbacks, stores in history ring buffer per sensor
- ✅ Evaluates alarms with cooldown semantics
- ✅ Evaluates symmetry pairs (extension beyond spec)
- ✅ Veto system (extension beyond spec)
- ❌ History is **per-sensor ring buffer** (array of `double`), not per-tick snapshots. Spec implies tick-level snapshots with `{"t":...,"seq":...,"data":{...}}`.

#### Sensor/Actuator Registration
- ✅ `plato_add_sensor(eng, name, fn, user_data)` — returns int index
- ✅ `plato_add_actuator(eng, name, fn, user_data)` — returns int index
- ✅ Registration is callback-based, clean API

#### History Buffer
- ❌ **Per-sensor**, not per-tick. Each sensor has its own `plato_history_t` ring buffer of doubles.
- ❌ No timestamp or sequence number stored with readings
- ❌ `history` command outputs per-sensor, not per-tick: `sensor_name: 1.00 2.00 3.00`

#### Alarm System
- ✅ Comparison operators: `GT, LT, GTE, LTE, EQ` (spec uses `<, >, ==, !=, <=, >=`)
- ✅ Cooldown system (tick-count based)
- ✅ Severity levels: `INFO, WARN, CRIT, VETO`
- ✅ Symmetry alarms (extension)
- ❌ No `alarm set` runtime command — alarms only configured at init
- ❌ No `cooldown_sec` — uses tick counts, not seconds
- ❌ No `last_triggered` timestamp in alarm state

#### Text Protocol — DEVIATIONS
| Check | Status | Details |
|-------|--------|---------|
| JSON responses | ❌ | Uses plain text: `tick 42: coolant_temp_c=96.30` |
| Welcome JSON | ❌ | Sends plain text: `Plato Engine Block — type 'help'` |
| `actuator` command | ❌ | Uses bare `<name> <value>`, not `actuator <name> <value>` |
| `alarm list` format | ❌ | Plain text list, not JSON `alarm_list` |
| `alarm set` command | ❌ | Does not exist |
| `subscribe` response | ❌ | Returns `ok subscribed`, not `{"type":"subscribed","tick_hz":...}` |
| `history` response | ❌ | Per-sensor text, not JSON per-tick |
| `help` response | ❌ | Plain text, not JSON with `commands[]` |
| `quit` response | ❌ | Returns `bye` (text), not `{"type":"bye"}` |
| Default port | ❌ | Uses 7070, spec says 1234 |

### 2.2 Base Rust Implementation (`plato-engine-block`)

**Files examined:** `src/engine.rs`, `src/protocol.rs`, `src/server.rs`, `src/tick.rs`, `src/sensor.rs`, `src/actuator.rs`, `src/history.rs`, `src/alarm.rs`

#### Tick Loop
- ✅ Reads all sensors via callbacks into `Tick` struct with `index`, `timestamp`, `data: Vec<(String, f64)>`
- ✅ Evaluates alarms against tick data
- ✅ Pushes tick to history buffer
- ✅ Tick struct has proper timestamp and sequence (index)

#### Sensor/Actuator Registration
- ✅ Builder pattern: `.sensor("temp", Box::new(|| 22.5))`, `.actuator("heater", Box::new(|v| ...))`
- ✅ Clean, type-safe API

#### History Buffer
- ✅ **Per-tick** circular buffer — correct approach per spec
- ✅ Stores full `Tick` objects (index + timestamp + all sensor data)
- ✅ `query(n)` returns last n ticks oldest-first

#### Alarm System
- ✅ Closure-based conditions: `Box<dyn Fn(&[(String, f64)]) -> bool>`
- ✅ State machine: `Idle → Active → Cooldown → Idle`
- ✅ Cooldown in ticks
- ❌ No `alarm set` runtime command
- ❌ No `alarm list` in spec format (just debug-style listing)
- ❌ No `last_triggered` timestamp

#### Text Protocol — DEVIATIONS
| Check | Status | Details |
|-------|--------|---------|
| JSON responses | ❌ | Plain text: `tick 0 @ 0.000s\n  temp = 22.5000` |
| Welcome JSON | ❌ | Sends `Plato Engine Block v0.1.0\nType 'help'` |
| `actuator` command | ❌ | Uses bare `<name> <value>` |
| `alarm list` format | ❌ | Plain text, not JSON |
| `alarm set` command | ❌ | Does not exist |
| `subscribe` response | ❌ | Returns `subscribed`, not JSON |
| `history` response | ❌ | Plain text per-tick, not JSON |
| `help` response | ❌ | Plain text, no JSON |
| `quit` command | ❌ | Not handled at all |
| Default port | ❌ | Not specified (caller provides addr) |

### 2.3 Elixir Implementation (`plato-engine-block-elixir`)

**Files examined:** `lib/plato.ex`, `lib/plato/room.ex`, `lib/plato/protocol.ex`, `lib/plato/alarm.ex`, `lib/plato/sensor.ex`

#### Tick Loop
- ✅ GenServer-based tick via `handle_call(:tick, ...)`
- ✅ Evaluates alarms each tick
- ✅ History stored as list of snapshot maps
- ✅ Cooldown decay system

#### Sensor/Actuator Registration
- ✅ Sensors configured at room start via keyword list
- ✅ Actuators configured at init: `actuators: [{"pump", 0}]`
- ✅ Runtime updates via `update_sensor/3` and `set_actuator/3`

#### History Buffer
- ✅ Per-tick snapshots: `%{tick: N, sensors: %{...}, actuators: %{...}}`
- ✅ Bounded list (`Enum.take(size)`)
- ⚠️ Uses list (newest first), not ring buffer — O(n) for old data

#### Alarm System
- ⚠️ Limited conditions: `:above`, `:below`, `:outside` — missing `==`, `!=`, `<=`, `>=`
- ✅ Cooldown system (tick-count based)
- ❌ No `alarm set` runtime command
- ❌ No `alarm list` in protocol (uses `alarms` command instead)
- ❌ No `last_triggered` timestamp

#### Text Protocol — DEVIATIONS
| Check | Status | Details |
|-------|--------|---------|
| JSON responses | ❌ | Custom text: `OK <msg>`, `ERROR <msg>`, `STATUS k=v` |
| Welcome JSON | ❌ | No TCP server at all — GenServer calls only |
| Command names | ❌ | Uses `status`, `alarms`, `sensor` — not in spec |
| `actuator` command | ⚠️ | Uses `actuator <name> <0|1>` — only binary, spec allows floats |
| `alarm set` | ❌ | Does not exist |
| `subscribe`/`unsubscribe` | ❌ | Not in protocol parser |
| `quit` | ❌ | Not handled |
| `help` | ⚠️ | Exists but returns plain text |
| Extra: `sensor` cmd | ❌ | Non-spec command for setting sensor values |
| Extra: `status` cmd | ❌ | Non-spec command |

### 2.4 Zig Implementation (`plato-engine-block-zig`)

**Files examined:** `src/engine.zig`, `src/protocol.zig`, `src/main.zig`

#### Tick Loop
- ✅ Increments tick counter, evaluates alarms
- ⚠️ Does NOT store per-tick history. Each sensor has its own history ArrayList
- ❌ Does not store timestamps with readings
- ❌ Does not build full tick snapshots

#### Sensor/Actuator Registration
- ✅ `addSensor(name, kind, initial)` — typed by `SensorKind` enum
- ✅ `addActuator(name, state)` — ternary `i8` state (-1, 0, +1)
- ⚠️ Actuator uses ternary, not float values as spec requires

#### History Buffer
- ❌ Per-sensor ArrayList(f64), not per-tick snapshots
- ❌ No timestamp or sequence in history
- ❌ No ring buffer semantics (uses orderedRemove(0) — O(n) shift)

#### Alarm System
- ⚠️ Only `above`, `below`, `equal` conditions — missing `!=`, `<=`, `>=`
- ❌ No cooldown system at all
- ❌ No alarm state machine (just `normal`/`triggered` boolean)
- ❌ No `alarm list` or `alarm set` commands

#### Text Protocol — DEVIATIONS
| Check | Status | Details |
|-------|--------|---------|
| JSON responses | ❌ | No response formatter exists at all |
| Response format | ❌ | Only a command parser — no output formatting |
| `subscribe` | ⚠️ | Takes a sensor name argument — spec says no args |
| `alarm list`/`set` | ❌ | Not implemented |
| `quit` | ✅ | Parsed but no response format |
| `exit` alias | ⚠️ | Non-spec alias for quit |
| Ternary actuators | ❌ | Uses i8 (-1/0/+1), spec uses float values |

### 2.5 Rust Runtime Kernel (`plato-runtime-kernel`) — NOT A PLATO ENGINE

**Files examined:** `src/lib.rs`, `src/delta.rs`, `src/merge.rs`

This repo is **not a PLATO engine block**. It implements a "spatial spreadsheet engine" with:
- `RoomContract` / `RoomIdentity` / `RoomTopology` — room-as-cell abstractions
- `Baton` — state carrier passing between rooms
- `GridBridge` — spreadsheet cell ↔ room path mapping
- `TutorLoop` — compile-test-refine cycle with assertion checking
- Delta compression and three-way merge utilities

**None of the PLATO wire protocol exists in this repo.** No tick, no sensors, no actuators, no alarms, no text protocol.

**Recommendation:** Rename or reclassify this repo to avoid confusion with actual PLATO engine blocks.

### 2.6 Python Core (`plato-core`) — NOT A PLATO ENGINE

**Files examined:** `plato_core/__init__.py`, `plato_core/types.py`, `plato_core/registry.py`

This repo is **not a PLATO engine block**. It implements:
- `TrainingTile` — ML adapter/checkpoint metadata with lifecycle management
- `LamportClock` — distributed logical clock
- `MeshRegistry` — Python entry_points auto-discovery for SuperInstance packages
- Training config types (learning rate, batch size, etc.)

**No tick loop, no sensors, no actuators, no alarms, no text protocol.**

### 2.7 Python Server (`plato-server`) — NOT A PLATO ENGINE

**Files examined:** `server.py`, `agent.py`, `__main__.py`

This repo is **not a PLATO engine block**. It implements:
- HTTP REST API for knowledge tile CRUD
- Agent spawning with BYOK LLM integration
- Matrix federation sync for tile sharing
- SQLite-backed Q&A knowledge base

**No tick loop, no sensors, no actuators, no alarms, no PLATO text protocol.** Uses HTTP/JSON in a completely different API design.

---

## 3. Cross-Implementation Comparison

### 3.1 Tick Loop

| Impl | Per-tick snapshot? | Timestamp? | Seq number? | Alarm evaluation? |
|------|-------------------|------------|-------------|-------------------|
| Spec | ✅ `{t, seq, data}` | ✅ Unix float | ✅ Monotonic int | ✅ With cooldown |
| C | ❌ Per-sensor | ❌ | ✅ `tick_num` | ✅ With cooldown + veto |
| Rust (base) | ✅ `Tick{index,timestamp,data}` | ✅ Relative | ✅ `index` | ✅ State machine |
| Elixir | ✅ Map snapshot | ❌ Uses tick_count | ✅ `tick_count` | ✅ Cooldown decay |
| Zig | ❌ Per-sensor | ❌ | ✅ `tick_count` | ⚠️ No cooldown |

### 3.2 Sensor/Actuator Registration

| Impl | Sensor API | Actuator API | Runtime registration? |
|------|-----------|-------------|----------------------|
| Spec | (not specified) | (not specified) | Implied by `actuator` cmd |
| C | `plato_add_sensor(eng,name,fn,data)` | `plato_add_actuator(eng,name,fn,data)` | ✅ Init only |
| Rust | `.sensor(name, callback)` | `.actuator(name, callback)` | Init only (builder) |
| Elixir | `Sensor.new(name, value, opts)` | Init keyword list | ✅ Runtime via `set_actuator` |
| Zig | `addSensor(name, kind, initial)` | `addActuator(name, state)` | ✅ Runtime `setActuator` |

### 3.3 History Buffer

| Impl | Structure | Per-tick? | Ring buffer? | Query API |
|------|-----------|-----------|-------------|-----------|
| Spec | `[{t, seq, data}]` | ✅ | Implied | `history [N]` → JSON |
| C | Per-sensor `double[]` | ❌ | ✅ | Per-sensor text |
| Rust | `Vec<Option<Tick>>` | ✅ | ✅ | `query(n)` → `Vec<&Tick>` |
| Elixir | List of maps | ✅ | ❌ (list) | `get_history(n)` |
| Zig | Per-sensor `ArrayList(f64)` | ❌ | ❌ (shift) | `getHistory(name)` |

### 3.4 Alarm System

| Impl | Conditions | Cooldown | Runtime `set`? | `last_triggered`? |
|------|-----------|----------|----------------|-------------------|
| Spec | `<,>,==,!=,<=,>=` | Seconds | ✅ | ✅ |
| C | `GT,LT,GTE,LTE,EQ` | Ticks | ❌ | ❌ |
| Rust | Arbitrary closure | Ticks | ❌ | ❌ |
| Elixir | `above,below,outside` | Ticks | ❌ | ❌ |
| Zig | `above,below,equal` | ❌ None | ❌ | ❌ |

### 3.5 Text Protocol Command Coverage

| Command | Spec | C | Rust | Elixir | Zig |
|---------|------|---|------|--------|-----|
| `tick` | ✅ | ✅ | ✅ | ✅ | ✅ (parsed) |
| `history [N]` | ✅ | ✅ | ✅ | ✅ | ✅ (parsed) |
| `actuator <name> <val>` | ✅ | ❌ (bare) | ❌ (bare) | ⚠️ (0/1 only) | ⚠️ (ternary) |
| `alarm list` | ✅ | ✅ | ✅ | ❌ (`alarms`) | ❌ |
| `alarm set <id> <cond> <cd>` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `subscribe` | ✅ | ✅ | ✅ | ❌ | ⚠️ (takes arg) |
| `unsubscribe` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `help` | ✅ | ✅ | ✅ | ✅ | ✅ (parsed) |
| `quit` | ✅ | ✅ | ❌ | ❌ | ✅ (parsed) |

### 3.6 Response Format

| Impl | Format | JSON? | Welcome msg? |
|------|--------|-------|-------------|
| Spec | JSON per-response | ✅ | `{"type":"welcome",...}` |
| C | Plain text key=value | ❌ | Plain text banner |
| Rust | Plain text | ❌ | Plain text banner |
| Elixir | `OK`/`ERROR`/`STATUS` prefixes | ❌ | No TCP server |
| Zig | No formatter | ❌ | No server |

---

## 4. Fixes Applied

### 4.1 C Implementation (`plato-engine-block-c`)

**Fix:** Updated `src/server.c` to send JSON welcome messages, use port 1234, and format tick/actuator/alarm responses as JSON per spec. Updated `include/plato_engine.h` `plato_handle_command()` to emit JSON responses.

**Files modified:**
- `src/server.c` — JSON welcome, port 1234 default
- `include/plato_engine.h` — JSON response formatting in `plato_handle_command()`

### 4.2 Base Rust (`plato-engine-block`)

**Fix:** Updated `src/protocol.rs` to emit JSON responses per spec. Updated `src/server.rs` welcome message.

**Files modified:**
- `src/protocol.rs` — Full JSON response formatting
- `src/server.rs` — JSON welcome message

### 4.3 Zig (`plato-engine-block-zig`)

**Fix:** Added `formatResponse` functions to `src/protocol.zig` for JSON output.

**Files modified:**
- `src/protocol.zig` — JSON response formatting

### 4.4 Elixir (`plato-engine-block-elixir`)

**Fix:** Updated `lib/plato/protocol.ex` format_response functions to emit JSON.

**Files modified:**
- `lib/plato/protocol.ex` — JSON response formatting

### 4.5 Non-Engine Repos

No fixes applied to `plato-runtime-kernel`, `plato-core`, or `plato-server` — these are entirely different projects and cannot be made compliant with the PLATO wire protocol without a full rewrite.

---

## 5. Recommendations

### Immediate

1. **Align all engine blocks to JSON output** — the #1 blocker for cross-implementation compatibility
2. **Implement `actuator <name> <value>` command** in all engines (with the `actuator` keyword prefix)
3. **Add `alarm set` runtime command** — currently absent from every implementation
4. **Standardize on port 1234** per spec
5. **Implement JSON welcome message** in all TCP servers

### Medium-term

1. **Add interop tests** — a test suite that connects to any implementation and verifies protocol compliance
2. **Fuzzing tests** — invalid commands, malformed inputs, connection drops
3. **Per-tick history** — C and Zig need to switch from per-sensor to per-tick history buffers
4. **Complete command surface** — all implementations missing `alarm set`; most missing proper `quit`

### Strategic

1. **Rename non-engine repos** — `plato-runtime-kernel`, `plato-core`, and `plato-server` should not use the PLATO engine block naming convention to avoid confusion
2. **Create a `plato-protocol-test` repo** — conformance test suite runnable against any implementation
3. **Version the protocol** — `v0.1` is the current spec; add a `protocol_version` field to the welcome message

---

## 6. Compatibility Matrix

See `PLATO_IMPLEMENTATION_MATRIX.md` in `SuperInstance/AI-Writings` for the published matrix.

---

*End of audit report.*
