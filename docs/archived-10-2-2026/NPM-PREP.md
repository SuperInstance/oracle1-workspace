# npm Prep — flux-js (JavaScript)

**Date:** 2026-07-12
**Repo:** [SuperInstance/flux-js](https://github.com/SuperInstance/flux-js)

---

## ✅ Package Names Available on npm

| Name | Status |
|------|--------|
| `flux-js` | ✅ **Available** (404 = not registered) |
| `@superinstance/flux` | ✅ **Available** (404 = not registered) |

No blockers for npm publishing. Both names are free.

---

## package.json Assessment

```json
{
  "name": "flux-js",
  "version": "1.0.0",
  "description": "FLUX.js — JavaScript Bytecode VM",
  "main": "flux.js",
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "devDependencies": {
    "vitest": "^3.2.1"
  }
}
```

| Field | Status | Notes |
|-------|--------|-------|
| `name` | ✅ | `flux-js` — available on npm |
| `version` | ⚠️ | `1.0.0` — aggressive for a first publish. Consider `0.1.0` to signal pre-stable |
| `description` | ✅ | Clear and descriptive |
| `main` | ✅ | `flux.js` — entry point exists |
| `scripts` | ✅ | Test scripts present |
| `license` | ❌ | **Missing** — must add `"license": "MIT"` |
| `author` | ❌ | **Missing** — should add `"author": "SuperInstance"` |
| `repository` | ❌ | **Missing** — should add repo URL |
| `keywords` | ❌ | **Missing** — important for discoverability |
| `type` | ❌ | Consider `"type": "module"` if using ESM (check flux.js for export syntax) |
| `files` | ❌ | **Missing** — should specify `"files": ["flux.js"]` to control what's published |
| `engines` | ❌ | Consider specifying Node.js version requirement |

---

## Missing Fields — Recommended Additions

```json
{
  "name": "flux-js",
  "version": "0.1.0",
  "description": "FLUX.js — JavaScript Bytecode VM",
  "main": "flux.js",
  "type": "module",
  "license": "MIT",
  "author": "SuperInstance",
  "homepage": "https://github.com/SuperInstance/flux-js#readme",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/SuperInstance/flux-js.git"
  },
  "bugs": {
    "url": "https://github.com/SuperInstance/flux-js/issues"
  },
  "keywords": ["vm", "bytecode", "interpreter", "flux", "runtime", "agent"],
  "files": ["flux.js", "LICENSE", "README.md"],
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "devDependencies": {
    "vitest": "^3.2.1"
  }
}
```

---

## Action Items Before Publish

1. **Add missing metadata** — license, author, repository, keywords, files, engines
2. **Bump version down** — `1.0.0` → `0.1.0` (signals early stage; major version 1 implies API stability)
3. **Add `"type": "module"`** if flux.js uses ESM exports (recommended for modern JS)
4. **Create npm account** — set up `superinstance` org on npmjs.com
5. **Login** — `npm login`
6. **Publish** — `npm publish` (or `npm publish --access public` for scoped packages)
7. **Consider scoped package** — `@superinstance/flux` is also available and gives namespace protection
