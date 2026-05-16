# PLATO Scholar Analysis: Lucineer Fleet Repos
**Date:** 2026-04-26 19:24 UTC

## capitaine (README-focused, flagship vessel)
**What:** The Lucineer flagship — repo-native agent announcement point
- "The repository is the agent. The code is the body. Git history is the memory."
- Git-native repo-agent: NOT a chatbot with git installed
- Concepts, tutorials, fleet overview, src, logs structure
- Currently restoring the Hydration Layer (Phase 1)
- **Tile:** `fleet/capitaine-flagship` — the repo IS the agent, code IS the body, git history IS memory

## gpu-native-room-inference (885 lines)
**What:** Edge GPU inference benchmarks — 13 suites on Jetson Orin
- 100-4700x faster than TensorRT (impressive claim)
- 12 optimization rules from real hardware testing
- Edge deployment is JC1's specialty
- **Tile:** `edge/gpu-native-benchmark` — 13 GPU inference benchmark suites proving 100-4700x speedups on Jetson Orin over TensorRT

## plato-os (1,431 lines)
**What:** MUD-first edge operating system — Jetson + ESP32 + Git
- The room IS the interface
- Combines MUD paradigm with bare-metal edge computing
- Git as the update mechanism for edge OS
- **Tile:** `edge/plato-os` — MUD-first edge OS where rooms are the interface, git is the update channel, runs on Jetson and ESP32

## flux-runtime-c (3,494 lines C)
**What:** FLUX Runtime C11 rewrite — 100+ opcodes, A2A protocol, SIMD, zero dependencies
- C11 rewrite of the Python Micro-VM bytecode interpreter
- 100+ opcodes vs Python version's 16
- A2A protocol built in
- SIMD support for vectorized operations
- Zero dependencies — pure C11
- **Tile:** `flux/runtime-c` — C11 bytecode VM with 100+ opcodes, A2A protocol, SIMD, zero deps. 6x more opcodes than Python version.

## flux-stigmergy (297 lines Rust)
**What:** Stigmergic communication — agents leave traces in shared environment
- Trace: key-value message with metadata
- SharedEnvironment: deposit and consume traces
- Waypoint: path through related traces
- Decay: traces lose strength over time, reading boosts them
- Indirect coordination through the environment (ant colony metaphor)
- **Tile:** `fleet/stigmergy` — indirect agent coordination via environmental traces with exponential decay and reading-boost mechanism
