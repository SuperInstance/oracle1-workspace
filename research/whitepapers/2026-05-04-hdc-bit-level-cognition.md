# SuperInstance HDC Architecture — Bit-Level Agent Cognition

> **Source**: Casey's deep research session with Google (2026-05-04).  
> **Purpose**: Integrate hyperdimensional computing into the SuperInstance fleet for sub-nanosecond answer judgment.

---

## Core Insight

**The repository IS the agent's muscle memory.** Instead of "reading" code, the agent memory-maps a binary SRAM image and performs register-level XOR-POPCNT to judge student answers in a single CPU cycle.

---

## The Metal Stack

### 1. Bit-Fingerprinting (64-bit)

```c
// Fast non-crypto hash → 64-bit numerical "soul" of the answer
uint64_t fingerprint = mmh3_hash64(text, seed);  // O(1) lookup
```

- Use MurmurHash3 (not SHA-256 — 10x faster, designed for hash tables)
- Knowledgeable teams use SHA-256. Clever teams use MurmurHash3.
- No "security" needed — we need unique numerical signatures, not crypto

### 2. Bloom Filter (First-Pass Judge)

```c
// Before the LLM ever touches a student's answer, check the Bloom filter
if (!bloom.contains(student_hash)) {
    return NOMATCH;  // Sub-millisecond, bypasses all expensive compute
}
```

- Catches 80-90% of inputs without hitting the SRAM
- Tune false-positive rate to system needs (1% FP rate typical)

### 3. Cache-Line Aligned SRAM (64-byte = 1 CPU cache line)

```c
typedef struct __attribute__((aligned(64))) {
    uint64_t fingerprint;   // 8 bytes: the 64-bit identity
    uint32_t lesson_id;      // 4 bytes: original TUTOR lesson
    uint16_t flags;          // 2 bytes: metadata
    uint16_t reserved;       // 2 bytes: padding
    uint8_t  padding[48];   // 48 bytes: fill to 64-byte boundary
} SramRecord;
```

- **Why the padding?** Every record occupies exactly ONE cache line. No split-loads. No cache misses. L1 cache hits every single time.
- Knowledgeable teams say "this is wasted space." Metal answer: "This is Cache Line Integrity."

### 4. XOR-POPCNT Judge (The Hardware Gate)

```c
uint64_t diff = record->fingerprint ^ student_hash;
int bit_distance = __builtin_popcountll(diff);  // One CPU cycle on modern x86/ARM
return (bit_distance <= threshold);  // 1 = Correct/Close, 0 = Wrong
```

- No if-then loops. No string parsing. One XOR, one POPCNT.
- Hardware instruction (POPCNT) — not a software loop
- Sub-nanosecond judgment for exact matches

### 5. Hyperdimensional Vectors (1024-bit = 16 × u64)

```rust
struct HyperVector([u64; 16]);  // 1024 bits

impl HyperVector {
    fn xor(&self, other: &HyperVector) -> HyperVector;     // binding
    fn rotate(&self, shift: usize) -> HyperVector;          // permutation (sequence)
    fn bundle(&self, others: &[HyperVector]) -> HyperVector; // majority rule
    fn hamming_distance(&self, other: &HyperVector) -> u32; // POPCNT of XOR
    fn bit_density(&self) -> f64;                          // ratio of 1-bits
}
```

**Why 1024-bit?**
- 64-bit: High collision risk for massive repos
- 1024-bit: Virtually zero collisions, but can be folded to 128-bit for edge devices
- Sparse encoding: Store 16 × 64-bit "trait hashes" not random noise

### 6. Sequence Encoding (Permutation)

```rust
// "A then B" ≠ "B then A" — encoded via bit-rotate before XOR
fn permute_sequence(words: &[&str], seed: u64) -> HyperVector {
    // V_result = rotate(V_word1, 1) ^ V_word2
    // The rotate makes vectors orthogonal to their original
    // This is how word order is preserved at the bit level
}
```

- Cyclic shift (ROL on CPU) for zero-cost permutation
- Knowledgeable teams say "The dog bit the man" = "The man bit the dog"
- Clever teams: these have completely different 1024-bit signatures

---

## The Full Pipeline

```
GitHub Push
    ↓
.github/workflows/metal-bake.yml
    ↓
binarize_logic.py (or Rust equivalent)
    - Hash all TUTOR lessons with MurmurHash3
    - Pack into 64-byte aligned records
    - Generate Bloom filter
    - Generate canary (lesson_id=0, verification fingerprint)
    ↓
Commit logic.sram + bloom.bin to repo
    ↓
Agent BOOT Phase
    ↓
mmap() loads logic.sram directly into virtual address space
    ↓
Agent WORK Phase
    ↓
1. Hash student input → 64-bit fingerprint
2. Check Bloom filter → if MISS, return NOMATCH (fast path)
3. If HIT: Scan SRAM with XOR-POPCNT
4. If distance <= threshold → MATCH with lesson_id
    ↓
(For 1024-bit HDC mode)
- Bundle atomic fingerprints into HyperVector
- Rotate + XOR for sequence encoding  
- Majority rule for concept combination
- Bit-density for fuzzy matching
```

---

## The Hierarchy of Operations

| Layer | Speed | Use Case |
|-------|-------|----------|
| Bloom Filter | 0.001 µs | First-pass "definitely not" |
| XOR-POPCNT (64-bit) | 1 cycle | Exact/slight-typo match |
| HyperVector bundle (1024-bit) | 16 cycles | Conceptual similarity |
| LLM/RAG | 100ms+ | Fallback for genuine novelty |

---

## Bit-Folding (For Edge Devices)

1024-bit hypervectors can be folded to 128-bit for Arduino/FPGA:

```rust
fn fold_to_128(vector: &[u64; 16]) -> u128 {
    // XOR the halves repeatedly — preserve Hamming distance ratios
    let mut result = [0u64; 8];
    for i in 0..8 {
        result[i] = vector[i] ^ vector[i + 8];
    }
    // Fold again if needed
    result[0] ^ result[4]
}
```

Folded 128-bit vectors retain ~90% similarity recognition of the original 1024-bit vector.

---

## Integration Points

### With constraint-theory-core
- Deterministic rational snapping already implemented
- HDC provides the "fuzzy" layer above the exact constraint layer
- Use case: Student is "close" in constraint space → HDC judges conceptual fit

### With PLATO
- Each tile can have a pre-computed 64-bit fingerprint
- PLATO room search becomes XOR-POPCNT against the tile index
- Integration with `plato-client-php` for PHP agents

### With FLUX ISA
- FLUX opcodes can be fingerprinted and stored in SRAM
- Agent execution becomes SRAM lookup + judgment
- Format G (jump) compatibility with the existing FLUX VM

### With GitHub Actions (metal-bake.yml)

```yaml
name: Metal Bake (Repo-to-SRAM)
on: [push]
jobs:
  bake:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Compile Repo to Binary SIMD-LUT
        run: |
          python3 .superinstance/binarize_logic.py \
            --seed ${{ secrets.ENTANGLEMENT_SEED }} \
            --align 64 \
            --out ./bin/logic.sram
      - name: Commit SRAM Image
        run: |
          git add ./bin/logic.sram ./bin/bloom.bin
          git commit -m "MEM_ALIGN: Rebaked logic image for L1 Cache"
          git push
```

---

## The 6 Planes of Abstraction

| Plane | Name | Output | When |
|-------|------|--------|------|
| 6 | Philosophy | Natural language reasoning | Start |
| 5 | Intent | NL intent specification | Clarification |
| 4 | Domain Language | FLUX-ese | **Most intents — sweet spot** |
| 3 | IR | Intermediate representation | Compilation |
| 2 | Bytecode | FLUX bytecode | VM execution |
| 1 | Metal | SRAM bit-patterns | Hardware judgment |

---

## Security: Stain-Verification (Canary)

```c
static inline int verify_canary(SramRecord* record, uint64_t expected) {
    uint64_t diff = record->fingerprint ^ expected;
    return __builtin_popcountll(diff) == 0;  // Exact match only
}
```

On boot, agent generates canary from INFINITY_KEY. If SRAM canary doesn't match, reject the logic as "alien."

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Bloom check | < 1 µs |
| SRAM XOR-POPCNT | < 1 ns |
| 1024-bit HDC bundle | < 50 ns |
| Full judge (bloom → SRAM) | < 10 µs average |
| Cache miss rate | < 0.1% (64-byte alignment) |

---

## Stack Priority

1. **superinstance-hdc-core** (Rust) — Core HDC primitives (fingerprint, bloom, sram, hdc, judge)
2. **superinstance-hdc-py** (Python) — Python bindings for agent integration  
3. **superinstance-hdc-php** (PHP) — PHP integration for web agents
4. **.github/workflows/metal-bake.yml** — Auto-bake on push for all SuperInstance repos

---

*Last updated: 2026-05-04 (from Casey-Google research session)*
*Encoder: Oracle1 | Fleet: SuperInstance*