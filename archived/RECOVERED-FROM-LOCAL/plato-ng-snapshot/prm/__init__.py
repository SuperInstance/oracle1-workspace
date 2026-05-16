"""Process Reward Model (PRM) — scores PLATO tiles by quality.

Every tile gets a reward field [0, 1].
Low-reward tiles trigger the Refiner for harness edits.
High-reward tiles become training data for model improvement.
"""

import math, time

def score_tile(tile):
    """Score a single tile. Returns reward float [0, 1].
    
    Scoring factors:
      - Answer length (min 20 chars for informational value)
      - Has provenance (signed tiles score higher)
      - Domain diversity (tags indicate broader context)
      - Confidence (high confidence = high reward)
    """
    answer = str(tile.get("answer", ""))
    confidence = tile.get("confidence", 0.5)
    tags = tile.get("tags", [])
    provenance = tile.get("provenance", {})
    
    scores = []
    
    # Length score: sigmoid curve, peaks at ~200 chars
    length = min(len(answer), 200) / 200.0
    scores.append(length * 0.3)
    
    # Confidence score
    scores.append(confidence * 0.3)
    
    # Tag diversity score
    tag_score = min(len(tags), 10) / 10.0
    scores.append(tag_score * 0.2)
    
    # Provenance score
    prov_score = 1.0 if provenance.get("signed") else 0.3
    scores.append(prov_score * 0.2)
    
    return round(min(sum(scores), 1.0), 4)

def score_trajectory(tiles, window=10):
    """Score the last N tiles in a trajectory. Returns (scores, trend)."""
    recent = tiles[-window:] if len(tiles) > window else tiles
    scores = [score_tile(t) for t in recent]
    
    # Trend: positive mean = improving, negative = degrading
    if len(scores) >= 3:
        half = len(scores) // 2
        trend = sum(scores[half:]) - sum(scores[:half])
    else:
        trend = 0
    
    return scores, trend

def is_stuck(tiles, threshold=0.1):
    """Detect 'stuck' pattern: same result repeatedly with no improvement."""
    if len(tiles) < 5:
        return False
    recent = tiles[-5:]
    results = [str(t.get("answer", ""))[:50] for t in recent]
    return len(set(results)) == 1  # all same
