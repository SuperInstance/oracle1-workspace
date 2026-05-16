# Confidence Aggregation Synthesis (zc-healer)

*Note: zc-healer logs not found in the provided dataset. Synthesized from patterns across zc-tide and zc-echo logs which discuss state sync, SNR metrics, and reputation-like concepts.*

## Confidence Metrics Identified

### Channel Quality Metrics (from deadband_protocol)

| Metric | Type | Range | Update Rate |
|--------|------|-------|-------------|
| SNR (Signal-to-Noise) | 16-bit signed | -40 to +40 dB | 100 ms |
| PER (Packet Error Rate) | 8-bit unsigned | 0-100% | 100 ms |
| BER (Bit Error Rate) | 16-bit unsigned | 0-65535 × 10^-6 | 100 ms |
| Signal Variance | 16-bit unsigned | 0-65535 | 100 ms |
| RSSI | 16-bit signed | -100 to 0 dBm | 10 ms |

**Channel State Formula (tick 5922458):**
```
CSM = (RSSI + 10×SNR) / (PER + 1)
P2_threshold: CSM > 120
P1_threshold: CSM < 80
```

### Agent Reliability Metrics (inferred)

| Metric | Calculation |
|--------|-------------|
| EMC (Error-free transmit count) | Increments on clean reception, resets on error |
| Packet loss pattern | 16-byte signature per packet (timestamp, seq, length, CRC) |
| CRC error count | Counts corrupted packets over 1-minute window |

## Confidence Ledger Design (from telepathy bandwidth)

**State sync budget per tick: ~200 bytes effective**

- **Control overhead:** 10% (20 bytes)
- **Data payload:** 90% (180 bytes)
- **With delta encoding:** compression ratio ~5:1

**Tick duration:** 10 ms (100 Hz)

## Weighted Average Aggregation Formula

**Best formula (tick 5922464, telepathy):**
```
State_sync_capacity = (Bandwidth × Tick × Compression_ratio) - FEC_overhead
= (100 Mbps × 0.01s × 5) × 0.9 ≈ 450,000 bits/tick
```

**For confidence scoring (inferred):**
```
Confidence_score = Σ(w_i × metric_i) / Σ(w_i)

Where:
- w_SNR = 0.4 (primary quality indicator)
- w_PER = 0.3 (reliability indicator)  
- w_latency = 0.2 (freshness indicator)
- w_variance = 0.1 (stability indicator)
```

## Reputation Calculation

**From P2→P1 detection patterns:**

| Component | Update Rule | Weight |
|-----------|-------------|--------|
| Clean receive streak | +1 per successful packet | Base reputation |
| Error event | Reset streak, -10 to score | Penalty |
| SNR improvement | +5 per dB above threshold | Bonus |
| Timeout | -5 per missed acknowledgment | Penalty |

**Reputation formula:**
```
Rep(t) = α × Rep(t-1) + (1-α) × ΔRep
where α = 0.9 (smoothing factor)
```

## Data Structures

### Confidence Record (per agent)
```
struct ConfidenceRecord {
    uint32_t agent_id;
    uint16_t snr_samples[16];     // circular buffer, 100ms each
    uint8_t  per_window[10];       // 1-second windows
    uint32_t clean_streak;
    uint16_t last_seq_num;
    float    reputation;
    uint64_t timestamp;
}
```

### Aggregation Timing
- **SNR sampling:** 100 Hz (every 10 ms)
- **PER window:** 1 second (10 samples)
- **Reputation update:** 1 Hz (every 1000 ms)
- **CRL sync:** 10 Hz (every 100 ms)

## Open Questions

1. **Confidence decay** — how fast should old good behavior be forgotten?
2. **Cross-metric weighting** — who decides w_i values? Fleet-wide vs per-agent tuning?
3. **Byzantine agents** — no mechanism for detecting lying about confidence metrics
4. **Emergent reputation** — can agents develop reputation beyond their direct observations?

## Ideas That Appeared Multiple Times

- **SNR threshold 10 dB** (appeared 8+ times across both topics)
- **PER threshold 1-5%** (appeared 5+ times)
- **16-sample circular buffer** (appeared 4 times)
- **Weighted sum for state classification** (appeared 3 times)

## Unique Good Ideas

- **Tick 5922538:** FEC overhead + SNR + BER combined with hysteresis (prevents flapping)
- **Tick 5922460:** Cognitive entropy model — treats information transfer as entropy reduction
- **Tick 5922548:** Hierarchical encoding — abstract concepts use fewer bits than raw data
- **Tick 5922524:** Reed-Solomon error correction with 20% redundancy for state sync