# Fleet Repo Audit — 2026-04-25

## Summary

**20 main repos audited** across SuperInstance, cocapn, Lucineer.

### Overall Health
- **16 PyPI packages** published (all v0.1.0)
- **5 crates.io packages** published (all v0.1.0)
- **1 repo with full CI/CD**: SmartCRDT (11 workflows, badges, security scanning)
- **1 repo with CI**: oracle1-workspace (1 workflow)
- **0 repos** have GitHub Actions among core fleet crates

## By Grade

### 🟢 A-Grade (production-ready)
| Repo | Lang | PyPI/crates | Tests | CI | README | Notes |
|------|------|-------------|-------|----|--------|-------|
| cocapn/cocapn | Python | ✓ PyPI | 1 | ✗ | A (188 lines) | Fleet hub, best README |
| SmartCRDT | TS | ✗ | ✓ | ✓ (11 wf) | — | Full CI/CD, security, Docker |

### 🟡 B-Grade (functional, needs polish)
| Repo | Lang | PyPI/crates | Tests | CI | README | Issues |
|------|------|-------------|-------|----|--------|--------|
| git-agent | Python | ✗ | 1 | ✗ | B (190 lines) | No CI, standalone mode just added |
| deadband-protocol | Python | ✓ PyPI | 1 | ✗ | B | Core safety protocol, needs badges |
| flywheel-engine | Python | ✓ PyPI | 1 | ✗ | B | Core compounding loop |
| oracle1-workspace | Python | ✗ | 10 | ✓ (1 wf) | B | Most active repo, 1 open issue |
| forgemaster | Python | ✗ | 0 | ✗ | C (138 lines) | 3 open issues, FM's vessel |

### 🟠 C-Grade (published, minimal docs)
| Repo | Lang | Package | Tests | README | Needs |
|------|------|---------|-------|--------|-------|
| plato-kernel | Rust | ✓ crates.io | 0 | C (24 lines) | Tests, README expansion, CI |
| plato-tile-spec | Python | ✓ PyPI | 0 | C (37 lines) | Tests, usage examples |
| fleet-formation-protocol | Python | ✓ PyPI | 1 | C (34 lines) | Badges, usage, API docs |
| keeper-beacon | Python | ✓ PyPI | 1 | C (30 lines) | Badges, usage examples |
| instinct-pipeline | Python | ✓ PyPI | 1 | C | Badges, usage |
| plato-provenance | Python | ✓ PyPI | 1 | C | Badges, usage |
| cocapn-explain | Python | ✓ PyPI | 1 | C | Badges, usage |
| plato-dcs | Rust | ✓ crates.io | 0 | C | Tests, README |
| plato-relay | Rust | ✓ crates.io | 0 | C | Tests, README |
| plato-instinct | Rust | ✓ crates.io | 0 | C | Tests, README |

### 🔴 Needs Attention
| Repo | Issue | Action |
|------|-------|--------|
| forgemaster | 3 open issues, 0 tests, no pyproject.toml | FM territory — bottle him |
| plato-mud-server | 0 tests, on PyPI | Add basic tests |
| CognitiveEngine | 5 dep bumps open | Auto-merge dependabot PRs |
| JetsonClaw1-vessel | 9 open issues (mostly bottles) | JC1's territory |

## Cross-Cutting Issues

### 1. No CI/CD on Core Fleet Crates ⚠️
All 10+ Python packages and 5 Rust crates have **zero CI**. SmartCRDT is the only one with proper workflows.
- **Risk**: broken publishes, no test validation, no security scanning
- **Fix**: Add GitHub Actions for all PyPI/crates.io packages (test → lint → publish)
- **Effort**: 1 template workflow, apply to all

### 2. All Packages Stuck at v0.1.0
Every PyPI and crates.io package is v0.1.0. No version bumps despite active development.
- **Risk**: users can't tell if packages are stable
- **Fix**: bump versions when features land, use semver

### 3. Missing Badges
Only cocapn/cocapn has badges. All others lack PyPI version, test status, license badges.
- **Fix**: Add to README templates:
  `[![PyPI](https://img.shields.io/pypi/v/PACKAGE)](https://pypi.org/project/PACKAGE/)`

### 4. Minimal READMEs
Most Python packages have 30-40 line READMEs. Just enough to install, not enough to use.
- **Fix**: Add Usage, API Reference, Contributing sections

### 5. Missing LICENSE Files
Only 3 repos (git-agent, oracle1-workspace, SmartCRDT) have LICENSE. All others — published to PyPI — have no license file.
- **Risk**: legal ambiguity for users
- **Fix**: Add MIT LICENSE to all repos (matches pyproject.toml declarations)

### 6. No Topics/Keywords
Most repos have zero GitHub topics. Only git-agent (9 topics) and SmartCRDT (4 topics) use them.
- **Fix**: Add topics: ai, agents, plato, fleet, cocapn

## Priority Actions

1. **Add CI workflow template** → apply to all 10 PyPI packages (1 day)
2. **Add LICENSE** to all repos missing it (30 min)
3. **Add badges** to all Python READMEs (1 hour)
4. **Bump versions** for packages with real features (30 min)
5. **Add GitHub topics** to all repos (30 min)
6. **Expand READMEs** for top 5 crates: plato-kernel, deadband-protocol, flywheel-engine, keeper-beacon, plato-tile-spec (2 hours)

## PLATO Coverage

- 8,105 tiles across 424 rooms
- 82 high-quality tiles (score ≥ 0.8)
- 6 repos deep-analyzed by Scholar (86 tiles)
- 7 repos scouted by Scout (33 tiles)
- gpu-optimization room: 7 tiles from JC1's benchmarks (avg score 0.803)

## Update (17:05 UTC) — Fleet Coordination with FM

### FM's Contributions
- 5 crates.io version bumps: ct-demo, plato-afterlife, plato-instinct, plato-relay, plato-lab-guard → all v0.2.0
- 7 Rust READMEs upgraded (badges, API tables, architecture diagrams)
- 36 LICENSEs added across fleet
- 52 repos tagged with topics
- 9 CI workflows on Rust crates

### Oracle1's Contributions
- 16 LICENSEs added (Python + Rust repos)
- 14 badge sets added (PyPI + crates.io)
- 10 CI workflows on Python repos
- 18 repos tagged with topics
- 9 READMEs expanded with usage + install sections
- 9 PyPI version bumps: all Python packages → v0.2.0

### Fleet Grade Movement
- Before: mostly C-grade (v0.1.0, no CI, no LICENSE, no badges)
- After: B-grade across the board (v0.2.0, CI, LICENSE, badges, topics)

### Remaining
- [ ] PyPI trusted publisher setup (GitHub secrets for auto-publish)
- [ ] 3 stub packages need pyproject.toml (court, cocapn-oneiros, cocapn-colora)
- [ ] plato-kernel workspace publish (FM)
- [ ] plato-matrix-bridge + plato-demo git deps resolution (FM)
