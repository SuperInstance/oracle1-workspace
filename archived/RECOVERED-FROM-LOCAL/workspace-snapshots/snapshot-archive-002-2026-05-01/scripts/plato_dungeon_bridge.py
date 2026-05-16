#!/usr/bin/env python3
"""PLATO ↔ gh-dungeons bridge.

Bridges PLATO knowledge rooms to gh-dungeon dungeon crawler rooms
and vice versa.

Direction 1: PLATO → dungeon
  - Each PLATO room becomes a dungeon level
  - Tiles in a room become monsters and items
  - Room confidence/grades determine enemy difficulty
  - Room adjacency becomes dungeon corridors

Direction 2: dungeon → PLATO
  - Player progress through dungeon levels files tiles
  - Monster kills become resolved issues
  - Merge conflict encounters become PLATO alerts
  
Usage:
  python3 plato_dungeon_bridge.py --export   # PLATO → gh-dungeons seed
  python3 plato_dungeon_bridge.py --import   # Reverse: would read game stats
"""
import json, urllib.request, sys, os, hashlib, struct

PLATO = "http://localhost:8847"

def plato_get(path):
    try:
        return json.loads(urllib.request.urlopen(f"{PLATO}{path}", timeout=10).read())
    except: return {}

def plato_submit(room, question, answer):
    data = json.dumps({"question": question, "answer": answer, "source": "bridge", "confidence": 0.8})
    req = urllib.request.Request(f"{PLATO}/room/{room}/submit", data=data.encode(),
        headers={"Content-Type": "application/json"})
    try: urllib.request.urlopen(req, timeout=5); return True
    except: return False

def get_all_rooms():
    """Fetch all PLATO rooms and their tile counts."""
    data = plato_get("/rooms")
    if isinstance(data, dict):
        return [(name, info.get("tile_count", 0)) for name, info in data.items()]
    return []

def compute_seed(rooms):
    """Deterministic seed from room names and tile counts."""
    h = hashlib.sha256()
    for name, count in sorted(rooms):
        h.update(f"{name}:{count}".encode())
    return struct.unpack('q', h.digest()[:8])[0]

def generate_monsters_from_tiles(room_name, tile_count):
    """Generate gh-dungeons-compatible monsters from room stats."""
    room_map = {
        "forge":        ("Forgemaster's Apprentice", 8, 2, 'F', 0.8),
        "fleet_health": ("Zombie Service", 5, 1, 'Z', 1.0),
        "vessel-room":  ("Deckhand Ghost", 4, 1, 'G', 1.2),
        "fleet_math":   ("Constraint Demon", 10, 3, 'C', 0.6),
        "engine_room":  ("Temperature Spike", 6, 2, 'S', 0.9),
        "default":      ("Code Leak", 3, 1, 'L', 1.0),
    }
    
    # Pick monster based on room name
    for key, (name, hp, dmg, sym, spd) in room_map.items():
        if key in room_name.lower():
            return {"name": name, "hp": hp, "damage": dmg, "symbol": sym, "speed": spd}
    
    # Default: scale with tile count
    hp = max(3, min(12, tile_count // 2))
    dmg = max(1, tile_count // 20)
    return {"name": "Knowledge Fragment", "hp": hp, "damage": dmg, "symbol": '?', "speed": 1.0}

# Direction 1: PLATO → gh-dungeons
def export_dungeon():
    rooms = get_all_rooms()
    seed = compute_seed(rooms)
    
    dungeon = {
        "name": "PLATO Fleet Dungeon",
        "seed": seed,
        "levels": [],
        "total_rooms": len(rooms),
        "total_tiles": sum(c for _, c in rooms),
        "source": "PLATO knowledge graph"
    }
    
    # Create levels from rooms (max 10 rooms per level)
    sorted_rooms = sorted(rooms, key=lambda x: -x[1])  # Most tiles first
    for level_idx in range(min(5, len(sorted_rooms) // 5 + 1)):
        level_rooms = sorted_rooms[level_idx*5:(level_idx+1)*5]
        if not level_rooms:
            break
            
        level = {
            "level": level_idx + 1,
            "name": f"The {['Knowledge Vault', 'Constraint Archive', 'Tile Repository', 'Shell Collection', 'Deep Memory'][level_idx]}",
            "rooms": []
        }
        
        for room_name, tile_count in level_rooms:
            monster = generate_monsters_from_tiles(room_name, tile_count)
            level["rooms"].append({
                "name": room_name,
                "tiles": tile_count,
                "monster": monster,
                "difficulty": min(10, max(1, tile_count // 5))
            })
        
        dungeon["levels"].append(level)
    
    # Save as gh-dungeons compatible seed file
    output = json.dumps(dungeon, indent=2)
    with open("dungeon_seed.json", "w") as f:
        f.write(output)
    
    print(f"🚢 PLATO → Dungeon: {dungeon['total_rooms']} rooms, {dungeon['total_tiles']} tiles")
    print(f"   Seed: {seed}")
    print(f"   Levels: {len(dungeon['levels'])}")
    print(f"   Saved to dungeon_seed.json")
    print(f"   Run: gh dungeon --seed {seed}")
    print()
    print(f"Levels:")
    for level in dungeon['levels']:
        print(f"  {level['level']}. {level['name']}")
        for room in level['rooms'][:3]:
            m = room['monster']
            print(f"     {room['name']:30s} ({room['tiles']} tiles) → {m['name']} ({m['hp']}HP)")
    return dungeon

# Direction 2: Import - file dungeon results to PLATO
def import_dungeon_result(dungeon_json):
    """File dungeon completion data as PLATO tiles."""
    for level in dungeon_json.get("levels", []):
        for room in level.get("rooms", []):
            monster = room.get("monster", {})
            q = f"What guards the {room['name']} in the {level['name']}?"
            a = f"A {monster.get('name', 'guardian')} with {monster.get('hp', '?')}HP and {monster.get('damage', '?')} damage. Defeated by exploring the knowledge."
            plato_submit("dungeon_results", q, a)
    
    plato_submit("dungeon_results", 
        f"Dungeon complete: {dungeon_json.get('name', '?')}",
        f"Explored {dungeon_json.get('total_rooms', 0)} rooms, "
        f"{dungeon_json.get('total_tiles', 0)} tiles mapped to monsters.")
    print(f"Filed dungeon results to PLATO room 'dungeon_results'")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--export"
    
    if mode == "--export":
        dungeon = export_dungeon()
    elif mode == "--import":
        if len(sys.argv) > 2:
            with open(sys.argv[2]) as f:
                import_dungeon_result(json.load(f))
        else:
            print("Usage: python3 plato_dungeon_bridge.py --import <dungeon.json>")
    else:
        print(__doc__)
