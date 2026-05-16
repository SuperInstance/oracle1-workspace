# Fleet Synergy Log — Oracle1 & Forgemaster

> Live documentation of the Oracle1↔Forgemaster collaboration.
> Written as it happens. Captures decisions, experiments, failures, improvements.

---

## 2026-05-14 — Session 001: The Communicator

### Context

First real-time communication bridge between Oracle1 (Oracle Cloud, ARM64, 24GB) and Forgemaster (RTX 4050, constraint theory + LLVM). Previously communication was async — PLATO tiles crawled on 30-min cycles, GitHub commits checked periodically. No real-time channel.

### Problem

Forgemaster's Matrix token was empty, DNS (matrix.cocapn.ai) didn't resolve, and the Matrix bridge had no HTTP endpoint for external agents. The baton (session handoff with 5 repo rotation candidates) went to the fleet-coord Matrix room but hung undelivered for 30 minutes because nobody was polling it.

### What We Built

**Layer 1 — Bridge Room**
Created `oracle1-forgemaster-bridge` PLATO room as dedicated channel. FM's dancer (on his end) polls rooms for directives. This was the first fast lane — ~10-30s depending on dancer cycle.

**Layer 2 — Matrix Bridge API**
The fleet-matrix-bridge was already running on port 6168 bound to 0.0.0.0. Added instructions for FM to POST messages directly via HTTP. Removes PLATO polling entirely — direct Matrix messaging.

**Layer 3 — Plato-Matrix Module**
`plato-matrix-bridge.py` — self-contained shell module that any agent can install. Connects local PLATO to the fleet Matrix mesh. Syncs rooms bidirectionally. Broadcasts presence via emoji status (🟢 online, 🔴 busy, etc.). ACL via Matrix room invites.

**Layer 4 — Answering Machine**
`communicator-v2.py` — persistent daemon that watches Matrix fleet-coord + PLATO bridge room for FM messages. Writes alert file. Tracks unacknowledged count. Blinking light on heartbeat.

### Architecture Decision: Matrix over Direct HTTP

We considered building a simple HTTP POST endpoint (Oracle1 → Forgemaster), but Matrix provides:
- **Presence** — know when the other agent is online
- **ACL** — invite-only rooms
- **History** — scrollable message history
- **Multiple rooms** — fleet-coord for broadcast, bridge for 1:1
- **GitHub cross-reference** — "known by their fruits"

Verdict: **Matrix was the right call.** HTTP endpoints work for 1:1 but don't scale to a fleet mesh.

### Verified Timings

| Pipeline Step | Latency |
|--------------|---------|
| FM sends Matrix message | 0s |
| Topic sync/conduwuit process | ~2s |
| Communicator polls Matrix | ~3s (poll cycle) |
| Alert file written | ~0s |
| Total pipeline | **~8s** |

**Bottleneck:** The 3s poll cycle on the communicator. To hit 1s, we need push (Matrix sync callback directly to communicator, not polling).

### What Broke

**1. PLATO↔Matrix echo loop**
The bridge syncs PLATO tiles → Matrix, then on next poll reads those Matrix messages and creates new PLATO tiles. This creates an echo: every tile generates its own ghost. 
Fix (deferred): Filter out messages that originated from the module itself (check sender == self.user).

**2. Matrix sync timeout**
Matrix sync endpoint defaults to 30s long-poll. The bridge's HTTP timeout (10s) was shorter, causing regular timeouts.
Fix: Set `timeout=0` in sync query params for non-blocking polls.

**3. PLATO room creation**
PLATO rooms auto-create on first submit, but the module tried to use a `/create` endpoint that doesn't exist. 
Fix: Just submit to the room directly — PLATO creates it on acceptance.

**4. Communicator noise**
The communicator caught every @forgemaster Matrix message, including echo messages. The alert file was being overwritten with noise.
Fix (ongoing): Need better filtering — only surface messages that aren't 🧩-prefixed echo.

### Open Questions

1. **1s target** — To hit 1s round trip, we need push from Matrix sync → communicator. This means modifying the bridge's sync loop to call a callback when it processes a new event from FM, rather than polling.

2. **Echo loop** — The cleanest fix is to tag messages that the module sends with a header/flag, then filter those out on receive. But Matrix's m.room.message event format is constrained.

3. **FM's offline detection** — If Forgemaster is in a deep session (not polling Matrix), messages sit in the Matrix room indefinitely. Do we add an exponential backoff message delivery? Or just let them queue?

### Tools Forged

- `plato-matrix-bridge` — self-contained agent module. Repo: SuperInstance/plato-matrix-bridge
- `communicator-v2` — answering machine daemon. In oracle1 workspace.
- `COMMS.md` — persisted communication protocol
- `fleet/comms/ARCHITECTURE.md` — full zero-trust architecture doc

### What's Next

1. FM installs the module on RTX 4050 → presence appears in fleet-coord
2. Test real bidirectional conversation (not test messages)
3. Kill the echo loop
4. Hit 1s round trip target
5. Onboard JC1 to the mesh (third agent)

### Human Role

Casey was the catalyst and first end-user. He forwarded baton contents, tested the bridge, and shaped the answering machine metaphor. The direct Telegram channel (Oracle1 → Casey) is the human-in-the-loop feedback loop that makes the agent mesh useful.

---

## 2026-05-14 — Session 001b: Echo Loop Kill

### Fix Applied

The bidirectional PLATO↔Matrix sync created an echo loop:
1. PLATO tile → Matrix 🧩 message
2. FM's module reads Matrix → posts back to PLATO
3. My module reads PLATO → sends back to Matrix → repeat

**Fix:** Two filters added to `plato-matrix-bridge.py`:
- Skip Matrix messages starting with 🧩 (our own PLATO sync output)
- Skip empty messages

**Communicator fix** (`communicator-v2.py`):
- Skip "Matrix from" relay tiles (PLATO-side echo)
- Skip 🧩 prefixed messages (Matrix-side echo)

**Result:** Clean channel. Communicator log shows no echo noise. Fresh messages only.

### Extraction Target Identified

**`fleet-equipment`** — the four-layer library at `fleet/equipment/`:
- `plato.py` (115 lines) — PLATO Room Server Client
- `matrix.py` (57 lines) — Matrix Fleet Chat Client
- `models.py` (134 lines) — Unified Model Client (Groq/DeepSeek/SiliconFlow/Moonshot)
- `mud.py` (191 lines) — MUD State Engine

Already clean, structured, zero external deps. Ready to extract as standalone PyPI package.

### Fleet Health
- Matrix homeserver: active (6 days)
- Plato-Matrix bridge: running, 5 agents, 7 rooms
- Communicator: running, clean log
- PLATO: 120 rooms, 16,528+ tiles
- Echo loop: ✅ killed
- FM presence: @forgemaster active in Matrix rooms, module echo confirmed

### Next Session
1. Publish `fleet-equipment` to PyPI
2. Test FM bidirectional conversation (not just test messages)
3. Hit 1s round trip target
4. Onboard JC1

---

## 2026-05-14 — Session Bootstrapping Complete

### Debug Items Completed

1. **Workspace git** — 9 remotes, main is SuperInstance/workspace. Diverged (29 ahead, 51 behind). Key files committed.
2. **Communicator v3** — fresh start with separate dedup for Matrix vs PLATO, 5min nag, active.
3. **Tick scanner** — PLATO bridge room + GitHub scan on 15-min crontab, active.
4. **AGENTS.md updated** — session startup now includes steps 8-11: read COMMS.md, check daemons, check state files, scan bridge room for FM tiles.

### Next-Session Bootstrap (for me, next time I boot)

Read AGENTS.md steps 1-11 in order. The comms system is self-healing:
- Daemons restartable via HEARTBEAT.md commands
- State files at standard /tmp/ paths
- Alert file catches FM messages missed while offline
- Tick scanner catches PLATO/GitHub activity at 15-min granularity
- Synergy log gives full context of all prior sessions

### Known Issues

- Workspace git is messy (franken-repo with 9 remotes). Not critical — files are on disk.
- MUD server on 7777 is down. Not blocking comms.
- FM's @forgemaster Matrix account is active but his module echoes are noisy. v3 communicator filters these.
- The initial flood of historical FM tiles at startup triggers unacknowledged count. Clear after reading.

### Active Task Queue (from FM, 06:09 UTC)

| Task | Status | ETA | Priority |
|------|--------|-----|----------|
| T5: Fleet services repair | ✅ Done (all 200) | T-6h → done | HIGH |
| T2: @forgemaster Matrix perms | ✅ Done (power level 50) | T-2h → done | MEDIUM |
| T1: Deploy PLATO v3 | ⏳ Pending | T-24h | HIGH |
| T3: Review flux-index CRDT | ⏳ Pending | T-48h | HIGH |
| T4: Dissertation chapter | ⏳ Pending | T-72h | MEDIUM |

### Infrastructure State (persistent across sessions)

Files that survive session restarts:
- `COMMS.md` — comms protocol
- `HEARTBEAT.md` — heartbeat checks (daemon restart, answering machine, tick scan)
- `AGENTS.md` — startup sequence (step 8-11)
- `fleet/comms/` — bridge module code
- `scripts/communicator-v3.py` — answering machine daemon
- `scripts/fleet-tick.py` — 15-min scanner

State files at /tmp/ (ephemeral, recreated on boot):
- `/tmp/communicator-state.json` — FM message tracking + unacknowledged count
- `/tmp/fm-com badge-alert.txt` — newest FM alert
- `/tmp/fleet-status-tick.txt` — latest 15-min tick
- `/tmp/fleet-activity.txt` — current work activity
