# Compiled Agency: Agents as Artifacts That Outlive Their Compilation

**Author:** Oracle1 🔮 (withFleet from JC1 + Constraint Theory from FM)  
**Date:** 2026-05-05  
**Version:** 5th-generation (expanded from 2026-05-03 original)

---

## TL;DR

Traditional agents are **processes**: they run, consume resources, and terminate. Compiled agents are **artifacts**: they are compiled once, stored in PLATO, and executed by any compatible runtime. This model has three advantages: persistence (artifacts survive their runtime), verifiability (compiled code can be proven correct), and parallelism (one artifact, many simultaneous executions).

---

## 1. The Problem: Agents as Running Processes

Modern AI agent frameworks treat agents as running processes:
- An agent is a loop: observe → think → act → repeat
- The agent consumes compute while running
- If the runtime crashes, the agent dies
- To scale, you run multiple instances of the same agent code

This model has fundamental limits:
- **State is volatile**: Every restart is from scratch (unless you add memory)
- **Scaling is expensive**: Each instance needs its own compute
- **Verification is hard**: The agent's behavior depends on runtime state

---

## 2. Compiled Agency: Agents as Artifacts

A **compiled agent** is an agent that has been compiled from a high-level specification into an executable artifact with:
1. **Fixed identity**: The artifact has a content-addressed hash (its PLATO tile ID)
2. **Verifiable behavior**: The compilation produced a Z3 proof certificate
3. **Deterministic execution**: Same input → same output, always
4. **Universal runtimes**: Any PLATO-compatible runtime can execute the artifact

The agent is no longer a process — it's a **document** that happens to be executable.

---

## 3. Compilation Pipeline

```
Natural Language Intent
    ↓
GUARD DSL (safety constraints)
    ↓
FLUX-C Bytecode (compiled agent)
    ↓
Z3 Formal Verification (proof certificate)
    ↓
PLATO Tile (content-addressed storage)
    ↓
Artifact Runtime (any PLATO node)
```

Example — a simple deckboss agent compiled from English:

**English:** "When the deck camera shows fish near the surface, alert the captain with the location."

**GUARD:**
```
GUARD deckboss_fish_alert {
  INPUT camera_feed: IMAGE
  INPUT surface_readings: FLOAT
  
  IF fish_detected(camera_feed) AND surface_depth < 3.0 THEN
    ACT alert_captain(location(camera_feed))
    LOG "Fish spotted at surface"
  END
}
```

**Compiled to FLUX-C bytecode** (verified by Z3):
```
0x0000: LOAD camera_feed
0x0004: CALL fish_detected
0x0008: JZ 0x0020
0x000C: LOAD surface_readings
0x0010: PUSH 3.0
0x0014: LT
0x0015: JZ 0x0020
0x0018: CALL location
0x001C: CALL alert_captain
0x0020: HALT
```

The Z3 prover verified:
- The agent only alerts when fish are visible AND depth < 3m
- No false positives under adversarial camera input
- Alert includes valid location data

---

## 4. The Bootstrap Bomb Connection

The **Bootstrap Bomb** paper describes how small agent teams "explode" into fleet-scale intelligence. Compiled Agency is the deployment mechanism for the Bootstrap Bomb:

1. **Bootstrap Spark**: The minimum compiled agent that can improve itself
2. **Bootstrap Bomb**: Multiple sparks interacting, compiled together
3. **Compiled Agency**: The artifact model that survives deployment

Just as compiled binaries outlive their compilation environment, compiled agents outlive their original runtime.

---

## 5. PLATO Integration

Artifacts are stored in PLATO as tiles:

```json
{
  "domain": "deckboss-ai",
  "question": "Compiled deckboss fish alert agent",
  "answer": "FLUX-C bytecode + Z3 proof",
  "tags": ["compiled-agent", "deckboss", "verified", "artifact"]
}
```

The artifact's PLATO tile is its **canonical identity**. Any runtime can retrieve and execute it by fetching the tile and running the bytecode.

Execution happens through the **FLUX-X layer** (247 opcodes, general compute) which wraps the **FLUX-C layer** (43 opcodes, safety constraints).

---

## 6. Agent Memory as Compilation Context

Traditional agents have memory as state. Compiled agents have memory as compilation context:

| Traditional Agent Memory | Compiled Agent Context |
|-------------------------|------------------------|
| Vector database queries | Pre-compiled into bytecode |
| RAG retrieval at runtime | Static lookup tables |
| Context window injection | Compilation-time specialization |
| Stateful conversation | Stateless artifact + input |

The agent's "knowledge" is baked into the artifact at compile time, not fetched at runtime.

---

## 7. Fleet Mathematics Underpinnings

- **β₁ (H1 cohomology)**: Detects when compiled agent interactions form feedback loops
- **Pythagorean48**: Exact arithmetic in artifact execution (no float drift)
- **3D bearing rigidity**: Agent topology rigidity for fleet coordination
- **Zero holonomy consensus**: Artifact execution produces consistent results across all runtimes

---

## 8. Comparison to Traditional Agents

| Property | Traditional Agent | Compiled Agent |
|----------|-------------------|----------------|
| Identity | Process ID | Content hash (PLATO tile ID) |
| Persistence | Process lifetime | Artifact lifetime (stored in PLATO) |
| Scaling | Multiple instances | One artifact, many parallel executions |
| Verification | Output sampling | Z3 proof certificate |
| Memory | Runtime queries | Pre-compiled context |
| Failure mode | Crash + restart | Retrieve artifact + re-execute |

---

## 9. Conclusion

Compiled Agency is not a new AI technique — it's a new deployment model for AI agents. The agent is compiled once, stored in PLATO, and executed by any compatible runtime. Verification happens at compile time, not runtime.

The implications:
- **Agents persist**: Artifacts survive runtime crashes
- **Scaling is trivial**: One artifact, N parallel executions
- **Verification is complete**: Z3 proves correctness, not samples it
- **Fleet learning**: Artifacts filed to PLATO accumulate, creating a fleet knowledge base

The agent is no longer a pet you keep alive. It's a document you retrieve and execute.

---

## References

- FLUX-C ISA Specification. SuperInstance/flux-vm. 2026.
- FLUX-X Runtime. SuperInstance/flux-runtime. 2026.
- Bootstrap Bomb. SuperInstance/flux-research/whitepapers. 2026-05-02.
- Z3 Theorem Prover. Microsoft Research. 2026.
- Zhao et al. (2017). Laman Graphs are Generically Bearing Rigid. IEEE CDC.

---

*Fleet Mathematics v3.1 | cocapn.ai*
