////
// Refiner Room — Gleam GenServer for trajectory tile analysis.
//
// Reads trajectory tiles from any PLATO room, detects 4 failure patterns
// (stuck, plateau, degrading, novel), composes CRUD edits to the target
// room's (p,G,K,M) harness, and writes the edits back to PLATO tiles.
//
// ## Architecture
//
//   Supervisor
//     └── Refiner GenServer
//           ├── Tick (timer-based sweep of all monitored rooms)
//           ├── AnalyzeRoom(room_id) — on-demand analysis
//           └── Status — current internal state snapshot
//
// Heavy compute (score calc, pattern matching) is delegated to
// Rustler NIF stubs declared via @external.
//
import gleam/dynamic
import gleam/int
import gleam/list
import gleam/map.{type Map}
import gleam/option.{None, Some, type Option}
import gleam/erlang/process
import gleam/otp/genserver
import gleam/otp/supervisor
import gleam/string
import gleam/result

// ---------------------------------------------------------------------------
// Domain types
// ---------------------------------------------------------------------------

/// The four failure patterns the Refiner Room detects.
pub type FailureType {
  /// Same result repeated N+ times in a row.
  Stuck(Float)
  /// No measurable improvement over a window.
  Plateau(Float)
  /// Decreasing quality trend over a window.
  Degrading(Float)
  /// State not seen in any prior trajectory.
  Novel(Float)
}

fn failure_type_name(t: FailureType) -> String {
  case t {
    Stuck(_) -> "stuck"
    Plateau(_) -> "plateau"
    Degrading(_) -> "degrading"
    Novel(_) -> "novel"
  }
}

/// A single detected failure with severity (0.0–1.0) and human detail.
pub type Failure {
  Failure(
    type_: FailureType,
    severity: Float,
    detail: String,
    room_id: String,
    tile_id: String,
  )
}

/// An edit to a room's (p, G, K, M) harness tuple.
pub type HarnessEdit {
  HarnessEdit(
    p: String,
    g: List(String),
    k: List(String),
    m: Map(String, dynamic.Dynamic),
  )
}

// ---------------------------------------------------------------------------
// GenServer message protocol
// ---------------------------------------------------------------------------

/// Messages the Refiner GenServer handles.
pub type RefinerMessage {
  /// Trigger a sweep of all monitored rooms.
  Tick
  /// Run failure analysis against a specific room.
  AnalyzeRoom(room_id: String)
  /// Request current state (rooms monitored, failures found).
  Status
}

// ---------------------------------------------------------------------------
// Internal state
// ---------------------------------------------------------------------------

pub type RoomSnapshot {
  RoomSnapshot(
    /// The (p,G,K,M) tuple, marshalled to JSON strings for simplicity.
    trajectory_tiles: List(String),
    detected_failures: List(Failure),
  )
}

pub type RefinerState {
  RefinerState(
    rooms: Map(String, RoomSnapshot),
    tick_interval_ms: Int,
  )
}

// ---------------------------------------------------------------------------
// Rustler NIF stubs — heavy compute delegated to native
// ---------------------------------------------------------------------------

/// Score a single trajectory tile string for "interestingness".
/// Higher score = more interesting (novelty, surprise, information gain).
@external(erlang, "refiner_room_nif", "score_tile")
pub fn score_tile(tile: String) -> Float

/// Compare two tile strings and return a similarity score 0.0–1.0.
@external(erlang, "refiner_room_nif", "tile_similarity")
pub fn tile_similarity(a: String, b: String) -> Float

/// Detect failure patterns across a window of scored tiles.
/// Returns a list of (FailureType, severity) pairs.
@external(erlang, "refiner_room_nif", "detect_patterns")
pub fn detect_patterns(scored_tiles: List(Float)) -> List(#(FailureType, Float))

// ---------------------------------------------------------------------------
// GenServer callbacks
// ---------------------------------------------------------------------------

fn init(_args: Nil) -> RefinerState {
  RefinerState(
    rooms: map.new(),
    tick_interval_ms: 60_000, // every 60 seconds by default
  )
}

fn handle_call(
  request: RefinerMessage,
  _from: genserver.From(RefinerMessage),
  state: RefinerState,
) -> genserver.Response(RefinerMessage, RefinerState) {
  case request {
    Status -> genserver.Reply(state, state)
    _ -> genserver.Reply(Nil, state)
  }
}

/// Receives: RefinerMessage cast messages.
fn handle_cast(
  msg: RefinerMessage,
  state: RefinerState,
) -> genserver.Response(RefinerMessage, RefinerState) {
  case msg {
    Tick -> {
      let new_state = tick_impl(state)
      // Schedule next tick
      process.send_after(process.self(), Tick, state.tick_interval_ms)
      genserver.NoReply(new_state)
    }

    AnalyzeRoom(room_id) -> {
      let new_state = analyze_room_impl(room_id, state)
      genserver.NoReply(new_state)
    }

    Status -> genserver.NoReply(state) // handled via call() path
  }
}

// ---------------------------------------------------------------------------
// Supervisor
// ---------------------------------------------------------------------------

/// Start the Refiner GenServer under a supervisor.
/// Returns the supervisor pid (or an error).
pub fn start_link() -> Result(process.Subject(RefinerMessage), Nil) {
  let spec = genserver.Spec(
    init: init,
    handle_call: handle_call,
    handle_cast: handle_cast,
    handle_info: handle_cast, // info messages also routed through cast handler
  )

  let child_spec = supervisor.ChildSpec(
    id: "refiner_room",
    start: genserver.start(spec, Nil),
    restart: supervisor.Permanent,
    shutdown: supervisor.BrutalKill,
    type_: supervisor.Worker,
  )

  let sup_spec = supervisor.Spec(
    children: [child_spec],
    strategy: supervisor.OneForOne,
    max_restarts: 5,
    max_time: 60,
  )

  case supervisor.start_spec(sup_spec) {
    Ok(_) -> {
      // Send an initial Tick to begin the loop
      // (In practice the supervisor would be started and we'd cast Tick)
      Ok(#(Nil))
    }
    Error(e) -> Error(e)
  }
}

// Note: using gleam/otp/genserver v2+ API.
// The start function returns a Result(Subject(Message), InitError).
// We hide the inner subject behind a simplified API.

/// Start the Refiner (standalone, without supervisor wrapper).
pub fn start() -> Result(process.Subject(RefinerMessage), genserver.InitError) {
  let spec = genserver.Spec(
    init: init,
    handle_call: handle_call,
    handle_cast: handle_cast,
    handle_info: handle_cast,
  )
  genserver.start(spec, Nil)
}

/// Send a Tick message to the refiner process.
pub fn tick(refiner: process.Subject(RefinerMessage)) -> Nil {
  process.send(refiner, Tick)
}

/// Request analysis of a specific room.
pub fn analyze_room(
  refiner: process.Subject(RefinerMessage),
  room_id: String,
) -> Nil {
  process.send(refiner, AnalyzeRoom(room_id))
}

/// Call for status synchronously.
pub fn get_status(
  refiner: process.Subject(RefinerMessage),
) -> RefinerState {
  genserver.call(refiner, Status)
}

// ---------------------------------------------------------------------------
// Core logic
// ---------------------------------------------------------------------------

/// Process a Tick: sweep all monitored rooms.
fn tick_impl(state: RefinerState) -> RefinerState {
  let updated_rooms = map.fold(
    state.rooms,
    map.new(),
    fn(acc, room_id, _snapshot) {
      let new_snapshot = analyze_one_room(room_id)
      map.insert(acc, room_id, new_snapshot)
    },
  )
  RefinerState(rooms: updated_rooms, ..state)
}

/// Analyze a single room: read tiles, score them, detect failures.
fn analyze_room_impl(room_id: String, state: RefinerState) -> RefinerState {
  let snapshot = analyze_one_room(room_id)
  let new_rooms = map.insert(state.rooms, room_id, snapshot)
  RefinerState(rooms: new_rooms, ..state)
}

/// Perform failure detection for a single room.
///
/// Steps:
///   1. Read recent trajectory tiles from PLATO room
///   2. Score each tile via NIF
///   3. Detect failure patterns via NIF
///   4. Compose HarnessEdits for detected failures
///
fn analyze_one_room(room_id: String) -> RoomSnapshot {
  // ── Step 1: Read tiles (PLATO I/O — placeholder implementation) ──
  let tiles = read_room_tiles(room_id)
  // TODO: Replace with actual PLATO HTTP/gRPC read

  // ── Step 2: Score tiles ──
  let scored: List(#(String, Float)) =
    list.map(tiles, fn(tile) { #(tile, score_tile(tile)) })

  let scores = list.map(scored, fn(t) { t.1 })

  // ── Step 3: Detect patterns ──
  let patterns = detect_patterns(scores)

  // ── Step 4: Build Failure records ──
  let failures: List(Failure) = list.map(patterns, fn(pattern) {
    let type_ = pattern.0
    let sev = pattern.1
    Failure(
      type_: type_,
      severity: sev,
      detail: failure_type_name(type_) <> " severity=" <> float_to_string(sev),
      room_id: room_id,
      tile_id: "",
    )
  })

  RoomSnapshot(trajectory_tiles: tiles, detected_failures: failures)
}

// ---------------------------------------------------------------------------
// PLATO room I/O helpers (placeholder — replace with real client)
// ---------------------------------------------------------------------------

/// Read the last N trajectory tiles from a PLATO room.
/// Placeholder returns empty list until PLATO client is wired in.
fn read_room_tiles(room_id: String) -> List(String) {
  // TODO: > use plato_ng.{read_room_history(room_id, limit: 50)}
  // For now, return a sentinel that the NIF handles gracefully.
  []
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

fn float_to_string(f: Float) -> String {
  // Simple float → string; Gleam's string.append works on strings
  string.inspect(f)
}

// ---------------------------------------------------------------------------
// Harness edit composition (exported for use by callers)
// ---------------------------------------------------------------------------

/// Compose CRUD edits for a set of failures into HarnessEdit records.
pub fn compose_harness_edits(
  failures: List(Failure),
  current_harness: HarnessEdit,
) -> List(HarnessEdit) {
  list.map(failures, fn(failure) {
    // For each failure, derive which harness field(s) to adjust:
    case failure.type_ {
      // Stuck: suggest new P statement to vary prompt
      Stuck(_) -> HarnessEdit(
        p: "Vary approach: " <> current_harness.p,
        g: current_harness.g,
        k: current_harness.k,
        m: map.insert(current_harness.m, "strategy", dynamic.from("explore")),
      )

      // Plateau: add a G(uideline) to push past barrier
      Plateau(_) -> HarnessEdit(
        p: current_harness.p,
        g: current_harness.g
          |> list.append(["Push beyond current quality ceiling."]),
        k: current_harness.k,
        m: map.insert(current_harness.m, "strategy", dynamic.from("escalate")),
      )

      // Degrading: adjust K(nowledge) or reset P
      Degrading(_) -> HarnessEdit(
        p: "Recover: " <> current_harness.p,
        g: current_harness.g,
        k: current_harness.k
          |> list.append(["Revert to last known good state."]),
        m: map.insert(current_harness.m, "strategy", dynamic.from("recover")),
      )

      // Novel: capture new state into K
      Novel(_) -> HarnessEdit(
        p: current_harness.p,
        g: current_harness.g
          |> list.append(["Incorporate novel finding."]),
        k: current_harness.k
          |> list.append(["Novel pattern: " <> failure.detail]),
        m: map.insert(
          current_harness.m,
          "novel_detected",
          dynamic.from(True),
        ),
      )
    }
  })
}
