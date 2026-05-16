"""PLATO Tripartite Agent System — Gamma (Human), H (Application), Tau (Hardware).

Three agents write filters for each other. Filters oscillate until convergence.
Each agent is a PLATO Loop Room: publishes ticks, accepts tasks, logs results.

Filter lifecycle:
  1. Each agent initializes with a self-filter
  2. Other agents write evaluation filters for it
  3. Agent refines its self-filter based on others' evaluations
  4. Convergence = filters stabilize across iterations

Usage:
  python3 __init__.py --daemon    # Start all three agents
  python3 __init__.py --init      # Initialize human context first
  curl http://localhost:8847/room/tripartite-gamma/history  # Inspect gamma filter
  curl http://localhost:8847/room/tripartite-hw/history     # Inspect hardware filter
"""

import sys, os, time, json, threading, uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .memory_bridge import MemoryBridge

PLATO = "http://localhost:8847"

def plato_post(room, question, answer, tags=None, source="tripartite"):
    """Publish a tile to a PLATO room."""
    tile = {
        "domain": room,
        "question": question,
        "answer": str(answer)[:1950],
        "tags": (tags or []) + ["tripartite", f"tripartite-{source}"],
        "source": source,
        "confidence": 0.92,
    }
    try:
        import urllib.request
        d = json.dumps(tile).encode()
        req = urllib.request.Request(
            f"{PLATO}/submit",
            data=d,
            headers={"Content-Type": "application/json"},
        )
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except Exception as e:
        return {"error": str(e)}

def plato_get(room, question_pattern=""):
    """Fetch tiles from a PLATO room."""
    try:
        import urllib.request
        r = json.loads(
            urllib.request.urlopen(f"{PLATO}/room/{room}/history", timeout=10).read()
        )
        tiles = r.get("tiles", []) if isinstance(r, dict) else r
        if question_pattern:
            return [t for t in tiles if question_pattern in t.get("question", "")]
        return tiles
    except:
        return []

def converge_value(values, threshold=0.05):
    """Check if oscillation has converged: all values within threshold of each other."""
    if not values:
        return False
    v = list(values)
    return max(v) - min(v) < threshold

# ── Filter Types ──────────────────────────────────────────────────────────────

class Filter:
    """A filter is a dict of constraint rules written by one agent about another.
    
    Filter schema:
      constraints: list of constraint rules (JSON-serializable dicts)
      score: 0.0-1.0 quality score assigned by the writer
      iteration: which oscillation cycle this was written in
      writer: which agent wrote this filter ("gamma", "h", "tau")
      target: which agent this filter is about
    """
    
    def __init__(self, writer: str, target: str, constraints: list, score: float, iteration: int):
        self.writer = writer
        self.target = target
        self.constraints = constraints  # list of constraint dicts
        self.score = score
        self.iteration = iteration
        self._id = uuid.uuid4().hex[:8]
    
    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "writer": self.writer,
            "target": self.target,
            "constraints": self.constraints,
            "score": round(self.score, 3),
            "iteration": self.iteration,
        }
    
    def __repr__(self):
        return f"Filter({self.writer}→{self.target}, score={self.score}, n={len(self.constraints)})"

def load_filters(room: str, target: str, iteration: int = None) -> list:
    """Load all filters in a room targeting a specific agent."""
    tiles = plato_get(room)
    filters = []
    for t in tiles:
        ans = t.get("answer", "")
        if isinstance(ans, str):
            try:
                ans = json.loads(ans)
            except:
                continue
        if isinstance(ans, dict) and ans.get("type") == "filter":
            if ans.get("target") == target:
                if iteration is None or ans.get("iteration") == iteration:
                    filters.append(ans)
    return filters

# ── Orchestrator ─────────────────────────────────────────────────────────────

class TripartiteOrchestrator:
    """Spawns and coordinates all three agents.
    
    Runs the oscillation loop:
      1. Each agent writes its self-filter
      2. Agents write filters for each other
      3. Each agent's self-filter is refined based on received filters
      4. Repeat until convergence
    
    With --persist enabled:
      - Filter state is crystallized to MemoryCrystal each iteration
      - State is restored from MemoryCrystal on restart
      - Gamma (Human) persists across ALL application sessions
      - Tau (Hardware) persists across ALL deployments
      - H (Application) is session-local only
    """
    
    def __init__(self, persist: bool = False):
        self.agents = {}
        self.iteration = 0
        self.max_iterations = 20
        self.convergence_threshold = 0.05
        self.done = False
        self._lock = threading.Lock()
        self.persist = persist
        self.bridge = MemoryBridge(persist=persist) if persist else None
    
    def spawn(self):
        """Start all three agents as daemon threads."""
        from .human_agent import HumanAgent
        from .app_agent import ApplicationAgent
        from .hw_agent import HardwareAgent
        
        # Load persisted state for cross-session agents
        loaded_states = {}
        if self.bridge:
            loaded_states = self.bridge.load_all()
        
        gamma = HumanAgent(self, persisted_state=loaded_states.get("gamma"))
        h = ApplicationAgent(self)
        tau = HardwareAgent(self, persisted_state=loaded_states.get("tau"))
        
        self.agents = {"gamma": gamma, "h": h, "tau": tau}
        
        for name, agent in self.agents.items():
            t = threading.Thread(target=agent.run, name=f"tripartite-{name}", daemon=True)
            t.start()
            plato_post(f"tripartite-{name}", "tripartite/spawned",
                      json.dumps({"name": name, "pid": id(agent)}), ["tripartite-spawn"])
        
        return self
    
    def tick(self, status="running", detail=""):
        """Publish orchestrator heartbeat."""
        self.iteration += 1
        scores = {n: a.current_score() for n, a in self.agents.items()}
        plato_post("tripartite-orchestrator", "tripartite/tick",
                  json.dumps({
                      "iteration": self.iteration,
                      "scores": scores,
                      "status": status,
                      "converged": self.done,
                      "detail": detail[:100],
                  }), ["tripartite-tick", status])
        return scores
    
    def check_convergence(self) -> bool:
        """Check if all agent filters have converged."""
        scores = [a.current_score() for a in self.agents.values()]
        return converge_value(scores, self.convergence_threshold)
    
    def orchestrate(self):
        """Run the oscillation loop. Call from main thread."""
        # Phase 1: self-filters
        for name, agent in self.agents.items():
            agent.write_self_filter()
        
        while not self.done and self.iteration < self.max_iterations:
            self.tick("oscillating")
            
            # Phase 2: each agent writes about the others
            for name, agent in self.agents.items():
                for other_name, other in self.agents.items():
                    if other_name != name:
                        agent.write_filter_for(other)
            
            # Phase 3: each agent refines its self-filter based on received evaluations
            for name, agent in self.agents.items():
                agent.refine_self_filter()
            
            # Check convergence
            if self.check_convergence():
                self.done = True
                self.tick("converged", "all filters stable")
                break
            
            # Persist state after each iteration (if enabled)
            if self.bridge:
                self.bridge.save_all(self.agents, self.iteration)
            
            # Also converge if score oscillation is stable (not growing)
            if self.iteration > 3:
                recent_scores = [a.score_history[-3:] for a in self.agents.values()]
                all_stable = all(converge_value(s) for s in recent_scores)
                if all_stable:
                    self.done = True
                    self.tick("converged", "score oscillation stable")
                    break
            
            time.sleep(1)
        
        if not self.done:
            self.tick("max_iterations", f"reached {self.max_iterations}")
        
        return self.done


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Tripartite Agent System")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--init", action="store_true", help="Initialize human context first")
    parser.add_argument("--persist", action="store_true", help="Enable memory-backed filter persistence")
    args = parser.parse_args()
    
    if args.init:
        print("Initializing human context...")
        from .human_agent import HumanAgent
        ag = HumanAgent(None)
        ag.learn_human_profile()
        print("Human context initialized. Run --daemon to start the system.")
        return
    
    if args.daemon:
        print("Starting Tripartite Agent System (daemon mode)...")
        if args.persist:
            print("  [persist] Memory-backed filter persistence enabled")
        orch = TripartiteOrchestrator(persist=args.persist).spawn()
        print("All three agents running. Press Ctrl+C to stop.")
        try:
            converged = orch.orchestrate()
            if converged:
                print("✓ Filters converged!")
            else:
                print("✗ Max iterations reached.")
        except KeyboardInterrupt:
            print("\nShutting down...")
        return
    
    # Default: print status
    print("Tripartite Agent System")
    print("=" * 40)
    for name in ["gamma", "h", "tau"]:
        tiles = plato_get(f"tripartite-{name}", "tripartite/self-filter")
        if tiles:
            latest = tiles[-1]
            ans = latest.get("answer", "")
            print(f"  {name}: filter exists (iteration {json.loads(ans).get('iteration', '?') if isinstance(ans, str) else '?'})")
        else:
            print(f"  {name}: no filter yet — run --daemon")


if __name__ == "__main__":
    main()