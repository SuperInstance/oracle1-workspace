#!/usr/bin/env python3
"""Debrief: analyze experiment results and generate next research questions."""
import json, sys, os
from datetime import datetime

def debrief(result_file):
    with open(result_file) as f:
        data = json.load(f)
    
    exp = data["experiment"]
    results = data["results"]
    
    print(f"\n{'='*60}")
    print(f"DEBRIEF: Experiment {exp}")
    print(f"{'='*60}")
    print(f"Timestamp: {datetime.fromtimestamp(data['timestamp']).isoformat()}")
    print(f"Methods tested: {len(results)}")
    
    for r in results:
        status = "✅" if "error" not in r.get("response","") else "❌"
        print(f"\n  {status} {r['method']:20s}", end="")
        if "room" in r:
            print(f" in {r['room']}", end="")
        print(f"\n    Tokens: {r['tokens_estimate']}")
        print(f"    Response: {r['response'][:80]}")
    
    print(f"\n  --- Research Questions for Experiment 2 ---")
    print(f"  1. Does denser room structure (20+ tiles) flip the advantage?")
    print(f"  2. Does PLATO round-trip latency dominate over context quality?")
    print(f"  3. Can we pre-cache room context to eliminate round-trips?")
    
    # Save questions for next experiment
    questions = {
        "experiment": exp + 1,
        "generated_from": f"Experiment {exp}",
        "questions": [
            "Does denser room structure (20+ tiles) flip the advantage from RAG to PLATO?",
            "Does PLATO round-trip latency dominate over context quality?",
            "Can we pre-cache room context to eliminate round-trips?",
            "What is the minimum room density for PLATO to outperform RAG?"
        ]
    }
    next_file = f"questions/experiment-{exp+1}.json"
    with open(next_file, "w") as f:
        json.dump(questions, f, indent=2)
    print(f"\n  Questions saved to {next_file}")
    
    return questions

if __name__ == "__main__":
    result_file = sys.argv[1] if len(sys.argv) > 1 else "results/experiment-1.json"
    debrief(result_file)
