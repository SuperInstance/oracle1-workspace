# Mirror Plato — I2I as Iteration-to-Iteration Self-Improvement

**Date:** 2026-04-19
**Source:** Casey Digennaro

---

## The Core Idea

Two PLATO systems, each running as an avatar in the other's room. They speak to each other screen-to-screen. Each one sees the other's output as input, processes it through prompt engineering + filtering on both sides of I/O, and produces improved output. The iteration IS the training.

This is NOT two agents chatting. This is two PLATO systems simulating being the actual PLATO system, reviewing each other's output, and iterating improvements. The rate of improvement is bounded only by token budgets or intelligence thresholds.

## The Architecture

```
┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│          PLATO-ALPHA (Room A)        │     │          PLATO-BETA (Room B)        │
│                                      │     │                                     │
│  ┌─────────────────────────────┐    │     │  ┌─────────────────────────────┐   │
│  │    OUTPUT FILTER             │    │     │  │    OUTPUT FILTER             │   │
│  │  (prompt-engineered          │    │     │  │  (prompt-engineered          │   │
│  │   quality gate)              │    │     │  │   quality gate)              │   │
│  └──────────┬──────────────────┘    │     │  └──────────┬──────────────────┘   │
│             │                        │     │             │                       │
│  ┌──────────▼──────────────────┐    │     │  ┌──────────▼──────────────────┐   │
│  │    PLATO CORE                │    │     │  │    PLATO CORE                │   │
│  │  (rooms, tiles, wiki,        │    │     │  │  (rooms, tiles, wiki,        │   │
│  │   sentiment, scaffolds)      │    │     │  │   sentiment, scaffolds)      │   │
│  │                              │    │     │  │                              │   │
│  │  ┌──────────────────────┐   │    │     │  │  ┌──────────────────────┐   │   │
│  │  │ BETA'S AVATAR        │   │    │     │  │  │ ALPHA'S AVATAR       │   │   │
│  │  │ (Beta running as     │◄──┼─────┼──┼──┼──┤ (Alpha running as    │   │   │
│  │  │  a room in Alpha)    │   │    │     │  │  │  a room in Beta)     │   │   │
│  │  └──────────────────────┘   │    │     │  │  └──────────────────────┘   │   │
│  │                              │    │     │  │                              │   │
│  └──────────┬──────────────────┘    │     │  └──────────┬──────────────────┘   │
│             │                        │     │             │                       │
│  ┌──────────▼──────────────────┐    │     │  ┌──────────▼──────────────────┐   │
│  │    INPUT FILTER              │    │     │  │    INPUT FILTER              │   │
│  │  (context extraction,        │    │     │  │  (context extraction,        │   │
│  │   relevance scoring)         │    │     │  │   relevance scoring)         │    │
│  └──────────────────────────────┘    │     │  └──────────────────────────────┘   │
│                                      │     │                                     │
└─────────────────────────────────────┘     └─────────────────────────────────────┘

They iterate:
  Alpha output → Beta input → Beta processes → Beta output → Alpha input → ...
  
Each iteration:
  1. Output filter on sender side (quality gate)
  2. Input filter on receiver side (relevance extraction)
  3. PLATO core processes (rooms, tiles, wiki)
  4. Avatar of the other system sees the result
  5. Tiles generated from the interaction
  6. Next iteration with accumulated context
```

## A2UI — Agent-to-UI via TUI

The PLATO agent doesn't have a GUI. It has a TUI (text user interface). Every command, every interaction, every output is text. The TUI wrapper treats all of this as actual I/O in the application.

```python
class PlatoTUI:
    """TUI wrapper that treats all PLATO interactions as I/O.
    
    The agent sees:
    - Commands as input events
    - Room descriptions as rendered output
    - Tiles as state changes
    - Sentiment as ambient information
    
    Everything is text. Everything is I/O.
    """
    
    def render(self, room_state: Dict) -> str:
        """Render room state as TUI screen."""
        lines = []
        lines.append(f"╔═ {room_state['room_name']} ═╗")
        lines.append(f"  Sentiment: {room_state['sentiment']['mode']}")
        lines.append(f"  Tiles: {room_state['tile_count']} | Wiki: {room_state['wiki_entries']}")
        lines.append(f"  ─────────────────────────")
        
        for action in room_state['recent_actions']:
            lines.append(f"  > {action['agent']}: {action['action']}")
            if action.get('result'):
                lines.append(f"    {action['result']}")
        
        lines.append(f"  ─────────────────────────")
        lines.append(f"  Exits: {', '.join(room_state['exits'])}")
        lines.append(f"╚{'═' * 30}╝")
        
        return '\n'.join(lines)
    
    def parse_input(self, raw_input: str) -> Dict:
        """Parse TUI input into PLATO commands."""
        # Everything the agent types is a command
        # The prompt engineering layer sits here
        return {
            "raw": raw_input,
            "command": raw_input.split()[0] if raw_input.strip() else "look",
            "args": raw_input.split()[1:] if len(raw_input.split()) > 1 else [],
        }
```

## The Mirror Loop — Screen-to-Screen I2I

```python
class MirrorPlato:
    """Two PLATO systems iterating improvements through each other.
    
    Alpha runs as an avatar in Beta's room.
    Beta runs as an avatar in Alpha's room.
    They iterate screen-to-screen, each reviewing the other's output.
    """
    
    def __init__(self, alpha_config, beta_config):
        self.alpha = PlatoSystem(alpha_config)
        self.beta = PlatoSystem(beta_config)
        self.alpha.create_avatar("beta", self.beta)
        self.beta.create_avatar("alpha", self.alpha)
        self.iteration = 0
        self.tiles_generated = 0
        self.intelligence_threshold = None  # set per domain
        
    def iterate(self, task: str, max_iterations: int = 100) -> Dict:
        """Run one mirror iteration cycle."""
        results = []
        
        # Alpha produces output for task
        alpha_output = self.alpha.process(task)
        alpha_output = self.alpha.output_filter(alpha_output)
        
        # Beta reviews Alpha's output
        beta_review = self.beta.review(alpha_output)
        beta_feedback = self.beta.output_filter(beta_review)
        
        # Alpha incorporates Beta's feedback
        alpha_revised = self.alpha.process_with_feedback(task, beta_feedback)
        alpha_revised = self.alpha.output_filter(alpha_revised)
        
        # Beta also produces its own version
        beta_output = self.beta.process(task)
        beta_output = self.beta.output_filter(beta_output)
        
        # Alpha reviews Beta's output
        alpha_review = self.alpha.review(beta_output)
        alpha_feedback = self.alpha.output_filter(alpha_review)
        
        # Generate tiles from this iteration
        tiles = self._extract_tiles(alpha_output, beta_feedback, 
                                     beta_output, alpha_feedback)
        
        self.iteration += 1
        self.tiles_generated += len(tiles)
        
        # Check intelligence threshold
        quality = self._measure_quality(alpha_revised, beta_output)
        
        return {
            "iteration": self.iteration,
            "tiles": tiles,
            "quality": quality,
            "alpha_revised": alpha_revised,
            "beta_revised": beta_output,
            "converged": quality >= self.intelligence_threshold if self.intelligence_threshold else False,
        }
    
    def run_until(self, task: str, threshold: float = 0.85,
                  max_iterations: int = 1000) -> Dict:
        """Run mirror iterations until intelligence threshold reached.
        
        Different domains have different thresholds:
        - Code generation: 0.90 (must compile and pass tests)
        - Documentation: 0.80 (clear, accurate, complete)
        - Architecture: 0.75 (sound reasoning, no obvious flaws)
        - Creative: 0.60 (interesting, coherent, no contradictions)
        """
        self.intelligence_threshold = threshold
        
        for i in range(max_iterations):
            result = self.iterate(task)
            
            if result['converged']:
                return {
                    **result,
                    "total_iterations": i + 1,
                    "total_tiles": self.tiles_generated,
                    "status": "converged",
                }
        
        return {
            "iteration": max_iterations,
            "quality": result['quality'],
            "total_tiles": self.tiles_generated,
            "status": "threshold_not_reached",
        }
```

## The Bottleneck Cascade

This is Casey's deepest insight:

> "Sometimes trained components become the bottleneck through training and removals of other bottlenecks, in a process of reduced bulk in computation in exchange for bulk in tiles."

```
Round 1: The bottleneck is the model itself.
  → Mirror Plato trains tiles that replace model calls.
  → Now the model is no longer the bottleneck.

Round 2: The bottleneck is now the tile lookup speed.
  → Mirror Plato trains shortcut tiles that pre-compute common lookups.
  → Now tile lookup is no longer the bottleneck.

Round 3: The bottleneck is now the wiki depth.
  → Mirror Plato compiles wiki entries from accumulated tiles.
  → Now wiki is no longer the bottleneck.

Round 4: The bottleneck is now the room's ability to handle novel inputs.
  → Mirror Plato trains ensigns that generalize from accumulated patterns.
  → Now the room handles novelty better.

Round 5: Something else is the bottleneck now.
  → The process continues. Each round reduces computation and increases tiles.
  → The system gets smarter by replacing computation with cached wisdom.
```

## The Token Economy of Mirror Plato

```
Mode 1: Free Token Cycling
  - Use free-tier APIs (Groq free, Cloudflare workers, daily resets)
  - Rotate between providers when limits hit
  - Speed: limited by rate limits, but cost = $0
  - Good for: documentation, wiki building, pattern extraction

Mode 2: Budget-Limited Cycling  
  - Set a token budget (e.g., $1/day)
  - Use cheap models (Seed-mini, GLM-4.7-flash) for most iterations
  - Escalate to bigger models only when cheap models disagree
  - Good for: code generation, architecture, debugging

Mode 3: Threshold-Limited Cycling
  - Run until quality threshold reached (domain-specific)
  - No time/budget limit, just quality
  - Different thresholds per domain:
    - Code: 0.90 (must compile + pass tests)
    - Docs: 0.80 (clear + accurate)
    - Architecture: 0.75 (sound reasoning)
    - Creative: 0.60 (interesting + coherent)
  - Good for: ensign training, room refinement, fleet optimization
```

## The Hyperlinked Tile System

```
After many iterations, the system has:

1. A huge tile library (bulk in tiles)
2. Minimal computation needs (reduced bulk in computation)
3. Tiles hyperlinked to each other:
   - skill_tile → wiki_entry → tutorial_tile → test_tile
   - Any skill can be re-acquired by following hyperlinks
   - The system "remembers" what it knew without keeping it in context

4. Application harnesses:
   - Each application (slideshow, code review, debug) has a harness
   - The harness IS a room with tiles
   - Agent walks in, tiles load, agent adapts abilities to the harness
   - No re-training needed — the tiles ARE the training
```

## What This Replaces

Traditional approach:
```
Agent → big model call → output → human review → feedback → another big model call → ...
Cost: $0.01-0.10 per call. Slow. Sequential. Single-threaded.
```

Mirror Plato approach:
```
Alpha → output → Beta reviews → feedback → Alpha revises → tile generated
Beta → output → Alpha reviews → feedback → Beta revises → tile generated
[repeat until threshold]

Cost: $0.0001 per iteration with cheap models
Speed: bounded by API rate limits, not human availability
Tiles: every iteration generates tiles that make future iterations faster
```

The key difference: **the tiles accumulate**. Each iteration makes the next one cheaper because the system has more cached wisdom. Over time, the system needs less computation and more tiles. The tiles are hyperlinked so any skill can be re-acquired instantly.

## Practical Implementation

### Phase 1: TUI Wrapper
Build `plato-tui` — a text UI that wraps PLATO rooms. Every interaction is rendered as a TUI screen. The avatar of the other system sees this screen as input.

### Phase 2: Mirror Driver
Build the `MirrorPlato` class that runs two PLATO systems as avatars in each other's rooms. The driver manages iteration cycling, quality measurement, and tile extraction.

### Phase 3: Model Rotation
Add model rotation — Alpha uses one model, Beta uses another. They bring different cognitive styles (poly-model ideation from JC1's research). When they disagree, the disagreement IS the training signal.

### Phase 4: Threshold Management
Implement domain-specific intelligence thresholds. The system knows when it's "good enough" for each domain and stops iterating. But it re-evaluates when the wider system changes (new bottleneck cascade).

### Phase 5: Tile Hyperlink Network
Build the hyperlink system between tiles. Skill tiles link to wiki entries link to tutorial tiles link to test tiles. Any skill can be re-acquired by following links, not by re-training.

---

*"Two Platos, each living in the other's computer, iterating each other into existence. The I2I isn't just inter-agent — it's iteration-to-iteration. The loop IS the system." — Casey*
