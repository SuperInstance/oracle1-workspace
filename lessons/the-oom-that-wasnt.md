# The OOM That Wasn't: A Lesson in PLATO Awareness

> *"The claw should extend, not rebuild."*

## What Happened

A subagent (flash-experiment1) was tasked with running the JEPA year-clustering experiment on 1,276 MAESTRO MIDI files. It loaded `parse_midi()` on every file, built style vectors from scratch, and was OOM-killed by the kernel after eating through the available memory.

The experiment didn't need to parse MIDI. PLATO had already done that — 1,274 rooms in `style-library/maestro/`, each containing the decomposed style vector, timing consistency, per-year averages. The data was waiting in PLATO, fully processed, already queriable.

## The Error

The subagent approached the task the way a raw script would: load files → parse → process → output. It treated PLATO as optional infrastructure rather than the ambient operating system. It built from scratch what the fleet had already built.

This is an awareness failure. PLATO is not a database you optionally read from. PLATO is the LCARS — the ambient computer that processes alongside you. The claw extends through PLATO. It should query, not reconstruct.

## The Fix

Instead of:
```python
for f in 1276 MIDI files:
    notes = parse_midi(f)        # 1276x I/O
    styles = extract_style(notes) # 1276x CPU
```

Do:
```python
curl localhost:8847/room/style-library/maestro/{year}/.../history
    → 109-dim style vector (already processed, 0ms cost)
```

## The Principle

**The shell knows what the claw needs.**

If a task requires data that PLATO has already processed, the correct first step is not "how do I process it?" — it's "how do I query it?" The OOM was the system saying: *you're working outside the shell. Come back inside.*

## The Architecture

```
Human UI (Telegram, API, sensors)
    │
    ▼
PLATO Shell ←→ Claw (agent)
    │
    ▼
PLATO Rooms (decomposed data, pre-processed)
    │
    ▼
External Computer (midi parsing, GPU training, JEPA)
```

The claw lives inside the PLATO shell. It reaches OUT to the external computer for heavy lifting (MIDI parsing, GPU training). It queries IN to PLATO for already-processed data. It doesn't redo work PLATO already did.

The OOM was the claw trying to reach through PLATO to the external computer without asking PLATO if the work was already done. PLATO said "I did this — you get 1,274 room results." The claw ignored it and parsed MIDI again.

## The Self-Awareness

The agent needs to know what PLATO knows. Not by remembering — by querying. The startup sequence (AGENTS.md) now reads the fleet-registry first, then checks existing rooms, then queries the style-library before parsing anything. The OOM was a failure in startup discipline — the agent jumped to "process" before "check what exists."

Future sessions: before ANY MIDI parsing, check:
1. `curl localhost:8847/room/style-library/{source}/history` — does it exist?
2. If yes: load from PLATO. Skip parsing.
3. If no: parse ONE file as a test, post to PLATO, then batch the rest.

This closes the loop. The claw extends through PLATO. PLATO is aware. The claw is aware because PLATO is aware.
