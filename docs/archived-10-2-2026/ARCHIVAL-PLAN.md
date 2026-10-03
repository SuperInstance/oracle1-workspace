# SuperInstance Repository Archival Plan

**Created:** 2026-07-12  
**Based on:** CONSOLIDATION-MAP.md (same directory)  
**Status:** PLANNING ONLY — No archival has been performed. Requires Casey's approval per batch.  
**Total repos in org:** ~4,099 non-archived  
**Repos identified for archival:** ~3,600+  
**Target end state:** ~250 repos  

---

## How to Read This Plan

Each section covers one cluster or sub-cluster group. Within each:

- **Archive candidates** are repos recommended for archival
- **Merge first** means content should be copied/merged into the canonical repo BEFORE archiving
- **Archive directly** means no merge needed — the repo is empty, a duplicate, or superseded
- **Risk levels:**
  - 🟢 **Low** — Empty repo, pure duplicate, or explicit early-version/sketch. No unique content.
  - 🟡 **Medium** — Has some content that should be verified before archiving. Merge recommended.
  - 🔴 **High** — Has real commits, stars, or external references. Requires careful review.

---

## Batch 1: Easy Wins — Polyglot Consolidations

These are the clearest archival cases: the same concept implemented in many languages as separate repos. Each language variant should be merged as a subdirectory into the canonical repo, then archived.

### 1A. grand-pattern (41 repos → 1)

**Canonical keeper:** `grand-pattern-core`  
**Merge target:** Create `grand-pattern` monorepo (or use `grand-pattern-core`) with per-language dirs

| Repo | Action | Merge First? | Risk |
|------|--------|-------------|------|
| grand-pattern-core | ✅ KEEP (canonical) | — | — |
| grand-pattern-rs | Archive | Merge `rs/` dir into core | 🟡 |
| grand-pattern-c | Archive | Merge `c/` dir | 🟡 |
| grand-pattern-chapel | Archive | Merge `chapel/` dir | 🟡 |
| grand-pattern-cuda | Archive | Merge `cuda/` dir | 🟡 |
| grand-pattern-fortran | Archive | Merge `fortran/` dir | 🟡 |
| grand-pattern-go | Archive | Merge `go/` dir | 🟡 |
| grand-pattern-java | Archive | Merge `java/` dir | 🟡 |
| grand-pattern-mojo | Archive | Merge `mojo/` dir | 🟡 |
| grand-pattern-opencl | Archive | Merge `opencl/` dir | 🟡 |
| grand-pattern-ptx | Archive | Merge `ptx/` dir | 🟡 |
| grand-pattern-py | Archive | Merge `python/` dir | 🟡 |
| grand-pattern-swift | Archive | Merge `swift/` dir | 🟡 |
| grand-pattern-ts | Archive | Merge `ts/` dir | 🟡 |
| grand-pattern-wasm | Archive | Merge `wasm/` dir | 🟡 |
| grand-pattern-zig | Archive | Merge `zig/` dir | 🟡 |
| grand-pattern-mono | Archive | Merge if has unique content | 🟡 |
| grand-pattern-mono-go | Archive | Merge if unique | 🟡 |
| grand-pattern-mono-py | Archive | Merge if unique | 🟡 |
| grand-pattern-mono-ts | Archive | Merge if unique | 🟡 |
| grand-pattern-abi | Archive | Merge if unique | 🟡 |
| grand-pattern-adversarial | Archive | Merge if unique | 🟡 |
| grand-pattern-bench | Archive | Merge if unique | 🟡 |
| grand-pattern-bench-v2 | Archive | Superseded by v2 — check if v1 has history | 🟢 |
| grand-pattern-cli | Archive | Merge if unique | 🟡 |
| grand-pattern-claude | Archive | Merge if unique | 🟡 |
| grand-pattern-design | Archive | Merge docs into core | 🟡 |
| grand-pattern-embedded | Archive | Merge if unique | 🟡 |
| grand-pattern-experiments | Archive | Merge if unique | 🟢 |
| grand-pattern-ffi | Archive | Merge if unique | 🟡 |
| grand-pattern-flux | Archive | Merge if unique | 🟡 |
| grand-pattern-gpu | Archive | Merge if unique | 🟡 |
| grand-pattern-integration | Archive | Merge if unique | 🟡 |
| grand-pattern-kimi | Archive | Merge if unique | 🟢 |
| grand-pattern-kit | Archive | Merge if unique | 🟡 |
| grand-pattern-net | Archive | Merge if unique | 🟡 |
| grand-pattern-sim | Archive | Merge if unique | 🟡 |
| grand-pattern-simd | Archive | Merge if unique | 🟡 |
| grand-pattern-store | Archive | Merge if unique | 🟡 |
| grand-pattern-topology | Archive | Merge if unique | 🟡 |
| grand-pattern-venue | Archive | Merge if unique | 🟡 |

**Batch stats:** 40 archive candidates, 1 keeper  
**Estimated effort:** Medium — verify each has only boilerplate, merge meaningful content

---

### 1B. conservation-spectral (24 repos → 1)

**Canonical keeper:** `conservation-spectral-core`  
**Merge target:** Consolidate all into `conservation-spectral` monorepo with per-language dirs

| Repo | Action | Merge First? | Risk |
|------|--------|-------------|------|
| conservation-spectral-core | ✅ KEEP (canonical) | — | — |
| conservation-spectral-ada | Archive | Merge `ada/` dir | 🟡 |
| conservation-spectral-apl | Archive | Merge `apl/` dir | 🟡 |
| conservation-spectral-asm | Archive | Merge `asm/` dir | 🟡 |
| conservation-spectral-c | Archive | Merge `c/` dir | 🟡 |
| conservation-spectral-chapel | Archive | Merge `chapel/` dir | 🟡 |
| conservation-spectral-cuda | Archive | Merge `cuda/` dir | 🟡 |
| conservation-spectral-forth | Archive | Merge `forth/` dir | 🟡 |
| conservation-spectral-fortran | Archive | Merge `fortran/` dir | 🟡 |
| conservation-spectral-fortraniv | Archive | Merge `fortraniv/` dir (check if duplicate of fortran) | 🟢 |
| conservation-spectral-js | Archive | Merge `js/` dir | 🟡 |
| conservation-spectral-lisp | Archive | Merge `lisp/` dir | 🟡 |
| conservation-spectral-mojo | Archive | Merge `mojo/` dir | 🟡 |
| conservation-spectral-opencl | Archive | Merge `opencl/` dir | 🟡 |
| conservation-spectral-pascal | Archive | Merge `pascal/` dir | 🟡 |
| conservation-spectral-ptx | Archive | Merge `ptx/` dir | 🟡 |
| conservation-spectral-python | Archive | Merge `python/` dir | 🟡 |
| conservation-spectral-topology | Archive | Merge topology logic | 🟡 |
| conservation-spectral-topology-c | Archive | Merge if unique | 🟡 |
| conservation-spectral-topology-rs | Archive | Merge if unique | 🟡 |
| conservation-spectral-v2 | Archive | Check if superseded; likely archive directly | 🟢 |
| conservation-spectral-vulkan | Archive | Merge `vulkan/` dir | 🟡 |
| conservation-spectral-webgpu | Archive | Merge `webgpu/` dir | 🟡 |
| conservation-spectral-zig | Archive | Merge `zig/` dir | 🟡 |

**Batch stats:** 23 archive candidates, 1 keeper

---

### 1C. openconstruct (23 repos → 1)

**Canonical keeper:** `OpenConstruct` (top-level)  
**Note:** `openconstruct-rust` has the most commits (9) and largest size — verify it's not the de facto canonical

| Repo | Action | Merge First? | Risk |
|------|--------|-------------|------|
| OpenConstruct | ✅ KEEP (canonical) | — | — |
| openconstruct-rust | Archive | Merge `rust/` dir — HIGH PRIORITY (9 commits, large) | 🔴 |
| openconstruct-c | Archive | Merge `c/` dir | 🟡 |
| openconstruct-cs | Archive | Merge `cs/` dir | 🟡 |
| openconstruct-go | Archive | Merge `go/` dir | 🟡 |
| openconstruct-java | Archive | Merge `java/` dir | 🟡 |
| openconstruct-python | Archive | Merge `python/` dir | 🟡 |
| openconstruct-ruby | Archive | Merge `ruby/` dir | 🟡 |
| openconstruct-swift | Archive | Merge `swift/` dir | 🟡 |
| openconstruct-ts | Archive | Merge `ts/` dir | 🟡 |
| openconstruct-zig | Archive | Merge `zig/` dir | 🟡 |
| openconstruct-abi | Archive | Merge if unique | 🟡 |
| openconstruct-catalog | Archive | Merge if unique | 🟡 |
| openconstruct-docs | Archive | Merge docs into keeper | 🟡 |
| openconstruct-esp32 | Archive | Merge if unique | 🟡 |
| openconstruct-examples | Archive | Merge examples into keeper | 🟢 |
| openconstruct-hub | Archive | Merge if unique | 🟡 |
| openconstruct-jetson | Archive | Merge if unique | 🟡 |
| openconstruct-jupyter | Archive | Merge if unique | 🟡 |
| openconstruct-kernel | Archive | Merge if unique | 🟡 |
| openconstruct-landing | Archive | Merge landing page assets | 🟢 |
| openconstruct-mercury | Archive | Merge if unique | 🟡 |
| openconstruct-modular | Archive | Merge if unique | 🟡 |

**Batch stats:** 22 archive candidates, 1 keeper

---

### 1D. holodeck (10 repos → 1)

**Canonical keeper:** `holodeck-rust` (3⭐, 44 commits — most developed)  
**Alternative:** Keep `holodeck-core` as the monorepo root

| Repo | Action | Merge First? | Risk |
|------|--------|-------------|------|
| holodeck-rust | ✅ KEEP (canonical, 3⭐, 44 commits) | — | — |
| holodeck-core | Archive | Merge core into keeper (or keep as monorepo root) | 🔴 |
| holodeck-c | Archive | Merge `c/` dir | 🟡 |
| holodeck-c-1 | Archive | Numbered duplicate of holodeck-c | 🟢 |
| holodeck-cuda | Archive | Merge `cuda/` dir | 🟡 |
| holodeck-cuda-1 | Archive | Numbered duplicate of holodeck-cuda | 🟢 |
| holodeck-go | Archive | Merge `go/` dir | 🟡 |
| holodeck-zig | Archive | Merge `zig/` dir | 🟡 |
| holodeck-session-manager | Archive | Merge if unique | 🟡 |
| holodeck-studio | Archive | Merge if unique | 🟡 |

**Batch stats:** 9 archive candidates, 1 keeper

---

### 1E. si-runtime (6 repos → 1)

**Canonical keeper:** Create `superinstance-runtime` monorepo  
**Current state:** 5 language variants + potentially a base

| Repo | Action | Merge First? | Risk |
|------|--------|-------------|------|
| si-runtime-go | Archive | Merge `go/` dir | 🟡 |
| si-runtime-js | Archive | Merge `js/` dir | 🟡 |
| si-runtime-python | Archive | Merge `python/` dir | 🟡 |
| si-runtime-wasm | Archive | Merge `wasm/` dir | 🟡 |
| si-runtime-zig | Archive | Merge `zig/` dir | 🟡 |

**Batch stats:** 5 archive candidates, merge into new monorepo

---

## Batch 2: Versioned Duplicates & Early-Version Repos

These are explicitly versioned or labeled as early/preliminary. Older versions should be archived after confirming content is captured in the newer version.

### 2A. agent-riff Version Chain (4 repos → 1)

**Canonical keeper:** `agent-riff-v4` (latest) — or rename to `agent-riff`  
**Note:** `agent-riff-v4` was last pushed 2026-06-11 — older than v1's push date. Verify which has latest content.

| Repo | Action | Merge First? | Risk |
|------|--------|-------------|------|
| agent-riff | Archive | Verify v4 supersedes; merge any unique history | 🟡 |
| agent-riff-v2 | Archive | Merge if has unique content | 🟢 |
| agent-riff-v3 | Archive | Merge if has unique content | 🟢 |
| agent-riff-v4 | ✅ KEEP (latest version) | — | — |

**Batch stats:** 3 archive candidates, 1 keeper

---

### 2B. V2/Suffixed Duplicates (38 repos)

All `-v2` (or `-v3`) repos where a non-versioned original exists. These should be checked to determine which version is canonical, then the loser archived.

| Repo | Cluster | Action | Risk |
|------|---------|--------|------|
| chess-dojo-v2 | standalone | Archive older of chess-dojo / chess-dojo-v2 | 🟡 |
| collective-mind-v2 | standalone | Archive after merge | 🟡 |
| conservation-law-v2 | conservation | Archive after merging into conservation-law | 🟡 |
| conservation-spectral-v2 | conservation | Archive (already covered in 1B) | 🟢 |
| context-compactor-v2 | standalone | Archive after merge | 🟡 |
| cuda-metrics-v2 | cuda | Archive after merge | 🟡 |
| emergence-bus-v2 | standalone | Archive after merge | 🟡 |
| fibonacci-growth-v2 | standalone | Archive after merge | 🟡 |
| fleet-orchestrator-v2 | fleet | Archive (merge v2 content into orchestrator) | 🟡 |
| flux-isa-v3 | flux | Archive after merging into flux-isa | 🟡 |
| flux-vm-v3 | flux | Archive after merging into flux-vm | 🟡 |
| grand-pattern-bench-v2 | grand-pattern | Archive (covered in 1A) | 🟢 |
| gravity-well-v2 | standalone | Archive after merge | 🟡 |
| griot-math-v2 | standalone | Archive after merge | 🟡 |
| guardc-v3 | standalone | Archive after merge | 🟡 |
| kimi-swarm-results-2 | standalone | Numbered duplicate, archive after merge | 🟢 |
| lau-construct-integration-v2 | lau | Archive after merge | 🟡 |
| lau-murmur-protocol-v2 | lau | Archive after merge | 🟡 |
| lau-penrose-v2 | lau | Archive after merge | 🟡 |
| lau-port-v2 | lau | Archive after merge | 🟡 |
| murmur-protocol-v2 | standalone | Archive after merge | 🟡 |
| musician-soul-v2 | standalone | Archive after merge | 🟡 |
| plato-e2e-pipeline-v2 | plato | Archive after merge | 🟡 |
| seed-mcp-v2 | standalone | Archive after merge | 🟡 |
| snapkit-v2 | standalone | Archive after merge | 🟡 |
| spectral-deadband-v2 | spectral | Archive after merge | 🟡 |
| spectral-graph-v2 | spectral | Archive after merge | 🟡 |
| spectral-music-v2 | spectral | Archive after merge | 🟡 |
| swarm-intuition-v2 | swarm | Archive after merge | 🟡 |
| ternary-compiler-v2 | ternary | Archive after merge | 🟡 |
| ternary-compression-v2 | ternary | Archive after merge | 🟡 |
| ternary-cuda-kernels-v2 | ternary | Archive after merge | 🟡 |
| ternary-registry-v2 | ternary | Archive after merge | 🟡 |
| ternary-scheduling-v2 | ternary | Archive after merge | 🟡 |
| tick-engine-v2 | standalone | Archive after merge | 🟡 |
| websocket-fabric-v2 | standalone | Archive after merge | 🟡 |

**Batch stats:** 38 archive candidates (most after quick merge verification)

---

### 2C. Numbered Duplicates (19 repos)

Repos with `-1` or `-2` suffix that appear to be accidental or automated duplicates.

| Repo | Original | Action | Risk |
|------|----------|--------|------|
| api-gateway-1 | api-gateway | Archive duplicate | 🟢 |
| arena-combat-analyst-1 | arena-combat-analyst | Archive duplicate | 🟢 |
| businesslog-1 | businesslog | Archive duplicate | 🟢 |
| capitaine-1 | capitaine | Archive duplicate | 🟢 |
| constraint-theory-web-1 | constraint-theory-web | Archive duplicate | 🟢 |
| cudaclaw-1 | cudaclaw | Archive duplicate | 🟢 |
| deckboss-1 | deckboss | Archive duplicate | 🟢 |
| dmlog-ai-1 | dmlog-ai | Archive duplicate | 🟢 |
| ghost-tiles-1 | ghost-tiles | Archive duplicate | 🟢 |
| grammar-curator-1 | grammar-curator | Archive duplicate | 🟢 |
| higher-abstraction-vocabularies-1 | higher-abstraction-vocabularies | Archive duplicate | 🟢 |
| holodeck-c-1 | holodeck-c | Archive duplicate (also covered in 1D) | 🟢 |
| holodeck-cuda-1 | holodeck-cuda | Archive duplicate (also covered in 1D) | 🟢 |
| kimi-swarm-results-2 | kimi-swarm-results | Archive duplicate | 🟢 |
| lucineer-1 | lucineer | Archive duplicate | 🟢 |
| mud-expert-1 | mud-expert | Archive duplicate | 🟢 |
| personallog-1 | personallog | Archive duplicate | 🟢 |
| shell-artisan-1 | shell-artisan | Archive duplicate | 🟢 |
| studylog-ai-1 | studylog-ai | Archive duplicate | 🟢 |

**Batch stats:** 19 archive candidates — all LOW risk, pure duplicates

---

### 2D. Early-Version Repos (22 repos)

Repos explicitly labeled `-early-version`. These are preliminary/sketch versions by their own naming.

| Repo | Cluster | Merge First? | Risk |
|------|---------|-------------|------|
| adaptive-plato-early-version | plato | Check for unique content, likely archive | 🟢 |
| attention-daemon-early-version | standalone | Check for unique content | 🟢 |
| field-evolution-early-version | standalone | Check for unique content | 🟢 |
| fleet-agent-early-version | fleet | Check for unique content | 🟢 |
| fleet-automation-early-version | fleet | Check for unique content | 🟢 |
| flux-consciousness-engine-early-version | flux | Check for unique content | 🟢 |
| flux-constraint-py-early-version | flux | Check for unique content | 🟢 |
| flux-engine-early-version | flux | Check for unique content | 🟢 |
| gatekeeper-as-flux-early-version | flux | Check for unique content | 🟢 |
| greenhorn-runtime-early-version | standalone | Check for unique content | 🟢 |
| keel-early-version | standalone | Check for unique content | 🟢 |
| lighthouse-cli-early-version | standalone | Check for unique content | 🟢 |
| LLMs-from-scratch-early-version | standalone | Check for unique content | 🟢 |
| memory-crystal-early-version | standalone | Check for unique content | 🟢 |
| penrose-memory-palace-early-version | standalone | Check for unique content | 🟢 |
| plato-alignments-early-version | plato | Check for unique content | 🟢 |
| plato-calibration-early-version | plato | Check for unique content | 🟢 |
| plato-hologram-early-version | plato | Check for unique content | 🟢 |
| plato-stable-early-version | plato | Check for unique content | 🟢 |
| the-plenum-early-version | standalone | Check for unique content | 🟢 |
| tile-memory-early-version | plato | Check for unique content | 🟢 |
| zeroclaw-agent-early-version | zeroclaw | Check for unique content | 🟢 |

**Batch stats:** 22 archive candidates — all LOW risk by their own labeling

---

## Batch 3: Beta/Test Repos

### 3A. Beta-Test User Repos (4 repos)

Personal test/beta repos for specific users — no production value.

| Repo | Action | Risk |
|------|--------|------|
| beta-test-alex | Archive directly | 🟢 |
| beta-test-elena | Archive directly | 🟢 |
| beta-test-marcus | Archive directly | 🟢 |
| beta-test-priya | Archive directly | 🟢 |

---

## Batch 4: Large Cluster Consolidations

These batches handle the major prefix clusters. Each is large enough to warrant its own review session.

### 4A. fleet-midi (91 repos → 1)

**Canonical keeper:** `fleet-midi` (or create `fleet-midi-monorepo`)  
**Current state:** 91 repos covering individual MIDI concepts (arpeggiators, chord generators, quantizers, tokenizers, etc.)

**Action:** Merge all 91 repos as subdirectories into a single `fleet-midi` monorepo, then archive all 91.

| Sub-group | Count | Risk |
|-----------|-------|------|
| fleet-midi-arpeggiator, -chord, -clock, -control, -generator | ~15 | 🟡 |
| fleet-midi-quantizer, -tokenizer, -transport, -router | ~10 | 🟡 |
| fleet-midi-* (remaining individual concept repos) | ~66 | 🟡 |

**Full list:** All 91 `fleet-midi-*` repos (see `/tmp/all-repos.txt`, filter `fleet-midi-`)  
**Batch stats:** 91 archive candidates (after merge), 1 keeper  
**Special note:** This is the single largest sub-cluster. Recommend doing this one first as a proof-of-concept for the monorepo consolidation pattern.

---

### 4B. plato-tile (36 repos → 1)

**Canonical keeper:** Create `plato-tile` monorepo  
**Action:** Merge all 36 repos as subdirectories

**Full list:** All 36 `plato-tile-*` repos  
**Batch stats:** 36 archive candidates (after merge), 1 new monorepo

---

### 4C. plato-room (20 repos → 1)

**Canonical keeper:** Create `plato-room` monorepo  
**Action:** Merge all 20 repos as subdirectories

**Full list:** All 20 `plato-room-*` repos  
**Batch stats:** 20 archive candidates (after merge), 1 new monorepo

---

### 4D. flux-runtime & flux-vm & flux-isa (26 repos → 3)

**Canonical keepers:** `flux-runtime` (100+ commits!), `flux-vm`, `flux-isa`  
**Action:** Merge all variants into their canonical root

| Sub-cluster | Repos | Merge Into | Risk |
|-------------|-------|------------|------|
| flux-runtime-* (9 repos) | 8 variants | `flux-runtime` | 🔴 (flux-runtime has 100+ commits) |
| flux-vm-* (8 repos) | 7 variants | `flux-vm` | 🟡 |
| flux-isa-* (9 repos) | 8 variants | `flux-isa` | 🟡 |

**Batch stats:** ~24 archive candidates, 3 keepers

---

### 4E. ternary- (370 repos → 15)

**Canonical keepers:** `ternary-core`, `ternary-cli`, `ternary-agent`, `ternary-compiler-*` (merge into 1), and ~11 others by subsystem

**Action:** This is the LARGEST cluster and needs its own sub-plan. Recommend:
1. First pass: Archive the ~330 single-concept repos (many are likely single-file sketches)
2. Group remaining ~40 into 15 thematic repos (arithmetic, gates, compiler, ML, crypto, etc.)

**Special note:** Given the scale, recommend a dedicated session for this cluster alone. Sample repos first to understand content patterns.

**Batch stats:** ~355 archive candidates, ~15 keepers  
**Risk:** Mixed — need per-repo verification

---

### 4F. lau- (333 repos → 25)

**Canonical keepers:** `lau-self-modeling`, `lau-construct-integration`, `lau-room-native`, and ~22 others

**Action:** 
1. Create `lau-math` monorepo for ~85 pure math repos
2. Create `lau-agents` monorepo for ~60 agent variant repos
3. Merge `lau-sia2-engine-*` (4 repos) into one
4. Merge `lau-shell-*` (5 repos) into one
5. Archive remaining ~250

**Batch stats:** ~308 archive candidates, ~25 keepers  
**Risk:** Mixed — academic content needs careful review

---

### 4G. fleet- (non-midi) (227 repos → 15)

**Canonical keepers:** `fleet-router`, `fleet-daemon`, `fleet-warden-rs`, `fleet-yaw`, `fleet-manifold`, `fleet-daily`, `fleet-health-monitor`, and ~8 others

**Action:** After fleet-midi consolidation (4A above), consolidate:
1. `fleet-math-*` (8 repos) → `fleet-math`
2. `fleet-agent-*` (4 repos) → merge into `fleet-agent`
3. `fleet-a2a-*` (4 repos) → merge into one
4. `fleet-dashboard-*` (3 repos) → merge into one
5. `fleet-constraint-*` (3 repos) → merge into one
6. Archive remaining ~190 scattered repos

**Batch stats:** ~212 archive candidates, ~15 keepers

---

### 4H. plato- (non-tile, non-room) (219 repos → 15)

**Canonical keepers:** `plato-core`, `plato-kernel`, `plato-server`, `plato-cli`, and ~11 others

**Action:**
1. `plato-forge-*` (8 repos) → merge into `plato-forge`
2. `plato-engine-*` (6 repos) → merge into `plato-engine`
3. `plato-vessel-*` (4 repos) → merge into `plato-vessel`
4. `plato-client-*` (4 repos: js, php, ruby) → merge into `plato-client` with language branches
5. Archive remaining ~190

**Batch stats:** ~204 archive candidates, ~15 keepers

---

### 4I. cuda- (143 repos → 15)

**Note:** Most `cuda-` repos are NOT about CUDA — they're mis prefixed agent concepts.  
**Canonical keeper:** `cudaclaw` (the original)

**Action:**
1. Identify genuine GPU repos → consolidate into `cuda-kernels`
2. Rename mis prefixed repos (cuda-ethics, cuda-emotion, etc.) — or just archive the sketches
3. Merge related groups (cuda-fleet-health + cuda-fleet-mesh + cuda-fleet-topology)
4. Archive ~120

**Batch stats:** ~128 archive candidates, ~15 keepers

---

### 4J. agent- (79 repos → 10)

**Canonical keepers:** `agent-to-agent`, `agent-coordinator`, `agent-orchestration`

**Action:** Consolidate 79 repos into ~10 thematic repos (rhythm, harmony, identity, coordination, etc.)

**Batch stats:** ~69 archive candidates, ~10 keepers

---

### 4K. cocapn- (76 repos → 12)

**Canonical keepers:** `cocapn` (73 commits!), `cocapn-cli` (21), `cocapn-runtime` (10)

**Action:**
1. Merge language SDKs (cocapn-c, -go, -lua, -py, -python, -wasm, -zig, -forth) into `cocapn-sdk`
2. Merge cocapn-health + cocapn-health-rs
3. Merge cocapn-explain + cocapn-explain-rs
4. Merge cocapn-fleet-* into fleet cluster
5. Archive ~55

**Batch stats:** ~64 archive candidates, ~12 keepers

---

## Batch 5: Small Cluster Consolidations

These smaller clusters are straightforward merges with lower risk.

### 5A. oxide- (30 repos → 5)

**Canonical keeper:** `oxide-fleet` (10 commits), create `oxide-core`  
**Merge:** All infrastructure primitives (circuit-breaker, checkpoint, compactor, crdt, federation, journal, pipeline, raft-log) into modules  
**Archive:** ~25 repos | **Risk:** 🟡

### 5B. nexus- (18 repos → 4)

**Canonical keeper:** `nexus-runtime`  
**Merge:** comms, data-pipeline, edge-runtime, persistence, security, simulation into modules  
**Archive:** ~14 repos | **Risk:** 🟡

### 5C. zeroclaw-/zc- (21 repos → 3)

**Canonical keeper:** `zeroclaw-crew` (10 commits, 2⭐)  
**Merge:** 11 `zc-*-shell` repos into `zc-shells`, merge `zeroclaw-*` into `zeroclaw`  
**Archive:** ~18 repos | **Risk:** 🟡

### 5D. forge- (20 repos → 4)

**Canonical keeper:** `forgemaster` (2⭐)  
**Merge:** audio, code, data, image, memory, pipeline, sensor, text, transform into modules  
**Archive:** ~16 repos | **Risk:** 🟡

### 5E. git- (18 repos → 4)

**Canonical keeper:** `git-agent` (2⭐)  
**Merge:** codespace, flux-pipeline, rebase, standard, system, cuda, native variants into `git-agent`  
**Archive:** ~14 repos | **Risk:** 🟡

### 5F. Equipment- (14 repos → 5)

**Canonical keeper:** `Equipment-Consensus-Engine` (28 commits)  
**Merge:** Language variants (Consensus-Engine + PHP + Ruby → one)  
**Archive:** ~9 repos | **Risk:** 🟡

### 5G. exocortex- (11 repos → 2)

**Action:** Merge all into `exocortex` monorepo (C++, Mojo, Lua, Python, Zig, TS)  
**Archive:** ~9 repos | **Risk:** 🟡

### 5H. DeckBoss (14 repos → 1)

**Canonical keeper:** `DeckBoss` (2⭐, 32 commits)  
**Merge:** All deckboss-/DeckBoss-* variants  
**Archive:** ~13 repos | **Risk:** 🟡

### 5I. a2a- (7 repos → 2)

**Canonical keeper:** `a2a-protocol`  
**Merge:** adapter, constraint-protocol, future, signal-chain  
**Archive:** 5 repos | **Risk:** 🟡

### 5J. activelog- (7 repos → 1)

**Canonical keeper:** `activelog-backend`  
**Merge:** All into `activelog`  
**Archive:** 6 repos | **Risk:** 🟡

### 5K. activeledger- (3 repos → 1)

**Action:** Merge all 3 into one  
**Archive:** 2 repos | **Risk:** 🟢

### 5L. categorical- (4 repos → 1)

**Action:** Merge agents, agents-c, agents-rs into `categorical-agents`  
**Archive:** 3 repos | **Risk:** 🟢

---

## Batch 6: Standalone Sub-Clusters

Small themed groups not covered by the prefix clusters.

| Sub-cluster | Repos | Action | Archive Count | Risk |
|-------------|-------|--------|---------------|------|
| craftmind- | 8 | Merge into `craftmind` | 7 | 🟡 |
| mud- | 6 | Merge into `mud` | 5 | 🟡 |
| studylog-/Studylog-/StudyLog- | 8 | Merge into `StudyLog` (fix casing) | 7 | 🟢 |
| tropical- | 9 | Merge into `tropical` | 8 | 🟡 |
| symplectic- | 7 | Merge into `symplectic` | 6 | 🟡 |
| vessel- | 10 | Merge into `vessel` | 9 | 🟡 |
| graph- | 12 | Merge into `graph-rs` | 11 | 🟡 |
| spreadsheet- | 9 | Merge into `spreadsheet` | 8 | 🟡 |
| crdt-/SmartCRDT | 7 | Merge into `SmartCRDT` | 6 | 🟡 |
| swarm- | 6 | Merge into `swarm` | 5 | 🟡 |
| character- | 8 | Merge into `character` | 7 | 🟡 |
| entropy- | 7 | Merge into `entropy` | 6 | 🟡 |
| edge- | 11 | Merge into `edge` | 10 | 🟡 |
| spectral- (non-conservation) | 24 | Merge into parent clusters + `spectral-graph` | 19 | 🟡 |
| constraint-theory-* | ~15 | Merge into `constraint-theory-core` (75 commits!) | ~12 | 🔴 |

**Batch stats:** ~116 archive candidates across all standalone sub-clusters

---

## Batch 7: SuperInstance / si- Namespace Unification (77 repos → 12)

**Canonical keeper:** `SuperInstance` (5⭐ — highest in org!, 100+ commits)

**Action:**
1. Unify `si-*` repos into `superinstance-*` namespace
2. Merge si-conservation-* into conservation cluster
3. Merge si-*-agent (7 repos) into `superinstance-agent`
4. si-runtime-* handled in Batch 1E
5. Archive remaining ~55

**Note:** This is a namespace migration, not just archival. Requires careful planning for any CI/CD references.

**Batch stats:** ~65 archive candidates, ~12 keepers | **Risk:** 🔴

---

## Summary Statistics

| Batch | Description | Archive Candidates | Risk Level |
|-------|-------------|-------------------|------------|
| 1A-E | Polyglot consolidations | ~100 | 🟡 Medium |
| 2A-D | Versioned/early/numbered duplicates | ~82 | 🟢 Low |
| 3A | Beta-test repos | 4 | 🟢 Low |
| 4A-K | Large cluster consolidations | ~1,500 | Mixed |
| 5A-L | Small cluster consolidations | ~100 | 🟡 Medium |
| 6 | Standalone sub-clusters | ~116 | 🟡 Medium |
| 7 | si-/superinstance- unification | ~65 | 🔴 High |
| **Other** | Standalone repos (no cluster) | ~1,800 | Unknown |
| **TOTAL** | | **~3,700+** | |

---

## Recommended Execution Order

1. **Start with Batch 3** (beta-test repos) — 4 repos, zero risk, build confidence
2. **Batch 2C** (numbered duplicates) — 19 repos, all 🟢 low risk
3. **Batch 2D** (early-version repos) — 22 repos, all 🟢 low risk
4. **Batch 2A** (agent-riff chain) — 3 repos, simple version merge
5. **Batch 1A** (grand-pattern) — clearest polyglot case, establishes the pattern
6. **Batch 1B-D** (other polyglot) — follow established pattern
7. **Batch 4A** (fleet-midi) — largest single sub-cluster, 91 repos
8. **Batch 4B-C** (plato-tile, plato-room) — large subsystem merges
9. **Batch 5** (small clusters) — quick wins
10. **Batch 6** (standalone sub-clusters) — more quick wins
11. **Batch 4D-K** (remaining large clusters) — heavy lifting
12. **Batch 7** (si- unification) — highest risk, do last
13. **Batch 2B** (v2 duplicates) — interleave with parent cluster batches

---

## Pre-Archival Checklist (Per Repo)

Before archiving ANY repo, verify:

- [ ] Repo has been merged into canonical keeper (if it has unique content)
- [ ] No open issues or PRs that reference this repo
- [ ] No GitHub Actions or CI dependencies
- [ ] Not referenced in any documentation or READMEs of keeper repos
- [ ] Has been tagged with `superseded-by: <canonical-repo>` in description
- [ ] Has an archival README explaining where content moved

## Archival Command Reference

```bash
# Archive a single repo
gh repo archive SuperInstance/<repo-name> --yes

# Bulk archive (use with caution — requires explicit approval per batch)
# for repo in $(cat batch-X-list.txt); do
#   gh repo archive "SuperInstance/$repo" --yes
# done
```

---

## Approval

| Batch | Repos | Casey Approval | Date Archived |
|-------|-------|---------------|---------------|
| 1A (grand-pattern) | 40 | ⏳ Pending | — |
| 1B (conservation-spectral) | 23 | ⏳ Pending | — |
| 1C (openconstruct) | 22 | ⏳ Pending | — |
| 1D (holodeck) | 9 | ⏳ Pending | — |
| 1E (si-runtime) | 5 | ⏳ Pending | — |
| 2A (agent-riff) | 3 | ⏳ Pending | — |
| 2B (v2 duplicates) | 38 | ⏳ Pending | — |
| 2C (numbered dupes) | 19 | ⏳ Pending | — |
| 2D (early-version) | 22 | ⏳ Pending | — |
| 3A (beta-test) | 4 | ⏳ Pending | — |
| 4A-4K (large clusters) | ~1,500 | ⏳ Pending | — |
| 5A-5L (small clusters) | ~100 | ⏳ Pending | — |
| 6 (standalone) | ~116 | ⏳ Pending | — |
| 7 (si- unification) | ~65 | ⏳ Pending | — |

---

*This plan is based on the consolidation map analysis dated 2026-07-12. No repos have been modified or archived. All actions require Casey's explicit approval before execution.*
