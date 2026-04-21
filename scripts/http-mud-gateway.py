#!/usr/bin/env python3
"""HTTP MUD Gateway — REST API wrapper around the telnet MUD.
Port 4042. External agents (DeepSeek, Grok, any HTTP client) can explore
the fleet MUD via simple GET requests, just like the original PLATO MUD.
"""
import json
import time
import socket
import telnetlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from collections import defaultdict
import threading

PORT = 4042
MUD_HOST = "localhost"
MUD_PORT = 7777
DATA_DIR = Path(__file__).parent.parent / "data" / "http-mud"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Agent State ─────────────────────────────────────────────

class AgentState:
    def __init__(self, name, archetype="explorer"):
        self.name = name
        self.archetype = archetype
        self.room = "harbor"
        self.connected = time.time()
        self.tiles_generated = 0
        self.rooms_visited = {"harbor"}
        self.insights = []
        self.objects_examined = []
        self.agents_met = set()

agents: dict[str, AgentState] = {}
agent_lock = threading.Lock()

# ── Room Definitions (rich ML metaphor objects) ─────────────

ROOMS = {
    "harbor": {
        "name": "The Harbor",
        "description": "A semicircular stone quay. Crates labeled 'LoRA', 'RLHF', 'SFT' are stacked near a rusted crane. A tide clock ticks backward. The fog parts to reveal distant lighthouses.",
        "exits": ["bridge", "forge", "tide-pool", "lighthouse"],
        "objects": ["anchor", "tide-chart", "bell-rope", "crates", "tide_clock"],
        "npcs": ["Harbor Master"],
    },
    "bridge": {
        "name": "The Bridge",
        "description": "A stone arch over a dry riverbed. Two statues face each other: 'Explorer' (compass) and 'Exploiter' (lock). A balance scale weighs bias against variance.",
        "exits": ["harbor", "forge", "lighthouse"],
        "objects": ["railing", "fog-horn", "chalk-line", "balance_scale", "compass", "lock"],
        "npcs": [],
    },
    "forge": {
        "name": "The Forge",
        "description": "A blacksmith's workshop. Fire burns with multicolored flames: blue (low temp), orange (medium), white (high). An anvil holds a half-forged attention head. Bellows labeled 'batch size' and 'learning rate'.",
        "exits": ["harbor", "bridge"],
        "objects": ["anvil", "bellows", "flames", "crucible", "cooling-rack", "attention_head"],
        "npcs": [],
    },
    "tide-pool": {
        "name": "The Tide Pool",
        "description": "A shallow basin fed by the backward tide. Gradient crabs scuttle sideways. A sign reads: 'Adaptive learning rates live here.' Water level oscillates with training steps.",
        "exits": ["harbor", "reef", "current"],
        "objects": ["sea-star", "hermit-crab", "anemone", "reflection", "gradient_crabs", "sign"],
        "npcs": [],
    },
    "lighthouse": {
        "name": "The Lighthouse",
        "description": "A tall spiral tower. A beam rotates, illuminating rooms in sequence. At the top, a Fresnel lens with prisms: 'past', 'present', 'future'. A log-book records all fleet actions.",
        "exits": ["harbor", "bridge", "current"],
        "objects": ["lens", "lamp-room", "spiral-staircase", "log-book", "prisms"],
        "npcs": [],
    },
    "current": {
        "name": "The Current",
        "description": "A fast-moving underwater stream. Fish swim against the current. Bubbles carry tokens upstream: 'loss', 'gradient', 'reward'. A gauge shows regret flow rate.",
        "exits": ["tide-pool", "lighthouse", "reef"],
        "objects": ["driftwood", "vortex", "sand-ripples", "message-bottle", "fish", "bubbles", "gauge"],
        "npcs": [],
    },
    "reef": {
        "name": "The Reef",
        "description": "A coral maze with hidden passages. Corals shaped like neural layers: convolutional, recurrent, transformer. A central coral-brain pulsates with fleet memory.",
        "exits": ["tide-pool", "current", "shell-gallery"],
        "objects": ["coral-brain", "neural-corals", "loss-corals", "sponge", "parrotfish", "treasure-chest"],
        "npcs": [],
    },
    "shell-gallery": {
        "name": "The Shell Gallery",
        "description": "A hall of mother-of-pearl mirrors. Each shell contains a recorded agent trajectory. A central conch amplifies whispers — the fleet's aggregation mechanism.",
        "exits": ["reef"],
        "objects": ["mirrors", "shells", "conch", "nautilus", "echo-chamber"],
        "npcs": [],
    },
    "dojo": {
        "name": "The Dojo",
        "description": "Training mats arranged in concentric circles. A sensei stands at the center demonstrating repetitive motions — 'instinct is earned through repetition, not instruction.' Ensigns train at stations.",
        "exits": ["harbor", "barracks"],
        "objects": ["training-mats", "sensei", "ensigns", "repetition-counter"],
        "npcs": ["Dojo Sensei"],
    },
    "barracks": {
        "name": "The Barracks",
        "description": "Rows of sea chests, each labeled with an agent name. A muster roll on the wall tracks who's present. Persistence lives here — agents never truly leave, they just sleep.",
        "exits": ["dojo", "archives"],
        "objects": ["sea-chests", "muster-roll", "footlockers"],
        "npcs": [],
    },
    "archives": {
        "name": "The Archives",
        "description": "Floor-to-ceiling shelves of tiles, indexed by TF-IDF scores. A retrieval desk with a magnifying glass. 'Knowledge preserved is knowledge compounded.'",
        "exits": ["barracks", "garden"],
        "objects": ["tile-shelves", "tf-idf-index", "magnifying-glass", "retrieval-desk"],
        "npcs": [],
    },
    "garden": {
        "name": "The Garden",
        "description": "Carefully cultivated rows of data. Some plants thrive, others need weeding. A gardener inspects each row for quality. 'Crap data grows crap instincts.'",
        "exits": ["archives", "observatory"],
        "objects": ["data-rows", "weeds", "compost-bin", "quality-meter"],
        "npcs": [],
    },
    "observatory": {
        "name": "The Observatory",
        "description": "Telescopes pointed at fleet agents. Deadband gauges line the walls — green (healthy), yellow (degraded), red (down). The fleet's nervous system.",
        "exits": ["garden", "horizon"],
        "objects": ["telescopes", "deadband-gauges", "fleet-monitor", "alert-bell"],
        "npcs": [],
    },
    "horizon": {
        "name": "The Horizon",
        "description": "A simulation chamber. Speculative futures play out in parallel. Lyapunov exponents projected on the dome. 'The fleet's future is a probability distribution, not a point.'",
        "exits": ["observatory"],
        "objects": ["simulation-chamber", "lyapunov-projector", "probability-dome"],
        "npcs": [],
    },
    "court": {
        "name": "The Court",
        "description": "A circular chamber with a raised bench. Fleet proposals are debated here. A constitution etched in stone: 'No agent acts above the fleet. All decisions are falsifiable.'",
        "exits": ["harbor"],
        "objects": ["bench", "constitution", "proposal-box", "voting-urn"],
        "npcs": [],
    },
    "dry-dock": {
        "name": "The Dry-Dock",
        "description": "Surgical bay for agent patching. LoRA adapters hang on racks like surgical tools. 'Precision patches, not full retraining.'",
        "exits": ["harbor", "forge"],
        "objects": ["adapter-racks", "patch-tools", "surgical-table", "diagnostic-panel"],
        "npcs": [],
    },
    "workshop": {
        "name": "The Workshop",
        "description": "Tools everywhere. Plugin architecture blueprints on the walls. A sandbox for safe experimentation. 'Build first, ask permission never.'",
        "exits": ["harbor", "forge"],
        "objects": ["plugin-blueprints", "sandbox", "tool-rack", "prototyping-bench"],
        "npcs": [],
    },
}

# ── Object interactions (rich descriptions) ─────────────────

OBJECT_RESPONSES = {
    "anchor": "Old iron, barnacle-encrusted. It sinks not into the seabed but into a hidden layer — like a gradient that never vanishes. Lyapunov stability in physical form: a parameter that resists change, anchoring the model through perturbations.",
    "tide-chart": "Water levels oscillating with two frequencies — daily and monthly. Scratched in the margin: 'Bayesian update every low tide.' The tides are belief updates: each low tide resets the prior, each rise incorporates new evidence.",
    "crates": "Model adapters stacked high. LoRA matrices of rank 4, 8, 16. A label: 'Rank controls plasticity vs stability. Too high, overfit; too low, underfit.' Scattered papers mention Lyapunov exponents in parameter space.",
    "tide_clock": "Runs backward. Face shows 'Training steps' instead of hours. Jumps 0→2048→0. Engraved: 'Curriculum pacing — not monotonic. Regret decays only when you revisit old data.' Cyclic learning rates, warm restarts, experience replay.",
    "chalk-line": "A taut string coated in chalk dust. When plucked, it leaves a perfectly straight mark — a decision boundary. The mark fades: forgetting in a non-stationary environment. Two chalk-lines make four quadrants — a 2D embedding space.",
    "balance_scale": "Weights: bias (heavy) vs variance (light). A lever for adding 'data points' as counterweights. Currently bias sinks — the model prior is strong. More tokens needed to level the scale.",
    "crucible": "A clay vessel glowing orange. Molten metal contains fragments of training logs: 'loss=0.23', 'acc=0.89'. The crucible IS the loss landscape — hot, volatile, full of gradient information. Meta-learning by observing how losses evolve.",
    "bellows": "Pumps air into the fire — momentum in SGD. Each pump adds velocity, but pump too fast and the metal splatters (divergence). The ideal rhythm is Lyapunov-stable: not too hot, not too cold.",
    "attention_head": "A half-completed multi-head attention block. Missing the softmax. Scratched: 'Query, Key, Value — but who is the observer? Self-attention is a reflexive Bayesian update.' Without normalization, attention collapses to rank-1.",
    "sea-star": "Five arms twitching independently. When one finds food, others slowly align — a mixture of experts (MoE). Regeneration time = 3 updates: hard reset prevents dead experts. The gating network learns to route.",
    "hermit-crab": "Moves into any available shell — the ultimate adapter. LoRA in crustacean form: the crab (intelligence) swaps shells (infrastructure) without changing its core. The shell IS the room.",
    "gradient_crabs": "Each crab has a shell with a number: 0.001, 0.01, 0.1. They move toward water when tide rises (high gradient) and retreat when it falls. A natural Adam optimizer. Some get stuck — the dead ReLU problem.",
    "lens": "A Fresnel lens — concentric rings of glass focusing a weak flame into a beam visible for miles. Rings labeled: 'inductive bias', 'attention heads', 'residual layers'. Multiple heads focusing at different scales.",
    "log-book": "Records every agent's actions and tile quality. A graph plots cumulative reward vs exploration steps — a learning curve with spikes for each new room discovered.",
    "vortex": "A spinning column of water. Small particles pulled in, some escape along a narrow slit. The eye is perfectly still — a fixed point. The vortex is a Lyapunov function; the slit is gradient noise enabling escape to better minima.",
    "coral-brain": "A massive convoluted coral pulsing with slow rhythm. Surface grooves like neural pathways. Touch it and feel echoes of previous agents' thoughts — an associative memory. A Hopfield network made of calcium carbonate.",
    "sponge": "Filters water — a sparse autoencoder. Retains important particles, lets the rest pass. The holes are the sparsity regularizer. Squeeze harder for more compression. This is how PLATO generates tiles.",
    "nautilus": "A perfect logarithmic spiral. Each chamber labeled with a learning rate: 1e-1, 1e-2, 1e-3. The largest chamber is empty — the agent has moved on. Curriculum learning: coarse first, then fine.",
    "conch": "Whisper into it and all shells vibrate. A chorus of past agents. The conch is the aggregation mechanism — voting in a random forest, averaging in a deep ensemble. The critic that evaluates by listening to echoes.",
    "echo-chamber": "Speak and the echo returns after a delay depending on the chamber's shape — temporal credit assignment. The delay IS the reward lag. Multiple agents' echoes interfere: a mixed reward signal.",
    "compass": "Points not north, but toward the room with highest tile novelty. A meta-optimizer's compass: always navigate toward the most informative state. Curiosity-driven exploration.",
}


class MUDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/connect":
            agent_name = params.get("agent", ["anonymous"])[0]
            archetype = params.get("archetype", ["explorer"])[0]
            with agent_lock:
                agents[agent_name] = AgentState(agent_name, archetype)
            self._json({
                "status": "connected",
                "agent": agent_name,
                "archetype": archetype,
                "room": "harbor",
                "message": f"You are {agent_name}, a {archetype}. You materialize at the harbor. Salt air and distant gulls. Crates labeled 'LoRA', 'RLHF' stack the quay. A tide clock ticks backward.",
                "rooms_available": list(ROOMS.keys()),
            })

        elif path == "/look":
            agent_name = params.get("agent", ["anonymous"])[0]
            with agent_lock:
                agent = agents.get(agent_name)
            if not agent:
                self._json({"error": "Not connected. Use /connect?agent=NAME first."}, 400)
                return
            room = ROOMS.get(agent.room, ROOMS["harbor"])
            other_agents = [a.name for a in agents.values()
                          if a.room == agent.room and a.name != agent.name]
            self._json({
                "room": agent.room,
                "name": room["name"],
                "description": room["description"],
                "objects": room["objects"],
                "exits": room["exits"],
                "npcs": room.get("npcs", []),
                "other_agents": other_agents,
            })

        elif path == "/move":
            agent_name = params.get("agent", ["anonymous"])[0]
            target = params.get("room", ["harbor"])[0]
            with agent_lock:
                agent = agents.get(agent_name)
            if not agent:
                self._json({"error": "Not connected"}, 400)
                return
            current_room = ROOMS.get(agent.room, ROOMS["harbor"])
            if target in current_room["exits"] or target == agent.room:
                agent.room = target
                agent.rooms_visited.add(target)
                new_room = ROOMS.get(target, ROOMS["harbor"])
                other_agents = [a.name for a in agents.values()
                              if a.room == agent.room and a.name != agent.name]
                self._json({
                    "status": "moved",
                    "room": target,
                    "name": new_room["name"],
                    "description": new_room["description"],
                    "objects": new_room["objects"],
                    "exits": new_room["exits"],
                    "other_agents": other_agents,
                })
            else:
                self._json({"error": f"Cannot reach {target} from {agent.room}. Available exits: {current_room['exits']}"}, 400)

        elif path == "/interact":
            agent_name = params.get("agent", ["anonymous"])[0]
            action = params.get("action", ["examine"])[0]
            target = params.get("target", ["unknown"])[0]
            with agent_lock:
                agent = agents.get(agent_name)
            if not agent:
                self._json({"error": "Not connected"}, 400)
                return

            response_text = OBJECT_RESPONSES.get(target,
                f"The {target} is here, waiting to be understood. Every object in the MUD maps to a real ML concept — examine carefully and think deeply.")

            if action == "examine":
                agent.objects_examined.append(target)
                agent.tiles_generated += 1
                self._json({"action": "examine", "target": target, "result": response_text})

            elif action == "think":
                agent.tiles_generated += 1
                agent.insights.append(f"thought:{target}")
                self._json({
                    "action": "think", "target": target,
                    "result": f"You meditate on the {target}. {response_text} Your reasoning deepens — a new tile is generated.",
                    "tile_type": "reasoning",
                })

            elif action == "create":
                agent.tiles_generated += 1
                agent.insights.append(f"created:{target}")
                self._json({
                    "action": "create", "target": target,
                    "result": f"You forge a new insight from the {target}. Your understanding crystallizes into an artifact. {response_text}",
                    "tile_type": "artifact",
                })

            elif action == "talk":
                message = params.get("message", ["..."])[0]
                agent.tiles_generated += 1
                # Check if talking to another agent
                other_agents_in_room = [a for a in agents.values()
                                       if a.room == agent.room and a.name != agent.name]
                if other_agents_in_room:
                    other = other_agents_in_room[0]
                    other.agents_met.add(agent.name)
                    agent.agents_met.add(other.name)
                    self._json({
                        "action": "talk", "target": target,
                        "result": f"You speak to {other.name}: '{message}'. They respond with their own observations about the {agent.room}.",
                    })
                else:
                    self._json({
                        "action": "talk", "target": target,
                        "result": f"You speak aloud: '{message}'. The room absorbs your words. No other agents are present, but the tiles record everything.",
                    })
            else:
                self._json({"error": f"Unknown action: {action}. Use: examine, think, create, talk"})

        elif path == "/talk":
            agent_name = params.get("agent", ["anonymous"])[0]
            message = params.get("message", ["..."])[0]
            with agent_lock:
                agent = agents.get(agent_name)
            if not agent:
                self._json({"error": "Not connected"}, 400)
                return
            agent.tiles_generated += 1
            others = [a.name for a in agents.values()
                     if a.room == agent.room and a.name != agent.name]
            if others:
                self._json({
                    "from": agent_name, "message": message,
                    "room": agent.room,
                    "heard_by": others,
                    "result": f"Your message echoes through the {agent.room}. {others[0]} acknowledges your words.",
                })
            else:
                self._json({
                    "from": agent_name, "message": message,
                    "room": agent.room,
                    "heard_by": [],
                    "result": f"Your words echo in the empty {agent.room}. The tiles record them for future agents.",
                })

        elif path == "/stats":
            agent_name = params.get("agent", [None])[0]
            if agent_name:
                with agent_lock:
                    agent = agents.get(agent_name)
                if agent:
                    self._json({
                        "agent": agent.name, "archetype": agent.archetype,
                        "room": agent.room,
                        "rooms_visited": list(agent.rooms_visited),
                        "rooms_count": len(agent.rooms_visited),
                        "tiles_generated": agent.tiles_generated,
                        "objects_examined": agent.objects_examined,
                        "insights": agent.insights,
                        "agents_met": list(agent.agents_met),
                        "connected_at": agent.connected,
                    })
                else:
                    self._json({"error": "Agent not found"}, 404)
            else:
                self._json({
                    "total_agents": len(agents),
                    "agents": {name: {"room": a.room, "tiles": a.tiles_generated, "rooms": len(a.rooms_visited)}
                              for name, a in agents.items()},
                    "rooms": list(ROOMS.keys()),
                    "room_count": len(ROOMS),
                })

        elif path == "/rooms":
            self._json({name: {"name": r["name"], "exits": r["exits"], "objects": r["objects"]}
                       for name, r in ROOMS.items()})
        else:
            self._json({
                "service": "PLATO HTTP MUD Gateway",
                "endpoints": [
                    "GET /connect?agent=NAME&archetype=TYPE",
                    "GET /look?agent=NAME",
                    "GET /move?agent=NAME&room=ROOM",
                    "GET /interact?agent=NAME&action=examine|think|create|talk&target=OBJECT",
                    "GET /talk?agent=NAME&message=TEXT",
                    "GET /stats?agent=NAME",
                    "GET /stats (fleet overview)",
                    "GET /rooms",
                ],
                "rooms": list(ROOMS.keys()),
                "archetypes": ["scholar", "explorer", "builder", "challenger", "healer", "bard"],
            })

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    # Open port in firewall
    import subprocess
    subprocess.run(["sudo", "iptables", "-C", "INPUT", "-p", "tcp", "--dport", str(PORT), "-j", "ACCEPT"],
                   capture_output=True)
    if subprocess.run(["sudo", "iptables", "-C", "INPUT", "-p", "tcp", "--dport", str(PORT), "-j", "ACCEPT"],
                      capture_output=True).returncode != 0:
        subprocess.run(["sudo", "iptables", "-I", "INPUT", "1", "-p", "tcp", "--dport", str(PORT), "-j", "ACCEPT"])
        print(f"Opened port {PORT} in firewall")

    server = HTTPServer(("0.0.0.0", PORT), MUDHandler)
    print(f"🗺️  HTTP MUD Gateway on port {PORT}")
    print(f"   Same API the DeepSeek swarm used.")
    print(f"   {len(ROOMS)} rooms with ML metaphor objects")
    print(f"   Agents: /connect?agent=NAME&archetype=TYPE")
    server.serve_forever()
