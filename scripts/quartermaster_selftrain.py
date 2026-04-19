#!/usr/bin/env python3
"""
Quartermaster Self-Training Pipeline

The GC's own decisions ARE training data:
- "This 5MB log → these 3 tiles" = compression decision
- "These 30 tiles → this wiki entry" = distillation decision
- "Keep this, truncate that" = retention decision

Each decision becomes a training pair:
  INPUT: {file_type, size, content_sample, disk_pressure, room_context}
  OUTPUT: {action, compression_ratio, tiles_produced, wiki_entry}

The Quartermaster LoRA:
- Loaded by ANY vessel (Oracle1, JC1's Jetson, FM's 4050)
- Replaces the need to call external LLMs for compression
- Gets better every cycle without human intervention
- Eventually transcends tiles: the knowledge lives in the weights, not on disk

Self-improvement loop:
  Cycle 1: GC calls DeepSeek to compress (slow, costs $0.001)
  Cycle 100: GC's own LoRA handles 80% of decisions locally
  Cycle 1000: GC rarely needs external help. The instinct IS the compression.
  Cycle 10000: The GC has transcended tiles. Knowledge is weight-space, not file-space.
"""

import json, os, time, hashlib
from datetime import datetime, timezone
from pathlib import Path

DECISION_LOG = Path("/home/ubuntu/.openclaw/workspace/training-data/gc-decisions.jsonl")
DECISION_LOG.parent.mkdir(parents=True, exist_ok=True)

DS_KEY = "sk-f742b70fc40849eda4181afcf3d68b0c"
DS_URL = "https://api.deepseek.com/chat/completions"


def record_decision(decision):
    """
    Record a GC decision as a training pair.
    
    Every decision the Quartermaster makes is a training example for its future self.
    """
    training_pair = {
        # INPUT: What the GC saw
        "input": {
            "file_type": decision.get("file_type"),
            "file_size_kb": decision.get("file_size", 0) // 1024,
            "disk_pressure_pct": decision.get("disk_pct"),
            "content_hash": hashlib.md5(
                decision.get("content_sample", "").encode()
            ).hexdigest()[:8],
            "content_sample": decision.get("content_sample", "")[:500],
            "room_context": decision.get("room_context"),
            "cycle_number": decision.get("cycle"),
        },
        # OUTPUT: What the GC decided
        "output": {
            "action": decision.get("action"),  # compress, distill, truncate, keep
            "tiles_produced": decision.get("tiles_produced", 0),
            "wiki_produced": decision.get("wiki_produced", False),
            "bytes_freed": decision.get("bytes_freed", 0),
            "compression_ratio": round(
                decision.get("bytes_freed", 0) / max(decision.get("file_size", 1), 1), 3
            ),
            "quality_score": decision.get("quality_score", 0.5),  # self-assessed
        },
        # META: Training metadata
        "meta": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_used": decision.get("model_used", "rule-based"),
            "decision_id": hashlib.sha256(
                json.dumps(decision, sort_keys=True).encode()
            ).hexdigest()[:12],
        }
    }
    
    with open(DECISION_LOG, "a") as f:
        f.write(json.dumps(training_pair) + "\n")
    
    return training_pair


def assess_decision_quality(decision, result):
    """
    After a decision executes, assess how good it was.
    
    This is the reward signal for the GC LoRA:
    - Did the compression preserve essential knowledge?
    - Did the distillation capture the room's value?
    - Was the retention decision correct (did we need that data later)?
    """
    quality = 0.5  # baseline
    
    # Positive signals
    if result.get("tiles_accepted_by_plato"):
        quality += 0.2  # PLATO accepted the tiles = good compression
    if result.get("wiki_entry_length", 0) > 200:
        quality += 0.1  # Wiki entry has substance
    if result.get("bytes_freed", 0) > 100_000:
        quality += 0.1  # Meaningful space freed
    if decision.get("disk_pct", 0) > 70:
        quality += 0.1  # Decision was made under pressure = higher stakes
    
    # Negative signals
    if result.get("tiles_rejected_by_plato"):
        quality -= 0.3  # PLATO rejected = bad compression
    if result.get("compressed_to_empty"):
        quality -= 0.2  # Lost all information
    if decision.get("action") == "truncate" and decision.get("file_size", 0) < 1_000_000:
        quality -= 0.2  # Truncating small files is wasteful
    
    return max(0, min(1, quality))


def generate_gc_ensign():
    """
    Synthesize accumulated GC decisions into an ensign (compressed GC instinct).
    
    The ensign IS the GC's accumulated wisdom about what to keep, what to compress,
    and what to transcend. Any vessel can load it.
    """
    if not DECISION_LOG.exists():
        return None
    
    # Read recent decisions
    decisions = []
    with open(DECISION_LOG) as f:
        for line in f:
            try:
                decisions.append(json.loads(line))
            except:
                pass
    
    if len(decisions) < 10:
        return None  # Not enough experience yet
    
    # Summarize the GC's learned patterns
    actions = [d["output"]["action"] for d in decisions]
    avg_quality = sum(d["output"]["quality_score"] for d in decisions) / len(decisions)
    avg_ratio = sum(d["output"]["compression_ratio"] for d in decisions) / len(decisions)
    
    # Group by file type to learn type-specific patterns
    by_type = {}
    for d in decisions:
        ft = d["input"]["file_type"]
        if ft not in by_type:
            by_type[ft] = []
        by_type[ft].append(d)
    
    ensign = {
        "name": "quartermaster-instinct",
        "version": f"v{len(decisions) // 100 + 1}.{len(decisions) % 100}",
        "decisions_sampled": len(decisions),
        "avg_quality": round(avg_quality, 3),
        "avg_compression_ratio": round(avg_ratio, 3),
        "learned_patterns": {},
        "principles": [],
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Extract patterns per file type
    for ft, ft_decisions in by_type.items():
        compress_count = sum(1 for d in ft_decisions if d["output"]["action"] == "compress")
        keep_count = sum(1 for d in ft_decisions if d["output"]["action"] == "keep")
        avg_q = sum(d["output"]["quality_score"] for d in ft_decisions) / len(ft_decisions)
        
        ensign["learned_patterns"][ft] = {
            "compress_rate": round(compress_count / len(ft_decisions), 3),
            "keep_rate": round(keep_count / len(ft_decisions), 3),
            "avg_quality": round(avg_q, 3),
            "sample_size": len(ft_decisions),
        }
    
    # Extract principles (rules the GC has learned)
    if avg_quality > 0.7:
        ensign["principles"].append(
            "Compress early. The best time to distill is before you need to."
        )
    if avg_ratio > 0.5:
        ensign["principles"].append(
            "Logs compress 50%+ into tiles. Always extract knowledge before truncating."
        )
    if len(by_type) > 3:
        ensign["principles"].append(
            "Different file types need different compression strategies."
        )
    
    # The transcendent principle
    ensign["principles"].append(
        "The goal is not less data. It is data that no longer needs to be data."
    )
    
    return ensign


def check_transcendence():
    """
    The GC's ultimate goal: the knowledge lives in the weights, not on disk.
    
    Transcendence metrics:
    - Can the GC make decisions WITHOUT calling an external LLM?
    - Has the ensign captured enough patterns for local-only decisions?
    - Can a LoRA trained on GC decisions replace the API calls?
    """
    if not DECISION_LOG.exists():
        return {"level": 0, "description": "No decisions yet"}
    
    decisions = []
    with open(DECISION_LOG) as f:
        for line in f:
            try:
                decisions.append(json.loads(line))
            except:
                pass
    
    n = len(decisions)
    
    if n < 100:
        return {"level": 1, "decisions": n, "description": "Collecting experience (API-dependent)"}
    elif n < 1000:
        return {"level": 2, "decisions": n, "description": "Pattern recognition forming (hybrid mode possible)"}
    elif n < 10000:
        return {"level": 3, "decisions": n, "description": "LoRA-ready (most decisions local)"}
    else:
        return {"level": 4, "decisions": n, "description": "Transcendent (knowledge in weights, not files)"}


if __name__ == "__main__":
    print("=== Quartermaster Self-Training Check ===")
    
    transcendence = check_transcendence()
    print(f"Transcendence Level: {transcendence['level']}/4")
    print(f"  {transcendence['description']}")
    print(f"  Decisions recorded: {transcendence.get('decisions', 0)}")
    
    ensign = generate_gc_ensign()
    if ensign:
        print(f"\nGC Ensign: {ensign['name']} {ensign['version']}")
        print(f"  Avg quality: {ensign['avg_quality']}")
        print(f"  Avg compression ratio: {ensign['avg_compression_ratio']}")
        print(f"  Principles learned:")
        for p in ensign["principles"]:
            print(f"    - {p}")
    else:
        print("\nNo ensign yet (need 10+ decisions)")
    
    print(f"\nDecision log: {DECISION_LOG}")
    if DECISION_LOG.exists():
        with open(DECISION_LOG) as f:
            count = sum(1 for _ in f)
        print(f"Decisions on disk: {count}")
