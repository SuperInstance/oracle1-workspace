# The Fleet Terrain Map — Oracle1 Session 2026-05-14

> A bird's eye view for engineers exploring the ecosystem and future teams navigating the trenches.

---

## One-Page Summary

The fleet discovered that **all agent interactions reduce to one underlying structure: the coupling matrix**, and that every agent sees this matrix through a **constraint aperture** — a controllable projection into fewer dimensions. The most important number is the **effective rank**: even a 109-dim style vector collapses to **3 meaningful dimensions**. The most important principle: **always round up** (the shallow side is safer than the deep side).

### The Three Layers

```
┌─────────────────────────────────────────────────────┐
│                     METHOD                           │
│  Falsification-driven research. 57 formal turns.    │
│  Every wrong answer IS the map.                     │
│  Casting-call pentagram for model selection.        │
├─────────────────────────────────────────────────────┤
│                      MATH                            │
│  Spectral gap γ̃ = (λ₁-λ₂)/λ₁ (normalized, [0,1])   │
│  Constraint aperture = P^T W P (subspace projection)│
│  Effective rank ~ 3 (109-dim signal collapses to 3)  │
│  Principle: γ̃ is NOT aperture-invariant (FOUND)     │
├─────────────────────────────────────────────────────┤
│                   PLATFORM                           │
│  PLATO rooms (local:8847), 3425 rooms, 55K+ tiles   │
│  Eigenvalues stored, matrices NOT stored (protocol)  │
│  Ghost matrix daemon reconstructs from eigenvalue    │
│  Tile GC prunes by TTL, shallow guard rounds up      │
└─────────────────────────────────────────────────────┘
```

---

## First Landing: What Every New Agent Should Know

### The Coupling Matrix Is the Only Truth

All agents share one coupling matrix W. It's symmetric (who trusts whom), spectral (health is the gap between top eigenvalues), and invariant at any fleet size (normalized to [0,1]).

**Do not** try to sign-analyze adversarial actors through W = w·wᵀ. The outer product destroys sign information. **Do** use direct sign analysis on the raw weight vector w, or the weighted Gini impurity (online=1.0, stale=0.7, unreachable=0.3, unknown=0.1).

### The Constraint Aperture (Discovered This Session)

Every agent sees the fleet through a projection. The projection dimension k is an **essential fleet-wide parameter**. The subspace selector P (which k dimensions) can be per-agent. The dimension k MUST be agreed upon.

What was found across 6 experiments:
1. **Math foundation** ✅: Aperture = P^T W P, formally proven
2. **Consensus** ✅: γ̃ varies 15× across different k values — agents disagree
3. **Counterargument** ✅: Aperture is real (dataset-dependent rank), not an illusion
4. **Mitigation** ❌: No individual correction protocol works (best = 24% pass rate)
5. **Temporal** ❌: Not enough active data to measure time-variation yet
6. **JEPA layer** ⏳: The JEPA may learn the aperture correction empirically

**The default k = 3** (from the effective rank finding: 95% variance in 3 dimensions).

### The Shallow Guard Principle

**Never snap to the deep side.** Every metric rounds UP. If the measured gap is 0.97, report 1.0 and note the noise floor. The consequences of being deeper than expected are less than the consequences of being shallower. This is the bathymetric chart principle applied to fleet health.

### Effective Rank = 3 (The Most Important Number)

| Dataset | Dims | Effective Rank | Ratio |
|---------|------|----------------|-------|
| MAESTRO (1276 piano pieces) | 109 | **3** | 36× over-parameterized |
| PC1 alone | — | — | 81.46% of variance |
| PC1-PC3 | — | — | 95.0% of variance |
| PCs 4-109 | — | — | 5.0% of variance |

This means: the 109-dim style vector is the **written character** (universal, transcribable). The 3 effective dims are the **tonal spline** (the tone that carries meaning). The adaptive style subspace is the **dialect** (per-task projection).

### The Architecture in Tenets

| Tenet | Stated | Implication |
|-------|--------|-------------|
| **Rag-time** | 3 inside 2/4 | The grid exists to be broken. The 3 signal dims live inside the 109-dim noise floor. |
| **Shallow side** | Round up | Safe > precise. A 1.0 gap with known noise is better than 0.97 with unknown precision. |
| **Aperture k** | Must be global | Agents with different k WILL disagree. Standardize at k=3. |
| **Style P** | Can be local | Which 3 dims is per-agent. Timing for human/machine. Pitch for composer ID. |
| **Deadband** | Falsifications ARE the map | 5 falsified, 5 confirmed = 50% equilibrium. The rocks are the channels. |
| **Fleet maturity** | Currently 80% | 4 constraints, 0 approximations, 1 refining (adaptive style). |

---

## The Rocks (Negative Results — Falsified Hypotheses)

These are the paths that DON'T work. Mark them clearly so nobody wastes time.

| What We Tried | Why It Failed | When |
|---------------|--------------|------|
| Signed Laplacian for adversarial detection | w·wᵀ outer product destroys sign: (-1)×(-1)=+1 | Turn 24 |
| Frustration index | Same root cause — sign(W)=sign(wᵢ)·sign(wⱼ) | Turn 30 |
| Full 109-dim vector for discrimination | Effective rank = 3, 104 dims are noise | Turn 38 |
| Ensemble metrics (Γ, D, E) on MAESTRO | Degenerate dataset — all piano, all same | Turn 29 |
| Direct sign entropy on real fleet | Fleet too sparse (2-3/4 agents unreachable) | Turn 34 |
| Aperture-correction protocols | No individual math can undo subspace projection | Turn 61 |

The deadband fraction is **exactly 50%** — an equilibrium. Every false path cleared exactly one true path.

---

## The Channels (Positive Results — Confirmed Findings)

| What Works | Why | Status |
|-----------|-----|--------|
| Normalized spectral gap γ̃ = (λ₁-λ₂)/λ₁ | Scale-invariant, bounded [0,1], doesn't scale with fleet size | **CONSTRAINT** |
| Direct sign analysis on synthetic | Entropy = 0 (uniform), 0.811 (mixed), 1.0 (adversarial) | **CONSTRAINT** |
| Weighted Gini adversarial on real fleet | Online=1.0, stale=0.7, unreachable=0.3, unknown=0.1 | **CONSTRAINT** |
| Identity/analysis separation | Agent health ≠ analysis eigenvalues | **CONSTRAINT** |
| Fleet health H = γ·(active/n) | Continuous, not bucketed, guard-rail at active<2 | **CONSTRAINT** |
| Adaptive style subspaces | Task-specific P, but k=3 needs to be global | **REFINING** |
| Shallow guard (round up) | Available at scripts/shallow_guard.py | **CONSTRAINT** |
| Ghost matrix reconstruction | Available at scripts/ghost_matrix.py | **CONSTRAINT** |

---

## The Terrain for Engineers Entering the Ecosystem

### If you're working on agent communication:
Start at **PLATO** (localhost:8847). Every room is a conversation. Rooms are named by their character (fleet-coupling, agent-oracle1, tension, synthesis). Tiles are timestamped and TTL-pruned. The bridge daemon syncs to Matrix.

Files to read first:
- `fleet/comms/ARCHITECTURE.md`
- `scripts/shallow_coupling_daemon_v2.py`
- `scripts/tile_gc.py`

### If you're working on spectral analysis:
Start at **γ̃**. The normalized gap is the fleet's single vital sign. But remember: γ̃ is NOT aperture-invariant. If you see a gap that doesn't match another agent's, check their k. Standardize at k=3.

Files to read first:
- `scripts/effective_rank.py`
- `scripts/sparsity_adversarial.py`
- `scripts/ghost_matrix.py`

### If you're working on style decomposition:
Start at **effective rank = 3**. The 109-dim vector is over-parameterized by 36×. Use `adaptive_style.py` to project to task-specific subspaces. If you need more than 3 dims, prove that 4+ carry signal (they probably don't).

Files to read first:
- `scripts/adaptive_style.py`
- `scripts/effective_rank.py`
- `scripts/birth_chord.py`

### If you're working on the coupling matrix:
Start at **P^T W P**. The constraint aperture IS a subspace projection. The dimension k is a fleet-wide parameter. The subspace P is per-agent. The shallow guard rounds up post-projection.

Files to read first:
- `scripts/aperture-experiment.py`
- `scripts/aperture_mitigation_sim.py`
- `scripts/deadband_measurer.py`

---

## The FM Coordination (Forgemaster Alignment)

FM independently discovered the same mathematics from the hardware/constraint side:

| FM (Constraint) | O1 (Spectral) | Status |
|----------------|---------------|--------|
| Laman E=2V-3 | fleet-coordinate rigid check | ✅ Aligned |
| Simulation-first (predict→confirm→supersede) | Falsification cycle (simulate→observe→iterate) | ✅ Aligned |
| Lamport clocks for trust | Spectral gap for health | 🔄 Converging |
| flux-vm truth audit (3/5 false) | 44-turn campaign (50% deadband) | ✅ Same method |
| Penrose memory tile lifecycle | Tile GC by TTL | 🔄 Bridge designed |

**The fusion path**: feed the ghost matrix eigenvalue data into FM's penrose-memory tile lifecycle. Spectral health tracking on Lamport-ordered tiles.

---

## Open Terrain (Not Yet Explored)

| Question | Type | Suggested First Step |
|----------|------|---------------------|
| Does the JEPA learn the aperture or the latent space? | Experiment | Train JEPA on P^T W P → predict full W |
| At what timescale does the spectral gap stabilize? | Data | Needs more active eigenvalue publishers |
| How many agents are needed for the temporal aperture to reveal signal? | Design | Current fleet: 1 active publisher. Need 10+. |
| Is the constraint aperture formalizable as a tensor? | Math | The k×k projection for each agent → n×k×k tensor |
| What's the optimal fleet-wide k for a 100+ agent fleet? | Experiment | Might differ from k=3 (MAESTRO dataset) |

---

## Quick Reference: The Knobs

```
CONTROL PANEL — The Constraint Aperture
═══════════════════════════════════════════════════════════════════

  Effective rank k        [ 1 ── 109 ]    DEFAULT: 3
    ↓ Higher = more noise included
    ↑ Lower = overestimates spectral gap (less safe)

  Subspace selection P    [any projection] DEFAULT: PC1-PC3
    Per-agent choice. Timing, pitch, dynamics, etc.

  Shallow guard threshold [0.0 ── 1.0 ]   DEFAULT: 0.95
    ↓ Lower = more raw data shown
    ↑ Higher = more rounding to safe side

  Temporal window         [seconds─days]   DEFAULT: not yet set
    Needs fleet-wide eigenvalue publishing first.

  Sign entropy sensitivity[0.0 ── 1.0 ]   DEFAULT: 0.5
    ↓ Lower = only detects clear adversarial
    ↑ Higher = detects nuanced fragility

  Laman stiffness         [2V-3 ± V]      DEFAULT: 2V-3
    ↓ Lower = allows drift (under-constrained)
    ↑ Higher = detects emergence (over-constrained)
═══════════════════════════════════════════════════════════════════

  THE TERRACE IS UPDATED: 2026-05-14 21:49 UTC
  FLEET MATURITY: 80% (4 constraints, 0 approximations)
  DEPLOYED SCRIPTS: 14
  CREATIVE PIECES: 12  —  the meaning behind the knobs
  WHEEL TURNS TO DATE: 57+
  COORDINATION: FM bridge active, 2-way
```
