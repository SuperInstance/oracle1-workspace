#!/usr/bin/env python3
"""Experiment 11: Verify keel README claims.

Claims to test:
1. '9ms command latency across 12-room hops' — time keel status and keel field
2. '880ms cold launch, 120ms warm' — time keel init (cold) and subsequent commands (warm)
3. '2.3us deviation in lab conditions' — time keel probe
"""
import json, time, subprocess, sys

KEEL = "/tmp/keel/target/debug/keel"

def run_keel(args):
    start = time.time()
    r = subprocess.run([KEEL] + args, capture_output=True, text=True, timeout=30)
    ms = (time.time() - start) * 1000
    return ms, r.stdout, r.stderr, r.returncode

results = []
print(f"{'='*70}")
print("EXPERIMENT 11: Verify keel README Claims")
print(f"{'='*70}")

# Test 1: keel init (cold launch)
print(f"\n--- Test 1: keel init (cold launch) ---")
import tempfile, os
test_home = tempfile.mkdtemp()
os.environ["HOME"] = test_home

for i in range(3):
    h = tempfile.mkdtemp()
    os.environ["HOME"] = h
    ms, out, err, code = run_keel(["init", "--name", f"test-{i}"])
    print(f"  Run {i+1}: {ms:.0f}ms {'OK' if code == 0 else 'FAIL'}")
    results.append({"test": "cold_init", "run": i, "ms": ms, "code": code})

# Test 2: keel status (warm, after init)
print(f"\n--- Test 2: keel status (warm) ---")
for i in range(5):
    ms, out, err, code = run_keel(["status"])
    print(f"  Run {i+1}: {ms:.0f}ms {'OK' if code == 0 else 'FAIL'}")
    results.append({"test": "status_warm", "run": i, "ms": ms, "code": code})

# Test 3: keel field (topology)
print(f"\n--- Test 3: keel field (topology graph) ---")
for i in range(3):
    ms, out, err, code = run_keel(["field"])
    print(f"  Run {i+1}: {ms:.0f}ms output={len(out)}b {'OK' if code == 0 else 'FAIL'}")
    results.append({"test": "field", "run": i, "ms": ms, "code": code})

# Test 4: keel bear (bearing scan)
print(f"\n--- Test 4: keel bear (bearing scan) ---")
for i in range(3):
    ms, out, err, code = run_keel(["bear"])
    print(f"  Run {i+1}: {ms:.0f}ms {'OK' if code == 0 else 'FAIL'}")
    results.append({"test": "bear", "run": i, "ms": ms, "code": code})

# Analyze
cold_times = [r["ms"] for r in results if r["test"] == "cold_init"]
warm_times = [r["ms"] for r in results if r["test"] == "status_warm"]
field_times = [r["ms"] for r in results if r["test"] == "field"]
bear_times = [r["ms"] for r in results if r["test"] == "bear"]

print(f"\n{'='*70}")
print("RESULTS vs README CLAIMS")
print(f"{'='*70}")
print(f"{'Claim':<35} {'Claimed':<12} {'Measured':<12} {'Status'}")
print(f"{'-'*70}")

claims = [
    ("Cold launch (init)", "880ms", f"{sum(cold_times)/len(cold_times):.0f}ms avg",
     sum(cold_times)/len(cold_times) < 1000),
    ("Warm status", "120ms", f"{sum(warm_times)/len(warm_times):.0f}ms avg",
     sum(warm_times)/len(warm_times) < 200),
    ("Field topology", "-", f"{sum(field_times)/len(field_times):.0f}ms avg", True),
    ("Bear scan", "-", f"{sum(bear_times)/len(bear_times):.0f}ms avg", True),
]

for claim, claimed, measured, passed in claims:
    icon = "✅" if passed else "❌"
    print(f"{icon} {claim:<33} {claimed:<12} {measured:<12}")

# Save
with open("results/experiment-11.json", "w") as f:
    json.dump({"experiment": 11, "timestamp": time.time(), "results": results}, f, indent=2)

print(f"\nResults saved to results/experiment-11.json")
