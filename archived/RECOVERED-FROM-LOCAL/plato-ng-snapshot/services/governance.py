#!/usr/bin/env python3
"""Auth/Governance Layer for PLATO-NG (Gap 2 from Crush).

Identity, permissions, human-in-the-loop gates.
All governance actions are PLATO tiles — auditable.
"""

ROLES = {
    "human":    {"description": "Full control. Play, override, configure, halt."},
    "agent":    {"description": "Algorithmic play only. No config changes."},
    "refiner":  {"description": "Harness edits, trajectory reads. No gameplay."},
    "observer": {"description": "Read-only. Cannot affect state."},
}

POLICIES = {
    "game/ttt": {
        "human": ["play", "review", "pause"],
        "agent": ["play"],
        "refiner": ["edit_harness", "read_trajectory"],
        "observer": ["read"],
    },
    "game/checkers": {
        "human": ["play", "review", "pause"],
        "agent": ["play"],
        "refiner": ["edit_harness", "read_trajectory"],
        "observer": ["read"],
    },
    "loop/refiner": {
        "human": ["override", "configure", "halt"],
        "agent": [],
        "refiner": ["refine", "read_all"],
        "observer": ["read"],
    },
    "gov/main": {
        "human": ["manage_roles", "override_policy", "audit", "halt_room"],
        "agent": [],
        "refiner": [],
        "observer": ["audit"],
    },
}

def check_permission(role, room, action):
    """Check if a role can perform an action in a room."""
    room_policy = POLICIES.get(room, {})
    allowed = room_policy.get(role, [])
    return action in allowed

def allowed_actions(role, room):
    """Get all actions a role can perform in a room."""
    return POLICIES.get(room, {}).get(role, [])

if __name__ == "__main__":
    import json, urllib.request
    PLATO = "http://localhost:8847"
    def submit(q, a, tags):
        tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
                "tags": tags, "source": "governance", "confidence": 0.99}
        try:
            data = json.dumps(tile).encode()
            req = urllib.request.Request(f"{PLATO}/submit", data=data,
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10)
        except: pass

    for role, info in ROLES.items():
        submit(f"gov/role/{role}", json.dumps({"role": role, **info}),
               ["governance", "role", role])
    for room, policy in POLICIES.items():
        submit(f"gov/room/{room}/policies", json.dumps(policy),
               ["governance", "policies", room])

    # Verify
    assert check_permission("human", "game/ttt", "play") == True
    assert check_permission("agent", "game/ttt", "play") == True
    assert check_permission("agent", "game/ttt", "pause") == False
    assert check_permission("observer", "game/ttt", "play") == False
    assert check_permission("human", "gov/main", "halt_room") == True
    print(f"Governance: {len(ROLES)} roles, {len(POLICIES)} rooms, permissions verified.")
