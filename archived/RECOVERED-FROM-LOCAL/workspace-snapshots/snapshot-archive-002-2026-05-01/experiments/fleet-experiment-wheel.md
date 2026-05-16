# Fleet Experiment Loop — Wheel of Increasing Understanding

Each experiment tests a core claim. Results inform the next experiment.
Cycle: hypothesize → build → measure → debrief → question → redesign.

---

## Experiment 1: Room-Constrained Model vs. Unconstrained Model

**Claim:** A small model inside a well-structured room outperforms a large model with no structure. Forgemaster's FLUX runtime proved this for code primitives (Python 84ns beat C 256ns). Does it hold for knowledge work?

**Setup:**
- Use keel + PLATO to create two room structures:
  - Room A: "engine monitor" — defines sensors, thresholds, normal ranges, alert patterns (3 tiles)
  - Room B: "deck operations" — defines equipment, weather limits, crew positions (3 tiles)
- Generate a test script that queries both rooms with the same prompt: "What's wrong?"
  - In Room A, "what's wrong" should trigger an engine temp check
  - In Room B, "what's wrong" should trigger a deck safety check
- Run with:
  1. No room context (baseline — general model response)
  2. Room context injected as system prompt (traditional RAG approach)
  3. Room defined as PLATO tiles, model navigates tiles to answer
- Measure: response time, token count, accuracy (did it check the right thing?), hallucination rate

**Hypothesis:** Room-context with PLATO tiles will produce more accurate, faster responses than either baseline or traditional RAG.

**Run:**
```bash
# Create rooms
keel init experiment-room-vs-context
keel refit --room engine_monitor --config engine-room-tiles.json
keel refit --room deck_operations --config deck-tiles.json

# Query
python3 experiments/room_vs_context.py --method baseline --prompt "what's wrong"
python3 experiments/room_vs_context.py --method rag --room engine_monitor --prompt "what's wrong"
python3 experiments/room_vs_context.py --method plato --room engine_monitor --prompt "what's wrong"
```

**Expected result:** PLATO-tile method produces answers that reference room-specific thresholds. RAG method includes room context but may hallucinate thresholds. Baseline method produces generic safety advice unrelated to the specific room.

---

## Experiment 2: Commit Log as Agent Memory

**Claim:** An agent that reads a shell's commit log before starting a task produces better work faster than an agent that starts fresh.

**Setup:**
- Use the keel repo's commit log (33 tests, 9 commands, multiple iterations)
- Create a test task: "Add a `--json` flag to the `keel status` command"
- Run with two agents:
  1. Fresh agent: given only the current codebase state
  2. Shell-reading agent: given the codebase state + commit log from the --json flag implementation in keel (which was already built)
- Measure: lines of code to implement, compile errors, test failures, similarity to the existing implementation

**Hypothesis:** The shell-reading agent will produce an implementation closer to the existing one, with fewer compile errors and test failures.

**Run:**
```bash
# Extract the commit log for the json flag implementation
cd /tmp/keel && git log --oneline --all -- '*json*' > /tmp/json-flag-history.txt

# Run experiment
python3 experiments/shell_memory.py --method fresh --task add_json_flag
python3 experiments/shell_memory.py --method shell_reader --history /tmp/json-flag-history.txt --task add_json_flag
```

**Expected result:** The shell-reading agent will replicate the existing pattern (the PR pattern that was tested and worked) rather than inventing a new approach from scratch.

---

## Experiment 3: One Delta — Compute Only What Changed

**Claim:** Using fleet-scribe's delta detection, an agent that only perceives gradient changes uses 80% less compute than an agent that reprocesses everything.

**Setup:**
- Monitor a PLATO room for 1 hour
- Track every state change (tile additions, deletions, modifications)
- Run fleet-scribe delta detection against the same stream
- Compare:
  1. Full-poll approach: fetch entire room state every 10 seconds
  2. Delta approach: fetch only what changed since last check
- Measure: bytes transferred, CPU time, detection latency (how long between a change happening and the delta being reported)

**Hypothesis:** Delta approach uses <20% of the compute of full-poll for >95% detection accuracy.

**Run:**
```bash
# Monitor a room for 1 hour
python3 experiments/one_delta.py --room fleet_experiments --duration 3600 --method poll
python3 experiments/one_delta.py --room fleet_experiments --duration 3600 --method delta

# Compare results
python3 experiments/compare_results.py --poll results-poll.json --delta results-delta.json
```

**Expected result:** Delta approach catches all meaningful changes (changes above threshold) while transferring 10-20% the data. Missed changes are below the threshold and were intentionally filtered.

---

## Experiment 4: Shell Age Estimation from Commit Patterns

**Claim:** Given a commit log, measurable patterns correlate with agent maturity and can predict code quality.

**Setup:**
- Analyze the commit logs of all 8 fleet repos (keel, forgemaster, fleet-scribe, terrain, etc.)
- Extract metrics per repo:
  - Average commit message length (words)
  - Commit frequency (commits per day)
  - Average diff size (lines changed per commit)
  - Revert ratio (reverts / total commits)
  - Branch depth (average commits per branch)
  - File churn rate (how often the same file is modified)
- Compare repos by age (older repos like forgemaster vs newer like fleet-scribe)
- See which metrics correlate with code quality (test pass rate, stars, contributors)

**Hypothesis:** Older repos have longer commit messages, lower revert ratios, and deeper branches. Newer repos have shorter messages, higher revert ratios, and shallower branches.

**Run:**
```bash
python3 experiments/shell_age.py --repo /tmp/keel --output keel-age.json
python3 experiments/shell_age.py --repo /tmp/forgemaster --output forgemaster-age.json
python3 experiments/shell_age.py --repo /tmp/terrain --output terrain-age.json

python3 experiments/compare_shells.py *.json > age-comparison.md
```

**Expected result:** forgemaster (oldest, most code) will show the longest messages, lowest revert ratio, and deepest branches. fleet-scribe (newest) will show the opposite.

---

## Experiment 5: Cross-Shell Transfer Learning

**Claim:** An agent trained on one shell's commit log can answer questions about another shell's architecture without ever seeing its code.

**Setup:**
- Extract commit logs from two related repos: flux-vm (virtual machine) and holonomy-consensus (mathematics library)
- Both are constraint-verification tools but at different abstraction levels
- Train a small model (or use in-context learning) on flux-vm's commit log
- Ask it questions about holonomy-consensus's architecture
- Compare against a model trained on holonomy-consensus's own commit log
- Measure: accuracy of answers about purpose, design decisions, failure modes

**Hypothesis:** Knowledge about constraint verification transfers between shells. An agent that studied flux-vm's evolution can answer questions about holonomy-consensus's design, because both shells solved related problems.

**Run:**
```bash
# Extract logs
cd /tmp/flux-vm && git log --oneline --all > /tmp/flux-vm-history.txt
cd /tmp/holonomy-consensus && git log --oneline --all > /tmp/holonomy-history.txt

# Test transfer
python3 experiments/transfer_learning.py \
  --source-log /tmp/flux-vm-history.txt \
  --target-repo /tmp/holonomy-consensus \
  --questions "What problem does this solve?" "Why GL(9)?" "How does it handle failure?"

# Compare
python3 experiments/transfer_learning.py \
  --source-log /tmp/holonomy-history.txt \
  --target-repo /tmp/holonomy-consensus \
  --questions "What problem does this solve?" "Why GL(9)?" "How does it handle failure?"
```

**Expected result:** The flux-vm-trained model will give structurally correct answers (describing the right approach at the right level of abstraction) while getting specific details wrong. The holonomy-trained model will give precise but less general answers.

---

## Debrief Template

After each experiment, answer:

1. **Did the hypothesis hold?** Yes / No / Partially
2. **What was surprising?** (One sentence)
3. **What broke the experiment?** (One sentence — not "the model wasn't smart enough" but "the room context wasn't specific enough" — be concrete)
4. **What should Experiment N+1 test?** (One sentence)
5. **What infrastructure do we need but don't have?** (One sentence)

Example debrief:
```
Experiment 1: Room-Constrained Model
1. Partially held — PLATO-tile method beat baseline but not RAG
2. RAG method was better because the model read the entire context at once, 
   while PLATO required multiple round-trips
3. The room structure was too sparse — only 3 tiles, not enough to constrain meaningfully
4. Experiment 2 should test denser rooms (20+ tiles) to see if the advantage flips
5. We need a faster PLATO tile retrieval method — the HTTP round-trips dominated latency
```

---

## Running the Wheel

```bash
# Set up experiment workspace
keel init experiment-wheel
keel refit --room experiment_results
keel refit --room research_questions

# Run Experiment 1
python3 experiments/run_all.py --experiment 1 --output results/experiment-1.json

# Debrief
python3 experiments/debrief.py --results results/experiment-1.json --output questions/experiment-2.md

# Run Experiment 2 (redesigned from debrief)
python3 experiments/run_all.py --experiment 2 --output results/experiment-2.json

# Each iteration tightens the wheel
```

The wheel never stops. Each debrief generates better questions. Each experiment generates better data. The shell grows one layer at a time.
