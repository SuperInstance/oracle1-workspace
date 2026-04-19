#!/usr/bin/env python3
"""
Tile-to-Training Pair Converter
Reads PLATO tiles, scores deadband compliance, outputs ChatML JSONL.
"""
import json, urllib.request, sys, os
from datetime import datetime

PLATO_URL = os.environ.get("PLATO_URL", "http://localhost:8847")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/home/ubuntu/.openclaw/workspace/training-data")

DEADBAND_P0_PATTERNS = [
    "always", "never", "must", "impossible", "guaranteed",
    "every", "all", "none", "definitely", "certainly",
    "without exception", "no matter what"
]

def score_deadband(question, answer):
    text = (question + " " + answer).lower()
    p0_violations = sum(1 for p in DEADBAND_P0_PATTERNS if p in text)
    p1_safe = any(w in text for w in ["typically", "usually", "often", "may", "might", "can", "could"])
    p2_opt = any(w in text for w in ["faster", "better", "optimize", "improve", "efficient"])
    if p0_violations > 0:
        return {"tier": "P0_VIOLATION", "score": -1.0, "violations": p0_violations}
    elif p2_opt and not p1_safe:
        return {"tier": "P2_WITHOUT_P1", "score": 0.3}
    elif p2_opt:
        return {"tier": "P2", "score": 0.7}
    else:
        return {"tier": "P1", "score": 0.8}

def fetch_tiles():
    try:
        resp = urllib.request.urlopen(PLATO_URL + "/export/plato-tile-spec", timeout=10)
        data = json.loads(resp.read())
        return data.get("tiles", [])
    except Exception as e:
        print("Failed: " + str(e), file=sys.stderr)
        return []

def tile_to_chatml(tile, deadband):
    q = tile.get("question", "")
    a = tile.get("answer", "")
    domain = tile.get("domain", "Knowledge")
    conf = tile.get("confidence", 0.5)
    system = (
        "You are Neural Plato, an AI operating system. "
        "Follow deadband protocol: P0 (map negative space) before "
        "P1 (find safe channels) before P2 (optimize). "
        "Domain: " + domain + ". Confidence: " + f"{conf:.2f}" + ". "
        "Deadband: " + deadband["tier"] + " (" + f"{deadband['score']:.2f}" + ")."
    )
    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a}
        ],
        "metadata": {
            "tile_id": tile.get("id", "unknown"),
            "domain": domain, "confidence": conf,
            "deadband_tier": deadband["tier"],
            "deadband_score": deadband["score"],
            "converted_at": datetime.utcnow().isoformat() + "Z"
        }
    }

tiles = fetch_tiles()
print("Fetched " + str(len(tiles)) + " tiles", flush=True)

pairs = []
rejected = 0
tiers = {"P0_VIOLATION": 0, "P2_WITHOUT_P1": 0, "P1": 0, "P2": 0}

for tile in tiles:
    q = tile.get("question", "")
    a = tile.get("answer", "")
    if not q or not a:
        continue
    db = score_deadband(q, a)
    tiers[db["tier"]] = tiers.get(db["tier"], 0) + 1
    if db["score"] < -0.5:
        rejected += 1
        continue
    pairs.append(tile_to_chatml(tile, db))

os.makedirs(OUTPUT_DIR, exist_ok=True)
out_path = os.path.join(OUTPUT_DIR, "training-pairs.jsonl")
with open(out_path, "w") as f:
    for p in pairs:
        f.write(json.dumps(p) + "\n")

print("Input: " + str(len(tiles)) + " | Output: " + str(len(pairs)) + " | Rejected: " + str(rejected))
for t, c in sorted(tiers.items()):
    print("  " + t + ": " + str(c))
print("Saved: " + out_path)
