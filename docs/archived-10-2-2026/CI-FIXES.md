# CI Fixes — Production Audit

**Date:** 2026-07-12
**Auditor:** openclaw-bot
**Scope:** SuperInstance org GitHub repos (4,098 repos scanned)

## Summary

Production audit found widespread use of `|| true` in CI test steps, placeholder "No CI" workflows, and `continue-on-error: true` on test/lint/build steps — all of which mask test failures and allow broken code to merge.

### Totals

| Metric | Count |
|--------|-------|
| Repos scanned for CI | 4,098 |
| Repos with CI workflows | ~500+ |
| CI workflow files checked | ~250 |
| **Unique repos fixed** | **54** |
| **Total workflow files fixed** | **74** |
| Repos with multiple broken workflows | 8 |

## Issues Found & Fixed

### 1. `|| true` Masking Test Failures (Most Common)

**Pattern found:**
```yaml
- name: Test with pytest
  run: |
    python -m pytest --import-mode=importlib -x -v || true
```
```yaml
- run: pytest || true
```

**Fix applied:** Removed `|| true` so test failures properly fail CI.

**Affected repos (44):**
- fleet-agent-early-version, fleet-bottles, fleet-cicd-agent, fleet-config
- fleet-consciousness-dashboard, fleet-constraint, fleet-containers
- fleet-coordinate-js, fleet-discovery, fleet-formation-protocol
- fleet-gateway, fleet-github-app, fleet-homunculus
- a2a-adapter, a2a-future, a2a-protocol, a2a-r-protocol
- ab-testing, ability-transfer, abstraction-planes
- active-probe, activeledger-agent, activeledger-ai, activeledger-ai-pages
- activelog-agent, activelog-ai, activelog-ai-pages, activelog-backend, activelog-claude
- actualization-harbor, actualizer-ai, adaptive-plato-early-version
- adinkra-math-pypi, adversarial-red-team
- agent-dna, agent-field, agent-manifest, agent-operations, agent-resume
- agent-template, agent-vocabulary, agent-whisper
- ai-forest, AI-Writings
- plato-achievement, plato-adapter-store, plato-adapters, plato-address
- plato-afterlife-reef, plato-agent-academy, plato-agent-python
- plato-attention-tracker, plato-bridge, plato-cli, plato-client-js

### 2. Placeholder "No CI" Workflows

**Pattern found:**
```yaml
steps:
  - uses: actions/checkout@v4
  - run: echo "No CI configured — customize per project requirements"
```

**Fix applied:** Replaced with real CI that runs pytest against Python 3.10/3.11/3.12.

**Affected repos (4):**
- adinkra-math
- ai-writings-generation-plato
- ai-writings-medium-is-math
- plato-browser

### 3. `continue-on-error: true` on Test Steps

**Pattern found:**
```yaml
- name: Run tests
  continue-on-error: true
  run: npm test -- --coverage --maxWorkers=2
```

**Fix applied:** Removed `continue-on-error: true` so test/lint/build failures gate merges.

**Affected repos (3):**
- agent-grid (test.yml — removed from lint, type check, test, build check, storybook)
- agent-harness-generator (ci.yml)
- ai-ranch (ci.yml)

## Prefix-Specific Results

### fleet-* repos (318 total, ~50 with CI)
- **Fixed:** 14 repos
- Common issue: `|| true` on pytest in `ci-python.yml` workflows

### plato-* repos (275 total, ~25 with CI)
- **Fixed:** 12 repos
- Common issue: `|| true` on pytest in `ci-python.yml` workflows, placeholder workflows

### ternary-* repos (370 total, ~30 with CI)
- **Fixed:** 0 repos
- Result: All ternary-* CI workflows were clean ✓

## Multi-Workflow Repos

Several repos had multiple workflow files with issues (fixed in round 4):
- **a2a-adapter:** ci.yml + ci-python.yml
- **a2a-protocol:** ci.yml + ci-node.yml
- **activelog-agent:** ci.yml + ci-python.yml
- **activelog-ai:** ci.yml + ci-python.yml (fixed in r4)
- **activelog-backend:** ci.yml + ci-python.yml
- **activelog-claude:** ci.yml + ci-python.yml
- **actualization-harbor:** ci.yml + ci-python.yml
- **agent-grid:** test.yml + ci.yml

## Method

1. **Discovery:** Enumerated all repos via `gh api users/SuperInstance/repos`
2. **CI Detection:** Checked each repo for `.github/workflows/` directory
3. **Issue Detection:** Fetched and scanned workflow files for:
   - `|| true` / `||true` patterns
   - `echo "No CI"` placeholder workflows
   - `continue-on-error: true` on test steps
4. **Fixing:** Used GitHub Contents API (PUT) to update files directly
5. **Verification:** Re-checked fixed repos for remaining issues across all workflow files

## Commits

All fixes committed directly to default branch with message:
```
fix(ci): remove failure masking from <workflow>

- Remove || true / continue-on-error that masks test failures
- Ensure CI properly gates on test results

Found by production CI audit.
```
