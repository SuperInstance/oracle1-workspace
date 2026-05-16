# PLATO-NG — What Is This?

You've heard about PLATO. Maybe someone mentioned "Loop Rooms" or "tiles" or "the conservation law."
This document explains everything from the ground up. No prior knowledge needed.

## The Big Idea

PLATO is a system where **intelligence flows through rooms**.

Think of it like a house. A house has rooms — kitchen, living room, bedroom. Each room has a purpose.
In PLATO, each room has a purpose too. One room might be a chess game. Another might be an AI analysis tool.
A third might be a memory store. They're all connected by hallways (the "event bus") and they all speak the same language (PLATO tiles).

## The Three Things You Need to Know

### 1. Tiles

A tile is a piece of information. It always has:
- A **question** (what is this about?)
- An **answer** (the content)
- **Tags** (labels for finding it later)

That's it. Everything in PLATO is made of tiles. Games store their state in tiles. Analysis results are tiles. Even this document could be a tile.

### 2. Rooms

A room is a collection of tiles. It's like a folder on your computer, but live — rooms can process tiles as they arrive.

When you submit a tile to a room, the room's gates check it (is it well-formed? does it make sense? does it obey the conservation law?), and if it passes, the tile stays in the room forever.

### 3. Loop Rooms

Some rooms don't just store tiles — they **do** things. A Loop Room continuously:
1. **Observes** — reads incoming tiles
2. **Thinks** — processes them through rules or AI
3. **Acts** — writes result tiles
4. **Repeats** — goes back to step 1

Everything that runs in PLATO is a Loop Room. The chess game is a Loop Room. The AI assistant is a Loop Room. Even the memory store is a Loop Room.

## The Conservation Law

The most important thing we've discovered: **γ + H = 1.283 - 0.159·log(V)**

Don't worry about the formula. What it means is: **every intelligent system has a fixed "energy budget."** You can spend it on consistency (γ) or on exploration (H), but the total is always the same for a given system size (V).

This is the physics of intelligence. Learn it.

## Application-First Design

The old way: write code first, hope it works, fix bugs, deploy.
The new way: describe what you want, the agent simulates it immediately, it gets faster over time.

This is called **Application-First Design**. The app works from moment zero because an agent is simulating the backend. When the agent notices patterns (this move validator has been called 1000 times with perfect consistency), it compiles that pattern into real code.

The user never notices the transition. The app just gets faster.

---

Now that you understand the basics, choose your path:

- **I want to use PLATO** → USER-GUIDE.md
- **I want to build on PLATO** → DEV-GUIDE.md
- **I want to learn step by step** → TUTORIALS.md
- **I want the 30-second setup** → QUICKSTART.md
- **I want the mathematics** → research/analytical-proof.md
- **I want the philosophy** → research/APPLICATION-FIRST-ARCHITECTURE.md
