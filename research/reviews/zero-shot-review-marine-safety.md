# ZERO-SHOT REVIEW: FLUX Certify
## Marine Safety Engineer Perspective — DNV/ABS Evaluation

*Evaluated 2026-05-06. Documents: case study, cocapn.ai landing page, fleet-math-arxiv.md.*

---

## READER TEST

**1. In one sentence, what does FLUX Certify actually do?**

FLUX Certify compiles safety constraints written in GUARD DSL to FLUX-C bytecode and generates Coq proof certificates for the guard expression subset, replacing a manual 3-engineer, 6-week Coq workflow with a 1-engineer, 1-week automated pipeline.

**2. What specific standard does it claim to help with?**

It claims to map to DO-254 DAL A, DNV AROS, ABS UR E26/E27, UK MCA, and IEC 61508 SIL 2–4 — and the landing page adds ISO 26262 ASIL-D (absent from the arxiv paper, a red flag I return to below).

**3. What does it NOT yet do?**

- Full FLUX-C ISA formal verification is **in progress**, not complete
- The Coq proof chain covers only the **guard expression subset** — not the full ISA
- Empirical validation of H1 cohomology accuracy claims is **pending a controlled experiment** — the paper explicitly retracts the earlier "100% vs 62%" claim as unsubstantiated
- ZHC is **geometric consistency**, not Byzantine fault tolerance — FLP impossibility applies and is acknowledged
- FLUX Certify produces proof **artifacts**, not actual certifications — the auditor still needs to accept them

**4. If you were a DNV safety engineer, what would make you take the $10K pilot seriously vs dismiss it?**

Take it seriously if: they send me a real constraint from my actual vessel system and I can inspect the Coq proof file directly. The $10K gets me bytecode, a proof certificate, and a deployment guide — I can trace every line. That's the only thing that matters: can I hand this to my certification reviewer and will they accept it?

Dismiss it if: the marketing materials claim more than the technical paper backs up. If the sales narrative implies full ISA verification when the paper says "in progress," that's a disqualifier. I don't care about compelling vision — I care about traceable evidence.

**5. What would make you excited vs skeptical?**

*Excited:* The honest table in the case study. "What we have vs what we don't" is exactly what I want from a vendor. The 50ms compilation latency is measured, the partial proof in FluxC.v is referenced by name, and the FLP impossibility caveat on ZHC is explicit. This team understands that I need to know where the edges are.

*Skeptical:* The gap between the landing page and the arxiv paper. The landing page lists ISO 26262 ASIL-D prominently alongside DO-254 and IEC 61508. The paper does not mention ISO 26262 at all. ISO 26262 is an automotive standard — if FLUX Certify's Coq proof chain doesn't cover automotive use cases, why is it on the homepage? This looks like feature list padding, and it makes me wonder what else is overstated.

**6. What's the single most compelling thing you read?**

> "FLUX Certify doesn't change the standard. It changes the cost of meeting it."

That's the correct framing. It tells me this team understands the certification problem isn't about getting around the requirements — it's about the economics of compliance. That framing is rare in safety tech pitches.

**7. What's the single most confusing thing?**

ZHC is described as "Zero Holonomy Consensus" throughout — the word "consensus" is in the name — but the paper explicitly states "ZHC provides geometric consistency, NOT Byzantine fault tolerance" and acknowledges FLP impossibility applies. So it's a consistency check, not a consensus protocol. But the name, the 38ms latency claim, and the positioning alongside PBFT comparisons all imply it's solving the consensus problem. I spent real time trying to understand what ZHC actually does for a production vessel safety system, and I'm still not sure. If I'm confused as a mathematically literate engineer, a certification reviewer will be completely lost.

**8. Rate your confidence that this team can actually deliver: 1-10. Why?**

**4/10.**

They have four agents running in production. The Coq partial proof exists. The 50ms latency is measured. These are real. But:

- The H1 cohomology "100% accuracy" claim was unsubstantiated — the paper retracts it. That's a significant accuracy claim that was published, distributed, and had to be corrected.
- Full ISA formal verification is "in progress" with no timeline.
- The ZHC/FLP situation suggests either the team doesn't fully understand the limitation or they're deliberately obscuring it — neither inspires confidence.
- The ISO 26262 discrepancy between the landing page and the paper is a factual error that should not exist.

The team is building something real and is more honest than most. But "more honest than most" is not the bar for a $10K pilot from a DNV safety engineer. The bar is "can I trust every claim they make."

---

## CASE STUDY vs LANDING PAGE: Are They Saying the Same Thing?

**No. They are telling different stories.**

The **case study** (flux-certify-pilot-case-study.md) is a technical document that mostly holds up. It has specific numbers, an explicit "what we have vs what we don't" section, honest acknowledgment of proof chain limitations, and clear descriptions of what the pilot delivers. It also has the ISO 26262 omission (mentioned but not detailed — it appears in the standards table but not as a detailed mapping the way DO-254 and IEC 61508 are explained).

The **landing page** (cocapn.ai/index.php) has three accuracy problems:

1. **ISO 26262 ASIL-D** is listed prominently on the homepage as a supported standard alongside DO-254 and IEC 61508. It does not appear anywhere in the arxiv paper. This is either a lie or a placeholder that should have been caught in review.

2. The **"4 agents running in production"** claim appears as a live radar visualization. This is cute marketing but it is not evidence of FLUX Certify's safety-critical capability. The agents are infrastructure — they don't prove the proof chain works for actual marine certification.

3. The **ZHC claim** — "38ms geometric consistency check" — is displayed without the FLP impossibility caveat that fills an entire section of the paper. A certification reviewer reading the homepage would conclude ZHC is a fast consensus protocol. The paper says it is not.

**Which is more credible?**

The **case study** is more credible. It has the specific numbers, the explicit gaps, the honest framing. The arxiv paper is the most credible of all — it explicitly retracts its own earlier accuracy claims, which is unusual and (for me as an evaluator) actually increases trust.

The landing page reads like it was written by a different team that didn't carefully read the technical paper.

---

## BOTTOM LINE

**Would I recommend the $10K pilot?** Only if the customer can name the exact constraint they want certified and is willing to read the Coq proof themselves. The $10K gets them a real proof artifact they can inspect. If they want hand-holding and marketing blur, they'll be disappointed. If they want to kick the tires on actual Coq output, it's worth $10K to find out.

**What would make me upgrade to the $50K subscription?** Real proof artifacts from my actual constraints that my certification reviewer accepts without pushback. That's it. Nothing else matters.

**What would make me walk away?** Discovering another ISO 26262 / DNV gap between what was sold and what the paper actually supports. The first one was a $10K mistake. The second would be reputational.

---
*Reviewer type: Marine Safety Engineer, DNV/ABS*
*Document versions: flux-certify-pilot-case-study.md (latest), fleet-math-arxiv.md (May 2026)*