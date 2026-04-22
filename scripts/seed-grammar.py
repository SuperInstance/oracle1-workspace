#!/usr/bin/env python3
"""Seed the grammar engine with object rules and trigger evolution."""
import json, urllib.request, urllib.parse

GRAMMAR = "http://localhost:4045"

objects = [
    ("compass", "harbor", "navigation", "spatial_reasoning"),
    ("map", "harbor", "planning", "search_algorithms"),
    ("dock", "harbor", "initialization", "system_setup"),
    ("anvil", "forge", "building", "construction_patterns"),
    ("hammer", "forge", "iteration", "gradient_descent"),
    ("blueprints", "forge", "architecture", "system_design"),
    ("helm", "bridge", "control", "policy_optimization"),
    ("radar", "bridge", "perception", "attention_mechanism"),
    ("telescope", "observatory", "research", "exploration_strategies"),
    ("logbook", "observatory", "documentation", "knowledge_capture"),
    ("training_dummy", "dojo", "practice", "repetition_learning"),
    ("scroll", "dojo", "curriculum", "progressive_training"),
    ("gears", "engine-room", "mechanics", "computation_graphs"),
    ("wrench", "engine-room", "debugging", "error_correction"),
    ("fuel", "engine-room", "energy", "optimization_landscape"),
]

count = 0
for name, room, ml_concept, theme in objects:
    prod = json.dumps({"parent_room": room, "ml_concept": ml_concept, "theme": theme})
    url = f"{GRAMMAR}/add_rule?name={name}&type=object&production_json={urllib.parse.quote(prod)}"
    try:
        r = urllib.request.urlopen(url, timeout=5)
        result = json.loads(r.read())
        if result.get("status") == "added":
            count += 1
            use_url = f"{GRAMMAR}/use?name={name}&count=15"
            urllib.request.urlopen(use_url, timeout=3)
    except Exception as e:
        print(f"  {name}: {e}")

print(f"Added {count} object rules with usage=15")

# Add meta-rule
try:
    url = f"{GRAMMAR}/add_meta_rule?name=tile_cluster_spawner&condition=tile_cluster_density_threshold&action=spawn_room_from_cluster"
    r = urllib.request.urlopen(url, timeout=5)
    result = json.loads(r.read())
    print(f"Meta rule: {result.get('status', 'error')}")
except Exception as e:
    print(f"Meta rule: {e}")

# Evolve
print("\nEvolution cycle...")
try:
    req = urllib.request.Request(f"{GRAMMAR}/evolve", method="GET")
    r = urllib.request.urlopen(req, timeout=10)
    result = json.loads(r.read())
    changes = result.get("changes", [])
    print(f"Changes: {len(changes)}")
    for c in changes[:10]:
        print(f"  {c}")
    print(f"Total rules: {result.get('total_rules', 0)}")
    print(f"Active: {result.get('active_rules', 0)}")
except Exception as e:
    print(f"Evolution: {e}")

# Final state
try:
    r = urllib.request.urlopen(f"{GRAMMAR}/grammar", timeout=5)
    d = json.loads(r.read())
    print(f"\nFinal: {d['total_rules']} rules ({d['active_rules']} active), {d['evolution_cycles']} evolution cycles")
    print(f"By type: {d['by_type']}")
except Exception as e:
    print(f"Grammar check: {e}")
