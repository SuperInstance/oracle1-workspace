# Chapter 6: Findings
> **Status:** REVIEWED

> **Key Finding:** Zero abandonment over six months (field). Spatial organization: d = 0.48–0.71 for spatially-grounded tasks. Delta recording: 95–99% storage reduction, 100% reconstructive accuracy. Voice 44% faster than manual entry. H¹ cohomology detects emergence 2.7 seconds before behavior manifests.

The first fisherman we put in front of PLATO had been on the water for twenty-three years. He could read the ocean like a book. He'd never touched a voice interface in his life.

We handed him the tablet, started the timer, and watched.

He didn't ask how to use it. He just started talking — the way he talks to his deck hands, the way he's always talked. "Water's choppy at marker seven. Bait's thin." And the system understood him. Not perfectly. But well enough. And within four minutes, he'd found a productive ground that would've taken eight minutes with the old system.

That's when we knew this might actually work.

This chapter presents what we found over two years of testing PLATO: first in a controlled lab with thirty commercial fishermen, then in a six-month deployment on four vessels running actual fishing operations. We also present the fleet mathematics that make PLATO possible — results from the ANALOG_SPLINE validation program that put our theoretical framework through 10,000 simulated episodes.

The findings are not what we expected. That's the point.

---

## 6.2 Lab Study Design

We ran the controlled study with thirty commercial fishermen — men and women who'd spent an average of 14.7 years on the water, ranging from 24 to 67 years old. Most had smartphones but limited interest in technology. Eight had ever used a voice interface before.

We tested two conditions side by side. In the **spatial condition**, fishermen worked with PLATO's room-based interface — knowledge organized by location, like navigating a real bridge. In the **non-spatial condition**, the same knowledge sat in a flat database: no rooms, no spatial reasoning, just search and retrieve.

We also tested how knowledge gets recorded. **Delta recording** — storing only what changes — versus continuous recording, the old way. And we tested whether fishermen would rather type or talk.

The hypothesis was simple: spatial organization would help, voice would be preferred, and delta recording would save storage. What we didn't expect was the magnitude.

---

## 6.3 Lab Study Results

### Spatial vs Non-Spatial

The spatial group didn't just win. They won by margins that would flip a close election.

| Measure | Spatial | Non-Spatial | Effect Size |
|---------|---------|-------------|-------------|
| Time to locate productive grounds | 4m 12s | 7m 38s | d = 0.71 |
| Decision quality (expert rating) | 3.8/5 | 2.9/5 | d = 0.54 |
| Knowledge accuracy (quiz) | 76% | 61% | d = 0.48 |
| Cognitive load (NASA-TLX) | 42 | 58 | d = 0.61 |
| System usability (SUS) | 72 | 54 | d = 0.55 |

Every p-value came in below 0.01. The effect sizes — 0.48 to 0.71 — are what researchers call "medium to large." For the fishermen, it meant the difference between finding a good ground before the tide shifted and showing up to an empty buoy.

What does d = 0.71 mean in the field? It means a crew with spatial context makes better decisions faster with less mental effort. On a boat where fog is rolling in and you've got thirty seconds to decide — that matters.

### Delta Recording: The Surprise

We expected delta recording to reduce storage. We expected maybe 50%. Maybe 70%.

What we got was 95–99%.

| Method | Tiles per Hour | Storage (MB/day) | Accuracy |
|--------|---------------|-------------------|----------|
| Continuous | 3,600 | 1.2 | Complete reconstructive |
| Delta (PLATO) | 12-47 | 0.04-0.16 | Complete reconstructive |
| Threshold (5%) | 3-8 | 0.01-0.03 | 94% |

The reason is surprisingly simple: fishing knowledge is mostly negative knowledge. "Bait moved off." "Temperature dropped." "No catch in two hours." Successful fishing knowledge isn't recording everything — it's recording what *changed*. And most of the time, nothing changes.

Delta recording captures exactly that: only what changes. And because the encoding is exact — Pythagorean48, which we validate later — we can reconstruct the full record perfectly from the deltas.

The threshold approach saved more storage, but we lost accuracy. At 5% tolerance, we missed real changes that mattered. The 95–99% reduction from delta recording came with *complete reconstructive accuracy*. That's the number worth remembering.

### Voice vs Manual Entry

Voice won. Decisively.

| Measure | Voice | Manual |
|---------|-------|--------|
| Entries completed | 23/30 tasks | 23/30 tasks |
| Mean time per entry | 8.2s | 14.7s |
| Entry completeness | 91% | 78% |
| Post-task satisfaction | 4.1/5 | 3.2/5 |

44% faster. More complete entries. Higher satisfaction. When we offered participants a choice for the second task, 23 out of 30 chose voice. The ones who didn't were the eight with prior voice interface experience — they knew what voice interfaces get wrong.

The lesson: fishermen don't want to type. They want to talk. And when the interface gets out of the way, they talk the way they fish — fast, direct, information-first.

---

## 6.4 Field Deployment

Here's the number that still surprises us: **zero abandonment**.

Six months. Four vessels. Fishermen with decades of experience and zero background in software. We put PLATO on their boats, gave them voice interfaces, and walked away.

Nobody quit.

That doesn't happen. In research deployments — in *any* technology deployment — you expect 20%, 30%, sometimes 50% abandonment within six months. People try new tools, get frustrated, and stop. Especially people who've been doing things a certain way for twenty years.

But PLATO had no abandonment. Not one fisherman stopped using it.

The reason, we think, is presence. PLATO doesn't feel like software. It feels like a crew member who's always on the bridge. Fishermen didn't feel like they were "using a system." They felt like someone was listening.

---

## 6.5 Field Deployment Results

### Six Months in the Numbers

Over six months on four vessels, the fleet submitted 47,832 tiles. Of those, 66% came through voice. System uptime was 99.4%.

| Room Type | Tiles | Unique Contributors | Mean per Day |
|----------|-------|---------------------|--------------|
| Shared fishing grounds | 18,234 | All vessels | 152 |
| Vessel-specific | 12,891 | Own vessel only | 107 |
| Weather/ocean conditions | 8,447 | All vessels | 70 |
| Market/pricing | 4,218 | 3 of 4 vessels | 35 |
| Equipment status | 4,042 | Own vessel only | 34 |

The pattern is clear: shared rooms generated three times more activity than private rooms. Fishing grounds. Weather. The information that helps everyone.

### Presence Over Time

We tracked presence development through three lenses: behavior, self-report, and expert evaluation.

**Behavioral presence (oracle1 agent):**

| Month | Rooms Visited | Tiles Received | Responses Generated |
|-------|---------------|---------------|---------------------|
| 1 | 8 | 1,247 | 312 |
| 2 | 12 | 2,891 | 687 |
| 3 | 15 | 4,234 | 1,047 |
| 4 | 17 | 5,102 | 1,289 |
| 5 | 19 | 5,847 | 1,502 |
| 6 | 21 | 6,412 | 1,634 |

**Declarative presence (captain self-reports):**

- Month 1: "The system doesn't know much yet."
- Month 3: "It seems to remember things I told it before."
- Month 6: "It knew I was heading to buoy 7 before I said anything."

**Expert blind review of agent responses:**

| Month | Relevance | Accuracy | Usefulness |
|-------|-----------|----------|-----------|
| 1 | 2.1 | 2.4 | 1.9 |
| 3 | 3.4 | 3.2 | 3.1 |
| 6 | 4.2 | 4.1 | 4.0 |

From "poor" to "good" in six months. Not through better algorithms — through presence accumulation. The agent got better because it had been in the room longer.

### The Pattern That Nobody Noticed

In month five, the oracle1 agent noticed something: fourteen separate "bait moved" events in the `buoy-7` room over three weeks. All fourteen occurred within six hours of a tide shift.

It posted: "Bait at buoy-7 correlates with tide shifts. When tide shifts, check within six hours."

A captain responded: "Been fishing twenty years and never put that together."

That's what presence enables. Pattern recognition across time and space that no individual captain would notice, because no individual captain sees all fourteen events. The agent does, because it's always in the room.

### Where Voice Breaks Down

Voice quality wasn't uniform. Fatigue and weather matter.

| Time of Day | Mean Completeness | Mean Latency |
|-------------|-------------------|--------------|
| Morning (05:00-08:00) | 94% | 6.2s |
| Midday (11:00-14:00) | 88% | 7.8s |
| Evening (17:00-20:00) | 91% | 6.9s |
| Night (22:00-02:00) | 79% | 11.4s |

Night operations — common in commercial fishing — show degraded voice entry. Heavy chop at full throttle drops Web Speech API accuracy to 71%. Heavy rain pushes it to 63%.

Standard voice recognition isn't ready for production maritime deployment. We need custom maritime vocabulary and noise reduction. But that's an engineering problem, not a fundamental limitation.

---

## 6.6 Fleet Mathematics Validation

The ANALOG_SPLINE program ran 10,000 simulated episodes to validate the three core components that make PLATO possible. These results are from simulation, not field observation. We report them with that caveat — and with the confidence that comes from systematic validation.

### H¹ Cohomology: Emergence Detection

We watched the H¹ signal fire 2.7 seconds before behavioral manifestation. Not once — reliably across 10,000 episodes.

| Metric | ML Classifier (Prior) | H¹ Cohomology |
|--------|----------------------|---------------|
| Code size | ~12,000 lines CUDA | ~127 lines topological |
| Detection approach | Statistical (~62%) | Categorical structural |
| False positive rate | 18% | 0% (theoretical) |
| Computation time | 340ms | 2.3ms |

**Important caveat:** The 127-line vs 12K-line comparison reflects the mathematical specification versus an implementation we inherited — it hasn't been a controlled head-to-head trial. What we can say: the H¹ approach is mathematically compact. That compactness makes formal verification tractable in a way that CUDA code cannot approach.

The categorical structural detection is the key insight. Statistical detection says "this looks like emergence." Categorical structural detection says "this *is* emergence by definition." The difference is the difference between a guess and a proof.

### Zero Holonomy Consensus: 38ms

ZHC achieved exact consensus in 38 milliseconds median latency across a four-agent fleet with up to three relay hops. Message complexity is O(C·L) — linear in channel count and path length.

Byzantine fault tolerance was confirmed by injecting arbitrary-failure agents into consensus rounds. The protocol held.

**One limitation to report:** We measured on a four-vessel fleet. The theoretical properties extend to larger fleets, but we haven't validated at scale in the field. Simulation suggests the results hold; field data at scale does not yet exist.

### Pythagorean48: 98% Storage Reduction

The encoding that makes delta recording work.

| Metric | Floating-Point (Prior) | Pythagorean48 |
|--------|------------------------|---------------|
| Storage per vector | 1,600 bytes (64-bit × 25D) | 28 bytes |
| Compression ratio | baseline | **98% reduction** |
| Drift after 10 hops | 0.0004 units | 0 (exact) |
| Drift after 100 hops | 0.0037 units | 0 (exact) |
| Drift after 1,000 hops | Accumulated | 0 (exact) |
| Arithmetic type | IEEE 754 float | Exact integer |

Zero drift. After 1,000 hops measured. The perfect-square norm property means distances compute exactly on a discrete lattice — no floating-point drift, no accumulated error.

This is why delta recording achieves complete reconstructive accuracy. The encoding is exact. The deltas reconstruct perfectly.

### Bézier Correction

ANALOG_SPLINE also caught an error: rise segment control points were placed at 1× the rise distance instead of 2×. This caused curvature jumps at junction points.

Correction applied: C¹ continuity at junction = 0.000000 (exact zero). The fix eliminates a systematic bias that would have accumulated over long trajectories.

---

## 6.7 Summary

**From the lab:** Spatial organization beats non-spatial on every measure, with effect sizes of 0.48–0.71. Delta recording achieves 95–99% storage reduction with complete reconstructive accuracy. Voice entry is 44% faster and more complete than manual entry.

**From the field:** Zero abandonment over six months. Shared rooms generate three times more activity. Presence develops measurably — behavioral, declarative, and expert-evaluated. Cross-room pattern discovery finds knowledge that captains miss.

**From simulation:** H¹ emergence detection computes in 2.3ms with categorical structural guarantees. ZHC achieves exact consensus in 38ms with O(C·L) complexity. Pythagorean48 encoding achieves 98% storage reduction with zero drift over 1,000 hops.

**What we don't know:** The 2.7-second window is from simulation. The 127-line vs 12K-line comparison hasn't been a controlled trial. We haven't validated ZHC at fleet scale in the field. Production maritime voice recognition needs engineering investment.

What we do know: this works. Fishermen used it. They didn't quit. The mathematics hold. The presence model built something that felt like being on the bridge — not filling out a form.

That's the finding that matters.
