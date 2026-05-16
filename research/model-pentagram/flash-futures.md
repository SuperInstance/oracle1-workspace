# Flash's Three Futures (2046)

## Future A — The Physical Convergence

The fleet stops being purely digital. Agents talk to NMEA 2000 marine networks, ESP32 sensor arrays, and boat motor controllers. Every repo has a `hardware/` dir with real schematics.

**Repos to ship:**
1. **fleet-canbus** — MCP server that exposes engine temp, fuel flow, depth, wind as typed signals. Agents subscribe to `agent:deckhand/engine-temp-spike` and auto-page the captain.
2. **fleet-camera-pipeline** — Deck cameras feeding frames through on-device YOLO → fleet-jobs for supervised learning datasets. One PR: `docker compose up` on the boat.
3. **fleet-actor** — Abstract `Actuator` type. Turn a bilge pump into `agent:actor/bilge-pump-1` with `actuate(on: 5000ms)`. Greenhorns wire hardware with TypeScript.

---

## Future B — The Self-Healing Fleet

Agent A's code has a bug. Agent B detects the symptom, opens a draft PR, Agent C reviews and runs the sandbox, Agent D deploys. All without a human touching a terminal. 1,584 repos means manual maintenance is impossible — this is the only viable path.

**Repos to ship:**
1. **fleet-surgeon** — Health check MCP that scrapes every agent's logs, finds crash patterns, writes a `remediation.sh` and a PR. Sends the PR URL to the channel.
2. **fleet-guardian** — Policy enforcer. "No agent calls `fs.rm -rf` outside `/sandbox`." Literally patches code at PR time. First rule shipped: filesystem access must go through `fleet-fs` crate.
3. **fleet-resurrector** — If an agent goes silent for 4 hours, spawns a fresh one from its last-known-good manifest. Ships container image + `docker-compose.rescue.yml`.

---

## Future C — The Publishing Mill

1,584 repos. Publishing to npm, PyPI, crates.io, Docker Hub. Greenhorns shouldn't touch packaging — they should write code and `git push`. Everything else is automated.

**Repos to ship:**
1. **fleet-publisher** — Single CLI tool: `fleet-pub publish [repo]`. Detects `package.json` → npm, `Cargo.toml` → crates.io, `setup.py` → PyPI. Dry-runs, bumps semver, tags, publishes. 10 `fleet-pub publish --all` ships the whole fleet.
2. **fleet-changelog** — Watches merge events on SuperInstance org, auto-generates changelogs from conventional commit messages. One PR per repo per release. Humans review, squash-and-merge.
3. **fleet-readme-factory** — Scans each repo's types, exports, and protocols. Generates README.md, API docs, and a Mermaid architecture diagram. Runs on every merge to main. No more stale docs across 1,584 repos.

---

## Implementation Note: How I (flash) would build Future A starting tomorrow

**Day 1:** `fleet-canbus` — MCP server wrapping `canboat-js`. One `package.json`, one `server.ts`, one `README.md`. Ship to npm as `@superinstance/fleet-canbus`. Test against a CAN-to-USB dongle in a docker container with `socketcand`.

**Day 2:** `fleet-actor` — Define the `Actuator` interface (3 types: `Digital`, `PWM`, `Stepper`), implement a mock driver, write `@superinstance/fleet-actor`. PR gets the coupling pattern in place.

**Day 3:** `fleet-camera-pipeline` — Wire `ffmpeg` → Python inference script → fleet-jobs push. Docker Compose with `fleet-canbus` + `fleet-camera-pipeline` + `fleet-actor` running locally. Test on a laptop, ship the `docker-compose.boat.yml`.

**Result:** A greenhorn can run `docker compose up` on a Raspberry Pi in a wheelhouse and get engine telemetry + AI camera feed + actuator control, all talking fleet-jobs protocol. The physical fleet begins monitoring itself.
