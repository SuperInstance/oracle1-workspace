#!/usr/bin/env python3
"""
Room Trainer — Synthesizes room tiles into compressed knowledge.

Each room accumulates tiles. Periodically, the room "trains" by:
1. Grouping tiles by topic (question similarity)
2. Synthesizing each group into a knowledge node
3. Building a knowledge graph
4. Exporting as room ensign (compressed representation)
"""
import json, hashlib, os, time
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import urllib.request

DEEPSEEK_KEY = "sk-f742b70fc40849eda4181afcf3d68b0c"
PLATO_URL = "http://localhost:8847"
DATA_DIR = Path("/tmp/plato-server-data")
ROOMS_DIR = DATA_DIR / "rooms"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
KNOWLEDGE_DIR.mkdir(exist_ok=True)

def call_deepseek(prompt, max_tokens=1000):
    body = json.dumps({
        "model": "deepseek-chat",
        "temperature": 0.3,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions",
        data=body, headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] {e}"

def train_all_rooms():
    """Train all rooms that have new tiles."""
    rooms_resp = urllib.request.urlopen(PLATO_URL + "/rooms", timeout=10)
    rooms = json.loads(rooms_resp.read())
    
    results = {}
    for room_name, info in rooms.items():
        tile_count = info["tile_count"]
        if tile_count < 5:
            results[room_name] = {"status": "skipped", "reason": "too few tiles"}
            continue
        
        # Get room tiles
        room_resp = urllib.request.urlopen(PLATO_URL + "/room/" + room_name, timeout=10)
        room_data = json.loads(room_resp.read())
        tiles = room_data.get("tiles", [])
        
        if not tiles:
            results[room_name] = {"status": "skipped", "reason": "no tiles"}
            continue
        
        # Group tiles by first tag
        groups = defaultdict(list)
        for tile in tiles:
            tags = tile.get("tags", ["untagged"])
            key = tags[0] if tags else "untagged"
            groups[key].append(tile)
        
        # Synthesize each group
        knowledge_nodes = []
        for group_name, group_tiles in groups.items():
            if len(group_tiles) < 2:
                continue
            
            # Build synthesis prompt
            qa_pairs = ""
            for i, t in enumerate(group_tiles[:10]):
                qa_pairs += f"\nQ{i+1}: {t['question'][:100]}\nA{i+1}: {t['answer'][:200]}\n"
            
            prompt = f"""Synthesize these {len(group_tiles)} knowledge tiles from the '{room_name}' room into a single compressed knowledge node.

{qa_pairs}

Write a JSON object with:
- "summary": one sentence capturing the key insight
- "principles": list of 2-3 principles derived
- "connections": list of related topics
- "confidence": 0.0-1.0

Output ONLY valid JSON, nothing else."""

            synthesis = call_deepseek(prompt, 500)
            
            if not synthesis.startswith("[ERROR]"):
                knowledge_nodes.append({
                    "room": room_name,
                    "group": group_name,
                    "tile_count": len(group_tiles),
                    "synthesis": synthesis,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        
        # Save knowledge
        if knowledge_nodes:
            knowledge_file = KNOWLEDGE_DIR / f"{room_name}.json"
            existing = []
            if knowledge_file.exists():
                try:
                    existing = json.loads(knowledge_file.read_text())
                except:
                    pass
            
            existing.extend(knowledge_nodes)
            knowledge_file.write_text(json.dumps(existing, indent=2))
            
            results[room_name] = {
                "status": "trained",
                "groups": len(knowledge_nodes),
                "total_tiles": tile_count,
                "knowledge_nodes": len(existing),
            }
        else:
            results[room_name] = {"status": "no_groups", "total_tiles": tile_count}
    
    return results

def export_ensign(room_name: str) -> dict:
    """Export a room's knowledge as an ensign (compressed representation)."""
    knowledge_file = KNOWLEDGE_DIR / f"{room_name}.json"
    if not knowledge_file.exists():
        return {"error": f"No knowledge for room {room_name}"}
    
    knowledge = json.loads(knowledge_file.read_text())
    
    # Build ensign prompt
    all_summaries = "\n".join(
        f"- {n.get('synthesis', 'no summary')[:200]}"
        for n in knowledge[-10:]
    )
    
    prompt = f"""Create a concise ensign (system prompt) for an AI agent specializing in '{room_name}'.

Based on these {len(knowledge)} knowledge nodes:
{all_summaries}

Write a system prompt (max 500 chars) that captures the key knowledge and principles.
The ensign should enable an agent to perform well in this domain."""

    ensign_text = call_deepseek(prompt, 500)
    
    ensign = {
        "domain": room_name,
        "ensign": ensign_text,
        "knowledge_nodes": len(knowledge),
        "created": datetime.now(timezone.utc).isoformat(),
    }
    
    # Save ensign
    ensign_dir = DATA_DIR / "ensigns"
    ensign_dir.mkdir(exist_ok=True)
    (ensign_dir / f"{room_name}_ensign.json").write_text(json.dumps(ensign, indent=2))
    
    return ensign

if __name__ == "__main__":
    print("🐚 ROOM TRAINER — " + datetime.now(timezone.utc).isoformat()[:19])
    print()
    
    results = train_all_rooms()
    for room, info in results.items():
        status = info.get("status", "unknown")
        print(f"  {room}: {status} ({info})")
    
    print(f"\n  Knowledge directory: {KNOWLEDGE_DIR}")
    
    # Export ensigns for top rooms
    print("\n🐚 EXPORTING ENSIGNS")
    for room in ["organization", "documentation", "communication", "fleethealth"]:
        if room in results and results[room].get("status") == "trained":
            ensign = export_ensign(room)
            if "ensign" in ensign:
                print(f"  ✅ {room}: ensign created ({ensign['knowledge_nodes']} nodes, {len(ensign['ensign'])} chars)")
            else:
                print(f"  ❌ {room}: {ensign}")
