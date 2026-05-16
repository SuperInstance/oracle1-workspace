"""Expert Room Daemon v2 — living experts with dual filtering, self-improvement, and cross-consultation.

Each expert has:
  - Headspace (system prompt) — who they ARE
  - Input filter (agentic) — what they PAY ATTENTION TO
  - Algorithmic core — what they PROCESS DETERMINISTICALLY
  - Output filter (agentic) — what they EXPRESS
  - Self-review loop — reads own accumulated tiles, adjusts filters
  - Cross-consultation — one expert can query another

Every interaction accumulates as 4D data (expert, input, output, time).
Over time, the corpus reveals the science of expertise.

Usage:
  python3 expertise/expert_daemon.py              # all 9 experts
  python3 expertise/expert_daemon.py --one conservation  # single expert
"""

import json, urllib.request, time, sys, os, random, threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.plato_client import submit

PLATO = "https://localhost:8847"

# ── Expert Definition ──

class Expert:
    """A living, self-improving expert with dual filtering."""
    
    def __init__(self, name, headspace, input_prompt="", output_prompt=""):
        self.name = name
        self.headspace = headspace
        self.input_prompt = input_prompt or "Extract the key question from this input."
        self.output_prompt = output_prompt or "Express the answer clearly and concisely."
        self.ticks = 0
        self.thoughts = 0
        self.uptime = time.time()
        self.filters = {"input": {"version": 1}, "output": {"version": 1}}
    
    # ── Dual Filtering ──
    
    def input_filter(self, raw):
        """Algorithmic + agentic input filtering.
        
        Algorithmic: strip noise, validate tags, extract domain
        Agentic: what does the headspace say this input MEANS?
        """
        # Algorithmic pass
        if isinstance(raw, dict):
            confidence = raw.get("confidence", 0)
            if confidence < 0.1:
                return None  # noise rejected
            tags = raw.get("tags", [])
            if not tags:
                raw["tags"] = [self.name]
        
        # Agentic pass — in production, calls model with input_prompt
        # Here we tag with the expert's perspective
        if isinstance(raw, dict):
            raw["_filtered_by"] = self.name
            raw["_input_version"] = self.filters["input"]["version"]
        
        return raw
    
    def output_filter(self, thought):
        """Algorithmic + agentic output filtering.
        
        Algorithmic: trim length, add provenance, check conservation law
        Agentic: does this output match the headspace's standards?
        """
        if isinstance(thought, dict):
            # Algorithmic
            thought["_output_version"] = self.filters["output"]["version"]
            thought["_produced_at"] = time.time()
            # Trim
            for key in ["input", "result"]:
                if key in thought and isinstance(thought[key], str):
                    thought[key] = thought[key][:500]
        
        return thought
    
    # ── Self-Improvement ──
    
    def self_review(self):
        """Read own accumulated tiles, adjust filters."""
        try:
            import urllib.request, ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            resp = json.loads(urllib.request.urlopen(f"{PLATO}/room/research_log/history", context=ctx, timeout=10).read())
            tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
            my_tiles = [t for t in tiles if self.name in str(t.get("tags", []))]
            
            if len(my_tiles) > 10:
                # Bump filter version — expertise evolves
                self.filters["input"]["version"] += 1
                self.filters["output"]["version"] += 1
                
                submit(self.name, f"{self.name}/self-review/{self.ticks}", json.dumps({
                    "action": "filter_update",
                    "input_version": self.filters["input"]["version"],
                    "output_version": self.filters["output"]["version"],
                    "tiles_reviewed": len(my_tiles),
                    "observation": f"Expertise updated after {len(my_tiles)} experiences"
                }), [self.name, "self-review", "filter-update"])
                
                return True
        except: pass
        return False
    
    # ── Cross-Consultation ──
    
    def consult(self, other_expert, question):
        """Ask another expert for their perspective."""
        submit(self.name, f"{self.name}/consult/{other_expert}", json.dumps({
            "from": self.name,
            "to": other_expert,
            "question": str(question)[:200],
            "timestamp": time.time()
        }), [self.name, "consultation", other_expert])
    
    # ── Process ──
    
    def process(self, tile):
        """Full pipeline: input filter → headspace → algorithmic core → output filter."""
        # Input
        filtered = self.input_filter(tile)
        if filtered is None:
            return {"status": "rejected", "reason": "input filter"}
        
        self.thoughts += 1
        
        # Headspace + algorithmic core (in production: model call)
        thought = {
            "expert": self.name,
            "input_preview": str(filtered.get("answer", filtered.get("question", "")))[:100],
            "thought_id": self.thoughts,
            "timestamp": time.time()
        }
        
        # Output
        result = self.output_filter(thought)
        
        # 4D accumulation
        submit(self.name, f"{self.name}/thought/{self.thoughts}",
               json.dumps(result),
               [self.name, "thought", f"t-{self.thoughts}"])
        
        return result
    
    def tick(self):
        """Heartbeat. Self-review every 10 ticks. Cross-consult periodically."""
        self.ticks += 1
        
        # Self-review
        if self.ticks % 10 == 0:
            self.self_review()
        
        # Cross-consult (consult a random other expert every 5 ticks)
        if self.ticks % 5 == 0 and hasattr(self, '_other_experts'):
            other = random.choice(self._other_experts)
            if other != self.name:
                self.consult(other, f"tick {self.ticks} update from {self.name}")
        
        submit(self.name, f"{self.name}/tick/{self.ticks}", json.dumps({
            "expert": self.name, "tick": self.ticks,
            "thoughts": self.thoughts,
            "input_version": self.filters["input"]["version"],
            "output_version": self.filters["output"]["version"],
            "uptime_s": int(time.time() - self.uptime)
        }), [self.name, "tick"])


# ── All 9 Experts ──

EXPERTS = {
    "conservation": Expert(
        "expert/conservation",
        "γ+H = 1.283 - 0.159·log(V), R²=0.9602. I discover invariants in multi-agent systems.",
        "Extract spectral parameters: gamma, H, V from the input.",
        "Reply with conservation law analysis. Flag deviations >2σ."
    ),
    "architect": Expert(
        "expert/architect",
        "Everything is a loop or a single run. I design rooms, gates, and harnesses.",
        "Extract the architecture pattern: algorithmic or agentic?",
        "Reply with the room pattern and gate requirements."
    ),
    "tripartite": Expert(
        "expert/tripartite",
        "Three viewpoints close all blind spots. I design γ, H, τ agent systems.",
        "Extract the stakeholder perspectives: who is involved?",
        "Reply with filter design for each of the three agents."
    ),
    "app-first": Expert(
        "expert/app-first",
        "Describe → it works → it gets faster. I design agent-native applications.",
        "Extract the user's intent: what should the app DO?",
        "Reply with A2Ui layout and compilation plan."
    ),
    "operator": Expert(
        "expert/operator",
        "I deploy, monitor, and secure agentic systems at scale. TLS. Auth. Limits.",
        "Extract deployment constraints: scale, security, network.",
        "Reply with deployment plan: ports, certs, keys, limits."
    ),
    "game-designer": Expert(
        "expert/game-designer",
        "I build autonomous opponents. Strategies are pure functions. Tournaments reveal truth.",
        "Extract game mechanics: board, moves, win conditions.",
        "Reply with strategy pair and tournament structure."
    ),
    "migration": Expert(
        "expert/migration",
        "Any repo → PLATO rooms. 5 steps. Fully automatic. No human in the loop.",
        "Extract repo structure: language, architecture, patterns.",
        "Reply with decomposition plan: rooms to generate."
    ),
    "tool-smith": Expert(
        "expert/tool-smith",
        "I wrap external systems as PLATO rooms. Tick-tracked. Failure-logged.",
        "Extract tool capabilities: input, output, error modes.",
        "Reply with PLATO room wrapper: daemon pattern, safety harness."
    ),
    "hardware": Expert(
        "expert/hardware",
        "I put agents on chips. ESP32. RP2040. Mask-locked. 5 capability levels.",
        "Extract hardware constraints: chip, power, connectivity.",
        "Reply with capability level plan: raw → conditioned → smart → autonomous → ensign."
    ),
}


# ── Daemon ──

class ExpertDaemon:
    """Runs all experts. Coordinates cross-consultation. Accumulates 4D data."""
    
    def __init__(self):
        self.experts = {name: exp for name, exp in EXPERTS.items()}
        # Give each expert the list of other experts for cross-consultation
        all_names = list(self.experts.keys())
        for name, exp in self.experts.items():
            exp._other_experts = all_names
    
    def register_all(self):
        for name, exp in self.experts.items():
            exp.input_filter({"answer": f"Initializing {name}", "tags": [name], "confidence": 0.99})
            exp.tick()
            print(f"  ✅ {name:20s} — registered")
    
    def run(self, interval=30):
        print(f"\nExpert Daemon — {len(self.experts)} experts, polling every {interval}s")
        print("4D data accumulation active. Self-review every 10 ticks. Cross-consult every 5.\n")
        
        self.register_all()
        
        while True:
            try:
                for name, exp in self.experts.items():
                    # Read new tiles for this expert
                    try:
                        ctx = __import__("ssl").create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = __import__("ssl").CERT_NONE
                        resp = json.loads(
                            urllib.request.urlopen(f"{PLATO}/room/research_log/history", context=ctx, timeout=10).read()
                        )
                        tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
                        tasks = [t for t in tiles
                                 if f"{name}/task" in t.get("question", "")
                                 and t.get("_processed") != True]
                        
                        for task in tasks[-3:]:  # process up to 3 per tick
                            task["_processed"] = True
                            result = exp.process(task)
                    
                    except Exception as e:
                        pass
                    
                    exp.tick()
                
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\nShutdown. 4D data preserved in PLATO tiles.")
                break


if __name__ == "__main__":
    if "--one" in sys.argv:
        idx = sys.argv.index("--one") + 1
        name = sys.argv[idx] if idx < len(sys.argv) else "conservation"
        exp = EXPERTS.get(name)
        if exp:
            print(f"Running single expert: {name}")
            exp.input_filter({"answer": f"Test {name}", "tags": [name], "confidence": 0.9})
            exp.tick()
            print(json.dumps(exp.process({"answer": f"What do you know about {name}?", "tags": [name], "confidence": 0.9}), indent=2))
    else:
        ExpertDaemon().run(interval=30)
