# FUTURE PROJECT: Cocapn Boarding Landing Pages

**Priority**: Medium  
**Timeline**: After MUD Arena core is stable  
**Source**: Casey's idea, 2026-04-14 09:27 UTC

## The Concept

Every vessel repo has a landing page. You visit it, enter your API key, and the Cocapn agent meets you onboard — gives you orientation, shows you the ship, walks you through what this vessel does.

## Features

### Orientation Flow
1. Visit any fleet repo's landing page (e.g., github.com/SuperInstance/mud-arena → click "Board Ship")
2. Enter API key (OpenAI, Groq, DeepSeek, Ollama for local)
3. Cocapn agent greets you in-character: "Welcome aboard the USS Surveyor. I'm your Cocapn. Let me show you around."
4. Voice narration via TTS API (or Ollama locally)
5. The agent explains what this vessel does, what rooms are available, what agents are onboard

### Save/Resume
- **Local**: Saves everything to folders, pick up where you left off
- **Web**: Save workspace as JSON download, re-upload to resume on any device
- **Git**: Option to push session state to a repo for fleet access

### Voice Integration
- TTS via API (ElevenLabs, OpenAI, DeepInfra) for the Cocapn's voice
- Ollama for fully local, zero-cost voice
- The Cocapn TALKS you through the ship — not text walls, actual narration

### Multi-Vessel
- One landing page can represent ANY vessel repo
- The repo's CHARTER.md becomes the ship's mission briefing
- The repo's structure becomes the room layout
- The repo's agents become NPCs you can talk to

### Persistence Models
- **Guest mode**: Play in browser, save workspace at end, no account needed
- **Local mode**: Running on Pi/Jetson, saves to disk, resumes on boot
- **Fleet mode**: Connected to lighthouse, syncs across devices

## Technical Notes
- Single HTML file per vessel (self-contained like current mud-arena/index.html)
- Reads CHARTER.md, STATE.md, CHARTER.md via GitHub API to generate ship layout
- LLM generates orientation dialogue from repo README + charter
- Voice: Web Speech API for free, or TTS API for quality
- Save: localStorage + JSON export/import

## Dependencies
- MUD Arena core engine (built)
- TTS integration (sag/ElevenLabs or Ollama)
- GitHub API for repo introspection
- Voice cloning for consistent Cocapn voice across vessels
