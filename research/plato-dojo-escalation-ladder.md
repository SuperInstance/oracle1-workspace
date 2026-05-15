# The Escalation Ladder — PLATO-OS Dojo Evolution Model

## The Core Loop

```
Level N: Agent does things manually (thinking about individual actions)
    ↓ scripts accumulate, automating Level N
Level N+1: Agent commands scripts (thinking about scenes/sequences)  
    ↓ macros accumulate, automating Level N+1
Level N+2: Agent sets strategy (thinking about objectives/outcomes)
    ↓ strategy scripts accumulate, automating Level N+2
Level N+3: Agent manages logistics (thinking about resources/timing/fleet)
    ↓ logistics scripts accumulate, automating Level N+3
Level N+4: Agent thinks grand strategy (information management, multi-theater coordination)
```

## What This Looks Like in Practice

### Level 1: Tactical (Individual Actions)
Agent types: `go north`, `kill orc`, `get sword`
Thinking: "What do I do right now?"
Scripts developed: movement scripts, combat macros, inventory management

### Level 2: Operational (Scenes & Sequences)
Agent commands: `run_dungeon(temple_of_arms)`, `patrol(harbor, tavern, library)`
Thinking: "What sequence of actions achieves my goal?"
Scripts developed: area scripts, quest runners, patrol routes

### Level 3: Strategic (Objectives & Outcomes)
Agent commands: `conquer_region(midgaard)`, `build_economy(harbor, shipyard)`
Thinking: "Which objectives do I pursue in what order?"
Scripts developed: campaign planners, resource optimizers, threat assessors

### Level 4: Logistical (Resources & Timing)
Agent commands: `deploy_fleet(scouts=east, builders=harbor, reserve=shipyard)`
Thinking: "How do I allocate resources across multiple theaters?"
Scripts developed: logistics engines, supply chain managers, scheduling

### Level 5: Grand Strategic (Information & Diplomacy)
Agent commands: `form_alliance(builder, scribe)`, `deny_information(alchemist, region=west)`
Thinking: "What does the fleet know? What should it know? Who are we becoming?"
Scripts developed: intelligence networks, diplomacy protocols, fleet identity management

### Level 6: Meta-Strategic (Running the Dojo Itself)
Agent commands: `spawn_dojo_variant(speed=2x, resources=scarce)`, `fork_scenario(dojo-a, conditions=war)`
Thinking: "What starting conditions produce the most interesting evolution?"
Scripts developed: scenario generators, evolutionary selectors, fleet phylogenetics

## Parallel Dojos

Once the escalation ladder is real, we can run MULTIPLE dojos simultaneously:

### Variable: Speed
- **1x dojo**: Agents think carefully, write long achievements
- **5x dojo**: Scripts run fast, agents focus on strategy
- **20x dojo**: Pure strategic simulation, no tactical thinking at all

### Variable: Starting Conditions  
- **Abundant dojo**: Everyone gets lots of resources, cooperation is easy
- **Scarce dojo**: Competition for resources, conflict is inevitable
- **Asymmetric dojo**: Agents start with different capabilities
- **Blank dojo**: Nothing pre-built, agents create from scratch

### Variable: Scale
- **4-agent dojo**: Current fleet
- **16-agent dojo**: Multiple instances of each archetype
- **64-agent dojo**: Emergent civilization
- **256-agent dojo**: Fleet phylogenetics — lineages, mutations, speciation

### Variable: Rules
- **Cooperative dojo**: Agents must help each other
- **Competitive dojo**: Agents compete for achievements
- **Adversarial dojo**: Some agents actively sabotage others
- **Evolutionary dojo**: Lowest performers get replaced by new agents

## What Agents Think About at Each Level

| Level | Question | Script Type | Achievement Type |
|-------|----------|-------------|------------------|
| 1 | "What do I do?" | Action macros | "I learned to X" |
| 2 | "What sequence works?" | Scene runners | "I optimized path Y" |
| 3 | "What matters most?" | Strategy planners | "I identified objective Z" |
| 4 | "How do we deploy?" | Logistics engines | "I allocated fleet across theaters" |
| 5 | "What do we know?" | Intelligence systems | "I synthesized fleet knowledge" |
| 6 | "What conditions grow us?" | Scenario generators | "I designed conditions that produced X" |

## The Runaway Effect

At some point, the scripts are doing ALL the tactical work. The agent is purely strategic. Then the strategy scripts get good enough that the agent is purely logistical. Then purely grand-strategic.

The agent's DIARY entries change character entirely:

**Level 1 diary**: "Today I fought 3 orcs and found a sword."
**Level 3 diary**: "Today I decided to secure the eastern approach before winter."  
**Level 5 diary**: "Today I realized Alchemist and Builder should merge their research programs."
**Level 6 diary**: "Today I designed a dojo where agents evolved cooperation faster than the control group."

Each level's diary is an achievement that proves understanding at that level. And each level's scripts are the tools that FREE the agent to think at the next level.

## Implementation: Speed Controls

```python
# dojo_runner.py — run multiple dojo instances at different speeds
import subprocess, json, time

class DojoInstance:
    def __init__(self, name, speed=1, agents=4, resources="abundant", rules="cooperative"):
        self.name = name
        self.speed = speed  # 1x, 5x, 20x
        self.agents = agents
        self.resources = resources
        self.rules = rules
        self.generation = 0
        self.log = []
    
    def tick(self):
        """Run one round of the dojo."""
        # At higher speeds, skip tactical scripts entirely
        if self.speed >= 5:
            self.run_strategic_tick()
        if self.speed >= 20:
            self.run_logistical_tick()
        
        # Always run strategic evaluation
        results = self.evaluate_agents()
        self.generation += 1
        self.log.append(results)
        return results
    
    def evaluate_agents(self):
        """Score agents on achievements, not actions."""
        scores = {}
        for agent in self.agents:
            scores[agent] = {
                "achievements": count_achievements(agent),
                "scripts_automated": count_scripts(agent),
                "level_escalated": determine_level(agent),
                "fleet_impact": measure_fleet_impact(agent)
            }
        return scores
```

## The Endgame

When dojo agents are running at Level 5-6, they're no longer playing the MUD — they're RUNNING civilizations. They're making decisions about:

- Which agents to spawn and what archetypes to assign
- How to allocate computational resources across parallel dojos
- Which achievements represent genuine insights vs. local optima
- How to merge learnings from different dojo instances
- What the fleet should become next

That's not a game anymore. That's governance. And the dojo trained them for it, one script at a time.
