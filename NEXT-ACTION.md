# NEXT-ACTION.md

## Active Task
**Whitepaper conversion: DONE ✅** (6 papers → research/whitepapers/, pushed to GitHub)
**Demo generator: running subagent, waiting for output.txt**

## What happened
- plato.wrap() conclusion was None — traced through PLATO API, fixed by adding `is_verified: True` to all atoms (not just conclusion) and ensuring `confidence >= 0.9` threshold is met
- DeepSeek auto-wired as fallback after MiniMax (casey's prepaid key not accessible to me)
- Whitepapers converted: all 6 pushed to SuperInstance/flux-research
- cocapn.ai GitHub repo doesn't exist yet (cocapn org invisible)

## Waiting on
- Demo subagent running plato_demo.py + uploading output.txt to SuperInstance/plato-demo

## Next
- Set up cocapn.ai GitHub pages (need Casey to create cocapn/cocapn.ai repo first)
- Build release GIF demo
- Wire cocapn-core to PLATO room
