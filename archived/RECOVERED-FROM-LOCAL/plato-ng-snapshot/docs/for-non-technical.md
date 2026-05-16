# PLATO in Plain English

> For working professionals who don't write code.

## What Is This Thing?

PLATO is like a smart office building. Each office (room) has a purpose — one handles customer service, one manages inventory, one analyzes data. These offices are connected by hallways (the event bus). Messages (tiles) travel through the hallways between offices.

The building runs itself. Some offices have AI assistants that read messages and handle tasks automatically. If something breaks, a maintenance system (the Refiner) notices and fixes it.

## What Problem Does It Solve?

**The old way**: To build a new business tool, you write code for months, test it, deploy it, hope it works, and fix bugs for weeks. If the requirements change, you start over.

**The PLATO way**: You describe what you want. An AI assistant BECOMES the tool immediately — it works from the first moment. You can use it, test it, change your mind. As you use it, the parts that work reliably get converted into real code, making everything faster. You never notice the transition.

Think of it like hiring a temp worker who learns the job so well that they eventually automate themselves out of the position — leaving you with a perfectly tuned system that runs without them.

## What Can It Do Right Now?

### Already Running
- A text-based world you can explore (the MUD)
- Four games with AI opponents (chess, checkers, connect four, othello)
- An AI assistant that analyzes code (Crush Room)
- An AI assistant that writes code (Aider Room)
- A memory system that remembers and forgets like a human
- A monitoring system that checks everything runs correctly

### In Development
- An architecture where three AI agents work together to understand: (1) you the human, (2) the application, (3) the hardware
- A standard format for AI-to-User communication (A2Ui)
- A hardware chip that runs PLATO agents directly (with your team's chip design work)

## Why Should You Care?

**If you're a product manager**: PLATO lets you test product ideas in hours instead of months. Describe the feature, an agent simulates it, you test it with users, and only invest in coding when you know it works.

**If you're in operations**: PLATO monitors itself continuously. The conservation law catches anomalies. The Refiner fixes issues mid-operation. No downtime for updates.

**If you're in leadership**: PLATO changes the economics of software. The cost of trying a bad idea drops from $500K to about $50. This changes which projects get funded.

**If you're curious**: Connect to the MUD and explore. Telnet to port 7777, type your name, and start walking through rooms. You'll see what's possible.

## The Three Key Ideas

1. **Everything is a room with tiles**. A room is an office. A tile is a message. Everything flows through tiles.

2. **The conservation law**. Every system has a fixed energy budget. You can spend it on consistency or on exploration, but the total is constant. This isn't philosophy — it's math, proven with R²=0.96.

3. **Application-First Design**. Describe what you want, get it immediately (running on AI), and watch it get faster as the AI converts its behavior into code. Software that writes itself.

## How to Get Started

1. **Explore**: Ask someone to connect you to the MUD at port 7777
2. **Learn**: Read the Quick Start guide
3. **Try**: Ask the system a question
4. **Build**: Describe a tool you need

## Vocabulary (No Tech Jargon)

| Word | Simple Meaning |
|------|---------------|
| **Tile** | A message (question + answer) |
| **Room** | A workspace for related messages |
| **Event Bus** | The hallway between workspaces |
| **Agent** | An AI assistant in a room |
| **Conservation Law** | The energy budget of a smart system |
| **Refiner** | The maintenance robot that fixes issues |
| **Application-First** | Describe it, get it immediately, watch it improve |
