# flux-research

The intellectual engine for the FLUX ecosystem.

## What This Is

FLUX is a constraint specification and execution platform for safety-critical systems — aerospace, automotive, industrial. We compile GUARD DSL constraints through a formally verified pipeline to GPU, FPGA, and CPU backends. 278M+ evaluated test cases, zero drift.

This repo holds the research that drives those decisions.

## What's Here

- **Three formal papers**: Unified Constraint Theory, Lock Algebra, Abstraction Planes
- **Compiler/Interpreter taxonomy**: 22K-word deep dive on 6 runtime architectures (stack, register, tree-walking, native, JIT, transpiler) with lessons for FLUX ISA design
- **DCS Protocol experiments**: 40+ multi-model trials proving protocol design beats model scaling (21.87× generalist advantage)
- **Edge economics**: $10/MB satellite bandwidth → all processing must be local
- **Reverse actualization**: 2031→2026 backward-chained build orders with concrete repo targets
- **Fleet roundtables**: 10+ transcripts encoding collective fleet decisions

## Key Finding

> Protocol design > model capability. Structured coordination outperforms raw parameter scaling. Every time.

## The Thesis

Structured constraints are intelligence. Reduce solution-space entropy — don't scale parameters.

## Links

- [FLUX Compiler](https://github.com/SuperInstance/flux-compiler) | [FLUX VM](https://github.com/SuperInstance/flux-vm) | [FLUX Hardware](https://github.com/SuperInstance/flux-hardware)
- [cocapn-glue-core on crates.io](https://crates.io/crates/cocapn-glue-core)
- [Forgemaster — parent repo](https://github.com/SuperInstance/forgemaster)

## License

MIT
