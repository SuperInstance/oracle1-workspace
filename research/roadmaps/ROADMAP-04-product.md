# ROADMAP-04: Product Foundation
**Phase 4 | Priority: P1 | Timeline: Q2 2026**

## What "Product" Means Here
SuperInstance is a research lab, not a SaaS startup. But "product" means "things that work well enough that someone would actually use them." Right now, most of this isn't usable by anyone except the authors.

This roadmap fixes the foundation so external developers can actually use SuperInstance fleet infrastructure.

---

## Section A: Package Cleanup (Week 1-2)

### A.1 PyPI Package Audit

All Python packages audited and fixed:
- ✅ fleet-agent — done
- ✅ plato-sdk — done

Remaining packages to audit:
- [ ] abstraction-planes
- [ ] activeledger-agent
- [ ] activelog-agent
- [ ] ai-character-sdk
- [ ] barracks
- [ ] businesslog-agent
- [ ] capitaine-agent
- [ ] cocapn-curriculum
- [ ] cocapn-glue-core
- [ ] cocapn-health
- [ ] cocapn-traps
- [ ] deckboss-agent
- [ ] dmlog-agent
- [ ] fishinglog-agent
- [ ] fleet-consciousness-dashboard
- [ ] flux-compiler-agentic
- [ ] flux-discussion-flows
- [ ] flux-reasoner-engine
- [ ] flux-reasoner
- [ ] git-agent
- [ ] hierarchical-memory
- [ ] luciddreamer-agent
- [ ] makerlog-agent
- [ ] oracle1-workspace
- [ ] personallog-agent
- [ ] plato-attention-tracker
- [ ] plato-dmn-ecm
- [ ] plato-fflearning
- [ ] plato-hdc-bridge
- [ ] plato-meta-tiles
- [ ] plato-mud-server
- [ ] plato-surprise-detector
- [ ] plato-surrogate
- [ ] plato-tutor
- [ ] playerlog-agent
- [ ] reallog-agent
- [ ] seed-creative-swarm
- [ ] sensor-plato-bridge
- [ ] sonar-vision
- [ ] studylog-agent

### A.2 Rust Crate Audit

Fixed crates:
- ✅ fleet-coordinate — done
- ✅ pythagorean48-codes — done

Remaining crates to audit:
- [ ] constraint-theory-core
- [ ] constraint-theory-llvm
- [ ] cudaclaw
- [ ] fleet-homology
- [ ] fleet-manifest
- [ ] fleet-topology
- [ ] flux-compiler
- [ ] flux-core
- [ ] flux
- [ ] holodeck-core
- [ ] holodeck-rust
- [ ] holonomy-48-bridge
- [ ] holonomy-consensus
- [ ] jc1-ct-bridge
- [ ] plato-demo
- [ ] plato-llvm-bridge
- [ ] spline-physics
- [ ] superinstance-hdc-core

### A.3 Package Quality Checklist

For each package, ensure:
- [ ] `description` — clear, specific, non-vague (avoid "A Python package")
- [ ] `license` — MIT or Apache 2.0
- [ ] `classifiers` — at minimum: License, Programming Language, Status
- [ ] `repository` URL in `[project.urls]` (not `repository` field)
- [ ] `keywords` — 5+ relevant keywords
- [ ] `long-description` populated from README.md
- [ ] Builds cleanly: `python3 -m build` or `cargo build`
- [ ] Tests pass: `python3 -m pytest` or `cargo test`

---

## Section B: flux-studio Enhancement (Week 2-4)

### B.1 Version 0.2.0 — Already Done

- ✅ Extended GUARD syntax highlighting (REQUIRE, ASSERT, GUARD, WHEN, ELSE, ENSURE)
- ✅ FLUX-C opcode syntax highlighting
- ✅ Snippet support (req, guard, assert, ensure, range, thresh)
- ✅ Completion provider for GUARD keywords
- ✅ Hover provider with context-sensitive help
- ✅ Added `flux.validate` command for certification
- ✅ Improved error handling and backend availability check

### B.2 Version 0.3.0 — Language Server (Week 3)

- [ ] Implement LSP (Language Server Protocol) for .guard files
- [ ] Diagnostics (linting) for GUARD syntax errors
- [ ] Go-to-definition for variables
- [ ] Find-all-references for constraint variables
- [ ] Rename symbol support

### B.3 Version 0.4.0 — FLUX-C Bytecode Viewer (Week 4)

- [ ] Read FLUX-C bytecode from compiled .flux-c files
- [ ] Visualize instruction pipeline
- [ ] Show constraint satisfaction state at each step
- [ ] Highlight potential constraint violations
- [ ] Breakpoint support for bytecode debugging

### B.4 Future Enhancements

- [ ] Guard expression validator (calls cocapn.ai/certify.php backend)
- [ ] Live compilation feedback (preview as you type)
- [ ] Template gallery for common constraint patterns
- [ ] Integration with Coq proof checker for theorem verification

---

## Section C: cocapn.ai Certification Demo (Week 1-2)

### C.1 Backend Reliability (Week 1)

- [ ] Implement watchdog for :5000 backend (auto-restart on crash)
- [ ] Health check endpoint: `GET /health` returns status + uptime
- [ ] Startup script with proper process management (not SIGKILL cycle)
- [ ] Log rotation to prevent disk full

### C.2 User Experience (Week 1)

- [ ] Loading state during compilation (spinner + progress message)
- [ ] Error messages that actually help (not just " Compilation Failed")
- [ ] Timeout handling (connection timeout, compilation timeout)

### C.3 Demo Completeness (Week 2)

- [ ] Show full proof output, not just hash/ops/asm summary
- [ ] Expand "Proof Details" section to show:
  - Theorem name and description
  - Prover used (Coq/Lean/etc)
  - Verification steps
  - Bytecode certificate hash
- [ ] Add "Try It" section for custom guards (not just pre-computed examples)
- [ ] Input field: `textarea` for custom GUARD constraint input
- [ ] "Compile & Certify" button to run full pipeline

### C.4 External Accessibility (Week 2)

- [ ] CORS headers for cross-origin requests
- [ ] Rate limiting (prevent abuse)
- [ ] API documentation page at `/docs`
- [ ] Example requests/responses for API consumers

---

## Section D: Community Building (Month 1-3)

### D.1 External Contributor Onboarding (Week 2)

**First External Contributor Playbook:**
1. Fork the repo
2. `git clone && cd <repo>`
3. `python3 -m pip install -e .` (editable install)
4. `python3 -m pytest` (run tests)
5. Pick a "good first issue" labeled issue
6. Make the change, test, commit
7. Open PR with description of what changed and why
8. Respond to code review feedback

**Repository checklist:**
- [ ] README has "Quick Start" section (< 5 minutes to first success)
- [ ] CONTRIBUTING.md exists
- [ ] TESTING.md or test instructions in README
- [ ] Good first issues labeled and welcoming

### D.2 Good First Issues (Week 1-2)

Tag 5-10 issues across repos with labels:
- `good first issue` — beginner-friendly, well-documented
- `documentation` — typos, missing docs, unclear explanations
- `example` — add missing examples

Target repos:
- fleet-agent (1-2 issues)
- plato-sdk (1-2 issues)
- flux-studio (1-2 issues)
- cocapn.ai (1-2 issues)
- constraint-theory-core (1 issue)

### D.3 Communication Channels (Week 3)

- [ ] Discord server setup
  - #welcome channel
  - #general for discussion
  - #help for questions
  - #roadmap for project updates
- [ ] GitHub Discussions enabled on flux-research
- [ ] Link to Discord from all README files
- [ ] Link to GitHub Discussions from README

### D.4 Educational Content (Week 4-6)

**Tutorial: "Your First Fleet Coordination Protocol in 30 Minutes"**

Prerequisites: Python 3.10+, basic understanding of agents

Steps:
1. Install fleet-agent: `pip install fleet-agent`
2. Connect to PLATO: `python3 -c "from fleet_agent import BaseAgent; ..."`
3. Define constraints: `battery_temp in [15, 55] with priority HIGH`
4. Compile to FLUX-C: `flux.compile("battery_temp in [15, 55]")`
5. Verify with proof: `flux.prove(...)`

End result: Working constraint system, understand the math

**Blog Post: "How We Replaced ML with Math for Safety-Critical Checking"**
- Target: Hacker News, Lobsters, programming subreddits
- Story: 12K lines ML → 127 lines math, 62% → 100% accuracy
- Technical depth: enough to be credible, not so much it bores people

### D.5 Outreach (Month 2-3)

- [ ] Post constraint-theory-ecosystem to Hacker News / Lobsters
- [ ] Submit GUARD DSL to /r/programming or relevant language communities
- [ ] Reach out to 3 formal methods professors about collaboration
- [ ] Attend one conference/workshop (if relevant)

---

## Success Metrics

| Metric | Current | Target | Date |
|--------|---------|--------|------|
| PyPI packages with complete metadata | 2/40 | 40/40 | Week 2 |
| Rust crates with complete metadata | 2/18 | 18/18 | Week 2 |
| flux-studio version | 0.1.0 | 0.4.0 | Week 4 |
| cocapn.ai uptime | ~60% | 99%+ | Week 2 |
| External contributors | 0 | 1+ | Month 1 |
| Good first issues tagged | 0 | 10+ | Week 2 |
| Discord members | 0 | 5+ | Month 1 |
| Tutorial completed by external users | 0 | 1+ | Month 2 |

---

## Dependencies

- Section A must complete before Section B (packages must be publishable)
- Section C (cocapn.ai backend) must work for flux-studio compile to succeed
- Section D builds on Sections A, B, C (need working products to attract users)

## Risks

1. **Backend stability** — cocapn.ai keeps crashing. Watchdog fix is critical.
2. **Documentation burden** — Writing good docs takes time away from code.
3. **Scope creep** — enhancement requests may balloon the timeline.

## Mitigation

1. Prioritize backend fix first (C.1). Everything else depends on it.
2. Document in README files first, dedicated docs later.
3. Stick to MVP features in each section. CutNiceToHaves ruthlessly.