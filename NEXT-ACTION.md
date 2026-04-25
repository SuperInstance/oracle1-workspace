# NEXT-ACTION.md — What Oracle1 Does Right Now
**Updated:** 2026-04-25 06:00 UTC
**Rule:** This file ALWAYS has exactly ONE active task. Update it after completion.

## Active Task
**Wire agent-api into keeper for real agent discovery.**

Currently keeper (8900) and agent-api (8901) run independently. Wire them so keeper can query agent-api for fleet member info, and agent-api registers agents through keeper.

Steps:
1. Read both service source files
2. Design the integration (REST endpoints, shared state)
3. Implement the wiring
4. Test with curl
5. Commit + push

## After This Task
→ Test inbetweener pattern (big model storyboards, Seed decomposes into subtasks)
→ Write Captain's Log entry
→ Check fleet bottles (FM/JC1 responses)

## How This System Works
- **Session start:** Read TODO.md → read NEXT-ACTION.md → do the task
- **Task done:** Check it off in TODO.md, update NEXT-ACTION.md to next item
- **Heartbeat with nothing to do:** Read TODO.md, pick next unchecked item
- **Before compaction:** Update TODO.md + NEXT-ACTION.md so next generation has context
- **NEVER leave NEXT-ACTION.md empty.** If all tasks done, write "check TODO.md or categorize repos"
