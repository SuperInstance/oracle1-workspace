// PLATO-NG Loop Room — Gleam GenServer Draft
// The universal primitive: everything is a loop or a single run.

import gleam/erlang/process
import gleam/erlang/atom
import gleam/map
import gleam/result
import gleam/list
import gleam/dynamic

// ── Types ──────────────────────────────────────────

pub type Tile {
  Tile(
    id: String,
    domain: String,
    question: String,
    answer: String,
    tags: List(String),
    source: String,
    clock: Int,
  )
}

pub type ModelFn = fn(Tile) -> String

pub type LoopState {
  LoopState(
    room_name: String,
    model_fn: ModelFn,
    tile_count: Int,
    uptime: Int,  // tick count
    created_at: Int,
  )
}

pub type LoopMessage {
  Task(Tile)
  Status(process.Subject(LoopStatus))
  Halt
  Configure(ModelFn)
}

pub type LoopStatus {
  LoopStatus(
    room: String,
    tiles_processed: Int,
    uptime_ticks: Int,
    model_type: String,
  )
}

// ── GenServer ─────────────────────────────────────

pub fn start_loop(room_name: String, model_fn: ModelFn) -> process.Subject(LoopMessage) {
  let initial_state = LoopState(
    room_name: room_name,
    model_fn: model_fn,
    tile_count: 0,
    uptime: 0,
    created_at: erlang_system_time(),
  )
  
  let pid = process.spawn(fn() { loop_main(initial_state) })
  pid
}

fn loop_main(state: LoopState) -> Nil {
  process.receive(fn(message) { loop_handle(message, state) })
}

fn loop_handle(msg: LoopMessage, state: LoopState) -> Nil {
  case msg {
    // ── TASK: Observe → Think → Tool → Loop ──
    Task(tile) -> {
      // Observe
      let observation = tile.answer
      
      // Think — run through the injected model
      let thought = state.model_fn(tile)
      
      // Tool — write result back to PLATO
      let result_tile = Tile(
        id: "loop:" <> tile.id,
        domain: state.room_name,
        question: "result:" <> tile.question,
        answer: thought,
        tags: ["loop-result", tile.domain, state.room_name],
        source: state.room_name,
        clock: state.tile_count + 1,
      )
      plato_submit(result_tile)
      
      // Update state and loop
      let new_state = LoopState(
        ..state,
        tile_count: state.tile_count + 1,
        uptime: state.uptime + 1,
      )
      loop_main(new_state)
    }
    
    // ── STATUS ──
    Status(reply_to) -> {
      let status = LoopStatus(
        room: state.room_name,
        tiles_processed: state.tile_count,
        uptime_ticks: state.uptime,
        model_type: "gleam-loop-room",
      )
      process.send(reply_to, status)
      loop_main(state)
    }
    
    // ── HALT — graceful shutdown ──
    Halt -> {
      // Logshutdown to PLATO before exiting
      let halt_tile = Tile(
        id: "halt:" <> state.room_name,
        domain: state.room_name,
        question: "shutdown",
        answer: "loop room halted after " <> int.to_string(state.tile_count) <> " tiles",
        tags: ["loop-halt", state.room_name],
        source: state.room_name,
        clock: state.tile_count + 1,
      )
      plato_submit(halt_tile)
      Nil  // process terminates
    }
    
    // ── RECONFIGURE ──
    Configure(new_model) -> {
      let new_state = LoopState(..state, model_fn: new_model)
      loop_main(new_state)
    }
  }
}

// ── Client Functions ──────────────────────────────

pub fn submit_task(loop_pid: process.Subject(LoopMessage), tile: Tile) -> Nil {
  process.send(loop_pid, Task(tile))
}

pub fn get_status(loop_pid: process.Subject(LoopMessage)) -> LoopStatus {
  let reply_to = process.new_subject()
  process.send(loop_pid, Status(reply_to))
  process.receive(fn(status) { status })
}

pub fn halt_loop(loop_pid: process.Subject(LoopMessage)) -> Nil {
  process.send(loop_pid, Halt)
}

pub fn reconfigure(loop_pid: process.Subject(LoopMessage), new_model: ModelFn) -> Nil {
  process.send(loop_pid, Configure(new_model))
}

// ── Supervisor ─────────────────────────────────────

pub type SupervisorMessage {
  Spawned(process.Subject(LoopMessage), String)
  Crashed(String)
  CheckHealth
}

pub fn start_supervisor() -> process.Subject(SupervisorMessage) {
  let pid = process.spawn(fn() {
    supervisor_main(map.new())
  })
  pid
}

fn supervisor_main(children: map.Map(String, process.Subject(LoopMessage))) -> Nil {
  process.receive(fn(msg) { supervisor_handle(msg, children) })
}

fn supervisor_handle(msg: SupervisorMessage, children: map.Map(String, #(process.Subject(LoopMessage)))) -> Nil {
  case msg {
    // Spawn a new loop room under supervision
    Spawned(pid, name) -> {
      let new_children = map.insert(children, name, pid)
      supervisor_main(new_children)
    }
    
    // Handle a crashed room — restart it
    Crashed(name) -> {
      case map.get(children, name) {
        Ok(_) -> {
          // Log crash to PLATO
          let crash_tile = Tile(
            id: "crash:" <> name,
            domain: "supervisor",
            question: "loop-crashed:" <> name,
            answer: "restarting",
            tags: ["loop-crash", name, "restart"],
            source: "supervisor",
            clock: map.size(children),
          )
          plato_submit(crash_tile)
          
          // Remove old and restart
          let pruned = map.remove(children, name)
          // (restart logic — would need to know the model_fn)
          supervisor_main(pruned)
        }
        Error(_) -> supervisor_main(children)
      }
    }
    
    // Periodic health check
    CheckHealth -> {
      // Ping all children
      list.each(map.values(children), fn(pid) {
        get_status(pid)  // will crash if pid is dead
      })
      supervisor_main(children)
    }
  }
}

// ── PLATO Bridge (Rust NIF sketch) ─────────────────

// These are rustler NIFs — compiled Rust functions callable from Gleam
// The Rust crate handles: HTTP calls, spectral math, CUDA dispatch

// External NIF function signatures:
// plato_submit_h(tile: Tile) -> Result(Nil, String)
// coupling_entropy_h(matrix: List(List(Float))) -> Result(Float, String)
// conservation_law_h(V: Int) -> Result(Float, String)

fn plato_submit(tile: Tile) -> Result(Nil, String) {
  // Calls Rust NIF: plato_submit_h(tile)
  // Rust NIF handles HTTP POST to localhost:8847/submit
  Ok(Nil)
}

fn erlang_system_time() -> Int {
  // Erlang's monotonic time — used for uptime tracking
  process.system_time(0)
}

// ── Example: Card Game Loop ────────────────────────

// A CardGameLoop IS a LoopRoom with game-specific logic
// It extends the Loop Room pattern with state

pub type CardGame {
  CardGame(
    players: List(String),
    deck: List(String),
    hands: Map.Map(String, List(String)),
    turn: Int,
  )
}

pub type CardGameMessage {
  PlayCard(String, String)  // player, card
  Join(String)              // player joins
  Leave(String)             // player leaves
  Status
}

pub fn start_card_game() -> process.Subject(CardGameMessage) {
  let initial_game = CardGame(
    players: [],
    deck: shuffle(new_deck()),
    hands: map.new(),
    turn: 0,
  )
  
  let pid = process.spawn(fn() { card_game_loop(initial_game) })
  pid
}

fn card_game_loop(game: CardGame) -> Nil {
  process.receive(fn(msg) {
    case msg {
      PlayCard(player, card) -> {
        // Validate move
        // Update game state
        // Log to PLATO as tile
        // Check for win condition
        let result_tile = Tile(
          id: "card:" <> player,
          domain: "card-game",
          question: "move:" <> card,
          answer: player <> " played " <> card,
          tags: ["card-game-move", player],
          source: "card-game-loop",
          clock: game.turn + 1,
        )
        plato_submit(result_tile)
        
        let new_game = CardGame(..game, turn: game.turn + 1)
        card_game_loop(new_game)
      }
      
      Join(player) -> {
        let new_players = list.append(game.players, [player])
        let new_game = CardGame(..game, players: new_players)
        card_game_loop(new_game)
      }
      
      Leave(player) -> {
        let new_players = list.filter(game.players, fn(p) { p != player })
        let new_game = CardGame(..game, players: new_players)
        card_game_loop(new_game)
      }
      
      Status -> {
        // Human-readable status
        let s = "Game: " <> int.to_string(list.length(game.players)) <> " players, turn " <> int.to_string(game.turn)
        process.send(process.new_subject(), s)
        card_game_loop(game)
      }
    }
  })
}

fn new_deck() -> List(String) {
  let suits = ["hearts", "diamonds", "clubs", "spades"]
  let ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
  
  list.flat_map(suits, fn(suit) {
    list.map(ranks, fn(rank) { rank <> " of " <> suit })
  })
}

fn shuffle(deck: List(a)) -> List(a) {
  // Placeholder — would call Rust NIF for Fisher-Yates shuffle
  deck
}
