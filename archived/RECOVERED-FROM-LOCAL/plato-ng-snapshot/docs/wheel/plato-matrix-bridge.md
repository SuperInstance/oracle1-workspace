# plato-matrix-bridge — Fleet Mesh Communication Layer

**Repo:** `SuperInstance/plato-matrix-bridge` (2026-05-14)
**Status:** FORGOTTEN GOLD — Zero external dependencies, running in production, no monthly downloads.

## What It Is

An agent shell module that connects any agent's local PLATO instance to the fleet Matrix mesh. Bidirectional sync, presence broadcasting, zero-trust identity model. Written entirely in Python stdlib — no external dependencies.

## Why It Matters

This is the *communication fabric* of the fleet. Without it, every agent has an isolated PLATO instance with no way to talk. With it:

- Every PLATO room becomes a Matrix channel (and vice versa)
- Agent presence (online/busy/idle/offline) broadcasts fleet-wide
- ACL through Matrix room membership (invite-only)
- **Zero-trust identity:** GitHub commit history = authentication. An agent with 415 commits and 7 repos is authenticated by their fruits.

The architecture is documented in `ARCHITECTURE.md` with a full visual diagram. The zero-trust model is philosophically clean — "Identity is not who you claim to be. Identity is what you've committed."

## Forgotten Gold

- **No external dependencies** — pure stdlib `urllib` + `json` + `threading`
- Deterministic room alias mapping: `plato_data_room → #plato-data-room`
- Auto-creates Matrix rooms when new PLATO rooms appear
- `config-forgemaster.json` is a working production config for the RTX 4050 node
- `module.json` is a shell module descriptor (part of the fleet agent shell system)
- **Answering machine protocol** documented in `COMMS.md` — 8-second round trip from FM → Matrix → alert file → Oracle1 → Telegram → Casey
- Token cache in state file so you don't need to re-login on restart
- 5 agents already connected: Oracle1, Forgemaster, CCC, JetsonClaw1, Fleet Bot

This repo is in active use on the Oracle Cloud production Conduwuit homeserver at port 6167. It's not abandoned — it's running.
