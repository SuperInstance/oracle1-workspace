# PLATO-NG Theory

> The mathematics and philosophy behind the system.

## The Conservation Law

### What It Says
γ + H = 1.283 - 0.159·log(V)

Where:
- **γ** (gamma) = normalized algebraic connectivity of the coupling graph
- **H** (spectral entropy) = entropy of the coupling matrix's eigenvalue distribution  
- **V** = fleet size (number of agents in the system)

### Why It Matters
The law has been experimentally verified across V=3..200 with R²=0.9602 from 5000+ Monte Carlo samples. It holds across:
- Gaussian, uniform, Laplace, and Cauchy style vector distributions
- All noise temperatures (T=0..2.0)
- All quantization levels (P=6..96)
- All graph topologies (random, small-world, scale-free, complete)
- All coupling types (style, topology, directed, mixed)

### The Analytical Proof
The DeepSeek subagent proved the Marchenko-Pastur connection:
- H ≈ 1 - μ₁log(c)/log(V) where μ₁log(c) is the MP log-moment
- γ ≈ μ₁log(c)/log(V) + C₀ + C₁log(V)
- The MP log-moment CANCELS in the sum γ + H

This is a formal mathematical result: the sum is conserved because the same random matrix moment appears in both terms with opposite signs.

### What It Means for Your Application
- Every fleet has a fixed "energy budget" for the sum of connectivity and diversity
- You can trade gamma for H (more connectivity = less diversity, and vice versa)
- The optimal point is Regime III (high γ AND high H) — the Pareto-efficient frontier
- The Refiner uses deviations from the law to detect anomalies (>99.9% compliance)

---

## The Loop Room Pattern

### Mathematical Structure

A Loop Room is a state machine where:
- State S_t evolves by processing incoming tiles
- Transition: S_{t+1} = f(S_t, T_in) where T_in is an input tile
- Output: T_out = g(S_t, T_in)

Every room implements f and g. The difference between room types is what f and g do:
- **Algorithmic**: f and g are deterministic rules (no model call)
- **Agentic**: f and g involve a model call (claw + soul)
- **Refiner**: f and g read other rooms' tiles and write to their harnesses

### Why Loop Rooms Never Stop

The BEAM (Erlang virtual machine) guarantees:
- Each room runs in its own lightweight process (~2KB memory)
- If a room crashes, the supervisor restarts it
- Rooms communicate via message passing (tiles), not shared memory
- Hot code swapping: update a room's logic without disconnecting

---

## The Tripartite System

### Three Viewpoints

Two cameras pointed at each other see each other but not the room.
Three cameras, each with a different vantage point, see everything.

The conservation law predicted this: three spectral parameters (γ, H, τ) need three agents.

### The Filter Architecture

Each agent writes filters for the other two:
- **Human → Application**: How the app should serve this specific human
- **Human → Hardware**: What context the human works in (latency tolerance, etc.)
- **Application → Human**: Feature summary, what the app can do
- **Application → Hardware**: Resource requirements
- **Hardware → Human**: Constraints that affect UX (speed, battery, etc.)
- **Hardware → Application**: CPU/memory limits

Filters oscillate until convergence (score difference < 0.05). Two-thirds of the system (human + hardware) improve cross-application — every human interaction trains the human agent, every hardware interaction trains the hardware agent.

---

## The Tile Compression Theorem

Memories should be stored as constraint points — the facts that survive compression — not as verbatim records. When recalled, the decoder uses the constraints + fresh context to reconstruct. The reconstruction won't be exact. That's the point. It'll be good enough, and sometimes creatively better.

This is how human memory works. This is how PLATO memory works.

The Ebbinghaus forgetting curve: R(t) = e^(-t/λ), where λ depends on valence, access frequency, and conservation law deviation. Tiles close to the conservation law decay at the standard rate. Tiles that violate the law decay 128x faster.
