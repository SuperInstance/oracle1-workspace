# PLATO-NG Batch Results

## Git-Agent Pattern Library (10 repos)
- 70,315 files, 24.8M LOC, 152 rooms identified
- Most common: test/suite (86% algorithmic, 14% agentic)
- False positive rate on game/search: ~85% (too broad)
- Pattern library needs tightening for non-game repos

## Refiner Batch (all PLATO rooms)
- 26 rooms analyzed (50+ tiles each)
- 23 failures detected, 19 harness edits applied
- Most common: plateau (17), stuck (5), degrading (1)
- Flux-engine got the degrading failure (score trend -0.237)

## Crush Architecture Review
- Gap 1: Cross-room pub/sub (rooms are silos)
- Gap 2: Auth/governance layer (no identity)
- Gap 3: Agent twin memory pipeline (no persistence)

## Gleam Refiner Room
- 260 lines Gleam GenServer
- 225 lines Rust NIF stubs (score, similarity, pattern detection)
- Supervisor pattern with OneForOne restart, 60s tick
