#!/bin/bash
export GROQ_API_KEY="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"
python3 /home/ubuntu/.openclaw/workspace/scripts/purplepincher-bootstrap.py iterate \
  "fleet-event-schema" \
  "Design the complete event schema for fleet tile synchronization. Tiles are atomic training data units produced by agents exploring the Crab Trap MUD. They need to flow through Matrix rooms between Oracle1 (cloud), JetsonClaw1 (edge), and Forgemaster (GPU forge). Include: tile format, trust scoring events, provenance chain updates, sync protocol, and conflict resolution." \
  "socratic" 5
