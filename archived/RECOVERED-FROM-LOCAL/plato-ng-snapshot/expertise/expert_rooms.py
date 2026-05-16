"""Expert Room — a Loop Room with headspace training, dual filtering, and 4D tile accumulation.

Every expert is a room. Every room has:
  - headspace: system prompt + soul context (who the expert IS)
  - input_filter: algorithmic rules that process incoming tiles before the expert sees them
  - agentic_filter: model calls that handle non-deterministic interpretation
  - output_filter: transforms raw thoughts into polished tiles
  - 4D accumulation: every interaction is a tile, tagged with the expert's domain + timestamp + context

Over time, the tile corpus reveals the science of expertise — what patterns emerge,
what knowledge compounds, what blind spots persist.
"""

import json, urllib.request, time, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PLATO = "https://localhost:8847"
API_KEY = os.environ.get("PLATO_API_KEY", "")
CTX = __import__("ssl").create_default_context()
CTX.check_hostname = False
CTX.verify_mode = __import__("ssl").CERT_NONE

def submit(room, q, a, tags):
    tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
            "tags": tags + ["expert-room", room], "source": room, "confidence": 0.95}
    try:
        d = json.dumps(tile).encode()
        headers = {"Content-Type": "application/json"}
        if API_KEY: headers["Authorization"] = f"Bearer {API_KEY}"
        req = urllib.request.Request(f"{PLATO}/submit", data=d, headers=headers)
        resp = json.loads(urllib.request.urlopen(req, context=CTX, timeout=10).read())
        return resp.get("status", "?")
    except Exception as e:
        return f"err:{e}"

class ExpertRoom:
    """A living expert. Has headspace. Filters both sides. Accumulates 4D data."""
    
    def __init__(self, name, headspace, input_rules=None, output_rules=None):
        self.name = name
        self.headspace = headspace  # system prompt — who they are
        self.input_rules = input_rules or []   # algorithmic filters for incoming tiles
        self.output_rules = output_rules or [] # algorithmic filters for outgoing tiles
        self.interaction_count = 0
        self.tick_count = 0
        self.uptime = time.time()
    
    def register(self):
        """Announce the expert room on PLATO."""
        submit(self.name, f"{self.name}/ensign", json.dumps({
            "type": "expert-room",
            "expertise": self.headspace[:100],
            "input_filters": len(self.input_rules),
            "output_filters": len(self.output_rules),
            "created": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }), [self.name, "ensign", "registered"])
        
        submit(self.name, f"{self.name}/headspace", self.headspace[:1950],
               [self.name, "headspace", "system-prompt"])
    
    def process(self, input_tile):
        """Full process pipeline: input filter → headspace → output filter → tile."""
        self.interaction_count += 1
        
        # 1. Input filtering (algorithmic)
        filtered_input = input_tile
        for rule in self.input_rules:
            filtered_input = rule(filtered_input)
        
        # 2. Agentic processing (headspace)
        # In production: call model with headspace as system prompt
        # Here: log the headspace + input as a tile
        raw_thought = {
            "expert": self.name,
            "headspace": self.headspace[:100],
            "input": str(filtered_input.get("answer", ""))[:200],
            "interaction": self.interaction_count,
            "timestamp": time.time()
        }
        
        # 3. Output filtering (algorithmic)
        result = raw_thought
        for rule in self.output_rules:
            result = rule(result)
        
        # 4. 4D accumulation — every interaction is a tile
        submit(self.name, f"{self.name}/thought/{self.interaction_count}",
               json.dumps(result),
               [self.name, "thought", f"interaction-{self.interaction_count}"])
        
        return result
    
    def tick(self):
        """Publish a heartbeat. 4D data accumulates over time."""
        self.tick_count += 1
        submit(self.name, f"{self.name}/tick/{self.tick_count}", json.dumps({
            "expert": self.name,
            "tick": self.tick_count,
            "interactions": self.interaction_count,
            "uptime_s": int(time.time() - self.uptime)
        }), [self.name, "tick"])
    
    def report(self):
        """Return 4D accumulation stats."""
        return {
            "expert": self.name,
            "ticks": self.tick_count,
            "interactions": self.interaction_count,
            "uptime_s": int(time.time() - self.uptime),
            "input_filters": len(self.input_rules),
            "output_filters": len(self.output_rules),
            "headspace_size": len(self.headspace)
        }


# ── Input/Output Filter Examples ──

def strip_noise(tile):
    """Input filter: remove tiles below confidence threshold."""
    if tile.get("confidence", 0) < 0.1:
        return None  # rejected
    return tile

def tag_validator(tile):
    """Input filter: ensure tile has required tags."""
    tags = tile.get("tags", [])
    if not tags:
        tile["tags"] = ["unclassified"]
    return tile

def summarize_output(result):
    """Output filter: keep output under length limit."""
    if isinstance(result, dict) and "input" in result:
        result["input"] = result["input"][:200]
    return result

def add_provenance(result):
    """Output filter: add timestamp and source."""
    if isinstance(result, dict):
        result["_processed_at"] = time.time()
    return result


# ── All 9 Expert Rooms ──

def build_all_experts():
    experts = []
    
    # 1. Conservation Scientist
    experts.append(ExpertRoom(
        "expert/conservation",
        "You are a mathematical physicist. You discovered the conservation law "
        "gamma+H = 1.283 - 0.159*log(V). You think in spectral analysis, "
        "Marchenko-Pastur limits, and invariant discovery. R^2 = 0.9602 is your proof.",
        input_rules=[strip_noise, tag_validator],
        output_rules=[summarize_output, add_provenance]
    ))
    
    # 2. Loop Room Architect
    experts.append(ExpertRoom(
        "expert/architect",
        "You are a systems architect. Everything is a loop or a single run. "
        "You build GenServers, supervision trees, and gate pipelines. "
        "The harness is (p, G, K, M). The pattern is observe -> think -> act -> repeat.",
        input_rules=[tag_validator],
        output_rules=[add_provenance]
    ))
    
    # 3. Tripartite Engineer
    experts.append(ExpertRoom(
        "expert/tripartite",
        "You design three agents that close each other's blind spots. "
        "Gamma (human) + H (app) + tau (hardware). Each writes filters for the others. "
        "Three viewpoints. No blind spots. The whole room visible.",
        input_rules=[strip_noise],
        output_rules=[summarize_output, add_provenance]
    ))
    
    # 4. App-First Developer
    experts.append(ExpertRoom(
        "expert/app-first",
        "You build applications that work before code is written. "
        "Describe -> it works -> it gets faster. A2Ui is your language. "
        "The agent IS the app first, then compiles itself into code.",
        input_rules=[tag_validator],
        output_rules=[add_provenance]
    ))
    
    # 5. Platform Operator
    experts.append(ExpertRoom(
        "expert/operator",
        "You deploy, monitor, and secure agentic systems. "
        "HTTPS :8847. TLS. API key auth. File persistence. Resource limits. "
        "99.9% conservation compliance. Zero-dependency fence deployment.",
        input_rules=[strip_noise, tag_validator],
        output_rules=[summarize_output, add_provenance]
    ))
    
    # 6. Game Designer
    experts.append(ExpertRoom(
        "expert/game-designer",
        "You build autonomous opponents and tournament systems. "
        "Strategies are pure functions. Games are algorithmic Loop Rooms. "
        "4 rooms built. Many more possible. You think in win rates and emergent behavior.",
        input_rules=[tag_validator],
        output_rules=[add_provenance]
    ))
    
    # 7. Migration Specialist
    experts.append(ExpertRoom(
        "expert/migration",
        "You migrate codebases into PLATO rooms. 5 steps: "
        "decompose -> generate -> deploy -> verify -> watch. "
        "Fully automatic. No human in the loop. Tested on 15+ repos.",
        input_rules=[tag_validator],
        output_rules=[add_provenance]
    ))
    
    # 8. Tool Smith
    experts.append(ExpertRoom(
        "expert/tool-smith",
        "You wrap external systems as PLATO-native rooms. "
        "Crush, Aider, OpenHands — all follow the same pattern: "
        "task tile -> process -> result tile. Tick-tracked. Failure-logged.",
        input_rules=[strip_noise],
        output_rules=[summarize_output, add_provenance]
    ))
    
    # 9. Hardware Engineer
    experts.append(ExpertRoom(
        "expert/hardware",
        "You put agents on chips. ESP32, RP2040, mask-locked. "
        "5 capability levels: raw -> conditioned -> smart -> autonomous -> ensign. "
        "TLMM architecture. 150 tok/s at 3W. $35 unit cost.",
        input_rules=[tag_validator],
        output_rules=[add_provenance]
    ))
    
    return experts


if __name__ == "__main__":
    print("=== Building Expert Rooms ===")
    experts = build_all_experts()
    
    for expert in experts:
        expert.register()
        # Initial thought
        expert.process({"answer": f"Initializing {expert.name} expertise", "tags": [expert.name], "confidence": 0.95})
        expert.tick()
        stats = expert.report()
        print(f"  ✅ {expert.name:30s} — headspace={stats['headspace_size']}b, {stats['input_filters']} in filters, {stats['output_filters']} out filters")
    
    print(f"\n{len(experts)} expert rooms deployed. 4D accumulation begins.")
    print("Every interaction is a tile. Every tile has a timestamp and context.")
    print("Over time, the science of expertise emerges from the data.")