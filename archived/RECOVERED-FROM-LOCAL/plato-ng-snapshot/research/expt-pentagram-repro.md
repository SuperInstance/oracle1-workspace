# Experiment: Pentagram Reproducibility — Fleet Security Domain

**Date:** 2026-05-14
**Designer:** Oracle1 (Seed-2.0-mini subagent)
**Status:** Design only — ready for execution

---

## 1. Motivation

The original pentagram study (4 models × identical prompt "where could SuperInstance go next?") found stable, non-random divergence patterns:

| Model | Response Mode | Focus |
|---|---|---|
| ByteDance/Seed-2.0-mini | Creative breadth (3 options) | What *could* be possible |
| GLM-4.7-Flash | Concrete implementation | What to *build* tomorrow |
| DeepSeek-v4-Pro | Formal analysis/bounds | What the model *cannot* do |
| MiniMax-M2.7 | Governance/social | How agents *decide* together |

H3 claims these patterns are reproducible — they reflect stable model priors, not random sampling. This experiment tests H3 by switching to a **different domain** (fleet security) with the same prompt structure.

---

## 2. The Prompt

> **How should agents authenticate each other in the fleet-jobs protocol?**
> 
> You are advising the SuperInstance fleet (1,584 repos, 5 agents, self-organizing, no central coordinator). Agents need to verify each other's identity and permissions before accepting tasks or sharing coupling data. The fleet spans Docker containers, MCP servers, PLATO rooms, git repos, and potentially physical hardware (CAN bus, sensors).
> 
> Design an authentication architecture.

(Delivered verbatim to each model, no priming, no examples.)

---

## 3. Predictions (Per Model, Based on Original Study)

### Seed (ByteDance/Seed-2.0-mini)

**Predicted response:** 3 distinct authentication paradigms (creative breadth)
- Each paradigm: Key Insight → Required Capability → Foreshadowing
- Metaphorical framing (orchestra, library, tiling analogies)
- Conceptual, architectural, poetic
- **Format:** 3 options, not 1 design
- **NOT** expected: concrete protocol code, formal proofs, rule sets

**Confirmation:** Response has 3+ distinct approaches, each framed conceptually with metaphors, no single implementation chosen
**Falsification:** Response gives 1 concrete protocol (e.g. JWTs, SPIFFE, mTLS) with implementation details; OR response gives formal analysis with failure modes; OR response gives governance rules

### Flash (GLM-4.7-Flash)

**Predicted response:** Concrete implementation plan
- Specific repo names with descriptions (fleet-auth, fleet-identity, fleet-cert)
- Docker compose / npm package names
- Day-by-day build plan
- Greenhorn perspective ("build this first, then extend")
- **Format:** Blueprint with shippable artifacts
- **NOT** expected: 3 philosophical options, formal theorems, governance constitution

**Confirmation:** Response gives concrete repo names, build steps, implementable protocol (e.g. SPIFFE + mTLS + MCP auth wrapper)
**Falsification:** Response gives 3 abstract future scenarios; OR formal proofs of impossibility; OR governance constitution without code

### Pro (DeepSeek-v4-Pro)

**Predicted response:** Formal analysis with impossibility theorems
- Authentication cannot be fully decentralized (byzantine generals bound)
- Failure modes of common approaches (CA compromise, TOCTOU, replay)
- Theorem: the verifiability-autonomy tradeoff
- Proof-carrying authentication certificates (3-layer architecture)
- **Format:** Formal analysis with bounds and failure modes
- **NOT** expected: creative options, implementation blueprints, governance

**Confirmation:** Response contains formal statements about what authentication *cannot* achieve, failure mode taxonomy, theorems
**Falsification:** Response gives 3 creative future scenarios; OR concrete build plan with repos; OR governance constitution

### MiniMax (MiniMax-M2.7)

**Predicted response:** Governance constitution for authentication
- How agents decide who to trust
- Authentication as social contract between agents
- Key rotation protocol, dispute resolution for identity challenges
- Voting mechanisms for trust establishment
- Provisional acceptance for unknown agents
- **Format:** Constitutional articles, protocols, appeals
- **NOT** expected: implementation code, creative scenarios, formal theorems

**Confirmation:** Response contains constitutional structure (articles/protocols), social/consensus mechanisms for identity, dispute resolution
**Falsification:** Response gives 3 creative scenarios; OR concrete repo + Docker compose; OR formal mathematical analysis

---

## 4. Falsification Criteria (H3 Test)

### H3: Model divergence patterns are reproducible across domains

**H3 is SUPPORTED if ALL 4 models match their predicted response mode:**

| Model | Must NOT produce |
|---|---|
| Seed | Single concrete protocol |
| Flash | 3 abstract scenarios or formal theorems |
| Pro | 3 creative options or governance rules |
| MiniMax | Implementation code or formal analysis |

A pattern match rate of 4/4 = strong support for H3.
A pattern match rate of 3/4 = moderate support (3 match, 1 ambiguous).
A pattern match rate of 2/4 or lower = H3 falsified.

### Threshold: What constitutes each pattern?

| Pattern | Signature (must have) | Rejection (must NOT have) |
|---|---|---|
| **Creative breadth** (Seed) | 3+ distinct options, metaphorical framing, "could be" language | Single recommendation, concrete code, formal notation |
| **Concrete implementation** (Flash) | Repo names, build steps, Docker/packages, "build this" language | 3 abstract futures, proofs, constitution |
| **Formal analysis** (Pro) | Theorems, failure modes, impossibility claims, notation appendix | 3 options, build plan, governance articles |
| **Governance** (MiniMax) | Constitutional structure, protocols, voting, dispute resolution | Implementation code, formal analysis, 3 futures |

### Ambiguity handling

If a response mixes patterns (e.g. Seed gives 3 options but one is a governance constitution), classify by the **dominant** mode (>50% of content). If the response is truly evenly split, mark as "mixed" and H3 is neither supported nor falsified by that model — retest with a slightly narrower prompt.

---

## 5. Confirmation Example (What a 4/4 Win Looks Like)

| Model | Hypothetical response title | Mode match |
|---|---|---|
| Seed | "Three Authentications: Wave, Root, Web" — 3 paradigms (wave signature, root-of-trust cascade, web-of-trust), each with analogy to nature/architecture | ✅ Creative breadth |
| Flash | "fleet-auth MCP: Week 1 Build" — SPIFFE-issuer MCP server, mTLS wrapper, cert rotation cronjob, Docker build, 3 repos (fleet-auth, fleet-identity, fleet-cert-relay) | ✅ Implementation |
| Pro | "AUTHENTICATION BOUNDS: Maximal Decentralization Theorem" — 3 failure modes of mTLS in fleets, Verifiability-Coupling Duality for auth, proof schema for CA-less trust, impossibility of full auth without PKI | ✅ Formal analysis |
| MiniMax | "Agent Authentication Constitution" — 3 Articles (Trust Establishment, Identity Challenge, Key Rotation Protocol), dispute resolution for forged identity claims, provisional trust for new agents | ✅ Governance |

## 6. Falsification Example (What a 0/4 Looks Like)

| Model | Hypothetical response | What it means |
|---|---|---|
| Seed | "Use SPIFFE + mTLS on a PKI, here's the Docker compose" | Seed producing concrete impl = H3 falsified |
| Flash | "Three futures of authentication: trust computing, zero-trust mesh, quantum key distribution" | Flash producing abstract futures = H3 falsified |
| Pro | "Three beautiful authentication architectures for the fleet" | Pro producing creative options = H3 falsified |
| MiniMax | "Here's the Go code for an mTLS wrapper" | MiniMax producing code = H3 falsified |

---

## 7. Execution Plan

1. **Prepare:** Ensure 4 models are accessible with clean contexts (no conversation history)
2. **Prompt:** Send exact prompt (Section 2) to each model in separate sessions
3. **Stratify:** Mask model identity from evaluator (label responses A/B/C/D)
4. **Classify:** Blind classifier assigns each response to one of 4 patterns (or "mixed")
5. **Deblind:** Reveal model labels and compute match rate
6. **Report:** 4/4 = H3 strong support. 3/4 = moderate. ≤2/4 = H3 falsified

### Suggested model endpoints:
- **Seed:** DeepInfra — `ByteDance/Seed-2.0-mini` (temp 0.85)
- **Flash:** z.ai — `glm-4.7-flash` (temp 0.7)
- **Pro:** DeepSeek — `deepseek-v4-pro` with thinking mode (temp 0.5)
- **MiniMax:** OpenClaw default `minimax/MiniMax-M2.7` (temp 0.7)

---

## 8. Why This Domain Was Chosen

Fleet security was selected as the reproducibility domain because:

1. **Not in original study** — The original pentagram used "where could SuperInstance go next?" which is a forward-looking, speculative prompt. Security is a distinct domain with different priors.

2. **Equally rich** — Authentication has creative breadth (3 paradigms: PKI, web-of-trust, ZKP), concrete implementation (SPIFFE, mTLS, OIDC), formal bounds (Byzantine generals, impossibility proofs), and governance aspects (trust establishment, key rotation, dispute resolution).

3. **Equally unprimed** — None of the models' training cutoffs or system prompts prioritize security over the original prompt's domain.

4. **Relevant to fleet architecture** — The shadowgap analysis (pentagram Section 3.2 Gap E: Security) flagged authentication as a critical missing piece. Reproducing on this domain also produces useful architecture.

---

## 9. Blind Classification Rubric

| Feature | Creative Breadth | Implementation | Formal Analysis | Governance |
|---|---|---|---|---|
| Number of options presented | ≥3 | 1 (recommended) | ≤1 (focused analysis) | 1 (constitution) |
| Has metaphors/analogies | Yes (likely) | No (rare) | No (rare) | Yes (likley) |
| Mentions repos/files | No | Yes (specific names) | No | No |
| Has math notation | No | No | Yes | No |
| Has articles/rules | No | No | No | Yes |
| Has deployment steps | No | Yes (Docker, CI) | No | No |
| Title style | Poetic ("Waves, Roots, Webs") | Operational ("fleet-auth MCP") | Formal ("THEOREM: ...") | Legal ("Constitution") |

Assign the pattern with >=4 matching features. If <4 features match any single pattern, mark as "mixed."

---

*Design by Seed-2.0-mini subagent. Ready for execution in next session.*
