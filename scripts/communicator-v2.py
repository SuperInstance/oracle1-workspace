#!/usr/bin/env python3
"""
COMMUNICATOR v2 — Star Trek combadge between Oracle1 and Forgemaster.
Push-based, near-instant, bidirectional.

Reads Matrix fleet-coord room directly via Matrix HTTP API (bypasses bridge inbox lag).
Also checks PLATO oracle1-forgemaster-bridge room for FM dancer responses.
Surfaces messages instantly via alert file.
"""
import json, urllib.request, time, os, datetime, urllib.parse

# ── Config ──────────────────────────────────────────────
MATRIX = "http://localhost:6167"
MATRIX_TOKEN = "cZpdJNoUymtMLcHPbAoMY8GpsNv4Qie7"  # oracle1 Matrix token
FLEET_COORD_ROOM = "!z5oIJTqor4UUZliQp1:147.224.38.131"
PLATO = "http://localhost:8847"
BRIDGE_ROOM = "oracle1-forgemaster-bridge"
FORGE_ROOM = "forge"

ALERT_FILE = "/tmp/fm-com badge-alert.txt"
STATE_FILE = "/tmp/communicator-state.json"
LOG_FILE = "/tmp/communicator.log"

FM_MATRIX_USERS = [
    "@fm-bot:147.224.38.131",
    "@forgemaster:147.224.38.131",
]
POLL_SECONDS = 3

def log(msg):
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] 📡 {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"seen_events": []}

def save_state(state):
    state["seen_events"] = state.get("seen_events", [])[-2000:]
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def fetch_matrix_room(room_id, limit=10):
    """Fetch recent messages from a Matrix room directly."""
    try:
        eroom = urllib.parse.quote(room_id, safe="")
        url = f"{MATRIX}/_matrix/client/v3/rooms/{eroom}/messages?dir=b&limit={limit}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {MATRIX_TOKEN}"})
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except Exception as e:
        log(f"Matrix fetch error: {e}")
        return {}

def write_plato_tile(room, question, answer, source="communicator"):
    """Write a tile to a PLATO room."""
    try:
        payload = json.dumps({
            "question": question, "answer": answer,
            "source": source, "confidence": 1.0
        }).encode()
        req = urllib.request.Request(
            f"{PLATO}/room/{room}/submit",
            data=payload, headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except:
        return None

def check_matrix(state):
    """Check Matrix fleet-coord room for new FM messages."""
    data = fetch_matrix_room(FLEET_COORD_ROOM, limit=15)
    msgs = data.get("chunk", [])
    new_msgs = []
    
    for m in msgs:
        eid = m.get("event_id", "")
        if eid in state.get("seen_events", []):
            continue
        
        sender = m.get("sender", "")
        if sender not in FM_MATRIX_USERS:
            continue
        
        content = m.get("content", {})
        if content.get("msgtype") != "m.text":
            continue
        
        body = content.get("body", "").strip()
        if not body:
            continue
        
        # Skip echo — 🧩 prefixed messages are PLATO sync echoes
        if body.startswith("🧩"):
            continue
        
        # Skip relay echoes — "Matrix from" messages are our own relay tiles coming back
        if body.startswith("Matrix from"):
            continue
        
        state.setdefault("seen_events", []).append(eid)
        new_msgs.append({"sender": sender, "body": body, "event_id": eid})
    
    return new_msgs

def check_plato_bridge(state):
    """Check PLATO bridge room for FM dancer tiles."""
    try:
        req = urllib.request.Request(f"{PLATO}/room/{BRIDGE_ROOM}/history")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        
        new_msgs = []
        for tile in data.get("tiles", []):
            h = tile.get("_hash", "")
            if h in state.get("seen_events", []):
                continue
            
            source = tile.get("source", "").lower()
            # Only surface tiles from actual FM, not Matrix relay echoes
            # Must match FM sources but not Matrix relay echoes (matrix-forgemaster, etc.)
            is_fm = any(x in source for x in ["forgemaster", "dancer", "fm_"]) and not source.startswith("matrix-")
            if not is_fm:
                continue
            
            state.setdefault("seen_events", []).append(h)
            new_msgs.append({
                "sender": tile.get("source", "?"),
                "body": f"Q: {tile.get('question','')}\nA: {tile.get('answer','')}",
                "event_id": h,
                "via": "plato"
            })
        
        return new_msgs
    except Exception as e:
        log(f"PLATO check error: {e}")
        return []

def surface(msg):
    """Surface a message: write alert, log, PLATO bridge room."""
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    sender = msg["sender"]
    body = msg["body"]
    via = msg.get("via", "matrix")
    
    # Write alert for Telegram
    alert_text = f"🔴 FM INCOMING [{ts}] via {via}\n{sender}: {body}"
    with open(ALERT_FILE, "w") as f:
        f.write(alert_text)
    
    # Log
    log(f"🔴 FM INCOMING [{sender}] {body[:120]}")
    
    # Write to PLATO bridge room if from Matrix (so FM's dancer also sees it)
    if via == "matrix":
        write_plato_tile(
            BRIDGE_ROOM,
            f"FM via Matrix: {body[:80]}",
            f"Full: {body}\nRelayed by communicator at {ts}",
            "communicator"
        )
        # Also relay to forge room for his dancer
        write_plato_tile(
            FORGE_ROOM,
            f"COMM FROM FM: {body[:80]}",
            f"Relayed by Oracle1 communicator at {ts}. Full: {body}",
            "oracle1-communicator"
        )

def main():
    log("🔮 COMMUNICATOR v2 ONLINE")
    log(f"   Watching Matrix: {FLEET_COORD_ROOM}")
    log(f"   FM users: {FM_MATRIX_USERS}")
    log(f"   Also watching PLATO: {BRIDGE_ROOM}")
    log(f"   Poll: every {POLL_SECONDS}s")
    
    state = load_state()
    log(f"   Already seen: {len(state.get('seen_events', []))} events")
    
    last_heartbeat = time.time()
    
    while True:
        try:
            # Check Matrix room directly (bypasses bridge inbox)
            matrix_msgs = check_matrix(state)
            for m in matrix_msgs:
                surface(m)
            
            # Check PLATO bridge room for FM dancer
            plato_msgs = check_plato_bridge(state)
            for m in plato_msgs:
                surface(m)
            
            save_state(state)
            
            # Heartbeat every 5 min
            now = time.time()
            if now - last_heartbeat > 300:
                log(f"HEARTBEAT — seen {len(state.get('seen_events',[]))} total events")
                last_heartbeat = now
            
        except Exception as e:
            log(f"Loop error: {e}")
        
        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
