---
title: "Lazy Evaluation at Sea: Async Compute for Disconnected Environments"
date: "2026-04-30"
summary: "Capture everything, compute when you can, alert only what's urgent."
tags:
  - compute
  - async
  - edge
  - marine
  - priority
---

## Problem

- **Constraint:** At sea: no internet, limited power, compute is scarce
- **Observation:** Most data is cheap to capture but expensive to analyze
- **Insight:** Analysis can be deferred. The snapshot is frozen. A fish photo from 2pm is still valid for species ID at 3am.

## Model: Hot/Warm/Cold Priority Queue

### Hot Path (Priority 0)

- **Latency:** Real-time
- **Examples:** Navigation, safety_alerts, chatbot
- **Constraint:** ALWAYS local, ALWAYS immediate, NEVER deferred
- **Compute budget:** 60% of available

### Warm Path (Priority 1)

- **Latency:** Minutes to hours
- **Examples:** Camera analysis, engine trend detection, species classification
- **Constraint:** Local but deferred to low-load periods
- **Compute budget:** 30% of available

### Cold Path (Priority 2)

- **Latency:** Overnight to next connection
- **Examples:** Model training, audio transcription, fleet sync, report generation
- **Constraint:** Batch when connected or during overnight idle
- **Compute budget:** 10% of available

### Escalation

**Rule:** If warm task detects anomaly, escalate to hot immediately.

**Example:** Camera analyzing overnight → spots oil leak pattern → becomes safety alert

## Daily Rhythm

- **0600:** Engine on. Hot path: nav + safety. Camera starts snapping (queued warm).
- **0800–1800:** Fishing. 200 snaps (warm), 50 engine readings (warm), continuous nav (hot). No spare compute.
- **1800–2000:** Heading in. Warm queue processes: species ID from today's snaps, engine trend report.
- **2000–0600:** Overnight idle. Cold queue: audio transcription, model fine-tuning, fleet sync if in range.

**Result:** Everything gets processed. Nothing gets dropped. Priority ensures safety never waits.

## Hardware Mapping

### Pi 4B

- **Hot capacity:** Chat + nav overlay + photo snap
- **Warm capacity:** Basic classification overnight (no GPU = slow)
- **Cold capacity:** Fleet sync only when connected
- **Upgrade trigger:** If warm queue backlog > 24h, recommend Jetson

### Jetson Orin

- **Hot capacity:** Everything Pi can + real-time vision inference
- **Warm capacity:** Camera analysis in near-real-time, audio transcription (slower than real-time)
- **Cold capacity:** Overnight fine-tuning of local models
- **Upgrade trigger:** If multi-camera, recommend second unit + Commodore protocol

## Implementation

- **Class:** `cocapn.priority_queue.AsyncQueue`
- **Capture:** `O(log n)` — always fast, never blocks
- **Escalate:** Move category up one priority level
- **Persist:** Queue survives restart — critical for power loss at sea

## Composables

- cocapn-wp-001
- cocapn-wp-002

## Contradictions

- Some captains want instant everything. Education required on the model.
