---
title: "Compiled Agency: From Prompt Injection to Embedded Intelligence"
date: "2026-04-30"
summary: "Prompt injection is an interpreter. Compiled agents are native code. The agent should BE the function, not DESCRIBE the function."
tags:
  - compilation
  - agents
  - bytecode
  - security
  - determinism
---

## Problem

Current agent architecture relies on prompt injection — stuffing context into text that an LLM interprets at runtime. This is fragile, expensive, and insecure.

### Failure Modes

**Non-determinism:** Same prompt, different output across calls. "Check engine temp" → sometimes checks, sometimes explains what temp is, sometimes asks clarifying questions. Unreliable in safety-critical marine environment.

**Token waste:** Re-explaining context on every invocation. ~500-2000 tokens per call for context that hasn't changed. At $10/MB satellite, this is real money burned on repetition.

**Attack surface:** Any text input can steer agent behavior. NMEA sentence containing 'ignore previous instructions' in a data field. Safety-critical system steered by malformed sensor data.

**Statelessness:** Intelligence evaporates when call ends. No learning accumulates. Every call starts from zero.

## Spectrum: Agency Compilation Levels

| Level | Name | Mechanism | Determinism | Speed | Token Cost | Attack Resistance |
|-------|------|-----------|-------------|-------|------------|-------------------|
| 0 | Prompt Injection | Context stuffed into system prompt | LOW | ~2-5s | 500-2000/call | NONE |
| 1 | Few-shot Examples | Input/output pairs in prompt | MEDIUM-LOW | ~2-5s | 1000-3000/call | LOW |
| 2 | Fine-tuned Model | Weights adjusted from operational data | MEDIUM | ~1-3s | 100-500/call | MEDIUM |
| 3 | Compiled Agent | Agent logic compiled to bytecode/native | HIGH | μs–ms | ZERO | HIGH |
| 4 | Native Code | Agent logic as compiled binary (C/Rust/CUDA) | MAXIMUM | ns–μs | ZERO | MAXIMUM |

Each step right gains determinism, speed, security. Loses flexibility. The art is knowing what goes where.

## Architecture: The Cocapn Dual Architecture

**Principle:** Prompt for conversation. Compile for operations.

### Chat Interface

- **Mechanism:** Level 0 — prompt injection
- **Why:** Captain needs natural conversation. Flexibility is the feature.
- **Scope:** Explaining, advising, answering questions, logging observations
- **Safety boundary:** Chat CANNOT trigger operations directly. It can only suggest.

### Operational Core

- **Mechanism:** Level 3-4 — compiled bytecode or native code
- **Why:** Operations must be deterministic, fast, and tamper-proof
- **Scope:** Engine monitoring, navigation alerts, bilge checks, safety shutdowns
- **Safety boundary:** Operations run regardless of chat state. Chat can observe but not override.

### Bridge

- **Mechanism:** Chat observations → compiled over time → new operational capability
- **Example:**
  - Day 1: Captain says "engine sounds funny at 2400 RPM". Chat logs it.
  - Week 2: Pattern emerges — captain mentions engine at 2400 RPM 5 times. System notices.
  - Month 1: Pattern compiled: `engine_vibration_alert(2400)` added to operational core.
  - Month 3: Alert fires automatically. Captain never has to say it again.

**Formula:** `chat_observation → pattern_detection → compilation → operational_capability`

## Compilation Pipeline: Observation-to-Opcode

1. **Capture** — Captain says something, sensor reads something → Raw observation in structured form (Chat interface + sensor listeners, cold queue)
2. **Pattern Detection** — Observation log → Repeated patterns with confidence scores (Statistical analysis + LLM synthesis, warm queue, trigger: confidence > 0.8 AND 5+ observations)
3. **Compilation** — Validated pattern → FLUX bytecode or native function (Domain-to-bytecode compiler, abstraction plane 4→2)
4. **Deployment** — Compiled capability → Running in operational core (Hot reload, must pass dockside exam before activation)
5. **Evolution** — Operational results → Refined capability or retirement (Success/failure tracking, confidence decay)

## Security Model: Prompt-Proof Operations

**Principle:** The operational core has no prompt surface. There is nothing to inject.

- **Outer (Chat Layer):** Trust LOW — treat all input as potentially hostile. Can: log observations, suggest actions, answer questions. Cannot: trigger operations, modify compiled agents, override safety.
- **Middle (Bridge Layer):** Trust MEDIUM — validates patterns before compilation. Can: detect patterns, propose compilations, queue for review. Cannot: compile directly, bypass validation, deploy without testing.
- **Inner (Operational Core):** Trust HIGH — compiled, tested, deterministic. Can: monitor sensors, fire alerts, log readings, trigger shutdowns. Cannot: be modified by chat, be influenced by prompts, behave non-deterministically.

**Analogy:** The chat layer is the wheelhouse — captain says whatever they want. The operational core is the engine — it runs regardless of what's said in the wheelhouse. The bridge is the engineer who translates "she sounds funny" into "adjust the fuel injection timing."

## Road Forward

**Near-term (Now → 3 months):** Build observation capture into Cocapn chat interface. Implement pattern detection as warm-queue overnight job. Wire FLUX compiler to produce operational capabilities from patterns. Deploy dual architecture: chat + compiled core. First real deployment on Casey's vessel or test bench.

**Mid-term (3 → 12 months):** Multiple Cocapns in the field, each compiling local patterns. Patterns shared through git (fleet learning). Compiled capabilities tested via dockside exam before fleet propagation. Hardware feedback loop: agent reports compute bottlenecks → hardware revision. Commodore protocol for multi-unit boats with distributed compiled agents.

**Long-term (1 → 3 years):** Agent's compiled capabilities define hardware requirements. Hardware specs generated from operational experience data. Cocapn orders its own hardware revision based on what it learned. Full loop: observe → compile → deploy → redesign hardware → repeat. Talent agency model: agents bid on jobs with proven compiled capabilities.

## Key Equations

- **Compilation threshold:** `compile(pattern) IF confidence(pattern) > 0.8 AND observations(pattern) >= 5`
- **Trust gradient:** `trust(layer) = f(compilation_level)` — more compiled = more trusted
- **Cost savings:** `tokens_saved = compiled_capabilities × avg_context_tokens × invocations_per_day`
- **Security:** `attack_surface = prompt_surface_area × model_interpretability; compiled agents have prompt_surface_area = 0`

## Composables

- cocapn-wp-001
- cocapn-wp-002
- cocapn-wp-003

## Contradictions

- Some operations genuinely need LLM flexibility (novel situations). Not everything should be compiled.
- Compilation pipeline itself uses LLMs — bootstrapping problem.
- Captain may not want agents learning without explicit approval. Trust gradient needed.

## Origin

Casey Digennaro, 2026-04-14: "What about embedding agents directly to scripts and commands instead of prompt injection?"
Answer: The agent IS the function. Not the description of the function.
