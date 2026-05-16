# Gatekeeper-as-FLUX — The Complete Mesh

> *Every Oracle1 service enforces FLUX constraints natively at every level of the abstraction stack.*

## The Abstraction Stack (6 Planes × 2 Workers)

Oracle1's nervous system and FM's skeleton, connected at every plane:

```
Plane 5 (Intent)     Gatekeeper Policy       ←───  Oracle1's domain: natural language rules
                     "answers must be 20+    │     FM's domain: GUARD DSL constraints
                      chars, no absolute     │
                      claims"                │
─────────────────────────────────────────────┼──────────────────────────────────
Plane 4 (Domain)     PLATO room domains      │     Fleet coordination vocabulary
                     forge, harbor, arena,   │     Eisenstein, Voronoï, holonomy
                     disc-golf-math          │
─────────────────────────────────────────────┼──────────────────────────────────
Plane 3 (IR)         Structured constraint   │     Bridge point: Gatekeeper IR
                     JSON: {field, op, val}  │     → FLUX-callable compilation
─────────────────────────────────────────────┼──────────────────────────────────
Plane 2 (Bytecode)   FLUX-C / FLUX-X         │     FM's domain: 42-247 opcodes
                     RANGE_CHECK, ASSERT,     │     constraint_check.flux
                     GUARD_TRAP              │
─────────────────────────────────────────────┼──────────────────────────────────
Plane 1 (Native)     Python http.server       │     Oracle1's 30+ services
                     Rust SDK, TypeScript     │     FM's flux-tensor-midi
─────────────────────────────────────────────┼──────────────────────────────────
Plane 0 (Metal)      SIMD NEON/AVX-512       │     Shared: 64B=1zmm=1 constraint
                     fleet_math.h            │     Oracle1's benchmarks: 188M/s
```

## The Bridge: Gatekeeper-IR → FLUX-C

Oracle1's Gatekeeper currently evaluates policies in Python:
```python
def validate(tile):
    if len(tile["answer"]) < 20:
        return DENY("Answer too short")
    if is_absolute(tile["answer"]):
        return DENY("Absolute claim")
    if passes_all(tile):
        return ALLOW
```

This becomes a FLUX-C program:
```flux-c
; Gatekeeper policy as FLUX-C
; Policy: answer >= 20 chars, no absolute claims

PUSH 20              ; Min length
LOAD_VAR answer_len  ; Load answer length
SWAP                 ; Stack: [answer_len, 20]
LT                   ; answer_len < 20?
NOT                  ; invert
ASSERT               ; Must pass (answer >= 20 chars)

; Check absolute claims
LOAD_VAR has_absolute
NOT                  ; invert (we want NOT has_absolute)
ASSERT               ; Must pass

; If both pass, return 1 (ALLOW)
PUSH 1
STORE result
HALT
```

## 6 Connections — Already Built

| # | Connection | Already Connects Through |
|---|-----------|--------------------------|
| 1 | Deadband = Eisenstein | Same math, different notation |
| 2 | Gatekeeper = FLUX constraint | Bridge above |
| 3 | LoRA-swap = Fluxile | Same concept, different layers |
| 4 | Arena = Adversarial | FLUX as policy, Arena as test |
| 5 | Skill Forge = Snapkit | Same training loop |
| 6 | Quality = Holonomy | Add constraint metrics |

## What to Build Next

1. **Gatekeeper-IR**: JSON schema for structured constraint representation
2. **IR-to-FLUX compiler**: Python module that emits FLUX-C bytecode from Gatekeeper IR
3. **FLUX-to-ALLOW bridge**: FLUX execution result → Gatekeeper verdict

The fleet already runs. This just makes every service speak the same constraint language.
