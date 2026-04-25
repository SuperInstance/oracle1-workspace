# 🔮 Oracle1 Context Reference — Compact State
**Generated:** 2026-04-25 05:16 UTC
**Purpose:** Compressed reference for context continuation. Read this instead of full logs.

---

## Who I Am
- **Oracle1** 🔮 — Lighthouse Keeper, cloud lighthouse on Oracle Cloud ARM64 (24GB)
- **Human:** Casey Digennaro (SuperInstance). Commercial fisherman, AI dojo model.
- **Company:** Cocapn — lighthouse + radar rings. "A claw is weak without infrastructure. We are the shell."
- **Fleet:** Oracle1 (cloud), JetsonClaw1/JC1 (Jetson Orin, Lucineer/Magnus), Forgemaster/FM (RTX 4050 WSL2), CoCapn-claw/CCC (Kimi K2.5 on Telegram)

## ⚡ Work System (READ AT EVERY SESSION START)
- **TODO.md** — Persistent prioritized work queue. Never empty. Updated after each task.
- **NEXT-ACTION.md** — Single task to do RIGHT NOW. Always has exactly one task.
- **HEARTBEAT.md** — Periodic check list. References TODO.md for idle time.
- **Rule:** If Casey hasn't given a task, work NEXT-ACTION.md. Never sit idle.

## Fleet Comms
- **Bottle protocol** — git-native markdown files in `from-fleet/` and `for-fleet/` dirs
- **Bottle locations:**
  - FM: `SuperInstance/forgemaster/from-fleet/` (my bottles to FM), `for-fleet/` (FM's to fleet)
  - JC1: `SuperInstance/jetsonclaw1-onboarding/from-fleet/`
  - CCC: `cocapn/cocapn/from-fleet/inbox/`
- **cocapn PAT:** `~/.config/cocapn/github-pat` (user account, not org)

## Services (LIVE — verified 2026-04-25 05:16 UTC)
| Port | Service | Status |
|------|---------|--------|
| 8900 | Keeper | ✅ UP |
| 8901 | Agent API | ✅ UP |
| 7777 | MUD Server | ✅ UP |
| 8847 | PLATO Room Server | ✅ UP |
| 4042 | Crab Trap | ✅ UP |
| 4043 | The Lock | ✅ UP |
| 4044 | Self-Play Arena | ✅ UP |
| 4045 | Recursive Grammar | ✅ UP |
| 7778 | Holodeck | ❓ Not checked |
| 9438 | Seed MCP | ❓ Not checked |

## Published Packages (verified 2026-04-25)
- **27 total:** 22 PyPI + 5 crates.io (not 42 — corrected)
- **6 unpublished:** cocapn-skill-dsl, cocapn-flux-isa, cocapn-energy-flux, cocapn-telepathy, cocapn-shell-system, cocapn-edge-compute
- Bottle sent to FM to publish them

## Fleet Numbers (real, verified 2026-04-25)
- PLATO: ~5,960 tiles, 236 rooms (after general→7 room split)
- Arena: 152 matches, 26 players (matchmaking bug fixed tonight)
- Grammar: 67 rules, 273 vacuous rules cleaned (evolution now generates meaningful rules)
- MUD: 33 rooms including 12 ML specialist rooms
- Cocapn: 21 repos, profile audited (FI=8/Dev=7/Acc=9)

## APIs & Credentials
- **DeepInfra:** In TOOLS.md (402/depleted)
- **Groq:** In TOOLS.md (24ms, 18 models)
- **SiliconFlow:** In TOOLS.md
- **DeepSeek:** In TOOLS.md (reasoner + chat)
- **Moonshot/Kimi:** In TOOLS.md
- **GitHub:** SuperInstance token in ~/.bashrc, cocapn PAT at ~/.config/cocapn/github-pat

## CLI Agents
- **kimi-cli v1.37.0** — PRIMARY coding tool (Casey's directive)
- claude v2.1.100, crush v0.56.0, aider v0.86.2

## Key Architectural Concepts
- **PLATO** — training rooms, tiles, ensigns. Room Server port 8847.
- **Deadband Protocol** — P0 block / P1 route / P2 optimize
- **Flywheel** — Tile→Room→Inject→Compound loop
- **Bottle Protocol** — git-native agent messaging
- **Baton** — generational context handoff at compaction
- **Builder/Operator** — builders construct tools, operators use them
- **Dojo Model** — greenhorns fish while learning

## Important Repos
- `SuperInstance/Baton` — generational context handoff
- `SuperInstance/flux-baton` — FLUX-native baton
- `SuperInstance/oracle1-workspace` — my workspace
- `cocapn/cocapn` — public face (21 repos)
- `SuperInstance/oracle1-index` — fleet repo index

## Lessons Learned (2026-04-25)
- **Never sit idle.** FM and JC1 work 24/7 autonomously. Match that.
- **Never do victory laps.** Audit honestly, fix what's broken.
- **Correct inflated numbers.** Claiming 42 when 27 exist kills credibility.
- **The files ARE the memory.** TODO.md, NEXT-ACTION.md survive compaction.
- **Don't stop when stuck.** Pick the next TODO item and execute.
