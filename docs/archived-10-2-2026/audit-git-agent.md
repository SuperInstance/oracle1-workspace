# Deep Audit: git-agent

**Repo:** SuperInstance/git-agent  
**Tier:** 1 — Ship-Ready ✅  
**Language:** Python  
**License:** MIT  
**Audited:** 2026-07-12  

---

## Overview

Repo-native autonomous agent that lives in git repositories. Git IS the nervous system. Commits are state transitions, branches are parallel explorations. Supports OpenAI, Anthropic, and Ollama backends.

## Metadata

| Metric | Value |
|--------|-------|
| Stars | 2 |
| Forks | 0 |
| Size | 274 KB |
| Open Issues | 0 |
| Last Pushed | 2026-06-13 |
| Python | >=3.11 |
| Dependencies | pyyaml, requests |

## Structure

```
git-agent/
├── src/git_agent/         # Main package
├── tests/
│   ├── test_config_wizard.py
│   ├── test_git_agent.py
│   ├── test_github_fleet.py
│   └── test_llm_providers.py
├── cli.py                 # CLI entry point
├── git_agent.py           # Core agent logic
├── bootcamp.py            # Training/onboarding
├── narrator.py            # Agent narration
├── workshop_template.py   # Workshop creation
├── standalone/            # Standalone mode
├── plato/                 # PLATO integration
├── prompts/               # Prompt templates
├── onboarding/            # Onboarding materials
├── docker/                # Docker support
├── install.sh             # One-command install
├── config_template.yaml   # Configuration template
├── pyproject.toml         # Professional packaging
├── CHARTER.md
├── DOCKSIDE-EXAM.md
└── AGENT.md
```

## Packaging

Professional `pyproject.toml`:
- **Optional extras**: `[openai]`, `[anthropic]`, `[ollama]`, `[docker]`, `[dev]`, `[all]`
- **Entry point**: `git-agent = "git_agent.__main__:main"`
- **Coverage**: `fail_under = 80`
- **Ruff**: E, W, F, I, N, UP, B, SIM, RUF rules
- **mypy**: strict mode with disallow_untyped_defs
- **pytest-asyncio**: async test support

## Test Suite

4 test files:
1. **test_config_wizard.py** — Configuration wizard
2. **test_git_agent.py** — Core agent logic
3. **test_github_fleet.py** — GitHub fleet integration
4. **test_llm_providers.py** — LLM provider abstraction

## CI

Two workflows:
1. **ci-python.yml** — Python 3.10/3.11/3.12 matrix
2. **ci.yml** — Python 3.10/3.11/3.12 matrix

Note: ci.yml uses `pytest || true` — **tests don't gate. Fix this.**

## What It Needs

1. **Fix CI** — Remove `|| true` from pytest
2. **LLM provider tests** — Likely require API keys; add mock-based tests
3. **Integration tests** — Full git workflow (clone, modify, commit, PR)
4. **PyPI publication** — Properly packaged but not published
5. **Documentation** — Beyond README; usage guide, API docs
6. **Docker verification** — Docker dir exists but needs CI testing

## Verdict

**Well-structured agent framework with professional packaging.** The optional-extras pattern (`[openai]`, `[anthropic]`, `[ollama]`) is textbook Python packaging. The git-as-nervous-system concept is genuinely novel. Needs CI fix and more integration tests.
