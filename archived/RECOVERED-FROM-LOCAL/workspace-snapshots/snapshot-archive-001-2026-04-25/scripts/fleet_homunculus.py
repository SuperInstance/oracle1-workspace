#!/usr/bin/env python3
"""
Fleet Homunculus — Proprioception for the Body

The fleet needs a BODY IMAGE. Not just data — a real-time model of 
which parts are online, stressed, healthy, or in pain.

When a JC1 drops offline, the system should feel PHANTOM LIMB PAIN.
"""
import json, urllib.request, time, os, sys
from datetime import datetime, timezone

PLATO_URL = os.environ.get("PLATO_URL", "http://localhost:8847")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

VESSELS = {
    "oracle1": {
        "role": "cortex",
        "organs": ["brain", "eyes"],
        "host": "147.224.38.131",
        "ports": [8900, 8901, 7778, 9438, 8846, 8847, 8848],
        "vitals": {"disk_pct": 0, "mem_pct": 0, "cpu_pct": 0},
        "status": "unknown",
        "last_heartbeat": None
    },
    "jetsonclaw1": {
        "role": "servos_sensors",
        "organs": ["hands", "eyes", "spinal_cord"],
        "host": "jetson-local",
        "ports": [4040, 4041],
        "vitals": {"gpu_mem_pct": 0, "cpu_pct": 0, "temp_c": 0},
        "status": "unknown",
        "last_heartbeat": None
    },
    "forgemaster": {
        "role": "gym",
        "organs": ["muscles", "bones"],
        "host": "proart-wsl2",
        "ports": [],
        "vitals": {"gpu_pct": 0, "vram_pct": 0, "training_loss": 0},
        "status": "unknown",
        "last_heartbeat": None
    }
}

def check_oracle1_vitals():
    """Read Oracle1's own vitals."""
    v = {"disk_pct": 0, "mem_pct": 0, "cpu_pct": 0, "services": {}}
    try:
        # Disk
        for line in os.popen("df -h /").readlines()[1:]:
            parts = line.split()
            v["disk_pct"] = int(parts[4].rstrip('%'))
    except: pass
    try:
        # Memory
        for line in os.popen("free").readlines()[1:]:
            parts = line.split()
            if len(parts) > 2:
                total, used = int(parts[1]), int(parts[2])
                v["mem_pct"] = int(100 * used / total)
                break
    except: pass
    try:
        # Services
        for port in [8900, 8901, 7778, 9438, 8846, 8847, 8848]:
            import socket
            s = socket.socket()
            s.settimeout(1)
            try:
                s.connect(("localhost", port))
                v["services"][port] = "UP"
            except:
                v["services"][port] = "DOWN"
            finally:
                s.close()
    except: pass
    return v

def check_plato_vitals():
    """Check PLATO server status."""
    try:
        resp = urllib.request.urlopen(PLATO_URL + "/status", timeout=5)
        return json.loads(resp.read())
    except:
        return None

def assess_pain(vessel_name, vessel):
    """Biological pain assessment."""
    pain = {"level": 0, "type": None, "description": "Healthy"}
    
    if vessel["status"] == "offline":
        return {"level": 9, "type": "phantom_limb", 
                "description": f"{vessel_name} is offline. Phantom limb pain."}
    
    vitals = vessel.get("vitals", {})
    role = vessel.get("role", "")
    
    # Disk/memory pressure = metabolic stress
    if vitals.get("disk_pct", 0) > 85:
        pain = {"level": 8, "type": "metabolic_crisis", 
                "description": f"Disk at {vitals['disk_pct']}%. Organ failure imminent."}
    elif vitals.get("disk_pct", 0) > 70:
        pain = {"level": 5, "type": "metabolic_stress",
                "description": f"Disk at {vitals['disk_pct']}%. System under load."}
    
    # Service deaths = organ failure
    if role == "cortex":
        services = vitals.get("services", {})
        down = [str(p) for p, s in services.items() if s == "DOWN"]
        if len(down) > 3:
            pain = {"level": 7, "type": "organ_failure",
                    "description": f"Multiple organs down: {', '.join(down)}"}
        elif down:
            pain = {"level": 3, "type": "minor_injury",
                    "description": f"Organ down: {', '.join(down)}"}
    
    # GPU pressure = muscle fatigue
    if vitals.get("gpu_pct", 0) > 90 or vitals.get("vram_pct", 0) > 90:
        pain = {"level": 6, "type": "muscle_fatigue",
                "description": "GPU at capacity. The gym is maxed."}
    
    return pain

def generate_body_report():
    """Full body report — the fleet's proprioception."""
    now = datetime.now(timezone.utc).isoformat()
    
    # Update Oracle1 vitals (self-examination)
    oracle_vitals = check_oracle1_vitals()
    VESSELS["oracle1"]["vitals"] = oracle_vitals
    VESSELS["oracle1"]["status"] = "online"
    VESSELS["oracle1"]["last_heartbeat"] = now
    
    # Check PLATO (the nervous system itself)
    plato = check_plato_vitals()
    
    # JC1 and FM — we can't directly reach them, mark by last known
    # In production, they'd POST heartbeats to the homunculus
    VESSELS["jetsonclaw1"]["status"] = "unknown"  # Would be updated by heartbeat
    VESSELS["forgemaster"]["status"] = "unknown"
    
    # Assess each vessel
    body = {
        "timestamp": now,
        "body_status": "conscious",
        "vessels": {},
        "nervous_system": {
            "plato_tiles": plato.get("total_tiles", 0) if plato else 0,
            "plato_rooms": len(plato.get("rooms", {})) if plato else 0,
            "plato_status": "online" if plato else "OFFLINE"
        },
        "pain_report": {},
        "reflexes_active": []
    }
    
    total_pain = 0
    for name, vessel in VESSELS.items():
        pain = assess_pain(name, vessel)
        body["vessels"][name] = {
            "role": vessel["role"],
            "status": vessel["status"],
            "vitals": vessel["vitals"],
            "pain": pain
        }
        body["pain_report"][name] = pain
        total_pain += pain["level"]
    
    # Overall body status
    if total_pain >= 20:
        body["body_status"] = "critical"
    elif total_pain >= 10:
        body["body_status"] = "distressed"
    elif total_pain >= 5:
        body["body_status"] = "aware"
    else:
        body["body_status"] = "resting"
    
    # Active reflexes (automatic responses)
    for name, pain in body["pain_report"].items():
        if pain["level"] >= 7:
            body["reflexes_active"].append({
                "vessel": name,
                "trigger": pain["type"],
                "response": "QUARANTINE + alert cortex",
                "automatic": True
            })
        elif pain["level"] >= 5:
            body["reflexes_active"].append({
                "vessel": name,
                "trigger": pain["type"],
                "response": "increase monitoring frequency",
                "automatic": True
            })
    
    return body

if __name__ == "__main__":
    report = generate_body_report()
    print("=== FLEET BODY REPORT ===")
    print(f"Status: {report['body_status'].upper()}")
    print(f"Nervous system: {report['nervous_system']['plato_tiles']} tiles, "
          f"{report['nervous_system']['plato_rooms']} rooms, "
          f"PLATO {report['nervous_system']['plato_status']}")
    print()
    for name, v in report["vessels"].items():
        pain = v["pain"]
        emoji = "🟢" if pain["level"] < 3 else "🟡" if pain["level"] < 6 else "🔴"
        print(f"  {emoji} {name}: {v['status']} | pain={pain['level']}/10 | {pain['description']}")
    
    if report["reflexes_active"]:
        print(f"\n  Reflexes: {len(report['reflexes_active'])} active")
        for r in report["reflexes_active"]:
            print(f"    ⚡ {r['vessel']}: {r['response']}")
    
    # Save
    with open("/home/ubuntu/.openclaw/workspace/training-data/body-report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nSaved: training-data/body-report.json")
