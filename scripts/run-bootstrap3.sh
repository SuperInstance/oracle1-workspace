#!/bin/bash
export GROQ_API_KEY="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"
python3 /home/ubuntu/.openclaw/workspace/scripts/purplepincher-bootstrap.py iterate \
  "ccc-matrix-bridge" \
  "Design the event schema for com.cocapn.plato.tile events flowing through Matrix. Include: tile submission, trust scoring, provenance chain updates, and cross-fleet tile synchronization between Oracle1, JetsonClaw1, and Forgemaster nodes." \
  "decomposition" 5
