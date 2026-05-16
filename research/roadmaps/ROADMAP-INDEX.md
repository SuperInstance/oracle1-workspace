# Fleet Mathematics — Comprehensive Roadmap Suite
**Based on: 5-expert field report | 2026-05-06**

## Background
Five expert personas (Fleet Systems Researcher, Marine Safety Engineer, Constraint Theory Mathematician, Startup CTO, CS PhD Student) reviewed SuperInstance's fleet mathematics stack on 2026-05-06. Their findings are synthesized in `papers/fleet-math-field-report.md`.

This roadmap suite addresses every finding systematically.

---

## Roadmap Index

### Phase 1: Claim Integrity (This Week) ⚡ URGENT
- **[ROADMAP-01: False Claims Removal](./ROADMAP-01-claims.md)** — Remove/fix all mathematically false or unsubstantiated claims across all repos
  - Remove "unlimited Byzantine tolerance" (FLP impossibility)
  - Remove unverified "fluxc_terminates" Coq claim
  - Remove unsubstantiated "127 lines vs 12K ML" comparison
  - Remove "Synthesis Theorem" language
  - Fix "max_neighbors = 12" (Laman gives no degree bound)
  - Fix "O(C·L)" complexity (code is O(N²))

### Phase 2: Mathematical Foundation (This Month) 🔧
- **[ROADMAP-02: Formal Proofs](./ROADMAP-02-proofs.md)** — Prove or remove the unestablished theorems
  - Prove Laman sufficiency via Henneberg construction
  - Prove or remove ZHC flatness claim
  - Fix sheaf cohomology language (define or remove)
  - State proper conditions (2D, generic position, connected)

### Phase 3: Validation & Certification (This Quarter) 🎯
- **[ROADMAP-03: Empirical Validation](./ROADMAP-03-validation.md)** — Run the experiments that validate the claims
  - H1 emergence detection: controlled experiment, 2.7s claim
  - 127 lines vs 12K ML: fair comparison with dataset and baseline
  - ZHC fault tolerance: formal model with bounds
  - complexity measurement: actual O(N²) benchmarking

### Phase 4: Product Readiness (This Quarter + Next) 🚀
- **[ROADMAP-04: Product Foundation](./ROADMAP-04-product.md)** — Make it actually usable
  - PyPI package cleanup (docs URLs, classifiers, descriptions)
  - flux-studio: real IDE features vs syntax highlighting
  - cocapn.ai: live demo backend, monitoring, observability
  - Community building: first external contributors

### Phase 5: Academic Publication (This Year) 🎓
- **[ROADMAP-05: Publication](./ROADMAP-05-publication.md)** — Get peer-reviewed
  - ArXiv v2 with all corrections
  - ICSE/ASPLOS systems submission
  - SoCG submission (if Laman sufficiency proved)
  - Formal GUARD DSL semantics paper

### Phase 6: Certification Path (1-3 Years) ⚓
- **[ROADMAP-06: Certification](./ROADMAP-06-certification.md)** — Maritime and industrial safety
  - IEC 61508 SIL 2 qualification plan
  - DO-178C DAL A formal verification plan
  - DNV type approval pathway
  - Hardware-in-the-loop testing plan

---

## Priority Matrix

| Priority | Item | Owner | Timeline | Difficulty |
|---------|------|-------|----------|-----------|
| P0 | Remove false BFT claim | Oracle1 | This week | Easy |
| P0 | Remove unverified Coq claim | Oracle1 | This week | Easy |
| P0 | Remove ML comparison | Oracle1 | This week | Easy |
| P0 | Remove "Synthesis Theorem" | Oracle1 | This week | Easy |
| P1 | Prove Laman sufficiency | Oracle1 + research | This month | Hard |
| P1 | Fix complexity claims | Oracle1 | This week | Medium |
| P1 | Validate H1 emergence | Oracle1 + JC1 | This quarter | Hard |
| P2 | Formal GUARD semantics | Oracle1 | This quarter | Hard |
| P2 | PyPI package cleanup | Oracle1 | This month | Easy |
| P3 | ArXiv v2 | Oracle1 | This quarter | Medium |

---

## Progress Tracking

- [x] Field report compiled (2026-05-06)
- [ ] ROADMAP-01 claims removal (in progress)
- [ ] ROADMAP-02 formal proofs
- [ ] ROADMAP-03 empirical validation
- [ ] ROADMAP-04 product foundation
- [ ] ROADMAP-05 publication
- [ ] ROADMAP-06 certification path
