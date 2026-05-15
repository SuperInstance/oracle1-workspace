# ROADMAP-05: Academic Publication
**Phase 5 | Priority: P2 | Timeline: This Year**

## Publication Strategy

### Target Venues (by priority)

| Venue | Type | Fit | Deadline | Notes |
|-------|------|-----|---------|-------|
| ASPLOS | Systems | High | ~Sep 2026 | Hardware+systems, LLVM work fits |
| ICSE | Systems/Empirical | High | ~Oct 2026 | Empirical validation track |
| ESOP | Theory | Medium | ~Nov 2026 | Programming languages theory |
| SoCG | Applied Math | Medium | ~May 2027 | If Laman sufficiency proved |
| OOPSLA | Systems | Medium | ~Mar 2027 | Language/PL work |

---

## Submission: ArXiv v2 (immediate)

**Current state:** ArXiv paper exists with false claims
**After ROADMAP-01:** Strip false claims, add FLP caveat, fix complexity
**Target:** Update within 2 weeks of ROADMAP-01 completion

**Sections to update:**
1. Abstract: remove "unlimited Byzantine tolerance"
2. Introduction: add FLP caveat, remove "127 lines" comparison
3. Related Work: add Laman (1970), Tay-Whiteley (1984), FLP (1985)
4. Conclusions: provisional language where needed

---

## Submission: ASPLOS 2027 (ambitious, ~Sep 2026)

**Paper concept:** "Fleet Mathematics: Geometric Constraints Replace ML for Safety-Critical Distributed Coordination"

**Novel contributions:**
1. ZHC: geometric consensus condition with formal model (NOT Byzantine tolerance)
2. H1 emergence detection: topological invariant for coordination failure prediction
3. PLATO: production deployed fleet coordination system
4. Empirical: 47,832 tiles of field data, 4-vessel fleet, 6 months

**Key weak point:** Still missing formal verification of bytecode certifier

---

## Submission: ICSE 2027 (achievable, ~Oct 2026)

**Paper concept:** "From 12K Lines to 127: Replacing ML with Integer Arithmetic for Safety-Critical Guard Checking"

**Novel contributions:**
1. GUARD DSL: Turing-incomplete DSL for safety-critical checking
2. Formal semantics: Galois connection-based integer refinement
3. Empirical: fair comparison on a defined task with dataset
4. Production: deployed at cocapn.ai

**Key weak point:** The "fair comparison" requires EXP-02 to be done

---

## Submission: SoCG 2027 (requires PROOF-01, ~May 2027)

**Paper concept:** "Rigidity-Theoretic Self-Coordination of Multi-Agent Fleets"

**Novel contributions:**
1. Fleet rigidity: Laman condition + fleet-specific interpretation
2. H1 emergence detection: topological invariant for over-constrained fleets
3. ZHC closure: geometric consistency condition with formal model
4. Connection to rigidity matroids and bar-joint frameworks

**Key weak point:** Needs PROOF-01 (Henneberg construction) and formal review by rigidity theorist

---

## Pre-Submission Checklist

- [ ] ArXiv v2 posted with all corrections
- [ ] EXP-01: H1 emergence validation complete
- [ ] EXP-02: 127 vs 12K ML comparison run
- [ ] EXP-03: ZHC fault tolerance bounds documented
- [ ] PROOF-01: Henneberg construction in code
- [ ] External co-author identified (advisor, collaborator)
- [ ] Writing feedback from non-SuperInstance reader
- [ ] All code open-sourced and reproducible
