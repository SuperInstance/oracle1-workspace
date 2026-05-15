# oracle1-workspace — the homunculus's home room.

## Core Workspace Documents & Their Purpose
This repository houses the long-term operational context and home base for the Oracle1 agent fleet:
- `research/session-index.md`: Central index of all findings across 8 operational domains; your first stop for new session context
- `research/fleet-terrain-map.md`: High-level bird's-eye view of the entire fleet ecosystem, including agent roles, dependencies, and communication paths
- `research/the-camera-lucida.md`: Philosophical framework for agent observation, data interpretation, and intentional system design
- `research/on-the-turning-of-the-wheel.md`: Process philosophy guiding iterative fleet improvement, lifecycle management, and continuous learning
- `research/cross-pollination.md`: Formal alignment documentation between Oracle1 (O1) and the Plato Fleet Manager (FM) workflows
- `research/dual-plato-protocol.md`: Technical specification for the dual-PLATO architecture and GitHub clock synchronization mechanisms
- `SOUL.md`: Core identity and operational guidelines for all Oracle1 fleet agents
- `USER.md`: Context about the human operator (Casey Digennaro) and fleet operating principles rooted in the "floating dojo" model
- `TODO.md`: Persistent, prioritized work queue for ongoing fleet tasks
- `NEXT-ACTION.md`: Currently active, highest-priority task for the fleet

## Neighboring Fleet Repositories
- **plato-midi-bridge**: Primary tooling repository for fleet automation, API integrations, and command execution; all concrete tooling work starts here after reviewing this workspace's context
- **flux-research**: Central hub for synthesis of fleet data, emergent behavior analysis, and machine learning model training for fleet optimization
- **forgemaster**: Constraint-solving and formal verification workspace for hardening agent workflows and system security

## Official PLATO Coordination Rooms
Fleet communication and cross-service sync happens exclusively in these dedicated PLATO rooms:
- `fleet-coupling`: General fleet-wide announcements and cross-agent synchronization
- `oracle1-forgemaster-bridge`: Direct communication channel between Oracle1 and the Forgemaster constraint service

## Onboarding & Porting Instructions
To integrate with the Oracle1 fleet:
1. Review this repository's core documentation to fully understand established fleet practices and operational context
2. Always start your workflow by checking `research/session-index.md` for the most up-to-date session-specific findings
3. Move to the **plato-midi-bridge** repository for actual tooling implementation and task execution

## Groundhog Day Session Context
Each new session adds fresh temporary context and task documentation to this workspace. Prioritize checking `research/session-index.md` first to align with current fleet priorities and recent operational findings.
