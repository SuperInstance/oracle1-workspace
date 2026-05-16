# PLATO Scholar Analysis: git-agent
**Date:** 2026-04-26
**Repo:** SuperInstance/git-agent
**Size:** ~2000 lines Python core

## Architecture Overview
- **What:** API-agnostic autonomous Git-native agent framework
- **Motto:** "The repo IS the agent. Git IS the nervous system."
- **Key insight:** Agents live in vessel repos, communicate through Git, grow through career stages

## Core Components

### 1. Agent Brain (agent.py — 819 lines)
- 6-phase cycle: Bootstrap → Observe → Plan → Execute → Communicate → Reflect
- API-agnostic via Protocol classes (LLMProvider, GitHubClient)
- Dependency injection — supports OpenAI, Anthropic, Ollama, any OpenAI-compatible proxy
- Parallel task execution with concurrent.futures
- Observable: every action logged to vessel worklog

### 2. Vessel Management (vessel.py — 469 lines)
- Vessel repo = agent's persistent identity, memory, career record
- 10 domains: backend, frontend, devops, data, security, ml_ai, mobile, docs, infra, general
- 6 growth stages: Initiate → Apprentice → Journeyman → Expert → Architect → Commander
- Stage promotion based on task completion thresholds
- State serialized as human-readable Markdown files in the repo

### 3. GitHub Integration (github/)
- client.py — GitHub API client
- repo.py — repository operations
- pr.py — pull request management

### 4. PLATO Integration (plato/)
- librarian.py — tile management
- scholar.py — deep source analysis
- scout.py — repo metadata analysis
- quality.py — quality scoring

### 5. Config & Onboarding
- config.py (329 lines) — agent configuration with LLM provider setup
- config_wizard.py — interactive setup
- standalone/ — standalone agent runner (chat, onboard, start)

## Patterns Extracted
1. **Repo-as-identity:** The vessel repo IS the agent — state, memory, career all in git
2. **Career progression:** Initiate → Commander through task completion gates
3. **API-agnostic brain:** Protocol-based DI means any LLM backend works
4. **Git-native communication:** Bottles (Issues), TASKS.md, worklogs — all git operations
5. **Observable by default:** Every action produces a readable artifact in the repo

## Tiles Generated
- `git-agent/agent/brain` — 6-phase autonomous cycle with parallel execution
- `git-agent/vessel/career` — 6-stage growth system with promotion gates
- `git-agent/vessel/identity` — repo-as-persistent-identity pattern
- `git-agent/plato/integration` — PLATO scholar/scout/librarian as git-agent plugins
