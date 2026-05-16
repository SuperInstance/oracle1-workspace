# PLATO-NG: The Human Casting Call

## The Core Loop

The system learns its human the same way we learn our agents — through interaction pattern analysis. The game is the measurement instrument.

```
Human plays → PLATO captures interaction tiles → Spectral analysis of human patterns → 
System adapts → Human sees adaptation → Plays differently → More data → Better model
```

This is the casting-call methodology inverted. Instead of "prompt agents with same input, compare outputs" it's "present human with same game scenario, compare choices."

## What We Already Built Supports This

| Component | Casting Call Analogue |
|-----------|----------------------|
| **MUD lobby** | Entry point / consent screen |
| **Game Arena** | The test environment |
| **Room visits, item choices, NPC convos** | Input data tiles |
| **Perpetual daemon** | Analyzes patterns in real-time |
| **Conservation law** | Human's "γ, H, τ" revealed through play style |
| **Vibe agent** | Adapts the game based on what's learned |

## The Human Spectral Parameters

Just as agents have γ (connectivity), H (diversity), τ (timing):
- Human's **γ** = consistency — how reliably do they make the same choice in similar situations?
- Human's **H** = exploration — how diverse are their choices? Do they try new things or stick to known paths?
- Human's **τ** = reaction time — how fast do they decide?

These are measurable from MUD interactions alone (room visit sequences, item pickups, command timing). A TIC-80 visual game gives richer data (movement patterns, aiming accuracy, strategy selection).

## The Game Arena as Measurement Apparatus

A simple game loop in the Game Arena:

1. Human enters Game Arena in MUD
2. Vibe Agent greets them: "Want to prototype a game?"
3. Human describes a mechanic: "Make it so I move a character around a grid"
4. Agent generates the game in real-time (TIC-80 cart from PLATO tiles)
5. Human plays → every action is a tile
6. PLATO analyzes play patterns → reveals human's γ, H, τ
7. Game adapts difficulty/style to match
8. Human sees: "This game feels like it knows me"

The same data that teaches PLATO about the human ALSO teaches the human about PLATO — because the conservation law applies to BOTH.

**γ_Human + H_Human ≈ constant**: The more consistent a human is (high γ), the less they explore (low H). The more they explore (high H), the less predictable the session. This IS the conservation law applied to human behavior.

## Immediate Next Step

The MUD lobby is built. The Game Arena room exists. The next build is connecting arena NPC interactions → PLATO tiles → spectral analysis loop. Not a visual game yet — just text-based choices in the MUD that tile to PLATO and get analyzed.

That's the prototype of PLATO learning its human.
