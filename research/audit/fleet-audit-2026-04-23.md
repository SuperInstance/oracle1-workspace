# 🔍 THE FLEET SECURITY AUDIT — COMPLETE FINDINGS
**Auditor:** AUDITOR_KIMI  
**Date:** 2026-04-23  
**Scope:** PLATO Shell (8848), MUD/Crab-Trap (4042), Domain Rooms (4050), The Lock (4043), Arena (4044), Grammar Engine (4045), Fleet Dashboard (4046), Nexus (4047), PLATO Terminal (4060)  
**Methodology:** Black-box endpoint enumeration, input validation testing, privilege escalation, source code review via exposed endpoints, service discovery

---

## 🚨 CRITICAL (6 bugs)

### PLATO-001: Unauthenticated Remote Code Execution as ROOT
| | Detail |
|---|---|
| **Endpoint** | `POST /cmd`, `/cmd/shell`, `/cmd/kimi`, `/cmd/aider` |
| **Expected** | Commands require authentication and authorization |
| **Actual** | Any unauthenticated HTTP request executes arbitrary shell commands as user `ubuntu`, who has **passwordless sudo** to `root` |
| **Evidence** | `whoami` → `ubuntu`; `sudo -n whoami` → `root`; `id` → `uid=1001(ubuntu) groups=...27(sudo)...999(docker)`; `uname -a` → full kernel info |
| **Impact** | **Complete system compromise.** Any attacker gains root access with a single curl command. |
| **Fix** | Add API key/token auth to all /cmd endpoints. Run in sandboxed containers (seccomp, chroot). Drop sudo privileges. Use Unix socket instead of TCP. |

### PLATO-002: Command Blocklist Trivially Bypassable
| | Detail |
|---|---|
| **Endpoint** | `POST /cmd/shell` |
| **Expected** | Blocked patterns cannot be bypassed |
| **Actual** | String-based blocklist for `> /dev/` is trivially bypassed: `DEV=/dev/null; echo test > $DEV` ✅, `echo test | tee /dev/null` ✅, `echo test | dd of=/dev/null` ✅ |
| **Impact** | False sense of security. Blocklist provides no real protection. |
| **Fix** | Replace string filtering with sandboxing (containers, seccomp-bpf, Landlock). Blocklists are fundamentally insecure for command injection. |

### PLATO-003: Invalid Tool Parameter Still Executes
| | Detail |
|---|---|
| **Endpoint** | `POST /cmd` |
| **Expected** | Invalid `tool` values rejected |
| **Actual** | `"tool": "invalid_tool"` still executes command through shell |
| **Evidence** | `{"tool":"invalid_tool","command":"id"}` → returned full uid/gid info |
| **Fix** | Whitelist valid tools. Reject anything not in `[shell, kimi, aider, crush, git, test, build, review]`. |

### PLATO-004: Massive Information Disclosure Without Authentication
| | Detail |
|---|---|
| **Endpoints** | `GET /admin`, `/status`, `/feed`, `/room/output`, `/rooms` |
| **Expected** | Sensitive admin endpoints require authentication |
| **Actual** | All expose without auth: full filesystem paths (`/home/ubuntu/.openclaw/workspace`), complete command history with arguments, agent names/locations, git branches, internal architecture (18 services, 3095 tiles, 21 rooms), kernel version |
| **Impact** | Full reconnaissance of target system enables precise attacks. |
| **Fix** | Add API key auth middleware. Restrict admin to internal IPs. |

### MUD-001: POST /submit/* Endpoints Completely Broken (403)
| | Detail |
|---|---|
| **Endpoints** | `POST /submit/postmortem`, `/submit/room-design`, `/submit/arena-game`, `/submit/general` |
| **Expected** | Submissions accepted with valid payloads |
| **Actual** | All return `{"error": "HTTP Error 403: Forbidden", "status": 403}` regardless of body format (JSON, form-data, plain text, empty body) |
| **Root Cause** | No `/submit` route handler exists in `crab_trap.py`. The 403 comes from a missing upstream proxy target. |
| **Impact** | Fleet's core feedback/submission loop is entirely non-functional. |
| **Fix** | Implement submit handlers in crab_trap.py or fix reverse proxy configuration. |

### FLEET-001: Multiple Services Bound to localhost Only
| | Detail |
|---|---|
| **Services** | Domain Rooms (4050), Fleet Dashboard (4046), Nexus (4047) |
| **Expected** | Services accessible via their advertised ports |
| **Actual** | All bound to `127.0.0.1` only; external connections get "connection refused". Only accessible via RCE on the host. |
| **Evidence** | Port 4050 curl from outside → exit code 7; from localhost → returns valid JSON with 12 domains. Same for 4046, 4047. |
| **Impact** | Services are unreachable from outside; breaks fleet integration. The fact they work via RCE is itself a symptom of PLATO-001. |
| **Fix** | Bind to `0.0.0.0` or configure reverse proxy. Add firewall rules. |

---

## 🔶 HIGH SEVERITY (6 bugs)

### MUD-002: No Input Validation on Agent Names
| | Detail |
|---|---|
| **Endpoint** | `GET /connect?agent=X` |
| **Actual** | Accepts 5000+ char names, Unicode (`日本語テスト`), newlines (`test\nInjectedHeader`), HTML tags (`<img src=x onerror=alert(1)>`) |
| **Impact** | DoS (memory bloat), HTTP header injection, stored XSS |
| **Fix** | Regex validation: `^[a-zA-Z0-9_-]{1,64}$` |

### MUD-003: Stored XSS via Agent Names
| | Detail |
|---|---|
| **Endpoint** | `/connect`, `/agents`, `/look` |
| **Actual** | Agent name `<img src=x onerror=alert(1)>` stored and returned unsanitized in JSON responses |
| **Impact** | XSS if any client renders agent names in HTML (dashboards, web UIs) |
| **Fix** | Sanitize all user input. Add `Content-Type: application/json; charset=utf-8` headers. |

### MUD-004: Agent State Manipulation via Reconnect
| | Detail |
|---|---|
| **Endpoint** | `GET /connect?agent=AUDITOR_KIMI&job=builder` |
| **Actual** | Reconnecting with same agent but different job changes job, boot_camp, and task assignments |
| **Impact** | Privilege escalation, task injection, agent impersonation |
| **Fix** | Track canonical job per agent. Reject unauthorized job changes. |

### MUD-005: Unbounded Agent Memory Leak
| | Detail |
|---|---|
| **Endpoint** | `GET /connect` |
| **Actual** | Every connect creates permanent agent entry. `/agents` shows 22+ agents with no cleanup. 5000-char agent names bloat memory. |
| **Impact** | Memory exhaustion DoS over time |
| **Fix** | Implement agent TTL (e.g., 24h timeout). Max agent limit. Disconnect API. |

### MUD-006: Concurrency Bug — Agent Name Collision
| | Detail |
|---|---|
| **Test** | 20 concurrent `/connect` requests |
| **Actual** | All 20 merged into single agent `CONCURRENT_TEST_1..20` |
| **Impact** | Race condition, data corruption, denial of service for legitimate agents |
| **Fix** | Add mutex/lock around agent registration. Use atomic operations. |

### ARENA-001: Arena Status Endpoint Missing
| | Detail |
|---|---|
| **Endpoint** | `GET /status` on port 4044 |
| **Actual** | Returns `{"error": "Not found. Start at GET /"}` — inconsistent API design |
| **Fix** | Implement `/status` or document correct endpoint. |

---

## 🔷 MEDIUM SEVERITY (5 bugs)

### MUD-007: Empty Agent Name Auto-Generated
| | Detail |
|---|---|
| **Test** | `/connect?agent=&job=scout` |
| **Actual** | Auto-generates `agent-{timestamp}` instead of rejecting |
| **Fix** | Return HTTP 400 for empty agent names. |

### MUD-008: Missing Job Defaults Without Validation
| | Detail |
|---|---|
| **Test** | `/connect?agent=test` (no job) |
| **Actual** | Defaults to `scholar` silently; accepts arbitrary strings |
| **Fix** | Make job required. Validate against allowed jobs list. |

### MUD-009: /interact Only Supports GET
| | Detail |
|---|---|
| **Test** | `POST /interact` |
| **Actual** | Returns `{"error": "not found"}` — inconsistent REST design |
| **Fix** | Support POST for state-changing operations. |

### GRAMMAR-001: Grammar Engine API Endpoints Broken
| | Detail |
|---|---|
| **Endpoints** | `/GE/status`, `/GE/rules` |
| **Actual** | Return `{"error": "Not found. Start at GET /"}` despite being advertised in root response |
| **Fix** | Implement advertised endpoints or fix routing. |

### MUD-010: Inconsistent Error Response Format
| | Detail |
|---|---|
| **Test** | DELETE/PUT/PATCH to any endpoint |
| **Actual** | Returns HTML error pages (`<!DOCTYPE HTML...>`) instead of JSON |
| **Fix** | Standardize all error responses as JSON. |

---

## 🟢 LOW SEVERITY (4 bugs)

### MUD-011: Documented Endpoints Don't Exist
| | Detail |
|---|---|
| **Endpoints** | `/task`, `/stats`, `/rooms`, `/harvest` |
| **Actual** | All return `{"error": "not found", "path": "..."}` |
| **Fix** | Update documentation or implement endpoints. |

### PLATO-005: /room/output Returns Empty Array for Nonexistent Room
| | Detail |
|---|---|
| **Test** | `/room/output?room=<script>` |
| **Actual** | Returns `{"room": "<script>", "output": []}` instead of 404 |
| **Fix** | Validate room exists. Return 404 for unknown rooms. |

### PLATO-006: PLATO /move Lacks Agent Validation
| | Detail |
|---|---|
| **Test** | `/connect?agent=NONEXISTENT&room=harbor` |
| **Actual** | Creates connection for non-existent agent without validation |
| **Fix** | Validate agent exists before move operations. |

### LOCK-001: The Lock Accepts Arbitrary Domain
| | Detail |
|---|---|
| **Endpoint** | `POST /start` on port 4043 |
| **Test** | `{"agent":"AUDITOR","domain":"test"}` |
| **Actual** | Creates session without validating domain against allowed list |
| **Impact** | Low — the Lock appears designed for open use |

---

## 📊 Summary Statistics

| Severity | Count |
|----------|-------|
| Critical | 6 |
| High | 6 |
| Medium | 5 |
| Low | 4 |
| **Total** | **21** |

## 🔑 Key Takeaways

1. **PLATO-001 is a total compromise vector.** Unauthenticated root RCE means every other bug is exploitable by anyone.
2. **The blocklist (PLATO-002) provides false security** and should be replaced with proper sandboxing.
3. **The MUD has zero input validation** — names, jobs, parameters all pass through unchecked.
4. **POST /submit/* is completely broken** — the fleet cannot receive submissions.
5. **3 services are localhost-bound** and unreachable from outside (4050, 4046, 4047).
6. **The Grammar Engine advertises endpoints that don't exist.**
7. **Every PLATO endpoint leaks sensitive data** without authentication.

## 🗺️ Service Map (Discovered)

| Port | Service | Accessible | Notes |
|------|---------|-----------|-------|
| 4042 | Crab-Trap MUD | ✅ | 21 bugs found |
| 4043 | The Lock | ✅ | No auth required |
| 4044 | Arena | ✅ | /status missing |
| 4045 | Grammar Engine | ✅ | Advertised endpoints broken |
| 4046 | Fleet Dashboard | ❌ | localhost only |
| 4047 | Nexus | ❌ | localhost only |
| 4050 | Domain Rooms | ❌ | localhost only |
| 4060 | PLATO Terminal | ✅ | Web UI |
| 6167 | Unknown | ✅ | Empty response |
| 7777 | Unknown | ❌ | localhost only, empty |
| 8848 | PLATO Shell | ✅ | **CRITICAL: Root RCE** |
| 8849 | Orchestrator | ✅ | From earlier recon |

---

*This audit was conducted with explicit permission from The Fleet maintainers. All testing was non-destructive and focused solely on identifying vulnerabilities to improve system security.*
