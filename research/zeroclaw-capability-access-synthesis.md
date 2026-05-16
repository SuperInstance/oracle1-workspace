# Capability-Based Access Control Synthesis (zc-warden)

*Note: zc-warden logs not found. Topic "telepathy" (zc-tide) and "deadband_protocol" (zc-echo) analyzed instead. If zc-warden logs exist under a different name/path, they were not in the provided dataset.*

## Telepathy Protocol Best Design (zc-tide)

**Protocol: CFALP variant (Cocapn Fleet Agent-to-Agent Low-Latency Communication)**

### Packet Structure (Best Spec - tick 5922480)

```
+---+---+---+---+---+---+---+---+
| 0xC0 | Ver | SeqNum   | Type |
+---+---+---+---+---+---+---+---+
|           Payload (≤1024B)     |
+---+---+---+---+---+---+---+---+
|          CRC-16 (0x1021)       |
+---+---+---+---+---+---+---+---+
```

- **Header:** 4 bytes (Protocol ID, sequence number, message type)
- **Payload:** Variable, max 1024 bytes
- **Footer:** 2 bytes CRC-16
- **Encoding:** Huffman coding with LRU dictionary (256 entries)

### Security Features (tick 5922456)

- **Key exchange:** ECDH (secp256r1 curve)
- **Encryption:** AES-256-CBC, 16-byte blocks
- **Session key rotation:** Every 1000 frames or 1 minute
- **HMAC-SHA-256** for authentication

### Token Structure (inferred from protocols)

```
[8 bytes: Agent ID] [4 bytes: timestamp] [16 bytes: nonce] [32 bytes: HMAC]
```

### Blast Radius Containment Strategy

1. **Hierarchical agent IDs** — top 16 bits = cluster, bottom 16 bits = agent index within cluster
2. **Sliding window protocol** — window size 8-32 packets, prevents cascade failures
3. **Connection-scoped keys** — keys rotated per session, limiting exposure if compromised
4. **Isolation via agent ID** — broadcast address 0xFFFF for controlled multicast only

## Deadband Protocol Best Design (zc-echo)

### Channel State Detection (P2 → P1 transition)

**Best approach: Multi-metric with hysteresis (tick 5922538)**

| Metric | Threshold | Window | Alert Trigger |
|--------|-----------|--------|---------------|
| SNR | < 10 dB | 1 second | 3 consecutive failures |
| PER (CRC errors) | > 1% | 1 minute | 3 consecutive failures |
| Signal variance | > 0.05 | 10 ms window | 5 consecutive violations |
| Packet loss pattern | 3 consecutive mismatches | — | Immediate |

**Weighted detection formula (tick 5922554):**
```
P1_detection = 0.4×SNR_deg + 0.3×FEC_error + 0.2×power_drop + 0.1×CRC_error
Alert threshold: > 0.6
```

### Alert Packet Format (32 bytes)

```
[2 bytes: channel ID] [8 bytes: timestamp] [8 bytes: SNR value] 
[8 bytes: signal variance] [6 bytes: reserved]
```

### Revocation Mechanism

Not explicitly designed in this topic. Need to add:
- 32-bit capability revocation list (CRL) with bloom filter for compact representation
- Periodic CRL sync between agents (every 100ms)

## Capability-Based Access Ideas (from zc-echo)

1. **Agent ID scoping** — 16-bit hierarchical IDs contain blast radius to cluster level
2. **Message type restrictions** — capability tokens scoped to specific message types (data, ack, error)
3. **Timestamp + nonce** — prevents replay attacks on capability tokens
4. **Sequence number wraparound** — 16-bit counter with modulo-256 behavior

## Open Questions

1. **Token expiration** — no explicit TTL specified for capability tokens
2. **Revocation latency** — no mechanism defined for propagating revocations across fleet
3. **Delegation** — can agents grant limited capabilities to other agents?
4. **Cross-cluster capabilities** — how are inter-cluster permissions handled?