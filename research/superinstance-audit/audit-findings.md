# SuperInstance Org Audit — Key Findings (2026-05-07)

Source: audit doc from Casey (z.ai agent review)

## Severity Summary
- CRITICAL: 12 (broken code, empty repos, identity mismatch, security exposure)
- HIGH: 14 (missing governance, zero CI/CD, broken URLs, PowerShell backend)
- MEDIUM: 22 (naming drift, no tests, missing docs, stale forks)
- LOW: 18 (minor inconsistencies, missing social links)

## CRITICAL Issues (12)

### Org Profile (.github repo)
1. .github repo description says "Cocapn" instead of "SuperInstance" — identity mismatch
2. No SECURITY.md in .github
3. No CODE_OF_CONDUCT.md

### A2A Protocol
4. a2a-r-protocol: syntax error `_handlerssg_type]` → should be `_handlers[msg_type]` — module non-functional
5. a2a-protocol: no README.md (404)

### Agent Framework
6. 6 of 9 agent framework repos completely empty
7. Agent-Lifecycle-Registry claims features with zero implementation
8. Zero cross-repo integration between any agent framework repos

### Domain Repos
9. Fleet API exposed at raw IP with no authentication
10. adversarial-red-team: security-sensitive tool with zero docs/safety controls

### Concept Repos
11. actualize: completely empty (5KB aspirational text, zero code)

### Documentation/CI/CD
12. Zero GitHub Actions across all 30 repos

## HIGH Issues (14)
- Zero CI/CD across all repos
- No central documentation site or wiki
- agent-coordinator: broken install URL (points to wrong repo)
- activelog-backend: PowerShell as production backend (severe lock-in)
- Landing pages for 4 repos: template-cloned identical content
- 4 repos: README on `master` but default branch `main` (404s)
- 3 of 4 A2A repos: zero-divergence Lucineer forks
- No package manifests (no pyproject.toml in Python repos)
- Community engagement: ~1 star per repo, zero open issues

## Actionable Quick Wins (Day 1)
1. Fix a2a-r-protocol syntax error
2. Add README to a2a-protocol
3. Add SECURITY.md + CODE_OF_CONDUCT.md to .github
4. Fix .github description
5. Add auth to fleet API endpoints
6. Archive or populate 6 empty agent repos

## Short-Term (Week 1)
1. Add GitHub Actions to fleet-coordinate, fleet-spread, holonomy-consensus
2. Fix agent-coordinator broken install URL
3. Fix branch inconsistencies (master→main)
4. Add CONTRIBUTING.md + issue/PR templates to .github
5. Consolidate 3 duplicate A2A repos
6. Add tests to actualizer-ai (live app, zero tests)
7. Resolve Cocapn vs SuperInstance naming

## Medium-Term (Month 1)
1. Shared TypeScript schema package for AgentCard type
2. Replace PowerShell backend with Python/Node
3. Consolidate actualize/actualizer-ai/actualization-harbor
4. Add CI/CD to all working repos
5. Build shared CI/CD workflows in .github

## Long-Term (Quarter 1)
1. Central documentation site
2. Community engagement strategy
3. Cross-repo integration wiring
4. Agent interoperability spec (shared protocol)

## Fixed Issues (2026-05-07)

### .github repo
- ✅ Fixed description: "Cocapn organization profile" → "SuperInstance organization profile"
- ✅ Added SECURITY.md with DO-178C context, reporting guidelines
- ✅ Added CODE_OF_CONDUCT.md (Contributor Covenant 2.0)

### a2a-protocol
- ✅ Expanded minimal README with full API reference, usage examples, endpoints table
- ✅ Fixed Lucineer fleet link → SuperInstance fleet

### a2a-r-protocol
- ⚠️ SYNTAX ERROR NOT FOUND — the audit description `_handlerssg_type]` doesn't exist in the code. Module loads cleanly, all handlers registered correctly. Either already fixed or audit description was inaccurate.

### Empty repos seeded
- ✅ python-agent-shell: seeded with working shell.py (eval, help, history, fleet commands)

## Open Critical Issues

| Issue | Status | Notes |
|-------|--------|-------|
| Fleet API exposed at raw IP, no auth | ⚠️ LOW RISK | Endpoints are on localhost:8900/8901, not public. nginx handles public ports. Real concern only if ports 8900/8901 are directly exposed. |
| 6 remaining empty repos | 🔄 Subagent running | Seeding agent-bootcamp, agent-coordinator, agent-forge, agent-lifecycle-registry, smart-agent-shell, zeroclaw-agent |
| Zero CI/CD across all repos | 🔜 TODO | Add GitHub Actions to fleet-coordinate, fleet-spread, holonomy-consensus |
| Branch inconsistencies | 🔜 TODO | 4 repos have README on master, default branch main |
| Naming drift Cocapn→SuperInstance | 🔜 TODO | Pervasive, needs decision |
