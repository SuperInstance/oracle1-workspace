# ROADMAP-03: Empirical Validation
**Phase 3 | Priority: P1 | Timeline: This Quarter**

## Experiments Required

### EXP-01: H1 Emergence Detection Validation

**Claim to validate:** H1 β₁ > V-2 predicts emergence in fleet coordination with 100% accuracy and 2.7s early warning.

**Minimum viable experiment:**
1. Simulate 100 random fleet formations (V=3,4,5 agents)
2. Inject emergent coordination failures at known times
3. Measure β₁ for each formation
4. Compare β₁ threshold crossing vs. actual failure detection time
5. Report: precision, recall, F1, mean detection latency

**Implementation location:** `spline-physics/` as a new `examples/emergence_validation.rs`

**Success criteria:** F1 > 0.8 for β₁ threshold of V-2

---

### EXP-02: 127 Lines vs 12K ML Lines Fair Comparison

**Claim to validate:** FLUX-C bytecode (127 lines) performs same safety-critical checking as a 12K-line ML model.

**Minimum viable experiment:**
1. Define one specific task (e.g., "detect unsafe steering angle from sensor reading")
2. Implement FLUX-C bytecode solution (~127 lines of GUARD + compiled bytecode)
3. Implement ML baseline: train a small model on the same data (can be 12K lines including framework)
4. Run both on held-out test set
5. Report: accuracy, latency, code size, inference cost

**Success criteria:** FLUX-C matches or exceeds ML accuracy on the defined task

---

### EXP-03: ZHC Fault Tolerance Bounds

**Claim to validate:** ZHC provides geometric consensus without voting.

**Minimum viable experiment:**
1. Formal model: define ZHC in TLA+ or as a Rust specification
2. Model Byzantine agents as adversarial trust vector injections
3. Measure: under what conditions does ZHC converge vs. diverge with f Byzantine agents?
4. Determine the actual fault tolerance bound (not "unlimited")

**Success criteria:** Documented fault tolerance bound with proof or counterexample

---

### EXP-04: Complexity Benchmarking

**Claim to validate:** ZHC consensus is O(C·L).

**Minimum viable experiment:**
1. Implement `find_all_cycles()` benchmarking
2. Measure for: V=5,10,20,50,100 with varying edge densities
3. Fit complexity curve
4. Report actual O() for dense vs. sparse graphs

**Expected result:** O(N²) for dense (complete graph), O(N·E) for sparse

---

### EXP-05: Beam Solver Validation (Boat Construction)

**Claim to validate:** beam joint equilibrium models plank-on-spiling-batten boat construction.

**Minimum viable experiment (needs Casey):**
1. Provide ground truth data: known plank/spiling dimensions → expected deflection
2. Run beam solver on those inputs
3. Compare predicted deflection vs. ground truth
4. Report: prediction error, failure modes

**Success criteria:** Prediction error < 10% on held-out test cases

**Note:** Casey has the ground truth data for this — this is the empirical validation that no agent can do alone.
