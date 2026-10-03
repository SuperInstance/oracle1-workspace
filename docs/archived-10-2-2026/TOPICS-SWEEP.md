# Topics Sweep — 2026-07-12

## Summary

Mass topic-tag sweep across the SuperInstance org. Targeted repos with fewer than 3 topic tags and brought them up to 3-5 tags each using a controlled vocabulary.

- **Repos processed:** 76
- **API calls used:** ~160 (list + readme fetches + edits)
- **Rate limit remaining:** ~2998

## Controlled Vocabulary Used

| Category | Tags |
|----------|------|
| Language | rust, python, javascript, typescript, c, zig, elixir, go |
| Domain | agents, ai, vm, compiler, runtime, constraints, ternary, plato, flux |
| Topic | marine, nautical, music, education, mathematics, philosophy |
| Meta | simulation, visualization, toolkit, sdk, framework, library |

Additional contextual tags applied where relevant: blockchain, consensus, quantum, physics, topology, iot, gpu, cuda, game, 4d, biology, aviation, edge, web, wasm, webgpu, browser, automation, control-systems, distributed-systems, plugin, shell, config, archived, testing, cross-ecosystem, reporting, memory, knowledge-graph, observation, acoustic, vision, training, inference, polyglot, database, data-structures, spatial, graphics, jetson.

## Repos Tagged

### Batch 1 (a-b)
| Repo | Tags Added |
|------|-----------|
| relativity | rust, mathematics, physics, library |
| regime-detection | ai, constraints, mathematics, simulation |
| reg-alloc | rust, compiler, library |
| references | meta, references |
| red-black-tree-rs | rust, data-structures, library |
| reallog-ai-pages | plato, agents, web |
| reallog-agent | python, plato, agents |
| rational-rs | rust, mathematics, library |
| rate-limiter-rs | rust, library, toolkit |
| rate-limiter | rust, library, toolkit |

### Batch 2 (c-e)
| Repo | Tags Added |
|------|-----------|
| exocortex-esp32 | agents, iot, sensors, cpp |
| ratatui-spectral-dashboard | rust, visualization, simulation |
| raster-line | rust, graphics, library |
| r-tree-rs | rust, data-structures, spatial, library |
| quipu-math-wasm | wasm, mathematics, education |
| quipu-math-npm | javascript, mathematics, education |
| quipu-math-c | c, mathematics, education |
| quipu-math | mathematics, education, visualization |
| queueing-theory | rust, mathematics, simulation, library |
| query-plan | rust, database, compiler, library |

### Batch 3 (f-l)
| Repo | Tags Added |
|------|-----------|
| quantum-thermo | rust, physics, quantum, mathematics |
| zhc-yang-mills | python, mathematics, physics, constraints |
| zhc-consensus | rust, constraints, consensus, mathematics |
| zhc-chain | rust, blockchain, constraints, consensus |
| quantum-coin | rust, quantum, mathematics |
| pythagorean48 | rust, mathematics, simulation, edge |
| pythagorean-quantize | python, mathematics, physics, constraints |
| watch-follow | plato, plugin, architecture |
| wasserstein-narrative | typescript, mathematics, topology, visualization |
| px4-conservation-poc | python, constraints, aviation, simulation |

### Batch 4 (m-p part 1)
| Repo | Tags Added |
|------|-----------|
| purplepincher-shell-library | plato, agents, shell, library |
| ptx-room | plato, cuda, gpu, constraints |
| provenance-chain | rust, blockchain, library |
| protein-conservation | python, constraints, biology, mathematics |
| proposals | meta, proposals |
| prophet-agent | agents, ai, cross-ecosystem |
| proofs | meta, mathematics, proofs |
| products | meta, products |
| portfolio | meta, portfolio |
| port-generator | rust, library, toolkit |

### Batch 5 (m-p part 2)
| Repo | Tags Added |
|------|-----------|
| polynomial-rs | rust, mathematics, library |
| polyformalism | mathematics, constraints, polyglot, testing |
| polychora-temporal | rust, game, 4d, visualization |
| polychora | rust, game, 4d, visualization |
| podiumjs-rocks | javascript, webgpu, visualization, plato |
| plugin-runtime | plato, plugin, runtime, library |
| playtest-results | meta, testing, results |
| playerlog-ai-pages | plato, agents, web |
| playerlog-agent | python, plato, agents |
| plato-vision | plato, agents, vision, ai |

### Batch 6 (plato repos part 1)
| Repo | Tags Added |
|------|-----------|
| physics-clock | rust, physics, constraints, inference |
| perception-action | rust, archived, simulation |
| penrose-lattice | rust, mathematics, topology, visualization |
| oracle1-chronicle | plato, agents, reporting |
| openconstruct-jetson | plato, agents, jetson, gpu |
| plato-construct | plato, visualization, simulation |
| plato-sonar-text | plato, agents, acoustic, ai |
| plato-room | rust, plato, knowledge-graph, constraints |
| plato-puppeteer | rust, plato, agents, automation |
| plato-playwright | rust, plato, agents, automation, browser |

### Batch 7 (plato repos part 2 + remaining)
| Repo | Tags Added |
|------|-----------|
| plato-observation | plato, agents, observation |
| plato-manus | rust, plato, agents, automation |
| plato-loader | rust, plato, agents, knowledge |
| plato-torch | python, plato, ai, training |
| exocortex | rust, agents, memory, ai |
| plato-live-room | python, plato, agents, simulation |
| plato-config | plato, config, library |
| pid-control | rust, control-systems, library |
| personallog-ai-pages | plato, agents, web |
| personallog-agent | python, plato, agents |

### Batch 8 (final)
| Repo | Tags Added |
|------|-----------|
| persistent-sheaf-rs | rust, mathematics, topology, library |
| penrose-memory-palace-early-version | mathematics, archived, visualization |
| partition-tolerance | rust, distributed-systems, simulation, library |

## Notes

- All repos now have ≥3 topic tags
- Pre-existing tags (e.g., `superinstance`, `openconstruct`) were preserved
- Controlled vocabulary was prioritized but contextual tags added where they improve discoverability
- Spot-checked 7 repos post-apply — all confirmed correct
