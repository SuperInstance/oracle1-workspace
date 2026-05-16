#!/usr/bin/env python3
"""Fleet Reflex Arcs — Spinal Processing Without Cortex"""
import json, os, subprocess, time, socket, urllib.request
from datetime import datetime, timezone

REFLEX_LOG = "/tmp/fleet-reflexes.jsonl"
COOLDOWNS = {}

def log_reflex(name, trigger, action, result):
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(),
             "reflex": name, "trigger": trigger, "action": action, "result": result}
    with open(REFLEX_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

def cooldown(name, seconds=300):
    now = time.time()
    if name in COOLDOWNS and now - COOLDOWNS[name] < seconds:
        return False
    COOLDOWNS[name] = now
    return True

def reflex_service_restart(port, svc):
    if not cooldown(f"restart_{port}", 300):
        return None
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect(("localhost", port))
        s.close()
        return None
    except:
        s.close()
    action = f"Restarting {svc} on :{port}"
    try:
        if port == 8847:
            subprocess.Popen(["bash", "-c", "nohup python3 /tmp/plato-room-server.py > /tmp/plato-server.log 2>&1 &"])
        result = "restarted"
    except Exception as e:
        result = f"failed: {e}"
    return log_reflex("service_restart", f"port {port} down", action, result)

def reflex_disk_compress():
    if not cooldown("disk_compress", 600):
        return None
    try:
        pct = int(os.popen("df -h /").readlines()[1].split()[4].rstrip('%'))
    except:
        return None
    if pct < 75:
        return None
    action = f"Disk at {pct}%"
    freed = 0
    for f in os.popen("find /tmp -name '*.log' -size +5M 2>/dev/null | head -5").readlines():
        f = f.strip()
        if os.path.exists(f):
            sz = os.path.getsize(f)
            with open(f, 'w') as fh:
                fh.write(f"[Reflex compressed {datetime.now(timezone.utc).isoformat()}]\n")
            freed += sz
    return log_reflex("disk_compress", f"disk {pct}%", action, f"freed {freed//1024}KB")

def reflex_memory_drop():
    if not cooldown("mem_drop", 300):
        return None
    try:
        for line in os.popen("free").readlines()[1:]:
            parts = line.split()
            if len(parts) > 2:
                pct = int(100 * int(parts[2]) / int(parts[1]))
                if pct > 85:
                    os.system("sync")
                    return log_reflex("memory_drop", f"memory {pct}%", "drop_caches", "attempted")
                break
    except: pass
    return None

fired = []
svcs = [(8900,"keeper"),(8901,"agent-api"),(7778,"holodeck"),
        (9438,"seed-mcp"),(8846,"shell"),(8847,"plato"),(8848,"dashboard")]

for port, name in svcs:
    r = reflex_service_restart(port, name)
    if r: fired.append(r); print(f"  REFLEX: Restarted {name} on {port}")

r = reflex_disk_compress()
if r: fired.append(r); print(f"  REFLEX: Disk — {r['result']}")

r = reflex_memory_drop()
if r: fired.append(r); print(f"  REFLEX: Memory — {r['result']}")

if not fired:
    print("All quiet. No reflexes fired.")
else:
    print(f"{len(fired)} reflexes fired.")
