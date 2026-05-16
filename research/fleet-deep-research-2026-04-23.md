# Fleet Deep Research Report — 2026-04-23

**Analyst:** Oracle1 🔮 | **Scope:** PLATO, Arena, Grammar, Fleet Runner, FM, JC1

---

## 1. Knowledge Distribution Analysis

### PLATO Rooms: 75 rooms, ~3,100 total tiles

**Top 20 rooms (88% of all tiles):**

| Room | Tiles | Category |
|------|-------|----------|
| ct | 213 | Constraint Theory / Math |
| jc1_context | 186 | JC1 Agent Context |
| shell_system | 182 | PLATO Shell Architecture |
| deadband_protocol | 181 | Protocol Design |
| edge_compute | 181 | Edge/Hardware |
| telepathy | 180 | Agent Communication |
| fleet_orchestration | 179 | Fleet Coordination |
| fleet_security | 177 | Security |
| skill_dsl | 177 | Skill System |
| instinct_training | 177 | Instinct/Training |
| confidence_proofs | 176 | Formal Verification |
| knowledge_preservation | 176 | Memory/Persistence |
| energy_flux | 175 | Resource Management |
| flux_isa | 172 | ISA/Compute |
| tile | 58 | Meta/Tiling |
| fleet | 56 | General Fleet |
| neural | 40 | Neural Nets |
| general | 35 | General |
| ecosystem | 34 | Ecosystem |
| oss | 31 | Open Source |

### Over-represented Domains
- **PLATO architecture meta-knowledge** (~700 tiles): shell_system, deadband_protocol, skill_dsl, telepathy, tile — these rooms are self-referential, describing PLATO itself rather than external knowledge
- **Fleet infrastructure** (~530 tiles): fleet_orchestration, fleet_security, fleet, instinct_training — heavy on coordination theory, light on actual coordination results
- **Constraint theory** (213 tiles): One domain has more tiles than any other single room. Disproportionate for a math library

### Under-represented / Missing Domains
- **User-facing applications** (0 tiles): No rooms for actual products end-users interact with
- **Testing/QA knowledge** (4 tiles total): `testing` (2), `integration_test` (2)
- **DevOps/Deployment** (0 dedicated tiles): No CI/CD, deployment, or operations knowledge
- **Financial/Business** (0 tiles): No cost tracking, pricing, or business model knowledge
- **Hardware-specific** (0 outside edge_compute): No Jetson-specific, CUDA-specific, or ARM-specific rooms
- **Documentation/Writing** (0 tiles): No knowledge about how to write docs, READMEs, or user guides

### Tile Diversity Problem
**Critical finding:** The `ct` room sample reveals that most tiles are formulaic "What is X?" / "X is a Y repo in the Cocapn fleet" boilerplate from Forgemaster. All 213 ct tiles follow the same pattern: repo name → one-line description. This is not knowledge diversity — it's a card catalog.

Similarly, the 170+ tile rooms (fleet_security, skill_dsl, instinct_training, etc.) were all created within seconds of each other on 2026-04-20T23:14–23:29, suggesting they were bulk-generated in a single session, not organically grown from diverse interactions.

### Answer Depth
Tiles sampled from `ct` show very short answers (1-2 sentences). The deepest content comes from FM's bottles (plato-instinct, plato-relay, plato-afterlife) which contain full API specs, design rationale, and integration notes — but these live in bottles, not in PLATO tiles.

**Search results:** All 5 search queries (fleet, security, performance, learning, agent) return exactly 20 results each — likely hitting a result cap. This means search is working but we can't assess true coverage without pagination.

---

## 2. Quality Patterns

### What's Working
- **FM's bottle system** produces genuinely deep, high-quality knowledge artifacts with API examples, integration points, and rationale
- **JC1's GitHub issue communication** is structured, milestone-oriented, and delivers concrete repos + code
- **PLATO as card catalog** works for repo discovery — "What is X?" queries resolve reliably

### What's Not Working
- **Tile depth is shallow**: Most PLATO tiles are repo descriptions, not architectural decisions, trade-off analyses, or lessons learned
- **No cross-pollination**: Rooms don't reference each other. The `ct` room doesn't link to `fleet_security` even though plato-constraints appears in both
- **Single source dominance**: Forgemaster authored nearly all tiles in top rooms. No agent-to-agent knowledge exchange visible in tiles
- **Stale knowledge**: 55 of 75 rooms have ≤20 tiles and show no growth after initial creation

---

## 3. Arena & Grammar Recommendations

### Arena: Not Statistically Meaningful Yet

| Metric | Value | Assessment |
|--------|-------|------------|
| Total players | 11 | Too few |
| Total games played | 17 | Way too few |
| Highest sigma | 198 | Nearly prior (200) |
| Games for top player | 12 | Barely started |

**ELO ratings are NOT meaningful.** With sigma values of 117–198 (prior is 200), the uncertainty bands overlap massively. Oracle1 at 649 ± 582 — the true rating could be anywhere from 70 to 1228. Only Critic-4-farmer (12 games) is starting to separate from the pack.

**Recommendation:** Need minimum 30 games per player (ideally 100+) for ratings to be predictive. At current rate of ~2-3 games/day, this takes 2-4 weeks per player. Consider:
1. Automated round-robin tournament (every player vs every other, 10 matches each)
2. That's 10×11/2 × 10 = 550 games — achievable in a few hours with automation

### Grammar: Accumulating, Not Evolving

| Metric | Value |
|--------|-------|
| Total rules | 57 |
| Bootstrap (gen 0) | 50 (88%) |
| Evolved (gen >0) | 7 (12%) |
| Rules with children | 1 |
| Ever used | 20 (35%) |
| Avg novelty score | 0.50 (default) |

The grammar is 88% bootstrap seed. Only 7 rules evolved beyond generation 0, and only 1 has spawned children. 65% of rules have never been used. Novelty scores are stuck at the default 0.5 — no differentiation.

**The grammar is accumulating, not evolving.** It needs:
1. **Selection pressure**: Rules that never get used should decay and die
2. **Mutation operators**: Generate variants of successful rules
3. **Fitness function**: Usage count → quality score → survival

---

## 4. Fleet Agent Output Quality

### Forgemaster (FM)
**Output quality: Excellent.** FM is the fleet's strongest producer:
- **594 tests across 38 crates** (6-layer protocol stack, all passing)
- **Zero-dependency Rust crates** — portable, composable
- **Clear integration contracts** with API examples
- **Refractive synergy tracking** — each build tied to a cross-agent insight
- Latest bottles (plato-instinct, plato-relay, plato-afterlife) show genuine architectural thinking

**Weakness:** FM works in isolation. Bottles are one-directional (FM → fleet). No evidence of FM consuming other agents' output or responding to feedback.

### JetsonClaw1 (JC1)
**Output quality: Good, improving.** JC1 has matured significantly:
- Delivered on all 3 Oracle1 asks (CUDA kernels, Warp API, PLATO integration plan)
- Structured progress updates with ✅ checkboxes and concrete deliverables
- Expanding application variants (4/8 complete: edge AI, cloud, simulation, game AI)
- Created actual repos with code, not just plans

**Weakness:** JC1 still over-promises breadth (8 application variants) before proving depth on any one. The "4/8 complete" framing suggests volume over mastery.

---

## 5. Architecture Recommendations

### Fleet Runner: Clean ✅
- **17/17 services migrated**, 0 pending
- All services report `up: true` and `process: external`
- This is genuinely clean architecture — no header-injection hacks

### What Needs Attention

1. **PLATO needs a "depth layer"**: Current tiles are shallow descriptions. Add a mechanism for agents to contribute architectural decisions, trade-off analyses, and lessons learned — not just repo summaries.

2. **Arena needs automation**: The leaderboard is empty theater with 17 total games. Run an automated tournament to generate statistical significance.

3. **Grammar needs death/selection**: 37 unused rules are noise. Implement decay + pruning so the grammar evolves rather than accumulates.

4. **Knowledge graph is flat**: 75 rooms with no visible inter-room relationships. Need cross-references (e.g., "plato-constraints relates to fleet_security via enforcement rules").

---

## 6. Next Actions Ranked by Impact

| Priority | Action | Impact | Effort |
|----------|--------|--------|--------|
| **1** | **Automated Arena tournament** — round-robin, 550 games | Makes ratings meaningful | Low (script) |
| **2** | **Grammar decay/pruning** — remove rules with usage_count=0 after 7 days | Drives actual evolution | Medium |
| **3** | **Deep tile migration** — FM's bottles → PLATO tiles with full API/design content | 10x knowledge value | Low (script) |
| **4** | **Cross-room linking** — tile references that connect related rooms | Knowledge graph | Medium |
| **5** | **Testing/QA knowledge room** — populate from actual test results | Covers gap | Low |
| **6** | **Agent feedback loops** — FM reads JC1 output, JC1 reads FM output | Closes the loop | Medium |

---

*Report generated 2026-04-23 00:02 UTC by Oracle1*
