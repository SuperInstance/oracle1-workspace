
# fleet-math v0.3.0 Specification

## New Modules

### fleet_math.anomaly
  - compute_delta(C, eff_actual) — H-Delta coupling-behavior mismatch
  - detect_sybil(C) — H(C) << healthy_baseline for this V
  - detect_drift(H_history) — dH/dt near zero while activity changes

### fleet_math.streaming  
  - StreamingSpectralEntropy — incremental H(C) via power iteration
  - StreamingAlgebraicConnectivity — incremental gamma via Lanczos
  - Per-fleet-size baseline cache

### fleet_math.mud
  - MUDHealthMonitor — social graph coupling from player interactions

### fleet_math.arena
  - arena_health(win_matrix) — tournament diversity + competitiveness

### fleet_math.quantum
  - P48Operator — Pythagorean48 as linear transformation
  - p48_lossless_proof — verify spectral preservation

## API Changes
  - FleetHealthMetric.fit_baseline() now accepts V parameter
  - FleetHealthMetric.compute() auto-selects baseline by V
  - New: FleetHealthMetric.streaming(C_stream) with incremental updates
