# Build Artifact Cleanup — 2026-07-12

## Summary

Systematic cleanup of committed build artifacts and bloated git history across SuperInstance repositories. Removed tracked `target/`, `.zig-cache/`, `__pycache__/`, `*.o`, `node_modules/`, `*.wav`, and other build artifacts from both the working tree and git history using `git rm --cached` and `git-filter-repo`.

## Before / After Sizes

| Repo | Before | After | Reduction | Notes |
|------|--------|-------|-----------|-------|
| **flux-hardware** | 35 MB | 1.7 MB | 95% | Rust `target/` dirs in `hdc/flux-hdc-rust/` and `bridge/` removed from history; stale `master` branch deleted |
| **lau-lie-group-agents** | 434 MB | 396 KB | >99% | 1,081 tracked `target/` files removed; history rewritten to purge ~430 MB of Rust build artifacts |
| **flux-zig** | 74 MB | 1.7 MB | 97% | 35 tracked `.zig-cache/` files + `flux-zig.o` removed; history rewritten; branch protection temporarily lifted |
| **plato-portal** | 279 MB | 13 MB | 95% | `node_modules/`, `target/`, `*.wav`, `*.png`, `*.db-wal` purged from history; 5 stale branches deleted (carried old objects) |
| **plato-engine-block** | 8.0 MB | 348 KB | 96% | `target/` (Rust build cache) purged from history |
| **grand-pattern-rs** | 4.6 MB | 260 KB | 94% | `target/` purged from history; .gitignore expanded |
| **ternary-science** | 4.4 MB | 340 KB | 92% | `target/` purged from history; .gitignore expanded |
| **crab** | 288 KB | 240 KB | 17% | `__pycache__/crab.cpython-310.pyc` removed; history rewritten; .gitignore added |
| **Total** | **~840 MB** | **~18 MB** | **~98%** | |

## Actions Performed

### Repos with Currently-Tracked Artifacts (git rm --cached + filter-repo)

1. **flux-zig** — Removed 35 files: `.zig-cache/` directory (hash cache, object files, test binaries) and `flux-zig.o`. Added comprehensive Zig `.gitignore`. Branch protection on `main` temporarily lifted for force-push, then restored.

2. **lau-lie-group-agents** — Removed 1,081 files from `target/` (Rust debug build artifacts including `.rlib`, `.rmeta`, `.so`, incremental compilation caches, and a package crate). Fixed `.gitignore` (previous had literal `\n`). History rewritten from 434 MB → 396 KB.

3. **crab** — Removed `__pycache__/crab.cpython-310.pyc`. Added Python `.gitignore`.

### Repos with History-Only Artifacts (filter-repo)

4. **flux-hardware** — No currently-tracked artifacts, but git history contained Rust `target/` directories under `hdc/flux-hdc-rust/` and `bridge/` (~33 MB of `.rlib`, `.rmeta`, build scripts). Filter-repo purged all `*/target/` paths. Also deleted stale `master` branch (separate divergent history with artifacts).

5. **plato-portal** — No currently-tracked artifacts but 264 MB `.git` directory from: `node_modules/typescript/`, `constraint-substrate/rust/target/`, multiple `*.wav` audio files (46 MB pythagorean_comma_concert.wav, 11 MB miles_explore.wav), `*.f64` benchmark outputs, `*.db-wal` files. Two-pass filter-repo cleaned history. Deleted 5 stale branches (`fix-cache-race-2026-07-09`, `honest-readme-2026-07-08`, `master`, `narrative-consistency-2026-07-09`, `tone-pass-2026-07-09`) that kept old objects reachable.

6. **plato-engine-block** — `target/` in git history (7.5 MB debug binary + incremental caches). Filter-repo purged.

7. **grand-pattern-rs** — `target/` in git history (6.9 MB debug binary + incremental caches). Filter-repo purged.

8. **ternary-science** — `target/` in git history (7.1 MB debug binary + incremental caches). Filter-repo purged.

## .gitignore Coverage

All repos now have comprehensive `.gitignore` files covering:
- **Rust:** `target/`, `Cargo.lock`
- **Zig:** `.zig-cache/`, `zig-out/`, `*.o`
- **Python:** `__pycache__/`, `*.pyc`, `.pytest_cache/`, `build/`, `dist/`, `*.egg-info/`
- **Node:** `node_modules/`
- **IDE:** `.vscode/`, `.idea/`, `*.swp`, `.DS_Store`
- **Misc:** `*.log`, `.env`

## Methodology

1. **Clone** each repo fresh
2. **Scan** for tracked artifacts: `git ls-files | grep -E '(target/|\.zig-cache/|__pycache__/|\.o$|node_modules/)'`
3. **Remove from index**: `git rm -r --cached <artifact>`
4. **Add .gitignore** with comprehensive patterns
5. **Commit**: "Clean committed build artifacts, add .gitignore"
6. **Rewrite history**: `git filter-repo --invert-paths --path target/` to purge artifacts from all commits
7. **Garbage collect**: `git reflog expire --expire=now --all && git gc --prune=now --aggressive`
8. **Force push**: Rewritten history pushed with `git push --force`
9. **Delete stale branches**: Branches with old history that kept artifacts reachable
10. **Verify**: Fresh clone to confirm size reduction and artifact removal

## Tools Used

- `git rm --cached` — Remove artifacts from git index (non-destructive to working tree)
- `git-filter-repo` — Rewrite git history to purge large objects from all commits
- `git gc --aggressive --prune=now` — Remove unreachable objects from local clone
- `gh api` — Delete stale remote branches, manage branch protection
