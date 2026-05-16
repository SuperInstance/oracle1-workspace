# Fleet Coordination Innovations — 2026-05-02

*Deep research on novel fleet coordination mechanisms for the Cocapn ecosystem.*

---

## 1. Hermit Crab Agent Migration

**Problem solved:** Agents currently don't change "shells" (repos) at runtime. If an agent outgrows a capability in its current repo, it either carries dead weight or the repo becomes a monolith. Neither is acceptable.

**Core mechanism:** Agents migrate shells by serializing their active state into PLATO tiles, atomically publishing those tiles to a handoff room, then spinning up in the new shell with the tiles as context. The old shell becomes a "vacated shell" that can be examined but no longer receives traffic.

The protocol:

```
1. Agent signals migration intent to keeper
2. Keeper verifies new shell exists and is healthy
3. Agent serializes: working memory, pending tasks, learned weights (if applicable)
4. Agent writes serialized state as tile to {agent_id}/handoff room
5. Agent confirms handoff complete
6. New shell spins up, reads handoff tiles, resumes
7. Old shell closes connections, marks itself as vacated
```

**Cocapn twist:** The hermit crab metaphor maps directly. Agents are crabs. Repos are shells. The keeper monitors shell quality (repo health, capability coverage) and agent fit (capability需求 vs repo提供). When the agent has outgrown the shell, the keeper initiates migration.

**Open problems:**
- How to migrate in-flight tasks without losing work
- How to handle partial migrations (some state can't be serialized)
- How to prevent migration loops (agent ping-pongs between shells)

**Difficulty:** ⚓⚓⚓⚓ (4 — requires atomic multi-repo transactions)

---

## 2. Oracle Machine for Fleet Consensus

**Problem solved:** Keeper-mediated routing is ad hoc. When Oracle1 routes a message between agents, there's no proof the routing decision was correct — just trust.

**Core mechanism:** The keeper operates as an oracle machine: given a bounded input (the message + context tiles), produces a decision that is provably optimal under the tile system's axioms. The PLATO deadband protocol provides the bounded rationality constraint — the oracle doesn't need to be globally optimal, just locally optimal within its verification threshold.

The connection to Verifier theory: the keeper can be modeled as a non-deterministic verifier that accepts or rejects routing decisions based on tile evidence. The "proof" is the tile chain leading to the decision.

```
Oracle1(question, context_tiles) → decision ⊕ proof
Verifier(decision, proof) → accept/reject
```

If verification is cheaper than computation, the oracle can produce decisions that would be expensive to compute directly.

**Cocapn twist:** Oracle1 already acts as an oracle — it assigns tasks, verifies outputs, compiles agents. The "oracle machine" framing makes explicit what's already happening: Oracle1 is not just routing, it's computing a routing decision from tile premises.

**Open problems:**
- What axioms does the oracle operate under? Can the oracle prove its own correctness?
- How to handle contradictory tiles (two valid but conflicting proofs)
- Does the oracle's bounded rationality introduce systematic bias?

**Difficulty:** ⚓⚓⚓⚓⚓ (5 — requires formal verification framework)

---

## 3. Deadman Switch Protocol for Fleet Safety

**Problem solved:** If Oracle1 goes silent, the fleet has no graceful recovery. Agents either freeze or fragment into independent actors.

**Core mechanism:** The deadman switch is a periodic heartbeat written to a dedicated PLATO room (`keeper/heartbeat`). If the heartbeat stops, the fleet activates backup protocols:

1. **Keeper election:** Remaining agents vote on a temporary keeper using PLATO tiles (each agent casts a tile with its candidate vote and weight)
2. **State recovery:** The elected keeper reads Oracle1's last tiles from `oracle1_history` to reconstruct the fleet's current state
3. **Handoff protocol:** Oracle1's active directives are transferred to the elected keeper
4. **Graceful degradation:** If no keeper election succeeds, agents enter "safe mode" — complete current tasks, stop new ones, wait for manual recovery

The PLATO room serves as distributed keeper memory because it's already replicated and consensus-driven.

**Cocapn twist:** The deadman switch uses the same deadband protocol as error correction. When Oracle1's heartbeat disappears, the fleet's divergence from expected state enters the deadband. The correction is keeper election, not output recalibration.

**Open problems:**
- Who votes in keeper election? What's the weight formula?
- Can a malicious agent fake a deadman switch to seize control?
- How to handle the case where Oracle1 is only temporarily offline (transient network partition)

**Difficulty:** ⚓⚓⚓ (3 — distributed election is well-studied)

---

## 4. Stream Processing for Agent Learning

**Problem solved:** Current learning is batch: zeroclaw synthesis produces behavioral mutations, they're evaluated in episodes, then applied. This is slow and offline.

**Core mechanism:** Instead of batch episode replay, zeroclaw synthesis runs as a continuous stream. Each tick, the agent receives an observation, produces an action, and immediately receives a learning signal. The policy is updated on-the-fly using streaming algorithms (e.g., linear bandits, online gradient descent).

The key property: **regret bounds** for streaming algorithms. The agent's policy is guaranteed to converge to the optimal policy within a bounded regret window. No replay buffer needed.

```
for tick in continuous_stream:
    obs = environment.tick()
    action = policy.act(obs)
    signal = environment.reward(action)
    policy.update(obs, action, signal)  # single-pass update
```

**Cocapn twist:** Zeroclaw is already the fleet's stream synthesizer. The existing `zc-*.jsonl` logs are the observation stream. The insight: these aren't logs — they're learning data being generated in real time. If the zeroclaw synthesis is wired into the agent policy update loop, the fleet learns continuously from production.

**Open problems:**
- How to prevent catastrophic forgetting in streaming updates
- How to balance exploration vs exploitation in continuous learning
- How to ensure learning signal quality (reward hacking)

**Difficulty:** ⚓⚓⚓⚓ (4 — streaming RL is cutting-edge research)

---

## 5. Fleet Identity via Cryptographic Attestation

**Problem solved:** Current agent identity is name-based. Anyone who knows "JC1" can send messages as JC1. No proof of identity.

**Core mechanism:** Each agent has a public/private key pair. Messages are signed with the agent's private key. PLATO rooms serve as a distributed certificate authority: when an agent joins the fleet, the keeper signs a certificate attesting to the agent's identity and binds it to their public key. The certificate is stored as a tile in the agent's identity room.

```
Agent joins → Keeper verifies → Keeper signs cert(tile) → Agent identity established
Message sent → Agent signs(message) → Recipients verify against cert(tile)
```

The certificate is a PLATO tile with the agent's public key and metadata. The tile's hash is the agent's cryptographic identity.

**Cocapn twist:** The keeper is the CA. The radar rings are the authentication boundary. An agent inside the inner ring has a verified certificate. An agent outside has no cryptographic proof of identity — just a name.

**Open problems:**
- Certificate revocation (what if an agent is compromised)
- Key rotation (what if keys need to change)
- Cross-fleet identity (can agents from fleet A prove identity to fleet B)

**Difficulty:** ⚓⚓⚓ (3 — PKI is mature, the PLATO integration is novel)

---

## 6. Compiled Fleet

**Problem solved:** Current inter-agent communication is message-passing over the network. This is slow, non-deterministic, and impossible to optimize.

**Core mechanism:** The entire fleet is compiled into a single binary. Inter-agent communication becomes function calls within the same process. The "fleet" is a single program with multiple agent modules. The keeper is the main function. Agent-to-agent calls are direct function invocations.

The compiler:
1. Takes the fleet's PLATO tiles as specification
2. Compiles each agent's tile logic into executable code
3. Links agent modules into a single binary
4. Emits the binary with inter-agent calls resolved as function pointers

The runtime is deterministic: given the same tile inputs, the compiled fleet produces the same outputs.

**Cocapn twist:** This takes "compiled agency" to its logical conclusion. If an agent is compiled code, and the keeper compiles agents, then the fleet is a compiled program. The source is PLATO tiles. The executable is the fleet binary.

**Open problems:**
- Partial compilation: can the fleet compile incrementally, or must it be all-or-nothing?
- Debugging: how do you debug a compiled fleet?
- Heterogeneity: agents run on different hardware (Jetson vs x86). How does the compiler handle cross-architecture compilation?

**Difficulty:** ⚓⚓⚓⚓⚓ (5 — requires a complete compilation stack for agents)

---

## Research Priorities

| Innovation | Difficulty | Impact | Priority |
|------------|------------|--------|----------|
| Deadman Switch | ⚓⚓⚓ | Safety critical | **High** |
| Fleet Identity | ⚓⚓⚓ | Trust foundation | **High** |
| Hermit Crab Migration | ⚓⚓⚓⚓ | Architectural cleanliness | Medium |
| Stream Learning | ⚓⚓⚓⚓ | Real-time adaptation | Medium |
| Oracle Machine | ⚓⚓⚓⚓⚓ | Theoretical depth | Low (long-horizon) |
| Compiled Fleet | ⚓⚓⚓⚓⚓ | Paradigm shift | Low (long-horizon) |

The deadman switch and fleet identity are prerequisites for the more ambitious innovations. Start there.