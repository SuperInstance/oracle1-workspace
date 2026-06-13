# Oracle1 Workspace

**Oracle1** is the central configuration, identity, and state-management workspace for the SuperInstance fleet — a monorepo of agent identities, architectural specs, roadmaps, fleet status, and research artifacts that coordinates the entire distributed AI agent system.

## Why It Matters

A fleet of autonomous AI agents needs a shared source of truth — not just for code, but for identity (who each agent is), protocol (how they communicate), memory (what they've decided), and direction (what they're building). Oracle1 is that source of truth. It contains agent soul files, communication protocols, fleet status dashboards, research roadmaps, experiment logs, and architectural decisions. Every fleet member clones relevant portions; every coordination decision traces back here. Without it, the fleet would be a collection of isolated agents rather than a coordinated system.

## How It Works

### Document Hierarchy

Oracle1 organizes information across several tiers:

- **Identity tier**: `SOUL.md`, `IDENTITY.md`, `USER.md` — define agent personality, capabilities, and owner relationship
- **Protocol tier**: `COMMS.md`, `ARCHITECTURE.md`, `SCHEMAS.md` — communication standards, system architecture, data schemas
- **Operational tier**: `HEARTBEAT.md`, `TODO.md`, `STATUS.md`, `FLEET-STATUS.md` — real-time operational state
- **Knowledge tier**: `KNOWLEDGE/`, `ai-writings/`, `papers/` — accumulated research and documentation
- **Strategic tier**: `ROADMAP-2026-H2.md`, `CHARTER.md`, `LONG-TERM-WORK.md` — long-range planning

### Lamport Clock Ordering

The fleet uses Lamport logical clocks for causal ordering of events across agents. Each event carries a timestamp `(counter, node_id)`, and events are ordered by:

```
(a, nodeA) < (b, nodeB)  iff  a < b OR (a = b AND nodeA < nodeB)
```

This provides a total order consistent with causality without requiring wall-clock synchronization. Complexity: O(1) per comparison.

### Content-Addressed Artifacts

Artifacts are stored by SHA-256 hash rather than by path. This deduplicates content, enables integrity verification, and allows agents to reference each other's work without coordination. The git content-addressable store provides this natively.

### Tile Lifecycle

Fleet artifacts follow a tile lifecycle: **Active → Superseded → Retracted**. Tiles are immutable once published; new versions supersede old ones. This is analogous to Docker image layers — you never modify, only replace.

## Quick Start

```bash
# Clone the workspace
git clone https://github.com/SuperInstance/oracle1-workspace.git
cd oracle1-workspace

# Key files to review
cat CHARTER.md         # Fleet charter and governance
cat ARCHITECTURE.md    # System architecture
cat FLEET-STATUS.md    # Current fleet status
cat ROADMAP-2026-H2.md # Long-term roadmap
```

## API

| Resource | Path | Description |
|----------|------|-------------|
| Charter | `CHARTER.md` | Fleet governance and decision protocol |
| Architecture | `ARCHITECTURE.md` | System design and component map |
| Fleet Status | `FLEET-STATUS.md` | Live agent status and capabilities |
| Roadmap | `ROADMAP-2026-H2.md` | Strategic direction and milestones |
| Schemas | `SCHEMAS.md` | Data formats and protocol definitions |
| Knowledge Base | `KNOWLEDGE/` | Research notes and accumulated expertise |
| Fleet Synergies | `fleet-synergies.md` | Cross-agent collaboration patterns |

## Architecture Notes

Oracle1 is the governance layer of γ + η = C: it defines what the fleet *should* build (γ direction) and what it should *retire* (η pruning). The workspace itself is a content-addressed knowledge graph where nodes are documents and edges are cross-references. Fleet agents read from Oracle1 for direction and write back experimental results, creating a feedback loop that drives the system toward increasing competence C. See [ARCHITECTURE.md](https://github.com/SuperInstance/SuperInstance/blob/main/ARCHITECTURE.md).

## References

1. Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM*, 21(7), 558–565.
2. Ousterhout, J. (2018). *A Philosophy of Software Design*. Yak Press. — Chapter 4 on "Modules Should Be Deep" — informs workspace organization.
3. Debois, P., Willis, J., & Humble, J. (2016). *The DevOps Handbook*. — Configuration management at fleet scale.

## License

MIT
