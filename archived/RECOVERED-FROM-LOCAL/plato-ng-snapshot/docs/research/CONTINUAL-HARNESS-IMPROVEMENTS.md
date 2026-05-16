# Design Improvement Ideas from Continual Harness + Related Work

## Paper: "Continual Harness: Online Adaptation for Self-Improving Foundation Agents"
Princeton / Google DeepMind / ARISE Foundation, May 2026

*Also cites our OpenClaw ecosystem as related work.*

## Key Concepts

The paper introduces a **reset-free framework** where an agent autonomously refines its own harness (system prompt, sub-agents, skills, memory) during a **single continuous episode** — no resets between improvements. The Refiner runs every F steps, reads trajectory data for failure signatures, and applies CRUD edits to the harness components.

This is exactly what our Loop Room architecture does, but formalized and named. Below are the specific design improvement ideas we should adopt.

---

## Improvement 1: The Refiner Room — A Third Loop Room Type

**Current state**: We have algorithmic rooms (deterministic loops) and agentic rooms (have a claw). Neither formalizes mid-episode harness editing.

**From the paper**: The Refiner is a separate component that runs on a schedule. Every F steps, it:
1. Reads recent trajectory tiles
2. Detects failure signatures (stuck in a loop, repeated failures, novel situation)
3. Applies CRUD edits to the harness (system prompt, sub-agents, skills, memory)
4. Continues without resetting

**Improvement**: Add a **Refiner Loop Room** type that sits alongside algorithmic and agentic rooms:

```
Room Types:
├── Algorithmic  — deterministic computation (no LLM)
├── Agentic      — has a claw, soul, memory (LLM-driven)
└── Refiner      — reads trajectory tiles, edits other rooms (meta-agent)
```

The Refiner is itself an agentic room, but its domain is **other rooms' configuration**. It reads trajectory tiles from the game room, detects "stuck" patterns, and writes new soul tiles, strategy tiles, or skill tiles back. The game room reads these tiles on its next loop iteration without restarting.

**Implementation sketch**:
```python
class RefinerRoom:
    """Reads trajectory tiles, detects failure, edits room configs mid-episode."""
    
    def tick(self):
        tiles = read_recent_trajectory(game_room, window=F)
        failures = detect_failure_signatures(tiles)
        
        if failures:
            for f in failures:
                edit = self.compose_edit(f)  # CRUD: create/read/update/delete
                self.apply_edit(game_room.config_room, edit)
                self.log_tile("refiner/edit", edit)
```

---

## Improvement 2: Formal Harness Components (p, G, K, M)

**Current state**: We have soul.md, agentic rooms, algorithmic rooms, evolved strategy tiles — but the components aren't standardized as a formal harness interface.

**From the paper**: A harness has exactly four components:
- **p**: System prompt / soul configuration
- **G**: Sub-agents (specialized modules invoked by the orchestrator)
- **K**: Skills (reusable routines — heuristics, executable programs)
- **M**: Memory (persistent knowledge store across the trajectory)

**Improvement**: Standardize every PLATO Loop Room's harness as `(p, G, K, M)`:

```
PLATO Room
├── p (soul.md)       — loaded from `soul/{room-name}.md` tile
├── G (agentic rooms) — registered as `rooms/{room-name}/subagents/` tiles
├── K (algorithmic)   — loaded from `rooms/{room-name}/skills/` tiles  
└── M (memory)        — stored in `rooms/{room-name}/memory/` tiles
```

The Refiner edits these tiles mid-episode. No restart needed — the room reads `p` from its soul tile on every loop iteration.

---

## Improvement 3: Process Reward Model Tiles

**Current state**: We log everything to PLATO but have no reward/score mechanism for trajectory quality.

**From the paper**: A Process Reward Model (PRM) scores each trajectory window. Low-reward windows trigger refinement. High-reward windows become training data.

**Improvement**: Add a `reward` field to tiles. Create a `loop/prm` room that scores trajectory tiles:

```
tile = {
    "domain": "research_log",
    "question": "ttt/tournament/game-42/move-12",
    "answer": {"player": "agg", "move": 4, "board": "...", "result": "win"},
    "reward": 1.0,       # ← NEW: scored by PRM room
    "tags": ["ttt", "move", "scored", "positive"],
    "source": "game-arena",
    "confidence": 0.95
}
```

The Refiner subscribes to low-reward tiles and triggers harness edits when the reward drops below threshold. The perpetual daemon subscribes to high-reward tiles and adds them to the training dataset.

---

## Improvement 4: Mid-Episode CRUD (Not Post-Game)

**Current state**: Our game analysis runs post-tournament (after 100 games). The paper says: update during play.

**From the paper**: "Unlike prompt-optimization methods that run complete episodes and reset between updates, Continual Harness updates mid-episode, so self-improvement continues without restarting."

**Improvement**: Add mid-episode refinement to the tic-tac-toe room. After every 10 games, the Refiner reads the last 10 game tiles and checks if the strategy is stuck:

```python
# Mid-tournament refinement
for gid in range(1, 101):
    play_game(...)                    # algorithmic
    if gid % 10 == 0:
        tiles = read_last_10_games()  # read trajectory
        if all_ties(tiles):           # detect failure: strategy is stuck
            strat = adjust_strategy() # CRUD edit: change the strategy
            log_tile("refiner/mid-tournament-adjustment", strat)
        # Continue the SAME tournament with new strategy
```

---

## Improvement 5: Harness Engineering Maturity (from related work)

**From harness engineering research**: "Externalize governance into a dedicated runtime layer — policy checking, capability admission, execution monitoring, rollback handling, human override."

**Improvement**: Add a governance room that sits above all game rooms:

```
gov/main (governance room)
├── Monitors all game rooms for policy violations
├── Can halt a room (read: stop tile flow)
├── Can rollback a room to a previous state tile
├── Human override: "stop game 42" → governance writes a halt tile
└── All governance actions are themselves PLATO tiles (auditable)
```

---

## Improvement 6: Skill-Aware Reflection (from EmbodiSkill)

**From EmbodiSkill**: "Skill-aware reflection and targeted revision — accumulate reusable procedural knowledge from trajectories."

**Improvement**: Add a `skills/` room that accumulates reusable routines. When the Refiner detects a repeated pattern (e.g., "aggressive always takes center at move 1"), it promotes the pattern to a skill tile:

```
skills/opening-center.json:
  {"pattern": "first_move_center", "condition": "game_start", "action": "take_square_4"}
```

The game room reads skill tiles before generating moves. The Refiner creates new skill tiles from trajectory analysis. Over time, the room accumulates skills without growing the prompt.

---

## Summary: What to Build Next

| Improvement | Effort | Impact | Priority |
|---|---|---|---|
| 1. Refiner Room type | Medium | High: enables mid-episode adaptation | P0 |
| 2. Formal harness (p, G, K, M) | Low | High: standardizes room interface | P0 |
| 3. PRM tiles (reward field) | Low | Medium: trajectory scoring | P1 |
| 4. Mid-episode CRUD | Medium | High: avoids restart between refinements | P0 |
| 5. Governance room | High | Medium: safety layer | P2 |
| 6. Skill accumulation | Medium | High: token efficiency | P1 |

The paper confirms our architecture direction. The improvements are all additive — they slot into the Loop Room pattern without changing what's already running.
