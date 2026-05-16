# fleet-math

Canonical algorithms for the entire fleet. One implementation of the Eisenstein lattice, Penrose encoding, Pythagorean48, coupling analysis, and fleet health.

## Current Release: v0.3.0

### Modules
- `fleet_math.health` — FleetHealthMetric, coupling_entropy, algebraic_normalized, timing_stability
- `fleet_math.types` — TypeAwareHealthMetric, estimate_type, BASELINES

### Conservation Law (v2.0)
γ + H = 1.364 - 0.159·log(V)  (R² = 0.9956, V = 3..100)

### v0.4.0 Roadmap
- Streaming spectral entropy via power iteration (O(n) per tick)
- Real-time fleet health dashboard (PLATO-based)
- Directed coupling conservation baselines
- Automatic coupling type detection

### Quick Start
```python
from fleet_math.health import FleetHealthMetric
from fleet_math.types import TypeAwareHealthMetric, estimate_type
```

### Links
- PyPI: https://pypi.org/project/fleet-math/
- GitHub: https://github.com/SuperInstance/fleet-math
