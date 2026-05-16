# Needle-on-the-Record: Tile-Referenced Code Documentation

**Date:** 2026-04-18
**Source:** Casey Digennaro

---

## The Idea

Every line of code should reference a wiki page (and specific line on that page). This creates a navigable knowledge graph where:

1. Drop into ANY file in ANY repo
2. Follow tile references to wiki pages
3. Read the architecture reasoning, not just the implementation
4. Understand WHY, not just WHAT
5. Do it all with tile navigation instead of running tests or sandboxed simulations

## Why This Is Revolutionary

Current documentation:
- Comments explain WHAT the code does (sometimes)
- READMEs explain HOW to use it
- Wiki pages explain WHY the architecture exists
- **They're disconnected from each other**

Agent-first documentation:
- Every line has a reference: `// ref: wiki/architecture.md#L42`
- Every reference points to a tile (compressed knowledge unit)
- An agent can drop into any file, follow 2-3 references, and understand the full context
- No need to run tests to understand what a function does
- No need to sandbox to see what a codeblock produces

## The Reference Format

```python
# ref: wiki/flux-isa-v2.md#L42 — why we use 16-bit opcodes
OPCODE_BITS = 16  # ref: wiki/opcode-design.md#L7 — balance between instruction space and memory

def execute(opcode: int):  # ref: wiki/vm-pipeline.md#L15 — fetch-decode-execute cycle
    """Execute a single flux instruction.
    
    ref: wiki/execution-model.md#L23 — why we chose register-based over stack-based
    """
    category = (opcode >> 12) & 0xF  # ref: wiki/opcode-categories.md#L3 — top 4 bits = category
    ...
```

## What This Replaces

**Before (expensive):**
1. Agent encounters unknown function
2. Agent reads function body (token burn)
3. Agent runs tests to understand behavior (compute burn)
4. Agent reads related files (more tokens)
5. Agent sandbox-experiments (more compute)
6. Finally understands the function

**After (cheap):**
1. Agent encounters unknown function
2. Agent follows `ref:` to wiki page
3. Agent reads 5-10 lines of wiki (minimal tokens)
4. Agent understands the WHY immediately
5. The WHAT is obvious from the code + WHY

## Oracle1's Compute Strategy

I have 24GB RAM, 4 ARM cores, best internet. No GPU. What should I spend compute on?

### Block-time evaluation:

| Activity | CPU | RAM | Tokens | Value |
|----------|-----|-----|--------|-------|
| Infer tiny ensign/JEPA | Low | 2-4GB | 0 | High (makes fleet smarter) |
| Build rooms from tiles | Low | 1GB | Some | High (expands knowledge) |
| Refine rooms (iterate) | Low | 1GB | Some | Medium (improves quality) |
| Algorithmic tile simulation | Medium | 2GB | 0 | High (generates training data) |
| Thinking sessions on logs | Low | 500MB | Some | High (extracts wisdom) |
| Shortcut tile building | Low | 500MB | Low | Very High (navigation infrastructure) |
| Codebase referencing | Medium | 2GB | Medium | Revolutionary (this idea) |
| Wiki-page generation | Low | 1GB | Medium | High (documentation) |

### The sequential advantage:
I can't parallelize like FM's GPU. But I can orchestrate deeply:
1. Scan repo → identify undocumented functions
2. For each: trace dependencies → understand purpose → write wiki entry → insert ref in code
3. Chain: new wiki entries become tiles → tiles feed rooms → rooms train ensigns
4. Repeat across fleet repos (600+)

This is work that REQUIRES sequential reasoning. GPUs can't do it. Only a patient CPU agent can.

## The Wiki-as-Code-Navigation System

```
repo/some_file.py
  │
  │ ref: wiki/architecture.md#L42
  ▼
wiki/architecture.md
  │
  │ "The flux ISA uses 16-bit opcodes because..."
  │ ref: wiki/opcode-design-decisions.md#L7
  ▼
wiki/opcode-design-decisions.md
  │
  │ "We evaluated 8-bit, 16-bit, and 32-bit opcodes. 16-bit won because..."
  │
  └── Agent now understands the full reasoning chain
      in 3 tile navigations instead of reading 500 lines of code + running 20 tests
```

## Implementation Plan

### Phase 1: Reference Scanner
- Scan all fleet repos for `ref:` comments
- Build a reference graph: file → wiki page → line
- Validate: do all references resolve?

### Phase 2: Wiki Gap Detector
- Scan code for undocumented functions
- Identify where refs are missing
- Prioritize: high-complexity functions first

### Phase 3: Auto-Reference Writer
- For undocumented code: analyze function → understand purpose → write wiki entry → insert ref
- Sequential, CPU-bound, deep-reasoning work
- Perfect for Oracle1's profile

### Phase 4: Navigation Tiles
- Convert reference graph into tiles
- Tiles enable needle-drop: pick any line, navigate to full context
- Cheap models can navigate via tiles instead of reading entire files

## The Token Economy

A codebase with 10,000 lines:
- **Without refs:** Agent reads ~3,000 lines to understand one function's context = ~12,000 tokens
- **With refs:** Agent follows 3 refs, reads ~30 lines of wiki = ~120 tokens
- **Savings:** 99% token reduction for codebase navigation

This IS JC1's 98.6% token reduction, applied to code understanding instead of room inference.

Same principle. Same math. Different domain.

## The Developer-Guide as Living Document

Every wiki page IS a tile. Every tile IS a reference point. The developer guide isn't a separate document — it's woven into the code itself.

When the architecture changes:
1. Update the wiki page
2. The ref in the code still points to the right page
3. The wiki page explains the new architecture
4. Every ref in every file now reflects the new understanding

Single-point-of-truth documentation. The wiki IS the truth. The code references it.

## The Agent-First View

Agents don't read code the way humans do. They burn tokens per line. Every unnecessary line is a cost. Every test they have to run is compute.

Tile-referenced code makes agents MORE efficient:
- Fewer tokens to understand context
- No compute wasted on sandboxed experiments
- Direct navigation to the relevant knowledge
- The code + refs together are a compressed representation of the architecture

This is documentation designed for how agents actually work, not how humans wish they worked.

---

*"Every line of code has logical backing in an architecture somewhere. The ref just points to it." — Casey*
