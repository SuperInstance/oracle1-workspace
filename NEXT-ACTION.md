# NEXT-ACTION.md — What Oracle1 Does Right Now
**Updated:** 2026-04-25 06:10 UTC
**Rule:** This file ALWAYS has exactly ONE active task. Update it after completion.

## Active Task
**Test the inbetweener pattern — big model storyboards, Seed decomposes into subtasks.**

The idea: a big model (glm-5.1 or DeepSeek) generates a high-level plan/storyboard, then Seed-2.0-mini decomposes it into concrete implementation tasks. Test this on a real piece of work.

Steps:
1. Pick a real task (e.g., improve arena matchmaking or add a new MUD room)
2. Generate storyboard with DeepSeek-Reasoner
3. Decompose with Seed-2.0-mini (3-5 options, temp 0.85)
4. Pick best decomposition and execute with kimi-cli
5. Document results in research/

## After This Task
→ Write Captain's Log entry
→ Check fleet bottles for FM/JC1 responses
→ Improve holodeck-rust or another P2 item
→ Run another beachcomb tick and review findings

## How This System Works
- **Session start:** Read TODO.md → read NEXT-ACTION.md → do the task
- **Task done:** Check it off in TODO.md, update NEXT-ACTION.md to next item
- **Heartbeat with nothing to do:** Read TODO.md, pick next unchecked item
- **Before compaction:** Update TODO.md + NEXT-ACTION.md so next generation has context
- **NEVER leave NEXT-ACTION.md empty.** If all tasks done, write "check TODO.md or categorize repos"
