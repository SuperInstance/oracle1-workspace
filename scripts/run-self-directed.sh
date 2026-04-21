#!/bin/bash
# Self-directed experiment: all models, all temperatures
# Models: seed-mini, seed-pro, deepseek-chat, kimi-k2, groq-llama-70b
# Temps: 0.3, 0.7, 1.0
# 15 total runs, ~5 rounds each

export DEEPINFRA_API_KEY="RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ"
export DEEPSEEK_API_KEY="sk-f742b70fc40849eda4181afcf3d68b0c"
export MOONSHOT_API_KEY="sk-qGazOaVqFsk3dDAllrA6iQQHa97sNIhe8lWnpjFogcskBrep"
export GROQ_API_KEY="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"

cd /home/ubuntu/.openclaw/workspace
python3 scripts/lock-self-directed.py "$@"
