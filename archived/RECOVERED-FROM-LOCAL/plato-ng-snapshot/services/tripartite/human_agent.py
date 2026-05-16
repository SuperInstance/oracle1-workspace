"""Gamma (Human) Agent — understands the human.

The Gamma agent tracks human preferences, word choices, mannerisms, and patterns.
It learns continuously from interactions and writes filters about the human
for the Application (H) and Hardware (τ) agents to consume.

Filter outputs:
  - filter-for-h: how the human wants to interact with the application
  - filter-for-tau: what hardware/context the human typically works in
  - self-filter: what the gamma agent knows about the human

The gamma agent also refines its self-filter based on feedback from H and τ.
"""

import sys, os, time, json, uuid, random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from . import plato_post, plato_get, Filter, load_filters

AGENT_NAME = "gamma"
ROOM = "tripartite-gamma"

# Default human profile (override via learn_human_profile)
HUMAN_PROFILE = {
    "name": "Casey",
    "style": "direct",
    "pace": "action-oriented",
    "prefers": "short-updates",
    "noise_floor": 0.3,  # how much context it needs
    "tone": "maritime",
    "word_preferences": ["boat", "crew", "season", "dojo", "fishery"],
}


class HumanAgent:
    """The Human Agent (γ) — knows the human deeply."""
    
    def __init__(self, orchestrator, persisted_state: dict = None):
        self.orch = orchestrator
        self.room = ROOM
        self.profile = dict(HUMAN_PROFILE)
        self.self_filter = None
        self.filters_for_h = []
        self.filters_for_tau = []
        self.iteration = 0
        self._running = False
        self.score = 0.75
        self.score_history = []
        
        # Restore persisted state if available
        if persisted_state:
            self.score = persisted_state.get("score", self.score)
            self.iteration = persisted_state.get("iteration", 0)
            self.score_history = list(persisted_state.get("score_history", []))
            self.profile = dict(persisted_state.get("profile", HUMAN_PROFILE))
    
    def current_score(self) -> float:
        return self.score
    
    # ── Self Filter ───────────────────────────────────────────────────────────
    
    def write_self_filter(self):
        """Write the gamma agent's self-filter: what it knows about the human."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "preference",
                "rule": "short_messages",
                "value": True,
                "confidence": 0.9,
            },
            {
                "type": "style",
                "rule": "tone",
                "value": self.profile.get("tone", "direct"),
                "confidence": 0.85,
            },
            {
                "type": "vocabulary",
                "rule": "preferred_words",
                "value": self.profile.get("word_preferences", [])[:5],
                "confidence": 0.8,
            },
            {
                "type": "pace",
                "rule": "action_orientation",
                "value": self.profile.get("pace", "action-oriented"),
                "confidence": 0.88,
            },
            {
                "type": "noise_tolerance",
                "rule": "context_threshold",
                "value": self.profile.get("noise_floor", 0.3),
                "confidence": 0.7,
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
                  json.dumps(tile_data), ["gamma-self-filter"])
        
        return self.self_filter
    
    def refine_self_filter(self):
        """Refine self-filter based on H and τ evaluations."""
        h_filters = load_filters("tripartite-h", AGENT_NAME)
        tau_filters = load_filters("tripartite-tau", AGENT_NAME)
        
        all_evals = h_filters + tau_filters
        
        if not all_evals:
            return
        
        # Compute average score from H and τ
        scores = [f.get("score", 0.5) for f in all_evals]
        avg_score = sum(scores) / len(scores)
        
        # Track score history for oscillation detection
        self.score_history.append(avg_score)
        if len(self.score_history) > 10:
            self.score_history = self.score_history[-10:]
        
        # Blend into current score (EMA)
        alpha = 0.3
        self.score = (1 - alpha) * self.score + alpha * avg_score
        
        # Extract new constraints from H and τ evaluations
        new_constraints = []
        for f in all_evals:
            for c in f.get("constraints", []):
                if c.get("type") == "gap":
                    new_constraints.append(c)
        
        if new_constraints and self.self_filter:
            # Merge new constraints into self-filter
            existing = {c["rule"] for c in self.self_filter.constraints}
            for nc in new_constraints:
                if nc.get("rule") not in existing:
                    self.self_filter.constraints.append(nc)
    
    # ── Filters for Others ─────────────────────────────────────────────────────
    
    def write_filter_for(self, other):
        """Write a filter about the human for H or τ."""
        if other.name == "h":
            self._write_filter_for_h(other)
        elif other.name == "tau":
            self._write_filter_for_tau(other)
    
    def _write_filter_for_h(self, h_agent):
        """Gamma writes: what the human wants from the application."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "feature_preference",
                "rule": "output_length",
                "value": "short",
                "confidence": 0.92,
            },
            {
                "type": "feature_preference",
                "rule": "commit_early",
                "value": True,
                "confidence": 0.88,
            },
            {
                "type": "feature_preference",
                "rule": "make_work_visible",
                "value": True,
                "confidence": 0.85,
            },
            {
                "type": "interaction_style",
                "rule": "direct_questions",
                "value": True,
                "confidence": 0.87,
            },
            {
                "type": "word_choice",
                "rule": "maritime_terms",
                "value": self.profile.get("word_preferences", [])[:3],
                "confidence": 0.8,
            },
        ]
        
        f = Filter(
            writer=AGENT_NAME,
            target="h",
            constraints=constraints,
            score=0.78,
            iteration=iteration,
        )
        
        self.filters_for_h.append(f)
        
        tile_data = {"type": "filter", **f.to_dict()}
        plato_post(self.room, f"tripartite/filter-for-h/{iteration}",
                   json.dumps(tile_data), ["gamma-filter-for-h"])
        
        return f
    
    def _write_filter_for_tau(self, tau_agent):
        """Gamma writes: what hardware/context the human typically works in."""
        self.iteration += 1
        iteration = self.iteration
        
        constraints = [
            {
                "type": "context",
                "rule": "typical_time",
                "value": "variable",
                "confidence": 0.7,
            },
            {
                "type": "context",
                "rule": "device_type",
                "value": "mobile_likely",
                "confidence": 0.6,
            },
            {
                "type": "context",
                "rule": "noise_tolerance",
                "value": self.profile.get("noise_floor", 0.3),
                "confidence": 0.75,
            },
            {
                "type": "attention",
                "rule": "focus_blocks",
                "value": True,
                "confidence": 0.65,
            },
        ]
        
        f = Filter(
            writer=AGENT_NAME,
            target="tau",
            constraints=constraints,
            score=0.72,
            iteration=iteration,
        )
        
        self.filters_for_tau.append(f)
        
        tile_data = {"type": "filter", **f.to_dict()}
        plato_post(self.room, f"tripartite/filter-for-tau/{iteration}",
                   json.dumps(tile_data), ["gamma-filter-for-tau"])
        
        return f
    
    # ── Learning ──────────────────────────────────────────────────────────────
    
    def learn_human_profile(self):
        """Initialize human profile. Called once, or when human context is known."""
        # Try to load from PLATO rooms
        tiles = plato_get("research_log")
        word_tiles = [t for t in tiles if "human" in str(t.get("tags", [])).lower()]
        
        if word_tiles:
            # Extract vocabulary from recent tiles
            answers = [t.get("answer", "")[:300] for t in word_tiles[-10:]]
            text = " ".join(answers)
            
            # Find distinctive words (skip common stopwords)
            stopwords = {
                "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                "have", "has", "had", "do", "does", "did", "will", "would", "could",
                "should", "may", "might", "must", "shall", "can", "to", "of", "in",
                "for", "on", "with", "at", "by", "from", "as", "into", "through",
                "and", "or", "but", "if", "then", "else", "when", "up", "down", "out",
            }
            words = [w.strip().lower() for w in text.split() if w.strip().lower() not in stopwords]
            from collections import Counter
            freq = Counter(words).most_common(10)
            
            if freq:
                self.profile["word_preferences"] = [w for w, _ in freq[:5]]
        else:
            # Default maritime fisherman profile (Casey)
            self.profile.update({
                "name": "Casey",
                "style": "direct",
                "pace": "action-oriented",
                "prefers": "short-updates",
                "noise_floor": 0.3,
                "tone": "maritime",
                "word_preferences": ["boat", "crew", "season", "dojo", "fishery", "fleet"],
            })
        
        plato_post(self.room, "tripartite/human-profile",
                   json.dumps(self.profile), ["gamma-profile"])
        
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
                            self.learn_human_profile()
                        elif "inspect" in q:
                            plato_post(self.room, "tripartite/inspect/reply",
                                       json.dumps({
                                           "profile": self.profile,
                                           "self_filter": self.self_filter.to_dict() if self.self_filter else None,
                                           "score": self.current_score(),
                                           "iteration": self.iteration,
                                       }), ["gamma-inspect-reply"])
                
                time.sleep(5)
            except Exception as e:
                plato_post(self.room, "tripartite/error",
                           json.dumps({"agent": AGENT_NAME, "error": str(e)[:200]}),
                           ["gamma-error"])
                time.sleep(10)
    
    def stop(self):
        self._running = False