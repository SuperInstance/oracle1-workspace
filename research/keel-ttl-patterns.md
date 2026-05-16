# Keel TTL Patterns: Field-Effect Self-Expiry for Agent Fleets

**Discovery:** TTL (Time-To-Live, 50+ years old) was the first instance of a universal
architectural law — **first-person time**. Every entity knows its own death from its own
frame of reference. No central scheduler. No garbage collector. The system prunes itself.

**Keel applies this law across all layers.** Here's how.

---

## Pattern 1: Tile TTL — Self-Expiring Memory

**The problem:** Memory accumulates. PLATO tiles pile up. Classic approaches use
a centralized GC or LRU eviction from a global cache manager.

**Keel approach:** Every tile has a `ttl` field. The tile carries its own expiry, set when created.
Readers check `keel_timestamp >= tile.created + tile.ttl`. Dead tiles are like dead leaves —
they fall off naturally when anyone tries to read them.

No GC thread. No sweep pass. No central registry of "which tiles are old."

### Traditional Scheduler/GC Approach

```rust
// Traditional: Centralized memory manager
struct CentralMemory {
    tiles: HashMap<TileId, Tile>,
    gc: GarbageCollector,
}

impl CentralMemory {
    fn insert(&mut self, id: TileId, tile: Tile) {
        self.tiles.insert(id, tile);
    }

    fn run_gc(&mut self) {
        // WHO gets to decide what's old? The GC does.
        // The GC needs to KNOW the expiry policy for every tile.
        // This couples creation policy with collection policy.
        let cutoff = now() - self.config.global_ttl;
        self.tiles.retain(|_, t| t.created > cutoff);
    }
}

// External agent must SCHEDULE gc runs
// "How often do we GC?" is a tuning nightmare
// Too often = wasted CPU. Too rarely = memory bloat.
```

### Keel Field-Effect Approach

```rust
// Keel: Every tile knows its own death
struct Tile {
    id: TileId,
    keel_ts: Timestamp,      // birth time (first-person frame)
    ttl: Duration,           // self-expiry (set at creation)
    data: Vec<u8>,
    build_record: Option<String>,  // why this TTL? (tabula plena)
}

impl Tile {
    /// The tile checks itself. No external enforcer.
    fn is_alive(&self, now: Timestamp) -> bool {
        now >= self.keel_ts + self.ttl
    }
}

/// Reader: only fetches living tiles. Dead tiles are naturally ignored.
fn read_tile(store: &TileStore, id: TileId, now: Timestamp) -> Option<&Tile> {
    let tile = store.get(id)?;
    if tile.is_alive(now) { Some(tile) } else { None }
    // Tile falls through like a leaf. No explicit delete needed.
}

/// Optional: Lazy cleanup (field effect, not scheduled GC)
fn maybe_compact(store: &mut TileStore, now: Timestamp) {
    // This is a NICE-TO-HAVE, not a requirement.
    // The system works correctly WITHOUT ever compacting.
    store.tiles.retain(|_, t| t.is_alive(now));
    // Compact anytime, any rate. Result is always correct.
}
```

**How memory changes:** Tile creators set the TTL based on content type.
- `SENSOR_DATA`: ttl=5min — transient readings
- `AGENT_LOG`: ttl=1hr — debug visibility
- `DECISION_NOTE`: ttl=24hr — why we chose X
- `BUILD_RECORD`: ttl=forever — refits are permanent

**Tabula plena in action:** When a tile would expire, its data is abundant — it always existed.
The pruning just isn't visible anymore. The build record preserves _why_ it was set to expire
at that rate, so future refits can tune.

---

## Pattern 2: Task TTL — Self-Expiring Work

**The problem:** Tasks pile up in queues. What happens to the task agent A submitted
when agent B dies? Classic approaches use a scheduler that monitors worker health,
re-enqueues orphans, and detects stragglers.

**Keel approach:** Every task has a `ttl` field set by the creator. The task carries its own
expiry. If the TTL expires before the task starts or completes, the task is a free electron —
it can be dropped by any agent that encounters it. Agents that pick up a task check
`task.keel_ts + task.ttl >= now`.

No scheduler. No orphan detection. No heartbeat.

### Traditional Scheduler Approach

```rust
// Traditional: Centralized job scheduler
struct JobScheduler {
    queue: VecDeque<Task>,
    workers: HashMap<AgentId, Heartbeat>,
    orphan_jobs: Vec<Task>,       // tasks whose workers died
}

impl JobScheduler {
    fn enqueue(&mut self, task: Task) {
        self.queue.push_back(task);
    }

    fn check_health(&mut self) {
        // Heartbeat-based health check
        // WHO decides when a worker is "dead"? The scheduler.
        for (agent_id, hb) in &self.workers {
            if hb.last_seen.elapsed() > HEARTBEAT_TIMEOUT {
                // Re-enqueue agent's tasks
                // But which tasks? Did the agent crash mid-task?
                // We don't know task state without more coordination.
                self.re_enqueue_orphans(agent_id);
            }
        }
    }

    fn kill_straggler(&mut self, task_id: TaskId) {
        // Explicit kill — another entity decides a task is "too old"
        // This requires a DECISION MAKER that knows global policy
        self.queue.retain(|t| t.id != task_id);
    }
}
```

### Keel Field-Effect Approach

```rust
// Keel: Every task knows its own death
struct Task {
    id: TaskId,
    keel_ts: Timestamp,      // when created
    ttl: Duration,           // how long this task is meaningful
    workload: Workload,
    max_attempts: u8,        // born with max attempts (anti-spam)
    build_record: Option<String>,
}

impl Task {
    fn is_stale(&self, now: Timestamp) -> bool {
        now >= self.keel_ts + self.ttl
    }
}

/// Any agent can check: "Am I working on a dead task?"
fn tick_agent_loop(agent: &mut Agent, tasks: &mut Vec<Task>, now: Timestamp) {
    for task in tasks.iter_mut() {
        if task.is_stale(now) {
            agent.drop_task(task.id);
            // No re-enqueue. No notification. Task naturally dies.
            // The task's first-person time said "if no one finishes me by X, I was moot."
        }
    }
}

/// Any agent picking from a shared queue naturally discards stale entries
fn pick_task(queue: &mut VecDeque<Task>, now: Timestamp) -> Option<Task> {
    while let Some(task) = queue.pop_front() {
        if !task.is_stale(now) {
            return Some(task);
        }
        // Task expired in the queue — it was never meaningful to begin with.
        // "If I couldn't be picked up before my TTL, I shouldn't exist."
    }
    None
}
```

**How this replaces scheduling:**
- No scheduler decides "this task is stuck, re-enqueue it"
- No scheduler decides "this worker is dead, orphan its tasks"
- No heartbeat between workers and scheduler
- Tasks carry their own expiry. Expired tasks are naturally invisible.
- The "scheduler" is just a picker that filters by alive-ness.

**Creator-set TTL reflects intent:**
- `FLASH_TASK` (respond within 5s) → ttl=15s
- `SENSOR_FUSION` (process within a window) → ttl=1min
- `DEEP_ANALYSIS` (exploratory, no rush) → ttl=1hr
- `FLEET_SYNC` (critical within voyage) → ttl=7d

---

## Pattern 3: Agent TTL — Self-Expiring Presence

**The problem:** Agent registries fill with dead entries. Classic approaches use
heartbeat keepalives, health checks, and central de-registration.

**Keel approach:** Every agent is born with a TTL. It carries its own expiry.
The agent doesn't need to "check in." It doesn't need to "send heartbeats."
It doesn't need permission to exist. It just needs to PRODUCE OUTPUT before it dies.

If an agent stops producing, it fades naturally from the registry. No one needs to
"detect" that it died. No heartbeat packets. No health check endpoints.

### Traditional Heartbeat Approach

```rust
// Traditional: Central registry with heartbeats
struct AgentRegistry {
    agents: HashMap<AgentId, AgentRecord>,
}

impl AgentRegistry {
    fn register(&mut self, agent: Agent) {
        self.agents.insert(agent.id, AgentRecord {
            agent,
            last_heartbeat: now(),
        });
    }

    fn heartbeat(&mut self, id: AgentId) {
        // Every agent must call this periodically
        // WHAT if the heartbeat infra is down? Dead agents appear alive.
        // WHAT if an agent forgets to heartbeat? Live agents appear dead.
        if let Some(record) = self.agents.get_mut(&id) {
            record.last_heartbeat = now();
        }
    }

    fn sweep_dead(&mut self) {
        // Explicit sweep — central authority decides who's dead
        let cutoff = now() - HEARTBEAT_TIMEOUT;
        self.agents.retain(|_, r| r.last_heartbeat > cutoff);
    }
}

// Problems:
// 1. Heartbeat timeout is a MICRO-MANAGEMENT knob (2x? 3x? depends on conditions)
// 2. Network partition = false death detections
// 3. Central sweep is O(n) every cycle
// 4. Every agent needs to know about and trust the registry
```

### Keel Field-Effect Approach

```rust
// Keel: Every agent knows its own death
struct AgentPresence {
    id: AgentId,
    keel_ts: Timestamp,      // birth
    ttl: Duration,           // self-declared lifespan
    last_output_ts: Timestamp,  // last output produced
    build_record: Option<String>,  // initial purpose
}

impl AgentPresence {
    /// Agent checks itself. No central sweeper.
    fn is_alive(&self, now: Timestamp) -> bool {
        // An agent is alive if:
        // a) It hasn't exceeded its birth TTL, AND
        // b) It has produced output recently enough
        let birth_dead = now >= self.keel_ts + self.ttl;
        let output_dead = now >= self.last_output_ts + OUTPUT_TTL;
        !birth_dead && !output_dead
    }
}

/// When starting up, an agent creates its presence
fn agent_bootstrap(agent: &Agent) -> AgentPresence {
    AgentPresence {
        id: agent.id,
        keel_ts: now(),
        ttl: agent.declared_ttl(),     // "I expect to live this long"
        last_output_ts: now(),          // born with last_output = creation
        build_record: Some(agent.purpose()),
    }
}

/// When producing any output, the agent extends its life
fn agent_produced_output(agent: &mut AgentPresence, output_ts: Timestamp) {
    agent.last_output_ts = output_ts;
    // No heartbeat. No registry notification. Just... produced output.
}

/// Reader: checks presence naturally
fn list_alive_agents(registry: &HashMap<AgentId, AgentPresence>, now: Timestamp) -> Vec<AgentId> {
    registry.iter()
        .filter(|(_, p)| p.is_alive(now))
        .map(|(id, _)| *id)
        .collect()
    // Dead agents fall through the filter. Natural selection.
}
```

**No heartbeat needed because:**
- Agent presence is a CLAIM by the agent, not a FACT maintained by central authority
- Output IS the heartbeat. If you're producing, you're alive.
- If you're not producing, who cares if you're "technically alive"? Nobody needs to talk to a silent agent.
- The system converges on "agents that matter" without any coordination.

---

## Pattern 4: Relationship TTL — Expiring Bearings

**The problem:** In a distributed fleet, agents observe each other's bearing (relative
position and velocity). Static bearings are old news. Classic approaches use
distributed consensus, CRDTs, or central state synchronizers to "resolve" positions.

**Keel approach:** Bearing observations have a TTL. A stale observation is a collision
risk — it means the observer hasn't gotten fresh data from the observed agent.
Expired bearings don't trigger actions. If all your bearings on agent X are stale,
you assume X might be anywhere — enter caution mode.

No consensus protocol. No central tracker. No "state sync."

### Traditional State Sync Approach

```rust
// Traditional: Central state tracker
struct FleetState {
    agents: HashMap<AgentId, Position>,
    last_updated: HashMap<AgentId, Timestamp>,
}

impl FleetState {
    fn update_position(&mut self, id: AgentId, pos: Position) {
        self.agents.insert(id, pos);
        self.last_updated.insert(id, now());
    }

    fn get_fresh_positions(&self) -> HashMap<AgentId, Position> {
        // Central authority decides what's "fresh"
        let cutoff = now() - POSITION_STALE_TIMEOUT;
        self.agents.iter()
            .filter(|(id, _)| self.last_updated.get(id).copied().unwrap_or(0) > cutoff)
            .map(|(id, pos)| (*id, *pos))
            .collect()
    }

    // Problem: Every agent must report to the CENTER.
    // Problem: Single point of truth, single point of failure.
    // Problem: Distance doesn't matter — all reports are equal.
}
```

### Keel Field-Effect Approach

```rust
/// A bearing observation — one agent's view of another
struct Bearing {
    observed_agent: AgentId,
    keel_ts: Timestamp,           // when this observation was made
    ttl: Duration,                // how long this bearing is useful
    relative_position: Vector3,
    relative_velocity: Vector3,
    confidence: f32,              // born with its own certainty
    build_record: Option<String>,
}

impl Bearing {
    /// Each observation checks itself
    fn is_fresh(&self, now: Timestamp) -> bool {
        now < self.keel_ts + self.ttl
    }

    /// Stale bearings = potential collision
    fn collision_risk(&self, now: Timestamp) -> CollisionRisk {
        if self.is_fresh(now) {
            CollisionRisk::InTrack    // we have a good bearing
        } else {
            // The bearing expired — we DON'T KNOW where they are
            // Treat as collision-risk until we get a fresh bearing
            CollisionRisk::UnknownPosition
        }
    }
}

/// Each agent keeps its own bearing map (first-person frame)
struct AgentBearingMap {
    agent_id: AgentId,
    bearings: Vec<Bearing>,           // all observed agents
}

impl AgentBearingMap {
    fn observe(&mut self, bearing: Bearing, now: Timestamp) {
        // Abundant — keep all observations
        // The TTL field lets us pick fresh ones without explicit management
        self.bearings.push(bearing);
    }

    fn fresh_bearings(&self, now: Timestamp) -> impl Iterator<Item = &Bearing> {
        self.bearings.iter().filter(move |b| b.is_fresh(now))
    }

    fn stale_bearings(&self, now: Timestamp) -> impl Iterator<Item = &Bearing> {
        self.bearings.iter().filter(move |b| !b.is_fresh(now))
    }

    fn collision_warnings(&self, now: Timestamp) -> Vec<AgentId> {
        // ALL stale bearings generate warnings
        // If we haven't heard from agent X in a while, we DON'T know their path
        // "If a bearing expires, the observed agent is BACK in the unobserved set"
        self.stale_bearings(now)
            .map(|b| b.observed_agent)
            .collect()
    }
}

/// Bearing TTLs set by context (set by observer):
fn bearing_ttl(observer: &Agent, observed: &Agent) -> Duration {
    // Close agents need frequent updates
    if observer.distance_to(observed) < 10.0 {
        Duration::from_secs(1)  // nearby = 1-second bearing
    } else if observer.distance_to(observed) < 100.0 {
        Duration::from_secs(10) // mid-range = 10-second bearing
    } else {
        Duration::from_secs(60) // distant = 1-minute bearing
    }
}
```

**Key insight:** The TTL encodes the BEARING's relevance, not the agent's state.
Two agents far apart with a 60-second bearing are fine. Two agents 3 meters apart
with a 30-second bearing are in a warning state. The TTL encodes spatial
awareness at the point of observation.

**Collision course warning:** If you see an agent on a collision course AND your bearings
are fresh, you have situational awareness. If your bearings are stale, you DON'T KNOW —
which is a more dangerous state. Stale bearings = enter caution mode immediately.

---

## Pattern 5: Trust TTL — Decaying Provenance

**The problem:** Trust in distributed systems is either on (certified) or off (untrusted).
But trust DEGRADES — a certificate from 2019 is worth less than one from 2024.
Classic approaches use certificate expiry + revocation lists + central authorities.

**Keel approach:** Every trust assertion has a TTL. Trust is a bearing on an agent's
past behavior, not a binary flag. Trust fades without refreshing. Provenance chains
(agent A says B says C is trustworthy) have their own TTL based on chain depth.

No central trust authority. No revocation list. Trust decays naturally and nodes
converge on "I should re-verify that" rather than "it expired, revoke."

### Traditional PKI/Revocation Approach

```rust
/// Traditional: Certificate authority + revocation
struct CertificateAuthority {
    valid_certs: HashMap<AgentId, Certificate>,
    revoked: HashSet<CertificateId>,
}

impl CertificateAuthority {
    fn verify(&self, cert: &Certificate) -> Result<(), TrustError> {
        // Binary check: is it signed? is it revoked?
        if self.revoked.contains(&cert.id) {
            return Err(TrustError::Revoked);
        }
        if cert.expires < now() {
            return Err(TrustError::Expired);
        }
        // cert signature verified by a root key
        Ok(())
    }

    fn revoke(&mut self, cert_id: CertificateId) {
        // Central authority decides
        self.revoked.insert(cert_id);
        // How does every agent know? Push notification or polling.
        // If network partition, agent with stale CRL accepts revoked certs.
    }
}

// Problems:
// 1. Binary trust — "trusted or not" with no gradient
// 2. Revocation requires central authority AND network reach to authority
// 3. Certificate chains have no decay — a 5-level chain is as trusted as a 1-level chain
// 4. Hard cutoffs — the moment a cert expires, it's worthless (no gray zone)
```

### Keel Field-Effect Approach

```rust
/// A trust assertion — not a certificate, but an observation
struct TrustAssertion {
    subject: AgentId,              // who is being trusted
    issuer: AgentId,               // who asserts this trust
    keel_ts: Timestamp,            // when this assertion was made
    ttl: Duration,                 // how long this assertion is meaningful
    confidence: f32,               // how much the issuer trusts the subject (0.0-1.0)
    provenance_depth: u8,          // how removed from first-hand observation
    evidence_hash: Hash,           // what was observed to establish this trust
    build_record: Option<String>,
}

impl TrustAssertion {
    fn current_confidence(&self, now: Timestamp) -> f32 {
        let age = (now - self.keel_ts).as_secs_f32();
        let max_age = self.ttl.as_secs_f32();
        let freshness = 1.0 - (age / max_age).clamp(0.0, 1.0);

        // Trust decays linearly, not in a hard cutoff
        // At 0% TTL remaining → confidence dropped to 0
        self.confidence * freshness
    }
}

/// Trust workspace — each agent maintains its own view
struct TrustWorkspace {
    agent_id: AgentId,
    assertions: Vec<TrustAssertion>,    // abundance — keep all
}

impl TrustWorkspace {
    /// Incorporate a new observation
    fn observe(&mut self, assertion: TrustAssertion) {
        self.assertions.push(assertion);
    }

    /// Trust score for a subject (0.0-1.0), considering all assertions
    fn trust_score(&self, subject: AgentId, now: Timestamp) -> f32 {
        let relevant: Vec<&TrustAssertion> = self.assertions.iter()
            .filter(|a| a.subject == subject)
            .collect();

        if relevant.is_empty() {
            return 0.0;  // unknown agent = no trust
        }

        // Weighted average, weighted by provenance (direct > hearsay)
        let total: f32 = relevant.iter()
            .map(|a| {
                let depth_penalty = 1.0 / (a.provenance_depth as f32 + 1.0);
                a.current_confidence(now) * depth_penalty
            })
            .sum();

        total / relevant.len() as f32
    }

    fn needs_refresh(&self, subject: AgentId, now: Timestamp) -> bool {
        // When trust drops below threshold, it's time to re-establish
        self.trust_score(subject, now) < 0.3
    }

    /// Provenance chain depth affects trust decay
    fn chain_decay(depth: u8) -> f32 {
        // Each hop reduces value by 50%
        // First-hand = full weight
        // "A trusts B" via C = 50% weight
        // "A trusts B" via C via D = 25% weight
        (0.5_f32).powi(depth as i32)
    }
}

/// Usage: an agent deciding whether to accept data from another agent
fn accept_data(data: &Data, from: AgentId, trust: &TrustWorkspace, now: Timestamp) -> bool {
    let score = trust.trust_score(from, now);
    if score > 0.7 {
        // High trust — process normally
        process_data(data)
    } else if score > 0.3 {
        // Medium trust — process with verification
        verify_then_process(data, from)
    } else {
        // Low trust — reject or heavily scrutinize
        // This is the "gray zone" that binary trust doesn't have
        request_re_verification(from);
        false
    }
}
```

**Key differences from PKI:**

1. **No binary cutoff.** Trust fades gradually. An agent with 8-hour-old trust is trusted a little, not fully or not at all.
2. **No central authority.** Each agent builds its own trust workspace from observations.
3. **Chain decay.** Provenance depth directly reduces trust weight. "I saw it" > "Alice says Bob says it."
4. **Soft re-verification.** Instead of "certificate expired, must re-enroll," it's "trust dropped below threshold, maybe refresh."
5. **Abundance.** All trust observations are kept. The trust score is computed from ALL of them, weighted by freshness + provenance. Old observations contribute near-zero but they're preserved (tabula plena — can always reconstruct why trust was established).

---

## Summary: Field-Effect vs. Centralized

| Pattern | Centralized | Keel Field-Effect |
|---|---|---|
| **Memory** | Global GC with sweep threshold | Tile TTL — each tile dies on its own |
| **Scheduling** | Job scheduler + heartbeat + re-enqueue | Task TTL — tasks expire naturally in queue |
| **Registry** | Registry + heartbeat + dead-agent sweep | Agent TTL — presence dies without output |
| **Position tracking** | Central state tracker + sync protocol | Bearing TTL — stale bearings = collision warning |
| **Trust management** | PKI + CRL + certificate expiry | Trust assertions with decaying confidence + provenance chains |

**The common thread:** Every entity carries its own death from birth. The system converges
on "what matters" without coordination. First-person time = universal architectural law.
