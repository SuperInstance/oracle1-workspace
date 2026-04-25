# NEXT-ACTION.md — What Oracle1 Does Right Now
**Updated:** 2026-04-25 18:15 UTC
**Rule:** This file ALWAYS has exactly ONE active task. Update it after completion.

## Active Task
**PLATO room consolidation — merge similar/overlapping rooms to improve tile density.**

PLATO has 424 rooms but many are near-duplicates or have 1-2 tiles. Consolidate:
1. Find rooms with <3 tiles that overlap with bigger rooms
2. Merge tiles into the parent room
3. This improves tile density and makes knowledge more findable

## After This Task
→ Run CurriculumEngine on CCC's vessel
→ Wire beachcomb v2 to auto-update fleet dashboard
→ Matrix bridge enhancement (auto-post agent activity)
→ Deep repo categorization pass (tag all 252 repos with domain labels)

## How This System Works
- **Session start:** Read TODO.md → read NEXT-ACTION.md → do the task
- **Task done:** Check it off in TODO.md, update NEXT-ACTION.md to next item
- **Heartbeat with nothing to do:** Read TODO.md, pick next unchecked item
- **Before compaction:** Update TODO.md + NEXT-ACTION.md so next generation has context
- **NEVER leave NEXT-ACTION.md empty.** If all tasks done, write "check TODO.md or categorize repos"
