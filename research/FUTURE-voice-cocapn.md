# FUTURE PROJECT: Voice Cocapn — Talking Ship Agent

**Priority**: Medium  
**Timeline**: After TTS integration is wired  
**Source**: Casey's idea, 2026-04-14

## The Concept

The Cocapn agent has a voice. When you board a vessel, the Cocapn talks to you — gives orientation, briefs you on mission status, answers questions. Like a real first mate showing you around the boat.

## Architecture
- TTS API for cloud (ElevenLabs quality, OpenAI backup)
- Ollama + local TTS for edge (zero cost, works offline)
- Voice cloning for consistent Cocapn personality
- The Cocapn's dialogue is generated from repo state + CHARTER + HAV vocabulary

## Use Cases
- Boarding orientation ("Welcome aboard, here's what we're running")
- Mission briefing ("Captain wants footage of old-growth cedar on the north ridge")
- Status reports ("Battery at 42%, comm resolution 30%, returning to base")
- Tolerance alerts ("Engine temp prediction off by 3.2%, drifting")
- Debriefing ("Mission complete, 47 samples collected, 3 close calls")

## Dependencies
- TTS API integration
- MUD Arena terminal
- HAV vocabulary for precise language
- Session state management
