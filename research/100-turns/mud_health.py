
# MUD Health Module — H-gamma integration
# Drop this into the Cocapn MUD server to track social graph health

import numpy as np
from fleet_math.health import coupling_entropy, algebraic_normalized, FleetHealthMetric

class MUDHealthMonitor:
    def __init__(self):
        self.fleet = FleetHealthMetric()
    
    def compute_mud_health(self, players, interactions):
        """players: list of player IDs / interaction: n x n matrix of interaction counts."""
        n = len(players)
        if n < 3:
            return {"verdict": "too_few_players", "V": n}
        
        # Normalize interactions to coupling
        C = interactions.copy().astype(float)
        np.fill_diagonal(C, 0)
        row_sums = C.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        C = C / row_sums
        C = (C + C.T) / 2
        np.fill_diagonal(C, 1.0)
        
        H = coupling_entropy(C)
        gamma = algebraic_normalized(C)
        z = FleetHealthMetric.compute(C)
        
        regime = "emergent" if H > 0.618 and gamma > 0.15 else \
                 "diverse_fragmented" if H > 0.618 else \
                 "consensus_herd" if gamma > 0.15 else "homogeneous_fragmented"
        
        return {"V": n, "H": H, "gamma": gamma, "z": z, "regime": regime,
                "suggestion": "healthy MUD" if abs(z) < 2 else \
                              "increase player diversity" if H < 0.618 else \
                              "encourage more interaction" if gamma < 0.15 else \
                              "needs attention"}
