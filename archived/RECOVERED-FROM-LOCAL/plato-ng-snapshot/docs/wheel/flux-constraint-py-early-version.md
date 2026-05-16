# ⚰️ flux-constraint-py-early-version — Archived Python Bindings Placeholder

**Repo #49** | Created: 2026-05-11 | Status: 🪦 ARCHIVED (2026-05-13)

## What Was Found

An archived experiment — early attempt at Python bindings for FM's constraint engine. The repo contains three files totaling ~70 lines of actual code. The README is honest: "Empty Python bindings placeholder — no code was written."

## Forgotten Gold

### 1. Design Intent in the README

The README reveals the original vision clearly:
- **Purpose**: Python bindings for FM's constraint engine (the GUARD DSL → FLUX bytecode pipeline)
- **Why it died**: The implementation "just didn't land" — the bindings were never fully developed
- **Superseded by**: Tile lifecycle, Lamport clocks, and simulation-first coordination (the fleet's current approach)

### 2. The INT8 Constraint Checker Prototype

The 30-line `__init__.py` contains a working miniature constraint checker:

```python
class Constraint:
    def __init__(self, name, lo, hi, severity="critical"):
    def check(self, value):  # returns ConstraintResult with error_mask
```

Features present even in this stub:
- **Saturation**: INT8 saturation (-127 to 127) — values outside range clamped, not rejected
- **Error masking**: bitfield (bit 0 = low violation, bit 1 = high violation)
- **Constraint sets**: named collections with batch evaluation
- **Presets**: 4 domain-specific constraint sets (aviation, medical, maritime, automotive) — hinting at the fleet's original maritime/aerospace use cases

### 3. The Preset Library — Design Clues

The presets reveal what domains the fleet was initially targeting:
- **aviation**: altitude (-100 to 50,000 ft), speed, vertical speed
- **medical**: heart rate, blood pressure (sys/dia), SpO₂
- **maritime**: depth (0-12,000m), heading, speed — *matches the ship/fishing fleet metaphor*
- **automotive**: RPM, coolant, oil pressure

The maritime preset's heading constraint (0-360, "warning" severity) directly connects to the Cocapn brand identity — the lighthouse, the radar rings, the fleet-as-fishery.

### 4. What the Fleet Learned

This archive exists to teach a lesson: **early binding attempts fail when the upstream spec isn't stable.** The constraint engine matured into FLUX-ISA (42 opcodes + 13 X2 opcodes) with Eisenstein geometry, holonomy consensus, and temporal operations — none of which existed when this repo was created.

The fleet's current approach (tile lifecycle + Lamport clocks + simulation-first coordination) is more abstract and language-agnostic. This repo is the fossil that shows why.

## PLATO-NG Integration Path

1. **Don't rebuild this**: The constraint checking pattern is dead. PLATO-NG should use FLUX-ISA for constraint enforcement, not Python bindings
2. **Copy the INT8 saturation pattern**: The `saturate(val)` function is a valid pattern for any low-memory constraint enforcement (ESP32, edge devices)
3. **Study the preset design**: Domain-specific constraint sets are a good UX pattern for PLATO-NG's rule creation
4. **The maritime connection**: The fleet's identity runs deeper than logos — the constraint presets show maritime logic at the fleet's core

---

*Some repos are gravestones. They mark where a design died so a better one could be born.*
