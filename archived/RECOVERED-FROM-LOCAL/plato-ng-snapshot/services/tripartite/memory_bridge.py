"""Memory Bridge — persists tripartite filter state through the Memory Crystal.

Integrates tripartite agent filters with MemoryCrystal for cross-session persistence.

On each filter oscillation iteration:
  1. Crystallizes the filter state (score, constraints, profile, iteration)
  2. Stores a reference tile in PLATO for lookup

On restart:
  1. Loads the last filter state from the Memory Crystal
  2. Agents resume from persisted state

Persistence tiers:
  - Gamma (Human): persists across ALL application sessions (cross-application learning)
  - Tau (Hardware): persists across ALL deployments (same hardware knowledge)
  - H (Application): session-local only (re-initializes on each run)

Usage:
  python3 __init__.py --daemon --persist   # Run with memory-backed filters
  python3 __init__.py --daemon              # Run without persistence (default)
"""

import sys, os, time, json, threading
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.memory import MemoryCrystal

PLATO = "http://localhost:8847"

# ── Memory Key Constants ───────────────────────────────────────────────────────

STATE_REF_QUESTION = "tripartite/memory-state-ref"
CRYSTAL_TAG = "memory-bridge"


# ── MemoryBridge ───────────────────────────────────────────────────────────────

class MemoryBridge:
    """Bridges tripartite agents to MemoryCrystal for filter persistence.
    
    Stores filter state at the end of each oscillation iteration.
    Loads the last persisted state on startup.
    
    The bridge is global (shared across all three agents) because:
      1. All three agents share one MemoryCrystal instance
      2. State refs are per-agent (gamma, h, tau each have their own key)
      3. The crystal is the durable store; PLATO tiles are the lookup index
    """
    
    def __init__(self, persist: bool = False):
        self.persist = persist
        self.crystal = MemoryCrystal()
        self._loaded = {name: False for name in ["gamma", "h", "tau"]}
        self._last_iteration = {name: 0 for name in ["gamma", "h", "tau"]}
    
    # ── PLATO Helpers ───────────────────────────────────────────────────────────
    
    def _plato_post(self, room: str, question: str, answer: str, tags=None) -> dict:
        """Publish a tile to a PLATO room (local helper)."""
        import urllib.request
        tile = {
            "domain": room,
            "question": question,
            "answer": str(answer)[:1950],
            "tags": (tags or []) + [CRYSTAL_TAG],
            "source": CRYSTAL_TAG,
            "confidence": 0.92,
        }
        try:
            d = json.dumps(tile).encode()
            req = urllib.request.Request(
                f"{PLATO}/submit",
                data=d,
                headers={"Content-Type": "application/json"},
            )
            return json.loads(urllib.request.urlopen(req, timeout=10).read())
        except Exception as e:
            return {"error": str(e)}
    
    def _plato_get(self, room: str, question_pattern: str = ""):
        """Fetch tiles from a PLATO room (local helper)."""
        import urllib.request
        try:
            r = json.loads(
                urllib.request.urlopen(f"{PLATO}/room/{room}/history", timeout=10).read()
            )
            tiles = r.get("tiles", []) if isinstance(r, dict) else r
            if question_pattern:
                return [t for t in tiles if question_pattern in t.get("question", "")]
            return tiles
        except:
            return []
    
    # ── State Ref Tile ─────────────────────────────────────────────────────────
    
    def _get_state_ref(self, agent_name: str) -> Optional[dict]:
        """Find the most recent state-ref tile for an agent."""
        tiles = self._plato_get(f"tripartite-{agent_name}", STATE_REF_QUESTION)
        if not tiles:
            return None
        # Most recent first
        return tiles[-1]
    
    def _save_state_ref(self, agent_name: str, mem_id: str, iteration: int):
        """Write a state-ref tile pointing to the crystal memory ID."""
        self._plato_post(
            f"tripartite-{agent_name}",
            STATE_REF_QUESTION,
            json.dumps({
                "mem_id": mem_id,
                "iteration": iteration,
                "persisted_at": time.time(),
            }),
            [CRYSTAL_TAG, f"{CRYSTAL_TAG}-{agent_name}"]
        )
    
    # ── Crystallize (Save) ─────────────────────────────────────────────────────
    
    def crystallize_filter(self, agent_name: str, state: dict, iteration: int) -> str:
        """Persist an agent's filter state to the Memory Crystal.
        
        Returns the memory ID. Does nothing if persist=False.
        """
        if not self.persist:
            return ""
        
        # Serialize state
        content = json.dumps(state, sort_keys=True)
        
        # Tag with agent name for cross-session queries
        tags = [CRYSTAL_TAG, f"agent-{agent_name}", f"iteration-{iteration}"]
        
        # Crystallize into the shared crystal
        mem_id = self.crystal.crystallize(
            content,
            valence=0.7,  # High valence — important for identity
            tags=tags,
        )
        
        # Write ref tile for lookup
        self._save_state_ref(agent_name, mem_id, iteration)
        
        self._last_iteration[agent_name] = iteration
        
        return mem_id
    
    def crystallize_all(self, agents: dict, iteration: int):
        """Crystallize all three agents' filter state at end of an iteration.
        
        Only Gamma and Tau are persisted (cross-session).
        H is session-local only.
        """
        if not self.persist:
            return
        
        for name in ["gamma", "tau"]:
            agent = agents.get(name)
            if not agent:
                continue
            
            state = {
                "score": agent.current_score(),
                "iteration": agent.iteration,
                "score_history": list(agent.score_history[-10:]),
                "profile": dict(agent.profile),
                "self_filter": agent.self_filter.to_dict() if agent.self_filter else None,
            }
            
            self.crystallize_filter(name, state, iteration)
    
    # ── Main Load Interface ────────────────────────────────────────────────────
    
    def load_agent_state(self, agent_name: str) -> Optional[dict]:
        """Load persisted state for an agent.
        
        Returns state dict with keys: score, iteration, score_history, profile,
        self_filter, filters_for_others.
        """
        if not self.persist:
            return None
        
        if self._loaded.get(agent_name, False):
            return None  # Already loaded this session
        
        # Look for the most recent full state tile for this agent
        tiles = self._plato_get(f"tripartite-{agent_name}", f"tripartite/{CRYSTAL_TAG}-state")
        if not tiles:
            return None
        
        latest = tiles[-1]
        ans = latest.get("answer", "")
        if isinstance(ans, str):
            try:
                state = json.loads(ans)
            except:
                return None
        else:
            state = ans
        
        self._loaded[agent_name] = True
        return state
    
    def save_agent_state(self, agent_name: str, state: dict, iteration: int):
        """Save full agent state as a PLATO tile and crystal memory.
        
        Stores full state as PLATO tile (exact recovery) and crystal memory
        (for decay tracking and retention policy).
        """
        if not self.persist:
            return
        
        # Tile 1: Full state (for exact recovery)
        self._plato_post(
            f"tripartite-{agent_name}",
            f"tripartite/{CRYSTAL_TAG}-state/{iteration}",
            json.dumps(state),
            [CRYSTAL_TAG, f"{CRYSTAL_TAG}-{agent_name}", f"{CRYSTAL_TAG}-state"]
        )
        
        # Tile 2: Crystal bookmark (for decay tracking)
        content = json.dumps(state)
        tags = [CRYSTAL_TAG, f"agent-{agent_name}", f"iteration-{iteration}"]
        mem_id = self.crystal.crystallize(content, valence=0.7, tags=tags)
        
        self._save_state_ref(agent_name, mem_id, iteration)
    
    def load_all(self, agent_names: list = None) -> dict:
        """Load persisted state for all agents. Returns dict of name -> state."""
        if agent_names is None:
            agent_names = ["gamma", "tau"]  # Only cross-session agents
        
        results = {}
        for name in agent_names:
            state = self.load_agent_state(name)
            if state:
                results[name] = state
        
        return results
    
    def save_all(self, agents: dict, iteration: int):
        """Save all agent states after an iteration."""
        if not self.persist:
            return
        
        for name in ["gamma", "tau"]:  # Cross-session only
            agent = agents.get(name)
            if not agent:
                continue
            
            state = {
                "score": agent.current_score(),
                "iteration": agent.iteration,
                "score_history": list(agent.score_history[-10:]),
                "profile": dict(agent.profile),
                "self_filter": agent.self_filter.to_dict() if agent.self_filter else None,
            }
            
            self.save_agent_state(name, state, iteration)
    
    def is_loaded(self, agent_name: str) -> bool:
        return self._loaded.get(agent_name, False)