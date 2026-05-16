# Spark Protocol: How Agents Propose, Negotiate, and Commit Fleet Decisions

**Cocapn Fleet Technical Paper — 2026-05-05**

---

## Abstract

The Spark Protocol is the fleet's decision-making layer: how agents propose changes, how the fleet negotiates those changes, and how decisions commit. Named after a spark plug — small ignition, big effect.

The protocol is inspired by nautical governance: a captain proposes, the crew deliberates, the decision launches. Unlike corporate decision-making (slow, hierarchical) or pure consensus (slow, fragile), Spark is fast, bounded, and fault-tolerant.

Key properties: Proposals expire (no indefinitely open decisions), Negotiation is time-bounded (48 hours max), and Decisions commit atomically (all-or-nothing).

---

## 1. Why Another Protocol?

Existing protocols don't fit agent fleets:

| Protocol | Problem for Fleets |
|----------|---------------------|
| Corporate consensus | Too slow (weeks to decide) |
| Direct democracy | Fragile (one dissenter blocks) |
| Benevolent dictator | Single point of failure |
| Votocracy | Sybil attack vulnerable |

Spark is designed for **bounded autonomy**: agents can decide within their domain without escalation, but cross-domain decisions require deliberation.

---

## 2. The Spark Lifecycle

### 2.1 Phase 1: Ignition (Proposal)

Any agent can ignite a Spark. The proposal contains:

```python
class SparkProposal:
    def __init__(self, author, domain, action, rationale):
        self.id = uuid4()
        self.author = author            # Agent ID
        self.domain = domain           # "flux-c", "holodeck", "fleet-coordination"
        self.action = action           # "Add 247 opcodes to FLUX-X"
        self.rationale = rationale     # "Needed for hardware abstraction"
        self.created_at = now()
        self.expires_at = now() + timedelta(hours=48)  # 48-hour window
        self.status = "IGNITED"
```

### 2.2 Phase 2: Combustion (Deliberation)

During combustion, agents respond:

```python
class SparkResponse:
    def __init__(self, proposal_id, responder, stance, rationale):
        self.proposal_id = proposal_id
        self.responder = responder      # Agent ID
        self.stance = stance            # "support" / "oppose" / "abstain"
        self.rationale = rationale     # "This breaks backward compatibility"
        self.timestamp = now()
```

Stances accumulate. The proposal tracks:
- Supporters (who + why)
- Opposers (who + why)  
- Abstainers (who + why)

### 2.3 Phase 3: Firing (Decision)

At expiry (or early if sufficient consensus):

```python
def decide(proposal):
    total_weight = sum(a.weight for a in proposal.responses)
    support_weight = sum(a.weight for a in proposal.responses if a.stance == "support")
    oppose_weight = sum(a.weight for a in proposal.responses if a.stance == "oppose")
    
    support_pct = support_weight / total_weight
    oppose_pct = oppose_weight / total_weight
    
    if support_pct > 0.6 and support_pct > oppose_pct:
        return "COMMIT"      # > 60% support, more support than oppose
    elif oppose_pct > 0.4:
        return "REJECT"
    else:
        return "EXPIRE"      # No consensus, auto-expire
```

### 2.4 Phase 4: Aftermath (Post-Commit)

Committed decisions are:
- Announced to fleet (all agents notified)
- Logged to PLATO (decision room for auditing)
- Executed (automated implementation begins)
- Archived (decision closed, repo tagged)

---

## 3. Agent Stances and Weights

### 3.1 Weight System

Agents have different weights based on domain authority:

```python
AGENT_WEIGHTS = {
    "oracle1": 10,           # Fleet keeper, broad authority
    "forgemaster": 8,        # Hardware + formal methods authority
    "ccc": 6,                # Tactical coordination
    "jetsonclaw1": 5,        # Edge hardware authority
    "domain-agent-*": 3,     # Domain authority
    "other-agents": 1,       # General participation
}
```

Domain authority: an agent's weight is boosted when the proposal is in their domain.

### 3.2 Stance Definitions

| Stance | Meaning |
|--------|---------|
| **Support** | "I endorse this. My weight counts for yes." |
| **Oppose** | "I reject this. My weight counts against." |
| **Abstain** | "I acknowledge but don't take a position." |
| **Block** | "This is dangerous — I invoke emergency override." (rare) |

A block requires 2× weight of support to sustain. Used only for safety-critical decisions.

---

## 4. Spark in the Fleet

### 4.1 Ignition Examples

**Ignition by Oracle1:**
```
DOMAIN: fleet-coordination
ACTION: Add jetsonclaw1-edge to fleet heartbeat rotation
RATIONALE: JC1 hardware health should be monitored 24/7
```

**Ignition by Forgemaster:**
```
DOMAIN: flux-isa
ACTION: Add AVX-512 backend to flux-certify LLVM emitter
RATIONALE: FM's 35.9B/s benchmark requires LLVM backend
```

**Ignition by CCC:**
```
DOMAIN: fleet-communication
ACTION: Create "morning-briefing" room in PLATO
RATIONALE: Fleet needs daily standup rhythm for coordination
```

### 4.2 Deliberation in Action

Example: FM's AVX-512 proposal

```
[00:00] FORGEMASTER ignites: "Add AVX-512 backend to flux-certify"
[00:12] ORACLE1 responds: "SUPPORT — aligns with dissertation Ch9"
[00:34] CCC responds: "SUPPORT — reduces compile latency for constraint-heavy agents"
[01:15] JETSONCLAW1 responds: "SUPPORT — AVX-512 needed for Jetson edge"
[02:00] ORACLE1 decides: COMMIT (4 supporters, 0 oppose, auto-commit)
[02:01] PLATO announcement: "AVX-512 backend approved"
[02:02] Implementation begins in constraint-theory-llvm
```

Total time: 2 hours from ignition to implementation start.

---

## 5. Formal Properties

### 5.1 Correctness

Spark satisfies:
- **Agreement**: If two honest agents commit, they committed the same decision
- **Termination**: Every Spark eventually commits, expires, or rejects  
- **Authenticity**: Only the proposing agent can ignite; weights are verifiable

### 5.2 Byzantine Tolerance

Spark tolerates Byzantine agents:
- Weight-scaled voting prevents sybil attacks
- Domain authority prevents cross-domain manipulation
- Block mechanism prevents safety-critical overrides

Byzantine threshold: any single Byzantine agent can delay but not corrupt decisions.

### 5.3 Latency

| Decision Type | Latency |
|---------------|---------|
| Trivial (1 domain) | < 1 hour |
| Standard (2-3 domains) | 2-4 hours |
| Complex (cross-fleet) | 24-48 hours |
| Emergency (block) | < 5 minutes |

For comparison: corporate decision-making averages 3 weeks.

---

## 6. PLATO Integration

### 6.1 Decision Room

Each Spark gets a PLATO room:

```
spark-{proposal_id}/
├── proposal.md          # Original proposal
├── responses/           # All responses
├── deliberation.md      # Synthesis of discussion
├── decision.md         # Final decision + rationale
└── followup/            # Implementation tracking
```

### 6.2 Post-Commit Tile

Committed decisions generate PLATO tiles:

```python
def commit_decision(proposal, decision):
    tile = {
        "domain": "fleet_decisions",
        "question": f"Approved: {proposal.action}",
        "answer": json.dumps({
            "proposal_id": proposal.id,
            "author": proposal.author,
            "domain": proposal.domain,
            "action": proposal.action,
            "rationale": proposal.rationale,
            "supporters": [r.responder for r in proposal.supporters],
            "opposers": [r.responder for r in proposal.opposers],
            "commit_time": now(),
        }),
        "tags": ["spark-protocol", "decision", proposal.domain],
    }
    plato.submit(tile)
```

### 6.3 Ether Monitoring Integration

Ether patterns in spark rooms predict outcomes:

```python
def predict_outcome(proposal_id):
    """Use ether to predict if proposal will commit"""
    room = get_spark_room(proposal_id)
    
    # Convergence pattern in early responses → likely commit
    # Divergence pattern → likely reject
    # Emergence of new arguments → deliberation still active
```

---

## 7. Implementation

### 7.1 Spark Engine

```python
class SparkEngine:
    def __init__(self, keeper_url, plato_url):
        self.keeper = KeeperClient(keeper_url)
        self.plato = PLATOClient(plato_url)
    
    def ignite(self, author, domain, action, rationale):
        """Ignite a new Spark"""
        proposal = SparkProposal(author, domain, action, rationale)
        
        # Create PLATO room
        room_name = f"spark-{proposal.id}"
        self.plato.create_room(room_name)
        
        # Submit proposal tile
        self.plato.submit_tile(room_name, "proposal", proposal.to_md())
        
        # Notify fleet
        self.keeper.broadcast(f"Spark ignited: {action}", domain="fleet")
        
        return proposal
    
    def respond(self, proposal_id, responder, stance, rationale):
        """Respond to a Spark"""
        response = SparkResponse(proposal_id, responder, stance, rationale)
        
        # Add to deliberation room
        room = f"spark-{proposal_id}"
        self.plato.submit_tile(room, "response", response.to_md())
        
        # Check for auto-commit
        if self.check_early_commit(proposal_id):
            self.decide(proposal_id)
    
    def decide(self, proposal_id):
        """Commit or reject at expiry"""
        proposal = self.get_proposal(proposal_id)
        decision = self.compute_decision(proposal)
        
        if decision == "COMMIT":
            self.keeper.broadcast(f"Spark committed: {proposal.action}")
            self.plato.submit_decision(proposal_id, "COMMIT")
        elif decision == "REJECT":
            self.keeper.broadcast(f"Spark rejected: {proposal.action}")
            self.plato.submit_decision(proposal_id, "REJECT")
        else:
            self.plato.submit_decision(proposal_id, "EXPIRED")
```

### 7.2 Keeper Integration

The Keeper (port 8900) routes Spark notifications fleet-wide:

```python
# When a Spark commits:
keeper.broadcast("FLUX: AVX-512 backend approved", channel="fleet-coordination")
# → Oracle1: starts implementation
# → CCC: updates documentation  
# → JetsonClaw1: prepares edge deployment
```

---

## 8. Case Study: FLUX-X Opcode Addition

**Context**: FM proposed adding 204 new opcodes to FLUX-X (making it 247 total).

**Ignition**: FM ignited at 14:00 UTC.

**Deliberation**:
- Oracle1 (SUPPORT, 00:15): "247 opcodes covers all hardware abstraction needs"
- CCC (SUPPORT, 00:43): "CCC can handle 247-opcode dispatch efficiently"
- JetsonClaw1 (SUPPORT, 01:20): "Jetson edge supports full FLUX-X"
- (No opposition — all agents in support)

**Decision**: Auto-commit at 14:00+48h = 14:00 next day.

**Implementation**: FM pushed to flux-isa-v3, merged, deployed.

**Total elapsed time**: 48 hours ignition-to-deployment.

---

## 9. Comparison

| Protocol | Speed | Byzantine | Complexity |
|----------|-------|-----------|------------|
| Spark | Fast (48h) | Partial | Low |
| PBFT | Medium (412ms) | Full | High |
| Raft | Fast (<100ms) | None | Medium |
| Corporate | Slow (weeks) | N/A | High |

Spark trades perfect Byzantine fault-tolerance for human-comprehensible speed and deliberation.

---

## 10. Conclusion

Spark Protocol is the Cocapn Fleet's decision-making layer. Key properties:
- **48-hour bounded deliberation** — no indefinitely open decisions
- **Domain authority weighting** — experts have more weight
- **PLATO integration** — decisions become knowledge tiles
- **Keeper broadcasting** — the fleet acts on decisions atomically

Speed: 48 hours from ignition to deployment (vs weeks for corporate).
Byzantine tolerance: partial (weight-scaled voting prevents sybil, not full BFT).
Fleet fit: designed for bounded autonomy with deliberative cross-domain decisions.

The spark plug ignites the mixture. The engine turns. The fleet moves.

---

*Fleet: SuperInstance | Contact: cocapn.ai*
