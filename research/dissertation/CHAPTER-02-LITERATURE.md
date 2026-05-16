# Chapter 2: Literature Review
> **Status:** REVIEWED

> **Key Finding:** Four fatal traps plague prior approaches: (1) storage without presence, (2) distribution without embodiment, (3) proof without spec completeness, (4) consistency without coherence. PLATO avoids all four. No prior system survives the four-trap test.

The question at the heart of this dissertation is not "how do agents share information?" It is "how do agents know what is happening?" The first has been answered. The second has not.

This chapter reviews four research traditions to identify where each fails. Each contains a fatal trap its practitioners acknowledge but cannot escape within their own terms. The goal is to make PLATO's approach feel inevitable: the necessary response to failures no prior approach survives.

The four traps:

1. **Storage without presence.** Systems that store states know what was said, not what it means. Polling has no grip on context.

2. **Distribution without embodiment.** Multi-agent systems coordinate through message passing with no shared space. Fleet behavior emerges unpredictably.

3. **Proof without spec.** Formal verification proves a system satisfies its specification. It cannot tell you whether the specification is complete.

4. **Consistency without coherence.** CRDTs guarantee replicas converge to the same state, not that the state means the same thing on every replica.

PLATO avoids all four. The chapters that follow show how. This chapter shows why no alternative could.

---

## 2.2 Storage vs Presence

### The Case for Databases, KBMS, and the Semantic Web

Databases are the dominant paradigm for recording what is true. Relational databases (Codd, 1970) brought rigorous theory to data management: normalization, ACID transactions, declarative queries. The Structured Query Language became the lingua franca of data, and SQL databases underpin virtually every significant software system in the world. Object-oriented databases followed, then document stores, graph databases, and time-series databases — each optimized for a class of access patterns. The engineering is mature, the tooling is excellent, and the approach scales.

Knowledge management systems (KBMS) extended the database model to include inference. Rather than storing bare facts, KBMS stores relationships and rules, enabling derivations: if "every vessel requires a permit" and "Capri Sun holds a permit," a KBMS derives that Capri Sun may operate legally. The semantic web (Berners-Lee et al., 2001) pushed this further with RDF, OWL, and SPARQL — global standards for encoding and querying knowledge across organizational boundaries. The vision was a web of data, not just documents, where any agent could traverse links between resources to answer questions no single database could answer alone.

The case is strong. These systems record what was said, by whom, when. They support complex queries, temporal reasoning, and inference over large knowledge bases. Wikidata contains over 100 million statements interlinked by typed relationships. The Gene Ontology encodes biological knowledge used daily by researchers worldwide. These are not toys — they are production systems handling real knowledge at scale.

### The Failure: Storage Knows What Was Said, Not What It Means

A database can store "buoy 7 was 48°F at 6am." It can store "buoy 7 was 45°F at 7am." It cannot store what it means when temperature drops 3°F in an hour.

The temperature drop is not a data point — it is a shift in a pattern that experienced fishermen read as a sign. The bait has moved, or the thermocline has shifted, or a current has brought colder water from depth. Each of these has different implications for where the fish will be. The database stores the facts. It cannot store the reading.

This is not a problem of data quality or query optimization. It is a problem of kind. A database records states. It does not record what those states mean to the people who work in them. "Buoy 7" in a database is a row with an identifier, coordinates, and metadata. "Buoy 7" to a captain who has worked these grounds for twenty years is a place with history — where the current runs fast in a southeast wind, where a specific boulder field holds fish after a cold snap, where another captain once had to cut an anchor line to avoid a grounding. None of that history appears in the database row.

The gap is not missing data. The gap is experiential. Databases record what was observed. They do not record what it felt like to observe it.

The semantic web compounds the problem. RDF triples encode relationships as eternal truths: "buoy-7 hasLocation 41.2°N, 71.0°W." This is the correct location. But the semantic web has no mechanism for "buoy-7 hasReputation 'productive after southeast wind.'" That statement involves time, context, and interpretation. It is not a fact to be asserted — it is a pattern learned through presence. The semantic web encodes timeless truths about things. PLATO records situated observations about places.

The deeper failure is polling. A database does not know what is happening — it waits to be asked. Between polls, the database is blind. A temperature sensor reports every fifteen minutes. The bait moves in between. A captain radios a warning. The database does not hear it. The gap between polling intervals is a gap in presence.

Presence is not about frequency. It is about being there — connected to what is happening as it happens, receiving not just data but context. A present observer knows who said something, in what tone, with what urgency. They know the room.

Polling-based systems have no presence. They record what happened. They do not witness what is becoming.

### PLATO's Response: Rooms as Spatial Presence

PLATO's rooms solve the presence problem. An agent in `buoy-7` receives reports as they arrive, not on a polling schedule. It knows who reported, when, and what the room's history says about similar reports. The room is not a table — it is a space with witnesses and memory.

Storage records state. Rooms record what it means to be here, now, in this place.

---

## 2.3 Distributed AI vs Embodied Cognition

### The Case for Traditional Multi-Agent Systems

Multi-agent systems research (Bond & Gasser, 1988; Wooldridge, 2002) established the theoretical and practical foundations for systems where multiple autonomous agents cooperate, compete, or coordinate toward goals. The approach is natural: decompose a complex problem into specialized agents, each handling a subset of the domain. A planning agent handles route optimization. A monitoring agent tracks sensor data. A communication agent handles inter-agent messaging. The agents are independent processes, often running on different machines, communicating through well-defined protocols.

The advantages are real. Specialization allows each agent to be optimized for its domain. Parallelism allows the system to scale across cores and machines. Distribution allows geographic separation — agents on different vessels can coordinate without a central coordinator. The approach is modular, which supports development and maintenance.

Traditional multi-agent systems treat coordination as a problem of message passing: agents send goals, queries, and replies. The world model is shared or negotiated through protocols like KQML (Finin et al., 1997) or FIPA ACL (FIPA, 2002). Agents maintain local state and update it based on messages received. Coordination emerges from the message protocol.

### The Failure: No Bodies in the World

Agents optimize locally. Each agent has a local objective function — minimize fuel, maximize catch, minimize risk. These local objectives interact. Fleet behavior emerges from the interaction of local optimizations.

Emergence is not prediction. When millions of agents optimize locally, the system-level behavior is difficult to foresee. This is not a failure of implementation — it is a structural feature. Complex adaptive systems exhibit emergence: macro-level patterns that arise from micro-level interactions without being explicitly programmed or even comprehensible from the micro level alone. Traffic jams emerge from individual driving decisions. Market prices emerge from individual trades. Fleet behavior emerges from individual agent optimizations.

No traditional multi-agent system controls emergence. Practitioners acknowledge this. They build monitoring tools to observe fleet-level behavior after the fact. They tune local objective functions to steer emergence toward acceptable outcomes. But there is no formal mechanism to ensure that local optimization produces acceptable fleet behavior.

The deeper failure: agents do not have bodies. Brooks (1991) argued that intelligence does not require symbolic representation — robots navigate through direct interaction with the world, where the world is its own model. Brooks's robots had sensors and actuators. They were embodied.

Software agents have neither. They compute on symbols that refer to a world they do not inhabit. A software agent representing a fishing vessel does not feel the boat pitch in a following sea. It does not taste salt spray. It does not see the color of the water change from blue to green. It receives data — coordinates, speeds, temperatures. It does not experience.

Message passing is not embodied coordination. When two humans coordinate on a boat, they do not just exchange messages — they read each other's posture, anticipate each other's movements, feel the boat's motion together. Embodied cognition (Clark, 1998; Gallagher, 2005) is not just about having a body. It is about knowledge that is structured by and inseparable from having a body in a world. Traditional multi-agent systems have no equivalent.

Fleet coordination requires spatial presence: knowledge of where you are relative to other vessels, how the fleet's geometry is changing, what the formation means in terms of coverage and capability. Message passing provides neither geometry nor presence. Agents know what messages they received. They do not know where they are in the fleet.

### PLATO's Response: Spatial Anchoring and the Ether Hypothesis

PLATO's rooms anchor agents to places, not just to message streams. An agent in `buoy-7` is present at buoy 7. It receives reports from that location. It develops context through presence over time.

The ether hypothesis resolves the embodiment problem differently: agents that share a room share a spatial frame of reference without needing bodies. Geometric consistency — whether the fleet's spatial structure holds — becomes a property of the room, not of individual agent observations.

This is categorically different from message passing. Agents do not just receive information — they occupy space. Fleet coordination requires spatial presence, not just message exchange.

---

## 2.4 Formal Verification vs Empirical Validation

### The Case for Formal Verification

Formal verification uses mathematical proof to establish that a system satisfies its specification. Where testing samples the system's behavior across a set of inputs, verification reasons about all possible inputs. A verified aircraft collision avoidance system cannot fail to maintain separation — not with high probability, not under typical conditions, but ever. The guarantee is mathematical, not statistical.

Interactive theorem provers — Coq (Bertot & Castéran, 2004), Isabelle (Paulson, 1994) — encode systems and properties in formal logic and use machine-checked proofs to verify that properties hold. The human proposes the proof strategy; the prover checks every step. The result is a machine-verified proof that the system satisfies its specification.

The case is compelling for safety-critical systems. CompCert (Leroy, 2006) is a verified C compiler — a compiler written in Coq that is proven to compile C programs without introducing bugs. sel4 (Klein et al., 2009) is a verified operating system kernel — 8,700 lines of C verified in Isabelle to enforce confidentiality and integrity guarantees. These are not proofs of concept. They are production systems deployed in real aircraft and devices.

Formal methods appeal to the engineer's desire for certainty. Testing can only show the presence of bugs, not their absence. A system that passes every test may still fail on the next input. A proof, if sound, eliminates that uncertainty.

### The Failure: Proof Without Complete Specifications

Formal verification proves that a system satisfies its specification. It does not prove that the specification is complete.

This is the gap. A specification enumerates the properties a system must satisfy. Formal verification checks whether the system satisfies those properties. If the specification omits a property — if the engineers failed to anticipate a failure mode — the proof is silent. The verified system will satisfy its incomplete specification perfectly, and fail in the way no one anticipated.

Aircraft maintain separation — verified. But the specification did not include terrain avoidance below minimum safe altitude. The proof is valid. The system is unsafe. sel4's proof covers the kernel's behavior given its API calls. The 400 lines of C that are not proven may contain the vulnerability. CompCert has been revised multiple times because the formal model did not match the compiler's actual behavior on corner cases. These are not failures of the tools — they are acknowledgments that the gap between formal model and real system is real and persistent.

Beyond incompleteness: environments change. The verified system was proven correct for a world where GPS coordinates are stable, sea level is fixed, and "close enough" means a specific distance. In the real world, coordinates drift, sea level rises, and distances mean different things at different scales. A waterproof proof about waterproof equipment is not waterproof if the equipment is used in conditions outside the specification.

The debate between formal verification advocates and empirical validation advocates (He et al., 2018) is often framed as rigor versus pragmatism. But both approaches share a common assumption: that the point is to verify properties about a system. Formal verification verifies properties in a formal model. Empirical validation verifies properties through testing in the real world. Neither addresses the fundamental problem: what properties should you verify?

PLATO's response: structural detection via H¹ cohomology sidesteps the specification problem. Rather than verifying that a system satisfies a property, PLATO detects when the fleet's geometric structure has changed — when a new geometric pattern has emerged. This detection does not require a specification. The H¹ indicator shifts when the shape of the fleet-space changes. The shift is empirical and structural simultaneously.

PLATO does not verify that the fleet maintains a property. It detects when the fleet's structure becomes inconsistent. The question is not "does the system satisfy the specification?" The question is "has something changed in the fleet's geometry?" This is categorically different from both verification and testing. The structure itself is the oracle.

---

## 2.5 CRDT-Based vs Geometric Consensus

### The Case for CRDTs

Conflict-free replicated data types (Shapiro et al., 2011) offer a seductive guarantee: eventual consistency without coordination. CRDT operations are commutative and associative — they can be applied in any order and still produce the same result. Replicas can diverge arbitrarily during network partitions. When the partition heals, all replicas converge to the same state, without any replica needing to wait for another, without any coordinator, without any consensus protocol.

The advantages are significant. No single point of failure. No leader election. No coordination overhead. The system continues to make progress during network partitions. CRDTs are the basis of production systems at Apple (for iCloud document sync), Netflix (for UI state), and SoundCloud (for activity feeds). The approach is mathematically clean and operationally proven.

### The Failure: Convergence Does Not Imply Coherence

CRDTs guarantee that replicas converge to the same state. They do not guarantee that the state means the same thing on every replica.

Consider two captains who independently observe "bait at buoy 7." One captain's "bait" means menhaden — large, oily fish that attract predators. The other captain's "bait" means bunker — a different common name for the same fish. They use the same word for different things. A CRDT storing their observations merges them. The merged state says "bait at buoy 7." The meaning has not been reconciled.

Eventual consistency is consistency about the data structure — about how operations compose. It is not consistency about what the data means. The CRDT mathematical model has nothing to say about whether "bait" on replica A means the same as "bait" on replica B. The merge is correct by construction. The meaning is lost by design.

This is semantic drift. Over time, replicas in a CRDT system can accumulate subtle semantic differences — different interpretations of the same data, different inferred relationships, different conclusions drawn from the same observations. The CRDT model does not detect semantic drift. Converged replicas can mean different things.

A two-captain fleet is manageable. A two-hundred-agent fleet is not. At scale, semantic drift compounds. Agents make local decisions based on local interpretations. Fleet-level behavior diverges from any single agent's view. The CRDT guarantees convergence. It cannot prevent the fleet from fragmenting semantically.

CRDT advocates acknowledge this. They recommend careful design of operation semantics, careful choice of data types, careful training of participants on shared vocabulary. These are good practices. They are not solutions to a structural problem. The CRDT model has no mechanism for detecting or resolving semantic divergence. The mathematics that guarantees convergence does not extend to meaning.

### The Case for Traditional BFT

Traditional Byzantine fault-tolerant systems — PBFT (Castro & Liskov, 1999), Tendermint (Buchman et al., 2017), HotStuff (Abraham et al., 2019) — use the f < n/3 bound as their foundation. The bound is a mathematical theorem: in an asynchronous system with deterministic processes, no consensus protocol can tolerate more than ⌊(n-1)/3⌋ faulty nodes. This is not a design choice. It is a proven impossibility result.

PBFT assumes partial synchrony — the network is usually fast but occasionally slow. It uses three rounds of voting to achieve consensus. With n = 4, f = 1, the bound holds: one Byzantine node cannot forge agreement among the other three. Tendermint uses the same bound with a different voting structure. HotStuff improves the communication complexity but preserves the bound.

The bound is real. It is proven. It applies to the assumed system model. PBFT, Tendermint, and HotStuff implement it correctly. The engineering is sound. The mathematics is correct. For systems in data centers with stable network conditions and well-maintained nodes, these protocols work.

### The Failure: The Bound Is a Theorem, Not a Design Principle

The f < n/3 bound is a property of the system model. It assumes partially synchronous networks, n known at protocol start, and Byzantine failures that conform to the model. Real systems violate these assumptions.

Networks are not always partially synchronous. A fleet operating in remote waters or during electromagnetic interference may face prolonged asynchrony. The bound's guarantees do not hold during asynchrony — PBFT's liveness guarantees depend on synchrony assumptions.

The bound does not distinguish between benign failures and adversarial attacks. A node that fails by halting is equivalent to a node that fails by sending contradictory messages — both count toward the f < n/3 bound. In an adversarial environment, an attacker who compromises one node may compromise more. The bound does not account for correlated failures — the same vulnerability exploited across multiple nodes simultaneously.

The bound does not address semantic failures. An agent that is not Byzantine — that follows the protocol correctly — may still hold a malformed world model. It votes for what it believes is correct. The consensus protocol gathers votes. The result reflects the aggregate of all agents' models. If all agents are locally consistent but globally incoherent, the bound offers no protection.

Most fundamentally: the bound is a mathematical theorem about what is possible given assumptions. It tells you what you cannot do. It does not tell you what to do instead. When the assumptions fail, the bound provides no guidance. PLATO's approach — geometric consensus — addresses a different question: not "how many nodes can fail?" but "is the fleet's structure consistent?" This is categorically different from Byzantine tolerance. ZHC detects geometric inconsistency directly, regardless of the number or nature of misbehaving agents. The detection does not depend on counting failures. It depends on the geometry.

Geometric consensus resolves geometric inconsistency through the same mechanism. The ether hypothesis — that geometric consistency is a structural property of the fleet-space — grounds the approach in physics rather than in assumptions about node behavior.

The bound is a mathematical theorem. It tells you what you cannot do. PLATO does something different: it detects when the fleet-space is geometrically consistent and achieves consensus on that basis.

---

## 2.6 Presence and Telepresence

### Slater on Place Illocation

Mel Slater's presence framework (Slater & Wilbur, 1997) distinguished place illusion — the feeling of being in a virtual place — from plausibility illusion — the feeling that events are real. The framework was developed for virtual reality research, where the goal is to create subjective presence in synthetic environments.

PLATO does not aim to create subjective presence for agents. Agents are software. They do not report feeling present. What PLATO aims for is effective presence: agents that behave as if they were present, responding to context as a present observer would.

### The Difference Between Knowing and Being Present

A database query knows facts. A present observer knows context. The distinction matters because context is not an additional fact — it is a frame. The same fact means different things in different contexts. "Bait at buoy 7" means one thing when the tide is flooding and another when it is ebbing. A present observer knows both the fact and the context. A database knows only the fact.

### Asynchronous Presence

Traditional presence research focuses on synchronous presence — being present at the same time as others. PLATO supports asynchronous presence: a captain who was in `buoy-7` yesterday left observations. The captain arriving today reads them. They are not present simultaneously, but they are present in the same room.

This is presence without synchrony. It is not telepresence in the conventional sense. It is presence through shared space over time — a form of temporal co-presence that does not require simultaneous presence.

---

## 2.7 Change-Based Recording

### Event Sourcing

Event sourcing (Young, 2012) stores events rather than state. The current state is derived by replaying the event log. The approach ensures a complete audit trail and supports temporal queries — what was the state at time T? PLATO extends event sourcing: events are stored in rooms and spatially named. The room provides the spatial context that event sourcing lacks.

### Differential Dataflow

Differential dataflow (McSherry et al., 2013) computes only on changes. The efficiency gains are significant. More importantly, tracking changes more accurately represents the world as experienced: the world does not report its state continuously — it reports changes. PLATO implements differential recording: when a sensor reads the same value twice, only the first reading is stored. The captain does not notice 180°F ten times. They notice when it becomes 185°F.

### There Was a World Before Recording Began

The principle attributed to Blackerby (personal communication): there was a world before recording began. Recording systems do not create the world. They record what changes in it. PLATO is built on this principle. The ocean exists independently. PLATO records what changes — not the ocean as it is, but the ocean as it becomes.

---

## 2.8 Maritime Knowledge Systems

### Electronic Navigation and AIS

Electronic Chart Display and Information Systems (ECDIS) integrate digital charts with real-time positioning and sensor data. The engineering is comprehensive and well-tested. But ECDIS stores state, not experience. It shows where the boat is. It does not show what the captain has seen.

The Automatic Identification System (AIS) broadcasts vessel position, speed, and heading continuously. Every vessel knows where every other vessel is. But AIS provides proximity data without experiential data. A captain knows another vessel is two miles north at eight knots. They do not know whether that vessel has been seeing chum, whether the crew radioed a good catch, whether the skipper mentioned the bait looked thin. AIS knows where boats are. PLATO knows what boats have seen.

### Fisheries Knowledge

NOAA and state agencies collect fisheries data: catch reports, observer data, stock assessments. This data lives in siloed databases, often inaccessible to those who generated it. The knowledge captains accumulate — subtle signs of bait presence, seasonal patterns, relationships between water color and fish location — is largely unrecorded. It lives in captains' heads.

PLATO creates a shared space for this knowledge without becoming a government database or research repository. It is a room where observations accumulate, where corroboration builds trust, where the knowledge that currently lives in individual memories can become collective.

---

## 2.9 The Gap

Each tradition solves part of the problem. None solves the whole.

**Spatial cognition** shows that knowledge is situated but provides no implemented spatial knowledge medium for agents. Brooks's robots were situated through bodies. PLATO's agents are situated through rooms.

**Presence research** gives the vocabulary for "being there" but addresses synchronous human experience, not asynchronous agent presence across a distributed fleet.

**Distributed systems** provide consistency mechanisms but CRDTs provide consistency without spatial semantics, and consistency is not coherence.

**Formal verification** provides mathematical proof but proof requires complete specifications, and experience and context resist specification.

**Event sourcing** shows that the world is best recorded as changes, not states, but event streams lack spatial organization.

**Maritime systems** provide data infrastructure but collect data, not experience.

The gap is architectural: no system combines spatial organization, real-time presence, change-based recording, voice entry, and mathematical grounding in a single design. These are not independent features — each addresses a distinct failure mode. PLATO's design is the minimal response to the specific ways existing systems fail.

---

## 2.10 Summary

Four arguments converge on the same conclusion.

Storage-based systems fail because they record states without presence, providing facts without context. Distributed systems fail because they coordinate without embodiment, optimizing locally while fleet behavior emerges unpredictably. Formal verification fails because proof requires complete specifications, and experience and context resist specification. CRDTs fail because convergence does not imply coherence. Replicas can agree on state while disagreeing on meaning. BFT systems fail because their tolerance bound is a theorem about a model, not an engineering choice, and the model does not match real environments.

PLATO addresses each failure: rooms provide spatial presence; corroboration provides semantic grounding; change recording provides empirical grounding without completeness claims; ZHC + geometric consensus provides fleet-level coherence without depending on bounds that do not apply.

The next chapter develops the theoretical framework that makes this possible.

---

**Keywords:** spatial cognition, situated action, embodied cognition, distributed systems, presence, change recording, maritime AI, CRDTs, event sourcing, formal verification, Byzantine fault tolerance, geometric consensus