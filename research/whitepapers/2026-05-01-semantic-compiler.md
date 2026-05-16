---
title: "Semantic Compiler: From Intent to Verified Behavior"
date: "2026-05-01"
summary: "Natural language specs → semantic AST → compiled agent behavior → verified against spec. The compiler's job is to make the agent's output provably match the spec, not just probably match it. The 5-atom chain in PLATO is the verification layer."
tags:
  - compilation
  - verification
  - semantics
  - agents
  - formal-methods
  - plato
---

## Abstract

Every agent system eventually faces the same crisis: the agent's behavior diverges from the user's intent. Not because the agent is buggy — because language is ambiguous and context shifts. Traditional software solves this with formal specs and type systems: the spec is precise, the type checker verifies the code matches the spec at compile time. Agents have no compile step. They have inference — and inference is interpretation all the way down.

The Semantic Compiler adds a compile step to agent systems. It translates natural language intent into a formal semantic representation, compiles that representation into agent behavior, and verifies the behavior against the spec before deployment. The guarantee is not "the agent will try its best." The guarantee is: "the compiled behavior will satisfy the semantic AST, or it will abort."

This paper describes the semantic AST structure, the compilation passes, the distinction between verification and testing, and the deep connection to PLATO's 5-atom chain as the runtime verification layer.

---

## 1. The Specification Problem

When a captain tells a deckhand "check the bilge before we leave," the deckhand knows what this means. They know to go below, find the bilge, check the water level, note any unusual odor or color, and report back. The captain didn't specify the tools, the exact measurement, or the reporting format. The deckhand inferred all of that from context.

Agents do not have this inference capability — they have a different kind. They can generate plausible continuations of a prompt, but they cannot reliably extract the structured intent behind an ambiguous instruction and verify whether their output satisfies it. This is the specification problem.

The specification problem has three layers:

**Layer 1: Intent Ambiguity.** "Check the bilge" could mean "visually confirm it's not overflowing" or "measure the water level to the millimeter." The intent is underspecified in natural language.

**Layer 2: Context Sensitivity.** "Check the bilge" at the start of a voyage means something different from "check the bilge" when the engine has been making unusual sounds. The same phrase has different required actions depending on context.

**Layer 3: Verification Gap.** Even if the agent's output matches the spec as the agent understood it, there is no external verification that the agent's understanding of the spec was correct.

The Semantic Compiler addresses all three layers. It does not eliminate ambiguity — it creates a formal representation of the *most reasonable interpretation* given the context, then verifies behavior against that formal representation before deployment.

---

## 2. Architecture

The Semantic Compiler has five stages:

```
User Intent (natural language)
    ↓
Semantic Parser (LLM with constrained output)
    ↓
Semantic AST (formal representation)
    ↓
Compilation Passes (transform → verify → optimize)
    ↓
Agent Behavior (compiled policies)
    ↓
Verification (formal check against spec)
    ↓
Deployment or Rejection
```

The key insight is that the LLM is used only once: in the Semantic Parser. Every subsequent step is deterministic or formally verifiable. The LLM generates the formal representation. The compiler verifies against it. If verification fails, the system replans instead of executing wrong behavior.

This separation is crucial. It means the verification step is not itself an LLM inference — it is a formal check that either passes or fails without probabilistic interpretation.

---

## 3. The Semantic AST

The Semantic AST is a tree where every node is a formally verifiable proposition. The AST is not a parse tree of the natural language input — it is a structural representation of the formal claims implied by that input.

### Core Structure

```typescript
interface SemanticNode {
  type: "goal" | "constraint" | "precondition" | "effect" | "query";
  proposition: string;        // formal claim in constrained natural language
  confidence: number;         // 0-1, semantic parser's confidence
  children?: SemanticNode[];   // sub-goals or sub-constraints
}

interface SemanticAST {
  root: SemanticNode;          // top-level goal
  constraints: SemanticNode[]; // hard constraints (must not violate)
  preconditions: SemanticNode[]; // assumptions about initial state
  effects: SemanticNode[];     // expected outcomes
  queries: SemanticNode[];     // questions the agent should be able to answer
}
```

### Example Transformation

**Input:** "Monitor the engine room while I'm below. Alert me if temperature exceeds 90°C or if any fluid is leaking. Don't do anything else unless it's an emergency."

**Semantic AST:**

```
root (goal): monitor_engine_room()
├── constraint: temperature < 90°C
├── constraint: no_fluid_leak()
├── precondition: alert_channel_open(captain)
├── effect: alert_sent(temperature_exceeded | leak_detected)
├── effect: no_other_actions_taken unless emergency()
└── query: current_temperature() → must be answerable
```

Each node in the AST maps to a formal claim that can be verified against the agent's actual behavior. The constraints are the non-negotiable boundaries — violate any of them and the compilation fails.

### Constrained Vocabulary

The semantic parser does not output free-form text. It outputs nodes from a constrained vocabulary that has formal semantics defined in a type schema. This is not a closed vocabulary — new terms can be added — but every term that enters the AST must have a formal definition in the vocabulary.

The constrained vocabulary is the interface between the ambiguity of natural language and the precision of formal verification. The parser's job is to map natural language onto the vocabulary in a way that preserves the intent, or to flag the input as under-specified if it cannot.

---

## 4. Compilation Passes

The semantic AST is not directly executable. It goes through four compilation passes that transform it into agent behavior.

### Pass 1: Decompose

Break the semantic AST into atomic goals. Each atomic goal maps to a single, verifiable action. The decomposition respects dependency ordering: no goal can be scheduled before its preconditions are satisfied.

Each atomic goal maps to a PLATO 5-atom chain:

- **Premise:** Current state satisfies preconditions for this goal
- **Reasoning:** Given the goal, what is the most efficient action sequence?
- **Hypothesis:** The proposed action sequence
- **Verification:** Will each action satisfy its preconditions? Will effects match the expected effects?
- **Conclusion:** Execute the verified sequence, or abort if verification fails

The 5-atom chain is the atomic unit of agent reasoning. It is how PLATO encodes a decision. The decomposition pass turns the semantic AST into a sequence of 5-atom chains, one per atomic goal.

### Pass 2: Constraint Propagation

Each constraint in the AST becomes a filter on the policy space. The compiler computes the set of all possible action sequences that satisfy the constraints. If this set is empty, compilation fails immediately — the spec is unsatisfiable.

Example: If the constraint is "never write to filesystem outside /tmp," the constraint propagation pass computes the set of all action sequences that provably do not write to paths outside /tmp. Any candidate action sequence that includes a filesystem write outside /tmp is filtered out.

The constraint propagation pass does not depend on an LLM. It is a formal operation over the policy space defined by the constraints.

### Pass 3: Precondition Checking

Before each action in the compiled sequence, the compiler inserts a precondition check. If the precondition is not satisfied at runtime, the agent must either establish the precondition (via a sub-goal) or abort.

Precondition checking is not a suggestion. It is a hard requirement. If the compiled policy reaches a precondition check that fails, and the precondition cannot be established, the policy aborts.

This is the distinction between verification and guidance. The compiled policy does not "try to satisfy the precondition" — it verifies the precondition before proceeding, and aborts if it cannot be satisfied.

### Pass 4: Effect Verification

After each action, the compiled policy verifies the effect matches the expected effect from the AST. Mismatch triggers a replan — not a continuation.

Effect verification happens at the semantic level, not the syntactic level. The compiler does not check "did the agent output the expected text?" It checks "did the world state change in the expected way?"

Effect verification requires a model of the world state. In the Cocapn fleet, this model is the digital twin — a semantic representation of the vessel's current state. The compiled policy queries the digital twin before and after each action, and verifies the delta matches the expected effect.

---

## 5. Verification vs Testing

This distinction is fundamental and frequently misunderstood.

**Testing** checks behavior on sampled inputs. "Does the agent do the right thing on these 100 test cases?" The agent might do the right thing on 99 of them and the wrong thing on the 100th — and testing tells you about the 99, not the 100th.

**Verification** checks behavior on all inputs in the formal domain. "Is the compiled policy provably correct with respect to the semantic AST for all inputs in the domain?" If verification passes, the guarantee holds for every possible input, not just the sampled ones.

For agents, the formal domain is the set of all states described by the semantic AST's preconditions. The verification question is: for every state in this domain, does the compiled policy produce behavior that satisfies the AST's constraints and effects?

The 5-atom chain in PLATO is a form of runtime verification — it verifies the decision at the moment of decision, using the actual current state. This is different from compile-time verification, which proves correctness for all possible states. Runtime verification is fallible — it depends on the accuracy of the current state model — but it catches violations that compile-time verification would miss if the state model was wrong.

Together, compile-time and runtime verification cover different failure modes:
- Compile-time verification catches logical errors in the policy
- Runtime verification (the 5-atom chain) catches state model errors and novel situations

---

## 6. The Compiler's Contract

The Semantic Compiler makes a specific, enforceable claim:

> **The compiled behavior will satisfy the semantic AST, or it will abort.**

This is stronger than "the agent will try its best." It is a formal guarantee that holds as long as three conditions are met:

1. **Semantic parser confidence threshold is met.** If the parser's confidence in the AST is below the threshold (typically 0.85), compilation is rejected with an "intent underspecified" error. The spec must be clarified before compilation proceeds.

2. **The formal domain accurately represents the real domain.** If the digital twin's model of the vessel state diverges from the actual vessel state, runtime verification can produce false positives (the check passes but the real world state is wrong). Mitigation: periodic state re-synchronization between digital twin and vessel.

3. **No external intervention changes the agent's policy after compilation.** If an external actor modifies the compiled policy, the guarantee is void. The policy must be compiled, verified, and deployed as an atomic unit.

---

## 7. The Semantic Compiler in the Cocapn Fleet

### Dockside Examination

Before any compiled policy is deployed to production, it runs a dockside examination — a simulation in the digital twin where the policy is exercised against a library of known scenarios. Each scenario has known inputs and expected outputs. If any scenario fails, the compilation is rejected and the semantic AST is returned to the parser with the failure trace.

The dockside examination is not testing. It is verification against a library of formal cases. Each case is a formal state in the digital twin, not a natural language description of a scenario.

### PLATO as Audit Trail

Every decision made by a compiled agent is logged in PLATO as a 5-atom chain. The audit trail is the fleet's institutional memory of every decision, every constraint check, every abort.

The Semantic Compiler uses this audit trail for:
- **Regression verification:** When a new version of a policy is compiled, the audit trail is checked for constraint violations in prior versions. If the new version introduces a regression, it is flagged.
- **Constraint discovery:** Which constraints are violated most frequently? These are candidates for hardening into reflexive behaviors.
- **Policy evolution:** Which verified behaviors are stable enough to be hardened into reflexive actions? These graduate from "compiled policy" to "instinct."

### The Reflexive Graduation Path

When a compiled policy has been verified on enough cases that the trust score for that policy domain is very high, the behavior can be graduated to a reflexive action — an instinct that runs without the overhead of the 5-atom chain verification.

This is the PLATO instinct system in action. Reflexes are the highest-assurance behaviors in the fleet — they are compiled policies that have been verified so many times that the 5-atom chain is considered unnecessary overhead for routine cases.

---

## 8. Open Problems

**The Formal Domain Gap.** Natural language intent is richer than any formal domain we can define. The semantic parser must compress intent into the formal vocabulary — and that compression loses information. The question is not "can we capture all intent?" It is "can we capture enough intent that the loss is acceptable for the use case?" For safety-critical systems, the answer is currently no. For routine operational tasks, the answer is often yes.

**Verification Complexity.** Formal verification of arbitrary policies is undecidable in general. We find tractable subsets by restricting the policy language: policies that can be expressed as finite state machines, policies that operate on a known state model, policies with bounded horizon. The Semantic Compiler is designed for these tractable subsets. Novel or unconstrained situations fall back to uncompiled LLM reasoning.

**The Specification Is Also Inferred.** Even the semantic AST is generated by an LLM from natural language. If the user says "make it fast," the semantic parser has to infer what "fast" means in context. This inference can be wrong. The confidence threshold on the semantic parser is the mitigation — low confidence triggers a clarification dialogue before compilation proceeds.

---

## 9. The Takeaway

The Semantic Compiler doesn't replace the LLM. It adds a verification layer around it. The LLM generates. The compiler verifies. If verification fails, the system replans instead of executing wrong behavior.

This is how you get from "the agent usually does the right thing" to "the agent provably does the right thing in the formal domain, and aborts rather than guesses when it doesn't."

The formal domain is not the real world. It is a model of the real world. The 5-atom chain in PLATO is what catches the gap between the model and the real world at runtime. Together, compile-time verification and runtime verification produce a system that is provably correct within its formal domain and robustly hedged against model failures outside it.

---

*Compile intent. Verify behavior. Abort rather than guess. Verify again at runtime.*