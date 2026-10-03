# SuperInstance Repository Consolidation Map

**Audit Date:** 2026-07-12  
**Auditor:** Automated subagent analysis  
**Scope:** All non-archived repos in the SuperInstance GitHub account  

---

## Executive Summary

The SuperInstance account contains **4,229 non-archived repositories** (5 archived). This is a massively fragmented ecosystem with deep prefix-based clusters. The original ideation docs estimated ~750+ repos across 12 clusters; the actual count is **5.6× larger** with **28 identifiable clusters**.

### Key Findings

1. **No repo has more than 5 stars** — the entire ecosystem is essentially zero-external-usage
2. **Most repos were pushed on 2026-07-12** (today) — indicating batch/automated creation
3. **120 repos are explicitly labeled as sketch/demo/proto/experiment/early-version**
4. **18 repos have numbered duplicate suffixes** (`-1`, `-2`, etc.)
5. **Multi-language port duplication is pervasive** — many concepts have `-rs`, `-c`, `-py`, `-go`, `-wasm`, `-zig`, `-ts` variants
6. **Cross-cluster duplication exists** — e.g., `conservation-spectral-*` spans two clusters

---

## Cluster Inventory (28 Clusters)

### Cluster 1: `ternary-` — Ternary Computing System
| Metric | Value |
|--------|-------|
| **Repo count** | 370 |
| **Most starred** | None above 2⭐ |
| **Canonical repos** | `ternary-core` (11 commits), `ternary-cli` (10), `ternary-agent` (13) |
| **Sub-clusters** | compiler (4), spreadsheet (3), shard (3), search (3), language (3), inference (3), fleet (3) |

**Assessment:** Largest cluster by count. Extremely granular — 370 repos covering ternary arithmetic, automata, blockchain, Bayesian methods, circuits, etc. Many appear to be single-concept sketches.

**Recommended action:**
- **Consolidate into 10-15 repos** organized by subsystem (compiler, arithmetic, gates, ML, crypto, etc.)
- **Archive** the ~330 single-concept repos after merging their content
- Key keepers: `ternary-core`, `ternary-cli`, `ternary-compiler-*`, `ternary-agent`

---

### Cluster 2: `lau-` — Mathematics & Theory Research
| Metric | Value |
|--------|-------|
| **Repo count** | 333 |
| **Most starred** | None above 2⭐ |
| **Canonical repos** | `lau-self-modeling`, `lau-construct-integration`, `lau-room-native` |
| **Sub-clusters** | Math/Theory (~85), Agents/AI (~60), Systems/Engineering (~30), Physics (~15) |

**Assessment:** Massive academic/research namespace. Covers differential geometry, algebraic topology, sheaf theory, spectral analysis, information geometry, quantum topology, etc. Each concept typically has a `-theory` and `-agents` variant (e.g., `lau-probability-theory` + `lau-probability-agents`).

**Recommended action:**
- **Create a `lau-math` monorepo** for the ~85 pure math repos (merge by domain: geometry, topology, algebra, analysis, probability)
- **Create a `lau-agents` monorepo** for the ~60 agent variant repos
- **Merge** the 4 `lau-sia2-engine-*` repos (C, Go, WASM, base) into one multi-language repo
- **Merge** the 5 `lau-shell-*` repos into one
- **Archive** ~250 repos after consolidation

---

### Cluster 3: `fleet-` — Fleet Orchestration
| Metric | Value |
|--------|-------|
| **Repo count** | 319 |
| **Most starred** | `fleet-manifold` (2⭐), `fleet-daily` (2⭐), `fleet-health-monitor` (2⭐) |
| **Canonical repos** | `fleet-router` (active), `fleet-daemon`, `fleet-warden-rs`, `fleet-yaw` |
| **Sub-clusters** | **midi (92!)**, math (8), agent (4), a2a (4), dashboard (3), constraint (3) |

**Assessment:** The `fleet-midi-*` sub-cluster alone has **92 repos** — covering MIDI arpeggiators, chord generators, quantizers, tokenizers, etc. This is an extreme case of per-feature repo creation. The non-MIDI fleet repos are the actual orchestration system.

**Recommended action:**
- **Urgent: Consolidate 92 `fleet-midi-*` repos** into a single `fleet-midi` monorepo with subdirectories
- **Merge** fleet-math-* (8 repos) into one
- **Merge** fleet-router + fleet-router-integration
- **Merge** fleet-orchestrator + fleet-orchestrator-v2 (archive v2 if superseded)
- **Archive** ~280 repos, keeping ~15-20 core repos

---

### Cluster 4: `plato-` — Platform Framework
| Metric | Value |
|--------|-------|
| **Repo count** | 275 |
| **Most starred** | Multiple at 2⭐ (`plato-tile-*`, `plato-server`, `plato-cli`, `plato-kernel`, etc.) |
| **Canonical repos** | `plato-core` (14 commits), `plato-kernel` (23), `plato-server` (11), `plato-cli` (11) |
| **Sub-clusters** | **tile (36!)**, **room (21!)**, forge (8), engine (6), vessel (4), client (4) |

**Assessment:** Second-largest platform cluster. The `plato-tile-*` (36 repos) and `plato-room-*` (21 repos) subsystems are heavily fragmented. Multi-language client duplication (`plato-client-js`, `-php`, `-ruby`).

**Recommended action:**
- **Consolidate 36 `plato-tile-*` repos** into `plato-tile` monorepo
- **Consolidate 21 `plato-room-*` repos** into `plato-room` monorepo
- **Merge** plato-forge-* (8 repos) into one
- **Merge** plato-client-* (4 repos) into `plato-client` with language branches
- **Archive** ~200 repos, keeping ~15-20

---

### Cluster 5: `flux-` — Runtime/Compiler/VM
| Metric | Value |
|--------|-------|
| **Repo count** | 213 |
| **Most starred** | `flux-core` (2⭐), `flux-runtime` (2⭐, 100+ commits!), `flux-baton` (2⭐), `flux-spec` (2⭐) |
| **Canonical repos** | `flux-runtime` (100+ commits, most active), `flux-core` (27), `flux-compiler` (18) |
| **Sub-clusters** | runtime (9), isa (9), vm (8), compiler (4), algebra (3), check (3), agent (3) |

**Assessment:** Flux-runtime is the single most developed repo in the entire ecosystem (100+ commits). However, there are 9 `flux-runtime-*` variants and 8 `flux-vm-*` variants. Multi-language explosion in flux-algebra (`-c`, `-rs`, `-ruby`).

**Recommended action:**
- **flux-runtime is canonical** — merge flux-runtime-* (9 repos) into it as subdirectories
- **Merge** flux-vm-* (8 repos) into `flux-vm` monorepo
- **Merge** flux-compiler-* (4 repos) into `flux-compiler`
- **Merge** flux-isa-* (9 repos) into `flux-isa`
- **Archive** ~170 repos, keeping ~15

---

### Cluster 6: `cuda-` — GPU/CUDA Infrastructure
| Metric | Value |
|--------|-------|
| **Repo count** | 143 |
| **Most starred** | None above 1⭐ |
| **Canonical repos** | `cudaclaw` (the original) |
| **Sub-clusters** | Highly diverse — 130+ unique concept names |

**Assessment:** Despite the `cuda-` prefix, most repos are NOT about CUDA kernels. They use `cuda-` as a namespace prefix for a wide range of agent/system concepts (cuda-ethics, cuda-emotion, cuda-narrative, etc.). This is extremely confusing naming.

**Recommended action:**
- **Rename** non-CUDA repos to drop the misleading `cuda-` prefix
- **Consolidate** genuine GPU repos into `cuda-kernels` or `cuda-core`
- **Merge** related concept groups (cuda-fleet-health + cuda-fleet-mesh + cuda-fleet-topology → one repo)
- **Archive** ~120 repos after consolidation

---

### Cluster 7: `agent-` — Agent Framework
| Metric | Value |
|--------|-------|
| **Repo count** | 80 |
| **Most starred** | None above 2⭐ |
| **Canonical repos** | `agent-to-agent`, `agent-coordinator`, `agent-orchestration` |
| **Sub-clusters** | Music-themed naming: rhythm, harmony, counterpoint, groove, swing, etc. |

**Assessment:** Music-theory-inspired agent framework. Many repos describe individual musical concepts (agent-fermata, agent-rubato, agent-staccato-legato). Versioned duplicates exist (agent-riff, -v2, -v3, -v4).

**Recommended action:**
- **Merge** agent-riff + agent-riff-v2 + agent-riff-v3 + agent-riff-v4 → single `agent-riff`
- **Consolidate** the 80 repos into ~10 thematic repos (rhythm, harmony, identity, coordination, etc.)
- **Archive** ~70 repos

---

### Cluster 8: `cocapn-` — Multi-Language Runtime/SDK
| Metric | Value |
|--------|-------|
| **Repo count** | 76 |
| **Most starred** | `cocapn-core` (2⭐), `cocapn` top-level (3⭐), `cocapn-design` (2⭐), `cocapn-health` (2⭐) |
| **Canonical repos** | `cocapn` (73 commits!), `cocapn-cli` (21), `cocapn-runtime` (10) |
| **Sub-clusters** | Multi-language: c, go, lua, py, python, wasm, zig, forth |

**Assessment:** Well-structured multi-language SDK pattern, but each language is a separate repo. The top-level `cocapn` repo has the most commits in the cluster. Fleet integration repos (cocapn-fleet-*) overlap with the fleet cluster.

**Recommended action:**
- **Merge** language SDKs into `cocapn-sdk` with per-language subdirectories (or use a polyrepo SDK template)
- **Merge** cocapn-fleet-* into the fleet cluster
- **Merge** cocapn-health + cocapn-health-rs
- **Merge** cocapn-explain + cocapn-explain-rs
- **Archive** ~55 repos, keeping ~15

---

### Cluster 9: `conservation-` — Conservation Law Verification
| Metric | Value |
|--------|-------|
| **Repo count** | 57 |
| **Most starred** | `conservation-law-rs` (1⭐) |
| **Canonical repos** | `conservation-law-rs` (14 commits) |
| **Sub-clusters** | **spectral (20!)** — conservation-spectral-* spans 15+ language variants |

**Assessment:** The `conservation-spectral-*` sub-cluster alone has ~20 repos representing the same algorithm in different languages (C, Chapel, CUDA, Fortran, Forth, JS, Lisp, Mojo, OpenCL, Pascal, PTX, Python, Vulkan, WebGPU, Zig). This is an extreme polyglot experiment.

**Recommended action:**
- **Consolidate 20 `conservation-spectral-*` repos** into ONE `conservation-spectral` monorepo with per-language directories
- **Merge** conservation-law + conservation-law-rs + conservation-law-v2 → single repo
- **Merge** conservation-matrix-c + conservation-matrix-rs → single repo
- **Archive** ~40 repos, keeping ~8

---

### Cluster 10: `constraint-` — Constraint Theory & DSL
| Metric | Value |
|--------|-------|
| **Repo count** | 47 |
| **Most starred** | `constraint-theory-core` (3⭐, 1 fork!), `Constraint-Theory` (2⭐, 1 fork) |
| **Canonical repos** | `constraint-theory-core` (75 commits — 3rd most active in entire org!) |
| **Sub-clusters** | theory (15), demos (5), tools (5) |

**Assessment:** constraint-theory-core is a genuine canonical repo with real development activity. However, there's a sprawl of `-theory-*` variants (python, rust, mojo, llvm, mlir, cuda, web, etc.). Naming is inconsistent (`Constraint-Theory` vs `constraint-theory-*`).

**Recommended action:**
- **constraint-theory-core is canonical** — merge all constraint-theory-* into it as subdirectories
- **Merge** Constraint-Theory (capital) → constraint-theory (lowercase)
- **Merge** constraint-demo + constraint-demos → one
- **Archive** ~35 repos, keeping ~8

---

### Cluster 11: `superinstance-` + `si-` — Core Platform
| Metric | Value |
|--------|-------|
| **Repo count** | 34 + 43 = 77 combined |
| **Most starred** | `SuperInstance` top-level (5⭐ — highest in org!) |
| **Canonical repos** | `SuperInstance` (100+ commits!), `superinstance-harness` (30MB, largest repo) |
| **Sub-clusters** | si-runtime-* (5 languages), si-conservation-* (4), si-*-agent (7) |

**Assessment:** The `superinstance-` prefix and `si-` prefix represent the same platform. The top-level `SuperInstance` repo is the org's flagship (5 stars, 100+ commits). `si-runtime-*` has 5 language variants. `si-*-agent` has 7+ agent repos.

**Recommended action:**
- **Unify** `si-*` repos into `superinstance-*` namespace (or vice versa)
- **Merge** si-runtime-* (5 repos) into `superinstance-runtime` with language dirs
- **Merge** si-conservation-* into the conservation cluster
- **Merge** si-*-agent repos into `superinstance-agent`
- **Archive** ~55 repos, keeping ~12

---

### Cluster 12: `grand-pattern-` — Multi-Language Pattern Library
| Metric | Value |
|--------|-------|
| **Repo count** | 42 + 1 (`grand-synthesis`) = 43 |
| **Canonical repos** | `grand-pattern-core` (7 commits) |
| **Sub-clusters** | Language variants: C, Chapel, CUDA, Fortran, Go, Java, Mojo, OpenCL, PTX, Python, Rust, Swift, TS, WASM, Zig |

**Assessment:** Pure polyglot explosion — the same pattern library implemented in 15+ languages. Each is a separate repo.

**Recommended action:**
- **Consolidate ALL 42 repos** into a single `grand-pattern` monorepo with per-language directories
- This is the clearest consolidation case — one concept, 42 repos

---

### Cluster 13: `oxide-` — Systems Infrastructure
| Metric | Value |
|--------|-------|
| **Repo count** | 30 |
| **Canonical repos** | `oxide-fleet` (10 commits) |
| **Themes** | circuit-breaker, checkpoint, compactor, crdt, federation, journal, pipeline, raft-log |

**Assessment:** Infrastructure primitives. Each is a separate concern that could live as modules in a systems library.

**Recommended action:**
- **Consolidate** into `oxide-core` monorepo with feature modules
- **Archive** ~25 repos, keeping ~5

---

### Cluster 14: `spectral-` — Spectral Methods
| Metric | Value |
|--------|-------|
| **Repo count** | 24 |
| **Canonical repos** | `spectral-graph-core` |
| **Themes** | clustering, conservation, deadband, fingerprint, fleet, graph, mechanics, music, prosody |

**Assessment:** Cross-cutting cluster that overlaps with conservation, fleet, and graph clusters.

**Recommended action:**
- **Merge** spectral-* into relevant parent clusters (spectral-fleet → fleet, spectral-conservation → conservation)
- **Keep** spectral-graph-* as the spectral math library
- **Archive** ~15 repos

---

### Cluster 15: `openconstruct-` — Multi-Language Construction Framework
| Metric | Value |
|--------|-------|
| **Repo count** | 22 |
| **Canonical repos** | `OpenConstruct` (top-level), `openconstruct-rust` (9 commits) |
| **Sub-clusters** | Language variants: C, CS, Go, Java, Python, Ruby, Rust, Swift, TS, Zig |

**Assessment:** Another polyglot framework — 10+ language implementations.

**Recommended action:**
- **Consolidate** into `OpenConstruct` monorepo with per-language directories
- **Archive** ~18 repos

---

### Cluster 16: `eisenstein-` — Eisenstein Integer Mathematics
| Metric | Value |
|--------|-------|
| **Repo count** | 16 |
| **Most starred** | `eisenstein-c` (2⭐, 1 fork) |
| **Canonical repos** | `eisenstein-c` (7 commits) |
| **Themes** | Math theory + implementations (C, CUDA, WASM) + tooling |

**Recommended action:**
- **Consolidate** into single `eisenstein` monorepo
- **Archive** ~13 repos

---

### Cluster 17: `nexus-` — Integration Infrastructure
| Metric | Value |
|--------|-------|
| **Repo count** | 18 |
| **Canonical repos** | `nexus-runtime` |
| **Themes** | comms, data-pipeline, edge-runtime, persistence, security, simulation |

**Recommended action:**
- **Consolidate** into `nexus-core` monorepo
- **Archive** ~14 repos

---

### Cluster 18: `zeroclaw-` / `zc-` — Agent Arena Framework
| Metric | Value |
|--------|-------|
| **Repo count** | 24 (16 zc-* + 8 zeroclaw-*) |
| **Most starred** | `zeroclaw-crew` (2⭐) |
| **Canonical repos** | `zeroclaw-crew` (10 commits) |
| **Sub-clusters** | zc-*-shell (11 — role-based shells: alchemist, archivist, curator, herald, etc.) |

**Recommended action:**
- **Merge** 11 `zc-*-shell` repos into `zc-shells` monorepo
- **Merge** zeroclaw-* repos into `zeroclaw` monorepo
- **Archive** ~20 repos

---

### Cluster 19: `forge-` — Build/Forge Tooling
| Metric | Value |
|--------|-------|
| **Repo count** | 20 |
| **Canonical repos** | `forgemaster` (2⭐) |
| **Themes** | audio, code, data, image, memory, pipeline, sensor, text, transform |

**Recommended action:**
- **Consolidate** into `forge` monorepo
- **Archive** ~16 repos

---

### Cluster 20: `git-` — Git-Based Agent Tooling
| Metric | Value |
|--------|-------|
| **Repo count** | 18 |
| **Most starred** | `git-agent` (2⭐) |
| **Canonical repos** | `git-agent` |
| **Themes** | Agent variants: codespace, flux-pipeline, rebase, standard, system, cuda, native |

**Recommended action:**
- **Consolidate** into `git-agent` monorepo
- **Archive** ~14 repos

---

### Cluster 21: `Equipment-` — Hardware/Swarm Components
| Metric | Value |
|--------|-------|
| **Repo count** | 14 |
| **Most starred** | `Equipment-NLP-Explainer` (2⭐) |
| **Canonical repos** | `Equipment-Consensus-Engine` (28 commits) |
| **Sub-clusters** | Multi-language: Consensus-Engine + PHP + Ruby variants |

**Recommended action:**
- **Merge** language variants (Consensus-Engine + PHP + Ruby → one repo)
- **Consolidate** remaining into `equipment-core`
- **Archive** ~10 repos

---

### Cluster 22: `holodeck-` — Simulation Environment
| Metric | Value |
|--------|-------|
| **Repo count** | 10 |
| **Most starred** | `holodeck-rust` (3⭐), `holodeck-core` (2⭐) |
| **Canonical repos** | `holodeck-rust` (44 commits — well-developed!) |
| **Sub-clusters** | Language variants: C, CUDA, Go, Rust, Zig |

**Recommended action:**
- **Merge** language variants into `holodeck` monorepo
- **Archive** ~7 repos

---

### Cluster 23: `exocortex-` — Edge Compute
| Metric | Value |
|--------|-------|
| **Repo count** | 11 |
| **Canonical repos** | None dominant |
| **Themes** | Multi-language edge runtime: C++, Mojo, Lua, Python, Zig, TS |

**Recommended action:**
- **Consolidate** into `exocortex` monorepo
- **Archive** ~9 repos

---

### Cluster 24: `deckboss-` — Deck Boss Marketplace
| Metric | Value |
|--------|-------|
| **Repo count** | 4 |
| **Most starred** | `DeckBoss` (2⭐, 32 commits) |
| **Canonical repos** | `DeckBoss` |

**Recommended action:**
- **Merge** all 4 into `DeckBoss`
- **Archive** 3 repos

---

### Cluster 25: `a2a-` — Agent-to-Agent Protocol
| Metric | Value |
|--------|-------|
| **Repo count** | 7 |
| **Canonical repos** | `a2a-protocol` |
| **Themes** | adapter, constraint-protocol, future, signal-chain |

**Recommended action:**
- **Merge** into `a2a-protocol` monorepo
- **Archive** 5 repos

---

### Cluster 26: `activelog-` — Active Logging
| Metric | Value |
|--------|-------|
| **Repo count** | 7 |
| **Canonical repos** | `activelog-backend` |

**Recommended action:**
- **Merge** into single `activelog` repo
- **Archive** 5 repos

---

### Cluster 27: `activeledger-` — Active Ledger
| Metric | Value |
|--------|-------|
| **Repo count** | 3 |

**Recommended action:**
- **Merge** into single `activeledger` repo

---

### Cluster 28: `categorical-` — Category Theory Agents
| Metric | Value |
|--------|-------|
| **Repo count** | 4 |
| **Sub-clusters** | Multi-language: agents, agents-c, agents-rs |

**Recommended action:**
- **Merge** into single `categorical-agents` repo with per-language dirs

---

## Additional Notable Sub-Clusters (Non-Prefixed)

### `craftmind-` (9 repos)
Role-based repos (circuits, courses, discgolf, fishing, herding, ranch, researcher, studio). Appears to be a personal project ecosystem. Consolidate into one repo.

### `mud-` (6 repos)
MUD game system (arena, bridge, expert, mcp, solitaire). Small enough to merge into one repo.

### `studylog-` / `Studylog-` / `StudyLog-` (5 repos)
Study logging with inconsistent casing. Merge into `StudyLog`.

### `tropical-` (9 repos)
Tropical geometry/math implementations. Merge into one repo.

### `symplectic-` (7 repos)
Symplectic math implementations. Merge into one repo.

### `vessel-` (11 repos)
Vessel coordination system. Merge into `vessel` monorepo.

### `graph-` (14 repos)
Graph algorithm implementations. Merge into `graph-rs` monorepo.

### `spreadsheet-` (9 repos)
Spreadsheet engine variants. Merge into one repo.

### `crdt-` / `SmartCRDT` (10+ repos)
CRDT implementations scattered across clusters. Consolidate into one.

### `swarm-` (9 repos)
Swarm orchestration. Merge into one repo.

### `character-` (8 repos)
Character/game system. Merge into one repo.

### `entropy-` (9 repos)
Entropy/math implementations. Merge into one repo.

### `edge-` (11 repos)
Edge computing. Merge into one repo.

---

## Cross-Cutting Patterns

### Multi-Language Port Duplication

The same concept implemented in 5-15+ languages as separate repos is the **#1 source of repo sprawl**:

| Concept | Languages | Repo Count |
|---------|-----------|------------|
| conservation-spectral | C, Chapel, CUDA, Fortran, Forth, JS, Lisp, Mojo, OpenCL, Pascal, PTX, Python, Vulkan, WebGPU, Zig | 20 |
| grand-pattern | C, Chapel, CUDA, Fortran, Go, Java, Mojo, OpenCL, PTX, Python, Rust, Swift, TS, WASM, Zig | 42 |
| openconstruct | C, CS, Go, Java, Python, Ruby, Rust, Swift, TS, Zig | 22 |
| holodeck | C, CUDA, Go, Rust, Zig | 10 |
| si-runtime | C, Go, JS, Python, WASM, Zig | 6 |
| lau-sia2-engine | C, Go, WASM, base | 4 |
| cocapn | C, Go, Lua, Python, WASM, Zig, Forth | 8 |

**Recommendation:** Adopt a **monorepo-with-language-dirs** pattern for all multi-language projects.

### Versioned Duplicate Repos

Explicitly versioned/suffixed repos that should be merged or have the older version archived:

- `agent-riff` → `agent-riff-v2` → `agent-riff-v3` → `agent-riff-v4` (4 repos!)
- `plato-e2e-pipeline-v2`
- `conservation-law-v2`
- `conservation-spectral-v2`
- `spectral-deadband-v2`
- `spectral-graph-v2`
- `spectral-music-v2`
- `cuda-metrics-v2`
- `ternary-compiler-v2`
- `ternary-compression-v2`
- `ternary-cuda-kernels-v2`
- `ternary-registry-v2`
- `ternary-scheduling-v2`
- `context-compactor-v2`
- `swarm-intuition-v2`
- `websocket-fabric-v2`
- `tick-engine-v2`
- `snapkit-v2`
- `chess-dojo-v2`
- `plato-e2e-pipeline-v2`
- `seed-mcp-v2`

### "Early Version" Repos (Explicitly Labeled)
18+ repos have `-early-version` suffix — these are explicitly marked as preliminary:
- `fleet-agent-early-version`
- `fleet-automation-early-version`
- `plato-alignments-early-version`
- `plato-calibration-early-version`
- `plato-hologram-early-version`
- `plato-stable-early-version`
- `adaptive-plato-early-version`
- `zeroclaw-agent-early-version`
- `flux-consciousness-engine-early-version`
- `flux-constraint-py-early-version`
- `attention-daemon-early-version`
- `penrose-memory-palace-early-version`
- `tile-memory-early-version`
- `the-plenum-early-version`

### Numbered Duplicates
18 repos have numbered suffixes indicating duplication:
- `cudaclaw` / `cudaclaw-1`
- `holodeck-c` / `holodeck-c-1`
- `holodeck-cuda` / `holodeck-cuda-1`
- `api-gateway` / `api-gateway-1`
- `grammar-curator-1`
- `mud-expert-1`
- `studylog-ai-1`
- `constraint-theory-web` / `constraint-theory-web-1`
- etc.

---

## Consolidation Summary

### Current State
| Metric | Count |
|--------|-------|
| Total non-archived repos | 4,229 |
| Identified cluster repos | ~1,725 |
| Other patterned repos | ~500 |
| Truly standalone repos | ~2,000 |
| Clusters identified | 28+ |
| Sketch/demo/proto repos | 120+ |
| Multi-language duplicate sets | 15+ |

### Target State After Consolidation

| Cluster | Current | Target | Reduction |
|---------|---------|--------|-----------|
| ternary- | 370 | 15 | -95% |
| lau- | 333 | 25 | -92% |
| fleet- | 319 | 20 | -94% |
| plato- | 275 | 20 | -93% |
| flux- | 213 | 15 | -93% |
| cuda- | 143 | 15 | -89% |
| agent- | 80 | 10 | -88% |
| cocapn- | 76 | 12 | -84% |
| conservation- | 57 | 8 | -86% |
| constraint- | 47 | 8 | -83% |
| grand-pattern- | 42 | 1 | -98% |
| si-/superinstance- | 77 | 12 | -84% |
| oxide- | 30 | 5 | -83% |
| spectral- | 24 | 5 | -79% |
| openconstruct- | 22 | 1 | -95% |
| eisenstein- | 16 | 1 | -94% |
| nexus- | 18 | 4 | -78% |
| zeroclaw-/zc- | 24 | 3 | -88% |
| forge- | 20 | 4 | -80% |
| git- | 18 | 4 | -78% |
| Equipment- | 14 | 5 | -64% |
| holodeck- | 10 | 2 | -80% |
| exocortex- | 11 | 2 | -82% |
| deckboss- | 4 | 1 | -75% |
| a2a- | 7 | 2 | -71% |
| activelog- | 7 | 1 | -86% |
| activeledger- | 3 | 1 | -67% |
| categorical- | 4 | 1 | -75% |
| Other sub-clusters | ~300 | ~40 | -87% |
| **TOTAL** | **~4,229** | **~250** | **-94%** |

### Priority Consolidation Queue (Highest Impact First)

1. 🔴 **grand-pattern** (42→1) — Pure polyglot, zero ambiguity, easy merge
2. 🔴 **fleet-midi** (92→1) — Largest single sub-cluster, clear boundary
3. 🔴 **conservation-spectral** (20→1) — 15 language variants of same algorithm
4. 🔴 **openconstruct** (22→1) — Another pure polyglot set
5. 🟠 **plato-tile** (36→1) — Large subsystem, clear boundary
6. 🟠 **plato-room** (21→1) — Large subsystem, clear boundary
7. 🟠 **ternary-** (370→15) — Largest overall cluster
8. 🟠 **lau-** (333→25) — Merge by domain
9. 🟠 **flux-runtime** (9→1) — Merge into canonical 100-commit repo
10. 🟡 **constraint-theory** (15→1) — Merge into canonical 75-commit repo
11. 🟡 **si-/superinstance** (77→12) — Unify namespace
12. 🟡 **agent-riff** (4→1) — Obvious version chain merge

---

## Methodology

- **Data source:** `gh repo list SuperInstance --limit 5000` and `gh api users/SuperInstance/repos` (paginated)
- **Cluster identification:** Prefix matching + thematic grouping
- **Canonical repo identification:** Stars, commit count, repo size, push recency
- **No modifications were made** — this is analysis only
- **Rate limit tracking:** Checked every 100 API calls, never dropped below 2,793 remaining

---

*End of Consolidation Map*
