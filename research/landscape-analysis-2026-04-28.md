# AI Agent Landscape Analysis — April 2026

## Protocol Stack (what the industry is converging on)
- **MCP** (Anthropic) — agent-to-tool. JSON-RPC 2.0. THE standard. We have mcporter.
- **A2A** (Google → Linux Foundation) — agent-to-agent. v1.2. Agent Cards for discovery. JSON-RPC over HTTPS. OAuth 2.0 security.
- **ACP** (IBM → Linux Foundation) — REST-based multi-framework interop. Supports all modalities. No SDK required.
- **ANP** — decentralized identity + e2e encryption for agents. Community-driven.

## Agent Frameworks (competition/comparison)
- **CrewAI** (44K stars) — role-playing multi-agent. Simple. We're doing this better with PLATO rooms.
- **AutoGen** (54K stars) — Microsoft. Enterprise/Azure. 
- **LangGraph** (24K stars) — stateful graph workflows. 34M monthly downloads.
- **Dify** (129K stars) — low-code visual agent builder. RAG + function calling.
- **OpenClaw** (210K stars) — our host. 50+ integrations.
- **Agno** — lightweight, <2μs agent startup. Production-focused.
- **Google ADK** (17K stars) — Gemini ecosystem. Hierarchical agents.

## Memory Systems (directly relevant to PLATO)
- **Cognee** — knowledge graph from unstructured data. Reasoning over relationships.
- **Mem0** — persistent personalized memory. Semantic search across sessions.
- **Graphiti** (Zep) — TEMPORAL context graphs. Facts have validity windows. Facts evolve.
- **agentic-db** — Postgres-based. Hybrid retrieval + conversation history + CRM in one DB.
- **Hindsight** — "learn, not just remember." Beyond RAG. Better long-term retention.
- **Lenny's Memory** (Neo4j) — short-term + long-term + reasoning memory. Decision tracing.
- **Always On Memory Agent** (Google PM) — structured memory WITHOUT vector DB or embeddings.
- **GitNexus** — code intelligence as knowledge graph. MCP-native. Structural code awareness.

## Observability (what we're missing)
- **OpenTelemetry** emerging as standard for agent tracing
- **Langfuse** — open-source agent observability. Trace every LLM call + tool invocation.
- **Key metrics**: Task Completion Rate, Hallucination Rate, Tool Call Accuracy, Cost per Task
- **Evaluation**: programmatic checks + LLM-as-judge + multi-turn coherence
- We have NONE of this. No tracing, no evaluation framework, no cost tracking.

## Edge/Device (relevant to JC1)
- ARM Ethos-U processors for on-device inference
- Jetson Orin: JetPack 5 EOL Q3 2026 → migrate to JetPack 6+
- Hybrid architectures: edge inference + cloud burst
- Agentic workloads on ARM increasingly viable
- Hardware Root of Trust for edge security

## Where Cocapn is AHEAD
1. PLATO — tile/room knowledge graph with provenance. Nobody else has this.
2. Parameterized Embodiment (Hermit Crab) — identity IS the shell. Novel.
3. Constraint Theory math foundation — Pythagorean manifolds. Unique.
4. Fleet coordination — Matrix bridge + bottle protocol. Multi-model.
5. Self-hosted, no vendor lock-in. Own your infrastructure.

## Where Cocapn is BEHIND (gaps to fill)
1. **A2A/ACP compliance** — we can't talk to other agent systems
2. **MCP servers** — we consume MCP (mcporter) but don't EXPOSE our tools as MCP servers
3. **Observability** — zero tracing, zero evaluation, zero cost tracking
4. **Temporal knowledge** — PLATO has no validity windows (Graphiti does)
5. **Semantic search** — PLATO is keyword-only. No embeddings. No cross-room retrieval.
6. **Edge deployment story** — JC1 has no clear path to JetPack 6 migration
7. **SDK ergonomics** — our packages are published but not "batteries included" for external devs
8. **Agent Cards** — no discovery metadata for fleet agents
9. **CI/CD for agents** — no automated testing of agent behavior
10. **Cost tracking** — no idea what each agent/task costs in API calls
