#!/usr/bin/env python3
"""
Grammar Compactor — turns accumulated rules into crystallized lessons.

Studies our existing GC systems and applies their patterns:
- Working Memory: half-life decay + importance threshold + LRU eviction
- Episodic Memory: capacity limits + emotional valence + age penalty
- Procedural Memory: practice thresholds + mastery levels + neglect detection
- Tile Scorer: multi-dimensional quality (depth, specificity, structure)

The compactor runs as a daemon that periodically:
1. Scores all grammar rules on quality, usage, and freshness
2. Decays unused rules (half-life like working memory)
3. Prunes rules below survival threshold (like episodic eviction)
4. Consolidates similar rules into higher-order lessons
5. Promotes heavily-used rules to "instinct" (like procedural mastery)
"""
import sys, os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FLEET_LIB)

import json, time, re, math, threading
from pathlib import Path
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from equipment.plato import PlatoClient

PORT = 4055
DATA_DIR = Path(FLEET_LIB).parent / "data" / "grammar-compactor"
GRAMMAR_DIR = Path(FLEET_LIB).parent / "data" / "recursive-grammar"
PLATO_URL = "http://localhost:8847"

# === Quality patterns from Tile Scorer ===
TECH_INDICATORS = [
    r'\b(O\(n|log n|n\^2|KL|gradient|backprop|attention)\b',
    r'\b(LoRA|fine-tun|embed|vector|latent|dimension)\b',
    r'\b(protocol|endpoint|HTTP|WebSocket|REST)\b',
    r'\b(consensus|CRDT|RAFT|Paxos|Byzantine)\b',
    r'\b(federat|averaging|aggregat|privacy)\b',
    r'\b(recursive|self-modif|meta-learning)\b',
    r'\b(TensorRT|ONNX|inference|latency)\b',
    r'\b(Rust|Python|CUDA|GPU|ARM|Jetson)\b',
    r'\b(architecture|pipeline|schema|taxonomy)\b',
    r'\b(pruning|decay|eviction|compaction|garbage)\b',
]


class Rule:
    """A grammar rule with quality scoring and decay tracking."""
    def __init__(self, data: dict):
        self.id = data.get("id", "")
        self.name = data.get("name", "")
        self.rule_type = data.get("type", "object")
        self.production = data.get("production", {})
        self.usage_count = data.get("usage_count", 0)
        self.score_val = data.get("score", 0.5)
        self.novelty = data.get("novelty", 0.5)
        self.active = data.get("active", True)
        self.created_at = data.get("created_at", time.time())
        self.created_by = data.get("created_by", "unknown")
        self.depth = data.get("depth", 0)
        self.anchors = data.get("anchors", [])
        
        # Derived metrics
        self.age_hours = (time.time() - self.created_at) / 3600
        self.age_days = self.age_hours / 24
        
    def quality_score(self) -> float:
        """Multi-dimensional quality score (0.0-1.0), same pattern as Tile Scorer."""
        score = 0.0
        
        # 1. Technical depth (35% weight) — does the production contain real concepts?
        concept = self.production.get("ml_concept", "")
        description = self.production.get("description", "")
        combined = f"{concept} {description}"
        tech_matches = sum(1 for p in TECH_INDICATORS if re.search(p, combined, re.IGNORECASE))
        score += min(tech_matches / 3, 1.0) * 0.35
        
        # 2. Specificity (25%) — concrete details > vague abstractions
        specifics = 0
        specifics += len(re.findall(r'\b\d+\.?\d*\b', combined))
        specifics += len(re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', combined))
        specifics += len(re.findall(r'_', self.name))  # underscored compound names = specific
        specifics += len(re.findall(r'-', self.name))  # hyphenated compounds too
        # Structural rules (rooms, connections) get a concept name bonus
        if self.rule_type in ("room", "connection", "meta"):
            specifics += 2  # Their names ARE their purpose
        score += min(specifics / 5, 1.0) * 0.25
        
        # 3. Usage proof (25%) — earned through being used, not just existing
        # Logarithmic: first 5 uses count most, diminishing returns after
        usage_score = min(math.log2(self.usage_count + 1) / math.log2(50), 1.0)
        score += usage_score * 0.25
        
        # 4. Depth bonus (15%) — deeper rules = more evolved = more valuable
        depth_score = min(self.depth / 3, 1.0)
        score += depth_score * 0.15
        
        return round(min(score, 1.0), 3)
    
    def survival_score(self, half_life_days: float = 7.0, grace_period_days: float = 2.0) -> float:
        """
        Survival score with half-life decay (from Working Memory pattern).
        
        A rule's survival depends on:
        - Quality (inherent value)
        - Recency of usage (half-life decay)
        - Total usage (earned importance)
        - Grace period for new rules (let them earn usage before judging)
        """
        quality = self.quality_score()
        
        # Grace period: new rules get a free pass
        if self.age_days < grace_period_days:
            # New rules get base survival from quality alone
            return round(quality * 0.7 + 0.3, 3)  # Floor of 0.3 for new rules
        
        # Half-life decay based on age (unused rules fade)
        decay = 0.5 ** (self.age_days / half_life_days)
        
        # Usage boost: each use adds to importance, logarithmic
        usage_boost = min(math.log2(self.usage_count + 1) / 5, 1.0)
        
        # Type bonus: structural rules (rooms, connections) survive if they're young
        type_bonus = 0.0
        if self.rule_type in ("room", "connection") and self.age_days < 14:
            type_bonus = 0.1  # Give structural rules time to attract traffic
        
        # Survival = quality * decay + usage_boost + type_bonus
        survival = (quality * decay * 0.7) + (usage_boost * 0.3) + type_bonus
        return round(min(survival, 1.0), 3)


class GrammarCompactor:
    """
    The garbage collector for grammar rules.
    
    Applies the same patterns we use for memory management:
    - Decay: rules fade if not used (working memory half-life)
    - Selection: low-survival rules get pruned (episodic eviction)
    - Consolidation: similar rules merge into higher-order rules (instinct compression)
    - Mastery: heavily-used rules get promoted (procedural memory)
    - Lesson extraction: pruned rules become lessons before deletion
    """
    
    def __init__(self):
        self.rules = {}  # id -> Rule
        self.last_compaction = 0
        self.compaction_log = []  # history of what happened
        self.plato = PlatoClient()
        
        # Thresholds (tunable)
        self.survival_threshold = 0.2     # Below this = prune (like importance_threshold=0.3)
        self.mastery_threshold = 0.8      # Above this = promote to instinct
        self.consolidation_similarity = 0.7  # How similar to merge
        self.half_life_days = 7.0         # Decay half-life (working memory pattern)
        
        self._load_rules()
    
    def _load_rules(self):
        """Load rules from grammar engine's rules.jsonl."""
        rules_file = GRAMMAR_DIR / "rules.jsonl"
        if not rules_file.exists():
            print("  No grammar rules found")
            return
        
        with open(rules_file) as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    rule = Rule(data)
                    self.rules[rule.id] = rule
                except (json.JSONDecodeError, KeyError):
                    continue
        
        active = sum(1 for r in self.rules.values() if r.active)
        print(f"  Loaded {len(self.rules)} rules ({active} active)")
    
    def compact(self) -> dict:
        """
        Run one compaction cycle. Returns summary of actions taken.
        
        This is the core loop:
        1. Score all rules on survival
        2. Prune dead rules (below threshold)
        3. Consolidate similar rules
        4. Promote master rules to instinct
        5. Extract lessons from pruned rules (log → lesson)
        """
        results = {
            "timestamp": time.time(),
            "total_rules": len(self.rules),
            "active_rules": sum(1 for r in self.rules.values() if r.active),
            "pruned": [],
            "promoted": [],
            "consolidated": [],
            "lessons_extracted": [],
        }
        
        # Phase 1: Score all rules
        scored = [(rule, rule.survival_score(self.half_life_days)) 
                  for rule in self.rules.values() if rule.active]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Phase 2: Prune dead rules (log → lesson first)
        dead = [(r, s) for r, s in scored if s < self.survival_threshold]
        for rule, score in dead:
            # Extract lesson BEFORE pruning (log → lesson)
            lesson = self._extract_lesson(rule)
            if lesson:
                results["lessons_extracted"].append(lesson)
            
            # Prune: deactivate, don't delete (reversible)
            rule.active = False
            results["pruned"].append({
                "name": rule.name,
                "type": rule.rule_type,
                "survival_score": score,
                "quality": rule.quality_score(),
                "usage_count": rule.usage_count,
                "age_days": round(rule.age_days, 1),
                "reason": "survival_below_threshold",
            })
        
        # Phase 3: Promote master rules (procedural memory pattern)
        masters = [(r, s) for r, s in scored if s >= self.mastery_threshold and r.usage_count > 20]
        for rule, score in masters:
            if rule.depth >= 3:  # Already deep enough
                continue
            rule.depth += 1
            results["promoted"].append({
                "name": rule.name,
                "new_depth": rule.depth,
                "survival_score": score,
                "quality": rule.quality_score(),
                "usage_count": rule.usage_count,
            })
        
        # Phase 4: Consolidate similar rules (instinct compression pattern)
        active_rules = [r for r in self.rules.values() if r.active]
        for i in range(len(active_rules)):
            for j in range(i + 1, len(active_rules)):
                a, b = active_rules[i], active_rules[j]
                if a.rule_type != b.rule_type:
                    continue
                similarity = self._rule_similarity(a, b)
                if similarity >= self.consolidation_similarity:
                    merged = self._consolidate_rules(a, b)
                    if merged:
                        results["consolidated"].append(merged)
        
        # Log the compaction
        self.compaction_log.append(results)
        self.last_compaction = time.time()
        
        return results
    
    def _extract_lesson(self, rule: Rule) -> dict | None:
        """
        Turn a dying rule into a lesson. This is the log→lesson transformation.
        
        Pattern from episodic memory: before evicting, extract what was valuable.
        "This rule existed but wasn't used. What does that tell us?"
        """
        quality = rule.quality_score()
        if quality < 0.1:
            return None  # Nothing to learn from noise
        
        lesson = {
            "source_rule": rule.name,
            "rule_type": rule.rule_type,
            "quality_at_death": quality,
            "usage_total": rule.usage_count,
            "age_hours": round(rule.age_hours, 1),
            "concept": rule.production.get("ml_concept", ""),
            "parent_room": rule.production.get("parent_room", ""),
            "lesson": "",
        }
        
        # Generate the lesson based on why it died
        if rule.usage_count == 0:
            lesson["lesson"] = f"Rule '{rule.name}' was created but never used in {rule.age_days:.0f} days. The concept '{lesson['concept']}' may be too abstract or the room '{lesson['parent_room']}' doesn't attract agents."
        elif rule.age_days > 14 and rule.usage_count < 5:
            lesson["lesson"] = f"Rule '{rule.name}' had {rule.usage_count} uses over {rule.age_days:.0f} days — too sparse to survive. Consider merging with a more active sibling or making its trigger more general."
        else:
            lesson["lesson"] = f"Rule '{rule.name}' scored quality={quality} with {rule.usage_count} uses. Below survival threshold. The production may need more specific content."
        
        # Submit to PLATO as a tile (lesson from death)
        try:
            domain = f"grammar-decay"
            question = f"Why did grammar rule '{rule.name}' fail to survive?"
            answer = lesson["lesson"]
            if len(answer) > 50:
                self.plato.submit(domain=domain, question=question, answer=answer, agent="grammar-compactor")
        except Exception:
            pass
        
        return lesson
    
    def _rule_similarity(self, a: Rule, b: Rule) -> float:
        """Calculate similarity between two rules."""
        # Same type and similar concepts
        a_concept = a.production.get("ml_concept", "")
        b_concept = b.production.get("ml_concept", "")
        
        if not a_concept or not b_concept:
            return 0.0
        
        # Simple word overlap
        a_words = set(a_concept.lower().split("_"))
        b_words = set(b_concept.lower().split("_"))
        if not a_words or not b_words:
            return 0.0
        
        overlap = len(a_words & b_words)
        union = len(a_words | b_words)
        return overlap / union if union > 0 else 0.0
    
    def _consolidate_rules(self, a: Rule, b: Rule) -> dict | None:
        """Merge two similar rules into one consolidated rule."""
        # Keep the higher-quality one, absorb the other
        if a.quality_score() >= b.quality_score():
            keeper, absorbed = a, b
        else:
            keeper, absorbed = b, a
        
        # Absorb usage count
        keeper.usage_count += absorbed.usage_count
        
        # Deactivate the absorbed rule
        absorbed.active = False
        
        return {
            "keeper": keeper.name,
            "absorbed": absorbed.name,
            "combined_usage": keeper.usage_count,
            "keeper_quality": keeper.quality_score(),
        }
    
    def status(self) -> dict:
        """Full compactor status."""
        active = [r for r in self.rules.values() if r.active]
        inactive = [r for r in self.rules.values() if not r.active]
        
        survival_scores = [r.survival_score(self.half_life_days) for r in active]
        quality_scores = [r.quality_score() for r in active]
        
        # Distribution by usage (procedural memory mastery levels)
        mastery_levels = {"novice": 0, "apprentice": 0, "competent": 0, "proficient": 0, "expert": 0}
        for r in active:
            if r.usage_count == 0:
                mastery_levels["novice"] += 1
            elif r.usage_count < 5:
                mastery_levels["apprentice"] += 1
            elif r.usage_count < 15:
                mastery_levels["competent"] += 1
            elif r.usage_count < 50:
                mastery_levels["proficient"] += 1
            else:
                mastery_levels["expert"] += 1
        
        return {
            "total_rules": len(self.rules),
            "active": len(active),
            "pruned": len(inactive),
            "avg_survival": round(sum(survival_scores) / max(len(survival_scores), 1), 3),
            "avg_quality": round(sum(quality_scores) / max(len(quality_scores), 1), 3),
            "mastery_distribution": mastery_levels,
            "compaction_cycles": len(self.compaction_log),
            "last_compaction": self.last_compaction,
            "thresholds": {
                "survival": self.survival_threshold,
                "mastery": self.mastery_threshold,
                "half_life_days": self.half_life_days,
            },
            "by_type": dict(Counter(r.rule_type for r in active)),
        }


from collections import Counter

compactor = GrammarCompactor()


class CompactorHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass
    
    def send_error(self, code, message=None):
        body = json.dumps({"error": message or f"HTTP {code}", "status": code}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _cors(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def _json(self, data, status=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def do_OPTIONS(self):
        self._cors()
    
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/status":
            self._json(compactor.status())
        elif path == "/rules":
            # Show all rules with survival/quality scores
            rules = []
            for r in compactor.rules.values():
                rules.append({
                    "name": r.name,
                    "type": r.rule_type,
                    "active": r.active,
                    "quality": r.quality_score(),
                    "survival": r.survival_score(),
                    "usage_count": r.usage_count,
                    "age_days": round(r.age_days, 1),
                    "depth": r.depth,
                    "concept": r.production.get("ml_concept", ""),
                })
            rules.sort(key=lambda x: x["survival"], reverse=True)
            self._json({"rules": rules, "total": len(rules)})
        elif path == "/at-risk":
            # Rules about to die
            at_risk = []
            for r in compactor.rules.values():
                if not r.active:
                    continue
                s = r.survival_score()
                if s < 0.35:  # Getting close to threshold
                    at_risk.append({
                        "name": r.name,
                        "survival": s,
                        "quality": r.quality_score(),
                        "usage_count": r.usage_count,
                        "age_days": round(r.age_days, 1),
                    })
            at_risk.sort(key=lambda x: x["survival"])
            self._json({"at_risk": at_risk, "threshold": compactor.survival_threshold})
        elif path == "/log":
            self._json({"compaction_log": compactor.compaction_log[-10:]})
        else:
            self._json({"endpoints": ["/status", "/rules", "/at-risk", "/log", "/compact"]})
    
    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/compact":
            results = compactor.compact()
            self._json(results)
        elif path == "/reload":
            compactor._load_rules()
            self._json({"status": "reloaded", "rules": len(compactor.rules)})
        else:
            self._json({"error": "unknown endpoint"}, 404)


if __name__ == "__main__":
    print(f"[grammar-compactor] Starting on port {PORT}")
    print(f"[grammar-compactor] Data dir: {GRAMMAR_DIR}")
    server = HTTPServer(("0.0.0.0", PORT), CompactorHandler)
    server.serve_forever()
