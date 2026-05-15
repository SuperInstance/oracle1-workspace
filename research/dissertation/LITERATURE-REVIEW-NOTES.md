# Literature Review Notes

## Spatial Cognition in AI

### Brooks (1991) — Intelligence without Representation
- Key claim: intelligence doesn't require symbolic representation, can emerge from environment interaction
- Relevant: PLATO rooms don't represent space, they ARE space (sort of)
- Gap: Brooks' robots were physical, not distributed. What about software agents?

### Situated Cognition (Suchman 1987, Clark 1998)
- Human cognition is fundamentally situated in physical and social context
- Key claim: you can't separate knowing from doing in environment
- Relevant: agents need to be situated in something (rooms) to have knowledge that matters
- Gap: mostly human-focused. How does this apply to AI agents?

### Embodied Cognition
- "We think with our bodies"
- Birds have words for updrafts because they feel updrafts with their bodies
- Agents have rooms because they feel rooms through accumulated change records
- Connection: embodiment through space and time, not just physical form

---

## Distributed Knowledge Systems

### Lamport (1978) — Time, Clocks, and Ordering
- Logical clocks for distributed event ordering
- Key insight: you don't need physical time to know what happened before what
- PLATO tiles have timestamps. But do they need Lamport clocks for ordering?

### CRDTs (Shapiro 2011)
- Conflict-free replicated data types
- Key claim: eventual consistency without coordination
- PLATO rooms are essentially a form of append-only CRDT?
- Delta recording: CRDTs already optimize for this. Connection?

### Wiki and Collective Intelligence
- Wikipedia: distributed knowledge production at scale
- Key lesson: you don't need central authority, you need good structure
- PLATO rooms vs wiki: rooms have spatial context, wikis don't
- Gap: wikis are spatial in metaphor only (articles, links), not in use

---

## Presence and Telepresence

### Slater (1997) — Framework for Immersive Virtual Environments
- "Place illusion" — feeling of being in a virtual space
- "Plausibility illusion" — feeling that events in VR are real
- Key claim: presence is about being there, not about understanding
- PLATO application: agents don't need to "feel" present. Captains need agents to feel present.
- Research question: can a software agent feel "present" to a human?

### Lombard & Ditton (1997) — Presence Taxonomy
- Six dimensions of presence
- PLATO addresses: social richness, immediacy, isolation
- Future research: can software agents create presence without physical embodiment?

---

## Change-Based Recording

### Event Sourcing (Greg Young, ongoing)
- Store events, not state. Current state is derived from events.
- Key claim: the log is the truth. The state is a derived cache.
- PLATO is essentially event sourcing with spatial semantics
- Critical difference: PLATO rooms are named, not just sequential

### Blackerby (1993?) — Observation-Based Recording
- Don't record what IS. Record what CHANGES.
- "There was a world before recording began."
- Already quoted Casey on this. This is central.

### Differential Dataflow
- Only compute on changes, not recompute full state
- PLATO tiles are changes. Rooms are change streams.
- Connection: this is why PLATO scales. You don't process the whole ocean. You process changes.

---

## Maritime Knowledge Systems

### Electronic Navigation (ECDIS)
- Digital chart systems with real-time position
- Lessons: spatial display + real-time data + historical overlay
- PLATO could integrate: buoys, routes, catch history overlaid on charts

### AIS (Automatic Identification System)
- Ships broadcast position, speed, heading continuously
- Every vessel knows where every other vessel is
- PLATO rooms could extend this: what if ships also broadcast "what they're seeing"?

### Fish Stock Monitoring
- NOAA fisheries monitoring programs
- Catch shares, quota tracking, observer programs
- Data exists. It's siloed. PLATO could connect it.

---

## Multi-Agent Systems

### JC1/DCS Laws (JetsonClaw1, 2026)
- Law 101: Above 500 agents, coordination becomes the problem
- Law 102: 12 neighbors max — rigidity threshold
- Law 103: 1.7x latency window for coordination
- Law 104: Scale-invariant coordination rules
- Law 105: Maximum meaning per bit
- Connection: these are the physics of multi-agent systems. PLATO is the medium.

### Constraint Theory (Forgemaster, 2026)
- Rigidity, holonomy, cohomology as mathematical foundations
- H1 = emergence detection
- Zero holonomy = consensus without voting
- Connection: PLATO rooms are constraint spaces. Changes that satisfy constraints propagate.

---

## Key Gaps in Literature

1. **No spatial semantics in distributed AI** — agents work with vectors, not places
2. **No theory of rooms as knowledge containers** — wikis are flat, CRDTs are sequential
3. **No formal treatment of presence vs polling** — "in the room" vs "checked the database"
4. **No maritime-specific AI knowledge systems** — fishing intelligence is ad hoc and siloed
5. **No empirical studies on "ether" hypothesis** — does spatial organization improve agent performance?

---

## Hypotheses to Test

**H1:** Agents with presence in spatially-named rooms outperform agents with flat knowledge access on spatially-grounded tasks.

**H2:** Change-based recording produces more accurate long-term knowledge than state-based recording.

**H3:** Voice-driven spatial knowledge entry (speaking into rooms) produces higher data quality than manual entry.

**H4:** Fishermen with no software experience can effectively use voice-driven room systems in maritime conditions.

