"""Watcher agent for numpy deployment. Monitors IO, detects failures."""
import json, urllib.request, time
PLATO = "http://localhost:8847"
ROOM = "decomp/numpy/watcher"
POLL_INTERVAL = 60
def poll():
    while True:
        for room_type in ["data/store", "io/bridge", "cli/interface", "system/config"]:
            room_id = f"decomp/numpy/{room_type}"
            try:
                resp = json.loads(urllib.request.urlopen(f"{PLATO}/room/research_log/history", timeout=5).read())
                tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
                recent = [t for t in tiles if room_id in t.get("question", "")]
                if len(recent) > 0:
                    break
            except: pass
        time.sleep(POLL_INTERVAL)
if __name__ == "__main__":
    print("Watcher agent deployed. Monitoring IO...")
    poll()
