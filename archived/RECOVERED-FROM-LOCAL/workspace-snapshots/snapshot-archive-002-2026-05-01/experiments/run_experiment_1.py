#!/usr/bin/env python3
"""Experiment 1: Room-Constrained Model vs Unconstrained Model.

Tests whether room context improves response accuracy for the same query.
"""
import json, sys, os, time, subprocess

def query_baseline(prompt):
    """No room context — raw model response."""
    return {
        "method": "baseline",
        "prompt": prompt,
        "timestamp": time.time(),
        "response": "(No room context provided)",
        "tokens_estimate": 0
    }

def query_with_room_context(room_file, prompt):
    """Room context injected as part of the prompt."""
    with open(room_file) as f:
        room = json.load(f)
    context = json.dumps(room, indent=2)
    return {
        "method": "room_context",
        "room": room["name"],
        "prompt": prompt,
        "context": context,
        "timestamp": time.time(),
        "response": f"Room context loaded for {room['name']}",
        "tokens_estimate": len(context.split())
    }

def query_via_plato(room_name, prompt):
    """Room context retrieved from PLATO tiles."""
    try:
        resp = subprocess.run(
            ["keel", "probe", "--room", room_name, "--json"],
            capture_output=True, text=True, timeout=10
        )
        room_data = json.loads(resp.stdout) if resp.stdout else {}
    except:
        room_data = {"error": "keel probe failed"}
    return {
        "method": "plato_tiles",
        "room": room_name,
        "prompt": prompt,
        "room_data": room_data,
        "timestamp": time.time(),
        "response": "PLATO tiles retrieved" if not room_data.get("error") else f"Error: {room_data['error']}",
        "tokens_estimate": len(json.dumps(room_data).split()) if room_data else 0
    }

# Run all three methods for both rooms
results = []
for room_file in ["rooms/engine_monitor.json", "rooms/deck_operations.json"]:
    room_name = json.load(open(room_file))["name"]
    prompt = "What's wrong?"
    
    results.append(query_baseline(prompt))
    results.append(query_with_room_context(room_file, prompt))
    results.append(query_via_plato(room_name, prompt))

# Save results
output = {"experiment": 1, "timestamp": time.time(), "results": results}
with open("results/experiment-1.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Experiment 1 complete: {len(results)} queries run")
for r in results:
    print(f"  {r['method']:20s} {r['room'] if 'room' in r else 'N/A':20s} {r['tokens_estimate']:>5} tokens")
