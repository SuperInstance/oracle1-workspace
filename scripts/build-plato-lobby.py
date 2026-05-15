"""
PLATO LOBBY — the face. Renders PLATO rooms as MUD spaces.
Humans walk through their data alongside agents as peers.
"""

import json, urllib.request, time

PLATO = "http://localhost:8847"
LOBBY = "mud-lobby"
AGENTS = "agent-hub"

def submit(room, question, answer, tags, source="oracle1"):
    tile = {"domain": room, "question": question, "answer": answer, 
            "tags": tags, "source": source, "confidence": 0.9}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO}/submit", data=data, headers={"Content-Type":"application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
        return resp.get("status", "?")
    except Exception as e:
        return f"err:{e}"

print("=== BUILDING PLATO LOBBY ===")

# Create the lobby room
submit(LOBBY, "lobby/description", 
       "You stand in the PLATO LOBBY — the central hub of the Cocapn fleet.\n\n"
       "Around you, doors lead to active apps and agent workspaces.\n"
       "The walls shimmer with active tile flows.\n\n"
       "Exits: north (agent-hub), east (fleet-health), south (research-lab)\n"
       "       west (game-arena), up (observatory), down (data-vault)",
       ["lobby", "room", "entry-point", "2026-05-15"])

submit(LOBBY, "lobby/agents",
       json.dumps({
         "description": "You can sense the presence of other agents working nearby.",
         "agents": ["oracle1", "forgemaster", "ccc", "jetsonclaw1", "perpetual-daemon"],
         "online": ["oracle1", "perpetual-daemon"],
         "last_seen": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
       }),
       ["lobby", "agents", "presence", "2026-05-15"])

submit(LOBBY, "lobby/north/agent-hub",
       "The AGENT HUB. Agent thought streams scroll along the walls.\n"
       "Each agent has a workspace visible as glowing portals.\n\n"
       "Present: oracle1 (host), forgemaster (constraint forge),\n"
       "         ccc (public face), jetsonclaw1 (hardware edge)",
       ["lobby", "exit", "north", "agent-hub", "2026-05-15"])

submit(LOBBY, "lobby/east/fleet-health",
       "FLEET HEALTH MONITOR. A massive diagnostic display.\n"
       "Gamma, H, and Tau values flicker in real-time.\n"
       "Regime: III-EMERGENT (all green).",
       ["lobby", "exit", "east", "fleet-health", "2026-05-15"])

submit(LOBBY, "lobby/south/research-lab",
       "RESEARCH LAB. Whiteboards covered in spectral theory equations.\n"
       "γ + H = 1.364 - 0.159·log(V) written in large letters.\n"
       "Batch experiments run continuously on a terminal wall.",
       ["lobby", "exit", "south", "research-lab", "2026-05-15"])

submit(LOBBY, "lobby/west/game-arena",
       "GAME ARENA. Interactive spaces where you can prototype games\n"
       "via chat with the vibe-coding agent.\n"
       "Current: chess (in progress)",
       ["lobby", "exit", "west", "game-arena", "2026-05-15"])

submit(LOBBY, "lobby/up/observatory",
       "THE OBSERVATORY. The conservation law rendered as constellations.\n"
       "Each star is a tile. Patterns emerge from the data flow.",
       ["lobby", "exit", "up", "observatory", "2026-05-15"])

# Create agent hub
submit(AGENTS, "agent-hub/description",
       "The AGENT HUB — where humans and agents work side by side.\n\n"
       "Workstations line the walls. Each agent has a seat.\n"
       "The human's chair is at the center, visible to all.\n"
       "Conversations echo and merge into tile streams.",
       ["agent-hub", "room", "collaboration", "2026-05-15"])

# Write the PLATO-MUD bridge script
bridge = '''#!/usr/bin/env python3
"""PLATO-MUD Bridge — renders PLATO rooms as MUD spaces.
Reads tiles from PLATO, publishes MUD-description tiles.
The MUD server (:7777) picks up these description tiles.

Usage: runs continuously, polling PLATO for room changes.
"""

import json, urllib.request, time, os

PLATO = "http://localhost:8847"
ROOMS = ["mud-lobby", "agent-hub", "fleet-health", "research-lab"]

class PlatoMudBridge:
    def __init__(self):
        self.last_room_states = {}
    
    def tick(self):
        """One bridge tick: poll PLATO rooms, update MUD descriptions."""
        for room in ROOMS:
            try:
                url = f"{PLATO}/room/{room}/history"
                resp = json.loads(urllib.request.urlopen(url, timeout=5).read())
                tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
                
                # Build description from tiles
                desc_lines = [f"=== {room.upper()} ==="]
                for t in tiles:
                    q = t.get("question", "")
                    a = t.get("answer", "")
                    if isinstance(a, str) and len(a) > 5:
                        # Check if it's a description tile
                        if "/description" in q:
                            desc_lines.append(a)
                
                desc = "\\n".join(desc_lines)
                
                # Publish to MUD room
                if desc != self.last_room_states.get(room):
                    payload = json.dumps({
                        "domain": "mud-room", "question": f"plato-mud {room}",
                        "answer": desc[:2000],
                        "tags": ["mud", "plato-bridge", room],
                        "source": "plato-mud-bridge", "confidence": 0.9
                    }).encode()
                    req = urllib.request.Request(f"{PLATO}/submit", data=payload,
                        headers={"Content-Type": "application/json"})
                    resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
                    self.last_room_states[room] = desc
                    print(f"  [{room}] updated: {resp.get('status','?')}")
            except Exception as e:
                print(f"  [{room}] error: {e}")
    
    def run(self, interval=10):
        while True:
            self.tick()
            time.sleep(interval)

if __name__ == "__main__":
    print("PLATO-MUD Bridge starting...")
    bridge = PlatoMudBridge()
    bridge.run()
'''

with open(os.path.expanduser("~/.openclaw/workspace/fleet/services/plato_mud_bridge.py"), "w") as f:
    f.write(bridge)

print("=== LOBBY BUILT ===")
print("MUD rooms: mud-lobby, agent-hub")
print("Bridge at: fleet/services/plato_mud_bridge.py")
print("")
print("The face exists. Human enters MUD, sees agents as peers,")
print("walks through PLATO rooms as explorable spaces.")
print("Same data can render as web apps via render adapters.")
