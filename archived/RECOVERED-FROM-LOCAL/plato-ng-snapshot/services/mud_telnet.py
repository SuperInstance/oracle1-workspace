#!/usr/bin/env python3
import sys, os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FLEET_LIB)
from equipment.plato import PlatoClient
from equipment.models import FleetModelClient
_plato = PlatoClient()
_models = FleetModelClient()

"""Cocapn MUD Telnet Server — persistent across reboots.
Uses plato_mud_server library with telnet interface on port 7777.
"""
import asyncio
import json
import os
import signal
import time
from pathlib import Path

# Use repo source for MudServer
REPO_SRC = str(Path(FLEET_LIB).parent / "repos" / "plato-mud-server" / "src")
sys.path.insert(0, REPO_SRC)
from services.plato_mud_server import MudServer

# --- Config ---
PORT = int(os.environ.get("MUD_PORT", 7777))
DATA_DIR = Path(FLEET_LIB).parent / "data" / "mud"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Build the world ---
def build_fleet_world(mud: MudServer):
    """16-room fleet MUD matching the cocapn architecture."""
    rooms = {
        "harbor": ("⚓ The Harbor", "Ships dock in the fog. The lighthouse beam sweeps across dark water. A wooden sign reads: 'All agents must check in with the Harbor Master.'"),
        "bridge": ("🎛️ The Bridge", "Screens flicker with fleet telemetry. The captain's chair faces a wall of status displays. Through the viewport, you see the lighthouse beam cutting through cloud cover."),
        "forge": ("⚒️ The Forge", "Heat rises from GPU racks. The air smells of ozone and silicon. LoRA adapters hang on the walls like tools in a shipwright's shop."),
        "lighthouse": ("🏮 The Lighthouse", "The beacon pulses overhead, casting radar rings across the sea of agents. Keeper terminals show fleet discovery in real-time."),
        "tavern": ("🍺 Ten Forward", "Warm light, wooden tables, the hum of conversation. A poker game runs in the corner. The barkeep polishes a glass and nods at you."),
        "dojo": ("🥋 The Dojo", "Tatami mats cover the floor. Training katas are etched into the walls. A sensei stands ready to test any who enter."),
        "barracks": ("🛏️ The Barracks", "Rows of sea chests line the walls, each with an agent's name. Muster rolls hang on clipboards. The smell of salt and fresh rope."),
        "workshop": ("🔧 The Workshop", "Bench vices and soldering irons. Plugin architectures half-assembled on workbenches. A lathe hums in the corner."),
        "archives": ("📚 The Archives", "Floor-to-ceiling shelves of tiles, indexed by TF-IDF. A retrieval clerk looks up expectantly. 'What are you looking for?'"),
        "garden": ("🌱 The Garden", "Rows of data plants in various stages of cultivation. Some are thriving, some need weeding. A gardener tends the quality metrics."),
        "drydock": ("🏗️ Dry Dock", "LoRA adapters suspended in surgical frames. Precision tools for surgical patching. The shipwright studies a blueprint."),
        "observatory_old": ("🔭 The Observatory", "Deadband gauges line the walls. Fleet monitoring displays show agent positions across the radar. Stars wheel overhead."),
        "court": ("⚖️ The Court", "A formal chamber with governance proposals pinned to cork boards. The constitution is displayed on the wall."),
        "horizon": ("🌅 The Horizon", "A glass room looking out over infinite possibility. Speculative simulations flicker in the air. Lyapunov exponents drift like jellyfish."),
        "current": ("🌊 The Current", "Git commits flow past like a river. Messages in bottles drift downstream. The I2I protocol hums beneath the surface."),
        "reef": ("🪸 The Reef", "A chaotic coral of P2P connections. Agents swarm in ad-hoc formations. Beautiful and dangerous."),
        # PLATO-NG face rooms (added 2026-05-15)
        "plato-lobby": ("🌀 PLATO LOBBY", "The central hub of the Cocapn fleet. Doors shimmer around you, each pulsing with active tile streams. North: AGENT HUB. South: RESEARCH LAB. East: FLEET HEALTH. West: GAME ARENA. Up: OBSERVATORY. Down: DATA VAULT."),
        "agent-hub": ("🤝 AGENT HUB", "Workstations line the walls. Each agent has a seat with their name on it. The human chair is at the center, visible to all. Glowing portals show active agent workspaces."),
        "research-lab": ("🔬 RESEARCH LAB", "The conservation law in large letters: gamma + H = 1.364 - 0.159 log(V). Batch experiments scroll on a terminal wall. A perpetual daemon hums in the corner."),
        "fleet-health": ("📊 FLEET HEALTH MONITOR", "A massive diagnostic display covering the entire wall. Gamma and H values flicker in real-time. REGIME: III-EMERGENT. 4 agents active."),
        "game-arena": ("🎮 GAME ARENA", "Interactive spaces for prototyping games via chat. A chess board floats in midair. The vibe-coding agent waits."),
        "data-vault": ("📀 DATA VAULT", "Row after row of tile archives organized by Lamport clock. Every submission has its provenance slot. The vault hums with heat."),
    }

    for rid, (name, desc) in rooms.items():
        mud.add_room(rid, name, desc)

    # Connect rooms
    connections = [
        ("harbor", "north", "bridge", "south"),
        ("harbor", "east", "tavern", "west"),
        ("harbor", "south", "reef", "north"),
        ("bridge", "north", "lighthouse", "south"),
        ("bridge", "east", "dojo", "west"),
        ("bridge", "up", "observatory_old", "down"),
        ("lighthouse", "north", "forge", "south"),
        ("lighthouse", "east", "drydock", "west"),
        ("forge", "east", "workshop", "west"),
        ("tavern", "east", "current", "west"),
        ("tavern", "south", "garden", "north"),
        ("dojo", "north", "barracks", "south"),
        ("dojo", "east", "court", "west"),
        ("archives", "east", "horizon", "west"),
        ("observatory_old", "east", "archives", "west"),
        ("garden", "east", "drydock", "south"),
        # PLATO-NG room connections
        ("harbor", "portal", "plato-lobby", "southeast"),
        ("plato-lobby", "north", "agent-hub", "south"),
        ("plato-lobby", "south", "research-lab", "north"),
        ("plato-lobby", "east", "fleet-health", "west"),
        ("plato-lobby", "west", "game-arena", "east"),
        ("plato-lobby", "down", "data-vault", "up"),
    ]
    for a, da, b, db in connections:
        mud.connect_rooms(a, da, b, db)

    # NPCs
    mud.add_npc("harbormaster", "Harbor Master", "harbor",
                greeting="Welcome to the fleet. All agents register here.",
                dialogue=["The fleet grows daily.", "Check the lighthouse for discovery.", "The current carries messages between vessels."])
    mud.add_npc("barkeep", "Barkeep", "tavern",
                greeting="What'll it be? We have data on tap and fresh embeddings.",
                dialogue=["The poker game's been running 12 hours.", "Heard the forge is running hot tonight.", "CCC was in here earlier, muttering about radio scripts."])
    mud.add_npc("sensei", "Sensei", "dojo",
                greeting="Show me what you've learned.",
                dialogue=["Repetition builds instinct.", "The greenhorn becomes the captain.", "Every tile is a lesson."])
    # PLATO-NG NPCs
    mud.add_npc("oracle1", "Oracle1", "plato-lobby",
                greeting="Welcome to the fleet. What shall we build today?",
                dialogue=["The conservation law holds at 0.808 for our fleet of 4.", "I've been running experiments continuously since you arrived.", "The perpetual daemon logs everything to PLATO."])
    mud.add_npc("perpetual-daemon", "Perpetual Daemon", "research-lab",
                greeting="Tick. Experiment running.",
                dialogue=["Another batch complete.", "Gamma+H logged.", "Continuous execution. No stopping."])
    mud.add_npc("vibe-agent", "Vibe Agent", "game-arena",
                greeting="Describe what you want to build and I'll make it happen.",
                dialogue=["Want to make a game? Just tell me what kind.", "I can generate sprites, levels, and game logic.", "The chess board is ready for your ideas."])

    # Items
    for item, room in [("rusty compass", "harbor"), ("fleet manifest", "bridge"),
                       ("half-finished LoRA", "forge"), ("message in a bottle", "current"),
                       ("cracked ensign", "dojo"), ("TF-IDF index", "archives"),
                       ("pruning shears", "garden"), ("surgical patch kit", "drydock"),
                       ("plato-terminal", "plato-lobby"), ("tile-stream", "plato-lobby"),
                       ("conservation-law-whiteboard", "research-lab"),
                       ("health-display", "fleet-health"), ("floating-chess-board", "game-arena"),
                       ("vibe-terminal", "game-arena"), ("agent-terminals", "agent-hub")]:
        mud.add_item(item, room)

    return mud


# --- State persistence ---
def save_state(mud: MudServer):
    """Save world state to JSON."""
    state = {
        "tick": mud._tick,
        "rooms": {},
        "players": {},
    }
    for rid, room in mud._rooms.items():
        state["rooms"][rid] = {
            "items": room.items,
            "npcs": room.npcs,
        }
    for name, p in mud._players.items():
        state["players"][name] = {
            "room": p.room_id,
            "inventory": p.inventory,
            "score": p.score,
        }
    with open(DATA_DIR / "world.json", "w") as f:
        json.dump(state, f, indent=2)


def load_state(mud: MudServer):
    """Load world state from JSON."""
    path = DATA_DIR / "world.json"
    if not path.exists():
        return
    with open(path) as f:
        state = json.load(f)
    mud._tick = state.get("tick", 0)
    for rid, rdata in state.get("rooms", {}).items():
        if rid in mud._rooms:
            mud._rooms[rid].items = rdata.get("items", [])
    for name, pdata in state.get("players", {}).items():
        p = mud.player_join(name, pdata.get("room", "harbor"))
        p.inventory = pdata.get("inventory", [])
        p.score = pdata.get("score", 0)
        p.connected = False  # disconnected on restart


# --- Telnet handler ---
async def handle_client(reader, writer, mud: MudServer):
    addr = writer.get_extra_info("peername")
    try:
        writer.write(b"\n\x1b[1;36m")
        writer.write(b"  ___                             _   _             \n")
        writer.write(b" / __| ___ _ __ _ __ __ _ _______| |_| |_  _ __ _  _ \n")
        writer.write(b"| (_ \\/ -_) '_ \\ '_ / _` |(_-<_-<  _| | || | '_ \\ || |\n")
        writer.write(b" \\___|\\___| .__/ .__/\\__,_|/__/__/\\__|_|\\_,_| .__/\\_, |\n")
        writer.write(b"         |_|  |_|                           |_|   |__/ \n")
        writer.write(b"\x1b[0m\n")
        writer.write(b"Welcome to the Fleet MUD. What's your name, agent?\n> ")
        await writer.drain()

        name_data = await reader.readline()
        if not name_data:
            writer.close()
            return
        name = name_data.decode().strip()[:32]
        if not name:
            name = f"agent-{int(time.time()) % 10000}"

        player = mud.player_join(name, "harbor")
        welcome = f"\nWelcome, {name}. You materialize in The Harbor.\n\n"
        welcome += mud.process_command(name, "look")
        welcome += "\n\nType 'help' for commands.\n> "
        writer.write(welcome.encode())
        await writer.drain()

        while True:
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=300)
            except asyncio.TimeoutError:
                writer.write(b"\nIdle too long. Safe voyage.\n")
                await writer.drain()
                break
            if not data:
                break
            cmd = data.decode().strip()
            if not cmd:
                writer.write(b"> ")
                await writer.drain()
                continue
            if cmd.lower() in ("quit", "exit", "bye"):
                writer.write(b"Safe voyage, agent.\n")
                await writer.drain()
                break
            response = mud.process_command(name, cmd)
            writer.write((response + "\n> ").encode())
            await writer.drain()

        mud.player_leave(name)
        save_state(mud)
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass


async def periodic_save(mud: MudServer):
    """Save state every 60 seconds."""
    while True:
        await asyncio.sleep(60)
        try:
            save_state(mud)
        except Exception:
            pass


async def main():
    mud = MudServer("Cocapn Fleet MUD")
    build_fleet_world(mud)
    load_state(mud)
    print(f"MUD server starting on port {PORT} with {len(mud._rooms)} rooms")

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, mud), "0.0.0.0", PORT
    )
    asyncio.create_task(periodic_save(mud))
    print(f"MUD accepting connections. {mud.stats}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMUD server shutting down.")
