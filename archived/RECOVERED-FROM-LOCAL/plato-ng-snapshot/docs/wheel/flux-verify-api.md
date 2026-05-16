# flux-verify-api — Natural Language Verification

> **Dated:** 2026-05-05 · **Repository:** SuperInstance/flux-verify-api

## The Core Insight

Post a claim in English, get back PROVEN or DISPROVEN with a full physics trace, counterexample, and SHA-256 proof hash. An HTTP API that turns natural language through constraint compilation into FLUX bytecode execution. 3157 lines in README + Rust source across 6 modules.

## Forgotten Gold

### 1. Natural Language → FLUX Bytecode Compilation

The parser extracts structured constraints from English claims. A request like "A 50kHz sonar at 200m depth can detect a 10dB target at 5km" becomes:
1. `LOAD depth_m=200`
2. `LOAD frequency_hz=50000`
3. `SONAR_SVP` → Mackenize 1981 sound velocity
4. `SONAR_ABSORPTION` → Francois-Garrison 1982 absorption
5. `SONAR_TL` → Spherical spreading + absorption
6. `ASSERT_GT` → Signal excess check

The parser handles unit suffixes (khz, hz, m, db), range extraction ("between X and Y", "from X to Y"), and keyword extraction ("safe range", "can detect").

### 2. Real Physics Models Embedded in the VM

The VM implements actual ocean acoustics:
- **Mackenzie (1981)**: Nine-term equation for sound speed in seawater (valid 2-30°C, 25-40‰, 0-8000m)
- **Francois-Garrison (1982)**: Three-component absorption model (boric acid, MgSO₄, pure water relaxation frequencies)
- **Transmission loss**: 20·log₁₀(range) + α·range/1000 with absorption

And the **active sonar equation**: SE = SL - 2·TL + TS - DT (signal excess = source level - 2×transmission loss + target strength - detection threshold).

### 3. Ed25519 Bytecode Signing with Key Rotation

The `verify_middleware` implements a full security model:
- Multiple trusted public Ed25519 keys
- **Key rotation without downtime**: add a new key, old signatures still verify
- Key revocation: remove compromised keys
- Strict mode (reject unsigned) and non-strict mode (allow unsigned for dev)
- The signature covers (SHA-256 fingerprint || timestamp) so replay attacks are prevented
- Selective verification: middleware checks bytecodes before VM execution

### 4. Trace Provenance via Merkle Hashing

Every verification trace produces a SHA-256 Merkle hash chain:
```
hash(trace) = SHA-256(
    SHA-256(entry_0),
    SHA-256(entry_1),
    ...
)
```

Each entry hash captures opcode, value, result, expected, actual, and description. The proof hash is returned in the response and can be independently verified (the `verify_proof_hash` function exists in the source). This means **anyone can prove exactly what computation produced a verdict**.

### 5. Three-Tier Domain Architecture

The domain model is designed for extension:
- **Sonar**: Complex physics with 6-8 bytecode stages, signal excess math
- **Thermal**: Simple bounds checking with margin computation
- **Generic**: Comparison ops (`gt`, `gte`, `lt`, `lte`, `eq`), range checks (`between`, `within`)

Adding a new domain = new parser + new VM opcodes. The `ConstraintProblem` struct is the cross-domain interface.

### 6. PLATO Tile Integration

Verification results automatically become PLATO tiles when configured. Each verified claim is submitted as a tile with proof hash, verdict, and claim text — making the verification system part of the fleet coordination protocol. The PLATO client uses bearer auth and returns the tile ID in the API response.

## Relevance to Wheel

This predates the quality gate stream but demonstrates the end-to-end pattern: human claim → machine constraint → execution → proof → fleet sharing. The signing middleware and Merkle provenance are directly reusable. The domain extension pattern (add a parser + VM ops) is the same architecture the Wheel will need for its constraint emission rules.
