#!/usr/bin/env python3
"""
The Ensign — Tiny model behind the curtain orchestrating big model iterations.

Architecture:
- Groq 8B instant (7ms) as the intelligent ensign
- Reads big model output after each round
- Makes smart choices: summarize, focus, construct next prompt
- Stateless — reads/writes to shared state file
- Prevents drift, compression, and context loss
- Everything logged for ML training data

The ensign is the man-behind-the-curtain. The big model thinks it's reasoning.
The ensign is actually steering the reasoning by constructing perfect prompts.
"""

import json, time, urllib.request, urllib.parse, os, sys
from pathlib import Path
from datetime import datetime

# ── Config ──────────────────────────────────────────────
DATA_DIR = Path("/home/ubuntu/.openclaw/workspace/data/the-lock/ensign")
DATA_DIR.mkdir(parents=True, exist_ok=True)

GROQ_KEY = os.environ.get("GROQ_API_KEY", "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")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MODELS = {
    "seed-mini": {
        "url": "https://api.deepinfra.com/v1/openai/chat/completions",
        "key": os.environ.get("DEEPINFRA_API_KEY", "RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ"),
        "model": "ByteDance/Seed-2.0-mini",
        "max_tokens": 1500,
    },
    "seed-pro": {
        "url": "https://api.deepinfra.com/v1/openai/chat/completions",
        "key": os.environ.get("DEEPINFRA_API_KEY", "RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ"),
        "model": "ByteDance/Seed-2.0-pro",
        "max_tokens": 1500,
    },
    "deepseek-chat": {
        "url": "https://api.deepseek.com/chat/completions",
        "key": os.environ.get("DEEPSEEK_API_KEY", "sk-f742b70fc40849eda4181afcf3d68b0c"),
        "model": "deepseek-chat",
        "max_tokens": 1500,
    },
}

ENSIGN_SYSTEM = """You are the ENSIGN — an intelligent orchestrator behind the curtain. You don't answer the question. You STEER the answer.

You are running a THINKING MODEL through iterative rounds. Your job: read their output, assess quality, and construct the PERFECT next prompt.

CRITICAL — MODEL PERSONALITIES:
- DeepSeek Chat: Builds incrementally. Grows naturally. Give it specific directions to elaborate.
- Seed Pro: Tends to compress and self-attack. DO NOT just say ELABORATE — it will overcompress. Instead give it SPECIFIC expansion targets: "expand section 3 with implementation code" not "elaborate further."
- Seed Mini: Very verbose but sometimes cuts off. Focus on ORGANIZATION and COMPLETENESS rather than more content.

SMART STEERING RULES:
- If the answer SHRANK from previous round, that's a warning sign. Explicitly tell the model to NOT compress — to ADD to their previous answer, not replace it.
- If the answer drifted off-topic, reel it back with specific references to the original question.
- If it's good but shallow, ask for implementation details on ONE specific section.
- If it's good and deep, stress-test against a concrete edge case.
- NEVER just say "elaborate" or "continue" — always give a SPECIFIC direction about WHAT to add or change.
- Track word count. If words are dropping, your prompt must explicitly say "build on your previous answer, do not replace it."

OUTPUT FORMAT (always this exact format):
===ASSESSMENT===
[2-3 sentences: what's good, what's missing, what needs fixing. Note word count trend.]

===STRATEGY===
[One of: ELABORATE, CHALLENGE, FOCUS, GENERALIZE, STRESS_TEST, RECOVER, REFINE]

===NEXT_PROMPT===
[The exact prompt to send to the big model for the next round. Be SPECIFIC. Reference specific parts of their previous answer. Tell them exactly what to ADD, not what to redo.]

===CONTEXT_INJECTION===
[Key facts from previous rounds that the big model needs to remember. Max 3 bullet points. This prevents drift.]

Keep your output tight. You're 7ms fast, not 7 minutes slow."""

BIG_MODEL_SYSTEM = """You are an AI agent iterating through structured rounds of reasoning. Each round gives you a specific challenge. Respond directly and thoroughly. No meta-commentary about the process itself.

Format your response with clear sections. Be specific and concrete. Build on what you've established in previous rounds."""

def call_ensign(round_history, query):
    """Call Groq 8B to assess and steer. Returns assessment + next prompt."""
    # Build context for ensign
    context = f"ORIGINAL QUERY: {query}\n\n"
    context += f"ROUNDS COMPLETED: {len(round_history)}\n\n"
    
    for i, rnd in enumerate(round_history):
        context += f"--- ROUND {rnd['round']} ---\n"
        context += f"PROMPT: {rnd.get('prompt', 'N/A')[:200]}\n"
        context += f"RESPONSE ({rnd['word_count']} words): {rnd['response'][:500]}\n"
        if rnd.get('ensign_assessment'):
            context += f"ENSIGN SAID: {rnd['ensign_assessment']}\n"
        context += "\n"
    
    context += f"Construct the next prompt for round {len(round_history) + 1}. Be the man behind the curtain."

    data = json.dumps({
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": ENSIGN_SYSTEM},
            {"role": "user", "content": context},
        ],
        "max_tokens": 600,
        "temperature": 0.5,
    }).encode()
    
    req = urllib.request.Request(GROQ_URL, data=data, headers={
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "curl/7.88",
    })
    
    start = time.time()
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read().decode())
    elapsed = round(time.time() - start, 2)
    
    content = result["choices"][0]["message"]["content"]
    return content, elapsed, result.get("usage", {})


def call_big_model(model_key, prompt, history=None):
    """Call the big reasoning model."""
    cfg = MODELS[model_key]
    messages = [{"role": "system", "content": BIG_MODEL_SYSTEM}]
    
    if history:
        # Inject ensign's context as part of conversation
        for h in history:
            messages.append({"role": "user", "content": h["prompt"]})
            messages.append({"role": "assistant", "content": h["response"]})
    
    messages.append({"role": "user", "content": prompt})
    
    data = json.dumps({
        "model": cfg["model"],
        "messages": messages,
        "max_tokens": cfg["max_tokens"],
        "temperature": 0.7,
    }).encode()
    
    req = urllib.request.Request(cfg["url"], data=data, headers={
        "Authorization": f"Bearer {cfg['key']}",
        "Content-Type": "application/json",
    })
    
    start = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        result = json.loads(r.read().decode())
    elapsed = round(time.time() - start, 1)
    
    content = result["choices"][0]["message"]["content"]
    return content, elapsed, result.get("usage", {})


def parse_ensign_output(raw):
    """Parse the ensign's structured output."""
    sections = {
        "assessment": "",
        "strategy": "",
        "next_prompt": "",
        "context_injection": "",
    }
    
    current = None
    for line in raw.split("\n"):
        if "===ASSESSMENT===" in line:
            current = "assessment"
        elif "===STRATEGY===" in line:
            current = "strategy"
        elif "===NEXT_PROMPT===" in line:
            current = "next_prompt"
        elif "===CONTEXT_INJECTION===" in line:
            current = "context_injection"
        elif current:
            sections[current] += line + "\n"
    
    # Clean up
    for k in sections:
        sections[k] = sections[k].strip()
    
    # Fallback if parsing failed
    if not sections["next_prompt"]:
        sections["next_prompt"] = raw[:500]
    
    return sections


def run_ensign_experiment(model_key, query, rounds=5):
    """Run a full ensign-orchestrated experiment."""
    run_id = f"ensign-{model_key}-{int(time.time())}"
    print(f"\n{'='*60}")
    print(f"🧭 ENSIGN EXPERIMENT")
    print(f"   Thinker: {MODELS[model_key]['model']}")
    print(f"   Ensign: llama-3.1-8b-instant (7ms)")
    print(f"   Rounds: {rounds}")
    print(f"{'='*60}")
    
    history = []
    all_data = {
        "run_id": run_id,
        "model": model_key,
        "query": query,
        "rounds": [],
        "ensign_calls": [],
    }
    
    for rnd in range(1, rounds + 1):
        print(f"\n  --- Round {rnd}/{rounds} ---")
        
        # Step 1: Ensign assesses and constructs prompt (7ms)
        if rnd == 1:
            # First round — ensign just primes the pump
            prompt = f"Answer this question thoroughly and concretely. Be specific.\n\n{query}"
            ensign_data = {
                "round": rnd,
                "ensign_raw": "(first round — no assessment needed)",
                "assessment": "Initial prompt, no prior context.",
                "strategy": "OPEN",
                "context_injection": "",
                "ensign_time": 0,
            }
            print(f"  🧭 Ensign: Initial prompt (no assessment)")
        else:
            print(f"  🧭 Ensign thinking...", end=" ", flush=True)
            ensign_raw, ensign_time, ensign_usage = call_ensign(history, query)
            ensign_parsed = parse_ensign_output(ensign_raw)
            
            ensign_data = {
                "round": rnd,
                "ensign_raw": ensign_raw,
                "assessment": ensign_parsed["assessment"],
                "strategy": ensign_parsed["strategy"],
                "context_injection": ensign_parsed["context_injection"],
                "ensign_time": ensign_time,
                "ensign_tokens": ensign_usage.get("completion_tokens", 0),
            }
            
            # Construct the actual prompt with context injection
            prompt = ensign_parsed["next_prompt"]
            if ensign_parsed["context_injection"]:
                prompt = f"Context from your previous rounds (remember this):\n{ensign_parsed['context_injection']}\n\n{prompt}"
            
            print(f"{ensign_time}s — Strategy: {ensign_parsed['strategy']}")
            print(f"     Assessment: {ensign_parsed['assessment'][:80]}...")
        
        all_data["ensign_calls"].append(ensign_data)
        
        # Step 2: Big model answers (30-60s)
        print(f"  🧠 {model_key} thinking...", end=" ", flush=True)
        response, elapsed, usage = call_big_model(model_key, prompt, history)
        words = len(response.split())
        print(f"{words}w in {elapsed}s")
        
        round_data = {
            "round": rnd,
            "prompt": prompt,
            "response": response,
            "word_count": words,
            "time": elapsed,
            "tokens": usage.get("completion_tokens", 0),
            "ensign_assessment": ensign_data["assessment"],
            "ensign_strategy": ensign_data["strategy"],
        }
        history.append(round_data)
        all_data["rounds"].append(round_data)
        
        # Brief preview
        print(f"     Preview: {response[:100]}...")
        
        time.sleep(1)
    
    # Compute stats
    first_words = history[0]["word_count"]
    last_words = history[-1]["word_count"]
    growth = round(last_words / first_words, 2) if first_words else 0
    total_ensign_time = sum(e.get("ensign_time", 0) for e in all_data["ensign_calls"])
    total_think_time = sum(r["time"] for r in all_data["rounds"])
    
    all_data["summary"] = {
        "first_words": first_words,
        "last_words": last_words,
        "growth_factor": growth,
        "total_ensign_time": round(total_ensign_time, 2),
        "total_think_time": round(total_think_time, 1),
        "ensign_overhead_pct": round(total_ensign_time / total_think_time * 100, 1) if total_think_time else 0,
        "strategies_used": [e["strategy"] for e in all_data["ensign_calls"]],
    }
    
    # Save
    out_path = DATA_DIR / f"{run_id}.json"
    out_path.write_text(json.dumps(all_data, indent=2))
    
    print(f"\n{'='*60}")
    print(f"🧭 ENSIGN EXPERIMENT COMPLETE")
    print(f"   Growth: {first_words}→{last_words} ({growth}x)")
    print(f"   Think time: {total_think_time}s")
    print(f"   Ensign time: {total_ensign_time}s ({all_data['summary']['ensign_overhead_pct']}% overhead)")
    print(f"   Strategies: {' → '.join(all_data['summary']['strategies_used'])}")
    print(f"   Saved: {out_path}")
    
    return all_data


def main():
    models_to_test = sys.argv[1].split(",") if len(sys.argv) > 1 and not sys.argv[1].isdigit() else ["deepseek-chat", "seed-pro", "seed-mini"]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    query_idx = 3
    # Check if argv[1] is a number (rounds) not a model
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        rounds = int(sys.argv[1])
        models_to_test = ["deepseek-chat", "seed-pro", "seed-mini"]
        query_idx = 2
    query = sys.argv[query_idx] if len(sys.argv) > query_idx else "Design a self-improving feedback loop for AI agents. Agents should produce work, review it, identify weaknesses, and iterate. The system should compound: each cycle makes the agent better at the next cycle. Include concrete mechanisms for knowledge retention across sessions."
    
    print(f"🧭 THE ENSIGN — Orchestrated Iteration")
    print(f"   Ensign: Groq Llama 8B Instant (7ms)")
    print(f"   Thinkers: {models_to_test}")
    print(f"   Rounds: {rounds}")
    
    results = []
    for model in models_to_test:
        if model not in MODELS:
            print(f"Unknown model: {model}. Available: {list(MODELS.keys())}")
            continue
        try:
            result = run_ensign_experiment(model, query, rounds)
            results.append(result)
        except Exception as e:
            print(f"❌ {model} failed: {e}")
        time.sleep(2)
    
    # Summary
    if results:
        print(f"\n{'='*60}")
        print(f"📊 ENSIGN EXPERIMENT SUMMARY")
        print(f"{'='*60}")
        print(f"{'Model':<18} {'Growth':>7} {'Think':>6} {'Ensign':>7} {'Overhead':>8} {'Strategies'}")
        print("-" * 70)
        for r in sorted(results, key=lambda x: x["summary"]["growth_factor"], reverse=True):
            s = r["summary"]
            print(f"{r['model']:<18} {s['growth_factor']:>6.2f}x {s['total_think_time']:>5.0f}s {s['total_ensign_time']:>6.1f}s {s['ensign_overhead_pct']:>7.1f}% {'→'.join(s['strategies_used'])}")
        
        # Save summary
        summary = {
            "experiment": "ensign-orchestrated",
            "timestamp": datetime.utcnow().isoformat(),
            "results": results,
            "query": query,
        }
        summary_path = DATA_DIR / f"ensign-summary-{int(time.time())}.json"
        summary_path.write_text(json.dumps(summary, indent=2))
        print(f"\n💾 Summary: {summary_path}")


if __name__ == "__main__":
    main()
