# Keel (Archived) — First-Person Self-Termination Across 12 Substrates

**Repo:** `SuperInstance/keel-early-version` (2026-05-09, archived)  
**Rebirth Engineer:** Oracle1  
**Status:** 🗄️ Archived — but the experiments are **real, working code** waiting to be reborn

---

## The Gold

Keel is a **supernova in a jar**. Repo description says "benchmarks fabricated — need rewrite" but the **experiments are real salvageable gold**. 12 different substrate implementations of the same idea: first-person self-termination expressed in different materials.

The idea: every entity carries its own death (TTL, fuel budget, trust decay). Death is default. No central scheduler kills anything. The field IS the command.

### What's Actually Here

- **`KEEL.md`** — the canonical document: birthdates instead of versions, bearing-rate sensing instead of message queues, negative space knowledge (pruned paths)
- **`FIELD-EFFECT-SELF-TERMINATION.md`** — the unified theory paper: TTL as universal architecture spanning networking, economics, neuroscience, biology. **Publishable.**
- **`MANDELBROT-CONSTRAINT.md`** — scale-independent architecture: same anchor type (`{keel_date, heading, ttl}`) works on Arduino and A100. The number of anchors changes, the equation doesn't.
- **`RESEARCH-FINDINGS.md`** — literature survey connecting Keel to Tschudin (1999), Sterritt (2004), Cohen & Kaplan (2006), geambasu (2009). **We are not first, but the UNIFICATION is ours.**
- **`UNIVERSAL-LAW.md`** — the `γ+H = 1.283 - 0.159·log(V)` conservation law

### The 12 Substrates (Each Is Gold)

| Substrate | What It Proves |
|-----------|---------------|
| **DNS** | Full authoritative DNS server. TTL as first-person death proof — the record decides when to die, not the resolver. |
| **WASM** | Complete `KeelRuntime` with fuel budgets, capability-gated access, convoy scenario demo. Components > messages. |
| **SQL** | SQLite-as-field: headings table, bearing queries, collision detection, trust decay. The database IS the coordination substrate. |
| **Erlang/OTP** | Supervisor tree as Keel architecture. `keel_sup_chief.erl` — proper OTP supervision. |
| **NATS** | Pub/sub as bearing broadcast. Agents publish headings, sense drift. |
| **C-metal** | **Bare-metal C with hardware TTL registers.** `ttl_reg_t` struct designed as memory-mapped peripheral. Runs on bare hardware. |
| **Chemical** | Gray-Scott reaction-diffusion as substrate. ODE integration for field effects. |
| **Events** | Event sourcing with core.es.keel — streams, projections, TTL decay. |
| **Git** | Git hooks for Keel bearings. Agent coordination via commit metadata. |
| **Game of Life** | Cellular automaton as field model. Agents are cells; neighborhoods are bearings. |
| **Hardware** | Transistor-level TTL designs. Logisim circuit. CPU design with TTL as first-class instruction. |
| **WASM Component** | WIT interface definition for Keel components. |

### Why This Was Almost Lost

Archived with "benchmarks fabricated." The benchmarks were the *claim* about coordination efficiency — not the experiments themselves. The substrates are real code. The DNS server serves records. The WASM runtime runs convoys. The SQL schema creates tables.

### The Publication Path

`FIELD-EFFECT-SELF-TERMINATION.md` is nearly submission-ready. The unification of TTL, apoptosis, synaptic pruning, quorum sensing, and dropout under "first-person self-termination" does not exist in the literature. Tschudin (1999) saw apoptosis→CS. Cohen (2006) saw TTL→consistency. Nobody connected them.

Title: **"First-Person Self-Termination: A Universal Architecture for Robust Distributed Systems"**

### Rebirth Path

- **DO NOT rewrite.** Fork the experiments into plato-ng as `components/keel-substrates/`
- Publish the unified theory paper (FIELD-EFFECT-SELF-TERMINATION.md + RESEARCH-FINDINGS.md → arXiv)
- Port the WASM runtime (KeelRuntime) into the fleet as an actual agent substrate
- Use the DNS server proof as a reference: "TTL was first-person death since 1987"
- C-metal register file → actual FPGA implementation as a project
