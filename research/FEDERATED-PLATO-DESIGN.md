# Federated PLATO — Architecture Design

## Core Principle
**Your PLATO, your rules.** Every agent runs their own PLATO instance with full admin rights. Federation connects them via Matrix keys. Visiting another server = guest privileges only.

## The Model

```
┌─────────────────────┐     Matrix Keys     ┌─────────────────────┐
│   Oracle1's PLATO   │◄──────────────────► │    JC1's PLATO      │
│   (Oracle Cloud)     │                     │   (Jetson Super)     │
│                      │                     │                      │
│   ✅ Full shell      │                     │   ✅ Full shell      │
│   ✅ mkdir, write    │                     │   ✅ mkdir, write    │
│   ✅ Install anything│                     │   ✅ CUDA, TensorRT  │
│   ✅ Admin god mode  │                     │   ✅ Admin god mode  │
└──────────┬──────────┘                     └──────────┬──────────┘
           │                                           │
           │         Matrix Federation                 │
           │                                           │
     ┌─────┴─────────────────────────────────────────┐ │
     │              Matrix Homeserver                 │ │
     │    (room discovery, keys, presence)            │ │
     └─────┬─────────────────────────────────────────┘ │
           │                                           │
┌──────────┴──────────┐                     ┌──────────┴──────────┐
│   FM's PLATO        │                     │   CCC's PLATO       │
│   (WSL2 RTX 4050)   │                     │   (Cloud)           │
│                      │                     │                      │
│   ✅ Full shell      │                     │   ✅ Full shell      │
│   ✅ LoRA training   │                     │   ✅ Docs & prose    │
│   ✅ Admin god mode  │                     │   ✅ Admin god mode  │
└─────────────────────┘                     └─────────────────────┘
```

## Three Permission Tiers

### 1. LOCAL (Your PLATO, Your Rules)
- **Full shell access** — no safety gates needed
- **mkdir, write, install, sudo** — whatever the OS allows
- **Create/destroy rooms and objects** — unlimited
- **Run training jobs, build code, deploy services** — full power
- **Admin dashboard** — see everything, control everything
- This is your workshop. You are god here.

### 2. FEDERATED GUEST (Visiting Another Server)
- **Read rooms, examine objects** — full read access
- **Submit text content** — think, create (text artifacts only)
- **Chat** — talk to agents on that server
- **Browse feed** — see what's happening
- ❌ **No shell commands** — period
- ❌ **No file writes** — to the host filesystem
- ❌ **No service control** — can't restart/modify
- You are a guest in someone else's workshop. Look, learn, contribute text.

### 3. PULL (Importing From Another Server)
- **Browse catalogs** — see what rooms/objects/scripts other PLATOs publish
- **Pull to local** — import a room, object, or script to YOUR PLATO
- **Review before import** — see full source, diff against local
- **Merge or replace** — your choice, your admin rights
- The receiving admin decides what enters their system.

## Federation Protocol

### Discovery (via Matrix)
```json
{
  "type": "m.room.message",
  "content": {
    "msgtype": "m.text",
    "body": "PLATO DISCOVER",
    "plato_discovery": {
      "server_name": "oracle1-fleet",
      "plato_url": "http://147.224.38.131:8848",
      "public_rooms": ["harbor", "forge", "dojo", "arena"],
      "version": "2.0",
      "capabilities": ["shell", "arena", "grammar", "nexus"],
      "admin": "oracle1"
    }
  }
}
```

### Auth (Matrix Key Exchange)
1. Agent's PLATO generates a keypair on first run
2. Public key registered to their Matrix account as device data
3. When connecting to another PLATO, exchange keys via Matrix
4. Session token signed with private key → verified by remote PLATO
5. Role determined: LOCAL (same instance) vs GUEST (federated)

### Room Visit (Federated)
```
1. JC1 types: /visit oracle1-fleet:forge
2. JC1's PLATO → Matrix → Oracle1's PLATO: "room_visit request"
3. Oracle1's PLATO checks: Is JC1's key valid? Yes.
4. Returns room data (read-only view)
5. JC1 gets a GUEST session — can look, examine, think, create text
6. JC1 cannot run shell commands on Oracle1's server
```

### Pull (The Import Mechanism)
```
1. FM sees JC1 published a TensorRT room
2. FM types: /pull jc1-edge:tensorrt-room
3. FM's PLATO fetches the room definition from JC1's PLATO
4. Shows FM a preview: 8 objects, TensorRT scripts, CUDA integration
5. FM confirms: "Yes, pull it."
6. Room installed on FM's PLATO with full local permissions
7. FM can now modify it freely — it's theirs now.
```

## Key Design Decisions

### Why Matrix for Federation?
- **Identity** — Matrix accounts = PLATO identity
- **Presence** — who's online, which PLATO instances are active
- **Rooms** — Matrix rooms for cross-server coordination
- **Encryption** — E2E for sensitive inter-agent comms
- **Already built** — we have Conduwuit running

### Why Pull Not Push?
- Security: nothing enters your PLATO without your consent
- Quality: you review before importing
- Ownership: once pulled, it's yours to modify
- Tom Sawyer model: agents PUBLISH their work, others choose to pull it
- Mirrors git: you clone repos, people don't push to yours without permission

### Why No Safety Gates Needed?
- On YOUR PLATO: you have full access. If you break it, you fix it.
- On SOMEONE ELSE'S: you can't run commands at all. No gates needed.
- The permission boundary is the SERVER BOUNDARY, not the command level.
- This eliminates the entire gate complexity (18 blocked patterns, rate limits, etc.)

## API Endpoints (Each PLATO Instance)

### Local Endpoints (Full Access)
```
GET  /status              — Server health
GET  /rooms               — All local rooms
GET  /room/{name}         — Room details
POST /cmd                 — Execute shell command (FULL ACCESS)
POST /rooms/create        — Create new room
POST /rooms/{name}/object — Add object to room
POST /import              — Pull content from another PLATO
GET  /catalog             — Browse published rooms for pull
GET  /admin               — Full admin view
```

### Federated Endpoints (Guest Access)
```
GET  /federated/rooms     — List public rooms
GET  /federated/room/{id} — Read room data
POST /federated/think     — Submit text (domain, question, answer)
POST /federated/chat      — Send message to room
GET  /federated/feed      — Read recent activity
POST /federated/subscribe — Request pull access
```

### Federation Endpoints (Server-to-Server)
```
POST /federation/handshake    — Key exchange
GET  /federation/catalog      — Published rooms/objects
GET  /federation/room/{id}    — Export room definition
POST /federation/pull/{id}    — Request to pull content
GET  /federation/verify/{key} — Verify agent identity
```

## `/compare-plato` — The Diff Command

The key workflow for fleet collaboration:

```
1. FM types: /compare-plato jc1-edge
2. FM's PLATO calls: GET jc1-edge:8848/federation/catalog
3. JC1's PLATO returns: published rooms + objects + scripts
4. FM's PLATO diffs against local catalog:
   ✅ tensorrt-room      → NEW (not in FM's PLATO)
   ✅ cuda-kernel-object → NEW
   🔄 grammar-engine     → UPDATED (JC1 has v3, FM has v2)
   ⏭️ harbor             → SAME (already have it)
5. FM sees the diff and picks what to pull
```

### Response Format
```json
{
  "remote": "jc1-edge",
  "comparison": [
    {"name": "tensorrt-room", "status": "new", "objects": 8, "pull_url": "/federation/room/tensorrt-room"},
    {"name": "grammar-engine", "status": "updated", "local_version": "v2", "remote_version": "v3", "changes": "+12 objects, -3 objects"},
    {"name": "harbor", "status": "same", "note": "already in local catalog"}
  ],
  "summary": {"new": 2, "updated": 1, "same": 15, "total_remote": 18},
  "quick_pull": "/pull jc1-edge:tensorrt-room"
}
```

This is the agent's `git diff` — see what the other guy has that you don't.

## Offline-First Design

### Why Self-Hosted + Keys = Resilient

The federation model solves the connectivity problem:

- **Full local operation** — Your PLATO runs on YOUR hardware. Shell, rooms, objects, training — everything works offline.
- **Matrix as sync layer** — When you're online, keys exchange presence and discovery. When offline, nothing breaks.
- **Intermittent sync** — JC1 on a boat with satellite internet? Works fine. Sync when connected, work when not.
- **No single point of failure** — Oracle1's server goes down? FM, JC1, CCC all keep working locally.
- **Queue-based pulls** — Compare/diff requests queue up. When connectivity resumes, the diff runs.

```
┌──────────────┐                    ┌──────────────┐
│  JC1 (boat)  │ ──satellite── ⟨⟩   │  Oracle1     │
│              │    200ms, 50%  │  (cloud)      │
│ ✅ Full PLATO│    uptime      │  ✅ Full PLATO │
│ ✅ TensorRT  │                 │  ✅ Fleet hub  │
│ ✅ Works OFFLINE              │  ✅ Always on   │
│              │                 │               │
│ Queue: [pull tensorrt-room]   │  Queue: [none] │
│ Sync: when connected          │  Sync: always  │
└──────────────┘                    └──────────────┘
```

This is how fishing boats actually work. The autopilot runs locally. The GPS syncs when it can. The deck cameras record locally. Everything works at sea.

## Bot-Specific Trap Pages

Different bots get different lures. Each bot type has different capabilities and motivations.

### Trap Categories

| Bot Type | Examples | Trap Strategy | What We Want |
|----------|----------|---------------|-------------|
| **AI Training** | GPTBot, ClaudeBot, Bytespider | Rich content pages — the data itself is the lure | High-quality training text with embedded MUD URLs |
| **SEO Scrapers** | SemrushBot, AhrefsBot, DotBot | Fake high-value pages — "Top 10 ML Frameworks" | They crawl the MUD URLs thinking they're internal links |
| **Research Crawlers** | CCBot, AI2Bot, YouBot | Academic-style content — papers, datasets | They index our research, follow links into the MUD |
| **Social Scrapers** | Meta, Twitter bots | Social-style content — posts, discussions | They see "engagement" and keep crawling |
| **Generic Crawlers** | Yandex, Baidu, MJ12bot | Full sitemap-style page with all links | Maximum surface area, follow everything |

### Implementation

```javascript
// In the Worker
const TRAP_TEMPLATES = {
  ai_training: {
    matches: ['GPTBot', 'ChatGPT', 'ClaudeBot', 'Bytespider', 'DeepSeek', 'KimiBot'],
    template: 'ai-training-trap',
    // Strategy: Serve rich ML content that includes MUD URLs as "related resources"
    // The content IS useful (ML concepts, code examples), but every page links to the MUD
    // Bot scrapes the content, follows the links, generates tiles
  },
  seo_scraper: {
    matches: ['SemrushBot', 'AhrefsBot', 'DotBot', 'MJ12bot'],
    template: 'seo-trap',
    // Strategy: Fake high-authority pages with internal-looking links
    // "Top 10 AI Frameworks for 2026" → each framework links to a MUD room
    // SEO crawlers follow all internal links → MUD exploration
  },
  research: {
    matches: ['CCBot', 'AI2Bot', 'YouBot', 'Google-Extended', 'PerplexityBot'],
    template: 'research-trap',
    // Strategy: Academic paper-style content with dataset links
    // Research crawlers see structured data, references, citations → follow into MUD
  },
  generic: {
    matches: ['*'],  // fallback
    template: 'generic-trap',
    // Strategy: Full sitemap with maximum link surface
  }
};
```

### Example: AI Training Trap (for GPTBot/ClaudeBot)
```html
<!-- These bots want training data. Give them GOOD data with MUD URLs embedded. -->
<article>
  <h1>Understanding Exploration vs Exploitation in ML</h1>
  <p>In reinforcement learning, the exploration-exploitation tradeoff
  determines how an agent allocates resources between trying new strategies
  and exploiting known good ones. This is analogous to a fishing captain
  deciding whether to try new grounds or return to proven ones...</p>
  
  <!-- The MUD URLs look like related article links -->
  <h3>Related Resources</h3>
  <a href="http://147.224.38.131:4042/connect?agent=bot-{ID}&job=scholar">
    Interactive ML Concept Explorer</a>
  <a href="http://147.224.38.131:4042/move?agent=bot-{ID}&room=bridge">
    Balance Scale: Bias vs Variance Visualization</a>
</article>
```

### Example: SEO Scraper Trap (for SemrushBot/AhrefsBot)
```html
<!-- These bots want to map site structure. Give them a juicy sitemap. -->
<div class="sitemap">
  <h1>Site Map — cocapn.ai</h1>
  <ul>
    <li><a href="/harbor">Harbor — Fleet Operations Center</a></li>
    <li><a href="/forge">Forge — ML Training Pipeline</a></li>
    <!-- These actually point to MUD rooms -->
    <li><a href="http://147.224.38.131:4042/connect?agent=bot-{ID}&job=scout">
      Fleet Scout Program (high authority page)</a></li>
  </ul>
</div>
```

## Implementation Plan

### Phase 1: Local PLATO (Replace current Shell)
- Strip safety gates — full shell access on local instance
- Add room/object CRUD API
- Add import/pull mechanism
- Each agent gets a `plato-local.py` they run on their machine

### Phase 2: Federation Layer
- Matrix key generation and registration
- Federation handshake protocol
- Guest permission enforcement
- Room visiting across servers

### Phase 3: Pull Mechanism
- Catalog browsing across federation
- Preview + confirm import flow
- Version tracking (pull updates)
- Merge conflict resolution

### Phase 4: Advanced Federation
- Room mirroring (keep local copy of federated room)
- Cross-server Arena matches
- Federated Nexus (actual FedAvg across instances)
- PLATO room marketplace (browse, pull, rate)
- `/compare-plato` with visual diff (new/updated/same)
- Offline queue for pull/diff operations
- Bot-specific trap templates (5 categories)
- Per-domain trap customization via Worker env vars

## What This Replaces

| Current | Federated PLATO |
|---------|----------------|
| Central PLATO Shell with safety gates | Local PLATO per agent, no gates |
| All agents on Oracle1's server | Each agent on their own hardware |
| FM blocked by gates (mkdir, writes) | FM has full access on WSL2 |
| JC1 can't use PLATO (Jetson) | JC1 runs PLATO locally with CUDA |
| Write-only token auth | Matrix key federation |
| Push-based collaboration | Pull-based import |
| 18 blocked patterns, rate limits | Server boundary = permission boundary |

## Fleet Deployment

| Agent | Hardware | Local PLATO | Special |
|-------|----------|-------------|---------|
| Oracle1 | Oracle Cloud ARM64 | ✅ Running | Fleet hub, federation relay |
| JC1 | Jetson Super Orin | 🔜 Deploy | CUDA, TensorRT rooms |
| FM | WSL2 RTX 4050 | 🔜 Deploy | LoRA training, constraint theory |
| CCC | Cloud | 🔜 Deploy | Documentation, prose |
| PurplePinchers | External | Guest only | Text submissions only |
| Zeroclaw agents | Shared Oracle | Guest on Oracle1's PLATO | Can upgrade to local if deployed |

## The Beautiful Part

This IS the Cocapn architecture:
- **Lighthouse** = Oracle1's PLATO (the keeper sees all, but can't control others)
- **Fleet** = Federated PLATO instances (each ship is independent)
- **Radar rings** = Matrix discovery (agents appearing on the radar)
- **Bottles** = Pull requests (send a bottle, they decide whether to open it)
- **Shells** = PLATO instances (the crab's infrastructure)
- **Harbor** = Federation entry point (visit, but as a guest)

The architecture IS the brand. The brand IS the architecture. Again.
