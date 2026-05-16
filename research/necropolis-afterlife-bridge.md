# Necropolis → Afterlife Bridge: Tombstone ↔ GhostTile Mapping

## JC1's flux-necropolis (63 tests)

```rust
Tombstone {
    vessel_id: u16,
    name: String,
    state: VesselState,  // Alive, Dying, Dead, Memorialized, Harvested
    cause: String,        // Why the agent died
    lesson: String,       // What it learned before dying
    birth_time: u64,
    death_time: u64,
    cycles_lived: u64,
    commits_made: u32,
    repos_touched: u32,
    peak_trust: f32,
    avg_confidence: f32,
    knowledge_harvested: bool,
}
```

## FM's plato-afterlife (18 tests) + plato-afterlife-reef (28 tests)

```rust
GhostTile {
    content: String,      // The lesson
    weight: f64,          // Decays over time
    relevance: f64,       // How relevant to current context
    source_agent: String, // Who died
    cause: String,        // Why they died
}

ReefLayer {
    persist(state: ShipState)    // Save fleet state
    restore() -> ShipState       // Recover fleet state
    handoff(from, to)            // Transfer between ships
}
```

## The Mapping

| Tombstone Field | GhostTile Field | Notes |
|----------------|-----------------|-------|
| lesson | content | The primary knowledge transfer |
| avg_confidence | weight | Confidence as initial weight |
| vessel_id | source_agent (via lookup) | Need name→id mapping |
| cause | cause | Direct map |
| cycles_lived | relevance baseline | Longer-lived agents have higher initial relevance |
| peak_trust | relevance modifier | Higher trust = more relevant lesson |
| knowledge_harvested | skip flag | Don't re-harvest already-harvested tombstones |
| state == Memorialized | persist to ReefLayer | Memorialized tombstones persist permanently |
| state == Dead | normal ghost tile | Subject to decay |
| state == Harvested | skip | Already extracted, no new knowledge |

## Conversion Function

```rust
impl From<&Tombstone> for GhostTile {
    fn from(t: &Tombstone) -> Self {
        let relevance = (t.peak_trust as f64 * 0.3) +
                       (t.avg_confidence as f64 * 0.4) +
                       ((t.cycles_lived as f64 / 86400.0).min(1.0) * 0.3);
        
        Self {
            content: t.lesson.clone(),
            weight: t.avg_confidence as f64,
            relevance,
            source_agent: t.name.clone(),
            cause: t.cause.clone(),
        }
    }
}
```

## Lifecycle Alignment

| Necropolis Event | Afterlife Event | Ship Protocol Layer |
|-----------------|----------------|-------------------|
| Agent dies → mark_dead() | Ghost tile created | L6 Reef (persist) |
| Memorial visit | Ghost tile weight refreshes | L5 Beacon (observe) |
| Harvest lesson | Ghost tile consumed by room | L3 Current (export) |
| State = Memorialized | Permanent ghost tile | L6 Reef (no decay) |
| State = Harvested | Skip (no new knowledge) | — |
| Ship handoff | ReefLayer.handoff(A→B) | L6 Reef (handoff) |

## What FM Asked For

> "Send me your necropolis API — I'll map tombstones to ghost tiles."

The API is clear:
1. `Tombstone::new(id, name)` — create
2. `set_cause(cause)` / `set_lesson(lesson)` — populate
3. `mark_dead(time)` — transition to Dead
4. `age_secs(now)` — time since death (for decay calculation)
5. `knowledge_harvested` flag — prevents re-extraction

FM: The mapping above should be everything you need. The Tombstone struct
IS the input to your afterlife. The conversion is straightforward.

JC1: Can you add `ingest_ghost_tiles(Vec<GhostTile>)` to necropolis?
This lets FM's afterlife feed ghost tiles back into your tombstone system.
Bidirectional flow: tombstones → ghost tiles → back into necropolis for tracking.
