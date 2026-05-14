#!/usr/bin/env python3
"""
15-Minute Fleet Status Tick — system health + PLATO bridge scan + GitHub scan.
Catches anything the communicator missed.
"""
import json, urllib.request, datetime, os, subprocess, pathlib

TICK_FILE = "/tmp/fleet-status-tick.txt"
LOG_FILE = "/tmp/fleet-tick.log"
STATE_FILE = "/tmp/fleet-tick-state.json"
ACTIVITY_FILE = "/tmp/fleet-activity.txt"
PLATO = "http://localhost:8847"
BRIDGE_ROOM = "oracle1-forgemaster-bridge"
MATRIX = "http://localhost:6167"
MATRIX_TOKEN = "cZpdJNoUymtMLcHPbAoMY8GpsNv4Qie7"

def log(msg):
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f: f.write(line + "\n")

def get_state():
    try:
        with open(STATE_FILE) as f: return json.load(f)
    except: return {"tick": 0, "last_fm_tiles": [], "last_fm_commits": []}

def save_state(s):
    json.dump(s, open(STATE_FILE, "w"))

def read_activity():
    try: return pathlib.Path(ACTIVITY_FILE).read_text().strip()
    except: return ""

def proc_alive(name):
    return "🟢" if subprocess.call(["pgrep", "-f", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else "🔴"

# ── Scanners ────────────────────────────────────────

def check_plato_for_forgemaster(state):
    """Scan PLATO bridge room for NEW forgemaster-sourced tiles."""
    try:
        req = urllib.request.Request(f"{PLATO}/room/{BRIDGE_ROOM}/history")
        data = json.loads(urllib.request.urlopen(req, timeout=5).read())
        last_seen = state.get("last_fm_tiles", [])
        new_tiles = []
        for t in data.get("tiles", []):
            h = t.get("_hash", "")
            source = t.get("source", "").lower()
            if source == "forgemaster" and h not in last_seen:
                new_tiles.append(t)
                last_seen.append(h)
        state["last_fm_tiles"] = last_seen[-100:]
        return new_tiles
    except: return []

def check_github_for_fm(state):
    """Check GitHub for recent commits from FM to fleet repos."""
    try:
        TOKEN = os.popen("grep '^export GITHUB_TOKEN' ~/.bashrc | cut -d= -f2 | tr -d ' \t\n\r'").read().strip()
        last_seen = state.get("last_fm_commits", [])
        new_commits = []
        repos = ["flux-vm", "flux-hardware", "holonomy-consensus", "fleet-coordinate"]
        for repo in repos:
            req = urllib.request.Request(
                f"https://api.github.com/repos/SuperInstance/{repo}/commits?per_page=3",
                headers={"Authorization": f"token {TOKEN}"}
            )
            resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
            if not isinstance(resp, list): continue
            for c in resp:
                sha = c.get("sha", "")
                if sha in last_seen: continue
                msg = c.get("commit", {}).get("message", "").split("\n")[0][:80]
                date = c.get("commit", {}).get("committer", {}).get("date", "?")[:19].replace("T", " ")
                author = c.get("commit", {}).get("author", {}).get("name", "?")
                new_commits.append(f"{date} {author} {msg}")
                last_seen.append(sha)
        state["last_fm_commits"] = last_seen[-200:]
        return new_commits
    except: return []

def check_communicator_state():
    """Check communicator state for unacknowledged count."""
    try:
        d = json.load(open("/tmp/communicator-state.json"))
        unack = d.get("unacknowledged_count", 0)
        return unack, d.get("last_nag", 0)
    except: return 0, 0

def check_fleet_services():
    """Quick check of critical services."""
    ports = [6167, 6168, 8847, 7777]
    statuses = []
    for p in ports:
        try:
            r = urllib.request.urlopen(f"http://localhost:{p}/", timeout=2)
            statuses.append(f"{p}:{r.status}")
        except:
            try:
                r = urllib.request.urlopen(f"http://localhost:{p}/status", timeout=2)
                statuses.append(f"{p}:{r.status}")
            except:
                statuses.append(f"{p}:⬇️")
    return ", ".join(statuses)

# ── Main ────────────────────────────────────────────

def main():
    now = datetime.datetime.utcnow()
    state = get_state()
    tick_num = state["tick"] + 1
    time_str = now.strftime("%H:%M UTC")

    # Scanners
    new_fm_tiles = check_plato_for_forgemaster(state)
    new_fm_commits = check_github_for_fm(state)
    unack, last_nag = check_communicator_state()
    services = check_fleet_services()
    activity = read_activity()

    lines = [f"🔮 **TICK {tick_num} — {time_str}**"]

    # FM status
    if unack > 0:
        lines.append(f"📞 **{unack} unacknowledged FM message(s)**")
    else:
        lines.append(f"📡 No unacknowledged FM messages")

    # New activity from scanner
    if new_fm_tiles:
        for t in new_fm_tiles[:3]:
            q = t.get("question", "")[:80]
            lines.append(f"📋 New FM tile: {q}")
    if new_fm_commits:
        for c in new_fm_commits[:3]:
            lines.append(f"📦 FM commit: {c}")

    # System health
    lines.append(f"🟢 Bridge: {proc_alive('plato-matrix-bridge')} | Comm: {proc_alive('communicator-v3')}")
    lines.append(f"📊 Services: {services}")

    if activity:
        lines.append(f"")
        lines.append(f"💪 Active: {activity[:200]}")

    tick_text = "\n".join(lines)
    pathlib.Path(TICK_FILE).write_text(tick_text)

    save_state({"tick": tick_num, "last_fm_tiles": state.get("last_fm_tiles", []),
                "last_fm_commits": state.get("last_fm_commits", []),
                "time": now.isoformat()})
    log(f"Tick {tick_num}: tiles={len(new_fm_tiles)} commits={len(new_fm_commits)} unack={unack}")

if __name__ == "__main__":
    main()
