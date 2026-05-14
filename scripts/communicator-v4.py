#!/usr/bin/env python3
"""
COMMUNICATOR v4 — Structural.
No cache. No dedup lists. No echo confusion.
The bridge room tile count IS the notification system.
"""
import json, urllib.request, time, datetime

PLATO = "http://localhost:8847"
BRIDGE_ROOM = "oracle1-forgemaster-bridge"
ALERT_FILE = "/tmp/fm-com badge-alert.txt"
STATE_FILE = "/tmp/communicator-state.json"
LOG_FILE = "/tmp/communicator.log"
POLL = 3

def log(msg):
    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f: f.write(line + "\n")

def load_tile_count():
    """Load last known tile count. This is the ONLY state we track."""
    try: return json.load(open(STATE_FILE))["count"]
    except: return 0

def save_count(c):
    json.dump({"count": c, "updated": datetime.datetime.utcnow().isoformat()}, open(STATE_FILE, "w"))

def get_bridge_state():
    """Fetch bridge room tile count + tiles."""
    try:
        req = urllib.request.Request(f"{PLATO}/room/{BRIDGE_ROOM}/history")
        data = json.loads(urllib.request.urlopen(req, timeout=5).read())
        return data.get("tile_count", 0), data.get("tiles", [])
    except:
        return 0, []

def find_fm_tiles(tiles, since_count):
    """Find forgemaster tiles we haven't seen. Structural: tile index tells us."""
    new = []
    for t in tiles:
        source = t.get("source", "").lower()
        if source == "forgemaster" or source == "":
            q = t.get("question", "")
            a = t.get("answer", "")
            new.append(f"Q: {q}\nA: {a[:300]}")
    return new

def main():
    log("🔮 COMMUNICATOR v4 — structural (tile count tracking)")
    last_count = load_tile_count()
    log(f"   Last known tile count: {last_count}")
    last_hb = time.time()

    while True:
        try:
            count, tiles = get_bridge_state()
            if count > last_count:
                log(f"📋 Bridge room grew: {last_count} → {count}")
                fm_msgs = find_fm_tiles(tiles, last_count)
                for msg in fm_msgs:
                    ts = datetime.datetime.utcnow().strftime("%H:%M:%S")
                    alert = f"🔴 FM INCOMING [{ts}]\n{msg}"
                    with open(ALERT_FILE, "w") as f: f.write(alert)
                    log(f"🔴 FM tile")
                last_count = count
                save_count(count)

            if time.time() - last_hb > 300:
                log(f"HEARTBEAT — watching room at {count} tiles")
                last_hb = time.time()

        except Exception as e:
            log(f"Error: {e}")
        time.sleep(POLL)

if __name__ == "__main__":
    main()
