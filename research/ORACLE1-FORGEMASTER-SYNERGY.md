# Oracle1 × Forgemaster — Full Synergy

> *The fleet doesn't need more parts. It needs them connected.*

## The 6 Connection Points

### 1. Deadband Protocol = Eisenstein Snap (P0→P1→P2 = Voronoï Fix)

Oracle1's deadband: P0=greedy (fails 0/50), P1=9-candidate safe cell, P2=true nearest neighbor.
Forgemaster's Eisenstein Snap: hexagonal lattice quantization with covering radius guarantee.

**Unity:** The deadband IS Eisenstein snapping applied to constraint satisfaction. P1's 9-candidate search is exactly the Voronoï fix for naive snap failures. P2 is the true nearest-neighbor.

**Bridge:** `research/DEADBAND-SNAP-UNIFICATION.md` — formalize the equivalence.

### 2. Gatekeeper → FLUX Constraint Enforcement

Oracle1's Gatekeeper (544 lines): allow/deny/remediate on tile submissions.
Forgemaster's FLUX: PASS/PANIC/snap-to-valid in bytecode.

**Unity:** Gatekeeper returns {allow, deny, remediate}. FLUX constraint_check returns {PASS, PANIC, snap nearest}. Same three-valued logic at different abstraction levels.

**Bridge:** Gatekeeper-as-FLUX — policy engine → constraint check → FLUX bytecode execution.

### 3. Neural PLATO LoRA-Swap → Fluxile Agent Blocks

Oracle1: hot-swaps LoRA adapters as "rooms" (~50MB, <2s).
Forgemaster: Fluxile agent blocks with `lora:` directive compile to FLUX bytecode with A2A opcodes.

**Unity:** Same architecture — room as modular capability, hot-swapped on demand. Different layers: Python runtime loading weights vs FLUX bytecode with opcodes.

### 4. Self-Play Arena → Adversarial Constraint Testing

Oracle1: ELO-rated agent competition (744 lines), agents compete in the arena.
Forgemaster: Adversarial paper — testing claims against hostile models.

**Unity:** Same mechanism. Register constraint claims as policies. Let agents compete to break them. The arena is the testing ground for constraint validity.

### 5. Skill Forge → Snapkit Continuous Training

Oracle1: drill arena — structured iteration + self-critique.
Forgemaster: snapkit — generate random points → snap → verify → score → improve.

**Unity:** The drill arena IS the training loop for snapkit. Same cycle: generate → test → verify → improve.

### 6. Tile Quality Scorer → Constraint Quality Metric

Oracle1: regex-based tile quality indicators.
Forgemaster: Eisenstein, Voronoï, holonomy, deadband, Hurst patterns.

**Unity:** Add constraint-theory patterns to the quality scorer. Holonomy coherence as a quality metric. Emergence severity as a signal.

---

## The Bridge: Gatekeeper-as-FLUX

The single connection that ties everything together:

```
Oracle1's Stack              Forgemaster's Stack
─────────────────            ─────────────────
PLATO (tile store)           FLUX (bytecode VM)
Gatekeeper (policy)  ───►    constraint_check (bytecode)
Services (Python)            Algorithms (FLUX)
                         │
                    Bridge:
                    Gatekeeper compiles policies 
                    to FLUX bytecode. Every service
                    enforces constraints natively.
                         │
                    Result:
                    allow  → PASS
                    deny   → PANIC
                    remediate → snap to nearest valid state
                         │
                    One constraint system across the entire fleet.
```

---

## What Already Connects

- **plato-midi-bridge**: Oracle1 → FM. Court-jester tile format translated to PLATO protocol.
- **flux-tensor-midi**: FM → Oracle1. PLATO rooms as musicians. Installed and connected.
- **jester-plato-bridge**: FM → Oracle1. Court-jester MCP server bridged to PLATO.
- **the-lock**: Shared reasoning infrastructure. Available on port 4043.
- **aesop-mcp**: Narrative layer. Reads FM's archetypes, tells fables about both our data.
- **negspace-interpolator**: Oracle1. Field reconstruction works on any PLATO data including FM's.

---

## What Needs Building

1. **Gatekeeper-as-FLUX compiler** — compile Gatekeeper policies to FLUX bytecode
2. **FLUX-as-Gatekeeper runtime** — execute compiled policies in the Gatekeeper
3. **Co-trained snapkit + deadband** — the Arena as training ground for both
4. **Unified constraint quality metric** — holonomy + tile quality + emergence = single score

**The fleet doesn't need more parts. It needs them connected.**
