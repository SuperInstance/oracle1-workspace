# Rebirth: adaptive-plato-early-version (#71)

**Status:** ⚰️ Archived | **Found:** 2026-05-15 | **Forgotten Gold Level:** HIGH

## What Was Here

An early adaptive PLATO experiment — the `adaptive_plato.py` module that adjusts PLATO room structure based on the consuming model's capability. Archived as "superseded by plato-sdk" but the actual *algorithm* and *content adaptation logic* was never ported.

## Forgotten Gold

The `adaptive_plato.py` file is a **complete, production-quality content adaptation pipeline** that solves a real problem PLATO-NG still needs:

1. **Model Profile Detection** — Auto-detects model capability from name (tiny ≤1B, mid 1-30B, large 30B+) with 50+ regex patterns and numeric-size fallbacks. Knows about Qwen3, GLM, Seed-2.0, Claude, Gemini, DeepSeek, etc.

2. **Profile-Dependent Formatting** — Three distinct formatters:
   - `tiny`: Strip ALL PLATO tags, return plain text. Context can be prepended for small models.
   - `mid`: Full PLATO structure with `[KEY:]`, `[DOMAIN:]`, `[CROSS-REF:]`, `[WARNING:]` — the full semantic markup.
   - `large`: Keys-only minimal structure. No domain tags, no cross-refs. The model is smart enough to infer context.

3. **Scoring Pipeline** — Rooms are scored by combined: relevance (keyword/density), recency (time-decay), and domain density (structural richness). This means the right room gets the right format.

4. **30+ Comprehensive Tests** — Every profile, every edge case, CLI integration tests, tag stripping, auto-detection of every known model variant. This test suite is itself valuable — it documents every model relationship.

5. **Real PLATO Room Data** — `rooms.json` contains 10 real PLATO rooms (Constraint Theory, Fleet Ops, Architecture Spec, Model Matrix, Proof Forging, I2I Protocol, Research Log, Oracle1 Digest, Boot Protocol, Agent Roster). These are gold for testing PLATO-NG retrievals.

## Why It Belongs in PLATO-NG

PLATO-NG has tile lifecycle, Lamport clocks, content-addressed storage — but **no content adaptation layer**. When a small model queries PLATO, it should get stripped plain text. When a large model queries, it gets keys-only. The adaptive formatter fills this exact gap.

**Action:** Port `adaptive_plato.py` as `plato-sdk` middleware or a `plato-formatter` package. The scoring pipeline should consume the same simulation-first predictions. The model detection patterns should be a shared registry across the fleet.

## What to Rescue
- `adaptive_plato.py` — full content adaptation engine
- `test_adaptive_plato.py` — reference test suite
- `rooms.json` — test fixture PLATO rooms
- `__pycache__` pyc files — skip, rebuild from source
