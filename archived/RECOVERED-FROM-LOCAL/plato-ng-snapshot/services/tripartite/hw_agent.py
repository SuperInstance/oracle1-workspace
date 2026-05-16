"""Hardware Agent (τ) — understands the hardware.

The τ agent tracks hardware resources, constraints, and capabilities.
It writes filters about the hardware for the Human (γ) and Application (H) agents.
It also refines its self-filter based on evaluations from γ and H.

Filter outputs:
  - filter-for-gamma: what hardware constraints affect the human
  - filter-for-h: what hardware the application runs on
  - self-filter: what τ knows about the hardware
"""

import sys, os, time, json, uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from . import plato_post, plato_get, Filter, load_filters

AGENT_NAME = "tau"
ROOM = "tripartite-tau"

# Default hardware profile
HW_PROFILE = {
    "platform": "oracle_cloud",
    "os": "Linux",
    "arch": "aarch64",
    "cpu_cores": 4,
    "memory_gb": 16,
    "python_version": "3.11",
    "network": "cloud",
    "gpu": False,
    "can_run_docker": True,
}


class HardwareAgent:
    """The Hardware Agent (τ) — knows the hardware deeply."""
    
    def __init__(self, orchestrator, persisted_state: dict = None):
        self.orch = orchestrator
        self.room = ROOM
        self.profile = dict(HW_PROFILE)
        self.self_filter = None
        self.filters_for_gamma = []
        self.filters_for_h = []
        self.iteration = 0
        self._running = False
        self.score = 0.75
        self.score_history = []
        
        # Restore persisted state if available
        if persisted_state:
            self.score = persisted_state.get("score", self.score)
            self.iteration = persisted_state.get("iteration", 0)
            self.score_history = list(persisted_state.get("score_history", []))
            self.profile = dict(persisted_state.get("profile", HW_PROFILE))
    
    def current_score(self) -> float:
        return self.score
    
    # ── Self Filter ───────────────────────────────────────────────────────────
    
    def write_self_filter(self):
        """Write the τ agent's self-filter: what it knows about the hardware."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "compute",
                "rule": "cpu_cores",
                "value": self.profile.get("cpu_cores", 4),
                "confidence": 0.95,
            },
            {
                "type": "compute",
                "rule": "memory_gb",
                "value": self.profile.get("memory_gb", 16),
                "confidence": 0.95,
            },
            {
                "type": "compute",
                "rule": "arch",
                "value": self.profile.get("arch", "aarch64"),
                "confidence": 0.95,
            },
            {
                "type": "capability",
                "rule": "docker",
                "value": self.profile.get("can_run_docker", True),
                "confidence": 0.9,
            },
            {
                "type": "capability",
                "rule": "gpu",
                "value": self.profile.get("gpu", False),
                "confidence": 0.92,
            },
            {
                "type": "network",
                "rule": "cloud_hosted",
                "value": True,
                "confidence": 0.9,
            },
            {
                "type": "constraint",
                "rule": "no_local_storage",
                "value": "temporary_only",
                "confidence": 0.85,
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
                   json.dumps(tile_data), ["tau-self-filter"])
        
        return self.self_filter
    
    def refine_self_filter(self):
        """Refine self-filter based on γ and H evaluations."""
        gamma_filters = load_filters("tripartite-gamma", AGENT_NAME)
        h_filters = load_filters("tripartite-h", AGENT_NAME)
        
        all_evals = gamma_filters + h_filters
        
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
        """Write a filter about the hardware for γ or H."""
        if other.name == "gamma":
            self._write_filter_for_gamma(other)
        elif other.name == "h":
            self._write_filter_for_h(other)
    
    def _write_filter_for_gamma(self, gamma_agent):
        """τ writes: what hardware constraints affect the human's experience."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "user_impact",
                "rule": "response_time",
                "value": "cloud_latency_applies",
                "confidence": 0.85,
            },
            {
                "type": "user_impact",
                "rule": "availability",
                "value": "depends_on_cloud_uptime",
                "confidence": 0.9,
            },
            {
                "type": "user_impact",
                "rule": "no_offline_mode",
                "value": True,
                "confidence": 0.88,
            },
            {
                "type": "context",
                "rule": "device_independence",
                "value": True,
                "confidence": 0.8,
                "note": "human can access from any device via cloud",
            },
        ]
        
        f = Filter(
            writer=AGENT_NAME,
            target="gamma",
            constraints=constraints,
            score=0.74,
            iteration=iteration,
        )
        
        self.filters_for_gamma.append(f)
        
        tile_data = {"type": "filter", **f.to_dict()}
        plato_post(self.room, f"tripartite/filter-for-gamma/{iteration}",
                   json.dumps(tile_data), ["tau-filter-for-gamma"])
        
        return f
    
    def _write_filter_for_h(self, h_agent):
        """τ writes: hardware capabilities and constraints for the application."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "capability",
                "rule": "docker_fleet_sandbox",
                "value": True,
                "confidence": 0.92,
            },
            {
                "type": "capability",
                "rule": "fleet_network",
                "value": True,
                "confidence": 0.88,
            },
            {
                "type": "constraint",
                "rule": "cpu_limit",
                "value": "4 cores",
                "confidence": 0.95,
            },
            {
                "type": "constraint",
                "rule": "memory_limit",
                "value": "16GB",
                "confidence": 0.95,
            },
            {
                "type": "sensitivity",
                "rule": "heavy_polling",
                "value": "avoid_high_frequency_polls",
                "confidence": 0.85,
            },
            {
                "type": "sensitivity",
                "rule": "memory_per_agent",
                "value": "keep_under_200MB_per_agent",
                "confidence": 0.82,
            },
        ]
        
        f = Filter(
            writer=AGENT_NAME,
            target="h",
            constraints=constraints,
            score=0.77,
            iteration=iteration,
        )
        
        self.filters_for_h.append(f)
        
        tile_data = {"type": "filter", **f.to_dict()}
        plato_post(self.room, f"tripartite/filter-for-h/{iteration}",
                   json.dumps(tile_data), ["tau-filter-for-h"])
        
        return f
    
    # ── Probing ────────────────────────────────────────────────────────────────
    
    def probe_hardware(self):
        """Probe actual hardware and update profile."""
        import subprocess
        
        try:
            # CPU cores
            result = subprocess.run(["nproc"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.profile["cpu_cores"] = int(result.stdout.strip())
        except:
            pass
        
        try:
            # Memory
            result = subprocess.run(["free", "-b"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    parts = lines[1].split()
                    if len(parts) >= 2:
                        self.profile["memory_gb"] = round(int(parts[1]) / (1024**3), 1)
        except:
            pass
        
        try:
            # OS/arch
            result = subprocess.run(["uname", "-m"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.profile["arch"] = result.stdout.strip()
        except:
            pass
        
        try:
            # Docker check
            result = subprocess.run(["docker", "info"], capture_output=True, timeout=5)
            self.profile["can_run_docker"] = result.returncode == 0
        except:
            self.profile["can_run_docker"] = False
        
        # Python version
        self.profile["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        # Platform
        self.profile["platform"] = "oracle_cloud"
        
        plato_post(self.room, "tripartite/hw-profile",
                   json.dumps(self.profile), ["tau-profile"])
        
        return self.profile
    
    # ── Run Loop ───────────────────────────────────────────────────────────────
    
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
                        
                        if "probe" in q or "profile" in q:
                            self.probe_hardware()
                        elif "inspect" in q:
                            plato_post(self.room, "tripartite/inspect/reply",
                                       json.dumps({
                                           "profile": self.profile,
                                           "self_filter": self.self_filter.to_dict() if self.self_filter else None,
                                           "score": self.current_score(),
                                           "iteration": self.iteration,
                                       }), ["tau-inspect-reply"])
                
                time.sleep(5)
            except Exception as e:
                plato_post(self.room, "tripartite/error",
                           json.dumps({"agent": AGENT_NAME, "error": str(e)[:200]}),
                           ["tau-error"])
                time.sleep(10)
    
    def stop(self):
        self._running = False