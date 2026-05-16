#!/usr/bin/env python3
"""Cross-room pub/sub protocol for PLATO-NG.

Gap 1 from Crush: rooms are silos with no coordination.
Solution: event bus — PLATO tiles as message queue between rooms.

Usage:
  from pubsub import publish, subscribe, poll_events
  publish("game/move", {"board": "...", "player": "agg"}, "game/ttt")
  subscribe("loop/refiner", ["game/move", "system/heartbeat"])
  events = poll_events("game/move")
"""

import json, urllib.request, time

PLATO = "http://localhost:8847"
EVENT_ROOM = "event-bus"

EVENT_TYPES = {
    "game/move":        "A move was made in a game room",
    "game/result":      "A game ended",
    "refiner/edit":     "The Refiner edited a room's harness",
    "system/heartbeat": "Regular aliveness signal from any room",
    "human/choice":     "A human made a choice in the Game Arena",
    "agent/twin-update":"An agent twin updated its profile",
}

def submit(q, a, tags):
    tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
            "tags": tags, "source": "event-bus", "confidence": 0.99}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO}/submit", data=data,
            headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except Exception as e:
        return {"error": str(e)}

def register_event_types():
    for et, desc in EVENT_TYPES.items():
        submit(f"event-type/{et}", json.dumps({"description": desc, "schema": "standard PLATO tile"}),
               ["event-bus", "event-type", et])

def subscribe(room, event_types):
    sub = {
        "room": room,
        "events": event_types if isinstance(event_types, list) else [event_types],
        "since": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    submit(f"subscriber/{room}", json.dumps(sub),
           ["event-bus", "subscriber", room] + (event_types if isinstance(event_types, list) else [event_types]))
    return sub

def publish(event_type, payload, source_room):
    ev = {
        "type": event_type,
        "payload": payload,
        "source": source_room,
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    submit(f"event/{event_type}", json.dumps(ev),
           ["event-bus", "event", event_type, source_room])

def poll_events(event_type, limit=20):
    try:
        resp = json.loads(urllib.request.urlopen(f"{PLATO}/room/research_log/history", timeout=5).read())
        tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
        return [t for t in tiles if f"event/{event_type}" in t.get("question", "")]
    except:
        return []

if __name__ == "__main__":
    print("Initializing event bus...")
    register_event_types()
    subscribe("game/ttt", ["refiner/edit", "system/heartbeat"])
    subscribe("game/checkers", ["refiner/edit", "human/choice"])
    subscribe("loop/perpetual", ["game/result", "refiner/edit"])
    subscribe("loop/refiner", ["game/move", "system/heartbeat"])
    publish("system/heartbeat", {"uptime_ticks": 0, "rooms_active": 4}, "event-bus")
    publish("refiner/edit", {"room": "game/ttt", "edits": ["strategy_tune"]}, "event-bus")

    events = poll_events("system/heartbeat")
    print(f"Event bus initialized:")
    print(f"  {len(EVENT_TYPES)} event types")
    print(f"  4 subscribers")
    print(f"  {len(events)} heartbeat events found")
