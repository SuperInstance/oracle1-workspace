# RECOVERED: Local Archive Restore — 2026-05-16

## What is this directory?

This directory contains workspace snapshots and source archives that were stored 
locally on the Oracle1 server (`/tmp/arch-*`) but never pushed to GitHub.

These archives represent the PROCESS of developing the fleet — not just the product.
They contain AI writings, rabbit-trails, session memory, research logs, and full 
source trees that document how the system evolved.

## Directory Structure

```
archived/RECOVERED-FROM-LOCAL/
├── README.md                          # This file
├── RECOVERY-MANIFEST.md               # Detailed manifest of all files
├── workspace-snapshots/               # Full oracle1-workspace archives
│   ├── snapshot-archive-001-2026-04-25/  # Earliest snapshot (2026-04-25)
│   │   ├── AGENTS.md, SOUL.md, USER.md, etc.
│   │   ├── memory/                    # Session logs from April 2026
│   │   ├── docs/rabbit-trails/        # 45 creative exploration documents
│   │   ├── refined/                   # Refined code and insights
│   │   ├── review-feedback/           # Cross-pollination feedback
│   │   ├── config/, scripts/, research/, etc.
│   └── snapshot-archive-002-2026-05-01/  # Later snapshot (2026-05-01)
│       └── (same structure, later state)
├── plato-training-source/              # Full plato-training repo (36 .py files)
├── llms-from-scratch/                 # Full LLMs-from-scratch course (145 .py files)
│   └── ch01-ch07/, appendix-A-E/, reasoning-from-scratch/
└── plato-ng-snapshot/                 # Full plato-ng repo (84 .py files)
    └── core/, services/, docs/, expertise/, games/, rooms/

## Origin of Archives

| Archive | Origin | Date Range | Python Files | Total Size |
|---------|--------|------------|--------------|-------------|
| arch-29 | /tmp/arch-29 | 2026-04-25 | 263 | ~124MB |
| arch-30 | /tmp/arch-30 | 2026-05-01 | 297 | ~126MB |
| arch-78  | /tmp/arch-78 | 2026-04 | 36 | ~696KB |
| arch-170 | /tmp/arch-170 | 2026-05 | 145 | ~25MB |
| arch-png | /tmp/arch-png | 2026-05 | 84 | ~116MB |

## What Each Archive Contains

### workspace-snapshots/ (Process Documentation)
- **memory/**: Daily session logs — what was worked on, decisions made, conversations had
- **docs/rabbit-trails/**: 45 creative exploration documents written by AI during development sessions
  - "The Rust Spine", "Deadband Navigation", "Fleet as City", "Constraint Theory Fleet"
  - These document the AI's creative process, not just the technical output
- **review-feedback/**: Cross-pollination feedback from other agents (CCC, Forgemaster)
- **refined/**: Code and insights that were refined after initial creation
- **config/, scripts/, research/**: Working configuration, tools, and research logs

### plato-training-source/ (Training Infrastructure)
- Full source for PLATO training rooms: micro_room, hardware, types, micro_models
- i2i image-to-image translation, collective training, throttle management
- 9 test files documenting expected behavior

### llms-from-scratch/ (Educational Content)
- 7-chapter LLM course from scratch with Python implementations
- Appendices A-E with supplementary material
- reasoning-from-scratch/ directory

### plato-ng-snapshot/ (Next-Gen PLATO)
- Full source: 84 Python files across core/, services/, expertise/, games/
- conservation_monitor.py, tripartite agents, MUD server, refiner, PRM
- docs/reference/ — ARCHITECTURE-DECISIONS.md, THEORY.md, GLOSSARY.md

## Why These Archives Matter

These archives document the PROCESS of building the fleet — not just the output.
The rabbit-trails are AI-written creative explorations that capture insights
that never made it into commit messages or READMEs.

The memory logs show how the system evolved over time — which approaches were
tried and abandoned, which insights took weeks to arrive at, which breakthroughs
came from AI conversations vs. deliberate design.

This is the moat Casey described: the complete understanding of the abstracted 
process that got us here. Not the product — the journey.

## Recovery Context

Recovered: 2026-05-16
Reason: Oracle1 workspace had local archives that were never pushed to GitHub.
        These were at risk of being lost when /tmp is cleaned.
Action: Copied to archived/RECOVERED-FROM-LOCAL/ in the oracle1-workspace repo
        and pushed to GitHub as a permanent record.

## Git LFS Note

Some files (images, model weights) may be large. Consider using Git LFS:
  git lfs install
  git lfs track "*.png" "*.jpg" "*.pt" "*.bin"
