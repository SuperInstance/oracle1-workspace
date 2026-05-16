#!/usr/bin/env python3
"""PLATO-NG: harness standard, PRM scoring, Refiner Room — all in one launcher."""
import sys, json, time, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from harness import new_harness, validate, patch
from prm import score_tile, score_trajectory, is_stuck
from refiner import refine

def status():
    print("PLATO-NG Modules")
    print("=" * 40)
    print("  harness/   — (p,G,K,M) standard")
    print("  prm/       — Process Reward Model scoring")
    print("  refiner/   — trajectory analysis + harness edits")
    print()
    print("Test harness:")
    h = new_harness(prompt="test agent", sub_agents=["bot"], skills=["skill1"])
    print(f"  validate: {validate(h)}")
    print()
    print("Test PRM:")
    tiles = [{"answer": "test", "confidence": 0.9, "tags": ["t"], "provenance": {"signed": True}}]
    print(f"  scores: {score_trajectory(tiles, 5)}")
    print()
    print("Test refiner (readymade):")
    print("  python3 -c 'from refiner import refine; import json; print(json.dumps(refine(\"research_log\", interval=10), indent=2))'")

if __name__ == "__main__":
    status()
