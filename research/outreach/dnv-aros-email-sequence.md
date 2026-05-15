# DNV/AROS Email Sequence — FLUX Certify

## Email 1: Initial Outreach

**To:** [DNV AROS contact]
**Subject:** AROS autonomous ship certification — GPU constraint verification in 4 hours

Hi [Name],

Congrats on the AROS autonomous ship notations launch — rigorous constraint verification for navigation and safety-critical functions is exactly the kind of framework that makes autonomous vessel certification tractable.

I'm reaching out because we're working with marine autonomy teams on exactly the problem AROS was built to solve: GPU-based perception running in safety-critical contexts, where every constraint needs a mechanically verifiable proof trace.

Current path: manual Coq engineering, 6+ weeks per module, $240K.
FLUX Certify path: GUARD DSL → FLUX-C bytecode + Coq proof certificate in under 50ms, 4 hours.

We've handled DO-254 DAL A, ISO 26262 ASIL-D, IEC 61508 SIL 3, IEC 60945. Safe-TOPS/W = 410M CPU / 241M GPU.

Worth a 30-min call to walk one of your AROS constraint types through the tool?

Best,
Casey Digennaro
cocapn.ai/certify

---

## Email 2: Follow-up (3 days later)

**Subject:** Re: AROS autonomous ship certification — GPU constraint verification in 4 hours

Hi [Name],

Following up on my earlier note about FLUX Certify for AROS compliance.

One thing I wanted to clarify: the tool doesn't replace your existing verification workflow — it automates the constraint-to-proof layer that currently requires dedicated Coq proof engineering. Your team stays on architecture and safety case; we handle the mechanical verification.

Here's what a typical AROS constraint looks like in our system:
```
battery_soc in [0.15, 1.0] with priority CRITICAL
gps_position within_fence [[-180, -90], [180, 90]]
collision_avoidance in [0, 1] when distance_to_vessel < 500
```

Each compiles to FLUX-C bytecode with a Coq proof certificate in <50ms.

If AROS certification timelines are a bottleneck for any of your teams, happy to show you the workflow directly.

Best,
Casey

---

## Email 3: Value Add (7 days later)

**Subject:** Marine constraint verification benchmark — FLUX Certify vs manual Coq

Hi [Name],

Last note from me on this — I wanted to share some hard numbers that might be relevant to your AROS work:

**Constraint verification benchmarks:**
| Method | Time | Cost | Engineers | Proof Quality |
|--------|------|------|-----------|---------------|
| Manual Coq | 6 weeks | $240K | 3 | Mechanically verified |
| FLUX Certify | 4 hours | $8K | 1 | Mechanically verified |

These numbers are from actual GPU safety systems in automotive and marine contexts.

The $10K pilot: one real constraint from your project, one week, you decide whether it holds. Full proof trace you own.

cocapn.ai/certify — try the live demo if you want to see it work before talking.

Best,
Casey
