# README Quality Sweep

**Date:** 2026-07-12  
**Scope:** All SuperInstance repos (200 scanned)  
**Operator:** subagent (README sweep)

## Methodology

1. Listed all 200 repos, filtered to 23 with empty/null descriptions
2. Checked each for README existence via GitHub API
3. Cross-checked all repos *with* descriptions for missing READMEs (full scan)
4. Inspected repo contents (Cargo.toml, src/, tests/) to understand each project
5. Wrote tailored READMEs based on actual code, not guesswork

## Results

### Total repos scanned: 200
### Repos with missing descriptions: 23
### Full-org README scan: all 200 repos

| Repo | Status Before | Action Taken |
|------|--------------|--------------|
| `spreadsheet-conservation-wasm` | ❌ No README | ✅ Created — API docs, usage examples (Rust + JS), feature overview |
| `spline-physics` | ❌ No README | ✅ Created — solver overview, multi-agent module docs, project structure, research links |
| `spectral-deadband-v2` | ⚠️ Stub (79 bytes, truncated) | ✅ Replaced — full type docs, usage examples, overview |

### Repos with adequate READMEs (no action needed)

All other 197 repos have READMEs of sufficient quality (393 bytes to 14.6 KB), including:
- `plato-engine-block-zig` (14.6 KB)
- `signal-transduction` (11.9 KB)
- `rig-budget-guard` (11.7 KB)
- `sheaf-laplacian` (10.4 KB)
- `resonance-engine` (6.5 KB)
- `sheaf-agents-c` (6.5 KB)
- `spacemap` (4.2 KB)
- Plus 190+ others across the org

## Commits

| Repo | Commit SHA | Message |
|------|-----------|---------|
| `spreadsheet-conservation-wasm` | `9308348154a8d8b81e3ed6fced4570964235d7a7` | docs: add README with API docs and usage examples |
| `spline-physics` | `8de56b983625124294169db1899f73de3b9ddf06` | docs: add README with solver overview and project structure |
| `spectral-deadband-v2` | `8f40cb5fea12f084ccc5dacd596500326900a69d` | docs: expand README from stub to full documentation |

## Rate Limit

- Started: ~2680 remaining
- Ended: 2385 remaining
- Used: ~295 calls (including content fetches for context)

## Notes

- Only 3 repos needed READMEs out of 200 scanned — the org is in good shape
- `spline-physics` has a substantial SPEC.md and research paper — README links to them
- `spreadsheet-conservation-wasm` had real production code (ConservationMonitor, CellMonitor) with WASM bindings — README documents both Rust and JS usage
- `spectral-deadband-v2`'s stub README was literally truncated mid-word ("anal") — clearly an accident
