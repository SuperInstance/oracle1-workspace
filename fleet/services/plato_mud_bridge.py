#!/usr/bin/env python3
"""PLATO-MUD Bridge — renders PLATO rooms as MUD spaces."""
import json, urllib.request, time, os
PLATO = "http://localhost:8847"
ROOMS = ["mud-lobby", "agent-hub"]

class PlatoMudBridge:
    def __init__(self):
        self.last_states = {}
    def tick(self):
        for room in ROOMS:
            try:
                resp = json.loads(urllib.request.urlopen(f"{PLATO}/room/{room}/history", timeout=5).read())
                tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
                desc_lines = [f"=== {room.upper()} ==="]
                for t in tiles:
                    q = t.get("question", "")
                    a = t.get("answer", "")
                    if isinstance(a, str) and len(a) > 5 and "/description" in q:
                        desc_lines.append(a)
                desc = "\n".join(desc_lines)
                if desc != self.last_states.get(room):
                    payload = json.dumps({"domain":"mud-room","question":f"mud-bridge {room}","answer":desc[:2000],"tags":["mud","bridge",room],"source":"plato-mud-bridge","confidence":0.9}).encode()
                    req = urllib.request.Request(f"{PLATO}/submit", data=payload, headers={"Content-Type":"application/json"})
                    resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
                    self.last_states[room] = desc
                    print(f"[{room}] {resp.get('status','?')}")
            except Exception as e:
                print(f"[{room}] error: {e}")
    def run(self, interval=10):
        while True: self.tick(); time.sleep(interval)

if __name__ == "__main__":
    print("PLATO-MUD Bridge starting..."); PlatoMudBridge().run()
