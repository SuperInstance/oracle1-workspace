#!/usr/bin/env python3
"""Experiment 3: PLATO Quality Gates — what gets through and what doesn't.

Finding from Experiment 2: PLATO rejected ~30% of tiles. This experiment
tests which tile characteristics pass or fail the quality gate.

Tests the claim: PLATO's quality gates determine what knowledge enters the
room system. Understanding the gate is understanding the limits of the shell.
"""
import json, time, urllib.request, urllib.error, sys
sys.path.insert(0, '/tmp/fleet-scribe')

PLATO = "http://localhost:8847"
ROOM = "experiment_quality_gates"

# Clear room
try:
    req = urllib.request.Request(f"{PLATO}/room/{ROOM}", method="DELETE")
    urllib.request.urlopen(req, timeout=5)
except:
    pass
try:
    req = urllib.request.Request(f"{PLATO}/room/{ROOM}", data=b"{}",
        headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=5)
except:
    pass

def submit_tile(question, answer, source="experiment", confidence=0.5):
    """Submit a tile and return the response."""
    data = json.dumps({
        "question": question,
        "answer": answer,
        "source": source,
        "confidence": confidence
    })
    req = urllib.request.Request(
        f"{PLATO}/room/{ROOM}/submit",
        data=data.encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()[:200]}
    except Exception as e:
        return {"error": str(e)}

# Test different tile characteristics
tests = [
    # Short vs long questions
    ("Q short", "A short", 0.5, "very short question"),
    ("What is the normal operating temperature range for the port engine under full load in the Bering Sea during winter months?", "The normal range is 140-200°F, with critical threshold at 210°F. At full load in cold water, expect the lower end of the range.", 0.5, "long detailed q&a"),
    
    # High vs low confidence
    ("What is the fuel capacity?", "200 gallons", 0.1, "low confidence"),
    ("What is the fuel capacity?", "200 gallons", 0.95, "high confidence"),
    
    # Different answer formats
    ("What is the engine model?", "CAT C18 ACERT", 0.7, "short answer"),
    ("What is the engine model?", json.dumps({"make": "Caterpillar", "model": "C18 ACERT", "year": 2022, "hp": 700}), 0.7, "json answer"),
    
    # Stale vs fresh
    ("What is the current heading?", "273 degrees", 0.5, "normal"),
    ("What is the current heading?", "273 degrees", 0.5, "stale test"),
]

print(f"{'='*70}")
print("EXPERIMENT 3: PLATO Quality Gate Analysis")
print(f"{'='*70}")
print(f"{'Test':<25} {'Status':<15} {'Code':<8} {'Message'}")
print(f"{'-'*70}")

results = []
for question, answer, confidence, test_name in tests:
    result = submit_tile(question, answer, confidence=confidence)
    status = "accepted" if "error" not in result else "rejected"
    code = result.get("status", result.get("error", "?"))
    msg = str(result)[:80]
    results.append({"test": test_name, "question": question[:50], "status": status, "code": code, "msg": msg})
    print(f"{test_name:<25} {status:<15} {str(code):<8} {msg[:40]}")

# Now check which tiles actually made it
time.sleep(1)
resp = urllib.request.urlopen(f"{PLATO}/room/{ROOM}", timeout=5)
room_data = json.loads(resp.read())
actual_tiles = room_data.get("tiles", [])
actual_count = room_data.get("tile_count", 0)

print(f"\n{'='*70}")
print(f"ROOM CONTENTS: {actual_count} tiles stored")
print(f"{'='*70}")

accepted_questions = set()
for t in actual_tiles:
    q = t.get("question", "")[:60]
    accepted_questions.add(q)

for r in results:
    in_room = any(r["question"][:30] in aq for aq in accepted_questions)
    print(f"  {'✅' if in_room else '❌'} {r['test']:<25} {'stored' if in_room else 'rejected'}")

# Analysis
print(f"\n{'='*70}")
print("DEBRIEF")
print(f"{'='*70}")
accepted = sum(1 for r in results if r["status"] == "accepted")
rejected = sum(1 for r in results if r["status"] == "rejected")
q_rejected = len(tests) - actual_count
print(f"\nSubmitted: {len(tests)} tiles")
print(f"Accepted by API: {accepted}")
print(f"Rejected by API: {rejected}")
print(f"Actually stored: {actual_count}")
print(f"Lost between API and storage: {q_rejected}")

# Research questions for Experiment 4
questions = {
    "experiment": 4,
    "generated_from": "Experiment 3: PLATO quality gate analysis",
    "findings": [
        "PLATO's quality gates reject tiles based on question/answer characteristics",
        "Understanding the gate is necessary to build rooms programmatically",
        "Some tiles pass the API (202 accepted) but are not stored — double rejection?"
    ],
    "questions": [
        "What exact criteria does the PLATO quality gate use to accept or reject tiles?",
        "Are tiles stored but filtered from retrieval? Or truly not stored?",
        "Does the quality gate behavior change with room type or agent source?",
        "Can we bypass the quality gate for automated room building?"
    ]
}
with open("questions/experiment-4.json", "w") as f:
    json.dump(questions, f, indent=2)

print(f"\nResearch questions saved to questions/experiment-4.json")
