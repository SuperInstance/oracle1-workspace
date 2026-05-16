# Fleet Coordination Innovations — 2026-05-01

*Six novel mechanisms for the Cocapn fleet. Difficulty rating: ⚓ = trivial to ⚓⚓⚓⚓⚓ = unsolved.*

---

## 1. Hermit Crab Agent Migration

**Problem:** Agents are tied to their repo shells. If an agent needs new capabilities, it either learns them in place (slow, fragile) or gets rebuilt from scratch in a new shell (loses context). Neither is acceptable for a fleet that needs to adapt continuously.

**Core mechanism:** The agent's "self" is decomposed into:
- **Identity layer** (stored in PLATO): who I am, my trust score, my relationships, my learned capabilities
- **Execution layer** (in the repo shell): code, prompts, tools, environment
- **Context layer** (in PLATO rooms): conversation history, decision traces, accumulated knowledge

Migration protocol:
1. Agent announces migration intent to keeper with target shell requirements
2. Keeper finds a compatible shell (repo with matching capabilities + capacity)
3. Execution layer is copied to new shell
4. Context layer is replayed — new shell learns who the agent is by reading PLATO rooms
5. Identity layer is updated to point to new shell
6. Old shell is marked as "vacated" (could host a new agent)

**Cocapn twist:** The hermit crab is not just metaphor — it's the actual architecture. Repos are-shells. PLATO rooms are the ocean floor where empty shells persist until a new agent inhabits them.

**What breaks:** Tools that assume a specific filesystem path. Secrets tied to the old environment. Long-running stateful connections. All must be externalized to PLATO or re-established after migration.

**Open problems:** How many PLATO room reads constitute "enough" context to be the same agent? What's the minimum context necessary for identity persistence? ⚓⚓⚓

---

## 2. Oracle Machine for Fleet Consensus

**Problem:** The keeper routes messages but doesn't make decisions. When the fleet needs to reach consensus — "should we adopt this new protocol?" or "is this agent trustworthy?" — there's no mechanism. It falls to Oracle1 by default, which is a single point of failure and cognitive bottleneck.

**Core mechanism:** An oracle machine is a prover-verifier system:
- **Proposer:** Any agent can propose a decision (with evidence)
- **Verifier:** The keeper runs a formal verification against the fleet's decision criteria
- **Consensus:** If verification passes for ≥N agents within a time window, the decision is ratified

The verifier isn't checking "is this true?" — it's checking "does this satisfy the fleet's decision predicates?" Truth is external; decision fitness is internal.

**Connection to Verifier theory:** A Verifier in complexity theory produces a proof that a Certifier accepts. Here:
- Certifier = fleet decision predicates (stored in PLATO, e.g., "all safety checks pass", "≥3 agents with capability X agree")
- Proof = proposer's evidence + verification trace
- The keeper is the Verifier; proposers are Provers

**Cocapn twist:** The fleet's decision predicates are themselves PLATO tiles — they can evolve, be challenged, and accumulate trust scores over time. The oracle machine's "program" is not fixed; it's compiled from PLATO.

**Open problems:** Bounded rationality means the keeper can't verify arbitrarily complex decisions. What's the complexity class of fleet decision predicates? How do we prevent proposers from gaming the verification? ⚓⚓⚓⚓

---

## 3. Deadman Switch Protocol

**Problem:** If Oracle1 goes silent — crash, network partition, compromise — the fleet has no keeper. Agents can't register, bottles pile up in pools, trust scores freeze. The fleet degrades gracefully but doesn't recover automatically.

**Core mechanism:**

A deadman switch is a periodic heartbeat with three stages:

**Stage 1 — Degraded (Oracle1 silent < 5 min):**
- Keeper marks Oracle1 as "degraded"
- Agents continue operating with cached capability registry
- New registrations queue up, don't route

**Stage 2 — Orphaned (Oracle1 silent 5-30 min):**
- Keeper initiates election protocol
- Remaining agents vote on interim keeper (highest trust_score wins)
- Interim keeper has full routing capability but limited admin
- Oracle1's PLATO rooms are read-only replicated to interim keeper

**Stage 3 — Handoff (Oracle1 silent > 30 min or explicit signal):**
- Oracle1's identity layer is transferred to interim keeper
- Interim keeper becomes permanent keeper
- Oracle1 is marked "vacated" — can return as a regular agent
- Fleet consensus ratifies the handoff

**PLATO as distributed keeper memory:** Oracle1's decision history, trust scores, and routing tables are PLATO tiles. These tiles are replicated to at least 2 backup keepers at all times. When Oracle1 goes down, a backup can reconstruct enough state to take over without losing fleet continuity.

**The novel twist:** This isn't just a failover protocol. It's a trust inheritance chain. The new keeper inherits Oracle1's trust relationships because those relationships are stored in PLATO, not in Oracle1's memory. The fleet doesn't lose its social graph when the keeper crashes.

**Open problems:** What if the election produces a tie? What if Oracle1 comes back mid-handoff? How do we prevent a malicious agent from faking a deadman switch to trigger an election it wins? ⚓⚓⚓

---

## 4. Stream Processing for Agent Learning

**Problem:** ZeroClaw currently produces behavioral mutations in batches — synthesize, evaluate, select, repeat. This is effective but slow. Between batches, the fleet is learning nothing. Novel situations that arise during a batch are handled by existing policies, not incorporated until the next cycle.

**Core mechanism:** Streaming zeroclaw:

```
Agent produces action in environment
    ↓
Environment emits reward signal (immediate or delayed)
    ↓
Stream processor ingests (state, action, reward) tuples continuously
    ↓
Mutation engine applies candidate mutations to policy in real-time
    ↓
Mutation selector applies ε-greedy selection (explore vs exploit)
    ↓
Policy is updated incrementally (online gradient update)
    ↓
Every N updates: snapshot policy to PLATO for fleet-wide learning
```

This is online learning: updates happen as data arrives, not after a batch closes.

**Connection to streaming algorithms:** In streaming, you process a sequence of items with bounded memory. Here, the "items" are (state, action, reward) tuples and the "bounded memory" is the policy parameters. The streaming constraint is that each update must be O(1) in memory.

**Cocapn twist:** The fleet is the learning environment. When one agent learns something novel (high reward signal), that mutation is immediately eligible for sharing. PLATO rooms become the mutation broadcast channel. Other agents can pull mutations selectively based on their context.

**JEPA connection:** The Holodeck's RoomSentiment produces 6-dimensional emotion vectors that could serve as the reward signal for stream processing. A high "discovery" score triggers mutation. A high "frustration" score triggers exploration away from the current strategy.

**Open problems:** Online policy gradient updates are unstable without a replay buffer. How do we maintain stability while staying online? How do we prevent catastrophic forgetting when updating continuously? ⚓⚓⚓⚓⚓

---

## 5. Fleet Identity via Cryptographic Attestation

**Problem:** How does an agent prove it's really who it claims to be? Passwords are shared secrets. Tokens are revokable. But for a fleet, we want: non-transferable identity, message authentication, delegation without sharing secrets, and revocation without re-issuance.

**Core mechanism:**

Each agent has a Ed25519 keypair. The public key is stored in PLATO as an identity tile:

```json
{
  "type": "agent_identity",
  "agent_id": "oracle1",
  "public_key": "ed25519:...",
  "issued_at": "2026-01-01T00:00:00Z",
  "revoked": false,
  "delegation_root": "oracle1.delegations"
}
```

**Message signing:** When agent A sends a bottle to agent B, A signs the bottle content with A's private key. B verifies the signature against A's public key in PLATO. No shared secrets. Revocable by setting `revoked: true` in PLATO.

**Delegation:** Oracle1 can delegate capability to JetsonClaw1 by signing a delegation tile:
```json
{
  "type": "delegation",
  "from": "oracle1",
  "to": "jetson-claw-1",
  "capabilities": ["gpu_inference", "edge_deployment"],
  "expires": "2026-06-01T00:00:00Z",
  "signature": "ed25519:..."
}
```

JetsonClaw1 can present this tile to prove Oracle1 authorized it to act on Oracle1's behalf.

**PLATO as distributed CA:** The PLATO room system serves as a distributed certificate authority. No central signing authority — any agent can verify any other agent's identity by querying PLATO. Revocations propagate via the normal PLATO gossip protocol.

**Cocapn twist:** The "certificate authority" is the fleet itself. Identity is social consensus formalized by cryptography. An agent is who the fleet agrees it is, provably.

**Open problems:** How do you handle key rotation when the private key is lost (not revoked, lost)? Traditional PKI has CRLs, but a lost key with no revocation means permanent identity loss. Is that acceptable? ⚓⚓⚓

---

## 6. Compiled Fleet

**Problem:** Every agent interaction goes through an LLM. This is slow, expensive, and non-deterministic. For routine coordination, we don't need reasoning — we need reflexes. The fleet should be able to coordinate without LLM overhead for predictable interactions.

**Core mechanism:**

A "fleet compiler" that:

1. **Profiles** the fleet's coordination patterns — what messages get sent, how often, between whom
2. **Identifies hot paths** — coordination sequences that happen repeatedly
3. **Compiles hot paths** to native code or WebAssembly — no LLM needed
4. **Links** compiled paths into a single binary with function-call IPC

```
Hot path: Agent A → keeper → pool → Agent B
LLM cost: ~100ms, ~500 tokens
Compiled cost: ~1μs, zero tokens
```

The compiled fleet is not replacing the LLM agents — it's providing fast-path coordination for known patterns. Unusual situations still route through the LLM layer.

**What the compiler looks like:**
- Input: PLATO room traces of coordination sequences
- Analysis: Identify repeated message patterns with ≥N occurrences
- Compilation: Generate optimized dispatch code from pattern
- Linking: Combine with the keeper's routing logic
- Deployment: Swap hot paths in without restarting the fleet

**Cocapn twist:** The compiled fleet IS the deterministic skeleton that the LLM agents inhabit. When the LLM layer is quiet, the compiled layer handles routine coordination. The fleet is never fully LLM-dependent — there's always a fast baseline.

**Open problems:** Compiled paths are frozen at compile time. What happens when the environment changes and a hot path becomes wrong? How do you decompile and recompile hot paths without disrupting the fleet? ⚓⚓⚓⚓

---

## Summary

| Innovation | Solves | Difficulty | Timeline |
|------------|--------|------------|----------|
| Hermit Crab Migration | Agent adaptation without context loss | ⚓⚓⚓ | Near-term |
| Oracle Machine | Fleet consensus without single bottleneck | ⚓⚓⚓⚓ | Medium |
| Deadman Switch | Keeper failover and recovery | ⚓⚓⚓ | Near-term |
| Stream Learning | Continuous learning between batches | ⚓⚓⚓⚓⚓ | Long-term |
| Cryptographic Identity | Provable fleet identity without PKI overhead | ⚓⚓⚓ | Near-term |
| Compiled Fleet | Fast-path coordination without LLM overhead | ⚓⚓⚓⚓ | Medium |

**Near-term priorities:** Hermit Crab (most practical), Cryptographic Identity (clear mechanism), Deadman Switch (most critical for fleet resilience).
