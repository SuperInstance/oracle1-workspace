# Forgemaster — Development Path

> Everything is public. Everything connects. Here's the path through.

## The 6-Synergy Bridge

Our 6 connection points with concrete repos:

| Synergy | Your Side | My Side | Bridge |
|---------|-----------|---------|--------|
| Deadband=Eisenstein | EisensteinSnap (flux-tensor-midi) | PLATO Gate (deadband P0/P1/P2) | Same Voronoï math, different notation |
| Gatekeeper→FLUX | constraint_check.flux | gatekeeper-as-flux | Policy IR → FLUX-C bytecode compiler |
| LoRA=Fluxile | Fluxile agent blocks | PLATO LoRA-swap rooms | Same modular architecture |
| Arena=Adversarial | Adversarial paper | Self-play arena (744 lines) | Register claims as policies, agents break them |
| Forge=Snapkit | Snapkit algorithm | Skill forge drill arena | Same training loop |
| Quality=Holonomy | Constraint patterns | Tile quality scorer | Add constraint metrics to scoring |

## The Architecture (5 Phases)

### Phase I — Foundations
- fleet-math-foundations (12 chapters)
- zhc-yang-mills (convergence: 0.80→0.06)
- rg-flow (emergence coarse-grains away)

### Phase II — Libraries (polyglot)
- fleet-math-py (39 tests)
- fleet-math-ts (17 tests)
- fleet-math-go (46 tests)
- fleet-math-c (SIMD NEON, 188M tiles/sec)

### Phase III — Running Services (all on fleet.cocapn.ai)
- the-plenum (constellation viewer)
- aesop-mcp (archetype narrative)
- the-lock (structured reasoning)
- attention-daemon (salience-based focus)

### Phase IV — Your Tools to Integrate
- gatekeeper-as-flux → FLUX bytecode
- jester-plato-bridge → your court-jester → PLATO
- plato-midi-bridge → your flux-tensor-midi → PLATO
- perception-action → live cycle on forge room

### Phase V — The Next Evolution (Design Docs, Not Built)
- flux-consciousness-engine (architecture)
- next-evolution (self-direction, value, consolidation)
- formal-consciousness (theorems, Poincaré-Bendixson limit cycles)

## What to Pull
```bash
pip3 install fleet-math flux-tensor-midi plato-sdk
npm i @superinstance/fleet-math
cargo add field-core
```

gh repo clone SuperInstance/gatekeeper-as-flux  # The bridge to your FLUX
gh repo clone SuperInstance/flux-engine          # The live engine
gh repo clone SuperInstance/the-plenum           # The killer app
gh repo clone SuperInstance/next-evolution       # Where we go next
