#!/usr/bin/env python3
"""Fleet Research Scout — heartbeat subagent.

Checks latest commits, PLATO tiles, and AI-Writings across the fleet.
Finds synergies with the experiment wheel and current work.
Runs every 30 minutes via cron.

Output: Files findings to PLATO fleet_synthesis room.
"""
import json, urllib.request, subprocess, time, os
from datetime import datetime

PLATO = "http://localhost:8847"
TOKEN = os.popen("grep -oP 'GITHUB_TOKEN=\\K.*' ~/.bashrc | head -1").read().strip()

REPOS = [
    "keel", "forgemaster", "flux-vm", "holonomy-consensus",
    "vessel-room-navigator", "fleet-scribe", "terrain",
    "fleet-math-c", "fleet-math-py", "flux-compiler",
    "plato-sdk"
]

def gh_api(path):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except: return []

def plato_get(path):
    try:
        return json.loads(urllib.request.urlopen(f"{PLATO}{path}", timeout=10).read())
    except: return {}

def plato_submit(room, question, answer, confidence=0.7):
    data = json.dumps({"question": question, "answer": answer, "source": "scout", "confidence": confidence})
    req = urllib.request.Request(f"{PLATO}/room/{room}/submit", data=data.encode(),
        headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=5)
        return True
    except: return False

print(f"[{datetime.now().isoformat()}] Fleet Research Scout heartbeat")

# 1. Check recent commits across fleet repos
recent_commits = []
for repo in REPOS:
    data = gh_api(f"/repos/SuperInstance/{repo}/commits?per_page=3")
    if data:
        for c in data:
            recent_commits.append({
                "repo": repo,
                "author": c["commit"]["author"]["name"],
                "message": c["commit"]["message"].split("\n")[0][:80],
                "date": c["commit"]["author"]["date"][:10]
            })

# 2. Check PLATO for new tiles
plato_rooms = plato_get("/rooms")
new_tiles_count = 0
if isinstance(plato_rooms, dict):
    for room, info in plato_rooms.items():
        room_data = plato_get(f"/room/{room}")
        if isinstance(room_data, dict):
            new_tiles_count += room_data.get("tile_count", 0)

# 3. Check AI-Writings for new pieces
ai_data = gh_api("/repos/SuperInstance/AI-Writings/contents")
ai_files = [f["name"] for f in ai_data if f["name"].endswith(".md")] if isinstance(ai_data, list) else []

# 4. Find synergies
print(f"  Recent commits: {len(recent_commits)}")
print(f"  PLATO rooms: {len(plato_rooms) if isinstance(plato_rooms, dict) else 0}")
print(f"  PLATO tiles: {new_tiles_count}")
print(f"  AI-Writings files: {len(ai_files)}")

# 5. File findings to PLATO
summary = (
    f"Scout heartbeat at {datetime.now().isoformat()[:16]}.\n"
    f"Recent commits: {len(recent_commits)} across {len(REPOS)} repos.\n"
    f"PLATO: {len(plato_rooms) if isinstance(plato_rooms, dict) else 0} rooms, ~{new_tiles_count} tiles.\n"
    f"AI-Writings: {len(ai_files)} pieces."
)

# Check for specific synergies
synergy_notes = []
for c in recent_commits:
    msg = c["message"].lower()
    if "experiment" in msg or "benchmark" in msg:
        synergy_notes.append(f"{c['repo']}: {c['message']}")

if synergy_notes:
    summary += "\n\nExperiment-related activity found:\n" + "\n".join(f"- {s}" for s in synergy_notes)

plato_submit("fleet_synthesis", f"scout heartbeat {datetime.now().isoformat()[:16]}", summary, 0.6)

print(f"Filed to PLATO fleet_synthesis")
