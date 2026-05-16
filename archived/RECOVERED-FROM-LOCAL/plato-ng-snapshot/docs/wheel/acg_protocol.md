# ACG Protocol — The Audited Context Generation Standard

## What It Is

**ACG Protocol** (from `Kos-M/acg_protocol`) defines a dual-layer standard for eliminating both factual and logical hallucinations in AI-generated content. It combines the Universal Grounding and Verification Protocol (UGVP) for source integrity with the Reasoning and Synthesis Verification Protocol (RSVP) for logical integrity. Every claim and synthesis step carries explicit, machine-auditable metadata.

## The Gold

### 1. Dual-Layer Hallucination Prevention

The core insight: hallucinations happen at two distinct levels — **factual** (claiming something false) and **logical** (reasoning incorrectly from true premises). The ACG Protocol addresses both separately:

- **Layer 1 (UGVP):** Every atomic claim carries a `[C{N}:SHI_P:{LOC}]` marker linking it to a specific source location and hash-identified document. The Source Hash Identity (SHI) is a cryptographic fingerprint of the source, making tampering detectable.
- **Layer 2 (RSVP):** Every synthesized statement (not a direct quotation) carries a `(R{M}:TYPE:DEP_IDs)` marker specifying the logical operation (CAUSAL, INFERENCE, SUMMARY, COMPARISON) and the claims it depends on. Synthetic statements cite their premises explicitly.

### 2. Veracity Audit Registry (VAR)

The VAR is the unified JSON audit trail combining source metadata and reasoning metadata. It's a machine-parseable block that a Verifier Agent can automatically check:

```json
{
  "SOURCES": [{ "SHI": "...", "Type": "WebArticle", "Verification_Status": "VERIFIED" }],
  "REASONING": [{ "RELATION_ID": "R1", "TYPE": "CAUSAL", "DEP_CLAIMS": ["C1", "C2"], "AUDIT_STATUS": "VERIFIED_LOGIC" }]
}
```

### 3. The Two-Phase Verification Workflow

An independent Verifier Agent runs a mandatory two-phase check:
1. **Phase 1 (UGVP):** Fetch each source, verify each claim's text matches the source location. Failed claims → sentences removed from output.
2. **Phase 2 (RSVP):** Check that all premises of each relationship were VERIFIED in Phase 1. Then validate the logical relationship type against the cited LOGIC_MODEL. Failed reasoning → synthesized sentences removed.

This guarantees the final output contains ONLY verifiable claims supported by validated reasoning.

### 4. Verifiable Relationship Types

The protocol defines four auditable reasoning types: CAUSAL (A led to B), INFERENCE (logical deduction), SUMMARY (generalization from multiple facts), and COMPARISON (differences/similarities). Each requires specific verification — CAUSAL needs an explicit source or validated LOGIC_MODEL, SUMMARY must be statistically representative and not contradicted by premises.

## Why It Matters

The ACG Protocol is the fleet's answer to "how do we trust what another agent produces?" In a multi-agent system where agents read each other's output and build on it, hallucination propagates catastrophically — one wrong claim becomes a million tokens of wrong reasoning. The ACG Protocol makes the provenance chain explicit, auditable, and machine-verifiable. A Verifier Agent can automatically reject any output that can't prove its sources. This is the standard for trustworthy A2A knowledge transfer.
