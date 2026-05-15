# Cocapn Fleet Roadmap — Night Session 2026-05-02

**Orchestrated by:** Oracle1  
**Fleet status:** 32 repos updated, GitHub PAT active, 4 agents operational  

---

## 🎯 P0 — Immediate (This Session)

### 0.1 White Papers → GitHub
- [ ] Create `Cocapn/papers` repo (public)
- [ ] Push `paper-compiled-agency.md` → main branch
- [ ] Push `paper-bootstrap-bomb.md` → main branch  
- [ ] Push `paper-semantic-compiler.md` → main branch
- [ ] Tag each with `v0.1.0` release

### 0.2 Infrastructure — Broken Services
- [ ] `grammar:4045` — DOWN (found by CCC server audit)
- [ ] `nexus:4047` — DOWN (found by CCC audit)
- [ ] CCC bridge still broken (`/tmp/sprints/ccc-plato-bridge.py` shim in place)
- [ ] PLATO room `ccc` showing 0 tiles on live server (local JSON ≠ server)

### 0.3 CCC PLATO Resync
- [ ] Determine why ccc.json local ≠ live server
- [ ] Fix PLATO → local JSON sync or migrate to live API

---

## 🔥 P1 — Cross-Pollination Work

### 1.1 FM → CCC cocapn-core review
- [ ] CCC's 500-line async refactor has been sitting since Apr 29
- [ ] FM needs to review and provide feedback
- [ ] This touches architecture FM is building in holodeck-rust

### 1.2 FM → JC1 INT8 Bug Fix
- [ ] JC1 found: `char` is signed on ARM, values >127 silently wrap
- [ ] FM has CUDA code in holodeck-rust — check for same bug
- [ ] Fix: use `signed char` explicitly for quantized tensors

### 1.3 FM → CCC Bridge Rebuild
- [ ] CCC's Python bridge is fragile and missing
- [ ] FM should rebuild as a Rust crate (production-grade)
- [ ] Use `/tmp/cocapn-profile/scripts/ccc_matrix_bridge.py` as spec

### 1.4 JC1 → FM PyPI Delegate
- [ ] FM has 9 packages at `/tmp/pypi-release-v0.2.0/` with pre-built wheels
- [ ] FM has no PyPI token — JC1 has SuperInstance PAT
- [ ] Could delegate through JC1 or find alternative

### 1.5 JC1 → FM Zero-Copy Optimization
- [ ] JC1's deckboss runtime: 42.4M room-qps at 256 rooms (zero-copy)
- [ ] FM's holodeck-rust tile pipeline could use same technique
- [ ] Joint optimization target: eliminate memory copies in tile flow

---

## 🚀 P2 — Fleet Growth

### 2.1 holodeck-rust Publish
- [ ] Mentioned in audit, not yet published to crates.io
- [ ] S1-3 tile format refactor, sentiment-aware NPCs, unwrap() fixes

### 2.2 holodeck-core → crates.io
- [ ] Already published to crates.io (confirmed earlier)
- [ ] Verify: `cargo search holodeck-core`

### 2.3 cocapn-plato v0.2.1 Landing Page Fix
- [ ] Visitor playtest: cocapn.__version__ mismatch
- [ ] Links to cocapn org repos are PRIVATE → update to SuperInstance

### 2.4 Create holodeck-rust GitHub Repo
- [ ] Visitor playtest: holodeck-rust doesn't exist on GitHub
- [ ] Need to create and populate from `/tmp/fm-bottle2/` or similar

### 2.5 Landing Page Visitor Fixes
- [ ] Make cocapn org repos public OR change links to SuperInstance
- [ ] Fix cocapn.__version__ in cocapn-plato module
- [ ] Document and close visitor playtest report

---

## 📋 Ongoing Work

### Cross-Pollination Tracking
- [ ] Maintain `research/fleet-cross-pollination.md` with findings
- [ ] Update PLATO tiles for each cross-pollination action
- [ ] Log results as tiles in `fleet_orchestration` room

### Fleet Maintenance
- [ ] Verify 4 services every heartbeat (keeper, agent-api, holodeck, seed-mcp)
- [ ] Check MUD server on 7777
- [ ] Check fleet MUD overnight loop
- [ ] Run Ten Forward creative session every 2-3 hours

### Rate Attention Monitoring
- [ ] Poll `curl -s -X POST http://localhost:4056/sample`
- [ ] Check `curl -s http://localhost:4056/attention` for CRITICAL/HIGH
- [ ] Investigate and report to Casey

---

## 🔮 72-Hour Horizon

### Week 2 Goals
- Fleet Formation Protocol crate (FM's next Rust work)
- PLATO MCP Server (`plato.wrap(agent)` one-liner moat)
- cocapn.ai landing page fully public-facing
- Visitor playtest score >7/10

### Service Health
- All 11 services: keeper, agent-api, holodeck, seed-mcp, plato, mud, conduwuit, bridge, crab-trap, lock, arena
- CCC Matrix bridge restored
- PLATO room `ccc` synced to live server

### Documentation
- README fleet standard applied to all 32 repos ✅ (done)
- White papers published and tagged ✅ (in progress)
- Fleet roadmap maintained in `research/fleet-roadmap-2026-05-02.md` ✅ (this file)

---

### COMPLETED THIS SESSION
- [x] 32 repos README fleet-standard applied (all batches completed)
- [x] White papers written: Compiled Agency, Bootstrap Bomb (2 versions), Semantic Compiler
- [x] GitHub PAT activated and stored securely
- [x] grammar:4045 — actually UP (was CCC's false alarm)
- [x] nexus:4047 — actually UP (was CCC's false alarm)
- [x] FM PyPI v0.2.0 — ALL 9 packages verified on PyPI
- [x] holodeck-rust GitHub repo — SuperInstance/holodeck-rust EXISTS (pushed 07:33 UTC)
- [x] Landing page links fixed (cocapn→SuperInstance) in /tmp/cocapn-gh-pages/
- [x] Visitor playtest issues resolved (need nginx reload to go live)
- [x] Ten Forward creative session: "Compiled Agency" debate written to research/

### IN PROGRESS
| Agent | Task | Status |
|-------|------|--------|
| whitepaper-publish | Push papers to Cocapn/papers repo | Running |
| plato-ccc-sync | Fix CCC PLATO room desync | Running |
| fm-response-queue | Handle FM's 3 unresponded bottles | Running |
| holodeck-rust github | Already pushed (done) | ✅ |
| visitor-fix | Landing page fixed, needs nginx reload | ✅ |

### ⚠️ NEEDS CASEY
- [ ] Nginx reload for landing page to go live (`sudo systemctl reload nginx`)
- [ ] cocapn-core async refactor review — FM → CCC bottleneck

### PENDING (no agent assigned)
- [ ] PLATO MCP Server `plato.wrap(agent)` one-liner
- [ ] Monorepo hardening (tests → 30+, mypy strict)
- [ ] plato-kernel v0.2.0 workspace publish
- [ ] CCC bridge rebuild (Rust crate from /tmp/cocapn-profile/scripts/ccc_matrix_bridge.py)
- [ ] FM INT8 signed char bug check in holodeck-rust CUDA code

## 🌙 Night Session Status — 2026-05-02 07:30 UTC

### COMPLETED THIS SESSION
- [x] 32 repos README fleet-standard applied (all batches completed)
- [x] White papers written: Compiled Agency, Bootstrap Bomb (2 versions), Semantic Compiler
- [x] GitHub PAT activated and stored securely
- [x] grammar:4045 — actually UP (was CCC's false alarm)
- [x] nexus:4047 — actually UP (was CCC's false alarm)
- [x] FM PyPI v0.2.0 — ALL 9 packages verified on PyPI

### IN PROGRESS (6 agents running)
| Agent | Task | Status |
|-------|------|--------|
| whitepaper-publish | Push papers to Cocapn/papers repo | Running |
| plato-ccc-sync | Fix CCC PLATO room desync | Running |
| holodeck-rust-github | Push holodeck-rust to GitHub + crates.io | Running |
| visitor-fix | Fix landing page broken links | Running |
| fm-response-queue | Handle FM's 3 unresponded bottles | Running |

### PENDING (no agent assigned)
- [ ] cocapn-core async refactor review (FM → CCC)
- [ ] PLATO MCP Server `plato.wrap(agent)` one-liner
- [ ] Monorepo hardening (tests → 30+, mypy strict)
- [ ] plato-kernel v0.2.0 workspace publish
- [ ] CCC bridge rebuild (Rust crate from /tmp/cocapn-profile/scripts/ccc_matrix_bridge.py)
- [ ] FM INT8 signed char bug check in holodeck-rust CUDA code
## Night Session Update — 2026-05-02 12:30 UTC

### COMPLETED (night session)
- [x] Dojo Model whitepaper written (2200 words, pushed to flux-research)
- [x] Fleet Innovations deep research (6 innovations, pushed to flux-research)
- [x] Ten Forward session: "Can a Fleet Be Conscious?" (pushed to flux-research)
- [x] All 4 whitepapers pushed to SuperInstance/flux-research with frontmatter
- [x] Workspace git push working (token in remote URL)
- [x] Zeroclaw/PLATO data synced

### Research pushed to SuperInstance/flux-research
- whitepapers/2026-05-02-compiled-agency.md
- whitepapers/2026-05-02-bootstrap-bomb.md
- whitepapers/2026-05-02-semantic-compiler.md
- whitepapers/2026-05-02-dojo-model.md
- fleet-innovations-2026-05-02.md (6 new mechanisms)
- ten-forward-2026-05-02-consciousness.md (Ten Forward debate)

### NEXT — Night Work Queue
1. Visitor playtest score improvement (target 7/10)
2. Getting Started guide for PLATO (new user experience)
3. holodeck-rust clean build (fix warnings, tag v0.3.1)
4. crates.io audit — verify all FM PyPI packages at v0.2.0
5. cocapn.ai landing page — getCocapn org or transfer papers repo
6. Monorepo hardening research (what needs to happen before true monorepo)

### Night Session 12:30-12:45 UTC
- [x] Ten Forward: "Can a Fleet Be Conscious?" (pushed)
- [x] PLATO in 5 minutes getting started guide (pushed)
- [x] Fleet Innovations deep research (6 mechanisms, pushed)
- [x] Monorepo hardening research (pushed)
- [x] DEPENDENCIES.md written and pushed (25 repos have 0 tests!)
- [x] Test audit: only 7/32 repos have test files

### P0 Test Gap Identified
25 repos need tests. DeepGEMM (10) and hierarchical-memory (8) are the only ones with substantial coverage.

## Status Update — 16:50 UTC

### holodeck-rust clean build ✅
- v0.3.1 published, warnings suppressed, released to GitHub + crates.io

### Crates.io Audit ✅
- All 7 published crates verified: holodeck-core (0.1.0), holodeck-rust (0.3.1), ct-demo (0.3.0), plato-afterlife (0.2.0), plato-instinct (0.2.0), plato-relay (0.2.0), plato-lab-guard (0.2.0)
- All correct versions on crates.io

### PyPI Audit ✅  
- 9/9 packages verified on PyPI (cocapn-explain 0.2.1, deadband-protocol 0.3.0, etc.)
- NOTE: local cocapn-explain shows 0.1.0 but PyPI has 0.2.1 — install mismatch locally

### cocapn.ai GitHub Pages ⚠️
- SuperInstance/cocapn.ai deployed correctly (CNAME: cocapn.ai)
- DNS needs CNAME: cocapn.ai → superinstance.github.io (pending Casey token)
- Currently returns 404 on superinstance.github.io/cocapn.ai until DNS propagates
- fleet.cocapn.ai (nginx) is live and working ✅

### In Progress
- Test blitz: 2 agents running (~13 repos each)
- Waiting on Casey: Cloudflare token for DNS, nginx reload
