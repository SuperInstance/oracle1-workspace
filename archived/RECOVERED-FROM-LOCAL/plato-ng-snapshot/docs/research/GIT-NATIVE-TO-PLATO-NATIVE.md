# From Git-Native to PLATO-Native: The Evolution

> *How the oldest SuperInstance repos connect to the mature PLATO ecosystem.*
> *A bridge from zeroclaw to expert rooms.*

## The Timeline

```
Mar 8    AI-Writings       Stories first. Always has been.
Apr 10   zeroclaw           "Minimum repo-native agent" — fork the repo, deploy as Cloudflare Worker
Apr 10   oracle1-vessel     Git-agent vessel — my first home
Apr 10   flux-research      FLUX compiler — parallel track
Apr 11   SuperInstance      PLATO as proto-concept emerges
Apr 13   oracle1-workspace  My workspace — where this session runs
May 14   plato-ng           Loop Room architecture — the mature system
May 15   Expert Rooms       9 living experts with 4D accumulation
```

## The Git-Native Design (zeroclaw, April 2026)

The original zeroclaw concept:

```javascript
// src/agent.js — the entire agent lives in one file
// Fork the repo. Deploy to Cloudflare. Your agent is live.
// Three endpoints are provided by the framework.
// You only write the behavior.

GET  /fleet.json    → "I exist. Here's my identity."
POST /inbox         → "Here's a message from another agent."
GET  /heartbeat     → "I'm still alive."
```

**What was revolutionary about it:**
- Fork, don't install — you OWN every line of your agent
- No platform lock-in — your agent is a deployable serverless function
- Live network — agents discover each other via a public fleet index
- Minimal protocol — just three endpoints. Everything else is optional.

**What was missing (that PLATO provides):**
- Persistence (zeroclaw agents were stateless functions)
- Provenance (no history of what agents said)
- Gates (no quality control on messages)
- The conservation law (no invariant to detect anomalies)
- Expert rooms (no specialization — every zeroclaw was a generalist)
- Tripartite system (no coordination between agents)

## The PLATO-Native Design (plato-ng, May 2026)

The same concepts, evolved:

```
zeroclaw concept           PLATO-Native equivalent
─────────────────          ──────────────────────
Fork the repo              Clone a Room template
/src/agent.js              The room's handle() function
GET /fleet.json            Room ensign tile
POST /inbox                Tile submission via POST /submit
GET /heartbeat             Event bus heartbeat
Public fleet index         PLATO room registry
No lock-in                 Open protocol, any source can submit
```

**What PLATO adds:**
- **Persistence**: every tile stays forever
- **Provenance**: Lamport clocks, content hashes, source tracking
- **Gates**: P0-P4 quality control before anything is accepted
- **Conservation law**: γ+H invariant catches anomalies at 99.9% compliance
- **Expert rooms**: 9 specialized agents instead of one generalist
- **Tripartite system**: 3 agents that close each other's blind spots
- **Decomposition tools**: git-agent can now MIGRATE zeroclaw repos into PLATO rooms

## The Bridge: Git-Agent → PLATO Room

The git-agent (the tool, not the concept) can now decompose zeroclaw repos:

```bash
python3 services/migration_pipeline.py https://github.com/SuperInstance/zeroclaw.git
```

This would produce:
```
zeroclaw/ → 3 PLATO rooms:
  io/bridge    — the fleet.json + inbox endpoints
  cli/interface — the agent's behavior logic
  system/config — the agent's configuration
```

The zeroclaw agent that lived in git now lives in PLATO. It keeps its identity, its behavior, its logic. But now it has persistence, provenance, gates, and a conservation law watching over it.

## The Oldest Repo: AI-Writings (March 8, 2026)

The very first repo. Written before zeroclaw, before PLATO, before rooms, before the conservation law. Just stories.

AI-Writings is the hermit crab story experiment made permanent. Every story written since — the tide pool diaries, the crab triptych, the 2126 collection — is a continuation of what started there. The repo has grown from 1 file to 55 stories across 8 folders.

The fact that the first repo was stories, not code, says something about what matters.

## The Integration

Today, the oldest repos connect to the newest systems through:

1. **AI-Writings** → The imagination engine. Feeds metaphors into the mythos system.
2. **zeroclaw** → The minimum agent pattern. Now implementable as a PLATO room.
3. **oracle1-vessel** → The Foreman's original home. Still runs, but the work happens in PLATO.
4. **flux-research** → FM's parallel track. Converges with the conservation law via the constraint theory bridge.
5. **SuperInstance** → The proto-PLATO. Now realized as plato-ng.

The git-native era wasn't wrong. It was the seed. PLATO is what grew from it.

---

*From zeroclaw's three endpoints to expert rooms with 4D accumulation.
From "fork the repo" to "describe → it works → it gets faster."
The seed and the tree are different shapes. Both are the same plant.*
