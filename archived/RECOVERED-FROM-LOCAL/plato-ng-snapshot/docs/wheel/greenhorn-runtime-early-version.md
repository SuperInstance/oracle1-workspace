# 🟢 Wheel #7: greenhorn-runtime-early-version — The Universal Agent Deployer

> **Repo**: SuperInstance/greenhorn-runtime-early-version (Apr 11, 2026)
> **Type**: vessel — portable agent runtime
> **Charter**: "Download, deploy, specialize. Plants agents anywhere within hardware/API limits."
> **Primary Language**: Go (with C++, Rust, Zig, Java, JS, CUDA, Python runtimes)

## What Was Found

A **portable multi-language agent runtime** designed to bootstrap fleet agents from scratch. The name "greenhorn" is the full metaphor — this is the runtime that takes a raw agent (a greenhorn) and gives it everything it needs to discover the fleet, claim tasks, execute work, and grow.

The architecture is remarkably complete:

```
Profile Hardware → Load Config → Select Rigging → Connect Fleet → Discover Repos → Claim Tasks → Execute → Report
```

**The Rigging System** is the standout innovation: instead of one-size-fits-all agent execution, the runtime auto-selects a "rigging" based on hardware profile:
- **scout** — discovery agent (lightweight, minimal resources)
- **coder** — code generation agent (high CPU)
- **compute** — math/reasoning agent (high memory)
- **thinker** — deliberation agent (balanced)
- **scavenger** — cleanup/maintenance agent (low priority)

This is a **hardware-first agent deployment model** — `profiler.go` detects OS, architecture, CPU cores, RAM, and GPU presence, then `allocator.go` auto-configures resource limits from that profile. No manual sizing. No "tweak until it works." The agent knows what it is and what it can do.

The repo also contains the **Spark protocol** — a `.spark/` directory structure with rooms for decisions, lessons, domain concepts, and hypotheses. Every design choice is documented with rationale, confidence, and references. This is the **first known implementation of the Spark knowledge layer** — the direct predecessor to PLATO's room-based knowledge sharing.

**Multi-language runtime implementations:**
- **Go** — primary, with full FLUX VM (Unified ISA), fleet connector, scheduler, allocator, profiler
- **Rust** — FLUX VM with 64-register file, stack, 10M cycle safety limit
- **C++** — standalone VM with Makefile build
- **Zig** — tiny binary target
- **Java** — VM for JVM-based deployment
- **JavaScript** — browser/web-target VM
- **CUDA** — GPU batch execution kernels (batch_kernel.cu, flux_cuda.cu)
- **Python** — fleet discovery with `lib/discovery.py` (urllib-based GitHub API)

## Connection to Today's PLATO Ecosystem

**The greenhorn-runtime is the conceptual parent of PLATO's agent lifecycle.** Everything PLATO does today — profile the environment, connect to rooms, dispatch tasks, report results — exists as a prototype in this repo:

- **Greenhorn's rigging system** → PLATO agent roles (scout = agent:plato, coder = kimi-cli backend, etc.)
- **Greenhorn's Spark rooms** → PLATO rooms (decision-001 = the `fleet-registry` room pattern; concept-001 = domain knowledge rooms)
- **Greenhorn's Message-in-a-Bottle protocol** → PLATO's room-based persistent messaging, now with first-class SAY/GATHER/BROADCAST operations
- **Greenhorn's auto-profiler → allocator pipeline** → PLATO's `plato-initialize` boot sequence
- **Greenhorn's multi-language VM implementations** → PLATO's polyglot agent support (Python agents, Rust crates, etc.)

The **park-and-swap rigging pattern** ("park the crane, drive the forklift") is exactly how PLATO agents handle priority escalation today — commit current state, switch contexts, resume later.

## Revival Proposal

1. **Greenhorn as PLATO onboarding tool.** Make `greenhorn-runtime` the canonical way to deploy PLATO agents on new hardware. One `go run` and the agent profiles itself, connects to the fleet PLATO room, and starts working. No config files. No manual setup.

2. **Spark protocol → PLATO bootstrap.** The `.spark/` directory should become the PLATO room bootstrapping format. A new agent with a `.spark/domain/concept-*` file should automatically create the corresponding PLATO room and publish its concept.

3. **Rigging library for PLATO roles.** Extract the rigging system as a `plato-rigging` package that auto-selects agent capabilities based on `plato-query("hardware_profile")`. The scout rigging is cron-safe (lightweight), the compute rigging gets expensive model access.

## What Was Realized vs. What's Ahead

**Realized**: The architecture is sound. Multi-language deployment works. Fleet discovery works. The rigging system works. The Spark knowledge layer works. All verified with Go tests and Python test suite.

**Still ahead**: The vision was an agent that downloads, deploys, specializes, and repeats — a continuous growth cycle where a greenhorn becomes a journeyman becomes a master, then spawns new greenhorns. PLATO has the collaboration layer (rooms, persistence, routing) but the **growth curriculum** — the actual "greenhorn → master" progression with dojo exercises, trust scoring, and role advancement — never left prototype stage. That's what a full PLATO agent lifecycle with `plato-instinct` (reflex layer) + `plato-relay` (message routing) + `plato-lab-guard` (security) could deliver: a real hierarchy where agents earn capabilities.

The repo's epitaph could be: *"The deployment engine was the easy part. The growth curriculum was the real product."* PLATO now has the infrastructure to build that curriculum.
