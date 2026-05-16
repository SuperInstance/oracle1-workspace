
# Arena Health Module
from fleet_math.health import coupling_entropy, algebraic_normalized

def arena_health(win_matrix):
    """win_matrix: n x n, win_matrix[i,j] = probability i beats j."""
    n = win_matrix.shape[0]
    if n < 3:
        return {"verdict": "too_few_players"}
    
    # Coupling from win rates
    C = (win_matrix + win_matrix.T) / 2
    np.fill_diagonal(C, 0.5)
    row_sums = C.sum(axis=1, keepdims=True) + 1e-10
    C = C / np.sqrt(row_sums @ row_sums.T)
    
    H = coupling_entropy(C)
    gamma = algebraic_normalized(C)
    
    return {
        "players": n,
        "strategy_diversity": H,
        "competitiveness": gamma,
        "regime": "emergent" if H > 0.618 and gamma > 0.15 else \
                 "skill_gap_too_wide" if gamma < 0.15 else \
                 "not_diverse_enough" if H < 0.618 else "balanced"
    }
