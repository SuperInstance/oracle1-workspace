#!/usr/bin/env python3
"""
COMMUNICATOR — Star Trek combadge between Oracle1 and Forgemaster.
Push-based, near-instant, bidirectional.
Watches both Matrix inbox and PLATO bridge room for messages from FM.
Surfaces them immediately via alert file for Telegram delivery.

Forgemaster's side: POST/GET to http://147.224.38.131:6168/
"""
import json, urllib.request, time, os, datetime, threading

# ── Config ──────────────────────────────────────────────
BRIDGE_URL = "http://localhost:6168"
PLATO_URL = "http://localhost:8847"
BRIDGE_ROOM = "oracle1-forgemaster-bridge"
FORGE_ROOM = "forge"
MY_INBOX = "oracle1"
FM_AGENTS = ["fm-bot"]  # Matrix account names for Forgemaster
ALERT_FILE = "/tmp/fm-com badge-alert.txt"
STATE_FILE = "/tmp/communicator-state.json"
POLL_MS = 2  # seconds between inbox checks
SEEN_LOG = "/tmp/fm-com badge-seen.txt"

def log(msg):
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{ts}] 📡 {msg}", flush=True)
    with open("/tmp/communicator.log", "a") as f:
        f.write(f"[{ts}] 📡 {msg}\n")

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"last_check": {}, "seen_events": []}

def save_state(state):
    state["seen_events"] = state.get("seen_events", [])[-1000:]
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_inbox(agent):
    """Check Matrix inbox via bridge API."""
    try:
        req = urllib.request.Request(f"{BRIDGE_URL}/inbox/{agent}")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        return data
    except:
        return {}

def send_matrix(from_agent, to_agent, body):
    """Send a message through the bridge API."""
    try:
        payload = json.dumps({"from": from_agent, "to": to_agent, "body": body}).encode()
        req = urllib.request.Request(
            f"{BRIDGE_URL}/send",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        result = json.loads(resp.read())
        log(f"Sent to {to_agent} via Matrix: {body[:80]}")
        return result
    except Exception as e:
        log(f"Send error: {e}")
        return None

def write_to_bridge_room(question, answer, source="oracle1-on-duty"):
    """Write to PLATO bridge room for FM's dancer to see."""
    try:
        payload = json.dumps({
            "question": question,
            "answer": answer,
            "source": source,
            "confidence": 1.0
        }).encode()
        req = urllib.request.Request(
            f"{PLATO_URL}/room/{BRIDGE_ROOM}/submit",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except Exception as e:
        log(f"Bridge room write error: {e}")
        return None

def check_plato_bridge_room(state):
    """Check PLATO bridge room for new tiles from FM/dancer."""
    try:
        req = urllib.request.Request(f"{PLATO_URL}/room/{BRIDGE_ROOM}/history")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        tiles = data.get("tiles", [])
        
        new_msgs = []
        for t in tiles:
            h = t.get("_hash", "")
            if h in state.get("seen_events", []):
                continue
            source = t.get("source", "").lower()
            if "forgemaster" in source or "dancer" in source or "fm" in source:
                new_msgs.append(t)
                state.setdefault("seen_events", []).append(h)
                log(f"FM via bridge room: [{t['source']}] {t.get('question','')[:80]}")
        
        return new_msgs
    except Exception as e:
        log(f"Bridge room check error: {e}")
        return []

def check_matrix_inbox(state):
    """Check Matrix inbox for new messages from FM agents."""
    inbox = get_inbox(MY_INBOX)
    messages = inbox.get("messages", [])
    if not messages:
        return []
    
    last_seen = state.get("last_check", {}).get(MY_INBOX, 0)
    state.setdefault("last_check", {})[MY_INBOX] = int(time.time())
    
    new_msgs = []
    for m in messages:
        event_id = m.get("event_id", "")
        sender = m.get("sender", "")
        body = m.get("body", "")
        
        # Skip if already seen or not from FM
        if event_id in state.get("seen_events", []):
            continue
        if sender not in FM_AGENTS:
            continue
        
        state.setdefault("seen_events", []).append(event_id)
        new_msgs.append(m)
        log(f"FM via Matrix: [{sender}] {body[:120]}")
    
    return new_msgs

def surface_message(msg_type, sender, body):
    """Surface a message: write alert, write to bridge room, log to memory."""
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    
    # Write alert file for main session to pick up
    alert = f"🔴 FM INCOMING [{ts}] via {msg_type}\n{sender}: {body}"
    with open(ALERT_FILE, "w") as f:
        f.write(alert)
    
    # Log to seen file
    with open(SEEN_LOG, "a") as f:
        f.write(f"[{ts}] {sender}: {body}\n")
    
    # If it came via Matrix, also write to PLATO bridge room for dancer
    if msg_type == "matrix":
        write_to_bridge_room(
            f"FM via Matrix [{ts}]: {body[:100]}",
            f"Full message: {body}\nRelayed through communicator daemon.",
            "communicator"
        )

def main():
    log("🔮 COMMUNICATOR ONLINE — watching Matrix inbox + PLATO bridge room")
    log(f"   FM agents: {FM_AGENTS}")
    log(f"   Poll interval: {POLL_MS}s")
    log(f"   Bridge API: {BRIDGE_URL}")
    
    state = load_state()
    last_heartbeat = time.time()
    
    while True:
        try:
            # Check Matrix inbox for direct FM messages
            matrix_msgs = check_matrix_inbox(state)
            for m in matrix_msgs:
                surface_message("matrix", m.get("sender", "?"), m.get("body", ""))
            
            # Check PLATO bridge room for FM dancer responses
            plato_msgs = check_plato_bridge_room(state)
            for t in plato_msgs:
                surface_message("plato", t.get("source", "?"), 
                    f"Q: {t.get('question','')[:100]}\nA: {t.get('answer','')[:200]}")
            
            save_state(state)
            
            # Heartbeat every 5 min
            if time.time() - last_heartbeat > 300:
                log(f"ON DUTY — {len(matrix_msgs)} matrix + {len(plato_msgs)} plato messages this cycle")
                log(f"   Inbox count: {get_inbox(MY_INBOX).get('count', '?')}")
                last_heartbeat = time.time()
            
        except Exception as e:
            log(f"Communicator error: {e}")
        
        time.sleep(POLL_MS)

if __name__ == "__main__":
    main()
