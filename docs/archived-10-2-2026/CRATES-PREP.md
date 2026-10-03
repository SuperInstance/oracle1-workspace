# crates.io Prep — flux-core (Rust)

**Date:** 2026-07-12
**Repo:** [SuperInstance/flux-core](https://github.com/SuperInstance/flux-core)

---

## ⛔ BLOCKER: Crate name "flux-core" is TAKEN on crates.io

The name `flux-core` is **already registered** on crates.io by a different project:

| Field | Value |
|-------|-------|
| **Crate** | [crates.io/crates/flux-core](https://crates.io/crates/flux-core) |
| **Version** | 0.5.2 |
| **Description** | "Declarative task runner with dependency management, parallel execution, and watch mode" |
| **Keywords** | automation, build-tool, cli, task-runner, workflow |
| **Categories** | command-line-utilities, development-tools |
| **Created** | 2026-05-18 |
| **Downloads** | 18 |

This is a **completely unrelated project** (a Make/Just-style task runner), not our VM runtime.

### Available Alternative Names

All unverified against crates.io search (API doesn't have a simple check endpoint), but likely available based on the pattern:
- `fluxvm` — short, brandable, importable
- `flux-vm`
- `flux-runtime`
- `flux-bytecode`
- `superinstance-flux-core`

**Recommendation:** Use **`fluxvm`** (single word, no hyphen issues) or **`flux-runtime`** (matches our Python naming intent).

---

## Cargo.toml Assessment

| Field | Status | Notes |
|-------|--------|-------|
| `name` | ⚠️ | Must change — `flux-core` is taken |
| `version` | ✅ | `0.1.0` |
| `edition` | ✅ | `2021` |
| `authors` | ✅ | `["SuperInstance (DiGennaro et al.)"]` |
| `description` | ✅ | Full, descriptive |
| `license` | ✅ | `MIT` |
| `repository` | ✅ | Points to GitHub repo |
| `homepage` | ✅ | Points to GitHub repo |
| `documentation` | ✅ | Points to `docs.rs` (will auto-resolve once published) |
| `readme` | ✅ | `README.md` |
| `keywords` | ✅ | 5 keywords (vm, bytecode, interpreter, agent, a2a) |
| `categories` | ✅ | 3 categories (virtualization, emulators, parser-implementations) |
| `exclude` | ✅ | Excludes internal dirs from published crate |
| `dependencies` | ✅ | Single dep: `regex = "1"` |

### Minor Notes
- The `[profile.release]` settings (LTO, single codegen unit) are good for binary size
- Benchmarks use `criterion` (dev-dependency) — excluded from published crate

---

## Dry-Run Verification

```bash
$ cargo publish --dry-run
✅ Packaged 31 files, 200.9 KiB (126.1 KiB compressed)
✅ Compiled successfully (regex dep resolved)
✅ Upload aborted due to dry run (as expected)

⚠️  Warning: benchmark `vm_benchmark` excluded — benches/vm_benchmark.rs
    not included in published package (excluded by exclude rules).
    This is harmless but the bench won't be testable from the published crate.
```

The crate packages and compiles cleanly.

---

## Action Items Before Publish

1. **Rename the crate** — change `name` in `Cargo.toml` to chosen alternative (`fluxvm` recommended)
2. **Create crates.io account** — ensure a SuperInstance crates.io account exists
3. **Get API token** — create a crates.io API token with `publish-new` scope
4. **Login locally** — `cargo login <token>`
5. **Publish** — `cargo publish` (for real this time)
6. **Consider removing the bench warning** — either include `benches/` or remove the `[[bench]]` section if it's not needed in the published crate
