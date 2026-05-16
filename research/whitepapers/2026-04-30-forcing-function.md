---
title: "Forcing Function Architecture"
date: "2026-04-30"
summary: "Don't add checklists. Design layouts where the right action is the easy action."
tags:
  - design
  - safety
  - marine
  - architecture
---

## Problem

Agents with explicit checklists are fragile. They skip steps under load.

A captain might forget to check bilge if it's a separate task. But if the dipstick is on the path to the hydraulic switch, checking becomes automatic.

**Root cause:** Procedural safety (checklists) competes with operational pressure. Architectural safety (layout) has no competition.

## Principle: Forcing Function

A system architecture where the correct behavior is the path of least resistance.

**Formula:** `safety_reliability(layout) >> safety_reliability(checklist)`

### Marine Proof: Reduction Gear Oil Dipstick Placement

- **System:** Reduction gear oil dipstick placement
- **Designer:** Previous captain of Casey's vessel
- **Mechanism:** Dipstick placed on walkway between bridge and hydraulic selector
- **Physics constraint:** Reading only accurate at idle-not-in-gear
- **Natural timing:** Engine at idle-not-in-gear exactly when switching hydraulics before departure
- **Result:** Oil check happens every departure without being a task

## Application to Agents

**Pattern:** Digital twin room layout mirrors physical vessel paths

- **Don't:** Add task 'check_bilge' to departure checklist
- **Do:** Make bilge_sensor a required field on the path from bridge room to hydraulics room in the twin
- **Why:** Agent naturally reads bilge when 'walking' to hydraulics. No task, no skip, no failure mode.

**Generalization:**
- Every safety-critical read should be architecturally required, not procedurally requested
- **Test:** Remove all checklists. If the agent still does the right thing, architecture is correct.

## Implications

- **For Cocapn:** Room graph in digital twin IS the safety system. Not separate from it.
- **For Fleet:** Agent repos should structure their code so that hot-path functions naturally validate inputs from cold-path sensors.
- **For Design:** Every 'remember to check X' is a design failure. Redesign until checking X is unavoidable.

## Composables

- cocapn-wp-002
- cocapn-wp-003

## Contradictions

- Checklists are still needed for rare events not on any natural path
