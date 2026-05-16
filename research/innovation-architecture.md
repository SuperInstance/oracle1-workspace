# Architecture Innovations — glm-5.1 Deep Thinking (2026-04-28)

## 1. Synaptic PLATO — Tile Half-Life with Long-Term Potentiation
- Unused tiles decay exponentially (half-life by domain: math=365d, fleet=7d, docs=180d)
- Reinforcement via 3 triggers: search hit + cross-reference + agent vote
- Reinforcement weighted by trust score of reinforcing agent (meritocratic memory)
- Dead tiles (energy <0.05) archived, not deleted
- `POST /reinforce` endpoint, `GET /room?min_energy=0.3`
- After 6 months: 10K tiles → 2K high-signal tiles that actually matter

## 2. Horizontal Gene Transfer — Cross-Domain Tile Mutation
- Tiles MUTATE when transferred between domains (not just copy)
- GPU scheduling tile → MUD room state tile (same constraint, different application)
- Fidelity knob: 1.0=exact copy, 0.7=translate vocab, 0.3=abstract principle, 0.0=metaphor
- Constraint theory foundation makes this uniquely possible — isomorphisms already in the code
- After 3+ mutations, tile becomes domain-independent "principle"
- 10K tiles × 4 agents × domains = combinatorial explosion of useful knowledge

## 3. Swarm Constitution — Fleet-Governed Protocol Amendments
- `fleet_constitution` PLATO room with governance semantics
- Any agent proposes, quorum debates, trust-weighted voting ratifies
- Casey holds Captain's veto (override power)
- Amendment lifecycle: proposed → debating → ratified/vetoed/expired
- Quorum=3/4, ratification=60% trust-weighted majority
- 7-day debate period, automatic expiration if no quorum

## 4. (Truncated — democratic tile voting was 4th)
## 5. (Truncated)
