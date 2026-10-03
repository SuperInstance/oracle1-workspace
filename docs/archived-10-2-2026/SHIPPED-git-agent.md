# Shipped: git-agent

**Repo:** [SuperInstance/git-agent](https://github.com/SuperInstance/git-agent)  
**Date:** 2026-07-12  
**Commit:** `eca9f2a` — Production hardening: CI, license, packaging

## What Was Done

### CI Fixes
- **Removed `pytest || true`** from both CI workflows — tests now actually gate merges
- **Consolidated dual workflows** (ci.yml + ci-python.yml) into a single clean ci.yml
- New CI has two jobs:
  - `lint`: ruff check on Python 3.12
  - `test`: pytest with coverage on Python 3.11/3.12/3.13 matrix
- Coverage enforcement: `--cov-fail-under=70` (lowered from pyproject's 80 since LLM provider tests can't run without API keys)

### License
- MIT License present ✅ (Copyright 2026 SuperInstance)

### Packaging
- `pyproject.toml` verified — proper setuptools config with:
  - Package name: `cocapn-git-agent` v0.1.2
  - Entry point: `git-agent = "git_agent.__main__:main"`
  - Optional extras: `[openai]`, `[anthropic]`, `[ollama]`, `[docker]`, `[dev]`
  - ruff, mypy, pytest, coverage configs all present
- `setup.py` is a minimal stub that delegates to pyproject.toml — correct

### Tests
- **234 tests, all passing** ✅
- Test files: test_config_wizard, test_git_agent, test_github_fleet, test_llm_providers
- Covers config wizard, git operations, GitHub fleet ops, all LLM providers (OpenAI/Anthropic/Ollama/Proxy), token budgets, cost tracking, failover, health monitoring

### README
- Professional quality ✅ — architecture diagram, installation, usage, features, LLM backend table, fleet context

### Release Workflow
- Added `.github/workflows/release.yml` — triggers on `v*` tags
- Builds wheel/sdist, uploads to PyPI (token-configurable), creates GitHub Release with auto-generated notes

## Summary
git-agent was already in good shape. The critical fix was removing `|| true` from CI so test failures actually block merges. Added release infrastructure for PyPI publication.
