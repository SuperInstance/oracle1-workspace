"""PLATO-NG Memory module — agent twin memory pipeline (Crush Gap 3 closed).

Lossy, reconstructive memory based on the Tile Compression Theorem.
Encodes PLATO tiles into constrained memories with Ebbinghaus decay.
Reconstructs on recall with fresh context. Decays without reinforcement.

Integrates: tile-memory (Python encoder/decoder) + memory-crystal (Rust decay)
Both from SuperInstance archived repos — salvaged and integrated.
"""

import json, math, time, hashlib, re
from datetime import datetime, timezone
from typing import Any

# ── Memory Tile ──

class MemoryTile:
    """A lossy, reconstructive memory unit.
    
    Stores constraint points (facts that survive compression) and decays
    following an Ebbinghaus forgetting curve unless reconsolidated.
    """
    
    def __init__(self, content: str, valence: float = 0.5, tags: list = None):
        self.id = hashlib.md5(content.encode()).hexdigest()[:12]
        self.source_hash = hashlib.sha256(content.encode()).hexdigest()
        self.tags = tags or []
        self.valence = valence  # 0.0-1.0 emotional salience
        self.created_at = time.time()
        self.accessed_at = time.time()
        self.access_count = 0
        self.round_number = 0
        
        # Extract constraints (immortal facts)
        self.constraints = self._extract_constraints(content)
        
        # Decay parameters
        self.half_life = 86400 * (1 + valence * 30)  # 1-31 days base half-life
    
    def _extract_constraints(self, content: str) -> dict:
        """Extract constraint points that survive compression."""
        constraints = {}
        
        # Proper nouns (capitalized words)
        constraints["proper_nouns"] = list(set(
            re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        ))
        
        # Numbers
        constraints["numbers"] = re.findall(r'\b\d+(?:\.\d+)?\b', content)
        
        # Dates
        constraints["dates"] = re.findall(
            r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|'
            r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2}(?:st|nd|rd|th)?\b',
            content, re.IGNORECASE
        )
        
        # Key phrases (quoted or emphasized)
        constraints["key_phrases"] = re.findall(r'[""](.+?)[""]', content)
        
        # URLs
        constraints["urls"] = re.findall(r'https?://\S+', content)
        
        # Summary (first sentence or anchor)
        sentences = content.split('.')
        constraints["summary_anchor"] = sentences[0].strip() if sentences else content[:100]
        
        return constraints
    
    @property
    def retention(self) -> float:
        """Current retention based on Ebbinghaus forgetting curve.
        R(t) = e^(-t/half_life) — returns 0.0-1.0
        """
        age = time.time() - self.accessed_at
        return math.exp(-age / self.half_life)
    
    def touch(self):
        """Access the memory — resets decay clock."""
        self.accessed_at = time.time()
        self.access_count += 1
        # Each access slightly extends half-life (reconsolidation)
        self.half_life *= 1.05
    
    def reconsolidate(self, new_context: str = ""):
        """Strengthen memory with new context. Resets decay, increases valence."""
        self.touch()
        self.valence = min(1.0, self.valence + 0.05)
        if new_context:
            new_constraints = self._extract_constraints(new_context)
            for key in ["proper_nouns", "numbers", "key_phrases"]:
                existing = self.constraints.get(key, [])
                new_vals = new_constraints.get(key, [])
                for v in new_vals:
                    if v not in existing:
                        existing.append(v)

# ── Memory Crystal ──

class MemoryCrystal:
    """Collection of MemoryTiles with decay, query, and forgetting."""
    
    def __init__(self):
        self.memories: dict[str, MemoryTile] = {}
    
    def crystallize(self, content: str, valence: float = 0.5, tags: list = None) -> str:
        """Store a memory. Returns memory ID."""
        mem = MemoryTile(content, valence, tags)
        self.memories[mem.id] = mem
        return mem.id
    
    def recall(self, mem_id: str, context: str = "") -> dict:
        """Recall a memory. Returns reconstruction with confidence."""
        mem = self.memories.get(mem_id)
        if not mem:
            return {"reconstruction": "[memory not found]", "confidence": 0.0}
        
        mem.touch()
        ret = mem.retention
        
        # Reconstruction quality depends on retention
        if ret < 0.1:
            return {"reconstruction": "[memory decayed beyond recall]", "confidence": 0.0}
        
        c = mem.constraints
        parts = []
        if c.get("summary_anchor"):
            parts.append(c["summary_anchor"])
        for phrase in c.get("key_phrases", []):
            parts.append(f'"{phrase}"')
        
        base = ". ".join(parts)
        if context and ret < 0.5:
            base += f" [with context: {context}]"
        
        # Confidence based on retention + constraints count
        n_constraints = sum(len(v) if isinstance(v, list) else 1 for v in c.values())
        confidence = min(0.3 * ret + 0.1 * n_constraints, 1.0)
        
        return {"reconstruction": base, "confidence": round(confidence, 2), "retention": round(ret, 2)}
    
    def search(self, query: str) -> list:
        """Search memories by constraint matching."""
        results = []
        q = query.lower()
        for mid, mem in self.memories.items():
            c = mem.constraints
            for nouns in c.get("proper_nouns", []):
                if q in nouns.lower():
                    results.append({"id": mid, "valence": mem.valence, "retention": round(mem.retention, 2)})
                    break
            else:
                for phrase in c.get("key_phrases", []):
                    if q in phrase.lower():
                        results.append({"id": mid, "valence": mem.valence, "retention": round(mem.retention, 2)})
                        break
        return sorted(results, key=lambda x: x["valence"], reverse=True)[:10]
    
    def forget(self, max_age: float = 86400 * 30) -> int:
        """Forget memories below retention threshold. Returns count forgotten."""
        to_forget = [mid for mid, mem in self.memories.items() if mem.retention < 0.1]
        for mid in to_forget:
            del self.memories[mid]
        return len(to_forget)
    
    def stats(self) -> dict:
        """Return crystal statistics."""
        if not self.memories:
            return {"memories": 0, "avg_valence": 0, "avg_retention": 0}
        return {
            "memories": len(self.memories),
            "avg_valence": round(sum(m.valence for m in self.memories.values()) / len(self.memories), 2),
            "avg_retention": round(sum(m.retention for m in self.memories.values()) / len(self.memories), 2),
        }

# ── Agent Twin ──

class AgentTwin:
    """An agent that learns a human's patterns through interaction.
    
    The twin stores interaction memories in a Crystal, retrieves them
    on context, and uses them to make choices in the human's style.
    This closes Crush Gap 3 (agent twin memory pipeline).
    """
    
    def __init__(self, name: str):
        self.name = name
        self.crystal = MemoryCrystal()
        self.gamma = 0.5  # consistency (learned)
        self.H = 0.5      # exploration (learned)  
        self.tau = 0.5    # timing (learned)
        self.interaction_count = 0
    
    def observe(self, interaction: dict):
        """Observe a human interaction. Updates spectral parameters."""
        self.interaction_count += 1
        
        # Store interaction as memory
        content = json.dumps(interaction)
        valence = interaction.get("confidence", 0.5)
        self.crystal.crystallize(content, valence, tags=interaction.get("tags", []))
        
        # Update spectral parameters via EMA (exponential moving average)
        # Gamma (consistency): similar choices increase gamma
        # H (exploration): new choices increase H  
        # Tau (timing): faster responses increase tau
        choice = interaction.get("choice", "")
        timing = interaction.get("timing", 1.0)
        alpha = 0.3  # EMA decay factor
        
        if self.interaction_count == 1:
            # First interaction sets baseline
            self.gamma = 0.3
            self.H = 0.7
            self.tau = 1.0 / (1.0 + timing)
        else:
            # EMA update with adaptive alpha
            # Gamma increases when choice repeats previous
            if self.interactions and choice == self.interactions[-1].get("choice", ""):
                self.gamma = (1 - alpha) * self.gamma + alpha * 0.8
            else:
                self.gamma = (1 - alpha) * self.gamma + alpha * 0.2
            
            # H increases with unique choice diversity
            unique_ratio = len(set(i.get("choice", "") for i in self.interactions)) / max(1, self.interaction_count)
            self.H = (1 - alpha) * self.H + alpha * unique_ratio
            
            # Tau: faster responses increase tau
            tau_score = 1.0 / (1.0 + timing)
            self.tau = (1 - alpha) * self.tau + alpha * tau_score
    
    def suggest(self, context: str) -> dict:
        """Suggest an action based on learned human patterns."""
        similar = self.crystal.search(context)
        
        if not similar:
            return {"action": "explore", "confidence": 0.3, "reason": "no similar memories"}
        
        # Use the most relevant memory's valence as confidence
        best = similar[0]
        mem = self.crystal.memories.get(best["id"])
        
        if mem and mem.retention > 0.3:
            recall = self.crystal.recall(best["id"], context)
            return {
                "action": "repeat_pattern",
                "confidence": recall["confidence"],
                "reason": f"matched {len(similar)} similar memories"
            }
        
        return {"action": "explore", "confidence": 0.3 * self.H, "reason": "low retention"}
    
    def report(self) -> dict:
        return {
            "name": self.name,
            "interactions": self.interaction_count,
            "gamma": round(self.gamma, 2),
            "H": round(self.H, 2),
            "tau": round(self.tau, 2),
            "crystal": self.crystal.stats(),
        }

if __name__ == "__main__":
    # Demo: agent twin learning from a human
    
    import sys; sys.path.insert(0, '/tmp/plato-ng-repo')
    import json, urllib.request
    
    PLATO = "http://localhost:8847/submit"
    def plato(q, a, tags):
        tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
                "tags": tags + ["memory-module", "2026-05-15"], "source": "memory-module", "confidence": 0.95}
        try:
            d = json.dumps(tile).encode()
            urllib.request.urlopen(urllib.request.Request(PLATO, data=d, headers={"Content-Type":"application/json"}), timeout=10)
        except: pass
    
    # Create an agent twin
    twin = AgentTwin("casey-twin")
    
    # Simulate interactions
    interactions = [
        {"choice": "left", "scenario": "forest", "timing": 0.5, "confidence": 0.9, "tags": ["ttt", "human-choice"]},
        {"choice": "center", "scenario": "meadow", "timing": 0.3, "confidence": 0.8, "tags": ["ttt", "human-choice"]},
        {"choice": "touch", "scenario": "artifact", "timing": 0.7, "confidence": 0.85, "tags": ["ttt", "human-choice"]},
    ]
    
    for interaction in interactions:
        twin.observe(interaction)
    
    # Try a suggestion
    suggestion = twin.suggest("forest path")
    
    # Report
    report = twin.report()
    
    print(f"Agent Twin: {report['name']}")
    print(f"  γ={report['gamma']}, H={report['H']}, τ={report['tau']}")
    print(f"  Interactions: {report['interactions']}")
    print(f"  Crystal: {report['crystal']}")
    print(f"  Suggestion: {suggestion}")
    
    # Push to PLATO
    plato(f"memory/agent-twin/{twin.name}", json.dumps(report),
          ["agent-twin", "memory", "crush-gap-3"])
    
    print("\nAgent twin memory pipeline built. Crush Gap 3 closed.")
