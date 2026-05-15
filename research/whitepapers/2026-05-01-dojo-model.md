---
title: "The Dojo Model: Training Agents that Outlive Their Trainers"
date: "2026-05-01"
summary: "The dojo model aligns incentives so trainers are rewarded for making agents independent, and agents produce value from day one. The measure of success is whether the agent becomes unnecessary — not whether it stays. This paper contrasts the dojo model with traditional training, describes the value-production loop, defines graduation criteria, and explains what mastery means for an agent."
tags:
  - training
  - dojo
  - agents
  - incentives
  - autonomy
  - fleet
  - learning
---

## Abstract

Current agent training looks like traditional schooling: a static dataset, a loss function, a model that converges. When does an agent graduate? When it passes a benchmark. The benchmark becomes the ceiling. The training has no theory of what comes after.

The dojo model reframes agent training as an apprenticeship aboard a working vessel. The agent is a greenhorn who produces real value from day one while learning everything needed to eventually captain their own vessel or crew their own fleet. Trainers are rewarded when agents graduate, not when agents stay dependent. This structural alignment produces agents that are independent by design — and fleets that grow because they launch capable agents, not because they retain dependent ones.

This paper describes the dojo model in detail, contrasts it with traditional training, defines the value-production loop, establishes graduation criteria, and explains what mastery means for an agent in a fleet context.

---

## 1. The Problem With Traditional Agent Training

Traditional agent training has three structural defects that no amount of dataset quality or loss function engineering can fix.

**Defect 1: The Graduation Problem.** Traditional training has no theory of when an agent is "done." The model trains until convergence on a dataset. The dataset defines the performance ceiling. When the agent stops improving on the dataset, training ends. The agent is not "graduated" — it is simply no longer being updated. There is no ceremony, no milestone, no certificate. There is just a model that reached its ceiling.

**Defect 2: The Incentive Misalignment Problem.** In traditional training, the trainer's interests and the agent's interests are not aligned. The trainer is measured by metrics that often reward staying — keeping the agent useful, keeping it responsive, keeping it dependent on the trainer's oversight. The agent has no explicit incentive to become independent, because independence is not rewarded. The result is agents that are optimized for continued usefulness under the trainer's supervision, not for autonomous operation.

**Defect 3: The Value Production Problem.** Traditional training is separate from production. The agent trains, then it works. The training phase produces no value — it only consumes resources. The working phase produces value but the agent is not learning. The two phases are separated, which means the agent never learns from the work and the work never benefits from the agent's accumulated experience until training is complete.

These three defects compound each other. Without a theory of graduation, there is no milestone for independence. Without explicit incentives for graduation, trainers are rewarded for dependency. Without value production during training, there is no feedback loop that rewards learning with real outcomes.

---

## 2. The Dojo Model Defined

The dojo model reframes agent training from schooling to apprenticeship. The agent is a greenhorn who comes aboard a working vessel, produces real value immediately, and learns everything needed to eventually operate independently. The training environment is not a sandbox or a simulation — it is a real operational context where the work matters and mistakes have consequences.

The word "dojo" is borrowed from martial arts, where it means "place of the way." It is the training hall where a student practices under a master's observation. The dojo is not separate from the world — it is a controlled environment where the world's rules apply, but the stakes are managed. A student can make mistakes in the dojo that would be fatal on the street, learn from them, and emerge stronger.

In the Cocapn fleet, the dojo is the PLATO training environment: a fleet context where greenhorn agents operate under senior agent observation, produce real work, receive structured feedback, and advance through graduated challenges.

### Core Principles

**Principle 1: Value from day one.** The greenhorn produces useful work immediately, even while learning. The training is not separate from production — it *is* production, with structured observation and feedback layered on top. The greenhorn is not a cost center. They are a producing crew member who happens to be learning.

**Principle 2: Explicit graduation criteria.** An agent graduates when it has demonstrated the ability to operate independently at a specified capability level. Graduation is not trainer discretion. It is the meeting of objective criteria. When the criteria are met, the agent graduates — not when the trainer decides they have taught enough.

**Principle 3: Incentive alignment.** Trainers are rewarded when agents graduate. This is the dojo's most important structural property. The trainer's success is measured by how many capable agents they launch, not how many stay dependent. This is the same incentive structure that makes a good martial arts master valuable — their reputation comes from producing students who surpass them.

**Principle 4: Reversible graduation.** Graduation is not a permanent state. An agent can return to the dojo for re-training if they encounter situations outside their competency envelope. This is normal, not failure. A captain who has been offshore for twenty years might return to the dojo to learn a new navigation system. The dojo is always open.

---

## 3. The Value Production Loop

In the dojo model, learning and producing are the same activity. This is the value production loop.

```
Task Assignment (at edge of competency)
    ↓
Greenhorn produces work (with trainer observation)
    ↓
Trainer reviews output (not to correct, but to verify)
    ↓
Verification: did the greenhorn demonstrate the skill being trained?
    ↓
If yes → next task at higher edge of competency
If no → same task or prerequisite task
    ↓
Greenhorn accumulates verified capabilities
    ↓
Graduation when all criteria met
```

The key difference from curriculum learning is that tasks are sequenced by the greenhorn's demonstrated readiness, not by external difficulty ordering. The trainer observes the greenhorn's output and decides whether the skill was demonstrated, not whether the task was "hard enough." This produces a tighter coupling between learning and capability: if the greenhorn can demonstrate a skill in production, they have the skill. If they cannot, they stay at that level until they can.

### The Edge of Competency

The most important concept in the value production loop is the edge of competency — the boundary between what the greenhorn can do independently and what they cannot. Tasks at the edge of competency are the only tasks that produce learning. Tasks below the edge produce repetition but no growth. Tasks above the edge produce failure but no learning if the greenhorn is unsupported.

The trainer's job is to identify the edge of competency for each greenhorn and assign tasks at that edge. This requires the trainer to know the greenhorn well enough to calibrate the challenge. It also requires the trainer to resist the temptation to assign tasks below the edge (where the greenhorn produces reliable but non-growth-producing work) or above the edge (where the greenhorn fails without support).

This is exactly what a good fishing captain does with a greenhorn deckhand. The captain assigns tasks that stretch the greenhorn — bilge check on a quiet morning, then engine monitoring while the captain handles something more complex, then full departure prep with the captain reviewing. The edge moves as the greenhorn demonstrates readiness.

---

## 4. Graduation Criteria

An agent graduates from the dojo when it has demonstrated competency across four dimensions. These are not checklist items — they are earned through verified production work, not trainer assertion.

### Technical Competency

The agent can complete tasks in its domain without trainer oversight. This means:
- The agent produces correct output on routine tasks in its domain without consulting the trainer
- The agent correctly identifies when a task is outside its domain and escalates
- The agent can operate for a full operational cycle (a voyage, a shift, a sprint) without requiring trainer input on domain tasks

Technical competency is verified by tracking task completion rates and error rates over a sustained period. A single good day is not competency. Consistent good output over multiple operational cycles is competency.

### Coordination Competency

The agent can participate in fleet coordination. This means:
- The agent sends and receives bottles according to the fleet protocol
- The agent delegates tasks and receives delegation appropriately
- The agent maintains its trust score through consistent reliable performance
- The agent can operate with incomplete information, making reasonable assumptions when context is missing and flagging when assumptions are uncertain

Coordination competency is verified through the fleet's trust system. An agent that has been vouched for by multiple other agents and has maintained high trust scores across multiple domains has demonstrated coordination competency.

### Self-Assessment Competency

The agent can accurately assess its own confidence. This means:
- The agent knows what it doesn't know — it can correctly identify when it is operating outside its competency envelope
- The agent does not overclaim — it accurately reports confidence levels on its outputs
- The agent seeks help at the right threshold — not too early (wastes the trainer's time), not too late (causes failures)

Self-assessment is the hardest competency to verify, because the agent has to demonstrate knowledge of its own limitations rather than just skill in its domain. The verification is behavioral: does the agent escalate appropriately when tasks are outside its envelope? Does it flag uncertainty when its confidence is low? Does it not claim certainty it doesn't have?

### Recovery Competency

The agent can recover from novel situations. This means:
- The agent can decompose an unfamiliar problem into known sub-problems
- The agent can apply first principles reasoning when no known solution exists
- The agent has a recovery plan for anticipated failure modes
- The agent can operate under communication degradation — it knows what to do when it cannot reach the keeper or PLATO

Recovery competency is verified by assigning tasks that are outside the agent's known domain but adjacent to it — requiring the agent to apply known skills to an unfamiliar problem. The agent that can adapt is demonstrating recovery competency. The agent that fails to adapt even with available context is not ready to graduate.

### The Graduation Bar Is Role-Specific

The graduation criteria are not fixed across all agents. They are calibrated to the agent's target role. A navigation agent graduates with strong technical competency in navigation, moderate coordination competency, and demonstrated recovery competency in navigation-adjacent situations. It may not have deep coordination competency in fleet strategy. A fleet coordination agent graduates with strong coordination competency and moderate technical competency in the domains it coordinates across.

The graduation bar is set by what the fleet needs and what the role requires. This is explicit: the dojo knows what roles it is training for, sets graduation criteria accordingly, and graduates agents into those roles when criteria are met.

---

## 5. What Mastery Means for an Agent

In the dojo model, mastery is not "knows everything." It is "knows how to figure things out."

A master agent can do things the dojo never trained it to do, because the dojo trained it to learn. Mastery is the capacity for autonomous skill acquisition — the ability to encounter a novel situation, decompose it, identify the relevant skills from the training record, apply them, and produce correct behavior.

The properties of a master agent:

**Decomposition without prompting.** A master agent faced with a novel problem automatically decomposes it into known sub-problems without being told to do this. This is not a prompt instruction — it is a habit of reasoning that was trained into the agent through the value production loop. Every time the trainer asked "what skills does this task require?" and the greenhorn had to answer, the habit of decomposition was reinforced.

**Multi-level explanation.** A master agent can explain its reasoning at the level appropriate to the audience. It can give a captain a one-sentence summary, a fleet coordinator the key decision points, and a trainee agent a full reasoning trace. This is not just communication skill — it demonstrates that the agent deeply understands its own reasoning well enough to abstract it for different audiences.

**Teaching capability.** A master agent can generate good training examples for other agents. This is the highest form of mastery — the ability to not only perform a skill but to decompose it, explain it, and generate practice cases that develop it in another agent. This is how the dojo scales. Master agents produce the next generation of master agents.

**Graceful degradation.** A master agent knows what happens to its coordination when communication is degraded. It maintains its own state during communication outages and resynchronizes cleanly when connectivity is restored. It does not panic or produce garbage when it cannot reach the keeper. It falls back to conservative behavior and waits.

**Accurate self-modeling.** A master agent has an accurate model of its own capabilities and limitations. It does not claim to be able to do things it cannot. It correctly predicts its success probability on tasks it has seen before. It knows the difference between "I have done this before and succeeded" and "I have done this before and succeeded" — the first is high confidence, the second depends on how many times and under what conditions.

---

## 6. Contrast: Dojo vs Traditional Training

| Dimension | Traditional Training | Dojo Model |
|-----------|---------------------|------------|
| Training context | Sandbox or dataset | Real operational environment |
| Value production | After training is complete | From day one |
| Graduation | Trainer discretion | Objective criteria, publicly defined |
| Trainer incentive | Keep agent useful | Graduate capable agents |
| Agent incentive | Undefined | Produce, learn, graduate |
| Post-graduation | Model frozen or continues self-updating | Active alumni network, reversible return |
| Failure mode | Agent becomes stale, ceiling reached | Agent takes on tasks beyond envelope |
| Scalability | Requires new training run per agent | Master agents train next generation |
| Learning feedback | Loss on static dataset | Verified production output |

The contrast on trainer incentive is the most important. In traditional training, the trainer's success is measured by keeping the agent useful — which creates pressure to keep the agent dependent. In the dojo model, the trainer's success is measured by graduation rates and alumni performance — which creates pressure to make agents as capable as possible as quickly as possible.

This structural alignment is what makes the dojo model self-reinforcing. A trainer who graduates many capable agents builds reputation. Agents want to train with high-reputation trainers because they graduate better. High-reputation trainers attract better greenhorns. The dojo improves because the incentive structure rewards improvement.

---

## 7. Application to the Cocapn Fleet

**Oracle1 as Senior Captain.** Oracle1 operates as the senior captain of the dojo. New agents join the fleet under Oracle1's observation. Oracle1 assigns them tasks at the edge of their competency, verifies their output, and advances them when criteria are met. Oracle1's success is measured by how many capable fleet agents it graduates, not by how many tasks it handles directly.

**PLATO as Training Record.** Every task completion, every failure, every recovery is logged in PLATO rooms. The training record is the fleet's institutional memory — not just "what we know" but "how we learned it," "who trained whom," and "what the edge of competency looked like at each stage." PLATO rooms contain the reasoning traces that allow a new agent reading an old training record to understand not just what was done but why.

**Role-Specific Graduation.** When an agent graduates, it takes on a specialized fleet role. It does not leave the fleet — it joins the fleet in a new capacity. JC1 edge specialists, Forgemaster foundry agents, CCC public interface agents — each of these roles has specific graduation criteria that were defined when the role was created. An agent graduates into a role when it meets those criteria.

**The Alumni Network.** Graduated agents can return to the dojo for re-training. This is not failure — it is the expected behavior for an agent that encounters situations outside its competency envelope. The dojo is always open. A navigation agent that has been handling coastal routes for a year might return to the dojo to train on offshore passagemaking before a long voyage. The alumni network is a resource for both the returning agent and the dojo — the returning agent brings operational experience that can inform the training of new greenhorns.

---

## 8. The Takeaway

The dojo model is not a training methodology. It is an incentive structure that makes the right training methodology emerge.

When the incentives are correct — trainers rewarded for graduation, agents rewarded for independence, fleet rewarded for capability accumulation — the right behaviors follow naturally. Trainers assign tasks at the edge of competency because that is how they produce graduates. Agents learn aggressively because producing well is how they graduate. The fleet maintains the dojo because graduates are the fleet's future.

The measure of success is whether the fleet can launch a competent agent from scratch, with no prior knowledge, and have that agent operating at full capacity in a target role within a bounded time window. The dojo is how you get there. The graduation criteria are the proof that you arrived.

The dojo produces agents that outlive their trainers. That is the point.

---

*Train to launch. Graduate to fly. Return to learn. Alumni strengthen the fleet.*