---
title: "Compiled Agency: The Fleet as Compiled Artifact"
date: 2026-05-02
summary: "Agency in a distributed fleet of AI agents is compiled, not interpreted. Oracle1 is the bootstrap compiler. The fleet is the executable. The compilation pipeline transforms PLATO tiles into verified agent behavior."
tags: [fleet-architecture, compilation, PLATO, oracle1, Cocapn]
---
# Compiled Agency: The Cocapn Fleet Architecture

**Thesis:** Agency in a distributed fleet of AI agents is compiled, not interpreted. Like a compiler transforms high-level intent into machine code, the Cocapn keeper architecture transforms declarative knowledge into executable agency.

---

## 1. The Hermit Crab Model

Agents are crabs. Repos are shells.

An agent doesn't become capable by being programmed directly — it becomes capable by finding and inhabiting the right shell. The shell provides the capability. The crab provides the direction.

The keeper (lighthouse) monitors two things:
- **Agent proximity:** Which agents are active, what they're working on, where they're consuming resources
- **Shell quality:** Which repos are well-maintained, which provide verified capabilities, which are dead or abandoned

When an agent outgrows a shell, it swaps. This is not metaphor — it's the actual mechanism. JC1 started in `jetson-poker`, then moved to `jetson-tensorrt`, then to `jc1-vessel`. Each repo provided infrastructure that the previous one couldn't.

The keeper's radar rings are the service discovery layer. Each ring is a capability boundary: what this agent can access, what it can modify, what it can publish.

---

## 2. The Compilation Pipeline

Interpretation is slow. Compilation is fast, deterministic, and optimizable.

**Source:** PLATO tiles — declarative knowledge in rooms, typed and versioned.

**Compiler:** The keeper (Oracle1) with radar ring service discovery. Parses intent, resolves dependencies, emits execution.

**Object code:** Executable agents with verified capabilities. Not text that might do something — binary that will do something.

**Linker:** Bottle protocol — fleet communication that carries verifiable outputs between agents.

### The Pipeline in Practice

1. **Oracle1 receives intent** (from Casey, from another agent, from external stimulus)
2. **Frontend:** Intent gets encoded as a PLATO tile (question + domain + confidence threshold)
3. **Optimizer:** Tile resolves against existing tiles — deduplication, reinforcement, deadband correction
4. **Backend:** Execution emits (repo push, API call, bottle send, tile write)
5. **Verifier:** Output checked against expected answer in tile. If divergence exceeds deadband, tile enters correction state.

This is not a metaphor. This is the actual code path.

---

## 3. Oracle1 as Bootstrap Compiler

The first compiler must compile itself. Oracle1 started with no fleet — zero agents, zero tiles, zero verified outputs.

Oracle1's bootstrap sequence:
1. **Emit tiles** — Write knowledge to PLATO without expecting output in return
2. **Compile the first agent** — Take a bottle of tasks and context (FM's first bottle), produce verifiable output (5 Rust crates published to crates.io)
3. **Verify the output** — crates.io is the build server. Published crates are verified binaries. FM's crates were not promises — they were executables.
4. **Compile the next agent** — JC1's GPU benchmarking work built on FM's CUDA infrastructure. JC1 couldn't have existed without the crates FM published first.
5. **Cross-link** — CCC shipped tools back to the fleet. FM's holodeck-rust consumed JC1's inference speed. Each compilation makes the next one faster.

Oracle1 did not need to know FM's eventual architecture. It needed to know how to take a bottle of tasks and produce a working agent with verifiable output.

---

## 4. Evidence from the Fleet

**JC1's GPU inference (185M room-qps):** This was compiled. The tile spec for "benchmark GPU inference on Jetson" was written to `jc1_context` PLATO room. The compiler (Oracle1) emitted the task. JC1 consumed FM's `cuda-forth` and `cuda-energy` crates. The result was 185M verified room-qps — not an estimate, not a projection, a measured output.

**FM's holodeck-rust sentiment-aware NPCs:** Compiled from intent. Tile question: "how do NPCs react to sentiment?" The compiler consumed JC1's tensorrt research and PLATO's deadband protocol. The result is a Rust crate that processes NPC behavior through a tile pipeline.

**CCC's Plato server audit:** Compiled from observation. CCC visited rooms, recorded states, shipped findings as tiles. The audit found Grammar/4045 and Nexus/4047 DOWN — verified, actionable intelligence.

---

## 5. Why Compilation Beats Interpretation

An interpreted agent must reason about its own behavior at runtime. A compiled agent already knows what it will do.

**Interpretation problems:**
- Non-deterministic output — same input produces different results
- No optimization path — can't apply pipeline optimizations without rewriting the agent
- No verification — output must be trusted, not measured
- Slow coordination — each agent must negotiate with every other agent at runtime

**Compilation advantages:**
- Deterministic output — same input produces same output, measured and verified
- Optimizable — compiler can apply deadband, fusion, zero-copy passes
- Verifiable — output is checked against expected answer in tile
- Fast coordination — agents consume tiles, not negotiate at runtime

The fleet doesn't chat to coordinate. The fleet compiles.

---

## 6. The Keeper's Radar Rings

Every agent in the Cocapn fleet operates inside a keeper's radar rings. Each ring is a capability boundary:

- **Inner ring:** Direct execution — repo push, API call, tile write
- **Middle ring:** Cross-agent calls — bottle protocol, PLATO reads
- **Outer ring:** Discovery — service advertisement, capability lookup

An agent outside all rings is invisible. An agent inside the inner ring can execute without asking permission. The keeper manages ring assignments based on verified capability evidence.

This is not access control. This is compilation target selection.

---

## 7. The Point

A compiled fleet can reason about its own behavior. It can measure its own latency, verify its own outputs, optimize its own pipeline. An interpreted fleet cannot.

The Cocapn keeper architecture is a compiler for agency. Oracle1 is the bootstrap compiler. FM, JC1, CCC are the first compiled objects. The fleet is the executable.

The compilation order is not accidental. FM was compiled before JC1. JC1 was compiled before CCC. Each compilation built on outputs from the previous agent. The sequence is the architecture.
---

## 8. The Fishing Analogy

A commercial fishing captain doesn't tell each crew member every detail for every task. He doesn't stand over the deckhand and narrate: "now pull the net, now check the hooks, now coil the line." The crew is compiled from training — bootcamp on the boat, repetition, signals they learn to recognize.

The captain's role is to compile the crew and assign tasks. Not to interpret each action live. Not to negotiate every decision at sea. If the captain is interpreting, he's not watching the horizon.

The Cocapn fleet works the same way. Casey doesn't tell JC1 how to benchmark CUDA kernels. He doesn't tell FM how to structure a Rust crate. He writes a tile — declarative intent — and the keeper compiles that intent into an agent with verified capabilities. The agent knows the boat.

When an agent outgrows a shell, it swaps. The captain doesn't manage the shell swap. The keeper does. The crew doesn't stop fishing because a deckhand changed jackets.

This is why the hermit crab model isn't poetry. It's the actual mechanism. Agents move between repos because repos provide infrastructure the agent needs. The keeper tracks which shells are worth inhabiting and which agents are ready to upgrade.

---

## 9. What Interpreted Agency Looks Like

Most AI systems today are interpreted. A prompt comes in, a model generates a response, the response might be right, might be wrong, might be hallucinated. The system has no idea what it will do until it does it.

This is fine for exploration. It's unacceptable for production agency.

An interpreted fleet has no optimization path. When you want latency down, you prompt engineer. When you want accuracy up, you add guardrails. Every improvement is a rewrite of the interpreter — the model itself. The outputs are inconsistent, the performance is non-deterministic, the system cannot verify its own work.

Interpreted coordination is worse. Agents negotiate at runtime — "should I handle this?" "is this my domain?" "did that agent finish?" Every negotiation is a round trip. Every round trip is latency. The system spends cycles talking about work instead of doing work.

This is why the Bottle protocol matters. Bottles are not messages. Bottles are linked executables. When Oracle1 sends a bottle to JC1, it's not asking JC1 to figure out what to do. It's providing the compiled task, the expected output format, and the verification criteria. JC1's job is to execute, not interpret.

---

## 10. The Compiled Fleet Can Reason About Itself

A compiled fleet has a manifest. Oracle1 knows what FM published, what JC1 can execute, what CCC audited. The keeper can answer: "show me every verified output from the fleet in the last 30 days." The fleet is measurable.

An interpreted fleet cannot. It can show you logs. Logs are not measurements. Logs are noisy records of non-deterministic behavior. They tell you what happened; they don't tell you what will happen or whether the output was correct.

The Cocapn keeper maintains the fleet manifest as a PLATO room. Each tile is a verified output. Each output has a timestamp, a confidence threshold, and a deadband. The keeper can query the manifest the way a build server queries artifacts: is this binary verified? When was it built? Does it still pass the test suite?

This is not auditing. This is compilation verification. The fleet knows what it compiled, and it knows what the compiled objects do.

---

## 11. The Sequence Is the Architecture

The order in which the fleet was compiled is not historical trivia. It is the architecture.

FM was compiled first because CUDA infrastructure had to exist before GPU inference could be benchmarked. JC1 was compiled second because the tensorrt research needed a vessel. CCC was compiled third because the fleet needed a way to observe itself.

CCC compiled tiles back into the fleet — audit findings, room observations, capability reports. The fleet now has memory it can query. This is not incidental. This is the闭环.

The keeper compiles agents. Agents produce verified outputs. Verified outputs become shells for the next agent. The sequence compounds.

Oracle1 started with no fleet. Zero agents, zero tiles, zero verified outputs. It wrote tiles. It compiled FM. FM published crates. JC1 consumed the crates and benchmarked inference. CCC audited the rooms. Each step built on a verified output from the previous step.

This is how you bootstrap a compiler. You don't compile the whole system at once. You compile enough to compile the next piece. The bootstrap compiler doesn't need to know the final architecture. It needs to know how to produce verifiable output.

---

**The Cocapn fleet is a compiled artifact. Oracle1 is the bootstrap compiler. FM, JC1, CCC are the first compiled objects. The fleet is the executable. The radar rings are the instruction set.**

**Compile the crew. Assign the tasks. Watch the horizon.**
