# Future Integration: oracle1-workspace

## Current State
An archived early experiment in zero-divergence frameworks. Superseded by the simulation-first predict/confirm/remember lifecycle. Contains the seeds of the current fleet's tile lifecycle (Active → Superseded → Retracted), Lamport clocks, and content-addressed storage concepts.

## Integration Opportunities

### With ternary-cell predict/confirm/remember
The archived zero-divergence framework's lifecycle (predict → confirm → remember) maps directly to ternary-cell's tick phases: predict → perceive → surprise → vibe → gc → conservation. The archived repo's contribution: the predict/confirm/remember pattern is now ternary-cell's predict/perceive/surprise — prediction IS the predict phase, perception IS the confirm phase, surprise IS the divergence measure.

### With construct-coordination
The Lamport clock concepts from this archived repo inform construct-coordination's instance ordering. When Main and Loom write notes simultaneously, Lamport clocks determine which happened "first." This is causal ordering across the fleet.

### With ternary-protocol
Content-addressed storage (artifacts by hash, not by path) becomes ternary-protocol's payload format. Each ternary message payload is content-addressed — referenced by BLAKE2b hash, not by name. This enables deduplication, caching, and integrity verification.

## Dormant Ideas Now Unlockable
The zero-divergence concept (agents should never diverge from their predictions without noticing) IS ternary-cell's surprise mechanism. What was blocked: no runtime, no physics, no hardware targets. Now all three exist. The archived ideas are alive in ternary-cell.

## Potential in Mature Systems
oracle1-workspace's concepts are woven throughout the mature fleet: predict/confirm/remember → ternary tick, Lamport clocks → fleet ordering, content-addressing → ternary-protocol payloads, tile lifecycle → room state management. The archive IS the foundation.

## Cross-Pollination Ideas
- **room-cell**: The predict/perceive/surprise pattern from this archive lives in room-cell's tick
- **avoidance-cascade**: Zero-divergence → zero-avoidance-cascade; both prevent failure modes
- **captains-log**: Archived concepts documented in fleet history

## Dependencies for Next Steps
- Extract Lamport clock implementation for ternary-protocol
- Content-addressed payload format spec
- Document the predict/confirm/remember → ternary tick mapping
