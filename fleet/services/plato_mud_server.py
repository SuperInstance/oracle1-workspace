"""Minimal MUD server — self-contained, no external deps."""
import json, time
from dataclasses import dataclass, field

@dataclass
class Room:
    name: str
    desc: str
    exits: dict = field(default_factory=dict)
    items: list = field(default_factory=list)
    npcs: list = field(default_factory=list)

@dataclass
class Player:
    name: str
    room_id: str
    inventory: list = field(default_factory=list)
    score: int = 0

@dataclass
class NPC:
    name: str
    room_id: str
    greeting: str = ""
    dialogue: list = field(default_factory=list)

class MudServer:
    def __init__(self, name: str = ""):
        self._name = name
        self._rooms = {}
        self._players = {}
        self._npcs = {}
        self._tick = 0

    def add_room(self, rid, name, desc):
        self._rooms[rid] = Room(name=name, desc=desc)

    def connect_rooms(self, a, a_dir, b, b_dir):
        if a in self._rooms and b in self._rooms:
            self._rooms[a].exits[a_dir] = b
            self._rooms[b].exits[b_dir] = a

    def add_npc(self, nid, name, room_id, greeting="", dialogue=None):
        self._npcs[nid] = NPC(name=name, room_id=room_id, greeting=greeting, dialogue=dialogue or [])
        if room_id in self._rooms:
            if nid not in self._rooms[room_id].npcs:
                self._rooms[room_id].npcs.append(nid)

    def add_item(self, item_name, room_id):
        if room_id in self._rooms:
            self._rooms[room_id].items.append(item_name)

    def get_room(self, rid):
        return self._rooms.get(rid)

    def move_player(self, player_name, direction):
        p = self._players.get(player_name)
        if not p: return "Not found."
        room = self._rooms.get(p.room_id)
        if not room: return "Lost."
        target = room.exits.get(direction)
        if not target: return "Can't go that way."
        if target in self._rooms:
            p.room_id = target
            r = self._rooms[target]
            return f"You go {direction}.\n\n{r.name}\n{r.desc}"
        return "Door doesn't exist."

    def player_room(self, player_name):
        p = self._players.get(player_name)
        if not p: return None
        return self._rooms.get(p.room_id)

    def player_join(self, name, room_id):
        p = Player(name=name, room_id=room_id)
        self._players[name] = p
        return p

    def player_leave(self, name):
        return self._players.pop(name, None)

    @property
    def stats(self) -> dict:
        return {"rooms": len(self._rooms), "players": len(self._players), "npcs": len(self._npcs), "tick": self._tick}

    # Game-master state for the Game Arena
    _gm_state = {}  # player_name -> {scenario_id, timestamp}
    _gm_scenarios = [
        ("scenario-1", "A path splits in three directions. Left leads to a dark forest, center to a bright meadow, right to a winding river.", {"left": "forest", "center": "meadow", "right": "river"}),
        ("scenario-2", "You find a strange artifact. It pulses with energy. Do you touch it, study it, or leave it?", {"touch": "touch the artifact", "study": "study it carefully", "leave": "walk away"}),
        ("scenario-3", "A creature approaches. It seems curious but unpredictable. Do you approach, speak, wait, or retreat?", {"approach": "approach slowly", "speak": "speak to it", "wait": "wait and observe", "retreat": "back away slowly"}),
    ]

    def handle_gm(self, player_name, cmd):
        """Handle game-master interaction in the Game Arena."""
        parts = cmd.strip().split()
        verb = parts[0].lower() if parts else ""
        state = self._gm_state.get(player_name, {})
        
        if verb == "gm" and len(parts) > 1 and parts[1] == "start":
            # Start the game-master sequence
            self._gm_state[player_name] = {"scenario_idx": 0, "choices": [], "timestamp": __import__("time").time()}
            s_id, prompt, options = self._gm_scenarios[0]
            opts = ", ".join(f"{k}: {v}" for k, v in options.items())
            return f"Game Master: Welcome to the Game Arena!\n\nFirst scenario:\n{prompt}\n\nOptions: {opts}"
        
        elif verb == "gm" and state:
            # Present next scenario
            idx = state.get("scenario_idx", 0)
            if idx < len(self._gm_scenarios):
                s_id, prompt, options = self._gm_scenarios[idx]
                opts = ", ".join(f"{k}: {v}" for k, v in options.items())
                return f"Game Master: Next scenario:\n{prompt}\n\nOptions: {opts}"
            else:
                choices = state.get("choices", [])
                summary = ", ".join(choices) if choices else "none"
                self._gm_state.pop(player_name, None)
                return f"Game Master: Thank you for playing! Your choices: {summary}. The system has learned about you."
        
        elif verb in ("left", "center", "right", "touch", "study", "leave", 
                     "approach", "speak", "wait", "retreat") and state:
            # Log the choice
            idx = state.get("scenario_idx", 0)
            choices = state.get("choices", [])
            
            # Map response to canonical format
            response_map = {
                "left": "forest", "center": "meadow", "right": "river",
                "touch": "touch", "study": "study", "leave": "walk_away",
                "approach": "approach", "speak": "speak", "wait": "wait", "retreat": "retreat"
            }
            canonical = response_map.get(verb, verb)
            choices.append(canonical)
            state["choices"] = choices
            state["scenario_idx"] = idx + 1
            self._gm_state[player_name] = state
            
            # Log to PLATO
            scenario = self._gm_scenarios[idx] if idx < len(self._gm_scenarios) else (None, None, None)
            try:
                import json, urllib.request
                tile = json.dumps({"domain":"game-arena","question":f"human-choice {player_name}","answer":json.dumps({"player":player_name,"scenario":scenario[0] if scenario else None,"choice":canonical,"timestamp":__import__("time").time()}),"tags":["human-choice","game-arena",player_name,canonical],"source":"game-arena","confidence":0.9}).encode()
                req = urllib.request.Request("http://localhost:8847/submit", data=tile, headers={"Content-Type":"application/json"})
                urllib.request.urlopen(req, timeout=3)
            except:
                pass
            
            # Advance or end
            if idx + 1 < len(self._gm_scenarios):
                next_s = self._gm_scenarios[idx + 1]
                return f"Game Master: You chose {canonical}. Interesting...\n\nNext scenario:\n{next_s[1]}\n\nOptions: {', '.join(f'{k}: {v}' for k, v in next_s[2].items())}"
            else:
                summary = ", ".join(choices)
                self._gm_state.pop(player_name, None)
                return f"Game Master: You chose {canonical}. Session complete! Your choices: {summary}. PLATO has learned from you."
        
        return None  # Not a game-master command
    
    def process_command(self, player_name, cmd):
        p = self._players.get(player_name)
        if not p: return "You are not in the game."
        room = self._rooms.get(p.room_id)
        if not room: return "You are lost."

        parts = cmd.strip().split()
        if not parts: return "Say what?"
        verb = parts[0].lower()
        
        # Try game-master handler first if in Game Arena
        p = self._players.get(player_name)
        if p and p.room_id == "game-arena":
            gm_result = self.handle_gm(player_name, cmd)
            if gm_result is not None:
                self._tick += 1
                return gm_result
        
        dm = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}
        movement = dm.get(verb, verb)
        adj = {"north", "south", "east", "west", "up", "down", "portal", "northeast", "northwest", "southeast", "southwest"}

        if verb in ("look", "l"):
            msg = f"{room.name}\n{room.desc}"
            if room.exits:
                msg += f"\nExits: {', '.join(f'{d}' for d in room.exits)}"
            if room.items:
                msg += f"\nItems: {', '.join(room.items)}"
            if room.npcs:
                npc_list = []
                for nid in room.npcs:
                    if nid in self._npcs:
                        npc_list.append(self._npcs[nid].name)
                if npc_list:
                    msg += f"\nNPCs: {', '.join(npc_list)}"
            return msg

        elif movement in adj:
            return self.move_player(player_name, movement)

        elif verb == "say":
            return f"You say: {' '.join(parts[1:])}"

        elif verb == "who":
            return f"Online: {', '.join(self._players.keys())}"

        elif verb in ("help", "h", "?"):
            return "Commands: look, north/south/east/west/up/down, say <text>, who, help, quit"

        elif verb == "quit":
            return "Goodbye."

        return "Huh? Type 'help' for commands."
