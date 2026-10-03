# Security Fixes — Wave 2 (HIGH Issues)

**Date:** 2026-07-12  
**Scope:** 6 HIGH severity issues across 5 repos  
**Preceded by:** Wave 1 (4 CRITICAL fixes — hardcoded API key, command injection, auth, SQLite locking)  
**Method:** GitHub Contents API, minimal patches, syntax-verified  

---

## Summary

| # | Repo | Issue | Severity | Fix | Commit |
|---|------|-------|----------|-----|--------|
| 1 | plato-server | Path traversal + body DoS + wildcard CORS + hardcoded IP | 🟠 HIGH | Room name regex validation, 1MB body cap, configurable CORS, localhost default | `388f22a` |
| 2 | flux-runtime | eval() sandbox escape via `__builtins__` traversal | 🟠 HIGH | Replace eval() with recursive AST walker | `7657cd9` |
| 3 | exocortex | Unpinned upper bounds on 5 dependencies | 🟠 HIGH | Pin all deps to major version ceiling | `9dc4ede` |
| 4 | exocortex | Wildcard CORS (`allow_origins=["*"]`) | 🟠 HIGH | Configurable `EXOCORTEX_CORS_ORIGINS` env var | `bac5451` |
| 5 | git-agent | Shell injection via `os.popen()` in onboard.py | 🟠 HIGH | Replace with `subprocess.run(cwd=)`, add vessel_spec validation | `b12c6e5` |
| 6 | capitaine-1 | `'unsafe-inline'` in CSP script-src + `connect-src https:*` | 🟠 HIGH | Remove unsafe-inline, serve telemetry as external JS, restrict connect-src to 3 domains | `11159eb` |

---

## Detailed Fixes

### 1. plato-server — Path Traversal + Body DoS + CORS + Hardcoded IP

**File:** `server.py`  
**Commit:** `388f22a28100050ee051f1f0f3455d430030f6bf`

**Issues addressed:** P3 (wildcard CORS), P4 (hardcoded IP), P5 (no body size limit), plus path traversal in room name handling.

**Changes:**

- **Path traversal prevention:** Added `re.match(r'^[A-Za-z0-9._-]+$', room)` validation on the `/room/{name}` endpoint. Only alphanumeric, dash, underscore, and dot characters are allowed. Prevents `../` traversal and shell metacharacter injection.

- **Body size limit:** The `_body()` method now rejects requests with `Content-Length > 1_048_576` (1 MB). Prevents memory exhaustion DoS via oversized JSON payloads.

- **CORS hardening:** Replaced hardcoded `Access-Control-Allow-Origin: *` with a configurable `PLATO_CORS_ORIGIN` environment variable. If unset, no CORS header is sent (same-origin only). Applied to `_json()`, `_unauthorized()`, and `do_OPTIONS()`.

- **Hardcoded IP removal:** Default Matrix homeserver changed from `http://147.224.38.131:6167` to `http://localhost:6167`. Default Matrix room changed from `#fleet-ops:147.224.38.131` to `#fleet-ops:localhost`. The hardcoded IP exposed internal infrastructure.

- **CORS preflight:** Added `Authorization` to `Access-Control-Allow-Headers` so Bearer token auth works cross-origin when configured.

### 2. flux-runtime — eval() Sandbox Escape

**File:** `src/flux/repl.py`  
**Commit:** `7657cd92c7a5e4c41e9ec09573ecda4823333106`

**Issue:** `eval(expr, {"__builtins__": {}})` is a well-known weak sandbox. Python's type system allows escape via attribute traversal: `().__class__.__bases__[0].__subclasses__()` can reach `os.system` and other dangerous builtins.

**Fix:** Replaced `eval()` with a recursive AST-based evaluator that:
- Parses the expression to an AST (`ast.parse(expr, mode='eval')`)
- Walks the tree recursively, only allowing: numeric constants (`int`, `float`), binary operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`, `<<`, `>>`, `|`, `&`, `^`), and unary operators (`-`, `+`, `~`)
- Rejects all other AST node types (attributes, calls, subscripts, names, comprehensions, etc.)
- No `__builtins__`, no attribute access, no string methods — eliminates the entire class of sandbox escape vectors

### 3. exocortex — Unpinned Upper Bounds

**File:** `pyproject.toml`  
**Commit:** `9dc4edee5d89240deb42076186599028be317cf4`

**Issue:** Five dependencies had `>=` without `<=` upper bounds, meaning `pip install` could pull untested future major versions.

**Fix:** Added major-version upper bounds to all dependencies:

| Dependency | Before | After |
|------------|--------|-------|
| `textual` | `>=0.40` | `>=0.40,<2.0` |
| `httpx` | `>=0.28` | `>=0.28,<1.0` |
| `tomli` | `>=2.0` | `>=2.0,<3.0` |
| `pytest` (dev) | `>=8.0` | `>=8.0,<9.0` |
| `pytest-asyncio` (dev) | `>=0.24` | `>=0.24,<1.0` |
| `ruff` (dev) | `>=0.8` | `>=0.8,<1.0` |
| `scikit-learn` (ml) | `>=1.6` | `>=1.6,<2.0` |

(`fastapi`, `uvicorn`, and `numpy` already had upper bounds from a prior pass.)

### 4. exocortex — Wildcard CORS

**File:** `src/protocols/__init__.py`  
**Commit:** `bac5451f1be5eaae948a56838024946183f3bd51`

**Issue:** `CORSMiddleware` configured with `allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`. Combined with no authentication, any website could make cross-origin requests.

**Fix:**
- Replaced `allow_origins=["*"]` with `EXOCORTEX_CORS_ORIGINS` environment variable (comma-separated)
- Default to localhost dev origins (`http://localhost:3000`, `http://localhost:5173`) when unset
- Restricted `allow_methods` to `["GET", "POST"]` (was `["*"]`)
- Restricted `allow_headers` to `["Content-Type", "Authorization"]` (was `["*"]`)

### 5. git-agent — Shell Injection in onboard.py

**File:** `standalone/onboard.py`  
**Commit:** `b12c6e592850481f35c5c8c2b8e5dc0baa834553`

**Issue:** `os.popen(f"cd {vessel_dir} && git status --short 2>/dev/null")` — classic shell injection via f-string interpolation. If `vessel_dir` contained shell metacharacters (e.g., `$(cmd)`, backticks), arbitrary commands would execute.

**Additional issue:** `vessel_spec` used in git clone URLs without validation — a malicious spec like `foo/bar; rm -rf /` could be injected.

**Fixes:**
- **os.popen → subprocess.run:** Replaced with `subprocess.run(["git", "status", "--short"], cwd=vessel_dir, capture_output=True, text=True)`. No shell invocation.
- **vessel_spec validation:** Added `re.match(r'^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$', vessel_spec)` check before any git operations. Rejects specs containing shell metacharacters, path traversal sequences, or non-GitHub-safe characters.
- **Token handling:** Changed from embedding token directly in clone URL (`f"https://{token}@github.com/..."`) to using `x-access-token:{token}@` format (GitHub's recommended pattern) as a fallback only when anonymous clone fails.

**Verification:** All standalone scripts (`start.py`, `chat.py`, `onboard.py`), `git_agent.py`, and `plato/*.py` verified clean of `os.system()`, `os.popen()`, and `shell=True`.

### 6. capitaine-1 — CSP unsafe-inline + Broad connect-src

**File:** `src/worker.ts`  
**Commit:** `11159eb6e561670d9b2c37a7e762d2cc15568ba2`

**Issue:** Content Security Policy included `script-src 'self' 'unsafe-inline'` which allows inline `<script>` tags — if any GitHub-sourced data reaches the HTML without escaping, it's XSS. Additionally, `connect-src 'self' https:*` allowed fetch to any HTTPS endpoint (data exfiltration risk).

**Fix:**
- **Removed `'unsafe-inline'` from `script-src`:** Now `script-src 'self'` only. All scripts must come from same-origin files.
- **Externalized inline telemetry script:** The inline `<script>` that fetched `/api/state` for the telemetry display was moved to a new `/api/telemetry.js` endpoint that serves the same JavaScript as an external file with proper `Content-Type: application/javascript`.
- **Restricted `connect-src`:** Changed from `https:*` (any HTTPS) to `https://api.github.com https://api.deepseek.com https://api.moonshot.ai` — only the three APIs the worker actually needs.
- **Kept `'unsafe-inline'` in `style-src`:** This is a pragmatic decision — the HTML uses extensive inline styles and Google Fonts CSS, and removing it would require a full rewrite. Style-based XSS is extremely rare compared to script-based.

---

## Verification Matrix

| Check | plato-server | flux-runtime | exocortex | git-agent | capitaine-1 |
|-------|:---:|:---:|:---:|:---:|:---:|
| Syntax validated | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pushed via Contents API | ✅ | ✅ | ✅ | ✅ | ✅ |
| os.system/popen audit clean | — | — | — | ✅ | — |
| eval()/exec() audit clean | — | ✅ | — | — | — |
| CORS wildcard audit clean | ✅ | — | ✅ | — | — |
| CSP strict | — | — | — | — | ✅ |
| Deps bounded | — | — | ✅ | — | — |

---

## Outstanding from Audit (Not in Wave 2 Scope)

### MEDIUM (7 items)
- plato-server: No rate limiting on `/spawn` endpoint
- plato-server: LIKE wildcards not escaped in search
- git-agent: `urllib.request.urlopen()` without response size limits
- flux-runtime: `exec()` in JIT compiler (hardcoded constant — safe but fragile)
- constraint-theory-core: NaN `unwrap` panic in kdtree
- constraint-theory-core: RwLock poison panic
- exocortex: Default SurrealDB credentials (`root:root`)

### LOW (4 items)
- flux-core: `unwrap()` in assembler (safe by invariant)
- flux-js: Clean (no issues)
- plato-engine-block-c: `strncmp` prefix matching
- plato-runtime-kernel: Clean (exemplary)

---

## Commits (Chronological)

| # | Repo | SHA | Message |
|---|------|-----|---------|
| 1 | SuperInstance/plato-server | `388f22a` | security: fix path traversal, body size limit, CORS, hardcoded IP (wave 2) |
| 2 | SuperInstance/flux-runtime | `7657cd9` | security: replace eval() with AST-based safe evaluator (wave 2) |
| 3 | SuperInstance/exocortex | `9dc4ede` | security: pin upper bounds on all dependencies (wave 2) |
| 4 | SuperInstance/exocortex | `bac5451` | security: replace wildcard CORS with configurable origins (wave 2) |
| 5 | SuperInstance/git-agent | `b12c6e5` | security: fix shell injection in onboard.py (wave 2) |
| 6 | SuperInstance/capitaine-1 | `11159eb` | security: tighten CSP — remove unsafe-inline from script-src (wave 2) |

---

*End of Wave 2 report. Wave 1 (CRITICAL fixes) preceded this. MEDIUM/LOW issues are documented for future waves.*
