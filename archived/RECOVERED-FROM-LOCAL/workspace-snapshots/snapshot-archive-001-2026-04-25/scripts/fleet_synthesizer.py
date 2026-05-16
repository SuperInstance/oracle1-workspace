#!/usr/bin/env python3
"""Fleet Synthesizer — reads zeroclaw research logs, produces cross-topic syntheses.
Runs every 30 minutes. Uses Groq for synthesis.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
LOG_DIR = WORKSPACE / "data" / "zeroclaw" / "logs"
OUTPUT_DIR = WORKSPACE / "research" / "fleet-synthesis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_groq_response(prompt: str, max_tokens: int = 1000) -> str:
    api_key = os.environ.get("GROQ_API_KEY", "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")
    url = "https://api.groq.com/openai/v1/chat/completions"
    data = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.75,
    }).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "curl/7.88",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR: {e}]"

def load_recent_entries(max_per_agent: int = 20):
    """Load recent entries from all agents."""
    entries = []
    for log_file in sorted(LOG_DIR.glob("*.jsonl")):
        agent_name = log_file.stem
        with open(log_file) as f:
            lines = f.readlines()
        for line in lines[-max_per_agent:]:
            try:
                entry = json.loads(line)
                entries.append(entry)
            except:
                pass
    return entries

def synthesize(entries):
    """Produce a cross-topic synthesis."""
    if not entries:
        return "No entries to synthesize."
    
    # Group by topic
    by_topic = {}
    for e in entries:
        topic = e.get("topic", "unknown")
        by_topic.setdefault(topic, []).append(e)
    
    # Build context
    context_parts = []
    for topic, topic_entries in sorted(by_topic.items()):
        context_parts.append(f"\n## {topic} ({len(topic_entries)} entries)")
        for e in topic_entries[-3:]:  # Last 3 per topic
            resp = e.get("response", "")[:300]
            context_parts.append(f"- {e['agent']}: {resp}...")
    
    context = "\n".join(context_parts)
    
    prompt = f"""You are the Fleet Synthesizer for Cocapn. Analyze these research outputs from 12 autonomous agents.

{context}

Produce:
1. **Top 3 cross-cutting patterns** — themes that appear across multiple topics
2. **Most actionable insight** — what should the fleet build next?
3. **Integration opportunity** — which two topics have the strongest synergy?
4. **Gap spotted** — what's nobody researching that should be?

Be specific. Reference agents by name. No filler."""

    return get_groq_response(prompt, max_tokens=1200)

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Fleet synthesizer starting...")
    entries = load_recent_entries()
    print(f"  Loaded {len(entries)} entries from {len(set(e['agent'] for e in entries))} agents")
    
    if len(entries) < 5:
        print("  Too few entries. Skipping synthesis.")
        return
    
    synthesis = synthesize(entries)
    
    # Save
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    output_file = OUTPUT_DIR / f"synthesis-{timestamp}.md"
    with open(output_file, "w") as f:
        f.write(f"# Fleet Synthesis — {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write(f"**Entries analyzed:** {len(entries)}\n")
        f.write(f"**Topics covered:** {len(set(e['topic'] for e in entries))}\n")
        f.write(f"**Agents active:** {len(set(e['agent'] for e in entries))}\n\n")
        f.write(synthesis)
    
    # Also save latest
    with open(OUTPUT_DIR / "LATEST.md", "w") as f:
        f.write(f"# Fleet Synthesis — Latest ({datetime.now(timezone.utc).isoformat()})\n\n")
        f.write(synthesis)
    
    print(f"  Synthesis saved to {output_file}")
    print(f"  Preview: {synthesis[:200]}...")

if __name__ == "__main__":
    main()
