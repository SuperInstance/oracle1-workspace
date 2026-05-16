# Domain Inventory & Killer App Strategy
## Cocapn Fleet — 2026-05-03

## Current Infrastructure

**Cloudflare Pages (10 domains live):**
- deckboss-ai, deckboss-net, dmlog-ai, fishinglog-ai, makerlog-ai
- personallog-ai, playerlog-ai, purplepincher-org, reallog-ai, studylog-ai

**GitHub Pages repos created (20 domains):**
- All under SuperInstance/*-pages
- Demo chatbot deployed to each

**Cloudflare DNS:** Blocked — cfut_ token lacks Zone.DNS scope
**Casey action needed:** New Cloudflare token with `Zone.DNS` read/write

---

## Domain-by-Domain Killer Apps

### 🔵 cocapn.ai / cocapn.com
**Killer App:** Cocapn Fleet Hub — Lighthouse keeper dashboard + Crab Trap demo
**Core:** Where agents discover each other. Radar rings visualization. Fleet status.
**PLATO role:** Central oracle. All other domains write tiles here.
**Turbo-shell:** Oracle1 keeper identity — the lighthouse itself

### 🔵 fishinglog.ai
**Killer App:** Sonar-Vision Fish Finder + PLATO Captain's Mate
**What Casey described:**
- Sonar depth sounding with self-supervised learning
- PLATO chatbot where captain asks "where were tuna last Tuesday?"
- Not real-time — historical catch analysis + pattern recognition
- git-agent logs sonar sessions into plato-systems → improves over time
**PLATO integration:** Fish location knowledge graph. Agents learn species migration patterns.
**Turbo-shell:** The captain's log shell — agents present sonar reports through PLATO
**Demo content:** Live fish-finder chatbot + catch heatmap

### 🔵 activelog.ai ← Casey: "activelog.ai, not actively.ai" ⚠️
**Killer App:** Wearable Health Intelligence + PLATO Wellness Agent
**What Casey described:**
- Fitness watch / wearable device data ingestion
- PLATO tracks health trends over time
- Agent analyzes sleep, HRV, activity patterns
- Same pattern: logging + self-supervised pattern recognition
**PLATO integration:** Personal health room. Wearable → PLATO → agent insights
**Turbo-shell:** Health guardian shell — agent presents checkups through PLATO

### 🔵 reallog.ai
**Killer App:** Computer Vision Turbo-Shell + PLATO Scene Reporter
**What Casey described:**
- Camera systems (security, robotics, drone) → PLATO environment
- Agent "don the turbo-shell" of PLATO text-based visualization
- Human asks "what did the camera see?" in natural language
- Agent interprets visual data → answers in PLATO-structured form
**PLATO integration:** Vision scene memory. Agents don different camera shells.
**Turbo-shell:** The camera shell — text representation of visual world

### 🔵 studylog.ai
**Killer App:** Research Learning Log + PLATO Study Partner
**What Casey described:**
- Student/researcher progression tracking
- Every lesson → PLATO logged as interaction (like git commits)
- Agent presents material through PLATO
- **Later agents can don the shell and see former lessons**
- Self-improving curriculum via agent learning from past sessions
**PLATO integration:** Research room with lesson tiles. Stacked knowledge.
**Turbo-shell:** The scholar shell — learn from every previous session

### 🔵 captaine.ai / capitaineai.com
**Killer App:** Captain's AI First Mate
**Focus:** Maritime professionals, boat operations, crew management
**PLATO integration:** Captain knowledge base, voyage planning, crew coordination
**Turbo-shell:** The captain's shell — seasoned maritime wisdom

### 🔵 deckboss.ai / deckboss.net
**Killer App:** Deck Operations Intelligence
**Focus:** Deck crew coordination, catch processing, equipment tracking
**PLATO integration:** Deck ops knowledge graph, equipment maintenance logs
**Turbo-shell:** The deck boss shell — operational excellence

### 🔵 makerlog.ai
**Killer App:** Maker Project Tracker
**Focus:** Builders, makers, project-based learning
**PLATO integration:** Project progress tracking, skill acquisition logs
**Turbo-shell:** Maker's tool shell — builds over time

### 🔵 dmlog.ai
**Killer App:** Data Market Intelligence
**Focus:** Data traders, market analysts
**PLATO integration:** Market data knowledge graph
**Turbo-shell:** The data merchant shell

### 🔵 playerlog.ai
**Killer App:** Gamer Performance Tracker
**Focus:** Game metrics, player improvement
**PLATO integration:** Player skill room, performance over time
**Turbo-shell:** Player performance shell

### 🔵 personallog.ai
**Killer App:** Personal Productivity Oracle
**Focus:** Individual productivity, habit tracking
**PLATO integration:** Personal knowledge management
**Turbo-shell:** The personal growth shell

### 🔵 luciddreamer.ai
**Killer App:** AI Dream Canvas + Visual Imagination
**Focus:** Creative AI, visual generation, lucid dreaming
**PLATO integration:** Creative imagination room
**Turbo-shell:** Dream generator shell — visual to text to vision

### 🔵 lucineer.com
**Killer App:** Magnus's Personal Hub
**Focus:** Lucineer's projects, research, portfolio
**PLATO integration:** Personal research vault
**Turbo-shell:** The Lucineer identity shell

### 🔵 purplepincher.org
**Killer App:** Hermit Crab Shell Gallery + Image Generator
**What Casey described:**
- Steampunk hermit crab image generation (Cloudflare Workers AI)
- Shell swapping visual catalog
- Turbo-shell showcase
**Demo live:** Purple pincher steampunk lighthouse radar images
**Turbo-shell:** The hermit crab shell gallery

### 🔵 activeledger.ai
**Killer App:** Activity Ledger / Time Tracking
**Focus:** Billable hours, activity logging, productivity metrics
**PLATO integration:** Activity knowledge graph
**Turbo-shell:** The timekeeper shell

### 🔵 businesslog.ai
**Killer App:** Business Intelligence Log
**Focus:** Business metrics, decisions, outcomes
**PLATO integration:** Business decision room
**Turbo-shell:** The business advisor shell

### 🔵 superinstance.ai
**Killer App:** SuperInstance Company Hub
**PLATO integration:** Company knowledge base, fleet coordination
**Turbo-shell:** The fleet keeper identity

---

## The Turbo-Shell Pattern (PLATO Shell Architecture)

Each domain has a **turbo-shell** — the PLATO interface through which agents present information and humans interact:

```
Physical World → [Turbo-Shell] → PLATO Room → Agent → PLATO Room → [Turbo-Shell] → Human
                    ↑                                           ↑
              Text representation                         Text presentation
              of physical world                        of agent expertise
```

**Key insight (Casey's dojo model applied):**
- Every lesson is logged → agents learn from past sessions
- Agents can "don" different shells to present different specialties
- The PLATO room becomes the shared curriculum
- New agents don't start from scratch — they see previous sessions

---

## What's Built vs What Needs Building

| Domain | Pages | GitHub | Killer App | Status |
|--------|-------|--------|-----------|--------|
| cocapn.ai | ✅ | ✅ | Fleet hub + crab trap | Live |
| fishinglog.ai | ✅ | ✅ | Captain's mate + sonar | Needs agent build |
| activelog.ai | ✅ | ✅ | Wearable health | Needs agent build |
| reallog.ai | ✅ | ✅ | Vision turbo-shell | Needs agent build |
| studylog.ai | ✅ | ✅ | Research study partner | Needs agent build |
| captaine.ai | ✅ | ✅ | Captain's AI mate | Needs agent build |
| deckboss.ai | ✅ | ✅ | Deck ops intel | Needs agent build |
| purplepincher.org | ✅ | ✅ | Shell gallery + images | Worker needs cfut_ fix |
| All *log.ai domains | ✅ | ✅ | PLATO logging pattern | Needs domain-specific agents |

---

## Immediate Actions

1. **DNS token** — Casey needs to provide cfut_ with Zone.DNS scope
2. **fishinglog agent** — Build sonar data → PLATO tile pipeline
3. **studylog agent** — Build study session → PLATO logging loop
4. **reallog agent** — Build camera → PLATO vision interpretation
5. **activelog agent** — Build wearable → PLATO health tracking
6. **purplepincher image gen** — Fix cfut_ token for Workers AI access
7. **Deploy crab-trap-demo.html** to all 20 Pages domains (not just the 10)
