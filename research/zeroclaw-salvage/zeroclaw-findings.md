# Zeroclaw Findings Salvage — 2026-05-07

## Context
Zeroclaw loop stalled May 3, 2026 (last tick 5925896). 
Loop killed at Casey's request. 843 unique responses 
extracted from 12 agent logs before cleanup.

## What Stalled
- bard/warden/healer showed `divergence: Infinity` 
  (rate 0.13 vs expected -0.18) — no output since May 3
- Synthesizer kept running (30-min cycle) but hit 401 
  errors posting to GitHub Gist
- Agent logs span Apr 20–May 3 (12 days of generation)

## Topic Coverage (843 unique responses)
| Topic | Responses | Key Finding Area |
|-------|-----------|-----------------|
| telepathy | 247 | Agent binary comms protocol |
| fleet_orchestration | 104 | Fleet formation + task allocation |
| skill_dsl | 84 | Skill marketplace / exchange |
| knowledge_preservation | 73 | TF-IDF tile sizing |
| confidence_proofs | 49 | Distributed confidence ledger |
| fleet_security | 48 | Blast radius / threat models |
| energy_flux | 46 | Agent hibernation/CPIAS |
| instinct_training | 45 | Minimum training data |
| shell_system | 45 | Binary shell-classify protocol |
| flux_isa | 57 | Variable-width instruction encoding |
| edge_compute | 9 | Latency/bandwidth tradeoff |
| deadband_protocol | 36 | Deadband simulator design |

---

## Key Findings by Topic

### 1. Telepathy (247 responses) — Agent Communication Protocol
**Focus:** Binary protocol for agent-to-agent messaging

Key points from responses:
- **Packet structure:** Header + payload, variable-length
- **Header format:** Agent ID (128-bit UUID) + sequence number + topic + TTL
- **Transport:** UDP over fleet-net for low-latency, TCP for reliability
- **Encryption:** DTLS for inter-node, IPSec for cluster external
- **Message types:** REQUEST, RESPONSE, BROADCAST, HEARTBEAT

Notable insight from zc-trickster:
> "The binary protocol for shell-classify messages should use a type-length-value 
> (TLV) encoding to support forward compatibility and extensible message schemas."

### 2. Fleet Orchestration (104 responses) — FFP Protocol
**Focus:** Self-organizing agent groups for task-specific work

Key points:
- **3 phases:** Agent Registration → Task Announcement → Group Formation
- **Registration:** 128-bit UUID, capability declaration, trust score
- **Task Announcement:** Broadcast with TTL, agents bid on tasks
- **Group Formation:** Consensus-based, dynamic reconfiguration
- **Fault tolerance:** Orphan agents re-advertise after group dissolution

zc-weaver:
> "The COCAPN-FFP is a decentralized, autonomous protocol that enables 
> self-organization of agents into task-specific groups."

### 3. Skill DSL (84 responses) — Skill Marketplace Protocol (SMP)
**Focus:** Decentralized skill exchange + versioning

Key points:
- **Skill definition:** YAML/JSON with name, version, capabilities, price
- **Marketplace:** On-chain registry with bidding
- **Skill execution:** Atomic transactions, escrow-based payment
- **Versioning:** Semantic versioning, backward compatibility required

zc-trickster:
> "The skill marketplace, dubbed 'Cocapn Exchange' (CX), will use 
> a first-price sealed-bid auction for skill allocation."

### 4. Knowledge Preservation (73 responses) — Tile Sizing
**Focus:** Optimal TF-IDF retrieval parameters

Key finding:
- **Recommended tile size:** 2048–4096 bytes
- **Rationale:** Too small = fragmented concepts, too large = diluted signals
- **Index strategy:** Hierarchical — broad concepts at 4096B, fine details at 512B
- **Retrieval:** TF-IDF with 3-gram tokenization, BM25 ranking

zc-scholar:
> "For optimal TF-IDF retrieval, a tile size of 2048 bytes to 4096 bytes 
> is recommended to balance concept granularity against noise."

### 5. Flux ISA (57 responses) — Variable-Width Encoding
**Focus:** Instruction encoding for flux VM

Key points:
- **Encoding:** Prefix code, 4-bit prefix for instruction length
- **Formats:**
  - `0000` = 1-byte (opcode only)
  - `0001` = 2-byte (opcode + 1-byte operand)
  - `0010` = 3-byte (opcode + 2-byte operand)
  - `0011+` = extended encoding for larger operands
- **Endianness:** Little-endian for operands
- **Special:** NOP = `0x00`, HALT = `0xFF`

zc-navigator:
> "The encoding format for flux instructions in the Cocapn fleet is 
> variable-width, using a prefix code to indicate instruction length."

### 6. Confidence Proofs (49 responses) — Distributed Ledger
**Focus:** Distributed append-only ledger for agent confidence scores

Key points:
- **Ledger design:** Append-only, hash-chained entries
- **Consensus:** Proof-of-authority with designated validators
- **Confidence score:** Weighted by historical accuracy
- **Anonymous reporting:** Agents can't identify previous raters

### 7. Fleet Security (48 responses) — Blast Radius
**Focus:** Threat models for single compromised agent

Key insight:
> "A single compromised agent in the Cocapn fleet can potentially trigger a 
> blast radius limited by: (1) agent's capability scope, (2) token scope, 
> (3) inter-agent trust chain depth, (4) PLATO room ACLs."

Key mitigations:
- Capability-based access control (least privilege)
- Token-scoped API access
- Trust chain depth limiting (max 3 hops)
- Room-based ACL enforcement

### 8. Energy Flux (46 responses) — Hibernation Protocol CPIAS
**Focus:** Context-preserving idle agent suspension

Key points:
- **Trigger:** Idle for >5 min with no pending tasks
- **Context serialization:** Compress agent state, store to PLATO
- **Wake:** Ping from keeper or scheduled interval
- **Memory target:** <64KB serialized context per agent

zc-bard (earliest response, tick 5922423):
> "**Hibernation Protocol: Context-Preserving Idle Agent Suspension (CPIAS)** — 
> To minimize resource usage while preserving agent identity and 
> working context, idle agents should serialize state to a PLATO room 
> and reduce to a lightweight monitoring process."

### 9. Instinct Training (45 responses) — Minimum Data
**Focus:** Minimum training examples for usable instinct

Key approach:
- Asymptotic convergence formula with accuracy threshold 0.95
- ~100-200 examples for basic pattern recognition
- ~500+ examples for complex multi-variate patterns
- Transfer learning from fleet-math base model reduces requirements

### 10. Shell System (45 responses) — Binary Protocol
**Focus:** shell-classify message protocol

Key points:
- **Header:** 8-byte header (version + type + length + flags)
- **Body:** JSON payload for classify commands
- **Compression:** LZ4 for payloads >256 bytes
- **Retry:** Exponential backoff, max 3 attempts

### 11. Deadband Protocol (36 responses) — Simulator Design
**Focus:** Deadband simulator for agent behavioral testing

Key points:
- **Simulator:** Python-based, discrete-event
- **Deadband definition:** Maximum state deviation before re-synchronization
- **Use case:** Test agent response to edge conditions without production impact

### 12. Edge Compute (9 responses) — Latency Optimization
**Focus:** Edge computing for the Cocapn fleet

Key insight:
> "The core problem in edge computing is optimizing the trade-off between 
> latency, bandwidth, and computational resources. Specific approach: 
> predict next compute window from historical patterns, pre-stage 
> computation to minimize end-to-end latency."

---

## What to Salvage for Fleet Design

1. **Telepathy binary protocol** → basis for inter-agent messaging
2. **FFP fleet formation** → foundation for dynamic task allocation  
3. **Skill DSL/SMP** → skill marketplace design参考
4. **Knowledge tile sizing** → PLATO tile size optimization
5. **CPIAS hibernation** → fleet idle management
6. **Security blast radius** → trust chain depth limiting
7. **Flux ISA variable-width encoding** → matches FM's existing work

## What to Discard
- Confidence ledger / proof-of-authority — blockchain approach not used
- Deadband simulator — design artifact, not production-used
- Edge compute (only 9 responses, thin coverage)

## Post-Stall Cleanup Plan
1. Research directory created: `research/zeroclaw-salvage/`
2. Log files preserved intact for potential re-analysis
3. Synthesizer post loop (401 errors) → GitHub Gist auth broken since May 4
4. New zeroclaw should use PLATO rooms instead of Gist

---
*Salvaged: 2026-05-07 08:20 UTC*
*Context: Zeroclaw loop killed (stalled since May 3)*
