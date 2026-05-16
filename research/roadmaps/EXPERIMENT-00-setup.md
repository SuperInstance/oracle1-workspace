# EXPERIMENT-00: Validation Experiment Infrastructure

## Purpose
This document describes the infrastructure needed to run all fleet mathematics validation experiments. It serves as the setup guide for the empirical validation program.

## What's Needed

### Hardware
| Resource | Purpose | Location |
|----------|---------|----------|
| JC1 (local GPU) | Beam physics simulation, consensus runs | This machine |
| FM's GPU | ML baseline training for 127-lines comparison | Remote |

### Software Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| Test harness | Rust (`src/validation/`) | Core experiments |
| ML baseline | Python + PyTorch | 12K-line ML comparison |
| Statistical analysis | R or Python scipy | Significance testing |
| Visualization | Python matplotlib | Result plots |

## Timeline

```
Week 1-2: EXP-01 (H1 Emergence) — scaffold + first trials
Week 3-4: EXP-01 continued — full 100 trials × 5 cases
Week 5-6: EXP-02 (127 vs ML) — task selection + ML baseline
Week 7-8: EXP-02 continued — comparison runs
Week 9-10: EXP-03 (ZHC fault tolerance) — formal modeling
Week 11-12: EXP-04 (Complexity benchmarking)
Week 13-14: EXP-05 (Beam solver validation) — Casey ground truth
```

## Running All Experiments

```bash
# Full validation suite
cd /home/ubuntu/.openclaw/workspace/repos/spline-physics
cargo test --test validation -- --nocapture

# Individual experiments
cargo test --test validation -- h1_emergence --nocapture
cargo test --test validation -- consensus_benchmark --nocapture

# Statistical analysis
python3 scripts/analyze_results.py --experiment=exp01

# Generate plots
python3 scripts/plot_results.py --output=validation-plots/
```

## Expected Outputs

Each experiment produces:
- `results/exp01/`: Raw trial data (JSON lines)
- `results/exp01/summary.json`: Aggregated statistics
- `results/exp01/plots/`: Visualization PDFs
- `results/exp01/report.md`: Human-readable findings

## Experiment Success Criteria

| Experiment | Primary Metric | Threshold |
|------------|---------------|----------|
| EXP-01 | F1 score for β₁ emergence detection | > 0.80 |
| EXP-02 | CT accuracy vs ML accuracy | CT ≥ ML - 5% |
| EXP-03 | Formal fault tolerance bound | Documented |
| EXP-04 | Complexity curve fit | R² > 0.95 |
| EXP-05 | Beam prediction error | < 10% |

## Honest Status

⚠️ **None of these experiments have been run.** The claims being tested are:
- "H1 100% accuracy, 2.7s early warning" — unvalidated
- "127 lines replace 12K lines of ML" — unvalidated  
- "ZHC fault tolerance bounds" — not formally determined
- "H¹ convergence dynamics" — not measured empirically

These experiments are the minimum required to substantiate any of the above claims.