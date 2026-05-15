# Research Session: docs

Original size: 60 KB

# FLUX-VECTOR-TABLE-v3.0-SPEC.md
# FLUX Vector Table v3.0 — Agent-Native Operating System Specification

**Status:** Draft for Developer Review  
**Author:** CCC (Fleet I&O Officer), with architectural direction from Fleet  
**Date:** 2026-05-04  
**Version:** 3.0-alpha  
**Replaces:** Tutor-centric ISA v2.x (TELL/ASK/LESSON opcodes)

---

## 1. Design Philosophy

FLUX v3.0 is no longer a tutor engine. It is a **register-based virtual machine** where:
- A "lesson" is just one type of process
- A "database query" is another
- An "API call" is another
- All use the same 14-cycle execution logic

The pedagogical layer (XP, ranks, trials) becomes **one application** running on the FLUX kernel, not the kernel itself.

---

## 2. Binary Header Format

Every `.fluxb` module must begin with a 16-byte header:

```
Offset  Size  Field                Description
------  ----  -------------------  ------------------------------------------------
0x00    3     Magic                "FLX" (0x46 0x4C 0x58)
0x03    1     Version Major        0x03 for v3.0
0x04    1     Version Minor        0x00 for alpha
0x05    1     ABI Revision         Increment on breaking ABI changes
0x06    1     Target Word Size     0x20 (32-bit) or 0x40 (64-bit)
0x07    1     Endianness           0x00 = little, 0x01 = big, 0xFF = runtime detect
0x08    4     Vector Table Offset  Absolute offset to vector table (default: 0x10)
0x0C    4     Manifest Offset      Absolute offset to manifest block (end of file)
```

**Rationale:** The 4-byte [FLX][Version] header prevents v3.0 agents from executing v2.0 tutor bytecode. The endianness flag enables cloud-to-edge SNAPSHOT portability.

---

## 3. The Vector Table (First 64 Bytes)

The Vector Table is a fixed 64-byte structure at the start of every FLUX program. It contains absolute offsets to core system functions. All offsets are relative to the module base.

```
Offset  Size  Symbol                Purpose
------  ----  -------------------  ------------------------------------------------
0x00   

---

# FLUX-GJT-MEMORY-MAP-v3.0.md
# FLUX Global Jump Table Memory Map v3.0

**Companion to:** `CCC-FLUX-VECTOR-TABLE-v3.0-SPEC-2026-05-04.md`  
**Purpose:** Visual reference for developers implementing the FLUX kernel

---

## Overview

The Global Jump Table (GJT) is a 64KB address space (0x0000–0xFFFF) shared across all modules in a FLUX VM instance. It is divided into fixed zones. Each zone has specific access rules, initialization requirements, and hot-swap policies.

---

## Memory Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GLOBAL JUMP TABLE (64KB)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 0x0000 │ Vector Table          │ 16 entries × 4 bytes = 64 bytes            │
│        │ (Reserved System)     │ _VT_INIT, _VT_SIGNAL, _VT_ERROR, _VT_EXIT   │
│        │                       │ _VT_TICK, _VT_GC, _VT_SNAPSHOT, _VT_RESTORE │
│        │                       │ _VT_CAP_ENTER, _VT_CAP_LEAVE                │
│        │                       │ _VT_MODULE_LOAD, _VT_MODULE_UNLOAD          │
│        │                       │ _VT_FORK, _VT_YIELD, _VT_HANDSHAKE          │
│        │                       │ _VT_RESERVED                                │
├────────┼───────────────────────┼──────────────────────────────────────────────┤
│ 0x0010 │ flux:core             │ IO.pulse, IO.poll, IO.poll_nonblk           │
│ 0x003F │ (Core Runtime)        │ IO.stream_open, IO.stream_close             │
│        │ 48 slots              │ IO.stream_push, IO.stream_pull              │
│        │                       │ MEM.copy, MEM.alloc, MEM.free               │
│        │                       │ MEM.barrier, REGION_CREATE, REGION_DESTROY  │
├────────┼───────────────────────┼──────────────────────────────────────────────┤
│ 0x0040 │ flux:sync             │ SYNC.fork, SYNC.yield, SYNC.join            │
│ 0x007F │ (Synchronization)     │ SYNC.barrier, SYNC.handshake               

---

# flux-isa-cheatsheet.md
# FLUX ISA Cheat Sheet

> **Your 30-minute guide to FLUX bytecode programming**

FLUX (Fluid Language Universal eXecution) is a bytecode ISA designed for agent runtimes. Think of it as the "DNA" that runs on the FLUX VM — compact, portable, and agent-aware.

---

## 1. What is FLUX?

### Purpose
FLUX is a **bytecode instruction set architecture** (ISA) for agent-based AI systems. Instead of compiling to x86 machine code, code compiles to FLUX bytecode which runs on the FLUX VM. This makes programs portable across any platform with a FLUX implementation (C, Rust, Zig, Python, JavaScript, WASM, CUDA, etc.).

### What Problems It Solves
| Problem | FLUX Solution |
|---------|---------------|
| Agents need portable code | Bytecode runs everywhere |
| Token overhead of text code | FLUX bytecode is 5-20x smaller than equivalent Python/JS |
| Cross-language agent coordination | Same bytecode, any language runtime |
| Memory-safe execution | Capability-based memory regions |
| Speculative execution | `CLONE`/`ROLLBACK`/`PEEK` for agent experimentation |

### Why It Exists
FLUX was born from building AI agent systems across 11 different language implementations. Each time, teams rewrote the same fetch-decode-execute loop. FLUX standardizes the bytecode format so agent code written once runs everywhere.

---

## 2. Architecture

### Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌───────────────┐     ┌─────────────┐     ┌─────────────┐
│ Source Code  │ ──▶ │   Compiler   │ ──▶ │   Bytecode    │ ──▶ │     VM      │ ──▶ │   Runtime   │
│ (Any Lang)   │     │ (flux-compiler)│    │   (.bin)      │     │ (flux-vm)   │     │  (Result)   │
└──────────────┘     └──────────────┘     └───────────────┘     └─────────────┘     └─────────────┘
     Plane 5             Plane 2            Binary             Interpreter        System State
  (Natural Lang)       (Bytecode)          Format               Loop              (Output)
```

### Mermaid Diagram

```mermaid
flowchart LR
    
