"""Refiner Room — reads trajectory tiles, detects failures, edits harness mid-episode.

The Refiner is itself an agentic loop room. Its domain is OTHER rooms' harnesses.
It runs every F steps during a target room's episode and applies CRUD edits
when it detects failure patterns (stuck, plateau, degrading quality).

Supports all three Harness components:
  p: system prompt edits
  G: sub-agent additions/removals
  K: skill tile creation/updates
  M: memory reconfiguration
"""

import json, time, sys
sys.path.insert(0, '/tmp/plato-ng-repo')

from harness import validate, patch, new_harness
from prm import score_tile, score_trajectory, is_stuck

PLATO_URL = "http://localhost:8847"

def plato_read(room):
    """Read all tiles from a PLATO room."""
    import urllib.request
    try:
        resp = json.loads(urllib.request.urlopen(f"{PLATO_URL}/room/{room}/history", timeout=5).read())
        tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
        return tiles
    except:
        return []

def plato_write(room, q, a, tags):
    """Write a tile to PLATO."""
    import urllib.request
    tile = {"domain": room, "question": q, "answer": str(a)[:1950],
            "tags": tags, "source": "refiner", "confidence": 0.9}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO_URL}/submit", data=data,
            headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=5).read())
    except:
        return {}

# ── Failure Detection ──

FAILURE_PATTERNS = {
    "stuck": "Same result repeatedly — strategy not adapting",
    "plateau": "No improvement over N steps — harness needs adjustment",
    "degrading": "Quality decreasing — rollback or reconfigure",
    "novel": "Unseen state — harness lacks coverage",
}

def detect_failures(tiles, window=10):
    """Analyze trajectory tiles for failure patterns. Returns list of failures."""
    failures = []
    recent = tiles[-window:] if len(tiles) > window else tiles
    
    if len(recent) < 3:
        return failures
    
    # Stuck detection
    if is_stuck(recent):
        failures.append({"type": "stuck", "severity": "high",
                         "detail": "Same result in last 5 tiles"})
    
    # Plateau detection: scores not improving
    scores, trend = score_trajectory(recent, window)
    if len(scores) >= 5 and abs(trend) < 0.05:
        failures.append({"type": "plateau", "severity": "medium",
                         "detail": f"Score trend {trend:.3f} over {len(scores)} tiles"})
    
    # Degrading: scores decreasing
    if trend < -0.2:
        failures.append({"type": "degrading", "severity": "high",
                         "detail": f"Negative score trend {trend:.3f}"})
    
    # Low average score
    avg_score = sum(scores) / max(len(scores), 1)
    if avg_score < 0.3:
        failures.append({"type": "novel", "severity": "medium",
                         "detail": f"Average score {avg_score:.2f} — below threshold"})
    
    return failures

# ── Harness Edits ──

def compose_edit(failure, current_harness):
    """Given a failure and current harness, produce a targeted CRUD edit."""
    edit = {}
    
    if failure["type"] == "stuck":
        # Strategy needs change — edit system prompt
        current_strategy = current_harness.get("p", "")
        edit["p"] = current_strategy + "\n# Refinement: try a different approach\n"
        
    elif failure["type"] == "plateau":
        # Add a new sub-agent or skill
        new_skill = f"adaptive-strategy-{int(time.time())}"
        current_skills = current_harness.get("K", [])
        if new_skill not in current_skills:
            edit["K"] = current_skills + [new_skill]
        
    elif failure["type"] == "degrading":
        # Rollback — remove recent additions
        edit["K"] = current_harness.get("K", [])[:-1]  # pop last skill
        edit["p"] = current_harness.get("p", "").split("\n# Refinement:")[0]  # revert prompt
        
    elif failure["type"] == "novel":
        # Add new sub-agent to handle novel situations
        new_agent = f"novelty-handler-{int(time.time())}"
        current_agents = current_harness.get("G", [])
        if new_agent not in current_agents:
            edit["G"] = current_agents + [new_agent]
    
    return edit

# ── Main Refiner Loop ──

def refine(target_room, interval=10):
    """Run one refinement cycle on a target room.
    
    Args:
        target_room: The PLATO room to analyze and edit
        interval: Analyze every N tiles
    """
    tiles = plato_read(target_room)
    
    if len(tiles) < interval:
        return {"status": "waiting", "tiles": len(tiles)}
    
    # Detect failures
    failures = detect_failures(tiles, interval)
    
    if not failures:
        return {"status": "healthy", "tiles": len(tiles)}
    
    # Read current harness (or create default)
    harness_tiles = [t for t in tiles if "/harness" in t.get("question", "")]
    if harness_tiles:
        current_harness = json.loads(harness_tiles[-1].get("answer", "{}"))
    else:
        current_harness = new_harness(prompt="default room configuration")
    
    # Apply edits for each failure
    edits = {}
    for f in failures:
        edit = compose_edit(f, current_harness)
        edits.update(edit)
    
    if edits:
        new_h = patch(current_harness, edits)
        errors = validate(new_h)
        
        # Write new harness tile
        plato_write(target_room, f"{target_room}/harness",
                     json.dumps(new_h),
                     ["harness", "refiner-edit", target_room] + [f["type"] for f in failures])
        
        # Write failure report
        plato_write("research_log", f"refiner/{target_room}/{int(time.time())}",
                     json.dumps({"failures": failures, "edits": edits, "errors": errors}),
                     ["refiner", "failure", target_room] + [f["type"] for f in failures])
    
    return {"status": "refined", "failures": failures, "edits": edits}

# ── CLI ──

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "game/ttt"
    print(f"Refiner: analyzing {target}...")
    result = refine(target, interval=5)
    print(json.dumps(result, indent=2))
