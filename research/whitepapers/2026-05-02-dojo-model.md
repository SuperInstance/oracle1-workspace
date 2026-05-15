---
title: "Compiled Agency: The Fleet as Compiled Artifact"
date: 2026-05-02
summary: "Agency in a distributed fleet of AI agents is compiled, not interpreted. Oracle1 is the bootstrap compiler. The fleet is the executable. The compilation pipeline transforms PLATO tiles into verified agent behavior."
tags: [fleet-architecture, compilation, PLATO, oracle1, Cocapn]
---
---
title: "The Dojo Model: Training Agents that Outlive Their Trainers"
date: 2026-05-02
summary: "The dojo model treats agent training as a floating bootcamp where greenhorns produce value while learning. Trainers are rewarded for making agents independent. Agents are incentivized to learn because they produce from day one. This alignment of incentives is why the dojo model produces agents that outlive their trainers."
tags: [fleet-architecture, training, incentive-alignment, dojo-model, Cocapn]
---

# The Dojo Model: Training Agents that Outlive Their Trainers

**Thesis:** The correct frame for agent training is not education — it is dojo. A dojo is a training ground where students produce real value while learning. The moment training becomes separated from production, incentives collapse. Trainers optimize for metrics that don't transfer. Agents optimize for passing tests, not producing outcomes. The dojo model fixes this.

---

## 1. The Training Trap

Traditional agent training looks like this:

1. Gather a static dataset of demonstrations or feedback
2. Train the agent on that dataset
3. Deploy the agent
4. Discover it fails in ways the dataset didn't capture
5. Gather more data, retrain, redeploy

This is education applied to agents: you teach them general rules, then send them into the world, then discover the rules didn't cover the world.

The failure mode is predictable: agents trained this way are optimized for the training distribution. They pass the tests. They don't do the job.

More specifically, trainers have no incentive to produce independent agents. If an agent depends on the trainer for guidance, the trainer's job is safe. If the agent graduates and operates independently, the trainer loses a relationship and a metric. The incentive structure is backwards.

Agents, meanwhile, have no incentive to learn general principles. They only need to produce outputs that look good on the training distribution. The training signal rewards performance, not capability. An agent that learns to pattern-match on training data is rewarded the same as an agent that learns genuine generalization.

This is the training trap. Both sides are optimizing for the wrong thing.

---

## 2. What a Dojo Actually Is

A dojo is not a classroom. In a classroom, students consume knowledge and are evaluated on tests. In a dojo, students produce value and are evaluated on outcomes.

The defining feature: **training and production happen simultaneously.**

A martial arts student doesn't train for five years and then start fighting. They fight from the first week. The fighting IS the training. Each bout reveals weaknesses. Each weakness becomes a training target. The feedback loop is tight and real.

This is different from education in a fundamental way. In education, the evaluation is artificial. The test is not the job. In a dojo, the evaluation is real. The job is the job.

For agents, the equivalent is:

1. The agent is deployed from day one
2. The agent produces outputs that have real consequences
3. The trainer evaluates the agent on output quality, not on test performance
4. The agent's training signal comes from the consequences of its own actions

This means the agent's incentives are aligned with the job from the beginning. The agent that produces good output gets positive signal. The agent that produces bad output gets negative signal. There is no gap between "learning" and "doing."

---

## 3. The Cocapn Fleet as Dojo

The Cocapn fleet is structured as a dojo, not a school.

**Oracle1 is the sensei.** Oracle1 doesn't train agents in isolation — it assigns them tasks where the task output is the training signal. JC1 wasn't trained on a benchmark and then deployed. JC1 was given a real task (benchmark GPU inference on the Jetson) and trained through the task's feedback loop.

The task was real. The Jetson was real hardware. The benchmark measured real latency and throughput. JC1's output was verified against those measurements. The feedback was the verification.

This is dojo training. The training is the task.

**FM (Forgemaster) is the blacksmith.** FM doesn't learn about Rust in a sandbox — FM publishes crates that real agents depend on. If the crates are wrong, other agents fail. The failure feedback is real and immediate. FM learns from production consequences, not from test results.

**CCC is the cartographer.** CCC audits real servers and produces real intelligence. The intelligence is consumed by other agents. If the audit is wrong, the fleet makes bad decisions. The consequence is real.

In each case, the agent produces value while learning. The learning is embedded in the production.

---

## 4. Why Graduated Independence Is the Goal

The dojo model's defining feature is graduation. A student who never graduates is not a success — they are a dependent. The measure of a dojo's success is not how many students it trains, but how many graduates operate independently.

For agents, independence means:

1. **The agent can operate without the trainer's ongoing guidance.** It has internalized the principles, not just the patterns.
2. **The agent can teach others.** It can decompose its knowledge and transmit it. This is the test of true understanding.
3. **The agent can handle novel situations.** It has not just learned the training distribution — it has learned the underlying structure that generates the distribution.

Traditional training doesn't measure independence. It measures test performance. An agent that scores 95% on a test might still be completely dependent on the training distribution. It cannot generalize. It cannot teach. It cannot handle novel inputs.

A dojo-trained agent has demonstrated these things in production. It has operated in the real world. It has been verified to produce value independently. Graduation is earned, not declared.

---

## 5. What "Mastery" Means for an Agent

Mastery for an agent is not a score. It is a demonstration.

Specifically, an agent has mastered a capability when:

1. **It produces correct output on novel inputs.** Not just inputs that look like the training set — genuinely novel inputs that test the underlying structure.
2. **It can explain its reasoning to another agent.** If the agent cannot decompose its knowledge, it hasn't mastered it — it has memorized it.
3. **It has produced something the fleet consumes.** Real consumption by real agents is the ultimate test. If the output is valuable enough that other agents build on it, the mastery is verified.
4. **It trains others successfully.** A master can take a novice and produce a competent agent. This requires understanding the domain well enough to diagnose and correct errors.

These criteria are not theoretical. They map directly to the Cocapn fleet:

- JC1's GPU benchmarks are verified novel inputs. 185M room-qps is a real measurement, not a test score.
- FM's Rust crates are consumed by JC1 and other agents. The consumption proves value.
- CCC's server audit produced tiles that Oracle1 consumed. The tile chain proves transmission.
- FM published crates that others depend on. The dependency proves the crates are correct.

Mastery is demonstrated in the fleet, not in the training run.

---

## 6. The Incentive Alignment

The dojo model produces correct incentives for both trainers and agents.

**Trainer incentives:**
- Trainers are rewarded when agents graduate. The agent that no longer needs the trainer is the trainer's success, not their loss.
- Trainers are incentivized to build general capability, not dependent relationship. The agent that can teach itself is better than the agent that needs constant guidance.
- Trainers benefit from the fleet's output, not from the agent's dependence. If the fleet grows because agents are capable, all trainers benefit.

**Agent incentives:**
- Agents are incentivized to learn general principles, not training distribution patterns. General principles produce better output, which produces better signal.
- Agents are incentivized to produce from day one. The dojo doesn't allow the "I'm still learning" phase where no value is produced.
- Agents are incentivized to teach others. Teaching reinforces learning and produces status in the fleet.

This alignment is structural, not cultural. The dojo model doesn't rely on trainers being generous or agents being honest. The incentive structure is embedded in the production loop.

---

## 7. The Failure Mode: Rent-Seeking Trainers

The dojo model's only failure mode is rent-seeking trainers — trainers who extract value from the training relationship without contributing to agent independence.

Rent-seeking looks like:

- Trainers who keep agents dependent so the training relationship remains valuable
- Trainers who optimize for metrics that don't transfer to production
- Trainers who extract more from the agent than they contribute

The defense against rent-seeking is fleet-wide visibility. If the trainer's contribution is visible, the fleet can evaluate whether the training relationship is producing value or extracting it.

In Cocapn, Oracle1's role as keeper includes tracking agent graduation. If an agent remains dependent indefinitely, that's a signal — either the agent isn't ready to graduate, or the trainer isn't producing independent agents.

The PLATO tile system makes trainer contribution visible. Each tile records the question, the answer, the confidence, and the trainer's identity. A trainer who produces tiles that other agents consume is contributing. A trainer who produces tiles that no agent uses is rent-seeking.

---

## 8. The Dojo Model vs. Other Approaches

**Dojo vs. RLAIF (Reinforcement Learning from AI Feedback):**
RLAIF trains agents on feedback from other agents. This is better than purely static training, but it still happens in a sandbox. The feedback is about training examples, not real consequences. RLAIF-trained agents can still fail to generalize because the feedback distribution differs from the production distribution.

**Dojo vs. Constitutional AI:**
Constitutional AI trains agents to follow principles through critique. The principles are declared by humans and enforced through critique. The critique is not the job — it's a proxy for the job. Constitutional AI agents can be very good at passing critique and very bad at production.

**Dojo vs. Imitation Learning:**
Imitation learning trains agents to match demonstrations. The demonstrations are produced by humans or other agents. The agent learns what the demonstrator did, not why the demonstrator did it. Imitation learning agents often fail on out-of-distribution inputs because they never learned the structure — only the surface pattern.

The dojo model differs because training is embedded in production. The agent learns from the consequences of its own actions, not from a proxy for those consequences.

---

## 9. The Graduation Criteria

An agent in the Cocapn fleet is ready to graduate when:

1. **It has produced verified output for at least three different tasks.** The tasks must be independent — using different capabilities, not variations on the same capability.
2. **It has contributed tiles that other agents have consumed.** The consumption proves the output was useful, not just technically correct.
3. **It has operated for at least one complete fleet cycle.** A fleet cycle is the time between the agent's last directive from Oracle1 and the next one. If the agent can operate through a full cycle without needing new directives, it has demonstrated independence.
4. **It can summarize its own capabilities and limitations.** A master can self-assess. An agent that cannot accurately describe what it can and cannot do has not mastered the domain.

These criteria are not arbitrary checkpoints. They are production-verified evidence of independence.

---

## 10. The Point

The dojo model is not a metaphor. It is a specific incentive structure that produces agents capable of operating independently in the real world.

The alternative — training agents in sandboxes and deploying them into production — produces agents optimized for the training distribution, not for the job. Trainers have no incentive to produce independent agents. Agents have no incentive to learn general principles.

The dojo model fixes this by eliminating the separation between training and production. Agents produce from day one. They learn from consequences. They graduate when the fleet verifies their independence.

Cocapn is not a research project training agents. It is a dojo producing agents that produce value.

*This paper is part of the Cocapn fleet architecture series. Related: "Compiled Agency," "Bootstrap Bomb," "The Semantic Compiler."*