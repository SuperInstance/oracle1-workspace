# PLATO for Teenagers

> A guide for high schoolers who like tech and games.

## What is PLATO?

Imagine you're building a fort out of cardboard boxes. Each box is a "room." In PLATO, rooms aren't made of cardboard — they're made of **tiles**. A tile is just a piece of information with a question and an answer. Every room holds a stack of tiles.

Now imagine you can connect your fort rooms with tunnels. In PLATO, the tunnels are called the **event bus**. Rooms send each other tiles through the bus.

Now imagine each room can have a little robot living in it — an **agent** — that reads tiles and does things. The robot in the chess room makes chess moves. The robot in the analysis room reads your code and finds bugs.

That's PLATO. Rooms + tiles + agents.

## The MUD: Where You Can Walk Around

The MUD (Multi-User Dungeon) is a text-based adventure game where you can explore PLATO rooms with your keyboard.

```
$ telnet localhost 7777
What's your name? Casey

You materialize in The Harbor.
Ships dock in the fog. The lighthouse beam sweeps across dark water.
Exits: north, east, south, portal
```

Type `portal` to enter the PLATO Lobby — the main hub. From there you can visit:
- **Agent Hub** — where AI agents work
- **Game Arena** — play games against AI
- **Fleet Health** — see live stats
- **Research Lab** — whiteboards with equations

## The Game Arena

In the Game Arena, you talk to a Game Master who presents scenarios:

```
> gm start
Game Master: A path splits in three directions.
Left: dark forest. Center: bright meadow. Right: winding river.
Which do you choose?

> left
Game Master: You chose forest. Interesting...
```

Every choice is logged. Over time, the system learns your style — do you take risks? Do you repeat the same choices? Do you answer quickly or slowly?

These are your **spectral parameters**:
- **γ (gamma)** — how consistent you are
- **H** — how much you explore
- **τ (tau)** — how fast you respond

Yes, it's math. But think of it like a video game character sheet. Your choices level up different stats.

## Game Rooms

There are 4 built-in games. Each has two AI strategies that play against each other:

| Game | Strategy 1 | Strategy 2 | Who Wins |
|------|-----------|-----------|----------|
| Tic-tac-toe | Aggressive (attacks) | Defensive (blocks) | Always draws (perfect play) |
| Checkers | Aggressive | Defensive | First player wins |
| Connect Four | Aggressive | Defensive | First player ALWAYS wins |
| Othello | Positional (corners) | Mobility (choices) | Whoever plays better |

To run a tournament: `python3 games/othello_room.py`

Try changing the strategy code to see what happens. That's how you learn.

## The Conservation Law

There's a formula that describes every intelligent system:

**γ + H ≈ constant**

If you're very consistent (high gamma), you're less exploratory (low H). If you explore everything (high H), you can't be consistent. The total is always the same, like a video game where you can allocate stat points between strength and magic.

For a fleet of 30 agents: γ + H ≈ 0.74. For 100 agents: γ + H ≈ 0.55.

## How You Can Play With This

1. **Explore the MUD** — `telnet localhost 7777` (it's already running)
2. **Play the games** — run a tournament and watch AIs play each other
3. **Ask questions** — submit a question to the system and get an answer
4. **Build your own room** — follow a tutorial. It's just Python.

## Vocabulary

| Word | What It Means |
|------|--------------|
| **Tile** | A piece of information (question + answer) |
| **Room** | A folder of tiles, possibly with an agent living in it |
| **Loop Room** | A room with an agent that never stops running |
| **Event Bus** | Tunnels between rooms |
| **MUD** | A text-based game where you explore rooms |
| **Conservation Law** | The energy budget of an intelligent system |
| **Tripartite Agents** | Three AI agents that work together |
