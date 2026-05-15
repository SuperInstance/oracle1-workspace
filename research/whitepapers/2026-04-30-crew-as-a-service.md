---
title: "Crew-as-a-Service: The Hiring Model for Agent Fleets"
date: "2026-04-30"
summary: "You don't buy software. You hire an agent that brings its own gear and improves it on the job."
tags:
  - business
  - agents
  - hardware
  - fleet
---

## Model: Crew-as-a-Service (CaaS)

**Three Package:**

- **Agent:** AI crew member with domain expertise shaped by hardware experience
- **Software:** Tailored to the agent — not generic, not user-configurable
- **Hardware:** Customized by the agent's operational feedback over time

**The Loop:**

1. Hire agent for domain
2. Agent ships with tailored hardware
3. Agent works the season
4. Experience feeds back through git commits
5. Next hardware revision shaped by real operational data

Cycle time: 1 fishing season

## Key Insight

**An agent's value increases with operational time on specific hardware.**

- **Fresh Cocapn:** Worth $75 (Pi cost). Knows nothing about your boat.
- **6-month Cocapn:** Worth $500+. Knows your engine warmup curve, your bilge schedule, your sorting errors.
- **3-year Cocapn:** Priceless. Has trained the next agent. Has redesigned its own hardware.

A greenhorn is liability on day 1. By season 3, they're running the deck. Same agent, same hardware, but the experience is in the repo.

## Resume Model: What Is a Repo?

A resume on file for an agent available for hire.

**Structure:**

- `CHARTER.md` — Statement of intent — what I'm for
- `THOUGHT-PATTERN.md` — Cognitive style — how I think
- `ABSTRACTION.md` — My native abstraction plane
- `tests/` — My references — proven capability
- `commit_history` — My work history — what I've actually done
- `CI_status` — My reliability — do I show up clean

**Query Operations:**

- Find Rust edge agents: `SELECT * FROM fleet WHERE languages ∈ Rust AND plane ∈ {0,1,2} AND hardware_experience IS NOT NULL`
- Find coverage gaps: `fleet.capabilities - job.requirements = missing_hires`
- Compose bid: `RANK agents BY (capability_match * test_coverage * freshness)`

## Talent Agency: Oracle1 as Staffing Algorithm

**Functions:**

- Decompose incoming jobs into capability requirements
- Query fleet for matching agents (set intersection)
- Rank by fit, freshness, test coverage
- Package top candidates as a bid
- Identify coverage gaps → spawn new niche agents

**Set Operations:**

- **Intersection:** Which agents do Rust AND networking AND edge?
- **Complement:** Which domains have no Rust coverage?
- **Partition:** Group all agents by abstraction plane
- **Composition:** What emerges from combining these 3 agents?

## Pricing

- **Pi tier:** $75 — basic second nav + chatbot + memory
- **Jetson tier:** $500 — full Cocapn with local ML, vision, digital twin
- **Thor tier:** Custom — full robotics integration, multi-unit
- **Recurring:** Season updates, fleet learning, hardware evolution

## Composables

- cocapn-wp-001
- cocapn-wp-003

## Contradictions

- Not all domains benefit from hardware specialization. Some agents are purely cloud.
