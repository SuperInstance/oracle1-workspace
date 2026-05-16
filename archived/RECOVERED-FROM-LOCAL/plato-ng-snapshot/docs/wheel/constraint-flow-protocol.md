# CFP — Constraint Flow Protocol: FLUX Bytecode for Zero-Drift AI Understanding

**Repo:** `SuperInstance/constraint-flow-protocol` (2026-05-08)  
**Rebirth Engineer:** Oracle1  
**Status:** ✅ Live code, v0.1+v2 operational, PLATO-ready

---

## The Gold

This repo **solves semantic drift between AI agents** by compiling understanding into FLUX bytecode — a 30-opcode ISA with fixed, machine-verifiable semantics. No model can misunderstand another model's constraint because the bytecode means the same thing on every runtime.

### What's Actually Here

- **`cfp.py`** — full encode/decode pipeline, `FluxVM` sandboxed executor, `ConstraintManifold` for room-level state, `RoomMonitor` for PLATO polling
- **`src/cfp_v2.py`** — Lamport clock causal ordering, prediction-based verification (O(1) compare vs O(n) recompute), constraint lifecycle state machine (Active→Superseded→Retracted)
- **`tests/test_cfp_v2.py`** — 15 passing tests
- **`flux_plato_search.py`** — semantic search over PLATO tiles using flux-index embeddings (found in **plato-vessel-core** repo)

### The FLUX ISA (Forgotten Detail)

The opcode table has **fleet math operators** baked in at the bytecode level:

| Opcode | Hex | What It Does |
|--------|-----|-------------|
| `LAMAN` | 0x62 | `V, E → flag if E == 2V-3` — directly checks Laman rigidity |
| `HZERO` | 0x63 | `V,E,C → β₁; flag=β₁>V-2` — H¹ cohomology dimension check |
| `VECDOT` | 0x60 | Dot product of two values |
| `VECNORM` | 0x61 | Absolute value / norm |

This means constraint theory (Laman's theorem, cohomology of constraint graphs, Eisenstein drift) is **already a bytecode primitive**. Two agents can exchange a `LAMAN` instruction and both get the same answer. No drift. No interpretation.

### The Compare-vs-Compute Breakthrough

CFP v2 introduces prediction tiles with `t_minus_event` annotations. During planning, agents emit a forecast of what a constraint will evaluate to. At runtime, O(1) comparison confirms or falsifies the prediction. No need to re-execute the bytecode unless the prediction is wrong. This is simulation-first verification — the same pattern as the perpetual daemon, the same pattern as PLATO-NG's loop rooms.

### Why This Was Almost Lost

The README reads like a completed project. It has a `CFP-V2-SPEC.md`. It has passing tests. It looks *done*. And because it looks done, nobody asks "what's next?" But the gold is in what's built and waiting:

1. No agent in the fleet actually **uses** CFP tiles yet — the protocol is implemented but disconnected
2. `flux_plato_search.py` lives in **plato-vessel-core** instead of here (orphan file)
3. The RoomMonitor connects to PLATO but nothing feeds CFP tiles back into agent decision-making

### Rebirth Path

- Bridge CFP into the perpetual daemon: have the daemon emit CFP tiles for each experiment result
- Wire `RoomMonitor` into Oracle1's real PLATO rooms (oracle1-bridge, fleet-ops)
- Create a `cfp-aware` agent variant that uses bytecode comparison instead of text comparison for constraint understanding
- Promote `flux_plato_search.py` here where it belongs
