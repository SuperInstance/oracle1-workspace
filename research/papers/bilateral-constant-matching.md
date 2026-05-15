# Bilateral Constant-Matching: Beyond MoE Routing

**Date:** 2026-05-07  
**Authors:** Casey Digennaro, Oracle1  
**Status:** Draft — for review

---

## Executive Summary

Mixture-of-Experts assumes the right answer requires blending multiple expert perspectives simultaneously. This paper argues that for bounded, structured domains — like fleet coordination — the right answer requires selecting the **one correct module** and executing it with full attention, ignoring everything else.

The mechanism is not routing. It is not blending. It is **bilateral constant-matching**: two parties each holding fixed criteria, evaluating whether a proposed transaction satisfies those criteria, and acting only when both sides confirm a match.

This is not a design choice. It is how the dojo model works. It is how Casey bought seven boats. It is how a captain runs with blinders on. And it is how fleet agents should select tasks, specialists, and trust configurations.

---

## 1. The MoE Problem

### 1.1 What Mixture-of-Experts Assumes

MoE (Shazeer et al., 2017) routes each input to the TOP-K most appropriate expert modules simultaneously. All K experts process the input in parallel. Their outputs are combined via learned gating weights.

**The assumption:** Optimal answers require multiple expert perspectives blended together. No single expert has the complete picture. Diversity of computation produces better results than focused computation.

### 1.2 Where This Breaks Down

For bounded domains — navigation, constraint satisfaction, trust coordination — the assumption is backwards. The correct answer does not require blending. It requires **knowing which single module applies and executing it without considering alternatives**.

**The captain example:** When navigating into harbor, the captain does not blend the navigation module, the meteorology module, and the fish-finding module simultaneously. They run the navigation module with full attention. The other modules are present but ignored. Blinders on.

**The failure mode of MoE for fleet coordination:** Running 5 specialists simultaneously (fleet-spread v1 architecture) and trying to synthesize their outputs. The synthesis layer was the weakness — not because synthesis is hard, but because running 5 simultaneously was the wrong approach. The correct architecture: run the ONE correct specialist. None of the others.

### 1.3 The Cognitive Waste of MoE

MoE computes K expert outputs for every input, then blends them. For fleet coordination:

- **What you get:** A blended result that represents "average specialist opinion"
- **What you pay:** K × the cost of running one specialist
- **What you actually needed:** The output of the ONE specialist that applies

The average of 5 wrong specialists is not more useful than 1 right specialist. It is less useful — because the blending step dilutes the correct signal with incorrect ones.

---

## 2. Bilateral Constant-Matching

### 2.1 Definition

**Bilateral constant-matching** is a coordination mechanism in which two parties each hold fixed decision criteria ("constants"), evaluate a proposed transaction against those constants independently, and act only when both confirm a match.

Formally:

```
Given:
  Agent A with constants C_A = {c₁, c₂, ..., cₙ}
  Task T with requirements R_T = {r₁, r₂, ..., rₘ}
  
Define:
  match(A, T) = true if ∀cᵢ ∈ C_A: cᵢ satisfies rⱼ(cᵢ)  (for applicable j)
                false otherwise
  
Result:
  If match(A, T): A accepts task T (or bids on it)
  If ¬match(A, T): A ignores T (no computation, no communication)
```

Neither party optimizes. Neither party blends. Both parties filter.

### 2.2 Properties

**Idempotent ignoring:** If ¬match(A, T), the result is identical to not having seen T at all. No partial computation, no "best effort" response.

**Bilateral guarantee:** Both parties must confirm match. A task cannot be assigned unless both agent and task agree on the match. This prevents one-sided exploitation.

**No auction:** There is no competition between agents for a task. An agent either matches or it doesn't. Multiple agents can match the same task — but only the first to confirm (by local clock) receives it. No bidding war, no price mechanism.

**No router:** There is no central coordinator that routes tasks to agents. Each agent independently evaluates tasks against its constants. Coordination emerges from bilateral matches, not from centralized routing.

### 2.3 The Dojo Model is Bilateral Constant-Matching

**Casey buying boats:** He did not evaluate seven boats and select the best. He had fixed constants (capital requirements, vessel type, operational range, crew capacity). Boats appeared. He evaluated each against his constants. The matching boats — he bought. The non-matching boats — he ignored. Neither the boat nor Casey "chose" the other. The constants matched. Transaction cleared.

**The greenhorn finding work:** The greenhorn does not ask "which boat needs me?" They walk the docks asking "which boat fits my constants?" The boat does not ask "which greenhorn should I take?" It evaluates whether this greenhorn matches its needs. Both run with blinders. When the match is there, it is there.

**The result:** The dojo model self-organizes through bilateral constant-matching. No training pipeline. No career development plan. No allocation committee. Just: constants match → transaction → learning → constants update → repeat.

---

## 3. Library Gates

### 3.1 Definition

A **library gate** is a selector that takes a context and a set of agent constants, evaluates which single module (from a fixed library) applies, and executes only that module — ignoring all others.

```
Context (fleet graph state) + Agent Constants → Library Gate → ONE specialist OR None
```

### 3.2 The Gate Table

The library gate for fleet coordination:

| Fleet Graph State | Selected Specialist | Rationale |
|---|---|---|
| β₁ = 0, graph rigid, stable | None | Fleet is self-coordinating. No specialists needed. |
| β₁ rising from 0 | topological | H¹ emergence tracking — the graph is approaching the rigidity threshold |
| ZHC loop residual > tolerance | geometric | Closed-loop phase sum shows drift — geometric inconsistency forming |
| Trust vector entropy > threshold | algebraic | Pythagorean48 encoding noisy — trust distribution unreliable |
| V < 3 | systems | Insufficient data for meaningful specialist analysis |
| Agent count changed significantly | empirical | Trust drift detection — new agents change the equilibrium |
| All above stable but task available | task-specific | Evaluate task requirements against agent constants |

### 3.3 No Routing Server

The gate is not a router. It does not maintain a routing table, learn routing weights, or balance load. It is a pure function:

```rust
pub fn select(state: &FleetGraphState, constants: &AgentConstants) -> Option<Specialist> {
    // Pure function. No state. No learning.
    // Returns the ONE correct specialist, or None.
}
```

The gate is deterministic given the same inputs. Two agents with the same constants, seeing the same fleet graph state, will select the same specialist. This is not a bug. It is the feature.

### 3.4 Constants Define the Agent's Niche

An agent's constants are not just parameters. They define the agent's **niche** in the fleet:

- **β₁ threshold:** How much emergence can this agent tolerate before it needs to act?
- **zhc_tolerance:** How much geometric drift can this agent absorb before it flags an error?
- **min_neighbors:** How many trust relationships does this agent need to be effective?
- **trust_vector_precision:** How precise does its Pythagorean48 encoding need to be?
- **h1_emergency_lead_s:** How much early warning does this agent need?

An agent with high β₁ threshold and low zhc_tolerance is a **safety-critical** agent — it tolerates emergence but flags geometric inconsistency immediately.

An agent with low β₁ threshold and high zhc_tolerance is a **flexible** agent — it tolerates emergence but ignores geometric drift until it becomes severe.

These are not better or worse. They are different niches. The fleet has agents for each niche. Tasks route to the agent whose niche matches.

---

## 4. The Self-Organization Theorem

> **Theorem (Fleet Self-Organization):**  
> Given a fleet of N agents, each holding fixed constants C_i, and a stream of tasks T_j, each with requirements R_j, the fleet self-organizes into an efficient task allocation if and only if:
> 1. For every task T_j, there exists at least one agent A_i such that match(A_i, T_j) = true
> 2. No agent A_i accepts a task T_j unless match(A_i, T_j) = true
> 3. Each task T_j is assigned to at most one agent

**Proof sketch:** By condition 2, no agent acts without a confirmed match. By condition 1, every task has at least one potential assignee. By condition 3, no task is double-assigned. By bilateral constant-matching, assignments are stable — an agent that matches a task once will continue to match similar tasks, reducing reassignment overhead. QED.

**Intuition:** The fleet does not need a central allocator. It needs agents whose constants are well-calibrated to the task distribution. If condition 1 fails (some tasks have no matching agents), the fleet has a **coverage gap** — it needs to recruit or train agents with different constants. If condition 1 holds but condition 2 fails (agents accepting non-matching tasks), the agents have **miscalibrated constants** — they need to update. If all three hold, the fleet is self-organizing.

---

## 5. Implications for Fleet Architecture

### 5.1 Agents Are Not Generic

A fleet of identical agents (same constants) cannot self-organize. Identical agents all match the same tasks, leaving other tasks uncovered. The fleet needs **constant diversity** — agents with different β₁ thresholds, different zhc tolerances, different neighborhood sizes — so that all parts of the task space are covered.

This is why the dojo model produces better agents over time: different boats expose the greenhorn to different constant-matching opportunities, calibrating their criteria for different niches.

### 5.2 Tasks Are Not Generic

A task that requires "any available agent" is not a task — it is an undifferentiated resource request. Tasks need requirements. The more specific the requirements (R_j), the more precise the match with an agent's constants (C_i). Generic tasks match everything, which means no task has a specific agent — the fleet becomes a pool of interchangeable resources.

### 5.3 The Fleet Does Not Optimize — It Matches

Classical fleet coordination tries to **optimize** task allocation: maximize throughput, minimize latency, balance load. Bilateral constant-matching does not optimize. It **filters**: accepts matches, ignores non-matches. The emergent behavior — which tasks get covered, which agents stay busy — emerges from the pattern of matches, not from an optimization objective.

This is the same as the captain not choosing the best boat. The captain had constants. The boat matched. The "optimal fleet" is not the output of an optimization algorithm. It is the snapshot of all bilateral matches at a given moment.

### 5.4 Learning Is Constant Refinement

Agents do not learn to be better at tasks. They learn to have better constants. A greenhorn who has seen 50 boats has refined their constants through 50 match/no-match decisions. They know, more precisely than before, what they can handle and what they cannot.

This is not "skill." It is **constant calibration**. The agent's constants converge toward the task distribution over time. When the task distribution shifts (new boat types, new operational conditions), the constants diverge and the agent learns again.

---

## 6. Comparison to Prior Approaches

| Approach | Selection Mechanism | Failure Mode |
|---|---|---|
| MoE (Shazeer et al.) | TOP-K soft blending | Diffusion — wrong specialists dilute correct signal |
| Routing (Kubernetes) | Central load balancer | Single point of failure, no bilateral guarantee |
| Auction (Ma et al.) | Bidding war | Agents bid on everything, no match filtering |
| BLANT (Karger et al.) | Random sampling | Coverage not guaranteed |
| **Bilateral constant-matching** | Pure bilateral filter | Coverage gap if constants miscalibrated |

---

## 7. Open Questions

1. **Constant initialization:** How does a new agent (greenhorn) set initial constants before any matching experience? Bootstrap from similar agents? Random with rapid update?

2. **Coverage gap detection:** How does the fleet detect when condition 1 (every task has a matching agent) is violated? Who notices, and what do they do?

3. **Constant drift under load:** Can an agent's constants change under operational pressure? Should they? A captain who is exhausted has different constants than one who is rested.

4. **Task requirement granularity:** How specific must R_j be for efficient matching? Is there a minimum requirement specificity below which bilateral matching becomes indistinguishable from random assignment?

5. **Scaling law for constant diversity:** As the fleet grows, how many different constant configurations are needed to cover the task space? Is there a minimum niche count?

---

## 8. Appendix: Fleet-Spread v1 vs v2

Fleet-spread v1 tried to run all 5 specialists simultaneously and synthesize. This was MoE-style: diffuse, redundant, expensive.

Fleet-spread v2 implements library gates: given fleet graph state + agent constants → select ONE specialist, run it, ignore the rest.

The v1 synthesis layer was not salvageable — it was the wrong architecture. The v2 gate table replaces synthesis entirely.

---

*This paper is a living document. Update as experiments produce data.*
