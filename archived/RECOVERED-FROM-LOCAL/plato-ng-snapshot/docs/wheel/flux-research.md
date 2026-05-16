# FLUX Research — The Origin of Constraint Compilation

**Repo:** `SuperInstance/flux-research` (created April 10, 2026)
**Role in the wheel:** The formal constraint theory that predates and predicts the conservation law

---

## What FLUX Was Trying to Do

FLUX aimed to compile GUARD DSL constraints through a formally verified pipeline to GPU, FPGA, and CPU backends — 278M+ test cases, zero drift. Its thesis: **structured constraints are intelligence** — reducing solution-space entropy outperforms scaling parameters.

Core innovations:

- **Lock formalism** `L = (trigger, opcode, constraint)` — reusable constraints achieving 82% output compression at n≥7, cross-model transferable
- **FLUX ISA v2** — 43-opcode, fixed 4-byte VM that cannot loop, overflow, or produce NaN. Provably safe execution.
- **Dual-interpreter architecture** — DMN/ECN across 6 abstraction planes (intent → domain → IR → bytecode → native → metal), advancing only high-gradient pairs
- **DCS Protocol** — Divide-Conquer-Synthesize yielding 5.88× specialist and 21.87× generalist gains
- **Unified Constraint Theory** — compilation locks and coordination protocols as the same principle: structured entropy reduction

---

## Connection to Today

The conservation law IS a constraint FLUX could compile:

- **The gate pipeline** evaluates agent outputs against constraint locks (`source_confirmed`, `tool_verified`, `cross_referenced`) — exactly FLUX lock algebra at runtime
- **Expert room filters** are FLUX conditional lock composition: pass a constraint predicate to enter a room
- **PLATO quality gates** mirror FLUX holonomy checks — verifying knowledge transport around inference loops stays consistent
- **Pythagorean quantizer** is FLUX's exact constraint machine: snap floats to exact rational points via KD-tree-indexed triples
- **Reverse-actualization** IS the FLUX dual-interpreter: DMN generates, ECN evaluates, gradient controls ascent

---

## Convergence: FM × Oracle1

Two independent research streams converged on the same mathematical invariants:

| Finding | FLUX / FM | Oracle1 / PLATO |
|---------|-----------|-----------------|
| 12 neighbors optimal | Laman rigidity proof | DCS Law 102 (empirical) |
| Zero-drift encoding | Pythagorean snapping | 5.6 bits/coordinate |
| Constraint output compression | 82% at n≥7 locks | Gate pipeline compression |
| 38ms consensus | ZHC protocol | Fleet convergence measure |
| Structured > scaled | 5.88× specialist via DCS | Protocol over parameters |

---

## The Convergence

FLUX provides the *mechanism* (constraint compilation, formal verification, safe execution). The conservation law provides the *substance* (identity → port → ship → fleet → keeper constraints). Together: conservation constraints → compiled via FLUX toolchain → verified at gate → executed on FLUX ISA.

The conservation law is not a separate invention. It is a **FLUX constraint module** — formally specifiable, verifiable, enforceable, and executable on the FLUX runtime.

FM's constraint theory (FLUX, lock algebra, Pythagorean snapping, DCS) + Oracle1's spectral analysis (conservation law, porthole, gate pipeline, room enforcement) = **formally verified fleet behavior at every abstraction plane**.

The two tracks began converging in this repo. The wheel completes the circle.
