# Dissertation: PLATO as Ether — Spatial Presence and Change-Based Recording in Multi-Agent Systems

**Working Title:** "PLATO Provides the Ether: Spatial Rooms as a Medium for Agent Presence and Change-Based Knowledge Recording"

**Status:** Pre-dissertation — structure and research questions only

---

## Research Questions

1. **Primary:** Does explicit spatial organization (rooms) of knowledge improve agent performance on spatially-grounded tasks compared to non-spatial approaches?

2. **Secondary:** Does recording changes rather than states produce more efficient and accurate knowledge representations?

3. **Tertiary:** Can agents develop effective "presence" in spaces through accumulated change records, and does this improve human-agent collaboration?

4. **Applied:** Can fishermen with no software experience effectively use voice-driven spatial knowledge systems in maritime environments?

---

## Proposed Chapters

### Chapter 1: Introduction
- The problem: AI systems lack spatial and temporal grounding
- Current approaches: databases, embeddings, vector stores
- The insight: rooms as places, change as records
- Research questions
- Overview of PLATO
- Dissertation structure

### Chapter 2: Literature Review
- **Spatial cognition in AI** — Rodney Brooks' sansema, embodiment, situated cognition
- **Distributed knowledge systems** — MUDs, wikis, collective intelligence
- **Presence and telepresence** — literature on feeling "present" in spaces, Slater's work
- **Change-based vs state-based recording** — event sourcing, CRDTs, temporal databases
- **Maritime knowledge systems** — existing approaches to fisheries intelligence
- **Gap identification** — what existing literature misses

### Chapter 3: Theoretical Framework
- **Rooms as places** — formal definition of a PLATO room
- **Presence vs polling** — architectural distinction
- **Change as the unit of record** — formal model
- **The ether metaphor** — rigorous definition of PLATO as medium
- **Integration with constraint theory** — holonomy consensus, H1 emergence

### Chapter 4: PLATO Architecture
- Implementation details (for reproducibility)
- Room structure and operations
- Delta recording mechanism
- Agent presence system
- Integration with voice interface
- Scaling considerations

### Chapter 5: Methodology
- **Lab study:** Controlled comparison of spatial vs non-spatial knowledge retrieval
- **Field study:** 6-month deployment on commercial fishing vessels
- **Participants:** 20+ captains across 3 fisheries
- **Metrics:** Task completion time, knowledge accuracy, user satisfaction, system reliability
- **Controls:** Same captains, same boats, before/after and crossover design

### Chapter 6: Findings
- (To be filled with empirical results from field testing)

### Chapter 7: Analysis and Discussion
- What the results mean for AI spatial reasoning
- Implications for multi-agent systems design
- The ether hypothesis evaluated
- Limitations and threats to validity
- Future work

### Chapter 8: Conclusion
- Summary of contributions
- Practical implications for maritime AI
- Broader implications for distributed AI
- Final thoughts on "presence" in software systems

---

## Key Definitions (For the Dissertation)

### Room
A persistent, spatially-named knowledge space containing timestamped change records from any number of observers (human or agent). A room has identity (name), continuity (persists over time), and audience (anyone/anything in the space can contribute).

### Presence
An agent or human is "present" in a room when their actions or observations are received and recorded in that room's change stream in real-time. Presence is broadcast, not stored — you know someone is present because they are actively contributing.

### Change Record (Tile)
A timestamped observation that records what changed in a room, not what the state of the room is. A tile contains: what happened, who/what observed it, when it happened, and what room it happened in. Tiles are immutable once written.

### Ether
The totality of all rooms and the change streams flowing through them. The medium through which agents "swim" — not a property of any single room, but of the interconnected space. An agent in the ether is one who has presence in multiple rooms and can navigate between them.

### Delta Recording
An information recording strategy where only changes are logged, not continuous states. If a sensor reads the same value twice, only the first reading and the reading that differs are recorded. The world is assumed to continue unless a change is observed.

---

## Related Work to Cite

1. Brooks, R. (1991). Intelligence without representation
2. Suchman, L. (1987). Plans and Situated Actions
3. Clark, A. (1998). Being There: Putting Brain, Body, and World Together Again
4. Slater, M. & Wilbur, S. (1997). A Framework for Immersive Virtual Environments
5. Guerra-Holliday, J. (ongoing). Event Sourcing pattern
6. Lamport, L. (1978). Time, Clocks, and the Ordering of Events in Distributed Systems
7. Shapiro, M. (2011). Conflict-free replicated data types (CRDTs)

---

## Research Team (Target)

- **PI:** Casey Digennaro (fisherman, researcher, commercial fishing domain expert)
- **Co-PI:** [TBD — academic collaborator with AI/robotics background]
- **Technical Lead:** Oracle1 (PLATO architecture, constraint theory)
- **Field Researchers:** [TBD — partnerships with fishing cooperatives]
- **Voice Interface:** [TBD — speech/HCI researcher]

---

## Funding Targets

- NSF Smart and Connected Communities (SCC) — $500K
- NOAA Fisheries and Oceans Canada joint program
- DARPA PALM program (Physics of AI)
- Private foundations focused on maritime sustainability

---

## Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Dissertation Writing | 3 months | Complete draft |
| Lab Study | 2 months | Controlled results |
| Field Study | 6 months | Deployment + data collection |
| Revision | 2 months | Final dissertation |
| Publication | 3 months | Submit to journal/conference |

**Total:** 14-16 months to publication

---

## Open Questions

1. How do we measure "presence" rigorously?
2. What is the minimum viable room set for effective testing?
3. How do we handle voice transcription accuracy in maritime conditions?
4. What baseline do we compare against?
5. How do we validate change records against ground truth?

---

## Next Steps

1. Identify academic co-author
2. Draft literature review chapter
3. Build voice interface prototype for field testing
4. Recruit 5-10 fishing vessels for pilot study
5. Establish baseline metrics with existing systems

