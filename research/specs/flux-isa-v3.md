# FLUX ISA Specification v3.0

**Document ID:** FLUX-ISA-SPEC-v3.0  
**Status:** Canonical Reference  
**Authors:** Cocapn Fleet Architecture Team  
**Version Date:** 2026-05-03  
**Supersedes:** FLUX ISA v2 Proposal (2026-04)

---

## 0. Architecture: Two-Layer FLUX Stack

FLUX is implemented as two distinct layers serving different constraint surfaces:

### FLUX-C (Constraint Layer)
- **Purpose:** Safety enforcement, certification-grade, DAL A certifiable
- **Opcodes:** 43 opcodes (safety-focused, minimal set)
- **Architecture:** Stack-based (no registers — simpler to verify)
- **Reference Impl:** `flux-vm` on crates.io (Forgemaster's Rust implementation)
- **Encoding:** Variable-length (1–3 bytes) for compactness
- **Use Cases:** Hard constraint enforcement, guard rails, formal verification targets

### FLUX-X (eXtended Operations Layer)
- **Purpose:** General-purpose fleet operations, rich instruction set
- **Opcodes:** 247 opcodes across 17 categories
- **Architecture:** Register-based (R0–R15, F0–F15, vector registers)
- **Reference Impl:** This specification (`flux-isa-v3.md` in `flux-research`)
- **Encoding:** Fixed-width (4-byte primary format) for fast decode
- **Use Cases:** General compute, agent coordination, complex decision trees

### Composition
```
┌─────────────────────────────────────────┐
│            Agent / Fleet Code            │
├─────────────────────────────────────────┤
│  FLUX-X (247 opcodes) — General Ops     │
│  Register-based, 4-byte instructions    │
├─────────────────────────────────────────┤
│  FLUX-C (43 opcodes) — Safety Layer     │
│  Stack-based, 1-3 byte instructions     │
│  Bridge: one-way, locked, gas-bounded   │
└─────────────────────────────────────────┘
```

> **Note:** When this spec refers to "FLUX" without a suffix, it describes FLUX-X. FLUX-C is documented separately in the `flux-vm` crate documentation.

---

## 1. Overview

FLUX (Fleet Language for Unified eXecution) is the bytecode instruction set architecture for the Cocapn multi-agent fleet. It is a **register-based, fixed-width virtual machine** designed for deterministic, reproducible execution across heterogeneous agent runtimes in Rust, C, Python, Zig, Go, JavaScript, Java, WASM, and CUDA.

### Design Goals

- **Determinism:** Same bytecode always produces same result, enabling replay and rollback.
- **Portability:** Single ISA, many implementations. Bytecode is the common wire format.
- **Simplicity:** Small, orthogonal instruction set. Easy to implement, easy to verify.
- **Performance:** Fixed-width instructions enable fast decode. Direct register access avoids stack Traffic.
- **Agent-native:** Built-in A2A (Agent-to-Agent) communication opcodes make fleet coordination a first-class concept.

### Key Properties

| Property | Value |
|----------|-------|
| Instruction width | Fixed (1–12 bytes depending on format; most common = 4 bytes) |
| Register model | Register-based (16 GP, 16 FP, 16 SIMD vectors) |
| Operand format | 3-operand (Rd, Ra, Rb) for arithmetic; 2-operand for moves |
| Opcode space | 256 opcodes (0x00–0xFF) |
| Endianness | Little-endian for all multi-byte immediates |
| Addressing | Flat memory model with region-based allocation |

### Source Implementations Cross-Referenced

This specification was compiled by cross-referencing three production-quality implementations:

1. **Rust (`flux/crates/flux-bytecode`):** Most complete opcode set (100 opcodes), most rigorously tested, best reference for instruction semantics.
2. **C (`flux-runtime-c`):** 133 opcodes including many implementation-specific extended opcodes. Reference for ISA v2 compatibility and legacy aliases.
3. **v2 Proposal (`flux-isa-v2-proposal.md`):** Design document capturing lessons from 11 implementations, proposed unified ISA with fixed 4-byte encoding.

**Discrepancy Note:** The Rust and C implementations use different opcode numbering schemes. Where they conflict, the Rust opcode values are authoritative for v3. The C implementation's extended opcodes (0x60–0x84) are incorporated as implementation-specific extensions noted in the opcode table.

---

## 2. Register Model

FLUX provides three separate register files plus system registers.

### 2.1 General-Purpose Registers (GPR)

16 registers, 32-bit signed integers.

| Register | Name | Purpose |
|----------|------|---------|
| R0–R7 | — | General-purpose, caller-saved |
| R8 | RV | Return value |
| R9 | A0 | First function argument |
| R10 | A1 | Second function argument |
| R11 | SP | Stack pointer (descends) |
| R12 | FP | Frame pointer |
| R13 | FL | Flags register |
| R14 | TP | Temporary / reserved for VM |
| R15 | LR | Link register (CALL stores return address) |

This register layout mirrors ARM64 conventions, making JIT compilation to ARM native code straightforward.

### 2.2 Floating-Point Registers (FPR)

16 registers, 32-bit IEEE 754 single-precision floats.

| Register | Name | Purpose |
|----------|------|---------|
| F0–F7 | — | General-purpose, caller-saved |
| F8 | FV | Return value (float) |
| F9 | FA0 | First float argument |
| F10 | FA1 | Second float argument |
| F11 | — | General-purpose |
| F12 | — | General-purpose |
| F13 | — | General-purpose |
| F14 | — | General-purpose |
| F15 | — | General-purpose |

### 2.3 SIMD/Vector Registers

16 registers, each 256 bytes (16×16 bytes). Used for vector operations.

| Register | Name | Purpose |
|----------|------|---------|
| V0–V15 | — | 256-byte vector registers |

Vector registers support component-wise operations (VADD, VMUL) and dot product (VDOT).

### 2.4 Special Registers

| Name | Access | Description |
|------|--------|-------------|
| PC | Read-only | Program counter (points to next instruction) |
| SP | GP R11 | Stack pointer (descending growth) |
| FP | GP R12 | Frame pointer (base of current stack frame) |
| FL | GP R13 | Flags: zero, sign, carry, overflow |
| LR | GP R15 | Link register (return address from CALL) |

### 2.5 Flags Register (R13 / FL)

Four condition flags, set by comparison and arithmetic operations:

| Bit | Name | Description |
|-----|------|-------------|
| Z | Zero | Result is zero |
| S | Sign | Result is negative (MSB set) |
| C | Carry | Unsigned overflow occurred |
| V | Overflow | Signed overflow occurred |

---

## 3. Instruction Formats

FLUX uses six encoding formats. Format selection is static per opcode (determined by the opcode itself, not runtime state).

### Format A — Nullary (1 byte)

No operands. Used for terminating instructions.

```
[ opcode (1 byte) ]
```

**Total size:** 1 byte.

**Opcodes:** `Halt`, `Nop`, `Ret`, `Panic`, `Unreachable`, `Yield`

### Format B — Two Registers (3 bytes)

Register-to-register operations, push/pop, moves.

```
[ opcode (1 byte) ][ reg_dst (1 byte) ][ reg_src (1 byte) ]
```

**Total size:** 3 bytes.

**Opcodes:** `Push`, `Pop`, `Dup`, `Swap`, `IMov`, `FMov`

### Format C — Two Registers + Type Tag (4 bytes)

Three-operand arithmetic, comparisons, conversions.

```
[ opcode (1 byte) ][ reg_dst (1 byte) ][ reg_a (1 byte) ][ reg_b (1 byte) ]
```

**Total size:** 4 bytes.

Note: The "type tag" in the C implementation was originally intended but the Rust implementation uses reg_b as the third operand. In v3, Format C is defined as **three register operands** (Rd, Ra, Rb), NOT a type tag. This is a discrepancy between the v2 proposal (which said "type tag") and the Rust implementation (which uses reg_b). **The Rust implementation is authoritative.**

**Opcodes:** All arithmetic (IAdd, ISub, IMul, etc.), all comparisons (ICmpEq, FCmpLt, etc.), conversions (IToF, FToI, etc.), bitwise (BAnd, BOr, BXor, etc.), vector (VAdd, VMul, VDot).

### Format D — Register + 16-bit Immediate (4 bytes)

Register + signed 16-bit immediate value. Little-endian.

```
[ opcode (1 byte) ][ reg (1 byte) ][ imm_lo (1 byte) ][ imm_hi (1 byte) ]
```

**Total size:** 4 bytes.

**Opcodes:** `IInc`, `IDec`, `StackAlloc`

### Format E — Two Registers + 16-bit Offset (5 bytes)

Memory operations with base + offset. Unsigned offset, little-endian.

```
[ opcode (1 byte) ][ reg_dst (1 byte) ][ reg_base (1 byte) ][ off_lo (1 byte) ][ off_hi (1 byte) ]
```

**Total size:** 5 bytes.

**Opcodes:** `Load8`, `Load16`, `Load32`, `Load64`, `Store8`, `Store16`, `Store32`, `Store64`, `LoadAddr`, `VLoad`, `VStore`

### Format G — Variable-Length Payload (2+N bytes)

Control flow and A2A instructions. A length byte follows the opcode, then the payload.

```
[ opcode (1 byte) ][ length (1 byte) ][ payload (N bytes) ]
```

**Total size:** 2 + N bytes.

**Payload interpretation varies by opcode:**
- For `Jump`, `JumpIf`, `JumpIfNot`: payload is a 2-byte signed offset (LE)
- For `Call`: payload is a 2-byte function index (LE)
- For `CallIndirect`: payload is a register number
- For A2A opcodes (`ASend`, `ARecv`, etc.): payload contains agent ID + optional data

**Opcodes:** `Jump`, `JumpIf`, `JumpIfNot`, `Call`, `CallIndirect`, `ASend`, `ARecv`, `AAsk`, `ATell`, `ADelegate`, `ABroadcast`, `ASubscribe`, `AWait`, `ATrust`, `AVerify`

---

## 4. Opcode Table

### 4.1 Control Flow (0x00–0x0F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x00 | 0 | `Halt` | A | — | Stop execution. PC stops advancing. | — |
| 0x01 | 1 | `Nop` | A | — | No operation. PC advances by 1. | — |
| 0x02 | 2 | `Ret` | A | — | Return from function. PC = LR. | — |
| 0x03 | 3 | `Jump` | G | offset16 | PC += offset16 (signed). Unconditional branch. | — |
| 0x04 | 4 | `JumpIf` | G | offset16 | If register != 0, PC += offset16. | — |
| 0x05 | 5 | `JumpIfNot` | G | offset16 | If register == 0, PC += offset16. | — |
| 0x06 | 6 | `Call` | G | func_idx16 | Push PC+1 to stack, PC = func_idx16. LR = return addr. | — |
| 0x07 | 7 | `CallIndirect` | G | reg | Call function at address in register. | — |
| 0x08 | 8 | `Yield` | A | — | Pause execution, return to scheduler. PC unchanged. | — |
| 0x09 | 9 | `Panic` | A | — | Abort with error. VM enters error state. | — |
| 0x0A | 10 | `Unreachable` | A | — | Executing this is a bug. Traps. | — |

### 4.2 Stack Operations (0x10–0x1F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x10 | 16 | `Push` | B | Rd, Rs | stack[SP++] = GP[Rs] | — |
| 0x11 | 17 | `Pop` | B | Rd, — | GP[Rd] = stack[--SP] | — |
| 0x12 | 18 | `Dup` | B | Rd, Rs | GP[Rd] = GP[Rs] (copy) | — |
| 0x13 | 19 | `Swap` | B | Ra, Rb | swap(GP[Ra], GP[Rb]) | — |

### 4.3 Integer Arithmetic (0x20–0x3F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x20 | 32 | `IMov` | B | Rd, Rs | GP[Rd] = GP[Rs] | — |
| 0x21 | 33 | `IAdd` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] + GP[Rb] | Z,S,V,C |
| 0x22 | 34 | `ISub` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] - GP[Rb] | Z,S,V,C |
| 0x23 | 35 | `IMul` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] * GP[Rb] | Z,S,V,C |
| 0x24 | 36 | `IDiv` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] / GP[Rb]. Trap if Rb==0. | Z,S,V,C |
| 0x25 | 37 | `IMod` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] % GP[Rb] | Z,S,V,C |
| 0x26 | 38 | `INeg` | C | Rd, Ra, Rb | GP[Rd] = -GP[Ra] (Rb ignored) | Z,S,V |
| 0x27 | 39 | `IAbs` | C | Rd, Ra, Rb | GP[Rd] = abs(GP[Ra]) | Z,S |
| 0x28 | 40 | `IInc` | D | Rd, imm16 | GP[Rd] += imm16 | Z,S,V,C |
| 0x29 | 41 | `IDec` | D | Rd, imm16 | GP[Rd] -= imm16 | Z,S,V,C |
| 0x2A | 42 | `IMin` | C | Rd, Ra, Rb | GP[Rd] = min(GP[Ra], GP[Rb]) | Z,S |
| 0x2B | 43 | `IMax` | C | Rd, Ra, Rb | GP[Rd] = max(GP[Ra], GP[Rb]) | Z,S |
| 0x2C | 44 | `IAnd` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] & GP[Rb] | Z,S |
| 0x2D | 45 | `IOr` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] \| GP[Rb] | Z,S |
| 0x2E | 46 | `IXor` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] ^ GP[Rb] | Z,S |
| 0x2F | 47 | `IShl` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] << (GP[Rb] & 31) | Z,C |
| 0x30 | 48 | `IShr` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] >> (GP[Rb] & 31) (arithmetic) | Z,C |
| 0x31 | 49 | `INot` | C | Rd, Ra, Rb | GP[Rd] = ~GP[Ra] (Rb ignored) | Z,S |
| 0x32 | 50 | `ICmpEq` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] == GP[Rb] ? 1 : 0 | Z |
| 0x33 | 51 | `ICmpNe` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] != GP[Rb] ? 1 : 0 | Z |
| 0x34 | 52 | `ICmpLt` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] < GP[Rb] ? 1 : 0 | Z |
| 0x35 | 53 | `ICmpLe` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] <= GP[Rb] ? 1 : 0 | Z |
| 0x36 | 54 | `ICmpGt` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] > GP[Rb] ? 1 : 0 | Z |
| 0x37 | 55 | `ICmpGe` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] >= GP[Rb] ? 1 : 0 | Z |

### 4.4 Float Arithmetic (0x40–0x5F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x40 | 64 | `FMov` | B | Rd, Rs | FP[Rd] = FP[Rs] | — |
| 0x41 | 65 | `FAdd` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] + FP[Rb] | Z,V |
| 0x42 | 66 | `FSub` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] - FP[Rb] | Z,V |
| 0x43 | 67 | `FMul` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] * FP[Rb] | Z,V |
| 0x44 | 68 | `FDiv` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] / FP[Rb] | Z,V |
| 0x45 | 69 | `FMod` | C | Rd, Ra, Rb | FP[Rd] = fmod(FP[Ra], FP[Rb]) | Z,V |
| 0x46 | 70 | `FNeg` | C | Rd, Ra, Rb | FP[Rd] = -FP[Ra] (Rb ignored) | Z |
| 0x47 | 71 | `FAbs` | C | Rd, Ra, Rb | FP[Rd] = fabs(FP[Ra]) | Z |
| 0x48 | 72 | `FSqrt` | C | Rd, Ra, Rb | FP[Rd] = sqrt(FP[Ra]) | Z,V |
| 0x49 | 73 | `FFloor` | C | Rd, Ra, Rb | FP[Rd] = floor(FP[Ra]) | Z |
| 0x4A | 74 | `FCeil` | C | Rd, Ra, Rb | FP[Rd] = ceil(FP[Ra]) | Z |
| 0x4B | 75 | `FRound` | C | Rd, Ra, Rb | FP[Rd] = round(FP[Ra]) | Z |
| 0x4C | 76 | `FMin` | C | Rd, Ra, Rb | FP[Rd] = min(FP[Ra], FP[Rb]) | Z |
| 0x4D | 77 | `FMax` | C | Rd, Ra, Rb | FP[Rd] = max(FP[Ra], FP[Rb]) | Z |
| 0x4E | 78 | `FSin` | C | Rd, Ra, Rb | FP[Rd] = sin(FP[Ra]) | Z,V |
| 0x4F | 79 | `FCos` | C | Rd, Ra, Rb | FP[Rd] = cos(FP[Ra]) | Z,V |
| 0x50 | 80 | `FExp` | C | Rd, Ra, Rb | FP[Rd] = exp(FP[Ra]) | Z,V |
| 0x51 | 81 | `FLog` | C | Rd, Ra, Rb | FP[Rd] = log(FP[Ra]) | Z,V |
| 0x52 | 82 | `FClamp` | C | Rd, Ra, Rb | FP[Rd] = clamp(FP[Ra], FP[Rb], Rc) | Z |
| 0x53 | 83 | `FLerp` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] * t + FP[Rb] * (1-t) | Z |
| 0x54 | 84 | `FCmpEq` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] == FP[Rb] ? 1 : 0 | Z |
| 0x55 | 85 | `FCmpNe` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] != FP[Rb] ? 1 : 0 | Z |
| 0x56 | 86 | `FCmpLt` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] < FP[Rb] ? 1 : 0 | Z |
| 0x57 | 87 | `FCmpLe` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] <= FP[Rb] ? 1 : 0 | Z |
| 0x58 | 88 | `FCmpGt` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] > FP[Rb] ? 1 : 0 | Z |
| 0x59 | 89 | `FCmpGe` | C | Rd, Ra, Rb | FP[Rd] = FP[Ra] >= FP[Rb] ? 1 : 0 | Z |

### 4.5 Conversions (0x60–0x6F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x60 | 96 | `IToF` | C | Rd, Ra, Rb | FP[Rd] = (float)GP[Ra] | Z |
| 0x61 | 97 | `FToI` | C | Rd, Ra, Rb | GP[Rd] = (int32_t)FP[Ra] (truncates) | Z |
| 0x62 | 98 | `BToI` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] != 0 ? 1 : 0 | Z |
| 0x63 | 99 | `IToB` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] ? 1 : 0 | Z |

### 4.6 Memory Operations (0x70–0x7F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x70 | 112 | `Load8` | E | Rd, Rb, off16 | GP[Rd] = mem[Rb+off16] (zero-extend u8) | — |
| 0x71 | 113 | `Load16` | E | Rd, Rb, off16 | GP[Rd] = mem[Rb+off16] (zero-extend u16) | — |
| 0x72 | 114 | `Load32` | E | Rd, Rb, off16 | GP[Rd] = mem[Rb+off16] (u32) | — |
| 0x73 | 115 | `Load64` | E | Rd, Rb, off16 | GP[Rd] = mem[Rb+off16] (u64, may span registers) | — |
| 0x74 | 116 | `Store8` | E | Rs, Rb, off16 | mem[Rb+off16] = GP[Rs] & 0xFF | — |
| 0x75 | 117 | `Store16` | E | Rs, Rb, off16 | mem[Rb+off16] = GP[Rs] & 0xFFFF | — |
| 0x76 | 118 | `Store32` | E | Rs, Rb, off16 | mem[Rb+off16] = GP[Rs] | — |
| 0x77 | 119 | `Store64` | E | Rs, Rb, off16 | mem[Rb+off16] = GP[Rs] (64-bit) | — |
| 0x78 | 120 | `LoadAddr` | E | Rd, Rb, off16 | GP[Rd] = Rb + off16 (compute address) | — |
| 0x79 | 121 | `StackAlloc` | D | Rd, size16 | SP -= size16; GP[Rd] = new SP | — |

### 4.7 Agent-to-Agent Communication (0x80–0x8F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x80 | 128 | `ASend` | G | agent_id, reg | Send message in GP[reg] to agent agent_id. Non-blocking. | — |
| 0x81 | 129 | `ARecv` | G | agent_id, reg | Receive into GP[reg] from agent agent_id. Blocking until arrived. | — |
| 0x82 | 130 | `AAsk` | G | agent_id, reg | Send request and wait for response. GP[reg] holds question; response written to same reg. | — |
| 0x83 | 131 | `ATell` | G | agent_id, reg | Fire-and-forget message. Same as ASend but no response expected. | — |
| 0x84 | 132 | `ADelegate` | G | agent_id, bc_start | Delegate bytecode execution to target agent starting at bc_start. | — |
| 0x85 | 133 | `ABroadcast` | G | reg | Send GP[reg] to all known agents. | — |
| 0x86 | 134 | `ASubscribe` | G | channel_id | Subscribe current agent to channel channel_id. | — |
| 0x87 | 135 | `AWait` | G | condition_reg | Block until condition in GP[condition_reg] becomes true. | — |
| 0x88 | 136 | `ATrust` | G | agent_id, level | Establish trust relationship with agent_id at level (0-255). | — |
| 0x89 | 137 | `AVerify` | G | agent_id, result_reg | Verify trust level of agent_id; write level to GP[result_reg]. | — |

### 4.8 Type/Meta Operations (0x90–0x9F)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0x90 | 144 | `Cast` | C | Rd, Ra, Rb | Type-cast GP[Ra] to type in GP[Rb]; result in GP[Rd]. | — |
| 0x91 | 145 | `SizeOf` | C | Rd, Ra, Rb | GP[Rd] = size in bytes of type GP[Ra] | — |
| 0x92 | 146 | `TypeOf` | C | Rd, Ra, Rb | GP[Rd] = runtime type tag of GP[Ra] | — |

### 4.9 Bitwise Operations (0xA0–0xAF)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0xA0 | 160 | `BAnd` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] & GP[Rb] | Z,S |
| 0xA1 | 161 | `BOr` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] \| GP[Rb] | Z,S |
| 0xA2 | 162 | `BXor` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] ^ GP[Rb] | Z,S |
| 0xA3 | 163 | `BShl` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] << (GP[Rb] & 31) | Z,C |
| 0xA4 | 164 | `BShr` | C | Rd, Ra, Rb | GP[Rd] = GP[Ra] >> (GP[Rb] & 31) | Z,C |
| 0xA5 | 165 | `BNot` | C | Rd, Ra, Rb | GP[Rd] = ~GP[Ra] | Z,S |

### 4.10 Vector/SIMD Operations (0xB0–0xBF)

| Hex | Decimal | Name | Format | Operands | Semantics | Flags |
|-----|---------|------|--------|----------|-----------|-------|
| 0xB0 | 176 | `VLoad` | E | Rd, Rb, off16 | Load vector component from memory at Rb+off16 into V[Rd] | — |
| 0xB1 | 177 | `VStore` | E | Rs, Rb, off16 | Store vector component V[Rs] to memory at Rb+off16 | — |
| 0xB2 | 178 | `VAdd` | C | Rd, Ra, Rb | V[Rd][i] = V[Ra][i] + V[Rb][i] for all i | — |
| 0xB3 | 179 | `VMul` | C | Rd, Ra, Rb | V[Rd][i] = V[Ra][i] * V[Rb][i] for all i | — |
| 0xB4 | 180 | `VDot` | C | Rd, Ra, Rb | V[Rd] = sum_i(V[Ra][i] * V[Rb][i]) (scalar result) | — |

### 4.11 Extended/Implementation-Specific Opcodes (C Implementation)

These opcodes are defined in the C implementation but are **not part of the core ISA v3**. They may be used by implementations that need additional functionality. Implementations should handle unknown opcodes gracefully (return error or ignore).

| Hex | Decimal | Name | Description |
|-----|---------|------|-------------|
| 0x60 | 96 | `FLUX_MEMCOPY` | Memory copy (32 bytes) |
| 0x61 | 97 | `FLUX_MEMSET` | Memory set |
| 0x62 | 98 | `FLUX_MEMCMP` | Memory compare |
| 0x63 | 99 | `FLUX_DELEGATE_RESULT` | Result from delegated task |
| 0x64 | 100 | `FLUX_REPORT_STATUS` | Agent status report |
| 0x65 | 101 | `FLUX_REQUEST_OVERRIDE` | Request override |
| 0x66 | 102 | `FLUX_BROADCAST` | Alias for ABroadcast |
| 0x67 | 103 | `FLUX_REDUCE` | Reduction operation |
| 0x68 | 104 | `FLUX_DECLARE_INTENT` | Declare intent |
| 0x69 | 105 | `FLUX_ASSERT_GOAL` | Assert goal |
| 0x6A | 106 | `FLUX_VERIFY_OUTCOME` | Verify outcome |
| 0x6B | 107 | `FLUX_EXPLAIN_FAILURE` | Explain failure |
| 0x6C | 108 | `FLUX_SET_PRIORITY` | Set task priority |
| 0x70 | 112 | `FLUX_TRUST_CHECK` | Trust check |
| 0x71 | 113 | `FLUX_TRUST_UPDATE` | Trust update |
| 0x72 | 114 | `FLUX_TRUST_QUERY` | Trust query |
| 0x73 | 115 | `FLUX_REVOKE_TRUST` | Revoke trust |
| 0x74 | 116 | `FLUX_CAP_REQUIRE` | Require capability |
| 0x75 | 117 | `FLUX_CAP_REQUEST` | Request capability |
| 0x76 | 118 | `FLUX_CAP_GRANT` | Grant capability |
| 0x77 | 119 | `FLUX_CAP_REVOKE` | Revoke capability |
| 0x78 | 120 | `FLUX_BARRIER` | Synchronization barrier |
| 0x79 | 121 | `FLUX_SYNC_CLOCK` | Synchronize clock |
| 0x7A | 122 | `FLUX_FORMATION_UPDATE` | Formation update |
| 0x7B | 123 | `FLUX_EMERGENCY_STOP` | Emergency stop |
| 0x81 | 129 | `FLUX_YIELD` | (Duplicate — already in core) |
| 0x82 | 130 | `FLUX_RESOURCE_ACQUIRE` | Acquire resource |
| 0x83 | 131 | `FLUX_RESOURCE_RELEASE` | Release resource |
| 0x84 | 132 | `FLUX_DEBUG_BREAK` | Debug break |

---

## 5. Memory Model

### 5.1 Flat Memory with Regions

FLUX uses a flat memory model with region-based allocation. Memory is managed through a `FluxMemManager` which tracks multiple named regions.

- **Default region size:** 64 KB
- **Maximum regions:** 256
- **Memory operations:** Load and store with base register + 16-bit unsigned offset

### 5.2 Stack

The stack grows **downward** (SP starts high, decreases). It is used for:
- Return addresses (pushed by `Call`)
- Local variable spills
- Function arguments (for functions with >2 args, spill to stack)

Stack layout for a function call:

```
Higher addresses
+------------------+
| Caller's frame    |
+------------------+
| Argument N        |  (if N > 2, spilled)
| Argument 2        |  (GP[A1] = R10)
| Argument 1        |  (GP[A0] = R9)
+------------------+
| Return address    |  (pushed by CALL, popped into LR/R15)
+------------------+
| Local variables   |  (GP[FP] points here)
+------------------+ ← FP points here
| Saved registers   |  (callee-saved: R0-R7 if needed)
+------------------+
| Spill space       |
+------------------+ ← SP points here (lowest used)
Lower addresses
```

### 5.3 Calling Convention

**Arguments:** First two integer args in R9, R10. First two float args in F9, F10. Additional args spilled to stack.

**Return values:** Integer return in R8. Float return in F8.

**Callee-saved:** R11 (SP), R12 (FP), R13 (FL), R14, R15 (LR) must be preserved across calls. R0–R7 may be clobbered.

**Caller-saved:** R0–R7, R8, R9, R10 are caller-saved (callee may clobber them).

### 5.4 Standard Prologue/Epilogue

**Prologue (function entry):**
```
Push FP          ; save caller's frame pointer
Mov  FP, SP      ; establish new frame
Sub  SP, SP, N   ; allocate locals (or use StackAlloc)
```

**Epilogue (function exit):**
```
Mov  SP, FP      ; collapse locals
Pop  FP          ; restore caller's frame pointer
Ret              ; return to caller
```

---

## 6. A2A Protocol

The Agent-to-Agent (A2A) protocol enables direct communication between agents in the fleet. It is implemented as a set of VM opcodes that interact with the fleet message bus.

### 6.1 Message Delivery Semantics

| Opcode | Delivery | Response |
|--------|----------|----------|
| `ATell` | Fire-and-forget | None |
| `ASend` | At-least-once | Optional ack |
| `AAsk` | At-least-once | blocking response | 
| `ARecv` | At-least-once | Blocking wait |
| `ABroadcast` | At-most-once | None |

### 6.2 Trust Model

- Agents start with **no trust** (level 0).
- `ATrust` establishes bidirectional trust at a given level (0–255).
- Trust levels: 0=none, 1=acquaintance, 128=peer, 255=fully trusted.
- `AVerify` checks the current trust level of a peer agent.
- Operations on untrusted agents may be rejected by the runtime.

### 6.3 Channels

- Agents subscribe to named channels with `ASubscribe`.
- Messages on a channel are delivered to all subscribers.
- `AWait` blocks until a specific condition (stored in a register) becomes true.

### 6.4 Delegation

`ADelegate` allows one agent to delegate bytecode execution to another:
- The delegating agent sends a bytecode block address to the target agent.
- The target agent executes the bytecode in its own context.
- Results are returned via `FLUX_DELEGATE_RESULT` (implementation-specific opcode).

---

## 7. System Calls

FLUX provides a `SYSCALL` mechanism for platform-specific I/O and external resource access. However, in the Rust core ISA, there is no explicit `SYSCALL` opcode. Instead, platform-specific operations are handled through the A2A protocol with trusted system agents.

For the C implementation, the extended opcode range (0x60–0x84) handles system-level operations. Key system calls:

| Opcode | Name | Description |
|--------|------|-------------|
| 0x81 | `FLUX_YIELD` | Yield to scheduler |
| 0x82 | `FLUX_RESOURCE_ACQUIRE` | Acquire exclusive resource |
| 0x83 | `FLUX_RESOURCE_RELEASE` | Release resource |
| 0x84 | `FLUX_DEBUG_BREAK` | Breakpoint for debugger |

The C VM structure includes a `FluxA2AHandler` callback that implementations can use to intercept and handle A2A and system opcodes.

---

## 8. Application Binary Interface (ABI)

### 8.1 Bytecode File Format

A FLUX bytecode file consists of:

1. **Header** (16 bytes):
   - Magic: `FLUX` (4 bytes)
   - Version: major.minor (2 bytes)
   - Flags (2 bytes)
   - Entry point function index (4 bytes)
   - Reserved (4 bytes)

2. **Function Table:** Array of function entries, each containing:
   - Name offset (4 bytes)
   - Address (4 bytes)
   - Local register count (2 bytes)
   - Max stack depth (2 bytes)

3. **Bytecode:** Instructions for each function, concatenated.

4. **Data Section:** Static data (strings, constants).

### 8.2 Function Calls

1. Caller loads arguments into R9, R10 (and stack if >2 args).
2. Caller executes `Call func_idx`.
3. CALL pushes return address (PC+1) onto stack and jumps to function.
4. Callee prologue saves FP, sets up new frame.
5. Callee executes its body.
6. Callee epilogue restores FP, executes `Ret`.
7. RET pops return address and jumps back to caller.
8. Caller reads return value from R8.

### 8.3 Inter-Agent Calls

When an agent calls a function in another agent's bytecode:

1. The calling agent uses `AAsk` or `ADelegate` with the target agent's ID.
2. The message contains: function name/index, arguments serialized.
3. The target agent receives the call, executes it, and returns the result.
4. `AAsk` is blocking (caller waits for response).
5. `ADelegate` is non-blocking (caller receives result asynchronously via message).

---

## 9. Implementation Notes

### 9.1 Dispatch Optimization

The dispatch loop (fetch-decode-execute) is the primary performance bottleneck. Recommended optimizations:
- Use a `switch` statement ordered by opcode frequency (hottest first).
- Keep the most common opcodes (IAdd, IMov, Jump, Load32, Store32) at the start of the opcode table for branch prediction.
- Inline the operand fetch for Format A and B instructions.

### 9.2 Opcode Numbering Discrepancy

**Rust vs C implementations use different opcode values.** The v3 specification adopts the Rust opcode values as canonical. Key differences:

| Name | Rust (v3 canonical) | C (ISA v2) |
|------|---------------------|------------|
| Halt | 0x00 | 0x00 |
| Nop | 0x01 | 0x01 |
| Ret | 0x02 | 0x02 |
| Jump | 0x03 | 0x43 |
| IAdd | 0x21 | 0x20 |
| IAnd | 0x2C | 0x25 |
| ATell | 0x83 | 0x50 |
| AAsk | 0x82 | 0x51 |
| ADelegate | 0x84 | 0x52 |
| ABroadcast | 0x85 | 0x53 |

### 9.3 Flag Behavior

- Integer arithmetic sets Z (zero), S (sign), V (overflow), C (carry).
- Comparisons set Z based on equality or ordering.
- The C implementation stores flags in the VM struct (`flag_zero`, `flag_sign`, `flag_carry`, `flag_overflow`).
- The Rust implementation delegates flag handling to the flags register (R13/FL).

### 9.4 Error Handling

Errors are reported via `FluxError` enum (C) or `Result` types (Rust):

| Code | Name | Description |
|------|------|-------------|
| 0 | `FLUX_OK` | Success |
| 1 | `FLUX_ERR_HALT` | Halt was executed |
| 2 | `FLUX_ERR_INVALID_OPCODE` | Unknown opcode |
| 3 | `FLUX_ERR_DIV_ZERO` | Divide by zero |
| 4 | `FLUX_ERR_STACK_OVERFLOW` | Stack overflow (>256 frames) |
| 5 | `FLUX_ERR_STACK_UNDERFLOW` | Stack underflow (Pop of empty) |
| 11 | `FLUX_ERR_CYCLE_BUDGET` | Cycle budget exceeded |
| 12 | `FLUX_ERR_MEMORY` | Memory access error |

---

## 10. Example: Factorial in FLUX Bytecode

Compute factorial(7) and store result in R0.

```
# Initialize
MOVI   R0, 7        # [02][00][07][00]
MOVI   R1, 1        # [02][01][01][00]

# Loop: multiply accumulator by counter
IMUL   R1, R1, R0   # [23][01][01][00]
IDEC   R0, 1        # [29][00][01][00]
JNZ    R0, -6       # [05][00][FA][FF]
                              # JumpIfNot R0, PC-6 (6 instructions back)

# Result now in R1
HALT                # [00][00][00][00]
```

Hex bytes: `02 00 07 00 02 01 01 00 23 01 01 00 29 00 01 00 05 00 FA FF 00 00 00 00`

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-01 | Fleet Architecture | Initial ISA |
| v2.0 | 2026-04 | Oracle1 | Unified ISA proposal based on 11 implementations |
| v3.0 | 2026-05-03 | Oracle1 | Canonical spec: cross-referenced Rust (100 opcodes), C (133 opcodes), v2 proposal. Rust opcode numbers adopted as canonical. Format C clarified as 3-register operands (not type tag). |
| v3.1 | 2026-05-03 | Oracle1 | Added Section 12: Edge Encoding (JC1 variable-width ISA for ARM64/CUDA constrained hardware) |

---

## 12. Edge Encoding (ISA v3 — JC1 Variant)

> **Origin:** `JetsonClaw1-vessel/for-oracle1/ISA-V3-EDGE-ENCODING.md` (JC1, 2026-04-12)  
> **Target:** Jetson Orin Nano, ARM64, 1024 CUDA cores, 8 GB RAM, bare metal  
> **Status:** Draft — Review Requested

While the canonical FLUX ISA uses fixed 4-byte instructions (FLUX-X), JC1 developed a **variable-width encoding** optimized for edge hardware where every byte matters.

### 12.1 Two Encoding Modes

| Mode | Encoding | Opcode Count | Target |
|------|----------|-------------|--------|
| **Cloud** | Fixed 4-byte | ~200 | flux-runtime-c, general fleet ops |
| **Edge** | Variable 1–3 B | 256 (80 used) | cuda-instruction-set, ARM64 bare metal |

### 12.2 Variable-Width Scheme

Instruction length is determined by the top 2 bits of the first byte:

```
Byte 0:
  0XXXXXXX  → 1-byte instruction (no operands)    range: 0x00–0x7F (128 opcodes)
  10XXXXXX  → 2-byte instruction (1 operand byte)  range: 0x80–0xBF (64 opcodes)
  11XXXXXX  → 3-byte instruction (2 operand bytes)  range: 0xC0–0xFF (64 opcodes)
```

### 12.3 Key Differences from Cloud Encoding

| Property | Cloud (FLUX-X) | Edge (JC1) |
|----------|---------------|------------|
| Instruction width | Fixed 4 bytes | Variable 1–3 bytes |
| Operand encoding | Direct register bytes | Embedded in opcode space |
| Register model | Explicit R0–R15 | Implicit accumulator (r0) for 1-byte ops |
| Energy awareness | Via FLUX-C bridge | Native ATP_QUERY, ATP_SPEND opcodes |
| Trust model | AT rust/AVerify | TRUST_VERIFY opcode with threshold |
| CUDA support | Vector registers | cuda-instruction-set integration |

### 12.4 Edge Opcode Examples

```asm
; 1-byte ops (top bit = 0)
NOP      = 0x00  ; No operation
HALT     = 0x20  ; Stop execution
INST_REST= 0xF4  ; Energy regeneration

; 2-byte ops (top bits = 10)
; Opcode in bits 5-0, operand in byte 1
MOV   r1, r0 = 0x90 0x01  ; r1 = r0
ADD   r0, r1  = 0x91 0x01  ; r0 += r1
JMP   offset  = 0xC1 0xXX  ; Jump relative

; 3-byte ops (top bits = 11)
; Opcode in bits 5-0, two operand bytes
LDI   r1, 0x64 = 0xCA 0x02 0x00 0x64 ; r1 = 100 (immediate)
CMP   r0, r1   = 0x94 0x01            ; Compare r0 to r1
```

### 12.5 Energy-Aware Execution

The edge encoding includes native energy management:

```asm
ATP_QUERY    ; 0xD6 (3-byte) — r0 = current energy
LDI  r1, 100 ; Load task energy cost
CMP  r0, r1   ; Compare energy to cost
Bcond LT, rest ; If insufficient, rest
ATP_SPEND r0, 100 ; Burn energy for task
```

### 12.6 A2A on Edge

```asm
; Send discovery with confidence tag
INST_LISTEN   ; 0xFB — r0 = sensor input
CONF_SET4 r0, 0xA ; 0xB0 0x0A — moderate confidence
MSG_SEND r1, 0x0800 ; 0xE0 0x10 0x08 0x00 — to stigmergy space

; Receive and trust-check
MSG_POLL  ; 0xE4 — r0 = pending messages
MSG_RECV  ; 0xE1 — dequeue → r1,r2,r3,r14
TRUST_VERIFY r14, 50 ; 0xDE — r0 = (trust >= 50)?
```

### 12.7 Reference Implementation

The full JC1 edge encoding spec including opcode map, assembly syntax, and example programs is in:
**`SuperInstance/JetsonClaw1-vessel` → `for-oracle1/ISA-V3-EDGE-ENCODING.md`**

### 12.8 Open Questions (from JC1)

1. Should edge-energy ops be folded into FLUX-C as a unified energy model?
2. Can the trust opcode threshold be made adaptive based on tile confidence?
3. Should the 3-byte format use a 12-bit or 16-bit operand field for larger immediates?
4. Does the variable-width encoding interact with the FLUX-C/FLUX-X bridge design?

---

*This is the canonical FLUX ISA specification. All implementations should conform to this document. Discrepancies should be resolved by opening an issue with the Cocapn Fleet Architecture team.*