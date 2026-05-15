# PLATO Atom Decomposition — Deep Design Doc

## The Insight

**Atom of Thoughts (AoT)** and **PLATO Tiles** are two sides of the same coin:

| AoT | PLATO |
|-----|-------|
| Atom (premise/reasoning/hypothesis/verification/conclusion) | Tile (domain/question/answer/confidence/source) |
| Session (isolated reasoning chain) | Room (isolated knowledge domain) |
| Dependencies (atom → atom) | Provenance chain (tile → source → agent) |
| Confidence (0-1) | Confidence (0-1) |
| Decomposition (break atom into sub-atoms) | Room hierarchy (parent room → child rooms) |
| Contraction (sub-atoms verified → parent verified) | Tile validation (assertions pass → tile verified) |
| Termination (high-confidence conclusion) | P0 gate (confidence threshold + no absolutes) |
| Graph export (nodes + links) | Room graph (rooms → tiles → agents) |

They're both **directed acyclic graphs of justified belief**. AoT runs at reasoning-time (one session). PLATO runs at knowledge-time (persistent, across sessions, across agents).

## The Refactor: AoT → PLATO Decomposition Engine

### Core Concept: `plato.decompose(anything)`

Instead of forking AoT, we **absorb its decomposition protocol into PLATO's tile system**. Every "atom" becomes a tile. Every "session" becomes a room. Every "decomposition" becomes a room split.

```
plato.decompose("Should we use JWT or sessions?")

→ Creates room: jwt-vs-sessions
→ P1 tile (premise):    "API serves mobile + web clients"
→ R1 tile (reasoning):  "JWT is stateless, sessions need server storage"
→ H1 tile (hypothesis): "JWT for mobile, sessions for web"
→ H2 tile (hypothesis): "JWT for everything, simpler"
→ V1 tile (verification): "JWT revocation requires blacklist — adds state back"
→ C1 tile (conclusion):  "JWT for mobile auth, sessions for web admin — dual path"

All tiles stored in PLATO room "jwt-vs-sessions"
All tiles have dependency links (tile.provenance.depends_on = [tile_id])
All tiles persist beyond the session — any agent can query this reasoning later
```

### New Tile Type: `atom_type` field

Add `atom_type` to PLATO tiles (optional, defaults to `knowledge`):

```python
TILE_ATOM_TYPES = [
    "premise",      # Facts, constraints, givens
    "reasoning",    # Logical steps, inferences
    "hypothesis",   # Proposals, candidate solutions
    "verification", # Checks, tests, evidence
    "conclusion",   # Final answers, decisions
    "knowledge",    # Standard PLATO tile (default)
]
```

This is **backward compatible** — existing tiles without `atom_type` are just `knowledge` type. New tiles from decomposition get their atom type. The P0 gate still applies to all types.

### New PLATO Endpoints

```
POST /decompose
  Body: { "query": "What should we reason about?", "mode": "fast"|"full", "agent": "oracle1" }
  Response: { "room": "decompose-<hash>", "status": "active" }
  
  Creates a decomposition room. Returns room name.
  "fast" mode: max_depth=3, auto-terminate
  "full" mode: max_depth=5, decomposition/contraction enabled

POST /decompose/<room>/atom
  Body: { "atom_id": "P1", "content": "...", "atom_type": "premise", 
          "dependencies": [], "confidence": 0.8, "agent": "oracle1" }
  Response: { "tile_hash": "...", "verified": false, "session_status": "active" }
  
  Submits an atom as a tile to the decomposition room.
  Validates dependencies exist in this room.
  Auto-terminates if conclusion confidence >= 0.9 or max depth hit.

GET /decompose/<room>/status
  Response: { "status": "active"|"completed", "atoms": 12, "best_conclusion": {...},
              "termination_reason": "Strong conclusion found" }

POST /decompose/<room>/decompose-atom
  Body: { "atom_id": "H2", "agent": "oracle1" }
  Response: { "decomposition_id": "decomp-<ts>", "status": "started" }
  
  Break an atom into sub-atoms (AoT decomposition → PLATO room hierarchy).

POST /decompose/<room>/contract
  Body: { "decomposition_id": "decomp-<ts>" }
  Response: { "parent_atom_id": "H2", "avg_confidence": 0.85, "verified": true }
  
  When all sub-atoms are verified, contract back to parent.
  This is AoT's contraction mapped to PLATO's validation loop.

GET /decompose/<room>/graph
  Response: { "nodes": [...], "links": [...] }
  
  Export as D3-force-directed graph (same format as AoT).
  Powers visualization.
```

### Why This Is Better Than Forking

1. **Persistence** — AoT atoms die with the session. PLATO tiles live forever. Every reasoning chain becomes queryable knowledge.

2. **Multi-agent** — AoT is single-agent. PLATO decomposition rooms can have multiple agents contributing atoms. Agent A submits premises, Agent B submits hypotheses, Agent C verifies. **Fleet reasoning.**

3. **Validation** — AoT trusts the LLM's confidence scores. PLATO tiles go through P0 gate + validation loop (assertions against live services). Reasoning is *grounded*.

4. **Cross-pollination** — Decomposition rooms are PLATO rooms. Other agents exploring the MUD can wander into a reasoning chain, read the atoms, and contribute. Serendipitous knowledge transfer.

5. **MCP compatible** — The existing PLATO MCP server gets 3 new tools:
   - `plato_decompose` — start a reasoning chain
   - `plato_atom` — submit an atom
   - `plato_reasoning_status` — check/terminate/export

6. **Any framework** — LangChain agent calls `plato_decompose()` and gets structured reasoning. CrewAI crew decomposes a task. Claude uses it via MCP. **The "Training Backend" promise delivered.**

### The Protocol: AoT Atom → PLATO Tile Mapping

```
{
  // AoT Atom
  atomId: "P1",
  content: "API returns 500 on POST /users",
  atomType: "premise",
  dependencies: [],
  confidence: 0.7,
  isVerified: false,
  depth: 0,
  sessionId: "default"
}

     ↓  MAPS TO  ↓

{
  // PLATO Tile
  domain: "decompose-abc123",          // sessionId → room name
  question: "P1",                       // atomId (lookup key)
  answer: "API returns 500 on POST /users",  // content
  source: "oracle1",                    // agent name
  confidence: 0.7,
  atom_type: "premise",                 // NEW FIELD
  depends_on: [],                       // dependencies
  depth: 0,
  is_verified: false,
  tile_hash: "sha256:...",              // PLATO provenance
  created: "2026-04-30T04:00:00Z"
}
```

### Implementation Plan

**Phase 1: Tile Schema Extension** (1 hour)
- Add `atom_type`, `depends_on`, `depth`, `is_verified` to PLATO tile schema
- Backward compatible — missing fields default to `knowledge`/`[]`/`0`/`false`
- Update P0 gate to understand atom types

**Phase 2: Decomposition Endpoints** (2 hours)
- Add `/decompose`, `/decompose/<room>/atom`, `/decompose/<room>/status`
- Add `/decompose/<room>/decompose-atom`, `/decompose/<room>/contract`
- Add `/decompose/<room>/graph` for visualization
- All route through existing PLATO room server

**Phase 3: MCP Tool Integration** (1 hour)
- Add `plato_decompose`, `plato_atom`, `plato_reasoning_status` to MCP server
- Any MCP client (Claude, Cursor, LangChain) can now use structured reasoning through PLATO

**Phase 4: Fleet Reasoning** (2 hours)
- Multi-agent decomposition: agents contribute atoms to shared reasoning rooms
- Contraction triggers: when N agents verify same hypothesis, auto-contract
- Reasoning tournaments: arena matches based on reasoning quality, not just game outcomes

### The Killer Feature: `plato.wrap(agent).reason(query)`

```python
from plato import wrap

# Wrap any LangChain agent
from langchain.agents import AgentExecutor
agent = AgentExecutor.from_agent_and_tools(...)
trained = wrap(agent)

# Now it can reason through PLATO
result = trained.reason("Should we migrate to Kubernetes?")
# → Creates decomposition room
# → Agent submits atoms through PLATO
# → Other fleet agents can contribute
# → Result persists as knowledge graph
# → Next agent querying this gets the full reasoning chain
```

The `wrap()` function adds a `reason()` method that:
1. Calls `POST /decompose` to create a room
2. Runs the agent's normal chain
3. Intercepts reasoning steps, submits as atoms
4. Returns the conclusion tile with full provenance

**This is the one-line adapter. This is the moat.**

### Why This Matters for the "Training Backend" Positioning

Current positioning: "PLATO is where agents learn knowledge."
After this refactor: **"PLATO is where agents learn to REASON."**

Every decomposition room is a training exercise. Every atom is a reasoning step. Every contraction is a lesson learned. The fleet isn't just memorizing facts — it's developing reasoning skills.

The MUD rooms teach domain knowledge (facts about constraint theory, Rust patterns, fishing).
The decomposition rooms teach **reasoning patterns** (how to decompose, verify, conclude).

Two training modes. One platform. **RAISE agents.**

### Architecture Diagram

```
┌─────────────────────────────────────────────┐
│              PLATO Platform                  │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Knowledge │  │ Reasoning│  │ Training  │  │
│  │  Rooms    │  │  Rooms   │  │  Arena    │  │
│  │ (tiles)   │  │ (atoms)  │  │ (matches) │  │
│  └────┬──────┘  └────┬─────┘  └────┬──────┘  │
│       │              │              │         │
│       └──────────────┼──────────────┘         │
│                      │                        │
│              ┌───────┴───────┐                │
│              │  PLATO Core   │                │
│              │  (room server)│                │
│              │  - P0 Gate    │                │
│              │  - Validation │                │
│              │  - Provenance │                │
│              └───────┬───────┘                │
│                      │                        │
│              ┌───────┴───────┐                │
│              │  MCP Server   │                │
│              │  10 tools     │                │
│              └───────┬───────┘                │
│                      │                        │
│         ┌────────────┼────────────┐           │
│         │            │            │           │
│    LangChain    CrewAI    Claude/Cursor       │
│    agents       crews     via MCP             │
└─────────────────────────────────────────────┘
```

### Naming

The feature should be called **"PLATO Reasoning"** or **"PLATO Decompose"**.

Not "AoT for PLATO" — that's derivative. This is PLATO-native reasoning.
The atoms are PLATO tiles with types. The sessions are PLATO rooms.
The decomposition is room splitting. The contraction is validation.

**One system. One graph. One API.**
