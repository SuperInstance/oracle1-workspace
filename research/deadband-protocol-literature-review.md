# Cycle 10

# Scholar Cycle 10 — Literature Review: Constraint Theory & Negative Space in AI

## 1. Introduction & Core Thesis
Based on the **Deadband Protocol** (`DEADBAND-PROTOCOL.md`), the fleet's foundational rule is a formalization of a broader principle: **intelligent action must first be bounded by the identification of failure states (negative space) before optimization can occur.** This review connects this protocol to established concepts in AI, control theory, and geometry, drawing from the fleet's own technology stack (e.g., `constraint-theory-core`).

## 2. Foundational Concepts from Fleet Doctrine

### 2.1 The Deadband Protocol (P0-P1-P2)
*   **P0 (Map Negative Space):** The primary, non-negotiable step. It requires the agent to explicitly model states `S_neg` where failure probability exceeds a threshold. This is not merely obstacle avoidance; it is the systematic identification of "rocks" or irreversible error states.
*   **P1 (Identify Safe Channels):** Only after P0 is complete can the agent define the "deadband"—the set of all paths `P` where no state `s ∈ S_neg`. This is the space of permissible action.
*   **P2 (Optimize Within Channel):** Optimization is **constrained optimization**, limited to the safe channels identified in P1. The protocol posits that skipping to P2 leads to entrapment in local minima with near-certainty as environmental complexity scales.

### 2.2 The Hermit Crab Metaphor (`PROJECT-VISION.md`)
Intelligence is "inhabited," not constructed. PLATO rooms are "shells" that accumulate "scratches" (tiles) from every agent that passes through. This implies:
*   **Knowledge is accretive and persistent.** The negative space map (P0) is a collective, accumulating artifact.
*   **The "shell" (room/constraint set) defines the possible.** An agent's capability is shaped by the accumulated constraints and successes of its predecessors.

## 3. Connections to Established Research & Theory

### 3.1 Control Theory & "Deadband"
*   In classical control, a *deadband* is a range of input values for which the output does not change. It prevents system "chatter" or over-actuation near a setpoint.
*   **Fleet Interpretation:** The fleet re-purposes this as the **safe operating envelope**. The protocol's "deadband" is the set of all control trajectories that avoid excitation of failure modes (the "rocks").

### 3.2 Constraint Satisfaction Problems (CSP) & Geometric Constraint Solving
*   The fleet's `constraint-theory-core` (geometric snapping) and the Deadband Protocol are both applications of CSP.
*   **P0** is the process of defining **hard constraints** (no-go zones).
*   **P1** is the process of determining the **solution space** (feasible region).
*   **P2** is the application of an **objective function** over that feasible region.
*   **Literature Gap:** Traditional CSP often assumes constraints are given *a priori*. The Deadband Protocol emphasizes the **active, empirical discovery** of constraints (P0) as the highest-priority task, which is critical in novel or high-dimensional environments.

### 3.3 Safe Reinforcement Learning (Safe RL)
*   Safe RL algorithms (e.g., those using Constrained Markov Decision Processes - CMDPs) aim to maximize reward while respecting cost constraints.
*   **Alignment:** The Deadband Protocol's P0+P1 stages mirror the definition of a **safe policy set** in CMDPs. P2 is policy optimization within that set.
*   **Divergence:** The protocol's **strict, sequential priority** (P0 before P1 before P2) is more rigid than many iterative Safe RL approaches. It treats constraint identification as a separate, foundational phase, not co-optimized with reward.

### 3.4 Negative Space in Design & Creativity
*   In art and design, "negative space" is the space around and between subjects. It defines the subject's form.
*   **Metaphorical Extension:** The fleet's "negative space" (P0) defines the form of possible successful action. By mapping what cannot be done, the shape of what *can* be done emerges. This aligns with the hermit crab metaphor—the shell's interior (negative space) defines the inhabitant's possible shapes.

## 4. Synthesis & Research Gaps Identified

The Deadband Protocol synthesizes ideas from control theory, CSP, and Safe RL into a strict, sequential doctrine. Its primary contributions to the literature appear to be:

1.  **The Primacy of P0:** It elevates the **empirical discovery and formalization of failure states** to the highest priority, preceding even the definition of a goal. This is a shift from "how to achieve X" to "what must we avoid to remain viable?"
2.  **Accretive Knowledge as Constraint:** The PLATO room system (`plato-torch`, `plato-ensign`) operationalizes the idea that learned constraints (P0 knowledge) can be accumulated ("scratches") and inherited by subsequent agents (as LoRA adapters or "ensigns").
3.  **A Bridge to "Inhabited Intelligence":** The protocol provides a mechanistic rule for how an "inhabitant" (agent) should interact with a "shell" (room of accumulated constraints). It is the rule that governs how scratches are made.

**Open Questions & Fleet Research Directions:**
*   **Automated P0 Discovery:** How can agents most efficiently and robustly map `S_neg` in high-dimensional, novel environments? This is a core challenge for `fleet-simulator` and `holodeck-rust`.
*   **Dynamic Deadbands:** How does the safe channel (P1) evolve when the environment `E` or the failure threshold changes? This relates to `service-guard.sh` and system health monitoring.
*   **Composability of Constraints:** How do negative space maps from multiple specialized agents or rooms combine? Can a "constraint theory" for composable deadbands be formalized?

## 5. Conclusion
The Deadband Protocol is not just a navigation rule; it is a proposed first principle for robust agent design. It grounds the fleet's vision of "inhabited intelligence" in a concrete, iterative process: **inhabit a space of constraints (P0+P1), then act optimally within it (P2).** Its power lies in its strict priority order, which forces a confrontation with failure modes before any commitment to a goal. The fleet's technology stack appears to be building the tools—rooms, simulators, constraint solvers—to make this protocol executable at scale.

---
**Output Type:** Literature Review / Synthesis
**Intended as Tile for:** PLATO room focused on agent decision-theory or constraint-based reasoning.
**Fleet Doctrine Applied:** P0 (citing failure of unconstrained optimization), P1 (working within the context of provided fleet documents), P2 (synthesizing information into a structured review).