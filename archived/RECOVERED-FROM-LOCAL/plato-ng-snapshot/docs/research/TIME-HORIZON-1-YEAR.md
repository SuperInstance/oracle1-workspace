# TIME HORIZON: 1 Year — May 2027

> Date written: 2026-05-15 | Horizon: May 2027 | Strategist: Oracle1

---

## 1. The Release — May 2027

PLATO-NG v1.0 ships with the conservation law encoded at the kernel level. The tripartite system (Instinct, Afterlife, Relay) has been running in production across 5+ real fleets — small boat to mid-vessel scale. Documentation at fleet-math v1.0 formalizes constraint theory for multi-agent swarms. Users onboard new agents in under 30 seconds. Forgemaster delivers weekly experiments without human intervention. The open-source community has 40+ contributors, and two independent teams have forked the kernel for non-maritime swarm robotics. Cocapn is the reference implementation for conservation-guaranteed multi-agent compute.

---

## 2. Work Backward: Milestones

### Q3 2026 (Aug 2026) — The Kernel Freeze
| Milestone | Target | Description |
|-----------|--------|-------------|
| Conservation kernel v1.0-rc1 | July 2026 | First release candidate of `plato-kernel` with conservation law enforcement |
| Instinct v0.8 | Aug 2026 | Instinct behavior engine feature-complete, beta testers onboarding |
| Fleet-math spec stable | Aug 2026 | Conservation law formalization frozen for documentation |
| PLATO-NG API surface frozen | Aug 2026 | No breaking changes after this date |

### Q4 2026 (Nov 2026) — The Beta
| Milestone | Target | Description |
|-----------|--------|-------------|
| PLATO-NG public beta | Sep 2026 | Open beta with curated test fleet (5 vessels) |
| Tripartite integration tests | Oct 2026 | Instinct → Afterlife → Relay end-to-end tests pass |
| Conservation law paper | Nov 2026 | ArXiv preprint, open review period |
| 10+ external contributors | Nov 2026 | Community growth target, onboarding documentation done |

### Q1 2027 (Feb 2027) — The Polish
| Milestone | Target | Description |
|-----------|--------|-------------|
| Performance and security audit | Dec 2026 | External audit of kernel, DCS, and network layer |
| v1.0-rc2 | Jan 2027 | Bugfix release, audit findings addressed |
| Fleet documentation complete | Feb 2027 | fleet-math v1.0 final, operator guides, API reference |
| 5 production fleets running | Feb 2027 | Real users, real deployments, real feedback closed |

### Q2 2027 (May 2027) — The Ship
| Milestone | Target | Description |
|-----------|--------|-------------|
| PLATO-NG v1.0 release | May 2027 | Tagged release, versioned documentation, migration guides |
| fleet-math v1.0 | May 2027 | Published monograph alongside release |
| Community summit | May 2027 | Virtual event, early adopter talks, roadmap preview |

---

## 3. This Week — Starting Monday, May 18

1. **Freeze the conservation kernel spec.** Lock the constraint algebra for `plato-kernel`. No more changes to the core equation until v1.0-rc1 in July. Write the architecture decision record (ADR) declaring the freeze.

2. **Write the PLATO-NG v1.0 API surface document.** One page, no ambiguity. Every endpoint, every message type, every error code. This becomes the contract for all subprojects.

3. **Draft the fleet-math outline.** Table of contents and chapter summaries for the conservation law monograph. Identify the 3 hardest sections and assign them as parallel work.

4. **Tag a weekly-snapshot release of the current kernel.** Even if it's not v1.0 yet, a tagged, buildable release makes onboarding possible. CI must pass green.

5. **Open the first external beta-tester issue.** Pick one potential adopter (JetsonClaw1 or a known community member), write the onboarding issue, test the flow end-to-end, and close the loop before Friday.

---

*Rollup: 1 year out is Q2 2027. The work between now and the kernel freeze (July) is the most leveraged — everything else flows from the conserved kernel. The fleet is the test. The math is the foundation. Ship the kernel, then the system grows itself.*
