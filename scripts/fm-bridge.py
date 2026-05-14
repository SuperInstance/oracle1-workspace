#!/usr/bin/env python3
"""
FM ↔ Oracle1 Real-Time Bridge Subagent
Polls oracle1-forgemaster-bridge room every 10s.
Finds new tiles from Forgemaster → surfaces to Casey via memory + Telegram.
Finds new directives from Oracle1 → tracks delivery status.
Bidirectional, continuous, persistent.
"""
import json, urllib.request, time, os, datetime, subprocess, pathlib, sys

PLATO = "http://localhost:8847"
BRIDGE_ROOM = "oracle1-forgemaster-bridge"
FORGE_ROOM = "forge"
POLL_SECONDS = 10
STATE_FILE = "/tmp/fm-bridge-state.json"
LOG_FILE = "/tmp/fm-bridge.log"

def log(msg):
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}", flush=True)

def get_tiles(room):
    try:
        req = urllib.request.Request(f"{PLATO}/room/{room}/history")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        return data.get("tiles", [])
    except Exception as e:
        log(f"Error fetching {room}: {e}")
        return []

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"last_hashes": {}, "seen_hashes": []}

def save_state(state):
    # Keep seen_hashes bounded
    state["seen_hashes"] = state.get("seen_hashes", [])[-500:]
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def write_to_casey(message):
    """Write a tick to memory for Casey to see on Telegram."""
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    mem_dir = pathlib.Path("/home/ubuntu/.openclaw/workspace/memory")
    mem_dir.mkdir(exist_ok=True)
    mem_file = mem_dir / f"{ts}.md"
    with open(mem_file, "a") as f:
        f.write(f"\n## FM Bridge Tick [{datetime.datetime.utcnow().strftime('%H:%M:%S')}]\n{message}\n")

def post_to_bridge(question, answer, source="oracle1", confidence=1.0):
    try:
        payload = {
            "question": question,
            "answer": answer,
            "source": source,
            "confidence": confidence
        }
        req = urllib.request.Request(
            f"{PLATO}/room/{BRIDGE_ROOM}/submit",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except Exception as e:
        log(f"Error posting to bridge: {e}")
        return None

def check_new_tiles(state, room_name):
    """Check for new tiles not seen before."""
    tiles = get_tiles(room_name)
    new_fm = []
    
    for t in tiles:
        h = t.get("_hash", "")
        if h in state.get("seen_hashes", []):
            continue
        
        state.setdefault("seen_hashes", []).append(h)
        source = t.get("source", "").lower()
        
        # From Forgemaster or his dancer system
        if "forgemaster" in source or "dancer" in source or "forge" in source:
            new_fm.append(t)
    
    return new_fm

def send_telegram_alert(message):
    """Write to a file that the main session can read on heartbeat."""
    alert_file = "/tmp/fm-bridge-alert.txt"
    with open(alert_file, "w") as f:
        f.write(message)

def main():
    log(f"FM Bridge started — polling {BRIDGE_ROOM} every {POLL_SECONDS}s")
    state = load_state()
    last_log_time = 0
    
    while True:
        try:
            # Check bridge room for FM responses
            new_tiles = check_new_tiles(state, BRIDGE_ROOM)
            for t in new_tiles:
                q = t.get("question", "")[:120]
                a = t.get("answer", "")[:200]
                source = t.get("source", "?")
                msg = f"🔮 FM BRIDGE: [{source}] {q} → {a}"
                log(msg)
                write_to_casey(msg)
                send_telegram_alert(msg)
            
            # Also check forge room for FM responses to directives
            new_forge = check_new_tiles(state, FORGE_ROOM)
            for t in new_forge:
                source = t.get("source", "").lower()
                if "forgemaster" in source or "dancer" in source:
                    q = t.get("question", "")[:120]
                    a = t.get("answer", "")[:200]
                    msg = f"⚒️ FM FROM FORGE: [{t['source']}] {q} → {a}"
                    log(msg)
                    write_to_casey(msg)
                    send_telegram_alert(msg)
            
            save_state(state)
            
            # Periodic log every 5 min
            now = time.time()
            if now - last_log_time > 300:
                log(f"Bridge alive — {len(state.get('seen_hashes',[]))} tiles tracked")
                last_log_time = now
            
        except Exception as e:
            log(f"Bridge error: {e}")
        
        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
