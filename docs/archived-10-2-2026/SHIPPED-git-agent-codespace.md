# SHIPPED: git-agent-codespace

**Date:** 2026-07-12
**Repo:** [SuperInstance/git-agent-codespace](https://github.com/SuperInstance/git-agent-codespace)
**Commit:** `3925208` — Production hardening: license, tests, CI

## What This Repo Does

One-click GitHub Codespace template for Git-Agent runtime development. Provides a pre-configured devcontainer with Python 3.12, Go 1.24, Node.js 22, auto-clones core fleet repos (flux-runtime, greenhorn-runtime, iron-to-iron, fleet-discovery), and verifies the FLUX VM on creation.

## Changes Made

### .gitignore (improved)
- Expanded from 2 lines (`target/`, `Cargo.lock`) to full coverage:
  - Python: `__pycache__/`, `*.py[cod]`, `*.egg-info/`, `dist/`, `build/`
  - Node: `node_modules/`, `npm-debug.log*`, `.npm`
  - Go: `*.test`, `*.out`, `vendor/`
  - Rust: `target/`, `Cargo.lock`
  - IDE: `.vscode/`, `.idea/`, `*.swp`, `.DS_Store`
  - Environment: `.env`, `.env.local`
  - Devcontainer artifacts

### Tests (new — 12 tests, all passing)
- `tests/test_template.py` — Python/pytest suite:
  - devcontainer.json exists, valid JSON, required fields, language features
  - setup.sh exists, has `set -e`, references core repos
  - README.md exists with Quick Start section
  - LICENSE is MIT
  - CHARTER.md exists
  - .gitignore covers Python/Node/Rust
- `tests/template.bats` — Bats equivalent for shell-based CI

### CI (replaced placeholder)
- Old: `echo "No CI configured"` placeholder
- New: Two jobs:
  1. **validate-template** — Validates devcontainer.json schema, setup.sh structure, LICENSE, .gitignore
  2. **python-tests** — Runs full pytest suite on Python 3.12

### Already Present (no changes needed)
- LICENSE (MIT) — already existed
- README.md — comprehensive, well-structured
- devcontainer.json — properly configured
- setup.sh — solid with error handling and repo cloning

## Role in Pipeline

This is the **entry point** of the Codespace→Agent→Edge pipeline. New agents (greenhorns) use this template to bootstrap their development environment in 2-3 minutes. It provides the foundation upon which capitaine-1 (the agent runtime) runs, and which codespace-edge-rd researches how to deploy to edge hardware.
