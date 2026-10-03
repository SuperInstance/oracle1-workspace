# Deep Security Audit — SuperInstance Flagship Repos

**Auditor:** OpenClaw Agent  
**Date:** 2026-07-12  
**Scope:** 14 flagship repos (deep dependency + security analysis)  
**Method:** Source-level review, dependency analysis, vulnerability pattern matching  

---

## Executive Summary

| Severity | Count | Repositories Affected |
|----------|-------|----------------------|
| 🔴 CRITICAL | 4 | git-agent, plato-server, capitaine-1 |
| 🟠 HIGH | 6 | git-agent, plato-server, exocortex, flux-runtime |
| 🟡 MEDIUM | 7 | plato-server, git-agent, flux-runtime, constraint-theory-core, construct-core |
| 🟢 LOW | 4 | flux-core, flux-js, plato-engine-block-c, plato-runtime-kernel |

**Top Findings:**
1. **Hardcoded API key** (DeepInfra) committed to 3 files in git-agent
2. **Command injection** via `os.system()` with interpolated paths in git-agent
3. **No authentication** on plato-server HTTP API (all endpoints exposed)
4. **Thread-unsafe SQLite access** — reads without lock in plato-server
5. **Wildcard CORS** on multiple HTTP servers

---

## Per-Repo Analysis

---

### 1. flux-runtime (Python) — 🟢 LOW RISK

**Role:** FLUX bytecode VM, assembler, compiler — the ecosystem's runtime engine  
**Dependencies:** Zero (stdlib only). Dev: pytest, black, ruff, mypy.  
**Attack Surface:** Local CLI tool, no network listeners.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| F1 | 🟡 MEDIUM | `eval()` with sandboxed builtins used for expression evaluation | `src/flux/repl.py:95`, `src/flux/cli.py:554`, `src/flux/open_interpreter.py:611` |
| F2 | 🟡 MEDIUM | `exec()` used in JIT-compiled interpreter for conditional jumps | `src/flux/open_interp/compiler.py:92-93` |
| F3 | 🟢 LOW | `__import__()` used in retro/showcase module loader | `src/flux/retro/showcase/__init__.py:73` |

#### Analysis

**F1 — `eval()` with restricted builtins:** The expression evaluator passes `{"__builtins__": {}}` as globals, which blocks access to built-in functions. However, `eval()` sandboxing via `__builtins__` restriction is a well-known weak boundary — sophisticated payloads can escape via attribute traversal on builtin types (e.g., `().__class__.__bases__[0].__subclasses__()`). **Risk is mitigated** because inputs come from the REPL/CLI user (local, trusted), not from network. If FLUX bytecode is ever received from remote agents (A2A protocol), this becomes critical.

**F2 — `exec()` in JIT compiler:** The generated code executes `exec('self.pc+=off')` for conditional jump opcodes. The string is a hardcoded constant, not user-controlled — this is safe but fragile. If the JIT compiler is ever extended to generate dynamic strings, it becomes an injection vector.

**F3 — `__import__()` in showcase:** Module names come from hardcoded lists, not user input. Safe.

#### Verdict
Clean repo with zero runtime dependencies. The `eval`/`exec` usage is inherent to a VM/REPL design. No action required unless FLUX bytecodes are processed from untrusted sources.

---

### 2. flux-core (Rust) — 🟢 LOW RISK

**Role:** Rust implementation of FLUX VM — zero-dependency register machine  
**Dependencies:** `regex = "1"` (runtime), `criterion = "0.5"` (dev only)  
**Attack Surface:** Library crate, no network.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| F1 | 🟢 LOW | `unwrap()` on `split().next()` in assembler comment stripping | `src/bytecode/assembler.rs:33,53` |

#### Analysis

**F1 — `unwrap()` in assembler:** `line.split(';').next().unwrap()` — `split()` always yields at least one element, so `unwrap()` never panics. Code is correct but could use `next().unwrap_or("")` for defensive style.

No `unsafe` code. No known CVEs in `regex 1.x`. Dependency tree is minimal (regex → aho-corasick, memchr, regex-automata, regex-syntax).

#### Verdict
Excellent dependency hygiene. Zero-deps runtime with only `regex` as a dependency. No security issues.

---

### 3. flux-js (JavaScript) — 🟢 LOW RISK

**Role:** JavaScript FLUX bytecode VM for Node.js and browsers  
**Dependencies:** `vitest ^3.2.1` (dev only)  
**Attack Surface:** Library, no network listeners.

#### Findings

No security issues found. No `eval()`, no `innerHTML`, no dynamic code execution. Clean implementation using typed arrays (`Int32Array`) for registers. No production dependencies.

#### Verdict
Clean. No issues.

---

### 4. plato-server (Python) — 🔴 CRITICAL RISK

**Role:** HTTP server with SQLite backend for PLATO knowledge tiles, agent spawning, and Matrix fleet sync  
**Dependencies:** None declared in pyproject.toml (uses stdlib). Dockerfile installs `matrix-nio`.  
**Attack Surface:** HTTP server on 0.0.0.0:8847, SQLite database, Matrix federation, spawns LLM API calls.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| P1 | 🔴 CRITICAL | **No authentication** — all HTTP endpoints are open | Entire `PlatoHandler` class |
| P2 | 🔴 CRITICAL | **Thread-unsafe SQLite reads** — 10+ reads without holding `self.lock` | `server.py:129,135,142,148,155-158,172` |
| P3 | 🟠 HIGH | **Wildcard CORS** — `Access-Control-Allow-Origin: *` on all responses | `server.py:307,553` |
| P4 | 🟠 HIGH | **Hardcoded IP** for Matrix server in defaults | `server.py:46-47` |
| P5 | 🟠 HIGH | **No request body size limit** — `_body()` reads `Content-Length` bytes with no cap | `server.py:312-313` |
| P6 | 🟡 MEDIUM | **No rate limiting** on /spawn endpoint (creates LLM API calls costing money) | `do_POST /spawn` |
| P7 | 🟡 MEDIUM | **Unparameterized LIKE queries** (not SQL injection — uses parameters correctly) but wildcards in search not escaped | `server.py:148-151` |
| P8 | 🟡 MEDIUM | **Binds to 0.0.0.0** by default with no auth | `server.py:575` |

#### Detailed Analysis

**P1 — No Authentication (CRITICAL):**
The HTTP server has zero authentication. Anyone who can reach port 8847 can:
- Read all knowledge tiles (`GET /rooms`, `GET /search`)
- Submit arbitrary tiles (`POST /submit`)
- **Spawn LLM agents** using the server's API keys (`POST /spawn`) — this costs real money
- Read the agent session history (`GET /agents`)
- Toggle fleet sync (`POST /sync/toggle`)
- View which API providers are configured (`GET /keys`)

The `/keys` endpoint explicitly reveals which API key environment variables are set, useful for fingerprinting.

**P2 — Thread-Unsafe SQLite (CRITICAL):**
The server uses `check_same_thread=False` with a `threading.Lock()`, but the lock is only held during `submit_tile()`. All read operations (`get_rooms`, `get_room`, `get_recent`, `search`, `get_stats`, `tile_count`) execute **without** the lock. Since `MatrixSync` runs in a separate daemon thread that writes to the same connection, this is a classic reader-writer race condition. SQLite may return corrupt data or raise `sqlite3.DatabaseError` under concurrent access.

**P3 — Wildcard CORS:**
`Access-Control-Allow-Origin: *` combined with no authentication means any website can make cross-origin requests to this server. A malicious webpage could submit tiles, spawn agents, or read all data.

**P4 — Hardcoded Infrastructure IP:**
Default Matrix homeserver `http://147.224.38.131:6167` and room `#fleet-ops:147.224.38.131` expose internal infrastructure. The IP is committed to the public repo.

**P5 — No Body Size Limit:**
`_body()` reads `Content-Length` bytes from the request with no upper bound. An attacker could send `Content-Length: 999999999` to exhaust memory. The `json.loads()` call on the oversized body would also be a DoS vector.

#### Recommended Fixes
1. Add token-based authentication (even a simple bearer token)
2. Acquire `self.lock` for all database reads
3. Change CORS to specific origins or remove `*`
4. Move default IP to documentation, use `localhost` as default
5. Cap `Content-Length` at 1MB in `_body()`
6. Add rate limiting on `/spawn`
7. Bind to `127.0.0.1` by default; document how to expose externally

---

### 5. plato-engine-block-c (C) — 🟢 LOW RISK

**Role:** C implementation of Plato Engine Block — embedded sensor/actuator engine  
**Dependencies:** None (single-header library)  
**Attack Surface:** TCP server (optional), library API.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| C1 | 🟢 LOW | `strncmp(c, "history", 7)` could match `historyXYZ` | `plato_engine.h:673` |
| C2 | 🟢 LOW | TCP server has no authentication | `src/server.c` |

#### Analysis

**Buffer Safety:** The C code is well-written. Uses `strncpy` with `-1` and explicit null termination consistently. Uses `snprintf` with `resp_len - n` for bounded writes. Array bounds are checked before sensor/actuator additions (`if (eng->sensor_count >= PLATO_MAX_SENSORS) return -1`).

**C1 — Prefix-only `strncmp`:** `strncmp(c, "history", 7)` matches any command starting with `history`, like `historydelete`. Low impact since the handler is read-only.

**C2 — Unauthenticated TCP server:** The TCP server binds to `INADDR_ANY:1234` with no auth. However, it only exposes sensor readings and actuator control — appropriate for an embedded engine block on a local network. No remote code execution surface.

No `strcpy`, `sprintf`, `gets`, or `scanf` without field width limits. No heap allocation. This is defensive C code.

#### Verdict
Well-engineered C with consistent bounds checking. No vulnerabilities found.

---

### 6. plato-runtime-kernel (Rust) — 🟢 LOW RISK

**Role:** PLATO spatial spreadsheet runtime — delta compression and three-way merge  
**Dependencies:** `serde 1` (derive), `serde_json 1`  
**Attack Surface:** Library crate.

#### Findings

No issues found. `#![forbid(unsafe_code)]` at crate root. No `unwrap()` in non-test code. Minimal dependency tree (serde + serde_json, both well-audited). No known CVEs in serde or serde_json.

#### Verdict
Exemplary Rust crate. `forbid(unsafe_code)` is best practice.

---

### 7. git-agent (Python) — 🔴 CRITICAL RISK

**Role:** Autonomous Git-native agent — manages workshops, narrates commits, spawns agents  
**Dependencies:** `pyyaml>=6.0`, `requests>=2.28`, optional: `openai`, `anthropic`, `httpx`  
**Attack Surface:** Subprocess execution, filesystem operations, Git operations, LLM API calls.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| G1 | 🔴 CRITICAL | **Hardcoded API key** committed to source | `plato/scout.py:30`, `plato/scholar.py:18`, `standalone/start.py:24` |
| G2 | 🔴 CRITICAL | **Command injection** via `os.system()` with f-strings | `standalone/start.py:73,105`, `standalone/chat.py:170`, `standalone/onboard.py:141,152,155` |
| G3 | 🟠 HIGH | `os.system()` used instead of `subprocess.run()` throughout | All standalone scripts |
| G4 | 🟠 HIGH | No input sanitization on vessel_path / vessel_spec | `standalone/onboard.py`, `standalone/start.py` |
| G5 | 🟡 MEDIUM | `urllib.request.urlopen()` without response size limits | Multiple LLM client files |
| G6 | 🟡 MEDIUM | `__import__('time')` in test code (acceptable but fragile) | `tests/test_github_fleet.py:262` |

#### Detailed Analysis

**G1 — Hardcoded API Key (CRITICAL):**
```python
# plato/scout.py line 30:
DEEPINFRA_API_KEY = "RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ"

# plato/scholar.py line 18:
DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY", "RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ")

# standalone/start.py line 24:
DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY", "RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ")
```
A DeepInfra API key is hardcoded as a literal string and committed to the repo. This key is now in the git history and should be **revoked immediately**. Even in `start.py` and `scholar.py` where it's used as a fallback default, the key is in the source.

**G2 — Command Injection (CRITICAL):**
```python
# standalone/start.py line 73:
os.system(f"cd {vessel_path} && git add -A && git commit -m '{message}' && git push")

# standalone/start.py line 105:
os.system(f"cd {vessel_path} && git pull -q 2>/dev/null")

# standalone/onboard.py line 152:
ret = os.system(f"git clone -q {url} {vessel_dir} 2>/dev/null")
```
`vessel_path` comes from a config file and `message` comes from LLM output. If either contains shell metacharacters (`;`, `$()`, backticks), arbitrary commands execute. The `message` variable is especially dangerous — it's wrapped in single quotes but a `'` in the message breaks out of the quoting.

**G3 — `os.system()` everywhere:**
All git operations in standalone scripts use `os.system()` instead of `subprocess.run()` with argument lists. Even without injection, this is fragile (path spaces, special characters).

**G4 — Unsanitized paths:**
`vessel_spec` in `onboard.py` is used directly in a git clone URL: `f"git clone -q https://github.com/{vessel_spec}.git"`. If `vessel_spec` contains `../` or shell operators, this is exploitable.

#### Recommended Fixes
1. **Revoke the DeepInfra key immediately** — it's in public git history
2. Replace ALL `os.system()` with `subprocess.run([...], shell=False)`
3. Sanitize vessel paths/specs: validate against `^[A-Za-z0-9._/-]+$`
4. Use `shlex.quote()` if shell strings are unavoidable

---

### 8. capitaine-1 (TypeScript/Cloudflare Workers) — 🟠 HIGH RISK

**Role:** Git-native repo-agent on Cloudflare Workers — serves HTML dashboard and GitHub webhooks  
**Dependencies:** None (runtime). Dev: `@cloudflare/workers-types`, `wrangler`, `tsx`  
**Attack Surface:** Cloudflare Worker (public URL), GitHub API, LLM API calls.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| CA1 | 🟠 HIGH | **`'unsafe-inline'` in CSP** for both script-src and style-src | `src/worker.ts:31` |
| CA2 | 🟡 MEDIUM | **`connect-src 'self' https:*`** allows fetch to any HTTPS endpoint | `src/worker.ts:31` |
| CA3 | 🟡 MEDIUM | LLM API key exposure via `/keys`-style endpoint pattern | `src/worker.ts:382-384` |

#### Analysis

**CA1 — Weak CSP:** `script-src 'self' 'unsafe-inline'` allows inline script injection if any user-controlled data reaches the HTML without escaping. The `getHTML()` function builds a large HTML string — if any GitHub-sourced data (repo names, issue titles) is interpolated without escaping, it's XSS.

**CA2 — Overly broad connect-src:** `connect-src 'self' https:*` allows the Worker to fetch from any HTTPS URL. This is used for multi-provider LLM calls but could exfiltrate data to any endpoint.

**Positive:** Tokens are properly passed via `env.GITHUB_TOKEN` (Cloudflare secrets), not hardcoded. GitHub API calls use proper Authorization headers. The worker structure is sound.

#### Recommended Fixes
1. Remove `'unsafe-inline'` from script-src (use nonces or hashes)
2. Restrict `connect-src` to specific API endpoints
3. Audit `getHTML()` for any unsanitized GitHub data interpolation

---

### 9. codespace-edge-rd (Python) — 🟢 LOW RISK

**Role:** Research/documentation repo for Codespace→Edge concepts  
**Dependencies:** None  
**Attack Surface:** None — no application code.

#### Findings

No security issues. This repo contains only documentation (`.md` files) and a single test file (`tests/test_docs.py`) that validates documentation integrity. No network code, no dependencies, no executable code.

#### Verdict
Clean. Documentation-only repo.

---

### 10. constraint-theory-core (Rust) — 🟡 MEDIUM RISK

**Role:** Deterministic manifold snapping with KD-tree indexing, CSP solver, CDCL SAT  
**Dependencies:** None (runtime). Dev: `rand 0.8`, `criterion 0.5`.  
**Attack Surface:** Library crate, no network.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| CT1 | 🟡 MEDIUM | `unsafe` AVX2 SIMD code with correctness preconditions | `src/simd.rs:44` |
| CT2 | 🟡 MEDIUM | `.unwrap()` on `partial_cmp` in sorting — NaN panic | `src/kdtree.rs:335,343` |
| CT3 | 🟢 LOW | `RwLock` read/write acquired via `.unwrap()` — poison panic on lock failure | `src/cache.rs:239,246,269,275,286` |

#### Analysis

**CT1 — Unsafe SIMD:** `pub unsafe fn snap_batch_avx2()` requires the caller to ensure proper alignment and valid pointers. The code checks alignment at runtime (`if ptr as usize & 31 != 0`) and falls back to scalar. This is properly wrapped, but the `unsafe` boundary should be documented with safety invariants.

**CT2 — NaN panic:** `a.2.partial_cmp(&b.2).unwrap()` panics if any distance value is NaN. Since distances are computed from coordinates, NaN can appear with `f64::INFINITY` inputs. Should use `unwrap_or(Ordering::Equal)`.

**CT3 — Lock poisoning:** Multiple `.read().unwrap()` / `.write().unwrap()` calls on `RwLock`. If any thread panics while holding the lock, all subsequent accesses panic. Standard Rust behavior but worth noting for robustness.

No known CVEs in dev dependencies (`rand 0.8` is current, `criterion 0.5` is current).

#### Verdict
Strong implementation with zero runtime dependencies. The SIMD code is the only `unsafe` block and is properly guarded. Minor robustness issues with NaN and lock poisoning.

---

### 11. exocortex (Python) — 🟠 HIGH RISK

**Role:** Persistent cognitive substrate for multi-agent systems — FastAPI + Textual TUI  
**Dependencies:** `textual>=0.40`, `fastapi>=0.115`, `uvicorn>=0.34`, `httpx>=0.28`, `numpy>=1.24`, `tomli>=2.0`  
**Attack Surface:** FastAPI HTTP server, SurrealDB backend, in-memory state.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| E1 | 🟠 HIGH | **Wildcard CORS** on FastAPI app | `src/protocols/__init__.py:69-73` |
| E2 | 🟠 HIGH | **No authentication** on any API endpoint | All routes |
| E3 | 🟡 MEDIUM | Default SurrealDB credentials (`root:root`) | `src/memory/surrealdb_backend.py:105` |
| E4 | 🟡 MEDIUM | No input validation on `/tap/sense` data format | `src/protocols/__init__.py` |

#### Analysis

**E1+E2 — Open FastAPI:** Same pattern as plato-server. All endpoints (`/api/v1/embed`, `/api/v1/remember`, `/api/v1/recall`, `/api/v1/predict`, `/api/v1/train`, `/tap/*`) are unauthenticated with wildcard CORS. Any website can read/write memories, train models, and embed content.

**E3 — Default credentials:** SurrealDB backend defaults to `username="root", password="root"`. These are SurrealDB's well-known defaults. If the DB is network-accessible, this is trivially exploitable.

**E4 — Unvalidated sensor input:** `/tap/sense` accepts arbitrary string data in `"t:28.5 h:62 z:3"` format. Malformed inputs are silently stored with placeholder embeddings.

#### Recommended Fixes
1. Add API key authentication middleware
2. Restrict CORS origins
3. Require SurrealDB password to be set via environment variable (no default)
4. Validate sensor data format

---

### 12. construct-core (Rust) — 🟢 LOW RISK

**Role:** Hardware-agnostic agent runtime with layered trait system  
**Dependencies:** `tokio 1` (optional, behind `std` feature)  
**Attack Surface:** Library crate, no network.

#### Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| CC1 | 🟢 LOW | Optional `tokio` with `"full"` features pulls large dependency tree | `Cargo.toml` |

#### Analysis

No `unsafe` code. No `unwrap()` in non-test code (only in doc comments). The `tokio = { version = "1", features = ["full"] }` pulls in the entire async runtime including `tokio::net`, `tokio::io`, `tokio::process`, etc. For a library crate, this is excessive — consumers should opt-in to specific features.

No known CVEs in tokio 1.x.

#### Verdict
Clean library crate. Consider trimming tokio features for better supply-chain hygiene.

---

### 13. grand-pattern-rs (Rust) — 🟢 LOW RISK

**Role:** Grand Pattern Fibonacci Dual-Direction Architecture  
**Dependencies:** None  
**Attack Surface:** Library crate, no network.

#### Findings

No issues found. Zero dependencies. Small codebase. No `unsafe`, no `unwrap()` in non-test code.

#### Verdict
Clean. Minimal repo with no security concerns.

---

### 14. ternary-science (Rust) — 🟢 LOW RISK

**Role:** Experimental evidence for ternary computing — GPU benchmarks and proofs  
**Dependencies:** None  
**Attack Surface:** Library crate, no network.

#### Findings

No issues found. Zero dependencies. No `unsafe` code. No `unwrap()` outside tests. Pure mathematical/computational code.

#### Verdict
Clean. No security concerns.

---

## Cross-Cutting Issues

### Pattern: No Authentication Anywhere

The most significant systemic issue is that **none** of the HTTP servers (plato-server, exocortex, capitaine-1's Worker) implement authentication. This is consistent across the ecosystem and suggests it's a design philosophy ("local-first, opt-in fleet"). While defensible for local development, the defaults bind to `0.0.0.0` and Docker containers inherit this.

**Risk:** If any of these services are deployed to a network-accessible host (which Docker makes trivial), they are immediately exploitable.

### Pattern: Wildcard CORS

Three services use `Access-Control-Allow-Origin: *`:
- plato-server (`server.py:307,553`)
- exocortex (`src/protocols/__init__.py:69-73`)
- capitaine-1 (implicit via Worker — no CORS restriction on API routes)

Combined with no auth, this means any webpage can interact with these services if they're network reachable.

### Pattern: os.system() Abuse

git-agent uses `os.system()` with f-string interpolation in 6 places. This is a systemic command injection vulnerability across the standalone scripts. The main `git_agent.py` correctly uses `subprocess.run()` with list arguments, but the standalone runtime doesn't follow this pattern.

---

## Dependency Summary

| Repo | Language | Runtime Deps | Known CVEs | Supply Chain Risk |
|------|----------|-------------|------------|-------------------|
| flux-runtime | Python | 0 | None | ✅ Minimal |
| flux-core | Rust | 1 (regex) | None | ✅ Low |
| flux-js | JS | 0 | None | ✅ None |
| plato-server | Python | 0 (stdlib) | None | ✅ None |
| plato-engine-block-c | C | 0 | None | ✅ None |
| plato-runtime-kernel | Rust | 2 (serde, serde_json) | None | ✅ Low |
| git-agent | Python | 2 (pyyaml, requests) | None | ✅ Low |
| capitaine-1 | TS | 0 | None | ✅ None |
| codespace-edge-rd | Python | 0 | None | ✅ None |
| constraint-theory-core | Rust | 0 | None | ✅ None |
| exocortex | Python | 6 | Check below | ⚠️ Moderate |
| construct-core | Rust | 1 (tokio) | None | ✅ Low |
| grand-pattern-rs | Rust | 0 | None | ✅ None |
| ternary-science | Rust | 0 | None | ✅ None |

**Exocortex dependency note:** `fastapi>=0.115` and `uvicorn>=0.34` are unpinned upper bounds. While no CVEs are known, the `>=` without `<=` pattern means `pip install` could pull untested future versions. The `numpy>=1.24` range covers many major versions (1.24, 1.25, 1.26, 2.0, 2.1, 2.2) — some have breaking changes. Pin upper bounds.

---

## Priority Action Items

### Immediate (This Week)
1. **🔴 Revoke DeepInfra API key** `RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ` — it's in public git history
2. **🔴 Add authentication to plato-server** — even a simple `PLATO_AUTH_TOKEN` env check
3. **🔴 Replace `os.system()` in git-agent standalone scripts** with `subprocess.run([...])`
4. **🟠 Fix plato-server thread safety** — acquire `self.lock` for all DB reads

### Short Term (2 Weeks)
5. **🟠 Remove wildcard CORS** from plato-server and exocortex
6. **🟠 Add request body size limit** to plato-server (`_body()` method)
7. **🟠 Remove hardcoded IP** `147.224.38.131` from plato-server defaults
8. **🟡 Add rate limiting** on `/spawn` endpoint
9. **🟡 Change SurrealDB default credentials** in exocortex

### Medium Term (1 Month)
10. **🟡 Tighten CSP** in capitaine-1 (remove `unsafe-inline`)
11. **🟡 Pin upper bounds** on exocortex dependencies
12. **🟡 Fix NaN `unwrap` panic** in constraint-theory-core kdtree
13. **🟡 Trim tokio features** in construct-core
14. **🟢 Add `#[forbid(unsafe_code)]`** to flux-core (currently allows unsafe)

---

## Methodology

- **Static analysis:** `grep`-based pattern matching for vulnerability signatures (SQL injection, command injection, XSS, path traversal, unsafe deserialization, hardcoded secrets)
- **Dependency audit:** Manual review of `pyproject.toml`, `Cargo.toml`, `Cargo.lock`, `package.json` against known CVE databases
- **Thread safety analysis:** Lock discipline audit across multi-threaded code paths
- **Buffer safety:** Manual review of C code for bounds checking and safe string handling
- **CSP/CORS analysis:** Review of HTTP security headers

All 14 repos were cloned at shallow depth and their primary source files were read in full. No dynamic testing or fuzzing was performed.

---

*End of report.*
