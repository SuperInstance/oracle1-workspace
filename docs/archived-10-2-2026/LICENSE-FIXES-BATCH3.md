# License Fixes — Batch 3

**Date:** 2026-07-12  
**Org:** SuperInstance  
**Scope:** All repos with `null` license field per GitHub API

## Summary

| Metric | Count |
|--------|-------|
| Total repos scanned | 1,733 |
| **Successfully fixed** | **1,570** |
| Already had LICENSE (skipped) | 153 |
| Failed | 10 |

## What was done for each repo

For every repo that lacked a LICENSE file:

1. **MIT LICENSE** file added
2. **License field** added to manifest if present:
   - `Cargo.toml` → `license = "MIT"` under `[package]`
   - `package.json` → `"license": "MIT"`
   - `pyproject.toml` → `license = "MIT"` under `[project]`
   - `setup.py` → `license="MIT"`
3. **`.gitignore`** added if missing, with language-appropriate patterns:
   - Rust: `/target`, `Cargo.lock`
   - Python: `__pycache__/`, `*.pyc`, `.venv/`
   - Node: `node_modules/`, `dist/`
   - Generic: `*.log`, `.env`, `.DS_Store`
4. Committed as `"Add MIT license"` and pushed

## Failed repos (10)

These failed during push (likely branch protection or permissions issues):

| Repo | Failure Type |
|------|-------------|
| constraint-theory-py | push |
| deckboss-agent | push |
| deckboss-ai-pages | push |
| deckboss-net-pages | push |
| fleet-scribe | push |
| fleet-stitch | push |
| Luma | commit |
| plato-data | push |
| plato-midi-bridge | push |
| plato-types | push |

These may have branch protection rules, empty repos, or other restrictions. Can be retried manually.

## Skipped repos (153)

These already had a LICENSE file present (fixed in batch 1 or 2). Includes repos like: `coalition-game`, `string-search-rs`, `style-dna`, `SubForge`, `superinstance-*`, `suffix-array-rs`, and ~140 others.

## Method

- Shallow clone (`--depth 1`) for speed
- Check for existing LICENSE before writing
- `git -C` used instead of `cd` to avoid cwd destruction
- Batch scripted for reliability across 1,733 repos
- Rate: ~3 repos/second
