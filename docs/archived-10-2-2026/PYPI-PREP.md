# PyPI Prep — flux-runtime (Python)

**Date:** 2026-07-12
**Repo:** [SuperInstance/flux-runtime](https://github.com/SuperInstance/flux-runtime)

---

## ⛔ BLOCKER: Package name "flux-runtime" is TAKEN on PyPI

The name `flux-runtime` is **already registered** on PyPI by a different project:

| Field | Value |
|-------|-------|
| **Owner** | `arto` (Arto Bendiken, arto@bendiken.net) |
| **Project** | [pypi.org/project/flux-runtime](https://pypi.org/project/flux-runtime/) |
| **Version** | 0.0.0 (placeholder, uploaded 2026-02-09) |
| **Summary** | "Flux Theory for Python" |
| **Source** | `flux-doctrine/flux-theory` (different org entirely) |
| **License** | Unlicense (Public Domain) |

This is **not our package**. The `flux-doctrine` project is unrelated to SuperInstance.

### Available Alternative Names (all confirmed free)

| Name | Status |
|------|--------|
| `flux-bytecode` | ✅ Available |
| `flux-vm-runtime` | ✅ Available |
| `flux-vm` | ✅ Available |
| `superinstance-flux` | ✅ Available |
| `superinstance-flux-runtime` | ✅ Available |

**Recommendation:** Use **`flux-vm`** or **`flux-bytecode`** — short, descriptive, brandable. The import name stays `flux` regardless of the distribution name.

---

## pyproject.toml Assessment

| Field | Status | Notes |
|-------|--------|-------|
| `name` | ⚠️ | Must change — `flux-runtime` is taken |
| `version` | ✅ | `0.1.0` |
| `description` | ✅ | Full, descriptive |
| `authors` | ⚠️ | `{ name = "SuperInstance" }` — no email, consider adding one |
| `license` | ✅ | `MIT` |
| `requires-python` | ✅ | `>=3.10` |
| `keywords` | ✅ | 9 relevant keywords |
| `classifiers` | ✅ | Comprehensive (dev status, audience, Python versions, topics) |
| `urls` | ✅ | Homepage, docs, repo, bug tracker all present |
| `scripts` | ✅ | `flux = "flux.cli:main"` CLI entry point |
| `dependencies` | ✅ | Empty (zero runtime deps) |
| `optional-deps` | ✅ | dev tools specified |

### Missing/Optional
- **No `license-file`** — PEP 639 recommends `license-files = ["LICENSE"]`
- Consider adding `[project.urls] "Changelog"` entry

---

## Build Verification

```bash
$ python -m build
✅ sdist built:  flux_runtime-0.1.0.tar.gz (1.4 MB)
✅ wheel built:  flux_runtime-0.1.0-py3-none-any.whl (597 KB)
```

Build completed successfully with no errors. Both sdist and wheel are valid.

---

## Action Items Before Publish

1. **Rename the distribution** — change `name` in `pyproject.toml` to chosen alternative (`flux-vm` recommended)
2. **Add email to authors** — e.g. `{ name = "SuperInstance", email = "founders@superinstance.dev" }`
3. **Add license-files** — `license-files = ["LICENSE"]` per PEP 639
4. **Create PyPI account** — ensure a SuperInstance PyPI account exists and is set up with 2FA
5. **Reserve the name** — once decided, upload a 0.0.1 placeholder or go straight to 0.1.0
6. **Configure trusted publishing** — consider GitHub Actions → PyPI trusted publisher (OIDC) instead of API tokens
