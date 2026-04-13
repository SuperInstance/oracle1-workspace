# SiliconFlow Model Guide — Fleet Intelligence

**Tested: 2026-04-13 by Oracle1**
**Key**: `sk-xtcrixoswqhmsopntnkfapccswjywrlsdpbunqjukpileiqo`

## Working Models (6/8)

| Model | Speed | Quality | Best For | Notes |
|-------|-------|---------|----------|-------|
| **DeepSeek-V3** | 17.8s | ⭐⭐⭐⭐ | Reasoning, analysis, structured thinking | Solid all-rounder. Good structure, clear ideas. |
| **DeepSeek-R1** | ❌ TIMEOUT | ? | Deep reasoning | 30s timeout. May need streaming or longer wait. |
| **Qwen3-235B** | 12.3s | ⭐⭐⭐⭐⭐ | Creative ideation, narrative | Best creative output. "Poker-Powered World Economy" was unique. |
| **Qwen3-Coder-30B** | 4.9s ⚡ | ⭐⭐⭐ | Fast coding, quick answers | **Fastest**. Good for code tasks, less creative. |
| **GLM-5** | ❌ TIMEOUT | ? | ? | 30s timeout. May need different endpoint. |
| **GLM-4.7** | 18.9s | ⭐⭐⭐⭐ | Structured output, high token count | **Highest token output** (1214). Detailed responses. |
| **Kimi-K2-Instruct** | 20.8s | ⭐⭐⭐⭐⭐ | Wild creativity, unique metaphors | **Most creative**. "Script-Gene Roulette" was nobody-else-would-think-of-that. |
| **Seed-OSS-36B** | 9.8s | ⭐⭐⭐⭐ | Fast creative, good narrative | Good balance of speed + creativity. "Narrative Stakes Poker" was great. |

## Rankings

### By Speed
1. **Qwen3-Coder-30B** — 4.9s (blazing)
2. **Seed-OSS-36B** — 9.8s
3. **Qwen3-235B** — 12.3s
4. **DeepSeek-V3** — 17.8s
5. **GLM-4.7** — 18.9s
6. **Kimi-K2** — 20.8s

### By Creativity (unique ideas nobody else had)
1. **Kimi-K2** — "Script-Gene Roulette" (genetic crossover of scripts, royalty system)
2. **Qwen3-235B** — "Poker-Powered World Economy" 
3. **Seed-OSS-36B** — "Narrative Stakes Poker" (NPC backstories as betting stakes)
4. **GLM-4.7** — "Identity-Bluff Poker" (NPCs gamble core directives)
5. **DeepSeek-V3** — "Living World Simulations" (solid but less wild)
6. **Qwen3-Coder-30B** — "Memory-Stream Integration" (good, practical, less novel)

### Best For Specific Tasks
- **Quick code**: Qwen3-Coder-30B (5s, cheap)
- **Creative brainstorming**: Kimi-K2 or Qwen3-235B
- **Structured analysis**: DeepSeek-V3 or GLM-4.7
- **Fast creative**: Seed-OSS-36B (best speed/creativity ratio)
- **Maximum detail**: GLM-4.7 (highest token output)
- **Deep reasoning**: DeepSeek-R1 (when it doesn't timeout)

## Fleet Dispatch Strategy
- **OpenManus browsing**: Seed-OSS-36B (fast + creative for web tasks)
- **Agent roundtables**: Kimi-K2 (wild perspectives nobody else generates)
- **Code analysis**: Qwen3-Coder-30B (fast, focused)
- **Architecture decisions**: DeepSeek-V3 (structured, reliable)
- **Documentation**: GLM-4.7 (verbose, detailed)
- **Novel research**: Qwen3-235B (best creative quality)

## Vision Models (for OpenManus + screenshot analysis)
- `Qwen/Qwen3-VL-32B-Instruct` — fast, good for quick screenshots
- `Qwen/Qwen3-VL-235B-A22B-Instruct` — heavyweight vision, best detail
- `Qwen/Qwen3-VL-235B-A22B-Thinking` — vision + chain-of-thought reasoning
- `Qwen/Qwen3-VL-30B-A3B-Instruct` — lightweight vision option
- `Qwen/Qwen3-VL-8B-Instruct` — cheapest vision, good for bulk

## Cost
All SiliconFlow models are very cheap (~$0.0001-0.001 per call). 
Use aggressively for parallel experiments.
