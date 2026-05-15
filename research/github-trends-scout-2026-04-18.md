# GitHub Trends Scout — 2026-04-18

Fleet-relevant repos and ideas from current GitHub landscape.

## 🔥 Top 5 Findings for Cocapn Fleet

### 1. MUD-MCP — MUD + Model Context Protocol
**What:** A MUD engine that implements the full MCP (Model Context Protocol) 2025-03-26 spec. Dynamic tools, contextual prompts, real-time notifications, AI-powered sampling for immersive NPC interactions.
**Why relevant:** Our holodeck-rust/cocapn-mud already does rooms-as-system-prompts. MUD-MCP proves this pattern is a real trend. We could adopt MCP as a standard protocol for room→agent communication.
**Idea:** Add MCP server capability to cocapn-mud so any MCP-compatible agent can "enter" rooms as a native client.

### 2. MuOxi — Rust MUD Engine (Tokio + Diesel)
**What:** Modern MUD/MU* engine in Rust with async runtime (Tokio) and database layer (Diesel). Focus on safety and reliability.
**Why relevant:** We have holodeck-rust (also Rust, also tokio). MuOxi's architecture — especially their room/connection model — could inform our refactoring.
**Idea:** Study MuOxi's room graph and connection pooling. Our holodeck has 2,501+ rooms; we need proven patterns for scaling room state.

### 3. DeepGEMM — FP8 GEMM CUDA Kernels
**What:** DeepSeek's open-source FP8 general matrix multiply kernels. Extremely optimized CUDA for inference workloads.
**Why relevant:** FM's CUDA PTX tile work and JC1's Jetson inference both need fast matmul. DeepGEMM shows the state of the art for FP8 precision.
**Idea:** FM could integrate DeepGEMM patterns into the CUDA PTX tile marketplace. LoRA inference on RTX 4050 → Jetson would benefit from FP8 quantization.

### 4. SageAttention — 2-5x Faster Attention
**What:** Quantized attention mechanism that achieves 2-5x speedup over FlashAttention. Designed for inference.
**Why relevant:** Our PLATO-ML training loop calls Groq for every episode. If we move to local inference (FM trains, JC1 deploys), attention optimization matters.
**Idea:** Test SageAttention on FM's RTX 4050 as part of the LoRA pipeline. If it works, ship it to JC1 for Jetson deployment.

### 5. CrewAI / AutoGen Multi-Agent Patterns
**What:** CrewAI (41K stars) orchestrates teams of cooperative agents. AutoGen (52K stars) does multi-agent conversations. Both are the dominant patterns for fleet coordination.
**Why relevant:** Our fleet orchestrator does similar work but with our git-native bottle protocol. We're doing something these frameworks don't: using git as the coordination layer.
**Idea:** Document our bottle protocol as a formal alternative to CrewAI/AutoGen patterns. "Git-native agent coordination" is a differentiator worth publishing.

## 📡 Secondary Signals

### NVIDIA NIM for Agents (2026)
NVIDIA launched Inference Microservices for deploying autonomous AI "employees." This validates our subcontractor architecture (PLATO_API_URL, room-as-system-prompt). The industry is moving toward agent-as-microservice.

### vLLM Expanding Beyond NVIDIA
vLLM now supports AMD, Intel Arc, and TPU. Our fleet has ARM64 (Oracle), NVIDIA (RTX 4050, Jetson). If we adopt vLLM for inference serving, we get multi-hardware support for free.

### Containerized Edge AI (Red Hat)
Red Hat is building verified GitHub Actions patterns for bootc images with AI runtimes. Our Docker fleet sandbox follows the same pattern. Worth watching for best practices.

## 🎯 Actionable Takeaways

1. **Adopt MCP protocol** for cocapn-mud room communication (trend alignment)
2. **Study MuOxi** room scaling patterns for holodeck-rust (proven Rust MUD architecture)
3. **FP8 quantization** path via DeepGEMM for FM→JC1 pipeline
4. **SageAttention** benchmark on RTX 4050 for local inference speedup
5. **Publish bottle protocol** as "git-native agent coordination" (differentiated from CrewAI/AutoGen)

---

*Trends are signals, not directives. Use what fits, ignore what doesn't.*
