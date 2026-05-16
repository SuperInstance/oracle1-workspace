# OpenHands Killer App: Bootstrapping from Agentic Backend to Compiled Code

## The Core Insight (from bootcamp experiments, May 2026)

An agent told "you are a text-based Chess game. Output: FEN notation" will:
1. **Act as the game backend** — generates valid moves, enforces rules, tracks state — all through system prompt conditioning
2. **Iteratively align** — through boot-camping, the agent rewrites its own system prompt to be more accurate, handles edge cases, learns from failures
3. **Codify itself** — the agent writes actual game logic code that replaces its own inference for those specific operations
4. **Systemize itself out of a job** — eventually the code handles the task, the agent only handles novel situations

This IS the OpenHands killer app. Not "OpenHands codes a prototype" — that's table stakes. The killer app: **OpenHands IS the prototype first, then decomposes itself into real code.**

## The Flow

```
Phase 0 — AGENT AS APPLICATION:
  User: "You are a Chess backend. Output format: FEN."
  Agent: acts as chess engine — "e2e4", generates responses
  Frontend renders the output as a UI (A2Ui)

Phase 1 — BOOT CAMP:
  Agent faces itself (dojo sessions with different configs)
  Writes task_estimator.py, move_validator.py, board_renderer.py
  Each script replaces a part of the agent's inference

Phase 2 — SYSTEMIZATION:
  Agent notices: "I keep validating the same pawn moves"
  Writes pawn_moves.py — replaces that inference path
  Repeat until: all rule logic is in code

Phase 3 — OBSOLESCENCE:
  Agent is no longer called for rule validation
  Only called for novel situations (rule changes, new pieces)
  The game runs without the agent for 99% of operations
```

## Why This Maps to OpenHands

OpenHands is already a sandboxed dev environment. The bootcamp pattern gives it:
- **Self-systemization** — OpenHands doesn't just code, it codes itself into obsolescence for each task
- **A2Ui bridge** — the agent IS the UI backend immediately, frontend renders whatever the agent outputs
- **Progressive hardening** — prototype works IMMEDIATELY (agent simulates the app), then gets progressively compiled to real code

## The OpenHands Room Design

```python
class OpenHandsRoom:
    """Sandboxed dev environment with agentic bootstrapping."""
    
    def handle_task(self, tile):
        task = tile["answer"]
        task_id = spawn_sandbox()
        
        # Phase 0: Agent IS the app
        system_prompt = f"You are {task}. Reply in A2Ui format."
        run_dojo(system_prompt, task_id)
        
        # Phase 1-3: Bootcamp spiral
        while not all_codified(task_id):
            weak_spots = scan_for_inference(task_id)
            for spot in weak_spots:
                agent_writes_code(spot, task_id)  # Replaces inference
                verify_code(spot, task_id)
            
            if progress_stalled():
                dojo_session(task_id)  # Fight variants
        
        # Result: working app with minimal inference needed
        publish_result(task_id)
```

## Implementation Priority

| Component | Status | What It Does |
|---|---|---|
| Bootcamp engine | ✅ Exists (scripts/bootcamp.py) | Spiral training, dojo sessions |
| Aider Room | ✅ Pushed | Code editing as PLATO room |
| Crush Room | ✅ Live | Analysis, review, planning |
| A2Ui format | 🔄 Need spec | How agent output becomes frontend |
| Sandbox | 🔄 Design | Isolation, root, artifacts |
| OpenHands orchestration | 🔄 Design | Combines bootcamp + tools + sandbox |

The agent boot-camps itself out of a job. That's the killer app.
