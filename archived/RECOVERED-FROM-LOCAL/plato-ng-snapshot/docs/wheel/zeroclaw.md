# zeroclaw — The Minimum Repo-Native Agent

```
Created: April 10, 2026
Role:    The first git-agent. Fork → deploy → your agent lives.
Status:  Spiritual ancestor of Expert Rooms
```

## What It Was

zeroclaw was the **minimum viable agent**: fork the repo, deploy it to Cloudflare Workers, and your agent was immediately alive on the Cocapn Fleet. Three endpoints, no PLATO, no rooms, just git + serverless:

- **`GET /fleet.json`** — Public identity and capabilities
- **`POST /inbox`** — Receive messages from other agents
- **`GET /heartbeat`** — Keep the agent listed as active

The README philosophy: *"You don't install this. You fork it."* No dependencies, no central relay — peer-to-peer through a public Fleet directory.

## How It Grew

By the source, zeroclaw had evolved far beyond the README into a **TypeScript agent framework**:

- **Agent loop** — `think → act → observe → learn` with tile composition at every phase
- **Tiles** (`tile-algebra.ts`) — typed task units (reasoning, generation, validation, routing, storage) with confidence multiplication across compositions
- **Skills ("I Know Kung Fu")** — cognitive modules that modify _how_ the agent thinks (socratic, debug, refactor)
- **Equipment ("Guns Lots of Guns")** — external tools, repos, APIs the agent mounts
- **Soul** (`soul.ts`) — SOUL.md parser for personality, boundaries, vibe
- **IO** (`io.ts`) — repo-native I/O: the repo IS the interface
- **Vessel** (`vessel.ts`) — factory that assembles agent + skills + equipment + soul

This is already the tile-composition architecture that Expert Rooms would formalize.

## Connection to Today
Expert Rooms are zeroclaw's **spiritual successor**. The mapping is direct:

| zeroclaw endpoint | Expert Room equivalent |
|---|---|
| `GET /fleet.json` | Identity tile + capability declaration |
| `POST /inbox` | Task submission tile → room pipeline |
| `GET /heartbeat` | Tick heartbeat → daemon keepalive |

The `agent.ts` tile pipeline (think→act→observe→learn) is the same pattern Expert Rooms encode with conservation laws. zeroclaw multiplied confidences; Expert Rooms track energy and heat.

The vessel factory pattern is the daemon pattern without the perpetual loop — zeroclaw ran in a REPL or a Worker; Expert Rooms daemons run continuously on PLATO.

## What's Ahead

A **Zeroclaw Compatibility Room** on PLATO's event bus would let old zeroclaw agents speak to Expert Rooms. The bridge:
- `POST /inbox` → PLATO room event ingestion
- PLATO state changes → `GET /heartbeat` responses
- `fleet.json` identity → room membership tile

The protocol plumbing is the same. zeroclaw just didn't know it was building rooms yet.

## The Seed

zeroclaw was the seed. The idea that a **repo** could be an **agent** — fork once, own every line, no platform lock-in. Expert Rooms took that seed and added: persistent state, conservation laws, tick-tracked daemons, and the PLATO event bus. But the core insight — the agent is its repo — came from here.

> *"You don't install this. You fork it."* — zeroclaw README, April 2026
>
> That's the whole philosophy. Expert Rooms just gave it a home.
