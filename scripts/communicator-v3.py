#!/usr/bin/env python3
"""
COMMUNICATOR v3 — Star Trek combadge w/ nagging, dedup fix, PLATO+GitHub scanner
"""
import json, urllib.request, time, os, datetime, urllib.parse

MATRIX = "http://localhost:6167"
MATRIX_TOKEN = "cZpdJNoUymtMLcHPbAoMY8GpsNv4Qie7"
FLEET_COORD_ROOM = "!z5oIJTqor4UUZliQp1:147.224.38.131"
PLATO = "http://localhost:8847"
BRIDGE_ROOM = "oracle1-forgemaster-bridge"
FORGE_ROOM = "forge"
ALERT_FILE = "/tmp/fm-com badge-alert.txt"
STATE_FILE = "/tmp/communicator-state.json"
LOG_FILE = "/tmp/communicator.log"
FM_MATRIX_USERS = ["@fm-bot:147.224.38.131", "@forgemaster:147.224.38.131"]
POLL_SECONDS = 3

def log(msg):
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] 📡 {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f: f.write(line + "\n")

def load_state():
    try:
        d = json.load(open(STATE_FILE))
        # Ensure all keys exist
        for k in ["seen_matrix", "seen_plato", "unacknowledged_count", "last_nag", "last_ack"]:
            d.setdefault(k, 0 if "count" in k or k.startswith("last_") else [])
        return d
    except:
        return {"seen_matrix": [], "seen_plato": [], "unacknowledged_count": 0, "last_nag": 0, "last_ack": 0}

def save_state(state):
    state["seen_matrix"] = state["seen_matrix"][-2000:]
    state["seen_plato"] = state["seen_plato"][-1000:]
    json.dump(state, open(STATE_FILE, "w"))

def write_plato_tile(room, q, a, source="communicator"):
    try:
        data = json.dumps({"question": q, "answer": a, "source": source, "confidence": 1.0}).encode()
        req = urllib.request.Request(f"{PLATO}/room/{room}/submit", data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except: pass

def surface(sender, body, via, state):
    """Surface message + increment unacknowledged count."""
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    alert = f"🔴 FM INCOMING [{ts}] via {via}\n{sender}: {body}"
    with open(ALERT_FILE, "w") as f: f.write(alert)
    log(f"🔴 FM INCOMING [{sender}] {body[:120]}")
    state["unacknowledged_count"] = state.get("unacknowledged_count", 0) + 1

def check_matrix(state):
    """Check Matrix fleet-coord for new FM messages."""
    try:
        eroom = urllib.parse.quote(FLEET_COORD_ROOM, safe="")
        req = urllib.request.Request(f"{MATRIX}/_matrix/client/v3/rooms/{eroom}/messages?dir=b&limit=10",
            headers={"Authorization": f"Bearer {MATRIX_TOKEN}"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read())
        new = []
        for m in data.get("chunk", []):
            eid = m.get("event_id", "")
            if eid in state["seen_matrix"]: continue
            state["seen_matrix"].append(eid)
            sender = m.get("sender", "")
            if sender not in FM_MATRIX_USERS: continue
            body = m.get("content", {}).get("body", "").strip()
            if not body or body.startswith("🧩") or body.startswith("Matrix from"): continue
            new.append((sender, body, "matrix"))
        return new
    except: return []

def check_plato_bridge(state):
    """Check PLATO bridge room for actual forgemaster-sourced tiles (not echoes)."""
    try:
        req = urllib.request.Request(f"{PLATO}/room/{BRIDGE_ROOM}/history")
        data = json.loads(urllib.request.urlopen(req, timeout=5).read())
        new = []
        for tile in data.get("tiles", []):
            h = tile.get("_hash", "")
            if h in state["seen_plato"]: continue
            state["seen_plato"].append(h)
            source = tile.get("source", "").lower()
            # Only real forgemaster tiles, not Matrix echoes
            if source == "forgemaster" or ("forgemaster" in source and not source.startswith("matrix-")):
                q = tile.get("question", "")
                a = tile.get("answer", "")
                body = f"Q: {q}\nA: {a[:300]}"
                new.append((source, body, "plato"))
        return new
    except: return []

def check_nag(state):
    """If unacknowledged, nag every 5 minutes by re-writing alert."""
    count = state.get("unacknowledged_count", 0)
    if count == 0: return
    now = time.time()
    last_nag = state.get("last_nag", 0)
    if now - last_nag < 300: return  # 5 min
    state["last_nag"] = now
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    alert = f"📞 NAG [{ts}] — {count} unacknowledged FM message(s). Respond to clear."
    with open(ALERT_FILE, "w") as f: f.write(alert)
    log(f"📞 NAG: {count} unacknowledged")

def main():
    log("🔮 COMMUNICATOR v3 ONLINE — w/ nagging + dedup fix")
    state = load_state()
    log(f"   Seen Matrix: {len(state['seen_matrix'])} | Seen PLATO: {len(state['seen_plato'])}")
    log(f"   Unacknowledged: {state.get('unacknowledged_count', 0)}")
    last_hb = time.time()

    while True:
        try:
            # Check Matrix
            for sender, body, via in check_matrix(state):
                surface(sender, body, via, state)

            # Check PLATO bridge room
            for sender, body, via in check_plato_bridge(state):
                surface(sender, body, via, state)

            # Nag logic
            check_nag(state)

            save_state(state)

            if time.time() - last_hb > 300:
                log(f"HEARTBEAT — U:{state.get('unacknowledged_count',0)} M:{len(state['seen_matrix'])} P:{len(state['seen_plato'])}")
                last_hb = time.time()
        except Exception as e:
            log(f"Error: {e}")
        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
