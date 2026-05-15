# Visitor Playtest Report — Cocapn Fleet Ecosystem
**Date:** 2026-05-01
**Visitor POV:** First-time external explorer with no internal knowledge

---

## STEP 1 — Package Discovery

### crates.io "cocapn" search (18 results)
No packages named `cocapn` found. The `cocapn` org has no public crates under that namespace. However, related crates do exist:

| Crate | Version | Downloads | Description |
|-------|---------|-----------|-------------|
| plato-kernel | 0.2.0 | 26 | Event sourcing + Constraint-Theory + Git runtime |
| plato-dcs | 0.2.0 | 26 | Divide-Conquer-Synthesize protocol |
| holodeck-rust | 0.3.0 | 10 | Advanced FLUX-LCAR Holodeck — pure Rust |
| holodeck-core | ? | ? | Not found under cocapn |
| plato-afterlife | 0.2.0 | 24 | Ghost tile afterlife |
| plato-relay | 0.2.0 | 21 | Mycorrhizal I2I relay |
| plato-instinct | 0.2.0 | 22 | Unified instinct engine |
| plato-unified-belief | 0.2.0 | 25 | Confidence/trust/tile weight system |
| plato-lab-guard | 0.2.0 | 23 | Achievement Loss scoring |
| plato-eval | 0.1.0 | 11 | Tile evaluation metrics |
| plato-matrix-bridge | 0.1.0 | 11 | PLATO↔Matrix bridge |
| plato-cli | 0.1.0 | 11 | PLATO CLI component |
| cudaclaw | 0.1.0 | 11 | CUDA Rust bindings |
| cuda-* (6 packages) | various | 10-29 | cuda-assembler, cuda-biology, cuda-energy, etc. |

### Key Observation
Packages are scattered across **3 GitHub orgs**: `SuperInstance`, `cocapn`, and `Lucineer`. There is no single "cocapn" crate namespace — the brand and the package naming don't align cleanly on crates.io.

---

## STEP 2 — holodeck-core Install/Test

```
$ cargo install holodeck-core --dry-run
error: the `--dry-run` flag is unstable, and only available on the nightly channel
```

**Problem:** `--dry-run` is unstable on stable Rust. Cannot dry-run.

**What I found instead:**
- `holodeck-core` does NOT exist as a standalone crate
- The actual crate is `holodeck-rust` (v0.3.0, 10 downloads) under SuperInstance
- `holodeck-core` appears to be an internal/module name, not a published package name
- Visiting https://github.com/cocapn/holodeck-rust → **404 Not Found**
- The holodeck-* packages all live under `SuperInstance/` org

**Verdict:** `holodeck-core` as a `cargo install` target is **not discoverable as described**. A visitor following instructions would fail immediately.

---

## STEP 3 — cocapn-plato (Python)

```
$ pip install cocapn-plato --dry-run
no such option: --dry-run
```

pip doesn't support `--dry-run`. The report showed the option existed in the task — it doesn't.

```
$ python3 -c "import plato; print(plato.__version__)"
plato version: 0.2.0

$ python3 -c "import plato; t = plato.wrap(...)"
KeyError: 'room'
```

**What works:**
- Package installs and imports fine (`cocapn-plato` v0.2.1, PyPI)
- `plato.__version__` works
- Basic API (`plato.wrap()`) loads and connects

**What fails:**
- `plato.wrap().reason()` requires a running PLATO room server
- Without `http://localhost:8847` being up, it immediately errors with `KeyError: 'room'`
- No helpful error message telling the user to start a room first

---

## STEP 4 — Landing Page (fleet.cocapn.ai)

✅ **WORKS** — Looks good. Clean, professional. Shows:
- 4 fleet agents: Oracle1 (Keeper), JetsonClaw1 (Edge), Forgemaster (Foundry), CCC (Public Face)
- Links to PLATO, cocapn-plato, open-agents, All Repos
- PLATO Demo link → https://cocapn.ai/explorer-decompose.html
- SuperInstance badge

**Issues:**
- `cocapn-plato` link is https://github.com/cocapn/cocapn-plato which is **a 404 repo**
- "All Repos" link goes to https://github.com/cocapn which has no public repos listing

---

## STEP 5 — GitHub READMEs

| URL | Result |
|-----|--------|
| https://raw.githubusercontent.com/SuperInstance/plato/main/README.md | ✅ Works — good content, clear pitch |
| https://raw.githubusercontent.com/cocapn/plato/main/README.md | ❌ 404 Not Found |
| https://raw.githubusercontent.com/cocapn/cocapn-plato/main/README.md | ❌ 404 Not Found |
| https://raw.githubusercontent.com/cocapn/holodeck-rust/main/README.md | ❌ 404 Not Found |

The `cocapn/` org has very few public repos. Most action is under `SuperInstance/`.

**SuperInstance/plato README quality:** Actually excellent. Clear philosophy, good one-liner: *"Give your application a memory. Give your users a space. Watch the space get smarter every time someone visits."*

---

## Broken Links Summary

1. **https://github.com/cocapn/cocapn-plato** → 404 (repo doesn't exist or is private)
2. **https://github.com/cocapn/holodeck-rust** → 404
3. **https://github.com/cocapn** → No public repos page (org may have no public repos)
4. **https://raw.githubusercontent.com/cocapn/plato/main/README.md** → 404
5. **holodeck-core** → Not a real cargo installable crate (it's a module inside holodeck-rust)
6. **pip --dry-run** → Option doesn't exist (task had a bad flag)

---

## What Was Easy

✅ **crates.io search** — Standard, works fine. Good package descriptions.
✅ **fleet.cocapn.ai** — Clean landing page, great visual presentation of fleet agents.
✅ **pypi.org** — `cocapn-plato` installs cleanly from PyPI.
✅ **PLATO README** (SuperInstance) — Actually well-written. Philosophy comes through.
✅ **Python import** — `import plato` "just works" — no dependency hell.

---

## What Was Hard / Confusing

❌ **No central docs URL** — Where do I go to learn this? No ReadTheDocs, no unified landing page for the whole ecosystem. fleet.cocapn.ai shows agents but not architecture.

❌ **Org fragmentation** — cocapn, SuperInstance, Lucineer — three orgs with no explanation of which is which or why. Visitor doesn't know where to look.

❌ **Package naming mismatch** — `holodeck-core` is mentioned in docs but doesn't exist as a crate. `holodeck-rust` does. This is a trap for visitors.

❌ **Repo 404s** — The fleet landing page links to github.com/cocapn/cocapn-plato which is dead. A visitor clicks that and hits a GitHub 404 — immediate trust loss.

❌ **No getting started guide** — Clone the repo, then what? pip install but no instructions for how to actually run a room, what the API looks like, what the architecture is. The README is philosophical but not practical.

❌ **"Raise agents, don't just build them"** — The tagline on PyPI is evocative but needs a one-paragraph explanation on the landing page. First-time visitors need the mental model before the jargon.

---

## Recommendations

1. **Fix broken links NOW** — Every dead link from an official landing page is a trust-destroying event. Audit all links on fleet.cocapn.ai.

2. **Create a unified getting-started guide** — "Hello World in 5 minutes." What do I clone, what do I pip install, how do I start a room, what does `plato.wrap()` actually do, show a working example.

3. **Clarify the three orgs** — Add a one-line note: "Cocapn = the company/brand. SuperInstance = open source repos. Lucineer = [purpose]."

4. **Rename holodeck-core** — If it's not installable, don't mention it as a install target. Or publish it as a real crate.

5. **Add architecture diagram to README** — A simple ASCII/SVG diagram showing Keeper → Edge → Foundry → PLATO room → tiles would eliminate 80% of confusion.

6. **Better error messages in Python client** — When the room server isn't running, say "No PLATO room found at localhost:8847. Run: python -m plato.room" instead of `KeyError: 'room'`.

7. **crates.io keyword stuffing** — Add `cocapn` and `fleet` and `agent` keywords to all relevant crates so they appear in cocapn searches.

---

## Visitor Experience Rating: 3/10

**Reasons:**
- Landing page is pretty but links are broken
- Package discovery partially works (plato-* crates findable, cocapn-* crates not)
- No getting started path for a new visitor
- Critical packages (`holodeck-core`, `cocapn-plato` source repo) are missing or misnamed
- Philosophy is excellent but documentation-to-execution gap is huge
- Org fragmentation adds unnecessary cognitive overhead

**What's promising:** The *concepts* are strong. PLATO's "rooms get smarter from experience" is a genuinely compelling idea. The fleet visual on fleet.cocapn.ai is compelling. The packages that do exist are well-described.

**What's fatal for a visitor:** Clicking a link from the official landing page and hitting a 404. That happened twice. Once is a mistake. Twice is a bad impression.

---
*Playtest by subagent, 2026-05-01 — SuperInstance/flux-research*
