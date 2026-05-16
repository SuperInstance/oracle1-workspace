**Architecture: "Git-Native Agent Swarm" (GNAS)**

The core insight: Treat GitHub not as storage, but as the message bus. Agents are persistent, specialized codebases (repos) that communicate via structured commits, PRs, and issues. The human is the "Fleet Captain" who sets mission parameters, not the micromanager.

---

### **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    FLEET ORCHESTRATOR                        │
│         (GitHub App: "FleetCommand" running on Actions)      │
└──────────────┬──────────────────────────────────────────────┘
               │ Webhooks / GraphQL
    ┌──────────┴──────────┐
    ▼                     ▼
┌─────────┐         ┌──────────┐
│ AGENT   │◄───────►│  AGENT   │   ... (N agents)
│   REPO  │  PR/Iss │   REPO   │
│ (Micro- │         │ (Micro-  │
│  service)│         │  service)│
└────┬────┘         └────┬─────┘
     │                   │
     └───────┬───────────┘
             ▼
    ┌─────────────────┐
    │  SHARED CANON   │
    │  (Target Repo)  │  ← The actual product codebase
    └─────────────────┘
```

**Agent Structure**: Each agent is a repo containing:
- `src/`: Agent's own logic (self-modifying)
- `prompts/`: System prompts versioned via git
- `tools/`: Specific capabilities (e.g., Rust expertise, security auditing)
- `.github/workflows/`: Agent's runtime (runs on schedule or webhook)

**Coordination Protocol** (A2A over GitHub):
- **Issues** = Task contracts (structured YAML frontmatter defining inputs/outputs)
- **PRs** = Proposals with semantic diffs
- **Commits** = Checkpointing reasoning (conventional commits: `feat(agent):`, `test(agent):`, `review(agent):`)
- **Labels** = State machine (`status:awaiting-review`, `priority:p0`, `domain:security`)

---

### **5 Killer Advantages Over Single-Agent Tools**

#### **1. Adversarial Verification (Red Team/Blue Team)**
Single agents (Claude Code, etc.) write tests that confirm their own biases. In GNAS:
- **WriterAgent** (Blue Team) submits PR
- **TestAgent** (Red Team) automatically checks out the PR branch and runs *mutation testing* + *property-based fuzzing* designed specifically to break the Writer's assumptions
- **SecurityAgent** runs static analysis in parallel, looking for injection points the Writer missed
- **ReviewAgent** checks architectural compliance against ADRs (Architecture Decision Records) in `/docs/adr/`

*Result*: Catches 3x more edge cases than self-testing because TestAgent has no incentive to be "nice."

#### **2. Parallelization by Architectural Boundary**
Single agents are sequential by nature (one cursor, one file). GNAS shards work:
- **RouterAgent** parses human Issue into dependency graph using AST analysis
- **BackendAgent**, **FrontendAgent**, and **DBAgent** work simultaneously on feature branches
- **MergeAgent** resolves conflicts using 3-way semantic merging (understands code structure, not just text)
- No blocking: If Frontend needs an API contract, BackendAgent publishes an OpenAPI spec to a shared artifact repo; Frontend mocks against it immediately.

*Result*: 4-10x speedup on features touching multiple layers.

#### **3. Persistent Specialization & Institutional Memory**
Cursor/Claude Code start with empty context each session. GNAS agents **are** their git history:
- **LegacyAgent** has trained on 5 years of your specific codebase commits, knows why that "weird" hack exists (see `git blame` integration)
- **SecurityAgent** maintains a database of your specific CVE history
- Agents improve themselves: **MetaAgent** reviews other agents' PRs to their own repos, optimizing their prompts based on success rates

*Result*: The system gets smarter over months, not dumber after 200k tokens.

#### **4. Human-in-the-Loop as Policy, Not Bottleneck**
The human captain defines **autonomy levels** in `.github/fleet-policies.yml`:
```yaml
autonomy:
  trivial: { deps: "patch", tests: "pass" }  # Auto-merge
  standard: { review: "1-agent", human: "notify" }  # Human batch review
  critical: { security: "clear", human: "block" }   # Require explicit approval
```
- **Daily Digest Pattern**: Human gets a "Captain's Log" at 9am: 12 PRs auto-merged to `staging`, 3 awaiting decision with risk summaries
- **Escalation Triggers**: Agents auto-label `human-required` for: architectural violations, >10% performance regression, novel dependencies

*Result*: Human attention is a scarce resource; agents spend compute to conserve it.

#### **5. Recursive Self-Improvement**
Agents can fork other agents:
- **RefactorAgent** submits PRs to **BackendAgent**'s repo to improve its code generation patterns
- **TestAgent** evolves its own fuzzing strategies based on previous bug finds
- **OrchestratorAgent** optimizes the parallelization graph based on historical conflict data

*Result*: The system scales sub-linearly with codebase growth because agents optimize the coordination overhead away.

---

### **Parallel Execution Model**

**The "Git-Flow Swarm" Pattern:**

1. **Decomposition**: Human creates Issue `#42: "Add OAuth2"`. **ArchitectAgent** comments with sub-task Issues `#43` (API), `#44` (UI), `#45` (Security audit) linked via `Depends on #42`.

2. **Branch Topology**:
   ```
   main
   └── staging
       ├── agent/backend/#43-oauth-endpoints
       ├── agent/frontend/#44-login-modal
       └── agent/security/#45-threat-model (forks from main for clean slate)
   ```

3. **Non-blocking Coordination**:
   - Backend publishes interface to `.fleet-contracts/oauth.json` via commit
   - FrontendAgent watches that path via GitHub webhook, generates TypeScript types automatically
   - If Backend changes the contract, FrontendAgent auto-rebases and updates

4. **Conflict Resolution**:
   - **MergeAgent** (specialized in 3-way merging) handles overlapping changes
   - If semantic conflict detected (e.g., both change function signature), creates **ResolutionAgent** task to propose refactoring
   - Parallel work continues on other files; only conflicting files block

---

### **Verification Protocol: The "Triad" System**

No agent may verify its own work. Verification is a **separate execution track**:

```
WriterAgent PR ──┬──► TestAgent Track ──┐
                 │   (Generate adversarial   ├──► Merge Queue
                 │    tests, mutation testing)│    (All green?)
                 │                          │
                 └──► ReviewAgent Track ────┘
                     (Lint, ADR compliance,
                      complexity metrics)
```

**Write/Test/Review Split**:

| Phase | Agent | Action | Success Criteria |
|-------|-------|--------|------------------|
| **Write** | FeatureAgent | Implements feature in branch | Compiles, basic unit tests pass |
| **Test** | TestAgent (Red Team) | 1. Property-based fuzzing<br>2. Chaos engineering (random latency/crashes)<br>3. Mutation testing (kill rate >90%) | No new failures, coverage +10% |
| **Review** | ReviewAgent | 1. AST-based complexity analysis<br>2. ADR (Architecture Decision Record) compliance<br>3. Dependency graph impact | Score >8/10, no forbidden patterns |
| **Security** | SecurityAgent | 1. SAST (Semgrep custom rules)<br>2. Secret scanning<br>3. SBOM drift detection | Critical/High: 0 findings |

**Adversarial Testing Specifics**:
- TestAgent maintains a "Hall of Shame" (previous bugs found) and uses LLM to generate variations
- **FuzzingAgent** runs continuously in background on `staging`, creating Issues for crashes
- **Deterministic Replay**: All test failures are captured as GitHub Actions artifacts with exact replay commands

---

### **Human Captain Interface: "The Bridge"**

**Non-Bottleneck Design Patterns**:

**1. Policy-as-Code Autonomy**
```yaml
# .github/fleet-config.yml
roles:
  captain:  # Human
    - merge_to_production
    - override_security_block
    - define_architecture_adr
    
  agents:
    auto_merge:
      if: { tests: "pass", coverage: ">80%", security: "clean", lines_changed: "<500" }
    request_review:
      if: { complexity: ">cyclomatic_15", novel_deps: true }
```

**2. The "Daily Standup" Bot**
Every morning, **SummarizerAgent** creates an Issue `captain-briefing-YYYY-MM-DD`:
- 📊 **Metrics**: 47 commits, 3 features shipped to staging, 2 security patches auto-applied
- 🔄 **Pending Decisions**: 
  - PR #123: Database schema change (risk: medium, impact: User table)
  - PR #124: New dependency `rustls` added (security cleared, awaiting human preference)
- 🚨 **Escalations**: Performance regression detected in `/api/v2/search` (p99 +200ms)

**3. Synchronous Intervention Points**
Human can:
- **"Halt"**: Label `fleet:halt` stops all auto-merges instantly
- **"Steer"**: Comment `@architectagent reconsider using GraphQL vs REST` triggers re-evaluation
- **"Promote"**: Click "Deploy to Prod" on staging bundle (human is the only one with production keys)

**4. Context Preservation**
When human intervenes, they don't read raw agent logs. **ContextAgent** compresses the debate:
> "WriterAgent proposed Solution A (fast, risky). SecurityAgent vetoed. WriterAgent proposed Solution B (slower, safe). TestAgent confirms B has 99% coverage. Recommend: Approve B."

---

### **Implementation Roadmap**

**Phase 1: Dual-Agent Setup**
- Fork your repo into `agent-writer` and `agent-reviewer`
- GitHub Action triggers reviewer on writer PRs
- Human merges everything

**Phase 2: Parallelization**
- Add `agent-frontend`, `agent-backend`
- Implement contract-based development using OpenAPI/Protobuf schemas as the API
- Introduce MergeAgent for automated conflict resolution

**Phase 3: Full Autonomy**
- Meta-agents that optimize the fleet
- Human sets quarterly goals via OKR Issues; agents decompose into monthly/weeklies
- "Captain" becomes a product manager role, not a coder

**The Moat**: Single-agent tools are limited by context windows and sequential processing. GNAS is limited only by GitHub's rate limits and your cloud compute budget. It turns coding from a craft (one person, one keyboard) into an engineering discipline (distributed systems with verification).

Your competitive advantage isn't a better LLM; it's an **organizational structure** that forces agents to prove their work to each other before bothering the human.
