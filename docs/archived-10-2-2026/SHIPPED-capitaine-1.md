# SHIPPED: capitaine-1

**Date:** 2026-07-12
**Repo:** [SuperInstance/capitaine-1](https://github.com/SuperInstance/capitaine-1)
**Commit:** `8ac45376` — Production hardening: license, tests, CI

## What This Repo Does

Capitaine is the Lucineer fleet flagship — a git-native repo-agent system where the repository itself IS the agent. A single TypeScript file on Cloudflare Workers implements a heartbeat cycle (detect mode → perceive → consult strategist → think → act → record) every 15 minutes. Features the crystallization curve concept: intelligence flows from fluid (LLM calls at $0.02/decision) to solid (compiled code at $0.0002/decision) over time. Includes 6 library modules: CrystalGraph, DeadReckoningEngine, DiscoveryEngine, ForgivenessEngine, LearningEngine, and TrustEngine.

## Changes Made

### Tests (new — 43 tests across 6 suites, all passing)
- **crystal.test.ts** (7 tests): Insight creation, use-based state promotion (fluid→solid→gas→metastatic), bonding, query matching, stats
- **dead-reckoning.test.ts** (6 tests): Compass pipeline progression, dependency blocking, cost estimation, status filtering, stats
- **discovery.test.ts** (8 tests): Fleet snapshot recording, equipment gap detection, convergence detection, cross-vessel opportunity detection, high-impact filtering
- **forgiveness.test.ts** (7 tests): Offense recording, crash escalation, security quarantine, offense resolution, quarantine lifting, pattern detection (chronic_instability, persistent_slowdown)
- **learning.test.ts** (7 tests): Lesson recording, tier promotion (hot→warm→cold), context query, vessel filtering, garbage collection, stats
- **trust.test.ts** (8 tests): Neutral baseline, positive/negative events, time decay, categorical levels, reset, custom decay rates
- **tests/run-all.sh**: Test runner script for CI execution

### Bug Fix: lib/trust.ts
- Removed stray markdown code fences (```typescript ... ```) that wrapped the entire file, preventing it from being imported/executed

### CI (consolidated and hardened)
- **Removed** `ci-node.yml` — used `|| true` on lint, build, and test steps, masking all failures
- **Replaced** `ci.yml` — old workflow ran `npm ci` (no package-lock exists) with Node 18/20/22 matrix
- **New** `ci.yml` — single job with real validation:
  - LICENSE, README, worker.ts, all 6 lib modules presence checks
  - .gitignore validation
  - Full test suite execution via `tests/run-all.sh`

### .gitignore (improved)
- Added: `.dev.vars`, `dist/`, `build/`, `*.tsbuildinfo`, `.env`, IDE files, test artifacts (`coverage/`, `.nyc_output/`, `*.lcov`)

### Already Present (no changes needed)
- LICENSE (MIT) — already existed
- README.md — excellent quality, comprehensive documentation
- All 6 lib modules — well-written, rich testable logic
- wrangler.toml — properly configured for Cloudflare Workers

## Role in Pipeline

Capitaine is the **agent runtime** in the Codespace→Agent→Edge pipeline. It's the actual agent brain that runs in a Codespace (provisioned by git-agent-codespace) and represents the intelligence that codespace-edge-rd researches how to transfer to edge devices.
