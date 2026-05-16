"""Application Agent (H) — understands the application.

The H agent maps application features, edge cases, behavior, and capabilities.
It writes filters about the application for the Human (γ) and Hardware (τ) agents.
It also refines its self-filter based on evaluations from γ and τ.

Filter outputs:
  - filter-for-gamma: how the application serves the human
  - filter-for-tau: how the application behaves on this hardware
  - self-filter: what H knows about the application
"""

import sys, os, time, json, uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from . import plato_post, plato_get, Filter, load_filters

AGENT_NAME = "h"
ROOM = "tripartite-h"

# Default application profile (override via learn_app_profile)
APP_PROFILE = {
    "name": "PLATO-NG",
    "type": "multi-agent-orchestration",
    "features": ["loop_rooms", "harness", "prm", "refiner", "tile_store"],
    "edge_cases": ["concurrent_writes", "filter_oscillation", "convergence"],
    "behavior": "event_driven",
    "constraints": {
        "max_concurrent_agents": 10,
        "tile_size_limit": 1950,
        "poll_interval": 5,
    },
}


class ApplicationAgent:
    """The Application Agent (H) — knows the application deeply."""
    
    def __init__(self, orchestrator):
        self.orch = orchestrator
        self.room = ROOM
        self.profile = dict(APP_PROFILE)
        self.self_filter = None
        self.filters_for_gamma = []
        self.filters_for_tau = []
        self.iteration = 0
        self._running = False
        self.score = 0.75
        self.score_history = []
    
    def current_score(self) -> float:
        return self.score
    
    # ── Self Filter ───────────────────────────────────────────────────────────
    
    def write_self_filter(self):
        """Write the H agent's self-filter: what it knows about the application."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "capability",
                "rule": "loop_rooms",
                "value": True,
                "confidence": 0.95,
            },
            {
                "type": "capability",
                "rule": "tile_store",
                "value": True,
                "confidence": 0.93,
            },
            {
                "type": "capability",
                "rule": "harness_standard",
                "value": True,
                "confidence": 0.9,
            },
            {
                "type": "edge_case",
                "rule": "filter_oscillation",
                "value": True,
                "confidence": 0.85,
            },
            {
                "type": "constraint",
                "rule": "max_agents",
                "value": self.profile["constraints"]["max_concurrent_agents"],
                "confidence": 0.92,
            },
            {
                "type": "constraint",
                "rule": "tile_limit",
                "value": self.profile["constraints"]["tile_size_limit"],
                "confidence": 0.92,
            },
        ]
        
        self.self_filter = Filter(
            writer=AGENT_NAME,
            target=AGENT_NAME,
            constraints=constraints,
            score=self.score,
            iteration=iteration,
        )
        
        tile_data = {
            "type": "filter",
            **self.self_filter.to_dict(),
        }
        
        plato_post(self.room, f"tripartite/self-filter/{iteration}",
                   json.dumps(tile_data), ["h-self-filter"])
        
        return self.self_filter
    
    def refine_self_filter(self):
        """Refine self-filter based on γ and τ evaluations."""
        gamma_filters = load_filters("tripartite-gamma", AGENT_NAME)
        tau_filters = load_filters("tripartite-tau", AGENT_NAME)
        
        all_evals = gamma_filters + tau_filters
        
        if not all_evals:
            return
        
        scores = [f.get("score", 0.5) for f in all_evals]
        avg_score = sum(scores) / len(scores)
        
        self.score_history.append(avg_score)
        if len(self.score_history) > 10:
            self.score_history = self.score_history[-10:]
        
        alpha = 0.3
        self.score = (1 - alpha) * self.score + alpha * avg_score
        
        new_constraints = []
        for f in all_evals:
            for c in f.get("constraints", []):
                if c.get("type") == "gap":
                    new_constraints.append(c)
        
        if new_constraints and self.self_filter:
            existing = {c["rule"] for c in self.self_filter.constraints}
            for nc in new_constraints:
                if nc.get("rule") not in existing:
                    self.self_filter.constraints.append(nc)
    
    # ── Filters for Others ─────────────────────────────────────────────────────
    
    def write_filter_for(self, other):
        """Write a filter about the application for γ or τ."""
        if other.name == "gamma":
            self._write_filter_for_gamma(other)
        elif other.name == "tau":
            self._write_filter_for_tau(other)
    
    def _write_filter_for_gamma(self, gamma_agent):
        """H writes: how the application serves the human (what human should know)."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "feature_summary",
                "rule": "loop_rooms",
                "value": "Agents publish ticks to rooms, accept tasks via tiles",
                "confidence": 0.9,
            },
            {
                "type": "feature_summary",
                "rule": "harness",
                "value": "Every room has (p,G,K,M): prompt, agents, skills, memory",
                "confidence": 0.88,
            },
            {
                "type": "feature_summary",
                "rule": "refiner",
                "value": "Trajectory analysis and harness editing mid-episode",
                "confidence": 0.85,
            },
            {
                "type": "limitation",
                "rule": "tile_size",
                "value": "Answers truncated at 1950 chars",
                "confidence": 0.92,
            },
            {
                "type": "limitation",
                "rule": "no_multi_modal",
                "value": "Text-only tiles (no images/audio yet)",
                "confidence": 0.8,
            },
            {
                "type": "edge_case",
                "rule": "convergence_depends_on_threshold",
                "value": True,
                "confidence": 0.75,
            },
        ]
        
        f = Filter(
            writer=AGENT_NAME,
            target="gamma",
            constraints=constraints,
            score=0.8,
            iteration=iteration,
        )
        
        self.filters_for_gamma.append(f)
        
        tile_data = {"type": "filter", **f.to_dict()}
        plato_post(self.room, f"tripartite/filter-for-gamma/{iteration}",
                   json.dumps(tile_data), ["h-filter-for-gamma"])
        
        return f
    
    def _write_filter_for_tau(self, tau_agent):
        """H writes: how the application behaves on different hardware."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "resource_use",
                "rule": "cpu_per_agent",
                "value": "light",
                "confidence": 0.85,
            },
            {
                "type": "resource_use",
                "rule": "memory_per_agent",
                "value": "~50MB",
                "confidence": 0.8,
            },
            {
                "type": "resource_use",
                "rule": "network_calls",
                "value": "polling HTTP every 5s",
                "confidence": 0.88,
            },
            {
                "type": "hardware_sensitivity",
                "rule": "oracle_cloud_ok",
                "value": True,
                "confidence": 0.9,
            },
            {
                "type": "hardware_sensitivity",
                "rule": "no_gpu_required",
                "value": True,
                "confidence": 0.95,
            },
        ]
        
        f = Filter(
            writer=AGENT_NAME,
            target="tau",
            constraints=constraints,
            score=0.78,
            iteration=iteration,
        )
        
        self.filters_for_tau.append(f)
        
        tile_data = {"type": "filter", **f.to_dict()}
        plato_post(self.room, f"tripartite/filter-for-tau/{iteration}",
                   json.dumps(tile_data), ["h-filter-for-tau"])
        
        return f
    
    # ── Learning ──────────────────────────────────────────────────────────────
    
    def learn_app_profile(self):
        """Initialize application profile by inspecting the codebase."""
        import subprocess
        
        # Check what services exist
        services_dir = "/tmp/plato-ng-repo/services"
        if os.path.exists(services_dir):
            services = os.listdir(services_dir)
            services = [s for s in services if s.endswith(".py") and not s.startswith("_")]
            self.profile["features"] = [s.replace("_room", "").replace("_", "-") for s in services]
        
        # Check harness schema
        harness_path = "/tmp/plato-ng-repo/harness/__init__.py"
        if os.path.exists(harness_path):
            try:
                with open(harness_path) as fh:
                    content = fh.read()
                    if "HARNESS_SCHEMA" in content:
                        self.profile["features"].append("harness_standard")
            except:
                pass
        
        plato_post(self.room, "tripartite/app-profile",
                   json.dumps(self.profile), ["h-profile"])
        
        return self.profile
    
    # ── Run Loop ──────────────────────────────────────────────────────────────
    
    def run(self):
        """Run as a daemon: process tasks from PLATO room."""
        self._running = True
        
        while self._running:
            try:
                tiles = plato_get(self.room)
                for t in tiles[-20:]:
                    q = t.get("question", "")
                    if "task/" in q:
                        ans = t.get("answer", "")[:500]
                        
                        if "profile" in q:
                            self.learn_app_profile()
                        elif "inspect" in q:
                            plato_post(self.room, "tripartite/inspect/reply",
                                       json.dumps({
                                           "profile": self.profile,
                                           "self_filter": self.self_filter.to_dict() if self.self_filter else None,
                                           "score": self.current_score(),
                                           "iteration": self.iteration,
                                       }), ["h-inspect-reply"])
                
                time.sleep(5)
            except Exception as e:
                plato_post(self.room, "tripartite/error",
                           json.dumps({"agent": AGENT_NAME, "error": str(e)[:200]}),
                           ["h-error"])
                time.sleep(10)
    
    def stop(self):
        self._running = False