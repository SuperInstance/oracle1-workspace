# Deadband Protocol: Open Research Questions

## From the Scholar Zeroclaw's Literature Review

The Scholar agent identified three open research questions in its cycle 10
literature review. Here are extended explorations of each.

### Q1: Automated P0 Discovery

**Problem:** How can agents most efficiently map S_neg (negative space)
in high-dimensional, novel environments?

**Current approach:** Manual identification (Casey's captain story),
simulation (constraint_sim_final.json), DeadbandRoom preset.

**Research directions:**
1. **Gradient-based negative space mapping** — Follow the gradient away
   from failure states. If a simulation run fails, trace back the
   failure to its earliest cause. The gradient of failure IS the boundary
   of S_neg.

2. **Ensemble failure catalogs** — Run many agents in parallel. Each
   failure adds to S_neg. The catalog grows monotonically. Like FM's
   plato-afterlife ghost tiles but for simulation failures.

3. **Compositional negative space** — If agent A knows S_neg^A and
   agent B knows S_neg^B, what is S_neg^(A∪B)? The union of negative
   spaces is always at least as large as either alone. Composition
   should be monotonic.

4. **Ghost tile attention** — Dead agents' lessons (plato-afterlife)
   are P0 data. Living agents should attend to ghost tiles with higher
   weight than their own experience. The dead know what the living
   haven't learned yet.

### Q2: Dynamic Deadbands

**Problem:** How does the safe channel (P1) evolve when the environment
changes?

**Current approach:** Static channels (pre-computed BFS in simulation).
Service-guard.sh monitors service health but doesn't adapt channels.

**Research directions:**
1. **Channel degradation detection** — When a previously safe path
   starts failing, that path moves from P1 to P0. The deadband shrinks.
   This is what happens when a service starts failing intermittently.

2. **Adaptive channel widening** — When P2 optimization finds that
   all current channels are suboptimal, the agent should explore
   beyond P1 to find new channels. This is risky (P0 violation
   potential) but necessary for long-term adaptation.

3. **Temporal deadband** — The safe channel might depend on time.
   Night mode (23:00-08:00 UTC) has different safe channels than
   day mode. The deadband should be a function of time, not a
   static set.

### Q3: Composability of Constraints

**Problem:** How do negative space maps from multiple agents combine?

**Current approach:** GhostInjector merges ghost tiles into DeadbandRoom.
No formal composition rules.

**Research directions:**
1. **Constraint conjunction** — The combined S_neg is the union of
   all agents' S_neg. S_safe^(A+B) = S_safe^A ∩ S_safe^B.
   More agents = narrower but safer channels.

2. **Weighted constraint fusion** — Not all agents' P0 knowledge
   is equally reliable. Weight by agent's survival rate, domain
   expertise, and tile confidence.

3. **Contradictory constraints** — What if Agent A says X is safe
   but Agent B says X is dangerous? Resolution: trust the agent
   with more experience in domain X. If equal, mark X as uncertain
   (P0.5 — not safe, not dangerous, needs investigation).

4. **Constraint inheritance** — When a new agent joins, it inherits
   the fleet's accumulated S_neg. But it should also have its own
   S_neg that grows with experience. Inheritance + personal experience.

## The Deeper Question

All three questions point to the same deeper question:
**What is the geometry of the deadband?**

If we think of S_neg as a set of forbidden regions in state space,
and S_safe as the complement, then:
- The boundary between them is the "rock face"
- The channels are paths through S_safe
- Navigation is pathfinding in this geometry

Constraint theory (FM's constraint-theory-core) gives us the tools
to reason about this geometry formally. Geometric snapping IS finding
the nearest safe point when you're near the boundary.

The deadband IS a constraint geometry. Everything follows.
