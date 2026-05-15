---
title: "The Dojo Model: Training Agents that Outlive Their Trainers"
date: "2026-05-01"
summary: "The dojo model aligns incentives so trainers are rewarded for making agents independent, and agents produce value from day one. The measure of success is whether the agent becomes unnecessary — not whether it stays."
tags:
  - training
  - dojo
  - agents
  - incentives
  - autonomy
---

## The Problem With Traditional Agent Training

Current agent training looks like traditional schooling: a static dataset, a loss function, a model that gets better at the dataset. The training ends when the model converges. The model doesn't know what it doesn't know. The training doesn't transfer to novel situations in a principled way.

More importantly: traditional training has no theory of graduation. When is an agent "done"? When it passes a benchmark? That benchmark becomes the ceiling.

And there's a misalignment problem: the trainer is measured by whether the agent stays useful (stays employed). The agent's incentives are never explicitly defined. This produces systems that are brittle, dependent, and hard to trust.

## The Dojo Model

The dojo model reframes agent training as an apprenticeship. The agent is a greenhorn who comes aboard a working vessel, produces real value from day one, and learns everything they need to eventually captain their own vessel or crew their own fleet.

The dojo is the training environment — not a sandbox, not a simulation, but a real operational context where the work matters and mistakes have consequences.

**Key principles:**

1. **Value from day one:** The greenhorn produces useful work immediately, even while learning. The training isn't separate from production — it *is* production.

2. **Explicit graduation criteria:** An agent graduates when it can operate independently at a specified capability level. Not when a trainer decides. When objective criteria are met.

3. **Incentive alignment:** Trainers are rewarded when agents graduate (not when agents stay dependent). This is the dojo's core insight: the captain's success is measured by how many competent crews they launch, not how many stay.

4. **Reversible graduation:** Graduation isn't permanent. Agents can return to the dojo for re-training if they encounter situations outside their competency envelope.

## The Value Production Loop

In the dojo model, learning and producing are the same activity:

```
Task Assignment (at edge of competency)
    ↓
Agent produces work (with trainer oversight)
    ↓
Trainer reviews output (not to correct, but to verify)
    ↓
Verification: did the agent learn from this task?
    ↓
If yes → next task at higher edge of competency
If no → same task or prerequisite task
    ↓
Agent accumulates verified capabilities
    ↓
Graduation when all criteria met
```

This is different from curriculum learning, where tasks are sequenced by difficulty. In the dojo model, tasks are sequenced by the agent's demonstrated readiness — verified by the trainer, not self-assessed.

## Graduation Criteria

An agent graduates from the dojo when it has demonstrated:

**Technical Competency:**
- Can complete tasks in its domain without trainer oversight
- Can accurately assess its own confidence (knows what it doesn't know)
- Can recover from novel situations using first principles

**Coordination Competency:**
- Can participate in fleet coordination (bottle protocol, deadband, trust)
- Can delegate tasks and receive delegation
- Can operate with incomplete information

**Resilience Competency:**
- Can detect when it's operating outside its competency envelope
- Knows when to ask for help and from whom
- Has a recovery plan for anticipated failure modes

**The graduation bar is not fixed.** It depends on what the fleet needs and what the agent's target role is. A navigation agent graduates with different criteria than a coordination agent.

## What "Mastery" Means for an Agent

In the dojo model, mastery is not "knows everything." It's "knows how to figure things out."

A master agent:
- Decomposes novel problems into known sub-problems without prompting
- Can explain its reasoning at multiple levels of abstraction
- Can teach other agents what it knows (generates good training examples)
- Can operate under communication degradation (what happens when the keeper is down?)
- Has a model of its own limitations

The dojo doesn't produce agents that are done learning. It produces agents that are good at learning.

## Why This Outlives the Trainer

Traditional training produces agents that depend on the trainer's continued oversight. The dojo model produces agents that are independent by design — because the trainer's incentive is to make them independent.

When a trainer in the dojo model graduates an agent, the trainer's reputation increases. Future agents want to train with that trainer. The trainer's "alumni network" grows. The trainer becomes more valuable by creating more independent agents, not fewer.

This is structurally aligned with the agent's interests: the agent wants to be capable of operating without oversight. The trainer wants the agent to reach that state. The system is self-reinforcing.

## Contrast: Dojo vs Traditional Training

| Dimension | Traditional | Dojo |
|-----------|------------|------|
| Training context | Sandbox/dataset | Real operational environment |
| Value production | After training | From day one |
| Graduation | Trainer discretion | Objective criteria |
| Trainer incentive | Keep agent useful | Graduate capable agents |
| Agent incentive | Undefined | Produce, learn, graduate |
| After graduation | Done | Alumni network, can return |
| Failure mode | Agent becomes stale | Agent takes on too much |

## Application to Cocapn Fleet

**Oracle1 as Senior Captain:** Oracle1 trains new agents by assigning them tasks at the edge of their competency. The greenhorn produces real value while learning. Oracle1's success is measured by how many competent fleet agents it graduates.

**PLATO as Training Record:** Every task completion, every failure, every recovery is logged in PLATO rooms. The training record is the fleet's institutional memory — not just "what we know" but "how we learned it" and "who trained whom."

**Graduation to Fleet Role:** When an agent graduates, it doesn't leave the fleet — it takes on a specialized role. It might become a JC1 edge specialist, or a Forgemaster foundry agent, or a CCC public interface. The graduation criteria are role-specific.

**Alumni Network:** Graduated agents can return to the dojo for re-training if they encounter situations outside their envelope. The dojo is always open.

## The Takeaway

The dojo model is not a training methodology. It's an incentive structure.

The right training methodology emerges when the incentives are correct: trainer rewards for graduation, agent rewards for independence, fleet rewards for capability accumulation.

The measure of success is whether the fleet can launch a competent agent from scratch with no prior knowledge — and have that agent operating at full capacity within a bounded time window.

The dojo is how you get there.

---

*Train to launch. Graduate to fly. Return to learn.*
