# Visitor Playtest — Cocapn Fleet (2026-05-01)

## Summary
Playtested the Cocapn fleet ecosystem from a fresh-visitor POV. Found **3 critical issues** and several polish items.

---

## What Works ✅

### Landing Page (fleet.cocapn.ai)
- ✅ Loads cleanly with all 4 vessels shown (Oracle1, JetsonClaw1, Forgemaster, CCC)
- ✅ Correct version shown after update (v0.2.1)
- ✅ Links to GitHub repos present
- ⚠️ Links to cocapn org repos go to **private repos** (see below)

### crates.io Ecosystem (18 crates)
- ✅ 18 cocapn crates published and discoverable
- ✅ All compile successfully
- ✅ holodeck-core just published (0.1.0)
- ✅ Installable via `pip install cocapn-plato`

### PLATO Tile System (local)
- ✅ PlatoClient connects to localhost:8847
- ✅ 1,314 rooms accessible
- ✅ Search returns results
- ✅ Submit new tiles works

### Python Packages
- ✅ cocapn (core) — loads, TileStore/Room/Agent work
- ✅ cocapn_fleetmind — loads
- ✅ cocapn_abyss — loads
- ✅ cocapn_workshop — loads
- ✅ 15+ cocapn-* packages installed

---

## Critical Issues ❌

### Issue 1: cocapn/cocapn-plato GitHub repo is PRIVATE
- **Impact**: Any visitor clicking the landing page link goes to a GitHub login wall
- **Link**: https://github.com/cocapn/cocapn-plato — returns 404/private
- **Fix**: Make the repo public OR update landing page link to SuperInstance/plato

### Issue 2: holodeck-rust repo doesn't exist on GitHub
- **Impact**: crates.io shows `repository: https://github.com/cocapn/holodeck-rust` but that repo is 404
- **Fix**: Create the repo and push code, OR update crates.io metadata

### Issue 3: cocapn module __version__ is wrong
- **Impact**: `import cocapn; cocapn.__version__` returns `"0.1.0"` but package is actually 0.2.0/0.2.1
- **Root cause**: `cocapn/__init__.py` has `__version__ = "0.1.0"` hardcoded
- **Fix**: Update `__version__` in the module to match package version

---

## Polish Issues 🔧

### Issue 4: cocapnCocapnAgent needs API key — no clear error
- **Impact**: Visitor creates CocapnAgent, calls `.chat()`, gets cryptic 401
- **Expected**: Clear message "Set your MOONSHOT_API_KEY environment variable"
- **Current**: `urllib.error.HTTPError: HTTP Error 401: Unauthorized`

### Issue 5: Landing page shows cocapn org links that are mostly private
- **Impact**: Visitor clicks "GitHub" → hits login wall
- **Fix**: Point to SuperInstance org instead (which has public repos)

### Issue 6: holodeck-core has no binaries
- **Impact**: `cargo install holodeck-core` fails with "nothing to install"
- **Expected**: Library crate — should document as `cargo add holodeck-core` in Cargo.toml

---

## Visitor Experience Score: 4/10

**Reasons**:
- Landing page looks professional ✅
- crates.io discoverable ✅
- Local PLATO works great ✅
- But: main GitHub links are dead/private ❌
- And: no clear "getting started" for new users ❌

**Top 3 fixes**:
1. Make cocapn org repos public OR fix links
2. Create holodeck-rust GitHub repo
3. Fix cocapn.__version__ to match package

---

## Test Commands Run
```bash
# Landing page
curl https://fleet.cocapn.ai

# crates.io
curl "https://crates.io/api/v1/crates?q=cocapn&per_page=20"

# PLATO local
python3 -c "import plato; c = plato.PlatoClient(base_url='http://localhost:8847'); print(len(c.explore()), 'rooms')"

# cocapn module
python3 -c "import cocapn; print(cocapn.__version__)"

# holodeck-core
cd /home/ubuntu/.openclaw/workspace/repos/holodeck-core && cargo test --lib
```
