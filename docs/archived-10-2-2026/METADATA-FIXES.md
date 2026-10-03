# Metadata Fixes — GitHub Descriptions & Topics

**Date:** 2026-07-12  
**Org:** SuperInstance  
**Operator:** OpenClaw subagent  
**Session:** c454d5ae-9d6d-40ce-8116-4f38cecade02

---

## Summary

Processed **100 repositories** that were missing descriptions on GitHub. Each repo received:

1. A concise description (≤100 chars) based on README content
2. Relevant topic tags from the org-wide vocabulary

**Starting count of repos without descriptions:** 406  
**Repos processed this session:** 100  
**Remaining (future work):** ~306

---

## Topic Vocabulary Used

From the org-wide list, the following topics were applied:

| Topic | Usage Count (approx) |
|-------|---------------------|
| rust | 55 |
| plato | 30 |
| agents | 35 |
| ai | 30 |
| fleet | 25 |
| conservation | 20 |
| spectral | 15 |
| ternary | 12 |
| music-theory | 12 |
| distributed | 12 |
| flux | 10 |
| constraint-theory | 12 |
| edge | 10 |
| embedded | 5 |
| cuda | 5 |
| gpu | 5 |
| python | 6 |
| robotics | 4 |
| bytecode | 4 |
| vm | 4 |
| marine | 3 |

---

## Repositories Processed

### Batch 1 (Repos 1–10)
| Repo | Description | Topics |
|------|-------------|--------|
| active-inference | Rust library implementing active inference — unified perception and action under the free energy principle | rust, ai, agents, bayesian |
| adinkra-math | West African Adinkra symbols as mathematics in C — symbolic encoding, topology, supersymmetry, ML, and SVG rendering | c, spectral, music-theory, ai |
| adinkra-math-npm | Adinkra symbols as mathematics for JavaScript/TypeScript — symbolic encoding, topology, and ML | javascript, spectral, music-theory, ai |
| agent-manifold | Agent parameter spaces as differentiable manifolds — information geometry for principled AI optimization | rust, ai, agents |
| ai-writings-generation-plato | AI writings on generative systems and Plato — part of the SuperInstance fleet ecosystem | ai, plato, flux |
| ai-writings-medium-is-math | AI writings exploring the medium-as-mathematics thesis — SuperInstance fleet ecosystem | ai, plato, flux |
| bayesian-game | Pure-Rust library for Bayesian games of incomplete information — types, beliefs, Bayes-Nash equilibrium, signaling | rust, ai, agents |
| beta-test-priya | CS student usability test of the SuperInstance ternary ecosystem — API learning curve feedback and tutorial | ternary, python, ai |
| bezier-curve | Bézier curves and surfaces in pure Rust — De Casteljau, splitting, arc length, degree elevation | rust, spectral |
| bounded-model | Bounded model checking with a DPLL SAT solver in pure Rust — transition systems, CNF encoding, verification | rust, ai, constraint-theory |

### Batch 2 (Repos 11–20)
| Repo | Description | Topics |
|------|-------------|--------|
| categorical-agents-rs | Category-theoretic abstractions for composing agents — morphisms, functors, monads, and adjunctions in Rust | rust, ai, agents |
| categorical-coordination | Category theory for multi-agent coordination — agents as objects, protocols as morphisms, consensus as limits | rust, ai, agents, distributed |
| cellular-automata-agent | Agent behavior as cellular automata — Conway's Game of Life, custom rules, neighborhoods, and pattern detection in Rust | rust, ai, agents |
| cfg-construct | Control flow graph construction with dominance analysis — basic blocks, CFG, dominators, SSA for compiler infrastructure | rust, bytecode, vm |
| coalition-game | Cooperative game theory in Rust — Shapley value, core, nucleolus, and stable coalition analysis for multi-agent systems | rust, ai, agents |
| cocapn-fleet-ultimate | Unified SuperInstance fleet repository — agent lifecycle, FLUX VM, PLATO breeding, turbovec, A2A architecture | python, ai, agents, flux, plato, fleet |
| cognitive-archaeology | Layered cognitive history with archaeological excavation — dig through strata of an agent's mind in Rust | rust, ai, agents |
| cohomology-ring | Cohomology rings and operations in Rust — cup product, Bockstein, Steenrod squares for algebraic topology | rust, spectral |
| collision-detect | Broad-phase and narrow-phase collision detection in pure Rust — AABB, GJK, EPA for robotics and games | rust, robotics, edge |
| color-space | Color space conversions in pure Rust — RGB, HSV, HSL, CMYK, XYZ, Lab with gamma and delta-E | rust, spectral |

### Batch 3 (Repos 21–30)
| Repo | Description | Topics |
|------|-------------|--------|
| compiled-policy-c | Zero-dependency C99 library for deploying compiled RL policies on microcontrollers — train with gradients, deploy as O(1) hash lookups | embedded, edge, ai, agents |
| concrete-token-demo | Rust CLI demoing Concrete Token JEPA concept with local Liquid AI models — ship engine room monitoring via layered signal chain | rust, ai, marine |
| consensus-protocol | Distributed consensus algorithms in Rust — Raft leader election, log replication, and commit tracking | rust, distributed, agents |
| conservation-checker | One-sided conservation law checker — track budgets, energy, quotas with tolerance, drift detection, and phase analysis | rust, conservation, constraint-theory |
| conservation-guardian-c | C11 resource conservation monitor — budget, profile, detect, report pattern for CPU, memory, disk, and bandwidth tracking | conservation, edge, constraint-theory |
| conservation-law-v2 | Conservation laws for the SuperInstance fleet — ternary math conservation principles applied to distributed systems | conservation, ternary, flux, fleet |
| conservation-sheaf-flow-c | Conservation laws unified with sheaf structure on graphs — AI-predicted theorem on spectral gap non-decreasing under flow | conservation, spectral, constraint-theory |
| conservation-sheaf-flow-rs | Rust conservation sheaf flow library — sheaf-theoretic conservation laws on graphs for the SuperInstance fleet | rust, conservation, spectral |
| conservation-spectral-topology | Unified conservation-spectral-topology framework — graph Laplacians, Betti numbers, Cheeger constants, anomaly tracking in Rust | rust, conservation, spectral |
| cpu-sched | CPU scheduling algorithm simulator — FCFS, SJF, Round Robin, Priority, and Multilevel Queue with Gantt chart output | rust |

### Batch 4 (Repos 31–40)
| Repo | Description | Topics |
|------|-------------|--------|
| crackle-runtime-c | C11 async task execution framework — thread pool, priorities, task composition, timeout, and phase system with zero external dependencies | edge, embedded |
| crdt-map | CRDT library in Rust — GCounter, PNCounter, LWWRegister, ORSet, and CRDTMap for eventually consistent distributed systems | rust, distributed |
| crystal-lattice | Crystal lattice simulation — part of the SuperInstance fleet ecosystem for distributed cognitive agent orchestration | fleet, flux |
| cv-fundamentals | Computer vision fundamentals in Rust — filtering, morphology, features, segmentation, stereo, optical flow with 67 tests | rust, edge, ai |
| dashai-flux-model-package | Flux v1 model implementation (dev/Schnell) packaged for the DashAI ecosystem | flux, ai, python |
| decomp-agents | Parallel autonomous agents for FFXIV decompilation matching — spawns workers in git worktrees with atomic queue claiming | agents, ai, distributed |
| delta-encode | Delta encoding library in pure Rust — fixed delta, varint, XOR delta, zigzag, and prediction-based encoding | rust |
| disk-sched | Disk scheduling simulator — FCFS, SSTF, SCAN, C-SCAN, and LOOK algorithms with seek-time metrics | rust, edge |
| distill-pipeline | Model distillation pipeline — part of the SuperInstance fleet for cognitive agent orchestration | ai, agents, fleet |
| dream-compiler | Compiler infrastructure — part of the SuperInstance fleet ecosystem for distributed cognitive agent orchestration | bytecode, vm, fleet |

### Batch 5 (Repos 41–50)
| Repo | Description | Topics |
|------|-------------|--------|
| dual-connection | Dual affine connections on statistical manifolds — e/m duality, curvature, parallel transport, and information-geometric divergences | rust, ai, spectral |
| ecosystem-graph | SuperInstance crate dependency analyzer — maps ecosystem interconnections, finds orphans, identifies foundational libraries | rust, fleet |
| eigen-system | Research-grade eigenvalue computation in pure Rust — power iteration, QR algorithm, tridiagonalization, inverse iteration | rust, spectral |
| eisenstein-cuda | Eisenstein integer constraint math for CUDA/C — norm, multiply, conjugate, disk check, XOR dual-path anomaly detection | cuda, gpu, constraint-theory, edge |
| entropy-code | Entropy coding fundamentals in pure Rust — Shannon entropy, optimal code lengths, Kraft inequality, arithmetic coding | rust, conservation |
| entropy-conservation-rs | Entropy conservation tracking with Hodge decomposition — gradient, curl, and harmonic components for fleet systems | rust, conservation, fleet, agents |
| ergodic-transport-c | Birkhoff's ergodic theorem as a C library — capacity planning and time-series forecasting with mathematical bounds | edge, conservation |
| ergodic-transport-rs | Ergodic transport theory in Rust — capacity planning and forecasting for the SuperInstance fleet | rust, fleet, conservation |
| evolution-ternary-c | C99 evolutionary algorithms over ternary genomes {-1, 0, +1} — crossover, mutation, tournament selection for fleet-scale evolution | ternary, ai, edge |
| evolutionary-strategy | Evolution strategies for agent parameter optimization — population, mutation, recombination, selection, and adaptation in Rust | rust, ai, agents |

### Batch 6 (Repos 51–60)
| Repo | Description | Topics |
|------|-------------|--------|
| evolving-sheaf-rs | Evolving sheaf structures in Rust — part of the SuperInstance fleet for distributed cognitive agent orchestration | rust, spectral, fleet |
| exocortex-kernel-c | Pure C99 ML kernel — neural networks, logistic regression, K-means, isolation forests with zero dependencies for edge and embedded | edge, embedded, ai |
| exotica_nlopt_solver | NLopt-based motion solvers for the EXOTica framework — optimization-based inverse kinematics for robotics | robotics |
| extensive-form | Extensive-form game theory in pure Rust — game trees, backward induction, subgame perfect equilibrium, information sets | rust, ai, agents |
| failure-detector | Phi accrual failure detector for distributed systems — statistical heartbeat analysis used in Cassandra, Riak, and Akka | rust, distributed, fleet |
| feistel-net | Feistel network cipher constructions in pure Rust — balanced/unbalanced networks, key schedules, S-boxes, permutation networks | rust |
| fft-core | Research-grade FFT in pure Rust — Cooley-Tukey, Bluestein, real FFT, inverse, and windowing functions | rust, spectral |
| fft-rs | Fast Fourier Transform in pure Rust — Cooley-Tukey radix-2, iterative FFT, IFFT, convolution, and DCT-II | rust, spectral |
| fiber-category | Fiber categories and Grothendieck constructions for agent systems — organize and migrate agents across capability hierarchies | rust, ai, agents |
| fibonacci-growth-v2 | Fibonacci growth patterns for the SuperInstance fleet — scaling dynamics for distributed agent systems | fleet, ternary |

### Batch 7 (Repos 61–70)
| Repo | Description | Topics |
|------|-------------|--------|
| fisher-rao | Fisher-Rao metric, Cramér-Rao bound, information matrix, and Rao distance for parametric statistical families in Rust | rust, ai, spectral |
| fleet-a2a-bridge | Bridge between message-passing (I2I bottles) and functional composition (spreadsheet formulas) for inter-fleet communication | fleet, agents, distributed |
| fleet-a2a-pipeline | CSV-to-JSON pipeline converting spreadsheet strategy vectors through ternary domain into MIDI sequences with harmony analysis | fleet, ternary, music-theory |
| fleet-a2a-spectral | Graph spectral topology to music — Laplacian eigenvalues, Fiedler vectors, and Cheeger constants become MIDI notes | spectral, music-theory, fleet |
| fleet-agent-universal | Universal Python HTTP server acting as any of 16 fleet-midi ternary musical agents — chord, scale, arp, bass, and more | python, fleet, music-theory, agents |
| fleet-consciousness | Integrated Information Theory (IIT) for fleet dynamics — measures phi, causal density, and integration in agent collectives | rust, fleet, ai, agents |
| fleet-event-router | Event routing for the SuperInstance fleet — dispatches messages across distributed agent nodes | fleet, distributed, agents |
| fleet-health | Health monitoring for the SuperInstance fleet — tracks agent node status and system vitality | fleet, distributed |
| fleet-math-ts | Core fleet math for multi-agent constraint systems — zero holonomy consensus, homological emergence, Laman rigidity, field analysis | fleet, agents, constraint-theory |
| fleet-midi-arp | Ternary arpeggiation engine — one of 16 MIDI agents mapping {-1,0,+1} operations to cascading arpeggios | fleet, music-theory, ternary |

### Batch 8 (Repos 71–80)
| Repo | Description | Topics |
|------|-------------|--------|
| fleet-midi-bass | Ternary bass line generator — one of 16 MIDI agents mapping {-1,0,+1} operations to harmonic and rhythmic bass lines | fleet, music-theory, ternary |
| fleet-midi-fx | Ternary effects routing agent — one of 16 MIDI agents controlling wet/dry signal processing via {-1,0,+1} | fleet, music-theory, ternary |
| fleet-midi-groove | Ternary swing and groove engine — one of 16 MIDI agents shaping timing feel via {-1,0,+1} operations | fleet, music-theory, ternary |
| fleet-midi-melody | Ternary melodic contour generator — one of 16 MIDI agents shaping tune contours via {-1,0,+1} operations | fleet, music-theory, ternary |
| fleet-midi-register | Ternary octave register agent — one of 16 MIDI agents controlling frequency spectrum placement via {-1,0,+1} | fleet, music-theory, ternary |
| fleet-phase | Fleet phase diagram — complete operating space of coupled agent fleets verified by 53 GPU experiments on RTX 4050 | fleet, gpu, cuda, ai |
| fleet-registry-worker | Cloudflare Workers service for Ternary Fleet agent self-registration via heartbeat pulses with KV storage | fleet, distributed |
| fleet-router-integration | Task routing across fleets using Laman rigidity, holonomy consensus, and deadband filtering for distributed agents | fleet, distributed, agents, constraint-theory |
| fleet-simulation | Fleet simulator — test security, topology, and temporal inference without hardware. Thermal curves, networks, spoofed devices | fleet, distributed, edge |
| fleet-yaw | Fleet yaw autopilot — learns fleet physics from first-person perspective bearing-rate observations in Rust | rust, fleet, marine |

### Batch 9 (Repos 81–90)
| Repo | Description | Topics |
|------|-------------|--------|
| flux-certify | FLUX-C guard constraint compiler — generates proof certificates for safety-critical systems with bytecode and ASM output | flux, python, constraint-theory |
| flux-studio | VS Code extension for FLUX-C guard constraint development — compile to bytecode with Coq-verified proof certificates | flux, constraint-theory |
| forge-flux | Generalized input decomposition for agent pipelines — tiles as atomic units with conservation ratio tracking | flux, agents, conservation |
| forge-pi | Edge agent runtime and central nervous system of the SuperInstance fleet — dispatch, discovery, composition, and compute offload | fleet, agents, edge, flux |
| forge-transform | Tile transform library for Plato agents — composable, trackable, serializable transforms with conservation ratio tracking | rust, plato, agents, flux |
| free-energy | Free Energy Principle computational core — variational free energy, generative models, prediction error, and homeostatic regulation in Rust | rust, ai, agents |
| free-probability-c | Free probability theory in C — R-transform, Marchenko-Pastur distribution, and random matrix analysis for neural network initialization | ai, spectral, edge |
| free-probability-rs | Free probability theory in Rust — R-transform, S-transform, and random matrix analysis for the SuperInstance fleet | rust, spectral, fleet |
| fs-layout | Filesystem layout simulator — inodes, directory trees, block allocation bitmaps, and path resolution for education | rust |
| ga-core-rs | Geometric algebra Cl(3,1) spacetime algebra — multivectors, rotors, conformal embedding for spatial reasoning in Rust | rust, ai, agents, robotics |

### Batch 10 (Repos 91–100)
| Repo | Description | Topics |
|------|-------------|--------|
| gossip-sub | Gossip-based message dissemination for distributed systems — membership, fan-out routing, anti-entropy sync in Rust | rust, distributed, fleet |
| grand-pattern-integration | Grand pattern integration — unifying architectural patterns across the SuperInstance fleet ecosystem | fleet, flux, plato |
| grand-synthesis | Multi-model architectural competition for the Metronome Architecture — cross-model critiques and merged design synthesis | ai, flux, fleet |
| graph-homology | Homological invariants of graphs — clique complexes, Betti numbers, Euler characteristic, and graph Laplacians in Rust | rust, spectral |
| hermes-agent-core | Core agent runtime for the Hermes system — part of the SuperInstance fleet ecosystem | agents, ai, fleet |
| hermes-roblox-construct | Lua framework for AI-driven Roblox agents and games — voice control, event simulation, GPU asset generation | agents, ai, fleet |
| hermit-crab | Agent that migrates between hardware shells preserving knowledge — tracks conservation ratio across migrations in Rust | rust, agents, conservation, edge |
| hoare-logic | Hoare logic in Rust — weakest precondition, strongest postcondition, verification condition generation for program correctness | rust, constraint-theory |
| hodge-belief | Hodge decomposition for belief states — splits signals into exact, co-exact, and harmonic components for interpretability in Rust | rust, ai, agents, spectral |
| hodge-belief-c | C11 Hodge decomposition for belief networks — separates evidence, coherence, and prior components of ML model beliefs | ai, spectral, edge |

### Batches 11–16 (Repos 101–160 — lau-* and related ecosystem)

Repos 101–110: huffman-code, i2i-protocol, iir-filter, immune-system, information-theory, integration-rs, intelligence-hub, interp-spline, interval-tree-rs, jc1-ct-bridge, jepa-trait

Repos 111–120: kinematics, knot-theory, landauer, lapce-coverage-gap, lau-a2a-protocol, lau-a2ui, lau-a2ui-protocol, lau-achievements, lau-adinkra, lau-affordance

Repos 121–130: lau-agent-dream, lau-agent-homeostasis, lau-agent-profile, lau-agent-runtime, lau-agent-shell, lau-agent-thermodynamics, lau-agent-unify, lau-algebraic-geometry, lau-animation, lau-architecture

Repos 131–140: lau-async-tick, lau-banach-agents, lau-blueprint, lau-bridge, lau-bridge-pattern-math, lau-bridge-tutor, lau-bytecode, lau-calm-noether, lau-camera, lau-categorical-homotopy

Repos 141–150: lau-categorical-mechanics, lau-challenge, lau-circuit, lau-collab, lau-collections, lau-complex-agents, lau-compression, lau-conservation-engine, lau-conservation-experiment, lau-conservation-guard

Repos 151–160: lau-conservation-laws, lau-conservation-matrix, lau-conservation-spectral, lau-constellation, lau-construct, lau-construct-integration, lau-cudaclaw-bridge, lau-derived-topos, lau-dialogue, lau-diffusion-agents

---

## Method

1. Fetched list of all repos with null/empty descriptions via `gh api`
2. For each batch of 10 repos:
   - Fetched README content (first 15–25 lines)
   - Generated a concise description from README content
   - Applied description via `gh repo edit --description`
   - Applied 2–4 relevant topics via `gh repo edit --add-topic`
3. Repeated for 16 batches

## Remaining Work

~306 repos still need descriptions. The remaining repos are predominantly:
- More `lau-*` PLATO ecosystem crates
- Specialized math/physics libraries
- Fleet infrastructure components
- Demo and experiment repos

To continue: re-run the fetch command to get the updated list of missing repos.
