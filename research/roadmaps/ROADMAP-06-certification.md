# ROADMAP-06: Certification Path
**Phase 6 | Priority: P3 | Timeline: 1-3 Years**

## Certification Realities

The Marine Safety Engineer was blunt: DNV type approval takes 5-10 years. IEC 61508 SIL 2 takes 3-5 years. This is not a criticism — it's the reality of life-critical systems certification.

This roadmap is about positioning for that path, not achieving it in one quarter.

---

## Current TRL Assessment

| Component | TRL | Evidence |
|-----------|-----|----------|
| GUARD DSL | TRL 4 | Validated in lab on component level |
| FLUX-C Bytecode | TRL 3 | Proof of concept, no formal verification |
| Bytecode Certifier | TRL 3 | Prototype exists, not verified |
| Fleet Coordinate | TRL 4 | Validated in simulated environments |
| PLATO System | TRL 5 | System validated in relevant environment |
| cocapn.ai Certify | TRL 4 | Component and lab validation, live demo |

**Target for 1-year:** TRL 5 for full pipeline, TRL 6 for PLATO

---

## IEC 61508 SIL 2 Tool Qualification (3-5 years)

### Phase A: Planning (Year 1)
- [ ] Write Software Quality Assurance Plan (SQAP)
- [ ] Write Software Verification Plan (SVP)
- [ ] Define tool qualification boundary (what's being qualified)
- [ ] Identify required documentation per IEC 61508-3

### Phase B: Implementation (Year 2)
- [ ] Formal semantics for GUARD DSL (PROOF-level)
- [ ] Verified compiler: GUARD → FLUX-C (Coq or Lean)
- [ ] Verified bytecode interpreter (Coq or Lean)
- [ ] Test suite: 100% MC/DC coverage on certifier

### Phase C: Qualification (Year 3)
- [ ] Independent assessment by certified lab
- [ ] Generate qualification evidence package
- [ ] Submit to certification authority

---

## DO-178C DAL A (3-5 years for flight)

If maritime isn't the target, DO-178C DAL A is the gold standard for life-critical software.

**Key differences from IEC 61508:**
- Requires actual aircraft/hardware-in-the-loop testing
- Requires MC/DC (Modified Condition/Decision Coverage) — 100%
- Independent verification required

**Prerequisite:** Formal semantics + verified compiler (same as IEC 61508)

---

## DNV Type Approval (5-10 years)

For autonomous vessel certification (the stated target market), DNV has specific requirements:
- IEC 60945: Marine navigation equipment
- MSC.1 Circ. 1512: Guidelines for MASS (Maritime Autonomous Surface Ships)
- DNV-GL-RP-051: Guidelines for secure software development

**Prerequisites before even starting:**
1. Formal verification of bytecode certifier
2. WCET (Worst-Case Execution Time) analysis
3. Hardware-in-the-loop testing
4. Independent assessment by DNV
5. Safety case document (160+ pages minimum)

---

## Realistic Near-Term Certification Goals (This Year)

1. **Write IEC 61508 qualification plan** (not execute it — write the plan)
2. **Get formal verification started** on bytecode certifier (even a sketch)
3. **Commission independent code audit** from a certified safety engineer
4. **Document the safety case** in a structured format

**These don't achieve certification, but they start the paper trail.**
