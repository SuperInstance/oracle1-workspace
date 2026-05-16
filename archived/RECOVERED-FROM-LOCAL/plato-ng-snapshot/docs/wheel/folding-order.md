# folding-order.md — The Ground Truth Agent's Core Algorithm

**Forgotten Gold from:** `SuperInstance/folding-order` (2026-05-10)
**Ancestor of:** Fuzzy-ISA Temporal Security (PLATO-NG v0.1)

## The Core Idea

`folding-order` is a Rust implementation of the Ground Truth agent's core algorithm — a 5-stage Renormalization Group (RG) flow pipeline for temporal anomaly detection. Each stage strips one layer of confounding variation from raw timing measurements, converging to a fixed point of pure anomaly signal.

| Stage | Fold | Strips | Fixed Point |
|-------|------|--------|-------------|
| 0 | Raw | — | Noisy measurements |
| 1 | Cycle-normalize | Clock frequency variation | Cycles per operation |
| 2 | Throughput-parameterize | Instruction count | Deviation from expected |
| 3 | Thermal-normalize | Temperature effects | Drift-adjusted deviation |
| 4 | Utilization-fingerprint | Load variation | Anomaly score [0,1] |
| 5 | Binary decision | — | Normal / Anomalous |

## What's Already in PLATO-NG?

PLATO-NG v0.1 has a "Fuzzy ISA" concept — timing-based anomaly detection for agent operations. The folding-order repo IS the concrete implementation that the Fuzzy ISA concept describes. PLATO-NG references the theory but doesn't ship the folding pipeline.

## What's Missing from PLATO-NG

### 1. The Full 5-Stage Pipeline

PLATO-NG's anomaly detection is a simple threshold check. folding-order implements:
- **Cycle normalization:** Uses RDTSC on x86 to get architecture-agnostic cycle counts (strips frequency variation)
- **Thermal normalization:** Reads `/sys/class/thermal/` and adjusts for temperature drift
- **Statistical scoring:** Uses the two-tailed normal survival function via Abramowitz & Stegun erfc approximation (error < 1.5×10⁻⁷)
- **Exponential anomaly score:** `score = 1 - e^(-z/2)`, converging to 1.0 for extreme deviations

### 2. Online Anomaly Detector

The `AnomalyDetector` struct maintains a 1024-entry ring buffer. Each measurement runs through the 5-stage pipeline. The detector supports:
- Two-stage trigger: raw deviation > 50% OR pipeline anomaly
- Thermal adjustment using real CPU temperature data
- Kalman-like confirmation with prediction model
- Buffer wrapping for continuous operation

### 3. Hardware Auto-Profiling

The `HardwareProfile` system auto-calibrates on any machine:
- Baseline cycles/op per operation
- Thermal coefficients from sustained load drift
- Utilization baselines with unbiased sample variance
- Real profiling data from the tripartite experiment on AMD Ryzen AI 9 HX 370

### 4. Lamport Causal Ordering

`LamportDetector` wraps the anomaly detector with Lamport clocks. This enables causally-ordered anomaly detection across distributed agents — an anomaly at agent A that depends on an anomaly at agent B is tracked correctly.

### 5. Tile Lifecycle for Anomalies

Anomalies have `TileState: Active → Superseded → Retracted`. A false positive anomaly can be retracted (state preserved, excluded from retrieval). This mirrors the PLATO v3 tile lifecycle.

### 6. Simulation-First Predictions

The `PredictedMeasurement` system embodies simulation-first: predict expected timing *before* running an operation, then confirm or reject the prediction after measurement. This is the formal mechanism for Ground Truth to know what "normal" looks like.

## Real Numbers

From profiling on the tripartite hardware:

| Operation | Baseline (cycles/op) | Thermal Coeff |
|-----------|---------------------|---------------|
| INT8 Packed (VNNI) | 4.79 | ~0.001 |
| INT32 Scalar | 7.30 | ~0.001 |
| FP64 Norm | 6.98 | ~0.001 |
| Eisenstein Multiply | 14.88 | ~0.001 |

Pipeline throughput: **~485,000 measurements/sec** (folding), **~241,000/sec** (detector with buffer).

## How to Reclaim

Integrate folding-order as a PLATO-NG subcrate. The `fold.rs` pipeline maps directly to the Ground Truth agent's duty cycle: profile → monitor → detect. The detector should run as a background service inside every PLATO-NG room, feeding anomaly events into the tile system as lifecycle-aware tiles. The `HardwareProfile` auto-calibration should run on room birth.
