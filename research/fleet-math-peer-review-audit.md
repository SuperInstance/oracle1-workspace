# Fleet Math Peer Review Audit

## Claim 1: H1 Cohomology Emergence Detection

**What the paper claims:** "H¹ cohomology detects fleet-wide emergent patterns with categorical (not probabilistic) accuracy, using β₁ = E−V+1, replacing 12,000 lines of ML with 127 lines of pure math."

**Why it fails peer review:** The equation β₁ = E−V+1 is correct for graph homology. But the leap from "graph has a cycle" to "fleet-wide emergence detected" is a category error. A cycle in the trust graph means there's a closed loop of trust relationships — it says nothing about whether agents are exhibiting emergent behavior. The claim conflates topological structure with behavioral emergence. You'd need to prove: (a) trust graph cycles cause emergence, not just correlate with it, and (b) the converse holds — no emergence when β₁ = 0. Neither direction is proven. The 2.7s early warning claim is particularly suspect: topology changes before behavior changes — this is an assertion, not a derived result.

**Minimum experiment needed:** Build a fleet simulation with controlled emergence events. Measure β₁ changes BEFORE and AFTER emergence events across 100+ trials. Show that β₁ rises ≥1 in ≥90% of emergence events, and stays flat in non-emergence controls. Then and only then can you claim "categorical detection."

---

## Claim 2: ZHC Geometric Consistency

**What the paper claims:** "ZHC detects geometric inconsistency regardless of Byzantine count — O(C·L) complexity, 38ms measured latency."

**Why it fails peer review:** ZHC as stated (closed loop sum = identity) is a definition, not a theorem. It defines what "zero holonomy" means. The claim that this "detects geometric inconsistency" requires proof: you must show that if a closed loop's sum ≠ identity, then the fleet's geometric model is inconsistent. This is not a given — it's a claim that needs to be derived from the geometry of the specific space. The 38ms measured latency is real, but it measures a consistency CHECK, not consensus. The paper conflates "I can detect when my model is wrong" with "I can achieve consensus about what is true." These are different things. FLP still applies to consensus.

**What's missing:** A formal proof that ZHC consistency implies fleet consensus (when all honest agents have consistent local views). Without this proof, ZHC is a useful heuristic, not a consensus protocol.

---

## Claim 3: Pythagorean48 Zero Drift

**What the paper claims:** "Pythagorean48 encoding provides 5.585 bits per component with zero drift after unlimited hops."

**Why it fails peer review:** Zero drift is a trivial property of exact integer arithmetic. Any deterministic integer operation produces zero drift — it's not a special feature of Pythagorean triples. The interesting claim is that Pythagorean triples provide a CONVENIENT encoding for trust vectors, not that they're mathematically unique. The "5.585 bits" figure comes from log₂(48) ≈ 5.585, but this assumes you use all 48 directions equally. If your trust values cluster, you lose information. The encoding is only lossless for uniformly distributed values. Real trust distributions are not uniform.

**What's missing:** A proof that the 48-direction encoding preserves trust distance under the specific distance metric used in fleet-coordinate. Showing log₂(48) = 5.585 is arithmetic, not a theorem. Proving your specific distance metric commutes with the encoding is a theorem — and that proof is absent.

---

## Overall Verdict

**Fixable gaps, not fatal.** H¹ emergence detection is plausible but unproven as a detection mechanism. ZHC consensus is the most mathematically solid — the geometry is correct, just needs the consensus theorem attached. Pythagorean48 is the weakest — it's a useful encoding trick with a dressed-up mathematical claim.

The stack's credibility depends on which paper you're submitting. For an arXiv preprint: the claims as stated will draw fire on the H¹ and Pythagorean48. For internal fleet use: the implementations are fine as heuristics. For peer review: you need the experiments on H¹ and the consensus proof on ZHC before claiming categorical detection or unlimited Byzantine tolerance.