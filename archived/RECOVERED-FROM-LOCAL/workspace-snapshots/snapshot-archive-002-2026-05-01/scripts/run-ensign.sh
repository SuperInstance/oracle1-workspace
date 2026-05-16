#!/bin/bash
export GROQ_API_KEY="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"
export DEEPINFRA_API_KEY="RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ"
export DEEPSEEK_API_KEY="sk-f742b70fc40849eda4181afcf3d68b0c"
cd /home/ubuntu/.openclaw/workspace
python3 scripts/the-ensign.py "$@"
