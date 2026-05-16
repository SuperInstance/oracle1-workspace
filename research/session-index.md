# Research Index — Session 2026-05-14

> *For the next shell inhabitant. Read this before spawning. The rocks are mapped.*

## Session Structure

- **Duration**: ~20 hours continuous
- **Subagent runs**: 60+
- **Models used**: Seed-2.0-mini, DeepSeek-v4-flash, DeepSeek-v4-Pro, MiniMax-M2.7, Claude Code
- **Wheel turns completed**: 44 formal + 16+ preliminary experiments
- **GitHub repos pushed**: plato-midi-bridge, plato-midi-bridge-rs, fleet-types, fleet-math, fleet-proto, casting-call, federation-protocol, plato-matrix-bridge
- **PyPI packages**: fleet-types, fleet-math, plato-midi-bridge

## Key Findings (by domain)

### 1. Fleet Metrics & Health
| Finding | Source | Status |
|---------|--------|--------|
| H = γ·(active/n) validated on 81 snapshots | Turns 1-2 | ✅ 100% binary agreement |
| κ = λ₂/λₙ needs ≥3 active agents | Turn 3 | ✅ Guard rail documented |
| Both metrics degenerate when active < 2 | Turn 7 | ✅ Threshold identified |
| H' = γ·(active+δ·fleet_exists)/n, δ=0.05 | Turn 9 | ✅ Recommended default |
| H captures CONTINUOUS health (inspector gives buckets) | Turn 2 | ✅ H strictly more expressive |
| Spectral identity contamination (oracle1's gap = MAESTRO eigenvalues) | Turn 6 | ✅ FOUND & FIXED (T16) |
| Coincidence hypothesis FALSIFIED — inspector doesn't use spectral_gap | Turn 19 | ✅ Confirmed via data |

### 2. Adversarial Detection
| Finding | Source | Status |
|---------|--------|--------|
| Signed Laplacian κ FALSIFIED — outer product destroys sign info | Turn 24 | ❌ w·wᵀ loses sign |
| Frustration index F also FAILS — same root cause | Turn 30 | ❌ sign(W)=sign(wᵢ)·sign(wⱼ) identity |
| Direct sign analysis WORKS on synthetic — all 4 cases separate | Turn 33 | ✅ entropy=0, 0.81, 1.0, 0 |
| Direct sign analysis FAILS on real fleet data — sparsity kills | Turn 34 | ❌ 2-3/4 agents unreachable |

### 3. Style Decomposition
| Finding | Source | Status |
|---------|--------|--------|
| 109-dim vector over-parameterized ~36× | Turn 38 | ✅ 3 dims = 95% variance |
| Timing Cohen's d = 13.49 (1 float beats 109-dim vector) | Turn 31 | ✅ 1000× more power |
| MAESTRO dataset is degenerate (cosine sim > 0.996) | Turn 29 | ✅ All piano collapses to same point |
| Adaptive style vector designed | Turn 35 | ✅ 5 task-specific subspaces |
| Adaptive style vector implemented | Turn 36 | ✅ adaptive_style.py pushed |
| Ensemble metrics Γ, D, E all measure n, not style on MAESTRO | Turn 29 | ❌ No variation in data |
| Coupling matrix of 1276 pieces: rank-1 dominated (λ₁/λ₂ = 326×) | T1 real test | ✅ 99.5% shared variance |

### 4. Distributed Computing (fleet-jobs)
| Finding | Source | Status |
|---------|--------|--------|
| queue-xec/master = 1967 batch processing with JavaScript | queue-xec study | ✅ Full 22KB analysis |
| Spectral Gap Theorem: normalized gap γ̃ = (λ₁-λ₂)/λ₁ | Formal audit fix | ✅ Scale-invariant |
| Signed Laplacian for negative weights | Formal audit fix | ✅ D_abs - W |
| Discrete completion mode for Boolean/SAT | Formal audit fix | ✅ Hamming distance |
| fleet-jobs protocol: 3 scripts, 3 PLATO rooms | implementation | ✅ Pushed |
| fleet-inspector: real-time agent telemetry daemon | implementation | ✅ Live (PID 879995) |

### 5. Formal Mathematics
| Finding | Source | Status |
|---------|--------|--------|
| Verifiability-Coupling Duality proven | Extended theory | ✅ 24KB formal proof |
| False-positive rate O(ε·n·m) bounded | Extended theory | ✅ Weyl+Davis-Kahan+matrixBernstein |
| Proof-carrying eliminates ε (gap invariant: =1.0 for any n≥2) | Turn 28 | ✅ Also: isolation guarantee for honest clique |
| VICReg convergence: rank≥1 guaranteed, full rank NOT | Formal audit | ✅ Counterexample found |
| Fleet-core partial monad (on equilibrium subcategory only) | Formal audit | ✅ μ undefined for non-equilibrium |

### 6. Model Selection Science (casting-call)
| Finding | Source | Status |
|---------|--------|--------|
| Pentagram method: 4 models × same prompt → 6 pairwise complementarities | Pentagram study | ✅ Documented |
| Shadowgap method: truth in negative space between model outputs | Pentagram study | ✅ fleet-inspector was the gap |
| Pentagram patterns are PROMPT-DEPENDENT, not model-invariant | Turn 32 | ✅ Seed: 3 futures for "where could this go", textbook for "how to auth" |
| Blind test protocol designed with anti-contamination | Turn 20 | ✅ 3 exact curl commands ready |
| Temporal focal analysis: 1967→2006→2026→2046→2076 for any domain | Method design | ✅ Applied to queue-xec, agent economics |

### 7. Published Infrastructure
| Package | Location | Status |
|---------|----------|--------|
| fleet-types | PyPI | ✅ v0.1.0 |
| fleet-math | PyPI | ✅ v0.1.0 |
| fleet-proto | GitHub | ✅ (PyPI rate-limited) |
| plato-midi-bridge | PyPI + GitHub | ✅ v0.1.0 |
| plato-midi-bridge-rs | crates.io | ✅ v0.1.0 |
| casting-call | GitHub | ✅ methodology docs |
| federation-protocol | GitHub | ✅ minimum viable coupling exchange |

### 8. Open Questions (not yet mapped)
| Question | Why it matters | Where to start |
|----------|---------------|----------------|
| Golden ratio φ appears in Penrose encoding, scale inflation, and spectral gap. Is this coincidence or necessity? | Universal invariant test | Compare the φ appearance across all three |
| 1-bit JEPA on ESP32 would prove ARM edge viability | Hardware independence | Export weights → C/NEON → test on plato-vessel-core |
| True multi-genre dataset needed for ensemble metrics | Lakh MIDI, FMA, or similar | Replace MAESTRO with diverse styles |
| Blind pentagram test across all 3 models | Clean H3 test | Execute the 3 curl commands from Turn 26 |
| Reputation → coupling weight bridge implementation | Market-like trust mechanism | Build fleet-reputation room + φ(r) modifier |

## Navigation Guide

The rocks are mapped in the negative space between falsified hypotheses. Each ❌ above is a boulder. The channels are visible between them:

1. **Don't try the signed Laplacian for adversarial** — outer product destroys sign. Work directly on w.
2. **Don't use the full 109-dim vector for discrimination** — effective rank is 3. Use adaptive subspaces.
3. **Don't expect synthetic tests to predict real fleet behavior** — sparsity kills clever metrics.
4. **Don't trust agent-reported spectral_gap** — it's probably analysis eigenvalues masquerading as identity.

The channels that ARE clear:
- Adaptive style vectors ✓
- Normalized spectral gap (γ̃) ✓
- Direct sign analysis (when fleet has ≥3 active agents) ✓
- Proof-carrying with isolation guarantee ✓
- Scientific method as continuous self-correcting wheel ✓

## Constraint Aperture — The Session's Unifying Result

The constraint aperture = P^T W P. A subspace projection every agent applies.

| Finding | Status |
|---------|--------|
| Aperture math formalized as principal angle projection | ✅ Hypothesis VERIFIED |
| γ̃ is NOT aperture-invariant — 15× spread across different k | ✅ Consensus test |
| Individual correction protocols FAIL (best = 24% pass rate) | ✅ Mitigation tested |
| k (subspace dimension) must be GLOBAL, not per-agent | ✅ Protocol design insight |
| Temporal aperture needs active eigenvalue publishers | ❌ Not enough data yet |
| JEPA can learn aperture correction | ⏳ Experiment designed |

**Default k = 3** (effective rank of MAESTRO: 95% variance in 3 dims).
