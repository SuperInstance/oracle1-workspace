# License Fixes — Batch 2

**Date:** 2025-07-12  
**Org:** SuperInstance  
**Operator:** OpenClaw subagent  

## Summary

Second wave of MIT license fixes across the SuperInstance org.

| Metric | Count |
|--------|-------|
| Repos identified missing licenses | ~1833 |
| Repos processed this batch | 100 |
| Successfully fixed | 100 |
| Failed | 0 |
| Success rate | 100% |

## What was done per repo

For each repo:

1. **Cloned** shallow (`--depth 1`)
2. **Added MIT LICENSE file** (standard MIT text, copyright SuperInstance)
3. **Updated license metadata** in manifest files where present:
   - `package.json` → `"license": "MIT"`
   - `Cargo.toml` → `license = "MIT"`
   - `pyproject.toml` → `license = {text = "MIT"}`
4. **Added `.gitignore`** if missing (covers node_modules, target/, __pycache__, IDE files, OS files, env files)
5. **Committed** with message `"Add MIT license"`
6. **Pushed** to default branch
7. **Cleaned up** `/tmp/lic-*` directories

## Processing approach

- Parallel batches of 5 repos concurrently
- Shallow clones (`--depth 1`) for speed
- No README reading — pure license injection

## Repos fixed (100)

First 100 repos from the missing-license list, including:

a2a-signal-chain, a2ui-cave-wall, a2ui-components, a2ui-protocol, a2ui-render, acg_protocol, active-probe, activeledger-agent, activeledger-ai-pages, activelog-agent, activelog-ai-pages, adaptive-plato-early-version, adinkra-math, adinkra-math-npm, adinkra-math-pypi, adjunction, aesop-mcp, agent-homeostasis-rs, agent-manifold, agent-native-language, agent-operations, agent-spectrum-os, agent-to-agent, agent-workspace-template, ai-forest, ai-writings-medium-is-math, algtop-rs, analog-spline-theory, anomaly-atlas, ant-colony, api-gateway, api-gateway-1, approximation-theory, architectures, archive, arithmetic-code, arm-neon-eisenstein-bench, attention-daemon-early-version, attention-economy, auction-theory, avx512-constraint-checker, b-tree, bare-metal-plato, bathydata-map, baton-router, bayesian-game, bayesian-update, belief-revision, bering-sea-architecture, betti-curve, betti-music-computation, bezier-curve, bigint-rs, blog-posts, bloom-filter-rs, bootstrap-spark, bounded-model, braid-group-rs, branch-bound, bregman-divergence, bsp-tree, businesslog-agent, businesslog-ai, businesslog-ai-pages, bwt-compress, c-ternary, c-ternary-integration-demo, caas-api, cache-guardian-c, capitaine-agent, capitaine-ai-pages, capitaineai-com-pages, captain, casting-call-gpu, casting-call-mcp, cat-agent, categorical-agents-c, categorical-agents-rs, categorical-coordination, cathedral-probe, causal-graph-rs, CCC, ccc-os, cech-complex, cellular-automata-agent, cellular-automata-rs, cfd-rs, cfg-construct, cg-from-scratch, channel-capacity, chaos-rs, chern-classes, chess-dojo-v2, chess-engine, chronicle-engine, circuit-breaker-rs, claude, clawcommit-lucid, climate-conservation, clockwork-schedule

## Remaining

~1733 repos still missing licenses. Subsequent batches recommended.
