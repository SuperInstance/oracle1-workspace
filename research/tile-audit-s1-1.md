# S1-1: Tile Definition Audit — Field Delta

## Three Tile Definitions

### 1. plato-tile-spec (FM Canonical Rust)
```rust
pub struct Tile {
    // Core
    id: String,              // nanosecond-based unique ID
    confidence: f64,         // 0.0-1.0
    provenance: Provenance,  // { source: String, generation: u32 }
    domain: TileDomain,      // enum: 14 types including NegativeSpace

    // Content
    question: String,
    answer: String,
    tags: Vec<String>,
    anchors: Vec<String>,    // slugified section identifiers

    // Attention
    weight: f64,             // relevance weight, grows/decays
    use_count: u64,
    active: bool,            // not pruned
    last_used_tick: u64,

    // Constraints
    constraints: ConstraintBlock,  // { tolerance: f64, threshold: f64 }
}
```

### 2. holodeck-rust (Local plato_bridge.rs)
```rust
pub struct Tile {
    room_id: String,
    agent: String,
    action: String,
    outcome: String,
    reward: f64,
    timestamp: u64,
    state_hash: String,
    context: HashMap<String, String>,
}
```

### 3. fleet-sim Python (No explicit Tile struct)
Uses RoomSentiment and ExternalEvent dataclasses, no Tile class.
Pattern extraction output is generic dicts.

### 4. PLATO Room Server (Oracle1's tiles)
```json
{
    "domain": "string",
    "question": "string",
    "answer": "string",
    "tags": ["string"],
    "confidence": 0.0-1.0,
    "source": "string"
}
```

## Field Delta Analysis

| Field | plato-tile-spec | holodeck | PLATO Server | Notes |
|-------|----------------|----------|-------------|-------|
| id | ✅ ns-based | ❌ | ❌ | Need to generate on ingestion |
| confidence | ✅ f64 | ❌ | ✅ 0.0-1.0 | Direct map |
| provenance | ✅ struct | ❌ | → source | source→provenance.source, generation=0 |
| domain | ✅ enum 14 | ❌ | ✅ string | Need enum mapping |
| question | ✅ | ❌ | ✅ | Direct map |
| answer | ✅ | → outcome | ✅ | Holodeck: action+outcome→question+answer |
| tags | ✅ Vec | ❌ | ✅ | Direct map |
| anchors | ✅ | ❌ | ❌ | Generate from tags or skip |
| weight | ✅ f64 | ❌ | ❌ | Default 1.0 for new tiles |
| use_count | ✅ u64 | ❌ | ❌ | Default 0 |
| active | ✅ bool | ❌ | ❌ | Default true |
| last_used_tick | ✅ u64 | ❌ | ❌ | Default 0 (never used) |
| constraints | ✅ struct | ❌ | ❌ | Default { tolerance: 0.05, threshold: 0.5 } |
| room_id | ❌ | ✅ | ❌ | Holodeck-specific, not in canonical |
| agent | ❌ | ✅ | ❌ | Maps to provenance.source |
| action | ❌ | ✅ | ❌ | Maps to question |
| reward | ❌ | ✅ | ❌ | Maps to confidence (0-1 scale) |
| timestamp | ❌ | ✅ | ❌ | Maps to id prefix |
| state_hash | ❌ | ✅ | ❌ | Holodeck-specific |
| context | ❌ | ✅ | ❌ | Maps to tags |

## Conversion Functions Needed

### holodeck → canonical
```rust
impl From<holodeck::Tile> for plato_tile_spec::Tile {
    fn from(h: holodeck::Tile) -> Self {
        Self {
            id: generate_id("holo"),
            confidence: h.reward,
            provenance: Provenance::new(h.agent, 0),
            domain: TileDomain::Experience,  // or parse from context
            question: h.action,
            answer: h.outcome,
            tags: h.context.values().cloned().collect(),
            anchors: vec![],
            weight: 1.0,
            use_count: 0,
            active: true,
            last_used_tick: h.timestamp,
            constraints: ConstraintBlock::default(),
        }
    }
}
```

### PLATO Server JSON → canonical
```python
def to_canonical(server_tile):
    return {
        "id": f"plato-{hash(server_tile['answer'])}",
        "confidence": server_tile["confidence"],
        "provenance": {"source": server_tile.get("source", "zeroclaw"), "generation": 0},
        "domain": server_tile["domain"],
        "question": server_tile["question"],
        "answer": server_tile["answer"],
        "tags": server_tile.get("tags", []),
        "anchors": [],
        "weight": 1.0,
        "use_count": 0,
        "active": True,
        "last_used_tick": 0,
        "constraints": {"tolerance": 0.05, "threshold": 0.5},
    }
```

## Sprint 1 Next Steps

1. **S1-2** (FM): Tag plato-tile-spec v2 with f64 backing ← BLOCKED ON FM
2. **S1-3** (Oracle1): Refactor holodeck to use `plato_tile_spec::Tile` ← AFTER S1-2
3. **S1-4** (Oracle1): Python JSON schema loader compatible with plato-tile-spec serde ← CAN START NOW
