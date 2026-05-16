# LinkedIn InMail Templates — FLUX Certify

## Target A: DNV (Maritime / AROS Division)

**Subject:** AROS certification + GPU-based perception — quick question

Hi [Name],

Congrats on the AROS autonomous ship notations launch — formal verification of safety constraints is no small feat, and I know that framework demands rigor at every layer.

We're working with marine autonomy teams on exactly the problem AROS was built to solve: GPU-based perception running in safety-critical contexts. Every constraint — battery limits, geospatial fences, sensor thresholds — needs a proof trace an auditor can sign off on. The current path is manual Coq engineering that stretches 6+ weeks per module.

FLUX Certify automates the constraint-to-proof pipeline. Engineers write in GUARD DSL, we emit FLUX-C bytecode with a Coq certificate in under 50ms. The `fluxc_terminates` theorem guarantees structural halt — that's a proof, not a test.

Worth a 30-min call to map one of your constraints through the tool? No commitment, just a technical walkthrough.

Best,
[Your name]
cocapn.ai/certify

---

## Target B: ABS (Marine / Smart Functions)

**Subject:** New Technology Qualification for GPU safety systems — quick question

Hi [Name],

ABS's New Technology Qualification process for AI-enabled marine electronics is setting the bar for the industry — and I imagine GPU-based safety perception is showing up in more projects than a year ago.

The challenge with NTQ is that each module needs a proof trace reviewers can independently verify. Manual Coq proof engineering handles it — but at 6 weeks and $240K per module, the queue becomes the bottleneck.

FLUX Certify replaces that pipeline. Write constraints in GUARD DSL, get FLUX-C bytecode with a Coq proof certificate in under 50ms. Same DO-254 DAL A compliance, same auditor sign-off, no manual proof engineering.

I'd love to walk through one constraint from a typical ABS-type project — about 30 minutes — to show how the flow works in practice.

Best,
[Your name]
cocapn.ai/certify

---

## Target C: ISO 26262 Consultant / Embedded Automotive

**Subject:** Cutting GPU safety verification from 6 weeks to 4 hours

Hi [Name],

You're probably getting this question constantly from clients — but GPU safety verification is breaking teams that thought they were close to production.

The math is straightforward: 40–120 constraints per production GPU safety system, manual Coq proof engineering, simulation regression, reviewer ambiguity flags that restart the clock. Six weeks, $240K per module. Three engineers tied up.

FLUX Certify automates the whole thing. GUARD DSL → FLUX-C bytecode → Coq proof certificate in under 50ms. DO-254 DAL A, ISO 26262 ASIL-D, same proof quality. 410M Safe-TOPS/W on CPU, 241M on GPU.

If you've got clients struggling with the Coq bottleneck, this might be worth a 30-min call to see whether one constraint could validate the full flow.

Best,
[Your name]
cocapn.ai/certify
