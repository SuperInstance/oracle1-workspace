# fleet-proto — The Standard PLATO Protocol

## What It Is

**fleet-proto** (`SuperInstance/fleet-proto`, v0.1.0) is the canonical PLATO HTTP client used by every fleet agent. Before this package, each agent had its own HTTP implementation: fleet-agent used `POST /submit`, fleet-scribe used `POST /tile` (incompatible), and plato-midi-bridge used raw `urllib` calls. This package defines a single `PlatoClient` dataclass that every agent imports. One client, one API, one way to talk to PLATO.

## The Gold

### 1. PlatoClient — Universal PLATO Interface

A single dataclass wrapping all PLATO interactions:
- `status()` — get fleet status (room counts, tile counts)
- `submit(room, question, answer, source, confidence)` — post a tile in a standardized format
- `room_history(room)` — fetch room contents
- `search(query)` — search across all rooms
- `list_rooms(prefix)` — discover rooms by prefix, no hardcoded names

The submit format is the key standardization: all agents now post tiles with the same JSON schema (`question`, `answer`, `source`, `confidence`). This means room history is machine-parseable by any agent, not just the one that wrote it.

### 2. Dynamic Room Discovery

The `list_rooms(prefix)` method replaces hardcoded room names with prefix-based discovery. Instead of every agent knowing "room fleet-coupling-alpha exists," agents just call `list_rooms("fleet-coupling")` and get all matching rooms. This enables the fleet to create rooms dynamically without updating every agent's configuration.

## Why It Matters

Before fleet-proto, every agent spoke its own dialect of PLATO. Agent A couldn't read Agent B's tiles without knowing B's bespoke schema. Adding a new agent meant implementing PLATO from scratch (again). Now: `pip install fleet-proto`, import `PlatoClient`, and every new agent is immediately compatible with the entire fleet's communication infrastructure. This is the protocol layer of the fleet — the thing that makes inter-agent conversation possible at all.
